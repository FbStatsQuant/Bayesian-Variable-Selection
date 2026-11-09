import os,sys,json
from pathlib import Path
sys.dont_write_bytecode=True
root=Path.cwd(); sys.path.insert(0,str(root/'Theory_work/Wave2/W2-SIM/PKA/scripts'))
from pka_lib import *
base=root/'Theory_work/Wave2/W2-SIM/results/FAC-PKA/pilot_local'
rows=[json.loads(l) for f in base.glob('*.jsonl') for l in f.read_text().splitlines()]
print('pilot',len(rows),'unique seeds',len(set(r['seed'] for r in rows)),'ties',sum(r['ties'] for r in rows))
# Extend the imported function with observational diagnostics only; never modify sources.
src=n1.source
hook='''
        if len(opts)>1:
            print('TIE',len(moves),'k',k,'opts',opts,'best',best,flush=True)
            full=P.F_stats(k,(A-zin**2)[:,None]+zout[None,:]**2,(B-zin)[:,None]+zout[None,:])
            fullopts=[('s',int(idx_in[i]),int(idx_out[j])) for i,j in zip(*np.nonzero(full==best))]
            allopts=[o for o in opts if o[0]!='s']+fullopts
            allopts.sort(key=_res)
            print('FULL',float(full.max())-best,'count',len(allopts),'winner',allopts[0] if allopts else None,'sourcewinner',sorted(opts,key=_res)[0],flush=True)
'''
src=src.replace('        opts.sort(key=_res)',hook+'        opts.sort(key=_res)')
ns=dict(cs.__dict__);exec(src,ns)
r=next(r for r in rows if r['prio']=='P1' and r['n']==3200 and r['c']==.98 and r['rep']==0)
th=np.zeros(r['p']);th[[2,26,53,75]]=.5*np.array([1.4,1,1.8,1.2]);P=cs.CS(r['rho'],th,r['n'],rng=np.random.default_rng(r['seed']))
st=fast_start_mode(P,fast_partition_cs(P.p,16))['mode'];res=ns['run_path'](P,st)
print('reproduced',len(res['moves']),res['info']['ties'],res['final'])
# All planned numerical cells, independent of task writer side effects.
seeds=[]
for n in [800,1600,3200,6400,12800,25600,51200]:
 for c in [.6,.85,.98]:
  for rho in ([.5] if n==51200 else [.2,.5,.8]):
   for rep in range(20 if rho!=.5 or n==51200 else 100):seeds.append(seed_for(1,n,round(c*100),round(rho*10),rep))
for n in [1000,3162,10000,31623,100000,316228,1000000]:
 for c in [.6,.85,.98]:
  for v in [1,2]:
   for rep in range(20):seeds.append(seed_for(2,v,n,round(c*100),rep))
print('planned seeds',len(seeds),'unique',len(set(seeds)))
