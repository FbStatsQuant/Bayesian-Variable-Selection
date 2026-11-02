"""
Exact small-p engine for the SMC-BVS v3 terminal round at phi = 1 (W1-T24G).

Everything is computed exactly (EX-A up to float64) by full enumeration of the 2^p models:
  - log BF(S), log prior varpi(S), F(S) = log varpi + log m  (up to the constant log m(empty));
  - blocks (complete linkage on 1-|r|, top-down cut at B, next-fit packing in leaf order),
    block tables r_b(U) = BF(U), gamma_0, pi_0, discrepancy d(S);
  - neighbour graph (threshold sqrt(2 log p / n), top-B, forced best partner, symmetric union);
  - for every state x, every label e of the round K_1, the exact transition law of e at x.

Bitmask convention: model S <-> integer sum_{j in S} 2^j (0-indexed variables).
Notation follows Docs/Theory/theorems/00_COMMON.md.
"""
import itertools, math
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.special import gammaln

A0 = B0 = 0.01


# ----------------------------------------------------------------------------- data
def scenario_cov(scen, p):
    g = np.ceil(np.arange(1, p + 1) / 5)
    H = (g[:, None] == g[None, :]).astype(float)
    I = np.eye(p)
    idx = np.arange(1, p + 1)
    if scen == 1:
        return I
    if scen == 2:
        return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if scen == 3:
        return 0.7 * H + 0.3 * I
    if scen == 4:
        return 0.85 * H + 0.15 * I
    if scen == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scen == 6:
        rho = 0.4 + 0.1 * ((g - 1) % 6)
        S = H * rho[None, :]          # R: H*matrix(rho,p,p) -> column-wise rho
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError


def truth_small(p):
    """Port of gen_dev_data.R::truth() pattern to p = 5*s0 (step = 1: one truth per group)."""
    s0 = p // 5
    pos = [3, 2, 4, 1, 5, 3]
    pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0)
    block = 1 + k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1   # 0-indexed
    beta = np.array([pattern[i % 6] for i in k])
    return active, beta


def gen_design(scen, p=20, n=200, c=1.0, seed=1):
    rng = np.random.default_rng(seed)
    Sig = scenario_cov(scen, p)
    U = np.linalg.cholesky(Sig).T                     # R's chol() is upper: Sigma = U'U
    Xr = rng.standard_normal((n, p)) @ U
    eps = rng.standard_normal(n)
    X0 = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)       # R scale(): the generator's X
    act, beta = truth_small(p)
    b = np.zeros(p); b[act] = beta
    yr = c * (X0 @ b) + eps
    # method preprocessing (00_COMMON s1): X already standardised; y = C y / s_y
    yc = yr - yr.mean()
    y = yc / np.sqrt(yc @ yc / (n - 1))
    S0 = int(sum(1 << int(j) for j in act))
    return X0, y, S0, b


# ----------------------------------------------------------------------------- scores
def popcount_array(N):
    a = np.arange(N, dtype=np.int64)
    c = np.zeros(N, dtype=np.int64)
    while a.any():
        c += a & 1
        a >>= 1
    return c


def enumerate_logbf(X, y, chunk=40000):
    """log BF(S) = log m(S) - log m(empty) for all 2^p subsets (exact formula of METHODOLOGY s5)."""
    n, p = X.shape
    G = X.T @ X
    z = X.T @ y
    yy = y @ y
    nu = A0 + n / 2
    N = 1 << p
    logm = np.empty(N)
    sizes = popcount_array(N)
    logm[0] = -nu * np.log(2 * B0 + yy)
    for k in range(1, p + 1):
        masks = np.nonzero(sizes == k)[0]
        # index lists
        bits = ((masks[:, None] >> np.arange(p)[None, :]) & 1).astype(bool)
        idx = np.nonzero(bits)[1].reshape(len(masks), k)
        for s in range(0, len(masks), chunk):
            ii = idx[s:s + chunk]
            Gs = G[ii[:, :, None], ii[:, None, :]]
            zs = z[ii]
            Hs = (n + 1) * Gs + np.eye(k)
            _, ldH = np.linalg.slogdet(Hs)
            _, ldG = np.linalg.slogdet(Gs + np.eye(k))
            sol = np.linalg.solve(Hs, zs[:, :, None])[:, :, 0]
            Q = yy - n * np.einsum('ij,ij->i', zs, sol)
            logm[masks[s:s + chunk]] = -0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)
    return logm - logm[0], sizes


def log_prior_size(p, K):
    """log w(k) - log W_K ;  w(k) = 1/(2 C(2p-1,k))."""
    k = np.arange(p + 1)
    lw = -np.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lw[k > K] = -np.inf
    lC = gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1)
    lWK = np.logaddexp.reduce((lC + lw)[k <= K])
    return lw - lWK


# ----------------------------------------------------------------------------- blocks
def make_blocks(X, B):
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    D = 1 - np.abs(R)
    np.fill_diagonal(D, 0)
    iu = np.triu_indices(p, 1)
    Zl = linkage(D[iu], method='complete')
    root = to_tree(Zl)

    def members(node):
        return sorted(node.pre_order())

    retained = []

    def cut(node):
        if node.get_count() <= B:
            retained.append(node)
            return
        kids = [node.get_left(), node.get_right()]
        kids.sort(key=lambda c: min(c.pre_order()))      # visit smallest index first
        for c in kids:
            cut(c)
    cut(root)
    # next-fit packing in dendrogram leaf order (retained clusters appear in leaf order already)
    leaf_order = root.pre_order()
    pos = {v: i for i, v in enumerate(leaf_order)}
    retained.sort(key=lambda nd: min(pos[v] for v in nd.pre_order()))
    blocks, cur = [], []
    for nd in retained:
        mem = members(nd)
        if len(cur) + len(mem) > B:
            blocks.append(cur); cur = []
        cur = cur + mem
    if cur:
        blocks.append(cur)
    return [sorted(b) for b in blocks]


def neighbour_graph(X, B):
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    rn = math.sqrt(2 * math.log(p) / n)
    N = [set() for _ in range(p)]
    for j in range(p):
        a = np.abs(R[j]).copy(); a[j] = -1
        order = sorted([l for l in range(p) if l != j], key=lambda l: (-a[l], l))
        part = [l for l in order if a[l] > rn]
        if order[0] not in part:
            part = [order[0]] + part
        part = sorted(part, key=lambda l: (-a[l], l))[:B]
        N[j].update(part)
    for j in range(p):
        for l in list(N[j]):
            N[l].add(j)
    return [sum(1 << l for l in N[j]) for j in range(p)]


# ----------------------------------------------------------------------------- model object
class Model:
    def __init__(self, X, y, S0, B=None, n_nb=None):
        self.X, self.y, self.S0 = X, y, S0
        n, p = X.shape
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        self.B = B if B is not None else min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
        self.n_nb = self.B if n_nb is None else n_nb      # number of neighbour-swap labels
        self.logbf, self.size = enumerate_logbf(X, y)
        lps = log_prior_size(p, self.K)
        self.F = lps[self.size] + self.logbf             # log gamma_1 (unnormalised posterior)
        self.logpi = self.F - np.logaddexp.reduce(self.F)
        self.blocks = make_blocks(X, self.B)
        self.bmask = [sum(1 << j for j in b) for b in self.blocks]
        idx = np.arange(1 << p, dtype=np.int64)
        tab = np.zeros(1 << p)
        for m in self.bmask:
            tab += self.logbf[idx & m]
        self.d = self.logbf - tab
        lg0 = lps[self.size] + tab
        self.logpi0 = lg0 - np.logaddexp.reduce(lg0)
        self.pi0 = np.exp(self.logpi0)
        self.Nb = neighbour_graph(X, self.B)
        self.m_labels = p + 1 + self.n_nb + 1

    # -- exact transition law of each label at state x: list of (dest, prob) incl. self-loop
    def gibbs_law(self, x, j):
        bit = 1 << j
        xp, xm = x | bit, x & ~bit
        if self.size[xp] > self.K:
            return [(xm, 1.0)]
        a, b = self.F[xp], self.F[xm]
        o = 1.0 / (1.0 + math.exp(b - a))
        return [(xp, o), (xm, 1 - o)]

    def uswap_law(self, x):
        k = int(self.size[x]); p = self.p
        if k in (0, p):
            return [(x, 1.0)]
        ins = [j for j in range(p) if x >> j & 1]
        outs = [l for l in range(p) if not x >> l & 1]
        out, stay = [], 1.0
        w = 1.0 / (k * (p - k))
        for j in ins:
            for l in outs:
                xn = (x & ~(1 << j)) | (1 << l)
                acc = min(1.0, math.exp(self.F[xn] - self.F[x]))
                out.append((xn, w * acc)); stay -= w * acc
        out.append((x, stay))
        return out

    def nswap_law(self, x):
        k = int(self.size[x])
        if k == 0:
            return [(x, 1.0)]
        ins = [j for j in range(self.p) if x >> j & 1]
        out, stay = [], 1.0
        for j in ins:
            cand = self.Nb[j] & ~x
            if cand == 0:
                continue
            ls = [l for l in range(self.p) if cand >> l & 1]
            for l in ls:
                xn = (x & ~(1 << j)) | (1 << l)
                ratio = math.exp(self.F[xn] - self.F[x]) * len(ls) / bin(self.Nb[l] & ~xn).count('1')
                pr = (1.0 / k) * (1.0 / len(ls)) * min(1.0, ratio)
                out.append((xn, pr)); stay -= pr
        out.append((x, stay))
        return out

    def ind_accept_vector(self, x):
        """pi0(S') * min(1, exp(d(S') - d(x))) for all S' (phi = 1)."""
        return self.pi0 * np.minimum(1.0, np.exp(self.d - self.d[x]))


# ----------------------------------------------------------------------------- region / potential
def region_arrays(M, d, e):
    """R_{d,e} = {U u P: U subset S0, |S0\\U| <= e, P subset S0^c, |P| <= d}; potential V."""
    p = M.p
    idx = np.arange(1 << p, dtype=np.int64)
    pc = popcount_array(1 << p)
    miss = pc[(~idx) & M.S0]
    extra = pc[idx & ~M.S0 & ((1 << p) - 1)]
    inR = (miss <= e) & (extra <= d)
    V = np.where(miss > 0, miss + d, extra)
    return inR, V, miss, extra
