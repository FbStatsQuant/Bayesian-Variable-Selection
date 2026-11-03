# Engine-faithful double scorer (v3_score.h: naive-loop Gram, Cholesky of H and A, forward solve, Q by subtraction,
# eta(S) heuristic of v3_score.h:242-246) versus the exact score of the same double data (Fractions + 60-digit Decimal).
# Compares only the data-dependent part of log m (log C_n is common), against eta minus its |log C_n| term.
import numpy as np, math, sys
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec=60
rng=np.random.default_rng(20261108); a0=b0=0.01; eps=np.finfo(float).eps
def dot(a,b):
    s=0.0
    for i in range(len(a)): s+=a[i]*b[i]
    return s
def chol(A,k):
    L=[[0.0]*k for _ in range(k)]
    for j in range(k):
        s=A[j][j]-sum(L[j][m]*L[j][m] for m in range(j))
        if s<=0: return None
        L[j][j]=math.sqrt(s)
        for i in range(j+1,k): L[i][j]=(A[i][j]-sum(L[i][m]*L[j][m] for m in range(j)))/L[j][j]
    return L
def engine(X,y,S):
    n=len(y); k=len(S); nu=a0+n/2; cols=[list(X[:,j]) for j in S]; yl=list(y)
    G=[[dot(cols[a],cols[b]) for b in range(k)] for a in range(k)]; z=[dot(cols[a],yl) for a in range(k)]; yty=dot(yl,yl)
    H=[[(n+1)*G[a][b]+(a==b) for b in range(k)] for a in range(k)]; A=[[G[a][b]+(a==b) for b in range(k)] for a in range(k)]
    LH=chol(H,k); LA=chol(A,k)
    ldH=2*sum(math.log(LH[a][a]) for a in range(k)); ldA=2*sum(math.log(LA[a][a]) for a in range(k))
    w=[0.0]*k
    for a in range(k): w[a]=(z[a]-sum(LH[a][m]*w[m] for m in range(a)))/LH[a][a]
    quad=sum(v*v for v in w); Q=yty-n*quad
    dH=[LH[a][a] for a in range(k)]; dA=[LA[a][a] for a in range(k)]
    cH=(max(dH)/min(dH))**2; cA=(max(dA)/min(dA))**2
    val=-0.5*(ldH-ldA)-nu*math.log(2*b0+Q)
    eta_noC=64*eps*(nu*(yty/Q)*(1+k*cH)+k*(cH+cA)+nu*abs(math.log(2*b0+Q)))
    return val,eta_noC
def det_fr(M):
    M=[r[:] for r in M]; k=len(M); d=Fr(1)
    for c in range(k):
        piv=next(r for r in range(c,k) if M[r][c]!=0)
        if piv!=c: M[c],M[piv]=M[piv],M[c]; d=-d
        d*=M[c][c]
        for r in range(c+1,k):
            f=M[r][c]/M[c][c]
            for cc in range(c,k): M[r][cc]-=f*M[c][cc]
    return d
def solve_fr(M,b):
    k=len(M); A=[M[i][:]+[b[i]] for i in range(k)]
    for c in range(k):
        for r in range(c+1,k):
            f=A[r][c]/A[c][c]
            for cc in range(c,k+1): A[r][cc]-=f*A[c][cc]
    x=[Fr(0)]*k
    for i in reversed(range(k)): x[i]=(A[i][k]-sum(A[i][j]*x[j] for j in range(i+1,k)))/A[i][i]
    return x
def lnF(q): return Decimal(q.numerator).ln()-Decimal(q.denominator).ln()
def exact(X,y,S):
    n=len(y); k=len(S); nu=Fr(a0)+Fr(n,2)
    cols=[[Fr(v) for v in X[:,j]] for j in S]; yl=[Fr(v) for v in y]
    G=[[sum(p*q for p,q in zip(cols[a],cols[b])) for b in range(k)] for a in range(k)]
    z=[sum(p*q for p,q in zip(cols[a],yl)) for a in range(k)]; yty=sum(v*v for v in yl)
    H=[[(n+1)*G[a][b]+(a==b) for b in range(k)] for a in range(k)]; A=[[G[a][b]+(a==b) for b in range(k)] for a in range(k)]
    Q=yty-n*sum(zi*xi for zi,xi in zip(z,solve_fr(H,z)))
    return float(-Decimal(1)/2*(lnF(det_fr(H))-lnF(det_fr(A)))-Decimal(nu.numerator)/Decimal(nu.denominator)*lnF(Fr(2*b0)+Q))
worst=(0,None); rows=[]
for t in range(60):
    n=int(rng.choice([20,50,200,1000])); k=int(rng.integers(1,4)); kind=t%3
    Xr=rng.standard_normal((n,k))
    if kind==1: Xr[:,1:]=Xr[:,:1]+1e-6*rng.standard_normal((n,k-1)) if k>1 else Xr
    if kind==2: Xr=Xr+1e3   # large common offset before centring
    yr=Xr.sum(1)+10**rng.uniform(-4,0)*rng.standard_normal(n)
    X=Xr-Xr.mean(0); X=X/np.sqrt((X**2).sum(0)/(n-1)); y=yr-yr.mean(); y=y/np.sqrt((y**2).sum()/(n-1))
    S=list(range(k)); v,eta=engine(X,y,S); e=exact(X,y,S); r=abs(v-e)/eta
    if r>worst[0]: worst=(r,(n,k,kind,abs(v-e),eta))
print("max |engine - exact| / eta (data part) = %.3g at (n,k,kind,|err|,eta)=%s"%(worst[0],worst[1]))
