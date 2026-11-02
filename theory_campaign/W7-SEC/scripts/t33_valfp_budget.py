#!/usr/bin/env python3
"""T33 budget evaluation (W7-SEC). Deterministic.

(1) Corollary T33-NF: the a-priori hypotheses (eps_H, eps_A, eps_Q <= 1/2 and (n+1) r_Q <= 1/2) at standardised
    columns (g_S = n - 1), worst case over |S| <= K and lambda_H >= 1, y'y/Q <= n + 1. Reports the worst-case quantities
    at the study's sizes and the largest n for which the corollary applies, for K = min(p, n/2) with p >= n/2, and K = 10.
    Also the universal (data-free) eta_Q bound nu (n+1) r_Q.
(2) Proposition T33-Z: eta_Z and the union-bound epsilon at the study's final-run budgets, with
    (a) measured per-score errors (max |dlogm| at n = 200 in results/t33_fp_check.txt, ~1.3e-13), and
    (b) the rigorous per-score bound eta'_m of Theorem T33-S for a well-conditioned model at n = 200 (~1e-8),
    for realised grid lengths T in {10, 100, T_e}.
"""
import math

u = 2.0 ** -53
uL = 2.0 ** -64

def gamma(j): return j * u / (1 - j * u)

def worst(n, K):
    g = n - 1; h = (n + 1) * g + 1; a = g + 1; k = K
    epsH = 1.01 * k * h * (n + k + 3) * u
    epsA = 1.01 * k * a * (n + k + 2) * u
    epsQ = 1.02 * k * h * (n + 3 * k + 3) * u
    omega = gamma(n) * math.sqrt(n * k * g)          # lambda_H >= 1
    rhoQ = epsQ
    rQ = gamma(n) + 2.03 * u + ((rhoQ + gamma(k)) / (1 - rhoQ)) * (1 + omega) ** 2 + 2 * omega + omega ** 2 if rhoQ < 1 else math.inf
    nu = 0.01 + n / 2
    th = (n + 1) * rQ
    etaQ = nu * th / (1 - th) if th < 1 else math.inf
    ok = max(epsH, epsA, epsQ) <= 0.5 and th <= 0.5 and n + 1 <= 1e7
    return dict(epsH=epsH, epsA=epsA, epsQ=epsQ, nrQ=th, etaQ_universal=etaQ, ok=ok)

print("(1) Corollary T33-NF, worst case (lambda_H = 1, y'y/Q = n+1), standardised columns")
for n, K in [(200, 100), (200, 20), (1000, 500), (1000, 20)]:
    w = worst(n, K)
    print(f"  n={n:5d} K={K:4d}: eps_H={w['epsH']:.2e} eps_A={w['epsA']:.2e} eps_Q={w['epsQ']:.2e} (n+1)r_Q={w['nrQ']:.2e} "
          f"universal eta_Q={w['etaQ_universal']:.2e}  hypotheses hold: {w['ok']}")
for label, Kf in [("K = n/2", lambda n: n // 2), ("K = 10", lambda n: 10), ("K = 1", lambda n: 1)]:
    lo, hi = 3, 10**7
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if worst(mid, Kf(mid))["ok"]: lo = mid
        else: hi = mid
    print(f"  largest n with the a-priori hypotheses, {label}: n = {lo}")

print("\n(2) Proposition T33-Z at the study's final run (n = 200)")
for p in [500, 1000]:
    n = 200
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    ell = math.ceil(math.log2(n + p + 1)); L = max(4, math.ceil(math.log2(n + 1)))
    N0 = max(2500, n, p); T0 = max(1000, ell ** 2)
    m = p + B + 2; J = math.ceil(p / B)
    for tier in [0, 1]:
        N = 4 ** tier * N0; Te = 4 ** tier * T0
        for T in [10, 100, Te]:
            Cdec = 4 * N * m * (T + L + 4)
            Qall = 4 * N * (T + L + 5)
            for lab, etam in [("measured", 1.3e-13), ("rigorous", 1.0e-8)]:
                s = 15                                   # typical model size near the truth (s0 = 14)
                eta_d = (s + 2) * etam
                eta_gamma = 2 * (2 * s + 2) * etam       # two states, each log gamma_phi uses <= s + 1 scores + constants
                eta_tab = etam
                Lam = 2e3
                rho_lse = (N / math.e + 4) * u + 1.01 * N * uL + 2 * u * Lam
                eta_Z0 = J * (2 * eta_tab + 2 * rho_lse) + 1e-13 + rho_lse
                eta_m0 = 1e-13
                Dmax = 2e3
                eta_Z = eta_m0 + eta_Z0 + eta_d + 2.01 * u * Dmax + T * (rho_lse + u * Lam)
                eps = Cdec * (eta_gamma + 2 ** -53 + 4 * u) + 2 * N ** 2 * eta_d + T * N * (N * gamma(N) + 2 ** -53) \
                      + Qall * (J + 1) * (2 * (eta_Z0 + 2 * eta_tab) + 2 ** -53)
                print(f"  p={p:5d} tier={tier} N={N:6d} T={T:5d}: decisions C_dec={Cdec:.2e}; [{lab:8s} per-score {etam:.0e}] "
                      f"eta_Z={eta_Z:.2e}  epsilon (union bound)={eps:.2e}")
