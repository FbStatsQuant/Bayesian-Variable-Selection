"""Sanity checks of vcore.py (seed 20261102).
1. logm_batch == logm_rel; tables vs direct scores.
2. pi0 normaliser by brute force vs by convolution of block size profiles with w(k) (cap included).
3. Partition port: merge heights equal scipy's complete linkage (continuous data, no ties).
4. Lemma 1.1/1.2/1.3 identities at random small designs (deterministic, any data).
"""
import itertools, math, sys
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V

rng = np.random.default_rng(20261102)


def std_data(n, p, rho=0.5):
    Z = rng.standard_normal((n, p)) + rho * rng.standard_normal((n, 1))
    X = Z - Z.mean(0); X /= X.std(0, ddof=1)
    y = X[:, :3] @ np.array([1.0, -0.5, 0.3]) + rng.standard_normal(n)
    y -= y.mean(); y /= y.std(ddof=1)
    return X, y


X, y = std_data(40, 12)
sf = V.Suff(X.T @ X, X.T @ y, y @ y, 40)
idx = np.array(list(itertools.combinations(range(12), 3)))
a = sf.logm_batch(idx); b = np.array([sf.logm_rel(t) for t in idx])
print('1. max |batch - single| =', np.abs(a - b).max())

blocks = V.make_blocks(np.corrcoef(X.T), V.B_rule(40, 12))
print('   blocks:', blocks)
logr = V.tables(sf, blocks)
S, k, lg = V.log_gamma0_all(sf, blocks, logr)
# convolution normaliser
prof = []
for C, t in zip(blocks, logr):
    m = len(C); codes = np.arange(1 << m); kk = V.popcount(codes)
    prof.append(np.array([np.logaddexp.reduce(t[kk == j]) for j in range(m + 1)]))
F = np.array([0.0])
for pr in prof:
    newF = np.full(len(F) + len(pr) - 1, -np.inf)
    for i, f in enumerate(F):
        for j, q in enumerate(pr):
            newF[i + j] = np.logaddexp(newF[i + j], f + q)
    F = newF
logZ_conv = np.logaddexp.reduce([F[j] + V.logw(12, j) for j in range(min(len(F), sf.K + 1))])
logZ_brute = np.logaddexp.reduce(lg[np.isfinite(lg)])
print('2. log Zbar0 (without W_K): brute %.12f  convolution %.12f' % (logZ_brute, logZ_conv))

Xc, _ = std_data(60, 30, rho=0.8)
R = np.corrcoef(Xc.T)
tree = V.complete_linkage(R)
p = 30
mine = sorted(max(1 - abs(R[i, j]) for i in V.leaves(tree, tree[0][nd], p) for j in V.leaves(tree, tree[1][nd], p))
              for nd in range(p, 2 * p - 1))
Dm = 1 - np.abs(R); np.fill_diagonal(Dm, 0)
sp = sorted(linkage(squareform(Dm, checks=False), 'complete')[:, 2])
print('3. max |merge heights mine - scipy| =', np.abs(np.array(mine) - np.array(sp)).max())

# 4. Lemma checks: deterministic identities/bounds at arbitrary data (small n, high SNR)
worst = 0
for rep in range(300):
    n = int(rng.integers(8, 60)); pp = 6
    Z = rng.standard_normal((n, pp)) + rng.uniform(0, 3) * rng.standard_normal((n, 1))
    X = Z - Z.mean(0); X /= X.std(0, ddof=1)
    y = X @ rng.normal(0, 3, pp) + rng.uniform(0.01, 1) * rng.standard_normal(n)
    y -= y.mean(); y /= y.std(ddof=1)
    sf = V.Suff(X.T @ X, X.T @ y, y @ y, n)
    G = sf.G
    phi2 = np.linalg.eigvalsh(G / (n - 1)).min()
    for T in itertools.chain.from_iterable(itertools.combinations(range(pp), r) for r in range(0, 5)):
        for l in range(pp):
            if l in T:
                continue
            Tl = tuple(sorted(T + (l,)))
            if len(Tl) > sf.K:
                continue
            def rss(U):
                U = list(U)
                if not U: return sf.yty
                return sf.yty - sf.z[U] @ np.linalg.solve(G[np.ix_(U, U)], sf.z[U])
            x = (rss(T) - rss(Tl)) / rss(T)
            Rm = sf.logm_rel(Tl) - sf.logm_rel(T) + 0.5 * math.log(n + 1) + sf.nu * math.log(1 - x)
            bound = (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + sf.nu * (1.02 + 1 / (n * phi2)) / min(rss(T), rss(Tl))
            worst = max(worst, abs(Rm) / bound)
print('4. max |R| / (Lemma 1.3 deterministic bound) over 300 random small designs =', worst)
