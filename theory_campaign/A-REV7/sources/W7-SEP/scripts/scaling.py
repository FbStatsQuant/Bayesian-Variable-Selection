"""W7-SEP: budget scaling on LH (exact Gram) at moderate/large p, using W4-T38FULL's exact start-law code (lh_w4.py).

For c in {2, 3}, groups of g = 9 (so g <= B < 2g), rho = 0.7, psi = 0.5, one visible hub, the rest null groups,
p = 9 G with G in {12, 24, 48, 96} (p <= n - 1), n in {1000, 4000}:
  * log pi0(S0) exactly (block-profile convolution with S0 forced: log gamma0(S0) - log Z0), Mstat, Q* = 1/pi0(S0);
  * Q_f (minimal final-run iid budget 4 N0 (L + 6)) and Q_f * pi0(S0) = expected number of iid hits;
  * LS0: production local search from the exact start mode; whether it scores S0; number of score evaluations used;
  * v3 ceiling proxy (n + p)(p + B) log2(n)^2 (T32-type, CONJECTURE) for orientation.
Seed fixed. Output: ../results/scaling.txt
"""
import math, numpy as np
from scipy.special import logsumexp
import lh_w4 as W

rng = np.random.default_rng(20261104)
rows = ["W7-SEP scaling.py, seed 20261104; LH exact Gram, g = 9, rho = 0.7, psi = 0.5, visible beta = 1.0; 3 reps per cell",
        "",
        "c | n | p | med log10 pi0(S0) | med Mstat | med log10 Q* | log10 Q_f | med Q_f*pi0(S0) | LS0 scores S0 | med LS0 score evals | log10 v3-ceiling proxy"]

def one(n, c, G, g=9, rho=0.7, psi=0.5):
    pairs = [(2 * i, 2 * i + 1, psi) for i in range(c)]
    vis = 2 * c
    Sig = W.lh_sigma(G, g, rho, pairs); p = G * g
    theta = np.zeros(p); betas = [1.4, -1.0, 1.2][:c]
    for i, (ga, gb, ps) in enumerate(pairs):
        theta[ga * g] = betas[i]; theta[gb * g] = -ps * betas[i]
    theta[vis * g] = 1.0
    S0 = tuple(sorted(np.flatnonzero(theta)))
    Sstar = tuple(sorted(set(S0) - {gb * g for (_, gb, _) in pairs}))
    A = rng.standard_normal((n, p + 1)); A[:, 0] = 1.0
    Qc = np.linalg.qr(A)[0][:, 1:p + 1]
    X = math.sqrt(n - 1) * Qc @ np.linalg.cholesky(Sig).T
    yr = X @ theta + rng.standard_normal(n); yc = yr - yr.mean(); y = yc / math.sqrt(yc @ yc / (n - 1))
    sc = W.Scorer(X, y)
    blocks = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    tabs = W.block_tables(sc, blocks)
    mode, pi0_S0 = W.pi0_mode_and_mass(sc, blocks, tabs, S0)
    ell = math.ceil(math.log2(n + p + 1))
    scored, end, moves = W.local_search(sc, mode, ell)
    nevals = moves + 1  # scans
    evals = len(scored)
    N0 = max(2500, n, p); L = max(4, math.ceil(math.log2(n + 1))); Qf = 4 * N0 * (L + 6)
    l0 = math.log(pi0_S0)
    return dict(l0=l0, M=l0 + c * math.log(p) + 0.5 * c * math.log(n), Qf=Qf, ls=(S0 in scored), evals=evals,
                ceil=(n + p) * (p + 16) * math.log2(n) ** 2, p=p, mode_ok=(mode == Sstar))

for c in (2, 3):
    for n in (1000, 4000):
        for G in (12, 24, 48, 96):
            if G * 9 > n - 1:
                continue
            R = [one(n, c, G) for _ in range(3)]
            med = lambda k: float(np.median([r[k] for r in R]))
            rows.append(f"{c} | {n} | {R[0]['p']} | {med('l0')/math.log(10):.2f} | {med('M'):.2f} | {-med('l0')/math.log(10):.2f} | "
                        f"{math.log10(R[0]['Qf']):.2f} | {float(np.median([r['Qf']*math.exp(r['l0']) for r in R])):.2e} | "
                        f"{sum(r['ls'] for r in R)}/3 | {med('evals'):.0f} | {math.log10(R[0]['ceil']):.2f}")
            print(rows[-1], flush=True)
open("../results/scaling.txt", "w").write("\n".join(rows) + "\n")
