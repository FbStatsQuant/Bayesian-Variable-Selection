"""Sanity checks for Lemma H (H.md). DRAFT helper, stream B. Run: python3 check_H.py > check_H_out.txt"""
import numpy as np
from scipy import integrate

rng = np.random.default_rng(1)

def affinity_closed(m1, s1, m2, s2):
    A = np.sqrt(2 * np.sqrt(s1 * s2) / (s1 + s2))
    B = np.exp(-(m1 - m2) ** 2 / (4 * (s1 + s2)))
    return A * B

def affinity_quad(m1, s1, m2, s2):
    f = lambda y: np.sqrt(np.exp(-(y - m1) ** 2 / (2 * s1)) / np.sqrt(2 * np.pi * s1)
                          * np.exp(-(y - m2) ** 2 / (2 * s2)) / np.sqrt(2 * np.pi * s2))
    return integrate.quad(f, -np.inf, np.inf, epsabs=1e-13, epsrel=1e-12)[0]

# 1. closed-form affinity vs quadrature
err = 0.0
for _ in range(200):
    m1, m2 = rng.normal(0, 3, 2)
    s1, s2 = np.exp(rng.normal(0, 1.5, 2))
    err = max(err, abs(affinity_closed(m1, s1, m2, s2) - affinity_quad(m1, s1, m2, s2)))
print(f"[1] max |closed-form affinity - quadrature| over 200 cases: {err:.2e}")

# 2. pointwise inequality H^2 <= (r-1)^2 + min(1, D^2/(4 w)) on a grid (w = sigma*^2 = 1 wlog by scaling? no: check general w)
worst = -np.inf
for w in [0.1, 1.0, 7.0]:
    for r in np.exp(np.linspace(-6, 6, 241)):
        v = r * w
        for D in np.concatenate([[0.0], np.exp(np.linspace(-8, 4, 121))]):
            H2 = 1 - affinity_closed(D, v, 0.0, w)
            bound = (r - 1) ** 2 + min(1.0, D ** 2 / (4 * w))
            worst = max(worst, H2 - bound)
print(f"[2] max (H^2 - bound) on grid (r in [e^-6,e^6], Delta in [0,e^4], w in {{0.1,1,7}}): {worst:.3e}  (must be <= 0)")

# 3. in-sample identity with a dropped true column
n, P = 30, 6
Xr = rng.normal(size=(n, P))
Xr[:, 2] = 3.7                       # true column constant in the sample -> dropped
beta = np.array([1.0, 0.0, -2.0, 0.5, 0.0, 0.0])
alpha = 0.3
eps = rng.normal(size=n) * 1.3
y = alpha + Xr @ beta + eps
C = np.eye(n) - np.ones((n, n)) / n
ret = [j for j in range(P) if np.linalg.norm(C @ Xr[:, j]) > 1e-12]
sh = {j: np.linalg.norm(C @ Xr[:, j]) / np.sqrt(n - 1) for j in ret}
X = np.column_stack([C @ Xr[:, j] / sh[j] for j in ret])
S = [0, 3, 4]                        # a model over retained columns (raw indices)
theta = rng.normal(size=len(S))
b = np.zeros(P)
for k, j in enumerate(S):
    b[j] = theta[k] / sh[j]
xbar = Xr.mean(0)
ahat = y.mean() - xbar @ b
Delta = ahat + Xr @ b - (alpha + Xr @ beta)
mu = C @ Xr @ beta
muhat = X[:, [ret.index(j) for j in S]] @ theta
lhs = np.mean(Delta ** 2)
rhs = eps.mean() ** 2 + np.sum((muhat - mu) ** 2) / n
print(f"[3] dropped true column present: {2 not in ret}; n^-1 sum Delta_i^2 = {lhs:.12f}; eps_bar^2 + |muhat-mu|^2/n = {rhs:.12f}; diff {abs(lhs-rhs):.1e}")
print(f"    max |Delta - (eps_bar 1 + muhat - mu)| = {np.max(np.abs(Delta - (eps.mean() + muhat - mu))):.1e}")
# population Delta(x) at a new x depends on x_2 (dropped column) — out-of-sample it is not absorbed:
print(f"    coefficient of x_2 in Delta(x): b_2 - beta_2 = {b[2]-beta[2]:.3f} (nonzero: the dropped column matters out of sample)")
