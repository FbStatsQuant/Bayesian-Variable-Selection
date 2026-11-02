"""ORTH at large (n, p) through sufficient statistics and null order statistics (seed 20261102).

Under ORTH (X'X = (n-1)I) every quantity is explicit in z_j = x_j'y:  x_j = z_j^2/(n Qbar), D_S = n^{|S|},
log BF(S) = -(|S|/2) log n - nu log(1 - X_S),  X_S = sum_{j in S} x_j,  tables the same per block.
Nulls: x_j'Y = sigma sqrt(n-1) Z_j, Z_j iid N(0,1).  We draw the top K0 null Z^2 exactly as order statistics of
m iid chi2_1 (exponential spacings), so p can be astronomically large.  Truths: x_j'Y = (n-1)theta_j + sigma sqrt(n-1) Z_j.

Reported, for w = 2 (one-step importance sampling pi0 -> pi):
  LB   = log(1 + max_k Ratio_k), Ratio_k = gamma_2(S0 u E_k)/gamma_2(S0), E_k = top-k nulls (assumed in distinct
         truth-free blocks: true w.p. -> 1 when k^2 B / p -> 0).  EXACT lower bound on ell(2) = -log q_2(S0).
  SEP  = Lemma SEP upper bound on ell(2) (q(2) from the top K0 exactly + conditional expectation for the rest).
  FD   = F-DRAFT's W(c) prediction  [R2 log p - 1/2 log n]_+ .
  kstar = argmax_k.  Since 1 + chi2(pi||pi0) = pi(S0)^2 exp(ell(2)) / pi0(S0), ell(2) is log(1+chi2) up to o(1).
"""
import math

import numpy as np
from scipy import integrate, stats

rng = np.random.default_rng(20261102)
A0 = B0 = 0.01


def g(z):
    return -np.log1p(-z)


def run(n, p, theta, sigma=1.0, K0=20000, w=2.0):
    s0 = len(theta)
    m = p - s0
    K0 = min(K0, m)
    # top-K0 order statistics of m iid chi2_1
    G = np.cumsum(rng.exponential(size=K0))
    U = G / (m + rng.normal(0, math.sqrt(m)))     # Gamma_{m+1} ~ m
    Z2top = stats.chi2.isf(U, 1)
    if m <= 200000:                                   # small m: draw all nulls directly
        Z2top = np.sort(rng.chisquare(1, size=m))[::-1][:K0]
    tau = Z2top[-1] if K0 < m else float(Z2top[-1])
    sumZ2_all = m + math.sqrt(2 * m) * rng.normal()
    Zt = rng.normal(size=s0)
    nm1 = n - 1.0
    chi_res = max(nm1 - p, 0.0) + math.sqrt(2 * max(nm1 - p, 1.0)) * rng.normal() if nm1 - p > 0 else 0.0
    YtY = nm1 * np.sum(theta ** 2) + 2 * math.sqrt(nm1) * sigma * np.sum(theta * Zt) + sigma ** 2 * (sumZ2_all + np.sum(Zt ** 2) + chi_res)
    sy2 = YtY / nm1
    Qb = 2 * B0 + nm1
    nu = A0 + n / 2.0
    xt = ((nm1 * theta + sigma * math.sqrt(nm1) * Zt) ** 2 / sy2) / (n * Qb)
    cnull = sigma ** 2 * nm1 / (sy2 * n * Qb)          # x_j = cnull * Z_j^2 for nulls
    xtop = cnull * Z2top
    s = xt.sum()
    XN = cnull * sumZ2_all
    ubar = XN / (1 - s)
    R2 = 1 - (1 - s)          # = s, the realised truth fit fraction
    # ---- LB: exact single-chain terms
    k = np.arange(1, K0 + 1)
    XE = np.cumsum(xtop)
    ok = XE < 1 - s
    ii = np.arange(K0, dtype=float)
    logprior = np.cumsum(np.log((s0 + ii + 1) / (2.0 * p - 1 - s0 - ii)))   # log w(s0+k)/w(s0), no cancellation
    logratio = logprior - 0.5 * k * math.log(n) + w * nu * (g(s + XE) - g(s)) - (w - 1) * nu * np.cumsum(g(xtop))
    logratio[~ok] = -np.inf
    i = int(np.argmax(logratio))
    LB = float(np.logaddexp(0, logratio[i]))
    # ---- SEP upper bound
    beta = (w / ((1 - s) * (1 - ubar)) - (w - 1)) if w >= 1 else 1 / ((1 - s) * (1 - ubar))
    c1 = beta * nu * cnull
    top = np.sum(np.exp(c1 * Z2top - 0.5 * math.log(n)))
    # E[e^{c1 Z^2} | Z^2 < tau]
    # E[e^{c1 Z^2} | Z^2 < tau], integrated in z (smooth integrand)
    zt = math.sqrt(tau)
    fz = lambda z: 2 * math.exp(c1 * z * z - 0.5 * z * z) / math.sqrt(2 * math.pi)
    Ein = integrate.quad(fz, 0, zt, limit=400)[0] / stats.chi2.cdf(tau, 1)
    rest = (m - K0) * Ein / math.sqrt(n)
    q = (top + rest) / p
    trunc = float(np.sum(np.log1p(2 * p * math.sqrt(n) * np.exp(-nu * xt))))
    SEP = trunc - (s0 + 1) * math.log1p(-q) if (q < 1 and ubar < 1) else float("inf")
    FD = max(0.0, R2 * math.log(p) - 0.5 * math.log(n))
    return dict(n=n, p=p, R2=R2, ubar=ubar, LB=LB, kstar=i + 1, SEP=SEP, q=q, FD=FD,
                logrho=R2 * math.log(p) - 0.5 * math.log(n))


def main():
    lines = []
    th = np.array([3 / math.sqrt(2), 3 / math.sqrt(2)])   # R2_pop = 0.9
    hdr = f"{'log10 n':>7} {'A':>5} {'R2':>6} {'ubar':>8} {'R2logp-.5logn':>13} {'FD=W(c)':>8} {'LB ell(2)':>10} {'k*':>6} {'SEP ell(2)':>10} {'q(2)':>9}"
    print(hdr); lines.append(hdr)
    for A in (0.4, 0.5, 0.7, 0.85, 0.95):
        for e in (4, 6, 8, 10, 12, 14, 16):
            n = 10 ** e
            p = int(n ** A)
            r = run(n, p, th)
            row = (f"{e:7d} {A:5.2f} {r['R2']:6.3f} {r['ubar']:8.2e} {r['logrho']:13.2f} {r['FD']:8.2f} {r['LB']:10.3g} "
                   f"{r['kstar']:6d} {r['SEP']:10.3g} {r['q']:9.2e}")
            print(row); lines.append(row)
    with open(__file__.replace("scripts", "results").replace(".py", ".txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
