"""Extra cells for the global-factor boundary (rho = 0.5, psi = 0.3; rho = 0.4, psi = 0.25) at n = 200, p in
{500, 1000}; same replicate function and seeding scheme as sim_partition.py. Output: results/sim_extra.txt"""
import sys, json
from multiprocessing import Pool
from sim_partition import one, cp
from part_core import block_size

CFG = [dict(n=200, p=p, g=10, rho=rho, psi=psi, kind="global") for p in (500, 1000)
       for (rho, psi) in ((0.5, 0.3), (0.4, 0.25), (0.6, 0.3))]
if __name__ == "__main__":
    lines = ["global factor boundary, n = 200, g = 10, B = 14: fail = blocks != groups (95% CP)"]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as pool:
        for cfg in CFG:
            reps = 100
            res = pool.map(one, [(cfg, r) for r in range(reps)], chunksize=5)
            k = sum(not x["beq"] for x in res); nu = sum(not x["union"] for x in res)
            lo, hi = cp(k, reps)
            lines.append(f"p={cfg['p']} rho={cfg['rho']} psi={cfg['psi']}: fail {k}/{reps} ({lo:.2e}, {hi:.2e}); not union {nu}")
            print(lines[-1], flush=True)
    open("../results/sim_extra.txt", "w").write("\n".join(lines) + "\n")
