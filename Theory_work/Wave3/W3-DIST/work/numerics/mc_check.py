"""Check Monte-Carlo (20000 fresh rows, float32) joint Hellinger against the closed form for Gaussian design AR(0.5)."""
import numpy as np
from common import *
for n in (100, 800):
    rng = np.random.default_rng(5 + n); p = 12
    bstar = beta_star("sparse", n, p)
    Xr = gen_design("ar", n, p, rng); yr = Xr @ bstar + rng.standard_normal(n)
    d = prep(Xr, yr); d.Xraw = Xr
    idx, lp, Q, sz = exact_family(d)
    B, s2, _ = sample_posterior(d, idx, lp, Q, 2000, rng)
    Xf = gen_design("ar", 20000, p, np.random.default_rng(99))
    r = distances(d, B, s2, bstar, Xf, 2000)
    v = r["v"]; w = 1.0
    braw = np.zeros((2000, p)); braw[:, d.keep] = d.sy * B / d.sd
    a = d.ybar - braw @ d.xbar0                       # x population mean 0 -> Delta ~ N(a, delta' Sigma delta)
    a = a + 0.0
    delta = braw - bstar[None, :]
    S = AR_SIGMA(p)
    s2x = np.einsum('ij,jk,ik->i', delta, S, delta)
    tau2 = 2 * (v + w)
    Eexp = np.sqrt(tau2 / (tau2 + s2x)) * np.exp(-a ** 2 / (2 * (tau2 + s2x)))
    c = np.sqrt(2 * np.sqrt(v * w) / (v + w))
    d2c = 1 - c * Eexp
    print(f"n={n}: MC d2 median {np.median(r['d2']):.3e}, closed-form median {np.median(d2c):.3e}; max |MC-exact| {np.abs(r['d2']-d2c).max():.2e}; "
          f"max relative err (d2>1e-4) {np.max(np.abs(r['d2']-d2c)/np.maximum(d2c,1e-4)):.3f}; mean n*d2 MC {n*r['d2'].mean():.4f} exact {n*d2c.mean():.4f}")
