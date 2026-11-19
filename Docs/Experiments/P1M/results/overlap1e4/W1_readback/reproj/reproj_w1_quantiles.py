#!/usr/bin/env python3
"""reproj_w1_quantiles.py -- BASE P10/P50/P90 per wave, counted-only basis, and the same for the 5:00-limit variant."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import reproj_w1 as R
for lab, cfg in (("BASE (3:00)", R.BASE), ("5:00 limit W2+W3", {**R.BASE, "cal_limit": 18_000.0}), ("W2 3:00 (released), W3 5:00", {**R.BASE, "cal_limit_W3": 18_000.0})):
    rng = np.random.default_rng(R.SEED)
    Q, ess = R.posterior(rng, cfg)
    o = R.simulate(rng, Q, cfg)
    t = o["total"]; tc = t - (R.SPENT - R.SPENT_COUNTED); c2 = R.SPENT + o["W2"]
    f = lambda x: "E %.0f P10/50/90 %s" % (x.mean(), [round(v) for v in R.q(x)])
    print(lab, "| W2", f(o["W2"]), "| W3", f(o["W3"]), "| cum after W2", f(c2), "| rung", f(t))
    print("   counted-only basis:", f(tc), "P>1.6k %.2f P>2.1k %.3f" % (np.mean(tc > 1600), np.mean(tc > 2100)))
    over = (o["cost"] > 172.5) | o["to"]
    print("   P>1.6k %.2f P>2.1k %.3f P>2.5k %.4f P(any>172.5 or TO) %.3f P(TO) %.3f" % (np.mean(t>1600), np.mean(t>2100), np.mean(t>2500), over.any(1).mean(), o["to"].any(1).mean()))
    print("   P(W3 > 1280) %.4f  P(W3>2*700) %.4f  E# esc AR in W3 %.2f  P(all 6 W3 AR esc) %.3f" % (np.mean(o["W3"] > 1280), np.mean(o["W3"] > 1400), o["esc"][:, 6:].sum(1).mean(), o["esc"][:, 6:].all(1).mean()))
