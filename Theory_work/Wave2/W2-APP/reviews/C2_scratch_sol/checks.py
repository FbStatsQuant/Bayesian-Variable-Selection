from pathlib import Path
import csv, math, itertools, hashlib
import numpy as np

ROOT = Path('C:/Users/felip/Bayesian-Variable-Selection')
APP = ROOT / 'Theory_work/Wave2/W2-APP'
lines = []
def log(s):
    lines.append(str(s))
    print(s)

# Entire asymptotic sequence: n=2^m, p=m, two equicorrelated
# blocks (floor(m/2), ceil(m/2)), s0=1 in the first block.
# For arbitrary n extend using p=2*floor(log2(n)/2), equal blocks.
log('ENUM boundary counterexample: p=2*floor(log2(n)/2), rho=1/2, s0=1')
for m in [20,40,80,160,320]:
    n=2**m; p=m; g=(p+1)//2; q0=p//2
    N0=max(2500,n,p); H0=(512*N0+2499)//2500
    threshold=(5*H0+4*N0)*p
    assert 2**p <= threshold
    enlarged=p < 2*q0+32+1
    assert enlarged
    log(f'm={m}, p={p}, |Omega|/threshold={2**p/threshold:.8g}, '
        f'(p-s0)/ln(n)={(p-1)/math.log(n):.8g}, g/ln(n)={g/math.log(n):.8g}')
log('Limits: p/ln(n)=1/ln(2), (p-s0)/ln(n)->1/ln(2)>1, '
    'g/ln(n)->1/(2ln(2)); LSF floor=1/2; PTV floor=|theta|/2.')

# Exhaustive inherited-position CD check: all conditioning sets, MA(2),
# non-Markov covariance. Check the exact innovation decomposition too.
p=10
ac=np.array([1+0.8**2+(-0.5)**2,0.8-0.4,-0.5])
S=np.zeros((p,p))
for j in range(p):
    for k in range(p):
        if abs(j-k)<3: S[j,k]=ac[abs(j-k)]/ac[0]
c,C=np.linalg.eigvalsh(S)[[0,-1]]
dist=np.abs(np.subtract.outer(np.arange(p),np.arange(p)))
a=1.; K=np.max(np.abs(S-np.eye(p))*np.exp(dist))
def ts(alpha,K,a):
    return a-np.log1p(1/(alpha/(4*K)+1/np.expm1(a)))
t1=ts(c,K,a); t2=ts(1/C,2/c,t1); K2=2*C
Th=np.linalg.inv(S); maxratio=0.; minvar=1.; nsets=0
for mask in range(2**p-1):
    V=[j for j in range(p) if not mask>>j&1]
    Cv=np.linalg.inv(Th[np.ix_(V,V)])
    bd=K2*np.exp(-t2*dist[np.ix_(V,V)])
    off=~np.eye(len(V),dtype=bool)
    if off.any(): maxratio=max(maxratio,float(np.max(np.abs(Cv[off])/bd[off])))
    minvar=min(minvar,float(np.min(np.diag(Cv))))
    assert np.linalg.eigvalsh(Cv)[0]>=c-1e-12
    assert np.max(np.diag(Cv))<=1+1e-12
    nsets+=1
assert maxratio<=1+1e-12
log(f'CD MA(2): {nsets} conditioning sets, max off-diagonal ratio={maxratio:.9g}, min var={minvar:.9g}, c={c:.9g}')

# Reconstruct outcome totals and the full-scan/screened separation from CSVs.
def rows(f):
    with open(APP/f,newline='',encoding='utf-8-sig') as h:return list(csv.DictReader(h))
key=lambda r:tuple(r[x] for x in ['design','n','p','seed'])
n2=rows('numerics/n2_results.csv'); n3=rows('numerics/n3_merged.csv')
screen=rows('numerics/n3b_results.csv'); sk={key(r) for r in screen}
yes=lambda r,x:r[x]=='True'
assert len(n2)==96 and sum(yes(r,'ls_final_eq_S0') for r in n2)==94
assert all(yes(r,'ls_S0_scored') and yes(r,'ls_certified') for r in n2)
assert sum(float(r['ls_moves'])==int(r['n_extra']) for r in n2)==95
vn=[r for r in n3 if r['design']!='V3b']; ctrl=[r for r in n3 if r['design']=='V3b']
assert len(vn)==40 and len(ctrl)==12 and len(sk)==16
assert all(yes(r,'ls_final_eq_S0') for r in n3)
log(f'n2: 96/96 scored S0 and certification flags; 94 endpoints=S0, 95 moves=extras')
log(f'n3: {len(vn)} VN examples, {sum(key(r) not in sk for r in vn)} full scan, '
    f'{sum(key(r) in sk for r in vn)} screened; {len(ctrl)} full-scan cancellation controls; all endpoints=S0')

# Direct sample eigenspectrum checks from the saved raw design CSVs.
master={r['name']:r for r in rows('data_diag/summary_table.csv')}
for name in ['diabetes_quad','digits']:
    dat=np.genfromtxt(APP/f'data_diag/data/{name}.csv',delimiter=',',names=True)
    names=[x for x in dat.dtype.names if x!='y']
    X=np.column_stack([dat[x] for x in names]); X-=X.mean(0)
    keep=X.std(0,ddof=1)>0; X=X[:,keep]; X/=X.std(0,ddof=1)
    R=X.T@X/(len(X)-1); ev=np.linalg.eigvalsh(R)
    floor=ev[0]; top=ev[-1]/len(ev)
    log(f'{name}: n,p={X.shape}; min eigenvalue={floor:.12g}; top1 share={top:.12g}')
    assert abs(floor-float(master[name]['lam_minR']))<1e-10
    assert abs(top-float(master[name]['top1']))<1e-10

core=ROOT/'Scripts/SMC_BVS/core'; copy=APP/'data_diag/core_copy'; checked=[]
for f in copy.rglob('*'):
    if f.is_file() and f.suffix in ['.R','.h','.cpp']:
        other=core/f.relative_to(copy)
        assert other.exists() and hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256(other.read_bytes()).digest(),str(f)
        checked.append(str(f.relative_to(copy)))
log(f'Core executable/source copy: {len(checked)} files byte-identical')
log('All independent assertions passed.')
Path(__file__).with_name('checks_out.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
