"""n3_tools.py -- N3: falsification checks of the exact tools (lemmas L0, L1) and of the level / centre / hole bounds (L4).

Part A (explicit n x p designs, RSS computed directly): for random designs (iid Gaussian rows with block-CS covariance,
and also unstructured random covariances) and random T containing S0, j in T\S0, l notin T:
  (A1) Pythagoras: Z^2(j;T\j->T) + Z^2(l;T) == Z^2(l;T\j) + Z^2(j; T\j u l)   [RSS_{T\j} - RSS_{T u l}, two orderings]
  (A2) jump inequality Z^2(l;T\j) <= Z^2(l;T) + Z^2(j;T)
  (A3) for a null l and T >= S0, Z(l;T) = <x~_l, eps>/(sigma ||x~_l||) is N(0,1): check distribution over seeds (KS-type moment check)
Part B (bcs_core, exact Gram): (B1) swap identity F(T\j u l) - F(T) == [F(T\j u l) - F(T\j)] + [F(T\j) - F(T)] (trivially exact; checked for the scanner);
  (B2) drift identity: c_bar_T - c_bar_{T\j} = kappa * r_j with kappa > 0 and kappa depending only on (u_G(j), W_T) -- check constancy within class;
  (B3) ytilde identity: ytilde_G(U) * c u w_{u-1} / sqrt(var^loc_{u-1}) == sum_{j in U} Z^loc_j(U) (a = 0 local statistics);
  (B4) closed-form residual r_l = sqrt(c)(xi_l - xibar_G) + c w_u (ghat_G - c_bar) and var_l formula vs scanner's Zsq_add.
Part C (paths): along S5 paths (p = 1000, several n), check at every step: level <= (sqrt(ell'(m)) + s_max |delta'|)^2 ;
  |delta'| <= (d_max^{3/2}/d_min) [sqrt(ell'(m)) + 1.3] ; hole <= sum over the group's deletion levels (local, a=0 form) and
  hole <= (sqrt((q-1) ell_max) + s_max|delta'|)^2 ; also the ratio hole/level and where along the path it is attained.
Output: N3_out.txt"""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bcs_core as bcs

out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    out_lines.append(s)

rng = np.random.default_rng(31)

# ------------------------------------------------------------------ Part A: explicit designs
def rss(X, Y, T):
    if len(T) == 0:
        return float(Y @ Y)
    XT = X[:, T]
    beta, *_ = np.linalg.lstsq(XT, Y, rcond=None)
    r = Y - XT @ beta
    return float(r @ r)

P("== Part A: Pythagoras identity and jump inequality on explicit designs ==")
worstA1, worstA2 = 0.0, -np.inf
for des in range(6):
    n, p, q = 300, 40, 5
    if des < 3:
        grp = np.arange(p) // q
        Hm = (grp[:, None] == grp[None, :]).astype(float)
        Sig = 0.3 + 0.4 * Hm + 0.3 * np.eye(p)
    else:
        A = rng.standard_normal((p, p))
        Sig = A @ A.T / p + 0.5 * np.eye(p)
        dd = np.sqrt(np.diag(Sig)); Sig = Sig / dd[:, None] / dd[None, :]
    L = np.linalg.cholesky(Sig)
    X = rng.standard_normal((n, p)) @ L.T
    X = X - X.mean(0)
    S0 = [2, 11, 23]
    th = np.zeros(p); th[S0] = [1.4, -1.0, 1.8]
    eps = rng.standard_normal(n)
    Y = X @ th + eps
    Y = Y - Y.mean()
    for trial in range(40):
        k = int(rng.integers(len(S0) + 2, p - 1))
        others = [i for i in range(p) if i not in S0]
        T = sorted(S0 + rng.choice(others, size=k - len(S0), replace=False).tolist())
        nulls_in = [t for t in T if t not in S0]
        j = int(rng.choice(nulls_in))
        outside = [i for i in range(p) if i not in T]
        l = int(rng.choice(outside))
        Tmj = [t for t in T if t != j]
        R_T, R_Tmj, R_Tl, R_Tmjl = rss(X, Y, T), rss(X, Y, Tmj), rss(X, Y, sorted(T + [l])), rss(X, Y, sorted(Tmj + [l]))
        lhs = (R_Tmj - R_T) + (R_T - R_Tl)       # Z^2(j;T) + Z^2(l;T)
        rhs = (R_Tmj - R_Tmjl) + (R_Tmjl - R_Tl)  # Z^2(l;T\j) + Z^2(j;T\j u l)
        worstA1 = max(worstA1, abs(lhs - rhs) / max(1.0, abs(lhs)))
        # jump inequality: Z^2(l;T\j) <= Z^2(l;T) + Z^2(j;T)
        viol = (R_Tmj - R_Tmjl) - ((R_T - R_Tl) + (R_Tmj - R_T))
        worstA2 = max(worstA2, viol)
P(f"A1 Pythagoras identity: max relative discrepancy = {worstA1:.2e}")
P(f"A2 jump inequality: max violation (should be <= 0 up to rounding) = {worstA2:.2e}")

# A3: distribution of Z(l;T) for fixed (T,l), null l, T >= S0
n, p, q = 400, 30, 5
grp = np.arange(p) // q
Hm = (grp[:, None] == grp[None, :]).astype(float)
Sig = 0.3 + 0.4 * Hm + 0.3 * np.eye(p)
L = np.linalg.cholesky(Sig)
X = rng.standard_normal((n, p)) @ L.T; X = X - X.mean(0)
S0 = [2, 11, 23]; th = np.zeros(p); th[S0] = [1.4, -1.0, 1.8]
T = sorted(S0 + [0, 1, 5, 7, 12, 13, 14, 20, 27]); l = 8
XT = X[:, T]; PT = XT @ np.linalg.pinv(XT)
xl = X[:, l] - PT @ X[:, l]
zs = []
for s in range(4000):
    eps = rng.standard_normal(n)
    zs.append(float(xl @ eps) / np.linalg.norm(xl))
zs = np.array(zs)
P(f"A3 Z(l;T) for fixed sets: mean={zs.mean():.3f} var={zs.var():.3f} P(Z^2>3.84)={np.mean(zs**2>3.841):.3f} (N(0,1): 0, 1, 0.05)")

# ------------------------------------------------------------------ Part B: exact-Gram closed forms
P("== Part B: block-CS closed forms (bcs_core, exact Gram) ==")
a, b, c, q = 0.3, 0.4, 0.3, 5
p, n = 60, 10 ** 6
th = np.zeros(p); th[[2, 26, 53]] = [1.4, -1.0, 1.8]
Pm = bcs.BCS(p, q, a, b, c, th, n, rng)
S0set = set(Pm.S0)
worstB1 = 0.0; worstB4 = 0.0; kap_rel = 0.0; kap_min = np.inf; worstB3 = 0.0

def centre(Pm, T):
    T = np.asarray(sorted(T)); u = np.bincount(Pm.grp[T], minlength=Pm.J).astype(float)
    hit = u >= 1
    xis = np.bincount(Pm.grp[T], weights=Pm.xi[T], minlength=Pm.J)
    yt = np.zeros(Pm.J); yt[hit] = math.sqrt(b) * Pm.zeta[hit] + math.sqrt(c) * xis[hit] / u[hit]
    d = np.full(Pm.J, np.inf); d[hit] = b + c / u[hit]
    W = float((1 / d[hit]).sum())
    cbar = a * float(((math.sqrt(a) * Pm.eta + yt[hit]) / d[hit]).sum()) / (1 + a * W)
    return cbar, W, u, yt, d

for trial in range(60):
    k = int(rng.integers(6, p - 1))
    others = [i for i in range(p) if i not in S0set]
    T = sorted(list(S0set) + rng.choice(others, size=k - 3, replace=False).tolist())
    nulls_in = [t for t in T if t not in S0set]
    j = int(rng.choice(nulls_in)); outside = [i for i in range(p) if i not in T]; l = int(rng.choice(outside))
    Tmj = [t for t in T if t != j]
    FT, FTmj, FTmjl = Pm.F(T), Pm.F(Tmj), Pm.F(sorted(Tmj + [l]))
    sc = Pm.scan(T)
    iT = T.index(j); iO = list(sc["O"]).index(l)
    worstB1 = max(worstB1, abs(sc["swap"][iT, iO] - ((FTmjl - FTmj) + (FTmj - FT))) / max(1, abs(FTmjl - FT)))
    # B2 drift identity: c_bar_T - c_bar_{T\j} vs r_j (residual of j w.r.t. T\j, in g units)
    cT, WT, uT, ytT, dT = centre(Pm, T)
    cTmj, _, _, _, _ = centre(Pm, Tmj)
    G = Pm.grp[j]; u = int(uT[G])
    # r_j in g-units: sqrt(c)(xi_j - mean xi over U\j) + c w_{u-1} (ghat_{U\j} - cbar_{T\j}); if u==1: g_j - cbar_{T\j}
    mates = [t for t in Tmj if Pm.grp[t] == G]
    if u >= 2:
        xib = Pm.xi[mates].mean()
        ghat = math.sqrt(a) * Pm.eta + math.sqrt(b) * Pm.zeta[G] + math.sqrt(c) * xib
        w = 1.0 / (c + b * (u - 1))
        r_j = math.sqrt(c) * (Pm.xi[j] - xib) + c * w * (ghat - cTmj)
    else:
        r_j = Pm.g[j] - cTmj
    kappa = (cT - cTmj) / r_j
    kap_min = min(kap_min, kappa)
    # predicted kappa: a * coef / (1 + a W_{T\j}) ... check only sign/positivity and class-constancy below
    # B3 ytilde identity (local a=0 statistics): ytilde_G(U) = sqrt(var^loc_{u-1})/(c u w_{u-1}) * sum_j Z^loc_j(U)
    U = [t for t in T if Pm.grp[t] == G]
    uu = len(U)
    if uu >= 1:
        yt = math.sqrt(b) * Pm.zeta[G] + math.sqrt(c) * Pm.xi[U].mean()
        w1 = 1.0 / (c + b * (uu - 1))
        varloc = c * (c + b * uu) / (c + b * (uu - 1))
        ssum = 0.0
        for jj in U:
            rest = [t for t in U if t != jj]
            if rest:
                xib = Pm.xi[rest].mean(); yrest = math.sqrt(b) * Pm.zeta[G] + math.sqrt(c) * xib
                rloc = math.sqrt(c) * (Pm.xi[jj] - xib) + c * w1 * yrest
            else:
                rloc = math.sqrt(b) * Pm.zeta[G] + math.sqrt(c) * Pm.xi[jj]
            ssum += rloc / math.sqrt(varloc)
        pred = math.sqrt(varloc) / (c * uu * w1) * ssum
        worstB3 = max(worstB3, abs(pred - yt) / max(1e-12, abs(yt)))
    # B4 closed-form add statistic vs scanner (standardized): Zsq_add * s^2/(n sigma^2) vs r_l^2/var_l in g units
    Gl = Pm.grp[l]; ul = int(uT[Gl])
    if ul >= 1:
        Ul = [t for t in T if Pm.grp[t] == Gl]
        xib = Pm.xi[Ul].mean(); ghat = math.sqrt(a) * Pm.eta + math.sqrt(b) * Pm.zeta[Gl] + math.sqrt(c) * xib
        w = 1.0 / (c + b * ul)
        r_l = math.sqrt(c) * (Pm.xi[l] - xib) + c * w * (ghat - cT)
        var_l = c * (1 + b * w) + a * c ** 2 * w ** 2 / (1 + a * WT)
    else:
        r_l = Pm.g[l] - cT; var_l = b + c + a / (1 + a * WT)
    Zsq_scan = sc["Zsq_add"][iO] * Pm.s ** 2 / n
    worstB4 = max(worstB4, abs(Zsq_scan - r_l ** 2 / var_l) / max(1e-9, r_l ** 2 / var_l))
P(f"B1 swap identity (scanner): max rel. discrepancy = {worstB1:.2e}")
P(f"B2 drift identity: min kappa = (c_bar_T - c_bar_(T\\j))/r_j over 60 random (T,j) = {kap_min:.4f} (must be > 0)")
P(f"B3 ytilde identity: max rel. discrepancy = {worstB3:.2e}")
P(f"B4 closed-form add statistic vs scanner (relative, incl. the O(1/n) ridge/scale corrections): {worstB4:.2e}")
# B2b: kappa class constancy: same u and same T -> same kappa
T = sorted(list(S0set) + [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 15, 16, 20, 21, 22, 30, 31, 32, 33, 34, 40, 45, 50, 51])
cT, WT, uT, ytT, dT = centre(Pm, T)
kap_by_u = {}
for j in T:
    if j in S0set: continue
    Tmj = [t for t in T if t != j]; cTmj = centre(Pm, Tmj)[0]
    G = Pm.grp[j]; u = int(uT[G]); mates = [t for t in Tmj if Pm.grp[t] == G]
    if u >= 2:
        xib = Pm.xi[mates].mean(); ghat = math.sqrt(a) * Pm.eta + math.sqrt(b) * Pm.zeta[G] + math.sqrt(c) * xib
        w = 1.0 / (c + b * (u - 1)); r_j = math.sqrt(c) * (Pm.xi[j] - xib) + c * w * (ghat - cTmj)
    else:
        r_j = Pm.g[j] - cTmj
    kap_by_u.setdefault(u, []).append((cT - cTmj) / r_j)
for u, ks in sorted(kap_by_u.items()):
    pred = a * (c / (c + b * (u - 1))) / (1 + a * WT - a * (u / (c + b * u) - (u - 1) / (c + b * (u - 1))))
    P(f"B2b kappa for u={u}: values {np.round(ks, 6).tolist()} ; predicted a*c*w_(u-1)/(1+aW_(T\\j)) = {pred:.6f}")

# ------------------------------------------------------------------ Part C: bounds along paths
P("== Part C: level / centre / hole bounds along S5 paths (p=1000) ==")
dmax, dmin = b + c, b + c / q
for n in [10 ** 4, 10 ** 6, 10 ** 10]:
    for seed in range(2):
        rng2 = np.random.default_rng(500 + seed + int(math.log10(n)))
        p = 1000
        th = bcs.study_layout(p, c=1.0, s0=4)
        Pm = bcs.BCS(p, q, a, b, c, th, n, rng2)
        S0set = set(Pm.S0)
        Ln = math.log(math.log(n))
        sc_fac = Pm.s ** 2 / n
        rec = dict(lev_ok=0, lev_tot=0, cen_ok=0, cen_tot=0, hole_ok=0, hole_tot=0, worst_lev=0.0, worst_cen=0.0, worst_hole=0.0,
                   hole_over_level=[], levels=[], ms=[])
        grp_levels = {}  # group -> list of deletion levels (standardized Z^2 of the deleted member at its deletion)
        state = dict(lmax=0.0)

        def record(Pm, T, sc, info):
            T = list(T); k = len(T)
            isN = np.array([t not in S0set for t in T])
            m = int(isN.sum())
            if m == 0:
                return
            cT, WT, uT, ytT, dT = centre(Pm, T)
            delta_p = cT - math.sqrt(a) * Pm.eta
            ell_p = 2 * math.log(2 ** (q + 1) * p / m) + 4 * Ln
            smax = 1.0 / math.sqrt(b + c + a / (1 + a * WT))
            zd = sc["Zsq_del"] * sc_fac
            level = float(zd[isN].min())
            rec["levels"].append(level); rec["ms"].append(m)
            state["lmax"] = max(state["lmax"], level)
            bound_lev = (math.sqrt(ell_p) + smax * abs(delta_p)) ** 2
            rec["lev_tot"] += 1; rec["lev_ok"] += level <= bound_lev; rec["worst_lev"] = max(rec["worst_lev"], level / bound_lev)
            bound_cen = (dmax ** 1.5 / dmin) * (math.sqrt(ell_p) + 1.3)
            rec["cen_tot"] += 1; rec["cen_ok"] += abs(delta_p) <= bound_cen; rec["worst_cen"] = max(rec["worst_cen"], abs(delta_p) / bound_cen)
            if np.size(sc["Zsq_add"]):
                za = sc["Zsq_add"] * sc_fac
                hole = float(za.max())
                rec["hole_over_level"].append((m, hole / level))
                bound_hole = (math.sqrt((q - 1) * state["lmax"]) + smax * abs(delta_p)) ** 2
                rec["hole_tot"] += 1; rec["hole_ok"] += hole <= bound_hole; rec["worst_hole"] = max(rec["worst_hole"], hole / bound_hole)
            if info.get("move") == "-N":
                j = info["j"]; idx = T.index(j)
                grp_levels.setdefault(int(Pm.grp[j]), []).append(float(zd[idx]))

        r = bcs.ls0_path(Pm, range(p), record=record, want_swaps=False)
        hol = rec["hole_over_level"]
        mx = max(hol, key=lambda t: t[1])
        big = [m for m, rt in hol if rt > 2.0]
        P(f"n={n:.0e} seed={seed}: pure={all(s.get('move')=='-N' for s in r['steps'] if s.get('move'))} final=S0:{r['final_is_S0']} | "
          f"level<=bound: {rec['lev_ok']}/{rec['lev_tot']} (worst ratio {rec['worst_lev']:.2f}) | "
          f"|delta'|<=bound: {rec['cen_ok']}/{rec['cen_tot']} (worst ratio {rec['worst_cen']:.2f}) | "
          f"hole<=(sqrt((q-1)lmax)+s|delta'|)^2: {rec['hole_ok']}/{rec['hole_tot']} (worst ratio {rec['worst_hole']:.2f}) | "
          f"max hole/level={mx[1]:.2f} at m={mx[0]}; steps with hole/level>2: {len(big)} (m range {min(big) if big else None}-{max(big) if big else None})")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "N3_out.txt"), "w") as f:
    f.write("\n".join(out_lines) + "\n")
