"""C3 Opus scratch checks (read-only reviewer). Run: C:/Users/felip/anaconda3/python.exe checks.py
(1) riboflavin null reference for max |r| over C(4088,2) pairs at n = 71 (independent-pairs heuristic, exact t law)
    vs the crude bound sqrt(2 log N / n) used in make_summary.R.
(2) ENUM sufficient condition 2^p <= 4 n p vs the coded inequality (EXB), saturating, for a few (n, p).
(3) Fixed-p onset n >= 2^p/(4p) for the Part-2 design widths (asymptotic only; onset is not a claim).
"""
import math
import numpy as np
from scipy import stats
from scipy.optimize import brentq

n, p = 71, 4088
N = p * (p - 1) // 2
crude = math.sqrt(2 * math.log(N) / n)
tail = lambda x: 2 * stats.t.sf(x * math.sqrt(n - 2) / math.sqrt(1 - x * x), n - 2)
med = brentq(lambda x: tail(x) - math.log(2) / N, 0.3, 0.99)
q99 = brentq(lambda x: tail(x) - (-math.log(0.99)) / N, 0.3, 0.99)  # P(max > x) ~ 1 - exp(-N tail) = 0.01
print(f"(1) crude sqrt(2logN/n) = {crude:.3f}; median max|r| = {med:.3f}; ~99% quantile = {q99:.3f}; "
      f"P(max>0.67) ~ {1 - math.exp(-N * tail(0.67)):.4f}")


def exb(n, p):
    K = min(p, n // 2)
    N0 = max(2500, n, p)
    H0 = (512 * N0 + 2499) // 2500
    thr = (5 * H0 + 4 * N0) * p
    s, c = 0, 1
    for k in range(K + 1):
        if k > 0:
            c = c * (p - k + 1) // k
        s += c
        if s > thr:
            return False
    return True


bad = 0
for e in range(4, 30):
    nn = 10 ** e
    for pp in range(2, 120):
        if 2 ** pp <= 4 * nn * pp and not exb(nn, pp):
            bad += 1
print(f"(2) cases with 2^p <= 4np but (EXB) false: {bad}")

for name, pw in [("iclaims", 10), ("spam", 57), ("digits", 61), ("diabetes_quad", 64), ("fred_md", 99),
                 ("tecator", 100), ("fred_qd", 170), ("riboflavin", 4088)]:
    print(f"(3) {name:14s} p={pw:5d}: exact branch for all n >= 2^p/(4p) = 10^{(pw * math.log10(2) - math.log10(4 * pw)):.1f}")
