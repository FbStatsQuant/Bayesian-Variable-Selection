"""O-WSTAB core: exact start law pi0, posterior pi, discrepancy d and every bridge divergence, for p <= 20.

Objects follow 00_COMMON.md / METHODOLOGY_v3.md §5-§6.3 exactly (standardised data, g = n, unit ridge,
IG(0.01, 0.01), BB(1,p) capped at K = min(p, floor(n/2)), tables r_b(U) = BF(U), gamma_0 = varpi * prod_b r_b).
Partition: port of v3_blocks.h (complete linkage on 1-|r|, R13 ties, top-down cut, next-fit packing), copied from
W1-EXP scripts/bvs_exact.py (theory/W1-EXP), which checked it against the C++ engine.

Everything is computed on sufficient statistics (R = X'X/(n-1), r = X'y/(n-1), y'y = n-1), so n can be huge.
Models are bitmasks; all 2^p models with |S| <= K are enumerated.  Python 3 + numpy only.
"""
import itertools
import math

import numpy as np

A0 = 0.01
B0 = 0.01


def lse(v):
    v = np.asarray(v, float)
    m = np.max(v)
    if not np.isfinite(m):
        return m
    return float(m + np.log(np.sum(np.exp(v - m))))


def lgamma(x):
    return math.lgamma(x)


def log_w(k, p):
    """log w(k) = log(1 / (2 binom(2p-1, k)))."""
    return -math.log(2.0) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k))


# ------------------------------------------------------------------ partition (port, see docstring)
def complete_linkage(Rc):
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


def _leaves(left, right, nd, p):
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
            clusters.append(_leaves(left, right, x, p))
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


# ------------------------------------------------------------------ scores
def score_parts(models, R, r, n):
    """For an int array of models (N, k): returns (logdetD, t) with D_S = det H_S / det(G_S + I),
    t_S = n z_S' H_S^{-1} z_S on the standardised data (G = (n-1) R_S, z = (n-1) r_S)."""
    models = np.asarray(models)
    N, k = models.shape
    if k == 0:
        return np.zeros(N), np.zeros(N)
    RS = R[models[:, :, None], models[:, None, :]]
    rS = r[models]
    I = np.eye(k)[None]
    H = (n + 1.0) * (n - 1.0) * RS + I
    G1 = (n - 1.0) * RS + I
    _, ldH = np.linalg.slogdet(H)
    _, ldG = np.linalg.slogdet(G1)
    z = (n - 1.0) * rS
    sol = np.linalg.solve(H, z[:, :, None])[:, :, 0]
    t = n * np.einsum("ij,ij->i", z, sol)
    return ldH - ldG, t


def log_bf_from_parts(ldD, t, n):
    """log BF(S) = -1/2 log D_S - nu log(1 - t_S/(2b0 + y'y)), y'y = n - 1."""
    nu = A0 + n / 2.0
    Q0 = 2 * B0 + (n - 1.0)
    return -0.5 * ldD - nu * np.log1p(-t / Q0)


class Space:
    """All models |S| <= K as bitmasks, with sizes."""

    def __init__(self, p, K):
        self.p, self.K = p, K
        masks, sizes, combos = [], [], []
        for k in range(K + 1):
            cs = list(itertools.combinations(range(p), k))
            combos.append(np.array(cs, dtype=int).reshape(len(cs), k))
            for c in cs:
                m = 0
                for j in c:
                    m |= 1 << j
                masks.append(m)
                sizes.append(k)
        self.masks = np.array(masks, dtype=np.int64)
        self.sizes = np.array(sizes, dtype=int)
        self.combos = combos
        self.index = {int(m): i for i, m in enumerate(self.masks)}

    def idx(self, S):
        m = 0
        for j in S:
            m |= 1 << int(j)
        return self.index[m]


def all_scores(space, R, r, n, chunk=40000):
    """(logdetD, t) for every model in the space (order of space.masks)."""
    ldD, tt = [], []
    for k, cs in enumerate(space.combos):
        if k == 0:
            ldD.append(np.zeros(1))
            tt.append(np.zeros(1))
            continue
        for s in range(0, len(cs), chunk):
            a, b = score_parts(cs[s:s + chunk], R, r, n)
            ldD.append(a)
            tt.append(b)
    return np.concatenate(ldD), np.concatenate(tt)


def block_local_index(space, C):
    """For block C (list of columns), the local subset index of S cap C for every model."""
    loc = np.zeros(len(space.masks), dtype=np.int64)
    for i, j in enumerate(C):
        loc |= ((space.masks >> j) & 1) << i
    return loc


class Problem:
    """Exact start/posterior/bridge objects for one data set (sufficient statistics)."""

    def __init__(self, R, r, n, blocks=None, space=None):
        p = R.shape[0]
        self.R, self.r, self.n, self.p = R, r, n, p
        self.K = min(p, n // 2)
        self.space = space if space is not None else Space(p, self.K)
        assert self.space.K == self.K and self.space.p == p
        self.B = block_size_B(n, p)
        self.blocks = blocks if blocks is not None else make_blocks(R, self.B)
        self.ldD, self.t = all_scores(self.space, R, r, n)
        self.logbf = log_bf_from_parts(self.ldD, self.t, n)
        self.lw = np.array([log_w(k, p) for k in range(self.K + 1)])[self.space.sizes]
        # block tables r_b(U) = BF(U), U subset C_b, and their per-model lookups
        self.logr_blocks, self.locs, self.t_blocks = [], [], []
        tot = np.zeros(len(self.space.masks))
        for C in self.blocks:
            m = len(C)
            ldDb, tb, lrb = np.zeros(2 ** m), np.zeros(2 ** m), np.zeros(2 ** m)
            for k in range(1, m + 1):
                for U in itertools.combinations(range(m), k):
                    li = sum(1 << i for i in U)
                    a, b = score_parts(np.array([[C[i] for i in U]]), R, r, n)
                    ldDb[li], tb[li] = a[0], b[0]
            lrb = log_bf_from_parts(ldDb, tb, n)
            loc = block_local_index(self.space, C)
            self.logr_blocks.append(lrb)
            self.locs.append(loc)
            self.t_blocks.append(tb[loc])
            tot += lrb[loc]
        self.sumlogr = tot
        self.lg0 = self.lw + tot          # log gamma_0 up to the constant W_K (cancels)
        self.d = self.logbf - tot         # discrepancy d(S)
        self.lZ0 = lse(self.lg0)

    # ---- bridge
    def Lam(self, phi):
        """Lambda(phi) = log Zbar_phi / Zbar_0 = log E_{pi0} e^{phi d}."""
        return lse(self.lg0 + phi * self.d) - self.lZ0

    def logq(self, phi):
        v = self.lg0 + phi * self.d
        return v - lse(v)

    def chi2(self, u, v):
        w = 2 * v - u
        return math.expm1(self.Lam(w) - 2 * self.Lam(v) + self.Lam(u))

    def log1pchi2(self, u, v):
        w = 2 * v - u
        return self.Lam(w) - 2 * self.Lam(v) + self.Lam(u)

    def kl(self, v, u):
        """KL(q_v || q_u)."""
        lqv = self.logq(v)
        Ed = float(np.sum(np.exp(lqv) * self.d))
        return (v - u) * Ed - self.Lam(v) + self.Lam(u)

    def renyi(self, alpha, v, u):
        """Renyi divergence D_alpha(q_v || q_u), alpha != 1."""
        a = u + alpha * (v - u)
        return (self.Lam(a) - alpha * self.Lam(v) + (alpha - 1) * self.Lam(u)) / (alpha - 1)

    def tv(self, u, v):
        return 0.5 * float(np.sum(np.abs(np.exp(self.logq(u)) - np.exp(self.logq(v)))))

    def var_d(self, phi):
        q = np.exp(self.logq(phi))
        m = float(np.sum(q * self.d))
        return float(np.sum(q * (self.d - m) ** 2))

    def mass(self, phi, S):
        return math.exp(self.logq(phi)[self.space.idx(S)])


# ------------------------------------------------------------------ data generators (sufficient statistics)
def suff_exact_gram(Sigma, theta, n, sigma, rng):
    """Fixed design with X'X = (n-1) Sigma exactly (Sigma a correlation matrix, p <= n-1); y = X theta + eps.
    Returns (R, r, extras) for the standardised response.  Simulates X'eps = sigma sqrt(n-1) L xi and
    ||eps_perp||^2 = sigma^2 chi^2_{n-1-p} exactly (as in W1-EXP family.py).  extras holds raw-scale
    quantities: XtMu = X'mu, mumu = ||mu||^2, Xteps, s_y."""
    p = Sigma.shape[0]
    assert p <= n - 1
    L = np.linalg.cholesky(Sigma)
    xi = rng.standard_normal(p)
    chi = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
    Xteps = sigma * math.sqrt(n - 1) * (L @ xi)
    XtMu = (n - 1) * Sigma @ theta
    mumu = (n - 1) * theta @ Sigma @ theta
    # eps in span(X): coordinates; ||P_X eps||^2 = sigma^2 xi'xi
    YtY = mumu + 2 * sigma * math.sqrt(n - 1) * theta @ L @ xi + sigma ** 2 * (xi @ xi + chi)
    sy = math.sqrt(YtY / (n - 1))
    r = (XtMu + Xteps) / ((n - 1) * sy)
    return Sigma.copy(), r, dict(XtMu=XtMu, mumu=mumu, Xteps=Xteps, sy=sy, YtY=YtY)


def gen_random_design(Sigma, beta, n, sigma, rng, scale=1.0):
    """Study-style data (gen_dev_data.R): raw rows ~ N(0, Sigma); X = scale(raw) (sd with n-1);
    signal = X beta (standardised X); y = scale*signal + eps.  Returns (R, r, extras) with X'mu exact."""
    p = Sigma.shape[0]
    L = np.linalg.cholesky(Sigma)
    raw = rng.standard_normal((n, p)) @ L.T
    X = raw - raw.mean(0)
    X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    mu = scale * (X @ beta)
    eps = sigma * rng.standard_normal(n)
    Y = mu + eps
    Y = Y - Y.mean()
    sy = math.sqrt(Y @ Y / (n - 1))
    R = X.T @ X / (n - 1)
    r = X.T @ Y / ((n - 1) * sy)
    mu_c = mu - mu.mean()
    return R, r, dict(XtMu=X.T @ mu_c, mumu=float(mu_c @ mu_c), sy=sy, X=X, mu=mu_c, theta=scale * beta)


# ------------------------------------------------------------------ leakage quantities (WS5)
def leakage(blocks, R, theta, S0, n):
    """Effective block coefficients and leakage remainders, on the standardised-X scale with mu = X theta
    and X'X = (n-1) R (exact for exact-Gram designs and for gen_random_design's X).
    For each block b: U* = S0 cap C_b, alpha_b = G_{U*}^{-1} X_{U*}' mu_{-b}, theta_tilde = theta_{U*} + alpha_b,
    Lambda_b = ||(P_{C_b} - P_{U*}) mu_{-b}||^2, kappa_b = ||P_{C_b} mu_{-b}||^2.  Returned per (n-1)."""
    S0 = list(S0)
    out = []
    for C in blocks:
        U = [j for j in C if j in S0]
        other = [j for j in S0 if j not in C]
        th_o = theta[other]
        # Gram blocks (per n-1)
        RCo = R[np.ix_(C, other)] @ th_o if other else np.zeros(len(C))   # X_C' mu_-b / (n-1)
        kap = float(RCo @ np.linalg.solve(R[np.ix_(C, C)], RCo)) if other else 0.0
        if U:
            RUo = R[np.ix_(U, other)] @ th_o if other else np.zeros(len(U))
            alpha = np.linalg.solve(R[np.ix_(U, U)], RUo)
            projU = float(RUo @ alpha)
            tt = theta[U] + alpha
        else:
            alpha, projU, tt = np.zeros(0), 0.0, np.zeros(0)
        out.append(dict(block=C, U=U, alpha=alpha.tolist(), theta_tilde=tt.tolist(),
                        Lambda=kap - projU, kappa=kap))
    return out


def cross_eps(R, blocks, S):
    """eps_S = || A^{-1/2} E A^{-1/2} ||_op for the standardised cross-block Gram of model S (WS4)."""
    S = sorted(S)
    if len(S) <= 1:
        return 0.0
    blk = {j: b for b, C in enumerate(blocks) for j in C}
    RS = R[np.ix_(S, S)]
    A = np.zeros_like(RS)
    for i, a in enumerate(S):
        for k, b in enumerate(S):
            if blk[a] == blk[b]:
                A[i, k] = RS[i, k]
    E = RS - A
    w, V = np.linalg.eigh(A)
    Ais = V @ np.diag(w ** -0.5) @ V.T
    return float(np.max(np.abs(np.linalg.eigvalsh(Ais @ E @ Ais))))
