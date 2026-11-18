#!/usr/bin/env python3
"""make_tables.py UNITS_TSV OUTDIR -- the 121 dataset/scale subset as two chunk tables (task, dataset, p, scales).
Tier A: p in {500,1000} x S1..S6 x r in {1,25,50,75,100}, scales c100,c050 (120 fits per side) + the one p500 stop p0500_S5_r088 (scale c100 only).
Task indices are per array: p1000 = 1..30, p500 = 1..31 (the stop dataset last). Seeds come from the units table (checked against the formula)."""
import csv, sys, os
units, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(units), delimiter="\t"))
by = {r["case_id"]: r for r in rows}
BASE = {500: 1410000, 1000: 1510000}
R = [1, 25, 50, 75, 100]
def chunks(p):
    ds = [(s, r, "c100,c050") for s in range(1, 7) for r in R]
    if p == 500: ds.append((5, 88, "c100"))
    return ds
for p, name in ((1000, "chunks_p1000.tsv"), (500, "chunks_p0500.tsv")):
    with open(os.path.join(out, name), "w") as f:
        f.write("task\tdataset\tp\tscales\n")
        for i, (s, r, sc) in enumerate(chunks(p), 1):
            d = "p%04d_S%d_r%03d" % (p, s, r)
            for c in sc.split(","):
                u = by[d + "_" + c]
                ds_ = BASE[p] + 10000 * s + r
                assert int(u["data_seed"]) == ds_ and int(u["method_seed"]) == ds_ + 4000000, d
                assert int(u["p"]) == p and int(u["scenario"]) == s and int(u["replicate"]) == r
            f.write("%d\t%s\t%d\t%s\n" % (i, d, p, sc))
