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
rc, o = run(probe(base)); check("healthy A0: no stop", rc == 0 and "no stop rule fired" in o and "SOFT TRIP" not in o, o)
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
rc, o = run(probe(base, islT={M4: 24})); check("behaviour hint (no grid dims yet): m4 with island T 24 -> HINT only, no FLAG, no STOP", rc == 0 and "HINT behaviour" in o and "FLAG behaviour" not in o, o)
rc, o = run(probe(base, islT={M4: 30})); check("behaviour hint: m4 with T 30 -> HINT only", rc == 0 and "HINT behaviour" in o and "FLAG" not in o, o)
# F1: the exact grid identity T = dims(grid) - 1 = refine_m x (dims(grid_unrefined) - 1) from calib_meta.json
rc, o = run(probe(base, islT={M4: 84}, calib={M4: {"grid_n": 85, "grid_unrefined_n": 22}})); check("F1 exact identity holds (84 = 4 x 21): no flag, no hint", rc == 0 and "behaviour" not in o, o)
rc, o = run(probe(base, islT={M4: 32}, calib={M4: {"grid_n": 33, "grid_unrefined_n": 9}})); check("F1 an ARweak-like m4 grid T = 32 (< 36) is fine by the identity: no flag", rc == 0 and "behaviour" not in o, o)
rc, o = run(probe(base, islT={M4: 80}, calib={M4: {"grid_n": 85, "grid_unrefined_n": 22}})); check("F1 identity fails (T 80 != 84) -> FLAG, not STOP", rc == 0 and "FLAG behaviour" in o and "identity" in o, o)
rc, o = run(probe(base, islT={M4: 84}, calib={M4: {"grid_n": 85, "grid_unrefined_n": 23}})); check("F1 identity fails (unrefined dims 23 -> 4 x 22 = 88) -> FLAG", rc == 0 and "FLAG behaviour" in o, o)
rc, o = run(probe(base, islT={I0: 23}, calib={I0: {"grid_n": 24, "grid_unrefined_n": 24}})); check("F1 identity also checked for m = 1 (T 23 = 1 x 23): no flag", rc == 0 and "behaviour" not in o, o)
rc, o = run(probe(base, diag={I0: (1, 3)})); check("behaviour: I_max 0 but cost_diag files -> FLAG, not STOP", rc == 0 and "I_max = 0 but 3 cost_diag" in o, o)
rc, o = run(probe(base, diag={XB: (3, 12)})); check("behaviour: I_max 3, I_used 2, diag k max 3 -> FLAG", rc == 0 and "I_used = 2" in o, o)
rc, o = run(probe(base, xy={A3: ("1" * 64, XY[1])})); check("DATA IDENTITY: dataset X differs across fits -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
refbad = {M4: ("1" * 64, "2" * 64), I0: ("1" * 64, "2" * 64), A3: ("1" * 64, "2" * 64), XB: ("1" * 64, "2" * 64)}
rc, o = run(probe(base, xy=refbad)); check("DATA IDENTITY: consistent but != overlap record -> STOP", rc == 3 and "differ from the overlap record" in o, o)
rc, o = run(probe(base, binsha={"PL_A0_2": "a" * 64})); check("BUILD IDENTITY: batch binary sha != leg -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(base, dbin={XB: "b" * 64})); check("BUILD IDENTITY: fit record binary.sha256 != leg -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(base, states={A3: "FAILED"})); check("FAILED stage -> STOP", rc == 3 and "non-infrastructure" in o, o)
rc, o = run(probe(base, states={A3: "NODE_FAIL"})); check("NODE_FAIL = INFO only", rc == 0 and "infrastructure fault" in o, o)
rc, o = run(probe(base, squeue=["100_3|p1m_PL_A0_1_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("QOS pending reason -> STOP", rc == 3 and "admission" in o, o)
rc, o = run(probe(base, engine=["/x/scratch/runs/PL_A0_1/f/log/island_1.log"])); check("engine resource_limit record -> STOP", rc == 3 and "engine record" in o, o)
os.environ["IGNORE_JOBS"] = "100"; rc, o = run(probe(base, states={M4: "FAILED"})); del os.environ["IGNORE_JOBS"]
check("known-failed job (IGNORE_JOBS) = INFO", rc == 0 and "known-failed" in o, o)
# F2: --soft overrides (soft column only); TABLE and hard column pinned; printed in every verdict
rc, o = run(probe(dict(base, **{M4: 20.0})), "--soft", "prec N2500 m4 I3=21.0"); check("F2 soft override 21.0: m4 20.0 is no soft trip; override printed", rc == 0 and "SOFT TRIP" not in o and "committed soft 18.5 -> 21.0" in o, o)
rc, o = run(probe(base)); check("F2 no override: verdict says 'SOFT OVERRIDES ...: none'", rc == 0 and "SOFT OVERRIDES" in o and "none" in o, o)
rc, o = run(probe(dict(base, **{M4: 31.0})), "--soft", "prec N2500 m4 I3=21.0"); check("F2 the hard line never moves: m4 31 > 30.9 still STOP with an override", rc == 3 and "HARD 30.9" in o, o)
rc, o = run(probe(base), "--soft", "prec N2500 m4 I3=40.0"); check("F2 a soft line above the hard line is refused (rc 64)", rc == 64, o)
rc, o = run(probe(base), "--soft", "no such class=3.0"); check("F2 an unknown class is refused (rc 64)", rc == 64, o)
os.environ["SOFT_OVERRIDES"] = "prec N2500 m4 I3=21.0;A3 n200=5.0"; rc, o = run(probe(dict(base, **{M4: 20.0, A3: 4.5}))); del os.environ["SOFT_OVERRIDES"]
check("F2 env SOFT_OVERRIDES (two classes) works", rc == 0 and "SOFT TRIP" not in o and "A3 n200: committed soft 4.1 -> 5.0" in o, o)
rc, o = run(probe(dict(base, **{M4: 20.0, I0: 9.0, A3: 4.5})), "--soft", "prec N2500 m4 I3=21.0"); check("F2 3 soft trips counted against the overridden lines (m4 no longer trips: 2 trips -> no STOP)", rc == 0 and o.count("SOFT TRIP") == 2, o)
# F6: only this wave's own jobs in squeue
rc, o = run(probe(base, squeue=["999|foreign_job|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("F6 a foreign pending job with a QOS reason is ignored (no false STOP)", rc == 0 and "other jobs of the account ignored: 1" in o, o)
rc, o = run(probe(base, squeue=["100_5|p1m_PL_A0_1_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("F6 own job (base id 100) pending on QOS -> STOP", rc == 3 and "admission" in o, o)
rc, o = run(probe(base, squeue=["100_[9-16%8]|p1m_PL_A0_1_islands|PENDING|JobArrayTaskLimit|0:00|4"])); check("own %k array throttle = INFO, printed once as 'INFO ...' (no 'INFO INFO')", rc == 0 and "INFO own array throttle" in o and "INFO INFO" not in o, o)
# WAVE STATE (explicit line every probe): ENDED = no squeue row of the wave AND every sacct row terminal AND every submitted job id seen in sacct
rc, o = run(probe(base)); check("WAVE STATE: all COMPLETED, empty squeue -> ENDED", "WAVE STATE: ENDED" in o and "WAVE STATE: RUNNING" not in o, o)
rc, o = run(probe(base, squeue=["100_5|p1m_PL_A0_1_islands|RUNNING|None|1:00|4"])); check("WAVE STATE: an own squeue row -> RUNNING", "WAVE STATE: RUNNING" in o and "1 squeue row" in o, o)
rc, o = run(probe(base, states={A3: "RUNNING"})); check("WAVE STATE: a RUNNING sacct row -> RUNNING", "WAVE STATE: RUNNING" in o and "non-terminal" in o, o)
rc, o = run(probe(base, states={A3: "PENDING"})); check("WAVE STATE: a PENDING sacct row -> RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = run(probe(base, extra_sacct=["100_[9-16%8]|p1m_PL_A0_1_islands|PENDING|0|4|0|00:30:00"])); check("WAVE STATE: a pending array row [a-b%k] -> RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = run(probe(base, squeue=["999|foreign|RUNNING|None|1:00|4"])); check("WAVE STATE: a foreign job in squeue does not keep the wave RUNNING", "WAVE STATE: ENDED" in o, o)
rc, o = run(probe(base, states={A3: "FAILED"})); check("WAVE STATE: a failed (terminal) stage -> ENDED, and still STOP", "WAVE STATE: ENDED" in o and rc == 3, o)
pth = probe(base); txt = [l for l in open(pth).read().split("\n") if not l.startswith("110_")]; open(pth, "w").write("\n".join(txt))
rc, o = run(pth); check("WAVE STATE: a submitted job id with no sacct row yet -> RUNNING", "WAVE STATE: RUNNING" in o and "not in sacct yet" in o, o)
pth = probe(base); txt = []; sec = None
for l in open(pth).read().split("\n"):
    if l.startswith("### "): sec = l
    if sec == "### SACCT" and not l.startswith("###"): continue
    txt.append(l)
open(pth, "w").write("\n".join(txt)); rc, o = run(pth); check("WAVE STATE: submitted but no sacct row at all -> RUNNING (never ENDED on an empty wave)", "WAVE STATE: RUNNING" in o and "no sacct row yet" in o, o)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# Boundary wave B1 (ADDENDUM_1): PL_B1_1 = V s1, s2 (class ARweak n100); PL_B1_2 = T s1, s2 (law mode, no class row, report above 172.5, T arm identity, BUILD_T)
LEGT = "7" * 64; LOGB = os.path.join(TMP, "deploy_leg_b1.log")
open(LOGB, "w").write("2026-11-20T10:00:00Z\tPL_A0_1\tBUILD\t%s\teefcbc4a\tsapphirerapids\t1\t6000\ttest\n2026-11-21T10:00:00Z\tPL_B1_2\tBUILD_T\t%s\teefcbc4a\tportable\t1\t6000\ttest\n" % (LEG, LEGT))
V1, V2, T1, T2 = ("4-ARweak-n100-r91-V-s1", "4-ARweak-n100-r91-V-s2", "4-ARweak-n100-r91-T-s1", "4-ARweak-n100-r91-T-s2")
BB = {V1: "PL_B1_1", V2: "PL_B1_1", T1: "PL_B1_2", T2: "PL_B1_2"}; OB = {"PL_B1_1": [V1, V2], "PL_B1_2": [T1, T2]}
def probe_b1(costs, states=None, calib=None, xy=None, binsha=None, dbin=None, squeue=()):
    L = ["### META utc=2026-11-22T11:00:00Z"]; off = 200
    for b in OB:
        L += ["### SUBMISSIONS " + b, json.dumps({"stage": "setup", "fit": "all", "job": str(off), "submitted_utc": "x"})]; off += 10
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]; off = 200
    for b, rs in OB.items():
        for i, r in enumerate(rs, 1):
            L.append("%d_%d|p1m_%s_setup|%s|60|8|%d|01:00:00" % (off, i, b, (states or {}).get(r, "COMPLETED"), int(costs.get(r, 0) * 3600)))
        off += 10
    L.append("### DATA_HASH")
    for r in (V1, V2, T1, T2):
        x, y = (xy or {}).get(r, ("a" * 64, "b" * 64)); L.append("%s|%s|c|%s|%s|%s" % (BB[r], r, x, y, (dbin or {}).get(r, LEGT if r in (T1, T2) else LEG)))
    L.append("### CALIB")
    for r in (V1, V2, T1, T2):
        rec = {"N": 10000, "rule": "coded", "I_max": 3, "refine_m": 1, "status": "completed", "cal_status": "ok", "source": "calib.bin.json settings"} if r in (T1, T2) else \
              {"N": 2500, "rule": "bounded", "I_max": 3, "refine_m": 1, "I_used": 3, "status": "completed", "cal_status": "ok", "source": "calib_meta.json"}
        rec.update((calib or {}).get(r, {})); L.append("%s|%s|%s" % (BB[r], r, json.dumps(rec)))
    L += ["### ISLAND_T"] + ["%s|%s|%d" % (BB[r], r, 21) for r in (V1, V2)] + ["### DIAG"] + ["%s|%s|3|12" % (BB[r], r) for r in (V1, V2)]
    L += ["### BINSHA"] + ["PL_B1_1|%s" % (binsha or {}).get("PL_B1_1", LEG), "PL_B1_2|%s" % (binsha or {}).get("PL_B1_2", LEGT)] + ["### ENGINE_FLAGS"]
    pth = os.path.join(TMP, "probe_b1.txt"); open(pth, "w").write("\n".join(L) + "\n"); return pth
def runb(pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_prec.py"), pth, "--wave", "B1", "--plans", PLANS, "--leg-log", LOGB,
                        "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
bb = {V1: 1.4, V2: 1.5, T1: 60.0, T2: 45.0}
rc, o = runb(probe_b1(bb)); check("B1 healthy: V ARweak n100 + T fits (60, 45): no stop, T rows have no class lines", rc == 0 and "no stop rule fired" in o and "T law" in o and "REPORT" not in o and "quote 115 -> stop > 230" in o, o)
rc, o = runb(probe_b1(dict(bb, **{T1: 180.0}))); check("B1 a T fit at 180 > 172.5: REPORT line, report-and-continue, rc 0", rc == 0 and "REPORT T fit" in o and "STOP" not in o, o)
rc, o = runb(probe_b1(dict(bb, **{T1: 112.0, T2: 100.0}))); check("B1 T fits under 172.5 (112, 100; wave 215 < 230): no report (a T fit is never class soft/hard-tripped)", rc == 0 and "REPORT" not in o and "SOFT" not in o.replace("SOFT OVERRIDES", ""), o)
rc, o = runb(probe_b1(dict(bb, **{V1: 3.2}))); check("B1 V ARweak n100: 3.2 > soft 3.0 -> SOFT TRIP only", rc == 0 and "SOFT TRIP" in o, o)
rc, o = runb(probe_b1(dict(bb, **{V2: 3.5}))); check("B1 V ARweak n100: 3.5 > hard 3.4 -> STOP", rc == 3 and "HARD 3.4" in o, o)
rc, o = runb(probe_b1(dict(bb, **{T1: 150.0, T2: 90.0}))); check("B1 wave 240 > 2 x 115 = 230 -> STOP", rc == 3 and "2 x quote 115" in o, o)
rc, o = runb(probe_b1(dict(bb, **{T1: 120.0, T2: 90.0}))); check("B1 wave 213 (< 230): no STOP", rc == 0, o)
rc, o = runb(probe_b1(bb, calib={T1: {"N": 40000}})); check("B1 T arm identity: tier 1 N = 40,000 is valid (10^4 x 4^1)", rc == 0 and "T ARM IDENTITY" not in o, o)
rc, o = runb(probe_b1(bb, calib={T1: {"N": 160000}})); check("B1 T arm identity: N = 160,000 (tier 2) valid", rc == 0, o)
rc, o = runb(probe_b1(bb, calib={T1: {"N": 20000}})); check("B1 T arm identity: N = 20,000 is not 10^4 x 4^k -> STOP", rc == 3 and "T ARM IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, calib={T2: {"rule": "bounded", "N": 2500}})); check("B1 T arm identity: rule 'bounded' on a T fit -> STOP", rc == 3 and "T ARM IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, calib={V1: {"rule": "coded"}})); check("B1 V arm identity still enforced (V with rule coded -> STOP)", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, binsha={"PL_B1_2": LEG})); check("B1 build identity: the T batch carrying the V build sha -> STOP", rc == 3 and "BUILD IDENTITY" in o and "T build" in o, o)
rc, o = runb(probe_b1(bb, binsha={"PL_B1_1": LEGT})); check("B1 build identity: the V batch carrying the T build sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, dbin={T2: LEG})); check("B1 build identity: a T fit record with the V sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, dbin={V1: LEGT})); check("B1 build identity: a V fit record with the T sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, xy={T2: ("c" * 64, "b" * 64)})); check("B1 data identity across V and T fits of the dataset -> STOP on a mismatch", rc == 3 and "DATA IDENTITY" in o, o)
rc, o = runb(probe_b1(bb, states={T1: "TIMEOUT"})); check("B1 T calibrate TIMEOUT -> STOP (a non-infrastructure failure)", rc == 3 and "non-infrastructure" in o, o)
rc, o = runb(probe_b1(bb), "--quote", "100"); check("B1 --quote override accepted", rc == 0 and "quote 100" in o, o)
rc2 = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_prec.py"), probe_b1(bb), "--wave", "B1", "--plans", PLANS, "--leg-log", LOG, "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")], capture_output=True, text=True)
check("B1 T batches but no BUILD_T line in the deploy log -> STOP", rc2.returncode == 3 and "no BUILD_T line" in rc2.stdout, rc2.stdout)
rc, o = runb(probe_b1(bb)); check("B1 projection counts the wave's own fits (not in waves.json): printed with fits left", "fits left" in o, o)
rc, o = runb(probe_b1(bb)); check("B1 WAVE STATE ENDED when everything is terminal", "WAVE STATE: ENDED" in o, o)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# FZ (m = 1, I_max = 0 frozen): the S1-S10 quote map of the I0-frozen scenario, the quote floor 5, cum-stop 900 for the science waves, pilot labels
import re as _re
def probe_wave(wave, per_fit=0.2, drop_first=False):
    bs = sorted(d for d in os.listdir(PLANS) if _re.fullmatch(r"PL_%s_\d+" % wave, d)); L = ["### META utc=2026-11-23T11:00:00Z"]; off = 300
    pf = {}
    for b in bs:
        pf[b] = [f["run_id"] for f in json.load(open(os.path.join(PLANS, b, "plan.resolved.json")))["fits"]]
        L += ["### SUBMISSIONS " + b, json.dumps({"stage": "setup", "fit": "all", "job": str(off), "submitted_utc": "x"})]; off += 10
    L += ["### SQUEUE", "### SACCT"]; off = 300
    for b in bs:
        for i, r in enumerate(pf[b], 1):
            L.append("%d_%d|p1m_%s_setup|COMPLETED|60|8|%d|01:00:00" % (off, i, b, int((per_fit(r) if callable(per_fit) else per_fit) * 3600)))
        off += 10
    L += ["### DATA_HASH", "### CALIB", "### ISLAND_T", "### DIAG", "### BINSHA", "### ENGINE_FLAGS"]
    pth = os.path.join(TMP, "probe_wave.txt"); open(pth, "w").write("\n".join(L) + "\n"); return pth
def runw(wave, pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_prec.py"), pth, "--wave", wave, "--plans", PLANS, "--leg-log", LOG,
                        "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
I0MAP = {"S1": 50, "S2": 40, "S3": 5, "S4": 35, "S5": 30, "S6": 15, "S7": 20, "S8": 70, "S9": 35, "S10": 55}
bad = []
for w, q in I0MAP.items():
    rc, o = runw(w, probe_wave(w, 0.01))
    if "quote %d -> stop > %d" % (q, 2 * q) not in o: bad.append((w, q, [l for l in o.split("\n") if l.startswith("wave actual")]))
check("S1-S10 map of the I0-frozen scenario: quote / stop 50/100, 40/80, 5/10, 35/70, 30/60, 15/30, 20/40, 70/140, 35/70, 55/110", not bad, str(bad))
rc, o = runw("S3", probe_wave("S3", 2.9)); check("quote floor: S3 (4 NULL fits at 2.9 = 11.6 > 10) -> STOP on the wave rule although every fit is under its 3.0 line", rc == 3 and "2 x quote 5" in o and "HARD" not in o and "SOFT TRIP" not in o, o)
rc, o = runw("S3", probe_wave("S3", 2.4)); check("quote floor: S3 at 9.6 (< 10): no stop (the stop is not off, and not 0)", rc == 0 and "stop > 10" in o, o)
rc, o = runw("S3", probe_wave("S3", 0.45)); check("S3 at the model (0.45 per fit): no stop", rc == 0, o)
rc, o = runw("S3", probe_wave("S3", 0.1), "--quote", "0"); check("--quote 0 is refused (rc 64): a zero quote must not switch the wave stop off", rc == 64, o)
rc, o = runw("S3", probe_wave("S3", 0.1), "--quote", "-3"); check("--quote -3 is refused (rc 64)", rc == 64, o)
rc, o = runw("S8", probe_wave("S8", 0.01), "--quote", "30"); check("--quote re-quote accepted (S8 30 -> stop > 60)", rc == 0 and "quote 30 -> stop > 60" in o, o)
os.makedirs(os.path.join(TMP, "plans11"), exist_ok=True); lk = os.path.join(TMP, "plans11", "PL_S11_1")
if os.path.lexists(lk): os.remove(lk)
os.symlink(os.path.join(PLANS, "PL_S3_1"), lk)
pw = probe_wave("S3", 0.1); txt = open(pw).read().replace("PL_S3_1", "PL_S11_1"); open(pw, "w").write(txt)
r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_prec.py"), pw, "--wave", "S11", "--plans", os.path.join(TMP, "plans11"), "--leg-log", LOG, "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")], capture_output=True, text=True)
check("a wave without a quote is a STOP (no silent 'no wave stop')", r.returncode == 3 and "no quote for wave S11" in r.stdout, r.stdout)
json.dump({"x": 890.0}, open(os.path.join(TMP, "prior890.json"), "w"))
rc, o = runw("S1", probe_wave("S1", 0.5), "--prior", os.path.join(TMP, "prior890.json")); check("cum-stop default 900 for a science wave: 890 + 14 = 904 -> STOP, line shows cum stop 900", rc == 3 and "cumulative 904" in o and "(cum stop 900)" in o, o)
rc, o = runw("S1", probe_wave("S1", 0.2), "--prior", os.path.join(TMP, "prior890.json")); check("science wave: 890 + 5.6 = 895.6 (< 900) -> no cumulative stop", "STOP cumulative" not in o and "(cum stop 900)" in o, o)
rc, o = runw("S1", probe_wave("S1", 0.5), "--prior", os.path.join(TMP, "prior890.json"), "--cum-stop", "1000"); check("--cum-stop 1000 overrides the science default", "STOP cumulative" not in o and "(cum stop 1000)" in o, o)
rc, o = run(probe(base), "--prior", os.path.join(TMP, "prior890.json")); check("a precision wave keeps the 1,000 default (A0 21.5 + 890 = 911.5: no cumulative stop)", "STOP cumulative" not in o and "(cum stop 1000)" in o, o)
rc, o = runw("S7", probe_wave("S7", 0.01)); check("pilot gate S7: prints 'S7 ... re-quotes S8'", "after S7 ends" in o and "re-quotes S8" in o, o)
rc, o = runw("S9", probe_wave("S9", 0.01)); check("pilot gate S9: re-quotes S10", "re-quotes S10" in o, o)
rc, o = runw("S6", probe_wave("S6", 0.01)); check("S6 is no pilot gate any more (no pilot line)", "pilot gate" not in o, o)
# the committed table is pinned: altering it is a STOP
src = open(os.path.join(HERE, "stop_rules_prec.py")).read().replace('"A3 n200": (2.76, 4.1, 6.9)', '"A3 n200": (2.76, 40.1, 60.9)')
alt = os.path.join(TMP, "stop_rules_prec_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe(base), "--wave", "A0", "--plans", PLANS, "--leg-log", LOG, "--waves-json", os.path.join(STG, "waves.json"), "--ref-hashes", os.path.join(TMP, "refs.json")], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
