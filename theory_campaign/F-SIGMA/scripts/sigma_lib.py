"""F-SIGMA shared library: v3 scores on sufficient statistics, block tables (BF and common-sigma^2),
exact start normaliser by size-profile convolution, exact iid start sampler, start mode by max-plus convolution.
Notation of 00_COMMON.md: nu = a0 + n/2, c = 2 b0 + y'y, t_U = n z' H^{-1} z, D_U = det H / det(G+I),
log BF(U) = -1/2 log D_U - nu log((c - t_U)/c);  log r^C(U) = -1/2 log D_U + t_U/(2 sigma_hat^2).
Standardisation: ||x_j||^2 = ||y||^2 = n - 1 (no centering step: the data are treated as contrast coordinates)."""
import numpy as np
from itertools import combinations
from scipy.special import gammaln, logsumexp

A0 = B0 = 0.01

def log_w(k, p):
    # w(k) = 1/2 / C(2p-1, k)
    return np.log(0.5) - (gammaln(2*p) - gammaln(k+1) - gammaln(2*p-k))

def bo_design(n, blocks, rho, rng):
    """Exact block-orthogonal design: blocks are orthogonal subspaces; within block equicorrelation rho."""
    p = sum(len(b) for b in blocks)
    assert p <= n - 1
    Q, _ = np.linalg.qr(rng.standard_normal((n, p)))
    X = np.zeros((n, p))
    for b in blocks:
        m = len(b)
        R = (1-rho)*np.eye(m) + rho*np.ones((m, m))
        L = np.linalg.cholesky(R)
        X[:, b] = Q[:, b] @ L.T
    X *= np.sqrt(n-1)
    return X

def iid_design(n, p, rng):
    X = rng.standard_normal((n, p))
    X -= X.mean(0)
    X *= np.sqrt(n-1)/np.linalg.norm(X, axis=0)
    return X

def make_y(X, theta, sigma, rng):
    n = X.shape[0]
    mu = X @ theta
    y = mu + sigma*rng.standard_normal(n)
    s = np.sqrt((y @ y)/(n-1))
    return y/s, mu/s, sigma/s   # standardised y; theta, sigma on the y scale rescale by 1/s

class Scorer:
    def __init__(self, X, y):
        self.X, self.y = X, y
        self.n, self.p = X.shape
        self.G = X.T @ X
        self.z = X.T @ y
        self.yty = y @ y
        self.nu = A0 + self.n/2
        self.c = 2*B0 + self.yty
    def tD(self, U):
        """t_U and log D_U for one model U (list of indices)."""
        if len(U) == 0:
            return 0.0, 0.0
        U = list(U)
        G = self.G[np.ix_(U, U)]; z = self.z[U]
        H = (self.n+1)*G + np.eye(len(U))
        t = self.n * z @ np.linalg.solve(H, z)
        ldH = np.linalg.slogdet(H)[1]; ldA = np.linalg.slogdet(G + np.eye(len(U)))[1]
        return t, ldH - ldA
    def tD_batch(self, Us):
        """Batched: Us is an array (m, j) of index lists of equal size j >= 1."""
        Us = np.asarray(Us); m, j = Us.shape
        G = self.G[Us[:, :, None], Us[:, None, :]]            # (m, j, j)
        z = self.z[Us]                                          # (m, j)
        H = (self.n+1)*G + np.eye(j)[None]
        sol = np.linalg.solve(H, z[:, :, None])[:, :, 0]
        t = self.n * np.einsum('ij,ij->i', z, sol)
        ldH = np.linalg.slogdet(H)[1]; ldA = np.linalg.slogdet(G + np.eye(j)[None])[1]
        return t, ldH - ldA
    def logBF_from(self, t, lD):
        return -0.5*lD - self.nu*np.log((self.c - t)/self.c)
    def logrC_from(self, t, lD, s2):
        return -0.5*lD + t/(2*s2)

def block_tables(sc, block):
    """All sub-models of a block: returns dict size j -> (array of index tuples (m,j), t (m,), lD (m,))."""
    out = {0: (np.zeros((1, 0), dtype=int), np.zeros(1), np.zeros(1))}
    B = len(block)
    for j in range(1, B+1):
        Us = np.array(list(combinations(block, j)), dtype=int)
        t, lD = sc.tD_batch(Us)
        out[j] = (Us, t, lD)
    return out

class Start:
    """Composite start from per-block log tables logr[b][j] (arrays over sub-models of size j)."""
    def __init__(self, blocks, tables, logr_fun, p, K):
        self.blocks, self.p, self.K = blocks, p, K
        self.J = len(blocks)
        self.logr = []   # logr[b][j] -> array
        self.Us = []
        for b in range(self.J):
            lr = {}; us = {}
            for j, (U, t, lD) in tables[b].items():
                lr[j] = logr_fun(t, lD) if j > 0 else np.zeros(1)
                us[j] = U
            self.logr.append(lr); self.Us.append(us)
        # size profiles log e_b(j)
        self.logprof = [np.array([logsumexp(self.logr[b][j]) if j in self.logr[b] else -np.inf
                                  for j in range(K+1)]) for b in range(self.J)]
        # convolution F_b(k)
        F = np.zeros(K+1); F[1:] = -np.inf
        self.Fs = [F.copy()]
        for b in range(self.J):
            lp = self.logprof[b]
            Fn = np.full(K+1, -np.inf)
            for k in range(K+1):
                terms = [F[k-j] + lp[j] for j in range(0, min(k, len(self.blocks[b]))+1) if np.isfinite(F[k-j]) and np.isfinite(lp[j])]
                if terms: Fn[k] = logsumexp(terms)
            F = Fn; self.Fs.append(F.copy())
        lk = np.array([log_w(k, p) + F[k] for k in range(K+1)])
        self.logZbar0 = logsumexp(lk)
        self.size_logmass = lk - self.logZbar0
    def log_gamma0(self, S):
        S = set(S); tot = log_w(len(S), self.p)
        for b, blk in enumerate(self.blocks):
            U = tuple(sorted(S & set(blk))); j = len(U)
            if j == 0: continue
            Us = self.Us[b][j]
            idx = np.where((Us == np.array(U)).all(1))[0][0]
            tot += self.logr[b][j][idx]
        return tot
    def log_pi0(self, S):
        return self.log_gamma0(S) - self.logZbar0
    def mode(self):
        """argmax pi0 by max-plus convolution over per-block per-size maxima."""
        K = self.K
        best = [{} for _ in range(self.J)]
        M = np.full(K+1, -np.inf); M[0] = 0.0; back = []
        for b in range(self.J):
            mb = np.array([self.logr[b][j].max() if j in self.logr[b] else -np.inf for j in range(K+1)])
            Mn = np.full(K+1, -np.inf); arg = np.zeros(K+1, dtype=int)
            for k in range(K+1):
                cand = [(M[k-j] + mb[j], j) for j in range(0, min(k, len(self.blocks[b]))+1)]
                v, j = max(cand); Mn[k] = v; arg[k] = j
            back.append(arg); M = Mn
        tot = np.array([log_w(k, self.p) + M[k] for k in range(K+1)])
        k = int(np.argmax(tot)); S = []
        for b in range(self.J-1, -1, -1):
            j = back[b][k]
            if j > 0:
                i = int(np.argmax(self.logr[b][j])); S += list(self.Us[b][j][i])
            k -= j
        return sorted(S)
    def sample(self, rng, m):
        """m exact iid draws: total size, block sizes backwards, sub-model within size class."""
        draws = []
        sizes = rng.choice(self.K+1, size=m, p=np.exp(self.size_logmass)/np.exp(self.size_logmass).sum())
        for k in sizes:
            S = []
            for b in range(self.J-1, -1, -1):
                lp = self.logprof[b]; F = self.Fs[b]
                js = np.arange(0, min(k, len(self.blocks[b]))+1)
                lw = np.array([F[k-j] + lp[j] for j in js])
                w = np.exp(lw - logsumexp(lw)); j = int(rng.choice(js, p=w/w.sum()))
                if j > 0:
                    lr = self.logr[b][j]; w2 = np.exp(lr - logsumexp(lr))
                    i = int(rng.choice(len(lr), p=w2/w2.sum())); S += list(self.Us[b][j][i])
                k -= j
            draws.append(tuple(sorted(S)))
        return draws

def psi(u):
    return u - 1 - np.log(u)
