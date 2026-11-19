#!/usr/bin/env python3
"""reproj_w1_extra.py -- (1) k1 thresholds for > 172.5 and for the 3:00 / 5:00 calibrate limit per design and node speed;
(2) W2 breach scenarios re-projected with W3 run under a 5:00 calibrate limit. Imports reproj_w1 (same folder)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import reproj_w1 as R
print("design speed | k1 first >172.5 | k1 first TIMEOUT 3:00 | cost k1=1 | +per k1 | cost at k1=14 (needs > 3:00? wall h)")
for d in ("AR", "ADJ", "ARweak"):
    for f in (0.92, 1.0, 1.08):
        g0 = R.G0[d] * f
        def cost(k1):
            wall = R.O0[d] + 14 * g0 + R.PIL1 * g0 + k1 * R.G1_RATIO * g0
            return R.FIXED + wall * R.CORE_PER_S + R.ISL40[d], wall
        k172 = next((k for k in range(1, 15) if cost(k)[0] > 172.5), None)
        kto = next((k for k in range(1, 15) if cost(k)[1] > 10800), None)
        print(f"{d:6s} {f:.2f} | {k172} | {kto} | {cost(1)[0]:.1f} | {cost(2)[0]-cost(1)[0]:.1f} | {cost(14)[0]:.0f} ({cost(14)[1]/3600:.2f} h)")
rng = np.random.default_rng(7)
R.NPRIOR = 3_000_000
c5 = dict(R.BASE); c5["cal_limit"] = 18_000.0
scen = {"S3 AR k1=7": [("AR", "slow", None, 7), ("ADJ", "slow", None, 1), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                       ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)],
        "S4 AR k1=14 TIMEOUT": [("AR", "slow", None, 14), ("ADJ", "slow", None, 1), ("ADJ", "slow", None, 4), ("ADJ", "slow", 13, None),
                                ("ARweak", "slow", None, 1), ("ARweak", "slow", None, 1)],
        "S4b ADJ k1=14 TIMEOUT": [("AR", "slow", None, 1), ("ADJ", "slow", None, 14), ("ADJ", "slow", 12, None), ("ADJ", "slow", 13, None),
                                  ("ARweak", "fast", None, None), ("ARweak", "slow", None, 1)]}
print("\nW2 scenario -> W3 under a 5:00 calibrate limit")
for lab, ex in scen.items():
    Q, ess = R.posterior(rng, R.BASE, ex)
    o = R.simulate(rng, Q, c5, fits=list(range(6, 12)))
    w2a = 13.0 + sum(R.fit_cost_det(*x) for x in ex)
    tot = R.SPENT + w2a + o["W3"]
    over = ((o["cost"][:, 6:] > 172.5) | o["to"][:, 6:]).any(1)
    print(f"{lab}: ESS {ess:.0f}; W2 {w2a:.0f}; W3 E {o['W3'].mean():.0f} P90 {np.percentile(o['W3'],90):.0f}; rung E {tot.mean():.0f} "
          f"P10/50/90 {[round(v) for v in R.q(tot)]}; P>2.1k {np.mean(tot>2100):.3f} P>2.5k {np.mean(tot>2500):.4f}; P(any W3 >172.5) {over.mean():.3f}")
