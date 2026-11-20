#!/usr/bin/env python3
"""GC_PLAN quote arithmetic (stdlib). python3 -I gc_quote.py
MEASURED: the 11-17 1M fit (F1M_PILOT_FIT: setup 15.25, calibrate 135.63, islands 269.25, merge 16.91, eval 0.40 = 437.44; P7 pilot island 14.96), the 10^5 rung / G-B (I_max 0 calibration 2-3 % of a fit; the
island factor N 10^4 / N 2,500 = 2.70 measured at 10^5; class means), closed 2,984.56 + rung 633.57 = 3,618.13. ESTIMATES (labelled): the I_max 0 calibration at 1M = the P7 pilot island + ~1 (export, grid);
the N 10^4 fit at the 10^5 factor (not measured at 1M; P90 at the 10^4-mini-leg factor 3.77); option D = the plan value 3.43 x; N 5,000 from a linear-in-N island model (f 1.57)."""
SETUP, CAL3, ISL, MERGE, EV = 15.25, 135.63, 269.25, 16.91, 0.40
P7 = 14.96
CAL0 = P7 + 1.0
u3 = SETUP + CAL3 + ISL + MERGE + EV
u0 = SETUP + CAL0 + ISL + MERGE + EV
print("1M fit: I_max 3 (11-17, measured) %.2f ; I_max 0 (frozen) E %.1f (calibration %.1f instead of %.1f: saving %.1f) ; plan unit 317" % (u3, u0, CAL0, CAL3, CAL3 - CAL0))
f = 2.698
others = SETUP + CAL0 + MERGE + EV
n10 = others + ISL * f; n10p90 = others + ISL * 3.768
f5 = 1 + (f - 1) / 3
n5 = others + ISL * f5
print("N 10^4 fit: E %.0f (f %.2f) ; P90 %.0f (f 3.77) ; N 5,000 option: E %.0f (f %.2f; plan 586)" % (n10, f, n10p90, n5, f5))
U = 317.0; ADJ = 330.0; D = 1087.0; COMP = 1052.0; N10 = 775.0
closed = 3618.13; ENV = 28300.0
rows = [("pilot (frozen rep-1 re-run)", 1 * U), ("AR replicates 2-20", 19 * U), ("ADJ-OPP r01", ADJ), ("AR-weak r01 (gated)", U), ("ONE N 10^4 fit on the rep-1 data", N10), ("option D (n 1,000)", D), ("ablations + competitors (plan values)", COMP)]
tot = sum(v for _, v in rows)
for k, v in rows:
    print("  %-40s %7.0f" % (k, v))
print("S2 block %.0f -> position %.0f (%.1f%%) ; +25%% on unspent %.0f (%.1f%%)" % (tot, closed + tot, 100 * (closed + tot) / ENV, closed + 1.25 * tot, 100 * (closed + 1.25 * tot) / ENV))
seeds = 19 * U
print("H-34 seeds (19, seed 1 = the pilot): %.0f -> position %.0f (%.1f%%) ; with 25%% on everything unspent %.0f (%.1f%%)" % (seeds, closed + tot + seeds, 100 * (closed + tot + seeds) / ENV, closed + 1.25 * (tot + seeds), 100 * (closed + 1.25 * (tot + seeds)) / ENV))
print("optional N 5,000 self-check: +%.0f (plan 586)" % n5)
p90 = 360 + 19 * U * 1.12 + 400 + 360 + 1062 + 1630 + COMP
print("P90 of the S2 block (assumption: pilot 360, replicates x1.12, ADJ-OPP 400, AR-weak 360, N10^4 1,062, D 1,630): %.0f -> position %.0f (%.1f%%)" % (p90, closed + p90, 100 * (closed + p90) / ENV))
print("worst stack (P90 S2 + seeds x1.12 + N5 option, 25%% reserve on all): %.0f (%.1f%%)" % (closed + 1.25 * (p90 + seeds * 1.12 + n5), 100 * (closed + 1.25 * (p90 + seeds * 1.12 + n5)) / ENV))
print("calibration sensitivity (Opus F4: the I_max 0 calibration share 14-21 %% of I_max 3): 19-29 per fit vs 15: +4..+14 per fit x 22 = %d..%d" % (22 * 4, 22 * 14))
for w, q in (("pilot", U), ("W1 (AR + ADJ-OPP)", U + ADJ), ("W2..W10 (AR pair)", 2 * U), ("X1 (AR-weak + N10^4)", U + N10), ("D", D), ("seed wave (pair)", 2 * U)):
    qq = 5 * round(q / 5); print("wave %-24s E %.0f quote %.0f stop %.0f" % (w, q, qq, 2 * qq))
S2E = U + 19 * U + ADJ + U + N10 + D
print("cumulative stop S2 fits: 1.6 x %.0f = %.0f ; seeds 1.6 x %.0f = %.0f" % (S2E, 1.6 * S2E, seeds, 1.6 * seeds))
print("per fit 1M sizes (11-17): islands 34.2, setup 10.1, calib 8.1, fit 2.4, data+raw 3.2, law 0.34 = 58.3 GB ; A-class (fit 2.4 + law 0.34 + sidecars ~0.05) ~ 2.8 GB x 43 fits = %.0f GB" % (2.8 * 43))
