"""C-MIS numerics core: exact posterior of the shipped SMC-BVS target on a candidate design, by full enumeration.

Target (Docs/Theory/theorems/00_COMMON.md §1; SoP 02_method.tex:87-106):
  standardised X (||x_j||^2 = n-1), y (||y||^2 = n-1); G_S = X_S'X_S; z_S = X_S'y; H_S = (n+1)G_S + I;
  D_S = det H_S / det(G_S + I); Q_S = y'y - n z_S' H_S^{-1} z_S; nu = a0 + n/2, a0 = b0 = 0.01;
  log m(S) = -1/2 log D_S - nu log(2 b0 + Q_S) (+ const); w(k) = 1/2 / C(2p-1, k); K = min(p, floor(n/2)).
Run with Python 3.13 (numpy). The default python 3.15 has no numpy.
"""
import itertools
import math
import numpy as np

A0 = B0 = 0.01


def standardise(Xr, yr):
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(0)
    sd = np.sqrt((Xc ** 2).sum(0) / (n - 1))
    X = Xc / sd
    yc = yr - yr.mean()
    sy = math.sqrt((yc ** 2).sum() / (n - 1))
    return X, yc / sy, sd


def all_subsets(p, K):
    out = []
    for k in range(0, min(p, K) + 1):
        out.extend(itertools.combinations(range(p), k))
    return out


def log_w(p, k):
    # log of 1/2 / C(2p-1, k)
    return math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))


def exact_posterior(Xr, yr, subsets=None):
    """Return (subsets, posterior probabilities) over Omega = {S : |S| <= K} for the candidate design Xr."""
    n, p = Xr.shape
    K = min(p, n // 2)
    X, y, _ = standardise(Xr, yr)
    G = X.T @ X
    z = X.T @ y
    yy = float(y @ y)
    nu = A0 + n / 2.0
    if subsets is None:
        subsets = all_subsets(p, K)
    logpost = np.empty(len(subsets))
    for i, S in enumerate(subsets):
        k = len(S)
        if k == 0:
            logD = 0.0
            Q = yy
        else:
            idx = list(S)
            GS = G[np.ix_(idx, idx)]
            H = (n + 1) * GS + np.eye(k)
            sH, ldH = np.linalg.slogdet(H)
            sG, ldG = np.linalg.slogdet(GS + np.eye(k))
            logD = ldH - ldG
            zS = z[idx]
            Q = yy - n * float(zS @ np.linalg.solve(H, zS))
        logpost[i] = log_w(p, k) - 0.5 * logD - nu * math.log(2 * B0 + Q)
    logpost -= logpost.max()
    w = np.exp(logpost)
    return subsets, w / w.sum()


def summarise(subsets, post, p, targets):
    """targets: dict name -> frozenset. Returns dict with masses, PIPs, HPM."""
    out = {}
    index = {frozenset(S): i for i, S in enumerate(subsets)}
    for name, T in targets.items():
        out["pi_" + name] = float(post[index[frozenset(T)]]) if frozenset(T) in index else 0.0
    pip = np.zeros(p)
    for S, q in zip(subsets, post):
        for j in S:
            pip[j] += q
    out["pip"] = pip.tolist()
    out["hpm"] = sorted(subsets[int(np.argmax(post))])
    return out
