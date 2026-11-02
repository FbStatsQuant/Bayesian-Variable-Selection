"""W6-FIXREV2: independent checks for the EXP′ / Lemma U items of A-REV2 (seed 20261102).

(1) Limit of kappa_n: (1+phi^-2)/(2 phi^2 (n-1)) + nu (1.02 + 1/(n phi^2))/(c n) -> 1.02/(2c) = 0.51/c, from above.
(2) A-REV2 §6.3 counterexample to the matching lower bound of C3 (exact sufficient statistics, n = 10^6).
(3) Repaired lower bounds: (C3-low) under mu in span X_T; (C3-low') general delta = 0 with coefficient sigma^2/(2 C_R).
    Checked deterministically on random small designs, on the realised events.
(4) Quantifier counterexample (A-REV2 §6.2): p = n-1 orthogonal columns; max over singletons of ||P_V eps||^2/sigma^2
    exceeds 0.5 log n with probability -> 1 (exact: independent chi^2_1).
(5) Exact remainder identity (Lemma 1.3) and the deterministic bound with the realised min RSS^y, all (T,l) with
    |T+l| <= 3 on p = 8 random designs (general-set form = Lemma U).
"""
import itertools, json, sys
from math import log
import numpy as np
from core import BVS, frame

OUT = {}


def kappa(n, phi2, c):
    nu = 0.01 + n / 2
    return (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + nu * (1.02 + 1 / (n * phi2)) / (c * n)


def check_kappa():
    sig2 = M = phi2 = 1.0
    c = sig2 / (8 * (M + 2 * sig2))
    rows = [(n, kappa(n, phi2, c)) for n in (10 ** 3, 10 ** 4, 10 ** 6, 10 ** 9)]
    # first n with kappa_n <= 0.52/c for this (phi2, c)
    lo, hi = 2, 10 ** 9
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if kappa(mid, phi2, c) <= 0.52 / c else (mid, hi)
    res = dict(c=c, limit_051_over_c=0.51 / c, wrong_052_over_c=0.52 / c, kappa_n=rows,
               decreasing=all(rows[i][1] > rows[i + 1][1] for i in range(len(rows) - 1)),
               first_n_kappa_le_052_over_c=hi, multiplier_of_M_plus_2sig2_over_sig2=0.51 * 8)
    OUT['kappa_limit'] = res
    return res


def c3_counterexample():
    n = 10 ** 6; N = n - 1; sig2 = 1.0; M = 1.0; phi2 = 1.0; L = 5.0
    Z2 = 65.0
    # contrast scale: Y = x1 + eps, eps ⟂ x1, u2'eps = sqrt(65), ||eps||^2 = N  => ||Y||^2 = 2N, s_y^2 = 2
    sy = np.sqrt(2.0)
    G = N * np.eye(2); z = np.array([N / sy, np.sqrt(Z2 * N) / sy]); yy = N
    m = BVS(G, z, yy, n)
    actual = m.logBF((1,)) + 0.5 * log(n + 1)
    cE = sig2 / (8 * (M + 2 * sig2))
    kap = kappa(n, phi2, cE)
    th = n ** (-1 / 3) + L * log(n) / (n - 1)
    thp = L * log(n) * (th + 3 / n) / (1 - th)
    claimed = Z2 / 2 - kap - thp
    # events E1-E4 (sigma = 1): projected noise energies on span X_V and span X_{V ∪ S0}
    E1 = dict(V2=Z2, V1=0.0, V12=Z2, bound=L * log(n))
    E2 = dict(min_RSS=N - Z2, floor=N * (1 - th))         # RSS_V >= ||(I-P_{V∪S0}) eps||^2 = N - 65 for every V
    E3 = dict(norm_eps2=N, bound=N * (1 + n ** (-1 / 3)))
    E4 = dict(normY2=2 * N, bound=(2 * M + 4 * sig2) * n)
    ok = (max(E1['V2'], E1['V12']) <= E1['bound'] and E2['min_RSS'] >= E2['floor'] and E3['norm_eps2'] <= E3['bound']
          and E4['normY2'] <= E4['bound'])
    # asymptotics: violation threshold on Z^2 for the limit statistic Z^2/4 vs Z^2/2 - kappa - theta'
    zthr = 4 * (0.51 / cE)
    res = dict(kappa_n=kap, theta_prime_n=thp, actual=actual, claimed_lower=claimed, violated=actual < claimed,
               events_E1_E4_hold=ok, E=dict(E1=E1, E2=E2, E3=E3, E4=E4),
               limit_violation_threshold_Z2=zthr)
    OUT['c3_counterexample'] = res
    return res


def c3_repaired(ndesign=200, seed=20261102):
    """Deterministic chain checks on realised data (sigma = 1 known):
       (C3-low)  mu in span X_T, l null-ish with delta = 0:  log odds_l + .5 log(n+1) >= nu Z^2/||C eps||^2 - |R|
       (C3-low') delta = 0 only:                            log odds_l + .5 log(n+1) >= nu Z^2/||Y||^2 - |R|
       and the sharper fact used:  -nu log(1-x) >= nu x  with x = Z^2/RSS_T.
       Here we check the exact inequality  -nu log(1-x) >= nu Z^2 / RSS_T  and  RSS_T <= ||C eps||^2 (if mu in span X_T)
       resp. RSS_T <= ||Y||^2 (always), i.e. the two links the repaired proofs use."""
    rng = np.random.default_rng(seed)
    viol = dict(low=0, lowp=0, span_link=0, gen_link=0); cnt = dict(low=0, lowp=0)
    for _ in range(ndesign):
        n = int(rng.choice([30, 80, 200])); p = 6
        E = frame(n, p + 2, rng)
        # columns 0,1 carry signal; column 5 is orthogonal to everything (delta = 0 at any T not containing it)
        X = E[:, :p].copy(); X[:, 1] = 0.6 * E[:, 0] + 0.8 * E[:, 1]
        th = rng.uniform(0.3, 1.5, 2)
        mu = X[:, :2] @ th
        eps = rng.standard_normal(n); eps -= eps.mean()
        Y = mu + eps
        for T in [(), (0,), (1,), (0, 1), (0, 1, 2), (2,), (0, 2)]:
            l = 5
            XT = X[:, list(T)] if T else np.zeros((n, 0))
            PT = XT @ np.linalg.pinv(XT) if T else np.zeros((n, n))
            C = np.eye(n) - np.ones((n, n)) / n
            r = (C - PT) @ X[:, l]; u = r / np.linalg.norm(r)
            delta = float(u @ mu); Z = float(u @ eps)
            assert abs(delta) < 1e-8
            RSS_T = float(Y @ (C - PT) @ Y); nu = 0.01 + n / 2
            x = Z * Z / RSS_T
            assert -nu * log(1 - x) >= nu * x - 1e-12
            inspan = set((0, 1)) <= set(T)
            if inspan:
                cnt['low'] += 1
                viol['span_link'] += int(RSS_T > float(eps @ C @ eps) + 1e-9)
            cnt['lowp'] += 1
            viol['gen_link'] += int(RSS_T > float(Y @ C @ Y) + 1e-9)
    res = dict(counts=cnt, violations=viol)
    OUT['c3_repaired_links'] = res
    return res


def quantifier_cex(seed=20261102):
    rng = np.random.default_rng(seed)
    res = {}
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        reps = 200 if n <= 10 ** 5 else 40
        mx = np.array([np.max(rng.standard_normal(n - 1) ** 2) for _ in range(reps)])
        res[str(n)] = dict(freq_max_gt_half_logn=float(np.mean(mx > 0.5 * log(n))), median_max=float(np.median(mx)),
                           two_log_n=2 * log(n))
    OUT['quantifier_cex'] = res
    return res


def remainder_identity(ndesign=40, seed=20261102):
    rng = np.random.default_rng(seed)
    maxerr = 0.0; maxR = 0.0; nviol = 0; npairs = 0
    for _ in range(ndesign):
        n, p = int(rng.choice([40, 100, 400])), 8
        idx = np.arange(p)
        Sig = 0.5 ** np.abs(idx[:, None] - idx[None, :])
        Xr = rng.standard_normal((n, p)) @ np.linalg.cholesky(Sig).T
        th = np.zeros(p); th[[0, 3]] = rng.uniform(0.3, 1.0, 2)
        yr = Xr @ th + rng.standard_normal(n)
        m = BVS.from_data(Xr, yr)
        Xs = Xr - Xr.mean(0); Xs /= np.sqrt((Xs ** 2).sum(0) / (n - 1))
        ys = yr - yr.mean(); ys /= np.sqrt((ys ** 2).sum() / (n - 1))
        sets = [S for k in range(0, 4) for S in itertools.combinations(range(p), k)]
        rss = {}
        for S in sets:
            if S:
                P = Xs[:, list(S)] @ np.linalg.pinv(Xs[:, list(S)])
                rss[S] = float(ys @ ys - ys @ P @ ys)
            else:
                rss[S] = float(ys @ ys)
        phi2 = min(np.linalg.eigvalsh(np.corrcoef(Xs[:, list(S)].T) if len(S) > 1 else np.eye(1))[0] for S in sets if S)
        nu = 0.01 + n / 2
        for S in sets:
            if len(S) == 3:
                continue
            for l in range(p):
                if l in S:
                    continue
                T2 = tuple(sorted(S + (l,)))
                lhs = m.logBF(T2) - m.logBF(S)
                x = 1 - rss[T2] / rss[S]
                R = lhs + 0.5 * log(n + 1) + nu * log(1 - x)
                # exact Lemma 1.3 decomposition
                Gd = lambda A: m.logD(A)
                aU = lambda A: 0.02 + m.Q(A) - rss[A]
                Rexact = -0.5 * (Gd(T2) - Gd(S) - log(n + 1)) - nu * (log(1 + aU(T2) / rss[T2]) - log(1 + aU(S) / rss[S]))
                maxerr = max(maxerr, abs(R - Rexact))
                bound = (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + nu * (1.02 + 1 / (n * phi2)) / min(rss[S], rss[T2])
                nviol += int(abs(R) > bound + 1e-9); maxR = max(maxR, abs(R)); npairs += 1
    res = dict(pairs=npairs, max_decomposition_error=maxerr, max_abs_R=maxR, bound_violations=nviol)
    OUT['remainder_identity'] = res
    return res


if __name__ == '__main__':
    for f in (check_kappa, c3_counterexample, c3_repaired, quantifier_cex, remainder_identity):
        r = f(); print(f.__name__, json.dumps(r, default=str))
    with open(sys.argv[1] if len(sys.argv) > 1 else 'lemmaU_checks.json', 'w') as fh:
        json.dump(OUT, fh, indent=1, default=str)
