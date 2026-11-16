"""W3-AUDIT track C -- collect task CSVs into summary.csv (median, q10, q90 over reps per design/cell/placement/proxy/
key) and trend.csv (log-log slope in n of |median| along the p = n and p = 10n series; the p = 2e4 cap cells are listed
at equal n).  numpy + csv only (no pandas on Owls).
Usage: python3 c_collect.py OUT_DIR [OUT_DIR2 ...] --to DEST_DIR"""
import csv
import glob
import os
import sys
from collections import defaultdict

import numpy as np

args = sys.argv[1:]
dest = args[args.index("--to") + 1]; srcs = args[:args.index("--to")]
files = sorted(f for s in srcs for f in glob.glob(os.path.join(s, "D*_n*_p*.csv")))
acc = defaultdict(list)
for f in files:
    with open(f) as fh:
        for r in csv.DictReader(fh):
            if r["proxy"] == "time":
                continue
            try:
                v = float(r["value"])
            except ValueError:
                continue
            acc[(int(r["design"]), r["name"], int(r["n"]), int(r["p"]), r["placement"], r["proxy"], r["key"])].append(v)


def series(n, p):
    if p == n:
        return "p=n"
    if p == 10 * n:
        return "p=10n"
    return "cap"


os.makedirs(dest, exist_ok=True)
summ = []
for k in sorted(acc):
    v = np.array(acc[k])
    summ.append(k + (float(np.median(v)), float(np.quantile(v, 0.1)), float(np.quantile(v, 0.9)), v.size, series(k[2], k[3])))
with open(os.path.join(dest, "summary.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["design", "name", "n", "p", "placement", "proxy", "key", "median", "q10", "q90", "reps", "series"])
    for r in summ:
        w.writerow(list(r[:7]) + [f"{x:.6g}" for x in r[7:10]] + list(r[10:]))

grp = defaultdict(list)
for r in summ:
    grp[(r[0], r[1], r[4], r[5], r[6], r[11])].append((r[2], r[7]))
with open(os.path.join(dest, "trend.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["design", "name", "placement", "proxy", "key", "series", "ns", "vals", "loglog_slope"])
    for k in sorted(grp):
        pts = sorted(grp[k])
        ns = np.array([a for a, _ in pts], float); ys = np.array([b for _, b in pts])
        sl = ""
        if k[5] != "cap" and len(pts) >= 2 and np.all(np.isfinite(ys)) and np.all(np.abs(ys) > 0):
            sl = f"{np.polyfit(np.log(ns), np.log(np.abs(ys)), 1)[0]:.3f}"
        w.writerow(list(k) + [" ".join(str(int(a)) for a in ns), " ".join(f"{b:.4g}" for b in ys), sl])
print(f"{len(files)} task files, {len(summ)} summary rows -> {dest}/summary.csv, trend.csv")
