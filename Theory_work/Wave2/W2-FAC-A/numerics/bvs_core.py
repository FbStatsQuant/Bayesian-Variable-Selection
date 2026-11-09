"""bvs_core.py -- exact objects of the SMC-BVS v3.1 method for ticket W1-GEN numerics.

Sources: SoP 04_theory.tex lines 69-74 (D0, score, prior, start), 02_method.tex lines 180-250, 459-510
(partition, tables, start mode, local search M 6.10, LS0).

Conventions / reading choices (recorded in SUMMARY.md):
  * score:   log m(U) = -0.5*[logdet H_U - logdet(G_U+I)] - nu*log(0.02+Q_U),  constant dropped.
  * prior:   log w(k) = -log 2 - log binom(2p-1,k); the common normaliser W_K is dropped everywhere
             (it cancels in F-comparisons and in pi_0 = gamma_0/Z_0 when Z_0 is summed with the same w).
  * ties:    "exact tie" for DP/backtracking is taken with absolute tolerance 1e-12 (production uses exact
             double equality); in local-search neighbour selection exact float equality is used.
  * partition: own complete-linkage implementation (union-lexicographic tie rule, left child = child with
             the smaller minimum index, distances tied within 1e-10); verified against scipy on random data.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import itertools
import math
from math import comb as _comb
import numpy as np
from scipy.special import gammaln, logsumexp

NEG = -np.inf


# --------------------------------------------------------------------------------------------------
# standardisation, prior, block size
# --------------------------------------------------------------------------------------------------
def standardize_X(Xr):
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(axis=0)
    nrm = np.sqrt((Xc ** 2).sum(axis=0))
    return Xc * (math.sqrt(n - 1) / nrm)


def standardize_y(yr):
    n = yr.shape[0]
    yc = yr - yr.mean()
    return yc * (math.sqrt(n - 1) / math.sqrt((yc ** 2).sum()))


def log_prior_w(p, K):
    """log w(k) = -log(2*binom(2p-1,k)), k=0..K."""
    k = np.arange(K + 1)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


def block_size(n, p):
    return min(math.isqrt(n), math.isqrt(p), 16)


def ell_cap(n, p):
    return math.ceil(math.log2(n + p + 1))


# --------------------------------------------------------------------------------------------------
# the scorer
# --------------------------------------------------------------------------------------------------
class Problem:
    """Standardised data + scorer with cache.  X: n x p (columns centred, squared norm n-1); y centred, norm^2 n-1."""

    def __init__(self, X, y, K=None):
        self.X = X
        self.y = y
        self.n, self.p = X.shape
        self.K = min(self.p, self.n // 2) if K is None else K
        self.XtX = X.T @ X
        self.Xty = X.T @ y
        self.yty = float(y @ y)
        self.nu = 0.01 + self.n / 2.0
        self.logw = log_prior_w(self.p, self.K)
        self.logm0 = -self.nu * math.log(0.02 + self.yty)
        self.cache = {(): self.logm0}

    # batch of models of equal size k>=1; idx int array (m,k)
    def logm_idx(self, idx):
        idx = np.asarray(idx)
        m, k = idx.shape
        if k == 0:
            return np.full(m, self.logm0)
        out = np.empty(m)
        chunk = max(1, int(4_000_000 // (k * k)))
        n, nu = self.n, self.nu
        eye = np.eye(k)
        for s in range(0, m, chunk):
            ii = idx[s:s + chunk]
            G = self.XtX[ii[:, :, None], ii[:, None, :]]
            z = self.Xty[ii]
            H = (n + 1.0) * G + eye
            GI = G + eye
            L1 = np.linalg.cholesky(H)
            L2 = np.linalg.cholesky(GI)
            ld1 = 2.0 * np.log(np.diagonal(L1, axis1=1, axis2=2)).sum(axis=1)
            ld2 = 2.0 * np.log(np.diagonal(L2, axis1=1, axis2=2)).sum(axis=1)
            sol = np.linalg.solve(H, z[..., None])[..., 0]
            quad = (z * sol).sum(axis=1)
            Q = self.yty - n * quad
            out[s:s + chunk] = -0.5 * (ld1 - ld2) - nu * np.log(0.02 + Q)
        return out

    def logm_many(self, models):
        """models: list of sorted tuples. Uses/updates cache."""
        res = np.empty(len(models))
        todo = {}
        for i, S in enumerate(models):
            v = self.cache.get(S)
            if v is None:
                todo.setdefault(len(S), []).append(i)
            else:
                res[i] = v
        for k, ids in todo.items():
            idx = np.array([models[i] for i in ids], dtype=np.int64).reshape(len(ids), k)
            vals = self.logm_idx(idx)
            for i, v in zip(ids, vals):
                res[i] = v
                self.cache[models[i]] = v
        return res

    def logm(self, S):
        return float(self.logm_many([tuple(S)])[0])

    def F(self, S):
        S = tuple(S)
        return float(self.logw[len(S)] + self.logm(S))

    def F_many(self, models):
        lw = self.logw[np.fromiter((len(S) for S in models), dtype=np.int64, count=len(models))]
        return lw + self.logm_many(models)


def direct_logm(X, y, U):
    """Independent re-implementation (E1): Gaussian-integral form with n x n matrices.
    beta|s2 ~ N(0, s2 * n (G+I)^-1) (i.e. g=n, tau=1), sigma2 ~ IG(.01,.01); returns log m(U) up to the same
    additive constant as Problem.logm (only differences log m(U)-log m(empty) are comparable)."""
    n = X.shape[0]
    U = list(U)
    if len(U) == 0:
        Sy = np.eye(n)
    else:
        XU = X[:, U]
        G = XU.T @ XU
        Aprec = (G + np.eye(len(U))) / n  # prior precision / s2
        Sy = np.eye(n) + XU @ np.linalg.inv(Aprec) @ XU.T
    sign, ld = np.linalg.slogdet(Sy)
    q = float(y @ np.linalg.solve(Sy, y))
    nu = 0.01 + n / 2.0
    return -0.5 * ld - nu * math.log(0.01 + 0.5 * q)


# --------------------------------------------------------------------------------------------------
# partition: complete linkage on 1-|r| (own implementation with explicit tie rule)
# --------------------------------------------------------------------------------------------------
def complete_linkage(R, tie_tol=1e-10):
    """Returns (root_id, children dict, members dict, heights dict). Leaves are 0..p-1."""
    p = R.shape[0]
    D = 1.0 - np.abs(R)
    D = np.clip(D, 0.0, None)
    np.fill_diagonal(D, np.inf)
    members = {i: (i,) for i in range(p)}
    children = {}
    heights = {}
    nodeid = list(range(p))
    mn = np.arange(p)
    nxt = p
    for _ in range(p - 1):
        dmin = D.min()
        ii, jj = np.nonzero(D <= dmin + tie_tol)
        keep = ii < jj
        ii, jj = ii[keep], jj[keep]
        if len(ii) > 1:
            m = np.minimum(mn[ii], mn[jj])
            sel = m == m.min()
            ii, jj = ii[sel], jj[sel]
            if len(ii) > 1:
                keys = [tuple(sorted(members[nodeid[i]] + members[nodeid[j]])) for i, j in zip(ii, jj)]
                kbest = min(range(len(keys)), key=lambda t: keys[t])
                ii, jj = ii[kbest:kbest + 1], jj[kbest:kbest + 1]
        i, j = int(ii[0]), int(jj[0])
        a, b = nodeid[i], nodeid[j]
        left, right = (a, b) if min(members[a]) < min(members[b]) else (b, a)
        members[nxt] = tuple(sorted(members[a] + members[b]))
        children[nxt] = (left, right)
        heights[nxt] = float(D[i, j])
        newrow = np.maximum(D[i], D[j])
        newrow[i] = np.inf
        newrow[j] = np.inf
        D[i, :] = newrow
        D[:, i] = newrow
        D[j, :] = np.inf
        D[:, j] = np.inf
        nodeid[i] = nxt
        mn[i] = min(mn[i], mn[j])
        nxt += 1
    return nxt - 1, children, members, heights


def partition_from_corr(R, B):
    """Top-down cut at B + next-fit packing in dendrogram leaf order. Returns list of sorted index lists."""
    p = R.shape[0]
    if p == 1:
        return [[0]]
    root, children, members, _ = complete_linkage(R)
    clusters = []
    stack = [root]
    while stack:
        nd = stack.pop()
        if len(members[nd]) <= B:
            clusters.append(list(members[nd]))
        else:
            l, r = children[nd]
            stack.append(r)
            stack.append(l)
    blocks, cur = [], []
    for cl in clusters:
        if len(cur) + len(cl) <= B:
            cur = cur + cl
        else:
            blocks.append(sorted(cur))
            cur = list(cl)
    if cur:
        blocks.append(sorted(cur))
    return blocks


def partition(X, B=None):
    n, p = X.shape
    if B is None:
        B = block_size(n, p)
    R = X.T @ X / (n - 1.0)
    return partition_from_corr(R, B)


def same_partition(blocks, groups):
    return sorted(tuple(sorted(b)) for b in blocks) == sorted(tuple(sorted(g)) for g in groups)


# --------------------------------------------------------------------------------------------------
# tables, start weight, start mode, normaliser
# --------------------------------------------------------------------------------------------------
def block_tables(prob, blocks):
    """tabs[b][k] = (idx (m_k,k) global index rows in lexicographic order, logr (m_k,)), r_b = m(U)/m(empty)."""
    tabs = []
    for C in blocks:
        Carr = np.array(C, dtype=np.int64)
        m = len(C)
        d = {0: (np.zeros((1, 0), dtype=np.int64), np.array([0.0]))}
        for k in range(1, min(m, prob.K) + 1):
            comb = np.array(list(itertools.combinations(range(m), k)), dtype=np.int64)
            idx = Carr[comb]
            lm = prob.logm_idx(idx)
            d[k] = (idx, lm - prob.logm0)
        tabs.append(d)
    return tabs


def block_id_array(blocks, p):
    bid = np.full(p, -1, dtype=np.int64)
    for b, C in enumerate(blocks):
        bid[list(C)] = b
    return bid


def log_gamma0(prob, blocks, S, bid=None):
    S = tuple(sorted(S))
    if bid is None:
        bid = block_id_array(blocks, prob.p)
    parts = {}
    for j in S:
        parts.setdefault(int(bid[j]), []).append(j)
    tot = float(prob.logw[len(S)])
    for b, U in parts.items():
        tot += prob.logm(tuple(U)) - prob.logm0
    return tot


class StartInfo:
    pass


def start_mode(prob, blocks, tabs=None, tie_tol=1e-12, enum_cap=20000):
    """Block DP: per-block per-size maxima, max-plus convolution over blocks, size prior.
    Ties: smallest size, then lexicographically smallest sorted index list (enumeration capped).
    Also log Z_0 = log sum_{|S|<=K} gamma_0(S) by log-sum-exp convolution of block size profiles."""
    if tabs is None:
        tabs = block_tables(prob, blocks)
    K = prob.K
    J = len(blocks)
    Mmax = np.full((J, K + 1), NEG)
    E = np.full((J, K + 1), NEG)
    ties = []
    for b in range(J):
        tb = {}
        for k, (idx, lr) in tabs[b].items():
            if k > K:
                continue
            mx = float(lr.max())
            Mmax[b, k] = mx
            E[b, k] = float(logsumexp(lr))
            sel = np.flatnonzero(lr >= mx - tie_tol)
            tb[k] = [tuple(int(v) for v in idx[i]) for i in sel[:enum_cap]]
        ties.append(tb)
    Fm = np.full((J + 1, K + 1), NEG)
    LF = np.full((J + 1, K + 1), NEG)
    Fm[0, 0] = 0.0
    LF[0, 0] = 0.0
    for b in range(J):
        for j in range(0, K + 1):
            if not np.isfinite(Mmax[b, j]):
                continue
            cand = Mmax[b, j] + Fm[b, :K + 1 - j]
            Fm[b + 1, j:] = np.maximum(Fm[b + 1, j:], cand)
            LF[b + 1, j:] = np.logaddexp(LF[b + 1, j:], E[b, j] + LF[b, :K + 1 - j])
    vals = prob.logw + Fm[J]
    best_k, best_v = None, NEG
    for k in range(K + 1):
        if vals[k] > best_v:
            best_k, best_v = k, vals[k]
    # enumerate all optimal choices (within tie_tol) and take lexicographically smallest union
    trunc = [False]
    count = [0]

    def rec(b, r, acc):
        if b < 0:
            if r == 0:
                yield acc
            return
        target = Fm[b + 1, r]
        for j in range(0, min(r, K) + 1):
            if not np.isfinite(Mmax[b, j]) or not np.isfinite(Fm[b, r - j]):
                continue
            if abs(Mmax[b, j] + Fm[b, r - j] - target) <= tie_tol:
                for U in ties[b].get(j, []):
                    for res in rec(b - 1, r - j, acc + U):
                        yield res

    bestset = None
    for acc in rec(J - 1, best_k, ()):
        s = tuple(sorted(acc))
        if bestset is None or s < bestset:
            bestset = s
        count[0] += 1
        if count[0] >= enum_cap:
            trunc[0] = True
            break
    info = StartInfo()
    info.mode = bestset
    info.size = best_k
    info.logZ0 = float(logsumexp(prob.logw + LF[J]))
    info.log_gamma0_mode = float(best_v)
    info.n_optimal = count[0]
    info.truncated = trunc[0]
    info.tabs = tabs
    info.blocks = blocks
    info.bid = block_id_array(blocks, prob.p)
    return info


def log_pi0(prob, info, S):
    return log_gamma0(prob, info.blocks, S, info.bid) - info.logZ0


# --------------------------------------------------------------------------------------------------
# production local search (M 6.10)
# --------------------------------------------------------------------------------------------------
def neighbours(S, p, K):
    S = tuple(S)
    Sset = set(S)
    out = [j for j in range(p) if j not in Sset]
    res = []
    if len(S) < K:
        for j in out:
            lst = list(S)
            # insertion keeping sort
            pos = 0
            while pos < len(lst) and lst[pos] < j:
                pos += 1
            lst.insert(pos, j)
            res.append(tuple(lst))
    for i in range(len(S)):
        res.append(S[:i] + S[i + 1:])
    for i in range(len(S)):
        base = S[:i] + S[i + 1:]
        for j in out:
            pos = 0
            while pos < len(base) and base[pos] < j:
                pos += 1
            res.append(base[:pos] + (j,) + base[pos:])
    return res


def local_search(prob, centre, ell):
    S = tuple(sorted(centre))
    prob.F(S)
    scored = {S}
    path = [S]
    moves = 0
    certified = False
    local_limit = False
    first_move = None
    while True:
        nb = neighbours(S, prob.p, prob.K)
        Fv = prob.F_many(nb) if nb else np.array([])
        scored.update(nb)
        FS = prob.F(S)
        mx = float(Fv.max()) if len(nb) else NEG
        if mx > FS:
            if moves >= ell:
                local_limit = True
                break
            cands = [nb[i] for i in np.flatnonzero(Fv == mx)]
            nxt = min(cands)
            if first_move is None:
                first_move = (S, nxt)
            S = nxt
            moves += 1
            path.append(S)
        else:
            certified = True
            break
    return dict(path=path, final=S, scored=scored, moves=moves, certified=certified,
                local_limit=local_limit, first_move=first_move)


def hpm_of(prob, scored):
    best, bf = None, NEG
    for S in scored:
        f = prob.F(S)
        if best is None or f > bf or (f == bf and (len(S), S) < (len(best), best)):
            best, bf = S, f
    return best


# --------------------------------------------------------------------------------------------------
# design generators
# --------------------------------------------------------------------------------------------------
def exact_gram_design(Sigma, n, rng):
    """X with centred columns and X'X = (n-1) Sigma exactly (needs p <= n-1)."""
    p = Sigma.shape[0]
    assert p <= n - 1, "exact Gram needs p <= n-1"
    Z = rng.standard_normal((n, p))
    Z -= Z.mean(axis=0)
    Q, _ = np.linalg.qr(Z)
    L = np.linalg.cholesky(Sigma)
    return math.sqrt(n - 1.0) * Q @ L.T


def iid_design_raw(Sigma, n, rng):
    L = np.linalg.cholesky(Sigma)
    return rng.standard_normal((n, Sigma.shape[0])) @ L.T


def make_y_std(X, theta, sigma, rng):
    """y = X theta + sigma*eps (X standardised), then centred/scaled to squared norm n-1."""
    n = X.shape[0]
    return standardize_y(X @ theta + sigma * rng.standard_normal(n))


def lh_sigma(G, g, rho, psis, nvis=0):
    """LH population correlation: G groups of size g, equicorrelation rho, c=len(psis) linked pairs
    (groups 2i, 2i+1, 0-based), then nvis visible groups. Hubs = first member of each group.
    Cross block: Sigma[C_a,C_b] = psi * Sigma[C_a,j_a] Sigma[j_b,C_b]."""
    p = G * g
    Sg = (1 - rho) * np.eye(g) + rho * np.ones((g, g))
    Sigma = np.zeros((p, p))
    groups = [tuple(range(h * g, (h + 1) * g)) for h in range(G)]
    for h in range(G):
        Sigma[h * g:(h + 1) * g, h * g:(h + 1) * g] = Sg
    c = len(psis)
    for i, psi in enumerate(psis):
        a, b = 2 * i, 2 * i + 1
        blk = psi * np.outer(Sg[:, 0], Sg[0, :])
        Sigma[a * g:(a + 1) * g, b * g:(b + 1) * g] = blk
        Sigma[b * g:(b + 1) * g, a * g:(a + 1) * g] = blk.T
    info = dict(groups=groups, a_hubs=[groups[2 * i][0] for i in range(c)],
                b_hubs=[groups[2 * i + 1][0] for i in range(c)],
                vis_hubs=[groups[2 * c + v][0] for v in range(nvis)],
                signal_groups=[groups[h] for h in range(2 * c + nvis)])
    return Sigma, info


def lh_theta(p, info, psis, betas, beta_vis):
    th = np.zeros(p)
    for i, (a, b) in enumerate(zip(info["a_hubs"], info["b_hubs"])):
        th[a] = betas[i]
        th[b] = -psis[i] * betas[i]
    for h in info["vis_hubs"]:
        th[h] = beta_vis
    return th


# --------------------------------------------------------------------------------------------------
# population helpers
# --------------------------------------------------------------------------------------------------
def _solve(A, B):
    try:
        return np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        return np.linalg.lstsq(A, B, rcond=None)[0] if A.ndim == 2 else np.stack(
            [np.linalg.lstsq(A[i], B[i], rcond=None)[0] for i in range(A.shape[0])])


class Pop:
    """Population (or exact-design) geometry.  Lambda_T = ||(I-P_T) mu||^2 = (n-1) theta'[Sigma - Sigma_.T Sigma_TT^-1 Sigma_T.]theta.
    For an exact design X use Pop.from_design(X, theta): Sigma := X'X/(n-1)."""

    def __init__(self, Sigma, theta, n, sigma2=1.0):
        self.Sigma = np.asarray(Sigma, dtype=float)
        self.theta = np.asarray(theta, dtype=float)
        self.n = n
        self.sigma2 = sigma2
        self.p = self.Sigma.shape[0]
        self.c = self.Sigma @ self.theta
        self.muvar = float(self.theta @ self.c)
        self.S0 = tuple(int(j) for j in np.flatnonzero(self.theta != 0))
        self.theta_min = float(np.min(np.abs(self.theta[list(self.S0)]))) if self.S0 else float("nan")
        self.logn = math.log(n)

    @classmethod
    def from_design(cls, X, theta, sigma2=1.0):
        n = X.shape[0]
        return cls(X.T @ X / (n - 1.0), theta, n, sigma2)

    def lam_unit_idx(self, idx):
        idx = np.asarray(idx)
        m, k = idx.shape
        if k == 0:
            return np.full(m, self.muvar)
        out = np.empty(m)
        chunk = max(1, int(3_000_000 // (k * k)))
        for s in range(0, m, chunk):
            ii = idx[s:s + chunk]
            SS = self.Sigma[ii[:, :, None], ii[:, None, :]]
            cT = self.c[ii]
            sol = _solve(SS, cT[..., None])[..., 0]
            out[s:s + chunk] = self.muvar - (cT * sol).sum(axis=1)
        return np.maximum(out, 0.0)

    def lam(self, T):
        T = tuple(sorted(T))
        return (self.n - 1.0) * float(self.lam_unit_idx(np.array(T, dtype=np.int64).reshape(1, len(T)))[0])

    def lam_table(self, C):
        """Array over bitmasks of positions in block C (sorted): Lambda_U."""
        m = len(C)
        Carr = np.array(C, dtype=np.int64)
        tab = np.empty(1 << m)
        for k in range(0, m + 1):
            if k == 0:
                tab[0] = (self.n - 1.0) * self.muvar
                continue
            comb = np.array(list(itertools.combinations(range(m), k)), dtype=np.int64)
            masks = (1 << comb).sum(axis=1)
            tab[masks] = (self.n - 1.0) * self.lam_unit_idx(Carr[comb])
        return tab

    # ---- block quantities --------------------------------------------------------------------
    def block_minimisers(self, blocks, tol=1e-7):
        """U*_b: smallest-size then lex minimiser of Lambda_U over U subset C_b (absolute tolerance tol)."""
        Us, tabs = [], []
        for C in blocks:
            m = len(C)
            tab = self.lam_table(C)
            tabs.append(tab)
            cand = np.flatnonzero(tab <= tab.min() + tol)
            best = None
            for mk in cand:
                pos = tuple(i for i in range(m) if (mk >> i) & 1)
                key = (len(pos), pos)
                if best is None or key < best:
                    best = key
            Us.append(tuple(C[i] for i in best[1]))
        self._tabs = tabs
        return Us

    def vis_margin(self, blocks, Ustar):
        """min over (b,U), U*_b not subset U, of g_{b,U}/(v_U log n);  g=Lambda_U-Lambda_{U u U*_b}, v_U=sigma2+Lambda_U/(n-1)."""
        best, arg = np.inf, None
        for b, C in enumerate(blocks):
            tab = self._tabs[b]
            m = len(C)
            u = sum(1 << C.index(j) for j in Ustar[b])
            masks = np.arange(1 << m)
            sel = masks[(masks & u) != u]
            if len(sel) == 0:
                continue
            g = tab[sel] - tab[sel | u]
            v = self.sigma2 + tab[sel] / (self.n - 1.0)
            r = g / (v * self.logn)
            i = int(np.argmin(r))
            if r[i] < best:
                best = float(r[i])
                arg = (b, tuple(C[q] for q in range(m) if (sel[i] >> q) & 1), Ustar[b])
        return best, arg

    def nl_leak(self, blocks, Ustar):
        """max over l in C_b\\U*_b, U*_b subset T subset C_b\\{l} of delta^2_{T,l}/(sigma2 log n)."""
        best, arg = 0.0, None
        for b, C in enumerate(blocks):
            tab = self._tabs[b]
            m = len(C)
            u = sum(1 << C.index(j) for j in Ustar[b])
            masks = np.arange(1 << m)
            for q in range(m):
                if (u >> q) & 1:
                    continue
                sel = masks[((masks & u) == u) & (((masks >> q) & 1) == 0)]
                d2 = tab[sel] - tab[sel | (1 << q)]
                i = int(np.argmax(d2))
                r = d2[i] / (self.sigma2 * self.logn)
                if r > best:
                    best = float(r)
                    arg = (b, C[q], tuple(C[t] for t in range(m) if (sel[i] >> t) & 1))
        return best, arg

    # ---- SEP and Lemma-3 decrement ---------------------------------------------------------------
    def sweep(self, V, subsets_by_size, S0=None):
        """For S in the given family (subsets of V): zeta = max_{S,l not in V}(Lambda_S-Lambda_{S+l}); and
        dec = min_{S not superset S0} max_{j in S0\\S}(Lambda_S-Lambda_{S+j}).  Units: Lambda (scaled by n-1)."""
        S0 = self.S0 if S0 is None else tuple(S0)
        Vset = set(V)
        out_idx = np.array([j for j in range(self.p) if j not in Vset], dtype=np.int64)
        tgt = np.concatenate([out_idx, np.array(S0, dtype=np.int64)])
        nout = len(out_idx)
        q = len(tgt)
        Sig, c = self.Sigma, self.c
        bvar = np.diag(Sig)[tgt]
        ct = c[tgt]
        zeta, argz = 0.0, None
        dec, argd = np.inf, None
        s0mask_cols = np.arange(q) >= nout
        for k, combos in subsets_by_size:
            m_all = len(combos)
            chunk = max(1, int(2_000_000 // max(1, k * q + k * k)))
            for s in range(0, m_all, chunk):
                cm = np.asarray(combos[s:s + chunk], dtype=np.int64)
                if k == 0:
                    cm = np.zeros((1, 0), dtype=np.int64)
                m = len(cm)
                if k == 0:
                    d = ct[None, :] ** 2 / bvar[None, :]
                    d = np.repeat(d, m, axis=0)
                    inS = np.zeros((m, q), dtype=bool)
                else:
                    SS = Sig[cm[:, :, None], cm[:, None, :]]
                    ST = Sig[cm[:, :, None], tgt[None, None, :]]
                    cS = c[cm]
                    rhs = np.concatenate([ST, cS[..., None]], axis=2)
                    sol = _solve(SS, rhs)
                    A = sol[:, :, :q]
                    w = sol[:, :, q]
                    num = ct[None, :] - np.einsum("mkq,mk->mq", ST, w)
                    den = bvar[None, :] - np.einsum("mkq,mkq->mq", ST, A)
                    inS = (cm[:, :, None] == tgt[None, None, :]).any(axis=1)
                    den = np.where(den < 1e-12, np.inf, den)
                    d = num ** 2 / den
                d = d * (self.n - 1.0)
                # SEP
                if nout:
                    dz = d[:, :nout]
                    i = np.unravel_index(int(np.argmax(dz)), dz.shape)
                    if dz[i] > zeta:
                        zeta = float(dz[i])
                        argz = (tuple(int(t) for t in cm[i[0]]), int(out_idx[i[1]]))
                # decrement: S must miss at least one truth
                if len(S0):
                    miss = ~inS[:, nout:]
                    anymiss = miss.any(axis=1)
                    if anymiss.any():
                        dd = np.where(miss, d[:, nout:], -np.inf).max(axis=1)
                        dd = np.where(anymiss, dd, np.inf)
                        i = int(np.argmin(dd))
                        if dd[i] < dec:
                            dec = float(dd[i])
                            argd = tuple(int(t) for t in cm[i])
        return dict(zeta=zeta, zeta_arg=argz, dec=dec, dec_arg=argd)


def all_subsets_by_size(V, kmax=None):
    V = sorted(V)
    kmax = len(V) if kmax is None else kmax
    res = []
    for k in range(0, kmax + 1):
        if k == 0:
            res.append((0, np.zeros((1, 0), dtype=np.int64)))
        else:
            res.append((k, np.array(list(itertools.combinations(V, k)), dtype=np.int64)))
    return res


def restricted_subsets_by_size(V, S0, rng, n_random=3000, extras=2, small=3):
    """Family used when |V| is too large for exhaustive enumeration: all S with |S \\ S0| <= extras,
    all S with |S| <= small, plus n_random random subsets."""
    V = sorted(V)
    S0 = sorted(S0)
    rest = [j for j in V if j not in set(S0)]
    fam = set()
    for r in range(len(S0) + 1):
        for A in itertools.combinations(S0, r):
            for e in range(extras + 1):
                for B in itertools.combinations(rest, e):
                    fam.add(tuple(sorted(A + B)))
    for k in range(small + 1):
        for A in itertools.combinations(V, k):
            fam.add(A)
    for _ in range(n_random):
        k = int(rng.integers(0, min(len(V), 14) + 1))
        fam.add(tuple(sorted(rng.choice(V, size=k, replace=False).tolist())))
    by = {}
    for S in fam:
        by.setdefault(len(S), []).append(S)
    return [(k, np.array(v, dtype=np.int64).reshape(len(v), k)) for k, v in sorted(by.items())]


def sep_and_decrement(pop, V, rng=None, exhaustive_max=20, S0=None):
    """Compute (zeta, Lemma-3 decrement) over S subset V.  Exhaustive if |V|<=exhaustive_max, else restricted family
    (then zeta is a lower bound and dec an upper bound of the true values)."""
    S0 = pop.S0 if S0 is None else tuple(S0)
    if len(V) <= exhaustive_max:
        fam = all_subsets_by_size(V)
        exh = True
    else:
        rng = np.random.default_rng(0) if rng is None else rng
        fam = restricted_subsets_by_size(V, S0, rng)
        exh = False
    r = pop.sweep(V, fam, S0)
    r["exhaustive"] = exh
    r["zeta_ratio"] = r["zeta"] / (pop.n * pop.theta_min ** 2)
    return r
