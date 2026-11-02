"""Sanity checks of vm_core against brute force / scipy (seed 5001). Output: results/sanity.txt"""
import math, itertools, sys
import numpy as np
from scipy.special import logsumexp
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from vm_core import *

rng = np.random.default_rng(5001)
out = []
# 1. add_scan vs direct
n, p = 60, 12
Xr = rng.standard_normal((n, p)); Xr[:, 1] += 0.8 * Xr[:, 0]
yr = Xr[:, 0] - 0.5 * Xr[:, 3] + rng.standard_normal(n)
X, y = standardise(Xr, yr); sc = Scorer(X, y)
err = 0
for T in [[], [0], [0, 3], [1, 4, 7]]:
    a = sc.add_scan(T)
    for l in range(p):
        if l in T: continue
        err = max(err, abs(a[l] - sc.logBF(T + [l])))
out.append(f"add_scan vs direct logBF: max abs err = {err:.2e}")
# 2. start law vs brute force (p = 12, K = 6)
blocks = [[0, 1, 2], [3, 4], [5, 6, 7, 8], [9, 10, 11]]
st = StartLaw(sc, blocks)
lg = {}
for k in range(sc.K + 1):
    for S in itertools.combinations(range(p), k):
        v = sc.logw[k]
        for blk in blocks:
            U = [j for j in S if j in blk]
            v += sc.logBF(U)
        lg[S] = v
Zb = logsumexp(list(lg.values()))
e1 = max(abs((lg[S] - Zb) - st.log_pi0(list(S))) for S in lg)
modeb = max(lg, key=lg.get)
out.append(f"pi0 convolution vs enumeration: max abs err log pi0 = {e1:.2e}; mode brute {list(modeb)} vs DP {st.mode()}")
q, e, lb = st.t22([0, 3])
out.append(f"T22(i) bound check at S°={{0,3}}: bound {lb:.4f} <= pi0 {math.exp(st.log_pi0([0,3])):.4f}")
# 3. partition port vs scipy complete linkage (no ties: continuous data)
ok = 0; tot = 0
for rep in range(20):
    n2, p2 = 80, int(rng.integers(20, 90))
    Z = rng.standard_normal((n2, p2)); F_ = rng.standard_normal((n2, 6))
    Z += F_[:, rng.integers(0, 6, p2)] * rng.uniform(0, 2, p2)
    X2, _ = standardise(Z, rng.standard_normal(n2))
    left, right, size, root = complete_linkage(X2)
    R = np.corrcoef(X2.T); Dm = 1 - np.abs(R); np.fill_diagonal(Dm, 0)
    Lk = linkage(squareform(Dm, checks=False), 'complete')
    # compare the sets of clusters (as frozensets) produced by each dendrogram
    def sets_mine():
        out_ = []
        for nd in range(p2, 2 * p2 - 1):
            out_.append(frozenset(vm_leaves(nd)))
        return set(out_)
    import vm_core
    def vm_leaves(nd): return vm_core._leaves(left, right, nd, p2)
    mine = sets_mine()
    memb = {i: frozenset([i]) for i in range(p2)}
    theirs = set()
    for t, (a, b, h, c) in enumerate(Lk):
        s_ = memb[int(a)] | memb[int(b)]; memb[p2 + t] = s_; theirs.add(s_)
    tot += 1; ok += (mine == theirs)
out.append(f"complete-linkage port vs scipy (cluster sets identical): {ok}/{tot}")
# 4. exact-Gram LH: partition = groups, and local search sanity
units, theta, S0, Sref, M, groups = lh_spec(12, 9, 0.7, [0.5], [1.4], [1.0])
Xr, yr = gen_lh_gram(400, 12, 9, units, theta, rng)
X, y = standardise(Xr, yr)
bl, B = partition(X)
out.append(f"exact-Gram LH (G=12,g=9,n=400,B={B}): blocks == groups: {bl == groups}")
print("\n".join(out))
open('../results/sanity.txt', 'w').write("\n".join(out) + "\n")
