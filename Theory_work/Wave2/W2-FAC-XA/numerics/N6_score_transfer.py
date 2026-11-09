"""Small exact enumeration to falsify L4 algebra and comparison scaling."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json,itertools
from pathlib import Path
def root(S):
 w,v=np.linalg.eigh(S);return (v*np.sqrt(w))@v.T
rows=[]
for seed in range(10):
 rng=np.random.default_rng(seed);p=8;n=512;d=n-1
 lam=np.linspace(.4,.85,p);S=np.diag(1-lam**2)+np.outer(lam,lam);A=root(S)
 X=rng.normal(size=(2048,p))@A;R=np.corrcoef(X,rowvar=False)
 invA=np.linalg.inv(A);E=invA@R@invA-np.eye(p);L=root(np.eye(p)+E);B=L@A
 e=np.linalg.norm(L-np.eye(p),2);z=rng.normal(size=p);r=float(rng.chisquare(d-p))
 th=np.zeros(p);th[:2]=[1,1.3];vals=[[],[]]; maxid=0.;maxJ=0.
 for ii,M in enumerate((A,B)):
  y=np.sqrt(d)*M@th+z;V=y@y+r
  for k in range(p-1):
   for extra in itertools.combinations(range(2,p),k):
    T=[0,1]+list(extra);U=M[:,T];G=d*U.T@U;v=np.sqrt(d)*U.T@y
    H=(n+1)*G+np.eye(len(T));Q=V-n*v@np.linalg.solve(H,v)
    P=U@np.linalg.solve(U.T@U,U.T);RSS=r+z@(np.eye(p)-P)@z
    J=Q-RSS-(V-RSS)/(n+1);maxJ=max(maxJ,J)
    assert J>=-1e-8
    W=RSS+(V-RSS)/(n+1)+J+.02*V/d
    direct=-.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1])-(n/2+.01)*np.log(.02+d/V*Q)
    D=np.linalg.slogdet(np.eye(len(T))+np.linalg.inv(G)/(n+1))[1]-np.linalg.slogdet(np.eye(len(T))+np.linalg.inv(G))[1]
    centered=-len(T)*np.log(n+1)/2-D/2-(n/2+.01)*np.log(W)
    maxid=max(maxid,abs(direct+(n/2+.01)*np.log(d/V)-centered))
    vals[ii].append(centered)
 err=float(np.max(np.abs(np.array(vals[0])-vals[1])))
 assert maxid<1e-8
 rows.append(dict(seed=seed,e=e,sets=len(vals[0]),max_algebra_error=maxid,max_J=maxJ,
                  centered_score_difference=err,ratio_to_scale=err/(e*(z@z+1)+p/n+1/n)))
Path(__file__).with_name('N6_score_transfer_out.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(dict(cases=len(rows),max_algebra_error=max(x['max_algebra_error'] for x in rows),
max_scale_ratio=max(x['ratio_to_scale'] for x in rows))))
