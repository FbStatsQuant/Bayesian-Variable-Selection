#!/usr/bin/env python3
"""W3-VT38E: D2 step 5 check. From x0 = {1} in CF(1), estimate P(one engine round at temperature phi scores S0)
and compare with W1's uniform-in-phi lower bound beta = (1 - Dep)_+ / (|D| + B + 3).
Usage: python3 v5_d2_round_prob.py n seed reps     (seed -1: W1's design via env W1DIR). Simulation seed 99.
"""
import sys, os
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], '0']          # reuse v4's setup with 0 pilot replications
NREP = int(os.environ.get('REPS', '4000'))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4_d2_pilot.py')).read())
rng = np.random.default_rng(99)
for phi in (0.0, 0.03, 0.1, 0.3, 1.0):
    hits = 0
    for _ in range(NREP):
        h = [None]; one_round(x0, phi, h); hits += h[0] is not None
    print("phi=%.2f: P(round from x0 scores S0) = %.4f (+- %.4f) vs beta = %.4f" % (phi, hits / NREP, (hits / NREP * (1 - hits / NREP) / NREP) ** 0.5, beta))
