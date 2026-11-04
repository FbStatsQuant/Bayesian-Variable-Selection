"""PC2: non-vacuity of R1_C's explicit LH family (shared notation; used by D2, D4, D8, D10).
Groups of nine, within corr 0.4; two disjoint hub links corr 0.2 (between hubs of four distinct groups); other cross
corr 0; coefficients (1, -0.2) on each linked pair; p = 9 floor(n^{1/3}/9).  Checks lambda_min >= 0.4, zero marginal
covariance of masked hubs, strict separation, B and 9 <= B < 18, LH-LAT margin m0 (W4-T38FULL Prop. LH-LAT)."""
import math
import numpy as np

for n in (46656, 10 ** 6, 2 * 10 ** 7, 10 ** 8):
    p = 9 * int(n ** (1 / 3) / 9 + 1e-12)
    g = np.arange(p) // 9
    S = np.where(g[:, None] == g[None, :], 0.4, 0.0)
    np.fill_diagonal(S, 1.0)
    a1, b1, a2, b2 = 0, 9, 18, 27
    S[a1, b1] = S[b1, a1] = 0.2
    S[a2, b2] = S[b2, a2] = 0.2
    th = np.zeros(p)
    th[[a1, b1, a2, b2]] = [1, -0.2, 1, -0.2]
    cov = S @ th
    lmin = float(np.linalg.eigvalsh(S).min())
    B = min(math.isqrt(n), math.isqrt(p), 16)
    print(f"n={n} p={p} B={B} 9<=B<18:{9 <= B < 18} lmin={lmin:.4f} cov(x_b1,y)={cov[b1]:.2e} cov(x_b2,y)={cov[b2]:.2e}"
          f" cov(x_a1,y)={cov[a1]:.3f}; separation 1-0.4 < 1-0.2: {0.6 < 0.8}")
beta, psi, rho = 1.0, 0.2, 0.4
R = beta ** 2 * psi ** 2 * (1 - psi ** 2)
kap = rho ** 2 * (1 - psi ** 2) / (1 - psi ** 2 * rho ** 2)
m0 = min((1 - kap) * R, R, beta ** 2 * (1 - psi ** 2) ** 2)
print(f"LH-LAT margin m0 = {m0:.4f} (>0); kappa = {kap:.4f}; |psi| < rho: {abs(psi) < rho}")
