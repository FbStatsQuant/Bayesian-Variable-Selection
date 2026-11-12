import sys, math, importlib, pathlib
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'numerics'))
import numpy as np
import a_orth, a_sph, c_counter, b_check
rng=np.random.default_rng(71913)
a_orth.V1(rng)
a_sph.V1(rng)
c_counter.V1(rng)
c_counter.E2()
b_check.F1(rng)
b_check.F2(rng)
# Exact grouped enumeration for orthogonal X, y=sum(signal columns)/sqrt(s).
# All models with t signal and u null columns have the same score.
from scipy.special import gammaln, logsumexp

def grouped(n,p,s):
    ts=np.arange(s+1)[:,None]; us=np.arange(p-s+1)[None,:]
    ks=ts+us
    lc=lambda a,k:gammaln(a+1)-gammaln(k+1)-gammaln(a-k+1)
    Q=(n-1)/n+((n-1)**2/n)*(s-ts)/s
    scores=-lc(2*p-1,ks)-.5*ks*math.log(n)-(n/2+.01)*np.log(.02+Q)
    logtotal=logsumexp(scores+lc(s,ts)+lc(p-s,us))
    pi=math.exp(float(scores[s,0]-logtotal))
    return pi
print('COUNTEREXAMPLES TO REPORT SUMMARY (not to the locked statement):')
for n,p,s in [(10000,100,99),(1000000,1000,999),(10000,200,100),(1000000,2000,1000)]:
    print(n,p,s,'pi(S0)=',grouped(n,p,s),'claimed critical cap=',math.exp(-s/math.sqrt(n)/2))
# Independent C upper envelope and constant arithmetic. Beyond 200: derivatives
# 24/(12 log n+3)-2.158 and 24/n-1/2 are negative.
n=np.arange(200,100001,dtype=float); L=np.log(n); k=np.ceil(12*L)
env=3.78*(12*L+3)**2*n**(-2.158)
assert np.all(k+2<=n/2)
assert np.max(env)<1
assert np.all(6*L**2+25.5*L+5.6<=12*L**2)
assert 1/42-1/100>=1/73
print('C envelopes: max cutoff envelope=',max(env),'at n=',n[env.argmax()],'; exponent margin=',1/42-1/100-1/73)
