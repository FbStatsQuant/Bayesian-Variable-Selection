"""W3-PSHARP numerics (a), boundary of the witness condition: an EQUICORRELATED null block.

Raw columns x^r_j = sqrt(rho) f + sqrt(1-rho) z_j (one common factor f ~ N(0, I_n), z_j iid N(0, I_n)), all p columns;
S0 = first s0 columns, beta = 1, sigma = 1. Every population eigenvalue floor of Theorem 1 holds (lambda_min = 1 - rho),
but the null scores share a common component, so (W-sph) fails: the directions are not independent of each other
given eps. Heuristic: (1/N) sum_j e^{chi2_j/2} -> E[e^{g^2/2} | common part] = O_P(1), so the one-step odds are
O_P(n^{-1/2}) with NO sqrt(log p) factor (in probability; the truncated mean is unchanged, the sum does not
concentrate). Reported: the exact one-step odds L1 (Lemma S closed form; a lower bound for delta/(1-delta)) divided
by Lambda_n and by (s0+1)/(2 sqrt n).
Run: py -3.13 -I a_boundary.py > a_boundary_out.txt
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script directory
sys.dont_write_bytecode = True
import numpy as np
from core import B0, standardise, Lambda
from a_sph import ratios


def L1_equi(n, p, s0, rho, rng, chunk=20000):
    f = rng.standard_normal(n)
    X0r = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, s0))
    yr = X0r.sum(1) + rng.standard_normal(n)
    X0, y = standardise(X0r, yr)
    G = X0.T @ X0; H = (n + 1) * G + np.eye(s0); z0 = X0.T @ y
    Q = float(y @ y - n * z0 @ np.linalg.solve(H, z0)); rho_t = y - (n + 1) * X0 @ np.linalg.solve(H, z0)
    tot, left = 0.0, p - s0
    while left > 0:
        m = min(chunk, left); left -= m
        Z = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, m))
        Z -= Z.mean(0); Z *= math.sqrt(n - 1) / np.sqrt((Z ** 2).sum(0))
        tot += float(ratios(n, p, s0, G, H, Q, (X0.T @ Z).T, rho_t @ Z).sum())
    return tot


if __name__ == "__main__":
    rng = np.random.default_rng(20261115)
    print("columns: rho n p s0 | Lambda_n | median, quartiles of L1/Lambda_n | median of L1/[(s0+1)/(2 sqrt n)] | sqrt(log N/pi)*2")
    for rho in (0.0, 0.5):
        for (n, p) in ((100, 1000), (400, 8000), (1600, 64000)):
            s0 = 1
            reps = 100 if n * p <= 4e6 else 30
            v = np.array([L1_equi(n, p, s0, rho, rng) for _ in range(reps)])
            lam = Lambda(n, p, s0, p - s0); base = (s0 + 1) / (2 * math.sqrt(n))
            q = np.quantile(v / lam, [0.25, 0.5, 0.75])
            print(f"  rho={rho} n={n:5d} p={p:6d} s0={s0} reps={reps} | Lam={lam:.4f} | {q[1]:.3f} [{q[0]:.3f}, {q[2]:.3f}] |"
                  f" {np.median(v) / base:.3f} | {2 * math.sqrt(math.log(p - s0) / math.pi):.3f}", flush=True)
