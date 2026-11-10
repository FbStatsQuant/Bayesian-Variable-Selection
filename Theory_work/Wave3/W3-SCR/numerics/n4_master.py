"""W3-SCR N4: numerical falsification attempt for the master gap theorem SCR-M (L7) and M3, M5.
Small problems, family H = all models of size <= q (full enumeration), default witness, counting form of b_H, c_H.
For each noise draw on which the events E1_H, E4_H, E2+ hold, check F(S + t(S)) - F(S) >= delta_S for every S in H^-.
Also: (M3) MC(q,x) or MC°(q,x) => delta_S > 0;  (M5) along coded search paths, a best-neighbour move from a centre
containing S0 to a model of H never drops a truth when all delta_S > 0 and the event holds.
Usage: py -3.13 n4_master.py > n4_out.txt"""
import itertools, math
import numpy as np
from scr_lib import Score, standardise

rng = np.random.default_rng(4242)


def design(n, p, kind):
    if kind == "iid": X = rng.standard_normal((n, p))
    elif kind == "cs": X = math.sqrt(.6) * rng.standard_normal((n, 1)) + math.sqrt(.4) * rng.standard_normal((n, p))
    elif kind == "dup":
        X = rng.standard_normal((n, p)); h = p // 2; X[:, h:2 * h] = X[:, :h] + 1e-3 * rng.standard_normal((n, h))
    return standardise(X)


def R_op(X, S, lam0):
    n = X.shape[0]
    if not S: return np.eye(n)
    XS = X[:, S]
    return np.eye(n) - XS @ np.linalg.solve(XS.T @ XS + lam0 * np.eye(len(S)), XS.T)


tot_draws = 0; ev_draws = 0; checks = 0; viol = 0; worst = np.inf; m3_cases = 0; m3_fail = 0; m5_moves = 0; m5_fail = 0
for kind, n, p, q, bscale, x in [("iid", 30, 8, 2, 1.0, 1.0), ("cs", 30, 8, 2, 2.0, 1.0), ("dup", 30, 8, 2, 1.5, 2.0), ("iid", 200, 7, 2, 0.6, 3.0),
                                 ("cs", 200, 7, 2, 0.8, 3.0), ("iid", 400, 6, 1, 0.5, 4.0), ("iid", 30, 8, 2, 0.2, 1.0),
                                 ("iid", 400, 6, 1, 1.5, 3.0), ("iid", 1000, 6, 2, 1.0, 3.0), ("cs", 1000, 6, 2, 1.5, 3.0), ("iid", 1500, 7, 2, 3.0, 4.0)]:
    X = design(n, p, kind); lam0 = 1 / (n + 1); sigma = 1.0; nu = 0.01 + n / 2
    S0 = [0, 1]; theta = np.zeros(p); theta[S0] = [bscale, -0.7 * bscale]; mu = X @ theta
    K = min(p, n // 2); assert q <= K - 1
    Hm = [list(c) for k in range(q + 1) for c in itertools.combinations(range(p), k) if not set(S0) <= set(c)]
    M = len(Hm); Nq = sum(math.comb(p, k) for k in range(q + 1))
    taun = math.sqrt(float(mu @ mu) / (n - 1) + sigma ** 2); ax = math.sqrt(x / (n - 1)); taubar = taun * (1 + 2 * ax)
    bH = cH = math.sqrt(2 * math.log(M) + 2 * x); rn = math.sqrt(2 * math.log(2 * Nq) + 2 * x)
    Tn = (1 + 1 / n) * (2 * math.log(2 * p - 1) + math.log(n + 1))
    info = []; Gam = np.inf; Psi = np.inf
    for S in Hm:
        R = R_op(X, S, lam0); T = [t for t in S0 if t not in S]
        gam = [float(X[:, t] @ R @ mu) ** 2 / (float(X[:, t] @ R @ X[:, t]) + lam0) for t in T]
        t = T[int(np.argmax(gam))]; g = max(gam)
        v = R @ X[:, t]; a = float(X[:, t] @ v) + lam0
        sgn = 1.0 if float(X[:, t] @ R @ mu) >= 0 else -1.0
        d = -sgn * v / math.sqrt(a)
        m2 = float(mu @ R @ mu); e = (R @ mu) / math.sqrt(m2) if m2 > 0 else np.zeros(n)
        k = len(S)
        XS = X[:, S]
        a1 = (float(X[:, t] @ X[:, t]) + 1.0 - (float((XS.T @ X[:, t]) @ np.linalg.solve(XS.T @ XS + np.eye(k), XS.T @ X[:, t])) if k else 0.0))
        D = (n + 1) * a / a1
        B = math.log((2 * p - 1 - k) / (k + 1)) + 0.5 * math.log(D)
        assert B >= 0
        G = max(math.sqrt(g) - sigma * bH, 0.0) ** 2
        U = 1.02 * taubar ** 2 + n / (n + 1) * (m2 + 2 * sigma * math.sqrt(m2) * cH + sigma ** 2 * (n - 1) * (1 + 2 * ax + 2 * ax ** 2))
        Ub = min(U, (n - 0.98) * taubar ** 2)
        u = n * G / ((n + 1) * Ub)
        delta = (-nu * math.log(1 - u) - B) if u < 1 else np.inf
        sS2 = sigma ** 2 + m2 / (n - 1)
        Gam = min(Gam, g); Psi = min(Psi, g / sS2)
        info.append((S, t, d, e, delta))
    th0 = 2 * ax + 2 * ax ** 2 + rn / math.sqrt(n - 1) + 1.02 * (n + 1) * taubar ** 2 / (n * (n - 1) * sigma ** 2)
    MC = math.sqrt(Gam) > taubar * math.sqrt(Tn) + sigma * rn
    MC0 = math.sqrt(Psi) > math.sqrt(Tn * (1 + th0)) + rn
    allpos = all(dl > 0 for *_, dl in info)
    if MC or MC0:
        m3_cases += 1
        if not allpos: m3_fail += 1
    Dm = np.array([d for _, _, d, _, _ in info]); Em = np.array([e for _, _, _, e, _ in info])
    ndraw = 400; ev = 0
    for _ in range(ndraw):
        eps = sigma * rng.standard_normal(n); ec = eps - eps.mean(); tot_draws += 1
        if not ((Dm @ eps).max() <= sigma * bH and (Em @ eps).max() <= sigma * cH and float(ec @ ec) <= sigma ** 2 * (n - 1) * (1 + 2 * ax + 2 * ax ** 2)
                and float(mu @ eps) <= sigma * math.sqrt(float(mu @ mu)) * math.sqrt(2 * x)):
            continue
        ev += 1; ev_draws += 1
        yc = mu + ec
        sc = Score(X, yc / math.sqrt(float(yc @ yc) / (n - 1)), standardised=True)
        for S, t, _, _, delta in info:
            dF = sc.F(sorted(S + [t])) - sc.F(S); checks += 1
            if np.isfinite(delta):
                worst = min(worst, dF - delta)
                if dF < delta - 1e-8: viol += 1
            else:
                viol += 1          # event should be empty when some u_S >= 1
        if allpos:                 # M5 along coded search paths from a few starts
            for st in ([], [2], [2, 3], [0, 2], S0 + [2], [1, 3, 4]):
                path = sc.local_search(st)["path"]
                for C, N in zip(path[:-1], path[1:]):
                    if set(S0) <= set(C) and len(N) <= q:
                        m5_moves += 1
                        if not set(S0) <= set(N): m5_fail += 1
    print(f"{kind} n={n} p={p} q={q} bscale={bscale} x={x}: |H^-|={M}, event held in {ev}/{ndraw} draws (bound >= {max(0, 1 - 4 * math.exp(-x)):.3f}); "
          f"min delta_S = {min(dl for *_, dl in info):.2f}; MC {MC}, MCdeg {MC0}, all delta_S > 0: {allpos}")
print(f"TOTAL: {ev_draws}/{tot_draws} draws on the event; {checks} gap checks, violations {viol}, min (dF - delta_S) = {worst:.4f}")
print(f"M3: {m3_cases} configurations with MC or MCdeg true, of which delta_S <= 0 for some S: {m3_fail}")
print(f"M5: {m5_moves} moves from a centre containing S0 to a model of size <= q (on the event, all delta_S > 0), truth dropped: {m5_fail}")
