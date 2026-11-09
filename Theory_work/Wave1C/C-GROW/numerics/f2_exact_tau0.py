"""Exact rational computation of the S5 TV margin tau0 (c = 1) on the coded partition {10b..10b+9} (reduction to
counts (a, b) of conditioning variables in the truth's own group / paired group), transcribed from reviews/R04
amendment 6.  tau0(c) = c^2 * tau0(1).  Output: F2_exact_tau0.txt."""
from fractions import Fraction as F
R, C = F(7, 10), F(3, 10)
mins = []
for t in (F(7, 5), F(-1), F(9, 5), F(-6, 5)):
    vals = []
    for a in range(5):
        for b in range(6):
            if a and b:
                A, B = 1 + (a - 1) * R, 1 + (b - 1) * R
                det = A * B - a * b * C * C
                g, d = (R * B - b * C * C) / det, (A * C - a * C * R) / det
            elif a:
                g, d = R / (1 + (a - 1) * R), F(0)
            elif b:
                g, d = F(0), C / (1 + (b - 1) * R)
            else:
                g = d = F(0)
            h = R * t + C - a * g * (F(2, 5) * t + C) - b * d * C
            v = 1 - a * g * R - b * d * C
            vals.append(h * h / v)
    mins.append(min(vals))
print("per-truth minima (c=1):", mins)
print("tau0(c=1) =", min(mins), "  tau0(c=0.5) =", min(mins) / 4)

# Partition used by the reduction, computed with the Python port's partition routine on the exact S5 correlation
# matrix (R08 item 6: the script itself now produces this line).
import numpy as np
import bvs_core as bc
p = 100
S = np.full((p, p), 0.3)
for g in range(20):
    S[5 * g:5 * g + 5, 5 * g:5 * g + 5] = 0.7
np.fill_diagonal(S, 1.0)
blocks = bc.partition_from_corr(S, 10)
print("partition (bvs_core.partition_from_corr, B = 10):", blocks)
print("consecutive blocks of 10:", all(list(b) == list(range(10 * i, 10 * i + 10)) for i, b in enumerate(blocks)))
