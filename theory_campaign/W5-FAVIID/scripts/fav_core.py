"""W5-FAVIID core: study-design generator (numpy port of Scripts/Data_generators/gen_dev_data.R, distributionally
equal, not bitwise), fast block tables, and helpers. Builds on pxn_core.py (W3-PXN, copied verbatim).

Notation: 00_COMMON.md. Exact arithmetic up to floating point (EX-A).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp
import pxn_core as pc

PATTERN = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
POS = np.array([3, 2, 4, 1, 5, 3])  # 1-based position inside the group (gen_dev_data.R::truth)


def truth(p):
    """0-based active indices, betas and 0-based truth groups, as gen_dev_data.R::truth (p = 500, 1000)."""
    s0 = {30: 5, 500: 14, 1000: 14}[p]
    step = {30: 1, 500: 7, 1000: 13}[p]
    k = np.arange(s0)
    grp = step * k                          # 0-based group index (R: block = 1 + step*k)
    active = 5 * grp + POS[k % 6] - 1       # 0-based
    beta = PATTERN[k % 6]
    return active, beta, grp


def group_rho(scen, p):
    """Within-group correlation per group of 5 (block-diagonal scenarios only)."""
    G = p // 5
    g = np.arange(G)
    if scen == 1:
        return np.zeros(G)
    if scen == 3:
        return np.full(G, 0.7)
    if scen == 4:
        return np.full(G, 0.85)
    if scen == 6:
        return 0.4 + 0.1 * (g % 6)
    raise ValueError("only block-diagonal scenarios 1, 3, 4, 6")


def gen_raw_X(scen, n, p, rng):
    """Rows iid N(0, Sigma), Sigma block-diagonal (groups of 5, equicorrelation rho_g)."""
    rho = group_rho(scen, p)
    Z = rng.standard_normal((n, p))
    if scen == 1:
        return Z
    # equicorrelated group: x = sqrt(rho) f + sqrt(1-rho) e  (exact Gaussian law, same as chol)
    G = p // 5
    f = rng.standard_normal((n, G))
    X = Z * np.repeat(np.sqrt(1 - rho), 5)[None, :] + np.repeat(f * np.sqrt(rho)[None, :], 5, axis=1)
    return X


def gen_study(scen, n, p, scale, rng, X=None):
    """Returns (Xraw, yraw, active, theta) following gen_dev_data.R: signal = X_std beta (sample-sd scaling),
    y = scale*signal + eps, eps ~ N(0,1). theta = scale*beta (population contrast-scale coefficients)."""
    if X is None:
        X = gen_raw_X(scen, n, p, rng)
    active, beta, _ = truth(p)
    Xs = X[:, active] - X[:, active].mean(0)
    Xs /= np.sqrt((Xs ** 2).sum(0) / (n - 1))
    eps = rng.standard_normal(n)
    y = scale * (Xs @ beta) + eps
    return X, y, active, scale * beta


# ------------------------------------------------------------------ fast tables
def _mask_index(g):
    masks = np.arange(1 << g)
    bits = ((masks[:, None] >> np.arange(g)[None, :]) & 1).astype(bool)
    pcnt = bits.sum(1)
    idx = {}
    for k in range(1, g + 1):
        sel = np.flatnonzero(pcnt == k)
        idx[k] = (sel, np.nonzero(bits[sel])[1].reshape(-1, k))
    return pcnt, idx


_MI = {}


def mask_index(g):
    if g not in _MI:
        _MI[g] = _mask_index(g)
    return _MI[g]


class FastTables(pc.Tables):
    """Same object as pxn_core.Tables (lr[b][mask] = log r_b(U)), built with vectorised mask enumeration."""

    def __init__(self, D, blocks, chunk=40000):
        self.D, self.blocks = D, blocks
        self.where = {}
        for b, C in enumerate(blocks):
            for t, j in enumerate(C):
                self.where[j] = (b, t)
        self.lr, self.size = [], []
        for C in blocks:
            g = len(C)
            G = D.gram(C)
            z = D.z[C]
            pcnt, idx = mask_index(g)
            lr = np.zeros(1 << g)
            for k in range(1, g + 1):
                sel, M = idx[k]
                for s in range(0, len(sel), chunk):
                    lr[sel[s:s + chunk]] = pc.log_m_batch(M[s:s + chunk], G, z, D.n, D.nu) - D.lm0
            self.lr.append(lr)
            self.size.append(pcnt)


def groups_of(p, scen):
    if scen == 1:
        return [[j] for j in range(p)]
    return [list(range(5 * h, 5 * h + 5)) for h in range(p // 5)]


def blocks_are_unions(blocks, groups):
    gid = np.empty(sum(len(g) for g in groups), int)
    for h, g in enumerate(groups):
        gid[g] = h
    for C in blocks:
        hs = set(gid[C])
        if sum(len(groups[h]) for h in hs) != len(C):
            return False
    return True


def ml_const(c):
    """c * E_{1/2}(1/c), E_{1/2}(x) = sum_j x^j/Gamma(j/2+1) = exp(x^2) erfc(-x)."""
    from scipy.special import erfc
    x = 1.0 / c
    return c * math.exp(x * x) * erfc(-x)
