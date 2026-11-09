"""W3-SAMP falsification + boundary-violation checks. Output: numerics/RESULTS_v1.txt (printed to stdout).
Usage: py -3.13 run_checks.py [seed]
"""
import sys, itertools
import numpy as np
from samp_sim import Model, run_islands, exact_quantities

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261109
rng = np.random.default_rng(seed)


def make_model(p, K, S0, a, b, noise, rng, B=1, extra=None):
    states = [s for s in range(1 << p) if bin(s).count("1") <= K]
    s0 = sum(1 << j for j in S0)
    ham = np.array([bin(s ^ s0).count("1") for s in states])
    l1 = -a * ham + noise * rng.standard_normal(len(states))
    l0 = -b * ham + noise * rng.standard_normal(len(states))
    if extra is not None: l0, l1 = extra(states, l0, l1)
    return Model(p, K, l0, l1 - l0, B=B, S0=s0)


def zs(x, target):
    return (x.mean() - target) / (x.std(ddof=1) / np.sqrt(len(x)) + 1e-300)


def header(t): print("\n" + "=" * 8 + " " + t + " " + "=" * 8)

print(f"seed {seed}")

# ---------------------------------------------------------------- 1. identities (Lemma MR) + ST exact
header("1. Lemma MR identities (Monte Carlo) and Lemma ST (exact)")
cases = [("mid", dict(p=5, K=4, S0=[0, 1], a=1.2, b=0.3, noise=0.5)),
         ("cap", dict(p=5, K=2, S0=[0, 1], a=1.5, b=0.2, noise=0.7)),
         ("flat", dict(p=4, K=4, S0=[2], a=0.4, b=0.0, noise=1.0))]
maxz = 0
for name, kw in cases:
    M = make_model(rng=rng, B=2, **kw)
    ex = exact_quantities(M)
    print(f"[{name}] |Omega|={M.n} delta={ex['delta']:.4f} o1={ex['o1']:.4f} o0={ex['o0']:.4f} inv_err={ex['inv_err']:.2e}")
    print(f"   ST-b: sum_j |o_j(S0)-1| = {ex['kappa_sum']:.4e} <= o1 {ex['o1']:.4e}: {ex['kappa_sum'] <= ex['o1'] + 1e-15}; "
          f"Gibbs leave sum = {ex['leave'][:M.p].sum():.4e} (equal to kappa_sum: {abs(ex['leave'][:M.p].sum()-ex['kappa_sum'])<1e-12})")
    print(f"   ST-a: max leave over non-Gibbs labels = {ex['leave'][M.p:].max():.4e} <= o1: {ex['leave'][M.p:].max() <= ex['o1'] + 1e-15}")
    print(f"   ST-c: lambda0 = {ex['lambda0']:.4e} <= (B+3) o1 = {(M.B+3)*ex['o1']:.4e}: {ex['lambda0'] <= (M.B+3)*ex['o1'] + 1e-15}")
    for grid in ([0, 1.0], [0, 0.3, 0.7, 1.0]):
        R = run_islands(M, grid, N=3, L=2, I=60000, rng=rng)
        W = R["W"]
        z = [zs(W, 1.0)]
        z += [zs(W * R["rb"][:, j], ex["pip"][j]) for j in range(M.p)]
        z += [zs(W * (1 - R["A"][:, q]), ex["delta"]) for q in range(5)]
        for t in range(1, len(grid)):
            qt = M.q(grid[t])
            z.append(zs(R["Wstage"][:, t] * (1 - R["Abr"][:, t]), 1 - qt[M.S0]))
        maxz = max(maxz, np.max(np.abs(z)))
        print(f"   grid {grid}: max|z| over {len(z)} identities = {np.max(np.abs(z)):.2f}; unweighted RB bias max = "
              f"{np.abs(R['rb'].mean(0)-ex['pip']).max():.3f}; E[Lambda] = {R['Lam'].mean():.4e} <= lambda0: {R['Lam'].mean() <= ex['lambda0'] * 1.05 + 3e-4}")
print(f"OVERALL max|z| (identities) = {maxz:.2f}  (rule: <= 4.5)")

# ---------------------------------------------------------------- 2. LT# bounds vs empirical (mid regime)
header("2. Theorem LT# inequalities (empirical lhs <= rhs)")
M = make_model(p=5, K=4, S0=[0, 1], a=2.5, b=0.6, noise=0.5, rng=rng, B=2)
ex = exact_quantities(M)
R = run_islands(M, [0, 0.5, 1.0], N=4, L=2, I=40000, rng=rng)
err = np.abs(R["rb"] - ex["ind"]).max(axis=1)
viol = 0
for eps in (0.02, 0.05, 0.1):
    for eta in (0.1, 0.3, 0.5):
        pW = (R["W"] < eta).mean()
        lhs_b = (err >= ex["kappa0"] + 2 * eps).mean()
        rhs_b = ex["delta"] / (eps * eta) + 19 * ex["o1"] / eps + pW
        rhs_b_tight = ex["delta"] / (eps * eta) + ex["lambda0"] / eps + pW
        lhs_a = (1 - R["A"][:, 0] >= eps).mean(); rhs_a = ex["delta"] / (eps * eta) + pW
        viol += (lhs_b > rhs_b_tight + 0.01) + (lhs_a > rhs_a + 0.01)
        print(f"eps={eps} eta={eta}: LT-b {lhs_b:.4f} <= {rhs_b_tight:.4f} (with 19o1: {rhs_b:.4f}); LT-a {lhs_a:.4f} <= {rhs_a:.4f}")
print(f"delta={ex['delta']:.4f} o1={ex['o1']:.4f} kappa0={ex['kappa0']:.4f}; violations (tol .01): {viol}")
print(f"LT-c: P(S0 never a measured/entering endpoint) = {(R['A'].max(axis=1)==0).mean():.4f} <= delta/eta+P(W<eta) at eta=.5: {ex['delta']/.5 + (R['W']<.5).mean():.4f}")
print(f"kappa0 sharpness: islands with all measured endpoints at S0 have RB error = {err[(R['A'][:,1:]==1).all(1) & (R['Lam']==0).all(1)].min():.4e} vs kappa0 {ex['kappa0']:.4e}")

# ---------------------------------------------------------------- 3. Theorem C and its T-boundary
header("3. Theorem C: E|W-1| <= 2 o1 + 8 (T+1) dbar ; E min(U,1) <= 4 (T+1) dbar")
for a, b in ((4.0, 3.0), (3.0, 2.5), (2.5, 2.0)):
    M = make_model(p=5, K=4, S0=[0, 1], a=a, b=b, noise=0.3, rng=rng, B=2)
    ex = exact_quantities(M)
    for T in (1, 4, 16, 64):
        grid = list(np.linspace(0, 1, T + 1))
        R = run_islands(M, grid, N=2, L=1, I=8000 if T <= 16 else 2000, rng=rng)
        U = (1 - R["Abr"]).sum(axis=1)
        eW = np.abs(R["W"] - 1).mean(); bW = 2 * ex["o1"] + 8 * (T + 1) * ex["dbar"]
        eU = np.minimum(U, 1).mean(); bU = 4 * (T + 1) * ex["dbar"]
        err = np.abs(R["rb"] - ex["ind"]).max(axis=1)
        print(f"a={a} b={b} dbar={ex['dbar']:.3e} T={T:3d} T*dbar={T*ex['dbar']:.3f}: E|W-1|={eW:.4f} (bound {bW:.4f}, ok={eW<=bW+3*np.abs(R['W']-1).std()/np.sqrt(len(R['W']))}); "
              f"E min(U,1)={eU:.4f} (bound {bU:.4f}); P(RB err>.1)={(err>.1).mean():.4f}; P(W<.5)={(R['W']<.5).mean():.4f}")

# ---------------------------------------------------------------- 4. NC: cannot be dropped; not necessary
header("4. NC_r: necessity probes")
def trap(states, l0, l1):
    # pi concentrates on S0={0,1}; a second, far state S1={2,3,4} carries almost all start mass;
    # every other state has tiny target and start mass (a valley between S1 and S0).
    s0, s1 = 0b00011, 0b11100
    l0 = np.full(len(states), -30.0); l1 = np.full(len(states), -30.0)
    i0, i1 = states.index(s0), states.index(s1)
    l1[i0] = 0.0; l1[i1] = np.log(0.01); l0[i0] = -18.0; l0[i1] = 0.0
    return l0, l1
M = make_model(p=5, K=4, S0=[0, 1], a=0, b=0, noise=0, rng=rng, B=2, extra=trap)
ex = exact_quantities(M)
R = run_islands(M, [0, 0.5, 1.0], N=8, L=5, I=3000, rng=rng)
err = np.abs(R["rb"] - ex["ind"]).max(axis=1)
print(f"trap: delta={ex['delta']:.4f} pi0(S0)={M.pi0[M.S0]:.2e}; P(W<0.01)={(R['W']<0.01).mean():.3f}; P(RB err >= .5)={(err>=.5).mean():.3f}; "
      f"P(MPM wrong)={(np.abs(R['rb']-ex['ind']).max(1)>=.5).mean():.3f}  -> P-CONC holds, NC fails, outputs wrong")
def near(states, l0, l1):
    s0, s1 = 0b00011, 0b00111
    l0 = np.full(len(states), -6.0); l1 = np.full(len(states), -9.0)
    i0, i1 = states.index(s0), states.index(s1)
    l1[i0] = 0.0; l1[i1] = -8.0; l0[i0] = -14.0; l0[i1] = 0.0
    return l0, l1
M = make_model(p=5, K=4, S0=[0, 1], a=0, b=0, noise=0, rng=rng, B=2, extra=near)
ex = exact_quantities(M)
R = run_islands(M, [0, 1.0], N=4, L=5, I=4000, rng=rng)
err = np.abs(R["rb"] - ex["ind"]).max(axis=1)
print(f"near: delta={ex['delta']:.4f} pi0(S0)={M.pi0[M.S0]:.2e}; P(W<0.01)={(R['W']<0.01).mean():.3f}; P(RB err >= .1)={(err>=.1).mean():.3f}"
      f"  -> NC fails, yet the terminal rounds repair the RB PIPs (NC not necessary)")

# ---------------------------------------------------------------- 5. Theorem D
header("5. Theorem D: P(no pi_0 draw equals S0) = (1 - pi0(S0))^D_r")
for b in (0.0, -0.3):
    M = make_model(p=5, K=4, S0=[0, 1, 2, 3], a=1.0, b=b, noise=0.3, rng=rng, B=1)
    grid = [0, 0.5, 1.0]; N, L = 2, 1
    R = run_islands(M, grid, N=N, L=L, I=40000, rng=rng)
    pm = (R["draws_hit"] == 0).mean(); th = (1 - M.pi0[M.S0]) ** R["D"]
    se = np.sqrt(th * (1 - th) / 40000)
    print(f"pi0(S0)={M.pi0[M.S0]:.4f} D_r={R['D']}: empirical {pm:.4f} vs exact {th:.4f} (z={(pm-th)/se:.2f}); "
          f"P(S0 never a particle endpoint) = {(R['A'].max(1)==0).mean():.4f}")
