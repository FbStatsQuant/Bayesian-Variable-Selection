#!/usr/bin/env python3
"""RUNG_PLAN quote arithmetic (stdlib). python3 -I rung_quote.py
MEASURED: G-B fits (AR n200 76.39, ADJ-OPP n200 65.65, N 10^4 I_max 0; records/gb), G-B stage costs of the I_max 0 pilots, T5 islands 28.10 (N 2,500), closed 2,984.56 (GB_READBACK).
ESTIMATES (labelled): n400 = 1.0 x AR (P90 1.6 x), IND = 1.0 x AR (P90 1.3 x), AR n200 / ADJ-OPP P90 1.2 x; continuity twins from the I_max 0 stage costs with f = 2.53 (the island factor implied by T5);
T6 = (reference island + 2 killed runs + the resumed run) wall at 48 CPUs from the G-B islands wall 396-447 s x the measured T6 ratio at N 2,500 (T6: 4:02 wall for islands of 1:52-2:33)."""
AR, AD = 76.39, 65.65
f = 71.12 / 28.10
ctAR = 0.5333 + 1.511 + 73.51 / f + 0.7644 + 0.0711
ctAD = 0.5067 + 1.813 + 62.40 / f + 0.8667 + 0.0667
t6_wall_min = 447 / 60 * (4 + 2 / 60) / (2 + 25 / 60) * 1.15      # T6 N 2,500: 4:02 over a 1:52-2:33 island (mean 2:23); +15 % for the 60-s cadence and the larger N 10^4 checkpoint
t6 = 48 * t6_wall_min / 60
print("T6 estimate: wall %.1f min -> %.1f core-h (worst 72 = 48 x 1.5 h)" % (t6_wall_min, t6))
r1 = AR + (ctAR + ctAD) + t6
r2 = 4 * AR + 2 * AR
r3 = 2 * AR + AD
print("R1: RG_1a AR n400 r01 %.1f + RG_1b twins %.1f (AR %.1f + ADJ-OPP %.1f) + T6 %.1f = %.1f" % (AR, ctAR + ctAD, ctAR, ctAD, t6, r1))
print("R2: RG_2a AR n200 r02-r05 %.1f + RG_2b AR n400 r02-r03 %.1f = %.1f" % (4 * AR, 2 * AR, r2))
print("R3: RG_3a IND x2 %.1f + RG_3b ADJ-OPP r02 %.1f = %.1f" % (2 * AR, AD, r3))
tot = r1 + r2 + r3
new = 4 * AR + 3 * AR + 2 * AR + AD
print("rung new fits (10) %.1f ; + twins %.1f = %.1f (HQ 813) ; + T6 %.1f = TOTAL %.1f" % (new, ctAR + ctAD, new + ctAR + ctAD, t6, tot))
p90 = 4 * AR * 1.2 + 3 * AR * 1.6 + 2 * AR * 1.3 + AD * 1.2 + (ctAR + ctAD) * 1.2 + 20
print("P90 (assumption: factors above, T6 20) %.0f" % p90)
for nm, q in (("R1", r1), ("R2", r2), ("R3", r3)):
    qq = 5 * round(q / 5)
    print("wave %s quote %.0f -> wave stop (2x) %.0f" % (nm, qq, 2 * qq))
print("cumulative stop 1.6 x %.0f = %.0f -> round up to 100: %d ; projection ceiling 1,326 (S2 rung figure) - G-B pilots 142.04 = %.0f of new spend" % (tot, 1.6 * tot, -(-int(1.6 * tot) // 100) * 100, 1326 - 142.04))
closed = 2984.56
pos = closed + tot
print("closed %.2f + rung %.0f = %.0f" % (closed, tot, pos))
u0, oneN4, D0, comp, seeds = 316.8, 1062.0, 1087.0, 1052.0, 6335.0
for lab, n in (("(b) 21 frozen fits", 21),):
    blk = n * u0 + oneN4 + D0 + comp
    print("%s 1M items %.0f ; position %.0f (%.1f%%); +25%% on unspent 1M items %.0f (%.1f%%); + H-34 seeds %.0f / %.0f" % (lab, blk, pos + blk, 100 * (pos + blk) / 28300, pos + 1.25 * blk, 100 * (pos + 1.25 * blk) / 28300, pos + blk + seeds, pos + 1.25 * (blk + seeds)))
