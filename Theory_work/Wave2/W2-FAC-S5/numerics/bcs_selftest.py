"""Self-test: bcs_core closed form vs W2-FAC-B fac_core.scan (general exact-Gram Schur scanner, itself verified
against direct n x p scoring in W2-FAC-B/numerics/fac_selftest_out.txt). Compares every flip gain (deletion and addition) and the best exhaustive swap gain (not each swap pair)."""
import sys, math, numpy as np
sys.path.insert(0, "../../W2-FAC-B/numerics")
import fac_core as fc, bvs_core as bc
import bcs_core as B

class Dummy: pass

def run(p, q, n, rb, rw, seed, frac):
    rng = np.random.default_rng(seed)
    grp = np.arange(p) // q
    th = B.layout(p, q, s0=3, c=1.0)
    P = B.BCS(n, grp, rb, rw, th, rng)
    D = Dummy()
    D.n, D.p, D.K = n, p, P.K
    Sig = np.zeros((p, p))
    for i in range(p):
        Sig[i] = rb + (rw - rb) * (grp == grp[i])
        Sig[i, i] = 1.0
    D.XtX = (n - 1.0) * Sig
    D.Xty = P.z
    D.yty = n - 1.0
    D.nu = P.nu
    D.logw = bc.log_prior_w(p, P.K)
    D.logm0 = -D.nu * math.log(0.02 + D.yty)
    assert np.allclose(D.logw - D.logw[0], P.logw - P.logw[0])
    mask = rng.random(p) < frac
    mask[P.S0] = True
    T = np.flatnonzero(mask)
    sc = fc.scan(D, tuple(T))
    path = B.Path(P, mask)
    G = path.gains(swaps=False)
    FT = sc["FT"]
    e_del = np.max(np.abs((sc["del"] - FT) - G["gdel"]))
    e_add = np.max(np.abs((sc["add"] - FT) - G["gadd"])) if len(sc["add"]) else 0.0
    # exhaustive swaps by brute force using bcs closed form per pair
    sw_ref = sc["swap"] - FT  # rows j in T, cols l in O
    bestref = float(np.max(sw_ref))
    best = path.gains(swaps=True, exhaustive=True)["swap"][0]
    best_c = path.gains(swaps=True, exhaustive=False, J=5)["swap"][0]
    # direct F check
    F1 = P.F(mask)
    return dict(p=p, q=q, n=n, k=len(T), err_del=e_del, err_add=e_add, swap_ref=bestref, swap_exh=best,
                swap_cand=best_c, err_swap=abs(best - bestref), cand_ok=abs(best_c - bestref) < 1e-6,
                F_closed_minus_scan=F1 - FT)

for (p, q, n, rb, rw, seed, frac) in [(30, 5, 10**6, .3, .7, 1, .6), (30, 5, 10**8, .3, .7, 2, .8),
                                       (40, 4, 10**5, .2, .6, 3, .5), (25, 5, 10**7, .3, .7, 4, .3),
                                       (36, 3, 10**6, .5, .8, 5, .7)]:
    print(run(p, q, n, rb, rw, seed, frac))
