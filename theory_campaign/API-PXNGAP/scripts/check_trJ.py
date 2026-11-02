"""Lemma Tr-J numerics (API-PXNGAP). Seed-free (deterministic quadrature).
(a) truncated moment bound vs exact numerical integral, for j up to 18 and u up to 20 (beyond PXN's j,u <= 16);
(c) chi-square/Beta tail bound at tau_n = 8(D+1) log n / n vs exact Beta tail, and the union bound over C n^D variables.
"""
import math, sys
import numpy as np
from scipy import integrate, special, stats

def exact_trunc(j, m, nu, tau):
    a, b = j / 2, (m - j) / 2
    logB = special.betaln(a, b)
    f = lambda x: math.exp((a - 1) * math.log(x) + (b - 1 - nu) * math.log1p(-x) - logB)
    val, _ = integrate.quad(f, 0, tau, limit=200)
    return val

def bound_trunc(j, m, u, nu, tau):
    e1 = (u + j + 3) / 2 + 0.01
    return 2 ** e1 * (m * tau / 2) ** (j / 2) / math.gamma(j / 2 + 1)

print("== (a) truncated moment: exact / bound (must be <= 1) ==")
worst = 0
for n in (100, 200, 800):
    nu = 0.01 + n / 2
    for u in (0, 1, 5, 20):
        m = n - 1 - u
        for j in (1, 2, 3, 8, 16, 17, 18):
            if m - j < 1: continue
            tau = 8 * (2 + 1) * math.log(n) / n  # D = 2 as an example
            tau = min(tau, 0.5)
            ex, bd = exact_trunc(j, m, nu, tau), bound_trunc(j, m, u, nu, tau)
            worst = max(worst, ex / bd)
            print(f"n={n:4d} u={u:2d} j={j:2d} tau={tau:.4f} exact={ex:.3e} bound={bd:.3e} ratio={ex/bd:.3e}")
print("max ratio exact/bound:", worst, "OK" if worst <= 1 else "VIOLATION")

print("\n== (c) uniform tail: P(Beta(j/2,(m-j)/2) > tau_n) vs (LM bound) and union bound over C n^D ==")
viol = 0
for n in (200, 400, 800, 1600, 3200):
    for (J, D, C) in ((16, 2, 2 ** 16), (5, 2 * 5, 2 ** 5)):  # (P3 row: J=16,D=A=2), (Lambda row: s0=3, J=s0+2, D=A(s0+2))
        tn = 8 * (D + 1) * math.log(n); tau = tn / n
        fam = C * n ** D
        worst_tail = 0
        for u in (0, 1, J):
            m = n - 1 - u
            for j in range(1, J + 1):
                if m - j < 1: continue
                tail = stats.beta.sf(tau, j / 2, (m - j) / 2)
                tp = tau * (m - j) / 2
                x = tp / 2 - math.sqrt(j * tp)
                lm = math.exp(-(m - j) / 16) + (math.exp(-x) if x > 0 else 1.0)
                if tail > lm * 1.0000001: viol += 1
                worst_tail = max(worst_tail, tail)
        print(f"n={n:5d} J={J:2d} D={D:2d} tau_n={tau:.4f} |family|={fam:.2e} max exact tail={worst_tail:.2e} "
              f"union bound={min(1, fam * worst_tail):.2e}  n^-(D+1)e^sqrt(2J(D+1)log n)*C n^D={C * n**D * n**(-(D+1)) * math.exp(math.sqrt(2*J*(D+1)*math.log(n))):.2e}")
print("tail-bound violations (exact > LM bound):", viol)
