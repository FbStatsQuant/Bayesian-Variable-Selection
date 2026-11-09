from pathlib import Path
import csv, hashlib, itertools, math
import numpy as np

ROOT = Path.cwd()
APP = ROOT / 'Theory_work/Wave2/W2-APP'
SCRATCH = APP / 'reviews/C3_scratch_sol'
log = []
def say(s):
    print(s)
    log.append(str(s))
def rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

# Re-run the supplied citation checker without writing its original output.
src = (APP / 'citecheck.py').read_text(encoding='utf-8')
src = src.replace('open(os.path.join(HERE, "reviews", "CITECHECK.txt"), "w", encoding="utf-8")',
                  'open(os.path.join(HERE, "reviews", "C3_scratch_sol", "CITECHECK_rerun.txt"), "w", encoding="utf-8")')
ns = {'__file__': str(APP / 'citecheck.py')}
exec(compile(src, str(APP / 'citecheck.py'), 'exec'), ns)
assert ns['bad'] == 0
say('Citation checker: TOTAL MISSES 0 (output redirected to C3 scratch).')

# Exhaustive non-Markov conditional-covariance check, with inherited positions.
p = 10
ma = np.array([1., .55, -.2])
ac = np.correlate(ma, ma, 'full')[2:]
S = np.array([[ac[abs(i-j)]/ac[0] if abs(i-j)<3 else 0.
               for j in range(p)] for i in range(p)])
c, C = np.linalg.eigvalsh(S)[[0,-1]]
a = .7
K = max(abs(S[i,j])*math.exp(a*abs(i-j)) for i in range(p) for j in range(p) if i != j)
def ct(alpha, k, aa):
    u = 1/(alpha/(4*k)+1/math.expm1(aa))
    return aa-math.log1p(u)
t1 = ct(c,K,a)
t2 = ct(1/C,2/c,t1)
Theta = np.linalg.inv(S)
ratio, low, high = 0., 1., 0.
count = 0
for bits in range(2**p-1):
    U = [i for i in range(p) if bits>>i & 1]
    V = [i for i in range(p) if not bits>>i & 1]
    conditional = np.linalg.inv(Theta[np.ix_(V,V)])
    if U:
        schur = S[np.ix_(V,V)] - S[np.ix_(V,U)] @ np.linalg.solve(S[np.ix_(U,U)], S[np.ix_(U,V)])
        assert np.max(abs(conditional-schur)) < 1e-12
    ev = np.linalg.eigvalsh(conditional)
    assert ev[0] >= c-1e-12 and ev[-1] <= C+1e-12
    low=min(low, np.diag(conditional).min());high=max(high,np.diag(conditional).max())
    for i,j in itertools.combinations(range(len(V)),2):
        ratio=max(ratio,abs(conditional[i,j])/(2*C*math.exp(-t2*abs(V[i]-V[j]))))
    count+=1
assert ratio <= 1+1e-12
say(f'CD exhaustive MA(2): {count} conditioning sets; c={c:.8g}, C={C:.8g}, t2={t2:.8g}; max bound ratio={ratio:.8g}; conditional variances=[{low:.8g},{high:.8g}].')

# L3.6 identities and the conditional variance of the omitted predictor.
rng=np.random.default_rng(202611093)
W=rng.multivariate_normal(np.zeros(p),S,size=73)
CW=W-W.mean(axis=0)
maxerr=0.
for bits in range(1<<7):
    T=[i for i in range(7) if bits>>i&1]
    l=8
    A=[i for i in T if abs(i-l)<=3]
    def innovation(indices):
        if not indices:return W[:,l].copy(),np.zeros(W.shape[0])
        fitted=W[:,indices]@np.linalg.solve(S[np.ix_(indices,indices)],S[indices,l])
        return W[:,l]-fitted, fitted
    eA,fA=innovation(A);eT,fT=innovation(T)
    g=eA-eA.mean()
    project=lambda v: CW[:,T]@np.linalg.lstsq(CW[:,T],v,rcond=None)[0] if T else np.zeros_like(v)
    h=g-project(g)
    direct=CW[:,l]-project(CW[:,l])
    D=fT-fA
    rhs=project(eT)+D-D.mean()
    maxerr=max(maxerr,np.max(abs(h-direct)),np.max(abs(project(g)-rhs)))
assert maxerr<1e-12
say(f'L3.6 exact projection identities: 128 T sets, max absolute error {maxerr:.3g}.')

# Visible-null floors: test population Schur complements independently.
rho=.4
E=(1-rho)*np.eye(20)+rho*np.ones((20,20))
maxerr=0.
for u in range(16):
    U=list(range(2,2+u))
    cov=E[0,1]-(E[0,U]@np.linalg.solve(E[np.ix_(U,U)],E[U,1]) if U else 0)
    ref=rho*(1-rho)/(1+(u-1)*rho)
    maxerr=max(maxerr,abs(cov-ref))
assert maxerr<1e-12
b=rng.uniform(-.6,.6,20);psi=1-b*b
F=np.outer(b,b)+np.diag(psi)
for u in range(16):
    U=list(range(2,2+u))
    cov=F[0,1]-(F[0,U]@np.linalg.solve(F[np.ix_(U,U)],F[U,1]) if U else 0)
    ref=b[0]*b[1]/(1+sum(b[U]**2/psi[U]))
    assert abs(cov-ref)<1e-12
say(f'VN Schur formulas: equicorrelation and one-factor, u=0,...,15, max equicorrelation error {maxerr:.3g}.')

# Exact integer branch arithmetic, including both earlier council examples.
for n in [10**e for e in [4,6,10,20,40,60]]:
    g=math.floor(math.log(n)/(2*math.log(2)))
    pp=2*g
    pp2=math.floor(math.log2(n))+math.floor(math.log2(math.log2(n)))
    n0=max(2500,n,pp2)
    h0=(512*n0+2499)//2500
    for q in [pp,pp2]:
        Kcap=min(q,n//2)
        count=sum(math.comb(q,k) for k in range(Kcap+1))
        assert count <= (5*h0+4*n0)*q
    say(f'ENUM n={n}: both prior-review examples covered, p={pp}/{pp2}.')

# Reconstruct numerical totals and the screened/full-scan split.
n2=rows(APP/'numerics/n2_results.csv')
assert len(n2)==96
for field in ['S0_in_mode','ls_S0_scored','ls_certified']:
    assert sum(r[field]=='True' for r in n2)==96
assert sum(r['ls_final_eq_S0']=='True' for r in n2)==94
say('Local-design totals: 96/96 truth included, scored, certified; 94/96 endpoints equal truth.')
n3=rows(APP/'numerics/n3_merged.csv'); fast=rows(APP/'numerics/n3b_results.csv')
key=lambda r: (r['design'],r['n'],r['p'],r['seed'])
fastkeys={key(r) for r in fast}
vn=[r for r in n3 if r['design']!='V3b']; ctrl=[r for r in n3 if r['design']=='V3b']
assert len(n3)==52 and len(vn)==40 and len(ctrl)==12 and len(fastkeys)==16
assert all(r['ls_final_eq_S0']=='True' for r in n3)
assert sum(key(r) not in fastkeys for r in vn)==24
assert all(key(r) not in fastkeys for r in ctrl)
met={}
for r in vn:
    bound=min(int(r['K'])-int(r['s0']), int(r['n_visible'])-15*int(r['s0']))
    k=(r['design'],r['n'],r['p'])
    met.setdefault(k,[0,0]);met[k][0]+=int(int(r['n_extra'])>=bound);met[k][1]+=1
say(f'VN port totals: 40/40 endpoints; 24 complete-scan, 16 screened; 12/12 complete-scan controls. Corrected bound tallies: {met}.')

# Verify all summary rows against saved eigenspectrum / block tables.
summary=rows(APP/'data_diag/summary_table.csv')
for r in summary:
    name=r['name']; eig=rows(APP/f'data_diag/out_{name}_eigs.csv');blocks=rows(APP/f'data_diag/out_{name}_blocks.csv')
    assert len(blocks)==int(r['p'])
    assert len({v['block'] for v in blocks})==int(r['nblocks'])
    assert abs(float(eig[0]['eigenvalue'])/int(r['p'])-float(r['top1']))<1e-10
    assert abs(np.median([float(v['leakage']) for v in blocks])-float(r['leak_med']))<1e-10
say('All 8 diagnostic master rows agree with saved spectrum shares, variable/block counts and median leakages.')
for name in ['digits','diabetes_quad']:
    data=np.genfromtxt(APP/f'data_diag/data/{name}.csv',delimiter=',',skip_header=1)
    X=data[:,:-1];X=X[:,X.std(axis=0)>0]
    R=np.corrcoef(X,rowvar=False)
    ev=np.linalg.eigvalsh(R)
    triples=np.array(list(itertools.combinations(range(X.shape[1]),3)))
    vals=np.linalg.eigvalsh(R[triples[:,:,None],triples[:,None,:]])[:,0]
    r=next(r for r in summary if r['name']==name)
    assert abs(ev[0]-float(r['lam_minR']))<1e-12
    assert abs(vals.min()-float(r['ex_k3']))<1e-12
    say(f'{name} independently reconstructed: n,p={X.shape}; lambda_min={ev[0]:.12g}; exact triple minimum={vals.min():.12g}; {len(triples)} triples.')

copied=APP/'data_diag/core_copy';production=ROOT/'Scripts/SMC_BVS/core'
sources=[q for q in copied.rglob('*') if q.is_file() and q.suffix in ['.R','.h','.cpp']]
for q in sources:
    assert q.read_bytes()==(production/q.relative_to(copied)).read_bytes(),str(q)
say(f'All {len(sources)} copied .R/.h/.cpp production sources match byte-for-byte.')
say('ALL INDEPENDENT CHECKS PASSED.')
(SCRATCH/'checks_out.txt').write_text('\n'.join(log)+'\n',encoding='utf-8')
