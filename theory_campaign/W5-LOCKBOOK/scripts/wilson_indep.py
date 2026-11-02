#!/usr/bin/env python3
"""W5-LOCKBOOK: Wilson 95% intervals for the PROD-H resource_limit counts (independent of W2-BOOK's wilson.py)."""
from math import sqrt
z = 1.959963984540054
def wilson(k, n):
    ph = k / n; c = z * z / n
    centre = (ph + c / 2) / (1 + c); half = z * sqrt(ph * (1 - ph) / n + c / (4 * n)) / (1 + c)
    return centre - half, centre + half
for lab, k, n in [("all fits", 6, 2400), ("S5", 6, 400), ("S5, p = 1000", 5, 200), ("S5, p = 500", 1, 200)]:
    lo, hi = wilson(k, n); print(f"{lab:14s} {k}/{n} = {k/n:.4f}  Wilson 95% [{lo:.4f}, {hi:.4f}]")
