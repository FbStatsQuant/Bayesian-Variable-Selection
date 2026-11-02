#!/usr/bin/env python3
"""W2-VT03R: re-examination of W1-T03R scripts/proof_n0.py ("deterministic steps of the T03 proof hold from n ~ 1.15e5").

W1 took delta_n <= 1/2 and n/5 >= (s0(A+1)+2) log n as binding and asserted 'other thresholds bind earlier'.
Here every explicit deterministic threshold of [P3] (as modified by W1 (C1)-(C10)) that does not involve phi0/M/sigma
is listed and evaluated, with the most favourable value (1 + 1/g0) -> 1 (g0 -> infinity), and with g0 = 1:
  (T1) delta_n <= 1/2                                   [P3] lem:ongood(b)
  (T2) N >= 4 log n and 3 sqrt(log n/N) <= 1            [P3] lem:Gprob(G1), lem:ongood(a)
  (T3) n/5 >= (s0(A+1)+2) log n                         [P3] Step 1
  (T4) q_n <= 1/2                                       [P3] prop:sup(b) / W1 (C5)(b)  (geometric series)
  (T5) e^{2 eps_n} <= 4                                 W1 (C5)(b) (q_n <= c_q r_n);  [P3] uses the analogous limit statement
with delta_n = 3 sqrt(log n/N) + C_A (m + s0) log n/N,  C_A = 8 + 3A,
     upsilon_n = (1 + (0.02n+1)/(n^2-1))/(1-delta_n),  eps_n = (upsilon_n - 1) C_A log n / 2,
     q_n^2 = e C_A log n/(4(n+1)) (1+1/g0) e^{2 eps_n},   m = m# (exact tail) or m_old.
p = round(n^A), s0 = 14. No randomness.
"""
import math
from math import lgamma, log

S0 = 14

def logq_over_ws0(p, s0, k):
    lC = lambda a, b: lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)
    return lC(p, k) - lC(2 * p - 1, k) + lC(2 * p - 1, s0)

def m_sharp(n, p, s0):
    K = min(p, n // 2)
    target = -(s0 + 2) / 2 * log(n)
    # R_m = sum_{k=m+1}^K t_k ; t_{k+1}/t_k <= 1/2 for k>=1, so R_m in [t_{m+1}, 2 t_{m+1}]; use exact-ish sum of 200 terms
    m = s0
    while m < K:
        terms = [logq_over_ws0(p, s0, k) for k in range(m + 1, min(K, m + 200) + 1)]
        mx = max(terms)
        lR = mx + log(sum(math.exp(t - mx) for t in terms))
        if lR <= target:
            return m
        m += 1
    return K

def m_old(n, p, s0):
    return math.ceil((s0 * log(2 * p) + (s0 + 2) / 2 * log(n)) / log(2))

def conds(n, A, which, g0inv):
    p = int(round(n ** A)); N = n - 1; L = log(n); CA = 8 + 3 * A
    m = m_sharp(n, p, S0) if which == "sharp" else m_old(n, p, S0)
    d = 3 * math.sqrt(L / N) + CA * (m + S0) * L / N
    if d >= 1:
        return dict(T1=False, T2=N >= 4 * L and 3 * math.sqrt(L / N) <= 1, T3=n / 5 >= (S0 * (A + 1) + 2) * L, T4=False, T5=False)
    ups = (1 + (0.02 * n + 1) / (n * n - 1)) / (1 - d)
    eps = (ups - 1) * CA * L / 2
    q2 = math.e * CA * L / (4 * (n + 1)) * (1 + g0inv) * math.exp(min(2 * eps, 700))
    return dict(T1=d <= 0.5, T2=N >= 4 * L and 3 * math.sqrt(L / N) <= 1, T3=n / 5 >= (S0 * (A + 1) + 2) * L,
                T4=q2 <= 0.25, T5=2 * eps <= log(4))

def first_n(A, which, key, g0inv):
    # coarse geometric scan then bisection (each condition is monotone in n over the scanned range; checked by the scan)
    grid = [int(200 * 1.05 ** i) for i in range(0, 600)]
    prev = None
    for i, n in enumerate(grid):
        c = conds(n, A, which, g0inv)
        ok = c[key] if key != "all" else all(c.values())
        if ok:
            lo, hi = (grid[i - 1] if i else 199), n
            while hi - lo > 1:
                mid = (lo + hi) // 2
                cm = conds(mid, A, which, g0inv)
                okm = cm[key] if key != "all" else all(cm.values())
                lo, hi = (lo, mid) if okm else (mid, hi)
            # monotonicity check on the next 40 grid points
            mono = all((conds(m2, A, which, g0inv)[key] if key != "all" else all(conds(m2, A, which, g0inv).values()))
                       for m2 in grid[i:i + 40])
            return hi, mono
    return None, None

def main():
    for A, lab in ((math.log(500) / math.log(200), "p=n^1.17"), (math.log(1000) / math.log(200), "p=n^1.30")):
        for which in ("sharp", "old"):
            row = []
            for key in ("T1", "T3", "T4", "T5", "all"):
                n1, mono = first_n(A, which, key, 0.0)
                row.append(f"{key}:{n1:,}{'' if mono else '(non-monotone!)'}")
            n2, _ = first_n(A, which, "all", 1.0)
            print(f"{lab:9} m={which:5}  first n (g0=inf): " + "  ".join(row) + f"   | all, g0=1: {n2:,}")

if __name__ == "__main__":
    main()
