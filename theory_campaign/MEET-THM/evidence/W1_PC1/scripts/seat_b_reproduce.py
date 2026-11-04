# Seat B local check: weak non-zero cross-block correlation vs the BO-equivalent bridge.
# n=60, p=6, blocks {0,1,2},{3,4,5}, within rho=0.5, cross eps, S0={0,3}, beta=(1,0.8); exact enumeration of Omega.
# Computes chi2(pi||pi0) via WS1(a), the BO-equivalent chi2 (d replaced by d_sigma), the WS4(e) bound 4*eta_W,
# and the greedy ESS-0.9 grid length (60 halvings) for both bridges.
import numpy as np, itertools, math
from scipy.special import comb, logsumexp
def run(n,p,eps,seed,rho=0.5,beta=(1.0,0.8)):
    rng=np.random.default_rng(seed); K=min(p,n//2); blocks=[list(range(p//2)),list(range(p//2,p))]
    Sig=np.full((p,p),eps)
    for b in blocks:
        for i in b:
            for j in b: Sig[i,j]=rho if i!=j else 1.0
    X=rng.multivariate_normal(np.zeros(p),Sig,size=n); y=beta[0]*X[:,0]+beta[1]*X[:,p//2]+rng.normal(size=n)
    X=X-X.mean(0); X/=X.std(0,ddof=1); y=y-y.mean(); y/=y.std(ddof=1)
    a0=b0=0.01; nu=a0+n/2; Qbar=2*b0+y@y
    def logBF(S):
        if not S: return 0.0,0.0
        Xs=X[:,S]; G=Xs.T@Xs; H=(n+1)*G+np.eye(len(S)); z=Xs.T@y
        t=n*z@np.linalg.solve(H,z); D=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(S)))[1]
        return -0.5*D-nu*math.log(1-t/Qbar), t/Qbar
    models=[list(S) for k in range(K+1) for S in itertools.combinations(range(p),k)]
    lw=lambda k: -math.log(2)-math.log(comb(2*p-1,k,exact=True))
    lg0=[];d=[];ds=[];etas=[]
    for S in models:
        lb,xS=logBF(S); parts=[[j for j in S if j in b] for b in blocks]
        lr=[logBF(u)[0] for u in parts]; xb=[logBF(u)[1] for u in parts]
        lg0.append(lw(len(S))+sum(lr)); d.append(lb-sum(lr)); ds.append(nu*(sum(math.log(1-x) for x in xb)-math.log(1-sum(xb))))
        if len(S)>=2 and all(parts):
            R=(X[:,S].T@X[:,S])/(n-1); A=np.array([[R[i,k] if (S[i] in blocks[0])==(S[k] in blocks[0]) else 0 for k in range(len(S))] for i in range(len(S))])
            Ah=np.linalg.inv(np.linalg.cholesky(A)); M=Ah@(R-A)@Ah.T; e=np.linalg.norm(M,2); F=np.linalg.norm(M,'fro')**2; xbar=sum(xb)
            etas.append((nu*e*xbar/(1-e-xbar)+F/(4*(1-e))) if (e<1 and xbar<1-e) else math.inf)
    lg0=np.array(lg0); d=np.array(d); ds=np.array(ds); eta=max(etas)
    Lam=lambda phi,dd: logsumexp(lg0+phi*dd)-logsumexp(lg0)
    chi=lambda u,v,dd: math.exp(Lam(2*v-u,dd)-2*Lam(v,dd)+Lam(u,dd))-1
    def grid(dd):
        u=0.0;T=0
        while u<1:
            if chi(u,1.0,dd)<=1/9: return T+1
            lo,hi=u,1.0
            for _ in range(60):
                mid=(lo+hi)/2
                if chi(u,mid,dd)<=1/9: lo=mid
                else: hi=mid
            u=lo;T+=1
        return T
    return chi(0,1,d),chi(0,1,ds),4*eta,grid(d),grid(ds),float(np.max(np.abs(d-ds)))
print("eps seed chi2 chi2_BOequiv 4eta_W T T_sig max|d-d_sig|")
for eps in (0.0,0.02,0.05,0.10,0.20):
    for seed in range(4): print(eps,seed,*["%.3g"%v for v in run(60,6,eps,seed)])
