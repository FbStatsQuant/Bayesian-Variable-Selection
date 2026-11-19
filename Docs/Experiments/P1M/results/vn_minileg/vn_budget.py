#!/usr/bin/env python3
"""vn_budget.py -- (b) the 1M consequence of the V-N decision and the operating characteristics of the N rule (MINILEG_PREREG.md sections 3.4 and 6). Stdlib, deterministic.
  vn_budget.py > vn_budget_output.txt
Every input is printed with its source. Envelope = H-9 / H-14 28,300 core-h; the projection convention is CAMPAIGN_RUN_PLAN's stress line: spent + 1.25 x unspent (25 % contingency on
EVERYTHING still to spend), and the same without contingency. NO number here is a new measurement; the island factor f (N = 10^4 / N = 2,500) is the same-machine 3.85 (3.4-4.6)."""
import math, random, statistics as st

ENV = 28300.0
SPENT = [("closed to 11-18 10:05 (gates, T5, P7, F1M pilot 437.44, T6, rr2400 172.6, freeze check; LEDGER)", 975.5), ("10^4 overlap W0-W3 (LEDGER)", 1010.43),
         ("precision + 10^4 science leg, 194 fits incl. B1 (LEG_READBACK 6; ledger prior_after_S10)", 462.48), ("VN_ID_1 F2 identity check (F2_IDENTITY_CHECK)", 1.99)]
spent = sum(v for _, v in SPENT)
F = 3.85; F_HI = 4.6; F_LO = 3.4
# 1M fit stages at N 2,500, I_max 3 (F1M_PILOT_FIT: MEASURED 437.44) -> frozen I_max 0: calibration x 0.10 (leg: I_max 0 calibration = 0.10 x I_max 3 at 10^4; CAMPAIGN_FREEZE_ADDENDUM 1)
M = {"setup": 15.25, "calib3": 135.63, "islands": 269.25, "merge": 16.91, "eval": 0.40}
def m1(f=1.0, I0=True):           # one 1M fit, island factor f relative to N 2,500
    return M["setup"] + M["calib3"] * (0.10 if I0 else 1.0) + M["islands"] * f + M["merge"] + M["eval"]
# 10^5 fit (T5_1e5: MEASURED 42.18 = setup 0.41 + calibrate 10.56 + islands 28.10 + isa_check 2.21 + merge 0.74 + eval 0.07; isa_check is a T5-only D-32 check)
T5 = {"setup": 0.41, "calib3": 10.56, "islands": 28.10, "merge": 0.74, "eval": 0.07}
def f5(f=1.0, I0=True):
    return T5["setup"] + T5["calib3"] * (0.10 if I0 else 1.0) + T5["islands"] * f + T5["merge"] + T5["eval"]
MINI = 248.3; TWIN = 42.18; OTHER = 482 + 400 + 170          # mini-leg E (vn_quote_output.txt); G-B I_max-3 twin (H-30, ~42); ablations 482 + competitors 400 (MANIFEST v0.4) + 1M competitors 170 (CAMPAIGN_RUN_PLAN)
D_FACTOR = 3.43                                              # option D (n = 1,000) = 3.43 x a fit (MANIFEST v0.4 / CAMPAIGN_RUN_PLAN: 1,509 / 440)
NREP = 22                                                    # 20 AR-strong (H-14; rep 1 re-run frozen = option (a), the conservative reading) + ADJ-OPP + AR-weak (gated)

def total(unspent, cont=1.25):
    return spent + cont * unspent

def scen(name, u10_5, u1m, twin, d):
    U = MINI + twin + u10_5 + OTHER + u1m + d
    return (name, U, total(U, 1.0), total(U, 1.25))

print("INPUTS")
for k, v in SPENT:
    print("  spent  %9.2f  %s" % (v, k))
print("  spent  %9.2f  TOTAL (NOTE: the LEDGER line '~2,041' already contains A0 + P1 = 55.09 of the 462.48; '2,041 + 462 + 1.99' would count them twice)" % spent)
print("  envelope %.0f ; remaining before the mini-leg %.0f" % (ENV, ENV - spent))
print("  1M fit (MEASURED 437.44 at N 2,500, I_max 3): frozen I_max 0, N 2,500 = %.1f ; N 10^4 = %.1f (f %.2f; range %.1f at f %.1f .. %.1f at f %.1f) ; N 5,000 (f %.3f) = %.1f ; R'=4 at N 10^4 (equal island cost) ~ %.1f"
      % (m1(), m1(F), F, m1(F_LO), F_LO, m1(F_HI), F_HI, F / 2, m1(F / 2), m1(F / 4)))
print("  10^5 fit: T5 42.18 (I_max 3, N 2,500, incl. isa_check 2.21); frozen N 2,500 = %.1f ; N 10^4 = %.1f ; I_max-3 fallback N 2,500 = %.1f, N 10^4 = %.1f" % (f5(), f5(F), f5(1, False), f5(F, False)))
print("  mini-leg E %.1f (vn_quote_output) ; G-B I_max-3 twin %.1f ; ablations + competitors (plan values, unspent) %d ; option D = %.2f x a fit ; 1M fits = %d (20 AR-strong + ADJ-OPP + AR-weak)" % (MINI, TWIN, OTHER, D_FACTOR, NREP))

rows = []
base1m = NREP * m1()
rows.append(scen("S0  KEEP N 2,500 everywhere (self-check N 5,000 + option D)", 12 * f5(), base1m + m1(F / 2), TWIN, D_FACTOR * m1()))
rows.append(scen("S1  ADOPT, everything at N 10^4 (22 fits, option D)", 12 * f5(F), NREP * m1(F), f5(F, False) , D_FACTOR * m1(F)))
rows.append(scen("S1b ADOPT, everything at N 10^4, option D dropped", 12 * f5(F), NREP * m1(F), f5(F, False), 0.0))
rows.append(scen("S2  ADOPT: 10^5 rung at N 10^4; 1M at N 2,500 + ONE N 10^4 self-check (rep-1 data); option D at N 2,500", 12 * f5(F), base1m + m1(F), f5(F, False), D_FACTOR * m1()))
rows.append(scen("S3  ADOPT: 10^5 at N 10^4 only; 1M at N 2,500 (no 1M N 10^4 fit); N 5,000 self-check", 12 * f5(F), base1m + m1(F / 2), f5(F, False), D_FACTOR * m1()))
print("\nPROJECTION TABLE (core-h). total = spent %.0f + unspent; 'cont' = spent + 1.25 x unspent" % spent)
print("%-100s %9s %9s %9s %10s" % ("scenario", "unspent", "no cont", "+25% cont", "vs 28,300"))
for n, U, t0, t1 in rows:
    print("%-100s %9.0f %9.0f %9.0f %10s" % (n, U, t0, t1, "FITS" if t1 <= ENV else ("fits w/o cont" if t0 <= ENV else "DOES NOT FIT")))
# S4: how many 1M fits at N 10^4 fit (with 25 % contingency; the fixed items as S2 but no N 5,000 self-check and no option D)
for f, lab in ((F, "f 3.85"), (F_HI, "f 4.6 (P90)")):
    fixed = MINI + f5(f, False) + 12 * f5(f) + OTHER
    room = ((ENV - spent) / 1.25 - fixed)
    nfit = int(room // m1(f))
    print("S4  ADOPT, 1M at N 10^4 for as many fits as fit, no option D, no N 5,000 self-check [%s]: room for the 1M block %.0f -> %d fits at %.0f each (%d AR-strong + ADJ-OPP + AR-weak gated), cost %.0f, total with cont %.0f"
          % (lab, room, nfit, m1(f), nfit - 2, nfit * m1(f), total(fixed + nfit * m1(f))))
r4 = MINI + f5(F, False) + 12 * f5(F) + OTHER + NREP * m1(F / 4)
print("S5  ADOPT, COST-NEUTRAL: N 10^4 with R' = 4 (4 islands; equal island cost to N 2,500, R' 16; T's own R' is 4): 22 fits x %.1f = %.0f ; total with cont %.0f ; NEEDS an HQ ruling on D-6 (R' = 16 at every rung) and the 1M memory plan at N 10^4"
      % (m1(F / 4), NREP * m1(F / 4), total(r4)))
print("\nTIME (gate-paced; 1M island wall at N 2,500: 526-792 s on 96 CPUs, F1M_PILOT_FIT): N 10^4 island wall ~ %.0f-%.0f min (linear in N), limit 2 h: fits; 1M island memory at N 10^4 NOT measured (plan-only memory check required)." % (526 * F / 60, 792 * F / 60))

# operating characteristics of the registered rule for an N arm: ADOPT iff for each of M1, M2, M3 the geometric-mean ratio r <= 1/sqrt(c_X) and r < 1 in every dataset
rng = random.Random(20261119)
print("\nOPERATING CHARACTERISTICS of the N rule (registered rule, N = 10^4 vs 2,500; 3 datasets x 2 replicates; metrics independent (conservative); c_X = 3.85 x lognormal(0, 0.09))")
print("  sd(log ratio) per dataset: 0.15 / 0.10 (the PREREG R3 range for independent seeds) / 0.05 (paired seeds share the grid: an ASSUMPTION, measured at the verdict)")
print("%-10s %-22s %10s %10s %10s" % ("true r", "(1/sqrt N-scaling=0.5)", "sd .15", "sd .10", "sd .05"))
for rho in (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.85):
    ps = []
    for sd in (0.15, 0.10, 0.05):
        ok = 0; n = 20000
        for _ in range(n):
            c = F * math.exp(rng.gauss(0, 0.09)); bar = 1 / math.sqrt(c); good = True
            for _m in range(3):
                lr = [math.log(rho) + rng.gauss(0, sd) for _d in range(3)]
                if math.exp(sum(lr) / 3) > bar or max(lr) >= 0:
                    good = False
            ok += good
        ps.append(ok / n)
    print("%-10.2f %-22s %10.3f %10.3f %10.3f" % (rho, "<- bar ~ 0.51" if rho == 0.50 else "", *ps))
