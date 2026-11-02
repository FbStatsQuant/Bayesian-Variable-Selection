"""O-DILUTE library: v3 blocks, block tables, exact start quantities by convolution.

Faithful (up to floating-point ties) Python port of METHODOLOGY_v3 §5 (score), §6.3 (blocks, tables, start).
Partition: complete linkage on 1-|r| (scipy; ties are measure-zero for continuous data), left child = child with
smaller minimum index (R13), top-down cut left-first, next-fit packing in leaf order.

Table variants (all product-form, all exactly samplable; Prop P(i) of F-DRAFT covers validity):
  'v3'     r_b(U) = m(U)/m(empty) on the full y, IG-integrated sigma^2 per table (the method).
  'known'  r_b(U) = (det H_U/det(G_U+I))^{-1/2} exp(t_U / (2 s2)) with ONE common plug-in s2 (F-DRAFT candidate).
  'resid'  v3 tables computed on a partial residual y_b = y - X_{-b} bhat_{-b} (backfit variant; pilot only).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4"); os.environ.setdefault("MKL_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")
import itertools
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from scipy.special import gammaln, logsumexp

A0 = 0.01; B0 = 0.01

# ----------------------------------------------------------------------------- data (port of gen_dev/gen_prod)
def scenario_covariance(s, p):
    g = (np.arange(p)) // 5
    H = (g[:, None] == g[None, :]).astype(float)
    I = np.eye(p)
    if s == 1: return I
    if s == 2: return 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    if s == 3: return 0.7 * H + 0.3 * I
    if s == 4: return 0.85 * H + 0.15 * I
    if s == 5: return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if s == 6:
        rho = 0.4 + 0.1 * (g % 6)
        S = H * rho[:, None]; S = np.where(H > 0, S, 0.0); np.fill_diagonal(S, 1.0); return S
    raise ValueError

def truth(p):
    s0 = 14; step = {500: 7, 1000: 13}[p]
    pos = [3, 2, 4, 1, 5, 3]; pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0); block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1   # 0-based
    beta = np.array([pattern[i % 6] for i in k])
    return active, beta

def gen_dataset(p, s, seed, n=200, scales=(1.0, 0.5), chol=None):
    rng = np.random.default_rng(seed)
    if chol is None: chol = np.linalg.cholesky(scenario_covariance(s, p))   # lower: Sigma = L L^T
    raw = rng.standard_normal((n, p)) @ chol.T
    X = (raw - raw.mean(0)) / raw.std(0, ddof=1)
    eps = rng.standard_normal(n)
    act, beta = truth(p)
    b = np.zeros(p); b[act] = beta
    sig = X @ b
    Ys = {c: c * sig + eps for c in scales}
    return X, Ys, act, b, eps

def std_y(y):
    yc = y - y.mean(); sy = yc.std(ddof=1); return yc / sy, sy

# ----------------------------------------------------------------------------- partition
def make_blocks(X, B):
    p = X.shape[1]
    R = np.corrcoef(X, rowvar=False)
    D = 1.0 - np.abs(R); np.fill_diagonal(D, 0.0); D = np.maximum(D, 0.0); D = (D + D.T) / 2
    Z = linkage(squareform(D, checks=False), method="complete")
    left = [-1] * (2 * p - 1); right = [-1] * (2 * p - 1); size = [1] * (2 * p - 1); mn = list(range(p)) + [0] * (p - 1)
    for i, (a, b, h, sz) in enumerate(Z):
        a = int(a); b = int(b); nn = p + i
        L, Rr = (a, b) if mn[a] < mn[b] else (b, a)
        left[nn] = L; right[nn] = Rr; size[nn] = size[a] + size[b]; mn[nn] = min(mn[a], mn[b])
    root = 2 * p - 2
    def leaves(nd):
        out, st = [], [nd]
        while st:
            x = st.pop()
            if x < p: out.append(x); continue
            st.append(right[x]); st.append(left[x])
        return out
    clusters, st = [], [root]
    while st:
        x = st.pop()
        if size[x] <= B: clusters.append(leaves(x)); continue
        st.append(right[x]); st.append(left[x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B: blocks.append(sorted(cur)); cur = []
        cur += c
    if cur: blocks.append(sorted(cur))
    return blocks

# ----------------------------------------------------------------------------- tables
def block_stats(X, blk, Ymat, n):
    """For block columns blk and responses Ymat (n x ny): per subset mask (0..2^m-1)
    returns size, ld (log det H - log det(G+I)) and t (n z' H^-1 z) for each response (2^m x ny)."""
    m = len(blk); Xb = X[:, blk]; G = Xb.T @ Xb; Zb = Xb.T @ Ymat           # m x ny
    ny = Ymat.shape[1]
    N = 1 << m
    ld = np.zeros(N); t = np.zeros((N, ny)); sz = np.zeros(N, dtype=int)
    for k in range(1, m + 1):
        combs = np.array(list(itertools.combinations(range(m), k)))      # C x k
        masks = (1 << combs).sum(1)
        Gs = G[combs[:, :, None], combs[:, None, :]]
        I = np.eye(k)
        H = (n + 1) * Gs + I
        s1, l1 = np.linalg.slogdet(H); s2, l2 = np.linalg.slogdet(Gs + I)
        zs = Zb[combs]                                                    # C x k x ny
        sol = np.linalg.solve(H, zs)
        ld[masks] = l1 - l2
        t[masks] = n * np.einsum("ckj,ckj->cj", zs, sol)
        sz[masks] = k
    return sz, ld, t

def log_r_v3(ld, t, yy, n):
    nu = A0 + n / 2.0
    Q = yy - t
    return -0.5 * ld - nu * (np.log(2 * B0 + Q) - np.log(2 * B0 + yy))

def log_r_known(ld, t, s2):
    return -0.5 * ld + t / (2.0 * s2)

def log_w(k, p):
    k = np.asarray(k, dtype=float)
    return np.log(0.5) - gammaln(2 * p) + gammaln(k + 1) + gammaln(2 * p - k)

# ----------------------------------------------------------------------------- exact start quantities
def start_summary(tabs, truthmasks, p, s0, K, t_tilt=None):
    """tabs: list of (sz, logr) per block; truthmasks: per block bitmask of truths.
    Returns dict with exact log pi0(S0), joint law of (#truths, #nulls), decomposition terms."""
    S0max = s0
    F = np.full((S0max + 1, K + 1), -np.inf); F[0, 0] = 0.0                    # log-scale joint (i truths, j nulls)
    logr_S0 = 0.0
    if t_tilt is None: t_tilt = (s0 + 1) / (2 * p - s0 - 1)
    lt = np.log(t_tilt)
    vis = 0.0; comp = 0.0; sumlogeb = 0.0; per_block = []
    for (sz, lr), tm in zip(tabs, truthmasks):
        N = len(lr); masks = np.arange(N)
        nt = np.array([bin(x & tm).count("1") for x in masks]); nn = sz - nt
        # local 2D table
        mt = nt.max(); mn_ = nn.max()
        loc = np.full((mt + 1, mn_ + 1), -np.inf)
        for a in range(mt + 1):
            for b in range(mn_ + 1):
                sel = (nt == a) & (nn == b)
                if sel.any(): loc[a, b] = logsumexp(lr[sel])
        # 2D log-convolution
        newF = np.full_like(F, -np.inf)
        for a in range(mt + 1):
            for b in range(mn_ + 1):
                if not np.isfinite(loc[a, b]): continue
                sh = F[: S0max + 1 - a, : K + 1 - b] + loc[a, b]
                newF[a:, b:] = np.logaddexp(newF[a:, b:], sh)
        F = newF
        lr_s0b = lr[tm]; logr_S0 += lr_s0b
        # tilted decomposition
        leb = logsumexp(lr + sz * lt); sumlogeb += leb
        k0 = bin(tm).count("1")
        if k0 > 0:
            lam = lr_s0b + k0 * lt
            v = np.logaddexp(0.0, -lam)                                     # softplus(-lam)
            rest = leb - np.logaddexp(0.0, lam)                             # log(1+eta)
            vis += v; comp += rest
            per_block.append(dict(k0=k0, lam=float(lam), vis=float(v), comp=float(rest), m=len(sz).bit_length() - 1))
        else:
            comp += leb
    kk = np.add.outer(np.arange(S0max + 1), np.arange(K + 1))
    valid = kk <= K
    lw = np.where(valid, log_w(np.minimum(kk, K), p), -np.inf)
    J = lw + F
    logZ0 = logsumexp(J[np.isfinite(J)])
    logpi0_S0 = log_w(s0, p) + logr_S0 - logZ0
    P = np.exp(J - logZ0); P[~np.isfinite(J)] = 0.0
    logA = log_w(s0, p) - s0 * lt + sumlogeb - logZ0
    out = dict(logpi0_S0=float(logpi0_S0), P=P, vis=float(vis), comp=float(comp), logA=float(logA),
               logr_S0=float(logr_S0), per_block=per_block)
    nulls = P.sum(0); tr = P.sum(1)
    out["pi0_R"] = {d: float(nulls[: d + 1].sum()) for d in range(4)}
    ham = np.zeros(S0max + K + 2)
    for i in range(S0max + 1):
        for j in range(K + 1):
            ham[(s0 - i) + j] += P[i, j]
    out["pi0_ham"] = {d: float(ham[: d + 1].sum()) for d in range(4)}
    out["E_truths"] = float((tr * np.arange(S0max + 1)).sum()); out["E_nulls"] = float((nulls * np.arange(K + 1)).sum())
    out["med_truths"] = int(np.searchsorted(np.cumsum(tr), 0.5))
    return out

def start_mode(tabs, p, K):
    """Exact argmax of gamma0 via max-plus DP over sizes. Returns list of (block index, mask)."""
    best = np.full(K + 1, -np.inf); best[0] = 0.0; back = []
    for bi, (sz, lr) in enumerate(tabs):
        m = sz.max()
        Mb = np.full(m + 1, -np.inf); Ab = np.zeros(m + 1, dtype=int)
        for k in range(m + 1):
            sel = np.where(sz == k)[0]
            j = sel[np.argmax(lr[sel])]; Mb[k] = lr[j]; Ab[k] = j
        new = np.full(K + 1, -np.inf); arg = np.zeros(K + 1, dtype=int)
        for k in range(m + 1):
            cand = np.full(K + 1, -np.inf); cand[k:] = best[: K + 1 - k] + Mb[k]
            upd = cand > new; new[upd] = cand[upd]; arg[upd] = k
        back.append((arg, Ab)); best = new
    tot = best + log_w(np.arange(K + 1), p)
    k = int(np.argmax(tot)); sel = []
    for bi in range(len(tabs) - 1, -1, -1):
        arg, Ab = back[bi]; kb = arg[k]; sel.append((bi, int(Ab[kb]))); k -= kb
    return sel[::-1]

def mask_to_cols(blk, mask):
    return [blk[i] for i in range(len(blk)) if (mask >> i) & 1]

def log_bf_full(X, y, S, n):
    """log BF(S) = log m(S) - log m(empty) under the v3 score, standardized data."""
    yy = float(y @ y)
    if len(S) == 0: return 0.0
    Xs = X[:, S]; G = Xs.T @ Xs; z = Xs.T @ y; k = len(S)
    H = (n + 1) * G + np.eye(k)
    ld = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
    tt = n * z @ np.linalg.solve(H, z)
    return float(log_r_v3(ld, tt, yy, n))
