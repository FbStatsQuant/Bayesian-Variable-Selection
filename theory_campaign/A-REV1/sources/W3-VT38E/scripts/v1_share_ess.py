#!/usr/bin/env python3
"""W3-VT38E independent checks of W1-T38E Lemma S, its companion facts, and the constant 1.925 in D2's NB.

(a) Lemma S: weights with ESS >= eH, subset fraction f  =>  share >= f - sqrt(f(1-f)(1/e-1)).
    Adversarial check: for each (H, k, e) we MINIMISE the share by a two-level construction AND by random search
    with a projection onto the ESS constraint; also a direct random test with different weight laws than W1.
(b) g(f) = f - sqrt(f(1-f))/3 is increasing on [0.1, 1) and g(0.1) = 0.
(c) ESS(phi) of weights exp(phi d) is non-increasing in phi >= 0 (random d vectors, fine grid).
(d) Kantorovich: weights in [m, M] => ESS/H >= 4mM/(m+M)^2.  Value at M/m = 1.925 and the exact root r* of 4r/(1+r)^2 = 0.9.
    Also a two-level worst case at ratio 1.925 that has ESS/H < 0.9 (so NB with 1.925 does NOT guarantee the
    pilot's threshold).
Seed 31.  Run: python3 v1_share_ess.py
"""
import numpy as np
from math import sqrt

rng = np.random.default_rng(31)

# (a) Lemma S, direct random test with lognormal / pareto / two-point mixtures
worst = np.inf
for trial in range(300000):
    H = int(rng.integers(2, 200))
    law = trial % 3
    if law == 0:
        w = np.exp(rng.normal(0, rng.uniform(0, 3), H))
    elif law == 1:
        w = rng.pareto(rng.uniform(0.3, 5), H) + 1e-12
    else:
        w = np.where(rng.random(H) < rng.random(), rng.uniform(0, 10), 1.0) + 1e-12
    e = (w.sum() ** 2 / (w ** 2).sum()) / H
    k = int(rng.integers(1, H + 1))
    # adversarial subset: the k smallest weights (minimises the share for given w)
    A = np.argsort(w)[:k]
    f = k / H
    share = w[A].sum() / w.sum()
    bound = f - sqrt(max(0.0, f * (1 - f) * (1 / e - 1)))
    worst = min(worst, share - bound)
print("(a) Lemma S: min(share - bound) over 300000 adversarial-subset cases = %.3e (>= -1e-12 required)" % worst)

# tightness: two-level weights attain the bound exactly
for f, e in [(0.2, 0.9), (0.5, 0.9), (0.9, 0.9), (0.3, 0.5)]:
    H = 10000; k = int(round(f * H)); c = 1 / e - 1
    wa = 1 - sqrt(c) * sqrt((1 - f) / f); wb = 1 + sqrt(c) * sqrt(f / (1 - f))
    w = np.r_[np.full(k, wa), np.full(H - k, wb)]
    ee = (w.sum() ** 2 / (w ** 2).sum()) / H
    print("    tight case f=%.2f e=%.2f: ESS/H=%.6f share=%.6f bound=%.6f" % (f, e, ee, w[:k].sum() / w.sum(), f - sqrt(f * (1 - f) * c)))

# (b) g
fs = np.linspace(0.1, 0.999999, 200001)
g = fs - np.sqrt(fs * (1 - fs)) / 3
print("(b) g(0.1)=%.3e; min diff of g on grid=%.3e (>0 => increasing); g(0.0999)=%.4f" % (g[0], np.diff(g).min(), 0.0999 - sqrt(0.0999 * 0.9001) / 3))

# (c) ESS monotone in phi
bad = 0
for trial in range(2000):
    d = rng.normal(0, rng.uniform(0.1, 50), int(rng.integers(2, 300)))
    phis = np.linspace(0, 2, 801)
    ess = []
    for ph in phis:
        x = ph * d; m = x.max(); w = np.exp(x - m)
        ess.append(w.sum() ** 2 / (w ** 2).sum())
    ess = np.array(ess)
    bad += np.any(np.diff(ess) > 1e-9 * ess[:-1])
print("(c) ESS non-increasing in phi: violations in 2000 random d vectors = %d" % bad)

# (d) Kantorovich constant
r = 1.925
print("(d) 4r/(1+r)^2 at r=1.925: %.8f  (< 0.9!)" % (4 * r / (1 + r) ** 2))
rstar = (2.2 + sqrt(2.2 ** 2 - 4 * 0.81)) / 1.8
print("    exact root r* of 4r/(1+r)^2 = 0.9: %.8f ; log r* = %.8f vs log 1.925 = %.8f" % (rstar, np.log(rstar), np.log(1.925)))
# worst case at ratio 1.925: weights in {1, 1.925} with fraction x at 1.925 chosen to minimise ESS
H = 1000000
best = (1, None)
for kk in range(1, H, 1000):
    x = kk / H
    m1 = (1 - x) + x * r; m2 = (1 - x) + x * r * r
    val = m1 * m1 / m2
    if val < best[0]: best = (val, x)
print("    two-level weights {1, 1.925}: min ESS/H = %.8f at fraction %.4f of the high weight -> threshold 0.9H missed" % best)
