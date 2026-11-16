"""W3-AUDIT track C -- designs D01-D19 (C_PLAN.md v3 §1).

Each design is an object with
  sigma_rows(idx)  -> Sigma[idx, :]  (len(idx) x p, unit diagonal)   [population Gram oracle]
  sigma_matvec(v)  -> Sigma @ v                                       [for P10 and lambda_min(Sigma)]
  draw(n, rng)     -> X (n x p), rows iid N(0, Sigma)
  lam_min_pop()    -> lambda_min(Sigma) (exact certificate for every population sparse floor)
plus the two truth placements (spread / clustered).  Python port of the plan's R recipe: the RNG stream differs from
gen_dev_data.R (numpy PCG64 seeded with seed = BASE + 10000*design + rep), the covariances are the same formulas.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_WAVE2 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Wave2"))
LDIR = os.environ.get("C_LDIR", os.path.join(REPO_WAVE2, "W2-SIM", "X", "data"))   # NOTS: the frozen data/ copy
BASE_SEED = 31160000          # track C base; seed = BASE + 10000 * design + rep (plan §1)
S0 = 4
BETA_SPREAD = np.array([1.4, -1.0, 1.8, -1.2])
BETA_CLUST = np.array([1.4, 1.0, 1.8, 1.2])


def _toeplitz_eig(t):
    """Eigenvalues of the minimal circulant embedding of the symmetric Toeplitz sequence t (length p)."""
    c = np.concatenate([t, t[-2:0:-1]])
    lam = np.fft.fft(c).real
    return lam


class Design:
    did = 0
    name = ""

    def __init__(self, p):
        self.p = int(p)

    # ---- placements ------------------------------------------------------------------------------------------------
    def spread(self):
        step = self.p // S0
        return np.arange(S0) * step, BETA_SPREAD.copy()

    def clustered(self):
        return np.arange(S0), BETA_CLUST.copy()

    def placements(self):
        return {"spread": self.spread(), "clustered": self.clustered()}

    # ---- generic helpers -------------------------------------------------------------------------------------------
    def lam_min_pop(self):
        p = self.p
        if p <= 3000:
            S = self.sigma_rows(np.arange(p))
            return float(np.linalg.eigvalsh(S)[0])
        from scipy.sparse.linalg import LinearOperator, eigsh
        op = LinearOperator((p, p), matvec=self.sigma_matvec, dtype=float)
        # smallest eigenvalue via the largest of (c I - Sigma), c = an upper bound on lambda_max
        lmax = eigsh(op, k=1, which="LA", tol=1e-6, return_eigenvectors=False)[0]
        c = lmax * 1.01
        op2 = LinearOperator((p, p), matvec=lambda v: c * v - self.sigma_matvec(v), dtype=float)
        top = eigsh(op2, k=1, which="LA", tol=1e-8, return_eigenvectors=False, maxiter=20000)[0]
        return float(c - top)


class Toeplitz(Design):
    """Sigma_jk = t(|j-k|); sampled by circulant embedding (exact when the embedding is PSD, checked)."""

    def __init__(self, p, t):
        super().__init__(p)
        self.t = np.asarray(t, float)
        self.lam = _toeplitz_eig(self.t) if p > 1 else np.array([1.0])
        if self.lam.min() < -1e-8 * self.lam.max():
            raise ValueError("circulant embedding not PSD")
        self.lam = np.maximum(self.lam, 0.0)

    def sigma_rows(self, idx):
        idx = np.atleast_1d(idx)
        return self.t[np.abs(idx[:, None] - np.arange(self.p)[None, :])]

    def sigma_matvec(self, v):
        m = len(self.lam)
        vv = np.zeros(m); vv[:self.p] = v
        return np.fft.ifft(self.lam * np.fft.fft(vv)).real[:self.p]

    def lam_min_pop(self):
        """p <= 3000: exact (dense).  Otherwise the minimum of the symbol f_p(w) = t0 + 2 sum_{h<p} t_h cos(h w) on a
        fine grid: every eigenvalue of T_p lies in [min f_p, max f_p], so this is a lower bound (certificate)."""
        if self.p <= 3000:
            return Design.lam_min_pop(self)
        m = 1 << 20
        c = np.zeros(m); c[:self.p] = self.t; c[0] = 0.5 * self.t[0]
        f = 2 * np.fft.fft(c).real
        return float(f.min())

    def draw(self, n, rng):
        p = self.p
        if p == 1:
            return rng.standard_normal((n, 1))
        m = len(self.lam)
        out = np.empty((n, p))
        sq = np.sqrt(self.lam / m)
        i = 0
        while i < n:                                           # each complex draw gives two independent rows
            w = rng.standard_normal(m) + 1j * rng.standard_normal(m)
            y = np.fft.fft(sq * w)
            out[i] = y.real[:p]; i += 1
            if i < n:
                out[i] = y.imag[:p]; i += 1
        return out


class IND(Toeplitz):
    def __init__(self, p):
        Design.__init__(self, p); self.t = np.r_[1.0, np.zeros(p - 1)]

    def sigma_matvec(self, v):
        return v.copy()

    def draw(self, n, rng):
        return rng.standard_normal((n, self.p))

    def lam_min_pop(self):
        return 1.0


class AR(Toeplitz):
    def __init__(self, p, rho):
        super().__init__(p, rho ** np.arange(p)); self.rho = rho

    def draw(self, n, rng):
        p, r = self.p, self.rho
        E = rng.standard_normal((n, p))
        X = np.empty((n, p)); X[:, 0] = E[:, 0]
        s = np.sqrt(1 - r * r)
        for j in range(1, p):
            X[:, j] = r * X[:, j - 1] + s * E[:, j]
        return X


class Block(Design):
    """Block compound symmetry: x = sqrt(rho_g) f_g + sqrt(1 - rho_g) e, rho may vary by block; optional global
    factor (S5: 0.3 11' + 0.4 H + 0.3 I)."""

    def __init__(self, p, bsize, rho_of_block, glob=0.0):
        super().__init__(p)
        self.g = np.arange(p) // bsize
        self.nb = int(self.g.max()) + 1
        self.rb = np.array([rho_of_block(b) for b in range(self.nb)], float)
        self.glob = glob

    def sigma_rows(self, idx):
        idx = np.atleast_1d(idx)
        same = self.g[idx][:, None] == self.g[None, :]
        S = self.glob + same * self.rb[self.g[idx]][:, None]
        S[np.arange(len(idx)), idx] = 1.0
        return S

    def sigma_matvec(self, v):
        bs = np.bincount(self.g, weights=v, minlength=self.nb)
        out = self.rb[self.g] * bs[self.g] + (1 - self.rb[self.g] - self.glob) * v
        if self.glob:
            out += self.glob * v.sum()
        return out

    def draw(self, n, rng):
        F = rng.standard_normal((n, self.nb))
        rw = self.rb[self.g]
        X = np.sqrt(rw)[None, :] * F[:, self.g]
        if self.glob:
            X += np.sqrt(self.glob) * rng.standard_normal((n, 1))
        X += np.sqrt(1 - rw - self.glob)[None, :] * rng.standard_normal((n, self.p))
        return X

    def lam_min_pop(self):
        return float(1 - self.glob - self.rb.max()) if self.p > 1 else 1.0


class LowRank(Design):
    """Sigma = L L' + psi I with unit diagonal (factor designs and the real-data-like tilings).
    copy[j] (tiling): Sigma_jk = 0 when copy differs."""

    def __init__(self, p, Lrows, psi, copy=None):
        super().__init__(p)
        self.L = np.asarray(Lrows, float); self.psi = psi
        self.copy = np.zeros(p, int) if copy is None else np.asarray(copy)
        self.ncopy = int(self.copy.max()) + 1
        assert np.allclose((self.L ** 2).sum(1) + psi, 1.0, atol=1e-6)

    def sigma_rows(self, idx):
        idx = np.atleast_1d(idx)
        S = self.L[idx] @ self.L.T
        if self.ncopy > 1:
            S *= (self.copy[idx][:, None] == self.copy[None, :])
        S[np.arange(len(idx)), idx] = 1.0
        return S

    def sigma_matvec(self, v):
        out = self.psi * v
        for c in range(self.ncopy):
            m = self.copy == c
            out[m] += self.L[m] @ (self.L[m].T @ v[m])
        return out

    def draw(self, n, rng):
        k = self.L.shape[1]
        X = np.sqrt(self.psi) * rng.standard_normal((n, self.p))
        for c in range(self.ncopy):
            m = self.copy == c
            X[:, m] += rng.standard_normal((n, k)) @ self.L[m].T
        return X

    def lam_min_pop(self):
        if self.p <= 3000:
            return super().lam_min_pop()
        lm = self.psi
        for c in range(self.ncopy):                         # each copy: psi + lambda_min(L_c L_c') (0 if rank < size)
            Lc = self.L[self.copy == c]
            if Lc.shape[0] <= Lc.shape[1]:
                lm = min(lm, self.psi + float(np.linalg.eigvalsh(Lc @ Lc.T)[0]))
        return float(lm)


def _factor(p, a, kf):
    h = 0.5 * p ** (a - 1.0)
    j = np.arange(p)
    loads = [np.ones(p), (-1.0) ** j, (-1.0) ** (j // 5)][:kf]
    L = np.column_stack(loads) * np.sqrt(h / kf)
    return LowRank(p, L, 1 - h)


_LCACHE = {}


def _loadL(name):
    if name not in _LCACHE:
        _LCACHE[name] = np.loadtxt(os.path.join(LDIR, f"{name}_L.csv"), delimiter=",")
    return _LCACHE[name]


def _real(p, name, did):
    L0 = _loadL(name); p0 = L0.shape[0]
    if p <= p0:
        rng = np.random.default_rng(20261116 + did * 100000 + p)
        rows = np.sort(rng.permutation(p0)[:p])
        d = LowRank(p, L0[rows], 0.1)
    else:
        j = np.arange(p)
        d = LowRank(p, L0[j % p0], 0.1, copy=j // p0)
    # clustered placement: column 0 and its three most correlated partners (population)
    r0 = np.abs(d.sigma_rows(np.array([0]))[0]); r0[0] = -1
    d._clu = np.r_[0, np.argsort(-r0)[:3]]
    d.clustered = lambda: (d._clu.copy(), BETA_CLUST.copy())
    return d


DESIGNS = {
    1: ("IND", lambda p: IND(p)),
    2: ("AR0.5", lambda p: AR(p, 0.5)),
    3: ("AR0.8", lambda p: AR(p, 0.8)),
    4: ("AR0.95", lambda p: AR(p, 0.95)),
    5: ("BLK5-0.7", lambda p: Block(p, 5, lambda b: 0.7)),
    6: ("BLK5-0.85", lambda p: Block(p, 5, lambda b: 0.85)),
    7: ("BLKsqrt-0.5", lambda p: Block(p, int(np.ceil(np.sqrt(p))), lambda b: 0.5)),
    8: ("TOEP-a1", lambda p: Toeplitz(p, (1.0 + np.arange(p)) ** -1.0)),
    9: ("TOEP-a2", lambda p: Toeplitz(p, (1.0 + np.arange(p)) ** -2.0)),
    10: ("FAC-a0.5-k1", lambda p: _factor(p, 0.5, 1)),
    11: ("FAC-a0.5-k3", lambda p: _factor(p, 0.5, 3)),
    12: ("FAC-a0.75-k1", lambda p: _factor(p, 0.75, 1)),
    13: ("FAC-a0.75-k3", lambda p: _factor(p, 0.75, 3)),
    14: ("FAC-a1-k1", lambda p: _factor(p, 1.0, 1)),
    15: ("FAC-a1-k3", lambda p: _factor(p, 1.0, 3)),
    16: ("S5", lambda p: Block(p, 5, lambda b: 0.4, glob=0.3)),
    17: ("S6", lambda p: Block(p, 5, lambda b: 0.4 + 0.1 * (b % 6))),
    18: ("RIBO", lambda p: _real(p, "riboflavin", 18)),
    19: ("FREDQD", lambda p: _real(p, "fred_qd", 19)),
}


def make_design(did, p):
    name, f = DESIGNS[int(did)]
    d = f(int(p)); d.did = int(did); d.name = name
    return d


def draw_X(d, n, rep):
    rng = np.random.default_rng(BASE_SEED + 10000 * d.did + int(rep))
    return d.draw(int(n), rng)


def standardize(X):
    """Z with centred, unit-norm columns, so R_hat = Z'Z (the code's X = sqrt(n-1) Z)."""
    Z = X - X.mean(0)
    Z /= np.sqrt((Z ** 2).sum(0))
    return Z
