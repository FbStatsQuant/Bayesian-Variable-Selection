#!/usr/bin/env python3
"""w2_t_validity.py -- is each W2 T fit a full valid fit?  4 islands at N = calib N_final, merge/eval completed, non-stub fit/eval.
stdlib only; read-only on records/overlap1e4/W2; prints a table and writes W2_T_fit_validity.csv"""
import csv, glob, json, os, re, sys
REC = os.path.expanduser("~/SMC_Engineering_Department/records/overlap1e4/W2")
rows = []
for u in sorted(glob.glob(REC + "/*-T-s*")):
    j = lambda n: json.load(open(os.path.join(u, n)))
    cb, fm, rm, lj, ev = j("calib.bin.json"), j("fit.bin.json"), j("run_manifest.json"), j("law.bin.json"), j("eval.bin.json")
    tf = cb["tier_final"]; Nf = [t["N_final"] for t in cb["settings"]["tiers"] if t["tier"] == tf][0]
    isl = [j("island_%d.bin.json" % k) for k in (1, 2, 3, 4)]
    sz = lambda n: os.path.getsize(os.path.join(u, n))
    ok = (cb["status"] == "completed" and cb["cal_status"] == "ok" and len(isl) == 4
          and all(i["status"] == "completed" and i["N"] == Nf and i["tier"] == tf and i["mode"] == "law" for i in isl)
          and rm["calib_N"]["N_final"] == Nf and not rm["calib_N"]["differs"] and fm["status"] == "completed" and fm["fit_state"] == "completed"
          and ev["status"] == "completed" and ev["fit_status"] == "completed" and sz("fit.bin") > 10e6 and sz("eval.bin") > 100e3 and lj["status"] == "completed")
    rows.append({"fit": os.path.basename(u), "tier_final": tf, "N_final": Nf, "calib_status": cb["status"], "cal_status": cb["cal_status"],
                 "calib_wall_s_engine": round(cb["seconds"], 1), "island_N": "/".join(str(i["N"]) for i in isl), "island_tier": "/".join(str(i["tier"]) for i in isl),
                 "island_status": "/".join(i["status"] for i in isl), "run_manifest_calib_N_final": rm["calib_N"]["N_final"], "fit_meta_Rp": fm["Rp"], "R_eff": round(fm["R_eff"], 4),
                 "fit_status": fm["status"], "eval_status": ev["status"], "eval_fit_status": ev["fit_status"], "law_M": lj["M"], "law_status": lj["status"],
                 "fit_bin_B": sz("fit.bin"), "law_bin_B": sz("law.bin"), "eval_bin_B": sz("eval.bin"), "eval_seed_param": ev["params"]["seed"], "island_seed": isl[0]["seed"],
                 "FULL_VALID": ok})
with open("W2_T_fit_validity.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
print("all full valid:", all(r["FULL_VALID"] for r in rows))
