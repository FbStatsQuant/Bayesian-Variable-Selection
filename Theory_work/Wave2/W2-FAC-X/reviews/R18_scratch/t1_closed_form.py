"""R18 t1: re-check L4r.0 (closed form, gains, e_j bound, drift) and L4r.2(a)/(b) with continuous (non-class) loadings."""
import sys, math, numpy as np
sys.path.insert(0, '../../T2/numerics')
import eg_core as eg

def gains_formula(P, T):
    """L4r.0 gain formulas (as written in L4r_path.md) for deletions of every j in T and additions of every l not in T."""
    n, nu, lw = P.n, P.nu, P.logw
    T = np.array(sorted(T)); k = len(T)
    O = np.setdiff1d(np.arange(P.p), T)
    Q = (n - 1) - n * P.quad_closed(T); psiT = 0.02 + Q
    MT = nu * n * P.k1sq / psiT
    Dp = 1 + P.lp[T] @ P.lp[T]
    X = (P.lp[T] @ P.zc[T] - P.rho0) / Dp
    tau = P.zc[T] - P.lp[T] * X
    gp = P.lp[T]**2 / (Dp - P.lp[T]**2)
    Dk = math.log((2*P.p - k)/k) + 0.5*math.log(n+1)
    # e_j(T) := L_T - L_{T\j} - log(n+1)
    e = np.array([P.L_closed(T) - P.L_closed(np.setdiff1d(T,[j])) - math.log(n+1) for j in T])
    Gd = Dk + 0.5*e - nu*np.log1p(MT*(1+gp)*tau**2/nu)
    Dk1 = math.log((2*P.p - k - 1)/(k+1)) + 0.5*math.log(n+1)
    tl = P.zc[O] - P.lp[O]*X
    el = np.array([P.L_closed(np.union1d(T,[l])) - P.L_closed(T) - math.log(n+1) for l in O])
    Ga = -Dk1 - 0.5*el - nu*np.log1p(-MT*(1 - P.lp[O]**2/(Dp + P.lp[O]**2))*tl**2/nu)
    return T, O, Gd, Ga, e, el, X

rng = np.random.default_rng(18)
worst = 0.0; worst_e = 0.0
for trial in range(40):
    n = int(rng.choice([200, 2000, 10**5]))
    p = int(rng.integers(5, 25))
    lam = rng.uniform(0.15, 0.95, p)
    th = np.zeros(p); s0 = int(rng.integers(1, 4)); S0 = rng.choice(p, s0, replace=False)
    th[S0] = rng.choice([-1,1], s0) * rng.uniform(0.3, 2, s0)
    P = eg.EGData(lam, th, n, rng)
    nulls = np.setdiff1d(np.arange(p), S0)
    K = rng.choice(nulls, int(rng.integers(0, len(nulls)+1)), replace=False)
    T = np.union1d(S0, K).astype(int)
    if len(T) >= P.K: continue
    T, O, Gd, Ga, e, el, X = gains_formula(P, T)
    FT = P.F_direct(T)
    for idx, j in enumerate(T):
        if len(T) == 1: break
        d = P.F_direct(np.setdiff1d(T,[j])) - FT
        worst = max(worst, abs(d - Gd[idx]) / max(1, abs(d)))
    for idx, l in enumerate(O):
        d = P.F_direct(np.union1d(T,[l])) - FT
        worst = max(worst, abs(d - Ga[idx]) / max(1, abs(d)))
    psilo = (1 - lam**2).min()
    worst_e = max(worst_e, np.abs(np.r_[e, el]).max() * (n-1) * psilo)
    # (e) X_T formula with varrho over kept nulls
    Kk = np.setdiff1d(T, S0)
    Xe = (np.sum(P.eps2[Kk]*P.ell[Kk]*P.xi[Kk]) - P.varrho) / (1 + P.lp[T] @ P.lp[T])
    assert abs(Xe - X) < 1e-8*(1+abs(X)), (Xe, X)
print("max rel err (closed-form gains vs direct F):", worst)
print("max |e_j| * (n-1) psi_lo  (claimed <= 3):", worst_e)

# L4r.2(a),(b) on random and adversarial sets with theoretical Hbar, Z_m
viol_a = viol_b = 0; cnt = 0; ratio_a = 0; ratio_b = 0
for trial in range(300):
    n = 10**int(rng.integers(4, 12)); p = int(rng.integers(20, 400))
    lam = rng.uniform(0.1, 0.97, p) if trial % 2 else rng.choice([0.2, 0.95], p)
    th = np.zeros(p); S0 = rng.choice(p, 2, replace=False); th[S0] = [1.0, -0.7]
    P = eg.EGData(lam, th, n, rng)
    nulls = np.setdiff1d(np.arange(p), S0); mall = len(nulls)
    Ln = math.log(math.log(n))
    Hb = math.sqrt(2*math.log(2*mall+2) + 2*Ln)
    if np.abs(P.xi[nulls]).max() > Hb or abs(P.eta) > Ln or np.abs(P.xi[S0]).max() > Ln: continue
    lplo = P.lp.min()
    # adversarial: sort by xi/ell desc (max X), random prefix length; also random sets
    order = nulls[np.argsort(-P.xi[nulls]/P.ell[nulls])]
    for mode in range(3):
        if mode == 0: m = int(rng.integers(1, mall+1)); K = order[:m]
        elif mode == 1: m = int(rng.integers(1, mall+1)); K = order[::-1][:m]
        else: K = rng.choice(nulls, int(rng.integers(1, mall+1)), replace=False); m = len(K)
        T = np.union1d(S0, K).astype(int)
        Dp = 1 + P.lp[T] @ P.lp[T]
        X = (P.lp[T] @ P.zc[T] - P.rho0) / Dp
        tau = P.zc[K] - P.lp[K]*X
        Ba = Hb + abs(P.varrho)/lplo
        cnt += 1
        if np.abs(tau).min() > Ba: viol_a += 1
        ratio_a = max(ratio_a, np.abs(tau).min()/Ba)
        Zm2 = 2*math.log(2*mall/m) + 4*Ln
        Bb = math.sqrt(Zm2 + 2)/lplo + abs(P.varrho)
        if abs(X) > Bb: viol_b += 1
        ratio_b = max(ratio_b, abs(X)/Bb)
print("L4r.2 sets checked:", cnt, " (a) violations:", viol_a, " max ratio", round(ratio_a,3), " (b) violations:", viol_b, " max ratio", round(ratio_b,3))
