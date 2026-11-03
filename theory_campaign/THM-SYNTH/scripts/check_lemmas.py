#!/usr/bin/env python3
"""THM-SYNTH scripts/check_lemmas.py — numerical checks of the three elementary NEW-SYNTH claims.

Run:  ~/.config/bvs-hq/owls/owls_run -j 1 -- python3 -I scripts/check_lemmas.py
Seed: 20261103. Pure python + fractions; no numpy needed.

(1) Lemma KL (THEOREM_LIST S2(c)): for probability vectors pi, pi0 on a finite set with a distinguished state S0,
    KL(pi||pi0) >= (1 - d1) * log(1/pi0(S0)) - log 2,   d1 = 1 - pi(S0).
    Checked on random vectors (exact KL in floats) and on adversarial vectors concentrated near S0.
(2) Isolation probability (THEOREM_LIST C1(a)): for a uniformly random equipartition of P items into K blocks of size
    s = P/K, P(a given other item shares the block of item j) = (s-1)/(P-1); P(j isolated from g given items)
    = C(P-1-g, s-1)/C(P-1, s-1)  >= 1 - g (s-1)/(P-1).  Checked exactly (fractions) and by Monte Carlo.
(3) Hub projection coefficient (THEOREM_LIST C1(e)): for an equicorrelated group of size g (corr rho) whose hub has
    corr psi with an outside column x_a, theta_hub = -psi*beta, theta_a = beta: the population projection coefficient
    of mu onto the group's span has hub entry psi*beta*([Sigma_bb^{-1}]_{11} - 1), which is 0 iff g = 1 (isolated hub)
    and > 0 for g >= 2, rho > 0; the marginal covariance cov(x_hub, mu) is 0 for every g.
"""
import math, random
from fractions import Fraction
from math import comb

random.seed(20261103)

# ---------- (1) Lemma KL ----------
def kl(p, q):
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q) if pi > 0)

def rand_simplex(m):
    v = [random.expovariate(1.0) for _ in range(m)]
    s = sum(v); return [x / s for x in v]

worst = float("inf"); cases = 0
for trial in range(20000):
    m = random.randint(2, 12)
    pi0 = rand_simplex(m)
    # pi: either random, or concentrated near state 0 with mass 1 - d1
    if trial % 2 == 0:
        pi = rand_simplex(m)
    else:
        d1 = random.random() ** 3
        rest = rand_simplex(m - 1)
        pi = [1 - d1] + [d1 * r for r in rest]
    # make pi0(S0) sometimes tiny (masked start)
    if trial % 3 == 0:
        pi0[0] *= 10 ** (-random.uniform(0, 12)); s = sum(pi0); pi0 = [x / s for x in pi0]
    d1 = 1 - pi[0]
    lhs = kl(pi, pi0); rhs = (1 - d1) * math.log(1 / pi0[0]) - math.log(2)
    worst = min(worst, lhs - rhs); cases += 1
print(f"(1) Lemma KL: {cases} cases, min(KL - bound) = {worst:.6g}  -> {'PASS' if worst >= -1e-9 else 'FAIL'}")

# ---------- (2) isolation probability ----------
def p_share_exact(P, s):
    return Fraction(s - 1, P - 1)

def p_isolated_exact(P, s, g):
    return Fraction(comb(P - 1 - g, s - 1), comb(P - 1, s - 1))

def mc_isolated(P, K, g, reps=20000):
    s = P // K; hits = 0
    items = list(range(P))
    for _ in range(reps):
        random.shuffle(items)
        block = {it: i // s for i, it in enumerate(items)}
        # item 0 = masked hub; items 1..g = partner + group members
        if all(block[0] != block[j] for j in range(1, g + 1)):
            hits += 1
    return hits / reps

print("(2) isolation probability for uniform equipartition")
print("     P    K   g   exact P(isolated)   lower bound 1-g(s-1)/(P-1)   Monte Carlo")
for (P, K, g) in [(16, 2, 1), (16, 2, 4), (64, 4, 4), (64, 8, 4), (256, 16, 9), (1024, 32, 9)]:
    s = P // K
    ex = p_isolated_exact(P, s, g); lb = 1 - g * Fraction(s - 1, P - 1)
    mc = mc_isolated(P, K, g, reps=4000)
    print(f"  {P:5d} {K:4d} {g:3d}   {float(ex):.4f}             {float(lb):+.4f}                      {mc:.4f}")
    assert ex >= lb - Fraction(0)  # the union bound is a valid lower bound (may be negative)
    assert abs(float(ex) - mc) < 0.03
print("     share probability (s-1)/(P-1): P=16,K=2 ->", p_share_exact(16, 8), "; P=1024,K=32 ->", p_share_exact(1024, 32))
print("     -> P(isolated) -> 1 as K grows (g fixed); at K=2, g=4 it is", float(p_isolated_exact(16, 8, 4)), "(bounded away from 0, small)")

# ---------- (3) hub projection coefficient ----------
def inv_equicorr(g, rho):
    # (1-rho) I + rho 11^T  ->  inverse = I/(1-rho) - rho/((1-rho)(1+(g-1)rho)) 11^T
    a = 1 / (1 - rho); b = rho / ((1 - rho) * (1 + (g - 1) * rho))
    return [[(a if i == j else 0.0) - b for j in range(g)] for i in range(g)]

print("(3) hub projection coefficient beta0_hub in a subset containing the hub's group but not x_a")
print("     g   rho   psi   beta   cov(x_hub,mu)   beta0_hub (formula)   beta0_hub (direct Sigma^-1 cov)")
for (g, rho, psi, beta) in [(1, 0.7, 0.5, 1.0), (2, 0.7, 0.5, 1.0), (4, 0.7, 0.5, 1.0), (9, 0.4, 0.2, 1.0), (5, 0.9, 0.3, 2.0)]:
    # group columns: index 0 = hub; cov(x_k, mu): hub: theta_hub + psi*beta = 0; member k: rho*theta_hub + 0 = -rho*psi*beta
    cov = [(-psi * beta + psi * beta)] + [(-rho * psi * beta)] * (g - 1)
    Sinv = inv_equicorr(g, rho) if g > 1 else [[1.0]]
    beta0 = [sum(Sinv[i][j] * cov[j] for j in range(g)) for i in range(g)]
    formula = psi * beta * (Sinv[0][0] - 1)
    print(f"   {g:3d}  {rho:.2f}  {psi:.2f}  {beta:.1f}    {cov[0]:+.3f}          {formula:+.5f}               {beta0[0]:+.5f}")
    assert abs(cov[0]) < 1e-12 and abs(formula - beta0[0]) < 1e-9
    if g == 1: assert abs(beta0[0]) < 1e-12
    else: assert beta0[0] > 0
print("     -> isolated hub (g=1 in its subset): beta0_hub = 0 exactly (Song-Liang Cor 2 excludes it);")
print("        hub with its group present: beta0_hub != 0 (Stage 1 can retain it). Condition 5 fails for every g.")
print("ALL CHECKS PASSED")
