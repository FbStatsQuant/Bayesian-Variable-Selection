"""W3-D3 numerics N1: size arithmetic of lemmas/B3w.md Step 0 and the threshold n1 of [R-3].
Checks, on a grid of (A, s0, p, n) with 2 <= p <= n^A, s0 <= K = min(p, n//2):
 (1) s0 + j0 <= floor(5(A+1)(s0+1) log n)   (j0 = ceil((2A+1)s0) + 1)
 (2) s0 + m#_n <= floor(5(A+1)(s0+1) log n), m#_n computed EXACTLY from its definition
     (W3-POST/STATEMENT.md:36-37: R_m = sum_{k>m}^K C(p,k) w(k)/w(s0) <= n^{-(s0+1)/2} e^{-omega}, omega = log(n)/2)
Also prints n1(s0, A, K=1) = least n >= max(3, 2 s0) with W(n)(1 + A log n) <= c2 n / K^4 for all larger n (c2 = 1e-5).
Run: python3 -I N1_window.py > N1_out.txt"""
import math

def lchoose(a, k):
    return math.lgamma(a + 1) - math.lgamma(k + 1) - math.lgamma(a - k + 1)

def msharp(n, p, s0):
    """m#_n(omega = log n / 2): least m >= s0 with R_m <= n^{-(s0+2)/2}. R_m = sum_{k=m+1}^{K} t_k,
    t_k = C(p,k) w(k)/w(s0); for k >= s0 the ratio t_{k+1}/t_k = (p-k)/(2p-1-k) <= 2/3, so the sum is truncated
    after 400 terms (relative error <= 3 (2/3)^400 < 1e-69)."""
    K = min(p, n // 2)
    logw = lambda k: -math.log(2) - lchoose(2 * p - 1, k)
    lt = lambda k: lchoose(p, k) + logw(k) - logw(s0)
    thr = -((s0 + 2) / 2) * math.log(n)
    m = s0
    while m < K:
        ks = [lt(k) for k in range(m + 1, min(K, m + 400) + 1)]
        mx = max(ks)
        logR = mx + math.log(sum(math.exp(t - mx) for t in ks))
        if logR <= thr:
            return m
        m += 1
    return K

viol = 0; cases = 0; worst = 0.0
for A in [1, 1.5, 2, 3, 5, 10]:
    for s0 in [1, 2, 3, 5, 8, 12]:
        for n in [3, 5, 10, 30, 100, 300, 1000, 10**4, 10**5, 10**6]:
            W = 5 * (A + 1) * (s0 + 1) * math.log(n)
            q = math.floor(W)
            j0 = math.ceil((2 * A + 1) * s0) + 1
            pmax = min(int(n ** A), 10**7)
            for p in sorted({2, 3, 5, 10, 50, 200, 1000, 10**4, pmax}):
                if p > pmax or p < 2: continue
                K = min(p, n // 2)
                if s0 > K: continue
                cases += 1
                ok1 = (s0 + j0 <= q)
                ms = msharp(n, p, s0)
                ok2 = (min(p, s0 + ms) <= min(p, q)) and (s0 + ms <= q)
                worst = max(worst, (s0 + ms) / W)
                if not (ok1 and ok2):
                    viol += 1
                    print("VIOLATION", A, s0, n, p, s0 + j0, s0 + ms, q)
print(f"N1 grid: {cases} cases, {viol} violations; max (s0 + m#_n)/W = {worst:.3f}")

c2 = 1e-5
for A in [1, 2, 5]:
    for s0 in [1, 3, 8]:
        f = lambda n: 5 * (A + 1) * (s0 + 1) * math.log(n) * (1 + A * math.log(n)) - c2 * n
        # f(n)/n decreasing for large n; find last sign change by bisection on a log grid
        lo, hi = max(3, 2 * s0), 10.0
        while f(hi) > 0: hi *= 2
        last_bad = lo
        x = lo
        while x < hi:
            if f(x) > 0: last_bad = x
            x *= 1.01
        print(f"n1 (K=1): A={A}, s0={s0}: about {int(last_bad * 1.01) + 1:.3e}")
