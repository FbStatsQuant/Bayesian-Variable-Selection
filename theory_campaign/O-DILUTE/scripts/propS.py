"""Proposition S (ranking ceiling) on the regenerated datasets: valid for the v3 tables AND for every common plug-in s2.

For truths j alone (among S0) in their block, and truth-free blocks F: M_j = #{F-blocks holding a null l with r_ly^2 >= r_jy^2}.
Order truths by r_jy^2 descending; count >= prod_i (1 + [M_(i) - (i-1)]_+);  pi0(S0) <= 1/count.
Same seeds as run_study.py. Usage: python propS.py <reps> > ../results/propS.txt
"""
import sys
import numpy as np
import dilute as D

n = 200; B = 14

def bound(X, y, blocks, S0set):
    r2 = (X.T @ y / (n - 1)) ** 2
    U = []; Fmax = []
    for blk in blocks:
        tr = [c for c in blk if c in S0set]
        if len(tr) == 1: U.append(tr[0])
        if len(tr) == 0: Fmax.append(r2[blk].max())
    Fmax = np.array(Fmax)
    rj = sorted([r2[j] for j in U], reverse=True)
    lc = 0.0; single = 0
    for i, v in enumerate(rj):
        M = int((Fmax >= v).sum()); single += M
        lc += np.log1p(max(M - i, 0))
    return lc, np.log1p(single), len(U)

if __name__ == "__main__":
    reps = int(sys.argv[1])
    print("Prop S ceiling: log10 pi0(S0) <= -log10(count); valid for v3 and every common-s2 table")
    print("%5s %2s %4s | %10s %10s %10s | %s" % ("p", "S", "c", "med", "min", "max", "median single-swap log10 bound"))
    for p in (500, 1000):
        for s in range(1, 7):
            chol = np.linalg.cholesky(D.scenario_covariance(s, p))
            out = {1.0: [], 0.5: []}; sing = {1.0: [], 0.5: []}
            for r in range(1, reps + 1):
                seed = 20261102 + 100000 * (p == 1000) + 1000 * s + r
                X, Ys, act, beta, eps = D.gen_dataset(p, s, seed, n=n, chol=chol)
                blocks = D.make_blocks(X, B); S0set = set(act.tolist())
                for c in (1.0, 0.5):
                    y, _ = D.std_y(Ys[c]); lc, l1, u = bound(X, y, blocks, S0set)
                    out[c].append(-lc / np.log(10)); sing[c].append(-l1 / np.log(10))
            for c in (1.0, 0.5):
                a = np.array(out[c])
                print("%5d %2d %4.1f | %10.2f %10.2f %10.2f | %.2f" % (p, s, c, np.median(a), a.min(), a.max(),
                                                                     np.median(sing[c])), flush=True)
