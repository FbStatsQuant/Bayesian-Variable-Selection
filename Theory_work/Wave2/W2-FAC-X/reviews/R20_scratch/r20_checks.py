# R20 council seat: independent falsification checks for Theorem FAC-CS-iid.
# (1) exact gain formula X1.4 (g3)/(g4) vs production gains; (2) X1.3 reference identity; (3) X1.4 (g5) algebraic identity;
# (4) scaling of exact delta_j(T) on path sets vs Hbar*sqrt(p log n / n) (Proposition X2 shape), pure-deletion path checks.
import sys, math, json, numpy as np
sys.path.insert(0, r"../../numerics")
import iid_core as ic

def setup(n, p, rho, s0, seed):
    rng = np.random.default_rng(seed)
    Lam = np.full(p, math.sqrt(rho))
    beta = np.zeros(p); S0 = sorted(int(s) for s in rng.choice(p, s0, replace=False))
    beta[S0] = rng.choice([-1, 1], s0) * rng.uniform(0.6, 1.4, s0)
    P = ic.IidData(Lam, beta, n, rng)
    A = P.A; N = n - 3; ell = math.sqrt(rho / (1 - rho))
    d = dict(P=P, S0=S0, N=N, ell=ell, xi=A[2:, 0].copy(), a=A[2:, 1].copy(), eta=A[1, 0], phi=A[1, 1],
             W=A[2:, 2:] @ A[2:, 2:].T, rho=rho, n=n, p=p)
    d["kap"] = N / (ell ** 2 * d["phi"] ** 2); d["vr"] = N * d["eta"] / (ell * d["phi"] ** 2)
    d["v1"] = d["xi"] + ell * d["eta"]; d["v2"] = ell * d["phi"] + d["a"]
    return d

def tauhat(d, T):
    T = list(T); k = len(T); gk = 1 / (k + d["kap"])
    AT = d["W"][np.ix_(T, T)] + np.outer(d["v2"][T], d["v2"][T]); Ai = np.linalg.inv(AT)
    om = (Ai @ d["v1"][T]) / np.sqrt(np.diag(Ai))
    xT = (d["xi"][T].sum() - d["vr"]) / (k + d["kap"])
    q = float(d["v1"][T] @ Ai @ d["v1"][T])
    return math.sqrt(d["N"]) * math.sqrt(1 - gk) * om, xT, q, om

def check_gain_formula(d, T):
    """compare exact production deletion gains with X1.4 (g3) without e1 and r (exact main term)."""
    P = d["P"]; n = d["n"]; T = sorted(T); k = len(T)
    st = ic.PathState(P, T); Gd, Ga, Gs, psi = st.gains()
    th, xT, q, om = tauhat(d, T)
    S0s = set(d["S0"]); nu = P.nu; gkm1 = 1 / (k - 1 + d["kap"])
    E = d["P"].A[0]; e2 = float(E @ E)  # ||e||^2 (sigma=1)
    s2 = (n - 1.0); # y = Y/s ; ||e||^2/s^2 needs s
    # recompute s from the data: Y = beta Xc + E
    Xc_y = None
    errs = []
    for r, j in enumerate(T):
        if j in S0s: continue
        qm = q - om[r] ** 2
        # exact OLS-based main term: Q_{T\j}-Q_T ~ (n/(n+1)) (||e||^2/s^2) om^2/((1+q)(1+qm))
        errs.append((j, r, qm))
    # s^2 = ||Y||^2/(n-1)
    beta = np.zeros(d["p"]); beta[d["S0"]] = d["P"].theta[d["S0"]] / d["P"].sd[d["S0"]]
    lam = math.sqrt(d["rho"]); A = d["P"].A
    Xc = lam * A[1][None, :] + math.sqrt(1 - d["rho"]) * A[2:]
    Y = beta @ Xc + A[0]; s2 = float(Y @ Y) / (n - 1)
    lw = P.logw
    out = []
    for j, r, qm in errs:
        Delta = lw[k - 1] - lw[k] + 0.5 * math.log(n + 1)
        M = nu * (n / (n + 1)) * (e2 / s2) / (d["N"] * (1 + q) ** 2 * psi)
        epsd = (1 + q) / (1 + qm) - 1
        pred = Delta - nu * math.log1p((1 + gkm1) * M * (1 + epsd) * th[r] ** 2 / nu)
        out.append(abs(pred - Gd[r]))
    return max(out)

def path_run(n, p, rho, s0, seed, nsample=15):
    d = setup(n, p, rho, s0, seed)
    P = d["P"]; S0 = d["S0"]; S0s = set(S0)
    res = ic.ls0_path(P, list(range(p)), S0)
    moves = res["moves"]; T = list(range(p)); deleted = []; maxd = 0.0; exc = 0.0; band = 0.0; gerr = 0.0
    steps = len(moves); sample = set(np.linspace(0, max(steps - 1, 0), min(steps, nsample)).astype(int))
    ok = all(m[0] == "delN" for m in moves) and set(res["final"]) == S0s
    for i, mv in enumerate(moves):
        if mv[0] != "delN": break
        j = mv[1]; Tn = [t for t in T if t not in S0s]; k = len(T)
        xT = (d["xi"][T].sum() - d["vr"]) / (k + d["kap"])
        dT = np.abs(d["xi"][Tn] - xT).min(); exc = max(exc, abs(d["xi"][j] - xT) - dT)
        below = [d["xi"][t] for t in Tn if d["xi"][t] < xT]; above = [d["xi"][t] for t in Tn if d["xi"][t] > xT]
        aT = max(below) if below else -np.inf; bT = min(above) if above else np.inf
        if deleted:
            dv = d["xi"][deleted]; band = max(band, max(0.0, float(np.maximum(aT - dv, dv - bT).max())))
        if i in sample and len(Tn) >= 1:
            th, xT2, q, om = tauhat(d, T); idx = {t: r for r, t in enumerate(T)}
            maxd = max(maxd, max(abs(th[idx[t]] - (d["xi"][t] - xT2)) for t in Tn))
            if k >= s0 + 2 and i % 3 == 0:
                gerr = max(gerr, check_gain_formula(d, T))
        T.remove(j); deleted.append(j)
    m_all = p - s0; Ln = math.log(math.log(n)); Hb = math.sqrt(2 * math.log(2 * m_all + 2) + 2 * Ln)
    scale = Hb * math.sqrt(p * math.log(n) / n)
    inf = res["info"]
    return dict(n=n, p=p, rho=rho, s0=s0, seed=seed, logratio=round(math.log(p) / math.log(n), 3), ok=bool(ok), moves=steps,
                maxdelta=round(maxd, 5), maxdelta_over_scale=round(maxd / scale, 3),
                slack_excess=round(exc, 5), slack_over_maxd=round(exc / maxd, 2) if maxd else None,
                band=round(band, 5), band_over_maxd=round(band / maxd, 2) if maxd else None,
                gain_formula_maxerr=float("%.3g" % gerr), max_add_over_logn=round(inf["max_add_gain"] / math.log(n), 3),
                max_truth=round(inf["max_truth_move"], 1), swap_minus_del=round(inf["max_swap_minus_del"], 3))

def ref_identity(seed=0):
    # X1.3: with W=N I and a=0, N A^{-1} v1 = xi - x_T and (A^{-1})_jj = (1-gamma_k)/N
    rng = np.random.default_rng(seed); N = 997.0; k = 7; ell = 0.8; phi = math.sqrt(1000.0); eta = rng.standard_normal()
    xi = rng.standard_normal(k); v1 = xi + ell * eta; A0 = N * np.eye(k) + ell ** 2 * phi ** 2 * np.ones((k, k))
    kap = N / (ell ** 2 * phi ** 2); vr = N * eta / (ell * phi ** 2); xT = (xi.sum() - vr) / (k + kap); g = 1 / (k + kap)
    Ai = np.linalg.inv(A0)
    return float(np.abs(N * Ai @ v1 - (xi - xT)).max()), float(np.abs(np.diag(Ai) - (1 - g) / N).max())

def swap_identity(trials=2000, seed=1):
    rng = np.random.default_rng(seed); worst = 0.0
    for _ in range(trials):
        k = rng.integers(2, 50); kap = rng.uniform(0.05, 20)
        g = lambda m: 1 / (m + kap)
        tj, tl = rng.standard_normal(2) * 3
        lhs = (1 + g(k - 1)) * ((1 - g(k)) ** 2 * (tl + g(k - 1) * tj) ** 2 - tj ** 2)
        rhs = tl ** 2 - tj ** 2 - g(k) * (tl - tj) ** 2
        worst = max(worst, abs(lhs - rhs))
    return worst

if __name__ == "__main__":
    print("ref_identity", ref_identity()); print("swap_identity_maxerr", swap_identity()); sys.stdout.flush()
    cfg = [(10**6, 100, 0.5, 2), (10**6, 250, 0.5, 2), (10**6, 500, 0.5, 2), (10**6, 900, 0.5, 2),
           (10**5, 300, 0.3, 1), (10**6, 300, 0.3, 1), (10**7, 300, 0.3, 1), (10**8, 300, 0.3, 1),
           (10**7, 900, 0.8, 3), (3*10**7, 900, 0.02, 2)]
    for c in cfg:
        for seed in (101, 102):
            print(json.dumps(path_run(*c, seed))); sys.stdout.flush()
