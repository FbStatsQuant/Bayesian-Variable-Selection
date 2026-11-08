"""N4: W7-PART Lemma 2 (Hotelling density bounds (U),(L)), cross-checks, Corollary B / Theorem R constant."""
import time
import numpy as np
import mpmath as mp
from scipy import integrate, stats
from scipy.special import gammaln, hyp2f1, logsumexp
from lhcommon import Tee

out = Tee("n4_pairlaw.txt")
out("N4 n4_pairlaw.py -- Hotelling density, Lemma 2 bounds (U),(L), Corollary B")
rng = np.random.default_rng(20260108)


def logf(x, n, r):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        val = (np.log(n - 2) + gammaln(n - 1) + 0.5 * (n - 1) * np.log1p(-r * r) + 0.5 * (n - 4) * np.log1p(-x * x)
               - 0.5 * np.log(2 * np.pi) - gammaln(n - 0.5) - (n - 1.5) * np.log1p(-r * x)
               + np.log(hyp2f1(0.5, 0.5, n - 0.5, (1 + r * x) / 2.0)))
    return val


def integ(fun, lo, hi, pts=None):
    v, e = integrate.quad(fun, lo, hi, points=pts, epsabs=0, epsrel=1e-11, limit=800)
    return v


def breakpoints(n, r, lo, hi):
    s = (1 - r * r) / np.sqrt(n)
    c = [r + s * k for k in (-8, -4, -2, -1, 0, 1, 2, 4, 8)]
    return [x for x in c if lo + 1e-9 < x < hi - 1e-9]


def log_prob(lo, hi, n, r, ref):
    """log int_lo^hi f(x; n, r) dx computed as ref + log int exp(logf - ref)."""
    v = integ(lambda x: np.exp(logf(x, n, r) - ref), lo, hi, breakpoints(n, r, lo, hi) or None)
    return ref + np.log(v) if v > 0 else -np.inf


def log_upper(t, n, r):          # log P(rhat >= t)
    return log_prob(t, 1.0, n, r, float(logf(t, n, r)))


def log_lower(t, n, r):          # log P(rhat <= t)
    return log_prob(-1.0, t, n, r, float(logf(t, n, r)))


# ------------------------------------------------------------------ 1. density sanity
out("\n=== 1. Hotelling density: normalisation, mpmath check of 2F1, Monte Carlo and Lemma-1 cross-checks ===")
worst = 0.0
for n in (10, 20, 50, 100, 200, 500):
    for r in (-0.9, -0.5, 0.0, 0.3, 0.7, 0.9):
        tot = np.exp(log_prob(-1.0, 1.0, n, r, 0.0))
        worst = max(worst, abs(tot - 1))
out("max |int_{-1}^{1} f - 1| over n in {10,20,50,100,200,500}, r in {-.9,-.5,0,.3,.7,.9}: %.2e" % worst)

mp.mp.dps = 40
dev = 0.0
for n, r, x in [(10, 0.5, 0.3), (20, -0.7, 0.9), (50, 0.9, 0.95), (100, 0.3, -0.5), (200, 0.7, 0.99), (500, 0.9, 0.97), (500, -0.9, 0.5)]:
    z = (1 + r * x) / 2
    ref = mp.hyp2f1(0.5, 0.5, n - 0.5, z)
    dev = max(dev, abs(float(ref) - hyp2f1(0.5, 0.5, n - 0.5, z)) / float(ref))
out("max relative deviation scipy hyp2f1 vs mpmath at 7 points (incl. n=500, z up to .985): %.2e" % dev)

N_MC = 400000


def mc_rhat(n, r, N, rng):
    out_ = np.empty(N)
    chunk = 50000
    for s in range(0, N, chunk):
        m = min(chunk, N - s)
        u = rng.standard_normal((m, n))
        w = rng.standard_normal((m, n))
        vv = r * u + np.sqrt(1 - r * r) * w
        u -= u.mean(1, keepdims=True)
        vv -= vv.mean(1, keepdims=True)
        out_[s:s + m] = (u * vv).sum(1) / np.sqrt((u * u).sum(1) * (vv * vv).sum(1))
    return out_


out("Monte Carlo (%d draws) vs exact Hotelling tails:" % N_MC)
out("%4s %6s %6s %5s | %12s %12s %9s %7s" % ("n", "r", "t", "tail", "exact", "MC", "MC se", "z"))
zmax = 0.0
for (n, r, t, side) in [(10, 0.5, 0.8, "U"), (10, 0.0, 0.5, "U"), (10, 0.7, 0.3, "L"), (20, 0.0, 0.4, "U"), (20, -0.6, -0.8, "L"),
                        (20, 0.7, 0.9, "U"), (50, 0.7, 0.55, "L"), (50, 0.5, 0.65, "U"), (100, 0.7, 0.6, "L"), (100, 0.0, 0.25, "U")]:
    rh = mc_rhat(n, r, N_MC, rng)
    if side == "U":
        ex = np.exp(log_upper(t, n, r)); emp = (rh >= t).mean()
    else:
        ex = np.exp(log_lower(t, n, r)); emp = (rh <= t).mean()
    se = np.sqrt(max(ex * (1 - ex), 1e-300) / N_MC)
    z = (emp - ex) / se
    zmax = max(zmax, abs(z))
    out("%4d %6.2f %6.2f %5s | %12.6e %12.6e %9.2e %7.2f" % (n, r, t, side, ex, emp, se, z))
out("max |z| over the 10 MC comparisons: %.2f" % zmax)

# independent exact route (Lemma 1): T = (Z + a sqrt(W))/sqrt(V/k), conditional on W noncentral t
out("Independent exact route (Lemma 1 mixture of noncentral t, quadrature over W~chi2_{n-1}) for P(rhat >= t):")
for (n, r, t) in [(10, 0.5, 0.8), (20, 0.0, 0.4), (20, 0.7, 0.9), (50, 0.5, 0.65), (50, 0.3, 0.7)]:
    k = n - 2
    a = r / np.sqrt(1 - r * r)
    tau = np.sqrt(k) * t / np.sqrt(1 - t * t)
    fun = lambda w: stats.chi2.pdf(w, n - 1) * stats.nct.sf(tau, k, a * np.sqrt(w))
    v, e = integrate.quad(fun, 0, np.inf, epsabs=0, epsrel=1e-10, limit=400)
    ex = np.exp(log_upper(t, n, r))
    out("  n=%3d r=%.1f t=%.2f: Hotelling %.10e   Lemma-1 mixture %.10e   rel diff %.1e" % (n, r, t, ex, v, abs(v - ex) / ex))

# ------------------------------------------------------------------ 2. Lemma 2 bounds
out("\n=== 2. Lemma 2: (U) t>=r: P(rhat>=t) <= a_n (1+|r|)^{3/2} (1-|r|)^{-1} (1-t) Lambda_r(t)^m ;  (L) t<=r: P(rhat<=t) <= a_n (...)(1+t) Lambda_r(t)^m ===")
NS = [10, 20, 50, 100, 200, 500]
RS = [round(x, 1) for x in np.arange(-0.9, 0.9001, 0.1)]
U_GRID = [0.0, 0.01, 0.03, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 0.95, 0.99, 0.999]


def logbound(n, r, t, side):
    m = (n - 4) / 2.0
    an = np.sqrt((n - 2) / (2 * np.pi))
    lam = np.log1p(-r * r) + np.log1p(-t * t) - 2 * np.log1p(-r * t)
    pref = np.log(an) + 1.5 * np.log1p(abs(r)) - np.log1p(-abs(r))
    return pref + (np.log1p(-t) if side == "U" else np.log1p(t)) + m * lam


t0 = time.time()
res = {"U": [], "L": []}
for n in NS:
    for r in RS:
        for u in U_GRID:
            # (U): t in [r,1)
            t = r + (1 - r) * u
            if t < 1 - 1e-12:
                lr = log_upper(t, n, r) - logbound(n, r, t, "U")
                res["U"].append((lr, n, r, t))
            # (L): t in (-1, r]
            t = -1 + (1 + r) * (1 - u) if u > 0 else r
            t = r - (r + 1) * u
            if t > -1 + 1e-12:
                lr = log_lower(t, n, r) - logbound(n, r, t, "L")
                res["L"].append((lr, n, r, t))
for side in "UL":
    arr = np.array([x[0] for x in res[side]])
    k = int(np.argmax(arr))
    viol = [x for x in res[side] if x[0] > 1e-9]
    out("(%s): %d (n,r,t) triples;  max ratio exact/bound = %.6g at (n,r,t)=(%d,%.1f,%.4f);  min ratio = %.3g;  #violations (ratio>1): %d" %
        (side, len(arr), np.exp(arr[k]), res[side][k][1], res[side][k][2], res[side][k][3], np.exp(arr.min()), len(viol)))
    for x in viol[:10]:
        out("   VIOLATION: n=%d r=%.1f t=%.4f ratio=%.4g" % (x[1], x[2], x[3], np.exp(x[0])))
    # worst by n
    out("   max ratio by n: " + ", ".join("%d: %.3g" % (n, np.exp(max(x[0] for x in res[side] if x[1] == n))) for n in NS))
out("(elapsed %.1fs)" % (time.time() - t0))

# consequences (two-sided forms)
out("\nTwo-sided consequences: |r|<=psib<t: P_r(|rhat|>=t) <= 2 a_n (1+psib)^{3/2}(1-psib)^{-1}(1-t) Lambda_psib(t)^m ;  within: 0<t<rho=r: P(|rhat|<=t) <= a_n (1+rho)^{3/2}(1-rho)^{-1}(1+t) Lambda_rho(t)^m")
viol2, mx_c, cnt = [], -np.inf, 0
for n in NS:
    for pb in (0.1, 0.3, 0.5, 0.7, 0.9):
        for r in (-pb, -pb / 2, 0.0, pb / 2, pb):
            for u in (0.05, 0.2, 0.5, 0.8, 0.95):
                t = pb + (1 - pb) * u
                lp = logsumexp([log_upper(t, n, r), log_upper(t, n, -r)])      # P(rhat>=t)+P(rhat<=-t)
                lb = np.log(2) + logbound(n, pb, t, "U")
                cnt += 1
                mx_c = max(mx_c, lp - lb)
                if lp - lb > 1e-9:
                    viol2.append((n, pb, r, t, np.exp(lp - lb)))
out("cross form: %d triples, max ratio exact/bound = %.4g, violations: %s" % (cnt, np.exp(mx_c), "none" if not viol2 else viol2[:10]))
viol3, mx_w, cnt = [], -np.inf, 0
for n in NS:
    for rho in (0.3, 0.5, 0.7, 0.9):
        for u in (0.05, 0.2, 0.5, 0.8, 0.95, 1.0):
            t = rho * u
            if t <= 0:
                continue
            # P(|rhat|<=t) = int_{-t}^{t} f_rho
            ref = float(logf(t, n, rho))
            lp = log_prob(-t, t, n, rho, ref)
            lb = logbound(n, rho, t, "L")
            cnt += 1
            mx_w = max(mx_w, lp - lb)
            if lp - lb > 1e-9:
                viol3.append((n, rho, t, np.exp(lp - lb)))
out("within form: %d triples, max ratio exact/bound = %.4g, violations: %s" % (cnt, np.exp(mx_w), "none" if not viol3 else viol3[:10]))

# ------------------------------------------------------------------ 3. Corollary B
out("\n=== 3. Corollary B: rho=0.7, psib=0.5 ===")
rho, pb = 0.7, 0.5
q = np.sqrt((1 - pb**2) / (1 - rho**2))
ts = (q - 1) / (q * rho - pb)
lam_r = (1 - rho**2) * (1 - ts**2) / (1 - rho * ts) ** 2
lam_p = (1 - pb**2) * (1 - ts**2) / (1 - pb * ts) ** 2
Is = -0.5 * np.log(lam_r)
out("q = %.6f, t* = %.6f, Lambda_rho(t*) = %.8f, Lambda_psib(t*) = %.8f (equal: %s), I* = %.6f (W7 claims 0.0126)" %
    (q, ts, lam_r, lam_p, abs(lam_r - lam_p) < 1e-12, Is))
g = 10
bad = []
out("%5s %6s | %12s | %12s %12s | %10s %10s | %s" % ("p", "n", "log LHS(Cor.B)", "log N_w*P_w", "log N_x*P_x", "log RHSexact", "log Bexplicit", "LHS/exactRHS  LHS>=exact?  LHS>=B-explicit?"))
for p in (100, 500):
    Nw = (p // g) * g * (g - 1) / 2.0
    Nx = p * (p - 1) / 2.0 - Nw
    for n in (200, 1000, 5000):
        lhs = np.log(2 / (np.sqrt(np.pi) * (1 - rho))) + 2 * np.log(p) + 0.5 * np.log(n) - (n - 4) * Is
        Pw = log_prob(-ts, ts, n, rho, float(logf(ts, n, rho)))
        Px = logsumexp([log_upper(ts, n, pb), log_upper(ts, n, -pb)])
        rhs = logsumexp([np.log(Nw) + Pw, np.log(Nx) + Px])
        bexp = logsumexp([np.log(Nw) + logbound(n, rho, ts, "L"), np.log(Nx) + np.log(2) + logbound(n, pb, ts, "U")])
        ok1, ok2 = lhs >= rhs - 1e-9, lhs >= bexp - 1e-9
        out("%5d %6d | %12.3f | %12.3f %12.3f | %10.3f %10.3f | ratio=%.4g  %s  %s" %
            (p, n, lhs, np.log(Nw) + Pw, np.log(Nx) + Px, rhs, bexp, np.exp(min(lhs - rhs, 700)), ok1, ok2))
        if not (ok1 and ok2):
            bad.append((p, n))
out("Corollary B violations:", "none" if not bad else bad)
out("Note: LHS>1 for n=200 (vacuous as a probability bound); the check is that LHS dominates the exact union bound.")

# Also: Corollary B across other (rho, psib) pairs -- extra falsification attempt of the closed form
out("\nExtra: Cor. B LHS >= B-explicit and >= exact union bound for other (rho,psib), p=500, g=10, n in {200,1000}:")
badx = []
for rho_ in (0.5, 0.7, 0.85, 0.95):
    for pb_ in (0.0, 0.2, 0.4, 0.6):
        if pb_ >= rho_:
            continue
        q_ = np.sqrt((1 - pb_**2) / (1 - rho_**2)); t_ = (q_ - 1) / (q_ * rho_ - pb_)
        I_ = -0.5 * np.log((1 - rho_**2) * (1 - t_**2) / (1 - rho_ * t_) ** 2)
        for n in (200, 1000):
            p = 500
            Nw = (p // g) * g * (g - 1) / 2.0; Nx = p * (p - 1) / 2.0 - Nw
            lhs = np.log(2 / (np.sqrt(np.pi) * (1 - rho_))) + 2 * np.log(p) + 0.5 * np.log(n) - (n - 4) * I_
            Pw = log_prob(-t_, t_, n, rho_, float(logf(t_, n, rho_)))
            Px = logsumexp([log_upper(t_, n, pb_), log_upper(t_, n, -pb_)])
            rhs = logsumexp([np.log(Nw) + Pw, np.log(Nx) + Px])
            bexp = logsumexp([np.log(Nw) + logbound(n, rho_, t_, "L"), np.log(Nx) + np.log(2) + logbound(n, pb_, t_, "U")])
            flag = (lhs >= rhs - 1e-9) and (lhs >= bexp - 1e-9)
            out("  rho=%.2f psib=%.2f n=%4d: t*=%.3f I*=%.4f  logLHS=%9.3f logExact=%9.3f logBexpl=%9.3f  ok=%s" % (rho_, pb_, n, t_, I_, lhs, rhs, bexp, flag))
            if not flag:
                badx.append((rho_, pb_, n))
out("extra violations:", "none" if not badx else badx)
out("\nDONE")
out.close()
