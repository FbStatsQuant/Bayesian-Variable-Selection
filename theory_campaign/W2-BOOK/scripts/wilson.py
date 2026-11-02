#!/usr/bin/env python3
"""Wilson 95% intervals for the observed guard-stop rates (PROD-H, BRIEFING 2026-10-28 / D61). Deterministic."""
from math import sqrt
z = 1.959963984540054
def wilson(x, n):
    c = (x + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * sqrt(x * (n - x) / n + z * z / 4)
    return max(0.0, c - h), c + h
for label, x, n in [("all fits", 6, 2400), ("S5 (both p, both c)", 6, 400), ("S5, p = 1000", 5, 200), ("S5, p = 500", 1, 200)]:
    lo, hi = wilson(x, n)
    print(f"{label:22s} {x}/{n} = {x/n:.4f}   Wilson 95% [{lo:.4f}, {hi:.4f}]")
