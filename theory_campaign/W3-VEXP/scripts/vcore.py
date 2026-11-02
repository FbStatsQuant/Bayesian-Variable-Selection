"""W3-VEXP independent core (referee code; written from the spec, not from W1-EXP's scripts).

Objects (METHODOLOGY_v3 §5, §6.3; 00_COMMON §1-2; engine cpp/v3_score.h, v3_blocks.h, v3_start.h):
  log m(S) = log C_n - 0.5[log det H_S - log det(G_S+I)] - nu log(0.02 + Q_S),
  H_S = (n+1)G_S + I, Q_S = y'y - n z_S' H_S^{-1} z_S, nu = 0.01 + n/2;
  w(k) = 1/(2 C(2p-1,k)), cap K = min(p, floor(n/2));
  blocks: complete linkage on 1-|r| with R13 ties, top-down cut at B, next-fit packing in leaf order;
  tables r_b(U) = m(U)/m(empty); gamma0(S) = w(|S|) prod_b r_b(S n C_b).
Everything is computed from (G, z, y'y, n) exactly in float64; log C_n cancels in every ratio used here.
"""
import itertools
import math
import numpy as np
from scipy.special import gammaln


def logw(p, k):
    """log w(k) = log(1/2) - log C(2p-1, k)."""
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class Suff:
    """Sufficient statistics of a standardised data set."""

    def __init__(self, G, z, yty, n):
        self.G = np.asarray(G, float)
        self.z = np.asarray(z, float)
        self.yty = float(yty)
        self.n = int(n)
        self.p = self.G.shape[0]
        self.nu = 0.01 + n / 2.0
        self.K = min(self.p, n // 2)

    def logm_rel(self, S):
        """log m(S) - log C_n for a single model S (tuple of indices)."""
        S = list(S)
        n = self.n
        if len(S) == 0:
            return -self.nu * math.log(0.02 + self.yty)
        Gs = self.G[np.ix_(S, S)]
        zs = self.z[S]
        H = (n + 1) * Gs + np.eye(len(S))
        A = Gs + np.eye(len(S))
        LH = np.linalg.cholesky(H)
        LA = np.linalg.cholesky(A)
        w = np.linalg.solve(LH, zs)
        Q = self.yty - n * float(w @ w)
        ld = 2 * np.log(np.diag(LH)).sum() - 2 * np.log(np.diag(LA)).sum()
        return -0.5 * ld - self.nu * math.log(0.02 + Q)

    def logm_batch(self, idx):
        """idx: (N, k) int array of models of common size k >= 1. Returns log m - log C_n."""
        n = self.n
        N, k = idx.shape
        Gs = self.G[idx[:, :, None], idx[:, None, :]]
        zs = self.z[idx]
        I = np.eye(k)
        H = (n + 1) * Gs + I
        A = Gs + I
        LH = np.linalg.cholesky(H)
        LA = np.linalg.cholesky(A)
        w = np.linalg.solve(LH, zs[:, :, None])[:, :, 0]
        Q = self.yty - n * np.einsum('ij,ij->i', w, w)
        ld = 2 * np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(1) - 2 * np.log(np.diagonal(LA, axis1=1, axis2=2)).sum(1)
        return -0.5 * ld - self.nu * np.log(0.02 + Q)


# ---------------------------------------------------------------- partition (port of v3_blocks.h)
def complete_linkage(R):
    """R: correlation matrix. Returns (left, right, size, minidx, root) with leaves 0..p-1 and internal nodes
    p..2p-2 in merge order. Merge = smallest complete-linkage distance; exact ties -> lexicographically smallest
    sorted union (R13); left child = child with the smaller minimum index."""
    p = R.shape[0]
    left = [-1] * (2 * p - 1); right = [-1] * (2 * p - 1)
    size = [1] * (2 * p - 1); minidx = list(range(p)) + [0] * (p - 1)
    if p == 1:
        return left, right, size, minidx, 0
    D = 1.0 - np.abs(R)
    D = D.astype(float).copy()
    np.fill_diagonal(D, np.inf)
    mem = [[j] for j in range(p)]
    node = list(range(p))
    active = np.ones(p, bool)
    nxt = p
    for step in range(p - 1):
        m = D.min()
        ii, jj = np.nonzero(D == m)
        if len(ii) > 2:
            best = None
            for a, b in zip(ii, jj):
                if a >= b:
                    continue
                u = sorted(mem[a] + mem[b])
                if best is None or u < best[0]:
                    best = (u, a, b)
            _, a, b = best
        else:
            a, b = min(ii[0], jj[0]), max(ii[0], jj[0])
        na, nb = node[a], node[b]
        L, Rr = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        nn = nxt; nxt += 1
        left[nn], right[nn] = L, Rr
        size[nn] = size[na] + size[nb]
        minidx[nn] = min(minidx[na], minidx[nb])
        newrow = np.maximum(D[a], D[b])
        D[a, :] = newrow; D[:, a] = newrow
        D[a, a] = np.inf
        D[b, :] = np.inf; D[:, b] = np.inf
        mem[a] = sorted(mem[a] + mem[b]); mem[b] = []
        active[b] = False
        node[a] = nn
    return left, right, size, minidx, nxt - 1


def leaves(tree, nd, p):
    left, right = tree[0], tree[1]
    out, st = [], [nd]
    while st:
        x = st.pop()
        if x < p:
            out.append(x); continue
        st.append(right[x]); st.append(left[x])
    return out


def make_blocks(R, B):
    p = R.shape[0]
    tree = complete_linkage(R)
    size, root = tree[2], tree[4]
    clusters, st = [], [root]
    while st:
        x = st.pop()
        if size[x] <= B:
            clusters.append(leaves(tree, x, p)); continue
        st.append(tree[1][x]); st.append(tree[0][x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B:
            blocks.append(sorted(cur)); cur = []
        cur += c
    if cur:
        blocks.append(sorted(cur))
    return blocks


def B_rule(n, p):
    return min(int(math.isqrt(n)), int(math.isqrt(p)), 16)


# ---------------------------------------------------------------- tables, pi0, pi
def tables(sf, blocks):
    """logr[b][code] for every U subset of block b (code = bitmask over the block's sorted members)."""
    out = []
    l0 = sf.logm_rel(())
    for C in blocks:
        m = len(C)
        t = np.zeros(1 << m)
        for k in range(1, m + 1):
            combs = list(itertools.combinations(range(m), k))
            idx = np.array([[C[i] for i in c] for c in combs])
            lm = sf.logm_batch(idx)
            codes = np.array([sum(1 << i for i in c) for c in combs])
            t[codes] = lm - l0
        out.append(t)
    return out


def all_masks(p):
    return np.arange(1 << p, dtype=np.int64)


def popcount(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


def log_gamma0_all(sf, blocks, logr):
    """log gamma0 (unnormalised, without W_K) for every subset of [p] (p <= 22), -inf beyond the cap."""
    p = sf.p
    S = all_masks(p)
    k = popcount(S)
    lg = np.array([logw(p, kk) for kk in range(p + 1)])[k]
    for C, t in zip(blocks, logr):
        code = np.zeros_like(S)
        for i, j in enumerate(C):
            code |= ((S >> j) & 1) << i
        lg = lg + t[code]
    lg[k > sf.K] = -np.inf
    return S, k, lg


def log_post_all(sf):
    """log [w(|S|) m(S)/C_n] for every subset (exact full enumeration, p <= 20)."""
    p = sf.p
    S = all_masks(p)
    k = popcount(S)
    out = np.full(len(S), -np.inf)
    out[0] = logw(p, 0) + sf.logm_rel(())
    for kk in range(1, min(p, sf.K) + 1):
        sel = np.nonzero(k == kk)[0]
        bits = ((S[sel][:, None] >> np.arange(p)[None, :]) & 1).astype(bool)
        idx = np.nonzero(bits)[1].reshape(len(sel), kk)
        for st in range(0, len(sel), 20000):
            out[sel[st:st + 20000]] = logw(p, kk) + sf.logm_batch(idx[st:st + 20000])
    return S, k, out


def normalise(lg):
    m = lg.max()
    w = np.exp(lg - m)
    return w / w.sum()


def mask_of(S):
    return int(sum(1 << j for j in S))
