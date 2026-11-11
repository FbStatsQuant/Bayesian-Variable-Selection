"""W3-SAMP numerics v4 (after SW1 #18, #26): non-vacuous LT tail checks on a concentrated target (right sides < 1),
direct test of E[W E_r] <= g (LT-b'), and a fixed-N T sweep for the T-free C bound with explicit Monte Carlo tolerance.
Usage: py -3.13 run_checks_v4.py [seed]  -> RESULTS_v4.txt
"""
import sys
import numpy as np
from samp_sim import Model, run_islands, exact_quantities

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 404
rng = np.random.default_rng(seed)


def ham_model(p, K, S0, a, b, noise, B=2):
    states = [s for s in range(1 << p) if bin(s).count("1") <= K]
    s0 = sum(1 << j for j in S0); ham = np.array([bin(s ^ s0).count("1") for s in states])
    l1 = -a * ham + noise * rng.standard_normal(len(states)); l0 = -b * ham + noise * rng.standard_normal(len(states))
    return Model(p, K, l0, l1 - l0, B=B, S0=s0)


def se3(x): return 3 * x.std(ddof=1) / np.sqrt(len(x))


viol = 0; nontriv = 0
print(f"seed {seed}\n==== LT tail bounds on concentrated targets (only cells with right side < 1 count as non-vacuous) ====")
for a, b in ((5.0, 1.0), (6.0, 2.0)):
    M = ham_model(5, 4, [0, 1], a, b, 0.3); ex = exact_quantities(M)
    g = min(1, ex["kappa0"] + ex["delta"] + (1 - ex["delta"]) * ex["lambda0"])
    R = run_islands(M, [0, 0.5, 1.0], N=4, L=2, I=40000, rng=rng)
    W = R["W"]; E = np.abs(R["rb"] - ex["ind"]).max(1)
    wE = W * E; okw = wE.mean() <= g + se3(wE); viol += int(not okw)
    print(f"[a={a} b={b}] delta={ex['delta']:.3e} o1={ex['o1']:.3e} kappa0={ex['kappa0']:.3e} lambda0={ex['lambda0']:.3e} g={g:.3e}; "
          f"E[W E_r]={wE.mean():.3e} <= g (+3se): {okw}")
    for eps in (0.05, 0.1, 0.2):
        for eta in (0.25, 0.5):
            pW = (W < eta).mean()
            rb = ex["delta"] / (eps * eta) + ex["lambda0"] / eps + pW
            lb = (E >= ex["kappa0"] + 2 * eps).mean()
            ra = ex["delta"] / (eps * eta) + pW; la = (1 - R["A"][:, 0] >= eps).mean()
            rbp = g / (eps * eta) + pW; lbp = (E >= eps).mean()
            for lhs, rhs, nm in ((lb, rb, "LT-b"), (la, ra, "LT-a"), (lbp, rbp, "LT-b'")):
                if rhs < 1:
                    nontriv += 1
                    bad = lhs > rhs + 3 * np.sqrt(max(lhs, 1e-4) / len(W)); viol += int(bad)
                    print(f"   eps={eps} eta={eta} {nm}: {lhs:.4f} <= {rhs:.4f} {'VIOLATION' if bad else 'ok'}")
print(f"non-vacuous LT cells: {nontriv}")

print("\n==== C (T-free) with N fixed (N=2), T varied; tolerance = 3 Monte Carlo standard errors ====")
for a, b in ((4.0, 3.0), (2.5, 1.5)):
    M = ham_model(5, 4, [0, 1], a, b, 0.3); ex = exact_quantities(M)
    s = M.S0; av = M.d - M.d[s]
    bm = (M.pi0 * np.maximum(0, 1 - np.exp(av))).sum(); bp = (M.pi0 * np.maximum(0, np.exp(av) - 1)).sum()
    c = M.pi0[s] / M.pi[s]; beta = 2 * max(bm, bp) / c
    print(f"[a={a} b={b}] delta={ex['delta']:.3e} o0={ex['o0']:.3e} b-={bm:.4f} beta={beta:.4f}")
    for T in (1, 4, 32, 128):
        grid = list(np.linspace(0, 1, T + 1))
        R = run_islands(M, grid, N=2, L=1, I=10000 if T <= 32 else 3000, rng=rng)
        qs = np.array([M.q(ph)[s] for ph in grid]); V = R["Wstage"] * M.pi0[s] / qs[None, :]
        loss = np.maximum(0, V[:, :-1] - V[:, 1:]).sum(1); aw = np.abs(R["W"] - 1)
        ok1 = loss.mean() <= bm + se3(loss); ok2 = aw.mean() <= beta + se3(aw); viol += int(not ok1) + int(not ok2)
        print(f"   T={T:3d}: E loss={loss.mean():.4f} (3se {se3(loss):.4f}) <= b-={bm:.4f}: {ok1}; "
              f"E|W-1|={aw.mean():.4f} (3se {se3(aw):.4f}) <= beta={beta:.4f}: {ok2}")
print(f"\nOVERALL violations = {viol}")
