"""W3-PSHARP numerics: shared helpers. The coded target pi exactly as in W3-POST STATEMENT section 0:
X, y centred and scaled to ||.||^2 = n-1; H = (n+1)G + I, A = G + I, Q = y'y - n z'H^{-1}z, nu = 0.01 + n/2,
b0 = 0.01, log m(S) = -0.5(logdet H - logdet A) - nu log(2 b0 + Q) (+ const), log w(k) = -log 2 - log C(2p-1, k),
K = min(p, n // 2).  Run scripts with:  py -3.13 -I <script>.py
"""
import math, itertools
import numpy as np

B0 = 0.01


def lchoose(a, k):
    return math.lgamma(a + 1) - math.lgamma(k + 1) - math.lgamma(a - k + 1)


def logw(p, k):
    return -math.log(2.0) - lchoose(2 * p - 1, k)


def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0)
    X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    y = yr - yr.mean()
    y = y / np.sqrt((y ** 2).sum() / (n - 1))
    return X, y


def log_score(X, y, S):
    """log of w(|S|) D_S^{-1/2} (2 b0 + Q_S)^{-nu}; also returns (logD, Q). Generic dense linear algebra."""
    n, p = X.shape
    nu = 0.01 + n / 2
    S = list(S)
    k = len(S)
    if k == 0:
        logD, Q = 0.0, float(y @ y)
    else:
        XS = X[:, S]
        G = XS.T @ XS
        z = XS.T @ y
        H = (n + 1) * G + np.eye(k)
        A = G + np.eye(k)
        logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(A)[1]
        Q = float(y @ y - n * z @ np.linalg.solve(H, z))
    return logw(p, k) - 0.5 * logD - nu * math.log(2 * B0 + Q), logD, Q


def enumerate_posterior(X, y):
    """All models S in Omega with their log scores (dict frozenset -> log score), by brute force."""
    n, p = X.shape
    K = min(p, n // 2)
    out = {}
    for k in range(K + 1):
        for S in itertools.combinations(range(p), k):
            out[frozenset(S)] = log_score(X, y, S)[0]
    return out


def logsumexp(a):
    a = np.asarray(a, dtype=float)
    m = a.max()
    return m + math.log(np.exp(a - m).sum())


def odds_against(post, S0):
    """delta/(1-delta) = sum_{S != S0} pi(S)/pi(S0), from an enumerate_posterior dict."""
    S0 = frozenset(S0)
    l0 = post[S0]
    rest = [v - l0 for s, v in post.items() if s != S0]
    return math.exp(logsumexp(rest))


def c_const(p, s):
    return (s + 1) * (p - s) / (2 * p - 1 - s)


def O_lb(n, p, s0):
    """The explicit lower bound of Corollary B: sum_{j=1}^{K-s0} C(s0+j, j) n^{-j/2} prod_{i<j} (p-s0-i)/(2p-1-s0-i)."""
    K = min(p, n // 2)
    tot, logterm = 0.0, 0.0
    for j in range(1, K - s0 + 1):
        i = j - 1
        logterm += math.log((s0 + j) / j) - 0.5 * math.log(n) + math.log((p - s0 - i) / (2 * p - 1 - s0 - i))
        tot += math.exp(logterm)
    return tot


def Lambda(n, p, s0, N):
    return (s0 + 1) * (2 * N / (2 * p - 1 - s0)) * math.sqrt(math.log(N) / (math.pi * n))
