#!/usr/bin/env python3
"""test_stop_rules_prec.py -- synthetic probes for stop_rules_prec.py (O-3). Scratch under $PREC_TEST_TMP or staging/precision1e4/_t (never /tmp).
Plans: the real A0 plan dirs (F_eefcbc4a/scripts/PL_A0_{1,2,3}). Each case builds a probe and checks the exit code and the lines printed."""
import json, os, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE)
TMP = os.environ.get("PREC_TEST_TMP", os.path.join(STG, "_t")); os.makedirs(TMP, exist_ok=True)
PLANS = os.path.join(STG, "current", "scripts")
LEG = "d" * 64
LOG = os.path.join(TMP, "deploy_leg.log")
open(LOG, "w").write("2026-11-20T10:00:00Z\tPL_A0_1\tBUILD\t%s\teefcbc4a\tsapphirerapids\t1\t6000\ttest\n" % LEG)
M4, I0, A3, XB = ("4-AR-n200-r01-P-N2500-m4-c1-s1", "4-AR-n200-r01-P-N2500-m1-I0-c1-s1", "4-AR-n200-r01-A3-exactlink-s1", "4-AR-n200-r01-V-XB-s1")
BATCH = {M4: "PL_A0_1", I0: "PL_A0_1", A3: "PL_A0_2", XB: "PL_A0_3"}
ORDER = {"PL_A0_1": [M4, I0], "PL_A0_2": [A3], "PL_A0_3": [XB]}
XY = ("e" * 64, "f" * 64)
def probe(costs, states=None, calib=None, islT=None, diag=None, xy=None, binsha=None, dbin=None, squeue=(), engine=(), extra_sacct=()):
    L = ["### META utc=2026-11-20T11:00:00Z"]; off = 100
    for b, rs in ORDER.items():
        L.append("### SUBMISSIONS " + b)
        L.append(json.dumps({"stage": "setup", "fit": "all", "job": str(off), "submitted_utc": "x"}))
        off += 10
    L.append("### SQUEUE"); L += list(squeue)
    L.append("### SACCT")
    off = 100
    for b, rs in ORDER.items():
        for i, r in enumerate(rs, 1):
            L.append("%d_%d|p1m_%s_setup|%s|60|8|%d|01:00:00" % (off, i, b, (states or {}).get(r, "COMPLETED"), int(costs.get(r, 0) * 3600)))
        off += 10
    for x in extra_sacct: L.append(x)
    L.append("### DATA_HASH")
    for r in (M4, I0, A3, XB):
        x, y = (xy or {}).get(r, XY); L.append("%s|%s|c%s|%s|%s|%s" % (BATCH[r], r, r[-6:], x, y, (dbin or {}).get(r, LEG)))
    L.append("### CALIB")
    plan = {M4: (4, 3), I0: (1, 0), A3: (1, 3), XB: (1, 3)}
    for r in (M4, I0, A3, XB):
        m, i = plan[r]; rec = {"N": 2500, "refine_m": m, "I_max": i, "I_used": 0 if i == 0 else 2, "rule": "bounded", "source": "calib_meta.json", "status": "completed", "cal_status": "ok"}
        rec.update((calib or {}).get(r, {})); L.append("%s|%s|%s" % (BATCH[r], r, json.dumps(rec)))
    L.append("### ISLAND_T")
    for r in (M4, I0, A3, XB):
        L.append("%s|%s|%d" % (BATCH[r], r, (islT or {}).get(r, 92 if r == M4 else 22)))
    L.append("### DIAG")
    for r in (M4, I0, A3, XB):
        k, c = (diag or {}).get(r, (0, 0) if r == I0 else (2, 8)); L.append("%s|%s|%d|%d" % (BATCH[r], r, k, c))
    L.append("### BINSHA")
    for b in ORDER: L.append("%s|%s" % (b, (binsha or {}).get(b, LEG)))
    L.append("### ENGINE_FLAGS"); L += list(engine)
    p = os.path.join(TMP, "probe.txt"); open(p, "w").write("\n".join(L) + "\n"); return p
def run(p, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_prec.py"), p, "--wave", "A0", "--plans", PLANS, "--leg-log", LOG,
                        "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
json.dump({"4-AR-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]}}, open(os.path.join(TMP, "refs.json"), "w"))
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
base = {M4: 12.0, I0: 5.0, A3: 2.5, XB: 2.0}
rc, o = run(probe(base)); check("healthy A0: no stop", rc == 0 and "no stop rule fired" in o and "SOFT" not in o, o)
rc, o = run(probe(dict(base, **{M4: 20.0}))); check("one soft trip (m4 20 > 18.5, <= hard 30.9): reported, continues", rc == 0 and "SOFT TRIP" in o and "1 soft trip" in o, o)
rc, o = run(probe(dict(base, **{M4: 20.0, I0: 9.0, A3: 4.5}))); check("3 soft trips -> STOP", rc == 3 and "3 soft trips" in o, o)
rc, o = run(probe(dict(base, **{M4: 31.0}))); check("hard trip (m4 31 > 30.9) -> STOP", rc == 3 and "HARD" in o, o)
rc, o = run(probe(dict(base, **{XB: 3.4}))); check("XB class AR n200: soft 3.3 -> soft trip only", rc == 0 and "SOFT TRIP" in o, o)
rc, o = run(probe(dict(base, **{M4: 28.0, I0: 14.0, A3: 6.0, XB: 5.0}))); check("wave > 2 x quote 25 = 50 -> STOP", rc == 3 and "> 2 x quote 25" in o, o)
rc, o = run(probe(base), "--prior", os.path.join(TMP, "prior.json")) if json.dump({"x": 990.0}, open(os.path.join(TMP, "prior.json"), "w")) is None else (0, "")
check("cumulative: wave 21.5 + prior 990 > 1,000 -> STOP", rc == 3 and "cumulative" in o, o)
json.dump({"4-AR-n200-r02-V-s1": 4100.0}, open(os.path.join(TMP, "prior2.json"), "w"))
rc, o = run(probe(base), "--prior", os.path.join(TMP, "prior2.json")); check("projection ceiling 4,127 -> STOP (and cumulative)", rc == 3 and "projection" in o, o)
rc, o = run(probe(base), "--cum-stop", "1600"); check("--cum-stop 1600 accepted", rc == 0, o)
rc, o = run(probe(base, calib={M4: {"refine_m": 1}})); check("ARM IDENTITY: m4 planned, record says refine_m 1 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run(probe(base, calib={I0: {"I_max": 3}})); check("ARM IDENTITY: I_max 0 planned, record says 3 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run(probe(base, calib={XB: {"N": 10000}})); check("ARM IDENTITY: N 10000 recorded -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run(probe(base, islT={M4: 24})); check("behaviour: m4 with island T 24 -> FLAG, not STOP", rc == 0 and "FLAG behaviour" in o and "T = 24" in o, o)
rc, o = run(probe(base, islT={M4: 30})); check("behaviour: m4 with T 30 (not % 4, < 36) -> FLAG", rc == 0 and "FLAG behaviour" in o, o)
rc, o = run(probe(base, diag={I0: (1, 3)})); check("behaviour: I_max 0 but cost_diag files -> FLAG, not STOP", rc == 0 and "I_max = 0 but 3 cost_diag" in o, o)
rc, o = run(probe(base, diag={XB: (3, 12)})); check("behaviour: I_max 3, I_used 2, diag k max 3 -> FLAG", rc == 0 and "I_used = 2" in o, o)
rc, o = run(probe(base, xy={A3: ("1" * 64, XY[1])})); check("DATA IDENTITY: dataset X differs across fits -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
refbad = {M4: ("1" * 64, "2" * 64), I0: ("1" * 64, "2" * 64), A3: ("1" * 64, "2" * 64), XB: ("1" * 64, "2" * 64)}
rc, o = run(probe(base, xy=refbad)); check("DATA IDENTITY: consistent but != overlap record -> STOP", rc == 3 and "differ from the overlap record" in o, o)
rc, o = run(probe(base, binsha={"PL_A0_2": "a" * 64})); check("BUILD IDENTITY: batch binary sha != leg -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(base, dbin={XB: "b" * 64})); check("BUILD IDENTITY: fit record binary.sha256 != leg -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(base, states={A3: "FAILED"})); check("FAILED stage -> STOP", rc == 3 and "non-infrastructure" in o, o)
rc, o = run(probe(base, states={A3: "NODE_FAIL"})); check("NODE_FAIL = INFO only", rc == 0 and "infrastructure fault" in o, o)
rc, o = run(probe(base, squeue=["9|p1m_PL_A0_1_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("QOS pending reason -> STOP", rc == 3 and "admission" in o, o)
rc, o = run(probe(base, engine=["/x/scratch/runs/PL_A0_1/f/log/island_1.log"])); check("engine resource_limit record -> STOP", rc == 3 and "engine record" in o, o)
os.environ["IGNORE_JOBS"] = "100"; rc, o = run(probe(base, states={M4: "FAILED"})); del os.environ["IGNORE_JOBS"]
check("known-failed job (IGNORE_JOBS) = INFO", rc == 0 and "known-failed" in o, o)
# the committed table is pinned: altering it is a STOP
src = open(os.path.join(HERE, "stop_rules_prec.py")).read().replace('"A3 n200": (2.76, 4.1, 6.9)', '"A3 n200": (2.76, 40.1, 60.9)')
alt = os.path.join(TMP, "stop_rules_prec_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe(base), "--wave", "A0", "--plans", PLANS, "--leg-log", LOG, "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
