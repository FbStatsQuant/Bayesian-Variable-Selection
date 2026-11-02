"""N2: divergence between pi and pi0 as the cross-block link psi sweeps through the masking point.

Design (exact Gram, X'X = (n-1) Sigma): p = 16, four groups of 4 (within-group rho = 0.7, scenario S3), hubs at
positions 0, 4, 8; truth theta_0 = 1.4, theta_4 = -0.7, theta_8 = 1.8 (group 3 null).  Cross-block dependence:
a rank-one link between the hubs 0 and 4 (W1-EXP family LH): corr(x_0, x_4) = psi, Sigma[C_0, C_1] =
psi Sigma[C_0, 0] Sigma[4, C_1].  The leakage remainder Lambda_b is exactly 0 for every psi, and the effective
coefficient of the hub 4 is theta_tilde_4 = -0.7 + 1.4 psi (zero at psi = 0.5): WS5 predicts masking exactly
there and nowhere else, although the raw cross-block correlation keeps growing with psi.
Also: a 'common factor' arm (scenario S5-like, all cross-block correlations gamma) for comparison.

Usage: python sweep_link.py <out.json> [reps]
Seed: 20261102 + 1000*arm + 100*psi_index + n_index.
"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from metrics import row_metrics
from wstab_core import Problem, Space, suff_exact_gram

G, g, RHO = 4, 4, 0.7
p = G * g
groups = [list(range(h * g, (h + 1) * g)) for h in range(G)]
theta = np.zeros(p)
theta[0], theta[4], theta[8] = 1.4, -0.7, 1.8
S0 = [0, 4, 8]
Sref = [0, 8]


def sigma_link(psi):
    S = np.zeros((p, p))
    for C in groups:
        S[np.ix_(C, C)] = RHO
    np.fill_diagonal(S, 1.0)
    cross = psi * np.outer(S[groups[0], 0], S[4, groups[1]])
    S[np.ix_(groups[0], groups[1])] = cross
    S[np.ix_(groups[1], groups[0])] = cross.T
    return S


def sigma_factor(gam):
    S = np.full((p, p), gam)
    for C in groups:
        S[np.ix_(C, C)] = gam + (1 - gam) * RHO
    np.fill_diagonal(S, 1.0)
    return S


def main(out, reps):
    NS = [100, 400, 1600, 6400, 25600]
    arms = {"link": (sigma_link, [0.0, 0.2, 0.35, 0.45, 0.5, 0.55, 0.65, 0.8, 0.9]),
            "factor": (sigma_factor, [0.0, 0.1, 0.2, 0.3, 0.4])}
    res = dict(p=p, S0=S0, Sref=Sref, theta=theta.tolist(), rho=RHO, rows=[])
    import os
    done = set()
    if os.path.exists(out):                      # resume: keep finished (arm, psi, n) cells
        old = json.load(open(out))
        cnt = {}
        for x in old["rows"]:
            cnt[(x["arm"], x["psi"], x["n"])] = cnt.get((x["arm"], x["psi"], x["n"]), 0) + 1
        done = {k for k, c in cnt.items() if c >= reps}
        res["rows"] = [x for x in old["rows"] if (x["arm"], x["psi"], x["n"]) in done]
    space = Space(p, p)
    t0 = time.time()
    for ai, (arm, (fn, grid)) in enumerate(arms.items()):
        for k, psi in enumerate(grid):
            Sig = fn(psi)
            assert np.linalg.eigvalsh(Sig).min() > 0
            for ni, n in enumerate(NS):
                if (arm, psi, n) in done:
                    continue
                rng = np.random.default_rng(20261102 + 1000 * ai + 100 * k + ni)
                rows = []
                for rep in range(reps):
                    R, r, ex = suff_exact_gram(Sig, theta, n, 1.0, rng)
                    P = Problem(R, r, n, space=space)
                    m = row_metrics(P, S0, theta=theta, ref=Sref, grid=True)
                    m.update(arm=arm, psi=psi, n=n, rep=rep,
                             blocks_are_groups=sorted(map(sorted, P.blocks)) == sorted(map(sorted, groups)))
                    rows.append(m)
                res["rows"].extend(rows)
                med = lambda key: float(np.median([x[key] for x in rows]))
                print(f"{arm:6s} psi={psi:.2f} n={n:6d} | pi0(S0)={med('pi0_S0'):.3g} pi(S0)={med('pi_S0'):.3g} "
                      f"q2(S0)={med('q2_S0'):.3g} ESS={med('ess_frac'):.3g} TV={med('tv'):.3g} "
                      f"KL={med('kl_pi_pi0'):.3g} KLr={med('kl_pi0_pi'):.3g} T={med('T_grid'):.0f} "
                      f"|tt|min={rows[0]['min_abs_theta_tilde']:.3f} Lam={rows[0]['max_Lambda']:.2e} "
                      f"epsS0={med('eps_S0'):.3f} grp={np.mean([x['blocks_are_groups'] for x in rows]):.2f} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
                with open(out, "w") as f:
                    json.dump(res, f)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12)
