#!/usr/bin/env python3
"""merge_cross.py -- merge per-pair smcbvs4_xeval records into the one --cross-file of compare_overlap.py.

  merge_cross.py OUT.json cross_<dataset>_s1.json cross_<dataset>_s2.json ...

Each input is the record written by `smcbvs4_xeval cross ... --dataset ID --seed-id 1|2`; only its `pairs` object is merged
(schema overlap1e4.cross_vt/1: {"pairs": {"<dataset>": {"1": {"h2": ..., "se": ...}, "2": {...}}}}). A record whose status is
not "completed", or a cell present twice, is an error (exit 1). The per-pair `xeval` blocks are kept under `records` for audit.
"""
import json
import sys


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    out, ins = argv[1], argv[2:]
    pairs, records = {}, {}
    for f in ins:
        with open(f) as fh:
            r = json.load(fh)
        if r.get("status") != "completed" or r.get("schema") != "overlap1e4.cross_vt/1":
            print("merge_cross: %s is not a completed overlap1e4.cross_vt/1 record" % f, file=sys.stderr)
            return 1
        if not r.get("pairs"):
            print("merge_cross: %s has no pairs cell (run xeval with --dataset and --seed-id)" % f, file=sys.stderr)
            return 1
        for ds, cells in r["pairs"].items():
            for s, cell in cells.items():
                if s in pairs.get(ds, {}):
                    print("merge_cross: cell %s/%s present twice (%s)" % (ds, s, f), file=sys.stderr)
                    return 1
                pairs.setdefault(ds, {})[s] = cell
                records["%s/%s" % (ds, s)] = {"xeval": r.get("xeval"), "inputs": r.get("inputs"), "binary": r.get("binary", {}).get("sha256")}
    with open(out, "w") as fh:
        json.dump({"schema": "overlap1e4.cross_vt/1", "pairs": pairs, "records": records}, fh, indent=1)
    print("merge_cross: %d dataset(s), %d cell(s) -> %s" % (len(pairs), sum(len(v) for v in pairs.values()), out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
