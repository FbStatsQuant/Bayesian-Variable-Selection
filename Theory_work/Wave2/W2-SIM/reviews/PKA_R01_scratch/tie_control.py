import sys,os
sys.dont_write_bytecode=True
sys.path.insert(0,'Theory_work/Wave2/W2-SIM/PKA/scripts')
from pka_lib import *
for eps in [1e-15,3e-15,1e-14,3e-14,1e-13,3e-13,1e-12]:
 P=cs.CS(.5,np.r_[1.,np.zeros(39)],60,rng=np.random.default_rng(1))
 P.z[:]=18.;P.z[:30]=5.;P.z[0]=25.;P.z[39]-=eps;P.z[38]+=eps
 st=tuple(range(30));r=run_path(P,st,max_moves=1)
 A=float(P.z[:30]@P.z[:30]);B=float(P.z[:30].sum())
 full=P.F_stats(30,(A-P.z[:30]**2)[:,None]+P.z[None,30:]**2,(B-P.z[:30])[:,None]+P.z[None,30:])
 ii,jj=np.nonzero(full==full.max());pairs=[(int(i),int(j+30)) for i,j in zip(ii,jj)]
 pairs.sort(key=lambda ab:tuple(sorted((set(st)-{ab[0]})|{ab[1]})))
 print(eps,'source',r['moves'][0], 'full',pairs[0], 'ties',len(pairs),'Qall',59-60*(P.z@P.z-P.be/(P.al+40*P.be)*P.z.sum()**2)/P.al)


