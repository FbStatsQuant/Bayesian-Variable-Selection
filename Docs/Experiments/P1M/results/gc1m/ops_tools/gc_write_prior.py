#!/usr/bin/env python3
"""gc_write_prior.py <P> [--out FILE] -- prior_after_<wave>.json = {run_id: billed core-h} cumulative over the GC waves up to and including <wave>, from records/gc1m/<batch>/_batch_<batch>/cost/cost_6-*.json
(p1m_cost.py; billed = sacct CPUTimeRAW / 3600). The monitor of the NEXT wave passes PRIOR=<this file>. Read-only on the records. Stdlib only."""
import argparse, glob, json, os, sys
WAVES = {"P": ["GC_P"], "D": ["GC_D"]}
ap = argparse.ArgumentParser(); ap.add_argument("wave"); ap.add_argument("--records", default="/home/fb31/SMC_Engineering_Department/records/gc1m"); ap.add_argument("--out"); a = ap.parse_args()
if a.wave not in WAVES: sys.exit("unknown wave %r" % a.wave)
prior, src = {}, []
for w in (["P"] if a.wave == "P" else ["P", "D"]):
    for b in WAVES[w]:
        for f in sorted(glob.glob(os.path.join(a.records, b, "_batch_%s" % b, "cost", "cost_6-*.json"))):
            j = json.load(open(f)); prior[j["run_id"]] = prior.get(j["run_id"], 0.0) + j["billed_core_h"]; src.append(f)
if not prior: sys.exit("no cost records under %s" % a.records)
out = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prior_after_%s.json" % a.wave)
json.dump({k: round(v, 2) for k, v in prior.items()}, open(out, "w"), indent=1); open(out, "a").write("\n"); open(out + ".sources", "w").write("\n".join(src) + "\n")
print("%s: %d fits, %.2f core-h -> %s" % (os.path.basename(out), len(prior), sum(round(v, 2) for v in prior.values()), out))
