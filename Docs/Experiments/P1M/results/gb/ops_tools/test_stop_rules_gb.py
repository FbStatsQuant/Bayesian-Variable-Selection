#!/usr/bin/env python3
"""test_stop_rules_gb.py -- synthetic probes for stop_rules_gb.py (G-B pilot set). Real plans (staging/gb/scripts/GB_G*), no NOTS. Scratch under $GB_TEST_TMP or staging/gb/_t (never /tmp)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE)
TMP = os.environ.get("GB_TEST_TMP", os.path.join(STG, "_t")); os.makedirs(TMP, exist_ok=True)
PLANS = os.path.join(STG, "scripts"); F2SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; OTHER = "c" * 64
LOG = os.path.join(TMP, "deploy_gb.log"); open(LOG, "w").write("2026-11-19T17:56:09Z\tVN_ID_1\tBUILD_F2\t%s\te993ece2\tsapphirerapids\t1\t6165\ttest\n" % F2SHA)
XY = ("e" * 64, "f" * 64)
def fits(wave):
    out = []
    for b in sorted(d for d in os.listdir(PLANS) if d.startswith("GB_%s" % wave) and len(d) == 6):
        for f in json.load(open(os.path.join(PLANS, b, "plan.resolved.json")))["fits"]:
            out.append((b, f))
    return out
def probe(wave, per_fit=1.0, costs=None, states=None, calib=None, xy=None, binsha=None, dbin=None, squeue=(), engine=(), extra_sacct=(), diag=None, islT=None, only=None, sections=None):
    fs = [x for x in fits(wave) if only is None or x[0] in only]; L = ["### META utc=2026-11-23T11:00:00Z"]; off = 300; seen = []
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
        rec = {"N": 10000, "refine_m": 1, "I_max": pm.get("I_max"), "I_used": 0 if pm.get("I_max") == 0 else 3, "rule": "bounded", "source": "calib_meta.json", "status": "completed", "cal_status": "ok",
               "sections": {"grid": "a" * 64, "grid_unrefined": "b" * 64} if pm.get("I_max") == 0 else {"grid": "d" * 64, "grid_unrefined": "b" * 64}}
        rec.update((calib or {}).get(f["run_id"], {})); L.append("%s|%s|%s" % (b, f["run_id"], json.dumps(rec)))
    L += ["### ISLAND_T"] + ["%s|%s|%d" % (b, f["run_id"], (islT or {}).get(f["run_id"], 21)) for b, f in fs]
    L += ["### DIAG"] + ["%s|%s|%d|%d" % (b, f["run_id"], *((diag or {}).get(f["run_id"], (0, 0) if (f.get("params") or {}).get("I_max") == 0 else (3, 12)))) for b, f in fs]
    L += ["### BINSHA"] + ["%s|%s" % (b, (binsha or {}).get(b, F2SHA)) for b in sorted({b for b, _ in fs})] + ["### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_%s.txt" % wave); open(p, "w").write("\n".join(L) + "\n"); return p
def run(wave, pth, *extra, env=None):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gb.py"), pth, "--wave", wave, "--plans", PLANS, "--deploy-log", LOG] + list(extra), capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
A0, A3, J0, J3 = "5-AR-n200-r01-V-s1", "5-AR-n200-r01-VI3-s1", "5-ADJOPP-n200-r01-V-s1", "5-ADJOPP-n200-r01-VI3-s1"
rc, o = run("G1", probe("G1")); check("G1 healthy: no stop, quote 226 -> stop > 450, WAVE STATE ENDED, arm identity on 2 fits", rc == 0 and "no stop rule fired" in o and "quote 226 -> stop > 450" in o and "WAVE STATE: ENDED" in o and "arm identity checked on 2 fits" in o, o)
rc, o = run("G2", probe("G2")); check("G2 healthy: quote 275 -> stop > 550", rc == 0 and "quote 275 -> stop > 550" in o and "WAVE STATE: ENDED" in o, o)
rc, o = run("G1", probe("G1", costs={A0: 163.0}, per_fit=1.0)); check("soft trip AR pilot 163 > 162: reported, continues (exit 0)", rc == 0 and "SOFT TRIP" in o and A0 in o, o)
rc, o = run("G1", probe("G1", costs={A0: 270.5})); check("hard: AR pilot 270.5 > 270 -> STOP", rc == 3 and "HARD 270" in o, o)
rc, o = run("G1", probe("G1", costs={A0: 269.0}, per_fit=1.0)); check("AR pilot 269 <= hard 270 -> soft trip only", rc == 0 and "SOFT TRIP" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)
rc, o = run("G1", probe("G1", costs={A3: 295.5})); check("hard: AR twin 295.5 > 295 -> STOP", rc == 3 and "HARD 295" in o, o)
rc, o = run("G2", probe("G2", costs={J0: 333.5})); check("hard: ADJ-OPP pilot 333.5 > 333 -> STOP", rc == 3 and "HARD 333" in o, o)
rc, o = run("G2", probe("G2", costs={J3: 355.5})); check("hard: ADJ-OPP twin 355.5 > 355 -> STOP", rc == 3 and "HARD 355" in o, o)
rc, o = run("G1", probe("G1", costs={A0: 226.0, A3: 226.0})); check("wave actual 452 > G1 stop 450 -> STOP (both fits under their hard lines)", rc == 3 and "wave stop 450" in o and "HARD" not in o, o)
rc, o = run("G1", probe("G1", costs={A0: 225.0, A3: 224.0})); check("wave actual 449 <= 450: no wave stop", rc == 0 and "wave stop" not in o, o)
rc, o = run("G2", probe("G2", costs={J0: 275.0, J3: 276.0})); check("G2 wave actual 551 > 550 -> STOP", rc == 3 and "wave stop 550" in o, o)
rc, o = run("G1", probe("G1", costs={A0: 200.0, A3: 200.0}), "--quote", "250"); check("--quote 250 -> stop > 500: 400 no stop", rc == 0 and "stop > 500" in o, o)
open(os.path.join(TMP, "prior.json"), "w").write(json.dumps({"5-AR-n200-r01-V-s1": 400.0, "5-AR-n200-r01-VI3-s1": 300.0}))
rc, o = run("G2", probe("G2", per_fit=40.0), "--prior", os.path.join(TMP, "prior.json")); check("cumulative 700 + 80 = 780 <= 800 -> no stop", rc == 0, o)
rc, o = run("G2", probe("G2", per_fit=51.0), "--prior", os.path.join(TMP, "prior.json")); check("cumulative 700 + 102 = 802 > 800 -> STOP", rc == 3 and "cumulative" in o, o)
rc, o = run("G1", probe("G1", only=("GB_G1a",)), "--prior", os.path.join(TMP, "prior.json")); check("projection counts the fits not started (G2 pair): spent 701 + E 275 > 800 -> STOP", rc == 3 and "projection" in o, o)
rc, o = run("G1", probe("G1", states={A3: "FAILED"})); check("FAILED stage -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = run("G1", probe("G1", states={A3: "TIMEOUT"})); check("TIMEOUT -> STOP", rc == 3, o)
rc, o = run("G1", probe("G1", states={A3: "OUT_OF_MEMORY"})); check("OUT_OF_MEMORY -> STOP", rc == 3 and "OUT_OF_MEMORY" in o, o)
rc, o = run("G1", probe("G1", states={A3: "NODE_FAIL"})); check("NODE_FAIL = INFO, not a stop", rc == 0 and "infrastructure fault" in o, o)
rc, o = run("G1", probe("G1", calib={A0: {"N": 2500}})); check("arm identity: recorded N 2,500 != 10,000 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("G1", probe("G1", calib={A3: {"I_max": 0}})); check("arm identity: twin recorded I_max 0 != plan 3 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("G1", probe("G1", calib={A0: {"refine_m": 4}})); check("arm identity: refine_m 4 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("G1", probe("G1", calib={A0: {"rule": "unbounded"}})); check("arm identity: rule != bounded -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("G1", probe("G1", diag={A0: (0, 2)})); check("I_max 0 with cost_diag files -> FLAG, exit 0", rc == 0 and "FLAG behaviour" in o and "cost_diag" in o, o)
rc, o = run("G1", probe("G1", diag={A3: (1, 12)})); check("I_max 3: largest diag index != I_used -> FLAG", rc == 0 and "FLAG behaviour" in o, o)
rc, o = run("G1", probe("G1", islT={A0: 17})); check("grid identity T != n_unrefined - 1 -> FLAG (grid_n/unrefined not in fixture: no flag)", rc == 0, o)
rc, o = run("G1", probe("G1", xy={A3: ("1" * 64, "2" * 64)})); check("data identity: pilot and twin X/y differ -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
rc, o = run("G1", probe("G1", binsha={"GB_G1a": OTHER})); check("build identity: batch bin sha != BUILD_F2 -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run("G1", probe("G1", dbin={A0: OTHER})); check("build identity: a fit's recorded binary sha != BUILD_F2 -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run("G1", probe("G1", engine=["/x/OUTCOME"])); check("OUTCOME / resource_limit record -> STOP", rc == 3 and "engine record" in o, o)
rc, o = run("G1", probe("G1", squeue=["1001_1|p1m_GB_G1a_calibrate|PENDING|QOSMaxCpuPerUserLimit|0:00|64"], states={A0: "PENDING"})); check("foreign job with a QOS reason ignored (not our job id)", rc == 0, o)
rc, o = run("G1", probe("G1", squeue=["300_1|p1m_GB_G1a_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|32"])); check("own job with a QOS pending reason -> STOP", rc == 3 and "QOS" in o, o)
rc, o = run("G1", probe("G1", only=("GB_G1a",))); check("only batch a submitted and terminal: WAVE STATE RUNNING (batch b not submitted yet), exit 0", rc == 0 and "WAVE STATE: RUNNING" in o and "GB_G1b" in o and "not submitted yet" in o, o)
rc, o = run("G1", probe("G1", states={A0: "RUNNING"})); check("a RUNNING sacct row -> WAVE STATE RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = run("G1", probe("G1", extra_sacct=["300_1|p1m_GB_G1a_islands|COMPLETED|700|48|1|00:45:00"])); check("INFO: island task 700 s outside 288-496 s", rc == 0 and "INFO island wall" in o, o)
rc, o = run("G1", probe("G1", extra_sacct=["300_1|p1m_GB_G1a_islands|COMPLETED|2200|48|1|00:45:00"])); check("INFO: task at 81 % of its limit", rc == 0 and "% of its limit" in o, o)
rc, o = run("G1", probe("G1", extra_sacct=["300_1|p1m_GB_G1a_islands|COMPLETED|400|48|1|00:45:00"])); check("island 400 s inside 288-496 s and 15 % of limit: no INFO", rc == 0 and "INFO island wall" not in o and "% of its limit" not in o, o)
rc, o = run("G1", probe("G1"), "--soft", "x=1"); check("--soft is an unknown option here (the G-B table has no overrides)", rc != 0, o)
src = open(os.path.join(HERE, "stop_rules_gb.py")).read().replace('"gb AR n200 N10000 I0": (108.0, 162.0, 270.0)', '"gb AR n200 N10000 I0": (108.0, 1620.0, 2700.0)'); alt = os.path.join(TMP, "stop_rules_gb_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe("G1"), "--wave", "G1", "--plans", PLANS, "--deploy-log", LOG], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
_t = open(probe("G1")).read()
p1 = os.path.join(TMP, "p_rc255_full.txt"); open(p1, "w").write(_t + "### REMOTE_RC\n255\n### REMOTE_STDERR\nboom\n")
rc, o = run("G1", p1); check("remote rc 255 but all sections present -> INFO only, exit 0", rc == 0 and "INFO remote ssh exit status 255" in o, o)
p2 = os.path.join(TMP, "p_trunc.txt"); open(p2, "w").write(_t.split("### DATA_HASH")[0] + "### REMOTE_RC\n255\n### REMOTE_STDERR\n")
rc, o = run("G1", p2); check("truncated probe -> FLAG PROBE ERROR, exit 4, verdict PROBE ERROR", rc == 4 and "FLAG PROBE ERROR" in o and "PROBE ERROR: stop rules not fully evaluated" in o, o)
p3 = os.path.join(TMP, "p_refetch.txt"); open(p3, "w").write(_t + "### REMOTE_RC\n0\n### REMOTE_NOTE\nfirst ssh rc 255 (connection cut); re-fetched\n### REMOTE_STDERR\n")
rc, o = run("G1", p3); check("re-fetched complete probe -> INFO probe transport, exit 0", rc == 0 and "INFO probe transport" in o, o)
p4 = os.path.join(TMP, "p_pyerr.txt"); open(p4, "w").write(_t.split("### DATA_HASH")[0] + "".join("### %s\n" % k for k in ("DATA_HASH", "CALIB", "ISLAND_T", "DIAG", "BINSHA", "ENGINE_FLAGS")) + "### PYERR\npython3 section exited 1\n### REMOTE_RC\n0\n")
rc, o = run("G1", p4); check("remote python failure with all headers -> FLAG PROBE ERROR, exit 4", rc == 4 and "remote python section failed" in o, o)
rc, o = run("G1", probe("G1")); check("pair INFO is printed (pilot vs twin calib sections)", "INFO pair 5-AR-n200-r01" in o, o)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
