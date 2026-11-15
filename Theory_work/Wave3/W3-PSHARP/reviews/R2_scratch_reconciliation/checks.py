from pathlib import Path
import ast
import math
import subprocess
import numpy as np
from scipy.special import gammaln, logsumexp

root = Path.cwd()
ticket = root / 'Theory_work/Wave3/W3-PSHARP'
rel = 'Theory_work/Wave3/W3-PSHARP/'
base = lambda f: subprocess.check_output(['git', 'show', '1f205b2:' + rel + f]).decode('utf-8')
read = lambda f: (ticket / f).read_text(encoding='utf-8')
old, new = base('numerics/b_check.py'), read('numerics/b_check.py')
old = old.replace('    Q_S - Q_{S+j} against generic linear algebra; D ratio <= n; equality iff x_j orthogonal to col X_S.',
                  '    Q_S - Q_{S+j} against generic linear algebra; D ratio <= n (the equality case is not tested here).')
old = old.replace('F1: Lemma S items 1-2 (Schur formulas, D ratio <= n, equality iff orthogonal)',
                  'F1: Lemma S items 1-2 (Schur formulas, D ratio <= n)')
assert ast.dump(ast.parse(old)) == ast.dump(ast.parse(new))
print('b_check.py: only the documented docstring/header changes; computation unchanged')
assert base('numerics/b_check_out.txt').splitlines()[1:] == read('numerics/b_check_out.txt').splitlines()[1:]
print('b_check_out.txt: every line after the first unchanged against 1f205b2')
rerun = (ticket / 'reviews/R2_scratch_reconciliation/b_check_rerun.txt').read_text(encoding='utf-16')
assert rerun.splitlines() == read('numerics/b_check_out.txt').splitlines()
print('Fresh full b_check.py run: all output lines match the frozen output')

def lc(a, k):
    return gammaln(a+1)-gammaln(k+1)-gammaln(a-k+1)

def grouped(n, s, p):
    # Orthogonal standardized columns; y=sum(signal columns)/sqrt(s).
    t = np.arange(s+1)[:, None]
    u = np.arange(p-s+1)[None, :]
    k = t+u
    q0 = (n-1)/n
    q = q0 + ((n-1)**2/n)*(s-t)/s
    logr = (lc(s, t)+lc(p-s, u)+lc(2*p-1, s)-lc(2*p-1, k)
            -.5*(k-s)*math.log(n) - (.01+n/2)*np.log((.02+q)/(.02+q0)))
    logr = np.where(k <= min(p, n//2), logr, -np.inf)
    pi = math.exp(-float(logsumexp(logr)))
    return pi, float(logsumexp(logr[:-1, :]))

for n in (10000, 1000000):
    s = math.isqrt(n)-1
    pi, missing = grouped(n,s,s+1)
    print(f'p=s+1 n={n} s={s}: pi={pi:.10f}, 1/(1+1/sqrt(n))={1/(1+1/math.sqrt(n)):.10f}; log missing odds={missing:.1f}')
    s = math.isqrt(n)
    pi, missing = grouped(n,s,2*s)
    print(f'p=2s n={n} s={s}: pi={pi:.10f}, exp(-1/3)={math.exp(-1/3):.10f}; log missing odds={missing:.1f}')
