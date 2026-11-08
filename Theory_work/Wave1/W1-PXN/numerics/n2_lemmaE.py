"""N2: Lemma E (PROOF s4) falsification on simulated LH-iid.  g=10, rho=.7, psi=.5, beta=beta_vis=1, sigma=1, c=1, v=1 (s0=3)."""
import itertools
import time
import numpy as np
from lhcommon import *

out = Tee("n2_lemmaE.txt")
out("N2 n2_lemmaE.py -- Lemma E: LH-iid, g=10, rho=0.7, psi=0.5, c=1, v=1, beta=1, beta_vis=1, sigma=1")
g, c, v, rho, psi, beta, bvis, sigma = 10, 1, 1, 0.7, np.array([0.5]), np.array([1.0]), np.array([1.0]), 1.0
s0 = 2 * c + v
CONFIGS = [(100, 60), (200, 120), (400, 200)]
NSEEDS = 5
NRAND = 2000

for (n, p) in CONFIGS:
    t0 = time.time()
    assert p % g == 0
    Sigma = build_sigma(p, g, c, rho, psi)
    theta = build_theta(p, g, c, v, psi, beta, bvis)
    lam0 = np.linalg.eigvalsh(Sigma)[0]
    phi02 = lam0 / 2.0
    M = 2 * theta @ Sigma @ theta + 1.0
    cE = sigma**2 / (12 * (M + sigma**2))
    kappaE = 0.52 / cE + 1.0
    L = np.linalg.cholesky(Sigma)
    out("\n" + "=" * 100)
    out("(n,p) = (%d,%d): lambda_min(Sigma)=%.4f (F4 bound (1-psi)(1-rho)=%.4f), phi0^2=%.4f, M=%.3f, c_E=%.5f, kappa_E=%.2f, nu=%.2f" %
        (n, p, lam0, (1 - 0.5) * (1 - rho), phi02, M, cE, kappaE, 0.01 + n / 2))
    # accumulators over all seeds
    acc = dict(n_sets=0, eig_min=np.inf, n_eig_lt=0,
               eta_lo_viol=0, eta_hi_viol=0, eta_min=np.inf, eta_max=-np.inf, eta_ratio_max=0.0,  # eta/(bound)
               ident_err=0.0, gap_min=np.inf, gap_max=-np.inf, gap_up=-np.inf, a_lo_viol=0, a_hi_viol=0,
               a_min=np.inf, a_max=-np.inf, a_hi_bound=None,
               rss_min=np.inf, rss_half_viol=0, Y2_max=-np.inf, Y2_viol=0, mu2n_max=-np.inf, mu2n_viol=0,
               rssy_min=np.inf, cE_viol=0, R_min=np.inf, R_max=-np.inf, R_viol=0, R_ident=0.0,
               e5_max=0.0, e5_ratio=0.0, eta_viol_given_E=0, a_viol_given_E=0, rss_viol_given_E=0, R_viol_given_E=0)
    per_seed = []
    for seed in range(NSEEDS):
        rng = np.random.default_rng([20260108, n, p, seed])
        Xr, yr = draw_raw(rng, n, L, theta, sigma)
        X, y, Y, Xc = standardise(Xr, yr)
        mu = Xc @ theta
        Y2 = float(Y @ Y)
        sc = Scorer(X, y)
        Fempty = None
        # family
        sets = [()]
        cols = list(range(4 * g))
        for k in (1, 2, 3):
            sets += list(itertools.combinations(cols, k))
        nfam = len(sets)
        for _ in range(NRAND):
            k = int(rng.integers(1, s0 + 3))  # sizes 1..s0+2
            sets.append(tuple(sorted(rng.choice(p, size=k, replace=False).tolist())))
        sdl = dict(minRSS=np.inf, maxR=-np.inf, minR=np.inf)
        acc["Y2_max"] = max(acc["Y2_max"], Y2)
        acc["Y2_viol"] += int(Y2 > 3 * (M + sigma**2) * n)
        mu2n = float(mu @ mu) / n
        acc["mu2n_max"] = max(acc["mu2n_max"], mu2n)
        acc["mu2n_viol"] += int(mu2n > M)
        seed_viol = 0
        for S in sets:
            S = list(S)
            k = len(S)
            acc["n_sets"] += 1
            XA = X[:, S]
            pr = sc.parts(S)
            # sample min eig of R_A
            if k > 0:
                RA = XA.T @ XA / (n - 1)
                e_min = np.linalg.eigvalsh(RA)[0]
            else:
                e_min = np.inf
            acc["eig_min"] = min(acc["eig_min"], e_min)
            inE = (e_min >= phi02)
            acc["n_eig_lt"] += int(not inE)
            # (E1)
            eta = pr["logD"] - k * np.log(n + 1)
            lo = -2.0 * k / ((n - 1) * phi02)
            acc["eta_min"] = min(acc["eta_min"], eta)
            acc["eta_max"] = max(acc["eta_max"], eta)
            if k > 0:
                acc["eta_ratio_max"] = max(acc["eta_ratio_max"], eta / lo)  # fraction of the allowed negative range used
            v1 = (eta < lo - 1e-12) or (eta > 1e-12)
            if eta < lo - 1e-12:
                acc["eta_lo_viol"] += 1
            if eta > 1e-12:
                acc["eta_hi_viol"] += 1
            if v1 and inE:
                acc["eta_viol_given_E"] += 1
            # (E2): matrix identity and Q - RSS^y
            if k > 0:
                G, H = pr["G"], pr["H"]
                Gi = np.linalg.inv(G)
                Hi = np.linalg.inv(H)
                lhs = Gi - n * Hi
                rhs = Gi @ (G + np.eye(k)) @ Hi
                acc["ident_err"] = max(acc["ident_err"], np.abs(lhs - rhs).max())
                rssy_formula = sc.yy - float(pr["z"] @ Gi @ pr["z"])
            else:
                rssy_formula = sc.yy
            res_y = proj_resid(y, XA) if k > 0 else y
            rssy = float(res_y @ res_y)
            assert abs(rssy - rssy_formula) < 1e-6 * max(1, rssy), (rssy, rssy_formula)
            gap = pr["Q"] - rssy
            acc["gap_min"] = min(acc["gap_min"], gap)
            acc["gap_max"] = max(acc["gap_max"], gap)
            gup = 1 + 1 / ((n - 1) * phi02)
            acc["gap_up"] = max(acc["gap_up"], gap / gup)
            a_A = 2 * B0 + gap
            acc["a_min"] = min(acc["a_min"], a_A)
            acc["a_max"] = max(acc["a_max"], a_A)
            acc["a_hi_bound"] = 2 * B0 + gup
            a_viol = (gap < -1e-9) or (gap > gup + 1e-9)
            acc["a_lo_viol"] += int(gap < -1e-9)
            acc["a_hi_viol"] += int(gap > gup + 1e-9)
            if a_viol and inE:
                acc["a_viol_given_E"] += 1
            # (E3)
            resY = proj_resid(Y, XA) if k > 0 else Y
            RSS = float(resY @ resY)
            acc["rss_min"] = min(acc["rss_min"], RSS)
            rv = RSS < n * sigma**2 / 2
            acc["rss_half_viol"] += int(rv)
            if rv and inE:
                acc["rss_viol_given_E"] += 1
            rssy2 = (n - 1) * RSS / Y2
            assert abs(rssy2 - rssy) < 1e-6 * max(1, rssy), (rssy2, rssy)
            acc["rssy_min"] = min(acc["rssy_min"], rssy / n)
            acc["cE_viol"] += int(rssy < cE * n)
            # (E4)
            Rk = -0.5 * eta - sc.nu * np.log(1 + a_A / rssy)
            acc["R_min"] = min(acc["R_min"], Rk)
            acc["R_max"] = max(acc["R_max"], Rk)
            rvv = abs(Rk) > kappaE
            acc["R_viol"] += int(rvv)
            if rvv and inE:
                acc["R_viol_given_E"] += 1
            Fk = sc.F(S)
            ident = Fk - (log_w(k, p) - 0.5 * k * np.log(n + 1) - sc.nu * np.log(RSS) + sc.nu * np.log(Y2 / (n - 1)) + Rk)
            acc["R_ident"] = max(acc["R_ident"], abs(ident))
            # (E5)
            mu_res = proj_resid(mu, XA) if k > 0 else mu
            LamA = float(mu_res @ mu_res)
            d = abs(RSS - n * sigma**2 - LamA)
            acc["e5_max"] = max(acc["e5_max"], d)
            acc["e5_ratio"] = max(acc["e5_ratio"], d / n ** (2 / 3))
    out("sets checked (all seeds): %d  (per seed: %d structured + %d random)" % (acc["n_sets"], nfam, NRAND))
    out("[E1] sample lambda_min(R_A): min over all sets = %.4f  (phi0^2 = %.4f);  #sets with lambda_min(R_A) < phi0^2 : %d  (event E fails there)" %
        (acc["eig_min"], phi02, acc["n_eig_lt"]))
    out("[E1] eta_A range: [%.4g, %.4g];  #violations of eta<=0: %d;  #violations of eta >= -2|A|/((n-1)phi0^2): %d;  max eta/lower-bound = %.4f (<=1 required)" %
        (acc["eta_min"], acc["eta_max"], acc["eta_hi_viol"], acc["eta_lo_viol"], acc["eta_ratio_max"]))
    out("[E1] violations among sets with lambda_min(R_A)>=phi0^2: %d" % acc["eta_viol_given_E"])
    out("[E2] max abs error of identity G^-1 - nH^-1 = G^-1 (G+I) H^-1 : %.3e" % acc["ident_err"])
    out("[E2] Q_A - RSS^y_A in [%.4g, %.4g];  upper bound 1+1/((n-1)phi0^2) = %.4f  (max gap/bound = %.4f);  #viol lower(<0): %d, upper: %d;  among E-sets: %d" %
        (acc["gap_min"], acc["gap_max"], 1 + 1 / ((n - 1) * phi02), acc["gap_up"], acc["a_lo_viol"], acc["a_hi_viol"], acc["a_viol_given_E"]))
    out("[E2] a_A in [%.4f, %.4f]; claimed [2b0, 2b0+1+1/((n-1)phi0^2)] = [0.02, %.4f]" % (acc["a_min"], acc["a_max"], acc["a_hi_bound"]))
    out("[E3] min RSS_A over all sets = %.2f  (n sigma^2/2 = %.1f);  #viol RSS_A >= n s^2/2 : %d;  among E-sets: %d" %
        (acc["rss_min"], n * sigma**2 / 2, acc["rss_half_viol"], acc["rss_viol_given_E"]))
    out("[E3] max ||Y||^2 over seeds = %.1f  (bound 3(M+s^2)n = %.1f); #seeds violating: %d of %d;   max ||mu||^2/n = %.3f  (M = %.3f), #seeds violating: %d" %
        (acc["Y2_max"], 3 * (M + sigma**2) * n, acc["Y2_viol"], NSEEDS, acc["mu2n_max"], M, acc["mu2n_viol"]))
    out("[E3] min RSS^y_A / n = %.4f  (c_E = %.5f); #viol RSS^y_A >= c_E n : %d" % (acc["rssy_min"], cE, acc["cE_viol"]))
    out("[E4] R_A range = [%.4f, %.4f];  kappa_E = %.2f;  claimed range [-0.52/c_E, J/((n-1)phi0^2)] = [%.2f, %.3f];  #viol |R_A|<=kappa_E : %d (among E-sets: %d)" %
        (acc["R_min"], acc["R_max"], kappaE, -0.52 / cE, (s0 + 2) / ((n - 1) * phi02), acc["R_viol"], acc["R_viol_given_E"]))
    out("[E4] identity F(A) = log w - |A|/2 log(n+1) - nu log RSS_A + c_n + R_A : max abs error = %.3e" % acc["R_ident"])
    out("[E5] max |RSS_A - n sigma^2 - Lambda_A| = %.2f ; max of that / n^(2/3) = %.3f  (C2 not explicit in PROOF)" % (acc["e5_max"], acc["e5_ratio"]))
    out("(elapsed %.1fs)" % (time.time() - t0))

out("\nDONE")
out.close()
