# Seat B, R2 local check 2: necessity scale of osc d at fixed cross-block correlation eps.
# Two blocks {0,1},{2,3}, within rho=.5, cross eps between every pair across blocks, exact Gram, sigma=1,
# truths at 0 and 2 (one per block) with coefficient theta. Reports osc d over all |S|<=K models,
# the two-model lower bound |d(S0)-d(empty)|, the prediction n*eps*theta1*theta2*(ratio) and the one-shot
# log(1+chi2(pi||pi0)). 5 seeds per (n, eps, signal), < 1 min.
import sys, math, numpy as np
from scipy.special import logsumexp
sys.path.insert(0, sys.argv[1])
import bvs_common as bc

def exact_gram_design(Sigma, n, rng):
    p = Sigma.shape[0]
    Z = rng.standard_normal((n, p + 1)); Z = Z - Z.mean(0)
    Q, _ = np.linalg.qr(Z); U = Q[:, :p]
    return math.sqrt(n - 1) * U @ np.linalg.cholesky(Sigma).T

p = 4; blocks = [[0, 1], [2, 3]]; rho = .5
print("signal   n    eps | osc_d  |d(S0)-d(0)|  n*eps*th^2  osc/(n eps th^2)  log(1+chi2)   [median over 5 seeds]")
for signal in ("fixed .5", "n^-1/4"):
    for eps in (0.05, 0.1):
        for n in (100, 400, 1600, 6400):
            Sigma = np.full((p, p), eps)
            for b in blocks:
                for i in b:
                    for j in b:
                        Sigma[i, j] = rho if i != j else 1.0
            th = .5 if signal == "fixed .5" else n ** -0.25
            K = min(p, n // 2)
            rows = []
            for seed in range(5):
                rng = np.random.default_rng(seed)
                X = exact_gram_design(Sigma, n, rng)
                beta = np.zeros(p); beta[0] = th; beta[2] = th
                y = X @ beta + rng.standard_normal(n)
                G, z, Y, _ = bc.suff_from_data(X, y)
                models, d, lbf = bc.d_table(G, z, Y, n, blocks, K)
                i0 = models.index((0, 2)); ie = models.index(())
                lg0 = np.array([bc.log_prior_w(p, len(S)) + (lbf[i] - d[i]) for i, S in enumerate(models)])
                Lam = lambda ph: logsumexp(lg0 + ph * d) - logsumexp(lg0)
                # standardised-scale prediction: y is standardised, so theta^2 -> theta^2/(var y)
                vy = 2 * th * th * (1 + eps) + 1.0
                pred = n * eps * th * th / vy
                rows.append([d.max() - d.min(), abs(d[i0] - d[ie]), pred, (d.max() - d.min()) / pred, Lam(2) - 2 * Lam(1)])
            m = np.median(np.array(rows), 0)
            print(f"{signal:8s} {n:5d} {eps:.2f} | {m[0]:7.2f} {m[1]:9.2f} {m[2]:10.2f} {m[3]:10.3f} {m[4]:10.3f}")
