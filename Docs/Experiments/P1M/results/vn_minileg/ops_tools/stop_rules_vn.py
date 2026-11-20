#!/usr/bin/env python3
"""stop_rules_vn.py <probe.txt> --wave V0 --plans <dir with VN_<wave>_<i>/plan.resolved.json> --deploy-log deploy_F2.log [options]
V-N MINI-LEG (MINILEG_PLAN §5.3; derived from the precision leg's stop_rules_prec.py; the precision leg's tool is untouched). One probe of vn_monitor_probe.sh. Read-only. Stdlib only.
Exit 0 = no stop rule, 3 = STOP. Rules:
  per fit soft  cost > soft line of its class in the COMMITTED CLASS TABLE (below, pinned by TABLE_SHA256) -> REPORT-and-continue; 3 soft trips in the wave -> STOP
  per fit hard  cost > hard line (2.5 x E, floor 3.0; pinned, never re-fitted)                                                    -> STOP
  wave          wave actual (all its batches) > 2 x the wave quote: V0 50, V1 75, V2 125 (--quote = a re-quote)                    -> STOP
  cumulative    mini-leg actual (this wave + --prior) > 400;  projection spent + class means x fits left > 600                    -> STOP
  failures      FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL, BOOT_FAIL = INFO); > 2 failed fits in the wave      -> STOP
  admission     engine resource_limit / admission / OUTCOME record; pending reason QOS / Assoc / MaxSubmit / Invalid / Limit (own wave's jobs only) -> STOP
  arm identity  the fit's recorded arm (calib_meta.json, fallback calib.bin.json settings): N (= 10,000 for every N 10^4 fit; 2,500 for XB2 and the r04 pair), refine_m 1,
                I_max (the plan's), rule bounded != the plan's -> STOP.  FLAGS (behaviour, not stops): I_max = 0: no cost_diag files; I_max = 3: largest diag index = I_used;
                the grid identity island T = refine_m x (dims(grid_unrefined) - 1) = dims(grid) - 1
  PAIRING       every section of the N 10^4 (and XB2) fit's calib.bin except `meta` (calib_meta.json sections[].sha256) equals its N 2,500 TWIN's in records/precision1e4
  identity      (the grid section above all): a mismatch -> STOP (the contrast would not isolate N). A twin or a calib_meta.json that is not there yet is reported, not a stop
  data identity truth.json X / y sha256 equal across all fits of a dataset and equal to the overlap / leg records (--ref-hashes)                                  -> STOP
  build         every batch's bin/smcbvs4 sha256 and every fit's recorded binary.sha256 == the BUILD_F2 line of deploy_F2.log (da0cf85b...)                      -> STOP
Every probe prints one line `WAVE STATE: RUNNING|ENDED` (ENDED = no squeue row of the wave AND every sacct row terminal AND every submitted job id seen in sacct).
"""
import argparse, glob, hashlib, json, math, os, re, sys
from collections import defaultdict

# ---- the COMMITTED class table of the mini-leg (MINILEG_PLAN §5.3): class -> (E, soft, hard); soft = max(3, 1.5E), hard = max(3, 2.5E) as committed -------------------------------
TABLE = {
    "vn N10000 m1 I0": (19.06, 28.6, 47.6),
    "vn N10000 m1 I3": (20.68, 31.0, 51.7),
    "XB2": (5.71, 8.6, 14.3),
    "r04 pair": (1.99, 3.0, 5.0),
}
TABLE_SHA256 = "3c2b1a68e4df7898537eb225c199e34b2a27cd200c1ca056f054c7a824aae79c"
QUOTE = {"V0": 50.0, "V1": 75.0, "V2": 125.0}                 # the wave stop is 2 x
CUM_STOP, PROJ_STOP = 400.0, 600.0
INFRA, PEND_BAD = {"NODE_FAIL", "BOOT_FAIL"}, re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)
TERMINAL = {"COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "NODE_FAIL", "BOOT_FAIL", "DEADLINE", "PREEMPTED", "REVOKED"}
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
RID = re.compile(r"^4-(AR|ARweak|ADJOPP|IND|BLK|NULL)-n(\d+)-r(\d+)-(.*)-s(\d+)$")
LEG_RECORDS = "/home/fb31/SMC_Engineering_Department/records/precision1e4"


def table_sha():
    return hashlib.sha256(json.dumps(TABLE, sort_keys=True).encode()).hexdigest()


def klass(rid):
    m = RID.match(rid)
    if not m:
        return None
    mid = m.group(4)
    if re.fullmatch(r"P-N10000-m1-I0-c\d", mid):
        return "vn N10000 m1 I0"
    if re.fullmatch(r"P-N10000-m1-c\d", mid):
        return "vn N10000 m1 I3"
    if mid == "P-N2500-m1-I0-XB2":
        return "XB2"
    if mid in ("VI3", "V") and m.group(1) == "ADJOPP" and m.group(3) == "04":
        return "r04 pair"
    return None


def expected_N(rid):
    return 10000 if "-N10000-" in rid else 2500


def twin(rid):
    """the leg run id whose calibration this fit must reproduce (same seed, data, H = 512): N 2,500 twin of an N 10^4 fit; XB2's own leg arm; none for the r04 pair"""
    m = re.match(r"^(4-\w+-n200-r01)-P-N10000-m1(-I0)?-c(\d)-s1$", rid)
    if m:
        return "%s-P-N2500-m1%s-c%s-s1" % (m.group(1), m.group(2) or "", m.group(3))
    if rid.endswith("-P-N2500-m1-I0-XB2-s1"):
        return rid.replace("-XB2-s1", "-c1-s1")
    return None


def dataset(rid):
    m = RID.match(rid)
    return "4-%s-n%s-r%s" % m.group(1, 2, 3) if m else rid


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
    ap.add_argument("--deploy-log"); ap.add_argument("--quote", type=float); ap.add_argument("--prior"); ap.add_argument("--cum-stop", type=float, default=CUM_STOP)
    ap.add_argument("--waves-json", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "F2_vn", "waves_vn.json"))
    ap.add_argument("--ref-hashes", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vn_refs.json"))
    ap.add_argument("--leg-records", default=LEG_RECORDS)
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
    for b in sorted(d for d in os.listdir(a.plans) if re.fullmatch(r"VN_%s_\d+" % a.wave, d)):
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
        if not name.startswith("p1m_VN_") or (user and user != "fb31"):
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
    if quote is None:
        flags.append("STOP no quote for wave %s" % a.wave)
    elif wave_cost > 2 * quote:
        flags.append("STOP wave %s actual %.1f > 2 x quote %g" % (a.wave, wave_cost, quote))
    if spent > a.cum_stop:
        flags.append("STOP cumulative %.1f > %.0f" % (spent, a.cum_stop))
    proj, pnote = spent, ""
    try:
        wj = json.load(open(a.waves_json))
        scope = [f["run_id"] for x in wj.values() for b in x["batches"] for f in b["fits"]]
        started = {k.split("/")[1] for k in cost} | set(prior)
        done = defaultdict(list)
        for k, s in state.items():
            if s == {"COMPLETED"}:
                done[klass(k.split("/")[1])].append(cost[k])
        for rid, v in prior.items():
            done[klass(rid)].append(v)
        left = [r for r in scope if r not in started]
        for r in left:
            kl = klass(r); xs = done.get(kl) or []
            proj += (sum(xs) / len(xs)) if len(xs) >= 3 else TABLE.get(kl, (3.0,))[0]
        pnote = "%d fits left" % len(left)
    except OSError as e:
        pnote = "waves_vn.json unreadable (%s): projection = spent" % e
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
            flags.append("STOP PLAN %s: the plan's N %s != the mini-leg's %s for this fit" % (k, f["N"], exp["N"]))
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
        tw = twin(rid)
        if tw and rec.get("sections"):
            cands = glob.glob(os.path.join(a.leg_records, "*", tw, "calib_meta.json"))
            if not cands:
                pair_note.append("%s: twin %s has no calib_meta.json under %s" % (rid, tw, a.leg_records)); continue
            tsec = {x["name"]: x["sha256"] for x in json.load(open(cands[0])).get("sections", []) if x.get("name") != "meta"}
            n_pair += 1
            diff = sorted(x for x in set(tsec) | set(rec["sections"]) if tsec.get(x) != rec["sections"].get(x))
            if diff:
                flags.append("STOP PAIRING IDENTITY %s vs twin %s: calib.bin sections differ: %s%s (the contrast would not isolate N)" % (rid, tw, ", ".join(diff[:6]), " [the grid section!]" if "grid" in diff else ""))
        elif tw:
            pair_note.append("%s: no calib_meta sections yet (run the probe with MAKE_CALIB_META=1): pairing identity not checked" % rid)
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
                flags.append("STOP DATA IDENTITY dataset %s: X/y sha256 differ from the overlap / leg record" % ds)
    if f2 is None:
        flags.append("STOP build identity: no BUILD_F2 line in the deploy log (cannot compare)")
    for l in S.get("BINSHA", []):
        b, sh = l.split("|")
        if f2 and sh != f2:
            flags.append("STOP BUILD IDENTITY batch %s bin/smcbvs4 sha256 %s.. != BUILD_F2 %s.." % (b, sh[:12], f2[:12]))
    for x in bsha:
        flags.append("STOP BUILD IDENTITY " + x)
    meta = next((k for k in S if k.startswith("META")), "(no META line)")
    print("probe", meta, "| wave", a.wave, "| batches", ",".join(sorted(runs)), "| class table sha256", table_sha()[:12], "(pinned)" if table_sha() == TABLE_SHA256 else "(ALTERED)")
    print("%-52s %-18s %8s %6s %6s  %s" % ("batch/fit", "class", "core-h", "soft", "hard", "stage states"))
    for b in sorted(runs):
        for r in runs[b]:
            k = b + "/" + r; kl = klass(r); t = TABLE.get(kl)
            print("%-52s %-18s %8.2f %6s %6s  %s" % (k, kl, cost.get(k, 0.0), "%.1f" % soft_ov.get(kl, t[1]) if t else "-", "%.1f" % t[2] if t else "-", ",".join(sorted(state.get(k, [])))))
    print("wave actual %.1f core-h (quote %s -> stop > %s) | mini-leg spent %.1f (cum stop %.0f) | projection %.0f (stop > %.0f; %s)" % (
        wave_cost, "%g" % quote if quote is not None else "none", "%g" % (2 * quote) if quote is not None else "n/a", spent, a.cum_stop, proj, PROJ_STOP, pnote))
    print("arm identity checked on %d fits; pairing identity checked on %d fits; datasets with hashes: %d; BUILD_F2 sha256 %s" % (n_arm, n_pair, len(hs), (f2 or "-")[:16]))
    print("SOFT OVERRIDES (soft column only; TABLE and the hard column pinned, sha256 %s): %s" % (table_sha()[:12], "; ".join("%s: committed soft %.1f -> %.1f" % (k, TABLE[k][1], v) for k, v in sorted(soft_ov.items())) or "none"))
    if n_foreign:
        print("squeue rows of other jobs of the account ignored: %d" % n_foreign)
    missing = sorted(set(jobmap) - sacct_jobs)
    ended = own_squeue == 0 and sacct_rows > 0 and not sacct_nonterm and not missing
    if ended:
        print("WAVE STATE: ENDED  (no squeue row of the wave's batches; %d sacct rows, all terminal; %d job ids seen) -> stop probing, report, collect (read-back)" % (sacct_rows, len(sacct_jobs)))
    else:
        why = []
        if own_squeue: why.append("%d squeue row(s) of the wave" % own_squeue)
        if sacct_nonterm: why.append("%d non-terminal sacct row(s), e.g. %s" % (len(sacct_nonterm), sacct_nonterm[0]))
        if missing: why.append("%d submitted job id(s) not in sacct yet" % len(missing))
        if sacct_rows == 0: why.append("no sacct row yet")
        print("WAVE STATE: RUNNING  (%s)" % "; ".join(why))
    if foreign:
        fj = sorted({j.partition("_")[0] for j, _, _ in foreign}); fn = sorted({n for _, n, _ in foreign}); fu = sorted({u or "?" for _, _, u in foreign})
        infos.append("INFO %d foreign sacct row(s) on our job id(s) %s ignored (not user fb31 / not p1m_VN_*): names %s, user(s) %s, e.g. %s (Slurm accounting job-id reuse; not ours, not touched)" % (len(foreign), ",".join(fj), ",".join(fn)[:80], ",".join(fu), foreign[0][0]))
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
