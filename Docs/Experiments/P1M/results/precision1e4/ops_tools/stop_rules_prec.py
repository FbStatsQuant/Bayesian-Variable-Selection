#!/usr/bin/env python3
"""stop_rules_prec.py <probe.txt> --wave A0 --plans <dir with PL_<wave>_<i>/plan.resolved.json> --leg-log deploy_leg.log [options]
PRECISION LEG (LEG_PLAN §5.3, HQ Q3 / Q4 approved, bd02631e). Evaluates one probe of monitor_probe.sh. Stdlib only, read-only. Exit 0 = no stop rule, 3 = STOP.
Rules:
  per fit soft  cost > soft line of its class in the COMMITTED CLASS TABLE (below, pinned by TABLE_SHA256)  -> REPORT-and-continue, each trip printed at once;
                3 soft trips in one wave -> STOP.  (The soft line may move after a pilot re-fit; the hard line never does: the table is the committed one.)
  per fit hard  cost > hard line (2.5 x E, floor 3.0)                                                      -> STOP
  wave          wave actual (all its batches, billed) > 2 x the wave quote (LEG_PLAN §4 table, or --quote = a re-quote)  -> STOP
  cumulative    leg actual (this wave + --prior) > 1,000 (--cum-stop: 1,600 m4-frozen / 900 I0-frozen)    -> STOP
  projection    spent + class means x fits left > 4,127 (the plan figure; fits left from waves.json, held H waves excluded unless --with-held)  -> STOP
  failures      FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED stage (NODE_FAIL, BOOT_FAIL = INFO); > 2 failed fits in the wave  -> STOP
  admission     engine resource_limit / admission / OUTCOME record, pending reason QOS / Assoc / MaxSubmit / Invalid / Limit  -> STOP
  arm identity  the fit's recorded arm (calib_meta.json when present, else calib.bin.json settings): N, refine_m, I_max, rule != the plan's  -> STOP.
                BEHAVIOUR checks (R5) are FLAGS, not stops (the record is authoritative): the grid identity (F1) island T = refine_m x (dims(grid_unrefined) - 1) = dims(grid) - 1
                from calib_meta.json (T >= 36 for m = 4 is only a HINT, when calib_meta.json is not there yet); I_max = 0: no cost_diag files;
                I_max = 3: the largest diagnostic rebuild index k in cost/ == I_used (needs calib_meta.json)
  data identity truth.json X / y sha256 equal across all fits of a dataset (NOT data.bin.json content_sha256: it embeds the binary block), and equal to the overlap records (--ref-hashes)  -> STOP
  build identity every batch's bin/smcbvs4 sha256 and every new fit's recorded binary.sha256 == the leg's single build (first BUILD line of deploy_leg.log)  -> STOP
                (the 14 reused overlap V fits are exempt by their listed shas; they are not run in this leg's batches)
"""
import argparse, hashlib, json, os, re, sys
from collections import defaultdict

# ---- the COMMITTED class table (LEG_PLAN §5.3; E per fit from quote_output.txt): class -> (E, soft, hard) ------------------------------------------------
TABLE = {
    "prec N2500 m1 I3": (6.28, 9.4, 15.7), "prec N2500 m1 I0": (5.76, 8.6, 14.4), "prec N2500 m4 I3": (12.36, 18.5, 30.9),
    "prec N10000 m1": (17.00, 25.5, 42.5), "prec N10000 m4": (41.29, 61.9, 103.2),
    "A3 n200": (2.76, 4.1, 6.9),
    "AR n100": (1.55, 3.0, 3.9), "AR n200": (2.18, 3.3, 5.5), "AR n400": (3.64, 5.5, 9.1), "AR n800": (6.94, 10.4, 17.4),
    "ARweak n100": (1.36, 3.0, 3.4), "ARweak n200": (1.87, 3.0, 4.7), "ARweak n400": (3.05, 4.6, 7.6), "ARweak n800": (5.67, 8.5, 14.2),
    "IND n100": (1.62, 3.0, 4.1), "IND n200": (2.30, 3.4, 5.8), "IND n400": (3.89, 5.8, 9.7),
    "BLK n100": (1.58, 3.0, 4.0), "BLK n200": (2.22, 3.3, 5.6), "BLK n400": (3.72, 5.6, 9.3),
    "ADJOPP n200": (2.69, 4.0, 6.7), "ADJOPP n400": (4.62, 6.9, 11.6),
    "NULL n200": (0.51, 3.0, 3.0),
}
TABLE_SHA256 = "c0fcd139db0a02d18c169eed1e9c46effdd6f5407a7d413ac97bb8046d9994b3"
QUOTE = {"A0": 25, "P1": 30, "P2": 30, "P3": 25, "P4": 45, "S1": 60, "S2": 30, "S3": 40, "S4": 40, "S5": 20, "S6": 30, "S7": 100, "S8": 50, "S9": 75,
         "H1": 115, "H2": 80, "H3": 155}                       # LEG_PLAN §4: the wave stop is 2 x
CUM_STOP, PROJ_STOP = 1000.0, 4127.0
EXEMPT_RUNS = {"4-AR-n200-r0%d-V-s%d" % (r, s) for r in (1, 2, 3, 4) for s in (1, 2)} | {"4-ARweak-n200-r01-V-s1", "4-ARweak-n200-r02-V-s1", "4-ADJOPP-n200-r01-V-s1",
               "4-ADJOPP-n200-r02-V-s1", "4-IND-n200-r01-V-s1", "4-NULL-n200-r01-V-s1"}   # reused overlap fits: exempt by their listed shas (never run here)
INFRA, PEND_BAD = {"NODE_FAIL", "BOOT_FAIL"}, re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
RID = re.compile(r"^4-(AR|ARweak|ADJOPP|IND|BLK|NULL)-n(\d+)-r(\d+)-(.*)-s(\d+)$")


def table_sha():
    return hashlib.sha256(json.dumps(TABLE, sort_keys=True).encode()).hexdigest()


def klass(rid):
    m = RID.match(rid)
    if not m:
        return None
    ds, n, rep, mid, s = m.groups()
    if mid.startswith("P-N"):
        mm = re.match(r"P-N(\d+)-m(\d)(-I0)?-c\d$", mid)
        if not mm:
            return None
        N, mval, i0 = mm.group(1), mm.group(2), mm.group(3)
        return "prec N2500 m%s I%s" % (mval, "0" if i0 else "3") if N == "2500" else "prec N10000 m%s" % mval
    if mid in ("A3-exactlink", "A3F-exactlink"):
        return "A3 n200"
    if mid in ("V", "VF", "V-XB"):
        return "%s n%s" % (ds, n)
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
    ap.add_argument("--leg-log"); ap.add_argument("--quote", type=float); ap.add_argument("--prior"); ap.add_argument("--cum-stop", type=float, default=CUM_STOP)
    ap.add_argument("--waves-json", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "waves.json"))
    ap.add_argument("--with-held", action="store_true"); ap.add_argument("--ref-hashes", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "overlap_refs.json"))
    ap.add_argument("--soft", action="append", default=[], metavar="CLASS=VALUE", help="override the SOFT column of a class (after a pilot re-fit, approved by the manager); TABLE and the HARD column stay pinned; also env SOFT_OVERRIDES='CLASS=V;CLASS=V'; every override is printed in the verdict")
    ap.add_argument("--ignore-jobs", default=os.environ.get("IGNORE_JOBS", "")); ap.add_argument("--ignore-batches", default=os.environ.get("IGNORE_FAILED", ""))
    a = ap.parse_args()
    flags, infos = [], []
    if table_sha() != TABLE_SHA256:
        flags.append("STOP the committed class table in this script was altered (sha256 %s != pinned %s)" % (table_sha()[:12], TABLE_SHA256[:12]))
    soft_ov = {}
    for item in list(a.soft) + [x for x in os.environ.get("SOFT_OVERRIDES", "").split(";") if x.strip()]:
        k, _, v = item.rpartition("=")
        k = k.strip()
        if k not in TABLE or not v.strip():
            print("bad --soft %r: class must be one of the committed table's and the value a number" % item, file=sys.stderr); sys.exit(64)
        v = float(v)
        if not (0 < v <= TABLE[k][2]):
            print("bad --soft %r: the soft line must be in (0, hard = %.1f]; the hard column never moves" % (item, TABLE[k][2]), file=sys.stderr); sys.exit(64)
        soft_ov[k] = v
    ign_jobs = {x for x in a.ignore_jobs.split(",") if x}; ign_b = {x for x in a.ignore_batches.split(",") if x}
    S = sections(a.probe)
    runs, planfit, arm_of = {}, {}, {}
    for b in sorted(d for d in os.listdir(a.plans) if re.fullmatch(r"PL_%s_\d+" % a.wave, d)):
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
    for l in S.get("SACCT", []):
        jid, name, st, el, cpus, cpuraw, lim = l.split("|")[:7]
        base, _, task = jid.partition("_")
        if base not in jobmap:
            continue
        b, fit = jobmap[base]
        if fit is None:
            if not task.isdigit():
                continue
            fit = runs[b][int(task) - 1]
        k = b + "/" + fit
        cost[k] += int(cpuraw or 0) / 3600.0
        s0 = st.split()[0]
        if base not in ign_jobs:
            state[k].add(s0)
        if s0 in BAD:
            known = b in ign_b or base in ign_jobs
            (infos if known else bad_stage).append(("known-failed: " if known else "") + "%s %s %s" % (jid, name, st))
        if s0 in INFRA:
            infos.append("infrastructure fault (not a stop rule; one rerun per fit, manager): %s %s %s" % (jid, name, st))
    n_foreign = 0
    for l in S.get("SQUEUE", []):
        i, n, st, rs = l.split("|")[:4]
        if i.split("_")[0] not in jobmap:   # F6: only this wave's own jobs (a foreign job of the account must not give a false STOP)
            n_foreign += 1; continue
        if st == "PENDING" and PEND_BAD.search(rs):
            # JobArrayTaskLimit with the array's own %k throttle in its id ([a-b%k]) = our own submit throttle, not a cluster limit
            # (A0 false alarm 11-19, 2791240_[9-16%8]; HQ: exclude it). Without a %k in the id it still STOPs.
            if rs == "JobArrayTaskLimit" and re.search(r"%\d+\]$", i):
                infos.append("own array throttle (not a stop): %s %s reason=%s" % (i, n, rs))
            else:
                pend.append("%s %s reason=%s" % (i, n, rs))
    prior = json.load(open(a.prior)) if a.prior else {}
    wave_cost = sum(cost.values()); spent = wave_cost + sum(prior.values())
    # ---- per fit: committed class table ------------------------------------------------------------------------------------------------------------------
    soft_trips = []
    for k, c in sorted(cost.items()):
        rid = k.split("/")[1]; kl = klass(rid)
        if kl not in TABLE:
            flags.append("STOP fit %s: no class in the committed table (class %r)" % (k, kl)); continue
        E, soft, hard = TABLE[kl]
        soft = soft_ov.get(kl, soft)
        if c > hard:
            flags.append("STOP fit %s [%s] cost %.2f core-h > HARD %.1f (2.5 x model, committed table)" % (k, kl, c, hard))
        elif c > soft:
            soft_trips.append((k, kl, c, soft))
            flags.append("SOFT TRIP fit %s [%s] cost %.2f > soft %.1f (1.5 x model): report and continue (≤ 3 lines to the manager)" % (k, kl, c, soft))
    if len(soft_trips) >= 3:
        flags.append("STOP 3 soft trips in wave %s: %s" % (a.wave, ", ".join(t[0] for t in soft_trips)))
    quote = a.quote or QUOTE.get(a.wave)
    if quote and wave_cost > 2 * quote:
        flags.append("STOP wave %s actual %.1f > 2 x quote %.0f" % (a.wave, wave_cost, quote))
    if spent > a.cum_stop:
        flags.append("STOP cumulative %.1f > %.0f" % (spent, a.cum_stop))
    # ---- projection: spent + class means x fits left (released scope of waves.json) ---------------------------------------------------------------------
    proj, pnote = spent, ""
    try:
        wj = json.load(open(a.waves_json))
        scope = [f["run_id"] for w, x in wj.items() if a.with_held or not w.startswith("H") for b in x["batches"] for f in b["fits"]]
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
        pnote = "waves.json unreadable (%s): projection = spent" % e
    if proj > PROJ_STOP:
        flags.append("STOP projection %.0f > %.0f" % (proj, PROJ_STOP))
    if bad_stage:
        flags.append("STOP non-infrastructure failed stage(s): " + "; ".join(bad_stage))
    failed = {k for k, s in state.items() if s & BAD and k.split("/")[0] not in ign_b}
    if len(failed) > 2:
        flags.append("STOP > 2 failed fits in the wave: %s" % sorted(failed))
    if pend:
        flags.append("STOP admission / QOS pending reason: " + "; ".join(pend))
    if S.get("ENGINE_FLAGS"):
        flags.append("STOP engine record (OUTCOME / resource_limit / admission): " + "; ".join(S["ENGINE_FLAGS"]))
    # ---- arm identity (settings) and behaviour (flags) -----------------------------------------------------------------------------------------------------
    calib = {}
    for l in S.get("CALIB", []):
        b, r, js = l.split("|", 2); calib[b + "/" + r] = json.loads(js)
    islT = {l.split("|")[0] + "/" + l.split("|")[1]: int(l.split("|")[2]) for l in S.get("ISLAND_T", [])}
    diag = {l.split("|")[0] + "/" + l.split("|")[1]: (int(l.split("|")[2]), int(l.split("|")[3])) for l in S.get("DIAG", [])}
    n_arm = 0
    for k, rec in sorted(calib.items()):
        f = planfit.get(k)
        if not f:
            continue
        pm = f.get("params") or {}
        exp = {"N": f["N"], "refine_m": pm.get("refine_m", 1), "I_max": pm.get("I_max", 3), "rule": "bounded"}
        got = {x: rec.get(x) for x in exp}
        n_arm += 1
        if got != exp:
            flags.append("STOP ARM IDENTITY %s: recorded %s (%s) != plan %s" % (k, got, rec.get("source"), exp))
            continue
        gn, un = rec.get("grid_n"), rec.get("grid_unrefined_n")
        if k in islT and gn and un:   # F1: the exact identity T = dims(grid) - 1 = refine_m x (dims(grid_unrefined) - 1), from calib_meta.json (all arms)
            mm = exp["refine_m"]
            if not (islT[k] == gn - 1 == mm * (un - 1)):
                flags.append("FLAG behaviour %s: island T = %d, dims(grid) - 1 = %d, refine_m x (dims(grid_unrefined) - 1) = %d x %d = %d: the identity T = refine_m x (n_unrefined - 1) fails; "
                             "the record is authoritative, tell the manager" % (k, islT[k], gn - 1, mm, un - 1, mm * (un - 1)))
        elif exp["refine_m"] == 4 and k in islT and not (islT[k] % 4 == 0 and islT[k] >= 36):
            infos.append("HINT behaviour %s: m = 4, island T = %d (hint: T %% 4 == 0 and T >= 36); the exact identity needs calib_meta.json (grid dims): re-check at the read-back" % (k, islT[k]))
        if k in diag:
            kmax, cnt = diag[k]
            if exp["I_max"] == 0 and cnt != 0:
                flags.append("FLAG behaviour %s: I_max = 0 but %d cost_diag files exist" % (k, cnt))
            if exp["I_max"] == 3 and rec.get("I_used") is not None and kmax != rec["I_used"]:
                flags.append("FLAG behaviour %s: I_used = %s but the largest diagnostic index in cost/ is %d" % (k, rec["I_used"], kmax))
    # ---- data identity ----------------------------------------------------------------------------------------------------------------------------------------
    hs, bsha = defaultdict(set), []
    leg = None
    if a.leg_log and os.path.exists(a.leg_log):
        for l in open(a.leg_log):
            f = l.rstrip("\n").split("\t")
            if len(f) > 3 and f[2] == "BUILD":
                leg = f[3]; break
    for l in S.get("DATA_HASH", []):
        b, r, cs, xs, ys, bs = l.split("|")
        hs[dataset(r)].add((xs, ys))   # X / y from truth.json only: data.bin.json content_sha256 embeds the binary block and differs per build (checked on the 40 overlap records)
        if leg and r not in EXEMPT_RUNS and bs != "-" and bs != leg:
            bsha.append("%s/%s recorded binary.sha256 %s.. != the leg build" % (b, r, bs[:12]))
    ref = json.load(open(a.ref_hashes)) if os.path.exists(a.ref_hashes) else {}
    for ds, v in hs.items():
        if len(v) > 1:
            flags.append("STOP DATA IDENTITY dataset %s: %d distinct truth.json (X, y) sha256 pairs across its fits" % (ds, len(v)))
        elif ds in ref:
            (xs, ys), = v
            if (xs, ys) != (ref[ds]["X_sha256"], ref[ds]["y_sha256"]):
                flags.append("STOP DATA IDENTITY dataset %s: X/y sha256 differ from the overlap record" % ds)
    if leg is None:
        flags.append("STOP build identity: no BUILD line in the deploy log (cannot compare)")
    for l in S.get("BINSHA", []):
        b, sh = l.split("|")
        if leg and sh != leg:
            flags.append("STOP BUILD IDENTITY batch %s bin/smcbvs4 sha256 %s.. != the leg build %s.." % (b, sh[:12], leg[:12]))
    for x in bsha:
        flags.append("STOP BUILD IDENTITY " + x)
    meta = next((k for k in S if k.startswith("META")), "(no META line)")
    print("probe", meta, "| wave", a.wave, "| batches", ",".join(sorted(runs)), "| class table sha256", table_sha()[:12], "(pinned)" if table_sha() == TABLE_SHA256 else "(ALTERED)")
    print("%-50s %-18s %8s %6s %6s  %s" % ("batch/fit", "class", "core-h", "soft", "hard", "stage states"))
    for b in sorted(runs):
        for r in runs[b]:
            k = b + "/" + r; kl = klass(r); t = TABLE.get(kl, (0, 0, 0))
            print("%-50s %-18s %8.2f %6.1f %6.1f  %s" % (k, kl, cost.get(k, 0.0), t[1], t[2], ",".join(sorted(state.get(k, [])))))
    print("wave actual %.1f core-h (quote %s -> stop > %s) | leg spent %.1f (cum stop %.0f) | projection %.0f (stop > %.0f; %s)" % (
        wave_cost, quote, "%.0f" % (2 * quote) if quote else "n/a", spent, a.cum_stop, proj, PROJ_STOP, pnote))
    print("arm identity checked on %d fits; datasets with hashes: %d; leg build sha256 %s" % (n_arm, len(hs), (leg or "-")[:16]))
    print("SOFT OVERRIDES (soft column only; TABLE and the hard column pinned, sha256 %s): %s" % (table_sha()[:12], "; ".join("%s: committed soft %.1f -> %.1f" % (k, TABLE[k][1], v) for k, v in sorted(soft_ov.items())) or "none"))
    if n_foreign:
        print("squeue rows of other jobs of the account ignored: %d" % n_foreign)
    for x in infos:
        print("INFO", x[5:] if x.startswith("INFO ") else x)
    for f in flags:
        print(f)
    stop = any(f.startswith("STOP") for f in flags)
    print("VERDICT:", "STOP SUBMITTING, tell the manager" if stop else "no stop rule fired" + (" (%d soft trip(s) reported)" % len(soft_trips) if soft_trips else ""))
    sys.exit(3 if stop else 0)


if __name__ == "__main__":
    main()
