"""Exact enumeration for the p=10 miniature design (g=2, c=2 linked pairs, 1 null group), used by N6 and N7."""
import itertools
import numpy as np
from lhcommon import *

P, GG, CC, VV = 10, 2, 2, 0
RHO, PSI, BETA, SIGMA = 0.7, 0.5, 1.0, 1.0
JA = [0, 4]          # hubs a_1, a_2
JB = [2, 6]          # hubs b_1, b_2 (masked)
S0 = (0, 2, 4, 6)
SDEG = (0, 4)        # S-degree = S0 minus masked hubs
_Sigma = build_sigma(P, GG, CC, RHO, np.array([PSI, PSI]))
_theta = build_theta(P, GG, CC, VV, np.array([PSI, PSI]), np.array([BETA, BETA]), np.array([]))
_L = np.linalg.cholesky(_Sigma)


def make_data(n, seed_key):
    rng = np.random.default_rng(seed_key)
    Xr, yr = draw_raw(rng, n, _L, _theta, SIGMA)
    X, y, Y, Xc = standardise(Xr, yr)
    return X, y


def all_models(K):
    ms = []
    for k in range(0, K + 1):
        ms += list(itertools.combinations(range(P), k))
    return ms


def enumerate_F(X, y):
    n = X.shape[0]
    K = min(P, n // 2)
    sc = Scorer(X, y)
    F = {}
    for S in all_models(K):
        F[S] = sc.F(S)
    return F, K


def posterior(F):
    keys = list(F.keys())
    f = np.array([F[k] for k in keys])
    lse = f.max() + np.log(np.exp(f - f.max()).sum())
    pi = {k: np.exp(F[k] - lse) for k in keys}
    return pi, lse


def log1m_pi(F, S, lse_cache=None):
    """log(1 - pi(S)) computed without cancellation."""
    f = np.array([v for k, v in F.items() if k != S])
    m = f.max()
    lo = m + np.log(np.exp(f - m).sum())
    fs = F[S]
    mm = max(lo, fs)
    lt = mm + np.log(np.exp(lo - mm) + np.exp(fs - mm))
    return lo - lt


def neighbours(S, K):
    """All feasible flips and swaps of S (as sorted tuples)."""
    Sset = set(S)
    out = []
    for l in range(P):
        if l not in Sset and len(S) < K:
            out.append(tuple(sorted(Sset | {l})))
    for k in S:
        out.append(tuple(sorted(Sset - {k})))
    for k in S:
        for l in range(P):
            if l not in Sset:
                out.append(tuple(sorted((Sset - {k}) | {l})))
    return out


def best_of(cands, F):
    """Best by score; ties broken lexicographically on sorted index tuples (smallest tuple)."""
    return min(cands, key=lambda s: (-F[s], s))


def local_search(F, K, start, ell):
    """Production local search (PROOF 8.4).  Returns dict(scored, path, status, final, moves, scans)."""
    centre = start
    scored = {start}
    path = [start]
    moves = 0
    scans = 0
    while True:
        nb = neighbours(centre, K)
        scans += 1
        scored.update(nb)
        best = best_of(nb, F)
        if F[best] > F[centre]:
            if moves < ell:
                centre = best
                moves += 1
                path.append(centre)
                continue
            return dict(scored=scored, path=path, status="local_limit", final=centre, moves=moves, scans=scans)
        return dict(scored=scored, path=path, status="local_certified", final=centre, moves=moves, scans=scans)


def lattice_states():
    """Lat(S0 degree) minus S0: S_deg + M' with M' proper subset of the masked hubs, as (S, I) pairs."""
    res = []
    for r in range(CC):
        for Mp in itertools.combinations(range(CC), r):
            S = tuple(sorted(list(SDEG) + [JB[i] for i in Mp]))
            I = [i for i in range(CC) if i not in Mp]
            res.append((S, I))
    return res


def check_DS(F, K, S, I):
    """(D_S): best progress neighbour beats S and every non-progress neighbour strictly.  Returns (holds, margin)."""
    prog = [tuple(sorted(set(S) | {JB[i]})) for i in I]
    Pbest = max(F[a] for a in prog)
    nonprog = [a for a in neighbours(S, K) if a not in prog] + [S]
    worst = max(F[a] for a in nonprog)
    return Pbest > worst, Pbest - worst


def check_L(F, K):
    """(L): S0 strict local maximum among all flips and swaps."""
    worst = max(F[a] for a in neighbours(S0, K))
    return F[S0] > worst, F[S0] - worst
