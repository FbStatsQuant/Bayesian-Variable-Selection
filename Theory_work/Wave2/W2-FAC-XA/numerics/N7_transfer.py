"""RN factorization and OT ordering falsification, ten seeds, local matrices."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import numpy as np,json,math
from pathlib import Path
from scipy.special import gammaln
def sym(S,f):
 w,v=np.linalg.eigh(S);return (v*f(w))@v.T
rows=[]
for seed in range(10):
 rng=np.random.default_rng(seed)
 for n,p in [(512,8),(2048,16)]:
  lam=np.linspace(.4,.85,p);Sig=np.diag(1-lam**2)+np.outer(lam,lam)
  A=sym(Sig,np.sqrt);Ai=np.linalg.inv(A);raw=rng.normal(size=(n,p))@A
  raw-=raw.mean(0);S=raw.T@raw/(n-1);Ds=np.diag(1/np.sqrt(np.diag(S)))
  X=raw@Ds;R=X.T@X/(n-1);E0=Ai@S@Ai-np.eye(p);F=Ai@(Ds-np.eye(p))@A
  ER=Ai@R@Ai-np.eye(p)
  ferr=np.linalg.norm(ER-((np.eye(p)+F)@(np.eye(p)+E0)@(np.eye(p)+F).T-np.eye(p)),2)
  assert ferr<1e-10
  th=np.zeros(p);th[:2]=[1,1.3];eps=rng.normal(size=n);eps-=eps.mean();Y=X@th+eps
  V=Y@Y;nu=n/2+.01
  def lw(k):return -math.log(2)-gammaln(2*p)+gammaln(k+1)+gammaln(2*p-k)
  def score(T):
   U=X[:,T];G=U.T@U;v=U.T@Y;H=(n+1)*G+np.eye(len(T));Q=V-n*v@np.linalg.solve(H,v)
   return lw(len(T))-.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1])-nu*np.log(.02+(n-1)/V*Q)
  maxerr=0.;mis=0;comparisons=0
  for repeat in range(10):
   T=sorted([0,1]+[j for j in range(2,p) if rng.random()<.7]);U=X[:,T]
   if len(T)==2:continue
   Q=np.linalg.qr(U,mode='reduced')[0];RSS=V-np.linalg.norm(Q.T@Y)**2
   W0=RSS+(V-RSS)/(n+1)+.02*V/(n-1);b=n/((n+1)*W0)
   gains=[];zsq=[];Ac=lw(len(T)-1)-lw(len(T))+.5*np.log(n+1);ft=score(T)
   for j in T[2:]:
    Tm=[i for i in T if i!=j];Qm=np.linalg.qr(X[:,Tm],mode='reduced')[0];v=X[:,j]-Qm@(Qm.T@X[:,j]);Z=v@eps/np.linalg.norm(v)
    gain=score(Tm)-ft;pred=Ac-nu*np.log1p(b*Z**2);maxerr=max(maxerr,abs(gain-pred))
    gains.append(gain);zsq.append(Z**2);comparisons+=1
   mis+=int(np.argmax(gains)!=np.argmin(zsq))
  rows.append(dict(seed=seed,n=n,p=p,factorization_error=ferr,
    relative=np.linalg.norm(ER,2),rn_log_scale=np.sqrt(p*np.log(p+1)/n),
    max_ot_remainder=maxerr,n_times_remainder=n*maxerr,ordering_discrepancies=mis,comparisons=comparisons))
Path(__file__).with_name('N7_transfer_out.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(dict(cases=len(rows),max_n_remainder=max(x['n_times_remainder'] for x in rows),
 ordering_discrepancies=sum(x['ordering_discrepancies'] for x in rows),max_factorization_error=max(x['factorization_error'] for x in rows))))
