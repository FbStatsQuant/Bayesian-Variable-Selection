import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,'Theory_work/Wave2/W2-SIM/PKA/scripts')
from pka_lib import *
checks=[]
for p in [31,60,79]:
 for rho in [.2,.5,.8]:
  b=fast_partition_cs(p,bc.block_size(200,p)); assert b==bc.partition_from_corr((1-rho)*np.eye(p)+rho*np.ones((p,p)),bc.block_size(200,p))
  checks.append(['partition',p,rho,True])
for n,c in [(200,.6),(400,.98)]:
 p=int(n*c);th=np.zeros(p);th[[2,26,53,75]]=[.7,.5,.9,.6]
 P=cs.CS(.5,th,n,rng=np.random.default_rng(seed_for(99,123,n)))
 b=fast_partition_cs(p,bc.block_size(n,p)); a=fast_start_mode(P,b);r=bc.start_mode(TableAdapter(P),b,tie_tol=0)
 assert a['mode']==r.mode and a['size']==r.size and a['log_gamma0_mode']==r.log_gamma0_mode
 checks.append(['start',n,c,True])
print(json.dumps(checks))

