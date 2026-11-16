# R1 opus scratch: check AE §2 truncated means and Lemma F/T arithmetic numerically.
import math, numpy as np
from math import lgamma
def EU_sphere(d,T,m=400001):
    tau=2*math.log(T); t=np.linspace(-math.sqrt(tau),math.sqrt(tau),m)
    cd=math.exp(lgamma(d/2)-lgamma((d-1)/2))/math.sqrt(math.pi*d)
    f=np.exp(t**2/2)*cd*(1-t**2/d)**((d-3)/2)
    return np.trapz(f,t)
for d,T in [(9,2.0),(39,5.0),(99,30.0),(999,1e3),(9999,1e6)]:
    if 2*math.log(T)>d/2: continue
    e=EU_sphere(d,T); g=2*math.sqrt(math.log(T)/math.pi)
    lo=g*(1-1/d)*math.exp(-2*math.log(T)**2/d); hi=g*math.exp(3*math.log(T)/d)
    print(f"d={d} T={T}: lo={lo:.6f} EU={e:.6f} hi={hi:.6f} ok={lo<=e<=hi}")
# Gaussian exact
T=50.; z=np.linspace(-math.sqrt(2*math.log(T)),math.sqrt(2*math.log(T)),200001)
print("gauss", np.trapz(np.exp(z**2/2)*np.exp(-z**2/2)/math.sqrt(2*math.pi),z), 2*math.sqrt(math.log(T)/math.pi))
# Lemma T Monte Carlo, N=1..3, c small, chi2_1 scores, no events
rng=np.random.default_rng(1)
for N,c in [(1,1e-3),(3,1e-3),(2,1e-2)]:
    eps=0.4; T=(eps/4)/c
    Z=rng.standard_normal((2_000_000,N)); V=np.exp(Z**2/2)
    odds=c*V.sum(1); delta=odds/(1+odds)
    L=c*N*2*math.sqrt(math.log(T)/math.pi)
    print(N,c,"E delta",delta.mean(),"LemmaT bound",L*(1-c*T-L))
