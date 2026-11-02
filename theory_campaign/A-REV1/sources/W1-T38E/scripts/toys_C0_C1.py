#!/usr/bin/env python3
"""W1-T38E toy checks (abstract state spaces; NOT BVS instances).

C0: the T22(iv) endpoint bound does NOT transfer from the singleton S0 to a set A:
    q_0(A) and q_1(A) both ~1 while q_phi(A) is tiny at an intermediate phi.
C1: SMC extinction counterexample: start mass on A, uniform bridge mass on A
    (inf_phi q_phi(A) close to 1), ZERO exits from A, yet with multinomial
    resampling every particle of A dies; Zhat/Z << 1 (lower tail fails).
Bridge: gamma_phi = gamma_0^{1-phi} gamma_1^phi (as in v3: gamma_phi = gamma_0 e^{phi d}).
Fixed seed. Run: python3 toys_C0_C1.py
"""
import numpy as np
from math import log, exp

def lse(v):
    v = np.asarray(v, float); m = v.max(); return m + np.log(np.exp(v - m).sum())

def q_phi(lg0, lg1, phi):
    lw = (1 - phi) * lg0 + phi * lg1
    return np.exp(lw - lse(lw))

phis = np.linspace(0, 1, 20001)

# ---------------- C0 ----------------
# states: a1 (start mode), a2 (truth), o (outside); A = {a1, a2}
lg0 = np.array([0.0, -30.0, -5.0]); lg1 = np.array([-30.0, 0.0, -5.0])
qA = np.array([q_phi(lg0, lg1, f)[:2].sum() for f in phis])
print("C0: q_0(A)=%.4f q_1(A)=%.4f inf_phi q_phi(A)=%.3e at phi=%.3f" % (qA[0], qA[-1], qA.min(), phis[qA.argmin()]))

# ---------------- C1 ----------------
# states 0=a1, 1=m, 2=a2, 3=o ; A = {a1, m, a2}; path kernel a1-m-a2 (Metropolis), o isolated
lg0 = np.array([0.0, -120.0, -55.2, -10.0])
lg1 = np.array([-2000.0, -2000.0, 0.0, -1930.0])
d = lg1 - lg0
pi0 = np.exp(lg0 - lse(lg0)); pi1 = np.exp(lg1 - lse(lg1))
qo = np.array([q_phi(lg0, lg1, f)[3] for f in phis])
print("C1: pi0(A)=%.6f pi(A)=%.6f pi0(o)=%.3e sup_phi q_phi(A^c)=%.3e (phi=%.4f); d(o)-d(a1)=%.1f" %
      (pi0[:3].sum(), pi1[:3].sum(), pi0[3], qo.max(), phis[qo.argmax()], d[3] - d[0]))

def ea(x):
    return exp(min(0.0, x))

def mh_round(counts, phi, rng):
    lw = (1 - phi) * lg0 + phi * lg1
    new = np.zeros(4, dtype=np.int64); new[3] += counts[3]
    # a1 -> propose m
    acc = ea(lw[1] - lw[0]); k = rng.binomial(counts[0], acc); new[1] += k; new[0] += counts[0] - k
    # a2 -> propose m
    acc = ea(lw[1] - lw[2]); k = rng.binomial(counts[2], acc); new[1] += k; new[2] += counts[2] - k
    # m -> propose a1 or a2 with prob 1/2 each
    nm = counts[1]; k1 = rng.binomial(nm, 0.5); k2 = nm - k1
    a = ea(lw[0] - lw[1]); x = rng.binomial(k1, a); new[0] += x; new[1] += k1 - x
    a = ea(lw[2] - lw[1]); x = rng.binomial(k2, a); new[2] += x; new[1] += k2 - x
    return new

def run_island(N, T, rng):
    counts = rng.multinomial(N, pi0)
    grid = np.linspace(0, 1, T + 1)
    logZhat = lse(lg0)  # log Zbar_0
    for t in range(1, T + 1):
        dphi = grid[t] - grid[t - 1]
        lw = np.where(counts > 0, np.log(np.maximum(counts, 1)) + dphi * d, -np.inf)
        logZhat += lse(lw[counts > 0]) - log(N)
        w = np.exp(lw - lse(lw[counts > 0])); w[counts == 0] = 0
        counts = rng.multinomial(N, w / w.sum())
        counts = mh_round(counts, grid[t], rng)
    for _ in range(9):  # terminal rounds (L + 4 with L = 5, illustrative)
        counts = mh_round(counts, 1.0, rng)
    return counts, logZhat - lse(lg1)

rng = np.random.default_rng(20261102)
T, R = 1000, 200
for N in (100000, 1000000):
    ext = 0; W = []
    for r in range(R):
        c, lW = run_island(N, T, rng)
        ext += (c[:3].sum() == 0); W.append(lW)
    W = np.array(W)
    print("C1: N=%d T=%d R=%d: fraction of islands with NO particle in A at the end = %.3f; median log(Zhat/Z) = %.1f; "
          "fraction with Zhat/Z<0.5 = %.3f" % (N, T, R, ext / R, np.median(W), np.mean(W < log(0.5))))
print("Mechanism: the o-lineage (start mass 4.5e-5, discrepancy 80 nats above a1) takes over by selection before the")
print("A-internal kernel can move a1 -> a2 (only possible near phi=1); when the few initial o copies die by drift, A survives.")
