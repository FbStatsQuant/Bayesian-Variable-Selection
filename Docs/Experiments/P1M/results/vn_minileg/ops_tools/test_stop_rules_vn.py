#!/usr/bin/env python3
"""test_stop_rules_vn.py -- synthetic probes for stop_rules_vn.py (V-N mini-leg). Real plans (F2_vn/scripts/VN_V*_*), real leg twin records (read-only) for the pairing identity.
Scratch under $VN_TEST_TMP or staging/vn_minileg/_t (never /tmp)."""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE)
TMP = os.environ.get("VN_TEST_TMP", os.path.join(STG, "_t")); os.makedirs(TMP, exist_ok=True)
PLANS = os.path.join(STG, "current", "scripts"); LEGREC = "/home/fb31/SMC_Engineering_Department/records/precision1e4"
F2SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; OTHER = "c" * 64
LOG = os.path.join(TMP, "deploy_F2.log"); open(LOG, "w").write("2026-11-19T17:56:09Z\tVN_ID_1\tBUILD_F2\t%s\te993ece2\tsapphirerapids\t1\t6165\ttest\n" % F2SHA)
XY = ("e" * 64, "f" * 64)
def fits(wave):
    out = []
    for b in sorted(d for d in os.listdir(PLANS) if d.startswith("VN_%s_" % wave)):
        for f in json.load(open(os.path.join(PLANS, b, "plan.resolved.json")))["fits"]:
            out.append((b, f))
    return out
def twin_sections(rid):
    import re
    m = re.match(r"^(4-\w+-n200-r01)-P-N10000-m1(-I0)?-c(\d)-s1$", rid)
    tw = ("%s-P-N2500-m1%s-c%s-s1" % (m.group(1), m.group(2) or "", m.group(3))) if m else rid.replace("-XB2-s1", "-c1-s1")
    p = glob.glob("%s/*/%s/calib_meta.json" % (LEGREC, tw))[0]
    return {x["name"]: x["sha256"] for x in json.load(open(p))["sections"] if x["name"] != "meta"}
def probe(wave, per_fit=1.0, costs=None, states=None, calib=None, xy=None, binsha=None, dbin=None, squeue=(), engine=(), extra_sacct=(), diag=None, islT=None, pair_break=None):
    fs = fits(wave); L = ["### META utc=2026-11-23T11:00:00Z"]; off = 300; seen = []
    for b in sorted({b for b, _ in fs}):
        L += ["### SUBMISSIONS " + b, json.dumps({"stage": "setup", "fit": "all", "job": str(off), "submitted_utc": "x"})]; seen.append((b, off)); off += 10
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]
    for b, o in seen:
        for i, (bb, f) in enumerate([x for x in fs if x[0] == b], 1):
            c = (costs or {}).get(f["run_id"], per_fit)
            L.append("%d_%d|p1m_%s_setup|%s|60|8|%d|01:00:00" % (o, i, b, (states or {}).get(f["run_id"], "COMPLETED"), int(c * 3600)))
    L += list(extra_sacct)
    L.append("### DATA_HASH")
    for b, f in fs:
        x, y = (xy or {}).get(f["run_id"], XY); L.append("%s|%s|c|%s|%s|%s" % (b, f["run_id"], x, y, (dbin or {}).get(f["run_id"], F2SHA)))
    L.append("### CALIB")
    for b, f in fs:
        pm = f.get("params") or {}
        rec = {"N": 10000 if "-N10000-" in f["run_id"] else 2500, "refine_m": 1, "I_max": pm.get("I_max"), "I_used": 0 if pm.get("I_max") == 0 else 3, "rule": "bounded", "source": "calib_meta.json",
               "status": "completed", "cal_status": "ok"}
        if "-P-" in f["run_id"]:
            sec = dict(twin_sections(f["run_id"]))
            if pair_break == f["run_id"]: sec["grid"] = "0" * 64
            rec["sections"] = sec
        rec.update((calib or {}).get(f["run_id"], {})); L.append("%s|%s|%s" % (b, f["run_id"], json.dumps(rec)))
    L += ["### ISLAND_T"] + ["%s|%s|%d" % (b, f["run_id"], (islT or {}).get(f["run_id"], 21)) for b, f in fs]
    L += ["### DIAG"] + ["%s|%s|%d|%d" % (b, f["run_id"], *((diag or {}).get(f["run_id"], (0, 0) if (f.get("params") or {}).get("I_max") == 0 else (3, 12)))) for b, f in fs]
    L += ["### BINSHA"] + ["%s|%s" % (b, (binsha or {}).get(b, F2SHA)) for b in sorted({b for b, _ in fs})] + ["### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_%s.txt" % wave); open(p, "w").write("\n".join(L) + "\n"); return p
def run(wave, pth, *extra, env=None):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_vn.py"), pth, "--wave", wave, "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(TMP, "refs.json"),
                        "--leg-records", LEGREC] + list(extra), capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr
refs = {"4-AR-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]}, "4-ARweak-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]}, "4-ADJOPP-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]},
        "4-ADJOPP-n200-r04": {"X_sha256": XY[0], "y_sha256": XY[1]}}
json.dump(refs, open(os.path.join(TMP, "refs.json"), "w"))
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
I0 = "4-AR-n200-r01-P-N10000-m1-I0-c1-s1"; I3 = "4-AR-n200-r01-P-N10000-m1-c1-s1"; XB2 = "4-AR-n200-r01-P-N2500-m1-I0-XB2-s1"; R3 = "4-ADJOPP-n200-r04-VI3-s1"; R0 = "4-ADJOPP-n200-r04-V-s2"
# ---- committed table, pinned -------------------------------------------------------------------------------------------------------------------------
import importlib.util as _u
_sp = _u.spec_from_file_location("srv", os.path.join(HERE, "stop_rules_vn.py")); m = _u.module_from_spec(_sp); _sp.loader.exec_module(m)
check("the committed class table is the plan's (E / soft / hard)", m.TABLE == {"vn N10000 m1 I0": (19.06, 28.6, 47.6), "vn N10000 m1 I3": (20.68, 31.0, 51.7), "XB2": (5.71, 8.6, 14.3), "r04 pair": (1.99, 3.0, 5.0)}, str(m.TABLE))
check("quotes 50 / 75 / 125, cumulative 400, projection 600", m.QUOTE == {"V0": 50.0, "V1": 75.0, "V2": 125.0} and m.CUM_STOP == 400.0 and m.PROJ_STOP == 600.0)
check("class map: all 15 plan fits map to a class", all(m.klass(f["run_id"]) in m.TABLE for w in ("V0", "V1", "V2") for _, f in fits(w)), str([f["run_id"] for w in ("V0","V1","V2") for _, f in fits(w) if m.klass(f["run_id"]) not in m.TABLE]))
# ---- healthy waves ---------------------------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", 1.0)); check("V0 healthy: no stop; quote 50 -> stop > 100; pairing checked on 3 fits (2 N 10^4 + XB2); WAVE STATE ENDED", rc == 0 and "no stop rule fired" in o and "quote 50 -> stop > 100" in o and "pairing identity checked on 3 fits" in o and "WAVE STATE: ENDED" in o, o)
rc, o = run("V1", probe("V1", 1.0)); check("V1 healthy: quote 75 -> stop > 150; pairing on 4 fits", rc == 0 and "quote 75 -> stop > 150" in o and "pairing identity checked on 4 fits" in o, o)
rc, o = run("V2", probe("V2", 1.0)); check("V2 healthy: quote 125 -> stop > 250; pairing on 6 fits", rc == 0 and "quote 125 -> stop > 250" in o and "pairing identity checked on 6 fits" in o, o)
# ---- per-fit soft / hard (committed lines) ---------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", 1.0, {I0: 29.0})); check("soft trip: N10^4 I0 fit 29 > 28.6: reported, continues", rc == 0 and "SOFT TRIP" in o, o)
rc, o = run("V0", probe("V0", 1.0, {I0: 47.7})); check("hard trip: N10^4 I0 fit 47.7 > 47.6 -> STOP", rc == 3 and "HARD 47.6" in o, o)
rc, o = run("V0", probe("V0", 1.0, {I3: 51.8})); check("hard trip: N10^4 I3 fit 51.8 > 51.7 -> STOP", rc == 3 and "HARD 51.7" in o, o)
rc, o = run("V0", probe("V0", 1.0, {XB2: 14.4})); check("hard trip: XB2 14.4 > 14.3 -> STOP", rc == 3 and "HARD 14.3" in o, o)
rc, o = run("V0", probe("V0", 1.0, {R3: 5.1})); check("hard trip: r04 fit 5.1 > 5.0 -> STOP", rc == 3 and "HARD 5.0" in o, o)
rc, o = run("V0", probe("V0", 1.0, {I0: 30.0, I3: 32.0, XB2: 9.0})); check("3 soft trips in the wave -> STOP", rc == 3 and "3 soft trips" in o, o)
rc, o = run("V0", probe("V0", 1.0, {I0: 30.0}), "--soft", "vn N10000 m1 I0=35.0"); check("--soft override (soft column only): 30 < 35 no trip; printed", rc == 0 and "SOFT TRIP" not in o and "committed soft 28.6 -> 35.0" in o, o)
rc, o = run("V0", probe("V0", 1.0, {I0: 48.0}), "--soft", "vn N10000 m1 I0=35.0"); check("--soft: the hard line never moves (48 > 47.6 still STOP)", rc == 3 and "HARD 47.6" in o, o)
rc, o = run("V0", probe("V0", 1.0), "--soft", "vn N10000 m1 I0=60.0"); check("--soft above the hard line refused (rc 64)", rc == 64, o)
# ---- wave / cumulative / projection ---------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", 1.0, {I0: 25.0, I3: 25.0, XB2: 8.0, R3: 2.9, R0: 2.9})); check("V0 wave 63.8 < 100: no wave stop", "2 x quote" not in o, o)
rc, o = run("V0", probe("V0", 1.0, {I0: 28.0, I3: 30.0, XB2: 8.0, R3: 2.9, R0: 2.9}), "--quote", "30"); check("--quote re-quote 30 -> stop > 60: wave 71.8 -> STOP", rc == 3 and "2 x quote 30" in o, o)
rc, o = run("V0", probe("V0", 1.0), "--quote", "0"); check("--quote 0 refused (rc 64)", rc == 64, o)
json.dump({"x": 395.0}, open(os.path.join(TMP, "prior395.json"), "w")); rc, o = run("V0", probe("V0", 1.0), "--prior", os.path.join(TMP, "prior395.json")); check("cumulative: 395 + 5 fits x 1.0 = 400 -> not above 400: no STOP; 395 + 6 > 400 -> STOP", "STOP cumulative" not in o, o)
rc, o = run("V0", probe("V0", 1.2), "--prior", os.path.join(TMP, "prior395.json")); check("cumulative: 395 + 6.0 = 401 > 400 -> STOP", rc == 3 and "STOP cumulative 401" in o, o)
json.dump({"y": 560.0}, open(os.path.join(TMP, "prior560.json"), "w")); rc, o = run("V0", probe("V0", 1.0), "--prior", os.path.join(TMP, "prior560.json")); check("projection ceiling 600: 560 + 5 + the 10 fits left at table E (~200) -> STOP", rc == 3 and "STOP projection" in o, o)
# ---- arm identity ------------------------------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", calib={I0: {"N": 2500}})); check("ARM IDENTITY: an N 10^4 fit recorded with N 2,500 (the default-N lesson) -> STOP", rc == 3 and "ARM IDENTITY" in o and "'N': 2500" in o, o)
rc, o = run("V0", probe("V0", calib={XB2: {"N": 10000}})); check("ARM IDENTITY: XB2 recorded with N 10,000 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("V0", probe("V0", calib={I0: {"I_max": 3}})); check("ARM IDENTITY: I_max 0 fit recorded I_max 3 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("V0", probe("V0", calib={I3: {"refine_m": 4}})); check("ARM IDENTITY: refine_m 4 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("V0", probe("V0", calib={R3: {"I_max": 0}})); check("ARM IDENTITY: the r04 I_max-3 twin recorded I_max 0 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("V0", probe("V0", diag={I0: (1, 3)})); check("behaviour: I_max 0 with cost_diag files -> FLAG only", rc == 0 and "FLAG behaviour" in o and "I_max = 0" in o, o)
rc, o = run("V0", probe("V0", calib={I3: {"I_used": 2}})); check("behaviour: I_max 3, I_used 2, diag max k 3 -> FLAG only", rc == 0 and "I_used = 2" in o, o)
rc, o = run("V0", probe("V0", calib={I3: {"grid_n": 22, "grid_unrefined_n": 22}}, islT={I3: 21})); check("grid identity T = n_unrefined - 1 holds (21): no flag", rc == 0 and "behaviour" not in o, o)
rc, o = run("V0", probe("V0", calib={I3: {"grid_n": 22, "grid_unrefined_n": 22}}, islT={I3: 30})); check("grid identity fails (T 30): FLAG only", rc == 0 and "FLAG behaviour" in o, o)
# ---- PAIRING identity ----------------------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", pair_break=I0)); check("PAIRING: the N 10^4 I0 fit's grid section differs from its twin -> STOP naming the grid", rc == 3 and "PAIRING IDENTITY" in o and "grid section" in o, o)
rc, o = run("V0", probe("V0", pair_break=XB2)); check("PAIRING: XB2 vs its leg arm: sections differ -> STOP", rc == 3 and "PAIRING IDENTITY" in o, o)
rc, o = run("V0", probe("V0", calib={I3: {"sections": {}}})); check("PAIRING: no calib_meta sections yet -> INFO only (not a stop)", rc == 0 and "pairing identity not checked" in o, o)
# ---- data / build identity ---------------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", xy={I3: ("1" * 64, XY[1])})); check("DATA IDENTITY: X differs inside the dataset (and from the record) -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
rc, o = run("V0", probe("V0", binsha={"VN_V0_2": OTHER})); check("BUILD IDENTITY: a batch binary sha != BUILD_F2 -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run("V0", probe("V0", dbin={I0: OTHER})); check("BUILD IDENTITY: a fit record with the F build sha (d0c30b65) -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
# ---- failures, admission, WAVE STATE ------------------------------------------------------------------------------------------------------------------
rc, o = run("V0", probe("V0", states={XB2: "FAILED"})); check("FAILED stage -> STOP (and WAVE STATE ENDED)", rc == 3 and "non-infrastructure" in o and "WAVE STATE: ENDED" in o, o)
rc, o = run("V0", probe("V0", states={XB2: "NODE_FAIL"})); check("NODE_FAIL = INFO only", rc == 0 and "infrastructure fault" in o, o)
rc, o = run("V0", probe("V0", squeue=["300_5|p1m_VN_V0_1_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("QOS pending reason on the wave's own job -> STOP", rc == 3 and "admission" in o, o)
rc, o = run("V0", probe("V0", squeue=["999|foreign|PENDING|QOSMaxCpuPerUserLimit|0:00|8"])); check("a foreign job on QOS is ignored", rc == 0 and "other jobs of the account ignored: 1" in o and "WAVE STATE: ENDED" in o, o)
rc, o = run("V0", probe("V0", squeue=["300_[9-64%32]|p1m_VN_V0_1_islands|PENDING|JobArrayTaskLimit|0:00|4"])); check("own %k array throttle = INFO; wave RUNNING", rc == 0 and "own array throttle" in o and "WAVE STATE: RUNNING" in o, o)
rc, o = run("V0", probe("V0", engine=["/x/log/island_1.log"])); check("engine resource_limit record -> STOP", rc == 3 and "engine record" in o, o)
rc, o = run("V0", probe("V0", states={XB2: "RUNNING"})); check("a RUNNING sacct row -> WAVE STATE RUNNING", "WAVE STATE: RUNNING" in o, o)
# ---- the pinned table ------------------------------------------------------------------------------------------------------------------------------
src = open(os.path.join(HERE, "stop_rules_vn.py")).read().replace('"XB2": (5.71, 8.6, 14.3)', '"XB2": (5.71, 80.6, 140.3)'); alt = os.path.join(TMP, "stop_rules_vn_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe("V0"), "--wave", "V0", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(TMP, "refs.json"), "--leg-records", LEGREC], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
