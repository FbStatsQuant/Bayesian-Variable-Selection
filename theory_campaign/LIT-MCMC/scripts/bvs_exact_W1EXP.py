"""Exact SMC-BVS v3 objects for small p (Python reimplementation for the W1-EXP theory run).

Implements, from METHODOLOGY_v3.md §5-§6.3 and Scripts/SMC_BVS/core/cpp/v3_blocks.h:
  * log m(S) on the standardised data (only through R = X'X/(n-1), r = X'y/(n-1), y'y = n-1),
  * the method partition (complete linkage on 1-|r|, R13 tie rule, top-down cut, next-fit packing),
  * block tables r_b(U) = BF(U), the composite start pi_0 (exact, by enumeration for p <= 20),
  * the full posterior pi (exact enumeration, batched by model size),
  * the T22(i) aggregation quantities q, u, e for a reference S°,
  * the EXP' remainders R_{n,b,T,l} for every within-block addition.
All work is on sufficient statistics, so n can be very large.  Python 3 + numpy/scipy only.
"""
import itertools
import math
import numpy as np
from scipy.special import gammaln

A0 = 0.01
B0 = 0.01


# ---------------------------------------------------------------- scores
def log_m(S, R, r, n):
    """log m(S) minus the S-free constant log C_n (cancels in every ratio we use).
    Standardised data: G_S=(n-1)R_S, z_S=(n-1)r_S, y'y=n-1."""
    S = list(S)
    nu = A0 + n / 2.0
    if len(S) == 0:
        Q = n - 1.0
        return -nu * math.log(2 * B0 + Q)
    RS = R[np.ix_(S, S)]
    rS = r[S]
    k = len(S)
    H = (n + 1.0) * (n - 1.0) * RS + np.eye(k)
    G1 = (n - 1.0) * RS + np.eye(k)
    sH, ldH = np.linalg.slogdet(H)
    sG, ldG = np.linalg.slogdet(G1)
    z = (n - 1.0) * rS
    Q = (n - 1.0) - n * z @ np.linalg.solve(H, z)
    return -0.5 * (ldH - ldG) - nu * math.log(2 * B0 + Q)


def log_m_batch(models, R, r, n):
    """Vectorised log m for an array of models of a common size k (shape (N,k))."""
    models = np.asarray(models)
    N, k = models.shape
    nu = A0 + n / 2.0
    if k == 0:
        return np.full(N, -nu * math.log(2 * B0 + n - 1.0))
    RS = R[models[:, :, None], models[:, None, :]]
    rS = r[models]
    I = np.eye(k)[None]
    H = (n + 1.0) * (n - 1.0) * RS + I
    G1 = (n - 1.0) * RS + I
    _, ldH = np.linalg.slogdet(H)
    _, ldG = np.linalg.slogdet(G1)
    z = (n - 1.0) * rS
    sol = np.linalg.solve(H, z[:, :, None])[:, :, 0]
    Q = (n - 1.0) - n * np.einsum("ij,ij->i", z, sol)
    return -0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)


def log_w(k, p):
    """log w(k) = log( 1/(2 binom(2p-1,k)) )."""
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


# ---------------------------------------------------------------- partition
def complete_linkage(Rc):
    """Port of v3_blocks.h::complete_linkage (R13 ties: smallest distance, then lexicographically
    smallest sorted union; left child = child with smaller minimum index)."""
    p = Rc.shape[0]
    dist = 1.0 - np.abs(Rc)
    mem = {j: [j] for j in range(p)}
    node = {j: j for j in range(p)}
    left, right, size, minidx = {}, {}, {j: 1 for j in range(p)}, {j: j for j in range(p)}
    active = set(range(p))
    D = {(a, b): dist[a, b] for a in range(p) for b in range(p) if a != b}
    nxt = p
    while len(active) > 1:
        best = None
        for a in active:
            for b in active:
                if a >= b:
                    continue
                key = (D[(a, b)], sorted(mem[a] + mem[b]))
                if best is None or key < best[0]:
                    best = (key, a, b)
        _, a, b = best
        na, nb = node[a], node[b]
        L, Rr = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        left[nxt], right[nxt] = L, Rr
        size[nxt] = size[na] + size[nb]
        minidx[nxt] = min(minidx[na], minidx[nb])
        mem[a] = sorted(mem[a] + mem[b])
        mem[b] = []
        active.discard(b)
        node[a] = nxt
        for x in active:
            if x == a:
                continue
            v = max(D[(x, a)], D[(x, b)])
            D[(x, a)] = D[(a, x)] = v
        nxt += 1
    root = nxt - 1 if p > 1 else 0
    return left, right, size, root


def subtree_leaves(left, right, nd, p):
    out, st = [], [nd]
    while st:
        x = st.pop()
        if x < p:
            out.append(x)
            continue
        st.append(right[x])
        st.append(left[x])
    return out


def make_blocks(Rc, B):
    p = Rc.shape[0]
    left, right, size, root = complete_linkage(Rc)
    clusters, st = [], [root]
    while st:
        x = st.pop()
        if size[x] <= B:
            clusters.append(subtree_leaves(left, right, x, p))
            continue
        st.append(right[x])
        st.append(left[x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B:
            blocks.append(cur)
            cur = []
        cur = cur + c
    if cur:
        blocks.append(cur)
    return [sorted(b) for b in blocks]


def block_size_B(n, p):
    return min(int(math.isqrt(n)), int(math.isqrt(p)), 16)


# ---------------------------------------------------------------- tables / start
def tables(blocks, R, r, n):
    """dict per block: {frozenset(U): log r_b(U)}"""
    l0 = log_m([], R, r, n)
    out = []
    for C in blocks:
        t = {}
        for k in range(len(C) + 1):
            for U in itertools.combinations(C, k):
                t[frozenset(U)] = log_m(U, R, r, n) - l0
        out.append(t)
    return out


def enumerate_models(p, K):
    for k in range(K + 1):
        for S in itertools.combinations(range(p), k):
            yield S


def start_logmass_all(blocks, tabs, p, n):
    """Return dict frozenset(S)->log pi_0(S) over Omega (exact enumeration; p <= 20)."""
    K = min(p, n // 2)
    blk = {}
    for b, C in enumerate(blocks):
        for j in C:
            blk[j] = b
    lw = [log_w(k, p) for k in range(K + 1)]
    keys, vals = [], []
    for S in enumerate_models(p, K):
        parts = [[] for _ in blocks]
        for j in S:
            parts[blk[j]].append(j)
        v = lw[len(S)] + sum(tabs[b][frozenset(parts[b])] for b in range(len(blocks)))
        keys.append(frozenset(S))
        vals.append(v)
    vals = np.array(vals)
    lz = np.logaddexp.reduce(vals)
    return dict(zip(keys, vals - lz))


def posterior_logmass_all(R, r, n):
    """dict frozenset(S)->log pi(S) over Omega (exact enumeration, batched by size)."""
    p = R.shape[0]
    K = min(p, n // 2)
    keys, vals = [], []
    for k in range(K + 1):
        combs = np.array(list(itertools.combinations(range(p), k)), dtype=int)
        if k == 0:
            combs = np.zeros((1, 0), dtype=int)
        lm = log_m_batch(combs, R, r, n) + log_w(k, p)
        keys.extend(frozenset(c) for c in combs.tolist())
        vals.append(lm)
    vals = np.concatenate(vals)
    lz = np.logaddexp.reduce(vals)
    return dict(zip(keys, vals - lz))


def region_mass(logmass, S0, d):
    """mass of R_d = {U u P : U subset S0, P subset S0^c, |P| <= d}"""
    S0 = frozenset(S0)
    v = [lv for S, lv in logmass.items() if len(S - S0) <= d]
    return float(np.exp(np.logaddexp.reduce(np.array(v))))


# ---------------------------------------------------------------- T22(i) quantities
def aggregation(blocks, tabs, Sref, p):
    """q, u, e of T22(i) (STATEMENT.md of T22) for reference Sref."""
    Sref = frozenset(Sref)
    s = len(Sref)
    Db, umax = [], {}
    e = 0.0
    for b, C in enumerate(blocks):
        Ub = frozenset(C) & Sref
        rest = [j for j in C if j not in Ub]
        t = tabs[b]
        # a_bj and D_b
        D = 0.0
        for j in range(1, len(rest) + 1):
            a = sum(math.exp(t[Ub | frozenset(V)] - t[Ub]) for V in itertools.combinations(rest, j))
            D = max(D, (math.factorial(j) * a) ** (1.0 / j))
        Db.append(D)
        # u: for l not in Sref, max over Ub subset T subset C\l
        for l in rest:
            others = [j for j in rest if j != l]
            m = -np.inf
            for k in range(len(others) + 1):
                for V in itertools.combinations(others, k):
                    T = Ub | frozenset(V)
                    m = max(m, t[T | {l}] - t[T])
            umax[l] = m
        # e
        for k in range(len(C) + 1):
            for U in itertools.combinations(C, k):
                U = frozenset(U)
                a = len(Ub - U)
                if a > 0:
                    e = max(e, math.exp((t[U] - t[U | Ub]) / a))
    e = 2 * p * e if s > 0 else 0.0
    if s < p:
        q = sum(Db) / (p - s)
        u = float(np.mean(np.exp([umax[l] for l in umax])))
    else:
        q = u = 0.0
    return q, u, e


def exp_prime_remainders(blocks, R, r, n):
    """All R_{n,b,T,l} = log[r_b(T+l)/r_b(T)] + 0.5 log(n+1) + nu log(1-x_{T,l}).
    x_{T,l} = (RSS_T - RSS_{T+l})/RSS_T computed on the standardised response (scale-free)."""
    nu = A0 + n / 2.0
    out = []

    def rss(T):  # RSS^y_T / (n-1) = 1 - r_T' R_T^{-1} r_T
        T = list(T)
        if not T:
            return 1.0
        return 1.0 - r[T] @ np.linalg.solve(R[np.ix_(T, T)], r[T])

    for C in blocks:
        for l in C:
            others = [j for j in C if j != l]
            for k in range(len(others) + 1):
                for T in itertools.combinations(others, k):
                    lr = log_m(list(T) + [l], R, r, n) - log_m(T, R, r, n)
                    x = 1.0 - rss(list(T) + [l]) / rss(T)
                    out.append(lr + 0.5 * math.log(n + 1) + nu * math.log1p(-x))
    return np.array(out)


# ---------------------------------------------------------------- exact start masses by convolution
def _lconv(a, b):
    """log-domain 2-D convolution of arrays a[k,j], b[k,j] (entries -inf allowed)."""
    K1, J1 = a.shape
    K2, J2 = b.shape
    out = np.full((K1 + K2 - 1, J1 + J2 - 1), -np.inf)
    for k in range(K2):
        for j in range(J2):
            if b[k, j] == -np.inf:
                continue
            out[k:k + K1, j:j + J1] = np.logaddexp(out[k:k + K1, j:j + J1], a + b[k, j])
    return out


def start_masses(blocks, tabs, p, n, S0, ds=(0, 1, 2)):
    """Exact log Zbar_0-normalised masses: log pi_0(S) for S=S0, and pi_0(R_d) for d in ds,
    via bivariate block profiles e_b(k, j) = sum_{|U|=k, |U minus S0|=j} r_b(U) and the capped size prior."""
    K = min(p, n // 2)
    S0 = frozenset(S0)
    acc = np.zeros((1, 1))
    for b, C in enumerate(blocks):
        prof = np.full((len(C) + 1, len(C) + 1), -np.inf)
        for U, lv in tabs[b].items():
            prof[len(U), len(U - S0)] = np.logaddexp(prof[len(U), len(U - S0)], lv)
        acc = _lconv(acc, prof)
    lw = np.array([log_w(k, p) for k in range(acc.shape[0])])
    tot = acc + lw[:, None]
    tot[K + 1:, :] = -np.inf
    lZ = np.logaddexp.reduce(tot.ravel())
    out = {}
    out["logZ0"] = lZ
    out["R"] = {d: float(np.exp(np.logaddexp.reduce(tot[:, :d + 1].ravel()) - lZ)) for d in ds}
    return out


def start_logmass(blocks, tabs, p, n, S, logZ0):
    blk = {j: b for b, C in enumerate(blocks) for j in C}
    parts = [[] for _ in blocks]
    for j in S:
        parts[blk[j]].append(j)
    return log_w(len(S), p) + sum(tabs[b][frozenset(parts[b])] for b in range(len(blocks))) - logZ0
