#!/usr/bin/env python3
"""GB_PLAN quote arithmetic (stdlib; all inputs are MEASURED figures quoted in the plan, estimates labelled). python3 -I gb_quote.py"""
# --- measured bases
T5 = dict(setup=0.41, cal=10.56, isl=28.10, isa=2.21, merge=0.74, ev=0.07)         # results/T5_1e5.md, N 2500, R' 16, I3
M1 = dict(setup=15.25, cal=135.63, isl=269.25, merge=16.91, ev=0.40)                  # results/F1M_PILOT_FIT.md, I3
P7_pilot_island = 96 * (9 * 60 + 21) / 3600.0                                        # P7: calibration pilot island, 96 CPU x 9:21
cal_I0_10_5 = 0.10 * T5["cal"]                                                        # PREREG/FZ: I_max=0 calibration = 0.10 x I3 (measured at 10^4)
NF = 3.85                                                                             # N 10^4 / N 2500 island ratio, Owls same-machine (VN_MINILEG_NOTE §1), ONE datum
print("P7 pilot island core-h %.2f" % P7_pilot_island)
# --- 10^5 fit, AR n200, N 2500
I3_5 = T5["setup"] + T5["cal"] + T5["isl"] + T5["merge"] + T5["ev"]
I0_5 = T5["setup"] + cal_I0_10_5 + T5["isl"] + T5["merge"] + T5["ev"]
print("10^5 AR n200 N2500: I3 %.1f (T5 incl isa_check %.1f)  I0 %.1f  saving %.1f" % (I3_5, I3_5 + T5["isa"], I0_5, I3_5 - I0_5))
isl_share = T5["isl"] / I0_5
f_N = (1 - isl_share) + isl_share * NF
print("N=1e4 factor on 10^5 fit (I0) %.2f -> I0 %.1f I3 %.1f" % (f_N, I0_5 * f_N, (I3_5 - I0_5) + I0_5 * f_N))
# R'=64 extension of one fit: +48 islands (+ merge x3.1)
ext = 48 * T5["isl"] / 16 + T5["merge"] * (0.3 + 0.7 * 4 - 1)
print("R'=64 extension per fit (N2500) +%.1f; pair +%.1f" % (ext, 2 * ext))
# ADJ-OPP, IND factors from the committed 10^4 class table (E n200: AR 2.18, ADJ 2.69, IND 2.30)
fa, fi = 2.69 / 2.18, 2.30 / 2.18
# 10^5 rung, 12 fits, N 2500, I0 (E): n400 factor 1.0 (10^4 measured 0.77x; plan model 1.6x for P90)
rung_E = 5 * I0_5 + 3 * I0_5 * 1.0 + 2 * I0_5 * fi + 2 * I0_5 * fa
rung_P90 = (5 * I0_5 + 3 * I0_5 * 1.6 + 2 * I0_5 * fi + 2 * I0_5 * fa) * 1.30
rung_rem = rung_E - I0_5
print("rung 12 fits I0 N2500: E %.0f  P90 %.0f ; remaining 11 (pilot is rung fit 1): E %.0f ; at I3 +%.0f" % (rung_E, rung_P90, rung_rem, 12 * (I3_5 - I0_5)))
print("rung N=1e4 I0: E %.0f P90 %.0f; remaining 11: %.0f" % (rung_E * f_N, rung_P90 * f_N, rung_rem * f_N))
# --- 1M per fit
cal_I0_1m = P7_pilot_island  # grid built from the pilot island; ~ the pilot island itself (measured), + small
others = M1["setup"] + M1["merge"] + M1["ev"]
I3_1 = sum(M1.values())
I0_1 = others + cal_I0_1m + M1["isl"]
print("1M N2500: I3 %.0f (measured)  I0 %.0f (cal %.0f instead of %.0f: saving %.0f)" % (I3_1, I0_1, cal_I0_1m, M1["cal"], I3_1 - I0_1))
I0_1N = others + cal_I0_1m + M1["isl"] * NF
I3_1N = others + M1["cal"] + M1["isl"] * NF
print("1M N1e4: I0 %.0f  I3 %.0f" % (I0_1N, I3_1N))
sc_I0 = others + cal_I0_1m + 2 * M1["isl"]
print("1M self-check N5000 I0 %.0f" % sc_I0)
D_ratio = 1510 / 440.0
print("option D (n=1000) I0 N2500: %.0f" % (I0_1 * D_ratio))
# --- block totals (N2500, I0)
def block(u, n_reps_run, extra_rep, selfcheck, D, ca):
    fits = n_reps_run + extra_rep
    return dict(AR=fits * u, ADJ=u, weak=u, self=selfcheck, D=D, ca=ca)
ca_I0 = 450 * I0_1 / 440 + 150
for name, reps in (("(b) 19 reps frozen (reps 2-20)", 19), ("(a) re-run rep 1: 20 reps", 20), ("(c) (b)+21st rep: 20 reps", 20)):
    b = block(I0_1, reps, 0, sc_I0, I0_1 * D_ratio, ca_I0)
    tot = sum(b.values())
    print("%-34s N2500 I0: %s  total %.0f ; +25%% cont. on everything %.0f" % (name, {k: round(v) for k, v in b.items()}, tot, tot * 1.25))
# --- envelope position
closed_ledger_1119 = 2041.0; leg_in_ledger = 55.09; leg_total = 462.48; ident = 1.99
closed = closed_ledger_1119 - leg_in_ledger + leg_total + ident
print("closed %.1f (ledger 2,041 includes 55.09 of the 462.48 leg: no double count) " % closed)
ml, ml90, ml_cap, adj_r04 = 440.0, 510.0, 600.0, 4.0
pos_pre = closed + ml + adj_r04
print("after mini-leg: %.0f (P90 %.0f, cap %.0f)" % (pos_pre, closed + ml90 + adj_r04, closed + ml_cap + adj_r04))
pair = I0_5 + I3_5
print("G-B pair E %.0f -> %.0f" % (pair, pos_pre + pair))
print("G-B pair + ADJ-OPP pair (I0 %.0f + I3 %.0f) E %.0f" % (I0_5 * fa, I3_5 * fa, pair * (1 + fa)))
pos_rung = pos_pre + pair + rung_rem
print("after rung (E): %.0f ; P90-ish %.0f" % (pos_rung, pos_pre + pair * 1.35 + rung_P90 - I0_5))
for name, reps in (("(b)", 19), ("(a)/(c)", 20)):
    b = block(I0_1, reps, 0, sc_I0, I0_1 * D_ratio, ca_I0); t = sum(b.values())
    print("%s: after 1M (base) %.0f ; with 25%% cont. on the 1M block %.0f ; vs 28,300" % (name, pos_rung + t, pos_rung + t * 1.25))
# N* = 1e4 capacity
pair_N = (I0_5 + I3_5 - I0_5 * 0 ) * 0 + (I0_5 * f_N + (I3_5 - I0_5) + I0_5 * f_N)
rung_remN = rung_rem * f_N
posN = pos_pre + pair_N + rung_remN
avail = 28300 - posN
print("N*=1e4: pair %.0f ; rung rem %.0f ; position before 1M %.0f ; available %.0f ; fits at %.0f each: %.1f (no reserve), %.1f (25%% reserve)" % (pair_N, rung_remN, posN, avail, I0_1N, avail / I0_1N, avail / 1.25 / I0_1N))
