"""N1X: iid Gaussian rows, compound-symmetric covariance (all loadings sqrt(rho)) -- uncapped LS0 path from [p].
Records: move types, final == S0, ties, NA/TL/swap margins, and the band diagnostics of the 1-D reduction:
  * hull defect: # kept nulls whose xi lies strictly inside [min, max] of the deleted nulls' xi (0 = interval hole);
  * empirical perturbation delta_hat(T) = max_j |r_j/c - (xi_j - x_hat)| over kept nulls, where r_j = u_j/sqrt(W1_jj)
    (the signed deletion statistic) and (c, x_hat) are fitted by least squares; compared with sqrt(k log p / n).
Usage: python n1x_iid_cs.py out.jsonl [quick]"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import iid_core as ic


def layout(p, s0, kind):
    th = np.zeros(p)
    idx = np.linspace(2, p - 3, s0).astype(int)
    vals = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])[np.arange(s0) % 6]
    if kind == "aligned":
        vals = np.abs(vals)
    th[idx] = vals
    return th


def run(job):
    rho, n, p, s0, kind, seed = job
    rng = np.random.default_rng(7919 * seed + 31 * p + 3)
    beta = layout(p, s0, kind)
    t0 = time.time()
    P = ic.IidData(math.sqrt(rho) * np.ones(p), beta, n, rng)
    S0 = P.S0
    S0set = set(S0)
    nulls = np.array([j for j in range(p) if j not in S0set])
    xi = P.xi
    rec = dict(dmax=0.0, dmax_ratio=0.0, dmed=[], hull_defect=0, hull_band=0.0, argmin_rank_max=0)

    def diag(P_, st, Gd, Ga, Gs, step):
        T = st.T
        isN = np.array([int(t) not in S0set for t in T])
        if isN.sum() < 4:
            return
        w1 = np.diag(st.W1)
        r = (st.u / np.sqrt(w1))[isN]
        xx = xi[T[isN]]
        A = np.c_[xx, np.ones_like(xx)]
        coef, *_ = np.linalg.lstsq(A, r, rcond=None)
        c, b = coef
        xhat = -b / c
        res = r / c - (xx - xhat)
        dm = float(np.max(np.abs(res)))
        k = len(T)
        ref = math.sqrt(k * math.log(p) / n)
        rec["dmax"] = max(rec["dmax"], dm)
        rec["dmax_ratio"] = max(rec["dmax_ratio"], dm / ref)
        # rank (in |xi - xhat|) of the null with the best deletion gain
        Gn = Gd[isN]
        ib = int(np.argmax(Gn))
        dist = np.abs(xx - xhat)
        rank = int((dist < dist[ib]).sum())
        rec["argmin_rank_max"] = max(rec["argmin_rank_max"], rank)

    out = ic.ls0_path(P, range(p), S0, diag_every=max(1, p // 60), diag_fn=diag)
    mv = out["moves"]
    # hull defect along the deletion order
    deleted = []
    kept = np.ones(p, bool)
    maxdef, maxband = 0, 0.0
    for m in mv:
        if m[0] == "delN":
            kept[m[1]] = False
            deleted.append(xi[m[1]])
            lo, hi = min(deleted), max(deleted)
            kn = np.array([j for j in nulls if kept[j]]) if len(deleted) % max(1, p // 200) == 0 else None
            if kn is not None and len(kn):
                inside = (xi[kn] > lo) & (xi[kn] < hi)
                d = int(inside.sum())
                if d > maxdef:
                    maxdef = d
                if d:
                    band = float(np.max(np.minimum(xi[kn][inside] - lo, hi - xi[kn][inside])))
                    maxband = max(maxband, band)
    types = {}
    for m in mv:
        types[m[0]] = types.get(m[0], 0) + 1
    cap = ic.ell_cap(n, p) + p
    return dict(rho=rho, n=n, p=p, A=round(math.log(p) / math.log(n), 3), s0=s0, kind=kind, seed=seed,
                moves=len(mv), types=types, final_is_S0=out["final_is_S0"], within_cap=len(mv) <= cap,
                pure_deletion=all(m[0] == "delN" for m in mv),
                max_add_gain_over_logn=out["info"]["max_add_gain"] / math.log(n),
                max_truth_move=out["info"]["max_truth_move"], max_swap_minus_del=out["info"]["max_swap_minus_del"],
                min_del_gain=out["info"]["min_del_gain"], ties=out["info"]["ties"],
                delta_hat_max=rec["dmax"], delta_hat_over_sqrt_klogp_n=rec["dmax_ratio"],
                argmin_rank_max=rec["argmin_rank_max"], hull_defect_max=maxdef, hull_band_max=maxband,
                t=round(time.time() - t0, 1))


if __name__ == "__main__":
    outf = sys.argv[1]
    quick = len(sys.argv) > 2
    J = []
    for rho in [0.3, 0.7]:
        for n in [10 ** 4, 10 ** 5, 10 ** 6]:
            ps = sorted(set([int(round(n ** a)) for a in (0.3, 0.45, 0.6)] + [min(1000, n // 2), min(1000, n // 8)]))
            ps = [q for q in ps if 10 <= q <= 1000]
            for p in ps:
                for s0, kind in [(4, "mixed"), (4, "aligned"), (1, "mixed")]:
                    for seed in range(1 if quick else 2):
                        J.append((rho, n, p, s0, kind, seed))
    done = set()
    if os.path.exists(outf):
        for line in open(outf):
            r = json.loads(line); done.add((r["rho"], r["n"], r["p"], r["s0"], r["kind"], r["seed"]))
    # the path from [p] does not depend on beta given (xi, W): 'aligned' duplicates 'mixed' (same seed) -> drop it
    J = [j for j in J if j not in done and j[4] != "aligned"]
    J.sort(key=lambda j: -j[2])
    print(len(J), "jobs", flush=True)
    with Pool(7) as pool:
        for r in pool.imap_unordered(run, J):
            with open(outf, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(r["rho"], r["n"], r["p"], r["s0"], r["kind"], r["seed"], "moves", r["moves"], r["types"],
                  "S0" if r["final_is_S0"] else "MISS", "dhat %.3f ratio %.2f defect %d band %.3f rank %d t %.0f" % (
                      r["delta_hat_max"], r["delta_hat_over_sqrt_klogp_n"], r["hull_defect_max"], r["hull_band_max"],
                      r["argmin_rank_max"], r["t"]), flush=True)
    print("done", flush=True)
