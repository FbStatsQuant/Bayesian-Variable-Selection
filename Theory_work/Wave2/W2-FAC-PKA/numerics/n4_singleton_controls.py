"""Exact small start control and early-swap falsification, <=20 seeds."""
from n3_singletons import *
import itertools

out={'enumeration':[],'early':[]}
for s0 in (1,2):
    for seed in range(3):
        n,p=14,10;theta=np.zeros(p);theta[:s0]=1
        P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
        lm=P.F_stats(1,P.z**2,P.z)-P.lw[1]-(P.F(())-P.lw[0])
        sets=[S for k in range(P.K+1) for S in itertools.combinations(range(p),k)]
        vals=[float(P.lw[len(S)]+sum(lm[list(S)])) for S in sets]
        best=min(((-v,len(S),S) for S,v in zip(sets,vals)))[2]
        assert best==singleton_start(P)
        out['enumeration'].append(dict(s0=s0,seed=seed,models=len(sets),matched=True))
for n in (800,2000,4000):
    for ratio in (.6,.85,.98):
        for s0 in (1,2):
            seed=0;p=int(ratio*n);theta=np.zeros(p);theta[:s0]=1
            P=cs.CS(.5,theta,n,rng=np.random.default_rng(seed))
            S=singleton_start(P);T=set(S)
            L=bc.ell_cap(n,p)+s0+2
            result=run_path(P,S,max_moves=L)
            initial=next((i for i,m in enumerate(result['moves']) if m[0]!='sN'),len(result['moves']))
            margins=[];centres=[];multipliers=[]
            for tag,jo,li in result['moves']:
                idx=np.array(sorted(T));outside=np.array(sorted(set(range(p))-T));z=P.z
                k=len(T);A=float(z[idx]@z[idx]);B=float(z[idx].sum());gam=P.be/(P.al+k*P.be)
                ft=P.F(tuple(idx));Fd=P.F_stats(k-1,A-z[idx]**2,B-z[idx])
                ext=outside[[int(np.argmin(z[outside])),int(np.argmax(z[outside]))]]
                Fs=P.F_stats(k,(A-z[idx]**2)[:,None]+z[ext][None,:]**2,(B-z[idx])[:,None]+z[ext][None,:])
                margins.append(float(Fs.max()-Fd.max()))
                b=((n-1)*.5*s0+math.sqrt((n-1)*.5)*P.eta)/P.s
                d=math.sqrt((n-1)*.5)/P.s
                centres.append(float((gam*B-b)/d))
                Q=n-1-n*(A-gam*B*B)/P.al
                multipliers.append(float(P.nu*n*d*d/(P.al*(.02+Q))))
                if jo is not None:T.remove(jo)
                if li is not None:T.add(li)
            out['early'].append(dict(n=n,p=p,s0=s0,seed=seed,start=len(S),truth_in_start=set(P.S0)<=set(S),
                top_nulls_match=set(S)-set(P.S0)==set(np.arange(s0,p)[np.argsort(P.xi[s0:])[-(P.K-s0):]]),
                L=L,initial_null_swaps_observed=initial,all_first_L_null_swaps=initial==L,
                min_swap_minus_deletion=min(margins),min_multiplier=min(multipliers),
                initial_centre=centres[0],max_centre_drift=max(abs(x-centres[0]) for x in centres)))
(HERE/'N4_singleton_controls.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
