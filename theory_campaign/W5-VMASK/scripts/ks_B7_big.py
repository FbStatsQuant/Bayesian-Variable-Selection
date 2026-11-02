"""Follow-up to ks_lemmaB.py: B7a gave KS p = 0.022 at psi = 0.5 (one of 20 tests). Re-test the masked-hub law with
20000 fresh reps (seed 9300), only the columns needed (pair unit 1 and the response). Output appended to
../results/ks_lemmaB.txt"""
import numpy as np
from scipy import stats
from vm_core import lh_spec, gen_lh_iid
n, G, g = 120, 8, 10
units, theta, S0, Sref, M, groups = lh_spec(G, g, 0.7, [0.5, 0.5], [1.0, -1.0], [1.0])
rng = np.random.default_rng(9300)
r2 = []
for _ in range(20000):
    Xr, yr = gen_lh_iid(n, G, g, units, theta, rng)
    r2.append(np.corrcoef(Xr[:, 10], yr)[0, 1] ** 2)
pv = stats.kstest(r2, stats.beta(0.5, (n - 2) / 2).cdf).pvalue
s = f"B7a re-test (psi = 0.5, 20000 reps, seed 9300): KS p = {pv:.3g}, mean {np.mean(r2):.5f} vs {0.5/(0.5+(n-2)/2):.5f}"
print(s)
open("../results/ks_lemmaB.txt", "a").write(s + "\n")
