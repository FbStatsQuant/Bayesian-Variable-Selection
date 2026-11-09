r"""loc_run.py -- one W2-SIM/LOC component-port run (Q1 Toeplitz / long memory, Q2 growing one-factor groups).

Usage: python3 loc_run.py OUT_JSON fam par place n prule seed [tmax_ls]
  fam   PT (gamma(h) = (1+h)^-alpha, par = alpha) | AF (ARFIMA(0,d,0), par = d) | CSG (par = "b,rho": block-diagonal
        compound-symmetry groups of size g = ceil(n^b), all groups the same size)
  place spread | adj (PT/AF: truths at round(p*{.15,.5,.85}) or p//2 + {-1,0,1}; theta = (1,-.8,1.2))
        CSG: one (3 truths, 3 groups, theta (1,-.8,1.2)) | one4 (4 truths, 4 groups, theta (1,.8,1.2,1)) |
             two (4 truths, 2 per group, theta (1,.8 | 1.2,1)) | twoM (masking stress: (1,-.8 | 1.2,1))
  prule q (p = n/4) | s (p = round(n^0.6)) ; CSG uses p = g * floor((n/4)/g)
Pipeline (method objects = W2-FAC-B bvs_core, unchanged): raw rows iid N(0, Sigma); X = standardize_X; y = make_y_std
(X theta + eps, sigma = 1); Problem(X, y); blocks = fast_partition (validated == bc.partition); bc.block_tables +
bc.start_mode (block DP, tie rule); LS0 = ls_loc (bc.local_search rule; screened, exact decisions) from the start mode with
cap ell_cap(n, p) + |start mode| (shipped MR1 cap).
Seed: SeedSequence([20261109, famcode, round(1000*par...), placecode, n, p, seed]) -- distinct across cells and seeds.
"""
import sys, os, json, time, math, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loc_core as lc
from loc_core import bc, np

FAMC = {"PT": 1, "AF": 2, "CSG": 3}
PLC = {"spread": 1, "adj": 2, "one": 3, "two": 4, "one4": 5, "twoM": 6}


def parse_par(fam, s):
    if fam == "CSG":
        b, rho = s.split(",")
        return (float(b), float(rho))
    return float(s)


def seed_seq(fam, par, place, n, p, seed):
    pv = [int(round(1000 * x)) for x in (par if isinstance(par, tuple) else (par,))]
    return np.random.SeedSequence([lc.BASE_SEED, FAMC[fam]] + pv + [PLC[place], n, p, seed])


def run(fam, par, place, n, prule, seed, tmax_ls=1e9, return_data=False):
    T0 = time.time()
    p = lc.p_of(prule, n)
    spec = lc.design_spec(fam, par, place, n, p)
    if spec["kind"] == "csg":
        p = spec["p"]
    S0 = tuple(spec["S0"])
    ss = seed_seq(fam, par, place, n, p, seed)
    rng = np.random.default_rng(ss)
    Xr = lc.gen_raw(spec, n, p, rng)
    X = bc.standardize_X(Xr); del Xr
    theta = np.zeros(p); theta[list(S0)] = spec["theta"]
    y = bc.make_y_std(X, theta, 1.0, rng)
    t_data = time.time() - T0
    if return_data:
        return X, y, S0, theta, spec, p
    exp = os.environ.get("LOC_EXPORT")
    if exp:      # the exact bytes used here are handed to the production fit (loc_prod_fit.R, design = file)
        X.T.astype("<f8").tofile(exp + ".X.bin")       # column-major n x p
        y.astype("<f8").tofile(exp + ".y.bin")
        with open(exp + ".json", "w") as f:
            json.dump(dict(S0_1based=[j + 1 for j in S0], beta=list(spec["theta"]), n=n, p=p, fam=fam, place=place,
                           par=list(par) if isinstance(par, tuple) else par, seed=seed,
                           X_sha256=hashlib.sha256(X.T.astype("<f8").tobytes()).hexdigest(),
                           y_sha256=hashlib.sha256(y.astype("<f8").tobytes()).hexdigest()), f)
    prob = bc.Problem(X, y)
    t1 = time.time()
    blocks, pinfo = lc.fast_partition(X, return_info=True)
    t_part = time.time() - t1
    del X
    t1 = time.time()
    info = bc.start_mode(prob, blocks)
    t_start = time.time() - t1
    mode = tuple(int(v) for v in info.mode)
    ell = bc.ell_cap(n, p)
    cap = ell + len(mode)
    res = lc.ls_loc(prob, mode, cap, tmax=tmax_ls, spot_seed=int(ss.generate_state(1)[0]))
    # ---------------- statistics (definitions in DESIGN.md v2 §2) ----------------
    S0s = set(S0)
    extras = sorted(set(mode) - S0s)
    missing = sorted(S0s - set(mode))
    bid = info.bid
    steps = res["steps"]
    path = res["path"]
    mv = [s.get("move") for s in steps if s.get("move")]
    deleted = [o for s in steps if s.get("move") for o in s["out"]]
    added = [i for s in steps if s.get("move") for i in s["in"]]
    final = res["final"]
    FS0 = prob.F(S0)
    deletions_only = all(m == "del" for m in mv)
    pure_deletion_to_S0 = (not missing and deletions_only and final == S0 and set(deleted) == set(extras)
                           and len(deleted) == len(extras))
    truths_deleted = sorted(set(deleted) & S0s)
    # per-truth-group / locality diagnostics
    if spec["kind"] == "csg":
        g = spec["g"]
        tg = sorted(set(j // g for j in S0))
        extra_in_truth_group = [l // g in set(tg) for l in extras]
        grp_diag = []
        for G_ in tg:
            mem = set(range(G_ * g, (G_ + 1) * g))
            bl = sorted(set(int(bid[l]) for l in mem))
            grp_diag.append(dict(group=G_, n_truths=sum(1 for j in S0 if j // g == G_), n_blocks_intersecting=len(bl),
                                 n_blocks_contained=sum(1 for b in bl if set(blocks[b]) <= mem),
                                 n_mode_in_group=sum(1 for l in mode if l in mem),
                                 n_extra_in_group=sum(1 for l in extras if l in mem)))
        dmeas = None
        extras_in_truth_groups = int(sum(extra_in_truth_group))
        extras_outside_truth_groups = len(extras) - extras_in_truth_groups
    else:
        grp_diag = None
        dmeas = [int(min(abs(l - j) for j in S0)) for l in extras]
        extras_in_truth_groups = extras_outside_truth_groups = None
    # NA diagnostics: F(T) - max_l F(T + l) at every scanned centre T (exact on the re-scored add set)
    na = [(s["na_margin"], set(S0) <= set(T)) for s, T in zip(steps, path) if s["na_margin"] is not None]
    na_sup = [m for m, sup in na if sup]
    first_S0 = next((i for i, T in enumerate(path) if T == S0), None)
    na_at_S0 = steps[first_S0]["na_margin"] if first_S0 is not None and first_S0 < len(steps) else None
    probS0 = prob.F_many([tuple(sorted(S0 + (l,))) for l in range(p) if l not in S0s]) if p <= 20000 else None
    na_at_S0_exact_all = float(FS0 - probS0.max()) if probS0 is not None else None    # exhaustive over all adds at S0
    hs = [s["h_max"] for s, T in zip(steps, path) if set(S0) <= set(T) and s.get("h_max") is not None]
    hS0 = lc.ols_h(prob, S0)
    out = dict(
        fam=fam, par=list(par) if isinstance(par, tuple) else par, place=place, n=n, prule=prule, p=p, seed=seed,
        alpha=spec["alpha"], g=spec.get("g"), G=spec.get("G"), rho=spec.get("rho"),
        S0=list(S0), theta=list(spec["theta"]),
        seed_key=[lc.BASE_SEED, FAMC[fam]] + [int(round(1000 * x)) for x in (par if isinstance(par, tuple) else (par,))] + [PLC[place], n, p, seed],
        B=bc.block_size(n, p), n_blocks=len(blocks), partition_certified=pinfo["certified"],
        partition_fallback=pinfo["fallback"], partition_n_flag=pinfo["n_flag"],
        truth_blocks=sorted(set(int(bid[j]) for j in S0)), truth_group_diag=grp_diag,
        mode=list(mode), mode_size=len(mode), S0_in_mode=not missing, missing=missing, n_extra=len(extras),
        extras=extras, extra_dist=dmeas, extra_dmax=max(dmeas) if dmeas else (0 if dmeas is not None else None),
        extras_in_truth_groups=extras_in_truth_groups, extras_outside_truth_groups=extras_outside_truth_groups,
        n_optimal=info.n_optimal, truncated=bool(info.truncated),
        ell=ell, cap=cap, ls_moves=res["moves"], ls_certified_screened=res["certified"], ls_local_limit=res["local_limit"],
        ls_timed_out=res["timed_out"], n_del=mv.count("del"), n_add=mv.count("add"), n_swap=mv.count("swap"),
        deletions_only=deletions_only, pure_deletion_to_S0=pure_deletion_to_S0, truths_deleted=truths_deleted,
        added=added, path_supersets_S0=all(set(S0) <= set(T) for T in path),
        final=list(final), final_eq_S0=(final == S0), returned_prod=list(res["returned_prod"]),
        returned_prod_eq_S0=(tuple(res["returned_prod"]) == S0), final_size=len(final), final_symdiff=len(set(final) ^ S0s),
        F_final_minus_F_S0=float(prob.F(final) - FS0), first_S0_step=first_S0,
        na_margin_final=steps[-1]["na_margin"], na_margin_at_S0=na_at_S0, na_at_S0_exhaustive=na_at_S0_exact_all,
        na_margin_min_supersets=min(na_sup) if na_sup else None, n_na_violations_supersets=sum(1 for m in na_sup if m < 0),
        na_margin_min_all=min(m for m, _ in na) if na else None,
        h_max_path_supersets=max(hs) if hs else None, h_max_S0=float(np.nanmax(hS0)),
        h_argmax_S0=int(np.nanargmax(hS0)),
        two_log_p=2 * math.log(p), cn_prime_S0=math.log(n + 1) + 2 * math.log(p) - 2 * math.log(len(mode) + 1),
        fast_err_max=res["fast_err_max"], spot_err_max=res["spot_err_max"], spot_beats=res["spot_beats"],
        n_window_up=res["n_window_up"], n_rescored=res["n_rescored"],
        t_data=round(t_data, 2), t_part=round(t_part, 2), t_start=round(t_start, 2), t_ls=round(res["secs"], 2),
        t_total=round(time.time() - T0, 2), bc_path=lc.BC_PATH,
        bc_sha256=hashlib.sha256(open(lc.BC_PATH, "rb").read()).hexdigest(),
        moves=[(s.get("move"), s.get("out"), s.get("in")) for s in steps if s.get("move")],
        step_k=[s["k"] for s in steps], step_hmax=[s.get("h_max") for s in steps],
        step_na=[s["na_margin"] for s in steps], step_window=[s["window"] for s in steps],
    )
    out.update(lc.pop_visibility(spec, n, p))
    return out

if __name__ == "__main__":
    a = sys.argv[1:]
    outp, fam, par, place, n, prule, seed = a[0], a[1], parse_par(a[1], a[2]), a[3], int(a[4]), a[5], int(a[6])
    tmax = float(a[7]) if len(a) > 7 else 1e9
    r = run(fam, par, place, n, prule, seed, tmax_ls=tmax)
    os.makedirs(os.path.dirname(os.path.abspath(outp)), exist_ok=True)
    with open(outp, "w") as f:
        json.dump(r, f, default=float)
        f.write("\n")
    print(json.dumps({k: r[k] for k in ("fam", "par", "place", "n", "p", "seed", "mode_size", "n_extra", "S0_in_mode",
                                         "ls_moves", "cap", "pure_deletion_to_S0", "final_eq_S0", "ls_certified_screened", "t_total")}, default=float))
