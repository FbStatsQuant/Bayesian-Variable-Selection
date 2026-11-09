"""Independent UM-FP falsification attempt, using the existing frozen C++ harness.

Run from any directory: python -B R33_falsify.py
Writes only its sibling R33_falsify_out.txt. No imports from repo modules.
Exact Fraction oracles compute mathematical f*, table error eta and gamma_m
sum-absolute-values bound epsilon; the test does not round those inequalities.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import math
import random
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HARNESS = ROOT / 'Theory_work/Wave1/W1-N3/numerics/sm_harness.exe'
HEADER = ROOT / 'Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp/v3_start.h'
U = F(1, 2**53)
SEED = 33082026
rng = random.Random(SEED)
cases = []


def add(family, blocks, K, lam, rho, cap=1, perturb=False):
    # rho entries above K are NaN, as in build_tables; never used by oracle.
    lm = [F(x) for x in lam]
    rm = [[F(x) if math.isfinite(x) else None for x in row] for row in rho]
    if perturb:
        # Independent exact-real mathematical tables, not claimed to be scorer data.
        lm = [x + rng.choice([-1, 0, 1]) * max(abs(x), F(1)) / 2**54 for x in lm]
        for row in rm:
            for c in range(1, len(row)):
                if row[c] is not None:
                    row[c] += rng.choice([-1, 0, 1]) * max(abs(row[c]), F(1)) / 2**54
    cases.append((family, blocks, K, lam, rho, cap, lm, rm))


# K=0 and empty winner, cap=1 (flag true even at one visited maximiser).
add('K0', [[0, 1], [2]], 0, [7.0], [[0.0, math.nan, math.nan, math.nan], [0.0, math.nan]])
add('empty', [[0], [1]], 2, [0.0, -10.0, -20.0], [[0.0, -1.0], [0.0, -1.0]])
# Subnormal addition and cancellation: valid gradual-underflow arithmetic.
tiny = math.ulp(0.0)
add('subnormal', [[1], [0]], 2, [0.0, 0.0, 0.0], [[0.0, tiny], [0.0, 2*tiny]])
add('subnormal', [[0], [1]], 2, [-tiny, 0.0, 0.0], [[0.0, tiny], [0.0, -tiny]])
# Unique exact-table winner {0,2}, but rounding makes the smaller {0} win.
# This MUST be rejected by the strict UM-FP hypothesis (negative control).
add('negative_control', [[0], [1, 2]], 2, [0.0, 0.0, 0.0],
    [[0.0, 1000.0], [0.0, 1e-14, 2e-14, -5.0]])
# Same unordered partition/objective; cap=1 ties make output order-dependent.
add('order_control', [[0], [1]], 1, [-10.0, 0.0], [[0.0, 1.0], [0.0, 1.0]])
add('order_control', [[1], [0]], 1, [-10.0, 0.0], [[0.0, 1.0], [0.0, 1.0]])

for trial in range(2400):
    p = rng.randint(1, 8)
    K = rng.randint(0, p)
    idx = list(range(p))
    rng.shuffle(idx)
    blocks = []
    while idx:
        size = rng.randint(1, min(3, len(idx)))
        blocks.append(sorted(idx[:size]))
        del idx[:size]
    family = ['integer', 'ulp', 'cancellation', 'wide', 'table_error', 'subnormal'][trial % 6]
    scale = {'integer': 1.0, 'ulp': 2.0**rng.randint(0, 52),
             'cancellation': 2.0**rng.randint(20, 52),
             'wide': 2.0**rng.randint(-500, 500),
             'table_error': 2.0**rng.randint(-10, 45), 'subnormal': tiny}[family]

    def value():
        if family == 'ulp':
            return rng.choice([-1, 1]) * (scale + rng.randint(-3, 3) * math.ulp(scale))
        if family == 'cancellation':
            return rng.choice([-scale, scale, -1.0, 1.0, 0.0])
        return rng.randint(-10, 10) * scale

    lam = [value() for _ in range(K+1)]
    rho = [[0.0] + [value() if c.bit_count() <= K else math.nan
                    for c in range(1, 1 << len(b))] for b in blocks]
    add(family, blocks, K, lam, rho, rng.choice([1, 2, 1000000]), family == 'table_error')

encoded = []
oracles = []
for number, (family, blocks, K, lam, rho, cap, lm, rm) in enumerate(cases):
    p = sum(map(len, blocks))
    encoded += [f'T r{number} {p} {K} {len(blocks)} {cap}', ' '.join(x.hex() for x in lam)]
    for b, row in zip(blocks, rho):
        encoded += [f'{len(b)} ' + ' '.join(map(str, b)), ' '.join(x.hex() for x in row)]
    vals = []
    eta, eps = F(0), F(0)
    for k in range(K+1):
        for S in combinations(range(p), k):
            selected = set(S)
            stored = F(lam[k])
            mathematical = lm[k]
            abs_sum = abs(stored)
            folded = 0.0
            m = 0
            for b, row, exact_row in zip(blocks, rho, rm):
                code = sum(1 << pos for pos, x in enumerate(b) if x in selected)
                if code:
                    m += 1
                    x = row[code]
                    stored += F(x)
                    mathematical += exact_row[code]
                    abs_sum += abs(F(x))
                    folded += x
            g = lam[k] + folded
            bound = m*U/(1-m*U) * abs_sum
            assert abs(F(g)-stored) <= bound, ('fold bound', number, S)
            eta = max(eta, abs(stored-mathematical))
            eps = max(eps, bound)
            vals.append((mathematical, S, g))
    vals.sort(key=lambda x: x[0], reverse=True)
    R = vals[0][1]
    # K=0 has a singleton feasible domain: explicitly use Delta=+infinity.
    margin = vals[0][0]-vals[1][0] if len(vals)>1 else None
    condition = margin is None or margin > 2*(eta+eps)
    max_g = max(x[2] for x in vals)
    oracles.append((family, R, margin, eta, eps, condition, vals, max_g))

completed = subprocess.run([str(HARNESS)], input='\n'.join(encoded)+'\n',
                           capture_output=True, text=True, check=True)
lines = completed.stdout.splitlines()
assert len(lines) == len(cases), (len(lines), len(cases), completed.stderr)
counts = Counter()
failures = []
negative = []
order_results = []
for number, (line, oracle) in enumerate(zip(lines, oracles)):
    t = line.split()
    assert t[0:2] == ['R', f'r{number}']
    got = tuple(map(int, t[6:]))
    assert len(got) == int(t[5])
    gcode = float.fromhex(t[2])
    family, R, margin, eta, eps, condition, vals, max_g = oracle
    counts[(family, 'total')] += 1
    gotvals = [x for x in vals if x[1] == got]
    if not gotvals or gotvals[0][2] != gcode or gcode != max_g:
        failures.append(('N3(e)', number, line))
    if condition:
        counts[(family, 'condition')] += 1
        if got != R:
            failures.append(('UM-FP', number, R, got, str(margin), str(eta), str(eps)))
    if got != R and (margin is None or margin > 0):
        counts[(family, 'unique_exact_mismatch_outside')] += 1
        if family == 'negative_control':
            negative.append(f'case={number} R={R} got={got} Delta={float(margin):.17g} '
                            f'2(eta+eps)={float(2*(eta+eps)):.17g} condition={condition}')
    if number in [0, 1]:
        assert got == R and t[3:5] == ['1', '1'], line
    if family == 'order_control':
        order_results.append(got)

assert negative, 'Negative control failed to exercise a unique-exact-winner disagreement'
assert order_results == [(0,), (1,)], order_results
report = [
    'R33 independent UM-FP falsification attempt',
    f'Python: {sys.version.split()[0]}; seed={SEED}',
    f'Harness: {HARNESS.relative_to(ROOT)}',
    f'Harness SHA256: {hashlib.sha256(HARNESS.read_bytes()).hexdigest()}',
    f'Frozen header SHA256: {hashlib.sha256(HEADER.read_bytes()).hexdigest()}',
    'Harness TABLE input; all stored finite values transferred losslessly as hex floats.',
    'All feasible subsets enumerated (p<=8). Exact Fraction oracle for f*, eta, epsilon, Delta.',
    'Independent mathematical-table perturbations included; no scorer-error guarantee inferred.',
    'Every set checked against the recursive-summation bound, including subnormals and cancellation.',
    'K=0 tested with explicit Delta=+infinity convention (missing from reviewed text).',
    'Unread above-K entries are NaN. Block order shuffled. Caps 1, 2, 1000000.',
    '', 'family: total / satisfying strict UM-FP condition / unique-exact mismatch outside condition',
]
for family in sorted({x[0] for x in cases}):
    report.append(f'{family}: {counts[family,"total"]} / {counts[family,"condition"]} / '
                  f'{counts[family,"unique_exact_mismatch_outside"]}')
report += ['', f'TOTAL={len(cases)}; CONDITION_PASSED={sum(v for (f,k),v in counts.items() if k=="condition")}',
           f'FAILURES={len(failures)}', 'Negative control:'] + negative
report += ['Failure details:'] + [repr(x) for x in failures]
report += [f'Order controls: cap=1, same unordered singleton partition/objective, outputs={order_results}.',
           'These are tied objectives; they refute order-invariance off uniqueness, not UM-FP.']
report += ['Conclusion: no counterexample with Delta > 2(eta+epsilon) found.' if not failures else 'COUNTEREXAMPLE/FAILURE FOUND.',
           'This finite abstract-table test is not a proof and does not validate FP-TAB for the coded scorer.']
result = '\n'.join(report)+'\n'
HERE.joinpath('R33_falsify_out.txt').write_text(result, encoding='utf-8')
print(result)
assert not failures
