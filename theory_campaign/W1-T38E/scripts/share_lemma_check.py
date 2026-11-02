#!/usr/bin/env python3
"""W1-T38E: check of the deterministic ESS share lemma (Lemma S).
For weights w_1..w_H with population ESS (sum w)^2/sum w^2 >= e*H and a subset A of fraction f,
the weighted share omega(A) >= f - sqrt(f(1-f)(1/e - 1)).  Also checks tightness (two-level weights).
Fixed seed."""
import numpy as np
rng = np.random.default_rng(7)
worst = np.inf
for trial in range(200000):
    H = rng.integers(2, 60)
    w = rng.exponential(1.0, H) ** rng.uniform(0, 3)
    ess = w.sum() ** 2 / (w ** 2).sum() / H
    k = rng.integers(1, H)
    A = rng.choice(H, k, replace=False)
    f = k / H
    omega = w[A].sum() / w.sum()
    bound = f - np.sqrt(f * (1 - f) * (1 / ess - 1))
    worst = min(worst, omega - bound)
print("min over 200000 random cases of (omega - bound) = %.3e (must be >= -1e-12)" % worst)
# tightness: A gets weight a, complement weight b, chosen so the bound is attained
for f, e in [(0.3, 0.9), (0.5, 0.9), (0.8, 0.9), (0.15, 0.9)]:
    H = 1000; k = int(f * H)
    c2 = 1 / e - 1                     # CV^2
    # normalized weights: mean 1; A: 1 - s*sqrt((1-f)/f), A^c: 1 + s*sqrt(f/(1-f)), CV^2 = s^2
    s = np.sqrt(c2)
    wa = 1 - s * np.sqrt((1 - f) / f); wb = 1 + s * np.sqrt(f / (1 - f))
    if wa < 0:
        print("f=%.2f e=%.2f: bound negative (A can be killed), wa<0 -> clipped" % (f, e)); continue
    w = np.r_[np.full(k, wa), np.full(H - k, wb)]
    ess = w.sum() ** 2 / (w ** 2).sum() / H
    print("f=%.2f e=%.2f: ess=%.4f omega=%.6f bound=%.6f" % (f, e, ess, w[:k].sum() / w.sum(), f - np.sqrt(f * (1 - f) * (1 / e - 1))))
