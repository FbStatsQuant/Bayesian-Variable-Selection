# e9_width_mc.py -- TH-SONG-ASSUMPTIONS, council R1 follow-up (Opus B1(c)).
# Monte Carlo of the one-sided conditional Gaussian width w_Dm(X) = E_g max_{|N|=m} ( -<v_S, g> ),
# v_S = (I-P_S)mu/||(I-P_S)mu||, S = (S0\D) u N, on simulated S1 designs (AR(1) rho = 0.6, beta as harness/generate.R),
# for single deletions D = {j} and m = 1 (all S1 cells with SNR >= 2) and m = 2 (p = 500 cells).
# Compares the A-MARGIN-U limit inequality (delta = gamma = t_n = 0, C = 1, classes with B_Dm > 0 only):
#     sqrt( min_{|N|=m} R_n(S)/sigma^2 ) >= w_Dm + sqrt( 2 B_Dm ),  B_Dm = Pr_n(1) - (m/2) log(n / log p).
# Population R_n(S) = n * b_D' Sigma_{DD.S} b_D (exact). No fits, no outcome data. Run single-threaded, under nice.
import os, sys, math
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np

S0 = np.arange(10); COEF = np.array([2, -3, 2, 2, -3, 3, -2, 3, -2, 3], float); RHO = 0.6
CELLS = [(500, 500), (500, 5000), (1000, 500), (1000, 5000)]
SNRS = [2.0, 3.0]; NX = int(sys.argv[1]) if len(sys.argv) > 1 else 4; NG = int(sys.argv[2]) if len(sys.argv) > 2 else 300

def ar1(a, b): return RHO ** np.abs(np.subtract.outer(a, b))

def R_pop(n, beta, D, S):
    D = np.asarray(D); S = np.asarray(S); bD = beta[D]
    SDD = ar1(D, D); SDS = ar1(D, S); SSS = ar1(S, S)
    return n * float(bD @ (SDD - SDS @ np.linalg.solve(SSS, SDS.T)) @ bD)

def sim_X(n, p, rng):
    X = np.empty((n, p)); X[:, 0] = rng.standard_normal(n); e = math.sqrt(1 - RHO ** 2)
    for j in range(1, p): X[:, j] = RHO * X[:, j - 1] + e * rng.standard_normal(n)
    X -= X.mean(0); X /= X.std(0, ddof=1); return X

def widths(X, mu, A, nulls, m, G, rng):
    Q, _ = np.linalg.qr(X[:, A]); r0 = mu - Q @ (Q.T @ mu)
    Z = X[:, nulls] - Q @ (Q.T @ X[:, nulls])
    a = Z.T @ r0; zz = (Z * Z).sum(0); rr = r0 @ r0
    g = rng.standard_normal((X.shape[0], G)); g -= Q @ (Q.T @ g)   # components in span(A) do not enter <r_N, g>
    b = Z.T @ g; r0g = r0 @ g
    if m == 1:
        num = r0g[None, :] - (a / zz)[:, None] * b                    # <r_N, g>
        den = np.sqrt(rr - a ** 2 / zz)[:, None]
        return float(np.mean(np.max(-num / den, axis=0)))
    # m == 2: closed-form 2x2 projections over all pairs (j < k)
    Gm = Z.T @ Z; out = np.full(G, -np.inf); P = len(nulls)
    for j in range(P - 1):
        k = np.arange(j + 1, P); g11 = zz[j]; g22 = zz[k]; g12 = Gm[j, k]; det = g11 * g22 - g12 ** 2
        c1 = (g22 * a[j] - g12 * a[k]) / det; c2 = (g11 * a[k] - g12 * a[j]) / det   # c = G_NN^{-1} a_N
        proj = c1 * a[j] + c2 * a[k]                                                  # ||P r0||^2
        den = np.sqrt(rr - proj)
        num = r0g[None, :] - c1[:, None] * b[j][None, :] - c2[:, None] * b[k]        # <r_N, g>
        out = np.maximum(out, np.max(-num / den[:, None], axis=0))
    return float(np.mean(out))

def main():
    rng = np.random.default_rng(20261127)
    print("\t".join(["n", "p", "snr", "j_deleted", "m", "price_d1", "B_Dm", "sqrt2B", "w_comb", "w_mc", "w_mc_sd",
                     "minR_over_sigma2", "sqrt_minR", "lhs_minus_rhs_comb", "lhs_minus_rhs_mc", "nX", "nG", "binding"]))
    for (n, p) in CELLS:
        nulls = np.arange(10, p); s0 = 10
        pr1 = math.log((2 * p - s0) / s0) + 0.5 * math.log(n + 1)
        ms = [1, 2] if p == 500 else [1]
        Xs = [sim_X(n, p, rng) for _ in range(NX)]
        for snr in SNRS:
            beta = np.zeros(p); beta[S0] = snr * math.sqrt(math.log(p) / n) * COEF
            Rd = [R_pop(n, beta, [j], np.setdiff1d(S0, [j])) for j in S0]
            jb_bind = int(np.argmin(Rd))                                  # binding single deletion
            for jb, m in [(j, m) for j in range(10) for m in ms]:
                B = pr1 - (m / 2) * math.log(n / math.log(p))
                if B <= 0: continue
                A = np.setdiff1d(S0, [jb])
                # min over |N| = m of population R(S): m = 1 exhaustive over nulls near S0 (far nulls are uncorrelated);
                # m = 2 exhaustive over pairs within the 40 nearest nulls (greedy = exhaustive in D1 for m <= 2).
                near = np.arange(10, 50)
                if m == 1: minR = min(R_pop(n, beta, [jb], np.r_[A, [k]]) for k in near)
                else: minR = min(R_pop(n, beta, [jb], np.r_[A, [k1, k2]]) for i, k1 in enumerate(near) for k2 in near[i + 1:])
                w = [widths(X, X[:, S0] @ beta[S0], A, nulls, m, NG, rng) for X in Xs]
                wcomb = math.sqrt(2 * math.log(math.comb(p - s0, m)))
                lhs = math.sqrt(minR)
                print("\t".join(str(v) for v in [n, p, snr, jb + 1, m, round(pr1, 4), round(B, 4), round(math.sqrt(2 * B), 4),
                      round(wcomb, 4), round(float(np.mean(w)), 4), round(float(np.std(w, ddof=1)), 4), round(minR, 3),
                      round(lhs, 4), round(lhs - wcomb - math.sqrt(2 * B), 4), round(lhs - float(np.mean(w)) - math.sqrt(2 * B), 4),
                      NX, NG, int(jb == jb_bind)]), flush=True)

if __name__ == "__main__":
    main()
