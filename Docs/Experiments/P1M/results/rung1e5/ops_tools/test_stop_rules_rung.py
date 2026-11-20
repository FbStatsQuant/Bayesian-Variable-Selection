#!/usr/bin/env python3
"""test_stop_rules_rung.py -- synthetic probes for stop_rules_rung.py (10^5 rung). Real plans (staging/rung1e5/scripts/RG_*), no NOTS. Scratch under $RUNG_TEST_TMP or staging/rung1e5/_t (never /tmp)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE)
TMP = os.environ.get("RUNG_TEST_TMP", os.path.join(STG, "_t")); os.makedirs(TMP, exist_ok=True)
PLANS = os.path.join(STG, "scripts"); F2SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; OTHER = "c" * 64
LOG = os.path.join(TMP, "deploy_rung.log"); open(LOG, "w").write("2026-11-19T17:56:09Z\tVN_ID_1\tBUILD_F2\t%s\te993ece2\tsapphirerapids\t1\t6165\ttest\n" % F2SHA)
XY = ("e" * 64, "f" * 64); REFS = os.path.join(TMP, "refs.json")
json.dump({"5-AR-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]}, "5-ADJOPP-n200-r01": {"X_sha256": XY[0], "y_sha256": XY[1]}}, open(REFS, "w"))
WAVES = {"R1": ["RG_1a", "RG_1b", "RG_T6"], "R2": ["RG_2a", "RG_2b"], "R3": ["RG_3a", "RG_3b"]}
def fits(wave, only=None):
    out = []
    for b in WAVES[wave]:
        if only is not None and b not in only: continue
        for f in json.load(open(os.path.join(PLANS, b, "plan.resolved.json")))["fits"]:
            out.append((b, f))
    return out
def probe(wave, per_fit=1.0, costs=None, states=None, calib=None, xy=None, binsha=None, dbin=None, squeue=(), engine=(), extra_sacct=(), diag=None, only=None):
    """costs / states / calib / xy / dbin keyed by 'batch/run_id' or by run_id (not for T6)"""
    fs = fits(wave, only); L = ["### META utc=2026-11-23T11:00:00Z"]; off = 300; seen = []
    g = lambda d, b, rid, dflt: (d or {}).get(b + "/" + rid, (d or {}).get(rid, dflt))
    for b in dict.fromkeys(b for b, _ in fs):
        L += ["### SUBMISSIONS " + b, json.dumps({"stage": "t6" if b == "RG_T6" else "setup", "fit": "all", "job": str(off), "submitted_utc": "x"})]; seen.append((b, off)); off += 10
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]
    for b, o in seen:
        for i, (bb, f) in enumerate([x for x in fs if x[0] == b], 1):
            L.append("%d_%d|p1m_%s_setup|%s|60|8|%d|01:00:00" % (o, i, b, g(states, b, f["run_id"], "COMPLETED"), int(g(costs, b, f["run_id"], per_fit) * 3600)))
    L += list(extra_sacct)
    L.append("### DATA_HASH")
    for b, f in fs:
        if b == "RG_T6": continue
        x, y = g(xy, b, f["run_id"], XY); L.append("%s|%s|c|%s|%s|%s" % (b, f["run_id"], x, y, g(dbin, b, f["run_id"], F2SHA)))
    L.append("### CALIB")
    for b, f in fs:
        if b == "RG_T6": continue
        pm = f.get("params") or {}
        rec = {"N": 2500 if f["run_id"].endswith("-VN25-s1") else 10000, "refine_m": 1, "I_max": pm.get("I_max"), "I_used": 0, "rule": "bounded", "source": "calib_meta.json", "status": "completed", "cal_status": "ok", "sections": {"grid": "a" * 64}}
        rec.update(g(calib, b, f["run_id"], {})); L.append("%s|%s|%s" % (b, f["run_id"], json.dumps(rec)))
    L += ["### ISLAND_T"] + ["%s|%s|%d" % (b, f["run_id"], 21) for b, f in fs if b != "RG_T6"]
    L += ["### DIAG"] + ["%s|%s|%d|%d" % (b, f["run_id"], *g(diag, b, f["run_id"], (0, 0))) for b, f in fs if b != "RG_T6"]
    L += ["### BINSHA"] + ["%s|%s" % (b, (binsha or {}).get(b, F2SHA)) for b in dict.fromkeys(b for b, _ in fs)] + ["### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_%s.txt" % wave); open(p, "w").write("\n".join(L) + "\n"); return p
def run(wave, pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_rung.py"), pth, "--wave", wave, "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", REFS] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
N4 = "RG_1a/5-AR-n400-r01-V-s1"; TA = "RG_1b/5-AR-n200-r01-VN25-s1"; TJ = "RG_1b/5-ADJOPP-n200-r01-VN25-s1"; T6 = "RG_T6/5-AR-n200-r01-V-s1"
A2 = "RG_2a/5-AR-n200-r02-V-s1"; N42 = "RG_2b/5-AR-n400-r02-V-s1"; I1 = "RG_3a/5-IND-n200-r01-V-s1"; J2 = "RG_3b/5-ADJOPP-n200-r02-V-s1"
rc, o = run("R1", probe("R1", per_fit=10.0)); check("R1 healthy: quote 150 -> stop > 300, ENDED, arm identity on 3 fits", rc == 0 and "no stop rule fired" in o and "quote 150 -> stop > 300" in o and "WAVE STATE: ENDED" in o and "arm identity checked on 3 fits" in o, o)
rc, o = run("R2", probe("R2", per_fit=10.0)); check("R2 healthy: quote 460 -> stop > 920, 6 fits", rc == 0 and "quote 460 -> stop > 920" in o and "arm identity checked on 6 fits" in o, o)
rc, o = run("R3", probe("R3", per_fit=10.0)); check("R3 healthy: quote 220 -> stop > 440, 3 fits", rc == 0 and "quote 220 -> stop > 440" in o and "arm identity checked on 3 fits" in o, o)
rc, o = run("R1", probe("R1", costs={N4: 115.0}, per_fit=1.0)); check("soft: AR n400 115 > 114 -> SOFT TRIP, exit 0", rc == 0 and "SOFT TRIP" in o and "n400" in o, o)
rc, o = run("R1", probe("R1", costs={N4: 190.5})); check("hard: AR n400 190.5 > 190 -> STOP", rc == 3 and "HARD 190" in o, o)
rc, o = run("R1", probe("R1", costs={TA: 80.5})); check("hard: AR twin 80.5 > 80 -> STOP", rc == 3 and "HARD 80" in o, o)
rc, o = run("R1", probe("R1", costs={TJ: 70.5})); check("hard: ADJ-OPP twin 70.5 > 70 -> STOP", rc == 3 and "HARD 70" in o, o)
rc, o = run("R1", probe("R1", costs={TA: 49.0}, per_fit=1.0)); check("twin AR 49 > soft 48 -> soft trip only", rc == 0 and "SOFT TRIP" in o, o)
rc, o = run("R1", probe("R1", costs={T6: 30.5})); check("hard: T6 30.5 > 30 -> STOP (class T6 by batch although the run id is the G-B pilot's)", rc == 3 and "HARD 30" in o and "[T6]" in o, o)
rc, o = run("R1", probe("R1", costs={T6: 19.0}, per_fit=1.0)); check("T6 19 > soft 18 -> soft trip", rc == 0 and "SOFT TRIP" in o, o)
rc, o = run("R2", probe("R2", costs={A2: 190.5})); check("hard: AR n200 190.5 > 190 -> STOP", rc == 3 and "HARD 190" in o, o)
rc, o = run("R3", probe("R3", costs={I1: 190.5})); check("hard: IND 190.5 > 190 -> STOP", rc == 3 and "HARD 190" in o, o)
rc, o = run("R3", probe("R3", costs={J2: 165.5})); check("hard: ADJ-OPP n200 165.5 > 165 -> STOP", rc == 3 and "HARD 165" in o, o)
rc, o = run("R1", probe("R1", costs={N4: 110.0, TA: 45.0, TJ: 40.0, T6: 6.0}), "--quote", "100"); check("R1 re-quote 100 -> stop > 200: wave 201 -> STOP (every fit under its soft line)", rc == 3 and "wave stop 200" in o and "SOFT TRIP" not in o and "HARD" not in o, o)
rc, o = run("R1", probe("R1", costs={N4: 110.0, TA: 45.0, TJ: 40.0, T6: 4.0}), "--quote", "100"); check("R1 re-quote 100: wave 199 <= 200: no wave stop", rc == 0 and "wave stop" not in o, o)
rc, o = run("R1", probe("R1", costs={N4: 190.0, TA: 80.0, TJ: 70.0, T6: 30.0})); check("R1 wave 370 > 300 with fits exactly at their hard lines: soft trips (4) -> STOP", rc == 3, o)
rc, o = run("R2", probe("R2", per_fit=154.0)); check("R2 wave 924 > 920 -> STOP (fits < 190)", rc == 3 and "wave stop 920" in o, o)
rc, o = run("R3", probe("R3", per_fit=147.0)); check("R3 wave 441 > 440 -> STOP", rc == 3 and "wave stop 440" in o, o)
rc, o = run("R1", probe("R1", per_fit=10.0), "--quote", "200"); check("--quote 200 -> stop > 400", rc == 0 and "stop > 400" in o, o)
json.dump({"5-AR-n400-r01-V-s1": 90.0, "T6:5-AR-n200-r01-V-s1": 12.0, "5-AR-n200-r01-VN25-s1": 32.0, "5-ADJOPP-n200-r01-VN25-s1": 28.0}, open(os.path.join(TMP, "prior_R1.json"), "w"))
rc, o = run("R2", probe("R2", per_fit=10.0), "--prior", os.path.join(TMP, "prior_R1.json")); check("cumulative 162 + 60 fine; projection counts the R3 fits (3 x E)", rc == 0 and "projection" in o, o)
json.dump({"5-AR-n400-r01-V-s1": 600.0, "T6:5-AR-n200-r01-V-s1": 12.0, "5-AR-n200-r01-VN25-s1": 400.0, "5-ADJOPP-n200-r01-VN25-s1": 380.0}, open(os.path.join(TMP, "prior_big.json"), "w"))
rc, o = run("R2", probe("R2", per_fit=10.0), "--prior", os.path.join(TMP, "prior_big.json")); check("cumulative 1392 + 60 = 1452 > 1400 -> STOP", rc == 3 and "cumulative" in o, o)
json.dump({"5-AR-n400-r01-V-s1": 76.0, "T6:5-AR-n200-r01-V-s1": 12.0, "5-AR-n200-r01-VN25-s1": 32.0, "5-ADJOPP-n200-r01-VN25-s1": 28.0}, open(os.path.join(TMP, "prior_p.json"), "w"))
rc, o = run("R2", probe("R2", only=("RG_2a",), per_fit=5.0), "--prior", os.path.join(TMP, "prior_p.json")); check("projection: spent 168 + 20 + E of 2 n400 + 3 R3 fits not started stays below 1,184", rc == 0, o)
json.dump({"5-AR-n400-r01-V-s1": 500.0, "T6:5-AR-n200-r01-V-s1": 12.0, "5-AR-n200-r01-VN25-s1": 300.0, "5-ADJOPP-n200-r01-VN25-s1": 28.0}, open(os.path.join(TMP, "prior_proj.json"), "w"))
rc, o = run("R2", probe("R2", only=("RG_2a",), per_fit=5.0), "--prior", os.path.join(TMP, "prior_proj.json")); check("projection: 860 + 20 + E(2 x 76 + 76 x 2 + 66) = 1,250 > 1,184 -> STOP", rc == 3 and "projection" in o, o)
rc, o = run("R1", probe("R1", states={N4: "FAILED"})); check("FAILED stage -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = run("R1", probe("R1", states={T6: "FAILED"})); check("the T6 JOB failing -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = run("R1", probe("R1", states={T6: "TIMEOUT"})); check("T6 TIMEOUT -> STOP", rc == 3, o)
rc, o = run("R1", probe("R1", states={N4: "OUT_OF_MEMORY"})); check("OOM -> STOP", rc == 3 and "OUT_OF_MEMORY" in o, o)
rc, o = run("R1", probe("R1", states={N4: "NODE_FAIL"})); check("NODE_FAIL = INFO", rc == 0 and "infrastructure fault" in o, o)
rc, o = run("R1", probe("R1", calib={TA: {"N": 10000}})); check("arm identity: the N 2,500 twin recorded N 10,000 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("R1", probe("R1", calib={N4: {"N": 2500}})); check("arm identity: the n400 pilot recorded N 2,500 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("R1", probe("R1", calib={N4: {"I_max": 3}})); check("arm identity: I_max 3 != plan 0 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run("R1", probe("R1", calib={N4: {"refine_m": 4}})); check("arm identity: refine_m 4 -> STOP", rc == 3, o)
rc, o = run("R1", probe("R1", diag={N4: (0, 2)})); check("I_max 0 with cost_diag files -> FLAG, exit 0", rc == 0 and "FLAG behaviour" in o, o)
rc, o = run("R1", probe("R1", xy={TA: ("1" * 64, "2" * 64)})); check("data identity: the twin's X/y differ from the G-B pilot's -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
rc, o = run("R1", probe("R1", xy={TA: ("1" * 64, "2" * 64), TJ: ("1" * 64, "2" * 64)})); check("data identity: both twins differ -> STOP", rc == 3 and "DATA IDENTITY" in o, o)
rc, o = run("R1", probe("R1", binsha={"RG_1b": OTHER})); check("build identity: batch bin sha != BUILD_F2 -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run("R1", probe("R1", dbin={N4: OTHER})); check("build identity: a fit's recorded sha != BUILD_F2 -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run("R1", probe("R1", engine=["/x/OUTCOME"])); check("OUTCOME -> STOP", rc == 3 and "engine record" in o, o)
rc, o = run("R1", probe("R1", squeue=["300_1|p1m_RG_1a_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|32"])); check("own job with a QOS pending reason -> STOP", rc == 3 and "QOS" in o, o)
rc, o = run("R1", probe("R1", squeue=["999_1|p1m_x|PENDING|QOSMaxCpuPerUserLimit|0:00|32"], per_fit=1.0)); check("foreign job with a QOS reason ignored", rc == 0, o)
rc, o = run("R1", probe("R1", only=("RG_1a",))); check("only RG_1a submitted: WAVE STATE RUNNING (RG_1b, RG_T6 not submitted yet)", rc == 0 and "WAVE STATE: RUNNING" in o and "RG_1b" in o and "not submitted yet" in o, o)
rc, o = run("R1", probe("R1", only=("RG_1a", "RG_1b"))); check("RG_T6 not submitted: RUNNING", "WAVE STATE: RUNNING" in o and "RG_T6" in o, o)
rc, o = run("R1", probe("R1", states={N4: "RUNNING"})); check("a RUNNING row -> RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = run("R1", probe("R1", extra_sacct=["300_1|p1m_RG_1a_islands|COMPLETED|2000|48|1|01:00:00"])); check("INFO: island 2,000 s > 1,788 s", rc == 0 and "INFO island wall" in o, o)
rc, o = run("R1", probe("R1", extra_sacct=["300_1|p1m_RG_1a_islands|COMPLETED|3000|48|1|01:00:00"])); check("INFO: task at 83 % of its limit", rc == 0 and "% of its limit" in o, o)
rc, o = run("R1", probe("R1", extra_sacct=["300_1|p1m_RG_1a_islands|COMPLETED|500|48|1|01:00:00"])); check("island 500 s: no INFO", "INFO island wall" not in o and "% of its limit" not in o, o)
rc, o = run("R1", probe("R1")); check("INFO twin vs the G-B pilot's calib sections is printed (real pilot record)", "INFO twin 5-AR-n200-r01-VN25-s1 vs the G-B pilot" in o, o)
src = open(os.path.join(HERE, "stop_rules_rung.py")).read().replace('"T6": (12.0, 18.0, 30.0)', '"T6": (12.0, 180.0, 300.0)'); alt = os.path.join(TMP, "stop_rules_rung_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe("R1"), "--wave", "R1", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", REFS], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
_t = open(probe("R1")).read()
p1 = os.path.join(TMP, "p_rc255_full.txt"); open(p1, "w").write(_t + "### REMOTE_RC\n255\n### REMOTE_STDERR\nboom\n")
rc, o = run("R1", p1); check("remote rc 255 with all sections -> INFO only", rc == 0 and "INFO remote ssh exit status 255" in o, o)
p2 = os.path.join(TMP, "p_trunc.txt"); open(p2, "w").write(_t.split("### DATA_HASH")[0] + "### REMOTE_RC\n255\n### REMOTE_STDERR\n")
rc, o = run("R1", p2); check("truncated probe -> FLAG PROBE ERROR, exit 4", rc == 4 and "PROBE ERROR: stop rules not fully evaluated" in o, o)
p3 = os.path.join(TMP, "p_refetch.txt"); open(p3, "w").write(_t + "### REMOTE_RC\n0\n### REMOTE_NOTE\nfirst ssh rc 255; re-fetched\n### REMOTE_STDERR\n")
rc, o = run("R1", p3); check("re-fetched probe -> INFO probe transport", rc == 0 and "INFO probe transport" in o, o)
# ---- foreign sacct rows (R3 probe 14:20:35Z: job 2814240 also listed 17 array tasks of another user's cmds_rmsd.list.sh from 2025-10-23 via job-id reuse) ----
_exact = os.path.join(STG, "tests", "probe_R3_foreign_cg160_20261120T142035Z.txt")
rc, o = run("R3", _exact, "--prior", os.path.join(STG, "prior_after_R2.json")); check("the EXACT 14:20:35Z probe: no crash, foreign rows reported as ONE INFO, no stop rule, exit 0", rc == 0 and "INFO 11 foreign sacct row(s)" in o and "2814240" in o and "no stop rule fired" in o and "FAILED" not in o.replace("FAILED / TIMEOUT", ""), o)
rc, o = run("R3", probe("R3", extra_sacct=["300_4|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00", "300_5|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00"])); check("foreign FAILED rows on our job id are ignored (no STOP), one INFO line", rc == 0 and o.count("INFO 2 foreign sacct row(s)") == 1, o)
rc, o = run("R3", probe("R3", extra_sacct=["300_4|p1m_RG_3a_setup|COMPLETED|10|2|20|12:00:00|someoneelse"])); check("a p1m_ name but another user -> foreign INFO", rc == 0 and "INFO 1 foreign" in o, o)
rc, o = run("R3", probe("R3", extra_sacct=["300_9|p1m_RG_3a_setup|COMPLETED|10|2|20|01:00:00|fb31"])); check("an own-looking row with a task outside the plan -> FLAG PROBE ERROR (exit 4), no IndexError", rc == 4 and "outside the plan" in o and "Traceback" not in o, o)
rc, o = run("R3", probe("R3", extra_sacct=["300_1|p1m_RG_3a_setup|COMPLETED"])); check("a malformed sacct row -> FLAG PROBE ERROR (exit 4)", rc == 4 and "malformed sacct row" in o, o)
rc, o = run("R3", probe("R3", extra_sacct=["300_1|p1m_RG_3a_setup|COMPLETED|10|2|20|01:00:00|fb31"])); check("an own row with the User column fb31 is evaluated normally", rc == 0, o)
_bad = open(probe("R3")).read().replace("### SQUEUE", "### SQUEUE\nnot|enough"); _pb = os.path.join(TMP, "p_crash.txt"); open(_pb, "w").write(_bad)
rc, o = run("R3", _pb); check("any unexpected parse crash -> FLAG PROBE ERROR + exit 4 (never a bare traceback)", rc == 4 and "FLAG PROBE ERROR: the verdict script crashed" in o and "WAVE STATE: UNKNOWN" in o, o)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
