"""Independent minimal implementation of the SMC-BVS v3 target (00_COMMON.md, Section 1).

Written for W6-FIXREV1; it does not import code from any other campaign run.
All quantities follow 00_COMMON.md:
  G_S = X_S'X_S, z_S = X_S'y, H_S = (n+1)G_S + I, D_S = det H_S / det(G_S + I),
  Q_S = y'y - n z_S' H_S^{-1} z_S, nu = 0.01 + n/2, a0 = b0 = 0.01,
  log m(S) = const - 0.5 log D_S - nu log(2 b0 + Q_S),
  w(k) = 0.5 / C(2p-1, k), K = min(p, floor(n/2)),
  BF(S) = m(S)/m(empty), gamma_1(S) = w(|S|) BF(S),
  start law gamma_0(S) = w(|S|) prod_b r_b(S cap C_b), r_b(U) = BF(U),
  discrepancy d(S) = log BF(S) - sum_b log r_b(S cap C_b).
"""
import itertools
import math

import numpy as np

A0 = B0 = 0.01


def standardise(X, y):
    """Centre columns and scale so that ||x_j||^2 = ||y||^2 = n - 1 (the method's preprocessing)."""
    n = X.shape[0]
    Xc = X - X.mean(axis=0)
    Xc = Xc / np.sqrt((Xc ** 2).sum(axis=0) / (n - 1))
    yc = y - y.mean()
    yc = yc / np.sqrt((yc ** 2).sum() / (n - 1))
    return Xc, yc


class Target:
    def __init__(self, X, y, blocks=None):
        self.X = np.asarray(X, float)
        self.y = np.asarray(y, float)
        self.n, self.p = self.X.shape
        self.K = min(self.p, self.n // 2)
        self.nu = A0 + self.n / 2.0
        self.Gram = self.X.T @ self.X
        self.zall = self.X.T @ self.y
        self.yy = float(self.y @ self.y)
        self._cache = {}
        self.blocks = blocks if blocks is not None else [[j] for j in range(self.p)]
        self.block_of = {}
        for b, C in enumerate(self.blocks):
            for j in C:
                self.block_of[j] = b
        self.logm_empty = self._logm(())

    # ---- scores ----
    def _logm(self, S):
        S = tuple(sorted(S))
        if S in self._cache:
            return self._cache[S]
        n = self.n
        if len(S) == 0:
            Q = self.yy
            logD = 0.0
        else:
            idx = list(S)
            G = self.Gram[np.ix_(idx, idx)]
            z = self.zall[idx]
            k = len(idx)
            H = (n + 1) * G + np.eye(k)
            sH, ldH = np.linalg.slogdet(H)
            sG, ldG = np.linalg.slogdet(G + np.eye(k))
            logD = ldH - ldG
            Q = self.yy - n * float(z @ np.linalg.solve(H, z))
        val = -0.5 * logD - self.nu * math.log(2 * B0 + Q)
        self._cache[S] = val
        return val

    def logBF(self, S):
        return self._logm(S) - self.logm_empty

    def logw(self, k):
        p = self.p
        return math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))

    def logg1(self, S):
        """log gamma_1(S) = log w(|S|) + log BF(S) (unnormalised posterior); -inf if infeasible."""
        if len(S) > self.K:
            return -math.inf
        return self.logw(len(S)) + self.logBF(S)

    def logg0(self, S):
        if len(S) > self.K:
            return -math.inf
        tot = self.logw(len(S))
        parts = {}
        for j in S:
            parts.setdefault(self.block_of[j], []).append(j)
        for b, U in parts.items():
            tot += self.logBF(tuple(U))
        return tot

    def d(self, S):
        tot = self.logBF(S)
        parts = {}
        for j in S:
            parts.setdefault(self.block_of[j], []).append(j)
        for b, U in parts.items():
            tot -= self.logBF(tuple(U))
        return tot

    def gibbs_o(self, W, j):
        """Heat-bath inclusion probability of coordinate j at state W, phi = 1 (0 if addition infeasible)."""
        Wp = tuple(sorted(set(W) | {j}))
        Wm = tuple(sorted(set(W) - {j}))
        if len(Wp) > self.K:
            return 0.0
        a = self.logg1(Wp) - self.logg1(Wm)
        if a > 0:
            return 1.0 / (1.0 + math.exp(-a))
        return math.exp(a) / (1.0 + math.exp(a))


def all_models(p, K):
    for k in range(K + 1):
        for S in itertools.combinations(range(p), k):
            yield S


def exact_gram_design(n, Sigma, rng):
    """Centred columns with X'X = (n-1) Sigma exactly (requires p <= n-1)."""
    p = Sigma.shape[0]
    Z = rng.standard_normal((n, p))
    Z -= Z.mean(axis=0)
    Qm, _ = np.linalg.qr(Z)  # orthonormal columns, orthogonal to 1 (Z centred)
    L = np.linalg.cholesky(Sigma)
    return math.sqrt(n - 1) * Qm @ L.T
