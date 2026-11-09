"""W3-SAMP lemma-check numerics v2 (SL1 suggestions): regression-realisable targets (T12 §0 score and prior, block-product
start), direct test of the stopped-sum inequality of Theorem C, heavy-tailed evidence, cap, MR/ST/LT/C/D re-checks.
Usage: py -3.13 run_checks_v2.py [seed]  -> stdout (saved as RESULTS_v2.txt)
"""
import sys, itertools, math
import numpy as np
from samp_sim import Model, run_islands, exact_quantities

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rng = np.random.default_rng(seed)


def regression_model(n, p, S0, beta, rho, blocks, B, rng):
    """T12 §0 target on standardised data; start gamma_0 = varpi * prod_b r_b(S n C_b), r_b = BF; d = log BF - sum log r_b."""
    C = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    X = rng.standard_normal((n, p)) @ np.linalg.cholesky(C).T
    y = X[:, S0] @ np.asarray(beta) + rng.standard_normal(n)
    X = X - X.mean(0); X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    y = y - y.mean(); y = y / np.sqrt((y ** 2).sum() / (n - 1))
    a0 = b0 = 0.01; nu = a0 + n / 2; K = min(p, n // 2)
    yy = y @ y

    def logBF(S):
        S = list(S)
        if not S: return 0.0
        G = X[:, S].T @ X[:, S]; z = X[:, S].T @ y; k = len(S)
        H = (n + 1) * G + np.eye(k)
        DS = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
        Q = yy - n * z @ np.linalg.solve(H, z)
        return -0.5 * DS - nu * (math.log(2 * b0 + Q) - math.log(2 * b0 + yy))

    def logprior(k):  # w(k) = 1/2 / C(2p-1, k) (normalisation irrelevant)
        return math.log(0.5) - (math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k))

    states = [s for s in range(1 << p) if bin(s).count("1") <= K]
    lbf = np.array([logBF([j for j in range(p) if s >> j & 1]) for s in states])
    lpr = np.array([logprior(bin(s).count("1")) for s in states])
    lr = np.zeros(len(states))
    for i, s in enumerate(states):
        for b in blocks:
            U = [j for j in b if s >> j & 1]
            lr[i] += logBF(U)
    lg0 = lpr + lr; d = lbf - lr
    return Model(p, K, lg0, d, B=B, S0=sum(1 << j for j in S0))


def zs(x, target):
    return (x.mean() - target) / (x.std(ddof=1) / np.sqrt(len(x)) + 1e-300)

print(f"seed {seed}")
viol = 0; maxz = 0
for name, kw in [("reg-indep-blocks", dict(n=80, p=6, S0=[0, 3], beta=[0.5, 0.4], rho=0.0, blocks=[[0, 1, 2], [3, 4, 5]], B=2)),
                 ("reg-AR0.7-split", dict(n=60, p=6, S0=[1, 3], beta=[0.45, -0.35], rho=0.7, blocks=[[0, 1, 2], [3, 4, 5]], B=2)),
                 ("reg-weak", dict(n=40, p=5, S0=[0, 2], beta=[0.25, 0.2], rho=0.5, blocks=[[0, 1], [2, 3, 4]], B=1))]:
    M = regression_model(rng=rng, **kw)
    ex = exact_quantities(M)
    print(f"\n[{name}] |Omega|={M.n} delta={ex['delta']:.3e} o1={ex['o1']:.3e} o0={ex['o0']:.3e} dbar={ex['dbar']:.3e} "
          f"pi0(S0)={M.pi0[M.S0]:.3e} osc(d)={M.d.max()-M.d.min():.2f} inv_err={ex['inv_err']:.1e}")
    print(f"  ST: kappa_sum={ex['kappa_sum']:.3e}<=o1:{ex['kappa_sum']<=ex['o1']+1e-15}; max non-Gibbs leave={ex['leave'][M.p:].max():.3e}<=o1:"
          f"{ex['leave'][M.p:].max()<=ex['o1']+1e-15}; lambda0={ex['lambda0']:.3e}<=(B+3)o1={(M.B+3)*ex['o1']:.3e}")
    for T in (1, 3, 10):
        grid = list(np.linspace(0, 1, T + 1)); N = 3
        R = run_islands(M, grid, N=N, L=2, I=30000, rng=rng)
        W = R["W"]
        z = [zs(W, 1.0)] + [zs(W * R["rb"][:, j], ex["pip"][j]) for j in range(M.p)] + [zs(W * (1 - R["A"][:, q]), ex["delta"]) for q in range(5)]
        for t in range(1, T + 1):
            z.append(zs(R["Wstage"][:, t] * (1 - R["Abr"][:, t]), 1 - M.q(grid[t])[M.S0]))
        maxz = max(maxz, np.max(np.abs(z)))
        x = 1 - R["Abr"]; V = np.cumsum(x, axis=1); Vprev = np.hstack([np.zeros((len(W), 1)), V[:, :-1]])
        U = V[:, -1]
        line = f"  T={T:2d}: max|z|={np.max(np.abs(z)):.2f};"
        for u in (0.25, 0.5):
            Y = (x * (Vprev <= u)).sum(1)
            ptw = np.all(np.minimum(U, u) <= Y + 1e-12)
            # stagewise pointwise bound x_t 1{V_{t-1}<=u} <= (1+dbar)/(1-u) W_t x_t
            stg = np.all(x * (Vprev <= u) <= (1 + ex["dbar"]) / (1 - u) * R["Wstage"] * x + 1e-12)
            bY = (T + 1) * ex["dbar"] / (1 - u)
            viol += (not ptw) + (not stg) + (Y.mean() > bY + 3 * Y.std() / np.sqrt(len(Y)))
            line += f" u={u}: min(U,u)<=Y all:{ptw}, stage bound all:{stg}, E[Y]={Y.mean():.4f}<= {bY:.4f};"
        prod = (M.pi[M.S0] / M.pi0[M.S0]) * np.prod(R["Abr"][:, :-1], axis=1)
        ci = np.all(W >= prod * (1 - 1e-12))
        eW = np.abs(W - 1).mean(); bW = 2 * ex["o1"] + 8 * (T + 1) * ex["dbar"]
        err = np.abs(R["rb"] - ex["ind"]).max(1)
        viol += (not ci) + (eW > bW + 3 * np.abs(W - 1).std() / np.sqrt(len(W)))
        print(line + f" C-i all:{ci}; E|W-1|={eW:.4f}<= {bW:.4f}; max W={W.max():.2f}; P(RB err>=kappa0+.1)={(err>=ex['kappa0']+.1).mean():.4f}; "
              f"P(MPM wrong)={(np.abs(np.where(R['rb']>0.5,1,0)-ex['ind']).max(1)>0).mean():.4f}")
    pm = (R["draws_hit"] == 0).mean(); th = (1 - M.pi0[M.S0]) ** R["D"]
    print(f"  D: P(no draw=S0) emp {pm:.4f} vs exact {th:.4f} (D_r={R['D']})")

# heavy-tailed evidence: start far from target on part of the space, W has rare large values
print("\n[heavy-tail W] artificial target, one rare state with huge pi/pi0")
states_p, K = 5, 4
M0 = Model(states_p, K, np.zeros(31), np.zeros(31), B=1, S0=0b00011)
lg0 = -1.0 * np.array([bin(s ^ 0b00011).count("1") for s in M0.states]); l1 = -2.0 * np.array([bin(s ^ 0b00011).count("1") for s in M0.states])
i_r = M0.idx[0b11100]; lg0[i_r] = -12.0; l1[i_r] = -3.0
M = Model(states_p, K, lg0, l1 - lg0, B=1, S0=0b00011)
ex = exact_quantities(M)
R = run_islands(M, [0, 0.5, 1.0], N=2, L=1, I=100000, rng=rng)
W = R["W"]
z = [zs(W, 1.0)] + [zs(W * R["rb"][:, j], ex["pip"][j]) for j in range(M.p)]
maxz = max(maxz, np.max(np.abs(z)))
print(f"  delta={ex['delta']:.3e}; max W={W.max():.1f}; P(W>5)={(W>5).mean():.2e}; identities max|z|={np.max(np.abs(z)):.2f}")
print(f"\nOVERALL: identity max|z| = {maxz:.2f} (rule <= 4.5); inequality violations = {viol}")
