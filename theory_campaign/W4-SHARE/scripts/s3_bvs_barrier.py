"""W4-SHARE s3: a posterior-level barrier design (outside R/SE at the given n): delivery succeeds, repair fails.

Design PB(n, J): p = 16, four blocks.  Truths a = x0, b = x4, c = x8 (three different blocks, each with three
proxies at correlation 0.9) and d = x12 (visible, noise block).  corr(a, b) = -0.3 and c = alpha(a + b) + e with
1 - R^2(c | a, b) = 0.01, e orthogonal to a, b.  mu = s*e + 0.3*x12 (so the masked part of the signal is the
residual e, invisible to every proper subset of {a, b, c}); s is set so that the joint gain is about J nats.
lambda_min(R_{S0}) = 0.004.  Start mode {12} (a subset of S0, so in R_0), pi0(R_0) ~ 0.98.

Checks: exact scores of the path states; the method grid; 25 x 4 final islands of N = 2500 at n = 4000 and 16000:
whether S0 is scored, delivery to R_0, the realised envelope, LT; LS0 (local search from the start mode) and a
T39-style scoring-only track check (deterministic part: the scan from {12} has no improving move).  Seed 20261102.
"""
import sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from bvs_core import BVS, suff_stats, lse

p = 16


def build_R(rab=-0.3, om=0.01, rprox=0.9, seed=0):
    rng = np.random.default_rng(seed)
    E = np.linalg.qr(rng.standard_normal((40, 40)))[0]
    a = E[:, 0]; b = rab * E[:, 0] + np.sqrt(1 - rab ** 2) * E[:, 1]; e = E[:, 2]
    alpha = np.sqrt((1 - om) / (2 * (1 + rab)))
    c = alpha * (a + b) + np.sqrt(om) * e
    V = [None] * p; k = 4
    for base, vec in [(0, a), (4, b), (8, c)]:
        V[base] = vec
        for q in range(1, 4):
            V[base + q] = rprox * vec + np.sqrt(1 - rprox ** 2) * E[:, k]; k += 1
    V[12] = E[:, 3]
    for q in range(13, 16):
        V[q] = E[:, k]; k += 1
    X = np.array(V)
    return X @ X.T, alpha


def local_search(m, centre, ell):
    """M §6.10 local search on exact scores: scan all flips and swaps of the centre, move to the best strict
    improvement, at most ell moves then one more scan.  Returns (final centre, set of scanned models)."""
    scanned = set(); cur = centre
    for mv in range(ell + 1):
        nb = []
        for j in range(m.p):
            nb.append(cur ^ (1 << j))
        mem = [j for j in range(m.p) if (cur >> j) & 1]; non = [l for l in range(m.p) if not (cur >> l) & 1]
        for j in mem:
            for l in non:
                nb.append((cur & ~(1 << j)) | (1 << l))
        nb = [s for s in nb if m.size[s] <= m.K]
        scanned.update(nb)
        best = max(nb, key=lambda s: (m.lg1[s], -m.size[s], -s))
        if m.lg1[best] > m.lg1[cur] and mv < ell:
            cur = best
        else:
            break
    return cur, scanned


out = []
pr = lambda s: (out.append(s), print(s, flush=True))
R, alpha = build_R()
pr(f"lambda_min(R) = {np.linalg.eigvalsh(R)[0]:.4f}; lambda_min(R_S0) = {np.linalg.eigvalsh(R[np.ix_([0,4,8,12],[0,4,8,12])])[0]:.4f}")
rng = np.random.default_rng(20261102)
for n in [4000, 16000]:
    J = 80
    s = np.sqrt(2 * J / (n - 1)); om = 0.01
    th = np.zeros(p); th[8] = s / np.sqrt(om); th[0] = th[4] = -alpha * s / np.sqrt(om); th[12] = 0.3
    z, yy = suff_stats(R, th, 1.0, n, np.random.default_rng(11))
    m = BVS(R, z, yy, n, [0, 4, 8, 12])
    Sd = 1 << 12
    pr(f"== PB(n={n}, J={J}): blocks {m.blocks}; pi(S0) = {m.post[m.S0]:.3f}; HPM = {m.fmt(int(np.argmax(m.lg1)))}; "
       f"pi0(S0) = {m.pi0[m.S0]:.2e}; start mode {m.fmt(m.start_mode)} (pi0 {m.pi0[m.start_mode]:.3f})")
    for st in [Sd | 1 << 8, Sd | 1 << 0, Sd | 1 << 8 | 1 << 0, Sd | 1 << 0 | 1 << 4, Sd | 1 << 4 | 1 << 8, m.S0]:
        pr(f"   {m.fmt(st):>14}: F - F({{12}}) = {m.lg1[st]-m.lg1[Sd]:7.2f}   log gamma0 diff = {m.lg0[st]-m.lg0[Sd]:7.2f}")
    R0 = m.R_d(0)
    grid, pil, forced = m.method_grid(); T = len(grid) - 1
    qmin = min(np.exp(lse(m.logq(ph)[R0])) for ph in np.linspace(0, 1, 201))
    pr(f"   pi0(R_0) = {m.pi0[R0].sum():.3f}; min over phi in [0,1] of q_phi(R_0) = {qmin:.3f}; grid T = {T}")
    ls_end, scanned = local_search(m, m.start_mode, m.L)
    pr(f"   LS0 from the start mode: stops at {m.fmt(ls_end)}; S0 scanned: {m.S0 in scanned}")
    sets = {"R0": R0}
    scored, deliv, minlogP, lz = 0, [], [], []
    t0 = time.time()
    for r in range(100):
        info = m.island(2500, grid, rng, sets=sets)
        scored += int(info["first_S0"] is not None)
        deliv.append(info["final_counts"]["R0"])
        minlogP.append(np.min(np.cumsum(info["logr"]["R0"])))
        lz.append(info["logZhat_over_Z"])
    deliv = np.array(deliv); lz = np.array(lz)
    pr(f"   100 final islands, N = 2500 ({time.time()-t0:.0f}s): S0 scored in {scored}/100 islands; "
       f"P(n_T(R_0) = 0) = {np.mean(deliv==0):.2f}, median n_T(R_0)/N = {np.median(deliv)/2500:.3f}; "
       f"min_t log P_t (h = 1_R0): median {np.median(minlogP):.2f}, worst {np.min(minlogP):.2f}; "
       f"log(Zhat/Z): median {np.median(lz):.1f}, max {np.max(lz):.1f}")
    # expected crossings per particle-round from {12} at phi = 1 (Monte Carlo over rounds from {12})
    S = np.full(200000, Sd, dtype=np.int64)
    hit = {"x": 0}

    def rec(states, mech):
        hit["x"] += int(np.sum(states == m.S0))
    m.one_round(S, 1.0, rng, rec)
    pr(f"   one round at phi = 1 from {{12}}, 200000 particles: S0 proposals/evaluations = {hit['x']}")
open(__file__.replace(".py", ".txt"), "w").write("\n".join(out) + "\n")
