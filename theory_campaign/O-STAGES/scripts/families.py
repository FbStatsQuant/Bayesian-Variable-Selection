"""Exact population grid on small-p block families (BO favourable; masked: proxy split, cancellation pair).
Uses bvs_exact.all_log_m / log_prior_size (copied from theory/W2-T26) with an EXPLICIT partition (Prop. P(i) of
F-DRAFT: the theory holds for any partition). Seeds fixed below. Usage: python families.py > ../results/families.txt
"""
import sys, numpy as np
from math import log, log2, sqrt, ceil
from scipy.special import logsumexp
from bvs_exact import all_log_m, log_prior_size, popcount, standardise
from grid_core import greedy_grid, F_from, N_halving, THR

WS = np.linspace(1.0, 2.0, 2001)


def build(X, y, blocks):
    n, p = X.shape
    K = min(p, n // 2)
    masks = np.arange(1 << p, dtype=np.int64); size = popcount(masks); feas = size <= K
    lm = all_log_m(X, y); lbf = lm - lm[0]
    lw = log_prior_size(p, K); logw = np.where(feas, lw[np.minimum(size, p)], -np.inf)
    slr = np.zeros(1 << p)
    for b in blocks:
        M = int(sum(1 << j for j in b)); slr += lbf[masks & M]
    lg0 = np.where(feas, logw + slr, -np.inf); d = np.where(feas, lbf - slr, 0.0)
    return lg0, d


def analyse(lg0, d, S0mask, label, R2=None, n=None, p=None):
    F = F_from(lg0, d)
    g = greedy_grid(F); T = len(g) - 1
    lq = lambda t, S: lg0[S] + t * d[S] - F(t)
    pi0S0, piS0 = np.exp(lq(0, S0mask)), np.exp(lq(1, S0mask))
    Delta = max(1 - pi0S0, 1 - piS0)
    qw = np.array([np.exp(lq(w, S0mask)) for w in WS])
    # Theorem F sandwich: w_- = first w where q_w(S0) < 0.9/(1-Delta) (sufficient side), w_+ = first w with q_w < 0.9(1-Delta)^2
    def first_below(level):
        idx = np.nonzero(qw < level)[0]
        return 2.0 if len(idx) == 0 else WS[idx[0]]
    w_minus = first_below(THR / (1 - Delta)) if Delta < 0.1 else 1.0
    w_plus = first_below(THR * (1 - Delta) ** 2)
    w_hat = first_below(THR)
    Nm, Np, Nh = N_halving(w_minus), N_halving(w_plus), N_halving(w_hat)
    S_start = int(np.nanargmax(lg0)); A0 = lg0[S_start] - lg0[S0mask]
    out = dict(label=label, T=T, Delta=Delta, pi0S0=pi0S0, piS0=piS0, w_minus=w_minus, w_plus=w_plus, w_hat=w_hat,
               N_wminus=Nm, N_wplus=Np, N_what=Nh, A0=A0, start=S_start)
    if R2 is not None:
        gg = log(sqrt(n) / 9) / (R2 * log(p))
        out['g'] = gg; out['Wprime'] = 1 if gg >= 1 else ceil(log2(1 + 1 / gg)) if gg > 0 else None
    # pair dominance on [0, 2] for masked cases
    if S_start != S0mask:
        ts = np.linspace(0, 2, 401)
        out['pair_out_max'] = max(1 - np.exp(lq(t, S_start)) - np.exp(lq(t, S0mask)) for t in ts)
    return out, g


def make_BO(rng, n, p, blocks):
    X = rng.standard_normal((n, p)); X = (X - X.mean(0)) / X.std(0, ddof=1)
    X1 = X[:, blocks[0]]
    for b in blocks[1:]:
        X[:, b] -= X1 @ np.linalg.solve(X1.T @ X1, X1.T @ X[:, b])
    return (X - X.mean(0)) / X.std(0, ddof=1)


def fmt(o):
    s = (f"{o['label']:<44} T*={o['T']:3d}  Delta={o['Delta']:.3g}  pi0(S0)={o['pi0S0']:.3g}  pi(S0)={o['piS0']:.3g}  "
         f"w-={o['w_minus']:.3f} w^={o['w_hat']:.3f} w+={o['w_plus']:.3f}  N(w-)={o['N_wminus']} N(w^)={o['N_what']} N(w+)={o['N_wplus']}")
    if 'g' in o: s += f"  g={o['g']:.3f} W'={o['Wprime']}"
    if 'pair_out_max' in o: s += f"  A0={o['A0']:.2f} log2A0+7.7={log2(max(o['A0'],1e-9))+7.7:.1f} pair_out_max={o['pair_out_max']:.3g}"
    return s


if __name__ == '__main__':
    rows = []
    p = 12; blocks = [list(range(6)), list(range(6, 12))]
    print("=== BO favourable family (p = 12, two blocks of 6, X_b1' X_b2 = 0 exactly) ===")
    for n in [200, 800, 3200, 12800]:
        for cfg, (S0, th) in enumerate([([0, 6], 1.5), ([0, 6], 0.6), ([0, 1], 1.5)]):
            for rep in range(3):
                rng = np.random.default_rng(20261102 + 1000 * n + 10 * cfg + rep)
                X = make_BO(rng, n, p, blocks)
                mu = th * X[:, S0].sum(1); yr = mu + rng.standard_normal(n)
                y = (yr - yr.mean()) / yr.std(ddof=1)
                R2 = float((mu - mu.mean()) @ (mu - mu.mean()) / ((mu - mu.mean()) @ (mu - mu.mean()) + (n - 1)))
                lg0, d = build(X, y, blocks)
                o, g = analyse(lg0, d, int(sum(1 << j for j in S0)), f"BO n={n} S0={S0} th={th} rep{rep}", R2, n, p)
                print(fmt(o)); rows.append(o); sys.stdout.flush()
    print("\n=== masked: proxy split (truth {0}; x6 = 0.9 x0 + noise, other block) ===")
    for n in [200, 800, 3200]:
        for rep in range(2):
            rng = np.random.default_rng(777 + n + rep)
            X = rng.standard_normal((n, p)); X[:, 6] = 0.9 * X[:, 0] + sqrt(1 - 0.81) * X[:, 6]
            X = (X - X.mean(0)) / X.std(0, ddof=1)
            yr = 1.5 * X[:, 0] + rng.standard_normal(n); y = (yr - yr.mean()) / yr.std(ddof=1)
            lg0, d = build(X, y, blocks)
            o, g = analyse(lg0, d, 1 << 0, f"PROXY n={n} rep{rep}")
            print(fmt(o)); rows.append(o); sys.stdout.flush()
    print("\n=== masked: cancellation pair across blocks (truth {0,6}, corr r=0.6, th6 = -r th0: x6 invisible to its table) ===")
    for n in [200, 800, 3200, 12800]:
        for rep in range(2):
            rng = np.random.default_rng(999 + n + rep)
            X = rng.standard_normal((n, p)); X[:, 6] = 0.6 * X[:, 0] + 0.8 * X[:, 6]
            X = (X - X.mean(0)) / X.std(0, ddof=1)
            yr = 1.0 * X[:, 0] - 0.6 * X[:, 6] + rng.standard_normal(n); y = (yr - yr.mean()) / yr.std(ddof=1)
            lg0, d = build(X, y, blocks)
            o, g = analyse(lg0, d, (1 << 0) | (1 << 6), f"CANCEL n={n} rep{rep}")
            print(fmt(o)); rows.append(o); sys.stdout.flush()
