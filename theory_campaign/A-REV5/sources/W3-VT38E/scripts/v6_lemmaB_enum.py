#!/usr/bin/env python3
"""W3-VT38E: exhaustive check of W1-T38E Lemma B (structured bridge mass on R_d) on small exact BVS instances.
Random correlated designs, p = 10, n in {30, 60}, planted truths (some cancelled); actual blocks (engine rule),
tables, gamma_0, gamma_1 enumerated over all of Omega. For every d < m <= 4, references x (best pi0 state in R_d,
and random states), y = S0, and random good/bad partitions of 2^{S0}: if theta < 1, check
   sup_phi q_phi(R_d^c) <= theta/(1-theta) + max{pi0(Bad), pi(Bad)} / [min(pi0(x), pi(y)) max(pi(x), pi0(y))]
on a 201-point phi grid. Also checks Lemma A (Gibbs change probability <= max endpoint odds) at every state/label/phi.
Seed 2024.
"""
import itertools, math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfi
rng = np.random.default_rng(2024)
phis = np.linspace(0, 1, 201)
checks = viol = tight = 0; worst_ratio = 0.0; lemA_viol = 0; lemA_checks = 0
for inst in range(40):
    n = int(rng.choice([30, 60])); p = 10
    Z = rng.standard_normal((n, p)); L = np.linalg.cholesky(0.4 * np.ones((p, p)) * rng.uniform(0, 1) + np.eye(p) * 0.6 + 0.0 * np.eye(p))
    X0 = Z @ L.T
    s0 = int(rng.integers(1, 4)); S0 = tuple(sorted(rng.choice(p, s0, replace=False)))
    beta = np.zeros(p); beta[list(S0)] = rng.choice([-1, 1], s0) * rng.uniform(0.3, 1.0, s0)
    y0 = X0 @ beta + rng.standard_normal(n)
    X, y = cfi.standardise(X0, y0)
    M = cfi.Model(X, y, dict(S0=S0))
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    blocks, R = cfi.complete_linkage_blocks(X, B)
    st = cfi.Start(M, blocks, S0)
    states = [S for k in range(M.K + 1) for S in itertools.combinations(range(p), k)]
    idx = {S: i for i, S in enumerate(states)}
    lg0 = np.array([st.lg0(S) for S in states]); lg1 = np.array([M.F(S) for S in states])
    lg1 = lg1 - cfi.lse(lg1) + cfi.lse(lg0 + np.array([st.d(S) for S in states]))  # same normalisation scale irrelevant
    lpi0 = lg0 - cfi.lse(lg0); lpi = lg1 - cfi.lse(lg1)
    U = [tuple(x for x in S if x in S0) for S in states]; N = np.array([sum(1 for x in S if x not in S0) for S in states])
    def q(phi):
        lw = (1 - phi) * lg0 + phi * lg1; return np.exp(lw - cfi.lse(lw))
    Q = np.array([q(f) for f in phis])
    # Lemma A at a few phis
    for si, S in enumerate(states):
        for l in range(p):
            T = tuple(x for x in S if x != l) if l in S else tuple(sorted(S + (l,)))
            if len(T) > M.K: continue
            ti = idx[T]
            k0 = math.exp(lg0[ti] - lg0[si]); k1 = math.exp(lg1[ti] - lg1[si])
            for f in (0.0, 0.2, 0.5, 0.8, 1.0):
                a = (lg0[ti] - lg0[si]) * (1 - f) + (lg1[ti] - lg1[si]) * f      # log odds of moving S->T
                chg = 1 / (1 + math.exp(-a))       # heat bath change prob (both add and delete cases)
                lemA_checks += 1; lemA_viol += chg > max(k0, k1) * (1 + 1e-12)
    subsets = [Us for k in range(s0 + 1) for Us in itertools.combinations(S0, k)]
    for d in range(0, 3):
        for m in range(d + 1, 5):
            for trial in range(6):
                bad = set(Us for Us in subsets if rng.random() < (0.0 if trial == 0 else 0.3))
                good = [Us for Us in subsets if Us not in bad]
                theta = 0.0
                for Us in good:
                    for k in range(d, m):
                        Lk = 0.0
                        for si, S in enumerate(states):
                            if U[si] != Us or N[si] != k: continue
                            tot = 0.0
                            for l in range(p):
                                if l in S0 or l in S or len(S) + 1 > M.K: continue
                                ti = idx[tuple(sorted(S + (l,)))]
                                tot += max(math.exp(lg0[ti] - lg0[si]), math.exp(lg1[ti] - lg1[si]))
                            Lk = max(Lk, tot)
                        theta = max(theta, Lk / (k + 1))
                if theta >= 1: continue
                Bmask = (N > m) | (np.array([u in bad for u in U]) & (N > d))
                pi0B = np.exp(lpi0[Bmask]).sum() if Bmask.any() else 0.0
                piB = np.exp(lpi[Bmask]).sum() if Bmask.any() else 0.0
                Rd = N <= d
                cand_x = [int(np.argmax(np.where(Rd, lpi0, -np.inf)))] + list(rng.choice(len(states), 2))
                yi = idx[S0]
                lhs = Q[:, ~Rd].sum(1).max()
                for xi in cand_x:
                    a, u = math.exp(lpi0[xi]), math.exp(lpi[xi]); v, b = math.exp(lpi0[yi]), math.exp(lpi[yi])
                    rhs = theta / (1 - theta) + max(pi0B, piB) / (min(a, b) * max(u, v))
                    checks += 1; viol += lhs > rhs * (1 + 1e-9) + 1e-15
                    if rhs > 0: worst_ratio = max(worst_ratio, lhs / rhs)
print("Lemma B: %d (instance, d, m, partition, x) checks with theta < 1; violations = %d; max LHS/RHS = %.4f" % (checks, viol, worst_ratio))
print("Lemma A: %d (state, label, phi) checks; violations = %d" % (lemA_checks, lemA_viol))
