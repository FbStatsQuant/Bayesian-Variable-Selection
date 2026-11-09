"""W2-UNI numerics N2 (parallel prover seat): falsification probe for lemmas/L1_metric.md (CT_M, CD_M, RB_M, TAIL_M, LOCL).

Adversarial features (beyond the lead's n1_metric.py):
  * zero-distance clusters (pseudometric, delta = 0 between distinct indices) and small positive distances (< 1);
  * non-unit diagonals of Psi (the R01-4 point: (B^-1)_ll >= 1/C, not >= 1);
  * both branches (Sigma-branch kernels; Theta-branch diagonally dominant precisions);
  * a block pseudometric (distance 0 within / p between blocks);
  * ANALYTIC constants of L1_metric (t*, K2, t2, B, t', L0, eps(r), kappa(r)) computed from (C0, d0, c, C, K, a),
    with C0 the exact growth constant sup_r N_delta(r)/(1+r)^d0 (attained at distance values);
  * exhaustive enumeration of every (l, T) at p = 10 for the LOCL identity and inequality chain.
t*(alpha, K, a) is computed from the series S(t) of L1_metric with an adaptive truncation (tail factor e^-50), i.e.
essentially exactly; any residual truncation UNDER-estimates S, hence OVER-estimates t*, which makes the checked bound
smaller (a stricter test), never looser.
Observations only: a falsification probe of the analytic lemmas, not a certificate.
Run: py -3.13 -B n2_metric.py > n2_metric_out.txt
"""
import itertools
import numpy as np

rng = np.random.default_rng(20261110)


# ---------------------------------------------------------------- analytic constants of L1_metric
def S_fun(t, K, a, C0, d0):
    M = int(min(50.0 / max(a - t, 1e-9) + 200, 2_000_000))
    m = np.arange(M + 1, dtype=float)
    return K * C0 * np.sum((m + 2.0) ** d0 * np.exp(-(a - t) * m) * (1.0 - np.exp(-t * (m + 1.0))))


def t_star(alpha, K, a, C0, d0):
    lo, hi = 0.0, a
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if S_fun(mid, K, a, C0, d0) <= alpha / 2:
            lo = mid
        else:
            hi = mid
    return lo


def shell_tail(M, t, C0, d0):
    """C0 * sum_{m >= M} (m+2)^d0 e^{-t m}, closed form for d0 in {1, 2} (robust for tiny t)"""
    x, omx, J = np.exp(-t), -np.expm1(-t), M + 2.0
    if d0 == 1:
        s = J / omx + x / omx ** 2
    elif d0 == 2:
        s = J ** 2 / omx + 2 * J * x / omx ** 2 + x * (1 + x) / omx ** 3
    else:
        raise ValueError(d0)
    return C0 * np.exp(-t * M) * s


def constants(c, C, K, a, C0, d0, branch):
    out = {}
    if branch == "Sigma":
        t1, K1 = t_star(c, K, a, C0, d0), 2.0 / c
        KP, tP = K, a
    else:
        t1, K1 = a, K
        KP, tP = 2.0 * C, t_star(1.0 / C, K, a, C0, d0)
    t2, K2 = t_star(1.0 / C, K1, t1, C0, d0), 2.0 * C
    tp = t_star(c, KP, tP, C0, d0)
    B = 2.0 * C / c
    L0 = B * shell_tail(0, tp, C0, d0)
    out.update(t1=t1, K1=K1, t2=t2, K2=K2, KP=KP, tP=tP, tp=tp, B=B, L0=L0)
    out["eps"] = lambda r: (1 + L0) * B * shell_tail(np.floor(r), tp, C0, d0)
    out["kappa"] = lambda r: (K2 ** 2 / c) * shell_tail(np.floor(r), 2 * t2, C0, d0)
    return out


def growth_C0(d, d0):
    # sup_r max_i N_i(r)/(1+r)^d0 = max_i max over row-i distance values v of N_i(v)/(1+v)^d0 (exact)
    best = 0.0
    for row in d:
        s = np.sort(row)
        cnt = np.searchsorted(s, s, side="right")
        best = max(best, (cnt / (1.0 + s) ** d0).max())
    return best


# ---------------------------------------------------------------- geometries (pseudometrics)
def geo_cluster2d(m=11, jitter=0.45, max_cl=3):
    cent = np.array([(i, j) for i in range(m) for j in range(m)], float)
    cent += rng.uniform(-jitter, jitter, cent.shape)          # centre distances can be ~0.1 (small positive)
    sizes = rng.integers(1, max_cl + 1, len(cent))
    lab = np.repeat(np.arange(len(cent)), sizes)
    x = cent[lab]
    d = np.sqrt(((x[:, None, :] - x[None, :, :]) ** 2).sum(-1))  # 0 inside a cluster
    return d, 2, "cluster2d(m=%d,jit=%.2f,cl<=%d)" % (m, jitter, max_cl)


def geo_line_gaps(p=260, pzero=0.3, mean_gap=0.6):
    gaps, run = [], 0
    for _ in range(p - 1):
        if rng.uniform() < pzero and run < 3:
            gaps.append(0.0); run += 1
        else:
            gaps.append(rng.exponential(mean_gap)); run = 0
    x = np.concatenate([[0.0], np.cumsum(gaps)])
    d = np.abs(x[:, None] - x[None, :])
    return d, 1, "line_gaps(p=%d,P0=%.1f,gap~Exp(%.1f))" % (p, pzero, mean_gap)


def geo_blocks(p=240, gmax=4):
    lab, b = [], 0
    while len(lab) < p:
        lab += [b] * int(rng.integers(1, gmax + 1)); b += 1
    lab = np.array(lab[:p])
    d = np.where(lab[:, None] == lab[None, :], 0.0, float(p))
    return d, 1, "blocks(p=%d,g<=%d)" % (p, gmax), lab


# ---------------------------------------------------------------- matrices
def psi_sigma(d, rho=0.6, phi=1.0, scale=True):
    p = d.shape[0]
    psi = (1 - rho) * np.eye(p) + rho * np.exp(-d / phi)       # exp kernel: PSD on (multi)sets of points
    s = rng.uniform(0.6, 1.4, p) if scale else np.ones(p)
    psi = psi * s[:, None] * s[None, :]
    K = rho * s.max() ** 2
    return psi, K, 1.0 / phi


def psi_theta(d, kap=0.3, phi=1.0, cut=2.5, mu=0.5, scale=True):
    p = d.shape[0]
    th = np.where(d <= cut, -kap * np.exp(-d / phi), 0.0)
    np.fill_diagonal(th, 0.0)
    th += np.diag(mu + np.abs(th).sum(1))
    s = rng.uniform(0.6, 1.4, p) if scale else np.ones(p)
    th = th / s[:, None] / s[None, :]
    K = kap / s.min() ** 2
    return np.linalg.inv(th), K, 1.0 / phi


def psi_blocks(lab, scale=True):
    p = len(lab)
    psi = np.zeros((p, p))
    for b in np.unique(lab):
        idx = np.where(lab == b)[0]
        r = rng.uniform(-0.3, 0.7)
        psi[np.ix_(idx, idx)] = r
    np.fill_diagonal(psi, 1.0)
    s = rng.uniform(0.6, 1.4, p) if scale else np.ones(p)
    psi = psi * s[:, None] * s[None, :]
    return psi, 1.0, 1.0   # off-block entries 0: any (K, a) works; K=1 covers in-block |entries| <= 1.96*0.7 at distance 0? not needed (j!=k at distance 0 need |.|<=K e^0)


def beta(psi, A, l):
    A = np.asarray(A, int)
    out = np.zeros(psi.shape[0])
    if len(A):
        out[A] = np.linalg.solve(psi[np.ix_(A, A)], psi[A, l])
    return out


# ---------------------------------------------------------------- probes
def probe(psi, K, a, d, d0, name, branch, n_sub=12, n_pairs=160):
    p = psi.shape[0]
    ev = np.linalg.eigvalsh(psi)
    c, C = ev.min(), ev.max()
    offd = ~np.eye(p, dtype=bool)
    if branch == "Sigma":
        ok_env = np.all(np.abs(psi[offd]) <= K * np.exp(-a * d[offd]) * (1 + 1e-9))
    else:
        th = np.linalg.inv(psi)
        ok_env = np.all(np.abs(th[offd]) <= K * np.exp(-a * d[offd]) * (1 + 1e-9) + 1e-12)
    C0 = growth_C0(d, d0)
    k = constants(c, C, K, a, C0, d0, branch)
    z0 = (np.abs(d[offd]) < 1e-12).sum()
    small = ((d[offd] > 1e-12) & (d[offd] < 1)).sum()
    print(f"== {name} [{branch}-branch] p={p} spec=[{c:.3f},{C:.3f}] diag=[{psi.diagonal().min():.2f},{psi.diagonal().max():.2f}]"
          f" K={K:.3f} a={a:.3f} d0={d0} C0={C0:.3f}; zero-dist pairs={z0}, 0<dist<1 pairs={small}; envelope holds: {ok_env}")
    print(f"   constants: t1={k['t1']:.4g} K1={k['K1']:.3g} t2={k['t2']:.4g} K2={k['K2']:.3g} t'={k['tp']:.4g} B={k['B']:.3g} L0={k['L0']:.4g}")
    th = np.linalg.inv(psi)
    # CT_M on Psi (alpha=c) in Sigma-branch, on Theta (alpha=1/C) in Theta-branch, over principal submatrices
    A_full, alpha = (psi, c) if branch == "Sigma" else (th, 1.0 / C)
    ts = t_star(alpha, K, a, C0, d0)
    worst_ct = 0.0
    for it in range(n_sub):
        if it == 0:
            I = np.arange(p)
        else:
            I = np.sort(rng.choice(p, size=int(p * rng.uniform(0.2, 0.95)), replace=False))
        inv = np.linalg.inv(A_full[np.ix_(I, I)])
        bound = (2 / alpha) * np.exp(-ts * d[np.ix_(I, I)])
        worst_ct = max(worst_ct, (np.abs(inv) / bound).max())
    print(f"   CT_M  ({'Psi' if branch=='Sigma' else 'Theta'}, alpha={alpha:.3f}, t*={ts:.4g}): max |inv_ij|/((2/alpha)e^(-t* d)) over {n_sub} principal submatrices = {worst_ct:.3f}")
    # Schur-test step of CT_M: for phi = delta(., j), E = D A D^-1 - A has row sums <= S(t) (shells from m = 0)
    worst_rs = 0.0
    for tt in (0.05 * a, 0.2 * a, 0.5 * a, 0.8 * a):
        St = S_fun(tt, K, a, C0, d0)
        for j in rng.choice(p, 15, replace=False):
            ph = d[:, j]
            E = np.abs(A_full) * np.abs(np.expm1(tt * (ph[:, None] - ph[None, :])))
            np.fill_diagonal(E, 0.0)
            worst_rs = max(worst_rs, E.sum(1).max() / St, E.sum(0).max() / St)
    print(f"   CT_M Schur step: max (row or column sum of |E|)/S(t) over t in (.05,.2,.5,.8)*a and 15 centres j = {worst_rs:.3f}")
    # CD_M: conditional covariances for random U
    worst_cd, spec_lo, spec_hi = 0.0, np.inf, 0.0
    for it in range(n_sub):
        U = np.sort(rng.choice(p, size=int(p * rng.uniform(0.0, 0.9)), replace=False))
        H = np.setdiff1d(np.arange(p), U)
        cov = np.linalg.inv(th[np.ix_(H, H)])
        worst_cd = max(worst_cd, (np.abs(cov) / (k['K2'] * np.exp(-k['t2'] * d[np.ix_(H, H)]))).max())
        V = H[rng.uniform(size=H.size) < 0.6]
        if V.size:
            e = np.linalg.eigvalsh(cov[np.ix_(np.isin(H, V), np.isin(H, V))])
            spec_lo, spec_hi = min(spec_lo, e.min()), max(spec_hi, e.max())
    print(f"   CD_M  max |Cov(j,k|U)|/(K2 e^(-t2 d)) = {worst_cd:.3g};  conditional spectra in [{spec_lo:.3f},{spec_hi:.3f}] vs [c,C]=[{c:.3f},{C:.3f}]")
    # RB_M
    worst_rb, maxl1, gll_min = 0.0, 0.0, np.inf
    for it in range(n_pairs):
        l = int(rng.integers(p))
        oth = np.setdiff1d(np.arange(p), [l])
        A = oth[rng.uniform(size=oth.size) < rng.uniform(0.05, 1.0)]
        b = beta(psi, A, l)
        if A.size:
            worst_rb = max(worst_rb, (np.abs(b[A]) / (k['B'] * np.exp(-k['tp'] * d[l, A]))).max())
            Bm = psi[np.ix_(np.r_[A, l], np.r_[A, l])]
            gll_min = min(gll_min, np.linalg.inv(Bm)[-1, -1])
        maxl1 = max(maxl1, np.abs(b).sum())
    print(f"   RB_M  max |beta_v|/(B e^(-t' d)) = {worst_rb:.3g}; max ||beta||_1 = {maxl1:.3f} (L0 = {k['L0']:.4g});"
          f" min (B^-1)_ll = {gll_min:.3f} vs 1/C = {1/C:.3f} (a value < 1 shows the unit-diagonal shortcut would be wrong)")
    # LOCL and TAIL_M
    radii = (0, 0.3, 0.7, 1, 1.5, 2, 3, 5, 8)
    worst = {r: [0.0, 0.0, 0.0, 0.0, 0.0] for r in radii}  # ||Delta||_1, ratio to eps, id-resid, var-id resid, varD/kappa
    chain_viol, opnorm_viol = 0, 0
    for it in range(n_pairs):
        l = int(rng.integers(p))
        oth = np.setdiff1d(np.arange(p), [l])
        kind = it % 5
        if kind < 3:
            T = oth[rng.uniform(size=oth.size) < (0.15, 0.5, 0.9)[kind]]
        elif kind == 3:
            T = np.setdiff1d(oth, rng.choice(oth, 4, replace=False))       # almost everything
        else:
            r0 = rng.choice(radii[1:6])                                       # far set + sparse near set
            T = oth[(d[l, oth] > r0) | (rng.uniform(size=oth.size) < 0.2)]
        bT = beta(psi, T, l)
        psi_lT = psi[l, l] - psi[l, T] @ bT[T] if T.size else psi[l, l]
        for r in radii:
            U = T[d[l, T] <= r]; V = T[d[l, T] > r]
            bU = beta(psi, U, l)
            Dl = bT - bU
            n1 = np.abs(Dl).sum()
            # exact identity beta_{T,U} = beta_U - Psi_UU^-1 Psi_UV beta_{T,V}
            if U.size and V.size:
                M = np.linalg.solve(psi[np.ix_(U, U)], psi[np.ix_(U, V)])
                resid = np.abs(bT[U] - (bU[U] - M @ bT[V])).max()
                op11 = np.abs(M).sum(0).max()
                maxbw = max(np.abs(beta(psi, U, w)).sum() for w in V)
                if abs(op11 - maxbw) > 1e-8 * max(1, op11): opnorm_viol += 1
                if op11 > k['L0']: opnorm_viol += 1
                if n1 > (1 + op11) * np.abs(bT[V]).sum() * (1 + 1e-9) + 1e-12: chain_viol += 1
            else:
                resid = 0.0
            psi_lU = psi[l, l] - psi[l, U] @ bU[U] if U.size else psi[l, l]
            varD = Dl @ psi @ Dl
            vres = abs(psi_lU - psi_lT - varD)
            w = worst[r]
            w[0] = max(w[0], n1); w[1] = max(w[1], n1 / k['eps'](r)); w[2] = max(w[2], resid); w[3] = max(w[3], vres)
            w[4] = max(w[4], varD / max(k['kappa'](r), 1e-300))
            if varD > C * k['eps'](r) ** 2 * (1 + 1e-9) + 1e-14: chain_viol += 1
    print(f"   LOCL  chain violations (||D||_1 > (1+||Psi_UU^-1 Psi_UV||_11)||beta_TV||_1, or VarD > C eps^2) = {chain_viol};"
          f" ||Psi_UU^-1 Psi_UV||_11 != max_w ||beta_U(w)||_1 or > L0: {opnorm_viol}")
    for r in radii:
        w = worst[r]
        print(f"     r={r:>4}: max||beta_T-beta_U||_1={w[0]:.3e}  max ratio to eps(r)={w[1]:.2e} (eps={k['eps'](r):.3g})"
              f"  id-resid={w[2]:.1e}  var-id resid={w[3]:.1e}  max VarD/kappa(r)={w[4]:.2e}")


def exhaustive_small(p=10):
    print(f"== exhaustive LOCL / variance identity at p={p} (line with zero gaps; non-unit diagonal), every l and every T")
    d, d0, _ = geo_line_gaps(p=p, pzero=0.4, mean_gap=0.5)
    for branch in ("Sigma", "Theta"):
        psi, K, a = (psi_sigma(d) if branch == "Sigma" else psi_theta(d))
        ev = np.linalg.eigvalsh(psi); C = ev.max()
        radii = sorted(set([0.0] + list(np.unique(d)[:8]) + [0.5, 1.0, 2.0]))
        worst_id = worst_var = 0.0; chain = 0; count = 0
        for l in range(p):
            oth = [v for v in range(p) if v != l]
            for kk in range(len(oth) + 1):
                for T in itertools.combinations(oth, kk):
                    T = np.array(T, int)
                    bT = beta(psi, T, l)
                    psi_lT = psi[l, l] - (psi[l, T] @ bT[T] if T.size else 0.0)
                    for r in radii:
                        U = T[d[l, T] <= r + 1e-12] if T.size else T; V = np.setdiff1d(T, U)
                        bU = beta(psi, U, l)
                        if U.size and V.size:
                            M = np.linalg.solve(psi[np.ix_(U, U)], psi[np.ix_(U, V)])
                            worst_id = max(worst_id, np.abs(bT[U] - (bU[U] - M @ bT[V])).max())
                            if np.abs(bT - bU).sum() > (1 + np.abs(M).sum(0).max()) * np.abs(bT[V]).sum() * (1 + 1e-9) + 1e-12:
                                chain += 1
                        Dl = bT - bU
                        psi_lU = psi[l, l] - (psi[l, U] @ bU[U] if U.size else 0.0)
                        worst_var = max(worst_var, abs(psi_lU - psi_lT - Dl @ psi @ Dl))
                        if Dl @ psi @ Dl > C * np.abs(Dl).sum() ** 2 * (1 + 1e-9) + 1e-14: chain += 1
                        count += 1
        print(f"   {branch}: {count} (l,T,r) triples; zero-dist pairs={int((d[~np.eye(p,dtype=bool)]==0).sum())};"
              f" max identity resid={worst_id:.1e}; max variance-identity resid={worst_var:.1e}; chain violations={chain}")


if __name__ == "__main__":
    d, d0, nm = geo_cluster2d()
    psi, K, a = psi_sigma(d); probe(psi, K, a, d, d0, nm, "Sigma")
    psi, K, a = psi_theta(d); probe(psi, K, a, d, d0, nm, "Theta")
    d, d0, nm = geo_line_gaps()
    psi, K, a = psi_sigma(d, rho=0.5, phi=1.5); probe(psi, K, a, d, d0, nm, "Sigma")
    psi, K, a = psi_theta(d); probe(psi, K, a, d, d0, nm, "Theta")
    d, d0, nm, lab = geo_blocks()
    psi, _, _ = psi_blocks(lab)
    Kb = np.abs(psi[~np.eye(len(lab), dtype=bool)]).max()           # in-block entries at distance 0
    probe(psi, Kb, 1.0, d, d0, nm, "Sigma")
    exhaustive_small()
