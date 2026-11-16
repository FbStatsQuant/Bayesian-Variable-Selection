#!/usr/bin/env python3
"""W1-T03R COUNTEREXAMPLE (PROOF.md Prop. D): under G and R alone (no SE), the posterior size tail of the exact v3
target can be ~2^{-m}, so no size cutoff of the form s0 + O(1) (in particular s0 + O(s0 log n / log p) with p = n^A)
gives Pi(|S| > m_n | y) = O_P(n^{-1/2}).

Design: s0 = 1, X^r = [x, x, ..., x] (p identical non-constant columns), y^r = alpha + beta1 x + eps, eps ~ N(0, sigma^2 I).
For every nonempty S with |S| = k: G_S = N 11^T, D_k = ((n+1)kN+1)/(kN+1),
Q_k = y'y - n k (xt'y)^2 / ((n+1) N k + 1)  (xt = standardised x, N = n-1). D_0 = 1, Q_0 = y'y = N.
Hence pi(|S| = k) is proportional to C(p,k) w(k) D_k^{-1/2} (2 b0 + Q_k)^{-nu}, computed exactly in log space.
"""
import math
import numpy as np
from scipy.special import gammaln

def size_posterior(n, p, beta1=1.0, sigma=1.0, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    y = 0.3 + beta1 * x + sigma * rng.standard_normal(n)
    N = n - 1
    xc = x - x.mean(); xt = xc / np.sqrt(xc @ xc / N)
    yc = y - y.mean(); yt = yc / np.sqrt(yc @ yc / N)
    c = xt @ yt
    K = min(p, n // 2)
    b0, a0 = 0.01, 0.01
    nu = a0 + n / 2
    k = np.arange(K + 1)
    D = np.where(k == 0, 1.0, ((n + 1) * k * N + 1) / (k * N + 1))
    Q = np.where(k == 0, float(N), N - n * k * c**2 / ((n + 1) * N * k + 1))
    logq = (gammaln(p + 1) - gammaln(k + 1) - gammaln(p - k + 1)) + np.log(0.5) \
        - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
    lp = logq - 0.5 * np.log(D) - nu * np.log(2 * b0 + Q)
    lp -= lp.max(); pr = np.exp(lp); pr /= pr.sum()
    tail = pr[::-1].cumsum()[::-1]  # tail[m] = Pi(|S| >= m)
    return pr, tail, K

if __name__ == "__main__":
    print("Pi(|S| > m | y) * 2^m for the duplicate design (s0 = 1, beta1 = 1, sigma = 1), one data set each")
    print(f"{'n':>7} {'p':>7} {'pi(S0 size=1 class)':>20} " + " ".join(f"m={m:<3}" for m in (1, 2, 4, 8, 12, 16)) +
          "   m*(n^-1/2)  0.5*log2(n)")
    for n in (200, 2000, 20000, 200000):
        for p in (500, n):
            pr, tail, K = size_posterior(n, p)
            vals = [tail[m + 1] * 2**m if m + 1 <= K else float('nan') for m in (1, 2, 4, 8, 12, 16)]
            mstar = next(m for m in range(K + 1) if (tail[m + 1] if m + 1 <= K else 0.0) <= n**-0.5)
            print(f"{n:>7} {p:>7} {pr[1]:>20.4f} " + " ".join(f"{v:5.3f}" for v in vals) +
                  f"   {mstar:>10d}  {0.5*math.log2(n):>10.2f}")
    # replicate check of the probability claim: fraction of data sets with Pi(|S|>m) >= 2^{-m}/8 for m = 1..12
    n, p, reps = 2000, 2000, 200
    ok = 0
    for r in range(reps):
        pr, tail, K = size_posterior(n, p, seed=1000 + r)
        ok += all(tail[m + 1] >= 2.0**-m / 8 for m in range(1, 13))
    print(f"\n[n={n}, p={p}] data sets with Pi(|S|>m|y) >= 2^-m/8 for all m=1..12: {ok}/{reps}")
