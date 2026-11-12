"""W3-PSHARP numerics (a), orthogonal witness (W-orth with all columns orthogonal): EXACT delta_n at large p.

Design: X'X = (n-1) I_p (p <= n-1), theta*_j = theta on S0 = {0..s0-1}, sigma* = 1.
Exact-in-law reduction (stated, and validated in V1 against an explicit matrix design + brute-force enumeration):
with u_k = x_k/sqrt(n-1) orthonormal in 1-perp, a_k := u_k'Cy^r = sqrt(n-1) theta*_k + g_k, g_k iid N(0,1);
||Cy^r||^2 = sum_k a_k^2 + chi^2_{n-1-p};  s_y^2 = ||Cy^r||^2/(n-1);  z_k = x_k'y = sqrt(n-1) a_k / s_y;
Q_S = (n-1) - sum_{k in S} z_k^2/n,  D_S = n^{|S|}.
Exact posterior odds:  delta/(1-delta) = sum_{S != S0} pi(S)/pi(S0), with
  pi(S)/pi(S0) = [w(|S|)/w(s0)] n^{-(|S|-s0)/2} (1 - (A_S - A_S0)/c*)^{-nu},  A_S = sum_{k in S} z_k^2/n,
  c* = 2 b0 + Q_S0.  Using (1-x)^{-nu} = E exp(x c* t), t ~ Gamma(nu, rate c*):
  1 + delta/(1-delta) = E_t [ sum_k (w(k)/w(s0)) n^{-(k-s0)/2} e_k(exp(t a_1), ..., exp(t a_p)) exp(-t A_S0) ],
e_k = elementary symmetric polynomial (DP over columns, log domain), t-integral by Gauss-Legendre.
Sizes k > kmax = s0 + 60 are omitted in the large runs, so the reported odds are a lower bound for delta/(1-delta)
(every omitted term is >= 0); V2 compares with all sizes up to K on cases where that is affordable.
Run: py -3.13 -I a_orth.py > a_orth_out.txt
"""
import sys, os, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script directory
import numpy as np
from numpy.polynomial.legendre import leggauss
sys.dont_write_bytecode = True
from core import B0, lchoose, logw, enumerate_posterior, odds_against, Lambda, c_const, logsumexp


def suff_stats(n, p, s0, theta, rng):
    g = rng.standard_normal(p)
    a = g.copy()
    a[:s0] += math.sqrt(n - 1) * theta
    rest = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
    tot = float((a ** 2).sum() + rest)
    sy2 = tot / (n - 1)
    z = math.sqrt(n - 1) * a / math.sqrt(sy2)
    return z, g, sy2


def exact_odds(n, p, s0, z, kextra=60, npts=None):
    """Returns (odds_le_kmax, one_step_odds). odds_le_kmax = sum over S != S0 with |S| <= kmax = min(K, s0+kextra)
    of pi(S)/pi(S0): exact up to quadrature error, and a LOWER bound for delta/(1-delta) (all omitted terms >= 0).
    kextra=None -> all sizes up to K (exact odds). Quadrature in u = log t: every model's integrand is the same
    log-Gamma shape (width 1/sqrt(nu)) shifted by -log(rate), rate in [c0 - A_top, c0]."""
    nu = 0.01 + n / 2
    K = min(p, n // 2)
    A = z ** 2 / n
    AS0 = float(A[:s0].sum())
    c0 = 2 * B0 + (n - 1)
    cst = c0 - AS0
    kmax = K if kextra is None else min(K, s0 + kextra)
    cmin = max(c0 - float(np.sort(A)[::-1][:kmax].sum()), 2 * B0)       # smallest rate among models of size <= kmax
    w = 1 / math.sqrt(nu)
    lo, hi = math.log(nu / c0) - 16 * w, math.log(nu / cmin) + 12 * w
    nodes = npts or int(max(400, math.ceil((hi - lo) / w * 10)))
    xg, wg = leggauss(nodes)
    u = 0.5 * (hi - lo) * xg + 0.5 * (hi + lo)
    t = np.exp(u)
    lw = np.log(0.5 * (hi - lo) * wg)
    lgam = nu * math.log(cst) - math.lgamma(nu) + nu * u - cst * t              # log Gamma(nu, rate cst) density in u
    L = np.full((nodes, kmax + 1), -np.inf)
    L[:, 0] = 0.0
    lhalf = -0.5 * math.log(n)
    for j in range(p):                                                          # prod_j (1 + n^{-1/2} e^{t A_j} x)
        L[:, 1:] = np.logaddexp(L[:, 1:], L[:, :-1] + (lhalf + t * A[j])[:, None])
    ks = np.arange(kmax + 1)
    lwk = np.array([logw(p, k) for k in ks]) - logw(p, s0) + 0.5 * s0 * math.log(n)
    F = L + lwk[None, :] - (AS0 * t)[:, None]
    total = math.exp(logsumexp((F + (lgam + lw)[:, None]).ravel()))             # = 1 + odds_le_kmax
    prior1 = (s0 + 1) / (2 * p - 1 - s0)
    one = prior1 * n ** -0.5 * float(np.exp(-nu * np.log1p(-A[s0:] / cst)).sum()) if s0 + 1 <= K else 0.0
    return total - 1.0, one


def V1(rng):
    print("V1: validation of the reduction + DP against an explicit design and brute-force enumeration")
    worst = 0.0
    for (n, p, s0, theta) in [(30, 12, 2, 1.0), (24, 11, 1, 0.8), (40, 13, 3, 0.7), (20, 12, 0, 0.0)]:
        for rep in range(3):
            # explicit orthogonal standardised design
            M = rng.standard_normal((n, n))
            M = M - M.mean(0)
            Qm, _ = np.linalg.qr(M[:, :p] - M[:, :p].mean(0))
            Qm = Qm - Qm.mean(0)
            Qm, _ = np.linalg.qr(Qm)
            X = math.sqrt(n - 1) * Qm
            assert np.abs(X.T @ X - (n - 1) * np.eye(p)).max() < 1e-8 and np.abs(X.sum(0)).max() < 1e-8
            th = np.zeros(p); th[:s0] = theta
            yr = 0.3 + X @ th + rng.standard_normal(n)
            yc = yr - yr.mean()
            y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
            post = enumerate_posterior(X, y)
            brute = odds_against(post, range(s0))
            z = X.T @ y
            dp, one = exact_odds(n, p, s0, z, kextra=None)
            # brute one-step sum
            l0 = post[frozenset(range(s0))]
            one_b = sum(math.exp(post[frozenset(list(range(s0)) + [j])] - l0) for j in range(s0, p)) if s0 + 1 <= min(p, n // 2) else 0.0
            rel = abs(dp - brute) / brute
            rel1 = abs(one - one_b) / max(one_b, 1e-300)
            worst = max(worst, rel, rel1)
            print(f"  n={n} p={p} s0={s0} rep={rep}: brute odds={brute:.10e} DP={dp:.10e} rel={rel:.1e}; one-step rel={rel1:.1e}")
    print(f"  worst relative difference: {worst:.2e}  (PASS if < 1e-7): {'PASS' if worst < 1e-7 else 'FAIL'}")


def V2(rng):
    print("V2: sizes above kmax = s0 + 60 and quadrature: (i) all sizes up to K (kextra=None) vs kextra=60;"
          " (ii) kextra 60 vs 120 and nodes x2 on a large case")
    for (n, p, s0) in [(400, 399, 3), (1600, 1599, 1), (1600, 200, 3)]:
        z, g, sy2 = suff_stats(n, p, s0, 1.0, rng)
        a = exact_odds(n, p, s0, z)[0]
        b = exact_odds(n, p, s0, z, kextra=None)[0]
        print(f"  n={n} p={p} s0={s0}: kextra=60: {a:.12e}; all sizes <= K: {b:.12e}; rel diff {abs(a-b)/b:.1e}", flush=True)
    n, p, s0 = 25600, 25599, 3
    z, g, sy2 = suff_stats(n, p, s0, 1.0, rng)
    a = exact_odds(n, p, s0, z)[0]
    b = exact_odds(n, p, s0, z, kextra=120, npts=1200)[0]
    print(f"  n={n} p={p} s0={s0}: kextra=60: {a:.12e}; kextra=120, 1200 nodes: {b:.12e}; rel diff {abs(a-b)/b:.1e}")


def E1(rng):
    print("E1: orthogonal witness. Columns: n p s0 | Lambda_n | medians of [odds/Lambda, one-step/Lambda, delta*sqrt(n)]"
          " | quartiles of odds/Lambda | P(odds >= 0.9 Lambda), P(odds >= 0.75 Lambda).  odds = sum over |S| <= s0+60 (lower bound for delta/(1-delta); see V2)")
    cfgs = []
    for n in (100, 400, 1600, 6400, 25600):
        for a in (0.5, 0.75, 1.0):
            p = n - 1 if a == 1.0 else int(round(n ** a))
            for s0 in (1, 3):
                cfgs.append((n, p, s0))
    for (n, p, s0) in cfgs:
        reps = 200 if p <= 2000 else (100 if p <= 7000 else 40)
        lam = Lambda(n, p, s0, p - s0)
        r, r1, ds = [], [], []
        for _ in range(reps):
            z, g, sy2 = suff_stats(n, p, s0, 1.0, rng)
            odds, one = exact_odds(n, p, s0, z)
            r.append(odds / lam); r1.append(one / lam); ds.append(odds / (1 + odds) * math.sqrt(n))
        r, r1 = np.array(r), np.array(r1)
        q = np.quantile(r, [0.25, 0.5, 0.75])
        print(f"  n={n:6d} p={p:6d} s0={s0} reps={reps:3d} | Lam={lam:.4f} | {q[1]:.3f} {np.median(r1):.3f} {np.median(ds):.3f}"
              f" | {q[0]:.3f} {q[2]:.3f} | {np.mean(r >= 0.9):.2f} {np.mean(r >= 0.75):.2f}", flush=True)


def E2(rng):
    print("E2: growing s0 on the orthogonal witness (Corollary A2): s0 = round(n^0.3), p = n-1, theta = 1")
    for n in (400, 1600, 6400):
        p, s0 = n - 1, int(round(n ** 0.3))
        lam = Lambda(n, p, s0, p - s0)
        r, pis = [], []
        for _ in range(60):
            z, g, sy2 = suff_stats(n, p, s0, 1.0, rng)
            odds, one = exact_odds(n, p, s0, z, kextra=80)
            r.append(odds / lam); pis.append(1 / (1 + odds))
        print(f"  n={n} p={p} s0={s0} | Lam={lam:.4f} | median odds/Lam={np.median(r):.3f}, min={min(r):.3f} | median pi(S0)={np.median(pis):.3f}", flush=True)


def E3():
    print("E3: the truncated moments used in Lemma W (chi^2_1, tau = 2 log N): exact mean sqrt(2 tau/pi) = 2 sqrt(log N/pi);")
    print("    second moment (2/sqrt(2 pi)) int_0^sqrt(tau) e^{z^2/2} dz vs sharp asymptote N/sqrt(pi log N) and crude bound 2 N sqrt(log N/pi);")
    print("    tail P(e^{chi2/2} > w) vs 1/(w sqrt(pi log w))")
    from scipy import integrate, stats
    for N in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 8):
        tau = 2 * math.log(N)
        m1 = integrate.quad(lambda zz: math.exp(zz * zz / 2) * math.exp(-zz * zz / 2) / math.sqrt(2 * math.pi), -math.sqrt(tau), math.sqrt(tau))[0]
        m2 = 2 / math.sqrt(2 * math.pi) * integrate.quad(lambda zz: math.exp(zz * zz / 2), 0, math.sqrt(tau))[0]
        tail = 2 * stats.norm.sf(math.sqrt(2 * math.log(N)))
        print(f"  N={N:.0e}: mean={m1:.6f} (formula {2*math.sqrt(math.log(N)/math.pi):.6f}); second/N={m2/N:.5f}, asymptote {1/math.sqrt(math.pi*math.log(N)):.5f},"
              f" crude {2*math.sqrt(math.log(N)/math.pi):.4f}; tail*N={tail*N:.5f} vs {1/math.sqrt(math.pi*math.log(N)):.5f}")


if __name__ == "__main__":
    t0 = time.time()
    rng = np.random.default_rng(20261111)
    which = sys.argv[1:] or ["V1", "V2", "E3", "E1", "E2"]
    for w in which:
        {"V1": lambda: V1(rng), "V2": lambda: V2(rng), "E1": lambda: E1(rng), "E2": lambda: E2(rng), "E3": E3}[w]()
        print(f"  [{w} done, {time.time()-t0:.0f}s]", flush=True)
