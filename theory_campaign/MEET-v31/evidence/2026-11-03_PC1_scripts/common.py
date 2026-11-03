import numpy as np, itertools, math
from scipy.special import gammaln, betaln, comb
a0=b0=0.01
def standardise(Xr, yr):
    X = Xr/np.max(np.abs(Xr),0); X = X - X.mean(0); X = X/X.std(0,ddof=1)
    y = yr/np.max(np.abs(yr)); y = y - y.mean(); y = y/y.std(ddof=1)
    return X, y
def logCn(n): return a0*math.log(2*b0)+gammaln(a0+n/2)-(n/2)*math.log(math.pi)-gammaln(a0)
def score_parts(X,y,S):
    n=len(y); S=list(S); k=len(S)
    if k==0: return 0.0, float(y@y)
    G=X[:,S].T@X[:,S]; z=X[:,S].T@y
    H=(n+1)*G+np.eye(k)
    ldD=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1]
    Q=float(y@y - n*z@np.linalg.solve(H,z))
    return ldD, Q
def logm(X,y,S):
    n=len(y); ldD,Q=score_parts(X,y,S)
    return logCn(n)-0.5*ldD-(a0+n/2)*math.log(2*b0+Q)
def logw(k,p): return math.log(0.5)-math.log(comb(2*p-1,k,exact=True))
def models(p,K):
    for k in range(K+1):
        for S in itertools.combinations(range(p),k): yield S
def logWK(p,K): 
    v=[math.log(comb(p,k,exact=True))+logw(k,p) for k in range(K+1)]; m=max(v); return m+math.log(sum(math.exp(t-m) for t in v))
def enum_F(X,y,K):
    n,p=X.shape; lW=logWK(p,K)
    return {S: logw(len(S),p)-lW+logm(X,y,S) for S in models(p,K)}
def lse(v): v=np.asarray(list(v)); m=v.max(); return m+np.log(np.exp(v-m).sum())
