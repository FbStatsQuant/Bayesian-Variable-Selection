"""R04 checks of L4: (a) production-score fidelity of the coupled coordinate representation on real
n x p data; (b) projection difference vs e/(1-e); (c) ST ratio under p,n scaling (random T>=S0);
(d) truth-out sets: discrepancy scale (diagnostic for a possible extension)."""
import os; os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np, json, math
from scipy.special import gammaln
def sym(S,f):
    w,v=np.linalg.eigh(S); return (v*f(w))@v.T
def prod_score(X,y,T,p,n):
    # D0 + prior, exactly as FAC-B section 1 (log c_n omitted: n-only constant)
    k=len(T); nu=0.01+n/2
    logw=-math.log(2)-(gammaln(2*p)-gammaln(k+1)-gammaln(2*p-k))
    if k==0: return logw-nu*math.log(.02+y@y)
    XT=X[:,T]; G=XT.T@XT; zz=XT.T@y; H=(n+1)*G+np.eye(k)
    Q=y@y-n*zz@np.linalg.solve(H,zz)
    return logw-.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(k))[1])-nu*math.log(.02+Q)
def coord_score(M,yv,T,p,n,d):
    # L4 representation: design columns sqrt(d) m_j (plus zero coord), response yv (len p+1)
    V=yv@yv; y=yv*math.sqrt(d/V); Xc=np.vstack([math.sqrt(d)*M,np.zeros((1,M.shape[1]))])
    return prod_score(Xc,y,T,p,n)
out={}
rng=np.random.default_rng(2026)
# (a) fidelity
fid=[]
for (n,p,rho) in [(400,12,.5),(2000,30,.3)]:
    d=n-1; Sig=(1-rho)*np.eye(p)+rho*np.ones((p,p)); A=sym(Sig,np.sqrt)
    Xr=rng.normal(size=(n,p))@A; Xc=Xr-Xr.mean(0); X=Xc/Xc.std(0,ddof=1)
    th=np.zeros(p); th[:3]=[1,-.7,1.2]; sig=1.3
    eps=rng.normal(size=n)*sig; Ce=eps-eps.mean(); Y=X@th+Ce; y=Y*math.sqrt(d/(Y@Y))
    R=X.T@X/d; W=sym(Sig,lambda w:1/np.sqrt(w))@R@sym(Sig,lambda w:1/np.sqrt(w))
    L=sym(W,np.sqrt); B=L@A; U=X@np.linalg.inv(B)/math.sqrt(d)
    z=U.T@Ce/sig; r=(Ce@Ce-(U.T@Ce)@(U.T@Ce))/sig**2
    yB=np.concatenate([math.sqrt(d)*B@th+sig*z,[sig*math.sqrt(r)]])
    md=0.
    for _ in range(60):
        k=rng.integers(0,p+1); T=sorted(rng.choice(p,k,replace=False).tolist())
        md=max(md,abs(prod_score(X,y,T,p,n)-coord_score(B,yB,T,p,n,d)))
    fid.append(dict(n=n,p=p,UtU_err=float(np.abs(U.T@U-np.eye(p)).max()),max_score_diff=md,
                    e=float(np.linalg.norm(L-np.eye(p),2)),whitened_dev=float(np.linalg.norm(W-np.eye(p),2))))
out['fidelity']=fid
# (b),(c),(d)
sc=[]
for rho in [.5]:
  for p in [10,40,80]:
    for n in [1000,10000,100000]:
        d=n-1; Sig=(1-rho)*np.eye(p)+rho*np.ones((p,p)); A=sym(Sig,np.sqrt)
        Xr=rng.normal(size=(n,p))@A; R=np.corrcoef(Xr,rowvar=False)
        Wm=sym(Sig,lambda w:1/np.sqrt(w))@R@sym(Sig,lambda w:1/np.sqrt(w)); L=sym(Wm,np.sqrt); B=L@A
        e=np.linalg.norm(L-np.eye(p),2); z=rng.normal(size=p); r=rng.chisquare(d-p); sig=1.0
        th=np.zeros(p); S0=[0,1,2]; th[S0]=[1,-.7,1.2]
        yA=np.concatenate([math.sqrt(d)*A@th+sig*z,[sig*math.sqrt(r)]])
        yB=np.concatenate([math.sqrt(d)*B@th+sig*z,[sig*math.sqrt(r)]])
        CA=-(n/2+.01)*math.log(d/(yA@yA)); CB=-(n/2+.01)*math.log(d/(yB@yB))
        st=0.; pd=0.; tout=0.
        for it in range(120):
            extra=sorted(rng.choice(range(3,p),rng.integers(0,p-2),replace=False).tolist())
            T=S0+extra if it>0 else list(range(p))
            fa=coord_score(A,yA,T,p,n,d)-CA; fb=coord_score(B,yB,T,p,n,d)-CB
            st=max(st,abs(fa-fb))
            PA=A[:,T]@np.linalg.pinv(A[:,T]); PB=B[:,T]@np.linalg.pinv(B[:,T]); pd=max(pd,np.linalg.norm(PA-PB,2))
            T2=[i for i in T if i!=0]  # truth-out set
            tout=max(tout,abs((coord_score(A,yA,T2,p,n,d)-CA)-(coord_score(B,yB,T2,p,n,d)-CB)))
        scale=e*(z@z+1)+p/n+1/n
        sc.append(dict(p=p,n=n,e=float(e),e_times_sqrt_n_over_p=float(e*math.sqrt(n)/p),
                       e_times_sqrt_n_over_sqrtp=float(e*math.sqrt(n/p)),
                       ST=float(st),ST_over_scale=float(st/scale),projdiff_over_e=float(pd/e),
                       truthout_disc=float(tout),truthout_over_ne=float(tout/(n*e))))
out['scaling']=sc
json.dump(out,open('R04_l4_checks_out.json','w'),indent=1)
print(json.dumps(out,indent=1))
