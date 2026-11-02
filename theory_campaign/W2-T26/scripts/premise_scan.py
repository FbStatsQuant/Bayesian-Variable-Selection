"""Step 4: are the premises (P1), (P2) of Theorem A non-vacuous at exact small p?

p = 18 is the smallest p at which SMC-BVS v3 takes the SMC branch for n >= 22 (2^18 > 12,560*18), so every model
here is one the actual method would NOT enumerate. B = 4, s0 = 3.

Designs (sigma* = 1):
  fav_iid : iid N(0,1) columns; S0 = {0, 6, 12}; beta = 0.6 on S0.
  fav_cor : 6 groups of 3 columns, within-group correlation 0.5; S0 = {0, 6, 12} (one per group); beta = 0.6.
  masked  : as fav_cor, plus column 3 correlated 0.6 with column 0 (cross-group); S0 = {0, 3, 12},
            beta_0 = 1, beta_3 = -0.6, beta_12 = 0.6, so x_3 has zero marginal covariance with the mean.
For each n and seed it records the exact premise quantities. Output: results/premise_scan.csv
Seeds: numpy default_rng(1000*design_index + seed).
"""
import sys, os, csv, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from bvs_exact import Problem

P = 18
NS = [40, 80, 160, 320, 640, 1280, 2560, 5120]


def design(name, n, rng):
    if name == 'fav_iid':
        X = rng.standard_normal((n, P))
        beta = np.zeros(P); S0 = [0, 6, 12]; beta[S0] = 0.6
    else:
        rho = 0.5
        Zg = rng.standard_normal((n, 6))
        E = rng.standard_normal((n, P))
        X = np.empty((n, P))
        for j in range(P):
            X[:, j] = np.sqrt(rho) * Zg[:, j // 3] + np.sqrt(1 - rho) * E[:, j]
        beta = np.zeros(P)
        if name == 'fav_cor':
            S0 = [0, 6, 12]; beta[S0] = 0.6
        else:  # masked
            # make x_3 correlated 0.6 with x_0 across groups
            X[:, 3] = 0.6 * X[:, 0] + np.sqrt(1 - 0.36) * X[:, 3]
            S0 = [0, 3, 12]; beta[0] = 1.0; beta[3] = -0.6; beta[12] = 0.6
    y = X @ beta + rng.standard_normal(n)
    return X, y, S0


def main():
    SEEDS = range(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results'), exist_ok=True)
    path = os.path.join(os.path.dirname(__file__), '..', 'results', 'premise_scan.csv')
    fields = ['design', 'n', 'seed', 'B', 'L', 'Tmax', 'blocks', 'one_minus_pi0', 'delta1', 'Delta', 'Delta_grid',
              'u_pi', 'rho_star', 'rho_bar_bound', 'T_ideal', 'P1_Tideal', 'P1_Tmax', 'P2', 'S0_is_HPM',
              'S0_is_start_mode']
    with open(path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for di, name in enumerate(['fav_iid', 'fav_cor', 'masked']):
            for n in NS:
                for seed in SEEDS:
                    t0 = time.time()
                    rng = np.random.default_rng(1000 * di + seed + 7919 * n)
                    X, y, S0 = design(name, n, rng)
                    pr = Problem(X, y, S0)
                    q = pr.premise()
                    grid = pr.ideal_grid()
                    Ti = len(grid) - 1 if grid else -1
                    row = dict(design=name, n=n, seed=seed, B=pr.B, L=pr.L, Tmax=pr.Tmax,
                               blocks='|'.join(','.join(map(str, b)) for b in pr.blocks), **q,
                               T_ideal=Ti, P1_Tideal=(Ti + 1) * q['Delta'], P1_Tmax=(pr.Tmax + 1) * q['Delta'],
                               P2=(pr.L + 4) * q['rho_star'],
                               S0_is_HPM=int(np.argmax(pr.lg1) == pr.S0),
                               S0_is_start_mode=int(np.argmax(pr.lg0) == pr.S0))
                    w.writerow(row)
                    fh.flush()
                    print(name, n, seed, f"1-pi0={q['one_minus_pi0']:.2e} d1={q['delta1']:.2e} "
                          f"Dgrid-D={q['Delta_grid'] - q['Delta']:.1e} rhobar<={q['rho_bar_bound']:.2e} "
                          f"rho*={q['rho_star']:.2e} T={Ti} P1max={row['P1_Tmax']:.2e} P2={row['P2']:.2e} "
                          f"({time.time() - t0:.1f}s)", flush=True)


if __name__ == '__main__':
    main()
