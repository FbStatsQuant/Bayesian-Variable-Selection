#!/usr/bin/env python3
"""Constants for the lower-bound half (Part L) of T05(ii), W7-SEC. Deterministic (no randomness).

(1) mu_q = E min(chi2_1, q) at q = median(chi2_1); beta0 = mu_q - q/2 - t_H (bottom-sum constant of event E_B).
(2) theta_inf(eps) = 1/(1 - 2 eps log(e^2/eps)) for the small-m regime.
(3) The smallest log n (on a grid) at which the deterministic sufficient conditions (N1), (C1), (C2) of Part L hold,
    for s0 in {1, 2, 5, 14}, worst case over p <= n - 1. This is the n0 implied by the crude constants; it is NOT a
    claim about where the limit becomes accurate (see t05_mc.txt for that).
"""
import math
from scipy.stats import chi2
from scipy.integrate import quad

q = chi2.ppf(0.5, 1)
mu_q = quad(lambda x: chi2.sf(x, 1), 0, q)[0]           # E min(Z, q) = int_0^q P(Z > x) dx
tH = 0.02
beta0 = mu_q - q / 2 - tH
print(f"q = median chi2_1 = {q:.6f}; mu_q = E min(chi2_1, q) = {mu_q:.6f}; mu_q - q/2 = {mu_q - q/2:.6f}")
print(f"with Hoeffding slack t_H = {tH}: beta0 = {beta0:.6f}; P(E_B^c) <= exp(-2 d t_H^2 / q^2) = exp(-{2*tH**2/q**2:.6f} d)")

eps = 0.008
W = 2 * eps * math.log(math.e**2 / eps)
print(f"eps = {eps}: 2 eps log(e^2/eps) = {W:.6f}; theta_inf = 1/(1 - that) = {1/(1-W):.6f}")

def conditions_hold(L, s0):
    """L = log n. Worst case over p <= n-1 (M <= d). delta = n^{-1/3}, a = log log n."""
    n = math.exp(L)
    d = n - 1 - s0
    delta = n ** (-1 / 3)
    a = math.log(L)
    # N1: tau - 2 log(eM) - 2a > 0, using tau - 2 log(eM) >= log n - 2 - 2 log s0
    N1 = L - 2 - 2 * math.log(s0) - 2 * a > 0
    # small-m regime
    r = 2 * (a + 2 * math.log(eps * d)) * (1 + math.log(eps * d))
    Wbar = W * d + r
    theta = (n + 0.02) / ((1 - delta) * d - Wbar)
    C1 = (1.5 - theta) * L > theta * (1 + a + 2 / math.e) + math.log(1 + s0)
    # large-m regime
    am = 2 * math.log(math.e / eps) + 2 * (a + 2 * L) / (eps * d)
    C2 = (n / 2 + 0.01) / (beta0 * d) * am < 0.5 * L
    return N1 and C1 and C2, (N1, C1, C2)

for s0 in [1, 2, 5, 14]:
    Lmin = None
    for L10 in range(30, 4000):
        L = L10 / 10
        ok, parts = conditions_hold(L, s0)
        if ok:
            Lmin = L; break
    print(f"s0 = {s0:2d}: crude sufficient conditions (N1),(C1),(C2) first hold at log n = {Lmin}")
