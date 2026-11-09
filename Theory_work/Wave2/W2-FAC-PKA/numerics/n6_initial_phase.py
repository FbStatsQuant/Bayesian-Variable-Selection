"""Initial swap phase controls for L3; retain finite-onset failures explicitly."""
from n3_singletons import *
phase_source=replace_once(source,'def run_path(', 'def initial_path(')
phase_source=replace_once(phase_source,'moves.append((tag, jo, li))','moves.append((tag, jo, li))\n        if typ != "s": break')
ns=dict(cs.__dict__);exec(phase_source,ns);initial_path=ns['initial_path']
rows=[]
for n in (800,2000,4000):
    for ratio in (.6,.85,.98):
        for s0 in (1,2):
            p=int(n*ratio);theta=np.zeros(p);theta[:s0]=1
            P=cs.CS(.5,theta,n,rng=np.random.default_rng(0))
            S=singleton_start(P);path=initial_path(P,S)
            swaps=[];first_other=None
            for m in path['moves']:
                if not m[0].startswith('s'):first_other=m[0];break
                swaps.append(m)
            imports=[li for _,_,li in swaps];exports=[jo for _,jo,_ in swaps]
            seen=set();reexport=False
            for _,jo,li in swaps:
                reexport|=jo in seen;seen.add(li)
            a=(1-ratio)/20;eta0=(1-ratio)/80
            pool={j for j in range(s0,p) if abs(P.xi[j])>=math.sqrt(a*math.log(n))}
            row=dict(n=n,p=p,ratio=ratio,s0=s0,seed=0,W=len(swaps),W_over_n=len(swaps)/n,
                first_other=first_other,terminal_if_no_other=first_other is None,
                distinct_imports=len(set(imports)),reexported_import=reexport,
                max_export_abs_xi=max((abs(P.xi[j]) for j in exports),default=0),
                min_import_abs_xi=min((abs(P.xi[j]) for j in imports),default=None),
                exceptional_pool=len(pool),all_imports_exceptional=set(imports)<=pool,
                H=math.ceil(n**(1-eta0)),pool_below_H_half=len(pool)<=math.ceil(n**(1-eta0))/2)
            rows.append(row)
(HERE/'N6_initial_phase.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
