"""N1: Lemma Tr-J (PROOF s3) falsification.  (a) truncated moment, (b) tail, (c-core) chi2 tail with t' >= 6j."""
import numpy as np
from scipy import integrate, stats
from scipy.special import gammaln, logsumexp
from lhcommon import Tee

out = Tee("n1_trJ.txt")
out("N1 n1_trJ.py -- Lemma Tr-J numerical falsification")

NS = [50, 100, 200, 800]
US = [0, 1, 5, 20]
TAUS = [0.01, 0.05, 0.2, 0.5]
JS = range(1, 25)


def log_exact_trunc(j, m, n, tau):
    """log E[(1-X)^{-nu} 1{X<=tau}], X ~ Beta(j/2,(m-j)/2); substitution x = tau w^{1/a} removes the x^{a-1} singularity."""
    a = j / 2.0
    b = (m - j) / 2.0
    nu = 0.01 + n / 2.0
    e1 = nu + 1 - b           # exponent of (1-x): b-1-nu = -e1
    logB = gammaln(a) + gammaln(b) - gammaln(a + b)
    f = lambda w: np.exp(-e1 * np.log1p(-tau * w ** (1.0 / a)))
    val, err = integrate.quad(f, 0.0, 1.0, epsabs=0, epsrel=1e-12, limit=400)
    return a * np.log(tau) - np.log(a) - logB + np.log(val), e1


def log_exact_trunc_direct(j, m, n, tau):
    """independent route (only for a>=1): direct quad of the density in x."""
    a = j / 2.0
    b = (m - j) / 2.0
    nu = 0.01 + n / 2.0
    logB = gammaln(a) + gammaln(b) - gammaln(a + b)
    f = lambda x: np.exp((a - 1) * np.log(x) + (b - 1 - nu) * np.log1p(-x) - logB)
    val, err = integrate.quad(f, 0.0, tau, epsabs=0, epsrel=1e-12, limit=400)
    return np.log(val)


# ------------------------------------------------------------------ (a)
out("\n=== (a) truncated moment:  E[(1-X)^-nu 1{X<=tau}]  <=  2^e1 (m tau/2)^{j/2} / Gamma(j/2+1) ===")
out("grid: n in", NS, " u in", US, " tau in", TAUS, " j in 1..24  (m = n-1-u)")
maxlr = -np.inf
arg = None
viol = []
ncell = 0
by_tau = {t: -np.inf for t in TAUS}
by_j = {j: -np.inf for j in JS}
chk_dev = 0.0
for n in NS:
    for u in US:
        m = n - 1 - u
        for tau in TAUS:
            for j in JS:
                if m - j < 1:
                    continue
                lex, e1 = log_exact_trunc(j, m, n, tau)
                e1_paper = (u + j + 3) / 2.0 + 0.01
                assert abs(e1 - e1_paper) < 1e-9, (e1, e1_paper)
                lb = e1_paper * np.log(2.0) + (j / 2.0) * np.log(m * tau / 2.0) - gammaln(j / 2.0 + 1)
                lr = lex - lb
                ncell += 1
                by_tau[tau] = max(by_tau[tau], lr)
                by_j[j] = max(by_j[j], lr)
                if lr > maxlr:
                    maxlr, arg = lr, (n, u, tau, j)
                if lr > 1e-9:
                    viol.append((n, u, tau, j, lr))
                if j >= 2 and ncell % 37 == 0:
                    chk_dev = max(chk_dev, abs(lex - log_exact_trunc_direct(j, m, n, tau)))
out("cells evaluated:", ncell)
out("self-check: max |log exact (substitution) - log exact (direct x-quad)| on a subsample (j>=2): %.2e" % chk_dev)
out("max ratio exact/bound = %.6g  (log = %.4f) at (n,u,tau,j) = %s" % (np.exp(maxlr), maxlr, arg))
out("max ratio by tau:", {t: float("%.4g" % np.exp(v)) for t, v in by_tau.items()})
out("max ratio by j (j=1,2,4,8,12,16,20,24):", {j: float("%.4g" % np.exp(by_j[j])) for j in [1, 2, 4, 8, 12, 16, 20, 24]})
out("VIOLATIONS of (a):", "none" if not viol else viol)

# ------------------------------------------------------------------ (b)
out("\n=== (b) tail:  P(X>tau) <= exp(-(m-j)/16) + P(chi2_j > tau (m-j)/2) ===")
maxlr = -np.inf
arg = None
viol = []
ncell = 0
for n in NS:
    for u in US:
        m = n - 1 - u
        for tau in TAUS:
            for j in JS:
                if m - j < 1:
                    continue
                lex = stats.beta.logsf(tau, j / 2.0, (m - j) / 2.0)
                lb = logsumexp([-(m - j) / 16.0, stats.chi2.logsf(tau * (m - j) / 2.0, j)])
                lr = lex - lb
                ncell += 1
                if lr > maxlr:
                    maxlr, arg = lr, (n, u, tau, j)
                if lr > 1e-9:
                    viol.append((n, u, tau, j, lr))
out("cells evaluated:", ncell)
out("max ratio exact/bound = %.6g (log %.4f) at (n,u,tau,j) = %s" % (np.exp(maxlr), maxlr, arg))
out("VIOLATIONS of (b):", "none" if not viol else viol)

# ------------------------------------------------------------------ (c-core)
out("\n=== (c-core) P(chi2_j > t') <= exp(-t'/2 + sqrt(j t')) for t' >= 6j ===")
viol = []
maxlr = -np.inf
arg = None
for j in range(1, 31):
    tp = 6.0 * j + np.concatenate([np.linspace(0, 100, 2001), np.linspace(100, 4000, 3000)[1:]])
    lex = stats.chi2.logsf(tp, j)
    lb = -tp / 2.0 + np.sqrt(j * tp)
    lr = lex - lb
    k = np.argmax(lr)
    if lr[k] > maxlr:
        maxlr, arg = lr[k], (j, tp[k])
    for kk in np.nonzero(lr > 1e-9)[0]:
        viol.append((j, tp[kk], lr[kk]))
out("grid: t' = 6j + [0..4000], 5000 pts per j; j = 1..30")
out("max ratio exact/bound over t' >= 6j = %.6g (log %.4f) at (j, t') = %s" % (np.exp(maxlr), maxlr, arg))
out("VIOLATIONS of (c-core) on t'>=6j:", "none" if not viol else viol[:20])

out("\nSlack of the condition t' >= 6j: scan r = t'/j on a fine grid [1,10] (step 0.001);")
out("'first fail' = smallest r where P(chi2_j>t') > exp(-t'/2+sqrt(j t')); 'last fail' = largest such r.")
out("(for r<4 the bound exceeds 1 so it cannot fail; the claim is only used for r>=6)")
rg = np.arange(1.0, 10.0 + 1e-12, 0.001)
rows = []
for j in range(1, 31):
    tp = rg * j
    lr = stats.chi2.logsf(tp, j) - (-tp / 2.0 + np.sqrt(j * tp))
    bad = np.nonzero(lr > 1e-12)[0]
    if len(bad):
        rows.append((j, rg[bad[0]], rg[bad[-1]], len(bad)))
        out("j=%2d  first fail r=%.3f  last fail r=%.3f  (#failing grid pts=%d)" % (j, rg[bad[0]], rg[bad[-1]], len(bad)))
    else:
        out("j=%2d  no failure anywhere on r in [1,10]  (max log-ratio %.4f at r=%.3f)" % (j, lr.max(), rg[np.argmax(lr)]))
if rows:
    out("largest 'last fail' ratio over j:", max(r[2] for r in rows), " (must be < 6 for the lemma's condition to be safe)")
out("\nDONE")
out.close()
