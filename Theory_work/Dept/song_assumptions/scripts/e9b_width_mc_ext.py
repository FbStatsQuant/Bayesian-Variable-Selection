# e9b_width_mc_ext.py -- TH-SONG-ASSUMPTIONS, council R2 follow-up (Opus R2 S-3, Neon R2 S3).
# Extends e9_width_mc.py to d = 1, 2, 3 deleted true predictors and reports the A-MARGIN-U limit-form surplus
#     sqrt(min_{|N|=m} R_n(S)/sigma^2) - w_Dm(X) - sqrt(2 [B_Dm]_+)
# under three credit conventions for B_Dm = Pr_n(d) - (m/2) log(n/(C log p))  (gamma = 0, delta = t_n = 0):
#     C = 1;  C = (s0+1)^2 (the constant implied by the step-2 one-null mass);  no credit (B = Pr_n(d)).
# Pr_n(d) = sum_{k=s0-d}^{s0-1} price(k), price(k) = log((2p-1-k)/(k+1)) + 0.5 log(n+1).
# For each (d, m), the 3 deletion sets D with the smallest population min_N R are evaluated (binding classes).
# m = 2 only at p = 500 (all pairs of nulls); m >= 3 not evaluated. Width does not depend on SNR (same direction).
# v2 (senior review C-2 / Sol R3-3): mu = X_raw[:, S0] beta with X_raw the CENTRED RAW AR(1) design, as in harness/generate.R.
# Column rescaling preserves projection spans, so only mu changes; for d = 1 the scaling cancels exactly (E9 unaffected).
# No fits, no outcome data. Single-threaded, run under nice.
import os, sys, math, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e9_width_mc import S0, COEF, CELLS, RHO, R_pop, widths

NX = int(sys.argv[1]) if len(sys.argv) > 1 else 4; NG = int(sys.argv[2]) if len(sys.argv) > 2 else 300
SNRS = [2.0, 3.0]; s0 = 10; NEAR = np.arange(10, 50); NBIND = 3

def sim_X(n, p, rng):   # same draws as e9_width_mc.sim_X, but centred only (raw scale)
    X = np.empty((n, p)); X[:, 0] = rng.standard_normal(n); e = math.sqrt(1 - RHO ** 2)
    for j in range(1, p): X[:, j] = RHO * X[:, j - 1] + e * rng.standard_normal(n)
    X -= X.mean(0); return X

def price(k, n, p): return math.log((2 * p - 1 - k) / (k + 1)) + 0.5 * math.log(n + 1)

def minR(n, beta, D, m):
    A = np.setdiff1d(S0, D)
    if m == 1: return min(R_pop(n, beta, D, np.r_[A, [k]]) for k in NEAR)
    return min(R_pop(n, beta, D, np.r_[A, [k1, k2]]) for k1, k2 in itertools.combinations(NEAR, 2))

def main():
    rng = np.random.default_rng(20261128)
    print("\t".join(["n", "p", "d", "m", "D", "Pr_d", "w_mc_mean", "w_mc_min", "w_mc_max", "snr", "sqrt_minR",
                     "surplus_C1", "active_C1", "surplus_C121", "active_C121", "surplus_nocredit"]))
    for (n, p) in CELLS:
        nulls = np.arange(10, p); Xs = [sim_X(n, p, rng) for _ in range(NX)]
        beta1 = np.zeros(p); beta1[S0] = math.sqrt(math.log(p) / n) * COEF      # unit-SNR direction
        for d in (1, 2, 3):
            Pr = sum(price(k, n, p) for k in range(s0 - d, s0))
            for m in ([1, 2] if p == 500 else [1]):
                Ds = [np.array(D) for D in itertools.combinations(range(10), d)]
                # binding D: smallest population min_N R at unit SNR (R scales with snr^2, so ranking is SNR-free)
                scored = sorted(((minR(n, beta1, D, m), tuple(D)) for D in Ds))[:NBIND]
                for R1, Dt in scored:
                    D = np.array(Dt); A = np.setdiff1d(S0, D)
                    w = [widths(X, X[:, S0] @ beta1[S0], A, nulls, m, NG, rng) for X in Xs]
                    wm = float(np.mean(w))
                    for snr in SNRS:
                        lhs = snr * math.sqrt(R1)
                        out = []
                        for C in (1.0, float((s0 + 1) ** 2)):
                            B = Pr - (m / 2) * math.log(n / (C * math.log(p)))
                            out += [round(lhs - wm - math.sqrt(2 * max(B, 0.0)), 4), int(B > 0)]
                        out.append(round(lhs - wm - math.sqrt(2 * Pr), 4))
                        print("\t".join(str(v) for v in [n, p, d, m, "-".join(str(j + 1) for j in Dt), round(Pr, 4),
                              round(wm, 4), round(min(w), 4), round(max(w), 4), snr, round(lhs, 4)] + out), flush=True)

if __name__ == "__main__":
    main()
