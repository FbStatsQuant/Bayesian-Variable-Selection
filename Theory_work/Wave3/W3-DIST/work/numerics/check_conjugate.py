"""Sanity: conjugate formulas vs brute-force quadrature (tensor trapezoid on beta and log sigma^2), n=8, p=3.
Prior implied by the coded posterior: beta_S | s2 ~ N(0, n s2 (G_S+I)^-1), s2 ~ IG(0.01, 0.01)."""
import numpy as np
from scipy.special import gammaln
from common import *
rng = np.random.default_rng(1)
n, p = 8, 3
Xr = rng.standard_normal((n, p)); yr = Xr @ [1, -1, 0.3] + rng.standard_normal(n)
d = prep(Xr, yr); X, y = d.X, d.y
print("n, kept p, K:", n, d.q, d.K, "| ||x_j||^2 =", np.round((X ** 2).sum(0), 6), "| y'y =", round(d.yty, 6))
a, b, nu = A0, B0, A0 + n / 2
ls = np.linspace(-4.5, 4.5, 500); dls = ls[1] - ls[0]
for S in [(), (0,), (1,), (0, 1), (0, 2), (1, 2)]:
    k = len(S)
    idx = np.array([list(S)], dtype=np.int32) if k else -np.ones((1, 1), dtype=np.int32)
    lp, Q, sz = batched_logpi(d, idx)
    G = d.G[np.ix_(S, S)] if k else np.zeros((0, 0)); z = d.z[list(S)] if k else np.zeros(0)
    H = (n + 1) * G + np.eye(k)
    Dd = np.linalg.det(H) / np.linalg.det(G + np.eye(k))
    logm_f = -n / 2 * np.log(2 * np.pi) - 0.5 * np.log(Dd) + a * np.log(b) - gammaln(a) + gammaln(nu) - nu * np.log(b + Q[0] / 2)
    Xs = X[:, list(S)] if k else np.zeros((n, 0))
    if k:
        L = 8.0; m = 241 if k == 2 else 2001
        g = np.linspace(-L, L, m); dg = g[1] - g[0]
        grids = np.meshgrid(*([g] * k), indexing="ij")
        Bt = np.stack([t.ravel() for t in grids], 1)           # (m^k, k)
        R = y[None, :] - Bt @ Xs.T                               # residuals (m^k, n)
        rr = (R ** 2).sum(1)
        quad = np.einsum('ij,jk,ik->i', Bt, G + np.eye(k), Bt)
        w_beta = dg ** k
    tot = 0.0; Es2 = 0.0; Eb = 0.0
    for l in ls:
        s2 = np.exp(l)
        lig = a * np.log(b) - gammaln(a) - (a + 1) * np.log(s2) - b / s2 + l       # incl. Jacobian
        if k:
            ll = -n / 2 * np.log(2 * np.pi * s2) - rr / (2 * s2)
            lpri = -k / 2 * np.log(2 * np.pi) + 0.5 * (np.linalg.slogdet(G + np.eye(k))[1] - k * np.log(n * s2)) - quad / (2 * n * s2)
            f = np.exp(ll + lpri + lig) * w_beta
            val = f.sum(); eb = (f * Bt[:, 0]).sum()
        else:
            val = np.exp(-n / 2 * np.log(2 * np.pi * s2) - (y @ y) / (2 * s2) + lig); eb = 0
        tot += val * dls; Es2 += val * s2 * dls; Eb += eb * dls
    mu = n * np.linalg.solve(H, z) if k else np.zeros(1)
    msg = f"S={S}: log m(S) formula {logm_f:.5f} brute {np.log(tot):.5f} | E[s2|S] formula {(b + Q[0] / 2) / (nu - 1):.5f} brute {Es2 / tot:.5f}"
    if k: msg += f" | E[beta_1|S] formula {mu[0]:.5f} brute {Eb / tot:.5f}"
    print(msg, flush=True)
# sampler check
S = (0, 1); idx = np.array([[0, 1]], dtype=np.int32)
lp, Q, sz = batched_logpi(d, idx)
B, s2, _ = sample_posterior(d, idx, lp, Q, 400000, np.random.default_rng(3))
H = (n + 1) * d.G[np.ix_(S, S)] + np.eye(2)
print("sampler (S=(0,1)): mean beta", np.round(B[:, :2].mean(0), 4), " formula", np.round(n * np.linalg.solve(H, d.z[list(S)]), 4))
print("sampler: E s2", round(s2.mean(), 4), "formula", round((B0 + Q[0] / 2) / (nu - 1), 4))
print("sampler: Var(beta) (marginal over s2) row0", np.round(np.cov(B[:, :2].T)[0], 4), " formula  n E[s2] H^-1 + Var(mean) = n E[s2] H^-1 row0:", np.round((n * (B0 + Q[0] / 2) / (nu - 1) * np.linalg.inv(H))[0], 4))
