#!/usr/bin/env python3
"""T33 floating-point check (W7-SEC). Seed fixed.

For several designs (well conditioned, near-collinear, exact duplicates, y almost in the span, large n), it
  1. standardises X and y in float64 the way v3_standardise does (main path: x/max|x|, centre, / sample SD);
  2. scores a list of models with the PRODUCTION scorer (v3_score.h compiled by t33_harness.cpp with the
     production flags -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2);
  3. computes the exact value of log m(S), F(S), Q_S, log det H_S, log det A_S ON THE STORED DOUBLES with an exact
     integer Gram and mpmath at 60 digits (the method's a0 = b0 = 1/100 exactly);
  4. evaluates the rigorous bound eta_m(S) of Theorem T33-S (REPORT/PROOF_T33.md) and the engine's heuristic
     error_bound(), and checks the structural facts Q_S >= y'y/(n+1), route = chol, no Q recomputation.
Usage: t33_fp_check.py HARNESS_BINARY
"""
import math, os, struct, subprocess, sys, tempfile
import numpy as np
import mpmath as mp

mp.mp.dps = 60
SEED = 20261103
u = 2.0 ** -53
cL = 2.0          # LIB hypothesis: |fl(log x) - log x| <= cL u |log x|

def standardise(x):
    mx = np.max(np.abs(x)); x1 = x / mx; mu = np.mean(x1); x2 = x1 - mu
    s = math.sqrt(np.sum(x2 * x2) / (len(x) - 1))
    return x2 / s

def int_columns(X):
    """Exact integer representation: X = Xi * 2^-E with Xi integer (object array)."""
    m, e = np.frexp(X)                              # X = m 2^e, 0.5 <= |m| < 1
    E = int(53 - e.min())
    Xi = np.empty(X.shape, dtype=object)
    it = np.nditer(X, flags=["multi_index"])
    for v in it:
        Xi[it.multi_index] = int(mp.mpf(float(v)) * mp.mpf(2) ** E)   # exact (mpf holds doubles exactly)
    return Xi, E

class Exact:
    def __init__(self, X, y):
        self.n, self.p = X.shape
        Xi, E = int_columns(np.column_stack([X, y]))
        self.Xi, self.E = Xi, E
        self.scale = mp.mpf(2) ** (-2 * E)
        n = self.n
        self.yty = mp.mpf(int(np.dot(Xi[:, -1], Xi[:, -1]))) * self.scale
        a0 = b0 = mp.mpf(1) / 100
        self.nu = a0 + mp.mpf(n) / 2
        self.logCn = a0 * mp.log(2 * b0) + mp.loggamma(a0 + mp.mpf(n) / 2) - (mp.mpf(n) / 2) * mp.log(mp.pi) - mp.loggamma(a0)
        self.b0 = b0
        self.logm0 = self.logCn - self.nu * mp.log(2 * b0 + self.yty)
        p = self.p; K = min(p, n // 2); self.K = K
        logw = [-mp.log(2) - (mp.loggamma(2 * p) - mp.loggamma(k + 1) - mp.loggamma(2 * p - k)) for k in range(K + 1)]
        terms = [mp.loggamma(p + 1) - mp.loggamma(k + 1) - mp.loggamma(p - k + 1) + logw[k] for k in range(K + 1)]
        mxv = max(terms); logWK = mxv + mp.log(mp.fsum(mp.e ** (t - mxv) for t in terms))
        self.logprior = [logw[k] - logWK for k in range(K + 1)]
        self.Gdiag = [mp.mpf(int(np.dot(Xi[:, j], Xi[:, j]))) * self.scale for j in range(p)]

    def score(self, S):
        n = self.n; k = len(S)
        if k == 0:
            return dict(logm=self.logm0, Q=self.yty, ldH=mp.mpf(0), ldA=mp.mpf(0), lamH=mp.mpf(1), lamA=mp.mpf(1))
        Xi = self.Xi
        G = mp.matrix(k, k); z = mp.matrix(k, 1)
        for a in range(k):
            for b in range(a, k):
                g = mp.mpf(int(np.dot(Xi[:, S[a]], Xi[:, S[b]]))) * self.scale
                G[a, b] = g; G[b, a] = g
            z[a] = mp.mpf(int(np.dot(Xi[:, S[a]], Xi[:, -1]))) * self.scale
        H = (n + 1) * G + mp.eye(k); A = G + mp.eye(k)
        LH = mp.cholesky(H); LA = mp.cholesky(A)
        ldH = 2 * mp.fsum(mp.log(LH[i, i]) for i in range(k)); ldA = 2 * mp.fsum(mp.log(LA[i, i]) for i in range(k))
        w = mp.lu_solve(LH, z)                      # L w = z (LH lower triangular)
        quad = mp.fsum(w[i] ** 2 for i in range(k))
        Q = self.yty - n * quad
        logm = self.logCn - (ldH - ldA) / 2 - self.nu * mp.log(2 * self.b0 + Q)
        Gf = np.array([[float(G[a, b]) for b in range(k)] for a in range(k)])
        ev = np.linalg.eigvalsh(Gf)
        lamG = max(ev[0], 0.0)
        return dict(logm=logm, Q=Q, ldH=ldH, ldA=ldA, lamH=(n + 1) * lamG + 1, lamA=lamG + 1,
                    lamHmax=(n + 1) * ev[-1] + 1, lamAmax=ev[-1] + 1)

def gamma(j):
    return j * u / (1 - j * u)

def bound(ex, S, r, logCn_err):
    """Theorem T33-S bound eta_m(S) on |log m_hat(S) - log m(S)| for k >= 1; returns (eta_m, parts)."""
    n = ex.n; k = len(S); yty = float(ex.yty); nu = float(ex.nu)
    gS = max(float(ex.Gdiag[j]) for j in S); hS = (n + 1) * gS + 1; aS = gS + 1
    epsH = 1.01 * k * hS * (n + k + 3) * u; epsA = 1.01 * k * aS * (n + k + 2) * u
    epsQ = 1.02 * k * hS * (n + 3 * k + 3) * u
    rhoH = epsH / float(r["lamH"]); rhoA = epsA / float(r["lamA"]); rhoQ = epsQ / float(r["lamH"])
    if max(epsH, epsA, epsQ) > 0.5:
        return math.inf, dict(det=math.inf, Q=math.inf, asm=0, C=logCn_err, kappaH=float(r["lamHmax"] / r["lamH"]))
    lH = math.log(1.01 * hS) + 1; lA = math.log(1.01 * aS) + 1
    etaH = k * rhoH / (1 - rhoH) + 1.01 * (k - 1 + cL) * k * u * lH
    etaA = k * rhoA / (1 - rhoA) + 1.01 * (k - 1 + cL) * k * u * lA
    omega = 1.001 * n * u * math.sqrt(n * k * gS / float(r["lamH"]))
    rQ = gamma(n) + 2.03 * u + ((rhoQ + gamma(k)) / (1 - rhoQ)) * (1 + omega) ** 2 + 2 * omega + omega ** 2
    Q = float(r["Q"]); thetaQ = (yty / Q) * rQ
    if thetaQ > 0.5:
        return math.inf, dict(det=0, Q=math.inf, asm=0, C=logCn_err, kappaH=float(r["lamHmax"] / r["lamH"]))
    larg = abs(math.log(2 * 0.01 + Q))
    etaQ = nu * (thetaQ / (1 - thetaQ) + 1.01 * u) + 1.01 * (cL + 2.01) * u * nu * larg
    logD = float(r["ldH"] - r["ldA"])
    asm = 1.01 * u * (2 * abs(float(ex.logCn)) + 2 * abs(logD) + nu * larg)
    eta = 0.5 * (etaH + etaA) + etaQ + asm + logCn_err
    return eta, dict(det=0.5 * (etaH + etaA), Q=etaQ, asm=asm, C=logCn_err, kappaH=float(r["lamHmax"] / r["lamH"]))

def run_design(name, X, y, models, harness, out):
    n, p = X.shape
    Xs = np.column_stack([standardise(X[:, j]) for j in range(p)])
    ys = standardise(y)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as fh:
        fh.write(struct.pack("<ii", n, p)); fh.write(Xs.astype("<f8").tobytes(order="F")); fh.write(ys.astype("<f8").tobytes())
        fh.write(struct.pack("<i", len(models)))
        for S in models:
            fh.write(struct.pack("<i", len(S))); fh.write(struct.pack(f"<{len(S)}i", *S))
        path = fh.name
    res = subprocess.run([harness, path], capture_output=True, text=True, check=True).stdout.splitlines()
    os.unlink(path)
    hdr = dict(kv.split("=") for kv in res[0].split()[1:])
    lp_hat = [float(v) for v in res[1].split()[1:]]
    ex = Exact(Xs, ys)
    logCn_err = abs(mp.mpf(float(hdr["logCn"])) - ex.logCn)
    prior_err = max(abs(mp.mpf(lp_hat[k]) - ex.logprior[k]) for k in range(ex.K + 1))
    rows = []
    worst_ratio = 0.0; worst_eng = 0.0; minQ = math.inf; routes = set(); qrec = 0; fails = 0
    for line in res[2:]:
        t = line.split()
        m, k = int(t[1]), int(t[2])
        if t[3] == "FAIL":
            fails += 1; continue
        S = models[m]
        logm_hat, F_hat, Q_hat, ldH_hat, ldA_hat, condH, route, qr, eb, condA = map(float, t[3:13])
        routes.add(int(route)); qrec += int(qr)
        r = ex.score(S)
        err = abs(mp.mpf(logm_hat) - r["logm"])
        errF = abs(mp.mpf(F_hat) - (ex.logprior[k] + r["logm"]))
        minQ = min(minQ, float(r["Q"] * (n + 1) / ex.yty))
        if k == 0:
            continue
        eta, parts = bound(ex, S, r, float(logCn_err))
        ratio = float(err) / eta; worst_ratio = max(worst_ratio, ratio)
        worst_eng = max(worst_eng, float(err) / eb)
        rows.append((k, float(err), float(errF), eta, eb, parts["kappaH"], float(ex.yty / r["Q"]),
                     abs(ldH_hat - float(r["ldH"])), abs(Q_hat - float(r["Q"])) / float(r["Q"])))
    out.write(f"\n## {name}: n={n}, p={p}, models={len(models)}\n")
    out.write(f"  constants: |logCn_hat - logCn| = {float(logCn_err):.2e}; max_k |logprior_hat - logprior| = {float(prior_err):.2e}\n")
    out.write(f"  routes used = {sorted(routes)} (0 = chol); Q recomputations = {qrec}; failures = {fails}; "
              f"min_S Q_S (n+1)/y'y = {minQ:.6f} (Lemma T33-Q says >= 1)\n")
    out.write(f"  max observed |logm_hat - logm| / eta_m(S) [rigorous, must be <= 1] = {worst_ratio:.3e}\n")
    out.write(f"  max observed |logm_hat - logm| / engine error_bound [heuristic] = {worst_eng:.3e}\n")
    out.write("  sample rows: k, |dlogm|, |dF|, eta_m (rigorous), engine bound, kappa(H_S), y'y/Q, |dlogdetH|, rel|dQ|\n")
    rows.sort(key=lambda r: -r[1])
    for rr in rows[:6]:
        out.write("   " + "  ".join(f"{v:.3e}" if isinstance(v, float) else f"{v:3d}" for v in rr) + "\n")
    return worst_ratio, worst_eng

def main():
    harness = sys.argv[1]
    rng = np.random.default_rng(SEED)
    out = sys.stdout
    out.write(f"T33 fp check: production scorer vs exact (60 digits) on the stored doubles; seed {SEED}; u = 2^-53; cL = {cL}\n")
    # D1: well conditioned
    n, p = 200, 60
    X = rng.standard_normal((n, p)); beta = np.zeros(p); beta[:5] = 0.5
    y = X @ beta + rng.standard_normal(n)
    models = [sorted(rng.choice(p, k, replace=False).tolist()) for k in rng.integers(1, 41, 60)] + [[], list(range(5))]
    run_design("D1 iid Gaussian", X, y, models, harness, out)
    # D2: near-collinear pairs (correlation 1 - O(1e-14))
    n, p = 100, 20
    Z = rng.standard_normal((n, p // 2))
    X = np.empty((n, p)); X[:, 0::2] = Z; X[:, 1::2] = Z + 1e-7 * rng.standard_normal((n, p // 2))
    y = Z[:, 0] - Z[:, 1] + 0.5 * rng.standard_normal(n)
    models = [list(range(2 * k)) for k in range(1, 11)] + [sorted(rng.choice(p, k, replace=False).tolist()) for k in rng.integers(2, 21, 30)]
    run_design("D2 near-collinear pairs (rho ~ 1 - 1e-14)", X, y, models, harness, out)
    # D3: exact duplicate columns
    n, p = 80, 12
    Z = rng.standard_normal((n, p // 2)); X = np.repeat(Z, 2, axis=1)
    y = Z[:, 0] + 0.3 * rng.standard_normal(n)
    models = [list(range(2 * k)) for k in range(1, 7)] + [[0, 1], [0, 1, 2, 3, 4, 5]]
    run_design("D3 exact duplicate columns", X, y, models, harness, out)
    # D4: y almost in the span (R^2 = 1 - 1e-18): maximal cancellation in Q
    n, p = 100, 10
    X = rng.standard_normal((n, p)); y = X[:, :3] @ np.array([1.0, -2.0, 0.5]) + 1e-9 * rng.standard_normal(n)
    models = [[0, 1, 2], [0, 1, 2, 3], list(range(10)), [0, 1], [0]]
    run_design("D4 y almost in span(X_{1:3})", X, y, models, harness, out)
    # D5: larger n
    n, p = 4000, 40
    X = rng.standard_normal((n, p)) + 0.9 * rng.standard_normal((n, 1))      # equicorrelated ~0.45
    y = X[:, :4].sum(axis=1) + rng.standard_normal(n)
    models = [list(range(k)) for k in (1, 5, 10, 20, 40)] + [sorted(rng.choice(p, 15, replace=False).tolist())]
    run_design("D5 n = 4000, equicorrelated", X, y, models, harness, out)

if __name__ == "__main__":
    main()
