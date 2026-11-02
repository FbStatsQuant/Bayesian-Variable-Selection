#!/usr/bin/env python3
"""High-replicate check that the MC estimate of P(S_dagger = S0) does not exceed the proven bound (U) at the row of
t05_mc.txt where the point estimate was 0.0009 above it (n = 1e7, p = 3163, s0 = 2, c = 0). Seed fixed. W7-SEC."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t05_mc import mc, U_bound, tau_n
from scipy.stats import norm
rng = np.random.default_rng(20261105)
n = 10**7; p = math.ceil(n**0.5); s0 = 2; tau = tau_n(n, p, s0); lam = tau
reps = 100000
h, o = mc(n, p, s0, lam, reps, rng, chunk=500)
se = math.sqrt(h * (1 - h) / reps)
print(f"n={n} p={p} s0={s0} c=0 reps={reps}: P(HPM=S0) = {h:.4f} (s.e. {se:.4f}); U-bound = {U_bound(n, p, s0, lam):.4f}; Phi(0)^2 = 0.25")
