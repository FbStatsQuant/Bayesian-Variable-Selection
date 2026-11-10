# R02 scratch: (1) code formula vs contrast identity (n vs n-1, IG 0.51); (2) den' / L1a' deterministic lower bound
# by numerical integration; (3) L1a' Q bound; (4) (B3)+(B1) superset bound of (C4) under SE_w only; (5) lem:spec(e).
import numpy as np
from scipy import integrate, special, stats
rng=np.random.default_rng(7)
def stdz(Xr):
    Xc=Xr-Xr.mean(0); return Xc/np.sqrt((Xc**2).sum(0)/(Xr.shape[0]-1))
def score_code(X,y,S):  # log m(S) up to S-free constant, exactly as v3_score.h
    n=len(y); a0=b0=0.01; nu=a0+n/2
    if len(S)==0: return -nu*np.log(2*b0+y@y)
    XS=X[:,S]; G=XS.T@XS; H=(n+1)*G+np.eye(len(S)); A=G+np.eye(len(S)); z=XS.T@y
    Q=y@y-n*z@np.linalg.solve(H,z)
    return -0.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(A)[1])-nu*np.log(2*b0+Q)
def U_of(n):
    C=np.eye(n)-1/n; w,V=np.linalg.eigh(C); return V[:,w>0.5]
def logmc(Xc,yc,S,b,n):  # log m^c_b(S) from P1 eq (mc), contrast space dim n-1
    nu=0.01+n/2
    if len(S)==0: D=1.0; Q=yc@yc
    else:
        XS=Xc[:,S]; G=XS.T@XS; H=(n+1)*G+np.eye(len(S)); z=XS.T@yc
        D=np.exp(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(S)))[1]); Q=yc@yc-n*z@np.linalg.solve(H,z)
    return -(n-1)/2*np.log(2*np.pi)+0.51*np.log(b)+special.gammaln(nu)-special.gammaln(0.51)-0.5*np.log(D)-nu*np.log(b+Q/2)
from itertools import combinations
worst={}
# (1) identity
n,p=15,5; Xr=rng.normal(size=(n,p)); Xr[:,4]=Xr[:,3]+1e-3*rng.normal(size=n)
yr=2+Xr[:,0]*1.3+rng.normal(size=n); X=stdz(Xr); sy=np.sqrt(((yr-yr.mean())**2).sum()/(n-1)); y=(yr-yr.mean())/sy
U=U_of(n); Xc=U.T@X; yc=U.T@yr; b=0.01*sy**2
mods=[list(c) for k in range(0,n//2+1) for c in combinations(range(p),k) if k<=min(p,n//2)]
d=[score_code(X,y,S)-logmc(Xc,yc,S,b,n) for S in mods]
worst['identity spread (should be 0)']=max(d)-min(d)
# (2)-(3): den' lower bound with arbitrary representation T,theta; random designs incl. near-collinear T
def den_check(n,sig2,M,X,T,theta,trials=30):
    mu=X[:,T]@theta; assert (mu@mu)<=n*M+1e-9
    bp=0.01*(2*(sig2+M)+1); cIG=min(stats.invgamma.pdf(v,0.51,scale=bp) for v in np.linspace(sig2,2*sig2,2001))
    U=U_of(n); Xc=U.T@X; worstr=np.inf; worstQ=-np.inf
    for _ in range(trials):
        e=rng.normal(scale=np.sqrt(sig2),size=n); ec=U.T@e; yc=U.T@mu+ec
        XT=Xc[:,T]; G=XT.T@XT; H=(n+1)*G+np.eye(len(T)); z=XT.T@yc; Q=yc@yc-n*z@np.linalg.solve(H,z)
        rho=(mu@mu+theta@theta)/n; E=ec@ec/sig2
        worstQ=max(worstQ,Q-(sig2*E+rho))
        D=np.exp(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1])
        f=lambda v: np.exp(-(n-1)/2*np.log(v/sig2)+E/2-Q/(2*v))*stats.invgamma.pdf(v,0.51,scale=bp)
        I=integrate.quad(f,1e-8,50*sig2+50,limit=400,points=[sig2,2*sig2])[0]/np.sqrt(D)
        Lam=abs(E-(n-1))/(2*np.sqrt(n))+E/(2*n)+rho/(2*sig2)
        lb=D**-0.5*cIG*sig2*n**-0.5*np.exp(-Lam)
        worstr=min(worstr,I/lb)
    return worstr,worstQ
for (n,eta,L) in [(20,1e-2,3.0),(40,1e-4,30.0),(60,1e-6,300.0)]:
    Z=rng.normal(size=(n,3)); Xr=np.c_[Z[:,0],Z[:,0]+np.sqrt(eta)*Z[:,1],Z[:,2]]; X=stdz(Xr)
    th=np.array([L,-L]); mu=X[:,[0,1]]@th; M=(mu@mu)/n*1.0001
    r,q=den_check(n,1.0,M,X,[0,1],th)
    worst[f'den ratio min (>=1 ok) n={n} eta={eta}']=r; worst[f'L1a Q-bound max excess (<=0 ok) n={n}']=q
# (4) (C4) ingredients with SE_w only: near-singular superset S0∪J (lambda_min(G)=g0 small, fixed)
def c4_check(n,g0target,trials=200):
    Z=rng.normal(size=(n,6)); X=stdz(Z)
    # make col5 nearly a combination of cols 1..4 so that lambda_min(G_{S0∪J}) ~ g0 (unnormalised)
    comb=X[:,1:5].sum(1); comb/=np.linalg.norm(comb); r=rng.normal(size=n); r-=r.mean()
    r-=X[:,:5]@np.linalg.lstsq(X[:,:5],r,rcond=None)[0]; r/=np.linalg.norm(r)
    v=comb*np.sqrt(n-1)+np.sqrt(g0target)*r*3; X[:,5]=v/np.linalg.norm(v)*np.sqrt(n-1)
    S0=[0]; J=[1,2,3,4,5]; S=S0+J; G=X[:,S].T@X[:,S]; g0=np.linalg.eigvalsh(G).min()
    phi2=np.linalg.eigvalsh(X[:,S0].T@X[:,S0]/(n-1)).min(); N=n-1; eta=1/((n+1)*N*phi2)
    U=U_of(n); Xc=U.T@X
    def DQ(T,yc):
        XT=Xc[:,T]; G=XT.T@XT; H=(n+1)*G+np.eye(len(T)); z=XT.T@yc
        return np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1], yc@yc-n*z@np.linalg.solve(H,z)
    ldS0,_=DQ(S0,Xc[:,0]); ldS,_=DQ(S,Xc[:,0])
    detgap=(ldS-ldS0)-len(J)*np.log((n+1)/(1+1/g0))  # must be >=0 (B1)
    worstB3=-np.inf
    def P(T):
        Qm,_=np.linalg.qr(Xc[:,T]); return Qm@Qm.T
    PS,PS0=P(S),P(S0)
    for _ in range(trials):
        yc=Xc[:,0]*rng.normal()*3+rng.normal(size=n-1)
        _,QS0=DQ(S0,yc); _,QS=DQ(S,yc); dt=QS0-QS
        bound=n/(n+1)*(yc@(PS-PS0)@yc+eta*yc@PS0@yc)
        worstB3=max(worstB3,dt-bound)
    return g0,detgap,worstB3
for n in [30,100,400]:
    g0,dg,b3=c4_check(n,0.5)
    worst[f'C4 n={n}: g0={g0:.3f} detgap(>=0) ']=dg; worst[f'C4 n={n}: (B3) excess (<=0)']=b3
for k,v in worst.items(): print(f'{k}: {v:.6g}')
