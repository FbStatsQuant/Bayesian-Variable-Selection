"""R04: when does shadow band E_t grow vs actual one-sided width (p=800, policy right/left)."""
import random, json
from R04_l3_adversary import onesided_width
def go(seed,p,eps,c,pol):
    rng=random.Random(seed); v=[rng.gauss(0,1) for _ in range(p)]
    ids=set(range(p)); h=(sum(v))/(p+c); E=0; rows=[]
    for t in range(p):
        m=len(ids); q=m+c; x=sum(v[i] for i in ids)/q
        d=min(abs(v[i]-x) for i in ids); al=[i for i in ids if abs(v[i]-x)<=d+eps]
        j=max(al,key=lambda i:v[i]) if pol=='right' else min(al,key=lambda i:v[i])
        others=[i for i in ids if i!=j]
        do=min(abs(v[i]-h) for i in others) if others else float('inf')
        rad=min(abs(v[j]-h),do); vv=h+(rad if v[j]>=h else -rad)
        E=max(E,abs(vv-v[j])); h=h-(vv-h)/(q-1); ids.discard(j)
        mm=len(ids)
        if mm in (700,400,200,100,50,20,10,5,2,1):
            rows.append(dict(m=mm,E_over_eps=round(E/eps,2),actual_w_over_eps=round(onesided_width(v,ids)/eps,3),
                             bound_over_eps=round(1+2*(p-mm-1)/(mm+1+c),1),h_minus_x_over_eps=round((h-sum(v[i] for i in ids)/(mm+c))/eps,2)))
    return rows
out={pol:go(7,800,0.1,1.05,pol) for pol in ['right','left']}
json.dump(out,open('R04_l3_shadow_growth_out.json','w'),indent=1)
for k,r in out.items():
    print(k); [print(x) for x in r]
