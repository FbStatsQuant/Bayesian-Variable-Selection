import math,itertools
import numpy as np
rng=np.random.default_rng(17819)
worst_det=0.; worst_fit=0.; worst_B=0.; cases=0
for n in (6,9,16):
 for p in (2,4,6):
  for trial in range(12):
   X=rng.normal(size=(n,p)); X-=X.mean(axis=0); X*=np.sqrt(n-1)/np.linalg.norm(X,axis=0)
   if trial%3==0: X[:,1]=X[:,0]
   y=rng.normal(size=n); y-=y.mean(); y*=np.sqrt(n-1)/np.linalg.norm(y)
   K=min(p,n//2); nu=.01+n/2
   models=[s for k in range(K+1) for s in itertools.combinations(range(p),k)]
   info={}
   for s in models:
    xs=X[:,s]; G=xs.T@xs; H=(n+1)*G+np.eye(len(s)); z=xs.T@y
    ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(s)))[1]
    Q=y@y-n*z@np.linalg.solve(H,z)
    logw=-math.log(2)-math.log(math.comb(2*p-1,len(s)))
    info[s]=(ld,Q,logw-.5*ld-nu*math.log(.02+Q))
   mx=max(v[2] for v in info.values()); Z=sum(math.exp(v[2]-mx) for v in info.values())
   for s in models:
    t=len(s)
    if t>=K: continue
    ld,Q,lp=info[s]; pi=math.exp(lp-mx)/Z; odds=(1-pi)/pi
    lb=sum(math.comb(t+j,j)*n**(-j/2)*math.prod((p-t-i)/(2*p-1-t-i) for i in range(j)) for j in range(1,K-t+1))
    worst_B=max(worst_B,lb/odds)
    xs=X[:,s]; G=xs.T@xs; H=(n+1)*G+np.eye(t); res=y-(n+1)*xs@np.linalg.solve(H,xs.T@y)
    for j in set(range(p))-set(s):
     u=tuple(sorted(s+(j,))); ld1,Q1,_=info[u]; g=xs.T@X[:,j]
     sch=n*n-(n+1)**2*g@np.linalg.solve(H,g)
     ratio=sch/(n-g@np.linalg.solve(G+np.eye(t),g))
     worst_det=max(worst_det,abs(math.exp(ld1-ld)-ratio))
     worst_fit=max(worst_fit,abs((Q-Q1)-n*(X[:,j]@res)**2/sch))
     assert ratio<=n+1e-8 and Q1>=-1e-8 and Q1<=Q+1e-8
     cases+=1
print('small-model checks',cases,'max determinant identity error',worst_det,'max fit identity error',worst_fit,'max B lower-bound / exact odds',worst_B)
# C: exact combinatorial tail; stable 2-dimensional representation of T.
max_R=0.; max_A=0.; min_cost=1.; min_gap=1.
for n in list(range(200,20001))+[100000,1000000,1000000000]:
 k=math.ceil(12*math.log(n)); p=k+2; m=k//2
 R=sum(math.comb(p,j)/math.comb(2*p-1,j)*math.comb(2*p-1,2) for j in range(m+1,p+1))
 eta=n**-2; c=(1+eta*eta*k)**-.5
 # row basis: x1 / sqrt(n-1), u / sqrt(k*(n-1)).
 B=np.sqrt(n-1)*np.array([[1.,c],[0.,-c*eta*np.sqrt(k)]])
 H=np.eye(2)+(n+1)*(B.T@B)
 detG=(n-1)**2*c*c*eta*eta*k; trG=2*(n-1)
 D=(1+(n+1)*trG+(n+1)**2*detG)/(1+trG+detG)
 # loss of unit signal e2 under the ridge smoother, inverse in observation basis.
 loss=np.eye(2)/(n+1)+n/(n+1)*np.linalg.inv(np.eye(2)+(n+1)*(B@B.T))
 max_R=max(max_R,R*n*n); max_A=max(max_A,R*np.sqrt(D*n)*n/2)
 min_cost=min(min_cost,loss[1,1]); assert p<=n//2 and k+1<=n-1
print('C cutoff max R*n^2',max_R,'max A/(2/n)',max_A,'min reference cost / energy',min_cost)

