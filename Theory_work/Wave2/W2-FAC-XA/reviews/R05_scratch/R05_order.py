# R05 scratch: is the production-score deletion gain (D0 of FAC-B STATEMENT s1) a monotone function of
# |Z_B(T\j,j)| up to O(1/n) gain noise?  Random iid-CS design, centered/standardized, T contains S0.
import numpy as np, json
def logm(X,y,T,n):
    nu=.01+n/2
    if len(T)==0: return -nu*np.log(.02+y@y)
    XT=X[:,T]; G=XT.T@XT; z=XT.T@y; H=(n+1)*G+np.eye(len(T))
    Q=y@y-n*z@np.linalg.solve(H,z)
    return -.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1])-nu*np.log(.02+Q)
res=[]
for seed in range(5):
  rng=np.random.default_rng(100+seed); n=3000; p=60; rho=.5; sig=1.0
  f=rng.standard_normal(n); X=np.sqrt(rho)*f[:,None]+np.sqrt(1-rho)*rng.standard_normal((n,p))
  X=X-X.mean(0); X=X/np.sqrt((X**2).sum(0)/(n-1))
  th=np.zeros(p); th[[0,1]]=[1.0,1.3]
  Y=X@th+sig*rng.standard_normal(n); Y=Y-Y.mean(); y=Y/np.sqrt(Y@Y/(n-1))
  T=[0,1]+sorted(rng.choice(np.arange(2,p),size=40,replace=False).tolist())
  F0=logm(X,y,T,n); gains=[];Zs=[]
  for j in T[2:]:
    Tm=[t for t in T if t!=j]; gains.append(logm(X,y,Tm,n)-F0)
    XT=X[:,Tm]; r=X[:,j]-XT@np.linalg.lstsq(XT,X[:,j],rcond=None)[0]
    Zs.append((r@Y)/np.sqrt(r@r))   # unnormalized residual statistic (sigma scale)
  gains=np.array(gains); Z2=np.array(Zs)**2
  # fit gain = a - nu*log(1+b*Z2) exactly through the monotone map; check residual of best monotone fit
  order_g=np.argsort(-gains); order_z=np.argsort(Z2)
  # residual after fitting gain ~ c0 - nu*log(1+c1*Z2) by least squares over c1 grid
  nu=.01+n/2; best=1e9
  for c1 in np.linspace(.5,2,3001)/(n-1):
    pred=-nu*np.log1p(c1*Z2); c0=np.mean(gains-pred); r_=np.max(np.abs(gains-pred-c0)); best=min(best,r_)
  res.append(dict(seed=seed,same_order=bool((order_g==order_z).all()),max_monotone_fit_resid=best,gain_range=float(np.ptp(gains))))
  print(res[-1])
json.dump(res,open("R05_order_out.json","w"),indent=1)
