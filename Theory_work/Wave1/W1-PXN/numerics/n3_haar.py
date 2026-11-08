"""N3: Haar-span step of Lemma Lambda(a) and Lemma B (PROOF s5, s8.2).  LH-iid, n=60, p=40, g=10, c=1, v=1 (groups: 1-2 linked pair, 3 visible, 4 null)."""
import time
import numpy as np
from scipy import stats
from lhcommon import *

out = Tee("n3_haar.txt")
out("N3 n3_haar.py -- Haar-span step, Lemma Lambda(a) and Lemma B; n=60, p=40, g=10, rho=.7, psi=.5, beta=beta_vis=1, sigma=1")
n, p, g, c, v, rho, psi, beta, bvis, sigma = 60, 40, 10, 1, 1, 0.7, np.array([0.5]), np.array([1.0]), np.array([1.0]), 1.0
NSEEDS, NDRAW = 5, 2000
Sigma = build_sigma(p, g, c, rho, psi)
theta = build_theta(p, g, c, v, psi, beta, bvis)
L = np.linalg.cholesky(Sigma)
ja, jb, jv = 0, g, 2 * g          # hubs of group 1 (a), group 2 (b), group 3 (visible)
null = list(range(3 * g, 4 * g))  # group 4
out("hubs: j_a=%d, j_b=%d, j_vis=%d; null group = %d..%d; lambda_min(Sigma) = %.4f" % (ja, jb, jv, null[0], null[-1], np.linalg.eigvalsh(Sigma)[0]))

# ---- tests of type "Lambda": W = (Lam_As - Lam_A)/Lam_As ~ Beta(|A0|/2, (n-1-|As|-|A0|)/2)
LAM_TESTS = [
    ("Lam1: A_s={j_a}, A_0=2 null members", [ja], null[:2]),
    ("Lam2: A_s={j_a}, A_0=3 null members", [ja], null[:3]),
    ("Lam3: A_s={j_a,j_vis}, A_0=2 null members", [ja, jv], null[:2]),
    ("Lam4: A_s={} (empty), A_0=2 null members", [], null[:2]),
    ("Lam5: A_s={j_a}, A_0=1 null member", [ja], null[:1]),
]
# ---- tests of type "B": x = 1 - RSS_{U+V}/RSS_U (RSS on y incl. noise) ~ Beta(|V|/2, (n-1-|U|-|V|)/2)
B_TESTS = [
    ("B(i'): U={j_a, a-nonhub 1}, l = a-nonhub 2 (neutral)", [ja, 1], [2]),
    ("B(i): a-group U0={j_a}, V={a-nonhub 1,2}", [ja], [1, 2]),
    ("B(i): b-group U0={}, V={j_b}  (masked hub, F2)", [], [jb]),
    ("B(i): b-group U0={}, V={j_b, proxy}", [], [jb, jb + 1]),
    ("B(i): visible group U0={j_vis}, V={vis nonhub}", [jv], [jv + 1]),
    ("B(ii): A = S0 minus b = {j_a, j_vis} + null member 31, l = null 32", [ja, jv, 31], [32]),
    ("B(i) null group U0={}, V={2 null members}", [], null[:2]),
    ("NEG-CONTROL: a-group U={}, V={j_a} (j_a carries signal) -- should NOT be the Beta law", [], [ja]),
]

nT = len(LAM_TESTS) + len(B_TESTS)
data = [[[] for _ in range(NSEEDS)] for _ in range(nT)]
t0 = time.time()
for seed in range(NSEEDS):
    rng = np.random.default_rng([20260108, 3, seed])
    for d in range(NDRAW):
        Xr, yr = draw_raw(rng, n, L, theta, sigma)
        Xc = Xr - Xr.mean(0)
        Y = yr - yr.mean()
        mu = Xc @ theta
        idx = 0
        for (_, As, A0) in LAM_TESTS:
            r1 = proj_resid(mu, Xc[:, As]) if As else mu
            r2 = proj_resid(mu, Xc[:, As + A0])
            lam_s, lam_a = float(r1 @ r1), float(r2 @ r2)
            data[idx][seed].append((lam_s - lam_a) / lam_s)
            idx += 1
        for (_, U, V) in B_TESTS:
            r1 = proj_resid(Y, Xc[:, U]) if U else Y
            r2 = proj_resid(Y, Xc[:, U + V])
            data[idx][seed].append(1.0 - float(r2 @ r2) / float(r1 @ r1))
            idx += 1
out("simulation: %d seeds x %d draws = %d draws per test, %.1fs" % (NSEEDS, NDRAW, NSEEDS * NDRAW, time.time() - t0))

out("\n%-95s %8s %8s | %8s %8s | %s" % ("test", "a", "b", "meanEmp", "meanThy", "KS p-values per seed | pooled KS p | #seeds p<.05"))
idx = 0
summary = []
for (name, As, A0) in LAM_TESTS:
    a, b = len(A0) / 2.0, (n - 1 - len(As) - len(A0)) / 2.0
    summary.append((name, a, b, idx)); idx += 1
for (name, U, V) in B_TESTS:
    a, b = len(V) / 2.0, (n - 1 - len(U) - len(V)) / 2.0
    summary.append((name, a, b, idx)); idx += 1
n_bad_pooled = []
for (name, a, b, i) in summary:
    cdf = stats.beta(a, b).cdf
    ps = [stats.kstest(np.array(data[i][s]), cdf).pvalue for s in range(NSEEDS)]
    allv = np.concatenate([np.array(data[i][s]) for s in range(NSEEDS)])
    pp = stats.kstest(allv, cdf).pvalue
    se = np.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)) / allv.size)
    out("%-95s %8.2f %8.2f | %8.5f %8.5f | %s | %.4f | %d" % (name[:95], a, b, allv.mean(), a / (a + b),
                                                                 " ".join("%.3f" % q for q in ps), pp, sum(q < 0.05 for q in ps)))
    out("%95s   mean z-score = %.2f, var emp/thy = %.3f" % ("", (allv.mean() - a / (a + b)) / se, allv.var() / (a * b / ((a + b) ** 2 * (a + b + 1)))))
    if not name.startswith("NEG"):
        n_bad_pooled.append((name, pp))
out("\nExpected under a correct Beta law: per-seed p-values ~ U(0,1) (about 5% below .05); pooled p-value uniform.")
bad = [x for x in n_bad_pooled if x[1] < 0.01]
out("Pooled KS p < 0.01 among the non-control tests:", "none" if not bad else bad)
out("(NEG-CONTROL row demonstrates the KS test has power: the Beta law must be rejected there.)")
out("\nDONE")
out.close()
