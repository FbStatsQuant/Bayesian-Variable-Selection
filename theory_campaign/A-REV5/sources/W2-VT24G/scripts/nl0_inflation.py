"""W2-VT24G: check W1 PROOF.md §6 claim 'equicorrelated nulls (r = 0.3) give inflation ~1.86 in Z^2'.
For Z ~ N(0, (1-r) I + r 11^T) (p nulls), the pairwise partial statistic is T_{l|l'} = (Z_l - r Z_l')^2/(1-r^2).
Compare max_{l != l'} T / (2 log p) with (1+r)/(1-r) (W1's value) and (1+r) (factor-model value). Seed 5."""
import numpy as np, json, sys
rng = np.random.default_rng(5); r = 0.3; out = []
for p in [100, 1000, 10000, 100000, 1000000]:
    vals = []
    for rep in range(20):
        Z = np.sqrt(r) * rng.standard_normal() + np.sqrt(1 - r) * rng.standard_normal(p)
        i, j = np.argmax(Z), np.argmin(Z)
        # max over ordered pairs of (Z_l - r Z_l')^2 is attained at (argmax, argmin) or (argmin, argmax)
        t = max((Z[i] - r * Z[j]) ** 2, (Z[j] - r * Z[i]) ** 2) / (1 - r ** 2)
        vals.append(t / (2 * np.log(p)))
    rec = dict(p=p, median_ratio=float(np.median(vals)), max_ratio=float(np.max(vals)))
    out.append(rec); print(rec)
print('W1 value (1+r)/(1-r) =', (1 + r) / (1 - r), ' factor-model value 1+r =', 1 + r)
json.dump(dict(r=r, rows=out, w1=(1 + r) / (1 - r), factor=1 + r), open(sys.argv[1], 'w'), indent=1)
