"""O-BGIBBS bg1: pilot FIRST-STAGE multi-flip discovery on the linked-hub family LH (exact Gram), c = 2 masked hubs.

Engine: bvs_core.py copied verbatim from theory/W4-SHARE (faithful re-implementation of METHODOLOGY_v3 §§4-6,
SR scoring of both Gibbs configurations, every proposal recorded).
For each replicate (fresh noise -> fresh data): H iid pi_0 draws, phi_1 from the engine's pilot rule (pilot_next_phi:
largest phi' with population ESS >= 0.9H by 60 halvings, floor 1/T_e), multinomial resampling, ONE round at phi_1.
Records: was S0 scored in that single round (Theorem BG1's event); start fraction at S°; the outsider-weight ratio
W_out/n° (uniform-in-phi bound: W_out <= sum_{outsiders} (1 + e^{Delta})); basin fraction after resampling;
phi_1; phi_hub = smallest phi at which every hub addition along the chain from S° and S°+k has odds >= 1.
Usage: python bg1_first_stage.py n1 n2 ... (seed fixed).
"""
import sys
import numpy as np
from bvs_core import BVS, suff_stats

def lh_design(g=4, rho=0.7, psi=0.5, beta=1.0):
    p = 4 * g
    S = np.zeros((p, p))
    for h in range(4):
        idx = range(h * g, (h + 1) * g)
        for i in idx:
            for j in idx:
                S[i, j] = 1.0 if i == j else rho
    for (a, b) in [(0, 1), (2, 3)]:            # linked pairs of groups; hubs = first member
        ja, jb = a * g, b * g
        for i in range(a * g, (a + 1) * g):
            for j in range(b * g, (b + 1) * g):
                S[i, j] = S[j, i] = psi * S[i, ja] * S[jb, j]
    theta = np.zeros(p)
    hubs_a, hubs_b = [0, 2 * g], [g, 3 * g]
    for ja, jb in zip(hubs_a, hubs_b):
        theta[ja] = beta; theta[jb] = -psi * beta
    return S, theta, hubs_a, hubs_b, g

def ess(dv, delta):
    w = np.exp(delta * (dv - dv.max()))
    return w.sum() ** 2 / (w ** 2).sum()

def pilot_next_phi(dv, phi, H, Te):
    thr = 0.9 * H
    if ess(dv, 1 - phi) >= thr:
        return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess(dv, mid - phi) >= thr: lo = mid
        else: hi = mid
    if lo - phi < 1.0 / Te:
        return min(1.0, phi + 1.0 / Te), True
    return lo, False

def main():
    ns = [int(a) for a in sys.argv[1:]] or [400, 1600]
    R, theta, ha, hb, g = lh_design()
    p = R.shape[0]
    S0 = [j for j in range(p) if theta[j] != 0]
    Sdeg = sum(1 << j for j in ha)                      # S° = S0 minus masked hubs
    masked_groups = [list(range(j, j + g)) for j in hb]
    basin = [Sdeg] + [Sdeg | (1 << k) for grp in masked_groups for k in grp]
    reps = 40
    rng = np.random.default_rng(20261102)
    print("LH exact Gram: p=%d, g=%d, rho=0.7, psi=0.5, beta=1, sigma=1, c=2; S0=%s, S°=%s, reps=%d" % (p, g, S0, ha, reps))
    for n in ns:
        out = []
        for r in range(reps):
            z, yy = suff_stats(R, theta, 1.0, n, rng)
            M = BVS(R, z, yy, n, S0, Te=1000)
            H = int(np.ceil(512 * max(2500, n, p) / 2500))
            # chain hub odds threshold phi_hub
            lg0, d = M.lg0, M.d
            chain = []
            for x in basin:
                for jb in hb:
                    if not (x >> jb) & 1:
                        chain.append((x, x | (1 << jb)))
            phis = []
            for x, y in chain:
                a0, a1 = lg0[y] - lg0[x], lg0[y] + d[y] - lg0[x] - d[x]
                phis.append(0.0 if a0 >= 0 else (np.inf if a1 <= 0 else -a0 / (a1 - a0)))
            phi_hub = max(phis)
            X = M.draw_pi0(H, rng)
            n_deg = int(np.sum(X == Sdeg))
            isb = np.isin(X, basin)
            Delta = d[X] - d[Sdeg]
            Wout = np.sum(1 + np.exp(np.minimum(Delta[~isb], 700)))
            phi1, forced = pilot_next_phi(d[X], 0.0, H, M.Te)
            w = np.exp(phi1 * (d[X] - d[X].max())); w /= w.sum()
            Xr = X[rng.choice(H, size=H, p=w)]
            bfrac = np.mean(np.isin(Xr, basin))
            hit = {"v": False}
            def rec(states, mech):
                if np.any(states == M.S0): hit["v"] = True
            init_hit = bool(np.any(X == M.S0))
            M.one_round(Xr.copy(), phi1, rng, rec)
            out.append((hit["v"], init_hit, n_deg / H, Wout / max(n_deg, 1), bfrac, phi1, forced, phi_hub, M.post[M.S0], M.pi0[M.S0], M.pi0[Sdeg]))
        a = np.array(out, dtype=float)
        print("n=%6d H=%5d | S0 scored in stage-1 round: %d/%d (S0 among initial draws: %d) | pi(S0) med %.3f | pi0(S0) med %.1e | pi0(S°) min %.3f"
              % (n, H, a[:, 0].sum(), reps, a[:, 1].sum(), np.median(a[:, 8]), np.median(a[:, 9]), a[:, 10].min()))
        print("          frac at S° min %.3f | W_out/n° max %.3g | basin frac after resampling min %.3f | phi1 min/med %.3g/%.3g (forced %d) | phi_hub max %.3g"
              % (a[:, 2].min(), a[:, 3].max(), a[:, 4].min(), a[:, 5].min(), np.median(a[:, 5]), a[:, 6].sum(), a[:, 7].max()))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
