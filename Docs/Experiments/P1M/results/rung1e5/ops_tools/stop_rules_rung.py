#!/usr/bin/env python3
"""stop_rules_rung.py <probe.txt> --wave R1 --plans <dir with RG_*/plan.resolved.json> --deploy-log deploy_rung.log [options]
10^5 RUNG (RUNG_PLAN §3; derived from the G-B stop_rules_gb.py, which is untouched). One probe of rung_monitor_probe.sh. Read-only. Stdlib only.
Exit 0 = no stop rule, 3 = STOP, 4 = PROBE ERROR (the rules were not fully evaluated). Waves: R1 = RG_1a (AR n400 r01), RG_1b (the 2 continuity twins, N 2,500), RG_T6 (restart test);
R2 = RG_2a (AR n200 r02-r05), RG_2b (AR n400 r02-r03); R3 = RG_3a (IND n200 r01-r02), RG_3b (ADJ-OPP n200 r02). Rules (every number committed in RUNG_PLAN §3):
  per fit soft  cost > soft line of its class in the COMMITTED CLASS TABLE (pinned by TABLE_SHA256) -> REPORT-and-continue; 3 soft trips in the wave -> STOP
  per fit hard  cost > hard line (2.5 x E; pinned, never re-fitted)                                                  -> STOP
  wave          wave actual > 2 x its quote: R1 150 -> 300, R2 460 -> 920, R3 220 -> 440 (--quote Q = a re-quote -> 2Q) -> STOP
  cumulative    new spend of the rung (this wave + --prior) > 1,400; projection (spent + E of the fits not started) > 1,184 = 1,326 - the two G-B pilots' 142.04 -> STOP
  failures      FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL, BOOT_FAIL = INFO); > 2 failed fits -> STOP. A T6 kill is NOT a failure (SIGKILLs by PID inside one job); the T6 JOB failing is.
  admission     engine resource_limit / admission / OUTCOME record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit (own wave's jobs only) -> STOP
  arm identity  the fit's recorded arm (calib_meta.json): N = 10,000 (2,500 for the -VN25- twins), refine_m 1, I_max 0, rule bounded != the plan's -> STOP; FLAG: I_max 0 and cost_diag files exist
  data identity truth.json X / y equal inside a dataset and equal to the G-B pilot's for AR / ADJ-OPP n200 r01 (the twins); -> STOP
  build         every batch's bin/smcbvs4 sha256 and every fit's recorded binary.sha256 == the BUILD_F2 line of deploy_rung.log (da0cf85b...) -> STOP
  INFO only     a task > 80 % of its time limit; an island task > 4 x 447 s = 1,788 s; a twin's calib.bin sections vs its G-B pilot's (expected equal: N-independent calibration)
Every probe prints one line `WAVE STATE: RUNNING|ENDED` (RUNNING while a batch of the wave is not submitted yet; ENDED = no squeue row AND every sacct row terminal AND every submitted job id seen).
"""
import argparse, glob, hashlib, json, math, os, re, sys
from collections import defaultdict

# ---- the COMMITTED class table of the 10^5 rung (RUNG_PLAN §3): class -> (E, soft = max(3, 1.5E), hard = max(3, 2.5E)) -----------------------------------------------------------------
TABLE = {
    "rung AR n200 N10000 I0": (76.0, 114.0, 190.0),
    "rung ADJOPP n200 N10000 I0": (66.0, 99.0, 165.0),
    "rung AR n400 N10000 I0": (76.0, 114.0, 190.0),
    "rung IND n200 N10000 I0": (76.0, 114.0, 190.0),
    "cont AR n200 N2500": (32.0, 48.0, 80.0),
    "cont ADJOPP n200 N2500": (28.0, 42.0, 70.0),
    "T6": (12.0, 18.0, 30.0),
}
TABLE_SHA256 = "723dfaa649c22a5df817c62dfd7a2a1de053be5de1fef895c77ddd70fe911f97"
WAVES = {"R1": ["RG_1a", "RG_1b", "RG_T6"], "R2": ["RG_2a", "RG_2b"], "R3": ["RG_3a", "RG_3b"]}
QUOTE = {"R1": 150.0, "R2": 460.0, "R3": 220.0}
WAVE_STOP = {"R1": 300.0, "R2": 920.0, "R3": 440.0}
CUM_STOP, PROJ_STOP = 1400.0, 1184.0
ISL_WALL_MAX = 1788.0                                       # 4 x 447 s, INFO only
INFRA, PEND_BAD = {"NODE_FAIL", "BOOT_FAIL"}, re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)
TERMINAL = {"COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "NODE_FAIL", "BOOT_FAIL", "DEADLINE", "PREEMPTED", "REVOKED"}
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
RID = re.compile(r"^5-(AR|IND|ADJOPP)-n(200|400)-r(\d\d)-(V|VN25)-s1$")
GBREC = "/home/fb31/SMC_Engineering_Department/records/gb"
PILOT = {"5-AR-n200-r01-VN25-s1": ("GB_G1a", "5-AR-n200-r01-V-s1"), "5-ADJOPP-n200-r01-VN25-s1": ("GB_G2a", "5-ADJOPP-n200-r01-V-s1")}


def table_sha():
    return hashlib.sha256(json.dumps(TABLE, sort_keys=True).encode()).hexdigest()


def klass(b, rid):
    """class of fit rid in batch b (the T6 batch repeats the G-B pilot's run id: its class is T6)"""
    if b == "RG_T6":
        return "T6"
    m = RID.match(rid)
    if not m:
        return None
    d, n, _, arm = m.groups()
    return ("cont %s n%s N2500" % (d, n)) if arm == "VN25" else ("rung %s n%s N10000 I0" % (d, n))


def expected_N(rid):
    return 2500 if rid.endswith("-VN25-s1") else 10000


def dataset(rid):
    m = RID.match(rid)
    return "5-%s-n%s-r%s" % m.group(1, 2, 3) if m else rid


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
    ap.add_argument("--ref-hashes", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rung_refs.json")); ap.add_argument("--gb-records", default=GBREC)
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
    isl = defaultdict(list)
    sacct_rows, sacct_nonterm, sacct_jobs = 0, [], set()
    for l in S.get("SACCT", []):
        jid, name, st, el, cpus, cpuraw, lim = l.split("|")[:7]
        base, _, task = jid.partition("_")
        if base not in jobmap:
            continue
        sacct_rows += 1; sacct_jobs.add(base); s0 = st.split()[0]
        if s0 not in TERMINAL:
            sacct_nonterm.append("%s %s" % (jid, s0))
        b, fit = jobmap[base]
        if fit is None:
            if not task.isdigit():
                continue
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
    n_foreign = own_squeue = 0
    for l in S.get("SQUEUE", []):
        i, n, st, rs = l.split("|")[:4]
        if i.split("_")[0] not in jobmap:
            n_foreign += 1; continue
        own_squeue += 1
        if st == "PENDING" and PEND_BAD.search(rs):
            if rs == "JobArrayTaskLimit" and re.search(r"%\d+\]$", i):
                infos.append("own array throttle (not a stop): %s %s reason=%s" % (i, n, rs))
            else:
                pend.append("%s %s reason=%s" % (i, n, rs))
    prior = json.load(open(a.prior)) if a.prior else {}
    wave_cost = sum(cost.values()); spent = wave_cost + sum(prior.values())
    soft_trips = []
    for k, c in sorted(cost.items()):
        b0, rid = k.split("/"); kl = klass(b0, rid)
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
    wstop = 2 * a.quote if a.quote is not None else WAVE_STOP.get(a.wave)
    if quote is None or wstop is None:
        flags.append("STOP no quote for wave %s" % a.wave)
    elif wave_cost > wstop:
        flags.append("STOP wave %s actual %.1f > the wave stop %g (quote %g)" % (a.wave, wave_cost, wstop, quote))
    if spent > a.cum_stop:
        flags.append("STOP cumulative %.1f > %.0f" % (spent, a.cum_stop))
    # projection: spent + E of every fit of the rung not started (this probe or --prior); scope = every fit of every wave in --plans (the T6 task counts as its own item; prior keys: run id, "T6:<run id>" for T6)
    scope = []
    for wb in WAVES.values():
        for b0 in wb:
            try:
                scope += [(b0, f["run_id"]) for f in json.load(open(os.path.join(a.plans, b0, "plan.resolved.json")))["fits"]]
            except OSError:
                pass
    st_rids = {k.split("/")[1] for k in cost if not k.startswith("RG_T6/")} | {r for r in prior if not r.startswith("T6:")}
    st_t6 = any(k.startswith("RG_T6/") for k in cost) or any(r.startswith("T6:") for r in prior)
    left = [(b0, r) for b0, r in scope if not (st_t6 if b0 == "RG_T6" else r in st_rids)]
    proj = spent + sum(TABLE.get(klass(b0, r), (0.0,))[0] for b0, r in left)
    pnote = "%d fits/tasks not started" % len(left)
    if proj > PROJ_STOP:
        flags.append("STOP projection %.0f > %.0f" % (proj, PROJ_STOP))
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
    for k, rec in sorted(calib.items()):
        rid = k.split("/")[1]
        if rid in PILOT and rec.get("sections"):
            pb, pr = PILOT[rid]; cm = os.path.join(a.gb_records, pb, pr, "calib_meta.json")
            if not os.path.exists(cm):
                pair_note.append("INFO twin %s: the G-B pilot's calib_meta.json (%s) is not there: calib comparison not done" % (rid, cm)); continue
            psec = {x["name"]: x["sha256"] for x in json.load(open(cm)).get("sections", []) if x.get("name") != "meta"}
            n_pair += 1; dif = sorted(z for z in set(psec) | set(rec["sections"]) if psec.get(z) != rec["sections"].get(z))
            pair_note.append("INFO twin %s vs the G-B pilot %s: calib.bin sections %d of %d equal%s (N-independent calibration: expected all equal)" % (rid, pr, len(set(psec) | set(rec["sections"])) - len(dif), len(set(psec) | set(rec["sections"])), "; differing: " + ", ".join(dif[:5]) if dif else ""))
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
                flags.append("STOP DATA IDENTITY dataset %s: X/y sha256 differ from the G-B pilot's" % ds)
    if f2 is None:
        flags.append("STOP build identity: no BUILD_F2 line in the deploy log (cannot compare)")
    for l in S.get("BINSHA", []):
        b, sh = l.split("|")
        if f2 and sh != f2:
            flags.append("STOP BUILD IDENTITY batch %s bin/smcbvs4 sha256 %s.. != BUILD_F2 %s.." % (b, sh[:12], f2[:12]))
    for x in bsha:
        flags.append("STOP BUILD IDENTITY " + x)
    for k, v in sorted(isl.items()):
        if v and max(v) > ISL_WALL_MAX:
            infos.append("INFO island wall %s: %d task(s) done, %d-%d s, above 4 x 447 s = %d s" % (k, len(v), min(v), max(v), ISL_WALL_MAX))
    meta = next((k for k in S if k.startswith("META")), "(no META line)")
    print("probe", meta, "| wave", a.wave, "| batches", ",".join(sorted(runs)), "| class table sha256", table_sha()[:12], "(pinned)" if table_sha() == TABLE_SHA256 else "(ALTERED)")
    print("%-52s %-18s %8s %6s %6s  %s" % ("batch/fit", "class", "core-h", "soft", "hard", "stage states"))
    for b in sorted(runs):
        for r in runs[b]:
            k = b + "/" + r; kl = klass(b, r); t = TABLE.get(kl)
            print("%-52s %-18s %8.2f %6s %6s  %s" % (k, kl, cost.get(k, 0.0), "%.1f" % soft_ov.get(kl, t[1]) if t else "-", "%.1f" % t[2] if t else "-", ",".join(sorted(state.get(k, [])))))
    print("wave actual %.1f core-h (quote %s -> stop > %s) | rung spent %.1f (cum stop %.0f) | projection %.0f (stop > %.0f; %s)" % (
        wave_cost, "%g" % quote if quote is not None else "none", "%g" % wstop if wstop is not None else "n/a", spent, a.cum_stop, proj, PROJ_STOP, pnote))
    print("arm identity checked on %d fits; twin-vs-G-B-pilot calib comparison on %d twins; datasets with hashes: %d; BUILD_F2 sha256 %s" % (n_arm, n_pair, len(hs), (f2 or "-")[:16]))
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
    main()
