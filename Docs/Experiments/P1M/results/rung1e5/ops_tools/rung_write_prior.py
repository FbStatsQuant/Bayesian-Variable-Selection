#!/usr/bin/env python3
"""rung_write_prior.py <R1|R2|R3> [--out FILE] -- prior_after_<wave>.json = {key: billed core-h}, CUMULATIVE over the rung waves up to and INCLUDING <wave>, from the collected cost records
records/rung1e5/<batch>/_batch_<batch>/cost/cost_5-*.json (p1m_cost.py; billed = sacct CPUTimeRAW / 3600). Key = run id, except the T6 task (batch RG_T6, whose run id is the G-B pilot's): "T6:<run id>".
The monitor of the NEXT wave passes PRIOR=<this file>. Read-only on the records. Stdlib only."""
import argparse, glob, json, os, sys
WAVES = {"R1": ["RG_1a", "RG_1b", "RG_T6"], "R2": ["RG_2a", "RG_2b"], "R3": ["RG_3a", "RG_3b"]}
ap = argparse.ArgumentParser(); ap.add_argument("wave"); ap.add_argument("--records", default="/home/fb31/SMC_Engineering_Department/records/rung1e5"); ap.add_argument("--out"); a = ap.parse_args()
order = ["R1", "R2", "R3"]
if a.wave not in order: sys.exit("unknown wave %r" % a.wave)
prior, src = {}, []
for w in order[:order.index(a.wave) + 1]:
    for b in WAVES[w]:
        for f in sorted(glob.glob(os.path.join(a.records, b, "_batch_%s" % b, "cost", "cost_5-*.json"))):
            j = json.load(open(f)); k = ("T6:" if b == "RG_T6" else "") + j["run_id"]; prior[k] = prior.get(k, 0.0) + j["billed_core_h"]; src.append(f)
if not prior: sys.exit("no cost records under %s up to %s" % (a.records, a.wave))
out = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prior_after_%s.json" % a.wave)
json.dump({k: round(v, 2) for k, v in prior.items()}, open(out, "w"), indent=1); open(out, "a").write("\n"); open(out + ".sources", "w").write("\n".join(src) + "\n")
print("%s: %d items, %.2f core-h (up to and including %s) -> %s" % (os.path.basename(out), len(prior), sum(round(v, 2) for v in prior.values()), a.wave, out))
