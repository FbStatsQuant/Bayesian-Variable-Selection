"""Aggregate item 5 -> out/analysis_item5.md.   DRAFT (by this seat, unchecked)"""
import sys, pickle
sys.dont_write_bytecode = True
import numpy as np
res = pickle.load(open("out/item5.pkl", "rb"))
L = []; pr = lambda *a: L.append(" ".join(str(x) for x in a))
pr("## Item 5 — B2-core: smallest value over q-sparse u and a of [n⁻¹Σ(a+u'z_i)²]/[a²+Var(u'z)]\n")
pr("p = 200. For a fixed support the minimum over (a, u_S) is exact (smallest generalised eigenvalue). q = 2: all 19 900 supports enumerated (exact minimum). "
   "q = 4: 40 restarts of best-swap hill climbing over supports (an UPPER bound on the true minimum, so `freq < ½` is a LOWER bound). R = 200 samples per cell.\n")
pr("| q | n | law | min over samples | q0.01 | q0.1 | median of the sample minima | freq(min < ½) | freq(min < 0.6) | search |"); pr("|---|---|---|---|---|---|---|---|---|---|")
cells = {}
for r in res: cells.setdefault((r["q"], r["n"], r["law"]), []).append(r)
for k in sorted(cells):
    v = np.array([x["minratio"] for x in cells[k]])
    pr(f"| {k[0]} | {k[1]} | {k[2]} | {v.min():.3f} | {np.quantile(v,.01):.3f} | {np.quantile(v,.1):.3f} | {np.median(v):.3f} | {np.mean(v<0.5):.3f} ({(v<0.5).sum()}/{len(v)}) | {np.mean(v<0.6):.3f} | {'exact' if cells[k][0]['exact'] else 'hill-climb'} |")
nb = [x for x in res if x["q"] == 2 and x["n_below_half_supports"] > 0]
pr(f"\nq = 2: samples with at least one support below ½: {len(nb)}; for those, the number of supports below ½ (of 19 900): " + (", ".join(str(x['n_below_half_supports']) for x in nb[:20]) or "none") + ".")
open("out/analysis_item5.md", "w").write("\n".join(L)); print("\n".join(L))
