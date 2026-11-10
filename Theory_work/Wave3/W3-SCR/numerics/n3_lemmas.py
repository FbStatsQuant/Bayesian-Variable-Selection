"""W3-SCR N3: numerical falsification attempts for lemmas L1-L6 on random instances (several design types, including
collinear ones). Every check prints the number of trials and the worst violation (should be <= ~1e-8, or 0 failures).
Usage: py -3.13 n3_lemmas.py > n3_out.txt"""
import itertools, math
import numpy as np
from scr_lib import Score, standardise

rng = np.random.default_rng(20261109)


def design(n, p, kind):
    if kind == "iid":
        X = rng.standard_normal((n, p))
    elif kind == "cs":
        X = math.sqrt(0.7) * rng.standard_normal((n, 1)) + math.sqrt(0.3) * rng.standard_normal((n, p))
    elif kind == "dup":      # near-duplicate columns (tiny sparse eigenvalues)
        X = rng.standard_normal((n, p)); h = p // 2
        X[:, h:2 * h] = X[:, :h] + 1e-4 * rng.standard_normal((n, h))
    elif kind == "lowrank":  # p > n style rank deficiency
        X = rng.standard_normal((n, 3)) @ rng.standard_normal((3, p)) + 0.05 * rng.standard_normal((n, p))
    return standardise(X)


def instance(n, p, kind, s0=3, bscale=1.0, sigma=1.0):
    X = design(n, p, kind)
    S0 = sorted(rng.choice(p, s0, replace=False).tolist())
    theta = np.zeros(p); theta[S0] = bscale * rng.choice([-1, 1], s0) * rng.uniform(0.5, 2.0, s0)
    mu = X @ theta
    eps = sigma * rng.standard_normal(n)
    yc = mu + eps - eps.mean()
    tau2 = float(yc @ yc) / (n - 1)
    sc = Score(X, yc / math.sqrt(tau2), standardised=True)
    return sc, X, S0, theta, mu, eps, yc, tau2


def R_op(X, S, lam0):
    n = X.shape[0]
    if len(S) == 0:
        return np.eye(n)
    XS = X[:, S]
    return np.eye(n) - XS @ np.linalg.solve(XS.T @ XS + lam0 * np.eye(len(S)), XS.T)


def a_lam(X, S, t, lam):
    xt = X[:, t]
    if len(S) == 0:
        return float(xt @ xt) + lam
    XS = X[:, S]; b = XS.T @ xt
    return float(xt @ xt) + lam - float(b @ np.linalg.solve(XS.T @ XS + lam * np.eye(len(S)), b))


def rand_S(p, kmax, exclude=()):
    k = int(rng.integers(0, kmax + 1))
    pool = [j for j in range(p) if j not in exclude]
    return sorted(rng.choice(pool, k, replace=False).tolist())


print("== L1: score algebra ==")
w = dict(q=0, onestep=0, Dlo=0, Dhi=0, aug=0, Qlo=0, Qhi=0); nt = 0; add_fail = 0; add_cases = 0; del_fail = 0; del_cases = 0
add0_fail = 0; add0_cases = 0
for kind in ["iid", "cs", "dup", "lowrank"]:
    for rep in range(40):
        n = int(rng.integers(12, 40)); p = int(rng.integers(6, 30))
        sc, X, S0, theta, mu, eps, yc, tau2 = instance(n, p, kind, s0=min(3, p - 1), bscale=float(rng.choice([0.05, 0.3, 1.0, 3.0])))
        lam0 = sc.lam0; y = sc.y; K = sc.K
        Tn = (1 + 1 / n) * (2 * math.log(2 * p - 1) + math.log(n + 1))
        for _ in range(15):
            S = rand_S(p, min(K - 1, 8)); k = len(S)
            others = [j for j in range(p) if j not in S]
            if not others: continue
            t = int(rng.choice(others)); nt += 1
            R = R_op(X, S, lam0)
            ldH, ldA, Q = sc.parts(S)
            qS = float(y @ y) / (n + 1) + n / (n + 1) * float(y @ R @ y)                    # L1.1
            w["q"] = max(w["q"], abs(qS - Q)); w["Qlo"] = max(w["Qlo"], (n - 1) / (n + 1) - Q); w["Qhi"] = max(w["Qhi"], Q - (n - 1))
            a = float(X[:, t] @ R @ X[:, t]) + lam0; a1 = a_lam(X, S, t, 1.0)
            D = (n + 1) * a / a1
            w["Dlo"] = max(w["Dlo"], 1 - D, (n + 1) * a / n - D); w["Dhi"] = max(w["Dhi"], D - (n + 1))   # L1.3
            g = float(X[:, t] @ R @ y) ** 2 / a
            St = sorted(S + [t])
            _, _, Qt = sc.parts(St)
            pred = -math.log((2 * p - 1 - k) / (k + 1)) - 0.5 * math.log(D) + sc.nu * math.log((0.02 + Q) / (0.02 + Qt))
            dF = sc.F(St) - sc.F(S)
            w["onestep"] = max(w["onestep"], abs(pred - dF), abs((Q - Qt) - n / (n + 1) * g))             # L1.2, L1.4
            # L1.7 augmented representation
            Xa = np.vstack([X, math.sqrt(lam0) * np.eye(p)]); ya = np.concatenate([y, np.zeros(p)])
            if k:
                Qa, _ = np.linalg.qr(Xa[:, S]); res = lambda v: v - Qa @ (Qa.T @ v)
            else:
                res = lambda v: v
            rt = res(Xa[:, t])
            w["aug"] = max(w["aug"], abs(float(rt @ rt) - a), abs(float(rt @ ya) - float(X[:, t] @ R @ y)))
            # L1.5 D-add
            if g >= Tn:
                add_cases += 1
                if not dF > 0: add_fail += 1
            # L1.5deg self-normalised D-add (centred units)
            rhobar = (2 * math.log(2 * p - 1) + math.log(n + 1)) / (n + 0.02)
            gyc = g * tau2; qSyc = Q * tau2
            assert rhobar * (n - 1) <= Tn + 1e-12
            if gyc >= rhobar * (n + 1) / n * (0.02 * tau2 + qSyc):
                add0_cases += 1
                if not dF > 0: add0_fail += 1
            # L1.6 D-del on (St, t)
            if dF >= 0:          # F(St \ t) <= F(St)
                del_cases += 1
                kk = k + 1
                rhs = (n + 1) / (n * sc.nu) * (0.02 + Qt) * (math.log((2 * p - kk) / kk) + 0.5 * math.log(D))
                if g < rhs - 1e-9: del_fail += 1
print(f"trials {nt}; worst |q_S - Q| {w['q']:.2e}; one-step F / Q identity {w['onestep']:.2e}; augmented identities {w['aug']:.2e}")
print(f"Q bounds violations (should be <= 0): lower {w['Qlo']:.2e} upper {w['Qhi']:.2e};  D bounds: lower {w['Dlo']:.2e} upper {w['Dhi']:.2e}")
print(f"L1.5 D-add: {add_cases} cases with g_y >= T_n, failures {add_fail};  L1.5deg: {add0_cases} cases, failures {add0_fail};  L1.6 D-del: {del_cases} cases, failures {del_fail}")

print("== L4: bridges ==")
worst40 = -np.inf; worstB2 = -np.inf; worstB2o = -np.inf; n40 = 0; nB2 = 0; nB2o = 0
for kind in ["iid", "cs", "dup", "lowrank"]:
    for rep in range(60):
        n = int(rng.integers(12, 40)); p = int(rng.integers(6, 14))
        sc, X, S0, theta, mu, eps, yc, tau2 = instance(n, p, kind, s0=min(3, p - 1), bscale=float(rng.choice([0.02, 0.3, 1.0])))
        lam0 = sc.lam0; cth = np.linalg.norm(theta) / math.sqrt(n + 1)
        for _ in range(10):
            S = rand_S(p, 5)
            T = [t for t in S0 if t not in S]
            if not T: continue
            R = R_op(X, S, lam0)
            gam = max(float(X[:, t] @ R @ mu) ** 2 / (float(X[:, t] @ R @ X[:, t]) + lam0) for t in T)
            if S:
                Qs, _ = np.linalg.qr(X[:, S]); proj = lambda v: v - Qs @ (Qs.T @ v)
            else:
                proj = lambda v: v
            Delta = float(proj(mu) @ proj(mu))
            if math.sqrt(Delta) >= cth:
                n40 += 1
                lb = Delta * (math.sqrt(Delta) - cth) ** 2 / (n * np.abs(theta[T]).sum() ** 2)
                worst40 = max(worst40, (lb - gam) / max(gam, 1e-300))
            # B2 per-S form with the anchored floor of this S
            XT = np.column_stack([proj(X[:, t]) for t in T])
            phi_a = np.linalg.eigvalsh(XT.T @ XT).min() / (n - 1)
            tmin = np.abs(theta[S0]).min()
            if phi_a > 0 and math.sqrt(phi_a * (n - 1)) * tmin >= cth:
                nB2 += 1
                lb2 = phi_a * (n - 1) / n * (math.sqrt(phi_a * (n - 1)) * tmin - cth) ** 2
                worstB2 = max(worstB2, (lb2 - gam) / max(gam, 1e-300))
                assert Delta >= phi_a * (n - 1) * float(theta[T] @ theta[T]) * (1 - 1e-9) - 1e-9
            if phi_a > 0 and math.sqrt(phi_a * (n - 1)) * tmin >= 2 * cth:          # B2deg (per model, sigma = 1)
                nB2o += 1
                sigS2 = 1.0 + float(mu @ R @ mu) / (n - 1)
                lb3 = (n - 1) ** 2 / n * phi_a ** 2 * tmin ** 2 / (4.0 + 9 * phi_a * len(S0) * tmin ** 2)
                worstB2o = max(worstB2o, (lb3 - gam / sigS2) / max(gam / sigS2, 1e-300))
print(f"L4.0: {n40} cases, worst (lower bound - gamma)/gamma = {worst40:.3e} (must be <= 0)")
print(f"B2 (per-model anchored floor): {nB2} cases, worst relative excess = {worstB2:.3e} (must be <= 0)")
print(f"B2deg (normalised visibility): {nB2o} cases, worst relative excess = {worstB2o:.3e} (must be <= 0)")

print("== L5 step 2: sum of excess gains vs projected norm ==")
worst = -np.inf; worst_w = -np.inf; nc = 0
for kind in ["iid", "cs", "dup", "lowrank"]:
    for rep in range(60):
        n = int(rng.integers(15, 40)); p = int(rng.integers(8, 20)); lam0 = 1 / (n + 1)
        X = design(n, p, kind)
        Xa = np.vstack([X, math.sqrt(lam0) * np.eye(p)])
        s0 = int(rng.integers(1, 4)); m = int(rng.integers(1, 6))
        idx = rng.choice(p, s0 + m, replace=False).tolist(); S0 = idx[:s0]; E = idx[s0:]; S = S0 + E
        G = X[:, S].T @ X[:, S]
        phi = np.linalg.eigvalsh(G).min() / (n - 1)
        if phi <= 1e-12: continue
        Q0, _ = np.linalg.qr(Xa[:, S0]); QS, _ = np.linalg.qr(Xa[:, S])
        v = rng.standard_normal(n + p)
        PWv = QS @ (QS.T @ v) - Q0 @ (Q0.T @ v)
        tot = 0.0; U = []
        for j in E:
            Sj = [i for i in S if i != j]
            Qj, _ = np.linalg.qr(Xa[:, Sj]); r = Xa[:, j] - Qj @ (Qj.T @ Xa[:, j]); u = r / np.linalg.norm(r)
            tot += float(u @ v) ** 2; U.append(u)
        U = np.column_stack(U); om = np.linalg.eigvalsh(U.T @ U).max()
        nc += 1
        worst = max(worst, tot - float(PWv @ PWv) / phi)
        worst_w = max(worst_w, tot - om * float(PWv @ PWv))
        assert om <= 1 / phi + 1e-8
print(f"{nc} cases; worst [sum_j (u_j'v)^2 - |P_W v|^2/phi] = {worst:.3e}; with omega(S) in place of 1/phi: {worst_w:.3e} (both must be <= ~1e-9)")

print("== L6: exact criterion at the empty model ==")
bad = 0; cnt = 0; suff_bad = 0
for rep in range(300):
    n = int(rng.integers(10, 60)); p = int(rng.integers(3, 40))
    sc, X, S0, theta, mu, eps, yc, tau2 = instance(n, p, "iid", s0=1, bscale=float(rng.choice([0.0, 0.1, 0.3, 0.6])))
    Ln = 2 * math.log(2 * p - 1) + math.log(n); un = Ln / (n + 0.02)
    F0 = sc.F([])
    for j in range(p):
        cnt += 1
        lhs = float(X[:, j] @ sc.y) ** 2 / n
        crit = lhs <= (n - 0.98) * (1 - math.exp(-un))
        actual = sc.F([j]) <= F0
        if abs(lhs - (n - 0.98) * (1 - math.exp(-un))) > 1e-9 and crit != actual: bad += 1
        gyc = float(X[:, j] @ yc) ** 2 * (n + 1) / n ** 2
        if un <= 2 and gyc <= tau2 * Ln * (1 - n ** -2) * (1 - un / 2) and not actual: suff_bad += 1
print(f"{cnt} singletons: exact criterion mismatches {bad}; sufficient condition (star) violations {suff_bad}")

print("== L2: Monte Carlo frequencies of the events against their bounds ==")
n, p, q, s0 = 30, 9, 3, 2
X = design(n, p, "cs"); lam0 = 1 / (n + 1)
S0 = [0, 1]; theta = np.zeros(p); theta[S0] = [1.0, -0.7]; mu = X @ theta; sigma = 1.0
taun = math.sqrt(float(mu @ mu) / (n - 1) + sigma ** 2)
subsets = [list(c) for k in range(q + 1) for c in itertools.combinations(range(p), k)]
Nq = len(subsets)
dirs = []          # witness directions R_S x_t(S) / sqrt(a): one per S (deterministic witness)
cross = []; mS2 = []; Rs = []
for S in subsets:
    R = R_op(X, S, lam0); Rs.append(R)
    v0 = R @ mu; m2 = float(mu @ v0); cross.append(v0 / math.sqrt(m2) if m2 > 0 else 0 * v0); mS2.append(m2)
    Tm = [t for t in S0 if t not in S]
    if not Tm: continue
    gam = [float(X[:, t] @ R @ mu) ** 2 / (float(X[:, t] @ R @ X[:, t]) + lam0) for t in Tm]
    t = Tm[int(np.argmax(gam))]
    v = R @ X[:, t]; a = float(X[:, t] @ v) + lam0
    dirs.append(v / math.sqrt(a))
Dm = np.array(dirs); Cm = np.array(cross); mS2 = np.array(mS2)
Qs = {tuple(S): np.linalg.qr(X[:, S])[0] for S in subsets if S}
for x in [1.0, 2.0, 3.0]:
    r = math.sqrt(2 * math.log(2 * Nq) + 2 * x)
    M = 20000; f1 = f2p = f2m = f3 = f4 = 0; step1_viol = 0; ax = math.sqrt(x / (n - 1))
    taubar = taun * (1 + 2 * ax)
    for it in range(M):
        e = sigma * rng.standard_normal(n)
        if np.abs(Dm @ e).max() > sigma * r: f1 += 1
        e4 = (Cm @ e).max() <= sigma * r
        f4 += (not e4)
        ec = e - e.mean()
        e2p = (float(ec @ ec) <= sigma ** 2 * (n - 1) * (1 + 2 * ax + 2 * ax ** 2)) and (float(mu @ e) <= sigma * math.sqrt(float(mu @ mu)) * math.sqrt(2 * x))
        if e4 and e2p and it % 50 == 0:      # SCR-Adeg step 1 (deterministic on E2+ and E4), all S
            ycc = mu + ec; t2 = float(ycc @ ycc) / (n - 1)
            for R, m2 in zip(Rs, mS2):
                lhs = 0.02 * t2 + float(ycc @ ycc) / (n + 1) + n / (n + 1) * float(ycc @ R @ ycc)
                sS2 = sigma ** 2 + m2 / (n - 1)
                rhs = 1.02 * taubar ** 2 + n / (n + 1) * (n - 1) * sS2 * (1 + 2 * ax + 2 * ax ** 2 + r / math.sqrt(n - 1))
                if lhs > rhs * (1 + 1e-12): step1_viol += 1
        yc = mu + e - e.mean(); th = math.sqrt(float(yc @ yc) / (n - 1))
        if th > taun * (1 + 2 * math.sqrt(x / (n - 1))): f2p += 1
        if th ** 2 < taun ** 2 * (1 - 4 * math.sqrt(x / (n - 1))): f2m += 1
        bad3 = False
        for S, Qm in Qs.items():
            k = len(S); U = (math.sqrt(k) + math.sqrt(2 * math.log(math.comb(p, k)) + 2 * x)) ** 2
            if float(((Qm.T @ e) ** 2).sum()) > sigma ** 2 * U: bad3 = True; break
        f3 += bad3
    print(f"x={x}: P(E4^c) {f4 / M:.4f} (bound {math.exp(-x):.4f}); SCR-Adeg step-1 violations on E2+ and E4: {step1_viol}")
    print(f"x={x}: P(E1^c) {f1 / M:.4f} (bound {math.exp(-x):.4f}); P(E2+^c) {f2p / M:.4f}, P(E2-^c) {f2m / M:.4f} (bound {2 * math.exp(-x):.4f}); "
          f"P(E3a^c, OLS part) {f3 / M:.4f} (bound {2 * q * math.exp(-x):.4f})")

print("== SCR-A / SCR-Adeg end to end on small problems (full enumeration of sparse models) ==")
def vis(X, mu, S0, q, lam0, sigma):
    """exact Gamma_n(q) and Psi_n(q) by enumeration"""
    n, p = X.shape; G = np.inf; Ps = np.inf
    for k in range(q + 1):
        for S in itertools.combinations(range(p), k):
            T = [t for t in S0 if t not in S]
            if not T: continue
            R = R_op(X, list(S), lam0)
            g = max(float(X[:, t] @ R @ mu) ** 2 / (float(X[:, t] @ R @ X[:, t]) + lam0) for t in T)
            G = min(G, g); Ps = min(Ps, g / (sigma ** 2 + float(mu @ R @ mu) / (n - 1)))
    return G, Ps

for kind, bscale, n in [("iid", 3.0, 40), ("iid", 1.0, 400), ("cs", 1.0, 400), ("iid", 0.25, 400), ("cs", 0.25, 400), ("iid", 0.8, 40), ("cs", 0.8, 40)]:
    p, q, s0 = 10, 2, 2
    X = design(n, p, kind); lam0 = 1 / (n + 1)
    S0 = [0, 1]; theta = np.zeros(p); theta[S0] = [bscale, -bscale]; mu = X @ theta; sigma = 1.0
    Gam, Psi = vis(X, mu, S0, q, lam0, sigma)
    taun = math.sqrt(float(mu @ mu) / (n - 1) + sigma ** 2)
    Tn = (1 + 1 / n) * (2 * math.log(2 * p - 1) + math.log(n + 1))
    Nq = sum(math.comb(p, k) for k in range(q + 1))
    def mc(x):
        ax = math.sqrt(x / (n - 1)); r = math.sqrt(2 * math.log(2 * Nq) + 2 * x)
        return math.sqrt(Gam) > taun * (1 + 2 * ax) * math.sqrt(Tn) + sigma * r
    def mc0(x):
        ax = math.sqrt(x / (n - 1)); r = math.sqrt(2 * math.log(2 * Nq) + 2 * x); tb = taun * (1 + 2 * ax)
        th = 2 * ax + 2 * ax ** 2 + r / math.sqrt(n - 1) + 1.02 * (n + 1) * tb ** 2 / (n * (n - 1) * sigma ** 2)
        return math.sqrt(Psi) > math.sqrt(Tn * (1 + th)) + r
    grid = np.linspace(0.05, 60, 1200)
    xa = max([x for x in grid if mc(x)], default=None); xo = max([x for x in grid if mc0(x)], default=None)
    M = 200; viol = 0
    cand = [list(c) for k in range(q + 1) for c in itertools.combinations(range(p), k) if not set(S0) <= set(c)]
    for _ in range(M):
        e = sigma * rng.standard_normal(n); yc = mu + e - e.mean()
        sc = Score(X, yc / math.sqrt(float(yc @ yc) / (n - 1)), standardised=True)
        viol += any(sc.is_certified(S) for S in cand)
    fa = None if xa is None else round(3 * math.exp(-xa), 6); fo = None if xo is None else round(4 * math.exp(-xo), 6)
    print(f"{kind} n={n} bscale={bscale}: sqrt(Gamma)={math.sqrt(Gam):.2f} sqrt(Psi)={math.sqrt(Psi):.2f} tau_n={taun:.2f} sqrt(T_n)={math.sqrt(Tn):.2f}; "
          f"MC up to x={None if xa is None else round(xa, 2)} (bound {fa}); MCdeg up to x={None if xo is None else round(xo, 2)} (bound {fo}); "
          f"draws with an LO model of size <= {q} missing a truth: {viol}/{M}")
