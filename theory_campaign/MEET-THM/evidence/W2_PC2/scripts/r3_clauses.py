"""W2_PC2: clause-level checks of R2_C §R3 (C2) parts (a), (b) and the 'continuous' row, by exact enumeration.
For each random design (block-structured correlated Sigma with cross corr eps, or generic correlated X), exact
sufficient statistics, coded partition (M §6.3) or an arbitrary partition, all feasible models S (|S| <= K):
 (a1) d = d_sigma + d_X with 0 <= d_sigma(S) <= C_sigma and |d_X(S)| <= b_X   [d_sigma per §R2 bridge constants]
 (a2) KL(pi||pi0), KL(pi0||pi), J = E_pi d - E_pi0 d all <= D_*; J identity
 (b1) chi2(q_{u+D}||q_u) <= e^{D D_*} - 1 on a grid of u, D
 (b2) continuity row: e^{-4 v b_X} <= [1+chi2(q_v||q_u)]/[1+chi2(q^s_v||q^s_u)] <= e^{4 v b_X}, 0<=u<v<=1
Only designs inside the matrix domain (a, dA, dH, r < 1) count as valid.  Fixed seeds; < 2 min.
"""
import math, itertools
import numpy as np
from bvs_common import (exact_gram_suff, coded_partition, method_sizes, d_table, card_Dstar, log_prior_w, A0, B0)


def lse(x):
    m = np.max(x); return m + math.log(np.exp(x - m).sum())


def dsigma(G, z, Y, n, blocks, S):
    nu = A0 + n / 2.0
    Qb = 2 * B0 + Y
    bid = {j: b for b, C in enumerate(blocks) for j in C}
    parts = {}
    for j in S:
        parts.setdefault(bid[j], []).append(j)
    xs = []
    for U in parts.values():
        GU = G[np.ix_(U, U)]; H = (n + 1) * GU + np.eye(len(U))
        xs.append(n * float(z[U] @ np.linalg.solve(H, z[U])) / Qb)
    return nu * (sum(math.log1p(-x) for x in xs) - math.log1p(-sum(xs))) if xs else 0.0


def chi2p1(lg0, d, u, v):
    # 1 + chi2(q_v||q_u) = Z_{2v-u} Z_u / Z_v^2
    return math.exp(lse(lg0 + (2 * v - u) * d) + lse(lg0 + u * d) - 2 * lse(lg0 + v * d))


rng0 = np.random.default_rng(7)
viol = dict(a1s=0, a1x=0, a2=0, Jid=0, b1=0, b2=0)
nvalid = ntot = 0
maxratio = dict(dsig=0, dX=0, J=0, KLf=0, KLr=0)
for it in range(160):
    rng = np.random.default_rng(10_000 + it)
    p = int(rng.integers(5, 10))
    n = int(rng.choice([40, 150, 600, 3000]))
    kind = it % 3
    if kind < 2:
        g = int(rng.integers(2, 4)); gid = np.arange(p) // g
        rho = rng.uniform(0.2, 0.7); eps = rng.choice([0.0, 0.002, 0.01, 0.05, 0.15])
        Sig = np.where(gid[:, None] == gid[None, :], rho, eps); np.fill_diagonal(Sig, 1.0)
        if np.linalg.eigvalsh(Sig).min() <= 0.05:
            continue
    else:
        A = rng.standard_normal((p, p)) * 0.4 + np.eye(p)
        Sig = A @ A.T; dd = np.sqrt(np.diag(Sig)); Sig = Sig / np.outer(dd, dd)
    th = np.zeros(p); k0 = int(rng.integers(1, 4))
    th[rng.choice(p, k0, replace=False)] = rng.normal(0, 1, k0) * rng.choice([0.05, 0.2, 0.6])
    G, z, Y, _ = exact_gram_suff(Sig, th, n, 1.0, rng)
    K, B = method_sizes(n, p)
    if it % 2 == 0:
        blocks = coded_partition(G, B)
    else:
        perm = rng.permutation(p); cuts = sorted(rng.choice(range(1, p), int(rng.integers(1, 4)), replace=False))
        blocks = [list(map(int, c)) for c in np.split(perm, cuts)]
    ntot += 1
    cs = card_Dstar(G, z, Y, n, blocks, K)
    if not cs['ok']:
        continue
    nvalid += 1
    models, d, lbf = d_table(G, z, Y, n, blocks, K)
    lp = np.array([log_prior_w(p, len(S)) for S in models])
    lg0 = lp + lbf - d
    ds = np.array([dsigma(G, z, Y, n, blocks, S) for S in models])
    dX = d - ds
    Cs, bX, Ds = cs['shared'], cs['bX'], cs['Dstar']
    if ds.min() < -1e-9 or ds.max() > Cs + 1e-9: viol['a1s'] += 1
    if np.abs(dX).max() > bX + 1e-9: viol['a1x'] += 1
    maxratio['dsig'] = max(maxratio['dsig'], ds.max() / Cs if Cs > 0 else 0)
    maxratio['dX'] = max(maxratio['dX'], np.abs(dX).max() / bX if bX > 0 else 0)
    lpi0 = lg0 - lse(lg0); lpi = lg0 + d - lse(lg0 + d)
    pi0, pi = np.exp(lpi0), np.exp(lpi)
    KLf = float(pi @ (lpi - lpi0)); KLr = float(pi0 @ (lpi0 - lpi)); J = float(pi @ d - pi0 @ d)
    if abs(KLf + KLr - J) > 1e-7 * max(1, J): viol['Jid'] += 1
    if max(KLf, KLr, J) > Ds + 1e-9: viol['a2'] += 1
    for key, val in (('J', J), ('KLf', KLf), ('KLr', KLr)):
        maxratio[key] = max(maxratio[key], val / Ds)
    for u in (0, .1, .3, .5, .7, .9):
        for D in (.02, .05, .1, .3, 1 - u):
            if u + D > 1 + 1e-12 or D <= 0: continue
            if math.log(chi2p1(lg0, d, u, u + D)) > D * Ds + 1e-9: viol['b1'] += 1
    for u, v in itertools.combinations([0, .2, .5, .8, 1.0], 2):
        lr = math.log(chi2p1(lg0, d, u, v)) - math.log(chi2p1(lg0, ds, u, v))
        if abs(lr) > 4 * v * bX + 1e-9: viol['b2'] += 1
print(f"designs={ntot} valid(matrix domain)={nvalid}")
print("violations:", viol)
print("max observed ratios (to C_sigma, b_X, D_*):", {k: round(v, 4) for k, v in maxratio.items()})
