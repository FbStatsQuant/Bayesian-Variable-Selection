"""W3-MISR numerics N1-N4 (sharpness gate; boundary-violation numerics). Local only.

Exact posterior of the coded target on a small candidate design, by full enumeration (formulas of W3-POST STATEMENT §0;
same implementation as Theory_work/Wave1C/C-MIS/numerics/mis_core.py, restated here so the file is self-contained).

  N1  Lemma R'(b) / MIS-R(i): residual variance v_n varying with n (v_n = sigma^2 + tau_n^2 = 2, 1 + n, 1 + n^2, 2/n, n^-2; sigma^2 = 0 allowed), with the
      signal-to-noise hypotheses held fixed. (i) common random numbers: the posterior is identical across v_n;
      (ii) independent seeds: delta_n / r_n is stable in n and across v_n.
  N2  Boundary of the relative margin: FIXED raw coefficients, omitted independent Gaussian column of variance n^(2a)
      (tau_n^2 = n^(2a)); the relative beta-min ratio is ~ n^(1-2a)/log n. a < 1/2: covered by MIS-R (not by C-MIS v1,
      which needs tau^2 fixed); a >= 1/2: relative margin fails.
  N3  Outside GR^c: (i) heavy-tailed iid residual (t_3); (ii) heteroscedastic residual within the design;
      (iii) common random slope (C-MIS Example E2): non-scalar contrast covariance, target changes; with the slope put
      in the conditioning sigma-field (MIS-R(ii)) the conditional target is recovered.
  N4  Outside (E^sigma): energy ||mu||^2/(n v) growing like n^b.

Run:  py -3.13 -I Theory_work/Wave3/W3-MISR/numerics/misr_numerics.py > Theory_work/Wave3/W3-MISR/numerics/misr_numerics_out.txt
"""
import itertools
import math
import sys
import zlib

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
A0 = B0 = 0.01
P = 8                      # candidate columns (exact enumeration over 2^8 models; K = min(p, n//2) = 8 for n >= 16)
NS = [100, 400, 1600, 6400]
REPS = 100
SUBSETS = [S for k in range(P + 1) for S in itertools.combinations(range(P), k)]
LOGW = [math.log(0.5) - (math.lgamma(2 * P) - math.lgamma(k + 1) - math.lgamma(2 * P - k)) for k in range(P + 1)]


def posterior(xr, yr):
    """Exact posterior over all subsets (requires n >= 2P). Returns array aligned with SUBSETS."""
    n = xr.shape[0]
    xc = xr - xr.mean(0)
    X = xc / np.sqrt((xc ** 2).sum(0) / (n - 1))
    yc = yr - yr.mean()
    y = yc / math.sqrt((yc ** 2).sum() / (n - 1))
    G = X.T @ X
    z = X.T @ y
    yy = float(y @ y)
    nu = A0 + n / 2.0
    lp = np.empty(len(SUBSETS))
    for i, S in enumerate(SUBSETS):
        k = len(S)
        if k == 0:
            lp[i] = LOGW[0] - nu * math.log(2 * B0 + yy)
            continue
        idx = list(S)
        GS = G[np.ix_(idx, idx)]
        H = (n + 1) * GS + np.eye(k)
        ldH = np.linalg.slogdet(H)[1]
        ldA = np.linalg.slogdet(GS + np.eye(k))[1]
        zS = z[idx]
        Q = yy - n * float(zS @ np.linalg.solve(H, zS))
        lp[i] = LOGW[k] - 0.5 * (ldH - ldA) - nu * math.log(2 * B0 + Q)
    lp -= lp.max()
    w = np.exp(lp)
    return w / w.sum()


IDX = {S: i for i, S in enumerate(SUBSETS)}


def seed(*key):
    """Deterministic seed from a key (Python's hash() of strings is salted per process)."""
    return zlib.crc32(repr(key).encode("utf-8"))


def design(rng, n, rho=0.3):
    z = rng.standard_normal((n, P))
    f = rng.standard_normal((n, 1))
    return math.sqrt(1 - rho) * z + math.sqrt(rho) * f


def summ(vals):
    a = np.asarray(vals)
    return a.mean(), a.std(ddof=1) / math.sqrt(len(a))


def rn(n):
    return math.sqrt(math.log(n) / n)


def line(tag, n, deltas, hpm_ok, extra=""):
    m, se = summ(deltas)
    print(f"  {tag:<34s} n={n:<5d} E[delta]={m:.4f} (se {se:.4f})  E[delta]/r_n={m / rn(n):.3f}  "
          f"P(HPM=target)={np.mean(hpm_ok):.2f} {extra}")


# ----------------------------------------------------------------------------------------------------------------
def n1():
    print("N1  variance v_n varying with n, signal-to-noise held fixed  (target S0 = {0,1}; raw beta_j^2 = 16 v log n / n; standardised theta_j^2 = sample_SD(x_j)^2 beta_j^2)")
    print("    model: y = x beta_C + x gamma + xi + eps;  beta_C = (b, 0, ...), gamma = (0, b, 0...) [candidate 1 is a proxy];")
    print("    xi ~ N(0, tau_n^2 I), eps ~ N(0, sigma^2 I);  v_n = sigma^2 + tau_n^2")
    regimes = [("sigma2=1, tau2=1 (fixed; v1 case)", lambda n: (1.0, 1.0)),
               ("sigma2=1, tau2=n", lambda n: (1.0, float(n))),
               ("sigma2=1, tau2=n^2", lambda n: (1.0, float(n) ** 2)),
               ("sigma2=1/n, tau2=1/n", lambda n: (1.0 / n, 1.0 / n)),
               ("sigma2=0, tau2=n^-2 (no noise)", lambda n: (0.0, float(n) ** -2))]
    target = IDX[(0, 1)]
    # (i) common random numbers
    print("  (i) common random numbers (same x, same standard normals): max over models of |pi - pi_ref|")
    for n in [100, 1600]:
        worst = 0.0
        for rep in range(5):
            rng = np.random.default_rng(1000 + rep)
            x = design(rng, n)
            g1 = rng.standard_normal(n)
            ref = None
            for name, f in regimes:
                s2, t2 = f(n)
                v = s2 + t2
                b = math.sqrt(16 * v * math.log(n) / n)
                # R'(b) is a statement in law; here the same unit-noise draw g1 is used in every regime, so the
                # posteriors must agree up to rounding (Lemma R'(a) applied to the common standardised response).
                yr = 3.0 + b * x[:, 0] + b * x[:, 1] + math.sqrt(v) * g1
                post = posterior(x, yr)
                if ref is None:
                    ref = post
                worst = max(worst, float(np.abs(post - ref).max()))
        print(f"     n={n}: max |pi - pi_ref| over 5 designs x {len(regimes)} regimes = {worst:.2e}")
    # (ii) independent seeds, full GR mechanism (eps and xi drawn separately)
    print("  (ii) independent draws (eps and xi separately), random design each replicate")
    for name, f in regimes:
        for n in NS:
            rng = np.random.default_rng(seed(name, n))
            d, ok = [], []
            for _ in range(REPS):
                x = design(rng, n)
                s2, t2 = f(n)
                v = s2 + t2
                b = math.sqrt(16 * v * math.log(n) / n)
                yr = -1.0 + b * x[:, 0] + b * x[:, 1] + math.sqrt(t2) * rng.standard_normal(n) + math.sqrt(s2) * rng.standard_normal(n)
                post = posterior(x, yr)
                d.append(1 - post[target]); ok.append(int(np.argmax(post)) == target)
            line(name, n, d, ok)


def n2():
    print("\nN2  fixed raw coefficients, omitted independent column of variance n^(2a)  (tau_n^2 = n^(2a), sigma^2 = 1)")
    print("    y = 1*x_0 + 1*x_1 + x_k + eps, x_k ~ N(0, n^(2a)) independent of the candidates; target {0,1};")
    print("    nominal (population-SD) relative beta-min ratio  beta^2 n / (v log n) ~ n^(1-2a)/log n")
    target = IDX[(0, 1)]
    for a in [0.0, 0.25, 0.4, 0.5, 0.6, 1.0]:
        for n in NS:
            rng = np.random.default_rng(seed("n2", a, n))
            d, ok = [], []
            v = 1.0 + float(n) ** (2 * a)
            for _ in range(REPS):
                x = design(rng, n)
                yr = x[:, 0] + x[:, 1] + float(n) ** a * rng.standard_normal(n) + rng.standard_normal(n)
                post = posterior(x, yr)
                d.append(1 - post[target]); ok.append(int(np.argmax(post)) == target)
            line(f"a={a}", n, d, ok, extra=f" ratio={n / (v * math.log(n)):.2f}")


def n3():
    print("\nN3  outside GR^c  (target {0,1}; raw beta_j^2 = 16 v log n / n, v = 1 the residual variance; standardised theta_j^2 = sample_SD(x_j)^2 beta_j^2)")
    target = IDX[(0, 1)]
    for name in ["(i) t_3 residual (iid, variance 1)", "(ii) heteroscedastic: sd_i = |x_i2| (mean variance 1)"]:
        for n in NS:
            rng = np.random.default_rng(seed(name, n))
            d, ok = [], []
            b = math.sqrt(16 * math.log(n) / n)
            for _ in range(REPS):
                x = design(rng, n)
                if name.startswith("(i)"):
                    e = rng.standard_t(3, n) / math.sqrt(3.0)
                else:
                    e = np.abs(x[:, 2]) * rng.standard_normal(n)
                yr = b * x[:, 0] + b * x[:, 1] + e
                post = posterior(x, yr)
                d.append(1 - post[target]); ok.append(int(np.argmax(post)) == target)
            line(name, n, d, ok)
    print("  (iii) common random slope (C-MIS Example E2): y = x_0 + Z x_1 + eps, Z ~ N(0,1) scalar, eps ~ N(0, I)")
    print("        mean-only target {0}; conditional (F_n contains Z) target {0,1}")
    t0, t01 = IDX[(0,)], IDX[(0, 1)]
    for n in NS:
        rng = np.random.default_rng(seed("n3iii", n))
        m0, m01, weak = [], [], 0
        for _ in range(REPS):
            x = design(rng, n)
            Z = rng.standard_normal()
            yr = x[:, 0] + Z * x[:, 1] + rng.standard_normal(n)
            post = posterior(x, yr)
            m0.append(post[t0]); m01.append(post[t01])
            weak += int(Z * Z * n / math.log(n) < 16)
        print(f"     n={n:<5d} E pi({{0}})={np.mean(m0):.3f}  E pi({{0,1}})={np.mean(m01):.3f}  "
              f"[share of draws with Z^2 n/log n < 16 (nominal conditional margin below 16): {weak / REPS:.2f}]")


def n4():
    print("\nN4  outside (E^sigma): ||mu||^2/(n v) ~ n^b  (fixed raw coefficients 1 on {0,1}; v = n^-b; GR^c holds)")
    target = IDX[(0, 1)]
    for b in [0.0, 0.5, 1.0, 2.0]:
        for n in NS:
            rng = np.random.default_rng(seed("n4", b, n))
            d, ok = [], []
            for _ in range(REPS):
                x = design(rng, n)
                yr = x[:, 0] + x[:, 1] + float(n) ** (-b / 2) * rng.standard_normal(n)
                post = posterior(x, yr)
                d.append(1 - post[target]); ok.append(int(np.argmax(post)) == target)
            line(f"b={b} (energy/(n v) ~ {2.6 * n ** b:.3g})", n, d, ok)


if __name__ == "__main__":
    print(f"W3-MISR numerics; p = {P}, reps = {REPS}, numpy {np.__version__}\n")
    n1(); n2(); n3(); n4()
    print("\nDONE")
