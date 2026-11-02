"""LIT-MCMC: numerical check of Proposition OB at the study's scale (study-LIKE generator, not the study's own).
n = 200, p in {500, 1000}, s0 = 14, truth at 1 + d(k-1) (0-based: d(k-1)), d = 7 / 13, coefficients cycling
(1.4, -1.0, 1.8, -1.2, 0.8, -1.6), sigma = 1. Designs: S1 (iid), S4 (blocks of 5, 0.85H + 0.15I).
Paper's exact target (W1-EXP score code via API-POS copy). For gamma_e = S0 + {e}: e* = argmax_e pi(gamma_e);
R_ub := max_{y in N(gamma_e*)} pi(y)/pi(gamma_e*)  (>= R, since R is a min over states); M_lb := |N(gamma_e*)| (<= M).
If R_ub < M_lb then R < M for certain, i.e. Chang-Zhou Thm 1 / ZYVR (1a)-type hypotheses fail on this data set.
Seed 20261102 + replicate.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvs_exact_W1EXP as bx  # noqa

PAT = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]


def design(rng, n, p, scen):
    Z = rng.standard_normal((n, p))
    if scen == "S1":
        return Z
    # S4: blocks of 5, corr 0.85 within: x = sqrt(.85) f_b + sqrt(.15) z
    f = rng.standard_normal((n, p // 5))
    return math.sqrt(0.85) * np.repeat(f, 5, axis=1) + math.sqrt(0.15) * Z


def lpi(models, R, r, n, p):
    models = np.asarray(models)
    return bx.log_m_batch(models, R, r, n) + bx.log_w(models.shape[1], p)


def one(n, p, scen, rep):
    rng = np.random.default_rng(20261102 + rep)
    s0 = 14
    d = 7 if p == 500 else 13
    S0 = [d * k for k in range(s0)]
    X = design(rng, n, p, scen)
    beta = np.zeros(p); beta[S0] = [PAT[k % 6] for k in range(s0)]
    y = X @ beta + rng.standard_normal(n)
    Xc = X - X.mean(0); Xs = Xc / Xc.std(0, ddof=1)
    yc = y - y.mean(); ys = yc / yc.std(ddof=1)
    R = Xs.T @ Xs / (n - 1); r = Xs.T @ ys / (n - 1)
    nulls = [j for j in range(p) if j not in set(S0)]
    G = np.array([sorted(S0 + [e]) for e in nulls])
    lg = lpi(G, R, r, n, p)
    i = int(np.argmax(lg)); e = nulls[i]; g = sorted(S0 + [e]); lgs = lg[i]
    l0 = lpi(np.array([S0]), R, r, n, p)[0]
    k = len(g); out = [j for j in range(p) if j not in set(g)]
    adds = np.array([sorted(g + [j]) for j in out])
    dels = np.array([[x for x in g if x != j] for j in g])
    swaps = np.array([sorted([x for x in g if x != a] + [b]) for a in g for b in out])
    best = max(lpi(adds, R, r, n, p).max(), lpi(dels, R, r, n, p).max(), lpi(swaps, R, r, n, p).max())
    logR = best - lgs
    Mlb = len(adds) + len(dels) + len(swaps)
    lp = math.log(p)
    return dict(e=e, l0_minus=l0 - lgs, logR=logR, logpR=logR / lp, logpM=math.log(Mlb) / lp,
                fail=logR < math.log(Mlb), pred=math.log(2 * math.sqrt(n) / (s0 + 1)) / lp)


if __name__ == "__main__":
    print("| p | scen | rep | e* | log pi(S0)/pi(S0+e*) | log_p R_ub | log_p M_lb | R < M certain | OB heuristic log_p(2 sqrt(n)/k) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for p in (500, 1000):
        for scen in ("S1", "S4"):
            for rep in range(3):
                a = one(200, p, scen, rep)
                print(f"| {p} | {scen} | {rep} | {a['e']} | {a['l0_minus']:.2f} | {a['logpR']:.2f} | {a['logpM']:.2f} | "
                      f"{'yes' if a['fail'] else 'no'} | {a['pred']:.2f} |", flush=True)
