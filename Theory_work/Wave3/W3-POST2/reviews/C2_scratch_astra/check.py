from fractions import Fraction
from math import ceil, comb, log, sqrt
from pathlib import Path

out = []
card_count = 0
ratio_count = 0
for p in range(2, 31):
    for s in range(1, p + 1):
        for A in (Fraction(1), Fraction(5, 4), Fraction(2), Fraction(5)):
            j = ceil((2 * A + 1) * s) + 1
            for K in range(s, p + 1):
                for inside in range(s):
                    for excess in range(min(j, p-s) + 1):
                        size = inside + excess
                        if size > K:
                            continue
                        assert size <= min(s+j-1, K) <= min(s+j, K)
                        card_count += 1
            for B in (j, s+j):
                for m in range(s, min(B, p)):
                    prod = Fraction(comb(p, s))
                    for i in range(s, m+1):
                        rho = Fraction(p-i, 2*p-1-i)
                        assert rho >= Fraction(1, 4*B)
                        prod *= rho
                    exact = Fraction(comb(p, m+1)*comb(2*p-1, s), comb(2*p-1, m+1))
                    assert prod == exact
                    assert exact >= Fraction(1, (4*B)**B)
                    ratio_count += 1
out.append(f'Cutoff cardinality tuples checked: {card_count}; all pass.')
out.append(f'E0 exact product/lower-bound instances checked: {ratio_count}; all pass.')
best = (float('inf'), None)
count = 0
for s in range(1, 21):
    for k in range(1000, 10001):
        A = k/1000
        j = ((2*k+1000)*s + 999)//1000 + 1
        CA = 8 + 3*A
        Cx = A*j + s + log(j+1) + 2
        Cstar = 2*s + 3*(A*j+s+log(j+1)+1)
        c0 = max(4*Cstar, 32*(s*(A+1)+2))
        c1 = (sqrt(2*Cx)+sqrt(2*Cx+CA*j+2/log(2)*(s*(A+1)+2)))**2
        assert c1 > c0
        if c1/c0 < best[0]:
            best = (c1/c0, (s, A, j, c0, c1))
        count += 1
out.append(f'c1/c0 grid: {count} points, A=1,1.001,...,10; all >1; minimum {best}.')
out.append('Finite checks supplement the analytic argument; no continuum or asymptotic theorem inferred from them.')
result = '\n'.join(out) + '\n'
Path(__file__).with_name('check_out.txt').write_text(result)
print(result, end='')
