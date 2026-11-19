#!/usr/bin/env python3
"""merge cross_vt.json of W0..W3 into cross_vt_all.json (10 datasets x 2 seeds = 20 cells); error on a duplicate cell."""
import json, sys, os
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.dirname(here)
files = [os.path.join(base, "W%d_readback" % i, "cross_vt.json") for i in range(4)]
pairs, records = {}, {}
for f in files:
    d = json.load(open(f))
    for ds, cells in d["pairs"].items():
        for s, c in cells.items():
            if s in pairs.get(ds, {}): sys.exit("duplicate cell %s/%s in %s" % (ds, s, f))
            pairs.setdefault(ds, {})[s] = c
    for k, v in d.get("records", {}).items():
        records[k] = v
n = sum(len(v) for v in pairs.values())
json.dump({"schema": "overlap1e4.cross_vt/1", "pairs": pairs, "records": records, "merged_from": files}, open(os.path.join(here, "cross_vt_all.json"), "w"), indent=1)
print(len(pairs), "datasets,", n, "cells")
for ds in sorted(pairs): print(ds, sorted(pairs[ds]))
