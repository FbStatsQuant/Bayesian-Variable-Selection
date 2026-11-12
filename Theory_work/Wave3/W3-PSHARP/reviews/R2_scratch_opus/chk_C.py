# Independent check of Proposition C item 2 constants and Lemma P / Step 1 bounds.
import math, numpy as np, itertools
from mpmath import mp, mpf, binomial, log as mlog, sqrt as msqrt
mp.dps = 50
def lchoose(a,k): return math.lgamma(a+1)-math.lgamma(k+1)-math.lgamma(a-k+1)
worst = 0; worstA = 0; worstD = 0
ns = list(range(200, 20001)) + [int(10**e) for e in np.linspace(4.31, 9, 400)]
for n in ns:
    k = math.ceil(12*math.log(n)); p = k+2; K = min(p, n//2); assert K == p and k+1 <= n-1
    mn = k//2
    # tail via mpmath exact rational-ish
    q = [mpf(1)/2*binomial(p,j)/binomial(2*p-1,j) for j in range(p+1)]
    R = sum(q[mn+1:K+1]) * 2*binomial(2*p-1,2)
    eta = mpf(n)**-2; c2 = 1/(1+eta**2*k)
    trG = 2*(n-1); detG = (n-1)**2*(1-c2)
    DT = (1+(n+1)*trG+(n+1)**2*detG)/(1+trG+detG)
    A = R*msqrt(DT)*msqrt(n)
    worst = max(worst, float(R*n*n)); worstD = max(worstD, float(DT/(2*n))); worstA = max(worstA, float(A*msqrt(n)))
print("max n^2 R_{m_n} =", worst, " max D_T/(2n) =", worstD, " max A*sqrt(n) =", worstA)
# Step 4/5 numeric constants for all n>=200 (L decreasing terms) - check inequalities at grid
bad=0
for n in ns:
    L=math.log(n); k=math.ceil(12*L); p=k+2
    lhs=(3*p-1)*math.log(2)+(k/2)*L
    if lhs>12*L*L: bad+=1
    if 4*(k+1) > 48*L+8+1e-9: bad+=1
print("step5/4 violations:", bad)
# Lemma P exact check on small instance: min over theta of ||mu - X_S th||^2 + th2^2/n vs bound
rng=np.random.default_rng(1)
for (n,k) in [(30,6),(50,8),(200,10)]:
    eta=n**-2.0; c=1/math.sqrt(1+eta*eta*k)
    M=rng.standard_normal((n,k+1)); M-=M.mean(0); Qm,_=np.linalg.qr(M)
    Xo=math.sqrt(n-1)*Qm; x1=Xo[:,0]; XT=Xo[:,1:]; u=XT.sum(1)
    x2=c*(x1-eta*u); X=np.column_stack([x1,x2,XT]); b=0.7; mu=b/math.sqrt(k)*u
    worst_ratio=np.inf; worst_step1=np.inf
    for size in range(0,k//2+1):
        for S in itertools.combinations(range(k+2),size):
            S=list(S); d=len([j for j in range(2,k+2) if j not in S])
            if d<1: continue
            if not S:
                val=mu@mu; val1=val
            else:
                XS=X[:,S]; W=np.zeros(len(S)); 
                if 1 in S: W[S.index(1)]=1/n
                th=np.linalg.solve(XS.T@XS+np.diag(W)+1e-300*np.eye(len(S)), XS.T@mu)
                val=np.sum((mu-XS@th)**2)+ (th[S.index(1)]**2/n if 1 in S else 0)
                th1=np.linalg.solve(XS.T@XS+np.eye(len(S))/n, XS.T@mu)
                val1=np.sum((mu-XS@th1)**2)+th1@th1/n
            bound=(n-1)*d*(b*b/k)/(1+n*(n-1)*d*c*c*eta*eta)
            worst_ratio=min(worst_ratio,val/bound)
            if size<=k//2: worst_step1=min(worst_step1,val1/((n-1)*b*b/4))
    print(f"n={n} k={k}: min LemmaP value/bound={worst_ratio:.6f}; min L_S/((n-1)b^2/4) over |S|<=k/2: {worst_step1:.4f}")
