# Independent brute-force check of Lemma S(3)-(4) and Corollary B on small adversarial cases (own implementation).
import math, itertools, numpy as np
B0=0.01
def std(Xr,yr):
    n=len(yr); X=Xr-Xr.mean(0); X/=np.sqrt((X**2).sum(0)/(n-1)); y=yr-yr.mean(); y/=np.sqrt((y**2).sum()/(n-1)); return X,y
def lsc(X,y,S):
    n,p=X.shape; nu=0.01+n/2; k=len(S)
    lw=-math.log(2)-(math.lgamma(2*p)-math.lgamma(k+1)-math.lgamma(2*p-k))
    if k==0: return lw-nu*math.log(2*B0+y@y), y@y
    XS=X[:,S]; G=XS.T@XS; H=(n+1)*G+np.eye(k); A=G+np.eye(k); z=XS.T@y
    Q=y@y-n*z@np.linalg.solve(H,z)
    return lw-0.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(A)[1])-nu*math.log(2*B0+Q), Q
rng=np.random.default_rng(7); minS=np.inf; minB=np.inf; cnt=0
for rep in range(150):
    n=int(rng.choice([6,8,10,14,30,100])); p=int(rng.choice([2,3,4,5,6,7]))
    Z=rng.standard_normal((n,p))
    kind=rep%4
    if kind==1: Z=Z+4*rng.standard_normal((n,1))
    if kind==2 and p>=3: Z[:,1]=Z[:,0]+1e-6*rng.standard_normal(n)
    yr = Z[:,:2].sum(1)*rng.uniform(0,3)+rng.standard_normal(n) if kind!=3 else rng.standard_cauchy(n)
    X,y=std(Z,yr); K=min(p,n//2)
    allS=[list(S) for k in range(K+1) for S in itertools.combinations(range(p),k)]
    sc={tuple(S):lsc(X,y,S) for S in allS}
    lz=np.logaddexp.reduce([v[0] for v in sc.values()])
    for S0 in allS:
        s0=len(S0)
        if s0>K-1: continue
        l0,Q0=sc[tuple(S0)]
        odds=math.exp(lz-l0)-1 if lz-l0>1e-8 else sum(math.exp(v[0]-l0) for k,v in sc.items() if list(k)!=S0)
        # Lemma S(4) with N = all nulls
        nu=0.01+n/2; tot=0
        for j in range(p):
            if j in S0: continue
            Q1=sc[tuple(sorted(S0+[j]))][1]; gam=(Q0-Q1)/(2*B0+Q0); assert -1e-12<=gam<1
            tot+=math.exp(nu*gam)
        rhs=(s0+1)/(2*p-1-s0)/math.sqrt(n)*tot
        minS=min(minS,odds/rhs)
        Olb=sum(math.comb(s0+j,j)*n**(-j/2)*math.prod((p-s0-i)/(2*p-1-s0-i) for i in range(j)) for j in range(1,K-s0+1))
        minB=min(minB,odds/Olb); cnt+=1
print(cnt,"cases; min odds/LemmaS(4) rhs =",minS,"; min odds/O_lb =",minB)
