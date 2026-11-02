#!/usr/bin/env python3
"""W3-VT38E independent reproduction of W1-T38E counterexamples C0 and C1 (abstract state spaces, not BVS).

C0: three states a1, a2, o; log g0 = (0, -30, -5), log g1 = (-30, 0, -5); A = {a1, a2}.
C1: four states a1, m, a2, o; log g0 = (0, -120, -55.2, -10), log g1 = (-2000, -2000, 0, -1930); A = {a1, m, a2}.
    SMC: N iid pi0 draws; T uniform stages on [0,1]; weights exp(dphi d); multinomial resampling; one kernel step
    per stage at phi_t; then 9 kernel steps at phi = 1. Report fraction of islands with no particle in A, and Zhat/Z.

Kernels (o is isolated in all of them: zero exits from A):
  'W1'   : W1's kernel (a1->m and a2->m proposed w.p. 1, m->a1/a2 w.p. 1/2, plain Metropolis ratio).
           This kernel is NOT reversible w.r.t. gamma_phi (the proposal is asymmetric and no Hastings factor is used).
  'rev'  : lazy symmetric path proposal (each end proposes m w.p. 1/2, m proposes a1/a2 w.p. 1/2) + Metropolis:
           reversible w.r.t. gamma_phi restricted to A, so a valid SMC move kernel.
  'rev5' : 'rev' applied 5 times per stage (a stronger mutation, to show the mechanism is selection, not weak moves).
Seed 4242.  Run: python3 v2_toys_C0_C1.py
"""
import numpy as np
from math import log, exp

def lse(v):
    v = np.asarray(v, float); m = v.max(); return m + np.log(np.exp(v - m).sum())

# ---------------- C0 ----------------
lg0 = np.array([0.0, -30.0, -5.0]); lg1 = np.array([-30.0, 0.0, -5.0])
phis = np.linspace(0, 1, 100001)
def qA(phi, lg0, lg1, idx):
    lw = (1 - phi) * lg0 + phi * lg1; return np.exp(lse(lw[idx]) - lse(lw))
vals = np.array([qA(f, lg0, lg1, [0, 1]) for f in phis])
print("C0: q0(A)=%.5f q1(A)=%.5f inf q_phi(A)=%.4e at phi=%.4f; closed form at 1/2: 2e^-10/(1+2e^-10)=%.4e" % (
      vals[0], vals[-1], vals.min(), phis[vals.argmin()], 2 * exp(-10) / (1 + 2 * exp(-10))))

# ---------------- C1 ----------------
lg0 = np.array([0.0, -120.0, -55.2, -10.0]); lg1 = np.array([-2000.0, -2000.0, 0.0, -1930.0])
d = lg1 - lg0
pi0 = np.exp(lg0 - lse(lg0))
qo = np.array([1 - qA(f, lg0, lg1, [0, 1, 2]) for f in phis])
print("C1: pi0(A)=%.6f pi0(o)=%.4e  log10 pi(A^c)=%.1f  sup_phi q_phi(A^c)=%.4e at phi=%.4f  d(o)-d(a1)=%.1f" % (
      pi0[:3].sum(), pi0[3], (lg1[3] - lse(lg1)) / log(10), qo.max(), phis[qo.argmax()], d[3] - d[0]))

def acc(x): return exp(min(0.0, x))

def step(counts, phi, rng, kind):
    lw = (1 - phi) * lg0 + phi * lg1
    new = np.zeros(4, dtype=np.int64); new[3] = counts[3]
    pend = 1.0 if kind == 'W1' else 0.5          # prob an end state proposes m
    for s in (0, 2):
        k = rng.binomial(counts[s], pend * acc(lw[1] - lw[s])); new[1] += k; new[s] += counts[s] - k
    nm = counts[1]; k1 = rng.binomial(nm, 0.5); k2 = nm - k1
    x = rng.binomial(k1, acc(lw[0] - lw[1])); new[0] += x; new[1] += k1 - x
    x = rng.binomial(k2, acc(lw[2] - lw[1])); new[2] += x; new[1] += k2 - x
    return new

def island(N, T, rng, kind):
    reps = 5 if kind == 'rev5' else 1
    kk = 'rev' if kind == 'rev5' else kind
    c = rng.multinomial(N, pi0); logZ = lse(lg0); grid = np.linspace(0, 1, T + 1)
    for t in range(1, T + 1):
        dphi = grid[t] - grid[t - 1]
        alive = c > 0
        lw = np.full(4, -np.inf); lw[alive] = np.log(c[alive]) + dphi * d[alive]
        L = lse(lw[alive]); logZ += L - log(N)
        w = np.zeros(4); w[alive] = np.exp(lw[alive] - L)
        c = rng.multinomial(N, w / w.sum())
        for _ in range(reps): c = step(c, grid[t], rng, kk)
    for _ in range(9 * reps): c = step(c, 1.0, rng, kk)
    return c, logZ - lse(lg1)

rng = np.random.default_rng(4242)
T, R = 1000, 200
for kind in ('W1', 'rev', 'rev5'):
    for N in (10 ** 5, 10 ** 6):
        ext = 0; W = []; a2 = 0
        for r in range(R):
            c, lw = island(N, T, rng, kind); ext += (c[:3].sum() == 0); a2 += c[2] > 0; W.append(lw)
        W = np.array(W)
        print("C1[%s]: N=%d T=%d R=%d: P(no particle in A at end)=%.3f (se %.3f); P(a2 occupied)=%.3f; median log(Zhat/Z)=%.1f; "
              "frac Zhat/Z<1/2=%.3f" % (
              kind, N, T, R, ext / R, np.sqrt(ext / R * (1 - ext / R) / R), a2 / R, np.median(W), np.mean(W < log(0.5))))
