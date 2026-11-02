"""Goal 4: Theorem W's PGD on the LH family vs W4-T38FULL Prop. LH-LAT (POP-LAT(S°, m0)).
LH exact-Gram builder copied from origin/theory/W4-T38FULL:theory_campaign/W4-T38FULL/scripts/ref_lhlat.py (build),
same 20 cases (5 fixed + 15 random, seed 1, identical RNG call order).
For each case:
  eta_lat   : 1 - max rho0/rho+ over Lat(S°) \\ {S0} (states S° u M' with M' a proper subset of M), brute force (engine).
  eta_LH    : formula of REPORT Prop. LH-PGD: min{1 - kappa_max, D_min / R_max} (capped at 1),
              D_min = min{min_i R_i, min_i beta_i^2 (1-psi_i^2)^2, min_h theta_h^2}.
  m0/R_max  : what POP-LAT(S°, m0) gives through the implication POP-LAT(m0) => PGD(m0/R_max).
  eta_reg   : PGD over the whole region R_{c,0} = {U subset S0 : |S0 \\ U| <= c} (Theorem W's region form, d = 0).
Deterministic given seed 1."""
import itertools
import numpy as np
from popcheck import scan


def build(G, g, rhos, pairs, vis):
    p = G * g; S = np.zeros((p, p))
    for h in range(G):
        idx = range(h * g, (h + 1) * g); r = rhos[h]
        for i in idx:
            for j in idx:
                S[i, j] = 1.0 if i == j else r
    hub = lambda h: h * g
    for (ga, gb, psi, beta) in pairs:
        A = list(range(ga * g, (ga + 1) * g)); B = list(range(gb * g, (gb + 1) * g))
        blk = psi * np.outer(S[A, hub(ga)], S[hub(gb), B])
        S[np.ix_(A, B)] = blk; S[np.ix_(B, A)] = blk.T
    th = np.zeros(p)
    for (ga, gb, psi, beta) in pairs:
        th[hub(ga)] = beta; th[hub(gb)] = -psi * beta
    for (gh, t) in vis:
        th[hub(gh)] = t
    return S, th


def eta_on_states(Sig, th, S0, states):
    from engine import NbrEngine
    E = NbrEngine(Sig, Sig @ th, th @ Sig @ th)
    c = len(th); is_t = np.zeros(c, bool); is_t[sorted(S0)] = True
    worst = -np.inf
    for S in states:
        S = sorted(S); s = len(S)
        o = E.eval(np.array([S], dtype=int).reshape(1, s), ld=False)
        DS = o['v'][0, 0]; inS = o['inS'][0]
        add = DS - o['add_v'][0, :, 0]
        prog = [add[x] for x in range(c) if not inS[x] and is_t[x]]
        non = [add[x] for x in range(c) if not inS[x] and not is_t[x]]
        for k, i in enumerate(S):
            de = DS - o['del_v'][0, k, 0]
            (non if is_t[i] else prog).append(de)
            for x in range(c):
                if inS[x]:
                    continue
                sw = DS - o['swap_v'][0, k, x, 0]
                (prog if (not is_t[i] and is_t[x]) else non).append(sw)
        worst = max(worst, max(non) / max(prog))
    return 1 - worst


rng = np.random.default_rng(1)
cases = []
cases.append((5, 3, [.7] * 5, [(0, 1, .5, 1.4), (2, 3, -.4, -1.0)], [(4, 1.0)]))
cases.append((6, 3, [.7, .6, .9, .8, .5, .7], [(0, 1, .69, 1.0), (2, 3, -.79, 2.0), (4, 5, .49, 0.7)], []))
cases.append((6, 3, [.3, .95, .95, .3, .6, .6], [(0, 1, -.29, 1.0), (2, 3, .29, 1.0), (4, 5, -.59, 1.5)], []))
cases.append((5, 3, [.99, .99, .5, .5, .5], [(0, 1, .98, 1.0), (2, 3, -.49, 1.0)], [(4, .3)]))
cases.append((5, 2, [.2, .9, .9, .2, .5], [(0, 1, .01, 3.0), (2, 3, -.19, 1.0)], [(4, 2.)]))
for _ in range(15):
    G = 6; g = int(rng.integers(2, 4)); rh = list(rng.uniform(.05, .97, G))
    pr = []
    for k in range(3):
        a, b = 2 * k, 2 * k + 1; mx = min(rh[a], rh[b]); ps = rng.uniform(.02, 1) * mx * rng.choice([-1, 1])
        pr.append((a, b, ps, rng.choice([-1, 1]) * rng.uniform(.3, 3)))
    cases.append((G, g, rh, pr, []))

lines = []
viol_impl = 0; viol_formula = 0
for ci, (G, g, rh, pr, vis) in enumerate(cases):
    Sig, th = build(G, g, rh, pr, vis)
    S0 = set(np.nonzero(th)[0].tolist()); M = [gb * g for (_, gb, _, _) in pr]
    Sc = S0 - set(M)
    R = [b ** 2 * ps ** 2 * (1 - ps ** 2) for (_, _, ps, b) in pr]
    kap = [rh[gb] ** 2 * (1 - ps ** 2) / (1 - ps ** 2 * rh[gb] ** 2) for (_, gb, ps, _) in pr]
    dels = R + [b ** 2 * (1 - ps ** 2) ** 2 for (_, _, ps, b) in pr] + [t ** 2 for _, t in vis]
    Dmin = min(dels)
    m0 = min([(1 - max(kap)) * min(R)] + [b ** 2 * (1 - ps ** 2) ** 2 for (_, _, ps, b) in pr] + [t ** 2 for _, t in vis])
    eta_LH = min(1.0, 1 - max(kap), Dmin / max(R))
    lat = [Sc | set(sub) for r in range(len(M)) for sub in itertools.combinations(M, r)]
    eta_lat = eta_on_states(Sig, th, S0, lat)
    sc = scan(Sig, th, sorted(S0), [], len(M), 0)
    eta_reg = sc['eta']
    ok1 = eta_lat >= m0 / max(R) - 1e-10
    ok2 = eta_lat >= eta_LH - 1e-10
    viol_impl += (not ok1); viol_formula += (not ok2)
    lines.append(f"case {ci:2d} (G={G}, g={g}, c={len(M)}): eta_lat={eta_lat:.4f}  eta_LH(formula)={eta_LH:.4f}  "
                 f"m0/R_max={m0 / max(R):.4f}  [eta_lat >= m0/Rmax: {ok1}; >= formula: {ok2}]  "
                 f"eta on R_(c,0)={eta_reg:.4f} ({sc['worst_type']})")
lines.append(f"violations: implication POP-LAT => PGD(m0/R_max): {viol_impl}/20; formula eta_LH: {viol_formula}/20")
print('\n'.join(lines))
open('../results/lh_pgd.txt', 'w').write('\n'.join(lines) + '\n')
