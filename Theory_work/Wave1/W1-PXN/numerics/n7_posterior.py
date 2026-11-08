"""N7: miniature of (P): 1 - pi(S0) on the p=10 design for increasing n.  pi0-free (no start)."""
import numpy as np
from lhcommon import Tee
from enumlib import *

out = Tee("n7_posterior.txt")
out("N7 n7_posterior.py -- miniature of (P); p=10 (g=2, c=2 linked pairs, 1 null group), rho=.7, psi=.5, beta=1, sigma=1; 20 seeds per n")
out("Far from p >> n: sanity check only that 1 - pi(S0) decreases.")
NS = [100, 400, 1600, 6400]
NSEEDS = 20
summ = []
for n in NS:
    d, miss, over, ok, mapok, big = [], [], [], 0, 0, []
    for seed in range(NSEEDS):
        X, y = make_data(n, [20260108, 7, n, seed])
        F, K = enumerate_F(X, y)
        l1 = log1m_pi(F, S0)
        d.append(np.exp(l1))
        if np.exp(l1) > 0.5:
            mp_ = min(F, key=lambda k: -F[k])
            big.append((seed, round(float(np.exp(l1)), 3), mp_))
        keys = list(F.keys())
        f = np.array([F[k] for k in keys])
        w = np.exp(f - f.max()); w /= w.sum()
        sup = np.array([set(S0) < set(k) for k in keys])
        notsup = np.array([not set(S0) <= set(k) for k in keys])
        over.append(w[sup].sum())
        miss.append(w[notsup].sum())
        ok += int(F[S0] == max(F.values()))
        mapok += int(w[keys.index(S0)] > 0.5)
    d = np.array(d)
    r = d / np.sqrt(np.log(n) / n)
    summ.append((n, np.median(d), np.quantile(d, 0.9), np.median(r), np.quantile(r, 0.9)))
    out("\nn = %d" % n)
    out("  1 - pi(S0):                median = %.4e   90%% quantile = %.4e   max = %.4e   min = %.4e" % (np.median(d), np.quantile(d, 0.9), d.max(), d.min()))
    out("  (1-pi(S0))/sqrt(log n/n):  median = %.4f   90%% quantile = %.4f   max = %.4f" % (np.median(r), np.quantile(r, 0.9), r.max()))
    out("  decomposition of 1-pi(S0): median mass of strict supersets of S0 = %.3e ; median mass of models not containing S0 = %.3e" %
        (np.median(over), np.median(miss)))
    out("  (1-pi(S0))*sqrt(n):         median = %.3f   90%% quantile = %.3f   (heavy right tail expected: e^{Z^2/2} has infinite mean)" % (np.median(d * np.sqrt(n)), np.quantile(d * np.sqrt(n), 0.9)))
    out("  seeds with 1-pi(S0) > 1/2: %d  %s" % (len(big), big))
    out("  MAP = S0 in %d/%d seeds;  pi(S0) > 1/2 in %d/%d seeds" % (ok, NSEEDS, mapok, NSEEDS))
out("\nMonotonicity of the median / 90%% quantile of 1-pi(S0) in n: median decreasing = %s ; q90 decreasing = %s" %
    (all(summ[i][1] > summ[i + 1][1] for i in range(len(NS) - 1)), all(summ[i][2] > summ[i + 1][2] for i in range(len(NS) - 1))))
out("Ratio (1-pi)/sqrt(log n/n) median by n: " + ", ".join("%d: %.3f" % (s[0], s[3]) for s in summ))
out("Ratio q90 by n:                          " + ", ".join("%d: %.3f" % (s[0], s[4]) for s in summ))
out("\nDONE")
out.close()
