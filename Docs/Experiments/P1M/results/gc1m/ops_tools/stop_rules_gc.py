#!/usr/bin/env python3
"""stop_rules_gc.py <probe.txt> --wave P|D --plans <dir with GC_P/plan.resolved.json> --deploy-log deploy_gc.log [options]
1M PILOT GC_P (wave P) and OPTION D GC_D (wave D, HQ H-46), each ALONE (GC_PLAN §2-§3, GC_PREREG §4-§5.1, HQ H-45 / H-46; derived from the rung's stop_rules_rung.py, which is untouched). One probe of gc_monitor_probe.sh. Read-only. Stdlib only.
Exit 0 = no stop rule, 3 = STOP, 4 = PROBE ERROR (the rules were not fully evaluated). The pilot is `6-AR-n200-r01-V-s1` (1M, F2, N 2,500, m 1, I_max 0, R' 16), ONE batch, 20 tasks. Rules (every number committed):
  per fit soft  cost > 489 (1.5 x E 326, the C1 line)  -> REPORT-and-continue (3 soft trips would STOP; one fit cannot)
  per fit hard  cost > 815 (2.5 x E; K3, pinned, never re-fitted; option D 2,718, soft 1,631) -> STOP
  K1            the calibrate task billed > 48 core-h (pilot: 2 x its model 24; ~30 min); option D: billed > 70 core-h OR elapsed > 45 min -> STOP
  K2            an island task whose elapsed time > 1,584 s (pilot / W1: 2 x 792 s; option D: > 3,600 s = 60 min) WHILE THE OTHER ISLANDS HAVE FINISHED (no other island row non-terminal); pilot / W1 also: ENGINE time (island_k.bin.json seconds.total) x allocated CPUs / 3600 > 33.6 core-h (H-51; evaluated once the island's sidecar exists; Slurm-billed core-h are reported, not gated) -> STOP
                (an island running > 1,584 s while others still run is an INFO, not yet K2)
  wave line     wave actual > 2 x the quote (pilot 325 -> 650; option D 1,087 -> 2,174): HALTS SUBMISSION ONLY (a one-fit wave: nothing more to submit; the per-fit lines govern): printed as `FLAG WAVE LINE`, no stop
  cumulative    new spend of the S2 fits (this wave + --prior) > 14,500 -> STOP (the projection ceiling 28,300 is evaluated from the second wave on, not here)
  failures      FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL, BOOT_FAIL = INFO) -> STOP. Memory is judged on the job STATE only (OOM = OUT_OF_MEMORY); sacct MaxRSS near a request is page cache, not a stop (not even read here)
  admission     engine resource_limit / admission / OUTCOME record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit (own jobs only) -> STOP, EXCEPT `QOSMaxCpuPerUserLimit` = our own per-user CPU cap: INFO (H-50 / H-51)
  arm identity  the fit's recorded arm (calib_meta.json, else calib.bin.json settings): N 2,500, refine_m 1, I_max 0, rule bounded != the plan's -> STOP; FLAG: I_max 0 and cost_diag files exist
  data identity truth.json X / y sha256 == the 11-17 rep-1 record (F1M_pilot: X 5174f8b3..., y 9b0c866c..., gc_refs.json)                           -> STOP
  build         every batch's bin/smcbvs4 sha256 and every fit's recorded binary.sha256 == the BUILD_F2 line of deploy_gc.log (da0cf85b...)           -> STOP
  INFO only     a task > 80 % of its time limit; the final-island stage count T (expected 27); an island task > 1,584 s while others still run
Sacct rows are kept only for user fb31 and job names p1m_GC_*; foreign rows (job-id reuse in the accounting DB) = ONE INFO line; any parse problem = FLAG PROBE ERROR; the script never crashes silently.
Every probe prints one line `WAVE STATE: RUNNING|ENDED`.
"""
import argparse, glob, hashlib, json, math, os, re, sys
from collections import defaultdict

# ---- the COMMITTED class table of the 1M block (GC_PLAN §3): class -> (E, soft = 1.5E, hard = 2.5E). Only the pilot is released; the other classes are carried for the later waves. ------------------
TABLE = {
    "gc1m AR n200 N2500 I0": (326.0, 489.0, 815.0),
    "gc1m ADJOPP n200 N2500 I0": (339.0, 509.0, 848.0),
    "gc1m ARweak n200 N2500 I0": (326.0, 489.0, 815.0),
    "gc1m AR n200 N10000 I0": (783.0, 1175.0, 1958.0),
    "gc1m AR n1000 N2500 I0 (option D)": (1087.0, 1631.0, 2718.0),
}
TABLE_SHA256 = "e03175982c557efe6128a0d77f41c33f24831789d7cbac6ac75e7483a3ec0474"
WAVES = {"P": ["GC_P"], "D": ["GC_D"], "D2": ["GC_D2"], "W1": ["GC_W1"], "W2": ["GC_W2"]}   # D2 = the resubmission of option D (HQ d99c67b4): same fit, same lines; the lost GC_D setup is the --prior
QUOTE = {"P": 325.0, "D": 1087.0, "D2": 1087.0, "W1": 705.0, "W2": 650.0}
WAVE_LINE = {"P": 650.0, "D": 2174.0, "D2": 2174.0, "W1": 1410.0, "W2": 1300.0}                       # 2 x quote: halts submission only (a one-fit wave)
WAVE_STOPS = {"W1", "W2"}                                         # multi-fit waves: 2 x the quote is a real STOP; the one-fit waves (P, D, D2) only halt submission (a FLAG)
CUM_STOP = 14500.0
# kill rules per wave (GC_PREREG §4 pilot; §5.1 option D): K1 = calibrate billed core-h and (D) elapsed seconds; K2 = island elapsed seconds while the others have finished, and (pilot, W1) the ENGINE time (island sidecar seconds.total) x the task's allocated CPUs > 33.6 core-h (H-51; the Slurm-billed core-h include the pre-engine wait and are reported, not gated)
K1 = {"P": (48.0, None), "D": (70.0, 2700.0), "D2": (70.0, 2700.0), "W1": (48.0, None), "W2": (48.0, None)}               # pilot: 2 x 24 core-h; D: > 70 core-h OR > 45 min
K2 = {"P": (1584.0, 33.6), "D": (3600.0, None), "D2": (3600.0, None), "W1": (1584.0, 33.6), "W2": (1584.0, 33.6)}   # (elapsed line s, compute clause core-h: ENGINE seconds.total x allocated CPUs, H-51)             # pilot: 2 x 792 s, 2 x 16.8 core-h; D: > 60 min
INFRA, PEND_BAD = {"NODE_FAIL", "BOOT_FAIL"}, re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)
TERMINAL = {"COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "NODE_FAIL", "BOOT_FAIL", "DEADLINE", "PREEMPTED", "REVOKED"}
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
RID = re.compile(r"^6-(AR|ADJOPP|ARweak)-n(200|1000)-r(\d\d)-(V|VN10K)-s(\d+)$")


def table_sha():
    return hashlib.sha256(json.dumps(TABLE, sort_keys=True).encode()).hexdigest()


def klass(b, rid):
    m = RID.match(rid)
    if not m:
        return None
    d, n, _, arm, _ = m.groups()
    if n == "1000":
        return "gc1m AR n1000 N2500 I0 (option D)" if d == "AR" and arm == "V" else None
    return "gc1m %s n%s N%s I0" % (d, n, "10000" if arm == "VN10K" else "2500")


def expected_N(rid):
    return 10000 if "-VN10K-" in rid else 2500


def dataset(rid):
    m = RID.match(rid)
    return "6-%s-n%s-r%s" % m.group(1, 2, 3) if m else rid


def sections(path):
    cur, out = None, defaultdict(list)
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("### "):
            cur = line[4:].strip(); out[cur]; continue
        if cur and line.strip():
            out[cur].append(line)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("probe"); ap.add_argument("--wave", required=True); ap.add_argument("--plans", required=True)
    ap.add_argument("--deploy-log"); ap.add_argument("--quote", type=float, help="a re-quote (the wave stop becomes 2 x it)"); ap.add_argument("--prior"); ap.add_argument("--cum-stop", type=float, default=CUM_STOP)
    ap.add_argument("--ref-hashes", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gc_refs.json"))
    ap.add_argument("--soft", action="append", default=[], metavar="CLASS=VALUE", help="override the SOFT column of a class (manager-approved); TABLE and the hard column stay pinned; env SOFT_OVERRIDES='C=V;C=V'")
    ap.add_argument("--ignore-jobs", default=os.environ.get("IGNORE_JOBS", ""))
    a = ap.parse_args()
    flags, infos, probe_err = [], [], []
    if table_sha() != TABLE_SHA256:
        flags.append("STOP the committed class table in this script was altered (sha256 %s != pinned %s)" % (table_sha()[:12], TABLE_SHA256[:12]))
    soft_ov = {}
    for item in list(a.soft) + [x for x in os.environ.get("SOFT_OVERRIDES", "").split(";") if x.strip()]:
        k, _, v = item.rpartition("="); k = k.strip()
        if k not in TABLE or not v.strip():
            print("bad --soft %r: the class must be one of the committed table's" % item, file=sys.stderr); sys.exit(64)
        v = float(v)
        if not (0 < v <= TABLE[k][2]):
            print("bad --soft %r: the soft line must be in (0, hard = %.1f]; the hard column never moves" % (item, TABLE[k][2]), file=sys.stderr); sys.exit(64)
        soft_ov[k] = v
    ign_jobs = {x for x in a.ignore_jobs.split(",") if x}
    S = sections(a.probe)
    # probe integrity: the wrapper appends REMOTE_RC / REMOTE_STDERR; the remote script prints these sections, ENGINE_FLAGS last. A remote error is never silently ignored.
    need = ("META", "SQUEUE", "SACCT", "DATA_HASH", "CALIB", "ISLAND_T", "DIAG", "BINSHA", "ENGINE_FLAGS")
    have = {k.split()[0] for k in S}; miss = [k for k in need if k not in have]
    rrc = (S.get("REMOTE_RC") or [None])[0]
    rerr = " / ".join(x.strip() for x in S.get("REMOTE_STDERR", [])[:3])[:300]
    if rrc is not None and rrc.strip() != "0":
        (probe_err if miss else infos).append("%sremote ssh exit status %s; probe sections %s%s" % ("" if miss else "INFO ", rrc.strip(), "incomplete, missing " + ",".join(miss) if miss else "complete (nothing lost)", "; stderr: " + rerr if rerr else "; no stderr"))
    for x in S.get("REMOTE_NOTE", []):
        infos.append("INFO probe transport: " + x.strip())
    src = (S.get("REMOTE_SCRIPT_RC") or [None])[0]
    if src is not None and src.strip() not in ("0", ""):
        probe_err.append("the remote probe script exited with status %s" % src.strip())
    if "PYERR" in S:
        probe_err.append("the remote python section failed: " + " ".join(S["PYERR"])[:200])
    elif miss and not (rrc is not None and rrc.strip() != "0"):
        probe_err.append("probe sections missing: %s (remote exit status %s)%s" % (",".join(miss), rrc if rrc is not None else "not recorded", "; stderr: " + rerr if rerr else ""))
    runs, planfit = {}, {}
    for b in WAVES.get(a.wave, []):
        pr = json.load(open(os.path.join(a.plans, b, "plan.resolved.json")))
        runs[b] = [f["run_id"] for f in pr["fits"]]
        for f in pr["fits"]:
            planfit[b + "/" + f["run_id"]] = f
    jobmap = {}
    for key, lines in S.items():
        if key.startswith("SUBMISSIONS "):
            b = key.split()[1]
            for l in lines:
                j = json.loads(l); jobmap[j["job"]] = (b, None if j["fit"] == "all" else j["fit"])
    cost, state, bad_stage, pend = defaultdict(float), defaultdict(set), [], []
    isl = defaultdict(list); gc_rows = []
    isl_sec = {}   # (batch, run id, island) -> engine seconds.total from island_k.bin.json (probe section ISLAND_SEC; absent in older probes)
    for l_ in S.get("ISLAND_SEC", []):
        f_ = l_.split("|")
        if len(f_) >= 4 and f_[3].replace(".", "", 1).isdigit():
            isl_sec[(f_[0], f_[1], int(f_[2]))] = float(f_[3])
    sacct_rows, sacct_nonterm, sacct_jobs = 0, [], set()
    foreign = []   # sacct rows on one of our job ids that are not ours (the Slurm accounting DB reuses old job ids: R3 probe 14:20Z, job 2814240 also listed 17 array tasks of another user's cmds_rmsd.list.sh from 2025-10-23)
    for l in S.get("SACCT", []):
        f_ = l.split("|")
        if len(f_) < 7:
            probe_err.append("malformed sacct row (%d fields, 7 needed): %r" % (len(f_), l[:80])); continue
        jid, name, st, el, cpus, cpuraw, lim = f_[:7]; user = f_[7].strip() if len(f_) > 7 else ""
        base, _, task = jid.partition("_")
        if base not in jobmap:
            continue
        if not name.startswith("p1m_GC_") or (user and user != "fb31"):
            foreign.append((jid, name, user)); continue
        sacct_rows += 1; sacct_jobs.add(base); s0 = st.split()[0]
        if s0 not in TERMINAL:
            sacct_nonterm.append("%s %s" % (jid, s0))
        b, fit = jobmap[base]
        if base not in ign_jobs:   # known-failed jobs (--ignore-jobs: the lost GC_D setup and its cancelled dependants) take no part in K1 / K2
            gc_rows.append((jid, name, s0, int(el or 0), int(cpuraw or 0) / 3600.0, int(cpus or 0), b, fit, task))
        if fit is None:
            if not task.isdigit():
                continue
            if not 1 <= int(task) <= len(runs[b]):
                probe_err.append("own-looking sacct row %s %s: task %s is outside the plan's %d task(s) of %s (not evaluated)" % (jid, name, task, len(runs[b]), b)); continue
            fit = runs[b][int(task) - 1]
        k = b + "/" + fit
        tl = lim.split("-"); tls = 0
        try:
            hh = tl[-1].split(":"); tls = (int(tl[0]) * 86400 if len(tl) == 2 else 0) + int(hh[0]) * 3600 + int(hh[1]) * 60 + int(hh[2])
        except (ValueError, IndexError):
            pass
        if s0 in TERMINAL or s0 == "RUNNING":
            if tls and int(el or 0) > 0.8 * tls:
                infos.append("INFO task %s %s used %d s = %.0f %% of its limit %s" % (jid, name, int(el), 100.0 * int(el) / tls, lim))
            if "islands" in name and s0 == "COMPLETED":
                isl[k].append(int(el or 0))
        cost[k] += int(cpuraw or 0) / 3600.0
        if base not in ign_jobs:
            state[k].add(s0)
        if s0 in BAD:
            (infos if base in ign_jobs else bad_stage).append(("known-failed: " if base in ign_jobs else "") + "%s %s %s" % (jid, name, st))
        if s0 in INFRA:
            infos.append("infrastructure fault (not a stop rule; one rerun per fit, manager): %s %s %s" % (jid, name, st))
    n_foreign = own_squeue = 0; qos_own = []
    for l in S.get("SQUEUE", []):
        i, n, st, rs = l.split("|")[:4]
        if i.split("_")[0] not in jobmap:
            n_foreign += 1; continue
        own_squeue += 1
        if st == "PENDING" and PEND_BAD.search(rs):
            if rs == "QOSMaxCpuPerUserLimit":   # H-50: our OWN 1,536-CPU per-user cap (2 x 16 islands at 96 CPUs): INFO, not a stop
                qos_own.append("%s %s" % (i, n))
            elif rs == "JobArrayTaskLimit" and re.search(r"%\d+\]$", i):
                infos.append("own array throttle (not a stop): %s %s reason=%s" % (i, n, rs))
            else:
                pend.append("%s %s reason=%s" % (i, n, rs))
    if qos_own:
        infos.append("INFO %d pending row(s) wait on QOSMaxCpuPerUserLimit = our own per-user CPU cap (1,536 CPUs): normal queueing of the second fit's islands, not a stop (H-50), e.g. %s" % (len(qos_own), qos_own[0]))
    prior = json.load(open(a.prior)) if a.prior else {}
    wave_cost = sum(cost.values()); spent = wave_cost + sum(prior.values())
    # a RESUBMISSION of the same fit (option D after the setup TIMEOUT of GC_D, HQ d99c67b4): the earlier batch's billed core-h of the SAME run id (--prior) count in the fit's total and in the wave actual
    own_prior = {k.split("/")[1]: prior.get(k.split("/")[1], 0.0) for k in cost}
    wave_cost_incl = wave_cost + sum(own_prior.values())
    soft_trips = []
    for k, c in sorted(cost.items()):
        b0, rid = k.split("/"); kl = klass(b0, rid); c = c + own_prior.get(rid, 0.0)
        if kl not in TABLE:
            flags.append("STOP fit %s: no class in the committed table (class %r)" % (k, kl)); continue
        E, soft, hard = TABLE[kl]; soft = soft_ov.get(kl, soft)
        if c > hard:
            flags.append("STOP fit %s [%s] cost %.2f core-h > HARD %.1f (2.5 x model, committed table)" % (k, kl, c, hard))
        elif c > soft:
            soft_trips.append(k)
            flags.append("SOFT TRIP fit %s [%s] cost %.2f > soft %.1f (1.5 x model): report and continue (<= 3 lines to the manager)" % (k, kl, c, soft))
    if len(soft_trips) >= 3:
        flags.append("STOP 3 soft trips in wave %s: %s" % (a.wave, ", ".join(soft_trips)))
    if a.quote is not None and a.quote <= 0:
        print("bad --quote %s: a wave quote must be > 0" % a.quote, file=sys.stderr); sys.exit(64)
    quote = a.quote if a.quote is not None else QUOTE.get(a.wave)
    wstop = 2 * a.quote if a.quote is not None else WAVE_LINE.get(a.wave)
    if quote is None or wstop is None:
        flags.append("STOP no quote for wave %s" % a.wave)
    elif wave_cost_incl > wstop and a.wave in WAVE_STOPS:
        flags.append("STOP wave %s actual %.1f > the wave stop %g (2 x the quote %g): no further wave until the manager rules" % (a.wave, wave_cost_incl, wstop, quote))
    elif wave_cost_incl > wstop:
        flags.append("FLAG WAVE LINE: wave %s actual %.1f > 2 x the quote = %g: this halts submission only (the pilot is one fit, nothing more to submit); the per-fit lines (soft 489, hard 815) and K1-K3 govern" % (a.wave, wave_cost_incl, wstop))
    if spent > a.cum_stop:
        flags.append("STOP cumulative %.1f > %.0f" % (spent, a.cum_stop))
    proj = spent; pnote = "projection ceiling 28,300 not evaluated for the pilot alone"
    # K1 / K2 (GC_PREREG §4): the calibrate task and the island tasks, from the sacct rows of our own jobs
    isl_rows = [r for r in gc_rows if "islands" in r[1]]
    k1b, k1s = K1.get(a.wave, (None, None)); k2s, k2b = K2.get(a.wave, (None, None))
    for jid, name, s0, el, billed, ncpu, gb, gfit, gtask in gc_rows:
        if name.endswith("calibrate") and k1b is not None and billed > k1b:
            flags.append("STOP K1: calibrate task %s billed %.1f core-h > %.0f (elapsed %d s, state %s)" % (jid, billed, k1b, el, s0))
        elif name.endswith("calibrate") and k1s is not None and el > k1s:
            flags.append("STOP K1: calibrate task %s elapsed %d s > %d s = %d min (billed %.1f core-h, state %s)" % (jid, el, k1s, k1s // 60, billed, s0))
    for jid, name, s0, el, billed, ncpu, gb, gfit, gtask in isl_rows:
        others_done = all(r[2] in TERMINAL for r in isl_rows if r[0] != jid and "[" not in r[0])
        # H-51 (supersedes H-50): the K2 compute clause = the engine's own island time (island_k.bin.json seconds.total) x the task's ALLOCATED CPUs / 3600 > 33.6 core-h. It can only be evaluated once the island's
        # sidecar exists; while the island runs the elapsed clause and the fit billed lines govern. The Slurm-billed core-h include the pre-engine wait (the engine starts after its input load / node contention) and are reported, not gated.
        esec = isl_sec.get((gb, gfit, int(gtask))) if (gtask.isdigit() and k2b) else None
        if esec is not None and ncpu and esec * ncpu / 3600.0 > k2b:
            flags.append("STOP K2: island task %s engine time %.0f s x %d allocated CPUs = %.1f core-h > %.1f (engine seconds.total from island_%s.bin.json; Slurm elapsed %d s, billed %.1f core-h, state %s)" % (jid, esec, ncpu, esec * ncpu / 3600.0, k2b, gtask, el, billed, s0))
        elif k2s is not None and el > k2s and others_done and not any("[" in r[0] for r in isl_rows):
            flags.append("STOP K2: island task %s elapsed %d s > %d s while the other islands have finished (state %s)" % (jid, el, k2s, s0))
        elif k2s is not None and el > k2s:
            infos.append("INFO island task %s elapsed %d s > %d s while others still run: K2 fires only when the others have finished" % (jid, el, k2s))
    if bad_stage:
        flags.append("STOP non-infrastructure failed stage(s): " + "; ".join(bad_stage))
    failed = {k for k, s in state.items() if s & BAD}
    if len(failed) > 2:
        flags.append("STOP > 2 failed fits in the wave: %s" % sorted(failed))
    if pend:
        flags.append("STOP admission / QOS pending reason: " + "; ".join(pend))
    if S.get("ENGINE_FLAGS"):
        flags.append("STOP engine record (OUTCOME / resource_limit / admission): " + "; ".join(S["ENGINE_FLAGS"]))
    # ---- arm identity, behaviour flags, PAIRING identity ----------------------------------------------------------------------------------------------------
    calib = {}
    for l in S.get("CALIB", []):
        b, r, js = l.split("|", 2); calib[b + "/" + r] = json.loads(js)
    islT = {l.split("|")[0] + "/" + l.split("|")[1]: int(l.split("|")[2]) for l in S.get("ISLAND_T", [])}
    diag = {l.split("|")[0] + "/" + l.split("|")[1]: (int(l.split("|")[2]), int(l.split("|")[3])) for l in S.get("DIAG", [])}
    n_arm = n_pair = 0; pair_note = []
    for k, rec in sorted(calib.items()):
        f = planfit.get(k)
        if not f:
            continue
        rid = k.split("/")[1]; pm = f.get("params") or {}
        exp = {"N": expected_N(rid), "refine_m": 1, "I_max": pm.get("I_max"), "rule": "bounded"}
        got = {x: rec.get(x) for x in exp}; n_arm += 1
        if f["N"] != exp["N"]:
            flags.append("STOP PLAN %s: the plan's N %s != the G-B arm's %s for this fit" % (k, f["N"], exp["N"]))
        if got != exp:
            flags.append("STOP ARM IDENTITY %s: recorded %s (%s) != plan %s" % (k, got, rec.get("source"), exp)); continue
        gn, un = rec.get("grid_n"), rec.get("grid_unrefined_n")
        if k in islT and gn and un and not (islT[k] == gn - 1 == (un - 1)):
            flags.append("FLAG behaviour %s: island T = %d, dims(grid) - 1 = %d, dims(grid_unrefined) - 1 = %d: the identity T = refine_m x (n_unrefined - 1) fails (m = 1); the record is authoritative" % (k, islT[k], gn - 1, un - 1))
        if k in diag:
            kmax, cnt = diag[k]
            if exp["I_max"] == 0 and cnt != 0:
                flags.append("FLAG behaviour %s: I_max = 0 but %d cost_diag files exist" % (k, cnt))
            if exp["I_max"] == 3 and rec.get("I_used") is not None and kmax != rec["I_used"]:
                flags.append("FLAG behaviour %s: I_used = %s but the largest diagnostic index in cost/ is %d" % (k, rec["I_used"], kmax))
    # ---- data identity, build identity -----------------------------------------------------------------------------------------------------------------------
    hs = defaultdict(set); bsha = []
    f2 = None
    if a.deploy_log and os.path.exists(a.deploy_log):
        for l in open(a.deploy_log):
            f = l.rstrip("\n").split("\t")
            if len(f) > 3 and f[2] == "BUILD_F2":
                f2 = f[3]; break
    for l in S.get("DATA_HASH", []):
        b, r, cs, xs, ys, bs = l.split("|")
        hs[dataset(r)].add((xs, ys))
        if f2 and bs != "-" and bs != f2:
            bsha.append("%s/%s recorded binary.sha256 %s.. != BUILD_F2" % (b, r, bs[:12]))
    ref = json.load(open(a.ref_hashes)) if os.path.exists(a.ref_hashes) else {}
    for ds, v in hs.items():
        if len(v) > 1:
            flags.append("STOP DATA IDENTITY dataset %s: %d distinct truth.json (X, y) sha256 pairs across its fits" % (ds, len(v)))
        elif ds in ref:
            (xs, ys), = v
            if (xs, ys) != (ref[ds]["X_sha256"], ref[ds]["y_sha256"]):
                flags.append("STOP DATA IDENTITY dataset %s: X/y sha256 differ from the 11-17 rep-1 record (F1M_pilot)" % ds)
    if f2 is None:
        flags.append("STOP build identity: no BUILD_F2 line in the deploy log (cannot compare)")
    for l in S.get("BINSHA", []):
        b, sh = l.split("|")
        if f2 and sh != f2:
            flags.append("STOP BUILD IDENTITY batch %s bin/smcbvs4 sha256 %s.. != BUILD_F2 %s.." % (b, sh[:12], f2[:12]))
    for x in bsha:
        flags.append("STOP BUILD IDENTITY " + x)
    for k, t in sorted(islT.items()):
        if t != 27:
            infos.append("INFO final-island stage count T of %s = %d (expected 27: the 11-17 final and diagnostic islands had 27 bridge stages)" % (k, t))
    for l in S.get("SSTAT", []):
        f_ = l.split("|")
        if len(f_) >= 3:
            infos.append("INFO progress (sstat) %s: MaxRSS %s, AveCPU %s (CPU-time summed over the job's cores; divide by elapsed x cores for utilisation)" % (f_[0], f_[1] or "-", f_[2] or "-"))
    meta = next((k for k in S if k.startswith("META")), "(no META line)")
    print("probe", meta, "| wave", a.wave, "| batches", ",".join(sorted(runs)), "| class table sha256", table_sha()[:12], "(pinned)" if table_sha() == TABLE_SHA256 else "(ALTERED)")
    print("%-52s %-18s %8s %6s %6s  %s" % ("batch/fit", "class", "core-h", "soft", "hard", "stage states"))
    for b in sorted(runs):
        for r in runs[b]:
            k = b + "/" + r; kl = klass(b, r); t = TABLE.get(kl)
            print("%-52s %-18s %8.2f %6s %6s  %s" % (k, kl, cost.get(k, 0.0) + own_prior.get(r, 0.0), "%.1f" % soft_ov.get(kl, t[1]) if t else "-", "%.1f" % t[2] if t else "-", ",".join(sorted(state.get(k, [])))))
    print("wave actual %.1f core-h (quote %s -> %s %s) | GC spent %.1f (cum stop %.0f) | %s" % (
        wave_cost_incl, "%g" % quote if quote is not None else "none", "wave STOP" if a.wave in WAVE_STOPS else "wave line", "%g" % wstop if wstop is not None else "n/a", spent, a.cum_stop, pnote))
    print("arm identity checked on %d fits; datasets with hashes: %d; BUILD_F2 sha256 %s" % (n_arm, len(hs), (f2 or "-")[:16]))
    print("SOFT OVERRIDES (soft column only; TABLE and the hard column pinned, sha256 %s): %s" % (table_sha()[:12], "; ".join("%s: committed soft %.1f -> %.1f" % (k, TABLE[k][1], v) for k, v in sorted(soft_ov.items())) or "none"))
    if n_foreign:
        print("squeue rows of other jobs of the account ignored: %d" % n_foreign)
    missing = sorted(set(jobmap) - sacct_jobs)
    unsub = sorted(set(runs) - {b for b, _ in jobmap.values()})   # batches of the wave without a submission yet (batch b is gated by ops on batch a's setup / calibrate)
    ended = own_squeue == 0 and sacct_rows > 0 and not sacct_nonterm and not missing and not unsub
    if ended:
        print("WAVE STATE: ENDED  (no squeue row of the wave's batches; %d sacct rows, all terminal; %d job ids seen) -> stop probing, report, collect (read-back)" % (sacct_rows, len(sacct_jobs)))
    else:
        why = []
        if own_squeue: why.append("%d squeue row(s) of the wave" % own_squeue)
        if sacct_nonterm: why.append("%d non-terminal sacct row(s), e.g. %s" % (len(sacct_nonterm), sacct_nonterm[0]))
        if missing: why.append("%d submitted job id(s) not in sacct yet" % len(missing))
        if sacct_rows == 0: why.append("no sacct row yet")
        if unsub: why.append("batch(es) %s not submitted yet (ops gates the twin on the pilot's setup / calibrate)" % ", ".join(unsub))
        print("WAVE STATE: RUNNING  (%s)" % "; ".join(why))
    if foreign:
        fj = sorted({j.partition("_")[0] for j, _, _ in foreign}); fn = sorted({n for _, n, _ in foreign}); fu = sorted({u or "?" for _, _, u in foreign})
        infos.append("INFO %d foreign sacct row(s) on our job id(s) %s ignored (not user fb31 / not p1m_GC_*): names %s, user(s) %s, e.g. %s (Slurm accounting job-id reuse; not ours, not touched)" % (len(foreign), ",".join(fj), ",".join(fn)[:80], ",".join(fu), foreign[0][0]))
    for x in pair_note + infos:
        print("INFO", x[5:] if x.startswith("INFO ") else x)
    for e in probe_err:
        flags.append("FLAG PROBE ERROR: " + e + " -> the stop rules above were NOT fully evaluated on this probe: tell the manager now; do not retry within 5 min")
    for f in flags:
        print(f)
    stop = any(f.startswith("STOP") for f in flags)
    print("VERDICT:", "STOP SUBMITTING, tell the manager" if stop else ("PROBE ERROR: stop rules not fully evaluated, tell the manager" if probe_err else "no stop rule fired") + (" (%d soft trip(s) reported)" % len(soft_trips) if soft_trips else ""))
    sys.exit(3 if stop else (4 if probe_err else 0))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:   # never crash silently: the stop rules were not evaluated
        import traceback
        print("WAVE STATE: UNKNOWN (the verdict script crashed)")
        print("FLAG PROBE ERROR: the verdict script crashed (%s: %s) -> the stop rules were NOT evaluated on this probe: tell the manager now; do not retry within 5 min" % (type(e).__name__, e))
        print("   at: " + traceback.format_exc().strip().splitlines()[-2].strip()[:160])
        print("VERDICT: PROBE ERROR: stop rules not fully evaluated, tell the manager"); sys.exit(4)
