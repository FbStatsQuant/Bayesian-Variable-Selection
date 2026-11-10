# R02 scratch: exact checks of E1(b),(c), E2(ii) (incl. STATEMENT §0 "Always" claim), L1_POST step (1).
from math import lgamma, log, exp, ceil, inf
def lch(a,b): return lgamma(a+1)-lgamma(b+1)-lgamma(a-b+1)
def logw(p,k): return -log(2)-lch(2*p-1,k)
def lse(a,b):
    if a==-inf: return b
    if b==-inf: return a
    M=max(a,b); return M+log(exp(a-M)+exp(b-M))
def tails(p,K,s0):
    # logR[m] for m=-1..K  (index m+1)
    L=[-inf]*(K+2); acc=-inf
    for k in range(K,-1,-1):
        L[k+1]=acc  # R_k = sum_{j>k}
        acc=lse(acc,lch(p,k)+logw(p,k)-logw(p,s0))
    L[0]=acc
    return L
def msharp(L,n,s0,om):
    thr=-(s0+1)/2*log(n)-om; m=s0
    while L[m+1]>thr+1e-12: m+=1
    return m
bad=[];cnt=0
for n in [3,4,5,7,10,20,50,200,1000,10**4]:
  for p in [2,3,4,5,10,30,100,500,2000]:
    K=min(p,n//2)
    for s0 in range(0,min(K,6)+1):
      L=tails(p,K,s0)
      for om in [-20,-2,0,0.5*log(n),5]:
        ms=msharp(L,n,s0,om); cnt+=1
        rhs=min(K, s0+ceil((lch(p,s0)+(s0+1)/2*log(n)+om)/log(2)))
        if ms>rhs: bad.append(('E2ii/Always',n,p,s0,round(om,3),ms,rhs))
      for m in range(s0,K+1):
        lr=L[m+1]
        if lr==-inf: continue
        g=(m*(m-1)-(s0-1)*(s0-2))/(4*(p-1))
        if lr> lch(p,s0)-(m-s0)*log(2)-g+1e-9: bad.append(('E1b',n,p,s0,m))
        if s0>=1 and m<=K-1:
          lo=lch(p,s0)-(m+1-s0)*log(2)-(m*(m-1)-(s0-1)*(s0-2))/(4*(p-m))
          if lr<lo-1e-9: bad.append(('E1c',n,p,s0,m))
for A in [1,1.5,2]:
  for n in [10,50,200,1000,10**4]:
    for p in sorted(set([2,3,int(n**0.5)+1,n,int(min(n**A,20000))])):
      if p<2 or p>n**A: continue
      K=min(p,n//2)
      for s0 in range(1,min(K,4)+1):
        L=tails(p,K,s0); ms=msharp(L,n,s0,0.5*log(n))
        mbar=ceil((s0*(A*log(n)+log(2))+log(2)+(s0+2)/2*log(n))/log(1.5))
        if ms>max(s0,mbar): bad.append(('POST1',A,n,p,s0,ms,mbar))
print('cases',cnt,'violations:',len(bad))
for b in bad[:60]: print(b)
for (n,p,s0) in [(100,100,1),(1000,1000,1),(1000,20000,2),(10**4,10**4,3)]:
  K=min(p,n//2); L=tails(p,K,s0); print(n,p,s0,'m#=',msharp(L,n,s0,0.5*log(n)),'K=',K)
from collections import Counter
print(Counter(b[0] for b in bad))
print('E2ii with omega>=0:',[b for b in bad if b[0]=='E2ii/Always' and b[4]>=0][:20])
print('E2ii with omega<0, s0>=1, rhs>=s0:',[b for b in bad if b[0]=='E2ii/Always' and b[4]<0 and b[3]>=1 and b[6]>=b[3]][:10])
print('other:',[b for b in bad if b[0]!='E2ii/Always'][:20])
