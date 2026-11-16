"""Item 1 extras: log-slope c_t of the pooled and per-data-set tails; relation of tail size to π(S₀). -> out/item1_extra.txt"""
import sys, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import spearmanr
for n in (100, 400):
    Z = np.load(f"out/item1_n{n}.npz"); tg = Z["tgrid"]; tail = Z["tail"]; ln = math.log(n)
    pooled = tail.mean(0)
    print(f"n={n}: pooled log-slope of P(n d² > t) between t=a and t=b (per unit t):")
    for a, b in [(2, 4), (4, 6), (6, 8), (8, 10), (10, 12)]:
        ja, jb = int(a / .25) - 1, int(b / .25) - 1
        if pooled[jb] > 0: print(f"   t {a}->{b}: {-(math.log(pooled[jb]) - math.log(pooled[ja]))/(b-a):.2f}")
    # per data set: smallest t with tail <= exp(-c t) for c = 1 and c = 1/2 ; distribution over data sets
    for c in (0.5, 1.0):
        th = np.array([next((tg[j] for j in range(len(tg)) if tail[r, j] <= math.exp(-c * tg[j])), np.inf) for r in range(tail.shape[0])])
        print(f"   t̂_c (smallest grid t with Π(n d²>t) ≤ e^(-c t)), c={c}: q0.5={np.quantile(th,.5):.2f} q0.9={np.quantile(th,.9):.2f} q0.99={np.quantile(th,.99):.2f} max={th.max():.2f};  t̂_c/log n at max = {th.max()/ln:.2f}")
    j6 = int(6 / .25) - 1
    rho = spearmanr(tail[:, j6], Z["pi0"])[0]
    print(f"   Spearman correlation across data sets of Π(n d²>6) with π(S₀): {rho:.2f};  Π(n d²>6) in the 10 data sets with smallest π(S₀): median {np.median(tail[np.argsort(Z['pi0'])[:10], j6]):.3e}; others median {np.median(tail[np.argsort(Z['pi0'])[10:], j6]):.3e}")
