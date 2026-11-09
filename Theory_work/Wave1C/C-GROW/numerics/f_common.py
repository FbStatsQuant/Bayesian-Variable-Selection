"""f_common.py -- C-GROW falsification tests (F1 AR(1), F2 S5, F3 start-mode size).  Reuses (does not modify) bvs_core.py.

Row spec (dict): id, kind ('ar1'|'s5'), p, n, rho or c, theta, S0, P, Q, and seeds.
Per row: X exact-Gram design (fixed per row), noise eps_s = default_rng(...).standard_normal(n), y = standardize_y(X theta + eps).
Tasks: 'pop' (population margins), 'lat' (lattice NA/TL/Z^2 over all seeds at once), ('seed', s) (start mode + LS runs).
"""
import os, sys, math, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.linalg import cho_factor, cho_solve
import bvs_core as bc

TH4 = np.array([1.4, -1.0, 1.8, -1.2])
BIG = 10 ** 4


# ------------------------------------------------------------------ designs / rows
def ar1_sigma(p, rho):
    i = np.arange(p)
    return rho ** np.abs(i[:, None] - i[None, :]) if rho != 0 else np.eye(p)


def ar1_truth(p):
    """s0 = 4 truths at floor(p/8 + k p/4), k = 0..3 (p=100: 12,37,62,87; p=199: 24,74,124,174; p=400: 50,150,250,350; p=399: 49,149,249,349)"""
    return [int(math.floor(p / 8.0 + k * p / 4.0 + 1e-9)) for k in range(4)]


def eta_of(p, n):
    A = math.log(p) / math.log(n)
    return A, 0.5 * (math.sqrt(2 * A + 1) - math.sqrt(2 * A)) ** 2


def dn_of(p, n, rho, s0=4, thmax=1.8):
    A, eta = eta_of(p, n)
    arg = 16 * s0 ** 2 * thmax ** 2 * n * (1 + rho ** 2) / (1 - rho ** 2) / (eta * math.log(n))
    return math.ceil(math.log(arg) / (2 * math.log(1 / abs(rho))))


def make_row_ar1(p, n, rho, nseeds=10, tag="F1"):
    S0 = ar1_truth(p)
    th = np.zeros(p)
    th[S0] = TH4
    dn = dn_of(p, n, rho)
    P = sorted(j for j in range(p) if j not in S0 and min(abs(j - t) for t in S0) <= dn)
    return dict(id=f"{tag}_rho{rho}_p{p}_n{n}", kind="ar1", p=p, n=n, rho=rho, c=None, theta=th, S0=S0, P=P,
                dn=dn, nseeds=nseeds, xseed=1000 + 7 * n + p + int(100 * (rho + 1)),
                noise_base=100000 + n, tag=tag)


def make_row_s5(p, n, c, nseeds=10):
    import study_common as sc
    spec = sc.spec_cached(5, p, 4, 5, c)
    S0 = list(spec["S0"])
    th = np.array(spec["theta"], float)
    P = [j for j in range(p) if j not in S0]
    return dict(id=f"F2_c{c}_p{p}_n{n}", kind="s5", p=p, n=n, rho=None, c=c, theta=th, S0=S0, P=P, dn=None,
                nseeds=nseeds, xseed=555 + n + 5, noise_base=None, tag="F2", Sigma=spec["Sigma"])


_XC = {}


def build_X(row):
    key = (row["kind"], row["p"], row["n"], row["rho"], row["xseed"])
    if key not in _XC:
        Sigma = ar1_sigma(row["p"], row["rho"]) if row["kind"] == "ar1" else row["Sigma"]
        X = bc.exact_gram_design(Sigma, row["n"], np.random.default_rng(row["xseed"]))
        _XC.clear()
        _XC[key] = (X, Sigma)
    return _XC[key]


def noise(row, s):
    n = row["n"]
    if row["kind"] == "s5":
        rng = np.random.default_rng(9000 * s + 31 * n + 7 * 5 + 5)
    else:
        rng = np.random.default_rng(row["noise_base"] * 1000 + s)
    return rng.standard_normal(n)


def make_y(row, X, s):
    eps = noise(row, s)
    return bc.standardize_y(X @ row["theta"] + eps), eps


# ------------------------------------------------------------------ population margins
def pop_margins(row):
    X, Sigma = build_X(row)
    n, p = X.shape
    S0, P = row["S0"], row["P"]
    Q = set(S0) | set(P)
    blocks = bc.partition(X)
    pop = bc.Pop.from_design(X, row["theta"])
    logn = math.log(n)
    tv, tv_arg = np.inf, None
    neg, neg_arg = -np.inf, None
    for C in blocks:
        m = len(C)
        s0pos = [q for q, j in enumerate(C) if j in S0]
        nullQ = [q for q, j in enumerate(C) if j not in Q]
        if not s0pos and not nullQ:
            continue
        tab = pop.lam_table(C)
        masks = np.arange(1 << m)
        for q in s0pos:
            sel = masks[((masks >> q) & 1) == 0]
            d2 = tab[sel] - tab[sel | (1 << q)]
            i = int(np.argmin(d2))
            if d2[i] / logn < tv:
                tv = float(d2[i] / logn)
                tv_arg = (C[q], tuple(C[t] for t in range(m) if (sel[i] >> t) & 1))
        s0mask = sum(1 << q for q in s0pos)
        for q in nullQ:
            sel = masks[((masks & s0mask) == s0mask) & (((masks >> q) & 1) == 0)]
            d2 = tab[sel] - tab[sel | (1 << q)]
            i = int(np.argmax(d2))
            if d2[i] / logn > neg:
                neg = float(d2[i] / logn)
                neg_arg = (C[q], tuple(C[t] for t in range(m) if (sel[i] >> t) & 1))
    A, eta = eta_of(p, n)
    etaA = (math.sqrt(2 * A + 1) - math.sqrt(2 * A)) ** 2
    return dict(id=row["id"], kind="pop", n=n, p=p, nblocks=len(blocks), maxblock=max(len(b) for b in blocks),
                B=bc.block_size(n, p), TV=tv, TV_arg=str(tv_arg), NEG=(neg if neg > -np.inf else float("nan")),
                NEG_arg=str(neg_arg), eta=eta, etaA=etaA, gram_err=float(np.abs(X.T @ X - (n - 1) * Sigma).max()),
                col_mean_max=float(np.abs(X.mean(0)).max()),
                blocks_with_truth=str([[int(j) for j in C if j in S0] for C in blocks if any(j in S0 for j in C)]),
                n_blocks_with_2_truths=sum(1 for C in blocks if sum(1 for j in C if j in S0) > 1))


# ------------------------------------------------------------------ lattice test (all seeds at once)
def cstar(n, p, k):
    return math.log(n + 1) + 2 * math.log(2 * p - 1 - k) - 2 * math.log(k + 1)


def lattice_family(row, rng, capA=4000, capB=None):
    S0, P = list(row["S0"]), list(row["P"])
    Q = sorted(S0 + P)
    m = len(P)
    fam = {}
    if m <= 12:
        for r in range(m + 1):
            for E in itertools.combinations(P, r):
                fam[frozenset(S0) | frozenset(E)] = "all"
        return fam, dict(mode="all", nA=len(fam), nB=0, nC=0)
    if capB is None:
        capB = 4000 if len(Q) <= 120 else 1000

    def sub(cap, gen):
        small = [E for r in (0, 1) for E in itertools.combinations(P, r)]
        two = list(itertools.combinations(P, 2))
        sampled = False
        if len(small) + len(two) > cap:
            idx = rng.choice(len(two), size=max(0, cap - len(small)), replace=False)
            two = [two[i] for i in idx]
            sampled = True
        return small + two, sampled
    A, sA = sub(capA, None)
    B, sB = sub(capB, None)
    for E in A:
        fam[frozenset(S0) | frozenset(E)] = "A"
    for R in B:
        fam[frozenset(Q) - frozenset(R)] = "B"
    nC = 0
    for _ in range(300):
        keep = rng.random(m) < 0.5
        fam[frozenset(S0) | frozenset(P[i] for i in range(m) if keep[i])] = "C"
        nC += 1
    return fam, dict(mode="sampled", nA=len(A), nB=len(B), nC=nC, sampledA=sA, sampledB=sB)


class Adder:
    """Vectorised F(base + l) - F(base) and Z^2 for all l, all seeds (seed-dependent parts only through z)."""

    def __init__(self, X, ys, epss, K):
        self.n, self.p = X.shape
        self.XtX = X.T @ X
        self.dg = np.diag(self.XtX).copy()
        self.Zy = X.T @ np.stack(ys, axis=1)      # p x S
        self.Xe = X.T @ np.stack(epss, axis=1)
        self.yty = np.array([float(y @ y) for y in ys])
        self.nu = 0.01 + self.n / 2.0
        self.K = K
        self.logw = bc.log_prior_w(self.p, K)
        self.S = len(ys)

    def adds(self, t, want_z=False):
        """t: sorted int array.  Returns (gain (p,S) with nan at members, logm_base (S,), Z2 (p,S) or None)."""
        n, p, nu = self.n, self.p, self.nu
        yty = self.yty
        k = len(t)
        S = self.S
        if k == 0:
            s1 = (n + 1.0) * self.dg + 1.0
            s2 = self.dg + 1.0
            quad_b = np.zeros(S)
            v = self.Zy
            quad_n = v ** 2 / s1[:, None]
            ldb = 0.0
            Z2 = None
            if want_z:
                Z2 = self.Xe ** 2 / self.dg[:, None]
        else:
            G = self.XtX[np.ix_(t, t)]
            B = self.XtX[t, :]
            I = np.eye(k)
            cf1 = cho_factor((n + 1.0) * G + I)
            cf2 = cho_factor(G + I)
            B1 = (n + 1.0) * B
            W1 = cho_solve(cf1, B1)
            s1 = (n + 1.0) * self.dg + 1.0 - (B1 * W1).sum(0)
            W2 = cho_solve(cf2, B)
            s2 = self.dg + 1.0 - (B * W2).sum(0)
            zt = self.Zy[t, :]
            a = cho_solve(cf1, zt)
            v = self.Zy - B1.T @ a
            quad_b = (zt * a).sum(0)
            quad_n = quad_b[None, :] + v ** 2 / s1[:, None]
            ldb = 2 * np.log(np.diag(cf1[0])).sum() - 2 * np.log(np.diag(cf2[0])).sum()
            Z2 = None
            if want_z:
                cf0 = cho_factor(G)
                W0 = cho_solve(cf0, B)
                s0 = self.dg - (B * W0).sum(0)
                num = self.Xe - B.T @ cho_solve(cf0, self.Xe[t, :])
                Z2 = num ** 2 / s0[:, None]
        logm_b = -0.5 * ldb - nu * np.log(0.02 + yty - n * quad_b)
        dl = (-0.5 * (np.log(s1) - np.log(s2)))[:, None] - nu * (np.log(0.02 + yty[None, :] - n * quad_n)
                                                                  - np.log(0.02 + yty - n * quad_b)[None, :])
        gain = dl + (self.logw[k + 1] - self.logw[k] if k + 1 < len(self.logw) else -np.inf)
        if len(t):
            gain[t, :] = np.nan
            if Z2 is not None:
                Z2[t, :] = np.nan
        return gain, logm_b, Z2


def lattice_test(row, seeds):
    np.seterr(divide='ignore', invalid='ignore')
    X, _ = build_X(row)
    n, p = X.shape
    S0, P = list(row["S0"]), list(row["P"])
    Q = sorted(set(S0) | set(P))
    K = min(p, n // 2)
    ys, es = [], []
    for s in seeds:
        y, e = make_y(row, X, s)
        ys.append(y)
        es.append(e)
    ad = Adder(X, ys, es, K)
    rng = np.random.default_rng(424242 + p + n)
    fam, finfo = lattice_family(row, rng)
    S = len(seeds)
    na_max = np.full(S, -np.inf); na_arg = [None] * S
    z2_max = np.full(S, -np.inf); z2_arg = [None] * S
    zm_max = np.full(S, -np.inf); zm_arg = [None] * S          # max of Z^2 - c*(k)
    sw_max = np.full(S, -np.inf); sw_arg = [None] * S          # TL swap  F(T-i+l)-F(T)
    del_max = np.full(S, -np.inf)                              # TL deletion F(T-i)-F(T)
    nT = 0
    nskip = 0
    S0set = set(S0)
    t_start = time.time()
    chk = []
    for T in fam:
        t = np.array(sorted(T), dtype=np.int64)
        k = len(t)
        if k > K:           # infeasible model (outside Omega = {|S|<=K}): not tested
            nskip += 1
            continue
        nT += 1
        nn = len(T - S0set)
        # NA + Z^2 (adds to T)
        if k < K:
            g, lmb, Z2 = ad.adds(t, want_z=True)
            gm = np.nan_to_num(g, nan=-np.inf)
            am = gm.argmax(0)
            val = gm[am, np.arange(S)]
            for s in range(S):
                if val[s] > na_max[s]:
                    na_max[s] = val[s]; na_arg[s] = (k, nn, int(am[s]), bool(int(am[s]) in Q), tuple(t.tolist()))
            zz = np.nan_to_num(Z2, nan=-np.inf)
            am = zz.argmax(0); val = zz[am, np.arange(S)]
            ck = cstar(n, p, k)
            for s in range(S):
                if val[s] > z2_max[s]:
                    z2_max[s] = val[s]; z2_arg[s] = (k, nn, int(am[s]), ck)
            zdiff = zz - ck
            am = zdiff.argmax(0); val = zdiff[am, np.arange(S)]
            for s in range(S):
                if val[s] > zm_max[s]:
                    zm_max[s] = val[s]; zm_arg[s] = (k, nn, int(am[s]), float(zz[am[s], s]), ck)
            if nT % 200 == 1 and len(chk) < 6:   # spot check of the incremental formula against bvs_core
                pr = bc.Problem(X, ys[0], K)
                l = int(np.nanargmax(g[:, 0]))
                d1 = pr.F(tuple(sorted(T | {l}))) - pr.F(tuple(sorted(T)))
                chk.append(abs(d1 - g[l, 0]))
        # TL: neighbours removing truth i
        for i in S0:
            tm = t[t != i]
            g, lmb, _ = ad.adds(tm)
            gi = g[i, :]                        # F(T) - F(T-i)
            del_d = -gi                         # F(T-i) - F(T)
            for s in range(S):
                if del_d[s] > del_max[s]:
                    del_max[s] = del_d[s]
            gg = g - gi[None, :]
            gg[i, :] = np.nan
            gg[t, :] = np.nan                   # l must be outside T
            gg = np.nan_to_num(gg, nan=-np.inf)
            am = gg.argmax(0); val = gg[am, np.arange(S)]
            for s in range(S):
                if val[s] > sw_max[s]:
                    sw_max[s] = val[s]; sw_arg[s] = (k, nn, int(i), int(am[s]), tuple(t.tolist()))
    # direct verification of the worst NA pair and worst TL swap per seed with bvs_core.Problem.F
    na_ver, sw_ver = [], []
    for si in range(S):
        pr = bc.Problem(X, ys[si], K)
        k_, nn_, l_, inq_, T_ = na_arg[si]
        na_ver.append(pr.F(tuple(sorted(set(T_) | {l_}))) - pr.F(tuple(T_)))
        k_, nn_, i_, l_, T_ = sw_arg[si]
        sw_ver.append(pr.F(tuple(sorted((set(T_) - {i_}) | {l_}))) - pr.F(tuple(T_)))
    na_arg = [a[:4] for a in na_arg]
    sw_arg = [a[:4] for a in sw_arg]
    return dict(id=row["id"], kind="lat", seeds=list(seeds), nT=nT, nskip_infeasible=nskip, K=K, finfo=finfo, na_max=na_max.tolist(), na_arg=na_arg,
                na_verified=na_ver, sw_verified=sw_ver,
                z2_max=z2_max.tolist(), z2_arg=z2_arg, zm_max=zm_max.tolist(), zm_arg=zm_arg, sw_max=sw_max.tolist(),
                sw_arg=sw_arg, del_max=del_max.tolist(), chk_maxdiff=(max(chk) if chk else float("nan")),
                secs=time.time() - t_start)


# ------------------------------------------------------------------ per-seed method runs
def classify_path(path, S0, S0t):
    extras = set(S0t) - set(S0)
    types = {"del_extra": 0, "del_truth": 0, "add": 0, "swap": 0}
    all_del = True
    for a, b in zip(path[:-1], path[1:]):
        sa, sb = set(a), set(b)
        if len(sb) == len(sa) - 1:
            r = next(iter(sa - sb))
            if r in extras:
                types["del_extra"] += 1
            else:
                types["del_truth"] += 1
                all_del = False
        elif len(sb) == len(sa) + 1:
            types["add"] += 1; all_del = False
        else:
            types["swap"] += 1; all_del = False
    return types, all_del


def ls_summary(prob, res, S0):
    S0t = tuple(sorted(S0))
    return dict(moves=res["moves"], final_is_S0=(res["final"] == S0t), certified=res["certified"],
                local_limit=res["local_limit"], S0_scored=(S0t in res["scored"]))


def seed_run(row, s, do_ls=True):
    X, _ = build_X(row)
    n, p = X.shape
    S0, P = tuple(sorted(row["S0"])), set(row["P"])
    y, eps = make_y(row, X, s)
    K = min(p, n // 2)
    prob = bc.Problem(X, y, K)
    blocks = bc.partition(X)
    t0 = time.time()
    info = bc.start_mode(prob, blocks)
    St = tuple(sorted(info.mode))
    ext = sorted(set(St) - set(S0))
    out = dict(id=row["id"], kind="seed", seed=s, n=n, p=p, B=bc.block_size(n, p), start_size=len(St),
               n_extras=len(ext), S0_in_start=set(S0) <= set(St),
               extras_in_P=all(e in P for e in ext), n_extras_outside_P=sum(1 for e in ext if e not in P),
               start_in_Q=(set(St) <= (set(S0) | P)),
               extras_dist=str(sorted(min(abs(e - t) for t in S0) for e in ext)) if row["kind"] == "ar1" else "",
               n_optimal=info.n_optimal, truncated=info.truncated, t_start=time.time() - t0)
    if do_ls:
        r = bc.local_search(prob, St, BIG)
        types, all_del = classify_path(r["path"], S0, St)
        out.update(path_moves=r["moves"], path_all_del_extras=all_del, path_types=str(types),
                   path_final_S0=(r["final"] == S0), path_certified=r["certified"])
        for nm, cap in (("prod", bc.ell_cap(n, p)), ("cap", bc.ell_cap(n, p) + len(St))):
            rr = bc.local_search(prob, St, cap)
            d = ls_summary(prob, rr, S0)
            out.update({f"{nm}_ell": cap, f"{nm}_moves": d["moves"], f"{nm}_final_S0": d["final_is_S0"],
                        f"{nm}_certified": d["certified"], f"{nm}_local_limit": d["local_limit"],
                        f"{nm}_S0_scored": d["S0_scored"]})
        out["t_ls"] = time.time() - t0
    return out
