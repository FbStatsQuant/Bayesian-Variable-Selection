#!/usr/bin/env python3
"""Assemble B1/cross_vt.json (schema overlap1e4.cross_vt/1) from cross/cross_*.json. Pair key = the dataset label the scorer builds (ds_id: '4-ARweak-n200-r91', cosmetic n200; ADDENDUM_1_BOUNDARY)."""
import json, glob, os
here = os.path.dirname(os.path.abspath(__file__)); pairs, records, files = {}, {}, []
for f in sorted(glob.glob(here + "/cross/cross_*_s[12].json")):
    j = json.load(open(f)); assert j["status"] == "completed", f
    (ds, cells), = j["pairs"].items(); (s, c), = cells.items(); key = "4-ARweak-n200-r91"
    pairs.setdefault(key, {})[s] = c; records["%s/%s" % (key, s)] = {"xeval": j["xeval"], "inputs": j.get("inputs"), "binary": j.get("binary"), "source_dataset_label": ds}; files.append(os.path.relpath(f, here))
json.dump({"schema": "overlap1e4.cross_vt/1", "pairs": pairs, "records": records, "merged_from": files}, open(here + "/cross_vt.json", "w"), indent=1)
print({k: sorted(v) for k, v in pairs.items()})
