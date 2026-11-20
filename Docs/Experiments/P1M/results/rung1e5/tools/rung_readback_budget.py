#!/usr/bin/env python3
"""RUNG_READBACK (2026-11-20): the D3 budget check (RUNG_PLAN section 5) and the measured 10^5 class costs / island factor. stdlib. python3 -I rung_readback_budget.py
Inputs MEASURED: the 16 fit costs of records/rung1e5 + records/gb (per-run cost files), ledger prior_after_R3.json 633.57, closed after G-B 2,984.56; 1M frozen unit costs from GB_PLAN section 6
(317 = 437.44 - 135.63 + P7 pilot island 14.96), 1M ablations + competitors 1,052 (plan values)."""
ar200 = [76.387, 69.000, 74.531, 60.769, 50.229]; ar400 = [46.738, 38.260, 44.240]; ind = [50.687, 63.376]; adj = [65.653, 69.971]
tAR, tAD = 29.567, 26.071
m = lambda x: sum(x) / len(x)
print("measured 10^5 class costs, N 10^4, I_max 0: AR n200 %.2f (n=5, %.1f-%.1f) | AR n400 %.2f (n=3) | IND n200 %.2f (n=2) | ADJ-OPP n200 %.2f (n=2) ; twins N 2,500: AR %.2f ADJ-OPP %.2f" % (m(ar200), min(ar200), max(ar200), m(ar400), m(ind), m(adj), tAR, tAD))
rho = m(ar400) / m(ar200)
import math
g = math.log2(rho)
u0 = 316.8
D_resized = max(u0, u0 * 5 ** g)
print("rho = AR n400 mean / AR n200 mean = %.4f ; g = log2 rho = %.3f ; n 1,000 = 5 x n 200 -> D = 317 x 5^g = %.1f -> floored at 317: %.1f ; plan value 1,087" % (rho, g, u0 * 5 ** g, D_resized))
isl = dict(AR10=73.507, AR25=26.760, AD10=62.400, AD25=23.560)
fAR, fAD = isl["AR10"] / isl["AR25"], isl["AD10"] / isl["AD25"]
f = (fAR + fAD) / 2
print("measured 10^5 island factor N 10^4 / N 2,500 (billed islands, same data, seed, grid): AR %.3f (T 30), ADJ-OPP %.3f (T 20), mean %.3f ; whole-fit ratio AR %.2f ADJ-OPP %.2f" % (fAR, fAD, f, 76.387 / tAR, 65.653 / tAD))
others = 15.25 + 14.96 + 16.91 + 0.40
for lab, ff in (("measured f %.2f" % f, f), ("pre-declared f 3.77", 3.768)):
    print("1M ONE N 10^4 fit (I_max 0): %s -> %.0f" % (lab, others + 269.25 * ff))
closed = 2984.56 + 633.57
print("closed spend after the rung: %.2f (LEDGER ~ 3,618)" % closed)
ENV = 28300.0; comp = 1052.0
oneN4 = others + 269.25 * f
seeds19 = 19 * u0
for lab, D in (("D re-sized (floor)", D_resized), ("D plan value 1,087", 1087.0)):
    base = 22 * u0 + oneN4 + D + comp          # rep 1 = (a): 22 frozen 1M fits (20 AR incl. the rep-1 re-run + ADJ-OPP + AR-weak)
    print("%-20s S2 with rep 1 = (a): 22 x 317 = %.0f + N10^4 fit %.0f + D %.0f + comp %.0f = %.0f -> position %.0f (%.1f%%) ; +25%% on unspent %.0f (%.1f%%) ; + H-34 (19 more seeds, seed 1 = the re-run) %.0f / %.0f (%.1f%% / %.1f%%)" % (
        lab, 22 * u0, oneN4, D, comp, base, closed + base, 100 * (closed + base) / ENV, closed + 1.25 * base, 100 * (closed + 1.25 * base) / ENV,
        closed + base + seeds19, closed + 1.25 * (base + seeds19), 100 * (closed + base + seeds19) / ENV, 100 * (closed + 1.25 * (base + seeds19)) / ENV))
worst = closed + 1.25 * (22 * u0 + (others + 269.25 * 3.768) + 1087.0 + comp + seeds19)
print("worst case (pre-declared f 3.77, D 1,087, H-34 seeds, 25%% reserve): %.0f (%.1f%%) <= 28,300: %s" % (worst, 100 * worst / ENV, worst <= ENV))
