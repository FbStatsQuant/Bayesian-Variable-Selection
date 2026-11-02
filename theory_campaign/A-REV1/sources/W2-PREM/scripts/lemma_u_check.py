"""Lemma U check (W2-PREM PROOF.md §2): uniform log-BF expansion over ALL additions with |T+l| <= k.

    log BF(T+l)/BF(T) = -(1/2) log(n+1) - nu log(1 - x_{T,l}) + R_{T,l},   |R| <= kappa  on E_n.

Design: exact Gram, p = 24, AR(1) correlation 0.5 (so phi0^2 >= lambda_min(Sigma)), s0 = 3 truths with
theta = (1.0, -0.8, 0.6) at columns 2, 9, 17; sigma = 1; k = 4 (all 51,152 pairs (T, l)).
Reports max |R| and the deterministic bound kappa of Lemma U (EXP' constant with M = ||mu||^2/n + 1).
Fixed seed.  Output: results/lemma_u_check.txt
"""
import numpy as np
from itertools import combinations
from bvs_score import Data

SEED = 7
p, k = 24, 4
rho = 0.5
Sigma = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
theta = np.zeros(p)
theta[[2, 9, 17]] = [1.0, -0.8, 0.6]
phi02 = np.linalg.eigvalsh(Sigma).min()
sig2 = 1.0
M = theta @ Sigma @ theta + 1.0          # ||mu||^2/n <= theta' Sigma theta < M
cstar = sig2 / (8 * (M + 2 * sig2))


def rssy(D, S):
    if not S:
        return D.yy
    idx = list(S)
    zS = D.z[idx]
    return D.yy - zS @ np.linalg.solve(D.G[np.ix_(idx, idx)], zS)


lines = [f"p={p}, k={k}, AR(0.5): phi0^2 >= {phi02:.3f}; M = {M:.3f}; c_* = {cstar:.4f}"]
lines.append("n | max|R| over all (T,l), |T+l|<=k | mean|R| | kappa bound")
for n in [200, 1000, 5000, 25000, 125000]:
    rng = np.random.default_rng(SEED + n)
    D = Data(Sigma, theta, n, rng)
    nu = D.nu
    kappa = (1 + 1 / phi02) / (2 * phi02 * (n - 1)) + nu * (1.02 + 1 / (n * phi02)) / (cstar * n)
    rs = {}
    Rmax, Rsum, cnt = 0.0, 0.0, 0
    for j in range(k):
        for T in combinations(range(p), j):
            rT = rs.setdefault(T, rssy(D, T))
            bT = D.logBF(T)
            for l in range(p):
                if l in T:
                    continue
                Tl = tuple(sorted(T + (l,)))
                rTl = rs.setdefault(Tl, rssy(D, Tl))
                x = (rT - rTl) / rT
                R = D.logBF(Tl) - bT + 0.5 * np.log(n + 1) + nu * np.log(1 - x)
                Rmax = max(Rmax, abs(R))
                Rsum += abs(R)
                cnt += 1
    lines.append(f"{n} | {Rmax:.3f} | {Rsum / cnt:.3f} | {kappa:.2f}   ({cnt} pairs)")
    print(lines[-1], flush=True)
txt = "\n".join(lines)
with open(__file__.replace("scripts/lemma_u_check.py", "results/lemma_u_check.txt"), "w") as f:
    f.write(txt + "\n")
print(txt)
