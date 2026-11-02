"""W7-SEP core: exact small-p computations on the linked-hub family LH (W1-EXP section 4.1).

Everything is computed exactly by full enumeration of all 2^p models (p <= 20):
  * the score F(S) = log w(|S|) + log m(S) of 00_COMMON section 1 (standardised X, y; nu = 0.01 + n/2;
    2 b0 = 0.02; beta_S ~ N(0, n sigma^2 (G_S + I)^{-1}); BB(1, p) prior capped at K = min(p, n // 2));
  * the composite start pi0(S) ∝ w(|S|) prod_b r_b(S ∩ C_b), r_b(U) = m(U)/m(∅), blocks = groups
    (W1-EXP Lemma 4.2 / W3-PXN P1: the v3 partition equals the groups w.p. -> 1 when g <= B < 2g; at these p the
    method itself would take the exact branch, so pi0 here is the analytically defined component law, as in W1-EXP);
  * the posterior pi(S) ∝ exp F(S);
  * the production local search (METHODOLOGY section 6.10): from a centre, scan every feasible flip and swap,
    move to the best strict improvement, at most ell = ceil(log2(n + p + 1)) moves, then one further scan.
    "S0 scored" = S0 is the centre or a scanned neighbour of some centre on the path (centre emitted).
    The successor map is computed for all 2^p centres at once (vectorised over bitmasks).

Scorer cross-checked against the dense formula of W4-T38FULL/scripts/lh_ls0_check.py (see sanity.py).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp


# ---------------------------------------------------------------- family
def lh_sigma(G, g, rho, pairs):
    """W1-EXP LH covariance. pairs: list of (group_a, group_b, psi); the hub of a group is its first index."""
    p = G * g
    S = np.zeros((p, p))
    for h in range(G):
        S[h * g:(h + 1) * g, h * g:(h + 1) * g] = rho
    np.fill_diagonal(S, 1.0)
    for (ga, gb, psi) in pairs:
        ja, jb = ga * g, gb * g
        for k in range(ga * g, (ga + 1) * g):
            for l in range(gb * g, (gb + 1) * g):
                S[k, l] = S[l, k] = psi * S[k, ja] * S[jb, l]
    return S


def make_config(name):
    """Returns dict(G, g, rho, pairs, betas, visible) for the named configuration."""
    if name == "B2":   # W1-EXP config B: c = 2, p = 20, 5 groups of 4, one null group
        return dict(G=5, g=4, rho=0.7, pairs=[(0, 1, 0.5), (2, 3, 0.5)], betas=[1.4, 1.8], visible={})
    if name == "C3":   # c = 3, p = 18, 6 groups of 3, no null group
        return dict(G=6, g=3, rho=0.7, pairs=[(0, 1, 0.5), (2, 3, 0.5), (4, 5, 0.5)],
                    betas=[1.4, 1.8, 1.6], visible={})
    if name == "V2":   # c = 2 plus one visible group and one null group, p = 18, groups of 3
        return dict(G=6, g=3, rho=0.7, pairs=[(0, 1, 0.5), (2, 3, 0.5)], betas=[1.4, 1.8], visible={4: 1.0})
    if name == "A1":   # c = 1 control (no separation expected), p = 16, 4 groups of 4
        return dict(G=4, g=4, rho=0.7, pairs=[(0, 1, 0.5)], betas=[1.4], visible={2: 1.8})
    raise ValueError(name)


def build(cfg, n, rng, design="gram"):
    G, g, rho, pairs = cfg["G"], cfg["g"], cfg["rho"], cfg["pairs"]
    p = G * g
    Sig = lh_sigma(G, g, rho, pairs)
    theta = np.zeros(p)
    for (ga, gb, psi), b in zip(pairs, cfg["betas"]):
        theta[ga * g] = b
        theta[gb * g] = -psi * b
    for h, b in cfg["visible"].items():
        theta[h * g] = b
    L = np.linalg.cholesky(Sig)
    if design == "gram":
        # exact Gram, centred: X'X = (n-1) Sigma; sufficient statistics simulated exactly (W1-EXP):
        # X'eps = sqrt(n-1) L xi, xi ~ N_p(0, I); ||(I - P_X) eps||^2 ~ chi^2_{n-1-p}; then centre/standardise y.
        xi = rng.standard_normal(p)
        Xte = math.sqrt(n - 1) * L @ xi
        resid2 = rng.chisquare(n - 1 - p)
        GX = (n - 1) * Sig
        Xty_raw = GX @ theta + Xte
        # ||y_c||^2 = theta'G theta + 2 theta'X'eps + ||P_X eps||^2 + ||(I-P_X) eps||^2 ; ||P_X eps||^2 = ||xi||^2
        yy_raw = theta @ GX @ theta + 2 * theta @ Xte + xi @ xi + resid2
    else:
        X = rng.standard_normal((n, p)) @ L.T
        X = X - X.mean(0)
        X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
        eps = rng.standard_normal(n)
        yr = X @ theta + eps
        yr = yr - yr.mean()
        GX = X.T @ X
        Xty_raw = X.T @ yr
        yy_raw = float(yr @ yr)
    s = math.sqrt(yy_raw / (n - 1))
    S0 = tuple(int(j) for j in np.flatnonzero(theta))
    M = tuple(gb * g for (_, gb, _) in pairs)
    Sstar = tuple(sorted(set(S0) - set(M)))
    blocks = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    null_groups = [h for h in range(G) if all(h not in (ga, gb) for (ga, gb, _) in pairs) and h not in cfg["visible"]]
    R = sorted(j for h in range(G) if h not in null_groups for j in range(h * g, (h + 1) * g))
    return dict(p=p, n=n, GX=GX, z=Xty_raw / s, yy=yy_raw / s ** 2, S0=S0, M=M, Sstar=Sstar,
                blocks=blocks, R=R, theta=theta, Sigma=Sig)


# ---------------------------------------------------------------- scores
def logw(k, p):
    """BB(1, p) prior mass of one model of size k: w(k) = 1/2 / C(2p-1, k) (W4-T38FULL convention)."""
    return math.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


def all_logm(d):
    """log m(S) (up to an S-free constant) for every bitmask S, by DFS with incremental Cholesky."""
    p, n, GX, z, yy = d["p"], d["n"], d["GX"], d["z"], d["yy"]
    nu = 0.01 + n / 2.0
    out = np.empty(1 << p)
    out[0] = -nu * math.log(0.02 + yy)
    # stack entries: (mask, last index, LH (chol of (n+1)G+I), LG (chol of G+I), w = LH^{-1} z_S, logdetH, logdetG)
    stack = [(0, -1, np.zeros((0, 0)), np.zeros((0, 0)), np.zeros(0), 0.0, 0.0, [])]
    while stack:
        mask, last, LHm, LGm, w, ldH, ldG, idx = stack.pop()
        k = len(idx)
        for j in range(last + 1, p):
            hcol = (n + 1) * GX[idx, j] if k else np.zeros(0)
            gcol = GX[idx, j] if k else np.zeros(0)
            if k:
                lh = np.linalg.solve(LHm, hcol) if k > 1 else hcol / LHm[0, 0]
                lg = np.linalg.solve(LGm, gcol) if k > 1 else gcol / LGm[0, 0]
            else:
                lh = lg = np.zeros(0)
            dh = math.sqrt((n + 1) * GX[j, j] + 1.0 - lh @ lh)
            dg = math.sqrt(GX[j, j] + 1.0 - lg @ lg)
            wj = (z[j] - lh @ w) / dh
            LH2 = np.zeros((k + 1, k + 1)); LH2[:k, :k] = LHm; LH2[k, :k] = lh; LH2[k, k] = dh
            LG2 = np.zeros((k + 1, k + 1)); LG2[:k, :k] = LGm; LG2[k, :k] = lg; LG2[k, k] = dg
            w2 = np.append(w, wj)
            ldH2 = ldH + 2 * math.log(dh)
            ldG2 = ldG + 2 * math.log(dg)
            Q = yy - n * float(w2 @ w2)
            m2 = mask | (1 << j)
            out[m2] = -0.5 * (ldH2 - ldG2) - nu * math.log(0.02 + Q)
            if j < p - 1:
                stack.append((m2, j, LH2, LG2, w2, ldH2, ldG2, idx + [j]))
    return out


def popcount_array(p):
    pc = np.zeros(1 << p, dtype=np.int64)
    for j in range(p):
        pc[1 << j:1 << (j + 1)] = pc[:1 << j] + 1
    return pc


def mask_of(S):
    m = 0
    for j in S:
        m |= 1 << j
    return m


def set_of(m, p):
    return tuple(j for j in range(p) if m >> j & 1)


def scores(d):
    p, n = d["p"], d["n"]
    K = min(p, n // 2)
    pc = popcount_array(p)
    lm = all_logm(d)
    lw = np.array([logw(k, p) for k in range(p + 1)])
    F = lw[pc] + lm
    F[pc > K] = -np.inf
    # start law: blocks = groups
    lr = lm - lm[0]                      # log BF(S) = log r(S) for the table of S itself
    log_g0 = lw[pc].copy()
    for blk in d["blocks"]:
        bm = mask_of(blk)
        log_g0 += lr[np.arange(1 << p) & bm]
    log_g0[pc > K] = -np.inf
    return dict(F=F, log_g0=log_g0, pc=pc, K=K,
                log_pi=F - logsumexp(F), log_pi0=log_g0 - logsumexp(log_g0))


# ---------------------------------------------------------------- production local search, all centres at once
def successor(F, p, K, pc):
    """succ[C] = best strict-improving flip/swap neighbour of C (ties: larger F first, then lexicographically
    smallest index tuple -- ties have probability 0 here), or C itself if none."""
    N = 1 << p
    allm = np.arange(N, dtype=np.int64)
    bestF = F.copy()
    best = allm.copy()
    cand_moves = []
    for j in range(p):
        cand_moves.append((j, None))
    for i in range(p):
        for j in range(p):
            if i != j:
                cand_moves.append((i, j))
    for (i, j) in cand_moves:
        if j is None:
            nb = allm ^ (1 << i)
            feas = (pc[nb] <= K)
        else:  # swap: i in C (deleted), j not in C (added)
            feas = ((allm >> i) & 1).astype(bool) & ~((allm >> j) & 1).astype(bool)
            nb = allm ^ (1 << i) ^ (1 << j)
        fn = np.where(feas, F[nb], -np.inf)
        upd = fn > bestF
        bestF = np.where(upd, fn, bestF)
        best = np.where(upd, nb, best)
    return best


def near_mask(p, K, pc, S0m):
    """True for centres C whose scan (or C itself) contains S0: C = S0, a flip of S0, or a swap of S0."""
    N = 1 << p
    allm = np.arange(N, dtype=np.int64)
    x = allm ^ S0m
    dist = popcount_array(p)[x]
    near = dist <= 1
    # swap neighbours: |C Δ S0| = 2 with |C| = |S0|
    near |= (dist == 2) & (pc == pc[S0m])
    # feasibility of the flip that reaches S0 (addition needs |C| < K): |C| = |S0|-1 <= K-1 always here
    return near


def ls_scores_S0(succ, near, ell):
    """For every centre: does the production search (<= ell moves, then one more scan) score S0?"""
    cur = np.arange(len(succ), dtype=np.int64)
    hit = near[cur].copy()
    moves = np.zeros(len(succ), dtype=np.int64)
    for _ in range(ell):
        nxt = succ[cur]
        moved = nxt != cur
        moves += moved
        cur = nxt
        hit |= near[cur]
    return hit, cur, moves
