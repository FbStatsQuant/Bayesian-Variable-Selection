"""Sanity: convolution pi0 vs brute force at p = 12 (seed 20261102)."""
import itertools, numpy as np
from scipy.special import logsumexp
import dilute as D
rng = np.random.default_rng(20261102)
n, p, B, K = 40, 12, 4, 6
X = rng.standard_normal((n, p)); X = (X - X.mean(0)) / X.std(0, ddof=1)
th = np.zeros(p); th[[0, 5, 9]] = [1.0, -0.7, 0.5]
y, _ = D.std_y(X @ th + rng.standard_normal(n)); yy = y @ y
blocks = D.make_blocks(X, B)
S0 = [0, 5, 9]
tabs, tms = [], []
for blk in blocks:
    sz, ld, t = D.block_stats(X, blk, y[:, None], n)
    tabs.append((sz, D.log_r_v3(ld, t[:, 0], yy, n)))
    tms.append(sum(1 << i for i, c in enumerate(blk) if c in S0))
out = D.start_summary(tabs, tms, p, len(S0), K)
# brute force
colblk = {c: (bi, i) for bi, blk in enumerate(blocks) for i, c in enumerate(blk)}
lg = []; models = []
for k in range(K + 1):
    for S in itertools.combinations(range(p), k):
        masks = [0] * len(blocks)
        for c in S: bi, i = colblk[c]; masks[bi] |= 1 << i
        lg.append(D.log_w(k, p) + sum(tabs[b][1][masks[b]] for b in range(len(blocks)))); models.append(S)
lg = np.array(lg); lz = logsumexp(lg)
i0 = models.index(tuple(S0))
print("blocks", blocks)
print("logpi0(S0) conv %.10f brute %.10f" % (out["logpi0_S0"], lg[i0] - lz))
R2 = sum(np.exp(lg[i] - lz) for i, S in enumerate(models) if len(set(S) - set(S0)) <= 2)
print("pi0(R2) conv %.10f brute %.10f" % (out["pi0_R"][2], R2))
dec = out["vis"] + out["comp"] + out["logA"]
print("decomposition -vis-comp+logA = %.10f" % (-out["vis"] - out["comp"] + out["logA"]))
mode = D.start_mode(tabs, p, K); Sm = sorted(sum((D.mask_to_cols(blocks[b], m) for b, m in mode), []))
print("mode DP", Sm, "brute", models[int(np.argmax(lg))])
