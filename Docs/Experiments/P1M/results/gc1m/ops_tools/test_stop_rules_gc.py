#!/usr/bin/env python3
"""test_stop_rules_gc.py -- synthetic probes for stop_rules_gc.py (1M pilot GC_P). Real plan (staging/gc1m/scripts/GC_P), no NOTS. Scratch under $GC_TEST_TMP or staging/gc1m/_t (never /tmp)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STG = os.path.dirname(HERE)
TMP = os.environ.get("GC_TEST_TMP", os.path.join(STG, "_t")); os.makedirs(TMP, exist_ok=True)
PLANS = os.path.join(STG, "scripts"); F2SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"; OTHER = "c" * 64
LOG = os.path.join(TMP, "deploy_gc.log"); open(LOG, "w").write("2026-11-19T17:56:09Z\tVN_ID_1\tBUILD_F2\t%s\te993ece2\tsapphirerapids\t1\t6165\ttest\n" % F2SHA)
REF = json.load(open(os.path.join(STG, "gc_refs.json"))); XY = (REF["6-AR-n200-r01"]["X_sha256"], REF["6-AR-n200-r01"]["y_sha256"])
RID = "6-AR-n200-r01-V-s1"
def probe(cost=None, states=None, calib=None, xy=XY, binsha=F2SHA, dbin=F2SHA, squeue=(), engine=(), extra=(), diag=(0, 0), islT=27, isl_el=None, isl_state=None, calib_state="COMPLETED"):
    """cost: dict stage -> billed core-h (per fit stage; islands = per task); defaults sum to 325.9"""
    c = dict(setup=15.25, calibrate=24.0, islands=16.8, merge=17.0, eval=0.4); c.update(cost or {}); st = dict(states or {})
    L = ["### META utc=2026-11-23T11:00:00Z", "### SUBMISSIONS GC_P"]
    jobs = dict(setup=300, calibrate=301, islands=302, merge=303, eval=304)
    for stg, j in jobs.items(): L.append(json.dumps({"stage": stg, "fit": "all" if stg in ("setup", "calibrate") else RID, "job": str(j), "submitted_utc": "x"}))
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]
    lim = dict(setup="00:45:00", calibrate="01:30:00", islands="01:00:00", merge="01:30:00", eval="01:00:00")
    for stg in ("setup", "calibrate", "merge", "eval"):
        s = st.get(stg, "COMPLETED"); L.append("%d_1|p1m_GC_P_%s|%s|%d|%d|%d|%s|fb31" % (jobs[stg], stg, s, 600, 96, int(c[stg] * 3600), lim[stg]))
    for i in range(1, 17):
        s = (isl_state or {}).get(i, st.get("islands", "COMPLETED")); el = (isl_el or {}).get(i, 600)
        L.append("%d_%d|p1m_GC_P_islands|%s|%d|96|%d|%s|fb31" % (jobs["islands"], i, s, el, int(c["islands"] * 3600), lim["islands"]))
    L += list(extra)
    L += ["### DATA_HASH", "GC_P|%s|c|%s|%s|%s" % (RID, xy[0], xy[1], dbin)]
    rec = {"N": 2500, "refine_m": 1, "I_max": 0, "I_used": 0, "rule": "bounded", "source": "calib.bin.json settings", "status": "completed", "cal_status": "ok"}; rec.update(calib or {})
    L += ["### CALIB", "GC_P|%s|%s" % (RID, json.dumps(rec)), "### ISLAND_T", "GC_P|%s|%d" % (RID, islT), "### DIAG", "GC_P|%s|%d|%d" % (RID, *diag), "### BINSHA", "GC_P|%s" % binsha, "### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_GC_P.txt"); open(p, "w").write("\n".join(L) + "\n"); return p
def run(pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gc.py"), pth, "--wave", "P", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
ok = fail = 0
def check(name, cond, out=""):
    global ok, fail
    if cond: ok += 1; print("PASS", name)
    else: fail += 1; print("FAIL", name); print(out)
rc, o = run(probe()); check("healthy pilot (325.9): no stop, WAVE STATE ENDED, arm identity 1 fit, class table pinned", rc == 0 and "no stop rule fired" in o and "WAVE STATE: ENDED" in o and "arm identity checked on 1 fits" in o and "(pinned)" in o, o)


rc, o = run(probe(cost=dict(islands=27.2))); check("soft trip: total 489.9 > 489 -> SOFT TRIP, exit 0 (K2 billed 33.6 not reached)", rc == 0 and "SOFT TRIP" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)

rc, o = run(probe(cost=dict(islands=33.0, merge=250.0))); check("hard: fit > 815 -> STOP (K3)", rc == 3 and "HARD 815" in o, o)
rc, o = run(probe(cost=dict(islands=33.0))); check("wave line: total 600 < 650: no flag", "FLAG WAVE LINE" not in o, o)
rc, o = run(probe(cost=dict(islands=33.0, merge=83.5))); check("wave line: total 651 > 650 -> FLAG WAVE LINE (halts submission only), soft trip, NO stop, exit 0", rc == 0 and "FLAG WAVE LINE" in o and "SOFT TRIP" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)
rc, o = run(probe(cost=dict(calibrate=47.0))); check("K1: calibrate billed 47 <= 48: no stop", rc == 0 and "K1" not in o, o)
rc, o = run(probe(cost=dict(calibrate=48.5))); check("K1: calibrate billed 48.5 > 48 -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = run(probe(states=dict(calibrate="RUNNING"), cost=dict(calibrate=49.0))); check("K1 fires on a RUNNING calibrate too (billed so far > 48)", rc == 3 and "STOP K1" in o, o)
rc, o = run(probe(cost=dict(islands=34.0))); check("K2: island billed 34 > 33.6 -> STOP", rc == 3 and "STOP K2" in o, o)
rc, o = run(probe(isl_el={5: 1600})); check("K2: one island 1,600 s > 1,584 s while the others have finished -> STOP", rc == 3 and "STOP K2" in o and "1600" in o, o)
rc, o = run(probe(isl_el={5: 1584})); check("K2: exactly 1,584 s: no stop", rc == 0, o)
rc, o = run(probe(isl_el={5: 1600}, isl_state={6: "RUNNING"})); check("island 1,600 s while another island still runs -> INFO only (K2 waits for the others)", rc == 0 and "INFO island task" in o and "STOP K2" not in o, o)
rc, o = run(probe(isl_state={7: "PENDING"})); check("an island PENDING -> WAVE STATE RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = run(probe(states=dict(merge="FAILED"))); check("FAILED merge -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = run(probe(states=dict(calibrate="OUT_OF_MEMORY"))); check("OOM -> STOP", rc == 3 and "OUT_OF_MEMORY" in o, o)
rc, o = run(probe(states=dict(islands="TIMEOUT"))); check("TIMEOUT -> STOP", rc == 3, o)
rc, o = run(probe(states=dict(eval="NODE_FAIL"))); check("NODE_FAIL = INFO", rc == 0 and "infrastructure fault" in o, o)
rc, o = run(probe(calib={"N": 10000})); check("arm: N 10,000 recorded != 2,500 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run(probe(calib={"I_max": 3})); check("arm: I_max 3 != 0 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = run(probe(calib={"refine_m": 4})); check("arm: refine_m 4 -> STOP", rc == 3, o)
rc, o = run(probe(calib={"rule": "unbounded"})); check("arm: rule != bounded -> STOP", rc == 3, o)
rc, o = run(probe(diag=(0, 3))); check("I_max 0 with cost_diag files -> FLAG, exit 0", rc == 0 and "FLAG behaviour" in o, o)
rc, o = run(probe(islT=26)); check("T != 27 -> INFO", rc == 0 and "INFO final-island stage count T" in o, o)
rc, o = run(probe(xy=("1" * 64, "2" * 64))); check("data identity: X/y != the 11-17 rep-1 record -> STOP", rc == 3 and "DATA IDENTITY" in o and "11-17" in o, o)
rc, o = run(probe(binsha=OTHER)); check("build identity: batch bin sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(dbin=OTHER)); check("build identity: a fit's recorded sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = run(probe(engine=["/x/OUTCOME"])); check("OUTCOME -> STOP", rc == 3 and "engine record" in o, o)
rc, o = run(probe(squeue=["300_1|p1m_GC_P_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|48"])); check("own job with a QOS pending reason -> STOP", rc == 3 and "QOS" in o, o)
rc, o = run(probe(squeue=["999_1|p1m_x|PENDING|QOSMaxCpuPerUserLimit|0:00|48"])); check("foreign job with a QOS reason ignored", rc == 0, o)
rc, o = run(probe(extra=["300_4|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00|cg160", "300_5|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00|cg160"])); check("foreign FAILED rows on our job id (job-id reuse): ONE INFO, no stop", rc == 0 and o.count("INFO 2 foreign sacct row(s)") == 1, o)
rc, o = run(probe(extra=["300_9|p1m_GC_P_setup|COMPLETED|10|2|20|01:00:00|fb31"])); check("own-looking row with a task outside the plan -> FLAG PROBE ERROR (exit 4)", rc == 4 and "outside the plan" in o, o)
rc, o = run(probe(extra=["300_1|p1m_GC_P_setup|COMPLETED"])); check("malformed sacct row -> FLAG PROBE ERROR (exit 4)", rc == 4 and "malformed sacct row" in o, o)
rc, o = run(probe(extra=["300_1|p1m_GC_P_setup|COMPLETED|10|48|20|00:45:00|fb31"], states={})); check("a user fb31 row is evaluated", rc == 0, o)
_t = open(probe()).read()
_pb = os.path.join(TMP, "p_crash.txt"); open(_pb, "w").write(_t.replace("### SQUEUE", "### SQUEUE\nnot|enough"))
rc, o = run(_pb); check("unexpected parse crash -> FLAG PROBE ERROR + exit 4, WAVE STATE UNKNOWN", rc == 4 and "the verdict script crashed" in o and "WAVE STATE: UNKNOWN" in o, o)
p1 = os.path.join(TMP, "p_rc255_full.txt"); open(p1, "w").write(_t + "### REMOTE_RC\n255\n### REMOTE_STDERR\nboom\n")
rc, o = run(p1); check("remote rc 255 with all sections -> INFO only", rc == 0 and "INFO remote ssh exit status 255" in o, o)
p2 = os.path.join(TMP, "p_trunc.txt"); open(p2, "w").write(_t.split("### DATA_HASH")[0] + "### REMOTE_RC\n255\n### REMOTE_STDERR\n")
rc, o = run(p2); check("truncated probe -> FLAG PROBE ERROR, exit 4", rc == 4 and "PROBE ERROR: stop rules not fully evaluated" in o, o)
p3 = os.path.join(TMP, "p_refetch.txt"); open(p3, "w").write(_t + "### REMOTE_RC\n0\n### REMOTE_NOTE\nfirst ssh rc 255; re-fetched\n### REMOTE_STDERR\n")
rc, o = run(p3); check("re-fetched probe -> INFO probe transport", rc == 0 and "INFO probe transport" in o, o)
src = open(os.path.join(HERE, "stop_rules_gc.py")).read().replace('"gc1m AR n200 N2500 I0": (326.0, 489.0, 815.0)', '"gc1m AR n200 N2500 I0": (326.0, 4890.0, 8150.0)'); alt = os.path.join(TMP, "stop_rules_gc_altered.py"); open(alt, "w").write(src)
r = subprocess.run([sys.executable, alt, probe(), "--wave", "P", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")], capture_output=True, text=True)
check("an altered class table -> STOP (pinned sha256)", r.returncode == 3 and "class table in this script was altered" in r.stdout, r.stdout)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
