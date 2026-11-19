#!/usr/bin/env python3
"""extract_measured.py -- the MEASURED V costs of the 10^4 overlap (20 counted V fits, n = 200, N = 2,500, R' = 16) that the
precision-leg quote is built on. Stdlib only, read-only. Output: measured_V_costs.csv (one row per V fit).

Inputs: results/overlap1e4/W{0..3}_readback/W*_cost_stages.csv (billed core-h per stage, sacct CPUTimeRAW/3600; role COUNTS (V) only,
the 'TOTAL' pseudo-stage is ignored) and the island records records/overlap1e4/W*/<run_id>/island_1.bin.json (T = number of
bridging stages of the frozen grid). Usage: extract_measured.py --overlap <results/overlap1e4> --records <records/overlap1e4> --out measured_V_costs.csv
"""
import argparse, csv, glob, json, os, re

ap = argparse.ArgumentParser(); ap.add_argument("--overlap", required=True); ap.add_argument("--records", required=True); ap.add_argument("--out", required=True)
a = ap.parse_args()
num = lambda x: float(x) if x not in ("", None) else 0.0
st = {}
for fn in sorted(glob.glob(os.path.join(a.overlap, "W*_readback", "W*_cost_stages.csv"))):
    for r in csv.DictReader(open(fn)):
        if r["role"] != "COUNTS (V)" or r["stage"] == "TOTAL":
            continue
        st.setdefault(r["fit"], {}).setdefault(r["stage"], 0.0)
        st[r["fit"]][r["stage"]] += num(r["billed_core_h"])
rows = []
for run in sorted(st):
    m = re.match(r"4-(\w+)-n200-r(\d+)-V-s(\d)$", run)
    d = glob.glob(os.path.join(a.records, "W*", run))
    assert m and len(d) == 1, run
    T = json.load(open(os.path.join(d[0], "island_1.bin.json")))["T"]
    s = st[run]
    rows.append([run, m.group(1), int(m.group(2)), int(m.group(3)), T, round(s["setup"], 4), round(s["calibrate"], 4), round(s["islands"], 4),
                 round(s["islands"] / 16, 5), round(s["merge"], 4), round(s["eval"], 4), round(sum(s.values()), 4)])
with open(a.out, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["run_id", "design", "rep", "seed", "T", "setup", "calibrate", "islands_total", "per_island", "merge", "eval", "fit_total"])
    w.writerows(rows)
print("wrote %d V fits to %s; fit_total mean %.3f" % (len(rows), a.out, sum(r[-1] for r in rows) / len(rows)))
