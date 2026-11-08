"""Shared helpers for the W1-PXN numerics (LH-iid design, score F, tee output).  ASCII only."""
import os
import numpy as np
from scipy.special import gammaln

HERE = os.path.dirname(os.path.abspath(__file__))
B0 = 0.01


class Tee:
    def __init__(self, name):
        self.path = os.path.join(HERE, name)
        self.lines = []

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.lines.append(s)

    def close(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")


# ---------------------------------------------------------------- LH-iid design
def build_sigma(p, g, c, rho, psi):
    """Population covariance: equicorrelation rho inside groups, linked pairs (2i,2i+1) via rank-one hub link."""
    Sigma = np.eye(p)
    G = p // g
    A = (1 - rho) * np.eye(g) + rho * np.ones((g, g))
    for h in range(G):
        Sigma[h * g:(h + 1) * g, h * g:(h + 1) * g] = A
    u = np.full(g, rho)
    u[0] = 1.0
    for i in range(c):
        a, b = 2 * i, 2 * i + 1
        blk = psi[i] * np.outer(u, u)
        Sigma[a * g:(a + 1) * g, b * g:(b + 1) * g] = blk
        Sigma[b * g:(b + 1) * g, a * g:(a + 1) * g] = blk.T
    return Sigma


def build_theta(p, g, c, v, psi, beta, betavis):
    th = np.zeros(p)
    for i in range(c):
        th[2 * i * g] = beta[i]
        th[(2 * i + 1) * g] = -psi[i] * beta[i]
    for h in range(v):
        th[(2 * c + h) * g] = betavis[h]
    return th


def draw_raw(rng, n, L, theta, sigma=1.0):
    p = L.shape[0]
    Xr = rng.standard_normal((n, p)) @ L.T
    yr = Xr @ theta + sigma * rng.standard_normal(n)
    return Xr, yr


def standardise(Xr, yr):
    """Return X (centred, col norm^2 = n-1), y (centred, norm^2 = n-1), Y = C y^r, mu = C X^r theta handled by caller."""
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(0)
    X = Xc / np.linalg.norm(Xc, axis=0) * np.sqrt(n - 1)
    Y = yr - yr.mean()
    y = Y / np.linalg.norm(Y) * np.sqrt(n - 1)
    return X, y, Y, Xc


# ---------------------------------------------------------------- score
def log_w(k, p):
    """log w(k) = log 0.5 - log binom(2p-1, k)."""
    N = 2 * p - 1
    return np.log(0.5) - (gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1))


class Scorer:
    """Scores log m(S) (const dropped) and F(S) for a standardised (X, y)."""

    def __init__(self, X, y):
        self.n = X.shape[0]
        self.p = X.shape[1]
        self.Gram = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)
        self.nu = 0.01 + self.n / 2.0

    def parts(self, S):
        S = list(S)
        k = len(S)
        n = self.n
        if k == 0:
            return dict(logD=0.0, Q=self.yy, G=np.zeros((0, 0)), z=np.zeros(0), H=np.zeros((0, 0)))
        G = self.Gram[np.ix_(S, S)]
        z = self.z[S]
        I = np.eye(k)
        H = (n + 1) * G + I
        logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + I)[1]
        Q = self.yy - n * float(z @ np.linalg.solve(H, z))
        return dict(logD=logD, Q=Q, G=G, z=z, H=H)

    def logm(self, S):
        pr = self.parts(S)
        return -0.5 * pr["logD"] - self.nu * np.log(2 * B0 + pr["Q"])

    def F(self, S):
        return log_w(len(S), self.p) + self.logm(S)


def proj_resid(v, M):
    """v - P_M v via QR (M may have 0 columns)."""
    if M.shape[1] == 0:
        return v.copy()
    Q, _ = np.linalg.qr(M)
    return v - Q @ (Q.T @ v)
