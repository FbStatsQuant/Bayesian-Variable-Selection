"""O-PW2 exact small-p check of the PW2-free variance bounds (REPORT.md Theorems A-C).

Builds the v3 bridge (00_COMMON score m(S), BB(1,p) prior, block tables, discrepancy d) for a
small synthetic data set, a grid by the restricted-ESS >= 0.9 rule with V = Omega, and the v3
round kernel (p Gibbs, 1 uniform swap, B neighbour swaps, 1 independence step; random order).
Then computes EXACTLY (finite-state linear algebra, no Monte Carlo):
  * h_{s,T}, F_{s,T} = Var_{q_s}(h_{s,T}), H_{s,T} = max h_{s,T}, sigma^2_T = sum_s F_{s,T}
  * stage constants chi2_t, delta2_t, gbar_t, lambda_t (L2 gap), eps_t (T09 minorisation)
  * v_t = E[W_t^2] for every t <= T and several N (two-particle pair recursion, REPORT Lemma 4)
  * bounds: sigma^2/N (asymptotic), Theorem B recursion U_T, Theorem C primitive bound,
    exact-refresh value prod(1+chi2/N)-1, OPTIONAL_PW2 (B)-(C) constants plugged into T25(iv) B_T
  * minimal PW2 constants a_t* = N (v_t - v_{t-1}) / v_{t-1}
Monte Carlo of the actual particle system cross-checks the exact v_T.

Simplifications (stated in REPORT): contiguous blocks of size <= B instead of complete-linkage;
for p >= 8 the uniform-random-order average is replaced by the average over R random orders
and their reverses (still q_phi-reversible and q_phi-invariant, so the theorems apply verbatim);
for p = 6 the exact uniform average over all m! orders is computed by subset DP.

Usage: python pw2_exact.py <p> <rho_corr> <kernel: full|gibbs1|indep> [seed]
"""
import sys, os, json, math, itertools
import numpy as np
from scipy.special import gammaln

np.set_printoptions(linewidth=160, precision=4)

def logsumexp(a):
    m = np.max(a); return m + np.log(np.sum(np.exp(a - m)))

def make_data(n, p, rho, seed):
    rng = np.random.default_rng(seed)
    C = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    Xr = rng.standard_normal((n, p)) @ np.linalg.cholesky(C).T
    beta = np.zeros(p); beta[[0, 2, p // 2 + 1]] = [0.6, -0.5, 0.4]
    yr = Xr @ beta + rng.standard_normal(n)
    X = Xr - Xr.mean(0); X = X / X.std(0, ddof=1)
    y = yr - yr.mean(); y = y / y.std(ddof=1)
    return X, y

def log_bf_all(X, y):
    n, p = X.shape
    nu = 0.01 + n / 2; b0 = 0.01
    yy = y @ y; A0 = 2 * b0 + yy
    out = np.zeros(2 ** p)
    for S in range(2 ** p):
        idx = [j for j in range(p) if S >> j & 1]
        if not idx: continue
        XS = X[:, idx]; G = XS.T @ XS; z = XS.T @ y
        H = (n + 1) * G + np.eye(len(idx))
        DS = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(len(idx)))[1]
        Q = yy - n * z @ np.linalg.solve(H, z)
        out[S] = -0.5 * DS + nu * (np.log(A0) - np.log(2 * b0 + Q))
    return out

def setup(p, rho, seed, n=60):
    X, y = make_data(n, p, rho, seed)
    lbf = log_bf_all(X, y)
    M = 2 ** p
    sizes = np.array([bin(S).count("1") for S in range(M)])
    lw = np.log(0.5) - np.array([gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k) for k in range(p + 1)])
    lprior = lw[sizes]; lprior -= logsumexp(lprior)
    B = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    blocks = [list(range(i, min(i + B, p))) for i in range(0, p, B)]
    lr = np.zeros(M)
    for blk in blocks:
        mask = sum(1 << j for j in blk)
        lr += lbf[np.arange(M) & mask]
    lg0 = lprior + lr
    d = lbf - lr
    R = np.corrcoef(X.T); thr = math.sqrt(2 * math.log(p) / n)
    nbr = [[l for l in range(p) if l != j and abs(R[j, l]) > thr] for j in range(p)]
    return dict(n=n, p=p, M=M, sizes=sizes, lg0=lg0, d=d, B=B, nbr=nbr)

def q_of(P, phi):
    a = P["lg0"] + phi * P["d"]; return np.exp(a - logsumexp(a))

def chi2(P, u, v):
    qu = q_of(P, u); a = (v - u) * P["d"]; g = np.exp(a - logsumexp(a + np.log(qu)))
    return qu @ g ** 2 - 1

def make_grid(P, thr=0.9):
    grid = [0.0]
    while grid[-1] < 1:
        u = grid[-1]
        if 1 / (1 + chi2(P, u, 1.0)) >= thr: grid.append(1.0); break
        lo, hi = u, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if 1 / (1 + chi2(P, u, mid)) >= thr: lo = mid
            else: hi = mid
        grid.append(lo)
    return grid

# ---------------- elementary kernels ----------------
def elementary(P, phi):
    M, p = P["M"], P["p"]; lg = P["lg0"] + phi * P["d"]; sizes = P["sizes"]
    Ks = []
    for j in range(p):  # Gibbs j
        K = np.zeros((M, M))
        for S in range(M):
            Sp, Sm = S | 1 << j, S & ~(1 << j)
            a, b = lg[Sp], lg[Sm]; m = max(a, b)
            pa = np.exp(a - m) / (np.exp(a - m) + np.exp(b - m))
            K[S, Sp] += pa; K[S, Sm] += 1 - pa
        Ks.append(K)
    K = np.zeros((M, M))  # uniform swap
    for S in range(M):
        k = sizes[S]
        if k in (0, p): K[S, S] = 1; continue
        ins = [j for j in range(p) if S >> j & 1]; outs = [l for l in range(p) if not S >> l & 1]
        pr = 1.0 / (k * (p - k)); stay = 1.0
        for j in ins:
            for l in outs:
                S2 = (S & ~(1 << j)) | 1 << l
                acc = min(1.0, math.exp(lg[S2] - lg[S])); K[S, S2] += pr * acc; stay -= pr * acc
        K[S, S] += stay
    Ks.append(K)
    Kn = np.zeros((M, M))  # neighbour swap
    nbr = P["nbr"]
    for S in range(M):
        if S == 0: Kn[S, S] = 1; continue
        ins = [j for j in range(p) if S >> j & 1]; stay = 1.0
        for j in ins:
            A = [l for l in nbr[j] if not S >> l & 1]
            if not A: continue
            for l in A:
                S2 = (S & ~(1 << j)) | 1 << l
                A2 = [jj for jj in nbr[l] if not S2 >> jj & 1]
                if j not in nbr[l]: continue
                acc = min(1.0, math.exp(lg[S2] - lg[S]) * len(A) / len(A2))
                pr = 1.0 / len(ins) / len(A); Kn[S, S2] += pr * acc; stay -= pr * acc
        Kn[S, S] += stay
    Ks += [Kn] * P["B"]
    pi0 = q_of(P, 0.0); d = P["d"]  # independence
    acc = np.minimum(1.0, np.exp(phi * (d[None, :] - d[:, None])))
    Ki = pi0[None, :] * acc
    np.fill_diagonal(Ki, 0); Ki[np.arange(M), np.arange(M)] = 1 - Ki.sum(1)
    Ks.append(Ki)
    return Ks

def round_kernel(P, phi, kind, R=None, rng=None):
    R = R or (12 if P["M"] <= 256 else 3)
    Ks = elementary(P, phi); m = len(Ks); M = P["M"]
    if kind == "gibbs1":  # one uniformly chosen Gibbs flip (weak kernel)
        return sum(Ks[:P["p"]]) / P["p"]
    if kind == "indep":
        return Ks[-1]
    if m <= 10:  # exact uniform average over all m! orders by subset DP
        A = {0: np.eye(M)}
        for size in range(1, m + 1):
            for comb in itertools.combinations(range(m), size):
                Sm = sum(1 << i for i in comb)
                A[Sm] = sum(A[Sm & ~(1 << i)] @ Ks[i] for i in comb)
            for key in [k for k in A if bin(k).count("1") == size - 1]: del A[key]
        return A[(1 << m) - 1] / math.factorial(m)
    out = np.zeros((M, M))
    for _ in range(R):
        perm = rng.permutation(m)
        for order in (perm, perm[::-1]):
            Kp = np.eye(M)
            for i in order: Kp = Kp @ Ks[i]
            out += Kp
    return out / (2 * R)

def lam_L2(K, q):
    s = np.sqrt(q); Sm = (s[:, None] * K) / s[None, :]
    Sm = (Sm + Sm.T) / 2 - np.outer(s, s)
    return np.max(np.abs(np.linalg.eigvalsh(Sm)))

def main():
    p = int(sys.argv[1]); rho = float(sys.argv[2]); kind = sys.argv[3]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 20261102
    thr = float(sys.argv[5]) if len(sys.argv) > 5 else 0.9
    rng = np.random.default_rng(seed + 1)
    P = setup(p, rho, seed)
    grid = make_grid(P, thr); T = len(grid) - 1
    q = [q_of(P, phi) for phi in grid]
    d = P["d"]
    g = [None]
    for t in range(1, T + 1):
        a = (grid[t] - grid[t - 1]) * d
        G = np.exp(a - a.max()); g.append(G / (q[t - 1] @ G))
    K = [None] + [round_kernel(P, grid[t], kind, rng=rng) for t in range(1, T + 1)]
    for t in range(1, T + 1):
        assert np.allclose(K[t].sum(1), 1) and np.allclose(q[t] @ K[t], q[t]), "kernel not q-invariant"
    pi0 = q[0]
    chi2s = [None] + [q[t - 1] @ g[t] ** 2 - 1 for t in range(1, T + 1)]
    del2 = [None] + [q[t] @ (g[t] - 1) ** 2 for t in range(1, T + 1)]
    gbar = [None] + [g[t].max() for t in range(1, T + 1)]
    lam = [None] + [lam_L2(K[t], q[t]) for t in range(1, T + 1)]
    eps = [None] + [np.min(pi0 / q[t]) for t in range(1, T + 1)]
    Krow_min = [None] + [np.min(K[t] / q[t][None, :]) for t in range(1, T + 1)]  # sharpest K >= beta q

    def hfun(s, Tp):
        h = np.ones(P["M"])
        for t in range(Tp, s, -1): h = g[t] * (K[t] @ h)
        return h
    def stats(Tp):
        F = []; H = []
        for s in range(Tp):
            h = hfun(s, Tp); assert abs(q[s] @ h - 1) < 1e-9
            F.append(q[s] @ h ** 2 - 1); H.append(h.max())
        return np.array(F), np.array(H)

    # exact second moments by the pair recursion
    def vexact(Tp, N):
        Fm = np.outer(g[Tp], g[Tp])
        for t in range(Tp - 1, 0, -1):
            KF = K[t] @ Fm @ K[t].T; Kd = K[t] @ np.diag(Fm)
            Fm = g[t][:, None] * g[t][None, :] * ((1 - 1 / N) * KF + (1 / N) * 0.5 * (Kd[None, :] + Kd[:, None]))
        return (1 - 1 / N) * q[0] @ Fm @ q[0] + (1 / N) * q[0] @ np.diag(Fm)

    def pairfun(Fm, top, N):  # E[W_top^2 qhat_top^{(x)2}(Fm)], Fm a pair function at level top
        for t in range(top, 0, -1):
            KF = K[t] @ Fm @ K[t].T; Kd = K[t] @ np.diag(Fm)
            Fm = g[t][:, None] * g[t][None, :] * ((1 - 1 / N) * KF + (1 / N) * 0.5 * (Kd[None, :] + Kd[:, None]))
        return (1 - 1 / N) * q[0] @ Fm @ q[0] + (1 / N) * q[0] @ np.diag(Fm)
    def e_exact(s, Tp, N):  # e_s = E[W_s^2 mu_s(h_{s,T}^2)]
        h2 = hfun(s, Tp) ** 2
        if s == 0: return q[0] @ h2
        return pairfun(np.outer(g[s], g[s] * (K[s] @ h2)), s - 1, N)

    Ns = [10, 30, 100, 300, 1000, 2500]
    allstats = {Tp: stats(Tp) for Tp in range(1, T + 1)}
    res = dict(p=p, rho=rho, kind=kind, seed=seed, thr=thr, T=T, grid=grid,
               chi2=chi2s[1:], delta2=del2[1:], gbar=gbar[1:], lam=lam[1:], eps_T09=eps[1:],
               beta_sharp=Krow_min[1:], drange=float(d.max() - d.min()))
    F, H = allstats[T]
    res["F_sT"] = F.tolist(); res["H_sT"] = H.tolist(); res["sigma2_T"] = float(F.sum())
    rows = []
    for N in Ns:
        v = [1.0] + [vexact(Tp, N) for Tp in range(1, T + 1)]
        V = [x - 1 for x in v]
        # Theorem B recursion with exact F, H
        U = [0.0]
        for Tp in range(1, T + 1):
            Fp, Hp = allstats[Tp]
            U.append((Fp.sum() + sum(Hp[s] ** 2 * math.sqrt(U[s] * (1 + U[s])) for s in range(1, Tp))) / N)
        # Theorem C primitive bounds on F_{s,T} (L2 recursion) and H_{s,T} (eps recursion), then B recursion
        def primF(Tp):
            Fb = [0.0] * (Tp + 1); Hb = [1.0] * (Tp + 1)
            for t in range(Tp, 0, -1):
                Fb[t - 1] = chi2s[t] + 2 * math.sqrt(del2[t]) * lam[t] * math.sqrt(Fb[t]) + gbar[t] * lam[t] ** 2 * Fb[t]
                Hb[t - 1] = gbar[t] * (Krow_min[t] + (1 - Krow_min[t]) * Hb[t])  # valid minorisation of the kernel used
            return Fb[:Tp], Hb[:Tp]
        Uc = [0.0]
        for Tp in range(1, T + 1):
            Fb, Hb = primF(Tp)
            Uc.append((sum(Fb) + sum(Hb[s] ** 2 * math.sqrt(Uc[s] * (1 + Uc[s])) for s in range(1, Tp))) / N)
        es = [e_exact(s, T, N) for s in range(T)]
        ident = sum((1 - 1 / N) ** (T - 1 - s) * (es[s] - 1) for s in range(T)) / N
        Fl, Hl = allstats[T]
        lowA = sum((1 - 1 / N) ** (T - 1 - s) * (Fl[s] - (Hl[s] ** 2 * math.sqrt(V[s] * (1 + V[s])) if s else 0)) for s in range(T)) / N
        Ush = [0.0]
        for Tp in range(1, T + 1):
            Fp, Hp = allstats[Tp]
            Ush.append(sum((1 - 1 / N) ** (Tp - 1 - s) * (Fp[s] + (Hp[s] ** 2 * math.sqrt(Ush[s] * (1 + Ush[s])) if s else 0)) for s in range(Tp)) / N)
        refresh = np.prod([1 + chi2s[t] / N for t in range(1, T + 1)]) - 1
        # OPTIONAL_PW2 (B)-(C) with beta = eps_T09 of K_{t-1} (t >= 2), a_1 = chi2_1
        a_opt = [chi2s[1]]
        for t in range(2, T + 1):
            be = Krow_min[t - 1]; h = gbar[t]
            e_t = (1 - be) * (h - 1); b_t = be * chi2s[t] + (1 - be) * (h ** 2 - 1)
            a_opt.append(b_t + (N - 1) * (2 * e_t + e_t ** 2))
        B_opt = np.prod([1 + a / N for a in a_opt]) - 1
        a_star = [N * (v[t] - v[t - 1]) / v[t - 1] for t in range(1, T + 1)]
        rows.append(dict(N=N, VarW_T=V[T], identity_rhs=ident, ThmB_lower=lowA, ThmB_sharp=Ush[T], sigma2_over_N=F.sum() / N, ThmB=U[T], ThmC=Uc[T],
                         refresh=refresh, T25iv_with_OPTIONAL=B_opt, a_star=a_star,
                         B_ok=bool(V[T] <= U[T] * (1 + 1e-9)), C_ok=bool(V[T] <= Uc[T] * (1 + 1e-9)),
                         allB_ok=bool(all(V[t] <= U[t] * (1 + 1e-9) for t in range(1, T + 1)))))
    res["rows"] = rows

    # Monte Carlo of the actual particle system (N = 20) to validate the exact recursion
    Nmc, R = 20, (100000 if P["M"] <= 64 else 20000 if P["M"] <= 256 else 4000)
    cum = [None] + [np.cumsum(K[t], 1) for t in range(1, T + 1)]
    c0 = np.cumsum(pi0)
    Wf = np.empty(R)
    for r in range(R):
        x = np.searchsorted(c0, rng.random(Nmc)); x = np.minimum(x, P["M"] - 1); W = 1.0
        for t in range(1, T + 1):
            w = g[t][x]; W *= w.mean()
            anc = rng.choice(Nmc, Nmc, p=w / w.sum()); x = x[anc]
            u = rng.random(Nmc); x = np.minimum((cum[t][x] < u[:, None]).sum(1), P["M"] - 1)
        Wf[r] = W
    res["mc"] = dict(N=Nmc, R=R, mean=float(Wf.mean()), var=float(Wf.var(ddof=1)),
                     var_se=float(math.sqrt((np.mean((Wf - Wf.mean()) ** 4) - Wf.var() ** 2) / R)), exact=float(vexact(T, Nmc) - 1))
    out = os.path.join(os.path.dirname(__file__), "..", "results", f"pw2_p{p}_rho{rho}_{kind}_thr{thr}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=1, default=float)
    print(json.dumps({k: res[k] for k in ["p", "rho", "kind", "T", "drange", "sigma2_T", "mc"]}, default=float))
    print("chi2", np.round(res["chi2"], 4)); print("gbar", np.round(res["gbar"], 3)); print("lam", np.round(res["lam"], 4))
    print("eps_T09", np.array(res["eps_T09"])); print("beta_sharp", np.array(res["beta_sharp"]))
    print("F_sT", np.round(F, 4)); print("H_sT", np.round(H, 3))
    for r in rows:
        print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items() if k != "a_star"},
              "a*", np.round(r["a_star"], 3))

if __name__ == "__main__":
    main()
