#!/usr/bin/env python3
"""W1-T03R: first n at which the explicit deterministic thresholds of the T03 proof hold (s0 = 14, p = n^A).
Binding condition: delta_n = 3 sqrt(log n/N) + C_A (m + s0) log n / N <= 1/2 (Lemma ongood(b) of PROOF_v2), C_A = 8 + 3A,
with m = m_old (locked) or m = m# (this run). Also n/5 >= (s0(A+1)+2) log n (Step 1). Other thresholds bind earlier.
These are NOT the n_0 of the O_P constants (unspecified tightness), only where the proof's deterministic steps start."""
import math
from tail_bound import thresholds
s0 = 14
for A in (math.log(500) / math.log(200), math.log(1000) / math.log(200)):
    CA = 8 + 3 * A
    for which in ("old", "sharp"):
        def ok(n):
            p = int(round(n ** A)); N = n - 1; L = math.log(n)
            m_old, m_sh, *_ = thresholds(n, p, s0)
            m = m_old if which == "old" else m_sh
            d = 3 * math.sqrt(L / N) + CA * (m + s0) * L / N
            return d <= 0.5 and n / 5 >= (s0 * (A + 1) + 2) * L
        lo, hi = 200, 10**9
        while hi - lo > 1:
            mid = (lo + hi) // 2
            lo, hi = (lo, mid) if ok(mid) else (mid, hi)
        print(f"A = {A:.4f}  m = {which:>5}: deterministic steps of the T03 proof hold from n = {hi:,}")
