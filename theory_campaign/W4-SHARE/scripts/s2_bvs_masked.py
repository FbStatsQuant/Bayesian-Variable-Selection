"""W4-SHARE s2: faithful small-p SMC-BVS final runs on start-masked designs in T03's regime (pi(S0) > 1/2).

Design family M(n, c): p = 16, four clusters of four columns (within-cluster correlation 0.6), one cross-cluster
correlation r(x0, x4) = 0.45; S0 = {0, 4, 8}, theta = c*(-0.45, 1, 0.7) on (x0, x4, x8), sigma = 1.  theta_0 =
-0.45 theta_4 cancels x0's marginal correlation with y, so block A's table does not see x0 (start masking), and block
A's best sub-model compensates x4's projection with proxies (start supersets).  Sufficient statistics are drawn from
their exact law (bvs_core.suff_stats); every score is exact.

For each design: method grid (idealised calibration, see bvs_core), 25 replications x 4 islands, N = 2500.
Reported per design: exact pi(S0), pi0(S0), start mode, pi0(R_d), inf over grid of q_phi(R_d);
over islands: the stage at which S0 is first scored in the final run (0 = initial draw, T+1 = terminal rounds, never),
the mechanism, n_T(R_d) (delivery), min_t log P_t for h = 1_{R_d} (realised D4 envelope with eta = 0),
the largest realised outsider fraction, and log(Zhat/Z) (LT).  Seed 20261102.
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from bvs_core import BVS, suff_stats, lse

p = 16


def design_R(rho_c=0.6, r04=0.45):
    R = np.eye(p)
    for c in range(4):
        idx = range(4 * c, 4 * c + 4)
        for i in idx:
            for j in idx:
                if i != j: R[i, j] = rho_c
    R[0, 4] = R[4, 0] = r04
    return R


def run(n, c, reps=25, N=2500, seed=20261102, label=""):
    rng = np.random.default_rng(seed)
    R = design_R()
    th = np.zeros(p); th[[0, 4, 8]] = c * np.array([-0.45, 1.0, 0.7])
    z, yy = suff_stats(R, th, 1.0, n, np.random.default_rng(7))
    m = BVS(R, z, yy, n, [0, 4, 8])
    grid, pil, forced = m.method_grid()
    T = len(grid) - 1
    out = []
    pr = lambda s: (out.append(s), print(s, flush=True))
    sm = m.start_mode
    pr(f"== design {label}: n={n} c={c}  blocks={m.blocks}")
    pr(f"   pi(S0)={m.post[m.S0]:.3f}  HPM={m.fmt(int(np.argmax(m.lg1)))}  pi0(S0)={m.pi0[m.S0]:.3e}  start mode={m.fmt(sm)} "
       f"(pi0={m.pi0[sm]:.3f}, d(S0)-d(mode)={m.d[m.S0]-m.d[sm]:.1f})")
    Rd = {d: m.R_d(d) for d in (0, 1, 2)}
    qinf = {d: min(np.exp(lse(m.logq(ph)[Rd[d]])) for ph in grid) for d in Rd}
    pr("   pi0(R_d), inf_grid q_phi(R_d), pi(R_d): " + "; ".join(
        f"d={d}: {m.pi0[Rd[d]].sum():.3f}, {qinf[d]:.3f}, {m.post[Rd[d]].sum():.3f}" for d in Rd))
    pr(f"   grid: T={T} stages (pilot {len(pil)-1}, forced {forced}); first phi's {np.round(grid[1:5], 4)}")
    sets = {f"R{d}": Rd[d] for d in Rd}
    first, mech, deliv, minlogP, maxout, lz = [], [], {k: [] for k in sets}, {k: [] for k in sets}, {k: [] for k in sets}, []
    t0 = time.time()
    for r in range(reps * 4):
        info = m.island(N, grid, rng, sets=sets)
        fs = info["first_S0"]
        first.append(fs[0] if fs else -1); mech.append(fs[1] if fs else "never")
        for k in sets:
            deliv[k].append(info["final_counts"][k])
            lr = info["logr"][k]
            minlogP[k].append(np.min(np.cumsum(lr)) if len(lr) else 0.0)
            cnt = info["counts"][k]
            maxout[k].append(1 - cnt.min() / N)
        lz.append(info["logZhat_over_Z"])
    first = np.array(first)
    bridge = np.mean((first >= 0) & (first <= T))
    term = np.mean(first == T + 1)
    never = np.mean(first < 0)
    pr(f"   {reps*4} islands ({time.time()-t0:.0f}s): S0 first scored at stage 0: {np.mean(first==0):.2f}, "
       f"stages 1-2: {np.mean((first>=1)&(first<=2)):.2f}, stages 3..T: {np.mean((first>=3)&(first<=T)):.2f}, "
       f"terminal rounds: {term:.2f}, never: {never:.2f}")
    ms, cs = np.unique(mech, return_counts=True)
    pr("   mechanism of first S0 score: " + ", ".join(f"{a}:{b}" for a, b in zip(ms, cs)))
    for k in sets:
        dv = np.array(deliv[k])
        pr(f"   W={k}: P(n_T(W)=0)={np.mean(dv==0):.3f}  median n_T/N={np.median(dv)/N:.3f}  "
           f"min_t log P_t: median {np.median(minlogP[k]):.2f}, worst {np.min(minlogP[k]):.2f}  "
           f"max outsider fraction: median {np.median(maxout[k]):.3f}, worst {np.max(maxout[k]):.3f}")
    lz = np.array(lz)
    pr(f"   LT: log(Zhat/Z) median {np.median(lz):.3f}, min {np.min(lz):.3f}; P(Zhat/Z < 1/2) = {np.mean(lz < np.log(0.5)):.3f}")
    return out


if __name__ == "__main__":
    allout = []
    for lab, n, c in [("E1a", 1000, 0.5), ("E1b", 1000, 0.3), ("E1c", 4000, 0.3), ("E1d", 4000, 0.5), ("E1e", 400, 0.8)]:
        allout += run(n, c, label=lab)
    open(__file__.replace(".py", ".txt"), "w").write("\n".join(allout) + "\n")
