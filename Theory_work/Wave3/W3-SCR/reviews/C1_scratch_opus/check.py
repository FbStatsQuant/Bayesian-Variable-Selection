"""C1 council (Opus seat): independent spot checks of L1, L4, L5 facts, L7 gap identity, L6 criterion."""
import numpy as np
from math import lgamma, log, sqrt
rng = np.random.default_rng(7)

def std(X):
    X = X - X.mean(0); return X / np.sqrt((X**2).sum(0) / (X.shape[0] - 1))

def lchoose(a, k): return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)

def F(S, X, y):
    n, p = X.shape; S = sorted(S); nu = 0.01 + n / 2
    lw = -log(2) - lchoose(2 * p - 1, len(S))
    if not S: return lw - nu * log(0.02 + y @ y), y @ y
    XS = X[:, S]; G = XS.T @ XS; z = XS.T @ y
    H = (n + 1) * G + np.eye(len(S)); Q = y @ y - n * z @ np.linalg.solve(H, z)
    return lw - 0.5 * np.linalg.slogdet(H)[1] + 0.5 * np.linalg.slogdet(G + np.eye(len(S)))[1] - nu * log(0.02 + Q), Q

def R(S, X, lam):
    n = X.shape[0]
    if not S: return np.eye(n)
    XS = X[:, sorted(S)]; return np.eye(n) - XS @ np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), XS.T)

worst = dict(onestep=0, Dlow=0, Dhigh=0, L40=-1e9, B2o=-1e9, facta=0, omega=-1e9, dual=0)
for trial in range(300):
    n = int(rng.integers(8, 40)); p = int(rng.integers(3, 9)); K = min(p, n // 2)
    rho = rng.uniform(-0.3, 0.9)
    Z = rng.standard_normal((n, p)); Z = Z + rho * rng.standard_normal((n, 1))
    X = std(Z); lam0 = 1 / (n + 1); nu = 0.01 + n / 2
    s0 = int(rng.integers(1, min(3, p) + 1)); S0 = list(rng.choice(p, s0, replace=False))
    th = np.zeros(p); th[S0] = rng.choice([-1, 1], s0) * rng.uniform(0.05, 1.0, s0)
    mu = X @ th; sig = rng.uniform(0.3, 2.0)
    yc = mu + sig * rng.standard_normal(n); yc -= yc.mean(); tau2 = yc @ yc / (n - 1); y = yc / np.sqrt(tau2)
    # random S, t not in S, |S| <= K-1
    k = int(rng.integers(0, K)); S = list(rng.choice(p, k, replace=False)); t = int(rng.choice([j for j in range(p) if j not in S]))
    RS = R(S, X, lam0); a = X[:, t] @ RS @ X[:, t] + lam0; a1 = X[:, t] @ R(S, X, 1.0) @ X[:, t] + 1.0
    D = (n + 1) * a / a1
    worst['Dlow'] = min(worst['Dlow'], D - 1); worst['Dhigh'] = min(worst['Dhigh'], n + 1 - D)
    gyc = (X[:, t] @ RS @ yc) ** 2 / a
    FS, QS = F(S, X, y); FSt, _ = F(S + [t], X, y)
    qS = yc @ yc / (n + 1) + n / (n + 1) * yc @ RS @ yc
    u = n / (n + 1) * gyc / (0.02 * tau2 + qS)
    B = log((2 * p - 1 - k) / (k + 1)) + 0.5 * log(D)
    worst['onestep'] = max(worst['onestep'], abs((FSt - FS) - (-B - nu * log(1 - u))))
    # L4.0 and B2deg-type bound on S missing a truth
    if not set(S0) <= set(S):
        T = [j for j in S0 if j not in S]
        PS = np.zeros((n, n)) if not S else X[:, S] @ np.linalg.pinv(X[:, S])
        Delta = mu @ (np.eye(n) - PS) @ mu; cth = np.linalg.norm(th) / sqrt(n + 1)
        gam = max((X[:, j] @ RS @ mu) ** 2 / (X[:, j] @ RS @ X[:, j] + lam0) for j in T)
        if sqrt(Delta) >= cth:
            lb = Delta * (sqrt(Delta) - cth) ** 2 / (n * np.abs(th[T]).sum() ** 2)
            worst['L40'] = max(worst['L40'], (lb - gam) / max(gam, 1e-300))
        v = X[:, T] @ th[T]; kap = (v @ (np.eye(n) - PS) @ v) / ((n - 1) * th[T] @ th[T])
        tmin = np.abs(th[S0]).min()
        if sqrt(kap * (n - 1)) * tmin >= 2 * cth and kap > 0:
            sS2 = sig**2 + mu @ RS @ mu / (n - 1)
            lb2 = ((n - 1)**2 / n) * kap**2 * tmin**2 / (4 * sig**2 + 9 * kap * s0 * tmin**2)
            worst['B2o'] = max(worst['B2o'], (lb2 - gam / sS2) / (gam / sS2))
    # L5 facts on a strict superset
    E = [j for j in range(p) if j not in S0]
    if len(E) >= 2 and s0 + 2 <= K:
        Ex = list(rng.choice(E, 2, replace=False)); Sup = S0 + Ex
        Xt = np.vstack([X, sqrt(lam0) * np.eye(p)])
        A0 = Xt[:, S0]; P0 = A0 @ np.linalg.solve(A0.T @ A0, A0.T)
        W = (np.eye(n + p) - P0) @ Xt[:, Ex]; M = W.T @ W; Mi = np.linalg.inv(M)
        for jj, j in enumerate(Ex):
            rest = [i for i in Sup if i != j]
            aj = X[:, j] @ R(rest, X, lam0) @ X[:, j] + lam0
            worst['facta'] = max(worst['facta'], abs(1 / Mi[jj, jj] - aj) / aj)
        N = np.diag(1 / np.sqrt(np.diag(Mi))); om = np.linalg.eigvalsh(N @ Mi @ N).max()
        GS = X[:, Sup].T @ X[:, Sup]; phi = min(1.0, np.linalg.eigvalsh(GS).min() / (n - 1))
        worst['omega'] = max(worst['omega'], om - 1 / phi)
        # dual basis: sum_j (u_j' v)^2 <= omega |P_W v|^2
        vv = rng.standard_normal(n + p); PW = W @ np.linalg.solve(M, W.T)
        s = 0
        for j in Ex:
            rest = [i for i in Sup if i != j]; Ar = Xt[:, rest]; Pr = Ar @ np.linalg.solve(Ar.T @ Ar, Ar.T)
            uj = (np.eye(n + p) - Pr) @ Xt[:, j]; uj /= np.linalg.norm(uj); s += (uj @ vv) ** 2
        worst['dual'] = max(worst['dual'], s - om * vv @ PW @ vv)
print(worst)

# L6 exact criterion at the empty model
bad = 0
for trial in range(500):
    n = int(rng.integers(6, 60)); p = int(rng.integers(2, 10)); X = std(rng.standard_normal((n, p)))
    yc = rng.standard_normal(n) + X[:, 0] * rng.uniform(0, 1); yc -= yc.mean(); tau2 = yc @ yc / (n - 1); y = yc / sqrt(tau2)
    L = 2 * log(2 * p - 1) + log(n); Bn = (n + 1) / n * (n - 0.98) * (1 - np.exp(-L / (n + 0.02)))
    F0, _ = F([], X, y)
    for j in range(p):
        g = (X[:, j] @ yc) ** 2 * (n + 1) / n**2
        Fj, _ = F([j], X, y)
        if (Fj <= F0) != (g <= tau2 * Bn): bad += 1
print('L6 criterion mismatches', bad)
