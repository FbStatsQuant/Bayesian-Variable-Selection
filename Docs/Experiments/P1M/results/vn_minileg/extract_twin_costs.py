#!/usr/bin/env python3
"""extract_twin_costs.py -- the MEASURED stage costs of the N = 2,500 twins of the V-N mini-leg's fits (precision leg, F build d0c30b65) and of the r04 science fit. Stdlib, read-only.
  extract_twin_costs.py --records ~/SMC_Engineering_Department/records/precision1e4 --out twin_costs.csv
Rows: every `4-*-n200-r01-P-N2500-m1[-I0]-c[12]-s1` fit (stage billed core-h from the batch cost files `cost_<run>.json`, T = island_1.bin.json T) and `4-ADJOPP-n200-r04-V-s1`."""
import argparse, csv, glob, json, os, re

ap = argparse.ArgumentParser(); ap.add_argument("--records", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
rows = []
for p in sorted(glob.glob(os.path.join(a.records, "*", "_batch_*", "cost", "cost_4-*.json"))):
    j = json.load(open(p)); rid = j["run_id"]
    if not (re.match(r"^4-(AR|ARweak|ADJOPP)-n200-r01-P-N2500-m1(-I0)?-c[12]-s1$", rid) or rid == "4-ADJOPP-n200-r04-V-s1"):
        continue
    d = os.path.join(p.split("/_batch_")[0], rid)
    T = json.load(open(os.path.join(d, "island_1.bin.json")))["T"]
    st = {k: v["billed_core_h"] for k, v in j["stages"].items()}
    cm = json.load(open(os.path.join(d, "calib_meta.json"))); cm = cm.get("meta", cm)
    rows.append([rid, cm.get("I_max"), cm.get("N"), T] + [round(st.get(k, 0.0), 4) for k in ("setup", "calibrate", "islands", "merge", "eval")] + [round(j["billed_core_h"], 3)])
with open(a.out, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["run_id", "I_max", "N", "T", "setup", "calibrate", "islands", "merge", "eval", "fit_total"]); w.writerows(rows)
print("wrote %d fits to %s" % (len(rows), a.out))
