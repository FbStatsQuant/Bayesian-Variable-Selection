"""F-SHARE H2 addendum: exact bridge-law mass q_phi(H), q_phi(W0), q_phi(!W2) on the method grid vs the simulated
per-stage fractions (mean over the 4 islands of dataset 0) for LH16, same datasets/seeds as f2_sim_lh.py."""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from bvs_core import BVS, suff_stats, popcount, lse
from lh_design import lh_config
c = lh_config("LH16"); p = c["p"]
recs = json.load(open(os.path.join(HERE, "..", "results", "f2_sim_lh_LH16.json")))
S0m = sum(1 << j for j in c["S0"]); Srefm = sum(1 << j for j in c["Sref"]); Mm = sum(1 << j for j in c["M"])
allm = np.arange(1 << p, dtype=np.int64)
W = (allm & Srefm) == Srefm; W0 = (allm & ~Mm) == Srefm; W2 = W & (popcount(allm & ~S0m) <= 2); H = (allm & S0m) == S0m
out = []
for n in (400, 1600, 6400):
    z, yy = suff_stats(c["R"], c["theta"], 1.0, n, np.random.default_rng(1000 * n))
    m = BVS(c["R"], z, yy, n, c["S0"])
    rs = [r for r in recs if r["n"] == n and r["ds"] == 0]
    grid = np.array(rs[0]["grid"])
    out.append(f"LH16 n={n} ds0: stage phi | exact q(H) sim fH | exact q(W0) sim fW0 | exact q(!W2) sim f!W2 | exact q(!W)")
    for t, ph in enumerate(grid):
        q = np.exp(m.logq(ph))
        sim = {k: np.mean([r["counts"][k][t] / r["N"] for r in rs]) for k in ("H", "W0", "W2")}
        out.append(f"  {t:>2} {ph:.4f} | {q[H].sum():.3f} {sim['H']:.3f} | {q[W0].sum():.3f} {sim['W0']:.3f} | "
                   f"{1-q[W2].sum():.4f} {1-sim['W2']:.4f} | {1-q[W].sum():.2e}")
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "..", "results", "f2_qH_check.txt"), "w").write(txt + "\n")
