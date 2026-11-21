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
rc, o = run(probe(cost=dict(islands=34.0))); check("H-51: a SLURM-billed island of 34 core-h (no sidecar yet / pre-engine wait) is NOT a K2 trip any more: reported, not gated", rc == 0 and "STOP K2" not in o, o)
rc, o = run(probe(extra=["### ISLAND_SEC", "GC_P|%s|3|1300" % RID])); check("H-51 K2 compute clause: engine time 1,300 s x 96 CPUs = 34.7 core-h > 33.6 -> STOP (the sidecar exists)", rc == 3 and "STOP K2" in o and "engine time 1300 s x 96" in o and "34.7" in o, o)
rc, o = run(probe(extra=["### ISLAND_SEC", "GC_P|%s|3|1260" % RID])); check("H-51: engine time 1,260 s x 96 = 33.6 core-h exactly: not a trip (strict >)", rc == 0 and "STOP K2" not in o, o)
rc, o = run(probe(extra=["### ISLAND_SEC", "GC_P|%s|3|700" % RID, "GC_P|%s|4|760" % RID], cost=dict(islands=40.0))); check("H-51: engine times 700 / 760 s (18.7 / 20.3 core-h) with a Slurm-billed 40 core-h per island: no K2 (the wait is not compute)", rc == 0 and "STOP K2" not in o, o)
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
rc, o = run(probe(squeue=["300_1|p1m_GC_P_setup|PENDING|QOSMaxCpuPerUserLimit|0:00|48"])); check("H-50 / H-51: own job pending on QOSMaxCpuPerUserLimit (our own per-user CPU cap) -> INFO, NOT a stop", rc == 0 and "INFO 1 pending row(s) wait on QOSMaxCpuPerUserLimit" in o, o)
rc, o = run(probe(squeue=["300_1|p1m_GC_P_setup|PENDING|QOSMaxJobsPerUserLimit|0:00|48"])); check("any OTHER own QOS pending reason still -> STOP (admission)", rc == 3 and "QOS" in o, o)
rc, o = run(probe(squeue=["300_1|p1m_GC_P_setup|PENDING|AssocMaxJobsLimit|0:00|48"])); check("an Assoc limit reason still -> STOP", rc == 3, o)
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

# ===================== option D (wave D: GC_D = 6-AR-n1000-r01-V-s1, quote 1,087, soft 1,631, hard 2,718, wave line 2,174; K1 calibrate > 70 core-h OR > 45 min; K2 island > 60 min while the others have finished) =====================
RIDD = "6-AR-n1000-r01-V-s1"
def probeD(cost=None, states=None, calib=None, xy=("a" * 64, "b" * 64), binsha=F2SHA, dbin=F2SHA, squeue=(), engine=(), extra=(), diag=(0, 0), islT=27, isl_el=None, isl_state=None, cal_el=600):
    c = dict(setup=55.0, calibrate=40.0, islands=40.0, merge=22.0, eval=1.0); c.update(cost or {}); st = dict(states or {})
    L = ["### META utc=2026-11-23T11:00:00Z", "### SUBMISSIONS GC_D"]; jobs = dict(setup=400, calibrate=401, islands=402, merge=403, eval=404)
    for stg, j in jobs.items(): L.append(json.dumps({"stage": stg, "fit": "all" if stg in ("setup", "calibrate") else RIDD, "job": str(j), "submitted_utc": "x"}))
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]
    lim = dict(setup="01:45:00", calibrate="02:00:00", islands="01:30:00", merge="01:30:00", eval="01:00:00")
    for stg in ("setup", "calibrate", "merge", "eval"):
        L.append("%d_1|p1m_GC_D_%s|%s|%d|96|%d|%s|fb31" % (jobs[stg], stg, st.get(stg, "COMPLETED"), cal_el if stg == "calibrate" else 900, int(c[stg] * 3600), lim[stg]))
    for i in range(1, 17):
        L.append("%d_%d|p1m_GC_D_islands|%s|%d|96|%d|%s|fb31" % (jobs["islands"], i, (isl_state or {}).get(i, st.get("islands", "COMPLETED")), (isl_el or {}).get(i, 1500), int(c["islands"] * 3600), lim["islands"]))
    L += list(extra)
    L += ["### DATA_HASH", "GC_D|%s|c|%s|%s|%s" % (RIDD, xy[0], xy[1], dbin)]
    rec = {"N": 2500, "refine_m": 1, "I_max": 0, "I_used": 0, "rule": "bounded", "source": "calib.bin.json settings", "status": "completed", "cal_status": "ok"}; rec.update(calib or {})
    L += ["### CALIB", "GC_D|%s|%s" % (RIDD, json.dumps(rec)), "### ISLAND_T", "GC_D|%s|%d" % (RIDD, islT), "### DIAG", "GC_D|%s|%d|%d" % (RIDD, *diag), "### BINSHA", "GC_D|%s" % binsha, "### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_GC_D.txt"); open(p, "w").write("\n".join(L) + "\n"); return p
def runD(pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gc.py"), pth, "--wave", "D", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
rc, o = runD(probeD()); check("D healthy (758): no stop, ENDED, class option D, quote 1,087 -> wave line 2,174, arm identity 1 fit", rc == 0 and "no stop rule fired" in o and "WAVE STATE: ENDED" in o and "option D" in o and "quote 1087 -> wave line 2174" in o and "arm identity checked on 1 fits" in o, o)
rc, o = runD(probeD(cost=dict(islands=75.0))); check("D soft: total 1,278 < 1,631: no trip", rc == 0 and "SOFT TRIP" not in o, o)
rc, o = runD(probeD(cost=dict(islands=106.0))); check("D soft trip: total 1,771? (55+40+16x106+22+1 = 1,814) > 1,631 -> SOFT TRIP, exit 0, below hard 2,718", rc == 0 and "SOFT TRIP" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)
rc, o = runD(probeD(cost=dict(islands=170.0))); check("D hard: total 2,838 > 2,718 -> STOP (K3)", rc == 3 and "HARD 2718" in o, o)
rc, o = runD(probeD(cost=dict(islands=160.0))); check("D: 2,678 <= 2,718: soft trip and wave line, no stop", rc == 0 and "SOFT TRIP" in o and "FLAG WAVE LINE" in o, o)
rc, o = runD(probeD(cost=dict(islands=130.0))); check("D wave line: 2,198 > 2,174 -> FLAG WAVE LINE (halts submission only), exit 0", rc == 0 and "FLAG WAVE LINE" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)
rc, o = runD(probeD(cost=dict(calibrate=70.0))); check("D K1: calibrate billed 70.0 (not > 70): no stop", rc == 0 and "K1" not in o, o)
rc, o = runD(probeD(cost=dict(calibrate=70.5))); check("D K1: calibrate billed 70.5 > 70 -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runD(probeD(cal_el=2700)); check("D K1: calibrate elapsed 2,700 s = 45 min (not >): no stop", rc == 0 and "K1" not in o, o)
rc, o = runD(probeD(cal_el=2701)); check("D K1: calibrate elapsed 2,701 s > 45 min -> STOP", rc == 3 and "STOP K1" in o and "45 min" in o, o)
rc, o = runD(probeD(states=dict(calibrate="RUNNING"), cal_el=2800)); check("D K1: a RUNNING calibrate beyond 45 min -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runD(probeD(isl_el={4: 3600})); check("D K2: island at exactly 3,600 s: no stop", rc == 0 and "K2" not in o, o)
rc, o = runD(probeD(isl_el={4: 3601})); check("D K2: island 3,601 s > 60 min while the others have finished -> STOP", rc == 3 and "STOP K2" in o, o)
rc, o = runD(probeD(isl_el={4: 3700}, isl_state={5: "RUNNING"})); check("D: island > 60 min while another island still runs -> INFO only", rc == 0 and "INFO island task" in o and "STOP K2" not in o, o)
rc, o = runD(probeD(isl_el={4: 1700})); check("D: island 1,700 s (> the pilot's 1,584 s but < 60 min): no K2 at D's own model", rc == 0 and "K2" not in o, o)
rc, o = runD(probeD(cost=dict(islands=40.0), isl_el={4: 1700})); check("D: the pilot's billed K2 line (33.6) does NOT apply to D (island billed 40)", rc == 0, o)
rc, o = runD(probeD(states=dict(merge="OUT_OF_MEMORY"))); check("D memory: state OUT_OF_MEMORY -> STOP", rc == 3 and "OUT_OF_MEMORY" in o, o)
rc, o = runD(probeD(extra=["403_1|p1m_GC_D_merge|COMPLETED|900|32|115200|01:30:00|fb31"])); check("D: no OOM, sacct near the request is not read: no stop", rc == 0, o)
rc, o = runD(probeD(states=dict(calibrate="FAILED"))); check("D FAILED stage -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = runD(probeD(states=dict(islands="TIMEOUT"))); check("D TIMEOUT -> STOP", rc == 3, o)
rc, o = runD(probeD(calib={"N": 10000})); check("D arm: N 10,000 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = runD(probeD(calib={"I_max": 3})); check("D arm: I_max 3 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = runD(probeD(calib={"refine_m": 4})); check("D arm: refine_m 4 -> STOP", rc == 3, o)
rc, o = runD(probeD(binsha=OTHER)); check("D build identity -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runD(probeD(dbin=OTHER)); check("D recorded binary sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runD(probeD(diag=(0, 2))); check("D I_max 0 with cost_diag files -> FLAG", rc == 0 and "FLAG behaviour" in o, o)
rc, o = runD(probeD(engine=["/x/OUTCOME"])); check("D OUTCOME -> STOP", rc == 3, o)
rc, o = runD(probeD(squeue=["400_1|p1m_GC_D_setup|PENDING|QOSMaxJobsPerUserLimit|0:00|48"])); check("D own job with a QOS reason -> STOP", rc == 3 and "QOS" in o, o)
rc, o = runD(probeD(extra=["400_4|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00|cg160"])); check("D foreign rows: one INFO, no stop", rc == 0 and "INFO 1 foreign" in o, o)
rc, o = runD(probeD(isl_state={7: "PENDING"})); check("D island PENDING -> WAVE STATE RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = runD(probeD(islT=26)); check("D T != 27 -> INFO", rc == 0 and "INFO final-island stage count" in o, o)
_td = open(probeD()).read(); _pd = os.path.join(TMP, "p_D_trunc.txt"); open(_pd, "w").write(_td.split("### DATA_HASH")[0] + "### REMOTE_RC\n255\n### REMOTE_STDERR\n")
rc, o = runD(_pd); check("D truncated probe -> PROBE ERROR, exit 4", rc == 4 and "PROBE ERROR" in o, o)
rc, o = run(probeD()); check("the pilot wave P does not read the D batch (no GC_P rows): no crash", rc in (0, 3, 4), o)

# ===================== wave D2 = the resubmission of option D after the setup TIMEOUT (HQ d99c67b4): same fit and lines; the lost GC_D setup (--prior, same run id) counts in the fit total =====================
def probeD2(**kw):
    s = open(probeD(**kw)).read().replace("SUBMISSIONS GC_D", "SUBMISSIONS GC_D2").replace("GC_D|", "GC_D2|").replace("p1m_GC_D_", "p1m_GC_D2_")
    p = os.path.join(TMP, "probe_GC_D2.txt"); open(p, "w").write(s); return p
def runD2(pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gc.py"), pth, "--wave", "D2", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
PD = os.path.join(TMP, "prior_D.json"); json.dump({RIDD: 84.0}, open(PD, "w"))
rc, o = runD2(probeD2(), "--prior", PD); check("D2 healthy: 758 + the lost setup 84 = 842 in the fit total, no stop, quote 1,087 -> wave line 2,174, ENDED", rc == 0 and "no stop rule fired" in o and "842.00" in o and "quote 1087 -> wave line 2174" in o and "WAVE STATE: ENDED" in o, o)
rc, o = runD2(probeD2(cost=dict(islands=95.0)), "--prior", PD); check("D2: islands 95 x 16 = 1,520 + 118 + 84 = 1,722 > soft 1,631 -> SOFT TRIP (the prior is in the total; without it 1,638 would also trip, so use hard below)", rc == 0 and "SOFT TRIP" in o, o)
rc, o = runD2(probeD2(cost=dict(islands=150.0)), "--prior", PD); check("D2 hard: 150 x 16 = 2,400 + 118 + 84 = 2,602 <= 2,718 soft trip only; the prior alone decides: 2,640+... see next", rc == 0 and "SOFT TRIP" in o and "STOP" not in o.replace("STOP SUBMITTING", ""), o)
rc, o = runD2(probeD2(cost=dict(islands=155.0)), "--prior", PD); check("D2 hard: 155 x 16 + 118 + 84 = 2,682 <= 2,718: still no stop", rc == 0 and "HARD" not in o, o)
rc, o = runD2(probeD2(cost=dict(islands=158.0)), "--prior", PD); check("D2 hard: 158 x 16 + 118 + 84 = 2,730 > 2,718 -> STOP (the lost setup counts)", rc == 3 and "HARD 2718" in o, o)
rc, o = runD2(probeD2(cost=dict(islands=158.0))); check("D2 without the prior the same probe (2,646) is NOT a hard trip (proves the prior is what pushes it over)", rc == 0 and "HARD" not in o, o)
rc, o = runD2(probeD2(cost=dict(calibrate=70.5)), "--prior", PD); check("D2 K1 billed > 70 -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runD2(probeD2(cal_el=2701), "--prior", PD); check("D2 K1 elapsed > 45 min -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runD2(probeD2(isl_el={3: 3601}), "--prior", PD); check("D2 K2 island > 60 min while the others finished -> STOP", rc == 3 and "STOP K2" in o, o)
rc, o = runD2(probeD2(states=dict(calibrate="OUT_OF_MEMORY")), "--prior", PD); check("D2 OOM state -> STOP", rc == 3, o)
rc, o = runD2(probeD2(), "--prior", PD); check("D2 job names p1m_GC_D2_* are accepted (not foreign)", "foreign" not in o, o)
_s = open(probeD2()).read().replace("### SQUEUE", "### SSTAT\n2817052_1.batch|23606760K|2-22:25:13\n### SQUEUE"); _ps = os.path.join(TMP, "p_sstat.txt"); open(_ps, "w").write(_s)
rc, o = runD2(_ps, "--prior", PD); check("an SSTAT section is printed as an INFO progress line", rc == 0 and "INFO progress (sstat) 2817052_1.batch: MaxRSS 23606760K, AveCPU 2-22:25:13" in o, o)

# ===================== option B (resume from the finished setup on the SAME batch GC_D; the lost setup + its cancelled dependants are --ignore-jobs) =====================
OLD = ["2817052", "2817053", "2817054", "2817055", "2817056"]
_old_rows = ["2817052_1|p1m_GC_D_setup|TIMEOUT|6307|48|302736|01:45:00|fb31", "2817053_1|p1m_GC_D_calibrate|CANCELLED|0|0|0|02:00:00|fb31", "2817054_[1-16%16]|p1m_GC_D_islands|CANCELLED|0|0|0|01:30:00|fb31", "2817055|p1m_GC_D_merge|CANCELLED|0|0|0|01:30:00|fb31", "2817056|p1m_GC_D_eval|CANCELLED|0|0|0|01:00:00|fb31"]
def probeB(**kw):
    s = open(probeD(**kw)).read()
    sub = "### SUBMISSIONS GC_D\n" + "\n".join(json.dumps({"stage": st, "fit": "all" if st in ("setup", "calibrate") else RIDD, "job": j, "submitted_utc": "x"}) for st, j in zip(("setup", "calibrate", "islands", "merge", "eval"), OLD)) + "\n"
    s = s.replace("### SUBMISSIONS GC_D\n", sub, 1).replace("### SACCT\n", "### SACCT\n" + "\n".join(_old_rows) + "\n", 1)
    p = os.path.join(TMP, "probe_GC_D_B.txt"); open(p, "w").write(s); return p
rc, o = runD(probeB(), "--ignore-jobs", ",".join(OLD)); check("B: the lost setup (TIMEOUT, 84.09 core-h) is a known-failed INFO, not a STOP; its core-h count in the fit total (758 + 84.09 = 842.09)", rc == 0 and "known-failed" in o and "842.09" in o and "no stop rule fired" in o, o)
rc, o = runD(probeB())  ; check("B without --ignore-jobs the old TIMEOUT is a STOP (the monitor MUST pass IGNORE_JOBS / --ignore-jobs)", rc == 3 and "TIMEOUT" in o, o)
rc, o = runD(probeB(isl_el={4: 3601}), "--ignore-jobs", ",".join(OLD)); check("B: K2 still fires although the old CANCELLED islands array row (with a [ ] id) is in the probe", rc == 3 and "STOP K2" in o, o)
rc, o = runD(probeB(cost=dict(calibrate=70.5)), "--ignore-jobs", ",".join(OLD)); check("B: K1 fires on the NEW calibrate only", rc == 3 and "STOP K1" in o, o)
rc, o = runD(probeB(cost=dict(islands=158.0)), "--ignore-jobs", ",".join(OLD)); check("B: hard line counts the lost setup: 158 x 16 + 55 + 40 + 22 + 1 + 84.09 > 2,718 -> STOP", rc == 3 and "HARD 2718" in o, o)
rc, o = runD(probeB(isl_state={7: "PENDING"}), "--ignore-jobs", ",".join(OLD)); check("B: WAVE STATE RUNNING while a new island is pending", "WAVE STATE: RUNNING" in o, o)

# ===================== wave W1 (GC_W1: AR r02 + ADJ-OPP r01, 2 fits, 1M): quote 705, wave STOP 1,410 (2 x), K1 / K2 as the pilot; AR soft 518 (H-46 re-fit, --soft override), ADJ-OPP soft 509, hard 815 / 848 =====================
RA, RJ = "6-AR-n200-r02-V-s1", "6-ADJOPP-n200-r01-V-s1"
def probeW1(cost=None, states=None, calib=None, xy=None, binsha=F2SHA, dbin=None, squeue=(), engine=(), extra=(), isl_el=None, isl_state=None, only_fit=None):
    """cost: {(fit, stage): billed per task (islands: per task) } ; fit in (RA, RJ)"""
    L = ["### META utc=2026-11-23T11:00:00Z", "### SUBMISSIONS GC_W1"]
    jobs = {"setup": 500, "calibrate": 501}; fj = {RA: dict(islands=502, merge=503, eval=504), RJ: dict(islands=505, merge=506, eval=507)}
    for stg, j in jobs.items(): L.append(json.dumps({"stage": stg, "fit": "all", "job": str(j), "submitted_utc": "x"}))
    for rid in (RA, RJ):
        for stg, j in fj[rid].items(): L.append(json.dumps({"stage": stg, "fit": rid, "job": str(j), "submitted_utc": "x"}))
    L += ["### SQUEUE"] + list(squeue) + ["### SACCT"]
    base = dict(setup=12.3, calibrate=16.2, islands=18.9, merge=14.0, eval=0.3); cc_ = lambda rid, stg: (cost or {}).get((rid, stg), base[stg])
    st = lambda rid, stg: (states or {}).get((rid, stg), "COMPLETED")
    for i, rid in enumerate((RA, RJ), 1):
        L.append("500_%d|p1m_GC_W1_setup|%s|900|48|%d|00:45:00|fb31" % (i, st(rid, "setup"), int(cc_(rid, "setup") * 3600)))
        L.append("501_%d|p1m_GC_W1_calibrate|%s|600|96|%d|01:30:00|fb31" % (i, st(rid, "calibrate"), int(cc_(rid, "calibrate") * 3600)))
        for k in range(1, 17):
            s = (isl_state or {}).get((rid, k), st(rid, "islands")); el = (isl_el or {}).get((rid, k), 700)
            L.append("%d_%d|p1m_GC_W1_islands|%s|%d|96|%d|01:00:00|fb31" % (fj[rid]["islands"], k, s, el, int(cc_(rid, "islands") * 3600)))
        L.append("%d|p1m_GC_W1_merge|%s|1500|32|%d|01:30:00|fb31" % (fj[rid]["merge"], st(rid, "merge"), int(cc_(rid, "merge") * 3600)))
        L.append("%d|p1m_GC_W1_eval|%s|100|8|%d|01:00:00|fb31" % (fj[rid]["eval"], st(rid, "eval"), int(cc_(rid, "eval") * 3600)))
    L += list(extra)
    L.append("### DATA_HASH")
    for rid in (RA, RJ):
        x, y = (xy or {}).get(rid, ("a" * 64, "b" * 64) if rid == RA else ("c" * 64, "d" * 64)); L.append("GC_W1|%s|c|%s|%s|%s" % (rid, x, y, (dbin or {}).get(rid, F2SHA)))
    L.append("### CALIB")
    for rid in (RA, RJ):
        rec = {"N": 2500, "refine_m": 1, "I_max": 0, "I_used": 0, "rule": "bounded", "source": "calib.bin.json settings", "status": "completed", "cal_status": "ok"}; rec.update((calib or {}).get(rid, {})); L.append("GC_W1|%s|%s" % (rid, json.dumps(rec)))
    L += ["### ISLAND_T"] + ["GC_W1|%s|27" % r for r in (RA, RJ)] + ["### DIAG"] + ["GC_W1|%s|0|0" % r for r in (RA, RJ)] + ["### BINSHA", "GC_W1|%s" % binsha, "### ENGINE_FLAGS"] + list(engine)
    p = os.path.join(TMP, "probe_GC_W1.txt"); open(p, "w").write("\n".join(L) + "\n"); return p
def runW1(pth, *extra):
    r = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gc.py"), pth, "--wave", "W1", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")] + list(extra), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
SOFT_AR = ["--soft", "gc1m AR n200 N2500 I0=518"]
rc, o = runW1(probeW1(), *SOFT_AR); check("W1 healthy (2 x ~346): no stop, quote 705, wave stop 1,410, ENDED, arm identity on 2 fits, the AR soft 518 override printed", rc == 0 and "no stop rule fired" in o and "quote 705" in o and "WAVE STATE: ENDED" in o and "arm identity checked on 2 fits" in o and "518.0" in o, o)
rc, o = runW1(probeW1(cost={(RA, "islands"): 29.0}), *SOFT_AR); check("W1: AR fit 12.3+16.2+16x29+14+0.3 = 506.8 <= 518: no soft trip with the override (it WOULD trip at the default 489)", rc == 0 and "SOFT TRIP" not in o, o)
rc, o = runW1(probeW1(cost={(RA, "islands"): 29.0})); check("W1: the same fit trips the DEFAULT soft 489 (control: the override matters)", rc == 0 and "SOFT TRIP" in o, o)
rc, o = runW1(probeW1(cost={(RA, "islands"): 31.5}), *SOFT_AR); check("W1: AR 12.3+16.2+504+14.3 = 546.8 > 518 -> SOFT TRIP (K2 billed 33.6 not reached), exit 0", rc == 0 and "SOFT TRIP" in o and RA in o, o)
rc, o = runW1(probeW1(cost={(RJ, "islands"): 30.0}), *SOFT_AR); check("W1: ADJ-OPP 12.3+16.2+480+14.3 = 522.8 > soft 509 -> SOFT TRIP", rc == 0 and "SOFT TRIP" in o and RJ in o, o)
rc, o = runW1(probeW1(cost={(RJ, "islands"): 29.0}), *SOFT_AR); check("W1: ADJ-OPP 490.8 < 509: no trip", rc == 0 and "SOFT TRIP" not in o, o)
rc, o = runW1(probeW1(cost={(RA, "merge"): 500.0}), *SOFT_AR); check("W1 hard: AR fit > 815 -> STOP", rc == 3 and "HARD 815" in o, o)
rc, o = runW1(probeW1(cost={(RJ, "merge"): 520.0}), *SOFT_AR); check("W1 hard: ADJ-OPP fit > 848 -> STOP", rc == 3 and "HARD 848" in o, o)
rc, o = runW1(probeW1(cost={(RA, "merge"): 380.0, (RJ, "merge"): 380.0}), *SOFT_AR); check("W1 wave stop: 2 fits ~ 711 + 711 = 1,422 > 1,410 -> STOP wave (each fit under its hard line), no HARD", rc == 3 and "wave stop 1410" in o and "HARD" not in o, o)
rc, o = runW1(probeW1(cost={(RA, "merge"): 370.0, (RJ, "merge"): 330.0}), *SOFT_AR); check("W1: 2 fits ~ 701 + 661 = 1,362 < 1,410: no wave stop (soft trips only)", rc == 0 and "wave stop" not in o, o)
rc, o = runW1(probeW1(cost={(RA, "calibrate"): 48.5}), *SOFT_AR); check("W1 K1: AR calibrate billed 48.5 > 48 -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runW1(probeW1(cost={(RJ, "calibrate"): 49.0}), *SOFT_AR); check("W1 K1: ADJ-OPP calibrate 49 -> STOP", rc == 3 and "STOP K1" in o, o)
rc, o = runW1(probeW1(isl_el={(RA, 3): 1600}), *SOFT_AR); check("W1 K2: an island 1,600 s while all other islands (both fits) have finished -> STOP", rc == 3 and "STOP K2" in o, o)
rc, o = runW1(probeW1(isl_el={(RA, 3): 1600}, isl_state={(RJ, 5): "RUNNING"}), *SOFT_AR); check("W1: island 1,600 s while ANOTHER fit's island still runs -> INFO only", rc == 0 and "INFO island task" in o and "STOP K2" not in o, o)
rc, o = runW1(probeW1(cost={(RJ, "islands"): 38.0}), *SOFT_AR); check("W1 H-51: Slurm-billed island 38 core-h (AR islands 2 / 4 of the 01:17Z probe: 38.1 / 35.2) is NOT a K2 trip without engine time", rc == 0 and "STOP K2" not in o, o)
rc, o = runW1(probeW1(extra=["### ISLAND_SEC", "GC_W1|%s|2|1300" % RJ]), *SOFT_AR); check("W1 H-51 K2 compute clause: ADJ-OPP island engine 1,300 s x 96 CPUs = 34.7 > 33.6 -> STOP", rc == 3 and "STOP K2" in o, o)
rc, o = runW1(probeW1(extra=["### ISLAND_SEC", "GC_W1|%s|2|1000" % RA, "GC_W1|%s|4|950" % RA], cost={(RA, "islands"): 38.0}), *SOFT_AR); check("W1 H-51: the 01:17Z pattern (engine 1,000 / 950 s = 26.7 / 25.3 core-h, Slurm-billed 38): no K2", rc == 0 and "STOP K2" not in o, o)
_f = os.path.join(STG, "tests", "probe_W1_falsestop_20261121T011722Z.txt")
rc, o = runW1(_f, *SOFT_AR); check("FIXTURE: the W1 01:17:22Z probe (the monitor's false STOP: K2 billed 38.1 / 35.2 + QOSMaxCpuPerUserLimit pending) gives NO STOP, with the INFO lines", rc == 0 and "no stop rule fired" in o and "VERDICT: no stop rule fired" in o and "INFO 1 pending row(s) wait on QOSMaxCpuPerUserLimit" in o and "WAVE STATE: RUNNING" in o, o)
rc, o = runW1(probeW1(states={(RJ, "merge"): "FAILED"}), *SOFT_AR); check("W1 FAILED merge -> STOP", rc == 3 and "failed stage" in o, o)
rc, o = runW1(probeW1(states={(RA, "calibrate"): "OUT_OF_MEMORY"}), *SOFT_AR); check("W1 OOM -> STOP", rc == 3, o)
rc, o = runW1(probeW1(calib={RJ: {"N": 10000}}), *SOFT_AR); check("W1 arm: ADJ-OPP recorded N 10,000 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = runW1(probeW1(calib={RA: {"I_max": 3}}), *SOFT_AR); check("W1 arm: AR I_max 3 -> STOP", rc == 3 and "ARM IDENTITY" in o, o)
rc, o = runW1(probeW1(binsha=OTHER), *SOFT_AR); check("W1 build identity -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runW1(probeW1(dbin={RJ: OTHER}), *SOFT_AR); check("W1 recorded binary sha -> STOP", rc == 3 and "BUILD IDENTITY" in o, o)
rc, o = runW1(probeW1(engine=["/x/OUTCOME"]), *SOFT_AR); check("W1 OUTCOME -> STOP", rc == 3, o)
rc, o = runW1(probeW1(isl_state={(RA, 7): "PENDING"}), *SOFT_AR); check("W1 an island PENDING -> RUNNING", "WAVE STATE: RUNNING" in o, o)
rc, o = runW1(probeW1(extra=["500_4|cmds_rmsd.list.sh|FAILED|10|2|20|12:00:00|cg160"]), *SOFT_AR); check("W1 foreign sacct row: one INFO", rc == 0 and "INFO 1 foreign" in o, o)
rc, o = runW1(probeW1(), "--soft", "gc1m AR n200 N2500 I0=900"); check("--soft above the pinned hard line (815) is refused (exit 64)", rc == 64, o)
_e = subprocess.run([sys.executable, os.path.join(HERE, "stop_rules_gc.py"), probeW1(), "--wave", "W1", "--plans", PLANS, "--deploy-log", LOG, "--ref-hashes", os.path.join(STG, "gc_refs.json")], capture_output=True, text=True, env=dict(os.environ, SOFT_OVERRIDES="gc1m AR n200 N2500 I0=518"))
check("SOFT_OVERRIDES env works like --soft", _e.returncode == 0 and "518.0" in _e.stdout, _e.stdout)
print("\n%d passed, %d failed" % (ok, fail)); sys.exit(1 if fail else 0)
