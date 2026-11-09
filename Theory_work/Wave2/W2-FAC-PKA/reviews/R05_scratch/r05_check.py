# R05 midpoint reviewer scratch: (A) closed-form CS score vs direct matrix score on a real X;
# (B) LS0 path simulation on exact-CS sufficient statistics, singleton partition, rho=1/2, sigma=1.
import numpy as np, math, json, sys
from scipy.special import gammaln
rng0 = np.random.default_rng(12345)
def lchoose(a,k): return gammaln(a+1)-gammaln(k+1)-gammaln(a-k+1)
# ---------- (A) direct check ----------
def direct_F(X,y,U,p):
    n=len(y); h=n-1
    if len(U)==0: Q=y@y; ld=0.0
    else:
        XU=X[:,U]; G=XU.T@XU; z=XU.T@y; H=(n+1)*G+np.eye(len(U))
        Q=y@y-n*z@np.linalg.solve(H,z); ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(U)))[1]
    nu=.01+n/2; lw=-math.log(2)-lchoose(2*p-1,len(U))
    return lw-.5*ld-nu*math.log(.02+Q)
def cs_consts(n):
    h=n-1; al=(n*n-1)/2+1; be=(n*n-1)/2; alp=h/2+1; bep=h/2
    return h,al,be,alp,bep
def closed_F(z,h,n,p,U):
    _,al,be,alp,bep=cs_consts(n); k=len(U); nu=.01+n/2
    lw=-math.log(2)-lchoose(2*p-1,k)
    if k==0: return lw-nu*math.log(.02+h)
    g=be/(al+k*be); zz=z[U]; quad=(zz@zz-g*zz.sum()**2)/al
    L=(k-1)*math.log(al/alp)+math.log((al+k*be)/(alp+k*bep))
    return lw-.5*L-nu*math.log(.02+h-n*quad)
n,p,rho=40,28,.5
A=rng0.standard_normal((n,n)); A-=A.mean(0); Qm,_=np.linalg.qr(A); Qm=Qm[:,:p]
Qm-=Qm.mean(0); Qm,_=np.linalg.qr(Qm)  # columns orthonormal in 1-perp
Sig=(1-rho)*np.eye(p)+rho*np.ones((p,p)); w,V=np.linalg.eigh(Sig); R=V@np.diag(np.sqrt(w))@V.T
X=math.sqrt(n-1)*Qm@R
th=np.zeros(p); th[:2]=1; Y=X@th+(np.eye(n)-np.ones((n,n))/n)@rng0.standard_normal(n); y=Y/math.sqrt(Y@Y/(n-1))
z=X.T@y; maxerr=0
for _ in range(200):
    k=rng0.integers(0,15); U=sorted(rng0.choice(p,k,replace=False).tolist())
    maxerr=max(maxerr,abs(direct_F(X,y,U,p)-closed_F(z,n-1,n,p,U)))
print("A: max |direct-closed| F =",maxerr, " max|1'X|=",np.abs(X.sum(0)).max()," Gram err=",np.abs(X.T@X-(n-1)*Sig).max())
# ---------- (B) LS0 simulation ----------
def ls0(n,c,s0,seed,cap_extra=0,Lcheck=None):
    rng=np.random.default_rng(seed); p=int(math.floor(c*n)); K=n//2; h,al,be,alp,bep=cs_consts(n); nu=.01+n/2
    eta=rng.standard_normal(); xi=rng.standard_normal(p); g=(eta+xi)/math.sqrt(2)
    th=np.zeros(p); th[:s0]=1; Sth=.5*th+.5*th.sum()
    # ||e||^2 = g' Sigma^-1 g + chi2_{n-1-p}
    Sinv_g = 2*(g - (.5*g.sum())/(.5+.5*p))   # Sigma^-1 = (1/(1-rho))(I - rho/(1-rho+p rho) J)
    e2 = g@Sinv_g + rng.chisquare(n-1-p)
    Y2 = h*th@Sth + 2*math.sqrt(h)*th@g + e2; s=math.sqrt(Y2/h)
    z=(h*Sth+math.sqrt(h)*g)/s
    lw=np.array([-math.log(2)-lchoose(2*p-1,k) for k in range(K+2)])
    def Lk(k): return 0.0 if k==0 else (k-1)*math.log(al/alp)+math.log((al+k*be)/(alp+k*bep))
    LK=np.array([Lk(k) for k in range(K+2)])
    def F_of(k,S1,S2):
        g_=be/(al+k*be) if k>0 else 0; quad=(S2-g_*S1*S1)/al
        return lw[k]-.5*LK[k]-nu*np.log(.02+h-n*quad)
    # start: top K by z^2 (singleton blocks, verified size K by score monotonicity below)
    order=np.argsort(-z*z); inT=np.zeros(p,bool); inT[order[:K]]=True
    truth_in=inT[:s0].all()
    ell=math.ceil(math.log2(n+p+1)); a=ell+K+cap_extra
    moves=[]; minsize=K; found=False; m=0
    while True:
        T=np.where(inT)[0]; O=np.where(~inT)[0]; k=len(T); S1=z[T].sum(); S2=(z[T]**2).sum(); Fc=F_of(k,S1,S2)
        # discovery check: S0 is centre or neighbour?
        S0=set(range(s0)); Ts=set(T.tolist()); sd=len(Ts^S0)
        if sd==0 or (sd==1) or (sd==2 and k==s0): found=True
        minsize=min(minsize,k)
        best=-np.inf; bm=None
        # deletions
        Fd=F_of(k-1,S1-z[T],S2-z[T]**2); i=np.argmax(Fd)
        if Fd[i]>best: best=Fd[i]; bm=('del',T[i],None)
        if k<K:
            Fa=F_of(k+1,S1+z[O],S2+z[O]**2); i=np.argmax(Fa)
            if Fa[i]>best: best=Fa[i]; bm=('add',None,O[i])
        S1s=S1-z[T][:,None]+z[O][None,:]; S2s=S2-(z[T]**2)[:,None]+(z[O]**2)[None,:]
        Fs=F_of(k,S1s,S2s); ij=np.unravel_index(np.argmax(Fs),Fs.shape)
        if Fs[ij]>best: best=Fs[ij]; bm=('swap',T[ij[0]],O[ij[1]])
        if not best>Fc: break
        if m>=a: break
        typ,j,l=bm
        kind=typ
        if typ=='swap': kind='swap_'+('T' if j<s0 else 'N')+('T' if l<s0 else 'N')
        if typ=='del': kind='del_'+('T' if j<s0 else 'N')
        moves.append(kind)
        if j is not None: inT[j]=False
        if l is not None: inT[l]=True
        m+=1
    L0=ell+s0+2
    first=moves[:L0]
    return dict(n=n,p=p,s0=s0,seed=seed,truth_in_start=bool(truth_in),ell=ell,cap=a,moves=m,
                first_L0_all_NN=all(x=='swap_NN' for x in first) and len(first)==L0,
                n_swapNN=sum(x=='swap_NN' for x in moves), n_del=sum(x.startswith('del') for x in moves),
                first_nonNN=next((i for i,x in enumerate(moves) if x!='swap_NN'),None),
                minsize=minsize, S0_found=found, last_kinds=moves[-3:])
out=[]
for n in [200,800,2000]:
    for s0 in [1,2]:
        for seed in range(4 if n<2000 else 2):
            r=ls0(n,.75,s0,seed); out.append(r); print(json.dumps(r)); sys.stdout.flush()
json.dump(out,open('r05_out.json','w'),indent=1)
