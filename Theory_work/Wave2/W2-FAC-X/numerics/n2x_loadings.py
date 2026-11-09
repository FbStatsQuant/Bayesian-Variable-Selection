"""N2X (Target 2 diagnosis): one factor, general loadings lambda_j, iid rows ('iid') and the exact reference design
('ref', W = N I, a = 0). Uncapped LS0 path from [p]. Records: pure deletion / final S0 / max add gain / ties, and the
deletion-order structure: rank of the deleted null in |xi_j - l_j X_T| / sqrt(1 - l_j^2/(kappa0 + |l_T|^2)) (the
reference statistic with variable-specific centre l_j X_T) and in |xi_j - lbar X_T| (common-centre proxy).
Usage: python n2x_loadings.py out.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import iid_core as ic

def loadings(p, kind, rng):
    if kind == "two03_09":
        return np.where(np.arange(p) % 2 == 0, 0.3, 0.9)
    if kind == "two05_095":
        return np.where(np.arange(p) % 2 == 0, 0.5, 0.95)
    if kind == "unif02_09":
        return np.random.default_rng(99 + p).uniform(0.2, 0.9, p)
    if kind == "cs07":
        return np.full(p, math.sqrt(0.7))
    raise ValueError(kind)

def run(job):
    kind, mode, n, p, seed = job
    rng = np.random.default_rng(1009 * seed + 7 * p + 11)
    lam = loadings(p, kind, rng)
    beta = np.zeros(p); idx = np.linspace(2, p - 3, 4).astype(int); beta[idx] = [1.4, -1.0, 1.8, -1.2]
    t0 = time.time()
    P = ic.IidData(lam, beta, n, rng, mode=mode)
    S0 = set(P.S0)
    ell = lam / np.sqrt(1 - lam ** 2)
    xi, eta = P.xi, float(P.eta[0])
    N = n - 3
    rec = dict(rank_var=0, rank_common=0)
    def diag(P_, st, Gd, Ga, Gs, step):
        T = st.T
        isN = np.array([int(t) not in S0 for t in T])
        if isN.sum() < 2: return
        # reference X_T with phi^2 ~ N (kappa0 = N/phi^2 ~ 1, varrho' = N eta/phi^2 ~ eta)
        lt = ell[T]
        X = (lt @ xi[T] - eta) / (lt @ lt + 1.0)
        stat = np.abs(xi[T] - lt * X) / np.sqrt(1 - lt ** 2 / (1.0 + lt @ lt))
        ib = int(np.argmax(np.where(isN, Gd, -np.inf)))
        sN = stat[isN]; bN = stat[ib]
        rec["rank_var"] = max(rec["rank_var"], int((sN < bN - 1e-12).sum()))
        lbar = lt.mean(); sc = np.abs(xi[T] - lbar * X)
        rec["rank_common"] = max(rec["rank_common"], int((sc[isN] < sc[ib] - 1e-12).sum()))
    out = ic.ls0_path(P, range(p), sorted(S0), diag_every=1, diag_fn=diag)
    mv = out["moves"]; types = {}
    for m in mv: types[m[0]] = types.get(m[0], 0) + 1
    return dict(kind=kind, mode=mode, n=n, p=p, seed=seed, moves=len(mv), types=types,
                pure_deletion=all(m[0] == "delN" for m in mv), final_is_S0=out["final_is_S0"],
                max_add_gain_over_logn=out["info"]["max_add_gain"] / math.log(n),
                max_swap_minus_del=out["info"]["max_swap_minus_del"], ties=out["info"]["ties"],
                rank_var_max=rec["rank_var"], rank_common_max=rec["rank_common"], t=round(time.time() - t0, 1))

if __name__ == "__main__":
    outf = sys.argv[1]
    J = []
    for kind in ["two03_09", "two05_095", "unif02_09", "cs07"]:
        for mode, ns in [("ref", [10 ** 5, 10 ** 8]), ("iid", [10 ** 5, 10 ** 6])]:
            for n in ns:
                for p in [100, 400]:
                    for seed in range(2):
                        J.append((kind, mode, n, p, seed))
    J.sort(key=lambda j: -j[3])
    print(len(J), "jobs", flush=True)
    with Pool(7) as pool:
        for r in pool.imap_unordered(run, J):
            with open(outf, "a") as f: f.write(json.dumps(r) + "\n")
            print(r["kind"], r["mode"], r["n"], r["p"], r["seed"], r["types"], "S0" if r["final_is_S0"] else "MISS",
                  "add/logn %.3f rank_var %d rank_common %d t %.0f" % (r["max_add_gain_over_logn"], r["rank_var_max"], r["rank_common_max"], r["t"]), flush=True)
    print("done", flush=True)
