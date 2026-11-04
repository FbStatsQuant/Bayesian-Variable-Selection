import json, math,itertools
from pathlib import Path
import numpy as np
out={}
# Design p=2 duplicates, centered norm sqrt(n-1), response correlation .5.
n=20
x=np.arange(n,dtype=float);x-=x.mean();x*=math.sqrt((n-1)/(x@x))
v=np.cos(np.arange(n));v-=v.mean();v-=x*(x@v)/(n-1);v*=math.sqrt((n-1)/(v@v))
y=.5*x+math.sqrt(.75)*v
out['tied_design']=dict(n=n,p=2,G=((np.column_stack([x,x])).T@np.column_stack([x,x])).tolist(),z=[float(x@y)]*2,Y=float(y@y))
# Exact-Gram weak nonzero correlation family for B(F), eventual coded blocks g=9, B=16.
# p ~ sqrt(n), lambda_min>=.4, two coefficients .2,.25, sigma=1, c0=.001.
out['B_F_family']=dict(g=9,rho=.6,c0=.001,sigma=1,theta=[.2,.25],A=1,eta=1e-4,eta_A=(math.sqrt(3)-math.sqrt(2))**2,leakage_bound_coefficient=.001**2*9*(.2+.25)**2/.4,Mn='loglog(n+exp(exp(1)))',p='9*floor(sqrt(n)/9); sufficiently large n; B=16, 9<=16<18')
# The leakage bound follows ||P_C mu_-||² <= (n-1) g psi² (sum outside beta)^2/lambda_min(R_C).
assert out['B_F_family']['leakage_bound_coefficient']<out['B_F_family']['eta']<out['B_F_family']['eta_A']
# SL: Gaussian noise has positive projection on isolated hub almost surely, even when x_h' mu=0.
u=x/math.sqrt(n-1);mu=v;noise=.1*u
out['SL_sample_cov_cex']=dict(n=n,x_mu=float(x@mu),x_y=float(x@(mu+noise)),note='Population cancellation x_h^T mu=0 does not imply x_h^T y=0; noise projection has continuous Gaussian law.')
# Simultaneous interval controls: discrete fixed grid does not determine exact quantiles.
out['CDF_quantile_gap']=dict(F='Uniform[0,1]',Ftilde='Uniform[0,1+epsilon]',pointwise_CDF_error='<=epsilon',quantile_error='positive for every alpha>0',conclusion='No exact equality of continuous quantiles from a positive CDF tolerance; need finite endpoint margin or inverse-CDF regularity for numerical error.')
# Arbitrary bounded h scale missing; weak signal necessity failure; delivery oscillation.
out['delivery_limit_cex']=dict(wrong_output=0,P_U_even=0,P_U_odd=.5,correct_even=1,correct_odd=.5,claimed_limit=.5)
# Weak-signal finite sequence: beta=n^-1/2, BO, leakage/cancellation zero.
weak=[]
for nn in (40,400,4000,40000):
    # Centered observed y with unit residual variance and signal beta, then standardise.
    yy=nn-1;zz=(nn-1)/math.sqrt(nn+1)
    gain=(nn*zz*zz)/(nn*nn)
    logBF=-.5*math.log(nn)-(.01+nn/2)*math.log1p(-gain/(yy+.02))
    # p=2, BO, independent block factors but global size weights: w0=1/2,w1=w2=1/6.
    # Observed second coordinate projection zero.
    rb=math.exp(logBF);rnull=nn**(-.5)
    truth=(rb/6)/(.5+(rb+rnull)/6+rb*rnull/6)
    weak.append(dict(n=nn,beta=nn**(-.5),logBF=logBF,pi0_truth=truth,leakage=0,cancellation=0))
out['weak_signal_no_cancellation']=weak
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
