"""Check of Lemma 3 (rotation invariance): for independent groups, conditionally on the within-group correlation
matrices, a cross correlation r_hat_jk has the null law, whatever the within-group statistics are. Test: KS of
r_hat_jk^2 against Beta(1/2,(n-2)/2), overall and within strata of (f_j, f_k) (the first-merge similarities, which
are functions of the within-group matrices), and Spearman correlation between |r_hat_jk| and f_j.
Seed fixed. Output: results/check_lemma3.txt"""
import numpy as np
from scipy import stats
from part_core import correlation, group_tree

rng = np.random.default_rng(99)
n, g, rho, reps = 60, 10, 0.5, 6000
R, F1, F2, M1 = [], [], [], []
for _ in range(reps):
    f = rng.standard_normal(n); X1 = np.sqrt(rho) * f[:, None] + np.sqrt(1 - rho) * rng.standard_normal((n, g))
    f = rng.standard_normal(n); X2 = np.sqrt(rho) * f[:, None] + np.sqrt(1 - rho) * rng.standard_normal((n, g))
    r = correlation(np.hstack([X1, X2]))
    t1 = group_tree(r[:g, :g]); t2 = group_tree(r[g:, g:])
    fj = [1 - nd[2] for nd in t1 if len(nd[0]) == 1]  # leaves listed first, in index order
    fk = [1 - nd[2] for nd in t2 if len(nd[0]) == 1]
    R.append(r[0, g]); F1.append(fj[0]); F2.append(fk[0]); M1.append(np.abs(r[:g, :g][np.triu_indices(g, 1)]).min())
R, F1, F2, M1 = map(np.array, (R, F1, F2, M1))
out = [f"n={n} g={g} rho={rho} reps={reps}: cross pair (j=0 of group 1, k=0 of group 2)"]
null = stats.beta(0.5, (n - 2) / 2)
out.append(f"KS r^2 vs Beta(1/2,(n-2)/2), all: p = {stats.kstest(R**2, null.cdf).pvalue:.3f}")
for name, Fv in (("f_j", F1), ("f_k", F2), ("m_h", M1)):
    q = np.quantile(Fv, [0, 1/3, 2/3, 1])
    for i in range(3):
        sel = (Fv >= q[i]) & (Fv <= q[i + 1])
        out.append(f"  stratum {name} tercile {i+1}: KS p = {stats.kstest(R[sel]**2, null.cdf).pvalue:.3f} (N={sel.sum()})")
    out.append(f"  Spearman(|r_jk|, {name}) = {stats.spearmanr(np.abs(R), Fv).statistic:+.4f} (p = {stats.spearmanr(np.abs(R), Fv).pvalue:.3f})")
open("../results/check_lemma3.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
