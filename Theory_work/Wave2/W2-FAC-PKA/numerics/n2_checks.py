"""Falsification checks, not proofs; <=20 seeds. No outside writes."""
from n1_exact_grid import *
import fac_core as fc
from types import SimpleNamespace

out = {}
# Realizability at rank boundary, plus impossible target minimum eigenvalue.
n,p,rho=16,15,.5
C=np.eye(n)-np.ones((n,n))/n
Q=np.linalg.qr(C[:,:p])[0]
Sigma=(1-rho)*np.eye(p)+rho*np.ones((p,p))
X=math.sqrt(n-1)*Q@np.linalg.cholesky(Sigma).T
out['rank']=dict(n=n,p=p,center_error=float(abs(X.sum(0)).max()),
    gram_error=float(abs(X.T@X-(n-1)*Sigma).max()),
    impossible_p16_target_rank=16,centered_rank_bound=15)
assert out['rank']['center_error']<1e-10 and out['rank']['gram_error']<1e-10
# Adapted path and tables versus dense scorer; same sufficient statistics.
tests=[]
for seed in range(5):
    n,p=30,22
    theta=np.zeros(p); theta[[0,7]]=[1,.6]
    P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
    D=SimpleNamespace(n=n,p=p,K=P.K,XtX=(n-1)*(.5*np.eye(p)+.5*np.ones((p,p))),
        Xty=P.z,yty=n-1,nu=P.nu,logw=P.lw,logm0=-P.nu*math.log(.02+n-1),cache={})
    D.logm_idx=lambda idx: bc.Problem.logm_idx(D,idx)
    D.logm_many=lambda sets: bc.Problem.logm_many(D,sets)
    blocks=[list(range(j,min(j+4,p))) for j in range(0,p,4)]
    start=bc.start_mode(TableAdapter(P),blocks,tie_tol=0).mode
    dense_start=bc.start_mode(D,blocks,tie_tol=0).mode
    path=run_path(P,start); dense=fc.ls0_path(D,start,P.S0)
    assert start==dense_start and path['final']==dense['final'] and len(path['moves'])==dense['moves']
    T=set(start)
    for move,step in zip(path['moves'],dense['steps']):
        if move[1] is not None:T.remove(move[1])
        if move[2] is not None:T.add(move[2])
        assert abs(P.F(tuple(sorted(T)))-step['best'])<1e-7
    tests.append(dict(seed=seed,start=len(start),moves=len(path['moves']),matched=True))
out['dense_controls']=tests
# Uniform-increment falsification samples over pure-null subsets, including p=n-1.
rows=[]
for n in (200,2000,20000):
    for p in (int(.51*n),int(.85*n),n-1):
        for seed in range(2):
            theta=np.zeros(p);theta[0]=2
            P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
            rng=np.random.default_rng(seed+100)
            vals=[]
            for u in range(16):
                for rep in range(20):
                    picks=rng.choice(np.arange(1,p),u+1,replace=False)
                    U=tuple(sorted(picks[:-1]));V=tuple(sorted(picks))
                    lm=P.F(V)-P.lw[u+1]-(P.F(U)-P.lw[u])
                    vals.append(float(lm-math.log(2*p)))
            rows.append(dict(n=n,p=p,seed=seed,min_block_increment_minus_worst_prior=min(vals)))
out['increment_samples']=rows
(HERE/'N2_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
