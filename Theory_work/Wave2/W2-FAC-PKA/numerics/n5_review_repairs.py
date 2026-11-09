"""Reproduce R02 evidence with provenance. <=20 seeds; writes only numerics.
Reference DP copied verbatim from reviews/R02_scratch/start_dp.py, imported only.
"""
from n1_exact_grid import *
import r02_start_dp_reference as ref
import fac_core as fc
from types import SimpleNamespace

def controls():
    rows=[]
    for n,p,rho in ((24,20,.3),(40,39,.7)):
        for seed in range(4):
            rng=np.random.default_rng(seed+1000)
            theta=np.zeros(p);theta[:2]=[.05,-.04] if seed%2 else [1,.8]
            P=cs.CS(rho,theta,n,rng=rng)
            D=SimpleNamespace(n=n,p=p,K=P.K,XtX=(n-1)*((1-rho)*np.eye(p)+rho*np.ones((p,p))),
                Xty=P.z,yty=n-1,nu=P.nu,logw=P.lw,logm0=-P.nu*math.log(.02+n-1),cache={})
            for k in (0,P.K-1,P.K):
                start=tuple(sorted(rng.choice(p,k,replace=False).tolist()))
                a=run_path(P,start);b=fc.ls0_path(D,start,P.S0)
                assert a['final']==b['final'] and len(a['moves'])==b['moves']
                T=set(start)
                for move,step in zip(a['moves'],b['steps']):
                    if move[1] is not None:T.remove(move[1])
                    if move[2] is not None:T.add(move[2])
                    assert abs(P.F(tuple(sorted(T)))-step['best'])<1e-7
                rows.append(dict(n=n,p=p,rho=rho,seed=seed,start=k,K=P.K,moves=b['moves'],final=list(b['final']),matched=True))
    (HERE/'N5_adapter_controls.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    print('adapter_controls',len(rows),'all matched',flush=True)

def saturation():
    rows=[]
    grid=[(800,680,'aligned'),(20000,17000,'aligned'),(20000,10200,'aligned'),
          (20000,19999,'single'),(20000,17000,'mixed')]
    for n,p,kind in grid:
        for seed in range(2):
            theta=np.zeros(p)
            if kind=='single':theta[0]=2
            else:theta[[2,26,53,75]]=.5*np.array([1.4,1 if kind=='aligned' else -1,1.8,1.2 if kind=='aligned' else -1.2])
            blocks=[list(range(j,min(j+16,p))) for j in range(0,p,16)]
            z=ref.data(.5,theta,n,np.random.default_rng(seed));K=n//2
            k,gap=ref.start_size(z,blocks,n,.5,K,p)
            if n==800:
                P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
                assert np.max(abs(P.z-z))<1e-7
                assert k==len(bc.start_mode(TableAdapter(P),blocks,tie_tol=0).mode)
            # Population null-block increment prediction at most adverse u=15.
            v=float(.5*(theta@theta)+.5*theta.sum()**2+1)
            u=15;cov=.5*theta.sum();R_u=v-cov**2*u/(1+(u-1)*.5)
            partial=cov*.5/(1+(u-1)*.5);condvar=1-.25*u/(1+(u-1)*.5)
            delta=partial**2/condvar
            pred=.5*n*math.log(R_u/(R_u-delta))-.5*math.log(n)
            row=dict(n=n,p=p,K=K,seed=seed,design=kind,theta_bar=float(theta.sum()),
                partition='contiguous blocks of 16, final remainder',last_block=blocks[-1],
                block_count=len(blocks),start=k,saturated=k==K,margin_K_over_best_smaller=gap,
                population_increment_prediction=pred,prediction_minus_worst_prior=pred-math.log(2*p),
                prediction_plus_prior_near_K=pred+math.log(K/(2*p-K)))
            rows.append(row)
            (HERE/'N5_saturation.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
            print(json.dumps(row),flush=True)

if __name__=='__main__':
    controls();saturation()
