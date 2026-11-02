"""FS / ULR / TS gaps on LH configuration B (population, n-free; exact Gram).  W2-PREM PROOF.md §8.

For every phase-1 state W of the SH family of x = S° and every truth i in W: the losses
loss(l) = [RSS^mu(W-i+l) - RSS^mu(W)]/(n-1) over all l not in W.  Reports, for thresholds c0, the maximal number of
l with loss < c0 (the D' of FS), the minimal loss over l in N(i) (must be >= c0 for FS), and the ULR and TS minima.
Also lists the substitute types.  Output: results/lh_fs_gap.txt
"""
import numpy as np
import lh_premises as L
from bvs_score import Data

n = 1000
D = Data(L.SIG, L.TH, n, np.random.default_rng(0))
N = L.neighbour_graph(n)
fam = L.Fam("SH", N, L.Sref)
ph1 = [W for W in fam.states() if L.S0 - W]
r = lambda W: D.rss_mu(tuple(sorted(W))) / (n - 1)
out = []
for c0 in [1e-9, 0.01, 0.05, 0.1]:
    Dp, nbmin, types = 0, 1e9, set()
    for W in ph1:
        base = r(W)
        for i in W & L.S0:
            losses = {l: r((W - {i}) | {l}) - base for l in range(L.p) if l not in W}
            sub = [l for l, v in losses.items() if v < c0]
            Dp = max(Dp, len(sub))
            for l in sub:
                types.add((i, l if l in L.S0 else ("C%d" % (l // 4))))
            for l in N[i]:
                if l not in W:
                    nbmin = min(nbmin, losses[l])
    out.append(f"c0={c0}: D' = max #substitutes = {Dp}; min loss over neighbours of the removed truth = {nbmin:.4f}; "
               f"substitute types (truth, l or group) = {sorted(types, key=str)}")
    print(out[-1], flush=True)
ulr = min(r((W - {k}) | {l}) - r(W) for W in ph1 for k in (W - L.S0) & L.A_LH(L.S0 - W)
          for l in range(L.p) if l not in W and l not in L.S0 and l not in L.A_LH(L.S0 - W))
ts = min(r(W - {i}) - r(W) for W in ph1 for i in W & L.S0)
out.append(f"ULR min loss = {ulr:.4f}; TS min loss = {ts:.4f}; phase-1 states = {len(ph1)}")
print(out[-1])
open(__file__.replace("scripts/lh_fs_gap.py", "results/lh_fs_gap.txt"), "w").write("\n".join(out) + "\n")
