"""Sanity checks of pxn_core against brute-force enumeration (p = 12, n = 30, so K = 12 > ... cap K = min(p, 15) = 12;
and n = 16 so that the cap K = 8 binds). Seed 1."""
import itertools, math, numpy as np
from scipy.special import logsumexp
from pxn_core import *
rng = np.random.default_rng(1)
for n in (30, 16):
    p = 12
    Xr = rng.standard_normal((n, p)); Xr[:, 1] += 0.8 * Xr[:, 0]
    yr = Xr[:, 0] - 0.7 * Xr[:, 1] + 0.5 * Xr[:, 5] + rng.standard_normal(n)
    D = Data(Xr, yr)
    blocks = v3_blocks(D, B=3)
    T = Tables(D, blocks); L = StartLaw(T)
    allS = [S for k in range(D.K + 1) for S in itertools.combinations(range(p), k)]
    lg = np.array([log_w(len(S), p) + T.log_r(S) for S in allS])
    lZ = logsumexp(lg)
    print("n", n, "K", D.K, "blocks", blocks)
    print(" logZ conv vs brute:", L.logZ, lZ - 0)
    S0 = [0, 1, 5]
    print(" log pi0(S0):", L.log_pi0(S0), lg[allS.index(tuple(S0))] - lZ)
    for d in (0, 1, 2):
        m = logsumexp([lg[i] for i, S in enumerate(allS) if len(set(S) - set(S0)) <= d]) - lZ
        print(" R_%d:" % d, L.log_mass_Rd(S0, d), m)
    pip = logsumexp([lg[i] for i, S in enumerate(allS) if 5 in S]) - lZ
    print(" PIP0(5):", L.log_mass_constrained(forced_in=[5]), pip)
    md, lm = L.start_mode(); ib = int(np.argmax(lg))
    print(" mode:", md, lm, list(allS[ib]), lg[ib] - lZ)
    # table vs full BF for a within-block set
    C = blocks[0]; U = C[:2]
    print(" table vs log BF:", T.log_r(U), log_bf_sets(D, [U])[0])
    dr = L.sample(4000, np.random.default_rng(2))
    emp = np.mean([tuple(S) == tuple(md) for S in dr])
    print(" sampler freq(mode) %.4f vs exact %.4f" % (emp, math.exp(lm)))
