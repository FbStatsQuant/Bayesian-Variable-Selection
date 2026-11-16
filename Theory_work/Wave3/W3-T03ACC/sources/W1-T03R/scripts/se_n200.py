#!/usr/bin/env python3
"""W1-T03R task 4: plausibility of the restricted eigenvalue conditions of T03# at n = 200, p = 500 (one design draw each).
SE_lambda(j0): lambda_min(R_{S0 u J}) >= phi0^2 for |J| <= j0 (j0 = ceil((2A+1)s0)+1 = 48 at p = 500).
SE_w(m):       lambda_min(G_{S0 u J}) >= g0 > 0 (unnormalised, G = X'X = (n-1)R) for |J| <= min(m#, K) = 100.
For each we report lambda_min for 20 random J of the maximal size and for a greedy adversarial J (add, one at a time, the
column that minimises lambda_min). The greedy value is an UPPER bound on the true minimum over J (not the minimum).
Designs: S1 = I_p; S4 = 0.85 H + 0.15 I (blocks of five); signal placement as in MASTER Part II.4 (p = 500, d = 7).
"""
import numpy as np

def design(n, p, scen, rng):
    Z = rng.standard_normal((n, p))
    if scen == "S1":
        X = Z
    else:  # S4: within-block corr 0.85 -> X = sqrt(0.85) * block factor + sqrt(0.15) * Z
        F = rng.standard_normal((n, p // 5))
        X = np.sqrt(0.85) * np.repeat(F, 5, axis=1) + np.sqrt(0.15) * Z
    X = X - X.mean(0); X = X / np.sqrt((X**2).sum(0) / (n - 1))
    return X

def support(p, s0=14, d=7):
    pos = [3, 2, 4, 1, 5]
    return [5 * (d * k) + pos[k % 5] - 1 for k in range(s0)]  # 0-based

def lmin(G):
    return np.linalg.eigvalsh(G)[0]

def greedy(G, S0, size, cand):
    T = list(S0)
    for _ in range(size):
        best, bl = None, np.inf
        for l in cand:
            if l in T: continue
            idx = T + [l]
            v = lmin(G[np.ix_(idx, idx)])
            if v < bl: bl, best = v, l
        T.append(best)
    return T, bl

if __name__ == "__main__":
    n, p, s0 = 200, 500, 14
    rng = np.random.default_rng(20261102)
    for scen in ("S1", "S4"):
        X = design(n, p, scen, rng); G = X.T @ X; R = G / (n - 1)
        S0 = support(p, s0)
        others = [j for j in range(p) if j not in S0]
        print(f"== {scen}: lambda_min(R_S0) = {lmin(R[np.ix_(S0, S0)]):.4f}")
        for size, lab in ((48, "SE_lambda: |J| = j0 = 48 (|T| = 62), normalised lambda_min(R)"),
                          (100, "SE_w: |J| = 100 (|T| = 114), unnormalised lambda_min(G) = (n-1) lambda_min(R)")):
            vals = []
            for r in range(20):
                J = list(rng.choice(others, size, replace=False)); T = S0 + J
                vals.append(lmin(R[np.ix_(T, T)]))
            cand = others  # full candidate pool
            _, g = greedy(R, S0, size, cand)
            scale = 1.0 if size == 48 else (n - 1)
            print(f"  {lab}\n    random J: min {scale*min(vals):.4f}  median {scale*np.median(vals):.4f}   "
                  f"greedy adversarial J (full pool): {scale*g:.4f}")
