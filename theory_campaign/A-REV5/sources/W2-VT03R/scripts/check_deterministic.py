#!/usr/bin/env python3
"""W2-VT03R: stress tests of the deterministic steps that W1-T03R changed, on random small designs
(iid, equicorrelated 0.9, and near-collinear designs with one pair at correlation 1 - 1/n), exhaustive over models.

Checked (contrast coordinates; X_c is N x p with column norms^2 = N; y_c arbitrary or model-drawn):
 [B3]  S subset T, S empty or g_S = lambda_min(G_S) > 0:
       u'(M_T - M_S)u <= n/(n+1) [ ||(P_T - P_S)u||^2 + eta_S ||P_S u||^2 ],  eta_S = 1/((n+1) g_S)      (W1 Lemma B(B3))
 [C6a] every underfitting S, S' = S u S0, every rate b > 0:  ell(S)/ell(S') <= (2p)^{|J|} (n+1)^{|J|/2}   (no eigen condition)
 [B1]  D_{S0 u J}/D_{S0} >= f(g)^{|J|} >= [(n+1)/(1+1/g)]^{|J|},  g = lambda_min(G_{S0 u J})              ([P1] lem:spec(e))
 [ID]  exact identity m(S)/m(S0) = (D_S0/D_S)^{1/2} (1 + (t_S - t_S0)/(2b+Q_S))^nu   ([P3] eq:score)
 [OGc'] (proposed SE_lambda-free variant of [P3] lem:ongood(c)) S != empty, g_S>0:
       Q_S <= ||(I-P_S)y||^2 + (1+1/g_S)/(n+1) ||P_S y||^2
 [CDl'] (proposed variant of the lower half of [P3] cor:diff, eigen bound g_T on T only):
       u'(M_T - M_S)u >= n/(n+1) [ ||(P_T-P_S)u||^2 - eta_T ||P_T u||^2 ],  eta_T = 1/((n+1) g_T)
 [T02i#] pointwise chain behind W1 Theorem T02(i#), on B_n, with true f0:
       (den')  m^c_{b+}(S0)/f0(y_c) >= (n+1)^{-s0/2} c_IG sigma^2 n^{-1/2} e^{-Lambda_n}
       (main)  Pi(|S|>m | y) <= R_m (n+1)^{s0/2} sqrt(n) c# e^{Lambda_n} Theta1_{n,m},  every m with R_m > 0
Seed fixed.  Prints the worst slack (should be <= 0 up to rounding) for each check.
"""
import itertools, math
import numpy as np
from math import lgamma, log

B0 = 0.01
rng = np.random.default_rng(31415)

def proj(A):
    if A.shape[1] == 0:
        return np.zeros((A.shape[0], A.shape[0]))
    Uq, s, _ = np.linalg.svd(A, full_matrices=False)
    r = (s > 1e-10 * s.max()).sum()
    return Uq[:, :r] @ Uq[:, :r].T

def smoother(A, n):
    if A.shape[1] == 0:
        return np.zeros((A.shape[0], A.shape[0]))
    G = A.T @ A
    H = (n + 1) * G + np.eye(G.shape[0])
    return n * A @ np.linalg.solve(H, A.T)

def logD(A, n):
    if A.shape[1] == 0:
        return 0.0
    G = A.T @ A
    k = G.shape[0]
    return np.linalg.slogdet((n + 1) * G + np.eye(k))[1] - np.linalg.slogdet(G + np.eye(k))[1]

def lmin(A):
    if A.shape[1] == 0:
        return np.inf
    return np.linalg.eigvalsh(A.T @ A)[0]

def logw(p, k):
    return log(0.5) - (lgamma(2 * p) - lgamma(k + 1) - lgamma(2 * p - k))

def design(kind, N, p):
    Z = rng.normal(size=(N, p))
    if kind == "equi":
        Z = 0.3 * Z + 0.95 * rng.normal(size=(N, 1))
    elif kind == "nearcol":
        Z[:, -1] = Z[:, -2] + rng.normal(size=N) * math.sqrt(2.0 / (N + 1))   # corr ~ 1 - 1/n
    return Z / np.linalg.norm(Z, axis=0) * math.sqrt(N)

def run():
    worst = {k: -np.inf for k in ["B3", "C6a", "B1", "ID", "OGc'", "CDl'", "den'", "main"]}
    counts = {k: 0 for k in worst}
    for trial in range(60):
        n = int(rng.integers(12, 41))
        N = n - 1
        p = int(rng.integers(4, 9))
        s0 = int(rng.integers(1, min(3, p - 1) + 1))
        kind = ["iid", "equi", "nearcol"][trial % 3]
        X = design(kind, N, p)
        S0 = tuple(range(s0))
        theta = np.zeros(p); theta[:s0] = rng.choice([-1, 1], s0) * rng.uniform(0.2, 1.5, s0)
        sig2 = 1.0
        mu = X @ theta
        e = rng.normal(size=N) * math.sqrt(sig2)
        yc = mu + e
        K = min(p, n // 2)
        allS = [S for k in range(0, p + 1) for S in itertools.combinations(range(p), k)]
        cache = {}
        def obj(S):
            if S not in cache:
                A = X[:, list(S)]
                cache[S] = (proj(A), smoother(A, n), logD(A, n), lmin(A))
            return cache[S]
        nu = 0.01 + n / 2
        # ---- B3 and CDl' on random pairs S subset T
        for _ in range(150):
            T = tuple(sorted(rng.choice(p, size=int(rng.integers(1, p + 1)), replace=False)))
            S = tuple(sorted(rng.choice(T, size=int(rng.integers(0, len(T) + 1)), replace=False)))
            PT, MT, _, gT = obj(T); PS, MS, _, gS = obj(S)
            u = rng.normal(size=N) * rng.uniform(0.1, 10)
            lhs = u @ (MT - MS) @ u
            if len(S) == 0 or gS > 1e-9:
                eta = 0.0 if len(S) == 0 else 1 / ((n + 1) * gS)
                rhs = n / (n + 1) * (u @ (PT - PS) @ u + eta * u @ PS @ u)
                worst["B3"] = max(worst["B3"], (lhs - rhs) / (1 + abs(rhs))); counts["B3"] += 1
            if gT > 1e-9:
                etaT = 1 / ((n + 1) * gT)
                rhs2 = n / (n + 1) * (u @ (PT - PS) @ u - etaT * u @ PT @ u)
                worst["CDl'"] = max(worst["CDl'"], (rhs2 - lhs) / (1 + abs(rhs2))); counts["CDl'"] += 1
        # ---- C6a: all underfitting S, several rates b
        for S in allS:
            J = set(S0) - set(S)
            if not J:
                continue
            Sp = tuple(sorted(set(S) | set(S0)))
            for b in [1e-4, 0.01, 1.0, 100.0]:
                def logell(R):
                    P, M, lD, _ = obj(R)
                    Q = yc @ yc - yc @ M @ yc
                    return logw(p, len(R)) - 0.5 * lD - nu * log(2 * b + Q)
                d = logell(S) - logell(Sp) - (len(J) * log(2 * p) + len(J) / 2 * log(n + 1))
                worst["C6a"] = max(worst["C6a"], d); counts["C6a"] += 1
        # ---- B1, ID for supersets of S0
        P0, M0, lD0, g00 = obj(S0)
        Q0 = yc @ yc - yc @ M0 @ yc
        b = B0 * (yc @ yc) / N
        for S in allS:
            if not set(S0) <= set(S) or len(S) == s0:
                continue
            P, M, lD, g = obj(S)
            j = len(S) - s0
            if g > 1e-12:
                f = ((n + 1) * g + 1) / (g + 1)
                worst["B1"] = max(worst["B1"], j * log(f) - (lD - lD0), j * log((n + 1) / (1 + 1 / g)) - j * log(f)); counts["B1"] += 1
            QS = yc @ yc - yc @ M @ yc
            tS, t0 = yc @ M @ yc, yc @ M0 @ yc
            lhs = -0.5 * lD - nu * log(2 * b + QS) - (-0.5 * lD0 - nu * log(2 * b + Q0))
            rhs = 0.5 * (lD0 - lD) + nu * log(1 + (tS - t0) / (2 * b + QS))
            worst["ID"] = max(worst["ID"], abs(lhs - rhs)); counts["ID"] += 1
        # ---- OGc'
        for S in allS:
            if len(S) == 0:
                continue
            P, M, _, g = obj(S)
            if g <= 1e-9:
                continue
            Q = yc @ yc - yc @ M @ yc
            rhs = yc @ (np.eye(N) - P) @ yc + (1 + 1 / g) / (n + 1) * (yc @ P @ yc)
            worst["OGc'"] = max(worst["OGc'"], (Q - rhs) / (1 + rhs)); counts["OGc'"] += 1
        # ---- T02(i#) pointwise chain
        M_ = max(mu @ mu / n, 1e-12)
        bm, bp = B0 * sig2 / 2, B0 * (2 * (sig2 + M_) + 1)
        sy2 = yc @ yc / N
        if not (sig2 / 2 <= sy2 <= 2 * (sig2 + M_) + 1):
            continue  # outside B_n
        kappa = (bp / bm) ** 0.51
        IG = lambda v, a, bb: math.exp(a * log(bb) - lgamma(a) - (a + 1) * log(v) - bb / v)
        cIG = min(IG(v, 0.51, bp) for v in np.linspace(sig2, 2 * sig2, 2001))
        csharp = kappa ** 2 / (cIG * sig2)
        phi02 = g00 / N
        Ep = e @ e / sig2
        gam = (1 + 1 / (N * phi02)) / (n + 1)
        Lam = abs(Ep - N) / (2 * math.sqrt(n)) + Ep / (2 * n) + gam * (yc @ P0 @ yc) / (2 * sig2)
        def logmc(R, bb):  # log m^c_b(R)
            _, M, lD, _ = obj(R)
            Q = yc @ yc - yc @ M @ yc
            return -(N / 2) * log(2 * math.pi) + 0.51 * log(bb) + lgamma(nu) - lgamma(0.51) - 0.5 * lD - nu * log(bb + Q / 2)
        logf0 = -(N / 2) * log(2 * math.pi * sig2) - Ep / 2
        lhs = logmc(S0, bp) - logf0
        rhs = -s0 / 2 * log(n + 1) + log(cIG * sig2) - 0.5 * log(n) - Lam
        worst["den'"] = max(worst["den'"], rhs - lhs); counts["den'"] += 1
        Om = [S for S in allS if len(S) <= K]
        lpost = np.array([logw(p, len(S)) + logmc(S, B0 * sy2) for S in Om])
        post = np.exp(lpost - lpost.max()); post /= post.sum()
        sizes = np.array([len(S) for S in Om])
        lnum = np.array([logw(p, len(S)) + logmc(S, bm) - logf0 for S in Om])
        for m in range(0, K):
            Rm = sum(math.comb(p, k) * math.exp(logw(p, k) - logw(p, s0)) for k in range(m + 1, K + 1))
            vm = sum(math.comb(p, k) * math.exp(logw(p, k)) for k in range(m + 1, K + 1))  # times 1/W_K cancels below
            Theta1 = np.exp(lnum[sizes > m]).sum() / vm
            Pi = post[sizes > m].sum()
            bound = Rm * (n + 1) ** (s0 / 2) * math.sqrt(n) * csharp * math.exp(Lam) * Theta1
            worst["main"] = max(worst["main"], math.log(Pi) - math.log(bound)); counts["main"] += 1
    for k in worst:
        print(f"[{k:5}] checks: {counts[k]:6d}   worst slack (<= 0 means the inequality holds; log or relative scale): {worst[k]: .3e}")

if __name__ == "__main__":
    run()
