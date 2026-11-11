import itertools, math
import numpy as np
from pathlib import Path

out=[]
min_f=0.; max_curv=0.
for n in [16,17,32,100,1000,10000]:
    N=n-1
    for ep in np.linspace(0,2*N,101):
        u=np.linspace(1,1+1/math.sqrt(n),301) if ep>=N else np.linspace(1-1/math.sqrt(n),1,301)
        f=-N/2*np.log(u)+ep/2*(1-1/u)
        curv=N/(2*u*u)-ep/u**3
        min_f=min(min_f,float(f.min())); max_curv=max(max_curv,float(abs(curv).max()/N))
        assert f.min()>=-3-1e-10 and abs(curv).max()<=6*N
out.append(f'C1: min F={min_f:.12g}; max |Fsecond|/N={max_curv:.12g}; PASS')
rng=np.random.default_rng(218)
min_gain=math.inf; max_err=0.; count=0
for n in [16,40,100]:
  for design in range(4):
    x=rng.normal(size=(n,6)); x-=x.mean(axis=0)
    if design==1: x[:,5]=x[:,4]
    if design==2: x[:,5]=x[:,0]+x[:,1]
    if design==3: x[:,5]=x[:,0]+1e-5*x[:,5]
    x*=np.sqrt((n-1)/(x*x).sum(axis=0))
    mu=x[:,:2]@np.array([1.,-1.]); e=rng.normal(size=n); e-=e.mean(); y=mu+e
    def mp(s):
      if not s: return np.zeros((n,n)),np.zeros((n,n))
      u,d,_=np.linalg.svd(x[:,s],full_matrices=False); keep=d>1e-10
      u=u[:,keep]; d=d[keep]
      return (u*(n*d*d/((n+1)*d*d+1)))@u.T,u@u.T
    m0,p0=mp([0,1]); R=y@(np.eye(n)-m0)@y-e@(np.eye(n)-p0)@e
    for k in range(7):
      for s in itertools.combinations(range(6),k):
        m,p=mp(list(s)); mt,pt=mp(sorted(set(s)|{0,1})); a=(np.eye(n)-m)@mu; L=mu@a
        q=y@(np.eye(n)-m)@y
        rhs=e@e-e@m@e+2*e@a+L
        max_err=max(max_err,abs(q-rhs))
        assert a@a<=L+1e-8
        assert np.linalg.norm(m@y-mu)**2<=2*e@p@e+2*L+1e-8
        gain=q-y@(np.eye(n)-mt)@y
        lower=L+2*e@a-e@(pt-p0)@e-R
        min_gain=min(min_gain,gain-lower); assert gain>=lower-1e-8
        count+=1
out.append(f'D1/E1: {count} models; max decomposition error={max_err:.12g}; min gain slack={min_gain:.12g}; PASS')
text='\n'.join(out)+'\n'
print(text)
Path(__file__).with_name('check_out.txt').write_text(text,encoding='utf-8')
