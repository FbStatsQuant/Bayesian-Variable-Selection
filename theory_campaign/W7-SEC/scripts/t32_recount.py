#!/usr/bin/env python3
"""Independent recount of W5-LOCKBOOK's Theorem T32(i) bound (T32-a) and its corollary (W7-SEC). Deterministic.

Written from the code reading in NOTES.md §1, not from W5's script. Prints (T32-a), the tier-0-only value, the
conjectured right-hand side, the floating-point variant (pilot T_e -> T_e + 1, REPORT §3.3), and checks the corollary
inequality conj >= (T32-a) on a grid of (n, p).
Tables use the bound sum_b 2^{|C_b|} <= p 2^B / B (W5 Step 7); W5 may have used the same bound.
"""
import math

def budgets(n, p):
    K = min(p, n // 2); B = min(math.isqrt(n), math.isqrt(p), 16)
    ell = math.ceil(math.log2(n + p + 1)); L = max(4, math.ceil(math.log2(n + 1)))
    N0 = max(2500, n, p); H0 = -(-512 * N0 // 2500); T0 = max(1000, ell * ell)
    kstar = min(K, p // 2); Mp = p + kstar * (p - kstar)
    return dict(K=K, B=B, ell=ell, L=L, N=[N0, 4 * N0], H=[H0, 4 * H0], T=[T0, 4 * T0], m=p + B + 2, Mp=Mp)

def t32a(n, p, tiers=(0, 1), efinal=1, fp_pilot=False):
    b = budgets(n, p); ell, L, m, Mp = b["ell"], b["L"], b["m"], b["Mp"]
    tables = p * 2 ** b["B"] // b["B"]
    c = tables
    for e in tiers:
        H, T = b["H"][e], b["T"][e]
        c += (1 + 4 * ell) * H * (1 + m * (T + L + 4))
        if fp_pilot:
            c += H * m                                  # one extra pilot stage of H particles
        c += (ell + 1) * (1 + (ell + 1) * Mp) + (ell + 1) * (40 * p + 1)
    N, T = b["N"][efinal], b["T"][efinal]
    c += 4 * N * (1 + m * (T + L + 4)) + (80 * p + 1) + (1 + (ell + 1) * Mp)
    return c, b

def conj(n, p):
    b = budgets(n, p); ell, L, m, Mp = b["ell"], b["L"], b["m"], b["Mp"]
    c = p * 2 ** b["B"] // b["B"]
    for e in (0, 1):
        c += (1 + 4 * ell) * b["H"][e] * (1 + 2 * m * (b["T"][e] + L + 4))
    c += 4 * b["N"][1] * (1 + 2 * m * (b["T"][1] + L + 4)) + (8 * ell + 3) * (ell + 1) * Mp
    return c

for n, p in [(200, 500), (200, 1000), (800, 1000)]:
    full, b = t32a(n, p)
    t0, _ = t32a(n, p, tiers=(0,), efinal=0)
    fpv, _ = t32a(n, p, fp_pilot=True)
    cj = conj(n, p)
    print(f"n={n}, p={p}: m={b['m']} Mp={b['Mp']} ell={b['ell']} L={b['L']}  (T32-a) both tiers = {full}  tier 0 only = {t0}  "
          f"conjectured = {cj}  ratio = {cj/full:.6f}  fp variant = {fpv} (+{fpv-full})")

worst = None
for n in [3, 4, 5, 10, 50, 200, 1000, 10**4, 10**5, 10**6, 10**7]:
    for p in [1, 2, 3, 10, 100, 1000, 10**4, 10**5, 10**6, 10**7]:
        d = conj(n, p) - t32a(n, p, fp_pilot=True)[0]
        if worst is None or d < worst[0]:
            worst = (d, n, p)
print(f"min over grid of conjectured - (T32-a, fp variant) = {worst[0]} at n = {worst[1]}, p = {worst[2]} (must be > 0)")
