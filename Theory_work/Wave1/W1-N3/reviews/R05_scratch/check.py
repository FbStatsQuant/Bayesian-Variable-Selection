import sys, pathlib, runpy, random, math
ROOT = pathlib.Path(__file__).resolve().parents[5]
NUM = ROOT / 'Theory_work/Wave1/W1-N3/numerics'
sys.path.insert(0, str(NUM))
import n3lib as n
from tdp import tdp
n.HARNESS = str(pathlib.Path(__file__).with_name('sm_harness.exe'))

def dm(m, cap):
    K = m + 2
    blocks = [[2*i, 2*i+1] for i in range(m)] + [list(range(2*m, 2*m+4))]
    last = {c: (5 if c in (6,9) else -3) for c in range(1,16)}
    last[0] = 0
    return n.Inst(2*m+4,K,blocks,[0]*(K+1),[{0:0,1:1,2:1,3:-10} for _ in range(m)]+[last],cap,f'm{m}c{cap}')

cases = [dm(m,cap) for m in range(9) for cap in range(1,2**m+1)]
for I,R in zip(cases,n.run_tables(cases)):
    m = (I.p-4)//2
    assert R['S'] == list(range(0,2*m,2))+[2*m+1,2*m+2]
    assert (R['lg0'],R['ties'],R['truncated']) == (m+5,I.cap,1)
print('D_m all caps 1..2^m, m=0..8:',len(cases),'PASS')

for m in range(5):
    I=dm(m,1)
    v,k,A,S=n.prescribed(I)
    expected=[]
    for bits in range(2**m):
        E=[2*i+((bits>>i)&1) for i in range(m)]
        expected += [E+[2*m,2*m+3],E+[2*m+1,2*m+2]]
    assert sorted(expected)==A and len(A)==2**(m+1)
    assert v==m+5 and k==m+2 and S==list(range(0,2*m,2))+[2*m,2*m+3]
    order=sorted(A,key=lambda S:n.dfs_key(I,S))
    assert all(S[-2:]==[2*m+1,2*m+2] for S in order[:2**m])
print('D_m complete maximiser sets / DFS prefix, m=0..4: PASS')

for script in ('cex_family.py','cex_default_cap.py','fp_example.py'):
    print('RERUN',script)
    runpy.run_path(str(NUM/script),run_name='__main__')

rng=random.Random(502)
cases=[]
for z in range(1200):
    p=rng.randrange(1,10)
    xs=list(range(p)); rng.shuffle(xs)
    blocks=[]
    while xs:
        m=rng.randrange(1,min(4,len(xs))+1)
        blocks.append(sorted(xs[:m])); del xs[:m]
    K=rng.randrange(p+1)
    def val():
        e=rng.choice([-1074,-1022,-500,-53,-1,0,1,40,53,500,900])
        return math.ldexp(rng.choice([-1.,1.,1.5,-1.5]),e)
    rho=[{c:(0.0 if c==0 else val()) for c in range(2**len(C))} for C in blocks]
    cases.append(n.Inst(p,K,blocks,[val() for _ in range(K+1)],rho,rng.choice([1,2,10**6]),f'fpwide{z}'))
for I,R in zip(cases,n.run_tables(cases)):
    best,k,A,S=n.prescribed(I,n.ghat)
    assert math.isfinite(best)
    assert R['lg0']==best==n.ghat(I,R['S']) and len(R['S'])==k, (I.iid,R,best,k)
    # Exact dyadic arithmetic oracle for the Python TDP, independent of floating results.
    V,ke,Ae,Se=n.prescribed(I)
    assert tdp(I)==(V,ke,Se),I.iid
print('Wide-exponent, subnormal, cancellation FP and exact Fraction TDP:',len(cases),'PASS')
print('ALL FOCUSED CHECKS PASS')
