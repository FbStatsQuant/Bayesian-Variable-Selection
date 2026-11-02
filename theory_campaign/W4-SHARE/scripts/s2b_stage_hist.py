"""W4-SHARE s2b: stage at which S0 is first scored in E1d (n=4000, c=0.5) and E1c, 40 islands each, N=2500.
Also the fraction of islands with log(Zhat/Z) < log(1/2) in PB designs is reported by s3.  Seed 20261103."""
import sys; sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
import numpy as np
from collections import Counter
import s2_bvs_masked as S
from bvs_core import BVS, suff_stats
out = []
for lab, n, c in [("E1c", 4000, 0.3), ("E1d", 4000, 0.5)]:
    R = S.design_R(); th = np.zeros(16); th[[0, 4, 8]] = c * np.array([-0.45, 1.0, 0.7])
    z, yy = suff_stats(R, th, 1.0, n, np.random.default_rng(7))
    m = BVS(R, z, yy, n, [0, 4, 8]); grid, _, _ = m.method_grid()
    rng = np.random.default_rng(20261103)
    C = Counter(m.island(2500, grid, rng)["first_S0"][0] for _ in range(40))
    s = f"{lab}: T={len(grid)-1}; grid phi at stages 1..8: {np.round(grid[1:9],3)}; first-S0 stage counts: {sorted(C.items())}"
    print(s); out.append(s)
open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
