#!/usr/bin/env python3
"""write_prior.py <wave> [--records DIR] [--out FILE] -- F3: the PRIOR file of the monitor (stop_rules_prec.py --prior / PRIOR=), written at each read-back.
prior_after_<wave>.json = {run_id: billed core-h}, CUMULATIVE over ALL waves up to and INCLUDING <wave> (A0, P1..P4, S1..S9 in plan order), from the collected cost records
records/precision1e4/<wave>/_batch_PL_<wave>_<i>/cost/cost_<run_id>.json (p1m_cost.py output, billed = sacct CPUTimeRAW / 3600). The monitor of the NEXT wave passes
PRIOR=<this file>, so its cumulative and projection rules count earlier waves (and must NOT include the monitored wave's own run ids). A run id collected twice (a rerun) is
summed (it is spent core-h). Values rounded to 2 decimals. A sidecar <file>.sources lists the cost files used. Stdlib only. Read-only on the records."""
import argparse, glob, json, os, sys
ORDER = ["A0", "P1", "P2", "P3", "P4", "FZ", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "H1", "H2", "H3"]
ap = argparse.ArgumentParser(); ap.add_argument("wave"); ap.add_argument("--records", default="/home/fb31/SMC_Engineering_Department/records/precision1e4")
ap.add_argument("--out"); a = ap.parse_args()
if a.wave not in ORDER:
    sys.exit("unknown wave %r" % a.wave)
prior, src = {}, []
for w in ORDER[:ORDER.index(a.wave) + 1]:
    for f in sorted(glob.glob(os.path.join(a.records, w, "_batch_PL_%s_*" % w, "cost", "cost_4-*.json"))):
        j = json.load(open(f)); rid = j["run_id"]; prior[rid] = prior.get(rid, 0.0) + j["billed_core_h"]; src.append(f)
if not prior:
    sys.exit("no cost records found under %s for waves up to %s" % (a.records, a.wave))
out = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prior_after_%s.json" % a.wave)
json.dump({k: round(v, 2) for k, v in prior.items()}, open(out, "w"), indent=1); open(out, "a").write("\n")
open(out + ".sources", "w").write("\n".join(src) + "\n")
print("%s: %d fits, %.2f core-h (waves up to and including %s) -> %s" % (os.path.basename(out), len(prior), sum(round(v, 2) for v in prior.values()), a.wave, out))
