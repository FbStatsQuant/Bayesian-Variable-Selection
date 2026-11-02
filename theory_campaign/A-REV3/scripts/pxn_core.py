"""W3-PXN core: exact SMC-BVS v3 start-side objects for p >> n designs (Python 3 + numpy/scipy).

Implements (notation of Docs/Theory/theorems/00_COMMON.md):
  * standardisation, log m(S) (S-free constant dropped), log BF, log w(k) (BB(1,p)), K = min(p, floor(n/2));
  * the v3 partition: complete linkage on 1-|r| (scipy; continuous data so the R13 tie rule is immaterial),
    R13 left child = child with the smaller minimum index, top-down cut at B, next-fit packing in leaf order;
  * block tables log r_b(U) for every U in C_b (batched by size);
  * exact start law pi0 by convolution of block size profiles with the capped size prior (log domain);
    pi0 of a single model, pi0(R_d) by a bivariate (size, extras) convolution, start PIPs, start mode
    (max-plus convolution), exact iid pi0 draws (backward sampler);
  * T22(i) aggregation quantities q, e for a reference S°;
  * full-model scores F(S) and the production local search (best strictly improving flip or swap).
Everything is exact up to floating point (EX-A).
"""
import math
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.cluster.hierarchy import linkage

A0 = 0.01
B0 = 0.01


# ------------------------------------------------------------------ data
class Data:
    """Standardised data; keeps X (n x p, columns of squared norm n-1) and y (squared norm n-1)."""

    def __init__(self, Xr, yr):
        n, p = Xr.shape
        X = Xr - Xr.mean(0)
        X /= np.sqrt((X ** 2).sum(0) / (n - 1))
        y = yr - yr.mean()
        y /= math.sqrt((y ** 2).sum() / (n - 1))
        self.X, self.y, self.n, self.p = X, y, n, p
        self.z = X.T @ y  # z_j = x_j'y
        self.nu = A0 + n / 2.0
        self.K = min(p, n // 2)
        self.B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
        self.lm0 = -self.nu * math.log(2 * B0 + n - 1.0)

    def gram(self, idx):
        Xs = self.X[:, idx]
        return Xs.T @ Xs


def log_w(k, p):
    k = np.asarray(k, float)
    return -math.log(2.0) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


def log_m_batch(models, G, z, n, nu):
    """log m (constant dropped) for models of a common size k: models (N,k) index into G (Gram) and z."""
    models = np.asarray(models, int)
    N, k = models.shape
    if k == 0:
        return np.full(N, -nu * math.log(2 * B0 + n - 1.0))
    GS = G[models[:, :, None], models[:, None, :]]
    zS = z[models]
    I = np.eye(k)[None]
    H = (n + 1.0) * GS + I
    _, ldH = np.linalg.slogdet(H)
    _, ldG = np.linalg.slogdet(GS + I)
    sol = np.linalg.solve(H, zS[:, :, None])[:, :, 0]
    Q = (n - 1.0) - n * np.einsum("ij,ij->i", zS, sol)
    return -0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)


def log_bf_sets(D, sets):
    """log BF(S) for a list of index sets (any sizes)."""
    out = np.empty(len(sets))
    bysize = {}
    for i, S in enumerate(sets):
        bysize.setdefault(len(S), []).append(i)
    for k, ids in bysize.items():
        if k == 0:
            out[ids] = 0.0
            continue
        M = np.array([sorted(sets[i]) for i in ids], int)
        cols = np.unique(M)
        pos = {c: t for t, c in enumerate(cols)}
        G = D.gram(cols)
        z = D.z[cols]
        Ml = np.vectorize(pos.get)(M)
        for s in range(0, len(ids), 20000):
            out[np.array(ids[s:s + 20000])] = log_m_batch(Ml[s:s + 20000], G, z, D.n, D.nu) - D.lm0
    return out


def log_F(D, sets):
    """F(S) up to the global constant: log w(|S|) + log BF(S)."""
    sizes = np.array([len(S) for S in sets])
    return log_w(sizes, D.p) + log_bf_sets(D, sets)


# ------------------------------------------------------------------ partition
def v3_blocks(D, B=None, corr=None):
    """v3 partition. corr: optional precomputed correlation matrix."""
    p = D.p
    B = D.B if B is None else B
    if corr is None:
        corr = (D.X.T @ D.X) / (D.n - 1)
    dist = 1.0 - np.abs(corr)
    np.fill_diagonal(dist, 0.0)
    iu = np.triu_indices(p, 1)
    Z = linkage(np.clip(dist[iu], 0, None), method="complete")
    left, right, size, minidx = {}, {}, {}, {}
    for j in range(p):
        size[j], minidx[j] = 1, j
    for t, (a, b, h, sz) in enumerate(Z):
        a, b, nd = int(a), int(b), p + t
        L, R = (a, b) if minidx[a] < minidx[b] else (b, a)
        left[nd], right[nd] = L, R
        size[nd] = size[a] + size[b]
        minidx[nd] = min(minidx[a], minidx[b])
    root = p + len(Z) - 1

    def leaves(nd):
        out, st = [], [nd]
        while st:
            x = st.pop()
            if x < p:
                out.append(x)
                continue
            st.append(right[x])
            st.append(left[x])
        return out

    clusters, st = [], [root]
    while st:
        x = st.pop()
        if size[x] <= B:
            clusters.append(leaves(x))
            continue
        st.append(right[x])
        st.append(left[x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B:
            blocks.append(sorted(cur))
            cur = []
        cur += c
    if cur:
        blocks.append(sorted(cur))
    return blocks


def group_margin(D, groups, chunk=2000):
    """Sufficient condition of Lemma P1: max within-group distance vs min cross-group distance (1-|r|).
    Returns (max_within, min_cross); blocks = groups when max_within < min_cross and g <= B < 2g."""
    p = D.p
    gid = np.empty(p, int)
    for h, C in enumerate(groups):
        gid[C] = h
    maxw, minc = 0.0, 2.0
    for s in range(0, p, chunk):
        R = np.abs(D.X[:, s:s + chunk].T @ D.X) / (D.n - 1)
        same = gid[s:s + chunk, None] == gid[None, :]
        idx = np.arange(s, min(s + chunk, p))
        R[idx - s, idx] = np.nan
        dw = 1 - R[same & ~np.isnan(R)]
        dc = 1 - R[~same]
        if dw.size:
            maxw = max(maxw, dw.max())
        if dc.size:
            minc = min(minc, dc.min())
    return maxw, minc


# ------------------------------------------------------------------ tables
class Tables:
    """Block tables: for block b, subsets enumerated as bitmasks over the sorted block members."""

    def __init__(self, D, blocks):
        self.D, self.blocks = D, blocks
        self.where = {}
        for b, C in enumerate(blocks):
            for t, j in enumerate(C):
                self.where[j] = (b, t)
        self.lr = []      # lr[b][mask] = log r_b(U)
        self.size = []    # popcount per mask
        for C in blocks:
            g = len(C)
            G = D.gram(C)
            z = D.z[C]
            masks = np.arange(1 << g)
            pc = np.array([bin(m).count("1") for m in masks])
            lr = np.zeros(1 << g)
            for k in range(1, g + 1):
                mk = masks[pc == k]
                M = np.array([[t for t in range(g) if (m >> t) & 1] for m in mk], int)
                for s in range(0, len(mk), 20000):
                    lr[mk[s:s + 20000]] = log_m_batch(M[s:s + 20000], G, z, D.n, D.nu) - D.lm0
            self.lr.append(lr)
            self.size.append(pc)

    def mask(self, b, S):
        C = self.blocks[b]
        m = 0
        for j in S:
            if j in self.where and self.where[j][0] == b:
                m |= 1 << self.where[j][1]
        return m

    def log_r(self, S):
        """Sum_b log r_b(S cap C_b)."""
        tot = 0.0
        per = {}
        for j in S:
            b, t = self.where[j]
            per[b] = per.get(b, 0) | (1 << t)
        for b, m in per.items():
            tot += self.lr[b][m]
        return tot

    def profile(self, b, forced_in=(), forced_out=()):
        """log sum_{|U|=k} r_b(U) for k=0..g, with optional constraints (bitmasks)."""
        g = len(self.blocks[b])
        lr, pc = self.lr[b], self.size[b]
        masks = np.arange(1 << g)
        ok = np.ones(1 << g, bool)
        fi = sum(1 << self.where[j][1] for j in forced_in if self.where[j][0] == b)
        fo = sum(1 << self.where[j][1] for j in forced_out if self.where[j][0] == b)
        if fi:
            ok &= (masks & fi) == fi
        if fo:
            ok &= (masks & fo) == 0
        out = np.full(g + 1, -np.inf)
        for k in range(g + 1):
            sel = ok & (pc == k)
            if sel.any():
                out[k] = logsumexp(lr[sel])
        return out


def conv_log(a, b, K):
    """log-domain convolution truncated at K."""
    la, lb = len(a), len(b)
    n = min(la + lb - 1, K + 1)
    out = np.full(n, -np.inf)
    for j in range(lb):
        if lb and np.isfinite(b[j]):
            m = min(la, n - j)
            if m > 0:
                out[j:j + m] = np.logaddexp(out[j:j + m], a[:m] + b[j])
    return out


class StartLaw:
    """Exact pi0 = w(|S|) prod_b r_b(S cap C_b) / Zbar0 on Omega = {|S| <= K}."""

    def __init__(self, T):
        self.T, self.D = T, T.D
        K, p = T.D.K, T.D.p
        self.prof = [T.profile(b) for b in range(len(T.blocks))]
        self.fwd = [np.array([0.0])]
        for pr in self.prof:
            self.fwd.append(conv_log(self.fwd[-1], pr, K))
        tot = self.fwd[-1]
        self.lw = log_w(np.arange(len(tot)), p)
        self.logZ = logsumexp(tot + self.lw)

    def log_pi0(self, S):
        return log_w(len(S), self.D.p) + self.T.log_r(S) - self.logZ

    def log_mass_constrained(self, forced_in=(), forced_out=()):
        K = self.D.K
        acc = np.array([0.0])
        fin, fout = set(forced_in), set(forced_out)
        for b in range(len(self.T.blocks)):
            C = set(self.T.blocks[b])
            if C & (fin | fout):
                pr = self.T.profile(b, [j for j in fin if j in C], [j for j in fout if j in C])
            else:
                pr = self.prof[b]
            acc = conv_log(acc, pr, K)
        return logsumexp(acc + log_w(np.arange(len(acc)), self.D.p)) - self.logZ

    def log_mass_Rd(self, S0, d):
        """log pi0(R_d), R_d = {S : |S minus S0| <= d} (subsets of S0 arbitrary)."""
        K, S0 = self.D.K, set(S0)
        E = d + 2  # extras bucket 0..d, d+1 = overflow
        acc = np.full((1, E), -np.inf)
        acc[0, 0] = 0.0
        for b, C in enumerate(self.T.blocks):
            g = len(C)
            tmask = sum(1 << t for t, j in enumerate(C) if j in S0)
            lr, pc = self.T.lr[b], self.T.size[b]
            masks = np.arange(1 << g)
            ex = np.array([bin(m & ~tmask).count("1") for m in masks])
            ex = np.minimum(ex, d + 1)
            pr = np.full((g + 1, E), -np.inf)
            for k in range(g + 1):
                for e in range(E):
                    sel = (pc == k) & (ex == e)
                    if sel.any():
                        pr[k, e] = logsumexp(lr[sel])
            nk = min(acc.shape[0] + g, K + 1)
            new = np.full((nk, E), -np.inf)
            for k2 in range(g + 1):
                for e2 in range(E):
                    if not np.isfinite(pr[k2, e2]):
                        continue
                    m = min(acc.shape[0], nk - k2)
                    if m <= 0:
                        continue
                    for e1 in range(E):
                        e3 = min(e1 + e2, d + 1)
                        new[k2:k2 + m, e3] = np.logaddexp(new[k2:k2 + m, e3], acc[:m, e1] + pr[k2, e2])
            acc = new
        lw = log_w(np.arange(acc.shape[0]), self.D.p)
        return logsumexp(acc[:, :d + 1] + lw[:, None]) - self.logZ

    def start_mode(self):
        """argmax pi0 by max-plus convolution over blocks (per total size), then over size."""
        K = self.D.K
        best = [np.array([0.0])]
        arg = []
        for b, C in enumerate(self.T.blocks):
            g = len(C)
            lr, pc = self.T.lr[b], self.T.size[b]
            bm = np.full(g + 1, -np.inf)
            bmask = np.zeros(g + 1, int)
            for k in range(g + 1):
                sel = np.flatnonzero(pc == k)
                i = sel[np.argmax(lr[sel])]
                bm[k], bmask[k] = lr[i], i
            prev = best[-1]
            nk = min(len(prev) + g, K + 1)
            cur = np.full(nk, -np.inf)
            ch = np.zeros(nk, int)
            for k2 in range(g + 1):
                m = min(len(prev), nk - k2)
                if m <= 0:
                    continue
                cand = prev[:m] + bm[k2]
                upd = cand > cur[k2:k2 + m]
                cur[k2:k2 + m][upd] = cand[upd]
                ch[k2:k2 + m][upd] = k2
            best.append(cur)
            arg.append((ch, bmask))
        tot = best[-1] + log_w(np.arange(len(best[-1])), self.D.p)
        k = int(np.argmax(tot))
        S = []
        for b in range(len(self.T.blocks) - 1, -1, -1):
            ch, bmask = arg[b]
            k2 = ch[k]
            m = bmask[k2]
            C = self.T.blocks[b]
            S += [C[t] for t in range(len(C)) if (m >> t) & 1]
            k -= k2
        return sorted(S), float(tot.max() - self.logZ)

    def sample(self, H, rng):
        """H exact iid pi0 draws (backward sampler)."""
        tot = self.fwd[-1] + self.lw
        pk = np.exp(tot - logsumexp(tot))
        k = rng.choice(len(pk), size=H, p=pk)
        out = [[] for _ in range(H)]
        for b in range(len(self.T.blocks) - 1, -1, -1):
            pr = self.prof[b]
            prevf = self.fwd[b]
            g = len(pr) - 1
            lp = np.full((H, g + 1), -np.inf)
            for j in range(g + 1):
                kk = k - j
                ok = (kk >= 0) & (kk < len(prevf))
                lp[ok, j] = pr[j] + prevf[kk[ok]]
            gum = lp + rng.gumbel(size=lp.shape)
            jj = np.argmax(gum, axis=1)
            lr, pc = self.T.lr[b], self.T.size[b]
            C = self.T.blocks[b]
            for j in np.unique(jj):
                if j == 0:
                    continue
                who = np.flatnonzero(jj == j)
                sel = np.flatnonzero(pc == j)
                pm = np.exp(lr[sel] - logsumexp(lr[sel]))
                ms = sel[rng.choice(len(sel), size=len(who), p=pm)]
                for w, m in zip(who, ms):
                    out[w] += [C[t] for t in range(len(C)) if (m >> t) & 1]
            k = k - jj
        return [sorted(S) for S in out]


def agg_q_e(T, Sref):
    """T22(i) quantities q and e for reference Sref (00_COMMON AGG / T22 STATEMENT)."""
    D = T.D
    p, s = D.p, len(Sref)
    Sref = set(Sref)
    sumD, emax = 0.0, -np.inf
    for b, C in enumerate(T.blocks):
        g = len(C)
        um = sum(1 << t for t, j in enumerate(C) if j in Sref)
        lr, pc = T.lr[b], T.size[b]
        masks = np.arange(1 << g)
        base = lr[um]
        sup = (masks & um) == um
        nfree = g - bin(um).count("1")
        Db = 0.0
        for j in range(1, nfree + 1):
            sel = sup & (pc == bin(um).count("1") + j)
            laj = logsumexp(lr[sel]) - base
            Db = max(Db, math.exp((gammaln(j + 1) + laj) / j))
        sumD += Db
        if um:
            for U in masks:
                a = bin(um & ~U).count("1")
                if a > 0:
                    emax = max(emax, (lr[U] - lr[U | um]) / a)
    q = sumD / (p - s) if s < p else 0.0
    loge = math.log(2 * p) + emax if np.isfinite(emax) else -np.inf
    return q, loge


# ------------------------------------------------------------------ local search
def neighbours(S, p, K):
    S = sorted(S)
    Sset = set(S)
    out = []
    for j in range(p):
        if j in Sset:
            out.append(tuple(x for x in S if x != j))
        elif len(S) < K:
            out.append(tuple(sorted(S + [j])))
    for i in S:
        rest = [x for x in S if x != i]
        for j in range(p):
            if j not in Sset:
                out.append(tuple(sorted(rest + [j])))
    return out


def local_search(D, centre, ell, S0=None):
    """Production local search (M §6.10 reading of W1-T37R): best strictly improving flip or swap,
    at most ell moves, then one more scan. Returns path, scores, number scored, whether S0 was scored."""
    S = tuple(sorted(centre))
    path = [S]
    fS = log_F(D, [list(S)])[0]
    scored_S0 = (S0 is not None and S == tuple(sorted(S0)))
    nsc = 1
    moves = 0
    while True:
        nb = neighbours(S, D.p, D.K)
        f = log_F(D, [list(x) for x in nb])
        nsc += len(nb)
        if S0 is not None and tuple(sorted(S0)) in set(nb):
            scored_S0 = True
        i = int(np.argmax(f))
        if f[i] <= fS or moves >= ell:
            return dict(path=path, F=fS, nscored=nsc, scored_S0=scored_S0, certified=bool(f[i] <= fS),
                        best_gain=float(f[i] - fS))
        S, fS = nb[i], f[i]
        path.append(S)
        moves += 1
