"""Adversarial / extra checks on the LH family (explicit exact-Gram designs, seed 20261102 + tag).

(B)  Config B of W1: p = 20, 5 groups of 4, rho = 0.7, two linked pairs (psi = 0.5), masked coefficients
     -0.7 (= -0.5*1.4) and -0.9 (= -0.5*1.8), one null group; c = 2, s = 2. Mstat = log pi0(S0) + 2 log p + log n.
(L)  Leakage chain (Thm 3/4 with CL(L_n)): Config A with the masked coefficient shifted by t = L/sqrt(n-1), so that
     delta_{empty, j_b} = L exactly. Predicted law log(48/29) + (L + Z)^2/(2v).
(P)  Lemma 4.2 boundary: psi in {0.69, 0.71, 0.8} with rho = 0.7 -- does the partition still equal the groups,
     and what happens to pi0(S0)?  (|psi| < rho is the lemma's hypothesis.)
(G)  Packing failure (2g <= B): p = 32, 8 groups of 4, n >= 64 gives B = 5 < 8 = 2g still; use g = 2 groups... see code.
Usage: python3 lh_more.py B|L|P|G
"""
import itertools, math, sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import vcore as V

which = sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else ""


def lh_sigma(p, g, rho, links):
    groups = [list(range(h * g, (h + 1) * g)) for h in range(p // g)]
    S = np.zeros((p, p))
    for G_ in groups:
        S[np.ix_(G_, G_)] = rho; S[G_, G_] = 1.0
    for (ha, hb, psi) in links:
        a, b = groups[ha], groups[hb]
        S[np.ix_(a, b)] = psi * np.outer(S[a, a[0]], S[b[0], b]); S[np.ix_(b, a)] = S[np.ix_(a, b)].T
    return S, groups


def one(n, Sigma, theta, rng, Xf=None, want_pi=False):
    p = len(theta)
    if Xf is None:
        Zm = rng.standard_normal((n, p)); Zm -= Zm.mean(0)
        Q, _ = np.linalg.qr(Zm)
        Xf = math.sqrt(n - 1) * Q @ np.linalg.cholesky(Sigma).T
    X = Xf
    mu = X @ theta
    eps = rng.standard_normal(n); eps -= eps.mean()
    Y = mu + eps; y = Y / math.sqrt(Y @ Y / (n - 1))
    G = X.T @ X
    sf = V.Suff(G, X.T @ y, y @ y, n)
    blocks = V.make_blocks(G / (n - 1), V.B_rule(n, p))
    logr = V.tables(sf, blocks)
    _, _, lg = V.log_gamma0_all(sf, blocks, logr)
    pi0 = V.normalise(lg)
    one.logpi0 = lg - np.logaddexp.reduce(lg[np.isfinite(lg)])
    piv = None
    if want_pi:
        _, _, lp = V.log_post_all(sf)
        piv = V.normalise(lp)
    return pi0, piv, blocks, Xf


if which == 'B':
    p, g, rho = 20, 4, 0.7
    Sigma, groups = lh_sigma(p, g, rho, [(0, 1, 0.5), (2, 3, 0.5)])
    th = np.zeros(p); th[0] = 1.4; th[4] = -0.7; th[8] = 1.8; th[12] = -0.9
    S0 = (0, 4, 8, 12); Sd = (0, 8)
    v = 1 + th @ Sigma @ th
    pred = math.log(3 * 20 / 37) + math.log(4 * 20 / 36)
    rng0 = np.random.default_rng(7)
    sim = pred + rng0.chisquare(2, 200000) / (2 * v)
    print('v =', v, 'predicted Mstat q05/med/q95:', np.round(np.quantile(sim, [.05, .5, .95]), 3))
    for n in [400, 6400, 102400]:
        rng = np.random.default_rng(20261102 + n)
        Ms, sp, R0, ps, bg = [], [], [], [], 0
        Xf = None
        for r in range(60):
            pi0, piv, blocks, Xf = one(n, Sigma, th, rng, Xf, want_pi=(r < 3))
            Ms.append(math.log(pi0[V.mask_of(S0)]) + 2 * math.log(p) + math.log(n))
            sp.append(math.sqrt(n) * (1 - pi0[V.mask_of(Sd)]))
            R0.append(sum(pi0[V.mask_of(t)] for k in range(5) for t in itertools.combinations(S0, k)))
            if piv is not None: ps.append(piv[V.mask_of(S0)])
            bg += sorted(map(tuple, blocks)) == sorted(map(tuple, groups))
        print(json.dumps(dict(n=n, Mstat=list(np.round(np.quantile(Ms, [.05, .5, .95]), 3)),
                              med_log10_pi0S0=round(float(np.median(np.array(Ms) - 2 * math.log(p) - math.log(n)) / math.log(10)), 3),
                              sqrtn_1mpi0Sd=round(float(np.median(sp)), 3), pi0R0=round(float(np.median(R0)), 4),
                              piS0=[round(float(x), 4) for x in ps], blocks_eq_groups=f"{bg}/60")), flush=True)

if which == 'L':
    p, g, rho, psi = 16, 4, 0.7, 0.5
    Sigma, groups = lh_sigma(p, g, rho, [(0, 1, psi)])
    for n in [1600, 102400]:
        for L in [0.0, 2.0, 4.0, math.sqrt(2 * math.log(n))]:
            th = np.zeros(p); th[0] = 1.4; th[8] = 1.8
            th[4] = -psi * 1.4 + L / math.sqrt(n - 1)
            # check delta exactly: delta = x_b' mu / sqrt(n-1) = sqrt(n-1) (Sigma theta)_b
            dl = math.sqrt(n - 1) * (Sigma @ th)[4]
            v = 1 + th @ Sigma @ th
            rng = np.random.default_rng(20261102 + n + int(100 * L))
            Ms = []; Xf = None
            for r in range(300):
                pi0, _, blocks, Xf = one(n, Sigma, th, rng, Xf)
                Ms.append(math.log(pi0[V.mask_of((0, 4, 8))]) + math.log(p) + 0.5 * math.log(n))
            zz = rng.standard_normal(200000)
            pr = math.log(48 / 29) + (L + zz) ** 2 / (2 * v)
            print(json.dumps(dict(n=n, L=round(L, 3), delta=round(dl, 6), obs=list(np.round(np.quantile(Ms, [.05, .5, .95]), 2)),
                                  pred=list(np.round(np.quantile(pr, [.05, .5, .95]), 2)))), flush=True)

if which == 'P':
    p, g, rho = 16, 4, 0.7
    for psi in [0.69, 0.71, 0.8, 0.95]:
        Sigma, groups = lh_sigma(p, g, rho, [(0, 1, psi)])
        th = np.zeros(p); th[0] = 1.4; th[4] = -psi * 1.4; th[8] = 1.8
        for n in [1600, 102400]:
            rng = np.random.default_rng(20261102 + n + int(1000 * psi))
            Ms = []; Sd = []; Xf = None
            for r in range(50):
                pi0, _, blocks, Xf = one(n, Sigma, th, rng, Xf)
                Ms.append(one.logpi0[V.mask_of((0, 4, 8))] + math.log(p) + 0.5 * math.log(n))
                Sd.append(pi0[V.mask_of((0, 8))])
            print(json.dumps(dict(psi=psi, med_pi0Sdeg=round(float(np.median(Sd)), 4), n=n, blocks=blocks, med_log10_pi0S0=round(float(np.median(np.array(Ms) - math.log(p) - 0.5 * math.log(n)) / math.log(10)), 3),
                                  Mstat_med=round(float(np.median(Ms)), 3))), flush=True)

if which == 'G':
    # packing: groups of g = 2 with B = 4 = 2g (violates B < 2g): two groups share a block.
    p, g, rho, psi = 16, 2, 0.7, 0.5
    Sigma, groups = lh_sigma(p, g, rho, [(0, 1, psi)])
    th = np.zeros(p); th[0] = 1.4; th[2] = -psi * 1.4; th[8] = 1.8
    for n in [1600, 102400]:
        rng = np.random.default_rng(20261102 + n)
        Ms = []; Xf = None
        for r in range(50):
            pi0, _, blocks, Xf = one(n, Sigma, th, rng, Xf)
            Ms.append(math.log10(pi0[V.mask_of((0, 2, 8))]))
        print(json.dumps(dict(n=n, B=V.B_rule(n, p), blocks=blocks, med_log10_pi0S0=round(float(np.median(Ms)), 3))), flush=True)
