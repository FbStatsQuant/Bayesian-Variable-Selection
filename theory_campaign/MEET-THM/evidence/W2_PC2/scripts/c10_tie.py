"""W2_PC2: R2_C C10 IC3 exhibit built as actual data. n = 40, p = 20; X columns 1,2 identical; columns 3..20
mutually orthogonal and orthogonal to column 1 (centred); y with squared correlation 1/2 with column 1, 0 with others.
Coded partition (M §6.3, B = min(isqrt 40, isqrt 20, 16) = 4); start score log pi0 up to constant
= log prior(|S|) + sum_b log r_b(S_b), r_b = BF of the block subset (full response).  Enumerates every model of size
<= 4 (dominance argument for larger sizes: every further column has z_j = 0) and lists the top start scores.
Also checks the dispatch rule of R2_C (2^p vs 200000 + 64 n p) and the exact-branch rule used in W1 (d14_family)."""
import math, itertools
import numpy as np
from math import comb
from bvs_common import standardise, method_sizes, coded_partition, log_m, log_prior_w

n, p = 40, 20
rng = np.random.default_rng(3)
Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
C = Q[:, 1:] - 0  # columns orthogonal to Q[:,0]; make them centred: use Helmert-like basis of centred space
# exact centred orthonormal basis
H = np.eye(n) - 1.0 / n
U, s, Vt = np.linalg.svd(H)
basis = U[:, :n - 1]  # orthonormal basis of the centred subspace
x1 = basis[:, 0]
X = np.column_stack([x1, x1] + [basis[:, j] for j in range(1, p - 1)])
y = math.sqrt(.5) * x1 + math.sqrt(.5) * basis[:, p - 1]  # corr^2 1/2 with x1, orthogonal to the others
Xs, ys = standardise(X, y)
G, z, Y = Xs.T @ Xs, Xs.T @ ys, float(ys @ ys)
r = G / (n - 1)
print("corr(x1,x2)=%.6f  corr^2(y,x1)=%.6f  max|corr(y,x_j>2)|=%.2e  max|cross corr others|=%.2e" % (
    r[0, 1], (z[0] / (n - 1)) ** 2, np.abs(z[2:]).max() / (n - 1), np.abs(r[2:, 2:] - np.eye(p - 2)).max()))
K, B = method_sizes(n, p)
blocks = coded_partition(G, B)
print("K=%d B=%d blocks=%s" % (K, B, blocks))
bid = {j: b for b, Cb in enumerate(blocks) for j in Cb}
l0 = log_m(G, z, Y, n, [])
cache = {}
def lr(U):
    U = tuple(sorted(U))
    if U not in cache: cache[U] = log_m(G, z, Y, n, U) - l0
    return cache[U]
scores = []
for k in range(0, 5):
    for S in itertools.combinations(range(p), k):
        parts = {}
        for j in S: parts.setdefault(bid[j], []).append(j)
        sc = (log_prior_w(p, k) - log_prior_w(p, 0)) + sum(lr(U) for U in parts.values())
        scores.append((sc, S))
scores.sort(key=lambda t: (-t[0], t[1]))
for sc, S in scores[:6]:
    print("start score rel. empty %.9f  S=%s" % (sc, [j + 1 for j in S]))
print("tie at top:", abs(scores[0][0] - scores[1][0]) < 1e-9, " lexicographic min of tied:", [j + 1 for j in scores[0][1]])
print("models (K=p) =", sum(comb(p, k) for k in range(K + 1)), " R2_C cutoff 200000+64np =", 200000 + 64 * n * p)
N0 = max(2500, n, p); H0 = math.ceil(512 * N0 / 2500)
print("W1 exact-branch rule (5H0+4N0)p =", (5 * H0 + 4 * N0) * p, " -> SMC dispatch:", 2 ** p > (5 * H0 + 4 * N0) * p)
