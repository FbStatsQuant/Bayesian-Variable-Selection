"""W3-SCR numerics library: independent implementation of the SMC-BVS v3.1 score F and of the coded local-search
neighbourhood (flips + swaps), with vectorised exact neighbour scores.

Score (Wave1C/FINAL/sections/s1_setting.tex:9-13; code Scripts/SMC_BVS/core/cpp/v3_score.h:57-70,223):
  X standardised (columns centred, ||x_j||^2 = n-1), y standardised (y'y = n-1), K = min(p, floor(n/2)),
  G_U = X_U'X_U, z_U = X_U'y, H_U = (n+1) G_U + I, Q_U = y'y - n z_U' H_U^{-1} z_U, nu = 0.01 + n/2,
  log m(U) = log C_n - (1/2)[log det H_U - log det(G_U + I)] - nu log(0.02 + Q_U),
  log w(k) = -log 2 - log C(2p-1, k),  W_K = sum_{k<=K} C(p,k) w(k),  F(U) = log w(|U|) - log W_K + log m(U).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


def standardise(v):
    v = np.asarray(v, float)
    v = v - v.mean(axis=0)
    return v / np.sqrt((v ** 2).sum(axis=0) / (v.shape[0] - 1))


class Score:
    def __init__(self, X, y, standardised=False):
        if not standardised:
            X = standardise(X); y = standardise(y)
        self.X = X; self.y = y
        self.n, self.p = X.shape
        n, p = self.n, self.p
        self.K = min(p, n // 2)
        self.G = X.T @ X
        self.z = X.T @ y
        self.yty = float(y @ y)
        self.nu = 0.01 + n / 2.0
        self.lam0 = 1.0 / (n + 1.0)
        self.logCn = 0.01 * math.log(0.02) + gammaln(0.01 + n / 2.0) - (n / 2.0) * math.log(math.pi) - gammaln(0.01)
        k = np.arange(0, self.K + 1)
        self.logw = -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
        # prior normaliser as in the core (v3_score.h:60-70): W_K = sum_k C(p,k) w(k)
        self.logWK = logsumexp(self.logw + gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1))

    # ---- direct evaluation (reference) -------------------------------------------------------------------------
    def parts(self, S):
        S = list(S); k = len(S); n = self.n
        if k == 0:
            return 0.0, 0.0, self.yty
        G = self.G[np.ix_(S, S)]; z = self.z[S]
        H = (n + 1.0) * G + np.eye(k)
        ldH = np.linalg.slogdet(H)[1]; ldA = np.linalg.slogdet(G + np.eye(k))[1]
        Q = self.yty - n * float(z @ np.linalg.solve(H, z))
        return ldH, ldA, Q

    def F(self, S):
        ldH, ldA, Q = self.parts(S)
        return self.logw[len(S)] - self.logWK + self.logCn - 0.5 * (ldH - ldA) - self.nu * math.log(0.02 + Q)

    # ---- vectorised one-column additions to a base set B --------------------------------------------------------
    def add_all(self, B):
        """F(B + l) for every l (entries for l in B are -inf). Uses the Schur complements
        a_lam(l|B) = G_ll + lam - G_lB (G_BB + lam I)^{-1} G_Bl for lam in {1/(n+1), 1} and the ridge gain."""
        B = list(B); n, p = self.n, self.p; lam0 = self.lam0
        ldH, ldA, Q = self.parts(B)
        d = np.diag(self.G).copy()
        if len(B) == 0:
            a0 = d + lam0; a1 = d + 1.0; r = self.z.copy()
        else:
            GB = self.G[np.ix_(B, B)]; GBX = self.G[B, :]
            M0 = np.linalg.solve(GB + lam0 * np.eye(len(B)), np.column_stack([GBX, self.z[B]]))
            a0 = d + lam0 - np.einsum('ij,ij->j', GBX, M0[:, :p])
            r = self.z - GBX.T @ M0[:, p]
            M1 = np.linalg.solve(GB + np.eye(len(B)), GBX)
            a1 = d + 1.0 - np.einsum('ij,ij->j', GBX, M1)
        gain = r ** 2 / a0                                   # ridge gain g_{lam0}(l | B)
        Qn = Q - (n / (n + 1.0)) * gain
        kb = len(B)
        out = np.full(p, -np.inf)
        if kb + 1 <= self.K:
            ok = np.ones(p, bool); ok[B] = False
            ok &= (0.02 + Qn) > 0
            val = (self.logw[kb + 1] - self.logWK + self.logCn
                   - 0.5 * (ldH + np.log((n + 1.0) * a0[ok]) - ldA - np.log(a1[ok])) - self.nu * np.log(0.02 + Qn[ok]))
            out[ok] = val
        return out, dict(a0=a0, a1=a1, gain=gain, Q=Q)

    # ---- the coded neighbourhood ---------------------------------------------------------------------------------
    def scan(self, C):
        """Complete scan of the coded neighbourhood of C (v3_engine.h:394-406): flips j = 1..p (additions excluded
        when |C| >= K), then swaps. Returns (best_F, best_model, FC, n_scanned); ties broken by lex order."""
        C = sorted(C); FC = self.F(C); best = (-np.inf, None); cnt = 0
        def offer(val, S):
            nonlocal best
            if val > best[0] or (val == best[0] and best[1] is not None and S < best[1]):
                best = (val, S)
        if len(C) < self.K:
            fa, _ = self.add_all(C)
            for l in np.argsort(-fa)[:3]:
                if np.isfinite(fa[l]): offer(float(fa[l]), sorted(C + [int(l)]))
            cnt += self.p - len(C)
        for j in C:
            Bm = [c for c in C if c != j]
            offer(self.F(Bm), Bm); cnt += 1
            fs, _ = self.add_all(Bm)
            fs[j] = -np.inf
            for l in np.argsort(-fs)[:3]:
                if np.isfinite(fs[l]): offer(float(fs[l]), sorted(Bm + [int(l)]))
            cnt += self.p - len(C)
        return best[0], best[1], FC, cnt

    def local_search(self, centre, ell=10 ** 9, tol=0.0):
        """The coded local search (strict improvement; at most ell moves then one further scan)."""
        C = sorted(centre); moves = 0; path = [list(C)]
        while True:
            bF, bS, FC, _ = self.scan(C)
            if bS is not None and bF > FC + tol:
                if moves >= ell:
                    return dict(returned=bS, certified=False, limit=True, moves=moves, path=path)
                C = bS; moves += 1; path.append(list(C))
            else:
                return dict(returned=C, certified=True, limit=False, moves=moves, path=path, F=FC)

    def is_certified(self, C, tol=0.0):
        bF, bS, FC, _ = self.scan(C)
        return not (bS is not None and bF > FC + tol)


def make_design(kind, n, p, rng, rho=0.5, k=3, S0=None):
    if kind == "iid":
        return rng.standard_normal((n, p))
    if kind == "ar":
        E = rng.standard_normal((n, p)); Z = E.copy()
        for j in range(1, p):
            Z[:, j] = rho * Z[:, j - 1] + math.sqrt(1 - rho ** 2) * E[:, j]
        return Z
    if kind == "cs":
        f = rng.standard_normal((n, 1))
        return math.sqrt(rho) * f + math.sqrt(1 - rho) * rng.standard_normal((n, p))
    if kind == "fac":
        L = rng.uniform(0.2, 0.9, (p, k)) / math.sqrt(k); Fm = rng.standard_normal((n, k))
        return Fm @ L.T + rng.standard_normal((n, p)) * np.sqrt(1 - (L ** 2).sum(axis=1))
    raise ValueError(kind)
