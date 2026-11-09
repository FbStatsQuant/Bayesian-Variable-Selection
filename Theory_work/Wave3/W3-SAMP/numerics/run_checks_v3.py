"""W3-SAMP numerics v3: falsification of the sharpness-gate amendments (STATEMENT v3).
C-iii: telescoping budget E sum_t (V_{t-1}-V_t)^+ <= b_-, E|W-1| <= beta <= 2 max(delta,(1-delta) o0); C-iv: E E_r <= g + beta/2,
bias |E p_hat(j) - PIP_j| <= beta/2; TR: exact minorization K_sigma >= pi/M for random fixed orders; E E_r <= g + e_L.
Usage: py -3.13 run_checks_v3.py [seed] -> RESULTS_v3.txt
"""
import sys
import numpy as np
from samp_sim import Model, run_islands, exact_quantities

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 31
rng = np.random.default_rng(seed)
src = open("run_checks_v2.py", encoding="utf-8").read()
exec(src.split("def zs(")[0].split("seed = int")[0])  # imports + regression_model only
exec("def regression_model" + src.split("def regression_model")[1].split("def zs(")[0])


def ham_model(p, K, S0, a, b, noise, B=2, extra=None):
    states = [s for s in range(1 << p) if bin(s).count("1") <= K]
    s0 = sum(1 << j for j in S0); ham = np.array([bin(s ^ s0).count("1") for s in states])
    l1 = -a * ham + noise * rng.standard_normal(len(states)); l0 = -b * ham + noise * rng.standard_normal(len(states))
    if extra is not None: l0, l1 = extra(states, l0, l1)
    return Model(p, K, l0, l1 - l0, B=B, S0=s0)


def betas(M):
    s = M.S0; a = M.d - M.d[s]
    bm = (M.pi0 * np.maximum(0, 1 - np.exp(a))).sum(); bp = (M.pi0 * np.maximum(0, np.exp(a) - 1)).sum()
    c = M.pi0[s] / M.pi[s]
    return bm, bp, c, 2 * max(bm, bp) / c


viol = 0
print(f"seed {seed}\n==== C-iii / C-iv (T-free) ====")
cases = [("ham-conc", lambda: ham_model(5, 4, [0, 1], 4.0, 3.0, 0.3)),
         ("ham-mid", lambda: ham_model(5, 4, [0, 1], 2.5, 1.5, 0.5)),
         ("ham-cap", lambda: ham_model(5, 2, [0, 1], 3.0, 1.0, 0.5)),
         ("reg-n400", lambda: regression_model(n=400, p=6, S0=[0, 3], beta=[0.5, 0.4], rho=0.0, blocks=[[0, 1, 2], [3, 4, 5]], B=2, rng=rng)),
         ("reg-AR0.5", lambda: regression_model(n=300, p=6, S0=[1, 4], beta=[0.5, -0.4], rho=0.5, blocks=[[0, 1, 2], [3, 4, 5]], B=2, rng=rng))]
for name, mk in cases:
    M = mk(); ex = exact_quantities(M); bm, bp, c, beta = betas(M)
    g = min(1, ex["kappa0"] + ex["delta"] + (1 - ex["delta"]) * ex["lambda0"])
    b2 = 2 * max(ex["delta"], (1 - ex["delta"]) * ex["o0"])
    viol += beta > b2 + 1e-12
    print(f"[{name}] delta={ex['delta']:.3e} o0={ex['o0']:.3e} beta={beta:.3e} <= 2max(delta,(1-delta)o0)={b2:.3e}; g={g:.3e}")
    for T, N in ((1, 1), (4, 2), (32, 2), (128, 1)):
        grid = list(np.linspace(0, 1, T + 1))
        R = run_islands(M, grid, N=N, L=2, I=20000 if T <= 32 else 4000, rng=rng)
        W = R["W"]; qs = np.array([M.q(ph)[M.S0] for ph in grid])
        V = R["Wstage"] * M.pi0[M.S0] / qs[None, :]
        loss = np.maximum(0, V[:, :-1] - V[:, 1:]).sum(1)
        E = np.abs(R["rb"] - ex["ind"]).max(1)
        se = lambda x: 3 * x.std() / np.sqrt(len(x))
        ok1 = loss.mean() <= bm + se(loss) + 1e-12; ok2 = np.abs(W - 1).mean() <= beta + se(np.abs(W - 1)) + 1e-12
        ok3 = E.mean() <= g + beta / 2 + se(E) + 1e-12
        bias = np.abs(R["rb"].mean(0) - ex["pip"]).max(); ok4 = bias <= beta / 2 + 3 * R["rb"].std(0).max() / np.sqrt(len(W)) + 1e-12
        viol += (not ok1) + (not ok2) + (not ok3) + (not ok4)
        print(f"   T={T:3d} N={N}: E loss={loss.mean():.4f}<=b-={bm:.4f}:{ok1}; E|W-1|={np.abs(W-1).mean():.4f}<=beta:{ok2}; "
              f"E E_r={E.mean():.4f}<=g+beta/2={g+beta/2:.4f}:{ok3}; max bias={bias:.4f}<=beta/2={beta/2:.4f}:{ok4}")

print("\n==== TR ====")
def near(states, l0, l1):
    s0, s1 = 0b00011, 0b00111
    l0 = np.full(len(states), -6.0); l1 = np.full(len(states), -9.0)
    i0, i1 = states.index(s0), states.index(s1)
    l1[i0] = 0.0; l1[i1] = -8.0; l0[i0] = -14.0; l0[i1] = 0.0
    return l0, l1
def overlap(states, l0, l1):  # start proportional to posterior off the truth (domination), moderate pi0(S0)
    s0 = 0b00011; l1 = l1.copy(); i0 = states.index(s0)
    l0 = l1.copy(); l0[i0] = l1[i0] - 1.5
    return l0, l1
for name, mk, L in (("ham-mid", lambda: ham_model(5, 4, [0, 1], 2.5, 1.5, 0.5), 3),
                    ("overlap", lambda: ham_model(5, 4, [0, 1], 3.0, 0.0, 0.3, extra=overlap), 3),
                    ("near", lambda: ham_model(5, 4, [0, 1], 0, 0, 0, extra=near), 20)):
    M = mk(); ex = exact_quantities(M)
    Mx = (M.pi / M.pi0).max(); Ks, _, _ = M.kernels(1.0)
    worst = np.inf
    for _ in range(200):
        Kx = np.eye(M.n)
        for l in rng.permutation(M.m): Kx = Kx @ Ks[l]
        worst = min(worst, (Kx / M.pi[None, :]).min())
    okm = worst >= 1 / Mx - 1e-12; viol += not okm
    g = min(1, ex["kappa0"] + ex["delta"] + (1 - ex["delta"]) * ex["lambda0"]); eL = (1 - 1 / Mx) ** L
    R = run_islands(M, [0, 1.0], N=4, L=L, I=4000, rng=rng)
    E = np.abs(R["rb"] - ex["ind"]).max(1)
    ok = E.mean() <= min(1, g + eL) + 3 * E.std() / np.sqrt(len(E)) + 1e-12; viol += not ok
    print(f"[{name}] M={Mx:.3e} L={L} e_L={eL:.3e} g={g:.3e}: min_sigma min K_sigma/pi={worst:.3e} >= 1/M={1/Mx:.3e}:{okm}; "
          f"E E_r={E.mean():.4f} <= min(1,g+e_L)={min(1,g+eL):.4f}:{ok}; median W={np.median(R['W']):.2e}")
print(f"\nOVERALL violations = {viol}")
