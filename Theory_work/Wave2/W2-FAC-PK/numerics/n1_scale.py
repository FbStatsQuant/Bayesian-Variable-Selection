"""N1 (W2-FAC-PK): scaling of the saturated start and the LS0 path, exact-Gram compound symmetry, p > K.
usage: python n1_scale.py OUT.jsonl  (grid below; multiprocessing)"""
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import pk_core as pk

def run(args):
    rho, n, frac, seed, c, s0pat = args
    p = int(round(frac * n))
    p = min(p, n - 2)
    th = np.zeros(p)
    S0 = [2, 26, 53, 75][:len(s0pat)]
    th[S0] = c * np.array(s0pat)
    t0 = time.time()
    P = pk.make_cs(rho, th, n, seed)
    B = pk.block_size(n, p)
    blocks = pk.cs_partition(p, B)
    sm = pk.start_mode_cs(P, blocks)
    t1 = time.time()
    r = pk.path_from(P, sm["mode"])
    summ = pk.summarize_moves(r["moves"])
    ell = pk.ell_cap(n, p)
    st = set(sm["mode"])
    out = dict(rho=rho, n=n, p=p, K=P.K, B=B, seed=seed, c=c, s0=len(S0), start=sm["size"], saturated=sm["size"] == P.K,
               has_S0=set(S0) <= st, size_ties=sm["n_size_ties"], within_ties=sm["within_ties"],
               moves=r["n_moves"], final_is_S0=r["final_is_S0"], k_hit=r["k_hit"], ell=ell,
               cap_MR1=ell + sm["size"], cap_2K=ell + 2 * sm["size"],
               MR1_scores=(r["k_hit"] is not None and r["k_hit"] <= ell + sm["size"]),
               excess_over_MR1=(r["k_hit"] - ell - sm["size"]) if r["k_hit"] is not None else None,
               t_start=round(t1 - t0, 1), t_path=round(time.time() - t1, 1), **summ)
    return out

if __name__ == "__main__":
    outf = sys.argv[1]
    grid = []
    for n in [600, 2000, 6000, 20000]:
        for frac in [0.6, 0.75, 0.95]:
            for seed in range(5):
                grid.append((0.5, n, frac, seed, 1.0, (1.4, 1.0, 1.8, 1.2)))
    with Pool(7) as pool, open(outf, "w") as f:
        for res in pool.imap_unordered(run, grid):
            f.write(json.dumps(res) + "\n"); f.flush()
            print(json.dumps({k: res[k] for k in ("n", "p", "seed", "start", "has_S0", "lead_swaps", "counts", "moves", "k_hit", "cap_MR1", "final_is_S0", "t_path")}), flush=True)
