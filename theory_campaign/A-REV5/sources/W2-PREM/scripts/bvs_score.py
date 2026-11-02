"""Exact scores for the SMC-BVS v3 target (00_COMMON §1), from sufficient statistics (W2-PREM).

Data are generated in the *exact-Gram* realisation used by W1-EXP: X'X = (n-1) Sigma exactly (standardised
columns), X'eps ~ N(0, sigma^2 X'X), ||C eps||^2 = (X'eps)' G^{-1} (X'eps) + sigma^2 chi^2_{n-1-p}.  Then the
response is standardised (||y||^2 = n-1).  Every score is the exact v3 formula:
    log m(S) = const - (1/2) log D_S - nu log(2 b0 + Q_S),  D_S = det H_S / det(G_S + I),  H_S = (n+1) G_S + I,
    Q_S = y'y - n z_S' H_S^{-1} z_S,  nu = 0.01 + n/2,  b0 = 0.01;  prior w(k) = (1/2)/C(2p-1, k).
F(S) = log w(|S|) + log m(S) (the constant and W_K cancel in every ratio used here).
"""
import numpy as np
from math import lgamma, log

B0 = 0.01


class Data:
    def __init__(self, Sigma, theta, n, rng, sigma=1.0):
        p = Sigma.shape[0]
        assert p <= n - 2
        self.p, self.n = p, n
        self.Sigma = Sigma
        G = (n - 1) * Sigma
        L = np.linalg.cholesky(G)
        xe = sigma * (L @ rng.standard_normal(p))                     # X'eps ~ N(0, sigma^2 G)
        Ceps2 = xe @ np.linalg.solve(G, xe) + sigma ** 2 * rng.chisquare(n - 1 - p)
        XY = G @ theta + xe
        YY = theta @ G @ theta + 2 * theta @ xe + Ceps2
        sy = np.sqrt(YY / (n - 1))
        self.G, self.z, self.yy = G, XY / sy, n - 1.0
        self.nu = 0.01 + n / 2.0
        self.logw = np.array([log(0.5) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k)) for k in range(p + 1)])
        self.cache = {}
        self.theta, self.sigma = theta, sigma
        # noise-free residual signal, for population checks: RSSmu(S) = ||(I - P_S) mu||^2 = th'G th - (G th)_S' G_S^{-1} (G th)_S
        self.Gth = G @ theta
        self.mu2 = theta @ G @ theta

    def logm(self, S):
        """log m(S) up to the S-free constant; S is a sorted tuple of column indices."""
        if S in self.cache:
            return self.cache[S]
        n = self.n
        if len(S) == 0:
            v = -self.nu * np.log(2 * B0 + self.yy)
        else:
            idx = list(S)
            GS = self.G[np.ix_(idx, idx)]
            H = (n + 1) * GS + np.eye(len(idx))
            cH = np.linalg.cholesky(H)
            cG = np.linalg.cholesky(GS + np.eye(len(idx)))
            logD = 2 * np.sum(np.log(np.diag(cH))) - 2 * np.sum(np.log(np.diag(cG)))
            w = np.linalg.solve(cH, self.z[idx])
            Q = self.yy - n * (w @ w)
            v = -0.5 * logD - self.nu * np.log(2 * B0 + Q)
        self.cache[S] = v
        return v

    def F(self, S):
        return self.logw[len(S)] + self.logm(S)

    def logBF(self, S):
        return self.logm(S) - self.logm(())

    def rss_mu(self, S):
        """Noise-free residual signal ||(I-P_S) mu||^2 (exact Gram)."""
        if len(S) == 0:
            return self.mu2
        idx = list(S)
        g = self.Gth[idx]
        return self.mu2 - g @ np.linalg.solve(self.G[np.ix_(idx, idx)], g)


def tup(s):
    return tuple(sorted(s))


def plogis(x):
    return 1.0 / (1.0 + np.exp(-x)) if x > -700 else 0.0
