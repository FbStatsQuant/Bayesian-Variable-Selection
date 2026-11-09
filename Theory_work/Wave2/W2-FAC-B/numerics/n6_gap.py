"""N6 (R02 item 4): direct test of the extended-gap invariant (C2)(iii) and of (C2)(i)-(ii) along exact CS paths
started at S* = [p] minus N0, including truth-complete-block cases (N0 nonempty, kept eligible for additions/swaps).
At every pre-move set T (including T_0 and one/two-extra states) checks:
  a_T < x_T < b_T (extended endpoints), deleted nulls == {j in N* : a_T < xi_j < b_T}, move = deletion of a null.
Output N6_raw.jsonl"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import json, math
import numpy as np
from multiprocessing import Pool
import cs_core as cc, cs_gain as cg

def run(job):
    rho, n, p, s0, c, seed, layout = job
    rng = np.random.default_rng(31 * seed + 7)
    th = np.zeros(p)
    vals = c * np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])[np.arange(s0) % 6]
    if layout == "oneblock":            # truths 0..s0-1 share a 16-block {0..15}: N0 = {s0..15}
        S0 = list(range(s0)); N0 = list(range(s0, 16))
    else:
        S0 = list(np.linspace(2, p - 3, s0).astype(int)); N0 = []
    th[S0] = vals
    P = cc.CS(rho, th, n, rng=rng)
    Sstar = [j for j in range(p) if j not in set(N0)]
    out = cg.ls0_path_gain(P, start=Sstar)
    xi = P.xi; al, be = P.al, P.be; kap = al / be
    varrho = (math.sqrt(n - 1) * rho * th.sum() / math.sqrt(1 - rho) + math.sqrt(rho / (1 - rho)) * al * P.eta) / be
    Nstar = np.array([j for j in Sstar if j not in set(S0)])
    inT = np.zeros(p, bool); inT[Sstar] = True
    ok_gap = ok_centre = ok_move = True; checked = 0; one_two = 0
    for mv in out["moves"] + [None]:
        T = np.flatnonzero(inT); k = len(T)
        x = (xi[T].sum() - varrho) / (k + kap)
        kept = Nstar[inT[Nstar]]; deleted = Nstar[~inT[Nstar]]
        below = xi[kept][xi[kept] <= x]; above = xi[kept][xi[kept] > x]
        a = below.max() if len(below) else -np.inf; b = above.min() if len(above) else np.inf
        if not (a < x < b): ok_centre = False
        gap = set(Nstar[(xi[Nstar] > a) & (xi[Nstar] < b)].tolist())
        if gap != set(deleted.tolist()): ok_gap = False
        checked += 1
        if len(kept) in (1, 2): one_two += 1
        if mv is None: break
        if mv[0] != "-N": ok_move = False; break
        j = mv[1]
        if j not in (set(kept[xi[kept] == a].tolist()) | set(kept[xi[kept] == b].tolist())): ok_gap = False
        inT[j] = False
    inf = out["info"]
    return dict(rho=rho, n=n, p=p, s0=s0, c=c, seed=seed, layout=layout, N0=len(N0), moves=len(out["moves"]),
                m0=len(Nstar), final_is_S0=out["final_is_S0"], gap_invariant=ok_gap, centre_in_gap=ok_centre,
                pure_null_deletion=ok_move, sets_checked=checked, one_two_extra_sets=one_two, ties=inf["ties"],
                max_add_gain_over_logn=inf["max_add_gain_over_logn"], max_swap_gain=inf.get("max_swap_gain"),
                max_swap_minus_del=inf["max_swap_minus_del"], max_truth_move=inf["max_truth_move"])

if __name__ == "__main__":
    J = []
    for rho in [0.3, 0.9]:
        for (s0, layout) in [(1, "oneblock"), (3, "oneblock"), (4, "spread"), (1, "spread")]:
            for (n, p) in [(10**5, 2000), (10**7, 3000), (20001, 10000)]:
                for seed in range(3):
                    J.append((rho, n, p, s0, 1.0, seed, layout))
    with Pool(6) as pool:
        for r in pool.imap_unordered(run, J):
            with open("N6_raw.jsonl", "a") as f: f.write(json.dumps(r) + "\n")
    R = [json.loads(l) for l in open("N6_raw.jsonl")]
    bad = [r for r in R if not (r["gap_invariant"] and r["centre_in_gap"] and r["pure_null_deletion"] and r["final_is_S0"])]
    print(len(R), "runs; violations", len(bad)); [print(b) for b in bad]
