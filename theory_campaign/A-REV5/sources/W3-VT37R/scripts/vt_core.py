"""W3-VT37R independent core (referee code; written from METHODOLOGY_v3 §5, §6.10 and v3_engine.h::local_search,
NOT from W1-T37R's td_core.py).

Score (M §5, 00_COMMON §1), on standardised X (||x_j||^2 = n-1) and y (||y||^2 = n-1):
  H_S = (n+1) G_S + I,  Q_S = y'y - n z_S' H_S^{-1} z_S,  nu = a0 + n/2,
  log m(S) = log C_n - 1/2 [logdet H_S - logdet(G_S + I)] - nu log(2 b0 + Q_S),
  F(S) = log w(|S|) - log W_K + log m(S),  w(k) = 1/2 / C(2p-1, k),  K = min(p, floor(n/2)).
Implemented with slogdet + solve (W1 used Cholesky); the two are cross-checked in selftest().

Local search, exactly as v3_engine.h::local_search:
  scan order: flips j = 0..p-1 (delete if j in S, add if j not in S and |S| < K), then swaps
  (j in S ascending) x (l not in S ascending); best = largest F, exact ties -> lexicographically smaller sorted
  index vector (proper prefix first); move only on strict improvement; at most ell moves; after ell moves one
  further scan: if it still improves -> local_limit (returned = that best neighbour), else local_certified.
"""
import numpy as np
from math import lgamma, log, ceil, log2

A0 = B0 = 0.01


def lch(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


def standardise(X, y):
    X = X - X.mean(0); X = X / np.sqrt((X ** 2).sum(0) / (X.shape[0] - 1))
    y = y - y.mean(); y = y / np.sqrt((y ** 2).sum() / (len(y) - 1))
    return X, y


class Model:
    def __init__(self, X, y, K=None):
        self.X, self.y = X, y
        self.n, self.p = X.shape
        n, p = self.n, self.p
        self.K = min(p, n // 2) if K is None else K
        self.G = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)
        self.nu = A0 + n / 2
        self.lCn = A0 * log(2 * B0) + lgamma(self.nu) - (n / 2) * log(np.pi) - lgamma(A0)
        lw = np.array([-log(2) - lch(2 * p - 1, k) for k in range(self.K + 1)])
        t = np.array([lch(p, k) for k in range(self.K + 1)]) + lw
        self.lWK = t.max() + log(np.exp(t - t.max()).sum())
        self.lpr = lw - self.lWK
        self.ell = ceil(log2(n + p + 1))
        self.cache = {}

    def Fmany(self, rows):
        """rows: list of sorted tuples, all of the same length k."""
        k = len(rows[0])
        if k == 0:
            return np.full(len(rows), self.lCn - self.nu * log(2 * B0 + self.yy) + self.lpr[0])
        idx = np.array(rows, dtype=int)
        G = self.G[idx[:, :, None], idx[:, None, :]]
        z = self.z[idx]
        I = np.eye(k)
        H = (self.n + 1) * G + I
        s1, ldH = np.linalg.slogdet(H)
        s2, ldA = np.linalg.slogdet(G + I)
        b = np.linalg.solve(H, z[:, :, None])[:, :, 0]
        Q = self.yy - self.n * (z * b).sum(1)
        return self.lCn - 0.5 * (ldH - ldA) - self.nu * np.log(2 * B0 + Q) + self.lpr[k]

    def F(self, S):
        S = tuple(sorted(S))
        if S not in self.cache:
            self.cache[S] = float(self.Fmany([S])[0])
        return self.cache[S]

    def Fset(self, models):
        """score a list of sorted tuples (mixed sizes), using the cache."""
        need = [m for m in models if m not in self.cache]
        by = {}
        for m in need:
            by.setdefault(len(m), []).append(m)
        for k, rows in by.items():
            for a in range(0, len(rows), 20000):
                chunk = rows[a:a + 20000]
                v = self.Fmany(chunk)
                for m, f in zip(chunk, v):
                    self.cache[m] = float(f)
        return np.array([self.cache[m] for m in models])

    # ---------------------------------------------------------------- neighbourhood in engine scan order
    def nbrs(self, S):
        S = tuple(sorted(S)); Ss = set(S)
        out = []
        for j in range(self.p):
            if j in Ss:
                out.append(tuple(x for x in S if x != j))
            elif len(S) < self.K:
                out.append(tuple(sorted(S + (j,))))
        for j in S:
            rest = tuple(x for x in S if x != j)
            for l in range(self.p):
                if l in Ss:
                    continue
                out.append(tuple(sorted(rest + (l,))))
        return out

    def scan(self, S):
        nb = self.nbrs(S)
        return nb, self.Fset(nb)

    def M(self, S):
        """greedy map: best strict improvement (engine tie rule) or None."""
        S = tuple(sorted(S))
        nb, f = self.scan(S)
        if not nb:
            return None
        mx = f.max()
        if not mx > self.F(S):
            return None
        cands = [nb[t] for t in np.nonzero(f == mx)[0]]
        return min(cands)          # python tuple order = plain lexicographic, proper prefix first

    def local_search(self, centre, ell=None):
        ell = self.ell if ell is None else ell
        C = tuple(sorted(centre)); path = [C]; moves = 0
        while True:
            B = self.M(C)
            if B is None:
                return dict(path=path, returned=C, certified=True, limit=False, moves=moves)
            if moves >= ell:
                return dict(path=path, returned=B, certified=False, limit=True, moves=moves)
            C = B; moves += 1; path.append(C)

    def greedy_uncapped(self, centre, maxit=10000):
        C = tuple(sorted(centre)); path = [C]
        for _ in range(maxit):
            B = self.M(C)
            if B is None:
                return path
            C = B; path.append(C)
        raise RuntimeError("no termination")


# ---------------------------------------------------------------- truth bookkeeping
def mis_ext(S, S0):
    S = set(S); S0 = set(S0)
    return len(S0 - S), len(S - S0)


def phi(S, S0):
    m, e = mis_ext(S, S0); return m + e


def move_class(S, T, S0):
    """class of the move S -> T: 'P' progress, 'N' neutral, 'R' regressive (by change of Phi)."""
    d = phi(T, S0) - phi(S, S0)
    return 'P' if d < 0 else ('N' if d == 0 else 'R')


def region(S0, nulls, a, d):
    """R_{a,d} = {U u P : U subset S0, |S0 - U| <= a, P subset nulls, |P| <= d}."""
    from itertools import combinations
    S0 = tuple(sorted(S0)); out = []
    for mm in range(a + 1):
        for A in combinations(S0, mm):
            U = tuple(x for x in S0 if x not in A)
            for e in range(d + 1):
                for P in combinations(nulls, e):
                    out.append(tuple(sorted(U + P)))
    return out


def selftest(seed=1):
    """cross-check the slogdet scorer against a direct dense-inverse formula."""
    rng = np.random.default_rng(seed)
    n, p = 30, 8
    X, y = standardise(rng.standard_normal((n, p)), rng.standard_normal(n))
    M = Model(X, y)
    worst = 0.0
    for S in [(), (0,), (1, 3), (0, 2, 5, 7)]:
        k = len(S)
        if k:
            XS = X[:, list(S)]; G = XS.T @ XS; z = XS.T @ y
            H = (n + 1) * G + np.eye(k)
            Q = y @ y - n * z @ np.linalg.inv(H) @ z
            ld = log(np.linalg.det(H)) - log(np.linalg.det(G + np.eye(k)))
        else:
            Q = y @ y; ld = 0.0
        F = M.lCn - 0.5 * ld - M.nu * log(2 * B0 + Q) + M.lpr[k]
        worst = max(worst, abs(F - M.F(S)))
    return worst


if __name__ == "__main__":
    print("selftest max |dF| =", selftest())
