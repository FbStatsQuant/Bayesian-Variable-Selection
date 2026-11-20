#!/usr/bin/env python3
"""gb_write_prior.py <G1|G2> [--out FILE] -- prior_after_<wave>.json = {run_id: billed core-h}, CUMULATIVE over the G-B waves up to and INCLUDING <wave>, from the collected cost records
records/gb/<batch>/_batch_<batch>/cost/cost_5-*.json (p1m_cost.py, billed = sacct CPUTimeRAW / 3600). The monitor of the NEXT wave passes PRIOR=<this file>. Read-only on the records. Stdlib only."""
import argparse, glob, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("wave"); ap.add_argument("--records", default="/home/fb31/SMC_Engineering_Department/records/gb"); ap.add_argument("--out"); a = ap.parse_args()
order = ["G1", "G2"]
if a.wave not in order: sys.exit("unknown wave %r" % a.wave)
prior, src = {}, []
for w in order[:order.index(a.wave) + 1]:
    for f in sorted(glob.glob(os.path.join(a.records, "GB_%s[a-z]" % w, "_batch_GB_%s[a-z]" % w, "cost", "cost_5-*.json"))):
        j = json.load(open(f)); prior[j["run_id"]] = prior.get(j["run_id"], 0.0) + j["billed_core_h"]; src.append(f)
if not prior: sys.exit("no cost records under %s up to %s" % (a.records, a.wave))
out = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prior_after_%s.json" % a.wave)
json.dump({k: round(v, 2) for k, v in prior.items()}, open(out, "w"), indent=1); open(out, "a").write("\n"); open(out + ".sources", "w").write("\n".join(src) + "\n")
print("%s: %d fits, %.2f core-h (up to and including %s) -> %s" % (os.path.basename(out), len(prior), sum(round(v, 2) for v in prior.values()), a.wave, out))
