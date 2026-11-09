"""Deterministic arithmetic checks for R37; standard library only."""
from fractions import Fraction as F
from math import sqrt
from pathlib import Path

pattern = [F(x) for x in ('1.4', '-1.0', '1.8', '-1.2', '0.8', '-1.6')]
beta = (pattern * 3)[:14]
assert sum(x*x for x in beta) == F('24.64')
# The nine-column equicorrelation matrix has every row sum equal to 3.
assert 1 + 8*F(1, 4) == 3
# Eight off-active coefficients equal theta*epsilon/3.
small_energy_factor = (8 + 8*7*F(1, 4))/9
assert small_energy_factor == F(22, 9)
# Nine null-block coefficients equal 2*theta*epsilon/3.
null_energy_factor = 4*(9 + 9*8*F(1, 4))/9
assert null_energy_factor == 12
eta, a = 0.1, 1
out = [f'sum beta^2 = {sum(x*x for x in beta)} = 24.64',
       'M = 49.28*c^2 + 1',
       'W active coefficient = theta*(1 + epsilon/3)',
       f'W signal-block small energy / ((n-1)*theta^2*epsilon^2) = {small_energy_factor}',
       f'W null-block energy / ((n-1)*theta^2*epsilon^2) = {null_energy_factor}',
       f'eta threshold for A=1 = {(sqrt(3)-sqrt(2))**2:.12f}',
       f'epsilon_0 upper bound for eta=0.1,A=1 = {(1-eta)**2/(8*eta)-a:.12f}']
for eps in (1, 0.001):
    exponent = eta/2 + sqrt(2*eta*(a+eps))
    out.append(f'eta=0.1,A=1,epsilon_0={eps}: exponent={exponent:.12f}, kappa_max={0.5-exponent:.12f}')
result = '\n'.join(out) + '\n'
Path(__file__).with_suffix('.txt').write_text(result, encoding='utf-8')
print(result, end='')
