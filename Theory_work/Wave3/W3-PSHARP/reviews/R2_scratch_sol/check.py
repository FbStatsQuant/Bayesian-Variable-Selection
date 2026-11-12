import sys, pathlib, math, itertools
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import gammaln
from scipy.integrate import quad
base=pathlib.Path.cwd()/'Theory_work/Wave3/W3-PSHARP'
sys.path.insert(0,str(base/'numerics'))
import a_sph, c_counter
rng=np.random.default_rng(20261112)
a_sph.V1(rng)
c_counter.V1(rng)
c_counter.E2()
# Sphere density bounds: independently integrate exponentially tilted density.
count=0
for d in (3,4,10,50,199,999):
    c=math.exp(gammaln(d/2)-gammaln((d-1)/2))/math.sqrt(math.pi*d)
    for tau in (.1,1,min(5,d/2),d/2):
        h=lambda t:c*(1-t*t/d)**((d-3)/2)
        ew=2*quad(lambda t: math.exp(t*t/2)*h(t),0,math.sqrt(tau))[0]
        ew2=2*quad(lambda t: math.exp(t*t)*h(t),0,math.sqrt(tau))[0]
        lo=math.sqrt(2*tau/math.pi)*(1-1/d)*math.exp(-tau*tau/(2*d))
        hi=math.sqrt(2*tau/math.pi)*math.exp(tau/2+3*tau/(2*d))
        assert ew>=lo*(1-1e-11) and ew2<=hi*(1+1e-11)
        count+=1
print('Independent sphere moment bounds:',count,'PASS')
# C: scan integer rounding points and universal envelopes; analytic monotonicity handles n beyond scan.
worst=(0,0)
for n in range(200,200001):
    L=math.log(n); k=math.ceil(12*L); p=k+2
    assert p<=n//2 and k+1<=n-1
    env=3.78*(12*L+3)**2*n**(-2.158)
    if env>worst[0]:worst=(env,n)
    assert env<=1
    assert (n-1)/(8*n)-(48*L+8)/(1200*L*L)-1/n >= .1
    assert (3*p-1)*math.log(2)+(k/2)*L <=12*L*L
    assert (2*n*n+2*k)/(2*n-1)<=2*n
assert 1/42-1/100>=1/73
print('C integer/envelope checks n=200..200000 PASS; maximum envelope',worst)
