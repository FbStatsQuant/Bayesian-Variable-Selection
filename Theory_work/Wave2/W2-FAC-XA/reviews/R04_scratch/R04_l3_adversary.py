"""R04: adversarial eps-fuzzy deletion paths. Check shadow claims (2),(3), identity q_t e_t=-sum delta,
certificate, bound (1); measure minimal one-sided two-tail width of the ACTUAL retained set."""
import random, math, json, bisect
def onesided_width(vals, kept):
    ks=sorted(vals[i] for i in kept); kset=set(kept)
    ds=sorted(vals[i] for i in range(len(vals)) if i not in kset)
    if not ds: return 0.0
    best=float('inf'); lo=-float('inf')
    for hi in ks+[float('inf')]:
        w=0.0
        if lo>-float('inf') and ds[0]<lo: w=max(w,lo-ds[0])
        if hi<float('inf') and ds[-1]>hi: w=max(w,ds[-1]-hi)
        best=min(best,w); lo=hi
    return best
def run(v,eps,c,B,policy,rng,check=True):
    p=len(v); ids=set(range(p)); h=(B+sum(v))/(p+c); S=0.0; E=0.0
    worst_ratio=0.0; worst_w_over_eps=0.0; trace=[]
    for t in range(p):
        m=len(ids); q=m+c; x=(B+sum(v[i] for i in ids))/q
        d=min(abs(v[i]-x) for i in ids)
        allowed=[i for i in ids if abs(v[i]-x)<=d+eps]
        if policy=='random': j=rng.choice(allowed)
        elif policy=='right': j=max(allowed,key=lambda i:v[i])
        elif policy=='left': j=min(allowed,key=lambda i:v[i])
        elif policy=='far': j=max(allowed,key=lambda i:abs(v[i]-x))
        elif policy=='shadowpush':  # maximize |delta| in the direction that increases |e|
            e=h-x
            j=max(allowed,key=lambda i:(v[i]-x)*(1 if e>=0 else -1)+abs(v[i]-x))
        elif policy=='greedyw':
            j=max(allowed,key=lambda i:onesided_width(v,ids-{i}) if m>1 else 0)
        e=h-x
        assert abs(q*e+S)<=1e-7*(1+abs(S)), (q*e,S)   # exact identity q e = -sum delta
        assert abs(e)<=t*eps/q+1e-9
        others=[i for i in ids if i!=j]
        dother=min(abs(v[i]-h) for i in others) if others else float('inf')
        rad=min(abs(v[j]-h),dother); vv=h+(rad if v[j]>=h else -rad); delta=vv-v[j]
        assert abs(delta)<=eps+2*abs(e)+1e-9
        if (e>=0 and delta<0) or (e<0 and delta>0): assert abs(delta)<=eps+1e-9
        if check and others:
            lo=max([v[i] for i in others if v[i]<=h],default=-float('inf'))
            hi=min([v[i] for i in others if v[i]>=h],default=float('inf'))
            assert lo-1e-9<=vv<=hi+1e-9
        h=h-(vv-h)/(q-1); S+=delta; E=max(E,abs(delta)); ids.discard(j)
        if ids:
            mm=len(ids)
            if check:
                lo=max([v[i] for i in ids if v[i]<=h],default=-float('inf'))
                hi=min([v[i] for i in ids if v[i]>=h],default=float('inf'))
                # all deleted originals within E of [lo,hi]
                for i in set(range(p))-ids:
                    assert v[i]>=lo-E-1e-9 and v[i]<=hi+E+1e-9
            bound=eps*(1+2*(p-mm-1)/(mm+1+c)); assert E<=bound+1e-9
            worst_ratio=max(worst_ratio,E/bound)
            if mm%max(1,p//20)==0 or mm<=10:
                w=onesided_width(v,ids); worst_w_over_eps=max(worst_w_over_eps,w/eps)
                trace.append((mm,w/eps,E/eps))
    return dict(maxE_over_bound=worst_ratio,max_actual_width_over_eps=worst_w_over_eps,
                final_E_over_eps=E/eps,trace=trace[-12:])
res=[]
for seed in range(6):
    for p in [50,200,800]:
        rng=random.Random(1000*seed+p); v=[rng.gauss(0,1) for _ in range(p)]
        for eps in [0.01,0.1]:
            for c in [1.05,1.5,4.0]:
                for pol in ['random','right','left','far','shadowpush']+(['greedyw'] if p<=200 else []):
                    r=run(v,eps,c,0.0,pol,rng,check=(p<=200))
                    r.update(seed=seed,p=p,eps=eps,c=c,policy=pol); del r['trace']; res.append(r)
summary={}
for p in [50,200,800]:
    rows=[r for r in res if r['p']==p]
    summary[p]=dict(max_actual_width_over_eps=max(r['max_actual_width_over_eps'] for r in rows),
                    max_shadowE_over_eps=max(r['final_E_over_eps'] for r in rows),
                    max_E_over_bound=max(r['maxE_over_bound'] for r in rows),
                    worst=max(rows,key=lambda r:r['max_actual_width_over_eps']))
json.dump(dict(summary=summary,rows=res),open('R04_l3_adversary_out.json','w'),indent=1)
print(json.dumps(summary,indent=1))
