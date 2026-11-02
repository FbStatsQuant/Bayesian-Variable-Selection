#!/usr/bin/env python3
"""W2-VT03R task 2: independent reproduction of W1-T03R Prop. D (duplicated-columns counterexample).

Design: p identical raw columns x (non-constant), beta* = (beta1, 0, ..., 0), y^r = alpha + X^r beta* + eps.
Claim (W1 PROOF.md section 3): with E_n = {m(empty) <= m({1})}, P0(E_n) -> 1, and on E_n, for 0 <= m <= K-1,
    Pi(|S| > m | y) >= 2^{-(m+4)} exp{-m(m-1)/(4(p-m))}.

Part A (brute force, small n): log m(S) computed from the 00_COMMON formulas with generic linear algebra
        (G_S, H_S, D_S = det H / det(G+I), Q_S = y'y - n z' H^{-1} z) for EVERY S in Omega; check (i) it depends on |S|
        only, (ii) it equals W1's closed form m_k, (iii) the tail bound on E_n.  Also adversarial y's (not model draws).
Part B (closed form, large n): replicate data sets, P(E_n), the bound for all m <= K-1, the cutoff needed for n^{-1/2}.
Part C: analytic constants used in the proof.
Seeds fixed.
"""
import itertools, math
import numpy as np
from math import lgamma, log, exp

B0 = A0 = 0.01

def standardise(Xr, yr):
    n = len(yr)
    C = np.eye(n) - np.ones((n, n)) / n
    Xc = C @ Xr
    sd = np.sqrt((Xc ** 2).sum(0) / (n - 1))
    X = Xc / sd
    yc = C @ yr
    sy = math.sqrt((yc ** 2).sum() / (n - 1))
    return X, yc / sy

def logm_generic(X, y, S, n):
    nu = A0 + n / 2
    const = A0 * log(2 * B0) + lgamma(nu) - (n / 2) * log(math.pi) - lgamma(A0)
    if len(S) == 0:
        return const - nu * log(2 * B0 + y @ y)
    XS = X[:, list(S)]
    G = XS.T @ XS
    k = len(S)
    H = (n + 1) * G + np.eye(k)
    D = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
    z = XS.T @ y
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    return const - 0.5 * D - nu * log(2 * B0 + Q)

def logm_closed(k, n, c):
    """W1 closed form: D_k = ((n+1)kN+1)/(kN+1), Q_k = N - n k c^2/((n+1)Nk+1)  (k>=1); k=0: D=1, Q=N."""
    N = n - 1
    nu = A0 + n / 2
    const = A0 * log(2 * B0) + lgamma(nu) - (n / 2) * log(math.pi) - lgamma(A0)
    if k == 0:
        return const - nu * log(2 * B0 + N)
    D = ((n + 1) * k * N + 1) / (k * N + 1)
    Q = N - n * k * c * c / ((n + 1) * N * k + 1)
    return const - 0.5 * log(D) - nu * log(2 * B0 + Q)

def logq(p, k):
    # q_k = C(p,k) w(k), w(k) = 1/2 / C(2p-1,k)
    lC = lambda a, b: lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)
    return lC(p, k) + log(0.5) - lC(2 * p - 1, k)

def tails_from_sizes(logw_k):
    """logw_k[k] = log(posterior weight of size class k) unnormalised -> Pi(|S|>m) for m = 0..K-1"""
    a = np.array(logw_k)
    a = a - a.max()
    w = np.exp(a)
    w /= w.sum()
    tail = np.cumsum(w[::-1])[::-1]  # tail[k] = P(|S| >= k)
    return tail[1:]                   # index m -> P(|S| > m), m = 0..K-1

def bound(m, p):
    return 2.0 ** (-(m + 4)) * math.exp(-m * (m - 1) / (4 * (p - m)))

def partA(rng, out):
    out.append("Part A: brute-force enumeration (generic linear algebra) vs closed form")
    worst_dev = 0.0
    nE = nbound_ok = ncases = 0
    min_ratio = np.inf
    for n, p in [(8, 4), (10, 5), (12, 6), (14, 7), (16, 8)]:
        K = min(p, n // 2)
        for rep in range(40):
            x = rng.normal(size=n)
            Xr = np.tile(x[:, None], (1, p))
            if rep < 30:   # model draws, various beta1 (incl. tiny/huge)
                beta1 = [1.0, 0.3, 3.0, 0.05, -2.0][rep % 5]
                yr = 0.7 + beta1 * x + rng.normal(size=n)
            else:          # adversarial y: arbitrary vectors (deterministic statement on E_n)
                yr = rng.normal(size=n) * (1 + rep) + (rep - 30) * x
            X, y = standardise(Xr, yr)
            N = n - 1
            c = float(X[:, 0] @ y)
            logms = {}
            for k in range(K + 1):
                vals = [logm_generic(X, y, S, n) for S in itertools.combinations(range(p), k)]
                worst_dev = max(worst_dev, max(vals) - min(vals), abs(vals[0] - logm_closed(k, n, c)))
                logms[k] = vals[0]
            logw = [logq(p, k) + logms[k] for k in range(K + 1)]
            tail = tails_from_sizes(logw)
            ncases += 1
            if logms[0] <= logms[1]:
                nE += 1
                ok = all(tail[m] >= bound(m, p) for m in range(K))
                nbound_ok += ok
                min_ratio = min(min_ratio, min(tail[m] / bound(m, p) for m in range(K)))
    out.append(f"   max |log m(S) - log m(S')| within a size class, and vs closed form: {worst_dev:.2e}")
    out.append(f"   cases: {ncases}; on E_n: {nE}; bound holds on E_n: {nbound_ok}/{nE}; min tail/bound on E_n = {min_ratio:.3f}")

def partB(rng, out):
    out.append("Part B: closed form at large n (beta1 = 1, sigma = 1, alpha = 0.7), 200 replicate data sets per row")
    out.append("      n       p     K   P(E_n)  bound_ok|E_n  min_m 2^m*tail (m<=16)  max_m 2^m*tail  cutoff m*(tail<=n^-1/2): min/med/max   0.5log2 n")
    for n, p, reps in [(50, 50, 200), (200, 200, 200), (200, 500, 200), (2000, 2000, 200), (20000, 20000, 100), (200000, 200000, 40)]:
        K = min(p, n // 2)
        lq = np.array([logq(p, k) for k in range(K + 1)])
        ks = np.arange(K + 1)
        N = n - 1
        nu = A0 + n / 2
        D = np.where(ks == 0, 1.0, ((n + 1) * ks * N + 1.0) / (ks * N + 1.0))
        nE = nok = 0
        lo, hi, cuts = np.inf, 0.0, []
        for r in range(reps):
            x = rng.normal(size=n)
            x = (x - x.mean()); x *= math.sqrt((n - 1) / (x @ x))
            e = rng.normal(size=n)
            yr = 0.7 + 1.0 * x + e
            yc = yr - yr.mean()
            y = yc / math.sqrt(yc @ yc / (n - 1))
            c = float(x @ y)
            Q = np.where(ks == 0, N, N - n * ks * c * c / ((n + 1) * N * ks + 1.0))
            lm = -0.5 * np.log(D) - nu * np.log(2 * B0 + Q)
            tail = tails_from_sizes(lq + lm)
            if lm[0] <= lm[1]:
                nE += 1
                ms = np.arange(K)
                b = 2.0 ** (-(ms + 4.0)) * np.exp(-ms * (ms - 1.0) / (4.0 * (p - ms)))
                nok += bool(np.all(tail >= b))
            sc = tail[:17] * 2.0 ** np.arange(17)
            lo, hi = min(lo, sc.min()), max(hi, sc.max())
            cuts.append(int(np.argmax(tail <= n ** -0.5)))
        cuts = np.array(cuts)
        out.append(f"   {n:>6} {p:>7} {K:>5}  {nE/reps:6.3f}  {nok}/{nE:<10}  {lo:22.3f}  {hi:14.3f}  {cuts.min():>3}/{int(np.median(cuts)):>3}/{cuts.max():>3}{'':27}{0.5*math.log2(n):.2f}")

def partC(out):
    out.append("Part C: analytic constants in W1's proof of Prop. D")
    r = math.sqrt(2 / 3) / (0.5 + math.exp(1.01))
    out.append(f"   sqrt(2/3)/(1/2+e^1.01) = {r:.5f}  (>= 1/4 needed: {'OK' if r >= 0.25 else 'FAIL'}; margin {r-0.25:.5f})")
    ok = all(n * n - 3.02 * n + 2 >= 0 for n in range(3, 10**5))
    ok2 = all(((n + 1) * (n - 1) + 1) * (n - 1 + 0.02) <= 2 * n * (n - 1) ** 2 for n in range(3, 10**5))
    out.append(f"   ((n+1)N+1)(N+2b0) <= 2nN^2 for 3<=n<1e5: {ok and ok2}  (equivalent to n^2-3.02n+2>=0)")
    ok3 = all((n + 1) / (n * (n - 1)) <= 2 / n for n in range(3, 10**5))
    out.append(f"   (n+1)/(nN) <= 2/n for 3<=n<1e5: {ok3};  e^(2nu/n)=e^(1+0.02/n) <= e^1.01 for n>=2: True")

def main():
    rng = np.random.default_rng(20261102)
    out = []
    partA(rng, out)
    partB(rng, out)
    partC(out)
    print("\n".join(out))

if __name__ == "__main__":
    main()
