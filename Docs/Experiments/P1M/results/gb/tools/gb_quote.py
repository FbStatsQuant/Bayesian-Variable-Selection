#!/usr/bin/env python3
"""GB_PLAN (final) quote arithmetic. stdlib; inputs are MEASURED figures quoted in the plan (estimates labelled). python3 -I gb_quote.py
v2 (2026-11-20): N* = 10^4 with the MEASURED island factor f = 3.768 (mean billed, 12 mini-leg pairs, MINILEG_READBACK T4); closed 2,686.91 (MINILEG_READBACK section 5)."""
T5 = dict(setup=0.41, cal=10.56, isl=28.10, isa=2.21, merge=0.74, ev=0.07)        # results/T5_1e5.md (N 2,500, R' 16, I_max 3)
M1M = dict(setup=15.25, cal=135.63, isl=269.25, merge=16.91, ev=0.40)             # results/F1M_PILOT_FIT.md
P7_PILOT_ISLAND = 96 * (9 * 60 + 21) / 3600.0                                      # 14.96
F = 3.768
CAL0 = 0.10 * T5["cal"]                                                            # I_max 0 calibration (10^4: x0.10)
MERGE_N = 0.80                                                                     # merge slightly up with N (10^4: non-island residual 0.36 -> 0.55 at R' 64)
ADJ = 2.69 / 2.18                                                                  # committed 10^4 class ratio ADJ-OPP / AR
IND = 2.30 / 2.18


def fit5(N, I, f=1.0):
    isl = T5["isl"] * (F if N == 10000 else 1.0) * f
    return T5["setup"] + (CAL0 if I == 0 else T5["cal"]) + isl + (MERGE_N if N == 10000 else T5["merge"]) + T5["ev"]


def adj(N, I):      # ADJ-OPP: islands x ADJ, the rest as AR
    return fit5(N, I) + T5["isl"] * (F if N == 10000 else 1.0) * (ADJ - 1)


print("== 10^5 fits (E): AR n200 | ADJ-OPP n200")
for N in (2500, 10000):
    for I in (0, 3):
        print("N %5d I_max %d: AR %.1f  ADJ-OPP %.1f" % (N, I, fit5(N, I), adj(N, I)))
pilotA, twinA, pilotD, twinD = fit5(10000, 0), fit5(10000, 3), adj(10000, 0), adj(10000, 3)
print("G-B set at N 10^4: AR pair %.0f (%.1f + %.1f) ; ADJ-OPP pair %.0f (%.1f + %.1f) ; set %.0f" % (pilotA + twinA, pilotA, twinA, pilotD + twinD, pilotD, twinD, pilotA + twinA + pilotD + twinD))
print("   the +49 approved at N 2,500 (ADJ-OPP I_max 3 twin) = %.1f ; at N 10^4 it is %.1f" % (adj(2500, 3), twinD))
print("   net of rung (the I_max 0 fits are rung fits): twins only %.0f" % (twinA + twinD))
# rung at N 10^4, I_max 0 (E): AR n200 x5, AR n400 x3 (1.0x; P90 1.6x on islands), IND x2, ADJ-OPP x2
isl = T5["isl"] * F
rungE = 5 * fit5(10000, 0) + 3 * fit5(10000, 0) + 2 * (fit5(10000, 0) + isl * (IND - 1)) + 2 * adj(10000, 0)
rungP = (5 * fit5(10000, 0) + 3 * (fit5(10000, 0) + 0.6 * isl) + 2 * (fit5(10000, 0) + isl * (IND - 1)) + 2 * adj(10000, 0)) * 1.25
rem = rungE - pilotA - pilotD
print("rung 12 fits N10^4 I0: E %.0f (P90 ~%.0f); the 2 pilots are rung fits (AR r01, ADJ-OPP r01) -> remaining 10: %.0f (P90 ~%.0f)" % (rungE, rungP, rem, rungP - pilotA - pilotD))
# FAIL branch: config (N 2500, I_max 3) = the I_max-3 verdict KEEP: rung 12 fits at N 2,500 I3
rungF = 5 * fit5(2500, 3) + 3 * fit5(2500, 3) + 2 * (fit5(2500, 3) + T5["isl"] * (IND - 1)) + 2 * adj(2500, 3)
print("FAIL branch rung (N 2500, I3) 12 fits: %.0f (all new; the N 10^4 fits are reported only)" % rungF)
# continuity twins: 2 fits at 10^5 N 2,500 on the same data + seeds as AR r01 and ADJ-OPP r01
ct0, ct3 = fit5(2500, 0) + adj(2500, 0), fit5(2500, 3) + adj(2500, 3)
print("continuity twins (AR r01 + ADJ-OPP r01 at N 2,500): I_max 0 %.0f ; (I_max 3 would be %.0f, not used)" % (ct0, ct3))
# 1M per fit
others = M1M["setup"] + M1M["merge"] + M1M["ev"]
u0 = others + P7_PILOT_ISLAND + M1M["isl"]; u3 = sum(M1M.values()); u0N = others + P7_PILOT_ISLAND + M1M["isl"] * F
print("1M per fit: N2500 I0 %.0f (I3 %.0f measured) ; N 10^4 I0 %.0f ; N 5000 I0 %.0f" % (u0, u3, u0N, others + P7_PILOT_ISLAND + M1M["isl"] * 2))
Dr = 1510 / 440.0
D0 = u0 * Dr
ca = 482 + 400 + 170.0                                                            # ablations + competitors (all rungs) + 1M competitors: plan values, as MINILEG vn_budget (unchanged, not re-costed)
print("option D (n=1000, x3.43) I0 N2500 %.0f ; ablations+competitors (plan values) %.0f" % (D0, ca))
# envelope
closed = 2686.91; ENV = 28300.0
print("closed %.2f, remaining %.0f" % (closed, ENV - closed))
seeds20 = 20 * u0
print("H-34 20 seeds on ONE 1M dataset (N 2500, I0): %.0f (HQ: ~6.4k)" % seeds20)
for lab, reps in (("(b) rep 1 separate: 21 frozen fits (19 AR + ADJ + weak)", 21), ("(a)/(c) 22 frozen fits", 22)):
    blk = reps * u0
    s2 = blk + u0N + D0 + ca
    print("%-58s 1M block %.0f ; + one N10^4 fit %.0f + D %.0f + comp %.0f = %.0f" % (lab, blk, u0N, D0, ca, s2))
def pos(reps, with_seeds, branch="PASS"):
    gb = pilotA + twinA + pilotD + twinD
    r = rem
    cont = ct0
    blk = reps * u0 + u0N + D0 + ca
    seeds = seeds20 - (u0 if reps >= 22 else 0) if with_seeds else 0   # under (a) seed 1 of the block IS the rep-1 re-run
    return closed + gb + r + cont + blk + seeds, closed + gb + r + cont + (blk + seeds) * 1.25 - 0
for reps, lab in ((21, "(b)"), (22, "(a)")):
    for ws in (False, True):
        e, e25 = pos(reps, ws)
        print("%s seeds=%s: position %.0f (%.1f%%) ; reserve 25%% on the unspent 1M items: %.0f (%.1f%%)" % (lab, ws, e, 100 * e / ENV, e25, 100 * e25 / ENV))
# FAIL branch totals (I3 at N 2500; KEEP row; N 5000 self-check)
u3b = u3; sc3 = others + M1M["cal"] + M1M["isl"] * 2; D3 = 1510.0; ca3 = ca
gbF = pilotA + twinA + pilotD + twinD
blkF = 21 * u3b + sc3 + D3 + ca3
posF = closed + gbF + rungF + blkF
print("FAIL branch: G-B set %.0f + rung %.0f + 1M block %.0f (21 x %.0f + self-check %.0f + D %.0f + comp %.0f) -> position %.0f (%.1f%%); +25%% on unspent: %.0f; + H-34 20 seeds at I3 %.0f -> %.0f" % (gbF, rungF, blkF, u3b, sc3, D3, ca3, posF, 100 * posF / ENV, closed + (gbF + rungF + blkF) * 1.25, 20 * u3b, closed + (gbF + rungF + blkF + 20 * u3b) * 1.25))
# stops
for nm, E in (("AR pilot I0", pilotA), ("AR twin I3", twinA), ("ADJ pilot I0", pilotD), ("ADJ twin I3", twinD), ("cont AR I0 N2500", fit5(2500, 0)), ("cont ADJ I0 N2500", adj(2500, 0))):
    Ec = round(E)
    print("class model %-18s E %4d  soft %5.1f  hard %5.1f" % (nm, Ec, 1.5 * Ec, 2.5 * Ec))
