"""Small reproduction using the pinned prior referee's implementation.

This is explicitly a reproduction, not independently written numerical code.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources/W3-VT38E/scripts"))
import cfi

X, y, info = cfi.build_cf(400, 2, 1)
model = cfi.Model(X, y, info)
blocks, _ = cfi.complete_linkage_blocks(X, info["B"])
start = cfi.Start(model, blocks, info["S0"])
centre, logmass = start.mode()
ell = math.ceil(math.log2(400 + info["p"] + 1))
path, scored, stop = cfi.local_search(model, centre, ell)
assert info["S0"] in scored
result = dict(n=400, p=info["p"], B=info["B"], seed=1, ell=ell,
              centre=[j + 1 for j in centre], centre_mass=math.exp(logmass),
              path=[[j + 1 for j in S] for S in path],
              truth=[j + 1 for j in info["S0"]], truth_scored=True,
              scored_models=len(scored), termination=stop)
(ROOT / "results/ls0_reproduction.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
