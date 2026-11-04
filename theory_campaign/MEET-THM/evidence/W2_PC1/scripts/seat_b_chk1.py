# Seat B, R2 local check 1: Seat C's D_* (PC2 cluster 4) evaluated on PC1's design D-eps
# (n=40, p=8, built pairs, within .6, cross eps, coefficients .25 at 0 and .2 at 4, exact Gram X'X=39*Sigma),
# with the method's own coded partition (PC2 bvs_common.coded_partition, M 6.3). 10 noise seeds per eps, < 1 min.
import sys, math, numpy as np
sys.path.insert(0, sys.argv[1])
import bvs_common as bc

def exact_gram_design(Sigma, n, rng):
    p = Sigma.shape[0]
    Z = rng.standard_normal((n, p + 1))
    Z = Z - Z.mean(0)
    Q, _ = np.linalg.qr(Z)           # orthonormal, centred columns
    U = Q[:, :p]
    L = np.linalg.cholesky(Sigma)
    return math.sqrt(n - 1) * U @ L.T   # X'X = (n-1) Sigma exactly, columns centred

n, p = 40, 8
pairs = [[0, 1], [2, 3], [4, 5], [6, 7]]
K, B = bc.method_sizes(n, p)
print("n p K B =", n, p, K, B)
print("eps seed | blocks=pairs | a dA dH r | D_* shared 2bX | osc_d | osc/D_* | log(1+chi2) <= osc?")
for eps in (1e-5, 1e-4, 1e-3, 1e-2):
    Sigma = np.full((p, p), eps)
    for b in pairs:
        for i in b:
            for j in b:
                Sigma[i, j] = 0.6 if i != j else 1.0
    for seed in range(10):
        rng = np.random.default_rng(seed)
        X = exact_gram_design(Sigma, n, rng)
        beta = np.zeros(p); beta[0] = .25; beta[4] = .2
        y = X @ beta + rng.standard_normal(n)
        G, z, Y, nn = bc.suff_from_data(X, y)
        blocks = bc.coded_partition(G, B)
        same = sorted(map(sorted, blocks)) == pairs
        models, d, lbf = bc.d_table(G, z, Y, n, blocks, K)
        out = bc.card_Dstar(G, z, Y, n, blocks, K)
        osc = d.max() - d.min()
        # one-shot chi2(pi||pi0) via WS1: log(1+chi2) = Lam(2) - 2 Lam(1), Lam(phi) = log E_pi0 e^{phi d}
        lg0 = np.array([bc.log_prior_w(p, len(S)) + (lbf[i] - d[i]) for i, S in enumerate(models)])
        from scipy.special import logsumexp
        Lam = lambda ph: logsumexp(lg0 + ph * d) - logsumexp(lg0)
        l1c = Lam(2.0) - 2 * Lam(1.0)
        if out['ok']:
            print(f"{eps:7.0e} {seed:2d} | {same} | {out['a']:.3f} {out['dA']:.2e} {out['dH']:.2e} {out['r']:.2e} | "
                  f"{out['Dstar']:.3f} {out['shared']:.3f} {2*out['bX']:.3f} | {osc:.3f} | {osc/out['Dstar']:.3f} | {l1c:.3f} {l1c <= osc + 1e-9}")
        else:
            print(f"{eps:7.0e} {seed:2d} | {same} | hypotheses fail: a={out['a']:.3f} dA={out['dA']:.2e} dH={out['dH']:.2e} | osc={osc:.3f}")
