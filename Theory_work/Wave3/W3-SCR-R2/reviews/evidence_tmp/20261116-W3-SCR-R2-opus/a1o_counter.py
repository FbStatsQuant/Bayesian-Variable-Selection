# Counterexample to the REPORT.md:30-31 summary of A1° ("beta-min ... suffices", competition "not the total signal").
# Orthogonal design (kappa = 1), s0 = 2, q = 1, n = 20000, p = 10, sigma = 1.
# theta_2 at the A1° beta-min level; theta_1 huge (violates ||mu|| = o(n sigma), the condition the REPORT drops).
import numpy as np, math, itertools
rng = np.random.default_rng(1)
n, p, sigma = 20000, 10, 1.0
Z = rng.standard_normal((n, p)); Z -= Z.mean(0)
Qm, _ = np.linalg.qr(Z); X = Qm * math.sqrt(n - 1)          # centred, orthogonal, ||x_j||^2 = n-1
q = 1; L = (q + 1) * math.log(p) + math.log(n)
bmin = 16 * sigma * math.sqrt(L / n)
print("L_n", L, "s0*L", 2 * L, "<= n/576", n / 576, "beta-min level", bmin)
theta = np.zeros(p); theta[0] = 1e5; theta[1] = 1.01 * bmin
mu = X @ theta
eps = sigma * rng.standard_normal(n); yc = mu + eps - eps.mean()
y = yc / math.sqrt(yc @ yc / (n - 1))
nu = 0.01 + n / 2; K = min(p, n // 2)
lw = lambda k: -math.log(2) - (math.lgamma(2*p) - math.lgamma(k+1) - math.lgamma(2*p-k))
def F(S):
    S = sorted(S); k = len(S)
    if k == 0: return lw(0) - nu * math.log(0.02 + y @ y)
    XS = X[:, S]; G = XS.T @ XS; z = XS.T @ y
    H = (n + 1) * G + np.eye(k); A = G + np.eye(k)
    Q = y @ y - n * z @ np.linalg.solve(H, z)
    return lw(k) - 0.5 * np.linalg.slogdet(H)[1] + 0.5 * np.linalg.slogdet(A)[1] - nu * math.log(0.02 + Q)
def nbrs(S):
    S = set(S); out = []
    for j in range(p):
        if j in S: out.append(S - {j})
        elif len(S) < K: out.append(S | {j})
    for j in S:
        for l in range(p):
            if l not in S: out.append((S - {j}) | {l})
    return out
C = {0}
fC = F(C); best = max(F(N) for N in nbrs(C))
print("||mu||/(n sigma) =", np.linalg.norm(mu) / (n * sigma))
print("F({1}) =", fC, " best neighbour F =", best, " {1} LO:", best <= fC)
print("F({1,2}) - F({1}) =", F({0, 1}) - fC)
