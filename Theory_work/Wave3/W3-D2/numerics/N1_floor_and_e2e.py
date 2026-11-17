#!/usr/bin/env python3
"""N1 (W3-D2): (i) floor-size arithmetic of Lemma D2-B1; (ii) one end-to-end exact check of Theorem 2X.

(i) For the coded size cutoff m#_n of [W3P] Theory_work/Wave3/W3-POST/STATEMENT.md:33-39
    q_k = C(p, k) w(k), w(k) = 1/2 / C(2p - 1, k)  (0 <= k <= K = min(p, floor(n/2))),
    R_m = sum_{k = max(m+1, 0)}^{K} q_k / w(s0),
    m#_n = min{m >= s0 : R_m <= n^{-(s0+1)/2} e^{-omega}},  omega = (1/2) log n,
    j0 = ceil((2A + 1) s0) + 1,  k_n = s0 + max(j0, m#_n)   (W3-MISR-R STATEMENT.md:96-100),
computed exactly in log space, and compared with 3(A+1)(s0+1) log n (Theorem 2X, (A2)) and with the recorded
row-1.2 size 5(A+1)(s0+1) log n. Worst case over the grid uses p = floor(n^A) (largest allowed p).

(ii) Exact enumeration of the coded target pi of [W3P] :16-29 (p = 6) under random Gaussian designs with
quantities that vary with n (allowed by Theorem 2X, outside the recorded Theorem 2):
    rows iid N_6(m, Sigma_n), Sigma_n = D (rho_n J + (1 - rho_n) I) D, D = diag(1, 2, 0.5, 3, 1, 1),
    rho_n = 0.5 - 1/log n, m = (5, -3, 0, 1, 0, 2);
    beta = (1, -0.7, 0, 0, 0, 0) / D (so Sigma_jj beta_j^2 = (1, 0.49)), alpha = 4;
    sigma_n^2 = (log n)^{1/2}   (grows; energy and beta-min relative to sigma_n^2 still hold).
Outputs per n: E delta_n, P(HPM != S0), P(MPM != S0), E max_j |PIP_j - 1{j in S0}|, and E delta_n / r_n.
"""
import itertools
import math
import sys

import numpy as np


def log_comb(a, b):
    return math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)


def logsumexp(v):
    m = max(v)
    return m + math.log(sum(math.exp(x - m) for x in v))


def m_sharp(n, p, s0):
    K = min(p, n // 2)
    if s0 > K:
        return None
    logw_s0 = math.log(0.5) - log_comb(2 * p - 1, s0)
    logq = [log_comb(p, k) + math.log(0.5) - log_comb(2 * p - 1, k) for k in range(K + 1)]
    thr = -((s0 + 1) / 2) * math.log(n) - 0.5 * math.log(n)
    # tail sums from the top: T[m] = log sum_{k=m+1}^{K} q_k
    tail = [-math.inf] * (K + 2)
    for k in range(K, -1, -1):
        a, b = tail[k + 1], logq[k]
        tail[k] = b if a == -math.inf else max(a, b) + math.log1p(math.exp(-abs(a - b)))
    for m in range(s0, K + 1):
        lr = (tail[m + 1] if m + 1 <= K else -math.inf) - logw_s0
        if lr <= thr:
            return m
    return K


def part_i():
    print("# (i) k_n = s0 + max(j0, m#_n) against 3(A+1)(s0+1) log n and 5(A+1)(s0+1) log n")
    print("# grid: A in {1, 1.5, 2, 3, 5}, s0 in {1, 2, 3, 5, 10}, n in {3, 10, 100, 400, 1e3, 1e4, 1e5}; p = floor(n^A) capped at 1e15")
    worst = 0.0
    rows = []
    for A in [1, 1.5, 2, 3, 5]:
        for s0 in [1, 2, 3, 5, 10]:
            for n in [3, 10, 100, 400, 1000, 10_000, 100_000]:
                if 2 * s0 > n:
                    continue
                p = int(min(math.floor(n ** A), 10 ** 15))
                if p < max(2, s0):
                    continue
                ms = m_sharp(n, p, s0)
                j0 = math.ceil((2 * A + 1) * s0) + 1
                kn = s0 + max(j0, ms)
                b3 = 3 * (A + 1) * (s0 + 1) * math.log(n)
                b5 = 5 * (A + 1) * (s0 + 1) * math.log(n)
                worst = max(worst, kn / b3)
                rows.append((A, s0, n, p, ms, j0, kn, b3, b5))
    for A, s0, n, p, ms, j0, kn, b3, b5 in rows:
        if n in (100, 400, 10_000) and s0 in (1, 5) and A in (1, 2):
            print(f"A={A:<4} s0={s0:<3} n={n:<7} p={p:<12} m#={ms:<5} j0={j0:<4} k_n={kn:<5} "
                  f"3(A+1)(s0+1)log n={b3:8.1f}  5(A+1)(s0+1)log n={b5:8.1f}")
    print(f"# max over the grid of k_n / [3(A+1)(s0+1) log n] = {worst:.4f} ({len(rows)} cases); must be <= 1")


def posterior(x, yr, models, P):
    n = x.shape[0]
    xc = x - x.mean(axis=0)
    sd = np.sqrt((xc ** 2).sum(axis=0) / (n - 1))
    X = xc / sd
    yc = yr - yr.mean()
    y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
    K = min(P, n // 2)
    nu = 0.01 + n / 2
    b0 = 0.01
    G = X.T @ X
    zf = X.T @ y
    yty = y @ y
    lp = {}
    for S in models:
        k = len(S)
        if k > K:
            continue
        logw = math.log(0.5) - log_comb(2 * P - 1, k)
        if k == 0:
            logD, Q = 0.0, yty
        else:
            idx = list(S)
            GS = G[np.ix_(idx, idx)]
            H = (n + 1) * GS + np.eye(k)
            logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(k))[1]
            z = zf[idx]
            Q = yty - n * z @ np.linalg.solve(H, z)
        lp[S] = logw - 0.5 * logD - nu * math.log(2 * b0 + Q)
    L = logsumexp(list(lp.values()))
    return {S: math.exp(v - L) for S, v in lp.items()}


def part_ii(R):
    P = 6
    models = [S for k in range(P + 1) for S in itertools.combinations(range(P), k)]
    D = np.array([1.0, 2.0, 0.5, 3.0, 1.0, 1.0])
    mvec = np.array([5.0, -3.0, 0.0, 1.0, 0.0, 2.0])
    beta = np.array([1.0, -0.7, 0, 0, 0, 0]) / D
    S0 = (0, 1)
    rng = np.random.default_rng(20261117)
    print(f"\n# (ii) end-to-end exact enumeration, p = 6, R = {R} replications per n, seed 20261117")
    print("n      rho_n   sigma2_n  E_delta   P(HPM!=S0)  P(MPM!=S0)  E_maxPIPerr  r_n     E_delta/r_n")
    for n in [50, 100, 200, 400, 800, 1600]:
        rho = 0.5 - 1 / math.log(n)
        Sig = np.diag(D) @ (rho * np.ones((P, P)) + (1 - rho) * np.eye(P)) @ np.diag(D)
        Lc = np.linalg.cholesky(Sig)
        s2 = math.sqrt(math.log(n))
        dl = hm = mm = pe = 0.0
        for _ in range(R):
            x = mvec + rng.standard_normal((n, P)) @ Lc.T
            yr = 4.0 + x @ beta + math.sqrt(s2) * rng.standard_normal(n)
            post = posterior(x, yr, models, P)
            d = 1 - post.get(S0, 0.0)
            pip = np.zeros(P)
            for S, v in post.items():
                for j in S:
                    pip[j] += v
            truth = np.array([1.0 if j in S0 else 0.0 for j in range(P)])
            mpm = tuple(j for j in range(P) if pip[j] > 0.5)
            hpm = max(post, key=post.get)
            dl += d
            hm += hpm != S0
            mm += mpm != S0
            pe += np.abs(pip - truth).max()
        rn = math.sqrt(math.log(n) / n)
        print(f"{n:<6} {rho:6.3f}  {s2:7.3f}   {dl / R:8.5f}  {hm / R:8.4f}    {mm / R:8.4f}    {pe / R:8.5f}     "
              f"{rn:.4f}  {dl / R / rn:7.3f}")


if __name__ == "__main__":
    part_i()
    part_ii(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
