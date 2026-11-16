"""Toy example for METHOD_INTUITION.md (W3-READER). Re-implements, in exact arithmetic up to float64, the coded
score (Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224), the start law (cpp/v3_start.h:68-137) and the local
search rule (cpp/v3_engine.h:370-419) for a 6-predictor problem with a FIXED partition {1,2},{3,4},{5,6}
(the coded partition for p=6 has blocks of size <= min(floor(sqrt n), floor(sqrt p), 16) = 2). Illustration only;
not the production code."""
import itertools, math
import numpy as np

rng = np.random.default_rng(20261115)
n, p = 100, 6
# latent construction: x2 ~ near-copy of x1 (same block), x5 correlated with x1 but in another block,
# x6 near-copy of x5; x3 true, x4 weakly related to x3; truth S0 = {1, 3}
z = rng.standard_normal((n, 6))
x1 = z[:, 0]
x2 = 0.95 * x1 + math.sqrt(1 - 0.95**2) * z[:, 1]
x3 = z[:, 2]
x4 = 0.6 * x3 + 0.8 * z[:, 3]
x5 = 0.7 * x1 + math.sqrt(1 - 0.49) * z[:, 4]
x6 = 0.9 * x5 + math.sqrt(1 - 0.81) * z[:, 5]
Xr = np.column_stack([x1, x2, x3, x4, x5, x6])
yr = 1.0 + 1.0 * x1 + 1.0 * x3 + rng.standard_normal(n)

# standardisation as coded: centre, scale to ||x_j||^2 = n-1; y = Cy/s_y
X = Xr - Xr.mean(0); X = X / X.std(0, ddof=1)
y = yr - yr.mean(); y = y / y.std(ddof=1)
a0 = b0 = 0.01; nu = a0 + n / 2; K = min(p, n // 2)
logw = lambda k: -math.log(2) - (math.lgamma(2*p) - math.lgamma(k+1) - math.lgamma(2*p-k))
def logm(S):
    S = list(S)
    if not S: return -nu * math.log(2*b0 + y @ y)
    XS = X[:, S]; G = XS.T @ XS; z_ = XS.T @ y
    H = (n+1)*G + np.eye(len(S)); A = G + np.eye(len(S))
    Q = y @ y - n * z_ @ np.linalg.solve(H, z_)
    return -0.5*(np.linalg.slogdet(H)[1] - np.linalg.slogdet(A)[1]) - nu*math.log(2*b0 + Q)
models = [frozenset(c) for k in range(K+1) for c in itertools.combinations(range(p), k)]
F = {S: logw(len(S)) + logm(S) for S in models}
mx = max(F.values()); Z = sum(math.exp(v - mx) for v in F.values())
post = {S: math.exp(F[S] - mx) / Z for S in models}
pip = [sum(v for S, v in post.items() if j in S) for j in range(p)]
blocks = [(0, 1), (2, 3), (4, 5)]
logr = {}
for b in blocks:
    for k in range(3):
        for U in itertools.combinations(b, k):
            logr[frozenset(U)] = logm(U) - logm(())
lg0 = {S: logw(len(S)) + sum(logr[frozenset(S & set(b))] for b in blocks) for S in models}
m0 = max(lg0.values()); Z0 = sum(math.exp(v - m0) for v in lg0.values())
pi0 = {S: math.exp(lg0[S] - m0) / Z0 for S in models}
lab = lambda S: "{" + ",".join(str(j+1) for j in sorted(S)) + "}"
corr = np.corrcoef(Xr.T)
print("sample correlations (rounded):"); print(np.round(corr, 2))
print("\nTop 5 models under the START LAW pi0:")
for S in sorted(models, key=lambda S: -pi0[S])[:5]: print(f"  {lab(S):10s} pi0={pi0[S]:.3f}  posterior={post[S]:.3f}")
print("\nTop 5 models under the POSTERIOR pi(.|y):")
for S in sorted(models, key=lambda S: -post[S])[:5]: print(f"  {lab(S):10s} posterior={post[S]:.3f}  pi0={pi0[S]:.3f}")
print("\nPIPs:", [round(v, 3) for v in pip])
# local search from the start mode, coded rule: best neighbour (add/delete/swap), move on strict improvement
cur = max(models, key=lambda S: (lg0[S], -len(S)))
print("\nstart mode:", lab(cur)); path = [lab(cur)]
while True:
    nb = [cur - {j} for j in cur] + ([cur | {j} for j in range(p) if j not in cur] if len(cur) < K else []) \
         + [(cur - {j}) | {l} for j in cur for l in range(p) if l not in cur]
    best = max(nb, key=lambda S: F[S])
    if F[best] > F[cur]: cur = best; path.append(lab(cur))
    else: break
print("LS0 path:", " -> ".join(path), "(certified: no neighbour improves)")
print("HPM:", lab(max(models, key=lambda S: post[S])), " MPM:", lab({j for j in range(p) if pip[j] > 0.5}))
