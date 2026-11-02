"""W6-FIXREV2 independent core: exact BVS score, greedy map M, production local search, D_S variants.

Written from 00_COMMON.md §1 and v3_engine.h::local_search (read 2026-11-02); not copied from any earlier run.

Score on standardised data (||x_j||^2 = ||y||^2 = n-1):
  G_S = X_S'X_S, z_S = X_S'y, H_S = (n+1)G_S + I, D_S = det H_S / det(G_S + I),
  Q_S = y'y - n z_S' H_S^{-1} z_S, nu = 0.01 + n/2,
  F(S) = log w(|S|) - 1/2 log D_S - nu log(0.02 + Q_S)    (constants common to all S dropped),
  w(k) = 1/(2 C(2p-1, k)),  K = min(p, floor(n/2)).
Everything is computed from the sufficient statistics (G, z, y'y, n), so huge-n examples need no n-vectors.

Local search (engine): scan all feasible flips (additions only if |S| < K) and all swaps (j in S) x (l not in S);
best neighbour = max F, exact F ties -> lex_less on sorted index vectors (proper prefix first, Python tuple order);
move only if best.F > F(centre) strictly; at most ell moves; after ell moves one further scan: if it still improves,
local_limit and returned = that best neighbour (scanned, not certified); else local_certified at the centre.
"""
import itertools
from math import lgamma, log
import numpy as np

A0 = B0 = 0.01


def lchoose(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


class BVS:
    def __init__(self, G, z, yy, n, K=None):
        self.G = np.asarray(G, float)
        self.z = np.asarray(z, float)
        self.yy = float(yy)
        self.n = int(n)
        self.p = self.G.shape[0]
        self.K = min(self.p, self.n // 2) if K is None else K
        self.nu = A0 + self.n / 2
        self.lw = [-log(2.0) - lchoose(2 * self.p - 1, k) for k in range(self.K + 1)]
        self._c = {}

    @classmethod
    def from_data(cls, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float)
        n = X.shape[0]
        X = X - X.mean(0); X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
        y = y - y.mean(); y = y / np.sqrt((y ** 2).sum() / (n - 1))
        return cls(X.T @ X, X.T @ y, y @ y, n)

    def logD(self, S):
        if not S:
            return 0.0
        idx = list(S)
        Gs = self.G[np.ix_(idx, idx)]
        k = len(idx)
        _, a = np.linalg.slogdet((self.n + 1) * Gs + np.eye(k))
        _, b = np.linalg.slogdet(Gs + np.eye(k))
        return a - b

    def Q(self, S):
        if not S:
            return self.yy
        idx = list(S)
        Gs = self.G[np.ix_(idx, idx)]
        zs = self.z[idx]
        H = (self.n + 1) * Gs + np.eye(len(idx))
        L = np.linalg.cholesky(H)
        v = np.linalg.solve(L, zs)
        return self.yy - self.n * float(v @ v)

    def logBF(self, S):
        """log m(S)/m(empty)."""
        S = tuple(sorted(S))
        return -0.5 * self.logD(S) - self.nu * (log(2 * B0 + self.Q(S)) - log(2 * B0 + self.yy))

    def F(self, S):
        S = tuple(sorted(S))
        if S not in self._c:
            self._c[S] = self.lw[len(S)] - 0.5 * self.logD(S) - self.nu * log(2 * B0 + self.Q(S))
        return self._c[S]

    # ---------------- neighbourhoods -----------------
    def neighbours(self, S):
        """Feasible flips then swaps, as sorted tuples, in engine scan order."""
        S = tuple(sorted(S)); Sset = set(S); out = []
        for j in range(self.p):
            if j in Sset:
                out.append(tuple(x for x in S if x != j))
            elif len(S) < self.K:
                out.append(tuple(sorted(S + (j,))))
        for j in S:
            for l in range(self.p):
                if l in Sset:
                    continue
                out.append(tuple(sorted([x for x in S if x != j] + [l])))
        return out

    def best_neighbour(self, S):
        """Engine rule: max F, exact ties -> lexicographically smallest sorted tuple."""
        best = None; bF = None
        for T in self.neighbours(S):
            f = self.F(T)
            if best is None or f > bF or (f == bF and T < best):
                best, bF = T, f
        return best, bF

    def M(self, S):
        """Greedy map: best neighbour if strictly improving, else None (bottom)."""
        T, f = self.best_neighbour(S)
        if T is not None and f > self.F(S):
            return T
        return None

    def local_search(self, centre, ell):
        C = tuple(sorted(centre)); scanned = [C]; moves = 0; path = [C]
        while True:
            nb = self.neighbours(C); scanned.extend(nb)
            T, f = self.best_neighbour(C)
            if T is not None and f > self.F(C):
                if moves >= ell:
                    return dict(returned=T, certified=False, limit=True, moves=moves, path=path, scanned=scanned)
                C = T; moves += 1; path.append(C)
            else:
                return dict(returned=C, certified=True, limit=False, moves=moves, path=path, scanned=scanned)


# ---------------- move classes relative to a truth S0 -----------------
def phi(S, S0):
    return len(set(S) ^ set(S0))


def is_progress(S, T, S0):
    return phi(T, S0) < phi(S, S0)


def D_strict(m, S, S0):
    """W1-T37R D_S: best progress neighbour strictly beats S and every non-progress neighbour."""
    nb = m.neighbours(S)
    prog = [m.F(T) for T in nb if is_progress(S, T, S0)]
    non = [m.F(T) for T in nb if not is_progress(S, T, S0)] + [m.F(S)]
    return bool(prog) and max(prog) > max(non)


def D_lex(m, S, S0):
    """A-REV2 tie-aware event: the lex-first maximiser of F over all feasible neighbours is progress and beats S."""
    T, f = m.best_neighbour(S)
    return T is not None and is_progress(S, T, S0) and f > m.F(S)


def TDP_via_M(m, family, S0):
    """TD'_P(family) as defined through the greedy map M (W1-T37R definition)."""
    S0 = tuple(sorted(S0))
    if m.M(S0) is not None:
        return False
    for S in family:
        S = tuple(sorted(S))
        if S == S0:
            continue
        T = m.M(S)
        if T is None or not is_progress(S, T, S0):
            return False
    return True


def region(p, S0, a, d, K):
    """R_{a,d}: U ∪ P, U ⊆ S0 missing ≤ a truths, P ⊆ nulls, |P| ≤ d, |U ∪ P| ≤ K."""
    S0 = tuple(sorted(S0)); nulls = [j for j in range(p) if j not in S0]; out = []
    for mm in range(0, min(a, len(S0)) + 1):
        for drop in itertools.combinations(S0, mm):
            U = [j for j in S0 if j not in drop]
            for e in range(0, d + 1):
                for P in itertools.combinations(nulls, e):
                    S = tuple(sorted(U + list(P)))
                    if len(S) <= K:
                        out.append(S)
    return out


def frame(n, k, rng):
    """k orthonormal vectors in range(C) (centred), each scaled to norm sqrt(n-1)."""
    Z = rng.standard_normal((n, k)); Z -= Z.mean(0)
    E, _ = np.linalg.qr(Z)
    return E * np.sqrt(n - 1)
