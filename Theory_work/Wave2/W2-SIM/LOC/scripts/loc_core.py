r"""loc_core.py -- W2-SIM family LOC: designs + fast (validated) re-implementations used with the ticket scorer.

Scorer / objects: W2-FAC-B numerics/bvs_core.py (imported unchanged, from the deployed main archive $CODE when set,
else from this repo): Problem (score F = log w(|S|) + log m(S)), block_tables, start_mode (block DP), local_search
(reference LS, used only for validation), standardize_X, make_y_std, ell_cap.

Fast re-implementations (validated against bvs_core on small cases by loc_validate.py; output saved):
  * fast_partition(X, B): complete linkage on 1-|r| via scipy.cluster.hierarchy.linkage (O(p^2)), then the SAME top-down
    cut at B and next-fit packing as bvs_core.partition_from_corr, with left child = child with the smaller minimum
    index. Equal to bvs_core.partition whenever no two linkage distances tie (probability one for continuous data);
    validation compares the block lists exactly.
  * ls_loc(prob, centre, ell): the bvs_core.local_search rule (neighbours = adds, deletes, swaps; move to the best
    neighbour iff it strictly beats the centre; ties -> lexicographically smallest sorted tuple; stop at the move cap),
    with all neighbour scores PRE-SCREENED by rank-one inverse updates of H = (n+1)G_S + I and G_S + I (O(k p) per
    removed index), and every neighbour whose fast score is within `window` of the fast maximum RE-SCORED EXACTLY by
    prob.F_many (bvs_core arithmetic). Decisions (move / certify / tie rule) use exact scores of the re-scored set.
    The certificate is therefore a screened certificate (a neighbour outside the window is not re-scored); the
    maximal |fast - exact| discrepancy observed on re-scored models is recorded per run (fast_err_max).
"""
import os, sys, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
_CODE = os.environ.get("CODE")
_BC = (os.path.join(_CODE, "Theory_work/Wave2/W2-FAC-B/numerics") if _CODE else
       os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../W2-FAC-B/numerics"))
sys.path.insert(0, os.path.abspath(_BC))
import numpy as np                       # noqa: E402
import bvs_core as bc                    # noqa: E402
from scipy.cluster.hierarchy import linkage   # noqa: E402
from scipy.spatial.distance import squareform  # noqa: E402
from scipy.special import gammaln       # noqa: E402
from scipy.linalg import solve_triangular, cho_solve  # noqa: E402

BC_PATH = os.path.abspath(os.path.join(_BC, "bvs_core.py"))
BASE_SEED = 20261109


# ------------------------------------------------------------------------------------------------------------------
# covariance families (unit diagonal)
# ------------------------------------------------------------------------------------------------------------------
def acf_poly(alpha, p):
    """gamma(h) = (1 + h)^(-alpha), h = 0..p-1 (convex, decreasing to 0 => positive definite Toeplitz, Polya)."""
    return (1.0 + np.arange(p)) ** (-float(alpha))


def acf_arfima(d, p):
    """ARFIMA(0,d,0) autocorrelation rho(h) = prod_{i=1}^{h} (i-1+d)/(i-d); rho(h) ~ C h^{2d-1} (alpha = 1-2d)."""
    h = np.arange(1, p)
    r = np.empty(p)
    r[0] = 1.0
    r[1:] = np.cumprod((h - 1 + d) / (h - d))
    return r


def toeplitz(acf):
    p = len(acf)
    i = np.arange(p)
    return acf[np.abs(i[:, None] - i[None, :])]


def design_spec(fam, par, place, n, p):
    """Returns dict: Sigma (or None for CSG), S0 (sorted tuple), theta values (in S0 order), groups (CSG), meta."""
    if fam in ("PT", "AF"):
        acf = acf_poly(par, p) if fam == "PT" else acf_arfima(par, p)
        alpha = float(par) if fam == "PT" else 1.0 - 2.0 * float(par)
        if place == "spread":
            S0 = tuple(sorted(int(round(p * f)) for f in (0.15, 0.5, 0.85)))
        elif place == "adj":
            c = p // 2
            S0 = (c - 1, c, c + 1)
        else:
            raise ValueError(place)
        th = np.array([1.0, -0.8, 1.2])
        return dict(kind="toep", acf=acf, S0=S0, theta=th, alpha=alpha)
    if fam == "CSG":
        b, rho = par
        g = int(math.ceil(n ** b))
        G = p // g
        assert G >= 4, "need >= 4 groups"
        p_eff = G * g
        if place == "one":           # 3 truths, one per group, groups spread
            gids = [int(round(x)) for x in np.linspace(0, G - 1, 5)[1:4]]
            S0 = tuple(gi * g + g // 2 for gi in gids)
            th = np.array([1.0, -0.8, 1.2])
        elif place == "one4":        # matched control: 4 truths in 4 different groups, theta = (1, .8, 1.2, 1)
            gids = [int(round(x)) for x in np.linspace(0, G - 1, 6)[1:5]]
            S0 = tuple(gi * g + g // 2 for gi in gids)
            th = np.array([1.0, 0.8, 1.2, 1.0])
        elif place == "two":         # 4 truths, two per group, same-sign pairs (1, .8) and (1.2, 1): PTV(empty) holds
            gids = [int(round(x)) for x in np.linspace(0, G - 1, 4)[1:3]]
            S0 = (gids[0] * g + g // 2, gids[0] * g + g // 2 + 1, gids[1] * g + g // 2, gids[1] * g + g // 2 + 1)
            th = np.array([1.0, 0.8, 1.2, 1.0])
        elif place == "twoM":        # MASKING STRESS arm: pair (1, -.8) in group A (at rho = .8 the 2nd truth has zero
            gids = [int(round(x)) for x in np.linspace(0, G - 1, 4)[1:3]]   # marginal signal: PTV fails at U = empty)
            S0 = (gids[0] * g + g // 2, gids[0] * g + g // 2 + 1, gids[1] * g + g // 2, gids[1] * g + g // 2 + 1)
            th = np.array([1.0, -0.8, 1.2, 1.0])
        else:
            raise ValueError(place)
        return dict(kind="csg", g=g, G=G, p=p_eff, rho=float(rho), S0=S0, theta=th, alpha=None)
    raise ValueError(fam)


def p_of(prule, n):
    if prule == "q":          # p = n/4
        return n // 4
    if prule == "s":          # p = n^0.6
        return int(round(n ** 0.6))
    raise ValueError(prule)


def gen_raw(spec, n, p, rng):
    if spec["kind"] == "toep":
        L = np.linalg.cholesky(toeplitz(spec["acf"]))
        Z = rng.standard_normal((n, p))
        return Z @ L.T
    g, G, rho = spec["g"], spec["G"], spec["rho"]
    f = rng.standard_normal((n, G))
    E = rng.standard_normal((n, G * g))
    return math.sqrt(1.0 - rho) * E + math.sqrt(rho) * np.repeat(f, g, axis=1)


def sigma_rows(spec, idx, p):
    """population rows Sigma[idx, :] (for visibility statistics)."""
    idx = np.asarray(idx)
    if spec["kind"] == "toep":
        return spec["acf"][np.abs(idx[:, None] - np.arange(p)[None, :])]
    g, rho = spec["g"], spec["rho"]
    gr = np.arange(p) // g
    R = np.where(gr[None, :] == (idx // g)[:, None], rho, 0.0)
    R[np.arange(len(idx)), idx] = 1.0
    return R


def pop_visibility(spec, n, p, sigma=1.0):
    """psi_l = Corr_pop(x_l, x theta) * sd ratio: marginal population correlation of x_l with y; counts of nulls with
    n psi^2 >= 2 log p and >= log n (descriptive), and the largest such distance to S0 (index distance)."""
    S0 = np.array(spec["S0"])
    th = spec["theta"]
    R = sigma_rows(spec, S0, p)               # s0 x p
    c = th @ R                                 # Cov(x_l, x theta)
    vy = float(th @ R[:, S0] @ th) + sigma ** 2
    psi2 = c ** 2 / vy
    null = np.ones(p, bool); null[S0] = False
    dist = np.abs(np.arange(p)[:, None] - S0[None, :]).min(1)
    out = {"truth_marg_corr": [float(v) for v in c[S0] / np.sqrt(vy)]}
    for tag, thr in (("2logp", 2 * math.log(p)), ("logn", math.log(n))):
        v = null & (n * psi2 >= thr)
        out["nvis_" + tag] = int(v.sum())
        out["rvis_" + tag] = int(dist[v].max()) if v.any() else 0
    return out


# ------------------------------------------------------------------------------------------------------------------
# fast partition (validated against bc.partition)
# ------------------------------------------------------------------------------------------------------------------
def _pair_of(k, p):
    """condensed index k -> (i, j), i < j (scipy squareform order)."""
    i = int(p - 2 - math.floor(math.sqrt(-8 * k + 4 * p * (p - 1) - 7) / 2.0 - 0.5))
    j = int(k + i + 1 - p * (p - 1) // 2 + (p - i) * ((p - i) - 1) // 2)
    return i, j


def fast_partition(X, B=None, tie_tol=1e-10, return_info=False):
    """Partition equal to bc.partition(X): scipy complete linkage + a per-merge CERTIFICATE that the reference
    (bvs_core.complete_linkage: distances within tie_tol of the current minimum are treated as tied, then its tie rules)
    makes the same merge. Certificate: for every merge t at height h_t, every original distance D[i, j] in
    [h_t, h_t + tie_tol] is inspected; if i and j lie in two current clusters (just before merge t) other than the merged
    pair and their complete-linkage distance is <= h_t + tie_tol, the reference could see a tie -> NOT certified -> the
    partition is computed by bc.partition(X) itself (fallback). Inter-cluster complete-linkage distances are original
    entries (max of entries), so every competing pair within the tolerance is inspected. Z must be sorted by height
    (checked). Returns blocks (and info dict with certified / n_flag / fallback when return_info)."""
    n, p = X.shape
    if B is None:
        B = bc.block_size(n, p)
    if p == 1:
        return ([[0]], dict(certified=True, n_flag=0, fallback=False)) if return_info else [[0]]
    R = X.T @ X / (n - 1.0)
    D = np.clip(1.0 - np.abs(R), 0.0, None)
    del R
    np.fill_diagonal(D, 0.0)
    c = squareform(D, checks=False)
    Z = linkage(c, method="complete")
    m = Z.shape[0]
    certified = bool(np.all(np.diff(Z[:, 2]) >= 0))
    n_flag = 0
    if certified:
        order = np.argsort(c, kind="stable")
        cs = c[order]
        lo = np.searchsorted(cs, Z[:, 2], side="left")
        hi = np.searchsorted(cs, Z[:, 2] + tie_tol, side="right")
        del cs
        owner = np.arange(p)
        members = {i: [i] for i in range(p)}
        for t in range(m):
            a, b = int(Z[t, 0]), int(Z[t, 1])
            h = Z[t, 2]
            if hi[t] - lo[t] > 1:          # more than one original entry in [h, h + tol]: inspect each
                for kk in order[lo[t]:hi[t]]:
                    i, j = _pair_of(int(kk), p)
                    assert D[i, j] == c[kk]
                    ca, cb = int(owner[i]), int(owner[j])
                    if ca == cb or {ca, cb} == {a, b}:
                        continue
                    n_flag += 1
                    if D[np.ix_(members[ca], members[cb])].max() <= h + tie_tol:
                        certified = False
                        break
                if not certified:
                    break
            mem = members.pop(a) + members.pop(b)
            members[p + t] = mem
            owner[mem] = p + t
        del order
    del D, c
    if not certified:
        blocks = bc.partition(X, B)
        return (blocks, dict(certified=False, n_flag=n_flag, fallback=True)) if return_info else blocks
    left = np.empty(m, np.int64); right = np.empty(m, np.int64)
    size = np.empty(p + m, np.int64); size[:p] = 1
    mn = np.empty(p + m, np.int64); mn[:p] = np.arange(p)
    for t in range(m):
        a, b = int(Z[t, 0]), int(Z[t, 1])
        if mn[a] > mn[b]:
            a, b = b, a
        left[t], right[t] = a, b
        size[p + t] = size[a] + size[b]
        mn[p + t] = mn[a]

    def leaves(nd):
        out, st = [], [nd]
        while st:
            x = st.pop()
            if x < p:
                out.append(x)
            else:
                st.append(right[x - p]); st.append(left[x - p])
        return out

    clusters, stack = [], [p + m - 1]
    while stack:
        nd = stack.pop()
        if size[nd] <= B:
            clusters.append(sorted(leaves(nd)))
        else:
            stack.append(int(right[nd - p])); stack.append(int(left[nd - p]))
    blocks, cur = [], []
    for cl in clusters:
        if len(cur) + len(cl) <= B:
            cur = cur + cl
        else:
            blocks.append(sorted(cur)); cur = list(cl)
    if cur:
        blocks.append(sorted(cur))
    return (blocks, dict(certified=True, n_flag=n_flag, fallback=False)) if return_info else blocks


# ------------------------------------------------------------------------------------------------------------------
# fast local search (screened by inverse updates; decisions on exact bvs_core scores)
# ------------------------------------------------------------------------------------------------------------------
def _chol_inv(A):
    L = np.linalg.cholesky(A)
    Li = solve_triangular(L, np.eye(A.shape[0]), lower=True)
    return 2.0 * np.log(np.diag(L)).sum(), Li.T @ Li


def fast_neighbour_F(prob, S):
    """fast F for all neighbours of S. Returns dict with arrays:
       J (outside indices), add (|J|,) or None, dele (k,), swap (k, |J|) or None, FS (fast F of S)."""
    S = list(S)
    k = len(S)
    n, p, nu = prob.n, prob.p, prob.nu
    G, z, yty, lw = prob.XtX, prob.Xty, prob.yty, prob.logw
    inS = np.zeros(p, bool); inS[S] = True
    J = np.flatnonzero(~inS)
    gJ = G[J, J]
    hH = (n + 1.0) * gJ + 1.0
    hG = gJ + 1.0
    zJ = z[J]
    if k == 0:
        quad = zJ ** 2 / hH
        Fadd = lw[1] - 0.5 * (np.log(hH) - np.log(hG)) - nu * np.log(0.02 + yty - n * quad)
        return dict(J=J, add=Fadd if prob.K >= 1 else None, dele=np.empty(0), swap=None, FS=prob.logm0 + lw[0])
    Sa = np.array(S)
    GS = G[np.ix_(Sa, Sa)]
    ldH, Hi = _chol_inv((n + 1.0) * GS + np.eye(k))
    ldG, Gi = _chol_inv(GS + np.eye(k))
    zS = z[Sa]
    wz = Hi @ zS
    quadS = float(zS @ wz)
    FS = lw[k] - 0.5 * (ldH - ldG) - nu * math.log(0.02 + yty - n * quadS)
    U = G[np.ix_(Sa, J)]                       # k x m
    WH = (n + 1.0) * (Hi @ U)                  # Hi @ UH
    WG = Gi @ U
    sH = hH - (n + 1.0) * (U * WH).sum(0)
    sG = hG - (U * WG).sum(0)
    cz = zJ - WH.T @ zS
    Fadd = None
    if k < prob.K:
        qa = quadS + cz ** 2 / sH
        Fadd = lw[k + 1] - 0.5 * ((ldH + np.log(sH)) - (ldG + np.log(sG))) - nu * np.log(0.02 + yty - n * qa)
    dH = np.diag(Hi).copy(); dG = np.diag(Gi).copy()
    ldHm = ldH + np.log(dH); ldGm = ldG + np.log(dG)
    qm = quadS - wz ** 2 / dH
    Fdel = lw[k - 1] - 0.5 * (ldHm - ldGm) - nu * np.log(0.02 + yty - n * qm)
    sHs = sH[None, :] + WH ** 2 / dH[:, None]
    sGs = sG[None, :] + WG ** 2 / dG[:, None]
    czs = cz[None, :] + WH * (wz / dH)[:, None]
    qs = qm[:, None] + czs ** 2 / sHs
    Fsw = lw[k] - 0.5 * ((ldHm[:, None] + np.log(sHs)) - (ldGm[:, None] + np.log(sGs))) - nu * np.log(0.02 + yty - n * qs)
    return dict(J=J, add=Fadd, dele=Fdel, swap=Fsw, FS=FS)


def ols_h(prob, T):
    """OLS add statistic h_{T,l} = (n-1)(RSS_T - RSS_{T+l})/RSS_T for all l (nan on T) -- GROW L2.0 / LOC2 d1 proxy."""
    G, z = prob.XtX, prob.Xty
    T = np.asarray(sorted(T), dtype=np.int64)
    if len(T) == 0:
        d = np.diag(G).copy(); c = z.copy(); rss = prob.yty
    else:
        L = np.linalg.cholesky(G[np.ix_(T, T)])
        A = solve_triangular(L, G[T, :], lower=True)
        b = solve_triangular(L, z[T], lower=True)
        d = np.diag(G) - (A ** 2).sum(0)
        c = z - A.T @ b
        rss = prob.yty - float(b @ b)
    h = (prob.n - 1) * c ** 2 / np.maximum(d, 1e-300) / rss
    if len(T):
        h[T] = np.nan
    return h


def ls_loc(prob, centre, ell, window=1e-3, tmax=1e9, record_h=True, spot=64, spot_seed=0):
    """bvs_core.local_search rule with fast screening + exact re-scoring (see module doc).
    Safeguards (R01-2): (a) every neighbour with a non-finite fast score is re-scored exactly; (b) adaptive window: if the
    max |fast - exact| on the re-scored set exceeds window/100, the window is multiplied by 100 and the step is redone;
    (c) spot check: a random sample of `spot` EXCLUDED neighbours is re-scored exactly (every step if k <= 300, else every
    10th step); the max |fast - exact| on them and the number of them whose exact F >= max(F(centre), chosen F) are
    recorded (spot_err_max, spot_beats). The certificate is a SCREENED certificate (`certified`), not an exhaustive one.
    Per-step records: k, F (exact F of the centre), best_F (exact max over re-scored neighbours), best_add_F (exact max
    over re-scored adds), na_margin = F(centre) - best_add_F (negative <=> some addition strictly improves the centre),
    h_max / h_argmax (OLS add statistic), move/out/in. At the move cap the core (cpp/v3_engine.h) returns the best
    improving neighbour of the last centre without counting a move: recorded as `returned_prod` (== final otherwise)."""
    t0 = time.time()
    rng = np.random.default_rng(spot_seed)
    S = tuple(sorted(int(v) for v in centre))
    path, steps = [S], []
    moves = 0
    certified = local_limit = timed_out = False
    err_max = spot_err = 0.0
    spot_beats = 0
    n_rescored = n_window_up = 0
    returned_prod = None
    while True:
        fs = fast_neighbour_F(prob, S)
        J, k = fs["J"], len(S)
        parts = []
        if fs["add"] is not None:
            parts.append(("add", fs["add"]))
        parts.append(("del", fs["dele"]))
        if fs["swap"] is not None:
            parts.append(("swap", fs["swap"].ravel()))

        def model_of(nm, i):
            if nm == "add":
                return tuple(sorted(S + (int(J[i]),)))
            if nm == "del":
                return S[:i] + S[i + 1:]
            a, j = divmod(int(i), len(J))
            return tuple(sorted(S[:a] + S[a + 1:] + (int(J[j]),)))
        w = window
        FSx = prob.F(S)
        while True:
            fin = [v[np.isfinite(v)] for _, v in parts]
            fmax = max([float(np.max(v)) for v in fin if len(v)] or [-np.inf])
            models, fastv, sel_mask = [], [], []
            for nm, v in parts:
                m_ = (v >= fmax - w) | ~np.isfinite(v)
                sel_mask.append(m_)
                for i in np.flatnonzero(m_):
                    models.append(model_of(nm, i)); fastv.append(float(v[i]))
            add_models, add_fast = [], []
            if fs["add"] is not None and len(fs["add"]):
                av = fs["add"]
                amax = float(np.max(av[np.isfinite(av)])) if np.any(np.isfinite(av)) else -np.inf
                for i in np.flatnonzero((av >= amax - w) | ~np.isfinite(av)):
                    add_models.append(model_of("add", i)); add_fast.append(float(av[i]))
            Fex = prob.F_many(models) if models else np.empty(0)
            Fadd = prob.F_many(add_models) if add_models else np.empty(0)
            n_rescored += len(models) + len(add_models)
            fv = np.array(fastv); fa = np.array(add_fast)
            errs = [abs(FSx - fs["FS"])]
            ok = np.isfinite(fv)
            if ok.any():
                errs.append(float(np.max(np.abs(Fex[ok] - fv[ok]))))
            oka = np.isfinite(fa)
            if oka.any():
                errs.append(float(np.max(np.abs(Fadd[oka] - fa[oka]))))
            disc = max(errs)
            if disc > w / 100.0:
                w *= 100.0; n_window_up += 1
                continue
            break
        err_max = max(err_max, disc)
        mx = float(Fex.max()) if len(Fex) else -np.inf
        if spot and (k <= 300 or len(steps) % 10 == 0):
            tot = sum(len(v) for _, v in parts)
            if tot > len(models):
                picks = rng.choice(tot, size=min(spot, tot), replace=False)
                offs = np.cumsum([0] + [len(v) for _, v in parts])
                sm, sf = [], []
                for q in picks:
                    pi = int(np.searchsorted(offs, q, side="right") - 1)
                    nm, v = parts[pi]
                    i = int(q - offs[pi])
                    if sel_mask[pi][i]:
                        continue
                    sm.append(model_of(nm, i)); sf.append(float(v[i]))
                if sm:
                    Fs = prob.F_many(sm)
                    spot_err = max(spot_err, float(np.max(np.abs(Fs - np.array(sf)))))
                    spot_beats += int(np.sum(Fs >= max(mx, FSx)))
        badd = float(Fadd.max()) if len(Fadd) else None
        rec = dict(k=k, F=FSx, best_F=mx, best_add_F=badd, na_margin=(FSx - badd) if badd is not None else None,
                   fast_max=fmax, n_rescore=len(models), window=w)
        if record_h:
            h = ols_h(prob, S)
            fh = np.isfinite(h)
            rec["h_max"] = float(np.max(h[fh])) if fh.any() else None
            rec["h_argmax"] = int(np.flatnonzero(fh)[np.argmax(h[fh])]) if fh.any() else None
        if mx > FSx:
            nxt = min(models[i] for i in np.flatnonzero(Fex == mx))
            if moves >= ell:
                local_limit = True
                returned_prod = nxt
                steps.append(rec)
                break
            if time.time() - t0 > tmax:
                timed_out = True
                steps.append(rec)
                break
            ins = sorted(set(nxt) - set(S)); outs = sorted(set(S) - set(nxt))
            rec["move"] = "swap" if len(ins) == 1 and len(outs) == 1 else ("add" if len(ins) == 1 else "del")
            rec["out"] = outs; rec["in"] = ins
            steps.append(rec)
            S = nxt
            moves += 1
            path.append(S)
        else:
            certified = True
            steps.append(rec)
            break
    return dict(path=path, final=S, returned_prod=returned_prod if returned_prod is not None else S, moves=moves,
                certified=certified, local_limit=local_limit, timed_out=timed_out, steps=steps, fast_err_max=err_max,
                spot_err_max=spot_err, spot_beats=spot_beats, n_window_up=n_window_up, n_rescored=n_rescored,
                secs=time.time() - t0)
