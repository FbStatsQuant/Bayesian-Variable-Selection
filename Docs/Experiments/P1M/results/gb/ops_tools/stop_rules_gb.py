#!/usr/bin/env python3
"""stop_rules_gb.py <probe.txt> --wave G1 --plans <dir with GB_<wave>[a-z]/plan.resolved.json> --deploy-log deploy_gb.log [options]
G-B PILOT SET (GB_PLAN §2.3; derived from the V-N mini-leg's stop_rules_vn.py, which is untouched). One probe of gb_monitor_probe.sh. Read-only. Stdlib only.
Exit 0 = no stop rule, 3 = STOP, 4 = PROBE ERROR (the probe itself failed: the rules were not fully evaluated). Rules (every number committed in GB_PLAN §2.3):
  per fit soft  cost > 1.5 x E (soft line of its class in the COMMITTED CLASS TABLE below, pinned by TABLE_SHA256) -> REPORT-and-continue; 3 soft trips in the wave -> STOP
  per fit hard  cost > 2.5 x E (the C1 STOP line; pinned, never re-fitted)                                          -> STOP
  wave          wave actual (all its batches) > the wave stop: G1 450, G2 550 (= 2 x the quotes 226 / 275; --quote Q = a re-quote -> 2Q) -> STOP
  cumulative    G-B actual (this wave + --prior) > 800; projection spent + E of the fits not started > 800          -> STOP
  failures      FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (an OOM is also a C3 finding; NODE_FAIL, BOOT_FAIL = INFO); > 2 failed fits -> STOP
  admission     engine resource_limit / admission / OUTCOME record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit (own wave's jobs only) -> STOP
  arm identity  the fit's recorded arm (calib_meta.json, fallback calib.bin.json settings): N = 10,000, refine_m 1, I_max (the plan's: 0 for -V-, 3 for -VI3-), rule bounded != the plan's -> STOP.
                FLAGS (behaviour, not stops): I_max = 0: no cost_diag files; I_max = 3: largest diag index = I_used; grid identity island T = n_unrefined - 1
  data identity truth.json X / y sha256 EQUAL inside each pair (pilot and twin of a dataset)                         -> STOP
  build         every batch's bin/smcbvs4 sha256 and every fit's recorded binary.sha256 == the BUILD_F2 line of deploy_gb.log (da0cf85b...)   -> STOP
  INFO only     a task > 80 % of its time limit; an island task outside 4 x (72-124 s) = 288-496 s (pilot island wall); pilot vs twin calib.bin sections equal / differing (I_max 3 refines the grid)
Every probe prints one line `WAVE STATE: RUNNING|ENDED` (ENDED = no squeue row of the wave AND every sacct row terminal AND every submitted job id seen in sacct).
"""
import argparse, glob, hashlib, json, math, os, re, sys
from collections import defaultdict

# ---- the COMMITTED class table of the G-B pilot set (GB_PLAN §2.3): class -> (E, soft = 1.5E, hard = 2.5E, the committed rounding) --------------------------------------------------
TABLE = {
    "gb AR n200 N10000 I0": (108.0, 162.0, 270.0),
    "gb AR n200 N10000 I3": (118.0, 177.0, 295.0),
    "gb ADJOPP n200 N10000 I0": (133.0, 200.0, 333.0),
    "gb ADJOPP n200 N10000 I3": (142.0, 213.0, 355.0),
    "cont AR n200 N2500 I0": (30.0, 45.0, 75.0),
    "cont ADJOPP n200 N2500 I0": (37.0, 56.0, 93.0),
}
TABLE_SHA256 = "c7644eb7b279452ba3805ab969c86bb31fc2da2ddf03679fbb838e9291f72939"
QUOTE = {"G1": 226.0, "G2": 275.0}
WAVE_STOP = {"G1": 450.0, "G2": 550.0}                       # committed (2 x quote, rounded as GB_PLAN §2.3)
CUM_STOP, PROJ_STOP = 800.0, 800.0
ISL_WALL = (288.0, 496.0)                                   # 4 x (72-124 s): pilot island wall, INFO only
INFRA, PEND_BAD = {"NODE_FAIL", "BOOT_FAIL"}, re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)
TERMINAL = {"COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "NODE_FAIL", "BOOT_FAIL", "DEADLINE", "PREEMPTED", "REVOKED"}
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
RID = re.compile(r"^5-(AR|ADJOPP)-n200-r01-(V|VI3|VN25)-s1$")


def table_sha():
    return hashlib.sha256(json.dumps(TABLE, sort_keys=True).encode()).hexdigest()


def klass(rid):
    m = RID.match(rid)
    if not m:
        return None
    return {"V": "gb %s n200 N10000 I0", "VI3": "gb %s n200 N10000 I3", "VN25": "cont %s n200 N2500 I0"}[m.group(2)] % m.group(1)


def expected_N(rid):
    return 2500 if rid.endswith("-VN25-s1") else 10000


def dataset(rid):
    m = RID.match(rid)
    return "5-%s-n200-r01" % m.group(1) if m else rid


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
    for b in sorted(d for d in os.listdir(a.plans) if re.fullmatch(r"GB_%s[a-z]" % a.wave, d)):
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
    foreign = []   # sacct rows on one of our job ids that are not ours (the Slurm accounting DB reuses old job ids: R3 probe 14:20Z, job 2814240 also listed 17 array tasks of another user's cmds_rmsd.list.sh from 2025-10-23)
    for l in S.get("SACCT", []):
        f_ = l.split("|")
        if len(f_) < 7:
            probe_err.append("malformed sacct row (%d fields, 7 needed): %r" % (len(f_), l[:80])); continue
        jid, name, st, el, cpus, cpuraw, lim = f_[:7]; user = f_[7].strip() if len(f_) > 7 else ""
        base, _, task = jid.partition("_")
        if base not in jobmap:
            continue
        if not name.startswith("p1m_GB_") or (user and user != "fb31"):
            foreign.append((jid, name, user)); continue
        sacct_rows += 1; sacct_jobs.add(base); s0 = st.split()[0]
        if s0 not in TERMINAL:
            sacct_nonterm.append("%s %s" % (jid, s0))
        b, fit = jobmap[base]
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
        rid = k.split("/")[1]; kl = klass(rid)
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
    # projection: spent + E of every fit of the set not started (this probe or --prior); scope = the 4 pilot fits (the plans of all waves in --plans)
    scope = []
    for d in sorted(glob.glob(os.path.join(a.plans, "GB_G[0-9][a-z]"))):
        try:
            scope += [f["run_id"] for f in json.load(open(os.path.join(d, "plan.resolved.json")))["fits"]]
        except OSError:
            pass
    started = {k.split("/")[1] for k in cost} | set(prior)
    left = [r for r in scope if r not in started]
    proj = spent + sum(TABLE.get(klass(r), (0.0,))[0] for r in left)
    pnote = "%d fits not started" % len(left)
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
    pilot_secs = {}
    for k, rec in sorted(calib.items()):
        if rec.get("sections"):
            pilot_secs[dataset(k.split("/")[1]), k.split("/")[1].rsplit("-", 2)[-2]] = rec["sections"]
    for ds in sorted({d for d, _ in pilot_secs}):
        if (ds, "V") in pilot_secs and (ds, "VI3") in pilot_secs:
            x, y = pilot_secs[ds, "V"], pilot_secs[ds, "VI3"]; n_pair += 1
            dif = sorted(z for z in set(x) | set(y) if x.get(z) != y.get(z))
            pair_note.append("INFO pair %s: calib.bin sections pilot (I_max 0) vs twin (I_max 3): %d of %d equal%s (the I_max 3 calibration refines the grid, so differences are expected)" % (ds, len(set(x) | set(y)) - len(dif), len(set(x) | set(y)), "; differing: " + ", ".join(dif[:5]) if dif else ""))
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
    for ds, v in hs.items():
        if len(v) > 1:
            flags.append("STOP DATA IDENTITY dataset %s: %d distinct truth.json (X, y) sha256 pairs across its fits (pilot and twin must share the data)" % (ds, len(v)))
    if f2 is None:
        flags.append("STOP build identity: no BUILD_F2 line in the deploy log (cannot compare)")
    for l in S.get("BINSHA", []):
        b, sh = l.split("|")
        if f2 and sh != f2:
            flags.append("STOP BUILD IDENTITY batch %s bin/smcbvs4 sha256 %s.. != BUILD_F2 %s.." % (b, sh[:12], f2[:12]))
    for x in bsha:
        flags.append("STOP BUILD IDENTITY " + x)
    for k, v in sorted(isl.items()):
        if v and (min(v) < ISL_WALL[0] or max(v) > ISL_WALL[1]):
            infos.append("INFO island wall %s: %d task(s) done, %d-%d s, outside 4 x (72-124 s) = %d-%d s" % (k, len(v), min(v), max(v), ISL_WALL[0], ISL_WALL[1]))
    meta = next((k for k in S if k.startswith("META")), "(no META line)")
    print("probe", meta, "| wave", a.wave, "| batches", ",".join(sorted(runs)), "| class table sha256", table_sha()[:12], "(pinned)" if table_sha() == TABLE_SHA256 else "(ALTERED)")
    print("%-52s %-18s %8s %6s %6s  %s" % ("batch/fit", "class", "core-h", "soft", "hard", "stage states"))
    for b in sorted(runs):
        for r in runs[b]:
            k = b + "/" + r; kl = klass(r); t = TABLE.get(kl)
            print("%-52s %-18s %8.2f %6s %6s  %s" % (k, kl, cost.get(k, 0.0), "%.1f" % soft_ov.get(kl, t[1]) if t else "-", "%.1f" % t[2] if t else "-", ",".join(sorted(state.get(k, [])))))
    print("wave actual %.1f core-h (quote %s -> stop > %s) | G-B spent %.1f (cum stop %.0f) | projection %.0f (stop > %.0f; %s)" % (
        wave_cost, "%g" % quote if quote is not None else "none", "%g" % wstop if wstop is not None else "n/a", spent, a.cum_stop, proj, PROJ_STOP, pnote))
    print("arm identity checked on %d fits; pilot/twin calib comparison on %d pairs; datasets with hashes: %d; BUILD_F2 sha256 %s" % (n_arm, n_pair, len(hs), (f2 or "-")[:16]))
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
        infos.append("INFO %d foreign sacct row(s) on our job id(s) %s ignored (not user fb31 / not p1m_GB_*): names %s, user(s) %s, e.g. %s (Slurm accounting job-id reuse; not ours, not touched)" % (len(foreign), ",".join(fj), ",".join(fn)[:80], ",".join(fu), foreign[0][0]))
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
