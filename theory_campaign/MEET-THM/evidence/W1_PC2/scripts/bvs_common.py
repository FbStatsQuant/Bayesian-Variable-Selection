"""Common exact-arithmetic (float64) helpers for W1_PC2 checks of Seat C cards.

Target = METHODOLOGY_v3 §5 (unchanged in v3.1): g = n, tau = 1, IG(a0, b0) with a0 = b0 = 0.01,
BB(1, p) prior capped at K = min(p, floor(n/2)).  Standardised data: ||x_j||^2 = n - 1, Y = y'y = n - 1.
Blocks: complete linkage on 1 - |r|, top-down size cut at B, next-fit packing in leaf order (M §6.3).
"""
import itertools
import math
import numpy as np
from scipy.special import gammaln

A0 = 0.01
B0 = 0.01


def standardise(X, y):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n = X.shape[0]
    Xc = X - X.mean(0)
    Xs = Xc / np.sqrt((Xc ** 2).sum(0) / (n - 1))
    yc = y - y.mean()
    ys = yc / np.sqrt((yc ** 2).sum() / (n - 1))
    return Xs, ys


def suff_from_data(X, y):
    Xs, ys = standardise(X, y)
    return Xs.T @ Xs, Xs.T @ ys, float(ys @ ys), Xs.shape[0]


def method_sizes(n, p):
    K = min(p, n // 2)
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    return K, B


def log_m(G, z, Y, n, S):
    """log m(S) minus log C_n."""
    nu = A0 + n / 2.0
    S = list(S)
    if len(S) == 0:
        return -nu * math.log(2 * B0 + Y)
    GS = G[np.ix_(S, S)]
    k = len(S)
    H = (n + 1) * GS + np.eye(k)
    A = GS + np.eye(k)
    LH = np.linalg.cholesky(H)
    LA = np.linalg.cholesky(A)
    ldH = 2 * np.log(np.diag(LH)).sum()
    ldA = 2 * np.log(np.diag(LA)).sum()
    w = np.linalg.solve(LH, z[S])
    Q = Y - n * float(w @ w)
    return -0.5 * (ldH - ldA) - nu * math.log(2 * B0 + Q)


def log_prior_w(p, k):
    # w(k) = B(1+k, 2p-k)/B(1,p)  (unnormalised over the cap; W_K cancels in d and in pi up to Z)
    return (gammaln(1 + k) + gammaln(2 * p - k) - gammaln(2 * p + 1)) - (gammaln(1) + gammaln(p) - gammaln(p + 1))


def all_models(p, K):
    out = []
    for k in range(0, K + 1):
        out.extend(itertools.combinations(range(p), k))
    return out


# ---------- coded partition (M §6.3) ----------

def complete_linkage_tree(Dm):
    """Return dendrogram as nested tuples; ties broken lexicographically on sorted index lists."""
    p = Dm.shape[0]
    clusters = [(i,) for i in range(p)]
    trees = {(i,): i for i in range(p)}
    while len(clusters) > 1:
        best = None
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                ca, cb = clusters[a], clusters[b]
                dist = max(Dm[i, j] for i in ca for j in cb)
                key = (dist, tuple(sorted(ca + cb)))
                if best is None or key < best[0]:
                    best = (key, a, b)
        _, a, b = best
        ca, cb = clusters[a], clusters[b]
        # child order: smallest index first
        if min(ca) > min(cb):
            ca, cb = cb, ca
        new = tuple(sorted(ca + cb))
        trees[new] = (trees[ca], trees[cb])
        clusters = [c for k, c in enumerate(clusters) if k not in (a, b)] + [new]
    return trees[clusters[0]]


def leaves(t):
    if isinstance(t, int):
        return [t]
    return leaves(t[0]) + leaves(t[1])


def cut_tree(t, B):
    """Top-down: split nodes with > B members into children (smallest index first)."""
    lv = leaves(t)
    if len(lv) <= B:
        return [lv]
    c0, c1 = t
    if min(leaves(c0)) > min(leaves(c1)):
        c0, c1 = c1, c0
    return cut_tree(c0, B) + cut_tree(c1, B)


def next_fit(clusters, B):
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) <= B:
            cur = cur + c
        else:
            blocks.append(cur)
            cur = list(c)
    if cur:
        blocks.append(cur)
    return blocks


def coded_partition(G, B):
    d = np.sqrt(np.diag(G))
    R = G / np.outer(d, d)
    Dm = 1 - np.abs(R)
    t = complete_linkage_tree(Dm)
    return next_fit(cut_tree(t, B), B)


# ---------- discrepancy and the card's D_* ----------

def d_table(G, z, Y, n, blocks, K):
    p = G.shape[0]
    bid = np.empty(p, int)
    for b, C in enumerate(blocks):
        for j in C:
            bid[j] = b
    lm0 = log_m(G, z, Y, n, [])
    cache = {}

    def lr(U):
        U = tuple(sorted(U))
        if U not in cache:
            cache[U] = log_m(G, z, Y, n, U) - lm0
        return cache[U]

    models = all_models(p, K)
    d = np.empty(len(models))
    lbf = np.empty(len(models))
    for i, S in enumerate(models):
        full = log_m(G, z, Y, n, S) - lm0
        parts = {}
        for j in S:
            parts.setdefault(bid[j], []).append(j)
        d[i] = full - sum(lr(U) for U in parts.values())
        lbf[i] = full
    return models, d, lbf


def card_Dstar(G, z, Y, n, blocks, K):
    p = G.shape[0]
    GD = np.zeros_like(G)
    for C in blocks:
        GD[np.ix_(C, C)] = G[np.ix_(C, C)]
    E = G - GD
    HD = (n + 1) * GD + np.eye(p)
    AD = GD + np.eye(p)
    nu = A0 + n / 2.0
    a = n * float(z @ np.linalg.solve(HD, z)) / (2 * B0 + Y)

    def rel(M, Pm):
        w, V = np.linalg.eigh(M)
        Mih = V @ np.diag(w ** -0.5) @ V.T
        return float(np.max(np.abs(np.linalg.eigvalsh(Mih @ Pm @ Mih))))

    dA = rel(AD, E)
    dH = rel(HD, (n + 1) * E)
    out = dict(a=a, dA=dA, dH=dH, nu=nu, K=K)
    if not (a < 1 and dA < 1 and dH < 1):
        out.update(r=float('nan'), ok=False, Dstar=float('inf'))
        return out
    r = dH * a / ((1 - dH) * (1 - a))
    out['r'] = r
    if not r < 1:
        out.update(ok=False, Dstar=float('inf'))
        return out
    bX = K / 2.0 * (-math.log1p(-dA) - math.log1p(-dH)) - nu * math.log1p(-r)
    out['bX'] = bX
    out['shared'] = nu * a * a / (2 * (1 - a))
    out['Dstar'] = out['shared'] + 2 * bX
    out['ok'] = True
    return out


def exact_gram_suff(Sigma, theta, n, sigma2, rng):
    """Exact sufficient statistics under model G with centred X'X = (n-1) Sigma (exact Gram realisation),
    response standardised afterwards.  X'eps ~ N(0, sigma2 (n-1) Sigma); eps'(C - P_X)eps ~ sigma2 chi2_{n-1-p}."""
    p = Sigma.shape[0]
    G = (n - 1) * Sigma
    L = np.linalg.cholesky(G)
    Xe = math.sqrt(sigma2) * (L @ rng.standard_normal(p))
    # ||P_X eps||^2 = Xe' G^{-1} Xe
    pxe = float(Xe @ np.linalg.solve(G, Xe))
    resid = sigma2 * rng.chisquare(n - 1 - p)
    Xty = G @ theta + Xe
    yy = float(theta @ G @ theta) + 2 * float(theta @ Xe) + pxe + resid
    sy = math.sqrt(yy / (n - 1))
    return G, Xty / sy, float(n - 1), n
