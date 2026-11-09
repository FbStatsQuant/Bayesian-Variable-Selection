"""N5 (falsification for L4): along the exact CS path from [p] record the L4 quantities:
x_T (centre, xi-units, exact formula of L1.4; centre_err is only a 0/1 indicator that the deleted index differs from
the null closest to this formula centre -- no numerical centre comparison is made; R07 item 12), H = sqrt(2 log(2 m0 + 2)),
max |x_T|/H in the bulk (m >= m1) and in the end phase, the asymmetry |R - L|, the end-phase imbalance I = N+ - N-,
the drift identity x' = x - (xi_j - x)/(k-1+kappa), and Top+/Top- structure of the kept set.
Output N5_raw.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import json, math, sys
import numpy as np
from multiprocessing import Pool
import cs_core as cc, cs_gain as cg

def run(job):
    rho, n, p, s0, c, seed, m1 = job
    rng = np.random.default_rng(777 * seed + 5)
    th = np.zeros(p); idx = np.linspace(2, p - 3, s0).astype(int)
    th[idx] = c * np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])[np.arange(s0) % 6]
    P = cc.CS(rho, th, n, rng=rng)
    out = cg.ls0_path_gain(P)
    S0 = set(P.S0); xi = P.xi
    a_ = n * n - 1.0
    al, be = P.al, P.be
    kap = al / be                       # gamma_u = 1/(u + kappa)
    # varrho: x_T = (s_T - varrho)/(k + kappa)
    sig = 1.0
    varrho = (math.sqrt(n - 1) * rho * th.sum() / (sig * math.sqrt(1 - rho)) + math.sqrt(rho / (1 - rho)) * al * P.eta) / be
    nulls = np.array([j for j in range(p) if j not in S0]); m0 = len(nulls)
    H = math.sqrt(2 * math.log(2 * m0 + 2))
    inT = np.ones(p, bool)
    s = float(xi.sum()); k = p
    rec = dict(max_x_over_H_bulk=0.0, max_x_over_H_end=0.0, max_asym_over_H_bulk=0.0, max_absI_end=0, drift_err=0.0,
               centre_err=0.0, top_structure_ok=True, min_side_count_bulk=10 ** 9)
    for mv in out["moves"]:
        assert mv[0] == "-N"
        j = mv[1]
        x = (s - varrho) / (k + kap)
        # centre check vs z-units: c_T = gamma_k B_T, x = (c_T - kappa0)/kappa1 not available directly; check via t
        kept = nulls[inT[nulls]]
        m = len(kept)
        above = kept[xi[kept] > x]; below = kept[xi[kept] <= x]
        if m >= m1:
            rec["max_x_over_H_bulk"] = max(rec["max_x_over_H_bulk"], abs(x) / H)
            if len(above) and len(below):
                R = xi[above].min() - x; L = x - xi[below].max()
                rec["max_asym_over_H_bulk"] = max(rec["max_asym_over_H_bulk"], abs(R - L) / H)
            rec["min_side_count_bulk"] = min(rec["min_side_count_bulk"], len(above), len(below))
        else:
            rec["max_x_over_H_end"] = max(rec["max_x_over_H_end"], abs(x) / H)
            I = int((xi[kept] > 0).sum() - (xi[kept] < 0).sum())
            rec["max_absI_end"] = max(rec["max_absI_end"], abs(I))
            pos = nulls[xi[nulls] > 0]; neg = nulls[xi[nulls] < 0]
            kp = set(kept[xi[kept] > 0].tolist()); kn = set(kept[xi[kept] < 0].tolist())
            tp = set(pos[np.argsort(-xi[pos])][:len(kp)].tolist()); tn = set(neg[np.argsort(xi[neg])][:len(kn)].tolist())
            if kp != tp or kn != tn: rec["top_structure_ok"] = False
        # drift identity
        x_new = (s - xi[j] - varrho) / (k - 1 + kap)
        rec["drift_err"] = max(rec["drift_err"], abs(x_new - (x - (xi[j] - x) / (k - 1 + kap))))
        # deleted point must be the kept null closest to x
        dist = np.abs(xi[kept] - x)
        if kept[int(np.argmin(dist))] != j: rec["centre_err"] = max(rec["centre_err"], 1.0)
        inT[j] = False; s -= xi[j]; k -= 1
    return dict(rho=rho, n=n, p=p, s0=s0, c=c, seed=seed, m1=m1, H=H, final_is_S0=out["final_is_S0"], **rec)

if __name__ == "__main__":
    J = []
    for rho in [0.3, 0.95]:
        for s0 in [1, 4]:
            for (n, p) in [(10**5, 5000), (10**8, 20000), (40001, 20000)]:
                for seed in range(3):
                    J.append((rho, n, p, s0, 1.0, seed, 20))
    with Pool(6) as pool:
        for r in pool.imap_unordered(run, J):
            with open("N5_raw.jsonl", "a") as f: f.write(json.dumps(r) + "\n")
            print(json.dumps(r), flush=True)
