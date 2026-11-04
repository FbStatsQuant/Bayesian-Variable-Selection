"""W2_PC2: R2_C §R5/C16 Jeffreys estimator J-hat on the W1 forced-dispatch coded-grid replica (smc_coded.py, copied
unchanged from W1_PC2).  Records per final island r: A_r = mean d over the N initial iid pi0 particles; B_r = mean d
over the four measured endpoint populations; W_r = Zhat_r/Z.  Checks: E[W_r B_r] = E_pi d, E[A_r] = E_pi0 d,
J-hat -> J, and the C16 tail bound min{1, 4(M2-1)/R' + 16 D^2 M2/(R' eps^2) + D^2/(R' N eps^2)} at R' in {4, 50}
against the empirical exceedance frequency over disjoint island groups.  Design 7 (W1 correlated p = 9), V = top.
Fixed seeds; ~2 min."""
import math
import numpy as np
import smc_coded as sc
from smc_coded import Sampler, design, lse

G, z, Y, n = design(7)
sm = Sampler(G, z, Y, n)
pi, pi0, d = sm.pi, sm.pi0, sm.d
f = sm.feas
J = float(pi[f] @ d[f] - pi0[f] @ d[f])
Ed, Ed0 = float(pi[f] @ d[f]), float(pi0[f] @ d[f])
D = sm.osc
print(f"osc d = D = {D:.4f}; J = {J:.5f}; E_pi d = {Ed:.4f}; E_pi0 d = {Ed0:.4f}")
rng = np.random.default_rng(21)
grid, why, temps = sm.pilot_grid(rng, 'top')
print("grid", why, len(grid) - 1)
L = max(4, math.ceil(math.log2(n + 1)))
N = sc.N_FINAL
Ws, As, Bs = [], [], []
for r in range(300):
    X = sm.draw_pi0(rng, N)
    A = float(d[sm.idx(X)].mean())
    logW = 0.0
    for t in range(1, len(grid)):
        dl = grid[t] - grid[t - 1]; dv = d[sm.idx(X)]; lw = dl * dv
        logW += lse(lw) - math.log(N)
        w = np.exp(lw - lw.max()); X = X[rng.choice(N, size=N, p=w / w.sum())]
        X = sm.round(X, grid[t], rng)
    for _ in range(L):
        X = sm.round(X, 1.0, rng)
    bs = []
    for _ in range(4):
        X = sm.round(X, 1.0, rng); bs.append(d[sm.idx(X)].mean())
    Ws.append(math.exp(logW - sm.logEd)); As.append(A); Bs.append(float(np.mean(bs)))
W, A, B = map(np.array, (Ws, As, Bs))
M2 = float((W ** 2).mean())
se = lambda v: v.std() / math.sqrt(len(v))
print(f"E[W B] = {(W*B).mean():.4f} (se {se(W*B):.4f}) vs E_pi d {Ed:.4f};  E[A] = {A.mean():.4f} (se {se(A):.4f}) vs E_pi0 d {Ed0:.4f}")
Jall = (W * B).sum() / W.sum() - A.mean()
print(f"J-hat over all 300 islands = {Jall:.5f} vs J = {J:.5f};  M2-hat = {M2:.4f};  min J-hat over groups below")
for Rp in (4, 50):
    g = len(W) // Rp
    Jh = np.array([(W[i*Rp:(i+1)*Rp] * B[i*Rp:(i+1)*Rp]).sum() / W[i*Rp:(i+1)*Rp].sum() - A[i*Rp:(i+1)*Rp].mean() for i in range(g)])
    for eps in (0.05, 0.2, 0.5):
        freq = float((np.abs(Jh - J) > eps).mean())
        bnd = min(1.0, 4 * (M2 - 1) / Rp + 16 * D * D * M2 / (Rp * eps ** 2) + D * D / (Rp * N * eps ** 2))
        print(f"R'={Rp:>3} groups={g:>3} eps={eps}: freq {freq:.3f} <= bound {bnd:.3f}: {freq <= bnd + 1e-12}; min J-hat {Jh.min():.4f}")
