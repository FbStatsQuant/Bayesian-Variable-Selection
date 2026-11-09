"""L1 falsification: exact identities of the two-level reduction vs direct Gaussian conditioning under Sigma (and the
a-regularised H-based deletion increment of the actual score). Random BCS instances, random T, random j/l."""
import math, numpy as np
rng = np.random.default_rng(7)
tested = 0
worst = dict(normal_eq=0, resid_decomp=0, var_formula=0, tau_bound_viol=0, indep_cov=0, score_tau=0)
for it in range(400):
    q = rng.integers(1, 6); G = rng.integers(2, 7); rb = rng.uniform(.05, .6); rw = rng.uniform(rb + .05, .95)
    b, d = rw - rb, 1 - rw
    sizes = rng.integers(1, q + 1, size=G); grp = np.repeat(np.arange(G), sizes); p = len(grp)
    S = rb + b * (grp[:, None] == grp[None, :]) + d * np.eye(p)
    eta = rng.standard_normal(); zeta = rng.standard_normal(G); xi = rng.standard_normal(p)
    h = math.sqrt(rb) * eta; y = math.sqrt(b) * zeta[grp] + math.sqrt(d) * xi; g = h + y
    T = np.flatnonzero(rng.random(p) < .6)
    if len(T) < 2: continue
    tested += 1
    # direct: E[h | g_T] with Cov(h, g) = rb*1
    ST = S[np.ix_(T, T)]
    hhat = rb * np.ones(len(T)) @ np.linalg.solve(ST, g[T]); e = h - hhat
    u = np.array([np.sum(grp[T] == gg) for gg in range(G)]); om = u / (u * b + d)
    ybar = np.array([y[T][grp[T] == gg].mean() if u[gg] else 0 for gg in range(G)])
    lhs = e * (1 / rb + om.sum()); rhs = h / rb - (om * ybar).sum()
    worst["normal_eq"] = max(worst["normal_eq"], abs(lhs - rhs))
    # residual of j in T given T\j
    for j in T:
        R = T[T != j]
        SR = S[np.ix_(R, R)]; beta = np.linalg.solve(SR, S[R, j])
        r = g[j] - beta @ g[R]; v = S[j, j] - beta @ S[R, j]
        U = R[grp[R] == grp[j]]; uu = len(U); c = d / (uu * b + d)
        a = y[j] - (1 - c) * (y[U].mean() if uu else 0.0)
        eR = h - rb * np.ones(len(R)) @ np.linalg.solve(SR, g[R])
        worst["resid_decomp"] = max(worst["resid_decomp"], abs(r - (a + c * eR)))
        s2 = d * (d + (uu + 1) * b) / (d + uu * b)
        uR = np.array([np.sum(grp[R] == gg) for gg in range(G)]); VR = 1 / (1 / rb + (uR / (uR * b + d)).sum())
        worst["var_formula"] = max(worst["var_formula"], abs(v - (s2 + c * c * VR)))
        tau = r / math.sqrt(v); A = a / math.sqrt(s2); k0 = 1 / math.sqrt(1 - rb)
        if abs(tau) > abs(A) + k0 * abs(eR) + 1e-12: worst["tau_bound_viol"] += 1
        # covariance of a_j(U) with (h, g_R): coefficient vector of a on (eta,zeta,xi) dotted with that of g_R and h
        # a = y_j - (1-c) ybar_U ; Cov(a, g_i) = Cov(y_j, y_i) - (1-c) mean_{U} Cov(y_k, y_i)
        covs = [ (b*(grp[j]==grp[i]) + d*(j==i)) - (1-c)*(np.mean([b*(grp[k]==grp[i]) + d*(k==i) for k in U]) if uu else 0) for i in R]
        worst["indep_cov"] = max(worst["indep_cov"], max(abs(x) for x in covs) if len(covs) else 0)
worst.pop('score_tau')
print(dict(generated=400, tested=tested, **{k: (float(v) if not isinstance(v, int) else v) for k, v in worst.items()}))
