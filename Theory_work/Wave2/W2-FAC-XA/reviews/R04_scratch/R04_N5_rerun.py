"""Local falsification only; <=20 fixed seeds; standard library, no score work."""
import json, math, random
from pathlib import Path

OUT = Path(__file__).parent

def metric(v, mask):
    deleted = [v[i] for i in range(len(v)) if not (mask >> i) & 1]
    kept = [v[i] for i in range(len(v)) if (mask >> i) & 1]
    if not deleted or not kept:
        return 0.0
    a, b = min(deleted), max(deleted)
    return max([0.0] + [min(z-a, b-z) for z in kept if a < z < b])

def exhaustive(v, eps, c=1.5, B=0.0, squared=False):
    p = len(v)
    full = (1 << p)-1
    states = {full: []}
    best = {'depth': 0.0, 'path': [], 'kept': [], 'values': v, 'eps': eps, 'c': c, 'B': B}
    for m in range(p, 0, -1):
        nxt = {}
        for mask, path in states.items():
            ids = [i for i in range(p) if (mask >> i) & 1]
            x = (B + sum(v[i] for i in ids))/(m+c)
            ds = {i: (v[i]-x)**2 if squared else abs(v[i]-x) for i in ids}
            d = min(ds.values())
            for i in ids:
                if ds[i] <= d + eps + 1e-12:
                    new = mask ^ (1 << i)
                    if new not in nxt:
                        nxt[new] = path+[i]
                    depth = metric(v, new)
                    if depth > best['depth']:
                        best.update(depth=depth, path=path+[i], kept=[j for j in range(p) if (new >> j)&1])
        states = nxt
    return best

def sampled(v, eps, rng, policy, c=1.5, B=0.0):
    p = len(v)
    ids = list(range(p)); deleted = []; best = 0.0; maxgap = 0.0
    for m in range(p, 0, -1):
        x = (B+sum(v[i] for i in ids))/(m+c)
        d = min(abs(v[i]-x) for i in ids)
        allowed = [i for i in ids if abs(v[i]-x) <= d+eps+1e-12]
        if policy == 'random':
            j = rng.choice(allowed)
        elif policy == 'outer':
            j = max(allowed, key=lambda i: abs(v[i]-x))
        elif policy == 'hull':
            def objective(i):
                a,b = min(deleted+[v[i]]), max(deleted+[v[i]])
                return max([0.0]+[min(v[k]-a,b-v[k]) for k in ids if k != i and a < v[k] < b])
            j = max(allowed, key=objective)
        else:
            j = max(allowed, key=lambda i: v[i] if m > p//2 else -v[i])
        ids.remove(j); deleted.append(v[j])
        if ids:
            a,b = min(deleted),max(deleted)
            best=max(best,max([0.0]+[min(v[k]-a,b-v[k]) for k in ids if a<v[k]<b]))
            xx=(B+sum(v[i] for i in ids))/(m-1+c)
            dd=min(abs(v[i]-xx) for i in ids)
            maxgap=max(maxgap,max(abs(z-xx) for z in deleted)-dd)
    return {'depth':best,'ratio':best/eps,'max_deleted_gap':maxgap}

def main():
    deterministic=[]
    for v in [[-4,-3,-2,-1,0,1,2,3,4],[-2,-.1,0,.1,2],[-3,-.4,-.3,-.2,0,.2,.3,.4,3],[-1,-.01,0,.01,1]]:
        for eps in [.01,.1,.5,1.0]:
            deterministic.append(exhaustive(v,eps))
    gaussian=[]; small=[]
    for seed in range(20):
        rng=random.Random(seed)
        v=sorted(rng.gauss(0,1) for _ in range(10))
        for eps in [.05,.2,.5]:
            small.append(dict(seed=seed,**exhaustive(v,eps)))
        v=sorted(rng.gauss(0,1) for _ in range(512))
        for eps in [.001,.01,.1]:
            for policy in ['random','outer','hull','switch']:
                r=sampled(v,eps,rng,policy)
                gaussian.append(dict(seed=seed,p=512,eps=eps,policy=policy,**r))
    result={'status':'UNCHECKED pending Claude; falsification only', 'seed_count':20,
            'deterministic':deterministic,'small_gaussian_exhaustive':small,'gaussian_paths':gaussian}
    (OUT/'R04_N5_rerun_results.json').write_text(json.dumps(result,indent=2))
    worst=max(small,key=lambda r:r['depth']/r['eps'])
    ids=list(range(len(worst['values']))); trace=[]
    for j in worst['path']:
        x=sum(worst['values'][i] for i in ids)/(len(ids)+worst['c'])
        d=min(abs(worst['values'][i]-x) for i in ids)
        trace.append(dict(j=j,x=x,d=d,selected_distance=abs(worst['values'][j]-x),
                          excess=abs(worst['values'][j]-x)-d))
        ids.remove(j)
    (OUT/'R04_N5_rerun_trace.json').write_text(json.dumps(trace,indent=2))
    print(json.dumps({'deterministic_max_ratio':max(r['depth']/r['eps'] for r in deterministic),
                      'small_gaussian_max_ratio':max(r['depth']/r['eps'] for r in small),
                      'sampled_max_ratio':max(r['ratio'] for r in gaussian),
                      'worst_small':max(small,key=lambda r:r['depth']/r['eps'])},indent=2))

if __name__ == '__main__': main()
