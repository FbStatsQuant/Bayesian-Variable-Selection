#!/usr/bin/env python3
"""T05 Monte Carlo through the exact representation (Lemma 1), seed fixed. W7-SEC.

Under G + ORTH, F(S) = kappa + log varpi(|S|) - (|S|/2) log n - nu log(c_n + V_S), with
V_S = R' + sum_{j not in S} T_j^2 + n^{-1} sum_{j in S} T_j^2, c_n = 0.02 V_tot/(n-1), T_j = sqrt(lambda_j) + xi_j,
xi iid N(0,1), R' ~ chi^2_{n-1-p}. The HPM is the top-k set (by T^2) at the best k (Corollary 1).

Outputs, per (n, p, s0, lambda):
  hpm   : MC estimate of P(S_dagger = S0);
  orac  : MC estimate of P(top-s0 by |z| = S0)  (known-size selector);
  limit : Phi(sqrt(lambda) - sqrt(tau))^{s0}  (the T05(ii) limit at c = sqrt(lambda) - sqrt(tau));
  U     : the finite-n upper bound of Theorem T05-U, optimised over delta on a grid;
  O     : the finite-n oracle failure bound of Proposition T05-O, optimised over x on a grid (reported as 1 - bound).
"""
import math, sys
import numpy as np
from scipy.stats import norm

SEED = 20261102

def logw_vec(p, K):
    k = np.arange(K + 1)
    from scipy.special import gammaln
    return -math.log(2) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))

def tau_n(n, p, s0):
    return math.log(n) + 2 * math.log((2 * p - s0) / s0)

def mc(n, p, s0, lam, reps, rng, chunk=200):
    K = min(p, n // 2)
    nu = 0.01 + n / 2
    lw = logw_vec(p, K)
    kk = np.arange(K + 1)
    hits = 0; orac = 0; done = 0
    while done < reps:
        b = min(chunk, reps - done)
        T = rng.standard_normal((b, p))
        T[:, :s0] += math.sqrt(lam)                 # S0 = {0..s0-1}, equal magnitudes, positive sign (WLOG)
        Rp = rng.chisquare(n - 1 - p, size=b) if n - 1 - p > 0 else np.zeros(b)
        T2 = T * T
        Vtot = Rp + T2.sum(axis=1)
        order = np.argsort(-T2, axis=1)[:, :K]
        top = np.take_along_axis(T2, order, axis=1)
        cs = np.concatenate([np.zeros((b, 1)), np.cumsum(top, axis=1)], axis=1)   # sum of top-k, k = 0..K
        V = Vtot[:, None] - (1 - 1 / n) * cs
        c = 0.02 * Vtot / (n - 1)
        g = lw[None, :] - 0.5 * kk[None, :] * math.log(n) - nu * np.log(c[:, None] + V)
        kh = np.argmax(g, axis=1)                    # first maximiser = smallest size (ties have prob. 0)
        topS0 = np.all(np.sort(order[:, :s0], axis=1) == np.arange(s0)[None, :], axis=1)
        hits += int(np.sum((kh == s0) & topS0))
        orac += int(np.sum(topS0))
        done += b
    return hits / reps, orac / reps

def U_bound(n, p, s0, lam):
    d = n - 1 - s0; tau = tau_n(n, p, s0); nup = (n - 1) * (n + 0.02) / n
    best = 1.0
    for delta in np.linspace(1e-4, 0.5, 2000):
        t = math.sqrt((1 - delta) * d * tau / nup)
        q = norm.cdf(math.sqrt(lam) - t) + norm.sf(math.sqrt(lam) + t)
        best = min(best, math.exp(-d * delta**2 / 4) + q**s0)
    return best

def O_bound(p, s0, lam):
    M = p - s0
    best = 1.0
    for x in np.linspace(0.01, 40, 4000):
        t = math.sqrt(2 * math.log(M) + 2 * x) if M >= 1 else 0.0
        best = min(best, math.exp(-x) + s0 * norm.cdf(t - math.sqrt(lam)))
    return best

if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    print(f"T05 Monte Carlo via Lemma 1; seed {SEED}; reps = {reps} per row (MC s.e. <= {0.5/math.sqrt(reps):.4f})")
    print("\n(A) threshold (ii): lambda = (sqrt(tau) + c)^2, s0 = 2, p = ceil(n^0.5)")
    print(f"{'n':>8} {'p':>6} {'c':>5} {'P(HPM=S0)':>10} {'Phi(c)^s0':>10} {'U-bound':>8} {'P(oracle)':>9}")
    for n in [10**3, 10**5, 10**7, 10**9]:
        p = math.ceil(n**0.5); s0 = 2; tau = tau_n(n, p, s0)
        for c in [-1.0, 0.0, 1.0]:
            lam = (math.sqrt(tau) + c) ** 2
            h, o = mc(n, p, s0, lam, reps, rng)
            print(f"{n:8.0e} {p:6d} {c:5.1f} {h:10.4f} {norm.cdf(c)**s0:10.4f} {U_bound(n, p, s0, lam):8.4f} {o:9.4f}")
    print("\n(B) gap (iii): p = ceil(n^a), a = 0.5, lambda = (1 - eps) tau with eps = 0.3 < 1/(1+2a) = 0.5")
    print(f"{'n':>8} {'p':>6} {'sqrt(lam)-sqrt(2logM)':>22} {'sqrt(tau)-sqrt(lam)':>20} {'P(HPM=S0)':>10} {'U-bound':>8} {'P(oracle)':>9} {'1-O-bound':>9}")
    for n in [10**3, 10**5, 10**7, 10**9]:
        a = 0.5; p = math.ceil(n**a); s0 = 2; tau = tau_n(n, p, s0); lam = 0.7 * tau
        h, o = mc(n, p, s0, lam, reps, rng)
        print(f"{n:8.0e} {p:6d} {math.sqrt(lam) - math.sqrt(2*math.log(p - s0)):22.3f} {math.sqrt(tau) - math.sqrt(lam):20.3f} "
              f"{h:10.4f} {U_bound(n, p, s0, lam):8.4f} {o:9.4f} {1 - O_bound(p, s0, lam):9.4f}")
    print("\n(C) the gap in amplitude units at p = n^a (leading order [sqrt(1+2a) - sqrt(2a)] sqrt(log n)):")
    for a in [0.25, 0.5, 0.75, 1.0]:
        for n in [10**3, 10**6, 10**12, 10**100]:
            p = n**a if a < 1 else n - 1; s0 = 2
            tau = math.log(n) + 2 * math.log((2 * p - s0) / s0)
            gap = math.sqrt(tau) - math.sqrt(2 * math.log(p - s0))
            lead = (math.sqrt(1 + 2 * a) - math.sqrt(2 * a)) * math.sqrt(math.log(n))
            print(f"  a={a:4.2f} n=1e{round(math.log10(n)):<3d} sqrt(tau)-sqrt(2log(p-s0)) = {gap:7.3f}   leading order {lead:7.3f}   "
                  f"energy ratio tau/2log(p-s0) = {tau/(2*math.log(p-s0)):6.3f}")
