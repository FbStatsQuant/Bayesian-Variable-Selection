"""O-SWAP library: exact g-prior / BB(1,p) score F(S) of 00_COMMON.md and
vectorised one-move neighbourhood scores around S0 (adds, drops, swaps).
Indices are 0-based internally; R files are 1-based."""
import numpy as np
from scipy.special import gammaln
import rdata

A0 = B0 = 0.01
STUDY = "/home/fb31/ls0_work/study_mt"
SCALE_COL = {"c100": 0, "c075": 1, "c050": 2, "c035": 3, "c025": 4}


def load(p, s, r):
    di = rdata.read_rds(f"{STUDY}/inputs/p{p:04d}/p{p:04d}_S{s}_r{r:03d}.rds")
    dt = rdata.read_rds(f"{STUDY}/truth/p{p:04d}/p{p:04d}_S{s}_r{r:03d}.rds")
    X = np.asarray(di["X"], float)
    Y = np.asarray(di["Y"], float)
    act = np.asarray(dt["active"], int) - 1
    beta = np.asarray(dt["beta"], float)
    return X, Y, act, beta, np.asarray(dt["eps"], float)


def standardise(X, yraw):
    """00_COMMON §1: centred X with ||x_j||^2 = n-1, y = C y / s_y."""
    n = X.shape[0]
    Xc = X - X.mean(0)
    Xc = Xc / np.sqrt((Xc ** 2).sum(0) / (n - 1))
    yc = yraw - yraw.mean()
    sy = np.sqrt((yc ** 2).sum() / (n - 1))
    return Xc, yc / sy, sy


def log_prior_table(p, n):
    K = min(p, n // 2)
    k = np.arange(K + 1)
    lw = np.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lC = gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1)
    lWK = np.logaddexp.reduce(lC + lw)
    return lw - lWK  # log varpi for a model of size k


def log_C(n):
    nu = A0 + n / 2
    return A0 * np.log(2 * B0) + gammaln(nu) - (n / 2) * np.log(np.pi) - gammaln(A0)


def F_exact(X, y, S, lprior):
    n = X.shape[0]
    nu = A0 + n / 2
    S = np.asarray(S, int)
    k = len(S)
    if k == 0:
        Q = y @ y
        return lprior[0] + log_C(n) - nu * np.log(2 * B0 + Q)
    XS = X[:, S]
    G = XS.T @ XS
    z = XS.T @ y
    H = (n + 1) * G + np.eye(k)
    ldH = np.linalg.slogdet(H)[1]
    ldG = np.linalg.slogdet(G + np.eye(k))[1]
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    return lprior[k] + log_C(n) - 0.5 * (ldH - ldG) - nu * np.log(2 * B0 + Q)


class Neighbourhood:
    """Precomputes, for fixed X and S0, everything needed to score all
    one-move neighbours of S0 for any y (only z = X'y changes with y)."""

    def __init__(self, X, S0, lprior):
        self.X = X
        n, p = X.shape
        self.n, self.p = n, p
        self.S0 = np.asarray(S0, int)
        s0 = len(S0)
        self.s0 = s0
        self.lprior = lprior
        self.nulls = np.setdiff1d(np.arange(p), self.S0)
        XS = X[:, self.S0]
        G0 = XS.T @ XS
        self.H0 = (n + 1) * G0 + np.eye(s0)
        self.Gi0 = G0 + np.eye(s0)
        self.H0inv = np.linalg.inv(self.H0)
        self.Gi0inv = np.linalg.inv(self.Gi0)
        self.ldH0 = np.linalg.slogdet(self.H0)[1]
        self.ldG0 = np.linalg.slogdet(self.Gi0)[1]
        C = XS.T @ X[:, self.nulls]           # s0 x m cross-products
        self.C = C
        gll = (X[:, self.nulls] ** 2).sum(0)   # = n-1
        # --- adds: Schur complements
        hT = (n + 1) * C
        self.sH_add = (n + 1) * gll + 1 - np.einsum('im,ij,jm->m', hT, self.H0inv, hT)
        self.sG_add = gll + 1 - np.einsum('im,ij,jm->m', C, self.Gi0inv, C)
        self.hT_add = hT
        # --- drops and swaps: per removed j, T = S0 - j
        self.drop = []
        for jj in range(s0):
            keep = np.delete(np.arange(s0), jj)
            HT = self.H0[np.ix_(keep, keep)]
            GT = self.Gi0[np.ix_(keep, keep)]
            HTi = np.linalg.inv(HT)
            GTi = np.linalg.inv(GT)
            ldHT = np.linalg.slogdet(HT)[1]
            ldGT = np.linalg.slogdet(GT)[1]
            CT = C[keep]
            hTl = (n + 1) * CT
            sH = (n + 1) * gll + 1 - np.einsum('im,ij,jm->m', hTl, HTi, hTl)
            sG = gll + 1 - np.einsum('im,ij,jm->m', CT, GTi, CT)
            self.drop.append(dict(keep=keep, HTi=HTi, ldHT=ldHT, ldGT=ldGT,
                                  hTl=hTl, sH=sH, sG=sG))

    def scores(self, y):
        """Return F(S0), F(S0+l) [m], F(S0-j) [s0], F(S0-j+l) [s0 x m] (all exact)."""
        n, s0 = self.n, self.s0
        nu = A0 + n / 2
        lc = log_C(n)
        lp = self.lprior
        X = self.X
        zS = X[:, self.S0].T @ y
        zl = X[:, self.nulls].T @ y
        yy = y @ y
        q0 = zS @ self.H0inv @ zS
        Q0 = yy - n * q0
        F0 = lp[s0] + lc - 0.5 * (self.ldH0 - self.ldG0) - nu * np.log(2 * B0 + Q0)
        # adds
        resid = zl - self.hT_add.T @ (self.H0inv @ zS)
        Qa = Q0 - n * resid ** 2 / self.sH_add
        Fa = (lp[s0 + 1] + lc - 0.5 * (self.ldH0 + np.log(self.sH_add) - self.ldG0 - np.log(self.sG_add))
              - nu * np.log(2 * B0 + Qa))
        Fd = np.empty(s0)
        Fs = np.empty((s0, len(self.nulls)))
        for jj, d in enumerate(self.drop):
            zT = zS[d['keep']]
            w = d['HTi'] @ zT
            qT = zT @ w
            QT = yy - n * qT
            Fd[jj] = lp[s0 - 1] + lc - 0.5 * (d['ldHT'] - d['ldGT']) - nu * np.log(2 * B0 + QT)
            res = zl - d['hTl'].T @ w
            Qs = QT - n * res ** 2 / d['sH']
            Fs[jj] = (lp[s0] + lc - 0.5 * (d['ldHT'] + np.log(d['sH']) - d['ldGT'] - np.log(d['sG']))
                      - nu * np.log(2 * B0 + Qs))
        return F0, Fa, Fd, Fs
