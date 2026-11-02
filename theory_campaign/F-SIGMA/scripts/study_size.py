"""F-SIGMA study-size numerics: n = 200, s0 = 14, study beta pattern, sigma = 1, c in {1, 0.5}.
Cells: BO196: exact block-orthogonal design p = 196 = 14 blocks of 14 (one truth per block; within-block rho = 0.3);
       IID500: iid Gaussian design p = 500, block size B = 14, blocks = consecutive index groups (36 blocks), one truth per block in 14 of them.
Per replicate: exact tables (all sub-models of all blocks), exact pi0^{v3}(S0), exact pi0^C(S0) at several sigma_hat^2,
the C-fix iteration, the Thm C1 bound, and an importance-sampling estimate of pi(S0) from pi0^C (exact iid start draws, weights e^{d^C}).
Seed 20261102 + cell offsets. Laptop: <= 4 cores."""
import sys, os, time; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy.special import logsumexp
from sigma_lib import *

beta_pat = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
n, s0, B = 200, 14, 14

def run(cell, cval, rep, rng, out):
    if cell == "BO196":
        p = 196; blocks = [list(range(14*b, 14*b+14)) for b in range(14)]
        X = bo_design(n, blocks, 0.3, rng)
    else:
        p = 500; blocks = [list(range(14*b, min(14*b+14, p))) for b in range(36)]
        X = iid_design(n, p, rng)
    K = min(p, n//2)
    truths = [blocks[b][0] for b in range(14)]
    theta = np.zeros(p); theta[truths] = cval*np.resize(beta_pat, 14)
    y, mu, sig = make_y(X, theta, 1.0, rng)
    sc = Scorer(X, y); S0 = tuple(sorted(truths))
    t0 = time.time()
    tabs = [block_tables(sc, b) for b in blocks]
    tt = time.time() - t0
    tS0, lDS0 = sc.tD(S0); s2_S0 = (sc.c - tS0)/(2*sc.nu)
    st_v3 = Start(blocks, tabs, lambda t, lD: sc.logBF_from(t, lD), p, K)
    mode_v3 = tuple(st_v3.mode()); tm, _ = sc.tD(mode_v3); s2_mode = (sc.c - tm)/(2*sc.nu)
    m = 20; top = list(np.argsort(-np.abs(sc.z))[:m]); tsc, _ = sc.tD(top); s2_scr = (sc.c - tsc)/(2*sc.nu)
    s2 = s2_mode; Sfix = mode_v3; its = 0
    for it in range(12):
        stC = Start(blocks, tabs, lambda t, lD, s2=s2: sc.logrC_from(t, lD, s2), p, K)
        Snew = tuple(stC.mode()); tn, _ = sc.tD(Snew); s2n = (sc.c - tn)/(2*sc.nu); its += 1
        if Snew == Sfix: break
        Sfix, s2 = Snew, s2n
    s2_fix = s2
    line = (f"[{cell} c={cval} rep={rep}] tables {tt:.1f}s; sigma^2(y-scale)={sig**2:.4f} s2_S0={s2_S0:.4f} s2_mode={s2_mode:.4f} (|mode_v3|={len(mode_v3)}, "
            f"|mode_v3 & S0|={len(set(mode_v3)&set(S0))}) s2_scr={s2_scr:.4f} s2_fix={s2_fix:.4f} ({its} its, |Sfix|={len(Sfix)}, |Sfix & S0|={len(set(Sfix)&set(S0))})\n"
            f"   log10 pi0^v3(S0) = {st_v3.log_pi0(S0)/np.log(10):.2f}")
    print(line); out.write(line + "\n")
    for lab, s2 in [("oracle sigma^2", sig**2), ("s2_S0", s2_S0), ("C-fix", s2_fix), ("v3-mode RSS", s2_mode), ("screen top20", s2_scr), ("null s_y^2", sc.c/(2*sc.nu)), ("0.7 sigma^2", 0.7*sig**2), ("0.5 sigma^2", 0.5*sig**2)]:
        stC = Start(blocks, tabs, lambda t, lD, s2=s2: sc.logrC_from(t, lD, s2), p, K)
        lp0 = stC.log_pi0(S0); u0 = (sc.c - tS0)/(2*sc.nu*s2)
        M = 400
        draws = stC.sample(rng, M)
        dC = np.array([sc.logBF_from(*sc.tD(S)) - (stC.log_gamma0(S) - log_w(len(S), p)) for S in draws])
        dC0 = sc.logBF_from(tS0, lDS0) - (stC.log_gamma0(S0) - log_w(s0, p))
        lE = logsumexp(dC) - np.log(M); ess = np.exp(2*logsumexp(dC) - logsumexp(2*dC))/M
        lpi = lp0 + dC0 - lE
        sizes = np.array([len(S) for S in draws])
        bound = lpi - sc.nu*psi(u0)
        line = (f"   s2 = {lab:14s} {s2:.4f} a={sig**2/s2:.3f} u0={u0:.3f}: log10 pi0^C(S0) = {lp0/np.log(10):7.2f}  IS log10 pi(S0) = {lpi/np.log(10):6.2f} (ESS frac {ess:.2f}, mean|S| {sizes.mean():.1f})  "
                f"nu psi(u0) = {sc.nu*psi(u0):8.2f}  C1 bound log10 = {bound/np.log(10):7.2f}  |mode|={len(stC.mode())}")
        print(line); out.write(line + "\n"); out.flush()

if __name__ == "__main__":
    cell = sys.argv[1]; reps = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    with open(os.path.join(os.path.dirname(__file__), "..", "results", f"study_size_{cell}.txt"), "w", encoding="utf-8") as out:
        for cval in (1.0, 0.5):
            for rep in range(reps):
                rng = np.random.default_rng(20261102 + 1000*(cell == "IID500") + 100*int(cval*2) + rep)
                run(cell, cval, rep, rng, out)
