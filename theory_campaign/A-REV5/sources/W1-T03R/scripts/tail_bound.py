#!/usr/bin/env python3
"""W1-T03R task 5: exact BB(1,p) size tail versus the locked 2^{-m} bound.

Quantities (notation of 00_COMMON.md; PROOF.md section 1):
  w(k) = 1/2 / C(2p-1,k),  q_k = C(p,k) w(k),  K = min(p, floor(n/2)).
  R_m  = varpi(|S|>m)/varpi(S0) = sum_{m<k<=K} q_k / w(s0)          (exact; W_K cancels)
  Old proof's bound on the same ratio (Lemma prior (c),(d) of PROOF_v3): R_m <= 4 (2p)^{s0} 2^{-m}.
  New closed form (Lemma E1(b)):  R_m <= C(p,s0) 2^{-(m-s0)} exp(-[m(m-1)-(s0-1)(s0-2)]/(4(p-1))).
  Lower bound (Lemma E1(c)):      R_m >= C(p,s0) 2^{-(m+1-s0)} exp(-[m(m-1)-(s0-1)(s0-2)]/(4(p-m)))  (s0>=1, m+1 <= K).
Thresholds at omega = (1/2) log n (the m_n used by T02(ii)/T03):
  m_old = ceil((s0 log(2p) + (s0+1)(log n)/2 + omega)/log 2)                   (00_COMMON)
  m_sharp = min{m >= s0 : R_m <= n^{-(s0+2)/2}}                               (exact; <= K always)
  m_cf    = min(K, ceil(s0 + [log C(p,s0) + (s0+2)/2 log n]/log 2))           (closed-form, no Gaussian factor)
All computations in log space with exact log-gamma (mpmath, 50 digits).
"""
import math
import mpmath as mp

mp.mp.dps = 50


def logC(a, b):
    return mp.loggamma(a + 1) - mp.loggamma(b + 1) - mp.loggamma(a - b + 1)


def logw(p, k):
    return mp.log(mp.mpf(1) / 2) - logC(2 * p - 1, k)


def log_R_all(n, p, s0, mcap=None, uncapped=False):
    """Return (dict m -> log R_m for 0 <= m <= min(K, mcap), K).
    Terms with k > kmax = min(K, mcap+60) are bounded above by 2*t_{kmax} (each later factor is <= 1/2 for k >= 1),
    so the returned values are exact for kmax = K and otherwise upper bounds that differ by < 2^-60 relatively."""
    K = p if uncapped else min(p, n // 2)
    if mcap is None:
        mcap = K
    kmax = min(K, mcap + 60)
    lw0 = logw(p, s0)
    lt = [logC(p, k) + logw(p, k) - lw0 for k in range(kmax + 1)]
    acc = mp.mpf('-inf') if kmax == K else mp.log(2) + lt[kmax]
    out = {}
    for m in range(kmax, -1, -1):
        out[m] = acc
        acc = lt[m] if acc == mp.mpf('-inf') else acc + mp.log(1 + mp.e ** (lt[m] - acc))
    return out, K


def thresholds(n, p, s0):
    logn = mp.log(n)
    m_old = int(mp.ceil((s0 * mp.log(2 * p) + (s0 + 1) * logn / 2 + logn / 2) / mp.log(2)))
    lR, K = log_R_all(n, p, s0, mcap=m_old + 1)
    target = -(s0 + 2) * logn / 2
    m_sharp = next((m for m in range(s0, min(K, m_old + 1) + 1) if lR[m] <= target), K)
    m_cf = min(K, int(mp.ceil(s0 + (logC(p, s0) + (s0 + 2) * logn / 2) / mp.log(2))))
    lRu, _ = log_R_all(n, p, s0, mcap=m_old + 1, uncapped=True)
    m_unc = next((m for m in range(s0, m_old + 2) if lRu[m] <= target), None)
    thresholds.m_unc = m_unc
    return m_old, m_sharp, m_cf, K, lR


def compare(n, p, s0, ms):
    """log10 of R_m exact, new closed form, old bound 4(2p)^s0 2^-m; and the full T02(i) prefactors."""
    lR, K = log_R_all(n, p, s0, mcap=max(ms))
    rows = []
    for m in ms:
        if m >= K:
            rows.append((m, None, None, None, None))
            continue
        ex = lR[m]
        cf = logC(p, s0) - (m - s0) * mp.log(2) - (m * (m - 1) - (s0 - 1) * (s0 - 2)) / (4 * (p - 1))
        lo = logC(p, s0) - (m + 1 - s0) * mp.log(2) - mp.mpf(m * (m - 1) - (s0 - 1) * (s0 - 2)) / (4 * (p - m))
        old = mp.log(4) + s0 * mp.log(2 * p) - m * mp.log(2)
        rows.append((m, ex, cf, lo, old))
    return rows


def l10(x):
    return float(x / mp.log(10))


if __name__ == "__main__":
    s0 = 14
    print("=== Thresholds (omega = 1/2 log n), s0 = 14 ===")
    print(f"{'n':>9} {'p':>9} {'K':>7} {'m_old':>6} {'m_sharp':>8} {'m_cf':>6} {'saved':>6} "
          f"{'old SE size':>11} {'new size':>9} {'m#_uncapped':>11} {'log2(s0!)':>9}")
    cases = [(200, 500), (200, 1000)]
    A500 = math.log(500) / math.log(200)
    A1000 = math.log(1000) / math.log(200)
    for n in [10**3, 10**4, 10**5, 10**6, 10**8]:
        cases.append((n, 500))
        cases.append((n, 1000))
        cases.append((n, int(round(n ** A500))))
        cases.append((n, int(round(n ** A1000))))
    for n, p in cases:
        if p > 5 * 10**6 and n > 10**6:
            pass
        m_old, m_sh, m_cf, K, _ = thresholds(n, p, s0)
        print(f"{n:>9} {p:>9} {K:>7} {m_old:>6} {m_sh:>8} {m_cf:>6} {m_old - m_sh:>6} "
              f"{m_old + s0:>11} {min(m_sh, K) + s0:>9} {str(thresholds.m_unc):>11} {math.log2(math.factorial(s0)):>9.2f}")

    print("\n=== log10 R_m: exact | new closed-form upper | lower bound | old upper 4(2p)^s0 2^-m ===")
    for n, p in [(200, 500), (200, 1000)]:
        print(f"-- n={n}, p={p}")
        for m, ex, cf, lo, old in compare(n, p, s0, [14, 20, 40, 60, 80, 99, 100]):
            if ex is None:
                print(f"  m={m:>3}: R_m = 0 (m >= K)")
            else:
                print(f"  m={m:>3}: {l10(ex):9.3f} | {l10(cf):9.3f} | {l10(lo):9.3f} | {l10(old):9.3f}"
                      f"   (old/exact = 10^{l10(old - ex):.2f})")

    print("\n=== Is the size-tail bound informative at n = 200?  min_{m<K} log10[R_m (n+1)^{s0/2} sqrt(n)] ===")
    for n, p in [(200, 500), (200, 1000)]:
        lR, K = log_R_all(n, p, s0)
        best = min(lR[m] + s0 / 2 * mp.log(n + 1) + mp.log(n) / 2 for m in range(s0, K))
        print(f"  n={n}, p={p}: min over m<K = 10^{l10(best):.2f}  (>1 means vacuous; the cap K={K} binds)")

    print("\n=== smallest n (p = n^A) at which the new / old size cutoff falls below K ===")
    for A, lab in [(A500, "A=log500/log200"), (A1000, "A=log1000/log200")]:
        for which in ("sharp", "old"):
            lo_n, hi_n = 200, 10**7
            def ok(n):
                p = max(s0 + 1, int(round(n ** A)))
                m_old, m_sh, m_cf, K, _ = thresholds(n, p, s0)
                return (m_sh < K) if which == "sharp" else (m_old < K)
            while hi_n - lo_n > 1:
                mid = (lo_n + hi_n) // 2
                if ok(mid):
                    hi_n = mid
                else:
                    lo_n = mid
            print(f"  {lab:>18} {which:>5}: n = {hi_n}")
