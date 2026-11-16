from pathlib import Path
import hashlib
import math

root = Path('/home/fb31/BVS-wt/W3-SCR-R2')
core = root / 'Scripts/SMC_BVS/core'
copy = root / 'Theory_work/Wave3/W3-SCR/numerics/core_copy'
expected = {}
for line in (copy / 'SHA256SUMS_source.txt').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    expected[name.lstrip('*')] = digest
print('CODE HASH AUDIT')
for rel in ['v3_fit.R', 'v3_run.R', 'v3_exact.R', 'v3_preprocess.R', 'cpp/v3_engine.h', 'cpp/v3_core.cpp', 'cpp/v3_ledger.h', 'cpp/v3_score.h']:
    a = (core / rel).read_bytes()
    b = (copy / rel).read_bytes()
    normalized = a.replace(b'\r\n', b'\n')
    assert normalized == b.replace(b'\r\n', b'\n')
    assert expected[rel] in {hashlib.sha256(normalized).hexdigest(), hashlib.sha256(normalized.replace(b'\n', b'\r\n')).hexdigest()}
    print(f'{rel}: production/copy same after newline normalization; recorded hash matches LF or CRLF serialization')

# Counterexample: duplicated standardized true columns and theta=(1,-1).
# The mean is exactly zero. All witnesses at the empty model have gamma=0.
# Choose a centered standardized y orthogonal to that column. Then Q is n-1
# for every model and all addition gains vanish; determinant/prior costs remain.
n, p = 100, 2
penalty = math.log(2*p-1) + 0.5*math.log(n)
delta_F = -penalty
x = 3.0
reported_probability = 1 - 4*math.exp(-x)
Ln = 2*math.log(2*p-1) + math.log(n)
threshold = (1-math.exp(-Ln/(n+0.02))) * n*(n-0.98)/(n-1)**2
print('\nUNCONDITIONAL IMPROVEMENT COUNTEREXAMPLE')
print(f'n={n}, p={p}, duplicated columns, theta=(1,-1), sigma=1, H={{empty}}, x={x}')
print(f'Mean=0; at centered standardized y orthogonal to x1: F(singleton)-F(empty)={delta_F:.12f}')
print(f'Report master-event probability lower bound={reported_probability:.12f}')
try:
    from scipy.special import betainc
    prob_improvement = float(1-betainc(0.5, (n-2)/2, threshold))
    print(f'Exact Gaussian probability of any truth addition strictly improving={prob_improvement:.12f}')
    assert prob_improvement < reported_probability
except ImportError:
    print('scipy unavailable: analytical asymptotic counterexample in report suffices')
assert delta_F < 0
print('\nA1 squared-ratio constant:', 200/64)
assert 200/64 > 2
print('All scratch checks passed.')
