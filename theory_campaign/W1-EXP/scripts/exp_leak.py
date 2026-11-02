"""W1-EXP Task 2 check: two-sided chain law with controlled leakage multiplier.
Config A (p=16, exact Gram), masked coefficient perturbed so that delta_{empty, j_b} = L_n exactly:
theta_{j_b} = -psi*beta + L_n*sigma/sqrt(n-1).  Prediction (Theorem 3/4 + limit sketch):
M = log pi0(S0) + log p + 0.5 log n  ~  log((s+1)p/(2p-s-1)) + (L_n + Z)^2 sigma^2/(2 v),  Z ~ N(0,1).
Seed 20261102 + 77*case + n_index."""
import json, math, sys
import numpy as np
from bvs_exact import block_size_B, make_blocks, tables, start_masses, start_logmass
from family import lh_sigma, lh_truth, suff_exact_gram
G, g, psi, beta = 4, 4, 0.5, 1.4
Sig, groups = lh_sigma(G, g, 0.7, 0, [(0, 1, psi)])
th0, S0, M, Sref = lh_truth(G, g, 0, [(0, 1, psi)], {0: 1.4, 2: 1.8})
p, s, jb = G * g, len(Sref), M[0]
NS = [100, 400, 1600, 6400, 25600, 102400, 409600, 1638400]
cases = [("L=0", lambda n: 0.0), ("L=2", lambda n: 2.0), ("L=4", lambda n: 4.0),
         ("L=sqrt(0.5 log n)", lambda n: math.sqrt(0.5 * math.log(n))), ("L=sqrt(2 log n)", lambda n: math.sqrt(2 * math.log(n)))]
out = []
for ci, (name, Lf) in enumerate(cases):
    for ni, n in enumerate(NS):
        rng = np.random.default_rng(20261102 + 77 * ci + ni)
        L = Lf(n)
        th = th0.copy(); th[jb] += L / math.sqrt(n - 1)
        v = 1 + th @ Sig @ th
        B = block_size_B(n, p)
        bl = make_blocks(Sig, B)
        Ms, refs = [], []
        for rep in range(300):
            R, r = suff_exact_gram(Sig, th, n, 1.0, rng)
            tabs = tables(bl, R, r, n)
            sm = start_masses(bl, tabs, p, n, S0)
            Ms.append(start_logmass(bl, tabs, p, n, S0, sm["logZ0"]) + math.log(p) + 0.5 * math.log(n))
            refs.append(math.exp(start_logmass(bl, tabs, p, n, Sref, sm["logZ0"])))
        z = np.random.default_rng(1).standard_normal(200000)
        pred = math.log((s + 1) * p / (2 * p - s - 1)) + (L + z) ** 2 / (2 * v)
        row = dict(case=name, n=n, L=L, M_q05=float(np.quantile(Ms, .05)), M_med=float(np.median(Ms)),
                   M_q95=float(np.quantile(Ms, .95)), pred_q05=float(np.quantile(pred, .05)),
                   pred_med=float(np.median(pred)), pred_q95=float(np.quantile(pred, .95)),
                   med_pi0_Sref=float(np.median(refs)))
        out.append(row); print(json.dumps({k: (round(x, 3) if isinstance(x, float) else x) for k, x in row.items()}), flush=True)
json.dump(out, open("../results/leak_chain.json", "w"))
