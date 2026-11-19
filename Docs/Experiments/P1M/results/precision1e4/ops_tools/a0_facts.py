#!/usr/bin/env python3
"""a0_facts.py -- facts for the A0 canary read-back (LEG_PLAN §6.4), from the collected records only (+ one nice'd `smcbvs4 info` per fit.bin on Owls).
Prints every number the read-back quotes. Stdlib only. Usage: a0_facts.py <records/precision1e4/A0> <deploy_leg.log> <overlap_refs.json> <info-bin>"""
import glob, json, os, re, subprocess, sys, tempfile
R, LOGF, REFS, BIN = sys.argv[1:5]
TABLE = {"prec N2500 m4 I3": (12.36, 18.5, 30.9), "prec N2500 m1 I0": (5.76, 8.6, 14.4), "A3 n200": (2.76, 4.1, 6.9), "AR n200": (2.18, 3.3, 5.5)}
CLS = {"4-AR-n200-r01-P-N2500-m4-c1-s1": "prec N2500 m4 I3", "4-AR-n200-r01-P-N2500-m1-I0-c1-s1": "prec N2500 m1 I0", "4-AR-n200-r01-A3-exactlink-s1": "A3 n200", "4-AR-n200-r01-V-XB-s1": "AR n200"}
BATCH = {"4-AR-n200-r01-P-N2500-m4-c1-s1": "PL_A0_1", "4-AR-n200-r01-P-N2500-m1-I0-c1-s1": "PL_A0_1", "4-AR-n200-r01-A3-exactlink-s1": "PL_A0_2", "4-AR-n200-r01-V-XB-s1": "PL_A0_3"}
PLAN = {"4-AR-n200-r01-P-N2500-m4-c1-s1": (4, 3, 64), "4-AR-n200-r01-P-N2500-m1-I0-c1-s1": (1, 0, 64), "4-AR-n200-r01-A3-exactlink-s1": (1, 3, 16), "4-AR-n200-r01-V-XB-s1": (1, 3, 16)}
J = lambda p: json.load(open(p))
leg = next(l.split("\t")[3] for l in open(LOGF) if "\tBUILD\t" in l)
refs = J(REFS)["4-AR-n200-r01"]
print("leg build sha256 (deploy_leg.log BUILD): %s" % leg)
tot = 0.0
for rid in CLS:
    u = os.path.join(R, rid); b = BATCH[rid]; m, im, rp = PLAN[rid]
    print("\n=== %s  [%s, %s, plan: refine_m %d, I_max %d, R' %d]" % (rid, b, CLS[rid], m, im, rp))
    cm = J(u + "/calib_meta.json")["meta"]; cj = J(u + "/calib.bin.json")
    print("calib_meta.json: N %s refine_m %s I_max %s I_used %s rule %s grid_unconverged %s escalated %s tier %s cal_status %s tau_cal %s" % (
        cm.get("N"), cm.get("refine_m"), cm.get("I_max"), cm.get("I_used"), cm.get("rule"), cm["flags"].get("grid_unconverged"), cm["flags"].get("escalated"), cm.get("tier"), cj.get("cal_status"), cm.get("tau_cal")))
    print("   triggers_fired %s; calib.bin.json settings I_max %s refine_m %s N_final %s" % (cm["flags"].get("triggers_fired"), cj["settings"]["I_max"], cj["settings"]["refine_m"], cj["settings"]["tiers"][0]["N_final"]))
    ok = (cm["N"], cm["refine_m"], cm["I_max"], cm["rule"]) == (2500, m, im, "bounded") and (im != 0 or cm["I_used"] == 0)
    print("   ARM IDENTITY vs plan: %s" % ("MATCH" if ok else "MISMATCH"))
    isl = sorted(glob.glob(u + "/island_*.bin.json"), key=lambda p: int(re.search(r"island_(\d+)", p).group(1)))
    Ts = sorted({J(p)["T"] for p in isl}); Ns = sorted({J(p)["N"] for p in isl}); st = sorted({J(p)["status"] for p in isl})
    print("islands: %d (plan R' %d), island T values %s, N %s, status %s; T %% 4 == 0: %s; T >= 36: %s" % (len(isl), rp, Ts, Ns, st, all(t % 4 == 0 for t in Ts), all(t >= 36 for t in Ts)))
    diag = sorted(os.listdir(u + "/cost")); dk = sorted({int(re.search(r"_k(\d+)_", f).group(1)) for f in diag if f.startswith("cost_diag")}); dn = sum(f.startswith("cost_diag") for f in diag)
    print("cost/: %d files; cost_diag files %d, diagnostic rebuild indices k %s; pilot files %d" % (len(diag), dn, dk, sum(f.startswith("cost_pilot") for f in diag)))
    sj = J(u + "/setup.bin.json"); print("setup.bin.json partition: %r" % sj.get("partition"))
    t = J(u + "/truth.json"); print("truth.json X_sha256 %s.. y_sha256 %s..; == overlap rep-1 record: %s" % (t["X_sha256"][:12], t["y_sha256"][:12], (t["X_sha256"], t["y_sha256"]) == (refs["X_sha256"], refs["y_sha256"])))
    shas = set()
    for p in glob.glob(u + "/*.json") + glob.glob(u + "/*/*.json"):
        if "/log/" in p or "/cost/" in p or "/manifests/" in p: continue
        d = J(p)
        if isinstance(d, dict) and isinstance(d.get("binary"), dict) and "sha256" in d["binary"]: shas.add(d["binary"]["sha256"])
    print("binary.sha256 in the unit's %s json records: %s -> %s the leg build" % ("sidecar", sorted(x[:16] for x in shas), "EQUAL to" if shas == {leg} else "NOT equal to"))
    ev = J(u + "/eval.bin.json"); print("eval.bin.json: status %s fit_status %s; evidence.logZ_r length %d (all finite: %s); fit.meta.occ present: %s; selection.hpm %s" % (
        ev["status"], ev["fit_status"], len(ev["evidence"]["logZ_r"]), all(abs(x) < 1e9 for x in ev["evidence"]["logZ_r"]), "occ" in ev["fit"]["meta"], ev["selection"]["hpm"]))
    for fn in ("fit.bin",):
        tmp = tempfile.mkdtemp(dir=os.path.dirname(R)); rec = os.path.join(tmp, "r.json")
        subprocess.run(["nice", "-n", "19", BIN, "info", os.path.join(u, fn), "--meta", "1", "--record", rec], check=True, stdout=subprocess.DEVNULL)
        r = J(rec); print("%s readable via info: verified %s, verified_sections %s, %d sections" % (fn, r.get("verified"), r.get("verified_sections"), len(r["sections"]))); subprocess.run(["rm", "-rf", tmp])
    c = J("%s/_batch_%s/cost/cost_%s.json" % (R, b, rid)); tot += c["billed_core_h"]
    E, soft, hard = TABLE[CLS[rid]]
    print("COST: fit total %.2f core-h; class model E %.2f, soft %.1f, hard %.1f -> %s (%.2f x E)" % (c["billed_core_h"], E, soft, hard, "within soft" if c["billed_core_h"] <= soft else ("SOFT TRIP" if c["billed_core_h"] <= hard else "HARD"), c["billed_core_h"] / E))
    for s, x in c["stages"].items():
        print("   %-9s tasks %2d  wall_max %4d s  billed %7.4f core-h  maxRSS %7.1f MB  states %s" % (s, x["tasks"], x["wall_s_max"], x["billed_core_h"], x["max_rss_bytes"] / 1e6, x["states"]))
print("\nWAVE actual (sum of the 4 fits, p1m_cost.py from the sacct dump): %.2f core-h; quote 25, stop 50; batch files: %s" % (tot, ", ".join("%s %.2f" % (b, J("%s/_batch_%s/cost/cost_batch.json" % (R, b))["billed_core_h"]) for b in ("PL_A0_1", "PL_A0_2", "PL_A0_3"))))
print("\ncalibrate array task -> fit (from starts.jsonl, task numbers as logged by the stage scripts):")
for b in ("PL_A0_1", "PL_A0_2", "PL_A0_3"):
    sub = [json.loads(l) for l in open("%s/_batch_%s/submissions.jsonl" % (R, b))]; jid = {x["stage"]: x["job"] for x in sub if x["fit"] == "all"}
    dec = json.JSONDecoder(); recs = []; glued = 0; bad = 0
    for l in open("%s/_batch_%s/starts.jsonl" % (R, b)):
        l = l.strip(); n = 0
        while l:
            try:
                x, e = dec.raw_decode(l); l = l[e:].lstrip(); n += 1; recs.append(x) if isinstance(x, dict) else None
            except ValueError:   # a fragment of an interleaved concurrent append: skipped and counted
                bad += 1; k = l.find('{"stage"', 1); l = l[k:] if k > 0 else ""
        glued += n > 1
    print("   %s starts.jsonl: %d records, %d line(s) with two glued records, %d unparseable fragment(s) (concurrent appends of simultaneously started island tasks; sacct is authoritative)" % (b, len(recs), glued, bad))
    for x in recs:
        if x["stage"] in ("setup", "calibrate"): print("   %s %s job %s task %s -> %s on %s" % (b, x["stage"], x["job"], x["task"], x["run_id"], x["host"]))
    print("   %s submitted: setup array %s, calibrate array %s" % (b, jid["setup"], jid["calibrate"]))
