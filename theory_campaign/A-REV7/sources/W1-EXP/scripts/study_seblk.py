"""SE-blk at the study size: min_b lambda_min(R_{C_b}) for the v3 partition on S1-S6 designs (n=200, p in {500,1000}),
iid Gaussian rows with scenario_covariance() of gen_dev_data.R (numpy RNG, seed 20261102+s; distributionally equal
to, not bitwise identical with, the R generator). Partition: scipy complete linkage on 1-|r| (no ties a.s.), children
reordered so the left child has the smaller minimum index (R13), top-down cut at B, next-fit packing in leaf order.
Also reports the EXP' remainder bound ingredients."""
import math, sys
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from pop_leak_study import cov

def blocks_v3(R, B):
    p = R.shape[0]
    D = 1 - np.abs(R); np.fill_diagonal(D, 0)
    Z = linkage(squareform(D, checks=False), method="complete")
    left, right, size, mn = {}, {}, {j: 1 for j in range(p)}, {j: j for j in range(p)}
    for k, (a, b, h, sz) in enumerate(Z):
        a, b, nd = int(a), int(b), p + k
        if mn[a] > mn[b]: a, b = b, a
        left[nd], right[nd], size[nd], mn[nd] = a, b, int(sz), min(mn[a], mn[b])
    def leaves(nd):
        out, st = [], [nd]
        while st:
            x = st.pop()
            if x < p: out.append(x); continue
            st.append(right[x]); st.append(left[x])
        return out
    clusters, st = [], [2 * p - 2]
    while st:
        x = st.pop()
        if size[x] <= B: clusters.append(leaves(x)); continue
        st.append(right[x]); st.append(left[x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B: blocks.append(cur); cur = []
        cur = cur + c
    if cur: blocks.append(cur)
    return [sorted(b) for b in blocks]

n = 200
for p in (500, 1000):
    B = min(math.isqrt(n), math.isqrt(p), 16)
    for s in range(1, 7):
        rng = np.random.default_rng(20261102 + 10 * s + p)
        L = np.linalg.cholesky(cov(s, p))
        X = rng.standard_normal((n, p)) @ L.T
        X -= X.mean(0); X /= X.std(0, ddof=1)
        R = X.T @ X / (n - 1)
        bl = blocks_v3(R, B)
        lm = min(np.linalg.eigvalsh(R[np.ix_(b, b)])[0] for b in bl)
        sizes = np.bincount([len(b) for b in bl])
        grp = np.arange(p) // 5
        whole = np.mean([len(set(grp[b])) * 5 == len(b) for b in bl])
        print(f"p={p} B={B} S{s}: J={len(bl)} min_b lambda_min(R_Cb)={lm:.4f}  frac blocks = union of whole groups={whole:.2f}", flush=True)
