"""Checks of pairlaw.py: (1) the density integrates to 1; (2) exact tails (Hotelling density) == noncentral-t
quadrature; (3) exact tails == Monte Carlo; (4) the explicit Lemma-2 bounds dominate the exact tails; (5) the
regression representation (Lemma 1) holds in distribution (KS). Seed fixed. Output: results/check_pairlaw.txt"""
import math, numpy as np, mpmath as mp
from scipy import stats
from pairlaw import *

rng = np.random.default_rng(7)
out = []
for n in (30, 200):
    for r in (0.0, 0.3, 0.7):
        tot = mp.quad(lambda x: dens(x, r, n), [-1, r, 1])
        out.append(f"n={n} r={r}: integral of density = {mp.nstr(tot, 15)}")
out.append("")
out.append("exact tail (density) vs noncentral-t quadrature vs Monte Carlo (1e6 draws) vs Lemma-2 bound")
for n in (30, 200):
    for (r, t, side) in [(0.0, 0.25, "U"), (0.3, 0.45, "U"), (0.5, 0.6, "U"), (0.7, 0.55, "L"), (0.7, 0.45, "L"),
                         (0.0, 0.40, "U"), (0.245, 0.45, "U")]:
        if side == "U":
            ex = float(upper(t, r, n)); nc = nct_upper(t, r, n); ub = ub_upper(t, r, n)
        else:
            ex = float(lower(t, r, n)); nc = 1 - nct_upper(t, r, n); ub = ub_lower(t, r, n)
        m = 1_000_000
        u = rng.standard_normal((m, n)) if n <= 30 else None
        # MC via the representation is checked separately; here direct simulation in chunks
        cnt = 0; tot = 0
        for _ in range(10 if n == 30 else 2):
            mm = 100_000
            a = rng.standard_normal((mm, n)); b = r * a + math.sqrt(1 - r * r) * rng.standard_normal((mm, n))
            a -= a.mean(1, keepdims=True); b -= b.mean(1, keepdims=True)
            rh = (a * b).sum(1) / np.sqrt((a * a).sum(1) * (b * b).sum(1))
            cnt += int((rh >= t).sum() if side == "U" else (rh <= t).sum()); tot += mm
        mc = cnt / tot
        out.append(f"n={n:4d} r={r:5.3f} t={t:4.2f} {side}: exact={ex:.6e} nct={nc:.6e} MC={mc:.3e} (N={tot}) "
                   f"bound={ub:.3e} bound/exact={ub/ex:.2f}")
out.append("")
# (5) representation: T = (Z + a sqrt W)/sqrt(V/k) vs sqrt(k) r/sqrt(1-r^2) from direct simulation
for (n, r) in [(20, 0.6), (200, 0.3)]:
    k = n - 2; a = r / math.sqrt(1 - r * r); mm = 20000
    Z = rng.standard_normal(mm); W = rng.chisquare(n - 1, mm); V = rng.chisquare(k, mm)
    T1 = (Z + a * np.sqrt(W)) / np.sqrt(V / k)
    A = rng.standard_normal((mm, n)); Bm = r * A + math.sqrt(1 - r * r) * rng.standard_normal((mm, n))
    A -= A.mean(1, keepdims=True); Bm -= Bm.mean(1, keepdims=True)
    rh = (A * Bm).sum(1) / np.sqrt((A * A).sum(1) * (Bm * Bm).sum(1))
    T2 = math.sqrt(k) * rh / np.sqrt(1 - rh * rh)
    out.append(f"Lemma 1 representation n={n} r={r}: two-sample KS p = {stats.ks_2samp(T1, T2).pvalue:.3f}")
# (6) Lemma-2 bound domination on a grid (exact tails), n in {10, 50, 200, 1000}
viol = 0; worst = 1e300; cnt = 0
for n in (10, 50, 200, 1000):
    for r in np.linspace(-0.6, 0.9, 7):
        for t in np.linspace(-0.8, 0.95, 8):
            if abs(t - r) < 1e-9:
                continue
            if t > r:
                ex = float(upper(t, r, n)); ub = ub_upper(t, r, n)
            else:
                ex = float(lower(t, r, n)); ub = ub_lower(t, r, n)
            cnt += 1
            if ex > 0:
                worst = min(worst, ub / ex)
            if ub < ex * (1 - 1e-12):
                viol += 1
out.append(f"Lemma 2 grid check: {cnt} (n, r, t) cases, violations = {viol}, min bound/exact = {worst:.3f}")
open("../results/check_pairlaw.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
