#!/usr/bin/env python3
"""vn_budget_rebase.py -- the PRE-DECLARED 1M table (MINILEG_PREREG section 6, `vn_budget.py`, sha 35591b2b...) RE-BASED on the measured mini-leg numbers. Descriptive; the pre-declared table governs.
Same formulas and unit costs as vn_budget.py; changes: spent = 2,450.40 (incl. VN_ID_1 1.99) + the mini-leg's measured 236.51 (the mini-leg is CLOSED, so not in `unspent`), and the island factor f = the measured
mean billed f. Stdlib."""
ENV = 28300.0; spent = 975.5 + 1010.43 + 462.48 + 1.99 + 236.51
M = dict(setup=15.25, calib3=135.63, islands=269.25, merge=16.91, eval=0.40); T5 = dict(setup=0.41, calib3=10.56, islands=28.10, merge=0.74, eval=0.07)
m1 = lambda f=1.0: M["setup"] + M["calib3"] * 0.10 + M["islands"] * f + M["merge"] + M["eval"]
f5 = lambda f=1.0, I0=True: T5["setup"] + T5["calib3"] * (0.10 if I0 else 1.0) + T5["islands"] * f + T5["merge"] + T5["eval"]
TWIN = 42.18; OTHER = 482 + 400 + 170; D = 3.43; N = 22
tot = lambda U, c=1.25: spent + c * U
print("spent %.2f (closed); remaining %.0f" % (spent, ENV - spent))
for F, lab in ((3.85, "pre-declared f 3.85"), (3.768, "MEASURED mean billed f 3.768"), (4.15, "measured max f 4.15")):
    print("\n== %s: 1M fit N 2,500 = %.1f ; N 10^4 = %.1f ; N 5,000 = %.1f ; 10^5 fit N 2,500 = %.1f, N 10^4 = %.1f (I_max-3 twin at N 10^4 %.1f)" % (lab, m1(), m1(F), m1(F / 2), f5(), f5(F), f5(F, False)))
    S = {"S0 KEEP everywhere": (12 * f5() + TWIN + OTHER + N * m1() + m1(F / 2) + D * m1()),
         "S1b all N 10^4, no D": (12 * f5(F) + f5(F, False) + OTHER + N * m1(F)),
         "S2 ADOPT default (10^5 at N 10^4; 1M N 2,500 + ONE N 10^4 + D at 2,500)": (12 * f5(F) + f5(F, False) + OTHER + N * m1() + m1(F) + D * m1()),
         "S5 ADOPT cost-neutral (R' 4 at N 10^4)": (12 * f5(F) + f5(F, False) + OTHER + N * m1(F / 4))}
    for k, U in S.items():
        print("  %-75s unspent %7.0f  no reserve %7.0f  +25%% %7.0f  %s" % (k, U, tot(U, 1.0), tot(U), "fits" if tot(U) <= ENV else "DOES NOT FIT"))
    fixed = f5(F, False) + 12 * f5(F) + OTHER
    room = (ENV - spent) / 1.25 - fixed; n = int(room // m1(F))
    print("  S4 ADOPT, 1M at N 10^4 for as many fits as fit (no D, no self-check): room %.0f -> %d fits at %.0f each; total with reserve %.0f" % (room, n, m1(F), tot(fixed + n * m1(F))))
