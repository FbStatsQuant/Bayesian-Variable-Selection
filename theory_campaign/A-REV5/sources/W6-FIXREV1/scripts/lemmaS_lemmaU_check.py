"""Lemma S (ESS share) attainment domain, and the Lemma U limiting constant.  Seed 20261105.

Lemma S: w_1..w_H > 0, ESS = (sum w)^2 / sum w^2 >= eH, |A| = fH  =>  omega(A) >= max(0, f - sqrt(f(1-f)(1/e-1))).
  (S1) exact rational check that the two-level weights are positive iff f > 1-e, and attain equality there;
  (S2) for f <= 1-e: weights eps on A and 1 off A keep ESS >= eH and omega(A) -> 0 (infimum 0, not attained);
  (S3) random positive weights: worst slack of the strengthened inequality;
  (S4) Kantorovich threshold r* = (11 + 2 sqrt 10)/9.
Lemma U: kappa_n = (1+phi^-2)/(2 phi^2 (n-1)) + nu (1.02 + 1/(n phi^2)) / (c_E n), nu = 0.01 + n/2,
  c_E = sigma^2/(8(M + 2 sigma^2)):  monotone decreasing, limit 0.51/c_E, and the first n with kappa_n <= 0.52/c_E.
"""
import json
import math
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

OUT = {}
# ---------------- Lemma S ----------------
mp.mp.dps = 40
s1 = []
for e in [mp.mpf('0.9'), mp.mpf('0.5'), mp.mpf('0.95')]:
    c = 1 / e - 1
    for f in [mp.mpf(x) / 100 for x in (1, 5, 9, 10, 11, 20, 50, 90, 99)]:
        wA = 1 - mp.sqrt(c * (1 - f) / f)
        wB = 1 + mp.sqrt(c * f / (1 - f))
        # mean-one normalisation: f wA + (1-f) wB = 1 ; mean square = 1/e
        mean = f * wA + (1 - f) * wB
        msq = f * wA ** 2 + (1 - f) * wB ** 2
        share = f * wA / mean
        bound = f - mp.sqrt(f * (1 - f) * c)
        s1.append(dict(e=float(e), f=float(f), one_minus_e=float(1 - e), wA=float(wA), positive=bool(wA > 0),
                       f_gt_1me=bool(f > 1 - e), mean=float(mean), ess_over_H=float(1 / msq),
                       share_minus_bound=float(share - bound)))
assert all(r['positive'] == r['f_gt_1me'] for r in s1 if abs(r['f'] - r['one_minus_e']) > 1e-12)
OUT['S1_two_level'] = s1

s2 = []
for (e, f) in [(Fr(9, 10), Fr(1, 20)), (Fr(9, 10), Fr(1, 10)), (Fr(1, 2), Fr(3, 10))]:
    rows = []
    for eps in [Fr(1, 10), Fr(1, 100), Fr(1, 10000)]:
        ess = (f * eps + (1 - f)) ** 2 / (f * eps ** 2 + (1 - f))   # ESS / H, exact
        omega = f * eps / (f * eps + (1 - f))
        rows.append(dict(eps=float(eps), ess_over_H=float(ess), ess_ok=bool(ess >= e), omega=float(omega)))
    s2.append(dict(e=float(e), f=float(f), rows=rows))
OUT['S2_infimum_zero'] = s2

rng = np.random.default_rng(20261105)
worst = math.inf
for _ in range(20000):
    H = int(rng.integers(2, 60))
    law = rng.integers(3)
    w = [rng.exponential(1, H), rng.lognormal(0, rng.uniform(0, 2), H), rng.uniform(0.01, 1, H)][law]
    ess = w.sum() ** 2 / (w ** 2).sum()
    e = ess / H
    k = int(rng.integers(0, H + 1))
    A = np.argsort(w)[:k]                      # smallest weights: the adversarial subset
    f = k / H
    om = w[A].sum() / w.sum()
    bnd = max(0.0, f - math.sqrt(max(0.0, f * (1 - f) * (1 / e - 1))))
    worst = min(worst, om - bnd)
OUT['S3_random_worst_slack'] = worst

rstar = (11 + 2 * mp.sqrt(10)) / 9
OUT['S4'] = dict(rstar=float(rstar), kant_at_rstar=float(4 * rstar / (1 + rstar) ** 2),
                 kant_at_1925=float(4 * mp.mpf('1.925') / (1 + mp.mpf('1.925')) ** 2))

# ---------------- Lemma U ----------------
rowsU = []
for (M, sig2, phi2) in [(1.0, 1.0, 0.5), (0.4, 1.0, 0.8), (3.0, 1.0, 0.2), (1.0, 0.25, 0.5)]:
    cE = sig2 / (8 * (M + 2 * sig2))

    def kappa(n):
        nu = 0.01 + n / 2
        return (1 + 1 / phi2) / (2 * phi2 * (n - 1)) + nu * (1.02 + 1 / (n * phi2)) / (cE * n)
    ns = [10, 100, 1000, 10 ** 4, 10 ** 6, 10 ** 9]
    ks = [kappa(n) for n in ns]
    mono = all(kappa(n) > kappa(n + 1) for n in range(3, 5000))
    n1 = next(n for n in range(3, 10 ** 7) if kappa(n) <= 0.52 / cE)
    rowsU.append(dict(M=M, sigma2=sig2, phi0sq=phi2, cE=cE, kappa=dict(zip(map(str, ns), ks)),
                      limit_051=0.51 / cE, printed_052=0.52 / cE, decreasing_n_3_5000=mono,
                      first_n_kappa_le_052=n1, kappa_1e9_minus_051=kappa(10 ** 9) - 0.51 / cE))
OUT['lemmaU'] = rowsU
print(json.dumps(OUT, indent=1))
with open(__file__.rsplit('/', 2)[0] + '/results/lemmaS_lemmaU_check.json', 'w') as fh:
    json.dump(OUT, fh, indent=1)
