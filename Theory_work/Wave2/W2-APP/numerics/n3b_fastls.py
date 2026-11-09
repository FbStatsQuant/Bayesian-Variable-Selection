r"""NOTE (lead, council r2): this is a SCREENED search; "EXACT" below refers only to rescoring of retained candidates,
not to completeness of the screening; its certified flag is not a complete-scan certificate (see LEAD_READING.md).
n3b_fastls.py -- re-run of the n3 data sets whose LS0 hit the 600 s guard in n3_visible_null.py
(V2 n=12800 [p=400 and p=200,s0=2], V3a n=3200 and 12800).
Same data/seeds/partition/start mode as n3 (build_data tag=4, same pipeline), but LS0 uses ls_fast: same search rule as bc.local_search
(neighbours = adds, deletes, swaps; best neighbour; ties -> lexicographically smallest; cap ell_cap(n,p)+|start|),
with swap-neighbourhood scores pre-screened by bordered-Cholesky (Schur complement) updates instead of k*p separate factorisations.
The decision uses EXACT bc scores: all adds/deletes and every swap whose fast score is within 1e-5 of the fast max are re-scored by prob.F_many.
Validated against bc.local_search (same path) in n3b_validate_out.txt."""
import sys, os, time, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n0_common import *
from n3_visible_null import visible_set
from multiprocessing import Pool
from scipy.linalg import solve_triangular

HERE = os.path.dirname(os.path.abspath(__file__))


def fast_swap_F(prob, S):
    """(J, F) with F[a, jj] = fast F of S minus S[a] plus J[jj], J = indices not in S"""
    S = list(S)
    k = len(S)
    p, n, nu = prob.p, prob.n, prob.nu
    G = prob.XtX
    z = prob.Xty
    inS = np.zeros(p, bool)
    inS[S] = True
    J = np.flatnonzero(~inS)
    out = np.empty((k, len(J)))
    Gjj = G[J, J]
    for a in range(k):
        b = np.array(S[:a] + S[a + 1:], dtype=np.int64)
        m = len(b)
        if m == 0:
            sH = (n + 1.0) * Gjj + 1.0
            sG = Gjj + 1.0
            q = z[J] ** 2 / sH
            ld = np.log(sH) - np.log(sG)
        else:
            Gb = G[np.ix_(b, b)]
            Hb = (n + 1.0) * Gb + np.eye(m)
            GIb = Gb + np.eye(m)
            LH = np.linalg.cholesky(Hb)
            LG = np.linalg.cholesky(GIb)
            ldH = 2.0 * np.log(np.diag(LH)).sum()
            ldG = 2.0 * np.log(np.diag(LG)).sum()
            gj = G[np.ix_(b, J)]
            VH = solve_triangular(LH, (n + 1.0) * gj, lower=True)
            VG = solve_triangular(LG, gj, lower=True)
            sH = (n + 1.0) * Gjj + 1.0 - (VH ** 2).sum(axis=0)
            sG = Gjj + 1.0 - (VG ** 2).sum(axis=0)
            uz = solve_triangular(LH, z[b], lower=True)
            q0 = float(uz @ uz)
            hw = VH.T @ uz
            q = q0 + (z[J] - hw) ** 2 / sH
            ld = (ldH + np.log(sH)) - (ldG + np.log(sG))
        Qv = prob.yty - n * q
        out[a] = -0.5 * ld - nu * np.log(0.02 + Qv)
    out += prob.logw[k]
    return J, out


def ls_fast(prob, centre, ell, tmax=1500.0, window=1e-5):
    t0 = time.time()
    S = tuple(sorted(centre))
    prob.F(S)
    scored = {S}
    path = [S]
    moves = 0
    certified = local_limit = timed_out = False
    p, K = prob.p, prob.K
    while True:
        k = len(S)
        Sset = set(S)
        out = [j for j in range(p) if j not in Sset]
        nb = []
        if k < K:
            for j in out:
                nb.append(tuple(sorted(S + (j,))))
        for i in range(k):
            nb.append(S[:i] + S[i + 1:])
        Fv = np.array(prob.F_many(nb)) if nb else np.array([])
        if k >= 1 and len(out) >= 1:
            J, fs = fast_swap_F(prob, S)
            m0 = Fv.max() if len(Fv) else -np.inf
            thr = max(m0, fs.max()) - window
            ii, jj = np.nonzero(fs >= thr)
            sw = [tuple(sorted(S[:i] + S[i + 1:] + (int(J[j]),))) for i, j in zip(ii, jj)]
            Fs = prob.F_many(sw)
            nb = nb + sw
            Fv = np.concatenate([Fv, Fs])
        FS = prob.F(S)
        mx = float(Fv.max()) if len(nb) else bc.NEG
        scored.update(nb)
        if mx > FS:
            if moves >= ell:
                local_limit = True
                break
            if time.time() - t0 > tmax:
                timed_out = True
                break
            cands = [nb[i] for i in np.flatnonzero(Fv == mx)]
            S = min(cands)
            moves += 1
            path.append(S)
        else:
            certified = True
            break
    return dict(path=path, final=S, scored=scored, moves=moves, certified=certified, local_limit=local_limit, timed_out=timed_out)


def job(args):
    did, n, p, seed, s0 = args
    t0 = time.time()
    D = build_data(did, n, p, seed, s0=s0, tag=4)
    X, y, S0 = D["X"], D["y"], D["S0"]
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    mode = tuple(info.mode)
    ell = bc.ell_cap(n, p) + len(mode)
    t1 = time.time()
    res = ls_fast(prob, mode, ell, tmax=1500.0)
    extras = sorted(set(mode) - set(S0))
    vis = visible_set(did, n, p, S0)
    bound = min(prob.K - len(S0), len(vis) - 16 * len(S0))
    return dict(design=did, n=n, p=p, seed=seed, s0=len(S0), mode_size=len(mode), n_extra=len(extras), n_visible=len(vis),
                n_visible_in_mode=len(vis & set(mode)), lemma_bound=bound, ell=ell, ls_moves=res["moves"],
                ls_certified=res["certified"], ls_limit=res["local_limit"], ls_timed_out=res["timed_out"],
                ls_S0_scored=(S0 in res["scored"]), ls_S0_on_path=(S0 in res["path"]), ls_final_eq_S0=(res["final"] == S0),
                ls_final_size=len(res["final"]), ls_final_symdiff=len(set(res["final"]) ^ set(S0)),
                t_ls=round(time.time() - t1, 1), secs=round(time.time() - t0, 1))


def validate():
    lines = []
    for (did, n, p, seed, s0) in [("V2", 3200, 200, 1, 3), ("V3a", 800, 200, 4, 3), ("L3", 800, 200, 2, 3)]:
        D = build_data(did, n, p, seed, s0=s0, tag=4)
        prob = bc.Problem(D["X"], D["y"])
        blocks = bc.partition(D["X"])
        info = bc.start_mode(prob, blocks)
        mode = tuple(info.mode)
        ell = bc.ell_cap(n, p) + len(mode)
        J, fs = fast_swap_F(prob, mode)
        sw = [tuple(sorted(mode[:i] + mode[i + 1:] + (int(J[jj]),))) for i in range(len(mode)) for jj in range(len(J))]
        ex = prob.F_many(sw).reshape(len(mode), len(J))
        err = float(np.abs(ex - fs).max())
        t = time.time(); r1 = bc.local_search(prob, mode, ell); t1 = time.time() - t
        prob2 = bc.Problem(D["X"], D["y"])
        t = time.time(); r2 = ls_fast(prob2, mode, ell); t2 = time.time() - t
        lines.append("%s n=%d p=%d seed=%d |start|=%d: max|fastF-exactF| over swaps=%.2e; path_equal=%s moves %d/%d certified %s/%s final_equal=%s time bc=%.1fs fast=%.1fs" % (
            did, n, p, seed, len(mode), err, r1["path"] == r2["path"], r1["moves"], r2["moves"], r1["certified"], r2["certified"], r1["final"] == r2["final"], t1, t2))
        print(lines[-1], flush=True)
    return lines


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        validate()
        sys.exit()
    t00 = time.time()
    old = list(csv.DictReader(open(os.path.join(HERE, "n3_results.csv"))))
    jobs = [(r["design"], int(r["n"]), int(r["p"]), int(r["seed"]), int(r["s0"])) for r in old if r["ls_timed_out"] == "True"]
    print("jobs", len(jobs), flush=True)
    with Pool(7) as pool:
        out = []
        for r in pool.imap_unordered(job, jobs):
            out.append(r)
            print(r["design"], r["n"], r["p"], r["seed"], "mode", r["mode_size"], "LS: S0scored", r["ls_S0_scored"], "final==S0", r["ls_final_eq_S0"],
                  "cert", r["ls_certified"], "lim", r["ls_limit"], "TO", r["ls_timed_out"], "moves", r["ls_moves"],
                  "finalsize", r["ls_final_size"], "secs", r["secs"], flush=True)
    out.sort(key=lambda r: (r["design"], r["n"], r["p"], r["seed"]))
    with open(os.path.join(HERE, "n3b_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print("total secs", round(time.time() - t00, 1))
