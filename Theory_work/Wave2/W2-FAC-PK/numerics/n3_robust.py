"""N3 (W2-FAC-PK): robustness grid of the LS0 path from the start mode, exact-Gram CS, p > K.
rho in {0.2, 0.5, 0.8, 0.95}; p/n in {0.55, 0.8, max (p = n-1)}; truth layouts: aligned (1.4,1,1.8,1.2), mixed
(1.4,-1,1.8,-1.2), s0=1 (1.0), negative total (-1.4,-1,-1.8,1.2), weak-mixed (0.3,-1,1.8,-1.2).
Records the same fields as N1 plus x_W/M_W at the end of the swap phase and whether swaps occur after the first deletion."""
import sys, json, math, time
import numpy as np
from multiprocessing import Pool
import pk_core as pk
LAY = {"aligned": (1.4, 1.0, 1.8, 1.2), "mixed": (1.4, -1.0, 1.8, -1.2), "s0=1": (1.0,), "negtot": (-1.4, -1.0, -1.8, 1.2),
       "weakmix": (0.3, -1.0, 1.8, -1.2)}
def run(args):
    rho, n, pspec, lay, seed = args
    p = n - 1 if pspec == "max" else int(round(pspec * n))
    th = np.zeros(p); co = LAY[lay]; S0 = [2, 26, 53, 75][:len(co)]; th[S0] = co
    t0 = time.time()
    P = pk.make_cs(rho, th, n, seed)
    blocks = pk.cs_partition(p, pk.block_size(n, p))
    sm = pk.start_mode_cs(P, blocks)
    rec = {}
    k1 = pk.xi_units(P)
    def cb(d):
        if "MW" not in rec and d["li"] is None:
            rec["MW"] = P.nu * n * k1 ** 2 / (P.al * d["psi"]); rec["W_at"] = d["nmoves"]
    r = pk.path_from(P, sm["mode"], callback=cb)
    summ = pk.summarize_moves(r["moves"])
    ell = pk.ell_cap(n, p)
    return dict(rho=rho, n=n, p=p, K=P.K, lay=lay, seed=seed, start=sm["size"], has_S0=set(S0) <= set(sm["mode"]),
                moves=r["n_moves"], final_is_S0=r["final_is_S0"], k_hit=r["k_hit"], cap_MR1=ell + sm["size"],
                cap_2=ell + 2 * sm["size"], MW=rec.get("MW"), t=round(time.time() - t0, 1), **summ)
if __name__ == "__main__":
    grid = []
    for n in [2000, 8000]:
        for rho in [0.2, 0.5, 0.8, 0.95]:
            for pspec in [0.55, 0.8, "max"]:
                for lay in LAY:
                    for seed in range(3):
                        grid.append((rho, n, pspec, lay, seed))
    with Pool(7) as pool, open(sys.argv[1], "w") as f:
        for res in pool.imap_unordered(run, grid, chunksize=2):
            f.write(json.dumps(res) + "\n"); f.flush()
