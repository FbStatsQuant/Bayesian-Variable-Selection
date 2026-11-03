# PC2 common: spec target (METHODOLOGY_v3 §5), exact enumeration helpers, box bounds of O-CERT C4.
import numpy as np, itertools, math
from scipy.special import gammaln, comb
a0=b0=0.01
def std(Xr, yr):
    X = Xr - Xr.mean(0); X = X/np.sqrt((X**2).sum(0)/(len(yr)-1))
    y = yr - yr.mean(); y = y/np.sqrt((y**2).sum()/(len(yr)-1))
    return X, y
def logCn(n): return a0*math.log(2*b0)+gammaln(a0+n/2)-(n/2)*math.log(math.pi)-gammaln(a0)
def QD(X,y,S):
    n=len(y); S=list(S); k=len(S)
    if k==0: return float(y@y), 0.0
    G=X[:,S].T@X[:,S]; z=X[:,S].T@y
    H=(n+1)*G+np.eye(k)
    ldD=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1]
    Q=float(y@y - n*z@np.linalg.solve(H,z))
    return Q, ldD
def logw(k,p): return math.log(0.5)-math.log(comb(2*p-1,k,exact=True))
def logWK(p,K):
    v=[math.log(comb(p,k,exact=True))+logw(k,p) for k in range(K+1)]; m=max(v); return m+math.log(sum(math.exp(t-m) for t in v))
class Target:
    def __init__(s,X,y):
        s.X,s.y=X,y; s.n,s.p=X.shape; s.K=min(s.p,s.n//2); s.nu=a0+s.n/2; s.lC=logCn(s.n); s.lW=logWK(s.p,s.K)
        s.lw=[logw(k,s.p) for k in range(s.K+1)]; s._c={}
    def qd(s,S):
        S=tuple(sorted(S))
        if S not in s._c: s._c[S]=QD(s.X,s.y,S)
        return s._c[S]
    def F(s,S):
        S=tuple(sorted(S)); 
        if len(S)>s.K: return -math.inf
        Q,lD=s.qd(S); return s.lw[len(S)]-s.lW+s.lC-0.5*lD-s.nu*math.log(2*b0+Q)
    def Phi(s,L,U):
        QU,_=s.qd(U); _,lDL=s.qd(L); return s.lw[len(L)]-s.lW+s.lC-0.5*lDL-s.nu*math.log(2*b0+QU)
    def M(s,L,U):
        QU,_=s.qd(U); _,lDL=s.qd(L); kL=len(L); f=len(U)-kL
        ks=range(kL, min(len(U),s.K)+1)
        if kL>s.K or not len(ks): return -math.inf
        v=[math.log(comb(f,k-kL,exact=True))+s.lw[k] for k in ks]; m=max(v)
        return m+math.log(sum(math.exp(t-m) for t in v))-s.lW+s.lC-0.5*lDL-s.nu*math.log(2*b0+QU)
    def models(s):
        for k in range(s.K+1):
            for S in itertools.combinations(range(s.p),k): yield S
    def enum(s): return {S:s.F(S) for S in s.models()}
def lse(v):
    v=np.asarray(list(v),dtype=float)
    if not len(v): return -math.inf
    m=v.max(); return m+np.log(np.exp(v-m).sum())
