"""W6-FIXREV2: independent recomputation of the T03 proof thresholds (A-REV2 §3.5 item; W2-VT03R R1). No randomness.

R_m = sum_{k=m+1}^{K} q_k / w(s0),  q_k/w(s0) = C(p,s0) prod_{i=s0}^{k-1} rho_i,  rho_i = (p-i)/(2p-1-i)   (W1-T03R E1(a)).
Computed as cumulative sums of log rho_i (no differences of large log-gamma values). Terms are summed exactly up to
kmax = min(K, m + 4000); the remainder is bracketed by [0, t_kmax] because rho_i <= 1/2 for i >= 1.
m#_n = min{m >= s0 : R_m <= n^{-(s0+2)/2}}   (omega = log(n)/2).

Conditions of the locked [P3] proof as modified by W1-T03R (C5), with C_A = 8 + 3A and the most favourable 1/g0 = 0:
  T1  delta_n <= 1/2,  delta_n = 3 sqrt(log n/N) + C_A (m + s0) log n / N
  T4  q_n <= 1/2,      q_n^2 = e C_A log n / (4(n+1)) * e^{2 eps_n}
  T5  e^{2 eps_n} <= 4, eps_n = (upsilon_n - 1) C_A log n / 2, upsilon_n = (1 + (0.02n+1)/(n^2-1))/(1 - delta_n)
"""
import math
import numpy as np

S0 = 14


def log_t(p, s0, kmax):
    """log(q_k/w(s0)) for k = s0..kmax."""
    lC = sum(math.log(p - i) - math.log(i + 1) for i in range(s0))
    i = np.arange(s0, kmax, dtype=float)
    lr = np.log(p - i) - np.log(2 * p - 1 - i)
    return np.concatenate([[lC], lC + np.cumsum(lr)])          # index j <-> k = s0 + j


def m_sharp(n, p, s0=S0):
    K = min(p, n // 2)
    target = -(s0 + 2) / 2 * math.log(n)
    kmax = min(K, s0 + 6000)
    lt = log_t(p, s0, kmax)
    # suffix log-sum-exp: lS[j] = log sum_{k >= s0+j}^{kmax} t_k
    mx = lt.max(); e = np.exp(lt - mx); suf = np.cumsum(e[::-1])[::-1]
    with np.errstate(divide="ignore"):
        lS = np.log(suf) + mx
    for m in range(s0, K):
        j = m + 1 - s0
        if j > len(lt) - 1:
            return m, 'tail-bound'
        lo = lS[j]
        hi = np.logaddexp(lS[j], lt[-1]) if kmax < K else lS[j]
        if hi <= target:
            return m, 'exact'
        if lo <= target < hi:
            return m, 'AMBIGUOUS'
    return K, 'cap'


def m_old(n, p, s0=S0):
    return math.ceil((s0 * math.log(2 * p) + (s0 + 2) / 2 * math.log(n)) / math.log(2))


def conds(n, A, which='sharp'):
    p = int(round(n ** A)); N = n - 1; L = math.log(n); CA = 8 + 3 * A
    m = m_sharp(n, p)[0] if which == 'sharp' else m_old(n, p)
    d = 3 * math.sqrt(L / N) + CA * (m + S0) * L / N
    if d >= 1:
        return dict(T1=False, T4=False, T5=False)
    ups = (1 + (0.02 * n + 1) / (n * n - 1)) / (1 - d)
    eps = (ups - 1) * CA * L / 2
    lq2 = math.log(math.e * CA * L / (4 * (n + 1))) + 2 * eps
    return dict(T1=d <= 0.5, T4=lq2 <= math.log(0.25), T5=2 * eps <= math.log(4))


def first_n(A, key, which='sharp'):
    lo, hi = 200, 200
    while not conds(hi, A, which)[key]:
        lo, hi = hi, int(hi * 1.5)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if conds(mid, A, which)[key] else (mid, hi)
    mono = all(conds(int(hi * f), A, which)[key] for f in (1.01, 1.1, 1.5, 2, 4))
    return hi, mono


def main():
    print('study points: (n,p) -> m#, flag, locked m_n')
    for p in (500, 1000):
        ms, fl = m_sharp(200, p)
        print(f'  (200,{p}): m# = {ms} ({fl}), K = 100, m_old = {m_old(200, p)}')
    for A, lab in ((math.log(500) / math.log(200), 'p=n^1.17'), (math.log(1000) / math.log(200), 'p=n^1.30')):
        for which in ('sharp', 'old'):
            row = []
            for key in ('T1', 'T4', 'T5'):
                n1, mono = first_n(A, key, which)
                row.append(f'{key}:{n1:,}{"" if mono else "(non-monotone!)"}')
            print(f'{lab:9} m={which:5} first n: ' + '  '.join(row))
    # point values of q_n at the n W1 called 'binding' and at V03's points (A-REV2 §3.5)
    for A, pts in ((math.log(500) / math.log(200), (115150, 130328, 2116048, 25571897)),
                   (math.log(1000) / math.log(200), (130328, 2457025, 29755302))):
        for n in pts:
            p = int(round(n ** A)); m = m_sharp(n, p)[0]; N = n - 1; L = math.log(n); CA = 8 + 3 * A
            d = 3 * math.sqrt(L / N) + CA * (m + S0) * L / N
            ups = (1 + (0.02 * n + 1) / (n * n - 1)) / (1 - d); eps = (ups - 1) * CA * L / 2
            q = math.sqrt(math.e * CA * L / (4 * (n + 1))) * math.exp(eps)
            print(f'  A={A:.4f} n={n:,} m#={m} delta={d:.4f} q_n={q:.4g} e^(2eps)={math.exp(2 * eps):.4g}')


if __name__ == '__main__':
    main()
