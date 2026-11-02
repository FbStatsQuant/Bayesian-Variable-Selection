"""W5-VMASK independent core library.

Written from 00_COMMON.md, METHODOLOGY_v3 and the C++ engine (v3_blocks.h, v3_start.h, v3_engine.h::local_search).
No code from W3-PXN, W4-T38FULL or W1-* is imported or copied.

Contents
  standardise(Xr, yr)                    -> X, y with ||x_j||^2 = ||y||^2 = n-1 (00_COMMON §1)
  Scorer(X, y)                           -> exact log BF(S), vectorised log BF(T + l) for all l, log w(k)
  partition(X, B)                        -> v3 blocks: complete linkage on 1-|r| with the R13 tie rule,
                                            top-down cut (left child first), next-fit packing, members sorted
  StartLaw(scorer, blocks)               -> block tables r_b(U) (all subsets), exact pi_0 normaliser by
                                            convolution, log pi_0(S), start mode by max-plus DP, T22 q and e
  local_search(scorer, centre, ell, ...) -> the production local search (scan, then move-limit test)
  sigma_LH(...), gen_lh_iid(...), gen_lh_gram(...)  -> LH designs (unit-wise Cholesky; exact-Gram frame)
"""
import math
from itertools import combinations
import numpy as np
from scipy.special import gammaln, logsumexp


# ----------------------------------------------------------------------------------------------- data
def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0) / (n - 1))
    y = yr - yr.mean()
    y = y / math.sqrt((y ** 2).sum() / (n - 1))
    return X, y


def log_binom(a, b):
    return gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)


# ----------------------------------------------------------------------------------------------- scorer
class Scorer:
    """Exact g-prior-type marginal of 00_COMMON: D_S = det H_S / det(G_S + I), H_S = (n+1)G_S + I,
    Q_S = y'y - n z_S' H_S^{-1} z_S, log m(S) = -1/2 log D_S - nu log(0.02 + Q_S) + const."""

    def __init__(self, X, y):
        self.X, self.y = X, y
        self.n, self.p = X.shape
        n, p = self.n, self.p
        self.nu = 0.01 + n / 2.0
        self.yy = float(y @ y)
        self.K = min(p, n // 2)
        self.zall = X.T @ y
        self.logm_empty = -self.nu * math.log(0.02 + self.yy)
        k = np.arange(self.K + 2)
        self.logw = math.log(0.5) - log_binom(2 * p - 1, k)

    def logBF(self, S):
        S = sorted(S)
        if len(S) == 0:
            return 0.0
        n = self.n
        XS = self.X[:, S]
        G = XS.T @ XS
        z = self.zall[S]
        H = (n + 1) * G + np.eye(len(S))
        ld1 = np.linalg.slogdet(H)[1]
        ld2 = np.linalg.slogdet(G + np.eye(len(S)))[1]
        Q = self.yy - n * z @ np.linalg.solve(H, z)
        return -0.5 * (ld1 - ld2) - self.nu * math.log(0.02 + Q) - self.logm_empty

    def F(self, S):
        return self.logw[len(S)] + self.logBF(S)

    def add_scan(self, T):
        """log BF(T + l) for every l in [p] (entries for l in T are meaningless; caller masks them)."""
        n, p = self.n, self.p
        T = sorted(T)
        h = (n + 1) * (n - 1) + 1.0
        if len(T) == 0:
            sH = np.full(p, h)
            sG = np.full(p, float(n))
            w = self.zall.copy()
            quadT, ldT = 0.0, 0.0
        else:
            XT = self.X[:, T]
            GT = XT.T @ XT
            g = XT.T @ self.X                      # |T| x p
            zT = self.zall[T]
            HT = (n + 1) * GT + np.eye(len(T))
            GI = GT + np.eye(len(T))
            HiG = np.linalg.solve(HT, g)
            GiG = np.linalg.solve(GI, g)
            HiZ = np.linalg.solve(HT, zT)
            sH = h - (n + 1) ** 2 * np.einsum('ij,ij->j', g, HiG)
            sG = n - np.einsum('ij,ij->j', g, GiG)
            w = self.zall - (n + 1) * (g.T @ HiZ)
            quadT = float(zT @ HiZ)
            ldT = np.linalg.slogdet(HT)[1] - np.linalg.slogdet(GI)[1]
        with np.errstate(divide='ignore', invalid='ignore'):
            ld = ldT + np.log(sH) - np.log(sG)
            Q = self.yy - n * (quadT + w ** 2 / sH)
            out = -0.5 * ld - self.nu * np.log(0.02 + Q) - self.logm_empty
        out[T] = np.nan
        return out


# ----------------------------------------------------------------------------------------------- partition
def _lex_less(u, v):
    """Lexicographic order on sorted int lists, proper prefix first (R13 / lex_less)."""
    for a, b in zip(u, v):
        if a != b:
            return a < b
    return len(u) < len(v)


def complete_linkage(X):
    """Complete linkage on d = 1 - |r| with r = G_jl / sqrt(G_jj G_ll) (v3_blocks.h). Merge = closest pair of
    current clusters; exact-distance ties broken by the lexicographically smallest sorted union (R13 (1)).
    Left child = child with the smaller minimum index (R13 (2)). Returns (left, right, size, root)."""
    p = X.shape[1]
    G = X.T @ X
    s = np.sqrt(np.diag(G))
    r = G / np.outer(s, s)
    D = 1.0 - np.abs(r)
    np.fill_diagonal(D, np.inf)
    active = np.ones(p, bool)
    mem = [[j] for j in range(p)]
    node = list(range(p))
    minidx = list(range(p)) + [0] * (p - 1)
    size = [1] * p + [0] * (p - 1)
    left = [-1] * (2 * p - 1)
    right = [-1] * (2 * p - 1)
    bestd = D.min(axis=1)
    nxt = p
    for _ in range(p - 1):
        m = bestd[active].min()
        rows = np.flatnonzero(active & (bestd == m))
        cand = None
        for i in rows:
            for j in np.flatnonzero(active & (D[i] == m)):
                u = sorted(mem[i] + mem[j])
                if cand is None or _lex_less(u, cand[2]):
                    cand = (int(min(i, j)), int(max(i, j)), u)
        a, b, u = cand
        na, nb = node[a], node[b]
        L, R = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        left[nxt], right[nxt] = L, R
        size[nxt] = size[na] + size[nb]
        minidx[nxt] = min(minidx[na], minidx[nb])
        old_a, old_b = D[a].copy(), D[b].copy()
        newrow = np.maximum(old_a, old_b)
        mem[a] = u
        mem[b] = []
        active[b] = False
        node[a] = nxt
        D[a, :] = newrow
        D[:, a] = newrow
        D[a, a] = np.inf
        D[b, :] = np.inf
        D[:, b] = np.inf
        bestd[b] = np.inf
        # rows whose minimum may have increased
        redo = np.flatnonzero(active & ((old_a == bestd) | (old_b == bestd)))
        redo = np.union1d(redo, [a])
        bestd[redo] = D[redo].min(axis=1)
        nxt += 1
    return left, right, size, nxt - 1


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


def partition(X, B=None):
    n, p = X.shape
    if B is None:
        B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    if p == 1:
        return [[0]], B
    left, right, size, root = complete_linkage(X)
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
    return [sorted(b) for b in blocks], B


def margin_partition_check(X, groups):
    """Sufficient condition of PXN Lemma P1 (deterministic part): D_in < D_out, i.e. every within-group |r|
    exceeds every cross-group |r|. Returns (min within |r|, max cross |r|). Memory-light (group by group)."""
    G = None
    n, p = X.shape
    lab = np.empty(p, int)
    for h, gr in enumerate(groups):
        lab[gr] = h
    s = np.sqrt((X ** 2).sum(0))
    minin, maxout = 1.0, 0.0
    for h, gr in enumerate(groups):
        R = (X[:, gr].T @ X) / np.outer(s[gr], s)
        inside = lab == h
        Rin = np.abs(R[:, inside])
        k = len(gr)
        Rin = Rin[~np.eye(k, dtype=bool)]
        minin = min(minin, Rin.min())
        maxout = max(maxout, np.abs(R[:, ~inside]).max())
    return minin, maxout


# ----------------------------------------------------------------------------------------------- start law
_COMBOS = {}


def _combos(m, k):
    key = (m, k)
    if key not in _COMBOS:
        _COMBOS[key] = np.array(list(combinations(range(m), k)), dtype=int).reshape(-1, k)
    return _COMBOS[key]


class StartLaw:
    def __init__(self, sc, blocks):
        self.sc, self.blocks = sc, blocks
        n = sc.n
        self.J = len(blocks)
        self.where = {}
        for b, blk in enumerate(blocks):
            for t, j in enumerate(blk):
                self.where[j] = (b, t)
        self.logr = []      # per block: array over bitmasks
        self.prof = []      # per block: log sum_{|U|=k} r_b(U)
        for blk in blocks:
            m = len(blk)
            Xb = sc.X[:, blk]
            Gb = Xb.T @ Xb
            zb = sc.zall[blk]
            lr = np.zeros(1 << m)
            pr = np.full(m + 1, -np.inf)
            pr[0] = 0.0
            for k in range(1, m + 1):
                cb = _combos(m, k)
                Gs = Gb[cb[:, :, None], cb[:, None, :]]
                zs = zb[cb]
                I = np.eye(k)[None]
                H = (n + 1) * Gs + I
                ld = np.linalg.slogdet(H)[1] - np.linalg.slogdet(Gs + I)[1]
                Q = sc.yy - n * np.einsum('ij,ij->i', zs, np.linalg.solve(H, zs[:, :, None])[:, :, 0])
                v = -0.5 * ld - sc.nu * np.log(0.02 + Q) - sc.logm_empty
                masks = (1 << cb).sum(axis=1)
                lr[masks] = v
                pr[k] = logsumexp(v)
            self.logr.append(lr)
            self.prof.append(pr)
        K = sc.K
        L = np.full(K + 1, -np.inf)
        L[0] = 0.0
        Mx = np.full(K + 1, -np.inf)
        Mx[0] = 0.0
        self.mx_arg = []
        self.bmax = []
        for b in range(self.J):
            pr = self.prof[b]
            m = len(pr) - 1
            lr = self.logr[b]
            pc = np.array([bin(x).count('1') for x in range(1 << len(self.blocks[b]))])
            bm = np.array([lr[pc == k].max() if k > 0 else 0.0 for k in range(m + 1)])
            self.bmax.append((bm, pc))
            newL = np.full(K + 1, -np.inf)
            newM = np.full(K + 1, -np.inf)
            arg = np.zeros(K + 1, int)
            for j in range(min(m, K) + 1):
                cl = np.full(K + 1, -np.inf)
                cl[j:] = L[:K + 1 - j] + pr[j]
                newL = np.logaddexp(newL, cl)
                cm = np.full(K + 1, -np.inf)
                cm[j:] = Mx[:K + 1 - j] + (bm[j] if j > 0 else 0.0)
                better = cm > newM
                newM = np.where(better, cm, newM)
                arg = np.where(better, j, arg)
            L, Mx = newL, newM
            self.mx_arg.append(arg)
        self.convL = L
        self.convM = Mx
        self.logZ0 = logsumexp(sc.logw[:K + 1] + L)

    def masks_of(self, S):
        mk = [0] * self.J
        for j in S:
            b, t = self.where[j]
            mk[b] |= 1 << t
        return mk

    def log_gamma0(self, S):
        mk = self.masks_of(S)
        return self.sc.logw[len(S)] + sum(self.logr[b][mk[b]] for b in range(self.J))

    def log_pi0(self, S):
        return self.log_gamma0(S) - self.logZ0

    def mode(self):
        K = self.sc.K
        tot = self.sc.logw[:K + 1] + self.convM
        k = int(np.argmax(tot))          # argmax returns the first (smallest size) maximiser
        S = []
        for b in range(self.J - 1, -1, -1):
            j = self.mx_arg[b][k]
            if j > 0:
                bm, pc = self.bmax[b]
                lr = self.logr[b]
                idx = np.flatnonzero(pc == j)
                mask = idx[np.argmax(lr[idx])]
                S += [self.blocks[b][t] for t in range(len(self.blocks[b])) if (mask >> t) & 1]
            k -= j
        return sorted(S)

    def t22(self, Sref):
        """AGG quantities of 00_COMMON / T22(i) for reference Sref: q, e and the (i-a) lower bound."""
        sc = self.sc
        p = sc.p
        s = len(Sref)
        mk = self.masks_of(Sref)
        Dsum, emax = 0.0, -np.inf
        for b in range(self.J):
            lr = self.logr[b]
            m = len(self.blocks[b])
            U = mk[b]
            full = (1 << m) - 1
            rest = full & ~U
            if rest:
                allm = np.arange(1 << m)
                sup = allm[(allm & U) == U]
                jj = np.array([bin(x & rest).count('1') for x in sup])
                Db = -np.inf
                for j in range(1, bin(rest).count('1') + 1):
                    aj = logsumexp(lr[sup[jj == j]] - lr[U])
                    Db = max(Db, (gammaln(j + 1) + aj) / j)
                Dsum += math.exp(Db)
            if U:
                allm = np.arange(1 << m)
                for Wm in allm:
                    a = bin(U & ~Wm).count('1')
                    if a > 0:
                        emax = max(emax, (lr[Wm] - lr[Wm | U]) / a)
        q = Dsum / (p - s) if s < p else 0.0
        e = 2 * p * math.exp(emax) if emax > -np.inf else 0.0
        lb = 1 - ((s + 1) * q / (1 - q) + s * e) if q < 1 else -np.inf
        return q, e, lb


# ----------------------------------------------------------------------------------------------- local search
def lex_less(u, v):
    return _lex_less(sorted(u), sorted(v))


def local_search(sc, centre, ell, target=None, emit_centre=True):
    """Production local search (v3_engine.h::local_search): scan all feasible flips (additions only if |C| < K)
    and all swaps; best = max F, exact ties -> lexicographically smaller set; move iff strictly better and
    moves < ell (the limit test comes after the scan); otherwise stop. Returns a dict with the path, the
    termination, whether `target` was scored (centre emitted or appears in some scan), and the scan count."""
    p, K = sc.p, sc.K
    C = sorted(centre)
    FC = sc.F(C)
    target = sorted(target) if target is not None else None
    scored = emit_centre and target is not None and C == target
    moves, path, nscan, ties = 0, [list(C)], 0, 0
    best_seen = (FC, list(C)) if emit_centre else (-np.inf, None)
    while True:
        nscan += 1
        inC = np.zeros(p, bool)
        inC[C] = True
        cands = []  # (F, set)
        # flips: additions
        if len(C) < K:
            a = sc.add_scan(C) + sc.logw[len(C) + 1]
            a[inC] = -np.inf
            l = int(np.argmax(a))
            cands.append((a[l], sorted(C + [l]), a))
        # flips: deletions
        for j in C:
            T = [x for x in C if x != j]
            cands.append((sc.F(T), T, None))
        # swaps
        for j in C:
            T = [x for x in C if x != j]
            a = sc.add_scan(T) + sc.logw[len(C)]
            a[inC] = -np.inf
            l = int(np.argmax(a))
            cands.append((a[l], sorted(T + [l]), a))
        if target is not None and not scored:
            d = set(C) ^ set(target)
            if len(d) == 1 and (len(target) <= K):
                scored = True
            elif len(d) == 2 and len(C) == len(target):
                scored = True
        # best with exact-tie lexicographic rule (ties within an addition vector are checked)
        best = None
        for Fv, S, vec in cands:
            if vec is not None:
                nt = int(np.sum(vec == Fv))
                if nt > 1:
                    ties += 1
            if best is None or Fv > best[0] or (Fv == best[0] and _lex_less(S, best[1])):
                best = (Fv, S)
        if best[0] > best_seen[0]:
            best_seen = (best[0], list(best[1]))
        if best[0] > FC:
            if moves >= ell:
                return dict(path=path, term='move_limit', returned=best[1], scored=scored, nscan=nscan,
                            moves=moves, ties=ties, certified=False, best_seen=best_seen)
            C, FC = best[1], best[0]
            moves += 1
            path.append(list(C))
        else:
            return dict(path=path, term='no_improvement', returned=C, scored=scored, nscan=nscan,
                        moves=moves, ties=ties, certified=True, best_seen=best_seen)


# ----------------------------------------------------------------------------------------------- LH designs
def unit_cov_pair(g, rho_a, rho_b, psi):
    Sa = np.full((g, g), rho_a)
    np.fill_diagonal(Sa, 1.0)
    Sb = np.full((g, g), rho_b)
    np.fill_diagonal(Sb, 1.0)
    u = Sa[:, 0]
    v = Sb[:, 0]
    S = np.block([[Sa, psi * np.outer(u, v)], [psi * np.outer(v, u), Sb]])
    return S


def unit_cov_group(g, rho):
    S = np.full((g, g), rho)
    np.fill_diagonal(S, 1.0)
    return S


def lh_spec(G, g, rho, psis, betas, vis_betas, rho_null=None, null_groups_rho=None):
    """Groups 0..2c-1 are the pairs (2i, 2i+1); next v groups visible; rest null. Returns the list of units
    (list of (group indices, covariance)), theta, S0, Sref, M, groups. rho_null: within-group correlation of
    the null groups listed in null_groups_rho (adversarial design)."""
    c = len(psis)
    p = G * g
    groups = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    units = []
    theta = np.zeros(p)
    M = []
    for i in range(c):
        a, b = 2 * i, 2 * i + 1
        units.append(([a, b], unit_cov_pair(g, rho, rho, psis[i])))
        theta[a * g] = betas[i]
        theta[b * g] = -psis[i] * betas[i]
        M.append(b * g)
    for h in range(2 * c, G):
        r = rho
        if null_groups_rho is not None and h in null_groups_rho:
            r = rho_null
        units.append(([h], unit_cov_group(g, r)))
    for k, bv in enumerate(vis_betas):
        theta[(2 * c + k) * g] = bv
    S0 = sorted(np.flatnonzero(theta).tolist())
    Sref = sorted(set(S0) - set(M))
    return units, theta, S0, Sref, sorted(M), groups


def gen_lh_iid(n, G, g, units, theta, rng, sigma=1.0):
    p = G * g
    Xr = np.empty((n, p))
    for gl, S in units:
        idx = np.concatenate([np.arange(h * g, (h + 1) * g) for h in gl])
        L = np.linalg.cholesky(S)
        Xr[:, idx] = rng.standard_normal((n, len(idx))) @ L.T
    yr = Xr @ theta + sigma * rng.standard_normal(n)
    return Xr, yr


def sigma_full(G, g, units):
    p = G * g
    Sig = np.zeros((p, p))
    for gl, S in units:
        idx = np.concatenate([np.arange(h * g, (h + 1) * g) for h in gl])
        Sig[np.ix_(idx, idx)] = S
    return Sig


def gen_lh_gram(n, G, g, units, theta, rng, sigma=1.0):
    """Exact-Gram realisation X'X = (n-1) Sigma, X centred (W1-EXP §4.2): X = sqrt(n-1) Q Sigma^{1/2},
    Q an n x p orthonormal frame orthogonal to 1 (random rotation, seeded)."""
    p = G * g
    Sig = sigma_full(G, g, units)
    A = rng.standard_normal((n, p))
    A = A - A.mean(axis=0)
    Q, _ = np.linalg.qr(A)
    w, V = np.linalg.eigh(Sig)
    root = (V * np.sqrt(w)) @ V.T
    Xr = math.sqrt(n - 1) * Q @ root
    yr = Xr @ theta + sigma * rng.standard_normal(n)
    return Xr, yr
