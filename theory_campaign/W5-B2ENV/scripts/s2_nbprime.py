"""W5-B2ENV s2: NB' and the pilot's first stage (route (b1'), Theorem NB'-LH / Corollary D2-LH) on LH, exact Gram,
exact scores by enumeration.  Seed 20261102.

Design: W1-EXP configuration A (G = 4 groups of g = 4, rho = 0.7, pair (0,1) psi = 0.5, visible group 2), p = 16, c = 1,
S0 = {0, 4, 8}, S° = {0, 8}, masked hub 4, proxies {5,6,7}.  B = 4 = g (blocks = groups; checked).
For each n: exact pi0, d over all 2^16 states;
  * the bound's ingredients: H*pi0(bad) split into (B1..B4) [here computed exactly as H*pi0(S notin G ∪ {S0})] and the
    C_b-touching part H*pi0(S ∩ C_b != ∅, S != S0); the d-range over G (|S∖S°| <= 2) against T0*log r*;
  * simulation of the tier-0 pilot first stage (H0 iid pi0 draws; NB' indicator; the pilot rule with 60 bisections and
    floor 1/T0; multinomial resampling; one full random-order round at phi_1 with SR scoring): frequency of NB'^c, of
    S0 among the draws, and of S0 scored by the end of stage 1.
At p = 16 the condition p/sqrt(n) -> inf fails for n >= 256, so the C_b-touching term grows like sqrt(n)/p: the script
shows the rate of Theorem NB'-LH, not its limit.
"""
import sys, time
from math import ceil, log, sqrt, floor
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bvs_core import BVS, lse, popcount
from lh_family import lh_sigma, lh_truth, suff_exact_gram

out = []
pr = lambda s: (out.append(s), print(s, flush=True))
RSTAR = (11 + 2 * sqrt(10)) / 9


def ess_frac(dv, delta):
    lw = delta * dv
    lw = lw - lw.max()
    w = np.exp(lw)
    return w.sum() ** 2 / (len(w) * (w ** 2).sum())


def pilot_first_phi(dv, Te, thr=0.9):
    if ess_frac(dv, 1.0) >= thr:
        return 1.0, False
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess_frac(dv, mid) >= thr: lo = mid
        else: hi = mid
    if lo < 1.0 / Te:
        return 1.0 / Te, True
    return lo, False


def run(n, reps, rng):
    G, g = 4, 4
    Sig, C = lh_sigma(G, g, 0.7, 0, [(0, 1, 0.5)])
    th, S0, M, Sref = lh_truth(G, g, 0, [(0, 1, 0.5)], {0: 1.4, 2: 1.8})
    R, r = suff_exact_gram(Sig, th, n, 1.0, rng)
    z = r * (n - 1); yy = n - 1.0
    l = ceil(log(n + 16 + 1, 2)); T0 = max(1000, l * l)
    m = BVS(R, z, yy, n, S0, Te=T0)
    assert [sorted(b) for b in m.blocks] == [list(range(4 * h, 4 * h + 4)) for h in range(4)], m.blocks
    H = ceil(512 * max(2500, n, 16) / 2500)
    S0m = m.S0; Srefm = sum(1 << j for j in Sref)
    Cb = sum(1 << j for j in C[1])
    allm = np.arange(m.nstates)
    supS = (allm & Srefm) == Srefm
    extras = popcount(allm & ~Srefm)
    good = supS & ((allm & Cb) == 0) & (extras <= 2)
    bad = ~good & (allm != S0m)
    touch = ((allm & Cb) != 0) & (allm != S0m)
    drange = m.d[good].max() - m.d[good].min()
    pr(f"n={n:6d}: pi0(S°)={m.pi0[Srefm]:.4f} pi0(S0)={m.pi0[S0m]:.2e} pi(S0)={m.post[S0m]:.4f}  H={H} T0={T0}  "
       f"H*pi0(bad)={H*m.pi0[bad].sum():.3f} [C_b-touching {H*m.pi0[touch].sum():.3f}; sqrt(n)/p={sqrt(n)/16:.2f}]  "
       f"d-range on G = {drange:.2f} vs T0 log r* = {T0*log(RSTAR):.0f} (12.1 log n = {12.1*log(n):.0f});  "
       f"d(S°+proxy)-d(S°) = {m.d[Srefm | (1<<5)] - m.d[Srefm]:.1f}")
    nbfail = s0drawn = scored = forced = 0
    t0 = time.time()
    for rep in range(reps):
        X = m.draw_pi0(H, rng)
        dv = m.d[X]
        hasS0 = bool(np.any(X == S0m))
        nbp = hasS0 or ess_frac(dv, 1.0 / T0) >= 0.9
        nbfail += (not nbp); s0drawn += hasS0
        phi1, f = pilot_first_phi(dv, T0); forced += f
        hit = [hasS0]
        def rec(states, mech):
            if not hit[0] and np.any(states == S0m): hit[0] = True
        lw = phi1 * dv; w = np.exp(lw - lw.max())
        anc = np.minimum(np.searchsorted(np.cumsum(w), rng.random(H) * w.sum(), side="left"), H - 1)
        S = X[anc].copy()
        S = m.one_round(S, phi1, rng, rec)
        scored += hit[0]
    pr(f"          {reps} pilot first stages ({time.time()-t0:.0f}s): P(NB'^c)={nbfail/reps:.3f}  P(S0 drawn)={s0drawn/reps:.3f}  "
       f"forced floor steps={forced}  P(S0 scored by end of stage 1)={scored/reps:.3f}")


if __name__ == "__main__":
    rng = np.random.default_rng(20261102)
    for n, reps in [(200, 200), (400, 200), (800, 200), (1600, 200), (3200, 200), (6400, 100), (25600, 50), (102400, 30)]:
        run(n, reps, rng)
    open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
