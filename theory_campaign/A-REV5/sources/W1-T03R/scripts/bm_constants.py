#!/usr/bin/env python3
"""W1-T03R: beta-min thresholds at n = 200 (s0 = 14, sigma* = 1). c0 = L* (proof artefact), M* = 2L*+1 (locked BM-C).
Required theta^2 >= c * log(n) / (n * phi0^2). Executed signals (THEORY_INVENTORY_20261028 sec. C): 0.64 (c=1), 0.16 (c=0.5), max 3.24."""
import math
n, s0 = 200, 14
for p, phi2_adv in ((500, 0.0334), (1000, None)):
    A = math.log(p) / math.log(n)
    j = math.ceil((2 * A + 1) * s0) + 1
    C = 2 * s0 + 3 * (A * j + s0 + math.log(j + 1) + 1)
    L = max(4 * C, 32 * (s0 * (A + 1) + 2))
    M = 2 * L + 1
    base = math.log(n) / n
    print(f"p={p}: A={A:.4f} j0={j} C*={C:.1f} c0=L*={L:.1f} M*={M:.1f}")
    print(f"   theta^2 needed, phi0^2=1: c0 -> {L*base:.2f} (x{L*base/0.64:.0f} the c=1 signal 0.64), M* -> {M*base:.2f} (x{M*base/0.64:.0f})")
    if phi2_adv:
        print(f"   with the greedy-adversarial S1 value phi0^2 <= {phi2_adv}: c0 -> {L*base/phi2_adv:.0f} (x{L*base/phi2_adv/0.64:.0f})")
    print(f"   r_n = {math.sqrt(base):.3f};  orthogonal-design heuristic scale (log n + 2 log p)/n = {(math.log(n)+2*math.log(p))/n:.3f}")
