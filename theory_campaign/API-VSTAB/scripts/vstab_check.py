#!/usr/bin/env python3
"""API-VSTAB: independent (Claude-written) exact check of A-REV7 §4's analytic STAB-LH certificate.

Written from the LH definition in W1-EXP PROOF.md §4.1 and the STAB-LH definition in W5-B2ENV PROOF.md §4.1;
it imports nothing from W5 or A-REV7.

Checks
  C0  lambda_min(Sigma_signal-units) >= lambda0 := (1-max|psi|)(1-rho_max)          (W1-EXP Lemma 4.1(a))
  C1  type-reduced m_STAB equals brute force over all V with S° ⊆ V ⊆ SU             (small g)
  C2  the concrete A-REV7 instance (g=9, c=2, v=0, rho=.4, psi=.2, beta=1): exact m_STAB vs certificate .4032
  C3  random sweep: m_STAB >= lambda0*b_vis^2 - R_M whenever ... (always; the inequality is unconditional)
  C4  structural facts used: Delta(S°)=R_M, ZJL, PZL, hub gain >= lambda0 psi^2 beta^2   (random sets)
  C5  reproduce A-REV7 §5 swap witness (rho=.85, psi=.5, beta_a=1.4, g=4): Delta(V)=.3675, Delta(W)=.36271...
Population quantities only (exact Gram: in-sample = population). Seed 20261102.
"""
import itertools, json, sys
import numpy as np

rng = np.random.default_rng(20261102)


def equi(g, r):
    return (1 - r) * np.eye(g) + r * np.ones((g, g))


def build(g, pairs, vis):
    """pairs: list of (rho_a, rho_b, psi, beta); vis: list of (rho_h, beta_h).
    Column layout: for each pair, C_a (hub first) then C_b (hub first); then visible groups (hub first).
    Returns Sigma, theta, list of units (column index lists), S° (list), S0 (list), info."""
    blocks, theta, units, Sstar, S0, hubs = [], [], [], [], [], {}
    off = 0
    P = sum(2 * g for _ in pairs) + g * len(vis)
    Sig = np.zeros((P, P)); th = np.zeros(P)
    for (ra, rb, psi, beta) in pairs:
        A, Bm = equi(g, ra), equi(g, rb)
        ia = np.arange(off, off + g); ib = np.arange(off + g, off + 2 * g)
        Sig[np.ix_(ia, ia)] = A; Sig[np.ix_(ib, ib)] = Bm
        cross = psi * np.outer(A[:, 0], Bm[0, :])
        Sig[np.ix_(ia, ib)] = cross; Sig[np.ix_(ib, ia)] = cross.T
        th[ia[0]] = beta; th[ib[0]] = -psi * beta
        units.append(list(range(off, off + 2 * g)))
        Sstar.append(ia[0]); S0 += [ia[0], ib[0]]
        off += 2 * g
    for (rh, bh) in vis:
        ih = np.arange(off, off + g)
        Sig[np.ix_(ih, ih)] = equi(g, rh); th[ih[0]] = bh
        units.append(list(range(off, off + g))); Sstar.append(ih[0]); S0.append(ih[0])
        off += g
    return Sig, th, units, Sstar, S0


def Delta(Sig, th, V):
    V = sorted(V)
    tot = th @ Sig @ th
    if not V:
        return tot
    c = (Sig @ th)[V]
    return tot - c @ np.linalg.solve(Sig[np.ix_(V, V)], c)


def mstab_brute(Sig, th, units, Sstar):
    SU = sorted(set(itertools.chain(*units)))
    rest = [j for j in SU if j not in Sstar]
    best = {"del": np.inf, "swap": np.inf}
    for r in range(len(rest) + 1):
        for E in itertools.combinations(rest, r):
            V = set(Sstar) | set(E); dV = Delta(Sig, th, V)
            for t in Sstar:
                best["del"] = min(best["del"], Delta(Sig, th, V - {t}) - dV)
                for l in SU:
                    if l not in V:
                        best["swap"] = min(best["swap"], Delta(Sig, th, (V - {t}) | {l}) - dV)
    return best


def unit_types(g, is_pair):
    """Type = representative column subset (relative indices). Pair unit: a-hub=0, a-nonhubs 1..g-1, b-hub=g,
    proxies g+1..2g-1. Visible unit: hub 0, others 1..g-1."""
    out = []
    if is_pair:
        for ha, ka, hb, kb in itertools.product((0, 1), range(g), (0, 1), range(g)):
            S = ([0] if ha else []) + list(range(1, 1 + ka)) + ([g] if hb else []) + list(range(g + 1, g + 1 + kb))
            out.append(((ha, ka, hb, kb), S))
    else:
        for hh, k in itertools.product((0, 1), range(g)):
            out.append(((hh, k), ([0] if hh else []) + list(range(1, 1 + k))))
    return out


def mstab_types(Sig, th, units, g, npairs):
    """Exact m_STAB using exchangeability within groups and orthogonality across units."""
    per = []
    for ui, cols in enumerate(units):
        is_pair = ui < npairs
        cols = np.array(cols)
        Su = Sig[np.ix_(cols, cols)]; tu = th[cols]
        D = {}
        for typ, S in unit_types(g, is_pair):
            D[typ] = Delta(Su, tu, list(S))
        dele, wswap, add = np.inf, np.inf, np.inf
        for typ, S in unit_types(g, is_pair):
            if typ[0] != 1:
                continue  # V must contain the unit's reference truth (a-hub / visible hub)
            d = D[typ]
            t0 = (0,) + typ[1:]
            dele = min(dele, D[t0] - d)
            # additions l in the unit, l not in V (one more of each available kind)
            if is_pair:
                ha, ka, hb, kb = typ
                adds = []
                if ka < g - 1: adds.append((ha, ka + 1, hb, kb))
                if hb == 0: adds.append((ha, ka, 1, kb))
                if kb < g - 1: adds.append((ha, ka, hb, kb + 1))
            else:
                hh, k = typ
                adds = [(hh, k + 1)] if k < g - 1 else []
            for a in adds:
                add = min(add, D[a] - d)
                # within-unit swap: remove reference truth, add a
                wswap = min(wswap, D[(0,) + a[1:]] - d)
        per.append(dict(dele=dele, wswap=wswap, add=add))
    m_del = min(u["dele"] for u in per)
    m_w = min(u["wswap"] for u in per)
    m_x = np.inf
    for i in range(len(per)):
        for j in range(len(per)):
            if i != j:
                m_x = min(m_x, per[i]["dele"] + per[j]["add"])
    # additions of l outside SU change nothing: swap to a null column = deletion (covered by m_del)
    return dict(m_del=m_del, m_wswap=m_w, m_xswap=m_x, m_stab=min(m_del, m_w, m_x))


def cert(Sig, th, units, Sstar, pairs, vis):
    psimax = max([abs(p[2]) for p in pairs] + [0])
    rhomax = max([max(p[0], p[1]) for p in pairs] + [v[0] for v in vis])
    lam0 = (1 - psimax) * (1 - rhomax)
    RM = sum(b ** 2 * ps ** 2 * (1 - ps ** 2) for (_, _, ps, b) in pairs)
    bvis2 = min(th[j] ** 2 for j in Sstar)
    lmin = np.linalg.eigvalsh(Sig)[0]
    return dict(lam0=lam0, lmin=lmin, RM=RM, bvis2=bvis2, cert=lam0 * bvis2 - RM, cert_lmin=lmin * bvis2 - RM)


res = {}
# ---------------- C2: the concrete instance ----------------
g = 9; pairs = [(.4, .4, .2, 1.0), (.4, .4, .2, 1.0)]; vis = []
Sig, th, units, Sstar, S0 = build(g, pairs, vis)
cr = cert(Sig, th, units, Sstar, pairs, vis)
ms = mstab_types(Sig, th, units, g, len(pairs))
res["instance"] = dict(cert=cr, mstab=ms, Delta_Sstar=Delta(Sig, th, Sstar))
print("C2 instance g=9 c=2 rho=.4 psi=.2 beta=1:", json.dumps({k: float(v) for k, v in {**cr, **ms}.items()}))
print("   Delta(S°) =", Delta(Sig, th, Sstar), " R_M =", cr["RM"])
assert cr["lmin"] >= cr["lam0"] - 1e-12
assert abs(Delta(Sig, th, Sstar) - cr["RM"]) < 1e-12
assert ms["m_stab"] >= cr["cert"] - 1e-12

# ---------------- C1: brute force vs type reduction ----------------
c1 = []
for (gg, pp, vv) in [(3, [(.6, .5, .3, 1.2), (.7, .4, -.25, -.8)], []),
                     (3, [(.85, .85, .5, 1.4)], [(.5, .7)]),
                     (4, [(.85, .85, .5, 1.4)], []),
                     (3, [(.4, .4, .2, 1.0)], [(.4, .01)])]:
    S_, t_, u_, ss_, _ = build(gg, pp, vv)
    bf = mstab_brute(S_, t_, u_, ss_); ty = mstab_types(S_, t_, u_, gg, len(pp))
    ok = abs(min(bf["del"], bf["swap"]) - ty["m_stab"]) < 1e-10 and abs(bf["del"] - ty["m_del"]) < 1e-10
    c1.append(dict(g=gg, pairs=pp, vis=vv, brute=bf, types=ty, agree=ok))
    print("C1 brute vs types", gg, pp, vv, "brute", {k: round(v, 10) for k, v in bf.items()},
          "types", round(ty["m_stab"], 10), "agree", ok)
    assert ok
res["brute_vs_types"] = c1

# ---------------- C3: random sweep of the certificate inequality ----------------
viol = 0; napplies = 0; nstab = 0; nboth = 0; worst_slack = np.inf; N = 0; lam_viol = 0
for it in range(1500):
    gg = int(rng.integers(2, 7)); cc = int(rng.integers(1, 3)); vv = int(rng.integers(0, 3))
    pp = []
    for _ in range(cc):
        ra, rb = rng.uniform(.15, .9, 2)
        ps = rng.uniform(.02, min(ra, rb)) * rng.choice([-1, 1])
        pp.append((ra, rb, ps, rng.uniform(.2, 2) * rng.choice([-1, 1])))
    vl = [(rng.uniform(.15, .9), rng.uniform(.05, 2) * rng.choice([-1, 1])) for _ in range(vv)]
    S_, t_, u_, ss_, _ = build(gg, pp, vl)
    cr_ = cert(S_, t_, u_, ss_, pp, vl); ty = mstab_types(S_, t_, u_, gg, len(pp))
    N += 1
    if cr_["lmin"] < cr_["lam0"] - 1e-12: lam_viol += 1
    slack = ty["m_stab"] - cr_["cert"]
    worst_slack = min(worst_slack, slack)
    if slack < -1e-10: viol += 1
    if cr_["cert"] > 0: napplies += 1
    if ty["m_stab"] > 0: nstab += 1
    if cr_["cert"] > 0 and ty["m_stab"] > 0: nboth += 1
res["sweep"] = dict(N=N, violations=viol, lam0_violations=lam_viol, min_slack=worst_slack,
                    cert_positive=napplies, stab_holds=nstab, cert_and_stab=nboth)
print("C3 sweep:", res["sweep"])
assert viol == 0 and lam_viol == 0

# ---------------- C4: structural facts on the instance ----------------
SU = sorted(set(itertools.chain(*units)))
r_ = Sig @ th
hubs_b = [S0[1], S0[3]]
neu = [j for k, u in enumerate(units) for j in (u[1:g] if k < len(pairs) else u[1:])]  # neutral signal-unit columns
bgrp = [j for u in units for j in u[g:]]
zjl = pzl = 0.0; hubgain_min = np.inf
for it in range(400):
    extra = [j for j in SU if j not in Sstar and rng.random() < .35]
    V = sorted(set(Sstar) | set(extra))
    Vv = V
    resid = th.copy()
    # population residual coefficient vector: theta - b_V, b_V = Sigma_VV^{-1}(Sigma theta)_V
    b = np.zeros_like(th); b[Vv] = np.linalg.solve(Sig[np.ix_(Vv, Vv)], r_[Vv]); e = th - b
    cov = Sig @ e  # <x_l, (I-P_V) mu>/(n-1)
    for l in neu:
        if l not in V: zjl = max(zjl, abs(cov[l]))
    VS0 = sorted(set(V) | set(S0))
    b2 = np.zeros_like(th); b2[VS0] = np.linalg.solve(Sig[np.ix_(VS0, VS0)], r_[VS0]); e2 = th - b2
    pzl = max(pzl, float(np.max(np.abs(Sig @ e2))))
    for i, hb in enumerate(hubs_b):
        if hb not in V:
            gain = Delta(Sig, th, V) - Delta(Sig, th, sorted(set(V) | {hb}))
            hubgain_min = min(hubgain_min, gain)
res["structural"] = dict(ZJL_max=zjl, PZL_max=pzl, hubgain_min=hubgain_min, hubgain_bound=cr["lam0"] * .2 ** 2)
print("C4 structural:", res["structural"])
assert zjl < 1e-10 and pzl < 1e-10 and hubgain_min >= cr["lam0"] * .04 - 1e-12

# ---------------- C5: A-REV7 §5 witness ----------------
Sg, tg, ug, ssg, _ = build(4, [(.85, .85, .5, 1.4)], [])
dV = Delta(Sg, tg, [0, 1, 2, 3]); dW = Delta(Sg, tg, [1, 2, 3, 4])
res["arev7_s5"] = dict(DeltaV=dV, DeltaW=dW, diff=dV - dW)
print("C5 A-REV7 §5 witness: Delta(V)=%.16f Delta(W)=%.16f improvement=%.15f" % (dV, dW, dV - dW))

json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "vstab_check.json", "w"), indent=1, default=float)
print("ALL ASSERTIONS PASSED")
