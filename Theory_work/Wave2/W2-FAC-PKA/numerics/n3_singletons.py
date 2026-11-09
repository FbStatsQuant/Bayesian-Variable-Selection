"""Nonproduction singleton-partition falsification diagnostic, <=20 seeds."""
from n1_exact_grid import *

def singleton_start(P):
    lm=P.F_stats(1,P.z**2,P.z)-P.lw[1]
    order=np.lexsort((np.arange(P.p),-lm))
    base=P.F(())-P.lw[0]
    vals=P.lw+np.r_[0,np.cumsum((lm-base)[order[:P.K]])]
    k=int(np.argmax(vals))
    return tuple(sorted(int(j) for j in order[:k]))

if __name__=='__main__':
    with (HERE/'N3_singletons.jsonl').open('w',encoding='utf8') as f:
        for n in (200,800,2000):
            for ratio in (.6,.85,.98):
                p=int(ratio*n)
                for seed in range(2):
                    theta=np.zeros(p);theta[0]=1
                    P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
                    S=singleton_start(P)
                    result=run_path(P,S)
                    moves=result['moves']; cap=bc.ell_cap(n,p)+len(S)
                    initial=next((i for i,m in enumerate(moves) if m[0]!='sN'),len(moves))
                    T=set(S); first=None
                    for t in range(len(moves)+1):
                        missing=set(P.S0)-T;extra=T-set(P.S0)
                        if len(missing)+len(extra)<=1 or len(missing)==len(extra)==1:
                            first=t;break
                        _,jo,li=moves[t] if t<len(moves) else ('',None,None)
                        if jo is not None:T.remove(jo)
                        if li is not None:T.add(li)
                    row=dict(n=n,p=p,seed=seed,start=len(S),truth_in_start=0 in S,
                        retained_null_mean=float(P.xi[[j for j in S if j!=0]].mean()),
                        initial_swaps=initial,swaps=sum(m[0]=='sN' for m in moves),
                        additions=sum(m[0].startswith('+') for m in moves),moves=len(moves),
                        cap=cap,first_scoring_scan=first,merged_scores=first is not None and first<=cap,
                        doubled_scores=first is not None and first<=bc.ell_cap(n,p)+2*len(S),final_is_truth=result['final_is_S0'])
                    f.write(json.dumps(row)+'\n');f.flush();print(json.dumps(row),flush=True)
