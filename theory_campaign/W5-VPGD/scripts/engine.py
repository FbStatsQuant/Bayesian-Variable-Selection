"""W5-VPGD neighbour engine (numpy only; written independently of W3-PGD's pgd_core.py).

For a Gram matrix G (c x c), response cross-products B (c x r), response second moments v (r,), and a ridge lam,
the engine evaluates, for a batch of states S (sorted index tuples of a common size s), the ridge residual

    v_S[k]   = v[k] - B_S[:,k]' (G_SS + lam I)^{-1} B_S[:,k]        (k = response column)
    ld_S     = log det(G_SS + lam I)

for S itself and for EVERY flip and swap neighbour of S:
    add x (x not in S), delete i (i in S), swap i -> x (i in S, x not in S).

Uses (K = (G_SS + lam I)^{-1}, W = G_{.,S} K, beta = K B_S):
    add x     : v - rc_x^2/dg_x,  ld + log dg_x,   rc = B - W B_S, dg = diag(G) + lam - rowsum(W * G_{.,S})
    delete i  : v + beta_i^2/K_ii,  ld + log K_ii
    swap i->x : from S - i: dg^(i) = dg + W_{.,i}^2/K_ii, rc^(i) = rc + W_{.,i} beta_i / K_ii.
Population use: G = Sigma, B = Sigma theta, v = theta' Sigma theta, lam = 0  -> v_S = Delta_S (normalised).
Score use: G = X'X, B = X'y, v = y'y, lam = 1/(n+1) (ridge quadratic + log det) and lam = 1 (log det only).
"""
import itertools
from math import lgamma, log
import numpy as np


class NbrEngine:
    def __init__(self, G, B, v, lam=0.0):
        self.G = np.asarray(G, float)
        self.c = self.G.shape[0]
        B = np.asarray(B, float)
        self.B = B[:, None] if B.ndim == 1 else B
        self.v = np.atleast_1d(np.asarray(v, float))
        self.lam = float(lam)
        self.dG = np.diag(self.G) + self.lam

    def eval(self, idx, want=('add', 'del', 'swap')):
        idx = np.asarray(idx, int)
        Bt, s = idx.shape
        c, r = self.c, self.B.shape[1]
        out = {}
        if s == 0:
            out['v'] = np.broadcast_to(self.v, (Bt, r)).copy()
            out['ld'] = np.zeros(Bt)
            out['add_v'] = (self.v[None, None, :] - self.B[None] ** 2 / self.dG[None, :, None]).repeat(Bt, 0)
            out['add_ld'] = np.log(self.dG)[None, :].repeat(Bt, 0)
            out['inS'] = np.zeros((Bt, c), bool)
            return out
        Gs = self.G[idx[:, :, None], idx[:, None, :]] + self.lam * np.eye(s)[None]
        K = np.linalg.inv(Gs)
        sign, ld = np.linalg.slogdet(Gs)
        GcS = np.transpose(self.G[idx], (0, 2, 1))           # (Bt, c, s)
        W = GcS @ K                                          # (Bt, c, s)
        dg = self.dG[None, :] - np.einsum('bcs,bcs->bc', W, GcS)
        bS = self.B[idx]                                     # (Bt, s, r)
        beta = K @ bS                                        # (Bt, s, r)
        rc = self.B[None] - W @ bS                           # (Bt, c, r)
        vS = self.v[None, :] - np.einsum('bsr,bsr->br', bS, beta)
        inS = np.zeros((Bt, c), bool)
        np.put_along_axis(inS, idx, True, axis=1)
        out.update(v=vS, ld=ld, inS=inS)
        if 'add' in want:
            dgm = np.where(inS, np.nan, dg)
            out['add_v'] = vS[:, None, :] - rc ** 2 / dgm[..., None]
            out['add_ld'] = ld[:, None] + np.log(dgm)
        Kii = np.einsum('bss->bs', K)
        vdel = vS[:, None, :] + beta ** 2 / Kii[..., None]
        lddel = ld[:, None] + np.log(Kii)
        if 'del' in want:
            out['del_v'] = vdel
            out['del_ld'] = lddel
        if 'swap' in want:
            Wt = np.transpose(W, (0, 2, 1))                  # (Bt, s, c)
            dgi = dg[:, None, :] + Wt ** 2 / Kii[..., None]  # (Bt, s, c)
            dgi = np.where(inS[:, None, :], np.nan, dgi)
            rci = rc[:, None, :, :] + Wt[..., None] * (beta / Kii[..., None])[:, :, None, :]
            out['swap_v'] = vdel[:, :, None, :] - rci ** 2 / dgi[..., None]
            out['swap_ld'] = lddel[:, :, None] + np.log(dgi)
        return out


# ----------------------------------------------------------------------------------------- region helpers
def region_states(truth, extras, a, d, amin=0):
    """All S = U u P with U subset of truth, amin <= |truth \\ U| <= a, P subset of extras, |P| <= d.
    Yields dict size -> list of (sorted tuple, m, e)."""
    truth = list(truth)
    by = {}
    for m in range(amin, a + 1):
        for miss in itertools.combinations(truth, m):
            U = [t for t in truth if t not in miss]
            for e in range(d + 1):
                for P in itertools.combinations(extras, e):
                    S = tuple(sorted(U + list(P)))
                    by.setdefault(len(S), []).append((S, m, e))
    return by


def lchoose(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


def log_prior(k, p, K):
    """log w(k) = log(1/2) - log C(2p-1, k) for k <= K, -inf otherwise (the common W_K is dropped)."""
    k = np.asarray(k)
    out = np.where(k <= K, -log(2.0) - np.vectorize(lambda kk: lchoose(2.0 * p - 1, kk))(np.minimum(k, K)), -np.inf)
    return out


class Scorer:
    """Exact log posterior score F(S) (up to a common constant) for standardised X (n x p) and y, 00_COMMON:
    F = log w(|S|) - 1/2 log D_S - nu log(2 b0 + Q_S),  D_S = det((n+1)G+I)/det(G+I),
    Q_S = y'y - n z'((n+1)G+I)^{-1} z.  Via the ridge engines: Q_S = y'y/(n+1) + n/(n+1) rho_lam(S),
    log D_S = s log(n+1) + logdet(G_S + lam I) - logdet(G_S + I), lam = 1/(n+1)."""

    def __init__(self, X, Y, a0=0.01, b0=0.01):
        n, p = X.shape
        self.n, self.p = n, p
        self.K = min(p, n // 2)
        G = X.T @ X
        Y = np.atleast_2d(Y.T).T if Y.ndim == 1 else Y
        self.yy = np.sum(Y ** 2, 0)
        lam = 1.0 / (n + 1)
        self.E1 = NbrEngine(G, X.T @ Y, self.yy, lam=lam)
        self.E2 = NbrEngine(G, np.zeros((p, 1)), np.zeros(1), lam=1.0)
        self.nu = a0 + n / 2.0
        self.b0 = b0
        self.lw = np.array([(-log(2.0) - lchoose(2.0 * p - 1, k)) if k <= self.K else -np.inf for k in range(p + 2)])

    def _F(self, rho, ld1, ld2, size):
        n = self.n
        Q = self.yy / (n + 1) + (n / (n + 1)) * rho
        logD = size[..., None] * log(n + 1) + ld1[..., None] - ld2[..., None]
        return self.lw[size][..., None] - 0.5 * logD - self.nu * np.log(2 * self.b0 + Q)

    def eval(self, idx):
        idx = np.asarray(idx, int)
        Bt, s = idx.shape
        o1 = self.E1.eval(idx)
        o2 = self.E2.eval(idx)
        out = {'inS': o1['inS']}
        sz = np.full(Bt, s)
        out['F'] = self._F(o1['v'], o1['ld'], o2['ld'], sz)
        out['add'] = self._F(o1['add_v'], o1['add_ld'], o2['add_ld'], np.full((Bt, self.p), s + 1))
        if s > 0:
            out['del'] = self._F(o1['del_v'], o1['del_ld'], o2['del_ld'], np.full((Bt, s), s - 1))
            out['swap'] = self._F(o1['swap_v'], o1['swap_ld'], o2['swap_ld'], np.full((Bt, s, self.p), s))
        return out


def F_direct(X, y, S, a0=0.01, b0=0.01):
    """Brute-force score (same additive constant convention as Scorer)."""
    n, p = X.shape
    K = min(p, n // 2)
    S = list(S)
    s = len(S)
    if s > K:
        return -np.inf
    lw = -log(2.0) - lchoose(2.0 * p - 1, s)
    yy = y @ y
    if s == 0:
        return lw - (a0 + n / 2) * log(2 * b0 + yy)
    XS = X[:, S]
    G = XS.T @ XS
    z = XS.T @ y
    H = (n + 1) * G + np.eye(s)
    logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(s))[1]
    Q = yy - n * z @ np.linalg.solve(H, z)
    return lw - 0.5 * logD - (a0 + n / 2) * log(2 * b0 + Q)
