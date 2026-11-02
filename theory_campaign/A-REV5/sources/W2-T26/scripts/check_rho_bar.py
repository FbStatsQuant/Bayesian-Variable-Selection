"""Monte Carlo check of Lemma 2's exact form rho_bar = 1 - prod_e (1 - K_e(S0, not S0)) using the simulator's round.
Seed: default_rng(5). Output printed (recorded in REPORT)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from bvs_exact import Problem
from smc_sim import Sim
from premise_scan import design
for name, n in [('fav_iid', 2000), ('fav_cor', 640), ('masked', 640)]:
    rng = np.random.default_rng(5)
    X, y, S0 = design(name, n, rng)
    pr = Problem(X, y, S0); q = pr.premise(); sim = Sim(pr)
    M = 200000
    S = np.full(M, pr.S0, dtype=np.int64); dep = np.zeros(M, bool)
    sim.round(S, 1.0, np.random.default_rng(6), track=dep)
    se = np.sqrt(dep.mean() * (1 - dep.mean()) / M)
    print(f"{name} n={n}: exact rho_bar={q['rho_bar']:.4f}  MC={dep.mean():.4f} (se {se:.4f})  sum-bound={q['rho_bar_bound']:.4f}  (B+3)u_pi={(pr.B+3)*q['u_pi']:.4f}")
