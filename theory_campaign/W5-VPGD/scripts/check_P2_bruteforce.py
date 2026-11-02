"""Check (i) popcheck.scan against an independent brute-force PGD (direct projections, every move enumerated);
(ii) W3-PGD Prop P2 (PGD iff (B1)-(B3) under BO) and Cor P2' (closed form eta*(d)) on small block designs;
(iii) GERC/TRC from scan against direct formulas.  Seed 7.  Output: results/check_P2_bruteforce.txt"""
import itertools
import numpy as np
from popcheck import scan

rng = np.random.default_rng(7)


def Delta(Sig, th, T):
    T = sorted(T)
    tot = th @ Sig @ th
    if not T:
        return tot
    cc = Sig[T] @ th
    return tot - cc @ np.linalg.solve(Sig[np.ix_(T, T)], cc)


def brute_pgd(Sig, th, truth, extras, a, d):
    c = len(th); truth = set(truth)
    worst = -np.inf; trc = np.inf; gerc = -np.inf
    for m in range(1, a + 1):
        for miss in itertools.combinations(sorted(truth), m):
            U = truth - set(miss)
            for e in range(d + 1):
                for P in itertools.combinations(extras, e):
                    S = frozenset(U | set(P))
                    DS = Delta(Sig, th, S)
                    prog, non = [], []
                    for x in range(c):
                        if x in S:
                            continue
                        r = DS - Delta(Sig, th, S | {x})
                        (prog if x in truth else non).append(r)
                    for i in S:
                        r = DS - Delta(Sig, th, S - {i})
                        (non if i in truth else prog).append(r)
                        for x in range(c):
                            if x in S:
                                continue
                            r = DS - Delta(Sig, th, (S - {i}) | {x})
                            (prog if (i not in truth and x in truth) else non).append(r)
                            if i in truth and x in truth:
                                aj = DS - Delta(Sig, th, S | {x})
                                au = Delta(Sig, th, (S - {i}) | {x}) - Delta(Sig, th, S | {x})
                                trc = min(trc, au / aj)
                    worst = max(worst, max(non) / max(prog))
    return 1 - worst, trc


def block_sigma(rhos, b=5):
    G = len(rhos); p = G * b
    S = np.zeros((p, p))
    for g, r in enumerate(rhos):
        I = slice(g * b, (g + 1) * b)
        S[I, I] = r
    np.fill_diagonal(S, 1.0)
    return S


def DgP(Sig, j, P):
    """D_g(P)/(N theta^2) = 1 - R^2(j | P)."""
    P = list(P)
    if not P:
        return 1.0
    cc = Sig[P, j]
    return 1 - cc @ np.linalg.solve(Sig[np.ix_(P, P)], cc)


def eta_B123(Sig, th, groups, truth_of, Dset, d):
    """Enumerate (B1)-(B3) directly (Prop P2) and return sup eta."""
    best = 1.0
    tg = [g for g in groups if truth_of[g] is not None]
    for g in tg:
        j = truth_of[g]; Ng = [x for x in groups[g] if x != j]; Nd = [x for x in Ng if x in Dset]
        for k in range(0, d + 1):
            for P in itertools.combinations(Nd, k):
                D0 = th[j] ** 2 * DgP(Sig, j, P)
                for l in Ng:
                    if l in P:
                        continue
                    best = min(best, th[j] ** 2 * DgP(Sig, j, P + (l,)) / D0)          # (B1)
                    for e in P:
                        Q = tuple(x for x in P if x != e) + (l,)
                        best = min(best, th[j] ** 2 * DgP(Sig, j, Q) / D0)            # (B2)
                for h in tg:
                    if h == g:
                        continue
                    jh = truth_of[h]; Nh = [x for x in groups[h] if x != jh and x in Dset]
                    for kq in range(0, d - k + 1):
                        for Q in itertools.combinations(Nh, kq):
                            best = min(best, th[jh] ** 2 * DgP(Sig, jh, Q) / D0)      # (B3)
    return best


def eta_formula(rhos_truth, thetas, b, d):
    v1 = min(1 - r ** 2 for r in rhos_truth)
    v3 = np.inf
    for g in range(len(thetas)):
        for h in range(len(thetas)):
            if g == h:
                continue
            k = min(d, b - 1); r = rhos_truth[h]
            kap = k * r ** 2 / (1 + (k - 1) * r)
            v3 = min(v3, thetas[h] ** 2 / thetas[g] ** 2 * (1 - kap))
    return min(v1, v3)


lines = []
# (i)+(ii): block designs, 3 truth groups of 5 + one pure-null group, truths at position 0 of their group
cases = [([.85, .85, .85, 0], [1.4, -1.0, 1.8]), ([.4, .7, .9, .3], [0.8, -1.6, 1.4]), ([.6, .0, .8, .5], [1.0, 1.0, -1.2])]
for rhos, ths in cases:
    Sig = block_sigma(rhos)
    p = Sig.shape[0]
    truth = [0, 5, 10]
    th = np.zeros(p); th[truth] = ths
    extras = [x for x in range(15) if x not in truth]          # D = all mates
    groups = {g: list(range(5 * g, 5 * g + 5)) for g in range(4)}
    truth_of = {0: 0, 1: 5, 2: 10, 3: None}
    for d in (1, 2):
        for a in (1, 2):
            eb, trc_b = brute_pgd(Sig, th, truth, extras, a, d)
            sc = scan(Sig, th, truth, extras, a, d)
            e123 = eta_B123(Sig, th, groups, truth_of, set(extras), d)
            ef = eta_formula(rhos[:3], ths, 5, d)
            lines.append(f"rhos={rhos} theta={ths} a={a} d={d}: eta brute={eb:.6f} scan={sc['eta']:.6f} "
                         f"(B1-B3)={e123:.6f} formula={ef:.6f} | TRC brute={trc_b:.6f} scan={sc['trc_min']:.6f} "
                         f"| binding {sc['worst_type']}")
# non-block random design: scan vs brute force
for rep in range(3):
    c = 9
    A = rng.standard_normal((c, 30)); Sig = A @ A.T / 30; dd = np.sqrt(np.diag(Sig)); Sig = Sig / dd[:, None] / dd[None]
    truth = [0, 3, 6]; th = np.zeros(c); th[truth] = rng.uniform(.5, 2, 3) * rng.choice([-1, 1], 3)
    extras = [1, 2, 4, 5, 7, 8]
    eb, trc_b = brute_pgd(Sig, th, truth, extras, 2, 2)
    sc = scan(Sig, th, truth, extras, 2, 2)
    lines.append(f"random rep {rep}: eta brute={eb:.6f} scan={sc['eta']:.6f} | TRC brute={trc_b:.6f} scan={sc['trc_min']:.6f}")
# (iii) GERC: direct ERC(S, l) = sum_j |c_j| ||x~_j|| / ||x~_l|| from explicit residual vectors
from popcheck import erc_batch
for rep in range(3):
    c = 9; n_ = 60
    X = rng.standard_normal((n_, c)) @ rng.standard_normal((c, c)) * 0.3 + rng.standard_normal((n_, c))
    X = X / np.linalg.norm(X, axis=0)
    Sig = X.T @ X
    truth = [0, 3, 6]; is_t = np.zeros(c, bool); is_t[truth] = True
    worst_diff = 0.0
    for S in [(), (1,), (0, 2), (3, 4, 8), (0, 1, 5)]:
        S = list(S)
        M = [t for t in truth if t not in S]
        P = X[:, S] @ np.linalg.pinv(X[:, S]) if S else np.zeros((n_, n_))
        R = X - P @ X
        best = -np.inf
        for l in range(c):
            if l in S or l in truth:
                continue
            coef = np.linalg.lstsq(R[:, M], R[:, l], rcond=None)[0]
            erc = sum(abs(coef[k]) * np.linalg.norm(R[:, M[k]]) for k in range(len(M))) / np.linalg.norm(R[:, l])
            best = max(best, erc)
        inS = np.zeros((1, c), bool); inS[0, S] = True
        got = erc_batch(Sig, np.array([S]).reshape(1, len(S)), inS, is_t)[0]
        worst_diff = max(worst_diff, abs(got - best))
    lines.append(f"GERC rep {rep}: max |erc_batch - direct| = {worst_diff:.2e}")
open('../results/check_P2_bruteforce.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
