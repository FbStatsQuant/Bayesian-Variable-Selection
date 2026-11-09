"""fac_exact.py -- exact-Gram simulator: X'X = (n-1) Sigma exactly, so every score depends on (Sigma, z = X'y, y'y).
Joint law (fixed X with orthonormal basis U of span X, U'1 = 0):  g := U'eps/sigma ~ N(0, I_p),
  X'Y = (n-1) Sigma theta + sigma sqrt(n-1) Sigma^{1/2} g,
  |Y|^2 = (n-1) theta'Sigma theta + 2 sigma sqrt(n-1) theta'Sigma^{1/2} g + sigma^2 (|g|^2 + chi2_{n-1-p}),
  y = Y sqrt(n-1)/|Y|  (centred/scaled response), z = X'y.
This reproduces the joint law of (X'y, y'y) of fac_common.build(mode='exact') without forming X (checked in selftest).
Provides ExactProb (bvs_core.Problem interface: XtX, Xty, yty, logm_idx, F...) and ExactFast (fac_common.Fast)."""
import math
import numpy as np
import bvs_core as bc
import fac_common as fc


def sym_sqrt(S):
    w, V = np.linalg.eigh(S)
    return (V * np.sqrt(np.maximum(w, 0))) @ V.T


def draw_z(Sigma, theta, n, sigma, rng, Sroot=None):
    p = Sigma.shape[0]
    if Sroot is None:
        Sroot = sym_sqrt(Sigma)
    g = rng.standard_normal(p)
    chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
    St = Sigma @ theta
    XtY = (n - 1) * St + sigma * math.sqrt(n - 1) * (Sroot @ g)
    Y2 = (n - 1) * float(theta @ St) + 2 * sigma * math.sqrt(n - 1) * float(theta @ (Sroot @ g)) + sigma ** 2 * (float(g @ g) + chi)
    z = XtY * math.sqrt(n - 1) / math.sqrt(Y2)
    return z, g


class ExactProb(bc.Problem):
    def __init__(self, Sigma, z, n, K=None):
        self.n, self.p = n, Sigma.shape[0]
        self.K = min(self.p, n // 2) if K is None else K
        self.XtX = (n - 1.0) * Sigma
        self.Xty = np.asarray(z, float)
        self.yty = float(n - 1)
        self.nu = 0.01 + n / 2.0
        self.logw = bc.log_prior_w(self.p, self.K)
        self.logm0 = -self.nu * math.log(0.02 + self.yty)
        self.cache = {(): self.logm0}


class ExactFast(fc.Fast):
    def __init__(self, Sigma, z, n, K=None):
        self.n, self.p = n, Sigma.shape[0]
        self.K = min(self.p, n // 2) if K is None else K
        self.XtX = (n - 1.0) * Sigma
        self.Xty = np.asarray(z, float)
        self.yty = float(n - 1)
        self.nu = 0.01 + n / 2.0
        self.logw = bc.log_prior_w(self.p, self.K)
        self.diag = np.diag(self.XtX).copy()


def partition_exact(Sigma, n):
    p = Sigma.shape[0]
    return bc.partition_from_corr(Sigma, bc.block_size(n, p))


def selftest():
    # compare with explicit X construction: same Sigma, z distribution moments are hard to compare; instead check
    # that for a given X (exact Gram) the scores computed from (X'X, X'y, y'y) agree with ExactFast.
    rng = np.random.default_rng(3)
    p, n = 20, 80
    Sigma = fc.sigma_of("CS3", p)
    X = bc.exact_gram_design(Sigma, n, rng)
    th = np.zeros(p); th[[1, 5]] = [1.0, -0.7]
    y = bc.make_y_std(X, th, 1.0, rng)
    f1 = fc.Fast(X, y)
    f2 = ExactFast(Sigma, X.T @ y, n)
    err = 0
    for T in [(), (1,), (1, 5, 7), tuple(range(10))]:
        a, ra = f1.scan(T)
        b, rb = f2.scan(T)
        err = max(err, abs(a - b), np.abs(ra["dele"] - rb["dele"]).max() if len(T) else 0)
    # law check: E[z_null] vs simulation with X (Monte Carlo, coarse)
    zs1, zs2 = [], []
    for s in range(400):
        r = np.random.default_rng(100 + s)
        y = bc.make_y_std(X, th, 1.0, r)
        zs1.append((X.T @ y)[[0, 1, 5]])
        z, _ = draw_z(Sigma, th, n, 1.0, r)
        zs2.append(z[[0, 1, 5]])
    zs1, zs2 = np.array(zs1), np.array(zs2)
    return err, zs1.mean(0), zs2.mean(0), zs1.std(0), zs2.std(0)


if __name__ == "__main__":
    print(selftest())
