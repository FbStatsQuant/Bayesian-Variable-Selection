"""W3-DIST numerics: exact posterior (W3-POST STATEMENT s0), distances, designs. numpy/scipy only."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy.special import gammaln

A0 = 0.01   # IG shape prior
B0 = 0.01   # IG rate prior
SIG_STAR = 1.0
MCHUNK = 250

# ---------------------------------------------------------------- designs
def gen_design(kind, n, p, rng, tau2=None):
    """raw design rows, unit variance coordinates. kind in ar, t25, pareto, spike, collin."""
    if kind in ("ar", "collin"):
        pp = 6 if kind == "collin" else p
        Z = rng.standard_normal((n, pp))
        X = np.empty((n, pp))
        X[:, 0] = Z[:, 0]
        r = 0.5; s = np.sqrt(1 - r * r)
        for j in range(1, pp):
            X[:, j] = r * X[:, j - 1] + s * Z[:, j]
        if kind == "collin":
            E = rng.standard_normal((n, p - 6))
            X = np.hstack([X, X[:, [0]] + np.sqrt(tau2) * E])
        return X
    if kind == "t25":
        return rng.standard_t(2.5, size=(n, p)) / np.sqrt(2.5 / 0.5)
    if kind == "pareto":
        a = 2.1
        U = rng.random((n, p))
        P = U ** (-1.0 / a)                      # Pareto(1, a), E P^2 = a/(a-2)
        sgn = rng.choice([-1.0, 1.0], size=(n, p))
        return sgn * P / np.sqrt(a / (a - 2))
    if kind == "spike":
        nz = rng.random((n, p)) < 2.0 / n
        sgn = rng.choice([-1.0, 1.0], size=(n, p))
        return nz * sgn * np.sqrt(n / 2.0)
    raise ValueError(kind)

AR_SIGMA = lambda p: 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))

def beta_star(name, n, p):
    b = np.zeros(p)
    if name == "sparse":
        b[:3] = [1, -1, 1]
    elif name == "nobetamin":
        c = 0.7 * np.sqrt(np.log(n) / n)
        b[:3] = [1, c, c]
    elif name == "approx":
        b[:] = np.arange(1, p + 1) ** -2.0
        S = AR_SIGMA(p)
        b *= np.sqrt(3.0 / (b @ S @ b))
    else:
        raise ValueError(name)
    return b

# ---------------------------------------------------------------- posterior
class Data:
    pass

def prep(Xr, yr):
    d = Data()
    n, p0 = Xr.shape
    xbar = Xr.mean(0)
    Xc = Xr - xbar
    ss = (Xc ** 2).sum(0)
    keep = np.where(ss > 1e-9)[0]
    sd = np.sqrt(ss[keep] / (n - 1))
    d.n, d.p0, d.keep, d.xbar0, d.sd = n, p0, keep, xbar, sd
    d.X = Xc[:, keep] / sd
    d.q = len(keep)
    d.ybar = yr.mean()
    yc = yr - d.ybar
    d.sy = np.sqrt((yc ** 2).sum() / (n - 1))
    d.y = yc / d.sy
    d.K = min(d.q, n // 2)
    d.G = d.X.T @ d.X
    d.z = d.X.T @ d.y
    d.yty = d.y @ d.y
    return d

def logw(k, q):
    return np.log(0.5) - (gammaln(2 * q) - gammaln(k + 1) - gammaln(2 * q - k))

def batched_logpi(d, idx):
    """idx (m,k) padded with -1. returns logpi (unnormalised), Q, sizes"""
    n = d.n
    m, k = idx.shape
    mask = idx >= 0
    ii = np.where(mask, idx, 0)
    Gs = d.G[ii[:, :, None], ii[:, None, :]]
    pm = mask[:, :, None] & mask[:, None, :]
    Gs = np.where(pm, Gs, 0.0)
    eye = np.eye(k)
    H = (n + 1) * Gs + eye
    G1 = Gs + eye
    zs = np.where(mask, d.z[ii], 0.0)
    _, ldH = np.linalg.slogdet(H)
    _, ldG = np.linalg.slogdet(G1)
    sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
    Q = d.yty - n * (zs * sol).sum(1)
    sizes = mask.sum(1)
    nu = A0 + n / 2
    lp = logw(sizes, d.q) - 0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)
    return lp, Q, sizes

_enum_cache = {}
def enum_all(q):
    if q not in _enum_cache:
        bits = (np.arange(2 ** q)[:, None] >> np.arange(q)) & 1
        idx = np.sort(np.where(bits == 1, np.arange(q), q), axis=1)
        idx[idx == q] = -1
        _enum_cache[q] = idx.astype(np.int32)
    return _enum_cache[q]

def exact_family(d):
    idx = enum_all(d.q)
    sizes = (idx >= 0).sum(1)
    idx = idx[sizes <= d.K]
    lp, Q, sz = batched_logpi(d, idx)
    return idx, lp, Q, sz

def restricted_family(d, support0, rng):
    """size<=2 over full q + subsets size 3..5 of pool U. returns idx padded to k=5."""
    q, n = d.q, d.n
    kmax = 5
    parts = []
    lps, Qs, szs = [], [], []
    # size <=2
    e0 = -np.ones((1, 2), dtype=np.int32)
    i1 = np.stack([np.arange(q), -np.ones(q, dtype=int)], 1).astype(np.int32)
    a, b = np.triu_indices(q, 1)
    i2 = np.stack([a, b], 1).astype(np.int32)
    A = np.vstack([e0, i1, i2])
    lp, Q, sz = batched_logpi(d, A)
    Ap = -np.ones((len(A), kmax), dtype=np.int32); Ap[:, :2] = A
    parts.append(Ap); lps.append(lp); Qs.append(Q); szs.append(sz)
    # pool U
    cors = np.abs(d.X.T @ d.y) / np.sqrt(d.yty * (n - 1))
    top = list(np.argsort(-cors)[:12])
    s0 = [j for j in range(q) if d.keep[j] in support0]
    rest = [j for j in range(q) if j not in set(s0) | set(top)]
    rnd = list(rng.choice(rest, size=min(4, len(rest)), replace=False))
    U = sorted(set(s0) | set(top) | set(rnd))
    import itertools
    rows = []
    for k in (3, 4, 5):
        for c in itertools.combinations(U, k):
            r = -np.ones(kmax, dtype=np.int32); r[:k] = c; rows.append(r)
    B = np.array(rows, dtype=np.int32)
    lp, Q, sz = batched_logpi(d, B)
    parts.append(B); lps.append(lp); Qs.append(Q); szs.append(sz)
    return np.vstack(parts), np.concatenate(lps), np.concatenate(Qs), np.concatenate(szs), U

def sample_posterior(d, idx, lp, Q, ndraw, rng):
    """returns bstd draws (ndraw, q) standardised beta (zeros outside S), sigma2 std-scale (ndraw,), model ids"""
    n = d.n
    pr = np.exp(lp - lp.max()); pr /= pr.sum()
    mid = rng.choice(len(lp), size=ndraw, p=pr)
    uid, inv = np.unique(mid, return_inverse=True)
    sub = idx[uid]                      # (u,k)
    kk = int((sub >= 0).sum(1).max()) if len(sub) else 0
    kk = max(kk, 1)
    sub = np.sort(np.where(sub >= 0, sub, 10 ** 9), axis=1)[:, :kk]
    sub = np.where(sub == 10 ** 9, -1, sub)
    mask = sub >= 0
    ii = np.where(mask, sub, 0)
    Gs = np.where(mask[:, :, None] & mask[:, None, :], d.G[ii[:, :, None], ii[:, None, :]], 0.0)
    H = (n + 1) * Gs + np.eye(kk)
    zs = np.where(mask, d.z[ii], 0.0)
    mean = n * np.linalg.solve(H, zs[:, :, None])[:, :, 0]
    L = np.linalg.cholesky(H)
    Linv = np.linalg.inv(L)             # H^{-1} = Linv^T Linv ; cov factor: Linv^T
    sig2 = 1.0 / rng.gamma(A0 + n / 2, 1.0 / (B0 + Q[mid] / 2))
    eps = rng.standard_normal((ndraw, kk))
    noise = np.einsum('dji,dj->di', Linv[inv], eps)      # Linv^T eps
    bet = mean[inv] + np.sqrt(n * sig2)[:, None] * noise
    bet = np.where(mask[inv], bet, 0.0)
    B = np.zeros((ndraw, d.q))
    rows = np.repeat(np.arange(ndraw), kk).reshape(ndraw, kk)
    mm = mask[inv]
    B[rows[mm], sub[inv][mm]] = bet[mm]
    return B, sig2, mid

# ---------------------------------------------------------------- distances
def h2_vec(a_over, v, w):
    """Hellinger^2 between N(a,v) and N(0,w): arrays broadcastable, Delta=a"""
    return 1 - np.sqrt(2 * np.sqrt(v * w) / (v + w)) * np.exp(-a_over ** 2 / (4 * (v + w)))

def distances(d, B, sig2, bstar, Xfresh, ndraw):
    """B std betas (ndraw,q). Returns dict of arrays over draws."""
    n, p0 = d.n, d.p0
    v = d.sy ** 2 * sig2                              # (ndraw,)
    braw = np.zeros((ndraw, p0))
    braw[:, d.keep] = d.sy * B / d.sd
    a = d.ybar - braw @ d.xbar0                       # (ndraw,)
    delta = braw - bstar[None, :]                     # (ndraw,p0)
    w = SIG_STAR ** 2
    c = np.sqrt(2 * np.sqrt(v * w) / (v + w))         # (ndraw,)
    inv4 = 1.0 / (4 * (v + w))
    # in-sample (n rows) : need raw X rows -> stored on d.Xraw
    Delta_in = d.Xraw @ delta.T + a[None, :]          # (n,ndraw)
    h2_in = 1 - c * np.exp(-Delta_in ** 2 * inv4).mean(0)
    tbar = np.minimum(1.0, Delta_in ** 2 / (4 * w)).mean(0)
    # fresh
    cols = np.where((np.abs(delta).sum(0) > 0))[0]
    Xf = Xfresh[:, cols].astype(np.float32)
    dl = delta[:, cols].astype(np.float32)
    d2 = np.empty(ndraw); dmean = np.empty(ndraw)
    for s in range(0, ndraw, MCHUNK):
        sl = slice(s, s + MCHUNK)
        D = Xf @ dl[sl].T + a[sl].astype(np.float32)[None, :]
        D2 = D * D
        E = np.exp(-D2 * inv4[sl].astype(np.float32)[None, :])
        d2[sl] = 1 - c[sl] * E.mean(0, dtype=np.float64)
        np.minimum(D2 * np.float32(1 / (4 * w)), np.float32(1.0), out=D2)
        dmean[sl] = D2.mean(0, dtype=np.float64)
    return dict(d2=d2, h2in=h2_in, tbar=tbar, dmean=dmean, v=v)
