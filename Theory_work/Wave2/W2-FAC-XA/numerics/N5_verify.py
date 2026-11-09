"""Exact rational witness and shadow-certificate checks; no new random seeds."""
from fractions import Fraction as F
from pathlib import Path
import json

root=Path(__file__).parent
r=json.loads((root/'N5_fuzzy_results.json').read_text())
values=[F(v) for v in ['-1.78','-.78','-.53','-.09','-.05','.28','.43','.57','.67','1.52']]
ids=list(range(10)); path=[2,3,8,7,5,6,1]; exact=[]
for j in path:
    x=sum(values[i] for i in ids)/(len(ids)+F(3,2))
    d=min(abs(values[i]-x) for i in ids)
    excess=abs(values[j]-x)-d
    assert excess < F(1,2)
    exact.append({'index':j,'center':str(x),'excess':str(excess),'excess_float':float(excess)})
    ids.remove(j)

count=0; max_bound_ratio=0.0
for case in r['deterministic']+r['small_gaussian_exhaustive']:
    v=case['values']; eps=case['eps']; c=case['c']; B=case['B']
    ids=list(range(len(v))); h=(B+sum(v))/(len(v)+c); replacements=[]
    for t,j in enumerate(case['path']):
        q=len(ids)+c
        x=(B+sum(v[i] for i in ids))/q
        assert abs(h-x)<=t*eps/q+1e-9
        others=[i for i in ids if i!=j]
        d=min(abs(v[i]-h) for i in others) if others else float('inf')
        radius=min(abs(v[j]-h),d)
        vv=h+(radius if v[j]>=h else -radius)
        delta=vv-v[j]
        assert abs(delta)<=eps+2*abs(h-x)+1e-9
        h=h-(vv-h)/(q-1)
        replacements.append(vv); ids.remove(j)
        if ids:
            lo=max([v[i] for i in ids if v[i]<=h],default=-float('inf'))
            hi=min([v[i] for i in ids if v[i]>=h],default=float('inf'))
            assert all(lo-1e-9<=z<=hi+1e-9 for z in replacements)
            E=max(abs(replacements[k]-v[case['path'][k]]) for k in range(t+1))
            bound=eps*(1+2*t/(len(ids)+1+c))
            assert E<=bound+1e-9
            max_bound_ratio=max(max_bound_ratio,E/bound)
        count+=1

out={'status':'UNCHECKED pending Claude','rational_trace':exact,
     'shadow_steps_checked':count,'max_actual_replacement_over_bound':max_bound_ratio,
     'note':'Checks witness paths stored by exhaustive subset search, not all shadow histories.'}
(root/'N5_verify_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
