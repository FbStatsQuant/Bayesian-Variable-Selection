# Sanity: convolution start masses == brute-force enumeration; partition of LH family = groups.
import numpy as np, math
from bvs_exact import *
from family import *
rng = np.random.default_rng(20261102)
G, g = 4, 4
links = [(0, 1, 0.5)]
Sig, C = lh_sigma(G, g, 0.7, 0, links)
th, S0, M, Sref = lh_truth(G, g, 0, links, {0: 1.4, 2: 1.8})
print("S0", S0, "masked", M, "Sref", Sref, "eig min", np.linalg.eigvalsh(Sig).min())
for n in [40, 200]:
    B = block_size_B(n, G * g)
    R, r = suff_exact_gram(Sig, th, n, 1.0, rng)
    bl = make_blocks(R, B)
    print("n", n, "B", B, "blocks", bl)
    tabs = tables(bl, R, r, n)
    sm = start_masses(bl, tabs, G * g, n, S0)
    allm = start_logmass_all(bl, tabs, G * g, n)
    print(" conv logpi0(S0)", start_logmass(bl, tabs, G*g, n, S0, sm["logZ0"]), " brute", allm[frozenset(S0)])
    print(" conv R_d", sm["R"], " brute", {d: region_mass(allm, S0, d) for d in (0, 1, 2)})
    lp = posterior_logmass_all(R, r, n)
    print(" pi(S0)", math.exp(lp[frozenset(S0)]), " pi0(Sref)", math.exp(allm[frozenset(Sref)]))
    # check batch vs single scoring
    S = S0
    print(" batch-vs-single", log_m_batch(np.array([S]), R, r, n)[0] - log_m(S, R, r, n))
    print(" EXP' max|R|", np.abs(exp_prime_remainders(bl, R, r, n)).max())
