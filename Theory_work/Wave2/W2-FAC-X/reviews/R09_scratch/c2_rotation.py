# R09: explicit-row check of X1.1-X1.4 (independent of iid_core)
import numpy as np, math
from scipy.special import gammaln
rng=np.random.default_rng(7)
n,p,rho,sig=300,25,0.6,1.3
S0=[3,11]; beta=np.zeros(p); beta[S0]=[1.0,-0.7]
F=rng.standard_normal(n); U=rng.standard_normal((n,p)); eps=sig*rng.standard_normal(n)
m=rng.standard_normal(p)*5
Xr=m+np.sqrt(rho)*F[:,None]+np.sqrt(1-rho)*U
yr=2.0+Xr@beta+eps
C=np.eye(n)-np.ones((n,n))/n
g=C@Xr; e=C@eps; f=C@F; u=C@U
e1=e/np.linalg.norm(e); eta=f@e1; fp=f-eta*e1; phi=np.linalg.norm(fp); e2=fp/phi
xi=u.T@e1; a=u.T@e2; up=u-np.outer(e1,xi)-np.outer(e2,a)
W=up.T@up; N=n-3; ell=math.sqrt(rho/(1-rho))
v1t=xi+ell*eta; v2t=ell*phi+a
# check g decomposition
print("g decomp err", np.abs(g-(np.outer(e1,math.sqrt(1-rho)*v1t)+np.outer(e2,math.sqrt(1-rho)*v2t)+math.sqrt(1-rho)*up)).max())
def rss(T):
    Gt=g[:,T]; P=Gt@np.linalg.solve(Gt.T@Gt,Gt.T); Y=C@yr; r=Y-P@Y; return r@r
def qT(T):
    A=W[np.ix_(T,T)]+np.outer(v2t[T],v2t[T]); return v1t[T]@np.linalg.solve(A,v1t[T]), A
T=sorted(set(range(p))-{0,5,7})
q,A=qT(T)
print("RSS rel err", rss(T)/(e@e/(1+q))-1)
# X1.2(b) omega and tau-hat, x_T
kap=N/(ell**2*phi**2); vr=N*eta/(ell*phi**2); k=len(T)
xT=(xi[T].sum()-vr)/(k+kap); gk=1/(k+kap)
Ai=np.linalg.inv(A); om=(Ai@v1t[T])/np.sqrt(np.diag(Ai))
tauhat=math.sqrt(N)*math.sqrt(1-gk)*om; tau=xi[T]-xT
print("max|delta|",np.abs(tauhat-tau).max(), " Hbar*sqrt(p log n/n)",math.sqrt(2*math.log(2*(p-2)+2)+2*math.log(math.log(n)))*math.sqrt(p*math.log(n)/n))
# Schur: q_T - q_{T\j} = omega^2
j=4; Tj=[t for t in T if t!=T[j]]
print("Schur err",(q-qT(Tj)[0])-om[j]**2)
# method score and deletion gain (g3)
sd=np.sqrt((g**2).sum(0)/(n-1)); X=g/sd; Y=C@yr; s=math.sqrt(Y@Y/(n-1)); y=Y/s
K=min(p,n//2); nu=0.01+n/2
def logw(k): return -math.log(2)-(gammaln(2*p)-gammaln(k+1)-gammaln(2*p-k))
def Fs(T):
    G=X[:,T].T@X[:,T]; z=X[:,T].T@y; H=(n+1)*G+np.eye(len(T))
    Q=(n-1)-n*z@np.linalg.solve(H,z)
    return logw(len(T))-0.5*(np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1])-nu*math.log(0.02+Q), Q
FT,QT=Fs(T); FTj,QTj=Fs(Tj)
psi=0.02+QT; ee=e@e
MT=nu*(n/(n+1))*(ee/s**2)/(N*(1+q)**2*psi)
qj=q-om[j]**2; epsd=(1+q)/(1+qj)-1
Dk=math.log((2*p-k)/k)+0.5*math.log(n+1)
# e1 term
G=X[:,T].T@X[:,T]; H=(n+1)*G+np.eye(k)
e1j=(math.log(np.linalg.inv(H)[j,j])-math.log(np.linalg.inv(G+np.eye(k))[j,j]))+math.log(n+1)
gk1=1/(k-1+kap)
approx=Dk-0.5*e1j-nu*math.log(1+(1+gk1)*MT*(1+epsd)*tauhat[j]**2/nu)
print("G_del exact",FTj-FT," (g3) w/o r_j",approx," M_T",MT)
