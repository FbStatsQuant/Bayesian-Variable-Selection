# Sharp exact-branch threshold of the coded rule vs Lemma ENUM's sufficient condition p <= c log n, c < 1/log 2.
import math
def exact(n,p):
    K=min(p,n//2); N0=max(2500,n,p); H0=(512*N0+2499)//2500; thr=(5*H0+4*N0)*p
    s=0;c=1
    for k in range(K+1):
        if k>0: c=c*(p-k+1)//k
        s+=c
        if s>thr: return False
    return True
for e in [4,6,8,10,15,20,30,40,60]:
    n=10**e
    pmax=max(p for p in range(1,400) if exact(n,p))
    print(f"n=1e{e}: max p on exact branch={pmax}, log2 n={math.log2(n):.2f}, pmax/log n={pmax/math.log(n):.4f}, 1/log2={1/math.log(2):.4f}, p=floor(log2 n)+floor(log2 log2 n) exact? {exact(n,int(math.log2(n))+int(math.log2(math.log2(n))))}")
