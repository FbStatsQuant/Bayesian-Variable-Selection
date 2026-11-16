"""Aggregate item 4 -> out/analysis_item4.md.   DRAFT (by this seat, unchecked)"""
import sys, pickle, math
sys.dont_write_bytecode = True
import numpy as np
res = pickle.load(open("out/item4.pkl", "rb"))
L = []; pr = lambda *a: L.append(" ".join(str(x) for x in a))
pr("## Item 4 — Lemma T: search for sup of E_x min{1,(a+u'x)²/c} − 2·(sample mean), p_raw = 50\n")
pr("`best` = largest value found over the restarts of a data set (a LOWER bound on the supremum, which is ≥ 0 trivially via u = 0, a = 0). η² = η²_n(d, 0.05) of STATEMENT §3. "
   "`max best` is the maximum over the data sets of that cell; `#sets best > η²` counts data sets in which the lemma (probability ≥ 0.95) would be violated.\n")
pr("| n | d | law | #sets | median best | max best | η²_n(d,0.05) | max best / η² | #sets best > η² | #sets best > 0.001 |"); pr("|---|---|---|---|---|---|---|---|---|---|")
cells = {}
for r in res: cells.setdefault((r["n"], r["d"], r["law"]), []).append(r)
tot_viol = 0; worst = (0, None)
for (n, d, law) in sorted(cells, key=lambda k: (k[0], k[1], ["gauss", "t2.1", "atom"].index(k[2]))):
    rs = cells[(n, d, law)]; b = np.array([x["best"] for x in rs]); e = rs[0]["eta2"]
    viol = int((b > e).sum()); tot_viol += viol
    if b.max() / e > worst[0]: worst = (b.max() / e, (n, d, law))
    pr(f"| {n} | {d} | {law} | {len(rs)} | {np.median(b):.4f} | {b.max():.4f} | {e:.3f} | {b.max()/e:.3f} | {viol} | {(b>0.001).sum()} |")
pr(f"\nTotal data sets {len(res)}; violations of the lemma (best > η²): {tot_viol}.  Largest ratio best/η² = {worst[0]:.3f} at (n, d, law) = {worst[1]}.")
pr("\nReference scale: for n = 100, η²_n(d, 0.05) > 1 for every d ≥ 1 (the lemma is vacuous since the left side is ≤ 1); for n = 1000, η² = " + ", ".join(f"d={d}: {cells[(1000,d,'gauss')][0]['eta2']:.3f}" for d in (1,2,3)) + ".")
open("out/analysis_item4.md", "w").write("\n".join(L)); print("\n".join(L))
