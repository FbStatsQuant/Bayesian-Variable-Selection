#!/usr/bin/env python3
"""quote_b1.py -- cost quote of the boundary add-on B1 (AR-weak, p=1e4, n=100, ONE dataset, V x2 seeds + T x2 seeds). Stdlib only, fixed seed.
Basis = the 20 measured T fits and 20 measured V fits of the overlap (n=200); n=100 is unmeasured (stated assumptions below)."""
import random, math
class st:
    mean = staticmethod(lambda xs: sum(xs) / len(xs))
import os
random.seed(20261119)
NF = float(os.environ.get("NF", 0.85)); PH = float(os.environ.get("PH", 0.75)); BETA = tuple(float(x) for x in os.environ.get("BETA", "2.1,3.9").split(","))   # defaults = the quoted case
# measured T fit totals (core-h, billed incl. escalation; W*_readback/*escalation.csv fit_total_core_h), n = 200
T_ESC   = [110.12, 60.72, 143.96]                                   # the 3 tier-1 fits (AR r01 s1, ARweak r01 s1, IND s2)
T_HARD0 = [48.28, 49.01, 36.73, 47.41, 43.13, 39.31, 41.88, 35.82, 39.44, 51.49, 36.56, 50.53]  # tier-0 AR / ADJ / IND fits
T_EASY0 = [9.28, 23.16, 7.66]                                      # tier-0 ARweak fits (posterior concentrated on S0)
V_AW200 = [1.62, 1.76, 2.08, 1.76]                                 # measured V ARweak n200 fits
def lognorm(m, s): return m * math.exp(random.gauss(0, s))
def one():
    nf = lognorm(NF, 0.20)                       # n=100 per-step cost factor, one draw per dataset (planning nf(100) = 0.7, nf(200) = 1.0; unmeasured for T)
    # dataset-level hardness: P(escalate | fit) ~ Beta, mean 0.35 (observed 3/20 = 0.15; a spread-out posterior should escalate MORE, so more than double)
    pesc = random.betavariate(*BETA)
    # P(posterior needs many calibration rebuilds = 'hard' tier-0 cost): ARweak n200 was 1/3 hard-like (the escalated one); here posterior is spread -> 0.75
    phard = PH
    tot = 0.0; Tc = []
    for _ in range(2):                              # T seeds
        if random.random() < pesc:
            c = lognorm(sum(T_ESC) / 3 * 0.95, 0.30) * nf
            if random.random() < 0.10: c *= 2.2    # tier 2 (N = 1.6e5): never seen, p = 0.1 given escalation
        else:
            base = random.choice(T_HARD0) if random.random() < phard else random.choice(T_EASY0)
            c = lognorm(base, 0.15) * nf
        Tc.append(c)
    Vc = [lognorm(st.mean(V_AW200) * (nf ** 0.5) * 1.1, 0.20) for _ in range(2)]   # V: ~ n-scaling sqrt-ish, +10% for a longer grid on a spread posterior
    return sum(Tc), sum(Vc), max(Tc)
R = [one() for _ in range(20000)]
def q(xs, p): xs = sorted(xs); return xs[int(p * (len(xs) - 1))]
tot = [t + v for t, v, _ in R]; Ts = [t for t, _, _ in R]; Vs = [v for _, v, _ in R]; mx = [m for _, _, m in R]
print("n=100 AR-weak, 2 T + 2 V fits (20,000 reps, seed 20261119)")
for lab, xs in (("T (2 fits)", Ts), ("V (2 fits)", Vs), ("TOTAL", tot)):
    print("%-11s E %.1f  P50 %.1f  P90 %.1f  P99 %.1f" % (lab, st.mean(xs), q(xs, .5), q(xs, .9), q(xs, .99)))
print("single T fit: P(> 172.5) = %.4f ; max-T-fit P90 %.0f" % (sum(m > 172.5 for m in mx) / len(mx), q(mx, .9)))
print("P(total > 120) = %.3f ; P(total > 2 x E) = %.3f" % (sum(x > 120 for x in tot) / len(tot), sum(x > 2 * st.mean(tot) for x in tot) / len(tot)))
print("sensitivity: the overlap's flat mean of all 20 T fits (incl. NULL) = %.1f; 2 T + 2 V at that mean + V 2.5 = %.1f" % (st.mean(T_ESC + T_HARD0 + T_EASY0 + [2.3, 2.3]), 2 * st.mean(T_ESC + T_HARD0 + T_EASY0 + [2.3, 2.3]) + 5))
