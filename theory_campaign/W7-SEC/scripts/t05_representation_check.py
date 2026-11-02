#!/usr/bin/env python3
"""T05 Lemma 1 check (W7-SEC). Seed fixed.

Builds an exactly orthogonal standardised design (X^T X = (n-1) I_p, columns centred), draws raw data
y^r = alpha + X beta + eps, standardises y as in 00_COMMON (y = C y^r / s_y), and checks by brute-force
enumeration over all |S| <= K:
  (a) D_S = n^{|S|}  and  Q_S = (n-1) V_S / V_tot  (the exact representation of Lemma 1);
  (b) the global HPM S_dagger by enumeration (tie rule: larger F, smaller size, lexicographic)
      equals the top-k-by-T^2 set at the best k (Corollary 1);
  (c) the necessary condition used in Part U:  F(S0) - F(S0 \\ j) <= (1/2)[nu' T_j^2 / Xi - tau].
F is computed generically (Cholesky of H_S, G_S + I), not through the representation.
"""
import itertools, math, sys
import numpy as np

rng = np.random.default_rng(20261102)

def lchoose(a, b):
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)

def run(n, p, s0, theta_mag, reps):
    K = min(p, n // 2)
    nu = 0.01 + n / 2
    logw = [-math.log(2) - lchoose(2 * p - 1, k) for k in range(K + 1)]
    worst = {"D": 0.0, "Q": 0.0, "U": -np.inf}
    hpm_agree = 0
    for r in range(reps):
        A = rng.standard_normal((n, p))
        A -= A.mean(axis=0)
        Qm, _ = np.linalg.qr(A)                      # orthonormal, orthogonal to 1 (columns of A are centred)
        X = Qm * math.sqrt(n - 1)                    # X^T X = (n-1) I_p, columns centred, sd 1
        S0 = sorted(rng.choice(p, s0, replace=False).tolist())
        theta = np.zeros(p); theta[S0] = theta_mag * rng.choice([-1, 1], s0)
        sigma = 1.3
        eps = sigma * rng.standard_normal(n)
        yr = 0.7 + X @ theta + eps
        yc = yr - yr.mean(); sy = math.sqrt(yc @ yc / (n - 1)); y = yc / sy
        G = X.T @ X; z = X.T @ y; yty = y @ y
        # representation quantities
        e = X / math.sqrt(n - 1)
        xi = e.T @ eps / sigma
        T = math.sqrt(n - 1) * theta / sigma + xi
        Rp = (eps @ eps - (eps.mean() ** 2) * n) / sigma**2 - xi @ xi   # ||C eps||^2/s^2 - sum xi^2
        Vtot = Rp + T @ T
        F = {}
        for k in range(K + 1):
            for S in itertools.combinations(range(p), k):
                S = list(S)
                if k == 0:
                    logdet_ratio = 0.0; Q = yty
                else:
                    GS = G[np.ix_(S, S)]
                    H = (n + 1) * GS + np.eye(k); Am = GS + np.eye(k)
                    LH = np.linalg.cholesky(H); LA = np.linalg.cholesky(Am)
                    logdet_ratio = 2 * np.log(np.diag(LH)).sum() - 2 * np.log(np.diag(LA)).sum()
                    w = np.linalg.solve(LH, z[S]); Q = yty - n * (w @ w)
                    worst["D"] = max(worst["D"], abs(logdet_ratio - k * math.log(n)))
                VS = Rp + sum(T[j] ** 2 for j in range(p) if j not in S) + sum(T[j] ** 2 for j in S) / n
                worst["Q"] = max(worst["Q"], abs(Q - (n - 1) * VS / Vtot) / Q)
                F[tuple(S)] = logw[k] - 0.5 * logdet_ratio - nu * math.log(0.02 + Q)
        # enumeration HPM with the tie rule
        best = max(F.items(), key=lambda kv: (kv[1], -len(kv[0]), tuple(-x for x in kv[0])))[0]
        order = np.argsort(-T**2, kind="stable")
        gk = [F[tuple(sorted(order[:k].tolist()))] for k in range(K + 1)]
        kh = int(np.argmax(gk))
        topk = tuple(sorted(order[:kh].tolist()))
        hpm_agree += (topk == best)
        # Part U inequality
        nup = (n - 1) * (n + 0.02) / n
        tau = math.log(n) + 2 * math.log((2 * p - s0) / s0)
        Xi = Rp + sum(xi[j] ** 2 for j in range(p) if j not in S0)
        for j in S0:
            lhs = F[tuple(S0)] - F[tuple(x for x in S0 if x != j)]
            rhs = 0.5 * (nup * T[j] ** 2 / Xi - tau)
            worst["U"] = max(worst["U"], lhs - rhs)
    return worst, hpm_agree

if __name__ == "__main__":
    print("T05 Lemma 1 / Corollary 1 / Part-U inequality, brute-force enumeration; seed 20261102")
    for (n, p, s0, mag, reps) in [(40, 6, 2, 0.35, 30), (25, 8, 3, 0.5, 20), (60, 10, 3, 0.25, 10), (13, 12, 2, 0.8, 10)]:
        w, a = run(n, p, s0, mag, reps)
        print(f"n={n:3d} p={p:2d} s0={s0} |theta|={mag}: max|logD - k log n| = {w['D']:.2e}, "
              f"max rel|Q - (n-1)V_S/V_tot| = {w['Q']:.2e}, HPM = top-k at best k in {a}/{reps}, "
              f"max[(F(S0)-F(S0-j)) - bound] = {w['U']:.3e} (must be <= 0)")
