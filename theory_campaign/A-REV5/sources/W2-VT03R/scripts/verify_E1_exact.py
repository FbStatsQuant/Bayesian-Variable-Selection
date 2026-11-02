#!/usr/bin/env python3
"""W2-VT03R: independent, EXACT (integer/rational) check of W1-T03R Lemma E1 (a)-(d), Lemma E2 (i)-(iii)
and the threshold table of W1 REPORT section 3.  Written from the definitions in 00_COMMON.md, not from W1 code.

Definitions:  w(k) = 1/2 / C(2p-1,k);  q_k = C(p,k) w(k);  K = min(p, floor(n/2));
              R_m = sum_{m<k<=K} q_k / w(s0);  m_old = m_n(1/2 log n) = ceil((s0 log 2p + (s0+2)/2 log n)/log 2);
              m_sharp = min{m >= s0 : R_m <= n^{-(s0+2)/2}}.
The threshold test R_m <= n^{-(s0+2)/2} is decided EXACTLY:  R_m^2 * n^{s0+2} <= 1 (integers/Fractions).
For huge K the tail beyond kmax is bracketed:  q_{k+1}/q_k = rho_k <= 1/2 for k >= 1, so
   0 <= sum_{k>kmax} q_k <= q_kmax  (kmax >= 1);  we accept a decision only if lower and upper agree.
No randomness (no seed needed).
"""
from fractions import Fraction as F
from math import comb, log, ceil, exp, lgamma, factorial
import sys

def qratio_list(p, s0, kmax):
    """t_k = q_k / w(s0) for k = 0..kmax as exact Fractions, via t_{k+1} = t_k * rho_k, rho_k = (p-k)/(2p-1-k)."""
    # q_k/w(s0) = C(p,k) w(k)/w(s0) = C(p,k) C(2p-1,s0)/C(2p-1,k)
    t0 = F(comb(2 * p - 1, s0), 1)  # k = 0: C(p,0)=1, C(2p-1,0)=1
    out = [t0]
    for k in range(kmax):
        out.append(out[-1] * F(p - k, 2 * p - 1 - k))
    return out

def check_lemma_E1(p, s0, K):
    """Exact identity (a) and float-checked inequalities (b),(c),(d) for all m in [s0, K]."""
    t = qratio_list(p, s0, K)
    # (a): q_k/w(s0) == C(p,s0) prod_{i=s0}^{k-1} rho_i  for s0<=k<=K ; and the identity for rho_i
    for i in range(0, min(p - 1, K) + 1):
        assert F(p - i, 2 * p - 1 - i) == F(1, 2) * (1 - F(i - 1, 2 * p - 1 - i)), ("rho identity", p, i)
    for k in range(s0, K + 1):
        direct = F(comb(p, k) * comb(2 * p - 1, s0), comb(2 * p - 1, k))
        assert direct == t[k], ("t_k recursion", p, s0, k)
        prod = F(comb(p, s0))
        for i in range(s0, k):
            prod *= F(p - i, 2 * p - 1 - i)
        assert prod == t[k], ("E1(a)", p, s0, k)
    # suffix sums R_m exactly
    R = [F(0)] * (K + 2)
    for m in range(K - 1, -1, -1):
        R[m] = R[m + 1] + t[m + 1]
    worst_b, worst_c, worst_d = 0.0, 0.0, 0.0
    for m in range(s0, K + 1):
        Rm = R[m] if m < K else F(0)
        lC = log(comb(p, s0))
        gam = (m * (m - 1) - (s0 - 1) * (s0 - 2)) / (4 * (p - 1))
        ub = exp(lC - (m - s0) * log(2) - gam)
        if Rm > 0:
            assert float(Rm) <= ub * (1 + 1e-12), ("E1(b) fails", p, s0, m, float(Rm), ub)
            worst_b = max(worst_b, float(Rm) / ub)
        if s0 >= 1 and m <= K - 1:
            lb = exp(lC - (m + 1 - s0) * log(2) - (m * (m - 1) - (s0 - 1) * (s0 - 2)) / (4 * (p - m)))
            assert float(t[m + 1]) >= lb * (1 - 1e-12), ("E1(c) fails", p, s0, m)
            assert Rm >= t[m + 1]
            worst_c = max(worst_c, lb / float(Rm))
        if s0 >= 1 and Rm > 0:
            old = 4 * (2 * p) ** s0 * 2.0 ** (-m)
            fac = 4 * factorial(s0) * exp(gam)
            assert ub * fac <= old * (1 + 1e-12), ("E1(d) fails", p, s0, m)
            worst_d = max(worst_d, ub * fac / old)
    return R, worst_b, worst_c, worst_d

def m_old(n, p, s0, omega_half=True):
    return ceil((s0 * log(2 * p) + (s0 + 2) * log(n) / 2) / log(2))

def le_thresh(Rm, n, s0):
    """exact test Rm <= n^{-(s0+2)/2}  <=>  Rm^2 n^{s0+2} <= 1"""
    return Rm * Rm * n ** (s0 + 2) <= 1

def m_sharp_exact(n, p, s0, uncapped=False):
    K = p if uncapped else min(p, n // 2)
    mo = m_old(n, p, s0)
    kmax = min(K, max(mo, s0) + 80)
    t = qratio_list(p, s0, kmax)
    # suffix sums truncated at kmax; tail bracket [0, t[kmax]] if kmax < K
    tail_hi = t[kmax] if kmax < K else F(0)
    S = F(0)
    suff = {}
    for m in range(kmax - 1, -1, -1):
        S += t[m + 1]
        suff[m] = S
    for m in range(s0, kmax):
        lo, hi = suff[m], suff[m] + tail_hi
        a, b = le_thresh(lo, n, s0), le_thresh(hi, n, s0)
        if a and b:
            return m, K, mo
        if a != b:
            return ("UNDECIDED", m), K, mo
    return K, K, mo  # R_K = 0

def main():
    out = []
    # ---- Part 1: Lemma E1 exhaustively on a grid of small/medium p
    cnt = 0
    wb = wc = wd = 0.0
    for p in list(range(2, 41)) + [57, 100, 151, 300]:
        for n in sorted({3, 7, 2 * p, 2 * p + 1, 4 * p}):
            K = min(p, n // 2)
            for s0 in range(0, K + 1):
                if s0 > 25:
                    continue
                _, b, c, d = check_lemma_E1(p, s0, K)
                wb, wc, wd = max(wb, b), max(wc, c), max(wd, d)
                cnt += 1
    out.append(f"Part 1: Lemma E1 (a) exact identity + (b),(c),(d) inequalities checked on {cnt} (p,n,s0) triples, all m in [s0,K]: PASS")
    out.append(f"   max R_m/ub(b) = {wb:.4f} (<=1 required);  max lb(c)/R_m = {wc:.4f} (<=1);  max ub*4 s0! e^gam/old = {wd:.4f} (<=1)")

    # ---- Part 2: Lemma E2 (i)-(iii) on a grid (omega = 1/2 log n), exact thresholds
    bad = []
    rows = 0
    for n in [20, 50, 100, 200, 400, 1000, 3000]:
        for p in [10, 30, 100, 500, 1000]:
            for s0 in [1, 2, 5, 14]:
                if s0 > min(p, n // 2):
                    continue
                ms, K, mo = m_sharp_exact(n, p, s0)
                if isinstance(ms, tuple):
                    bad.append(("undecided", n, p, s0)); continue
                rows += 1
                # (i)
                if not (s0 <= ms <= min(K, mo)):
                    bad.append(("E2(i)", n, p, s0, ms, K, mo))
                # (ii) closed form: s0 + ceil((log C(p,s0) + (s0+1)/2 log n + 1/2 log n)/log2)
                cf = min(K, s0 + ceil((log(comb(p, s0)) + (s0 + 2) / 2 * log(n)) / log(2)))
                if ms > cf:
                    bad.append(("E2(ii)", n, p, s0, ms, cf))
                # (iii) lower bound when ms <= K-1
                if ms <= K - 1:
                    lbm = (log(comb(p, s0)) + (s0 + 2) / 2 * log(n)) / log(2) - 1 - ms * (ms - 1) / (4 * (p - ms) * log(2))
                    if ms - s0 < lbm - 1e-9:
                        bad.append(("E2(iii)", n, p, s0, ms, lbm))
    out.append(f"Part 2: Lemma E2 (i)-(iii) on {rows} (n,p,s0) cases with exact thresholds: " + ("PASS" if not bad else f"FAIL {bad}"))

    # ---- Part 3: W1 table (s0 = 14), exact
    A5 = log(500) / log(200)
    A10 = log(1000) / log(200)
    cases = [(200, 500), (200, 1000), (10**3, 500), (10**3, 1000), (10**4, 1000), (10**6, 1000),
             (10**4, round((10**4) ** A5)), (10**6, round((10**6) ** A5)), (10**8, round((10**8) ** A10))]
    out.append("Part 3: threshold table, s0 = 14 (exact rational decisions)")
    out.append("   n         p             K         m_old  m_sharp  m_sharp_uncapped  saving  log2(14!)=%.1f" % (log(factorial(14)) / log(2)))
    for n, p in cases:
        ms, K, mo = m_sharp_exact(n, p, 14)
        mu, _, _ = m_sharp_exact(n, p, 14, uncapped=True)
        out.append(f"   {n:<9} {p:<13} {K:<9} {mo:<6} {str(ms):<8} {str(mu):<17} {mo - ms if isinstance(ms, int) else '-'}")

    # ---- Part 4: first n where m_sharp < K, for p = n^{A5} (exact) and the locked m_old < K
    first_exact = first_old = None
    for n in range(200, 700):
        p = round(n ** A5)
        ms, K, mo = m_sharp_exact(n, p, 14)
        if first_exact is None and isinstance(ms, int) and ms < K:
            first_exact = n
        if first_old is None and mo < K:
            first_old = n
        if first_exact and first_old:
            break
    out.append(f"Part 4: p = round(n^(log500/log200)): first n with m_sharp < K: {first_exact};  first n with m_old < K: {first_old}")
    txt = "\n".join(out)
    print(txt)

if __name__ == "__main__":
    main()
