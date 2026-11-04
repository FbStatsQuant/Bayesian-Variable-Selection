"""PC2: exact small-case checks of R1_C cards D2, D3, D5, D7, D11, D13, D15-KL (statement sanity).
All by exact enumeration of the actual target at p <= 10 on random correlated designs (fixed seeds), plus
synthetic finite exponential families for the grid clauses.  ~1 minute."""
import math
import numpy as np
from bvs_common import (suff_from_data, method_sizes, coded_partition, d_table, log_m, log_prior_w, all_models,
                        A0, B0)


def lse(x):
    m = np.max(x)
    return m + math.log(np.exp(x - m).sum())


def rand_design(rng, p, n, dup=False):
    S = np.eye(p)
    for i in range(p):
        for j in range(i + 1, p):
            S[i, j] = S[j, i] = rng.uniform(-0.3, 0.6) if abs(i - j) < 3 else rng.uniform(-0.1, 0.1)
    w = np.linalg.eigvalsh(S)
    if w.min() < 0.05:
        S += (0.05 - w.min()) * np.eye(p)
        d = np.sqrt(np.diag(S))
        S = S / np.outer(d, d)
    X = rng.standard_normal((n, p)) @ np.linalg.cholesky(S).T
    if dup:
        X[:, 1] = X[:, 0]
    th = np.zeros(p)
    th[rng.choice(p, 2, replace=False)] = rng.uniform(0.2, 1.0, 2)
    y = X @ th + rng.standard_normal(n)
    return suff_from_data(X, y)


fails = {}


def bad(key, msg):
    fails.setdefault(key, []).append(msg)


rng = np.random.default_rng(424242)
for it in range(40):
    p = int(rng.integers(3, 10))
    n = int(rng.choice([6, 9, 15, 40, 200]))
    G, z, Y, n = rand_design(rng, p, n, dup=(it % 5 == 0 and p >= 3))
    K, B = method_sizes(n, p)
    blocks = coded_partition(G, max(B, 1))
    models, d, lbf = d_table(G, z, Y, n, blocks, K)
    lp = np.array([log_prior_w(p, len(S)) for S in models])
    lgam = lp + lbf                      # log pi up to Z (relative to m(empty))
    lg0 = lgam - d
    lZ0 = lse(lg0)
    lpi0 = lg0 - lZ0
    lpi = lgam - lse(lgam)
    pi, pi0 = np.exp(lpi), np.exp(lpi0)
    # ---- D2: pi0(S) = A(|S|) prod_b q_b(S_b), A(k) = w(k) prod B_b / Zbar0
    bid = {j: b for b, C in enumerate(blocks) for j in C}
    lm0 = log_m(G, z, Y, n, [])
    Bb, lr = [], {}
    for C in blocks:
        tot = []
        for k in range(len(C) + 1):
            for U in __import__('itertools').combinations(sorted(C), k):
                v = log_m(G, z, Y, n, U) - lm0
                lr[U] = v
                tot.append(v)
        Bb.append(lse(np.array(tot)))
    for S, l0 in zip(models, lpi0):
        parts = {}
        for j in S:
            parts.setdefault(bid[j], []).append(j)
        lq = sum(lr[tuple(sorted(parts.get(b, [])))] - Bb[b] for b in range(len(blocks)))
        lA = log_prior_w(p, len(S)) + sum(Bb) - lZ0
        if abs(lA + lq - l0) > 1e-8:
            bad('D2', f"p={p} n={n} S={S}")
    # ---- D3: 1+chi2 >= pi(S0)^2/a, KL(pi||pi0) >= pi(S0) log(1/a) - log 2, for every S0
    onepchi = float((pi ** 2 / pi0).sum())
    kl = float((pi * (lpi - lpi0)).sum())
    for i in range(len(models)):
        if onepchi < pi[i] ** 2 / pi0[i] * (1 - 1e-12):
            bad('D3chi', f"p={p}")
        if kl < pi[i] * (-lpi0[i]) - math.log(2) - 1e-9:
            bad('D3KL', f"p={p}")
    # ---- D5: U >= Z with U_m = sup m (N17 envelope); TV(pi, pi|T) = 1 - Z_T/Z <= 1 - Z_T/U
    nu = A0 + n / 2
    lUm = -nu * math.log(2 * B0 + Y / (n + 1)) - lm0   # relative to m(empty): envelope on BF via N17 / D11
    lw = lp - lse(np.array([log_prior_w(p, len(S)) for S in models]))  # normalised capped prior
    lZ = lse(lw + lbf)
    if lbf.max() > lUm + 1e-9:
        bad('D11env', f"p={p} n={n}: max log BF {lbf.max()} > envelope {lUm}")
    for trial in range(5):
        T = rng.choice(len(models), size=max(1, len(models) // 4), replace=False)
        lZT = lse(lw[T] + lbf[T])
        resid = 1 - np.exp(lw[T]).sum()
        U = math.exp(lZT) + math.exp(lUm) * max(resid, 0)
        if U < math.exp(lZ) * (1 - 1e-10):
            bad('D5U', f"p={p}")
        piT = np.zeros(len(models))
        piT[T] = np.exp(lw[T] + lbf[T] - lZT)
        piw = np.exp(lw + lbf - lZ)
        tv = 0.5 * np.abs(piw - piT).sum()
        if abs(tv - (1 - math.exp(lZT - lZ))) > 1e-9 or tv > 1 - math.exp(lZT) / U + 1e-12:
            bad('D5TV', f"p={p}")
    # ---- D11: Q_S >= Y/(n+1), 1 <= det H/det(G+I) <= (n+1)^k
    for S in models[1:]:
        S = list(S)
        GS = G[np.ix_(S, S)]
        H = (n + 1) * GS + np.eye(len(S))
        Q = Y - n * z[S] @ np.linalg.solve(H, z[S])
        r = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(len(S)))[1]
        if Q < Y / (n + 1) * (1 - 1e-9) or r < -1e-9 or r > len(S) * math.log(n + 1) + 1e-9:
            bad('D11', f"p={p} n={n} S={S}")

    # ---- D15-KL: mixture bounds for lambda = (1-qL) pi + qL nu
    for trial in range(5):
        nuv = rng.dirichlet(np.ones(len(models)) * 0.3)
        qL = rng.uniform(0, 0.9)
        lam = (1 - qL) * pi + qL * nuv
        kl1 = float((pi * (np.log(pi) - np.log(lam))).sum())
        kl2 = float((lam * (np.log(lam) - np.log(pi))).sum())
        if kl1 > -math.log(1 - qL) + 1e-12 or kl2 > qL * math.log(1 / pi.min()) + 1e-12:
            bad('D15KLmix', f"p={p}")
        # forward empirical KL <= chi2 <= 4 TV^2 / pi_min
        cnt = rng.multinomial(4 * 50, pi) / 200.0
        m = cnt > 0
        klf = float((cnt[m] * (np.log(cnt[m]) - np.log(pi[m]))).sum())
        chi = float(((cnt - pi) ** 2 / pi).sum())
        tv = 0.5 * np.abs(cnt - pi).sum()
        if klf > chi + 1e-12 or chi > 4 * tv ** 2 / pi.min() + 1e-12:
            bad('D15KLemp', f"p={p}")

# ---- D7 identity and coded-grid count on synthetic finite families
from smc_coded import build_grid, rhoV
cnt_viol = 0
for it in range(300):
    M = int(rng.integers(3, 60))
    lg0 = rng.normal(0, 3, M)
    dv = rng.normal(0, rng.choice([1, 5, 30, 200]), M)
    V = rng.choice(M, size=int(rng.integers(1, M + 1)), replace=False)
    u = rng.uniform(0, 1)
    v = u + rng.uniform(1e-3, 1)
    w = 2 * v - u
    F = lambda idx, t: lse(lg0[idx] + t * dv[idx])
    allx = np.arange(M)
    la = lambda t: F(V, t) - F(allx, t)
    a = lambda t: math.exp(la(t))
    lrf = 2 * F(allx, v) - F(allx, u) - F(allx, w)
    lrr = 2 * F(V, v) - F(V, u) - F(V, w)
    rf, rr = math.exp(lrf), math.exp(lrr)
    if abs(lrf - (lrr + la(u) + la(w) - 2 * la(v))) > 1e-8 * max(1, abs(lrf)):
        bad('D7id', f"M={M}")
    eta = 1 - min(a(u), a(w))
    if rr >= 0.9 and rf < 0.9 * (1 - eta) ** 2 - 1e-12:
        bad('D7transfer', f"M={M}")
    # grid count: pilot targets P random, D_V = osc_V d; bound P + ceil(2/h) + 1
    P = int(rng.integers(1, 8))
    targets = sorted(set(list(rng.uniform(0, 1, P - 1)) + [1.0]))
    grid, why = build_grid(lg0[V], dv[V], targets, 10 ** 6)
    DV = float(dv[V].max() - dv[V].min())
    if grid is not None and DV > 0:
        h = 2 * math.sqrt(math.log(10 / 9)) / DV
        if len(grid) - 1 > len(targets) + math.ceil(2 / h) + 1:
            cnt_viol += 1
            bad('D7count', f"M={M} intervals={len(grid) - 1} bound={len(targets) + math.ceil(2 / h) + 1}")
        # every increment <= h passes
        for uu in np.linspace(0, 0.99, 5):
            if rhoV(lg0[V], dv[V], uu, uu + h) < 0.9 - 1e-12:
                bad('D7h', f"M={M}")
    elif grid is None:
        bad('D7gridfail', why)

# ---- D13: ideal two-state exact maximal-increment ESS-0.9 grid, crossing cost vs log2 A
print("D13 two-state: A, stages, stages - log2 A")
for A in (10, 100, 1e3, 1e4, 1e6, 1e9, 1e12):
    c = 2.0          # terminal log odds +c on the other side
    Dl = A + c       # d(b) - d(a)
    t, stages = 0.0, 0
    while t < 1 - 1e-15:
        def ess(delta):
            lo = -A + t * Dl            # log odds of b under q_t
            lpb = -np.logaddexp(0, -lo)
            lpa = -np.logaddexp(0, lo)
            w = delta * Dl
            m1 = np.logaddexp(lpa, lpb + w)
            m2 = np.logaddexp(lpa, lpb + 2 * w)
            return math.exp(2 * m1 - m2)
        if ess(1 - t) >= 0.9:
            t = 1.0
        else:
            lo_, hi_ = 0.0, 1 - t
            for _ in range(200):
                mid = 0.5 * (lo_ + hi_)
                if ess(mid) >= 0.9:
                    lo_ = mid
                else:
                    hi_ = mid
            t += lo_
        stages += 1
    print(f"  A={A:.0e}: stages={stages}, stages-log2A={stages - math.log2(A):.3f}")

print("\nFailures by clause (empty = no counterexample):")
for k in ['D2', 'D3chi', 'D3KL', 'D5U', 'D5TV', 'D11', 'D11env', 'D15KLmix', 'D15KLemp', 'D7id', 'D7transfer',
          'D7count', 'D7h', 'D7gridfail']:
    print(f"  {k}: {len(fails.get(k, []))}", fails.get(k, [])[:3])
