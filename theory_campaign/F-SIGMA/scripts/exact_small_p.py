"""F-SIGMA exact check at small p (p = 12, 3 blocks of 4, n = 200, exact BO design), full enumeration (2^12 models).
Checks Lemma S1 (d^C = h(t_S) exactly under BO; odds-transfer identity; odds bound), the W2-analogue, and
the dependence of pi0^C(S0) on sigma_hat^2 / sigma^2 (dichotomy at small p: mild), against v3 and the posterior.
Seed 20261102."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from itertools import combinations
from scipy.special import logsumexp
from sigma_lib import *

rng = np.random.default_rng(20261102)
n, p = 200, 12
blocks = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
K = min(p, n//2)
theta = np.zeros(p); theta[[0,4,8]] = [1.5, 1.5, 0.35]      # one truth per block; the third is weak (dilution-masked in v3)
S0 = (0,4,8)
for rep in range(3):
    X = bo_design(n, blocks, 0.3, rng)
    y, mu, sig = make_y(X, theta, 1.0, rng)
    sc = Scorer(X, y)
    models = [S for k in range(K+1) for S in combinations(range(p), k)]
    tD = {S: sc.tD(S) for S in models}
    ks = np.array([len(S) for S in models])
    logF = np.array([log_w(len(S), p) + sc.logBF_from(*tD[S]) for S in models])
    logpi = logF - logsumexp(logF)
    idx = {S: i for i, S in enumerate(models)}
    tabs = [block_tables(sc, b) for b in blocks]
    st_v3 = Start(blocks, tabs, lambda t, lD: sc.logBF_from(t, lD), p, K)
    t0, _ = tD[S0]; s2_S0 = (sc.c - t0)/(2*sc.nu)                  # plug-in at the truth: (2b0 + Q_S0)/(2 nu)
    mode_v3 = tuple(st_v3.mode()); tm, _ = tD[mode_v3]; s2_mode = (sc.c - tm)/(2*sc.nu)
    # C-fix iteration from the v3 mode
    s2 = s2_mode; Sfix = mode_v3
    for it in range(10):
        stC = Start(blocks, tabs, lambda t, lD, s2=s2: sc.logrC_from(t, lD, s2), p, K)
        Snew = tuple(stC.mode()); tn, _ = tD[Snew]; s2n = (sc.c - tn)/(2*sc.nu)
        if Snew == Sfix: break
        Sfix, s2 = Snew, s2n
    s2_fix = s2
    print(f"rep {rep}: sigma^2 (y scale) = {sig**2:.4f}; s2_S0 = {s2_S0:.4f}; v3 mode = {mode_v3}, s2_mode = {s2_mode:.4f}; C-fix mode = {Sfix}, s2_fix = {s2_fix:.4f} after {it+1} its")
    print(f"   pi(S0) = {np.exp(logpi[idx[S0]]):.4f}; pi0^v3(S0) = {np.exp(st_v3.log_pi0(S0)):.3e}; argmax pi = {models[int(np.argmax(logpi))]}")
    for lab, s2 in [("0.5 s2_S0", 0.5*s2_S0), ("0.7 s2_S0", 0.7*s2_S0), ("0.9 s2_S0", 0.9*s2_S0), ("s2_S0", s2_S0), ("1.1 s2_S0", 1.1*s2_S0), ("1.5 s2_S0", 1.5*s2_S0), ("2 s2_S0", 2*s2_S0), ("v3-mode RSS", s2_mode), ("C-fix", s2_fix), ("null s_y^2", sc.c/(2*sc.nu))]:
        stC = Start(blocks, tabs, lambda t, lD, s2=s2: sc.logrC_from(t, lD, s2), p, K)
        lp0 = np.array([stC.log_pi0(S) for S in models])
        logBF = logF - log_w(ks, p)
        sumlogr = lp0 + stC.logZbar0 - log_w(ks, p)
        dC = logBF - sumlogr
        ts = np.array([tD[S][0] for S in models])
        h = -sc.nu*np.log(1 - ts/sc.c) - ts/(2*s2)
        err_S1 = np.abs(dC - h).max()
        u = (sc.c - ts)/(2*sc.nu*s2); u0 = u[idx[S0]]
        lhs = lp0 - lp0[idx[S0]]; rhs = logpi - logpi[idx[S0]] - sc.nu*(psi(u) - psi(u0))
        err_odds = np.abs(lhs - rhs).max()
        pS0 = np.exp(logpi[idx[S0]]); p0S0 = np.exp(lp0[idx[S0]])
        upi = (1 - pS0)/pS0; upi0 = (1 - p0S0)/p0S0
        bound_ok = upi0 <= np.exp(sc.nu*psi(u0))*upi*(1+1e-9)
        lr, ap = [], []
        for l in range(p):
            if l in S0: continue
            S = tuple(sorted(S0 + (l,))); g = tD[S][0] - t0
            lr.append(sc.nu*(psi(u[idx[S]]) - psi(u0))); ap.append((1/u0 - 1)*g/(2*s2))
        lr, ap = np.array(lr), np.array(ap)
        print(f"   sigma_hat^2 = {lab:12s} ({s2:.4f}, a = sigma^2/s2 = {sig**2/s2:.3f}, u0 = {u0:.4f}): pi0^C(S0) = {p0S0:.4f}  max|d^C - h| = {err_S1:.1e}  max|odds id| = {err_odds:.1e}  odds bound holds: {bound_ok}  nu*psi(u0) = {sc.nu*psi(u0):.3f}  W2: max|LR - approx| = {np.abs(lr-ap).max():.3f} (max|LR| = {np.abs(lr).max():.2f})  mode = {stC.mode()}")
