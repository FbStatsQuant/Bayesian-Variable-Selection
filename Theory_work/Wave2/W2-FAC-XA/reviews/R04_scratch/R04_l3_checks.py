"""R04 independent checks of L3 (deterministic). Fractions for witnesses; floats for adversarial sweeps."""
from fractions import Fraction as F
import random, math, json, sys
out={}
# 1. rational witness
v=[F(s) for s in ['-1.78','-.78','-.53','-.09','-.05','.28','.43','.57','.67','1.52']]
c=F(3,2); B=F(0); eps=F(1,2)
ids=list(range(10)); path=[2,3,8,7,5,6,1]; exc=[]
for j in path:
    x=(B+sum(v[i] for i in ids))/(len(ids)+c)
    d=min(abs(v[i]-x) for i in ids); exc.append(abs(v[j]-x)-d); ids.remove(j)
out['witness_excess']=[str(e) for e in exc]; out['witness_all_lt_eps']=all(e<eps for e in exc)
kept=ids; dele=[v[j] for j in path]
a,b=min(dele),max(dele)
out['kept']=[str(v[i]) for i in kept]
out['hull_depth']=str(max(min(v[k]-a,b-v[k]) for k in kept if a<v[k]<b))
def onesided_width(vals,keptset):
    ks=sorted(vals[i] for i in keptset); ds=[vals[i] for i in range(len(vals)) if i not in keptset]
    gaps=[(None,ks[0])]+[(ks[i],ks[i+1]) for i in range(len(ks)-1)]+[(ks[-1],None)]
    best=None
    for lo,hi in gaps:
        w=0
        for z in ds:
            if lo is not None and z<lo: w=max(w,lo-z)
            if hi is not None and z>hi: w=max(w,z-hi)
        best=w if best is None else min(best,w)
    return best
out['witness_min_onesided_width']=str(onesided_width(v,set(kept)))
# 2. crossing example
c2=F(3,2); m=2; z=F(-1,2); y=F(3,2); B2=F(-1); q=m+c2
x=(B2+z+y)/q; x2=x-(y-x)/(q-1)
out['crossing']=dict(x=str(x),x_next=str(x2),excess=str(abs(y-x)-min(abs(y-x),abs(z-x))),bound_u=str(1/(q-2)),u=str(abs(x-z)))
# extremal version: u=eps/(q-2)
u=F(1)/(q-2); x=F(0); zz=-u; yy=u+1; Bx=x*q-zz-yy; x2=x-(yy-x)/(q-1)
out['crossing_extremal']=dict(B=str(Bx),x_next=str(x2),z=str(zz),disp=str(abs(x2-x)),bound=str(1/(q-2)))
print(json.dumps(out,indent=1))
