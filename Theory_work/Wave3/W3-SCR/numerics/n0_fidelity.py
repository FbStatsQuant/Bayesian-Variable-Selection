"""W3-SCR N0 (fidelity): the Python score scr_lib.Score.F against the production core's F on the models the core
stored (HPM, top store, LS0 path, final-search scanned centres), on the standardised data the core itself used.
Also: (a) vectorised add_all against direct F; (b) the reported certified model is certified under the Python scan.
Usage: py -3.13 n0_fidelity.py dump/<tag>   (reads <tag>_X.csv, <tag>_y.csv, <tag>_models.json)"""
import json, sys
import numpy as np
from scr_lib import Score

tag = sys.argv[1]
X = np.loadtxt(tag + "_X.csv", delimiter=","); y = np.loadtxt(tag + "_y.csv", delimiter=",")
M = json.load(open(tag + "_models.json"))
sc = Score(X, y, standardised=True)
kept = M["kept"]; pos = {int(o): i for i, o in enumerate(kept)}
def idx(model):
    if isinstance(model, int): model = [model]
    return [pos[int(j)] for j in model]
print(f"n={sc.n} p={sc.p} K={sc.K} (core K={M['K']})  ||x_j||^2 range [{np.diag(sc.G).min():.6f},{np.diag(sc.G).max():.6f}]  y'y={sc.yty:.6f}")
ds = []
for grp, lst in M["models"].items():
    if grp == "hpm": lst = [lst]
    for e in lst:
        if e.get("F") is None: continue
        ds.append(sc.F(idx(e["model"])) - e["F"])
ds = np.array(ds)
print(f"F_py - F_core on {len(ds)} core-scored models: max |difference| = {np.abs(ds).max():.3e} (median {np.median(ds):.3e})")
rng = np.random.default_rng(1)
w2 = 0.0
for _ in range(20):
    k = int(rng.integers(0, 12)); B = sorted(rng.choice(sc.p, k, replace=False).tolist())
    fa, _ = sc.add_all(B)
    for l in rng.choice(sc.p, 5, replace=False):
        if l in B: continue
        w2 = max(w2, abs(fa[l] - sc.F(sorted(B + [int(l)]))))
print(f"vectorised additions vs direct F: max abs diff = {w2:.3e}")
h = idx(M["models"]["hpm"]["model"])
print("core HPM", sorted(h), "certified under the Python scan (tol 1e-9):", sc.is_certified(h, tol=1e-9))
