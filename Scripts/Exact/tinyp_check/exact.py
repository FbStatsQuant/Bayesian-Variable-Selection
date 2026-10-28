"""Tiny-p check, part 2 (CRITERIA.md): exact posterior by B's frozen oracle, one JSON per dataset.

Usage: python -B exact.py ORACLE_DIR DATA_DIR OUT_DIR
ORACLE_DIR is B's frozen oracle folder (b_payload/oracle); its oracle_score.py is used unchanged.
"""
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

oracle_dir, data_dir, out_dir = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(oracle_dir))
import oracle_score  # noqa: E402

out_dir.mkdir(parents=True, exist_ok=False)
for meta_path in sorted(data_dir.glob("D*_rep*.json")):
    meta = json.loads(meta_path.read_text())
    n, p, ident = meta["n"], meta["p"], meta["id"]
    # R wrote X column-major float64 little-endian; reshape in Fortran order.
    X = np.fromfile(data_dir / (ident + ".X.bin"), dtype="<f8").reshape((n, p), order="F")
    y = np.fromfile(data_dir / (ident + ".y.bin"), dtype="<f8")
    assert y.shape == (n,)
    t0 = time.time()
    scorer = oracle_score.Scorer(X, y)
    assert scorer.status == "ready" and scorer.p == p, (ident, scorer.status, scorer.p)
    e = oracle_score.enumerate_exact(scorer)
    e.update(id=ident, n=n, p=p, K=scorer.K, seconds=time.time() - t0,
             oracle_sha256=hashlib.sha256((oracle_dir / "oracle_score.py").read_bytes()).hexdigest())
    (out_dir / (ident + ".exact.json")).write_text(json.dumps(e, indent=1) + "\n")
    print(ident, "enumerated", e["enumerated"], "log_Z_bf %.6f" % e["log_Z_bf"],
          "hpm", [j + 1 for j in e["hpm"]], "%.1fs" % e["seconds"], flush=True)
print("EXACT_DONE")
