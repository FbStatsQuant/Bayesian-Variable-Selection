import time
from fcommon import *
n,p=400,12
rng=np.random.default_rng(1)
Sig=ar_sigma(p)
Lc=np.linalg.cholesky(Sig)
t=time.time()
Xr=rng.standard_normal((n,p))@Lc.T
b=np.zeros(p); b[:3]=[1,-1,1]
yr=Xr@b+rng.standard_normal(n)
d,idx,pi,sz,Q,B,s2=exact_posterior_draws(Xr,yr,100000,rng)
print('post',time.time()-t); t=time.time()
d2=gauss_d2(d,B,s2,b,Sig)
print('d2',time.time()-t, np.quantile(n*d2,[.5,.9,.99,.999]), (n*d2>6).mean(), sample_quantities(d,b))
