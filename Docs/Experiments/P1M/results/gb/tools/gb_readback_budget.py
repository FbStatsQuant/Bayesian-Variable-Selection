#!/usr/bin/env python3
"""G-B read-back (2026-11-20): the re-quote at the MEASURED G-B costs and the envelope position. stdlib. python3 -I gb_readback_budget.py
Inputs MEASURED: the 4 G-B fits (records/gb, cost files), closed 2,686.91 (MINILEG_READBACK), T5 (28.10 islands at N 2,500, I_max 3, T = 30), the 1M unit costs of GB_PLAN section 6.
ESTIMATES (labelled): IND = AR; AR n400 = 1.0 x AR (P90 1.6 x); rung P90 = 1.5 x; continuity twins from the I_max 0 stage costs with islands at the T5 / f-implied N 2,500 level."""
AR0, AR3, AD0, AD3 = 76.39, 83.11, 65.65, 72.50
gb = AR0 + AR3 + AD0 + AD3
closed = 2686.91 + gb
print("G-B set measured %.2f (quote 501: %.0f%%) ; closed after G-B %.2f" % (gb, 100 * gb / 501, closed))
isl = dict(AR0=73.51, AR3=71.12, AD0=62.40, AD3=62.77); T5isl = 28.10
print("islands billed N 10^4: AR I0 %.2f / I3 %.2f ; T5 (N 2,500, I3, same data and seed, T 30) %.2f -> implied f = %.2f (I3 pair) ; quote used f 3.768 (islands 105.9)" % (isl["AR0"], isl["AR3"], T5isl, isl["AR3"] / T5isl))
rem = 4 * AR0 + 3 * AR0 * 1.0 + 2 * AR0 * 1.0 + AD0           # AR r02-r05, AR n400 x3, IND x2 (= AR), ADJ-OPP r02
full = rem + AR0 + AD0
print("10^5 rung N 10^4 I_max 0, 12 fits at measured unit costs: %.0f ; remaining 10 after the two pilots: %.0f (P90 ~ %.0f) [GB_PLAN quote: 1,360 / 1,119]" % (full, rem, 1.5 * rem))
f_imp = isl["AR3"] / T5isl
ctAR = 0.5333 + 1.511 + isl["AR0"] / f_imp + 0.7644 + 0.0711
ctAD = 0.5067 + 1.813 + isl["AD0"] / f_imp + 0.8667 + 0.0667
print("continuity twins (N 2,500, I_max 0), ESTIMATE with the implied f %.2f: AR %.1f + ADJ-OPP %.1f = %.0f (HQ ~60; GB_PLAN 67)" % (f_imp, ctAR, ctAD, ctAR + ctAD))
ct = ctAR + ctAD
u0, u3, oneN4, D0, comp, seeds = 316.8, 437.0, 1062.0, 1087.0, 1052.0, 6335.0
b = 21 * u0 + oneN4 + D0 + comp; a = 22 * u0 + oneN4 + D0 + comp
base = closed + rem + ct
print("position before 1M %.0f" % base)
for lab, blk in (("(b) 21 frozen fits", b), ("(a)/(c) 22 frozen fits", a)):
    print("%-22s 1M items %.0f ; position %.0f (%.1f%%) ; +25%% on the unspent 1M items %.0f (%.1f%%) ; + H-34 seeds %.0f / %.0f (%.1f%% / %.1f%%)" % (lab, blk, base + blk, 100 * (base + blk) / 28300, base + 1.25 * blk, 100 * (base + 1.25 * blk) / 28300,
          base + blk + seeds - (u0 if "(a)" in lab else 0), base + 1.25 * (blk + seeds - (u0 if "(a)" in lab else 0)), 100 * (base + blk + seeds - (u0 if "(a)" in lab else 0)) / 28300, 100 * (base + 1.25 * (blk + seeds - (u0 if "(a)" in lab else 0))) / 28300))
print("if the 10^5 island factor (%.2f) held at 1M: the ONE N 10^4 1M fit = %.0f instead of %.0f (not measured at 1M; not used)" % (f_imp, 15.25 + 15.0 + 269.25 * f_imp + 17.3, oneN4))
