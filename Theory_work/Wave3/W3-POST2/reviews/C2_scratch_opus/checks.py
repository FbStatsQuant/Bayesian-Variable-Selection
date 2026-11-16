# C2 seat B checks: (1) c0 < c1 grid (#14); (2) Lemma E0 bound and m#_n >= min(B,K) by exact R_m (#9, #11);
# (3) intercept orthogonality identity (#8).
import math, itertools, random
from math import comb, log
def j0f(s0,A): return math.ceil((2*A+1)*s0)+1
def c0(s0,A):
    j=j0f(s0,A); Cs=2*s0+3*(A*j+s0+math.log(j+1)+1)
    return max(4*Cs,32*(s0*(A+1)+2))
def c1(s0,A):
    j=j0f(s0,A); CA=8+3*A; Cx=A*j+s0+math.log(j+1)+2
    return (math.sqrt(2*Cx)+math.sqrt(2*Cx+CA*j+(2/math.log(2))*(s0*(A+1)+2)))**2
mn=(9,None)
for s0 in range(1,21):
    for k in range(0,901):
        A=1+k*0.01
        r=c1(s0,A)/c0(s0,A)
        if r<mn[0]: mn=(r,(s0,A))
print("s0=0: c1/c0=%.4f (no underfits; relation vacuous)"%(c1(0,1)/c0(0,1)))
print("grid s0=1..20, A=1..10 step .01: min c1/c0 = %.4f at %s"%mn)
print("s0=A=1: c0=%.1f c1=%.2f"%(c0(1,1),c1(1,1)))
# (2) exact R_m and m#_n
def mstar(n,p,s0):
    K=min(p,n//2)
    if s0>K: return None
    from fractions import Fraction as Fr
    w=lambda k: Fr(1,2*comb(2*p-1,k))
    q=[comb(p,k)*w(k) for k in range(K+1)]
    thr=n**(-(s0+2)/2)
    for m in range(s0,K+1):
        Rm=float(sum(q[m+1:K+1])/w(s0))
        if Rm<=thr: return m,K
    return K,K
bad=0; worst=[]
for A in [1,2]:
  for s0 in [0,1,2,3]:
    j0=j0f(s0,A)
    for B in sorted({j0,s0+j0,s0+1}):
      for n in [50,200,1000,5000]:
        thrOK = (4*B)**(-B) > n**(-(s0+2)/2)
        if not thrOK: continue
        for p in list(range(max(2,s0),40))+[100,min(int(n**A),400)]:
          if p<s0: continue
          r=mstar(n,p,s0)
          if r is None: continue
          m,K=r
          if m<min(B,K): bad+=1; worst.append((A,s0,B,n,p,m,K))
print("E0 exact check (cases where (4B)^-B > n^-(s0+2)/2): violations =",bad, worst[:5])
# smallest-p cases named in the brief: p=K=2, s0=A=1
for n in [50,1000]:
    print("p=2,s0=1,n=%d: (m#,K)="%n, mstar(n,2,1))
# (3) intercept identity
random.seed(1); mx=0
for _ in range(2000):
    n=random.randint(3,30)
    a=[random.gauss(0,1) for _ in range(n)]; b=[random.gauss(0,1) for _ in range(n)]
    ma=sum(a)/n; mb=sum(b)/n; a=[x-ma for x in a]; b=[x-mb for x in b]   # mu-hat, mu in 1-perp
    eb=random.gauss(0,1)
    lhs=sum((eb+x-y)**2 for x,y in zip(a,b)); rhs=n*eb**2+sum((x-y)**2 for x,y in zip(a,b))
    mx=max(mx,abs(lhs-rhs))
print("intercept: max |sum(ebar+muhat-mu)^2 - (n ebar^2 + ||muhat-mu||^2)| =",mx)
