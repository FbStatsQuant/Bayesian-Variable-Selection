# Lemma W(ii): sphere truncated moments vs claimed bounds; c_d sqrt(2pi) bounds.
import math
from scipy import integrate, special
bad=0
for d in [3,4,5,10,50,200,1000,10000]:
    lc = special.gammaln(d/2)-special.gammaln((d-1)/2)-0.5*math.log(math.pi*d)
    cd=math.exp(lc); v=cd*math.sqrt(2*math.pi)
    if not (1-1/d-1e-12<=v<=1+1e-12): bad+=1; print("cd bound fail",d,v)
    for tau in [0.5,1,2,math.log(d) if d>2 else 1, d/4, d/2]:
        if tau>d/2: continue
        h=lambda t: cd*(1-t*t/d)**((d-3)/2)
        EW=integrate.quad(lambda t: math.exp(t*t/2-tau/2)*h(t),-math.sqrt(tau),math.sqrt(tau),limit=200)[0]
        EW2=integrate.quad(lambda t: math.exp(t*t-tau)*h(t),-math.sqrt(tau),math.sqrt(tau),limit=200)[0]
        lo=math.sqrt(2*tau/math.pi)*(1-1/d)*math.exp(-tau*tau/(2*d))
        hi=math.sqrt(2*tau/math.pi)*math.exp(-tau/2+3*tau/(2*d))
        lo*=math.exp(-tau/2)
        if EW<lo*(1-1e-10) or EW2>hi*(1+1e-10): bad+=1; print("fail",d,tau,EW,lo,EW2,hi)
print("Lemma W(ii) violations:",bad)
# Lemma W chebyshev constant check: chi2_1 exact
for N in [10,1000,10**6]:
    tau=2*math.log(N)
    EW=math.sqrt(2*tau/math.pi); EW2=2/math.sqrt(2*math.pi)*integrate.quad(lambda z: math.exp(z*z/2),0,math.sqrt(tau))[0]
    print(N, EW2 <= EW*N)
