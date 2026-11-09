"""Independent council checks. Writes only its report beside this script.

Run: py -3.13 -B Theory_work/Wave1C/C-PACK/reviews/C1_sol_checks.py
The pre-existing W1-N3 harness is executed, not rebuilt. No production fit,
source mutation, cache write, or git operation is performed.
"""
import sys
sys.dont_write_bytecode = True
import itertools
import math
import random
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'Theory_work/Wave1/W1-N3/numerics'))
import n3lib as nl

counts = Counter()
rng = random.Random(90117)
instances = []
for j in range(600):
    p = 1 + j % 8
    order = list(range(p))
    rng.shuffle(order)
    blocks = []
    while order:
        width = rng.randint(1, min(3, len(order)))
        blocks.append(sorted(order[:width]))
        del order[:width]
    rng.shuffle(blocks)
    k = rng.randint(0, p)
    def draw():
        return rng.randint(-12, 12) * (1.0 if j < 300 else math.ldexp(1.0, rng.randint(-500, 500)))
    lam = [draw() for _ in range(k + 1)]
    rho = [{c: (0.0 if c == 0 else draw())
            for c in range(1 << len(b))} for b in blocks]
    instances.append(nl.Inst(p, k, blocks, lam, rho,
                             [1, 2, 1000000][j % 3], str(j)))
results = nl.run_tables(instances)
for idx, (inst, res) in enumerate(zip(instances, results)):
    sets = list(nl.all_sets(inst))
    vals = [nl.ghat(inst, s) for s in sets]
    best = max(vals)
    assert res['lg0'] == best == nl.ghat(inst, res['S'])
    counts['compiled_rounded_value_membership'] += 1
    opt = [s for s, v in zip(sets, vals) if v == best]
    if len(opt) == 1:
        assert res['S'] == opt[0]
        counts['compiled_unique_rounded_mode'] += 1
    if idx < 300:
        exact = [nl.f_exact(inst, s) for s in sets]
        arg = [s for s, v in zip(sets, exact) if v == max(exact)]
        if len(arg) == 1:
            assert res['S'] == arg[0]
            counts['compiled_UM_unique_exact'] += 1
    # Treat the stored objective as f*, so eta=0; compare the real fold error
    # to I1's gamma_m bound, using exact rationals throughout.
    eps = F(0)
    exact = []
    for s, val in zip(sets, vals):
        ex = nl.f_exact(inst, s)
        exact.append(ex)
        codes = inst.parts(s)
        terms = [F(inst.rho[b][c]) for b, c in enumerate(codes) if c]
        m = len(terms)
        bound = F(m, 2**53 - m) * (abs(F(inst.lam[len(s)])) + sum(map(abs, terms)))
        assert abs(F(val) - ex) <= bound
        eps = max(eps, bound)
        counts['exact_fraction_fold_bounds'] += 1
    target = max(range(len(sets)), key=lambda z: exact[z])
    others = [v for z, v in enumerate(exact) if z != target]
    if not others or exact[target] - max(others) > 2 * eps:
        assert res['S'] == sets[target]
        counts['compiled_FP_TAB_eta_zero'] += 1

# Integer weights eliminate probability roundoff in the SL0/store checks.
for p in range(1, 8):
    for k in range(p + 1):
        omega = [m for m in range(1 << p) if m.bit_count() <= k]
        weights = {m: rng.randint(0, 99) for m in omega}
        weights[0] += 1
        total = sum(weights.values())
        pip = [sum(w for m, w in weights.items() if m & (1 << j)) for j in range(p)]
        for truth in range(1 << p):
            miss = total - weights.get(truth, 0)
            errors = [abs(pip[j] - total * bool(truth & (1 << j))) for j in range(p)]
            assert max(errors) <= miss
            fn = max([errors[j] for j in range(p) if truth & (1 << j)], default=0)
            fp = max([errors[j] for j in range(p) if not truth & (1 << j)], default=0)
            assert fn + fp <= 2 * miss
            if 2 * miss < total:
                assert truth in omega
                assert all(weights[truth] > w for m, w in weights.items() if m != truth)
                assert sum(1 << j for j, v in enumerate(pip) if 2 * v > total) == truth
            counts['SL0_integer_truth_law_pairs'] += 1
            if truth not in omega or weights[truth] == 0:
                continue
            chosen = [m for m in omega if rng.randrange(2)]
            chosen = set(chosen) | {truth}
            mass = sum(weights[m] for m in chosen)
            for j in range(p):
                stored = sum(weights[m] for m in chosen if m & (1 << j))
                err = abs(stored - mass * bool(truth & (1 << j)))
                assert err * total <= miss * mass  # sharper than SL2's 2 delta
            counts['SL2_truth_containing_stores'] += 1

# Check L8's Schur-complement VIS lower bound and small-part leakage for
# 12 seeds, 6 columns, all U and all admissible (T,l). No asymptotic claim.
worst_vis = 0.0
worst_leak = 0.0
for seed in range(12):
    gen = np.random.default_rng(seed + 90117)
    n, p = 40, 6
    x = gen.normal(size=(n, p))
    x -= x.mean(axis=0)
    x /= np.sqrt((x*x).sum(axis=0) / (n-1))
    floor = float(np.linalg.eigvalsh(x.T @ x)[0])
    large = np.array([1.2, 0, -0.8, 0, 0, 0])
    small = np.array([0, 0.02, 0, -0.015, 0.025, 0.01])
    signal_large, signal_small = x @ large, x @ small
    mu = signal_large + signal_small
    def project(ix, y):
        return x[:, ix] @ np.linalg.lstsq(x[:, ix], y, rcond=None)[0] if ix else np.zeros(n)
    support = {0, 2}
    for mask in range(1 << p):
        u = [j for j in range(p) if mask & (1 << j)]
        missing = sorted(support - set(u))
        if missing:
            gain = np.linalg.norm(project(sorted(set(u) | support), mu) - project(u, mu))
            bound = math.sqrt(floor) * np.linalg.norm(large[missing]) - np.linalg.norm(signal_small)
            worst_vis = max(worst_vis, bound - gain)
            assert gain + 1e-10 >= bound
            counts['L8_VIS_subsets'] += 1
        if support <= set(u):
            for j in set(range(p)) - set(u):
                res = x[:, j] - project(u, x[:, j])
                leak = float(res @ mu)**2 / float(res @ res)
                energy = float(signal_small @ signal_small)
                worst_leak = max(worst_leak, leak - energy)
                assert leak <= energy + 1e-10
                counts['L8_leakage_pairs'] += 1
assert .05 + math.sqrt(.2 * 2) > .5
assert .05 + math.sqrt(.2 * 1.001) < .5
counts['L8_epsilon_negative_and_positive_controls'] = 2

lines = ['C1 Sol independent checks: PASS',
         'Python 3.13; seed 90117 for finite tables/laws; 12 Gaussian-design seeds 90117..90128.',
         'No source or git mutation. Only this script and its adjacent output are written.',
         'Pre-existing compiled W1-N3 harness used; not rebuilt in this review.',
         'Table domains p<=8, arbitrary shuffled ordered partitions, K=0..p, cap=1/2/1000000.',
         'FP-TAB tests here take eta=0; nonzero encoding-error cases are in the existing R33 evidence.']
lines += [f'{key}: {value}' for key, value in sorted(counts.items())]
lines += [f'L8 largest positive VIS excess: {worst_vis:.3g}',
          f'L8 largest positive leakage excess: {worst_leak:.3g}',
          'Finite tests are falsification evidence, not proofs of asymptotic probability statements.']
out = '\n'.join(lines) + '\n'
Path(__file__).with_name('C1_sol_checks_out.txt').write_text(out, encoding='utf-8')
print(out)
