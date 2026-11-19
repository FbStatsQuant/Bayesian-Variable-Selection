#!/usr/bin/env python3
"""w2_pit_check.py -- where did the W2 outcome fall under the W1 Opus model (reproj_w1.py, imported read-only from W1_readback/reproj)?
W2 = fits 0..5 of reproj_w1.REM; actual W2 = 221.15 core-h (T 207.09 + V 14.06), 0 of 6 T fits escalated."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/BVS-wt/P1M/Docs/Experiments/P1M/results/overlap1e4/W1_readback/reproj"))
import numpy as np
import reproj_w1 as R
rng = np.random.default_rng(R.SEED)
Q, ess = R.posterior(rng, R.BASE, None)
o = R.simulate(rng, Q, R.BASE, fits=list(range(6)))
w2 = o["W2"]; nesc = o["esc"][:, :6].sum(1); tcost = o["cost"][:, :6].sum(1)
print(f"W1-model W2: E {w2.mean():.0f} P10/50/90 {[round(v) for v in R.q(w2)]}; ESS {ess:.0f}")
print(f"P(W2 <= 221.15) = {np.mean(w2 <= 221.15):.3f}; P(T cost <= 207.09) = {np.mean(tcost <= 207.09):.3f}")
print(f"E #esc in 6 = {nesc.mean():.2f}; P(0 of 6) = {np.mean(nesc==0):.3f}; P(<=1) = {np.mean(nesc<=1):.3f}")
for j, nm in enumerate(["ARweak r02 s1", "ARweak r02 s2", "ADJ r01 s2", "ADJ r02 s1", "ADJ r02 s2", "AR r01 s2"]):
    print(f"  {nm:<14s} P(esc) {o['esc'][:, j].mean():.2f}  E cost {o['cost'][:, j].mean():.1f}")
print("actual T costs: 23.16 7.66 36.73 47.41 43.13 49.01")
