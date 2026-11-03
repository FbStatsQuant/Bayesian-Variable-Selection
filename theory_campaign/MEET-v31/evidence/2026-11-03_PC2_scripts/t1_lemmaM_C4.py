# Lemma M (a)(b)(d) on random chains; C4 box bounds Phi >= F and M >= log-sum on all boxes (p=8) / random boxes (p<=12).
import numpy as np, itertools, math, sys
sys.path.insert(0, __file__.rsplit('/',1)[0]); from pc2_common import *
rng=np.random.default_rng(20261103)
def design(n,p,kind):
    if kind=='indep': Xr=rng.standard_normal((n,p))
    elif kind=='corr': Z=rng.standard_normal((n,1)); Xr=0.9*Z+0.45*rng.standard_normal((n,p))
    yr=Xr[:,:3]@np.array([1.,-.8,.6])+rng.standard_normal(n)
    return std(Xr,yr)
worstM=worstD=worstQ=worstPhi=worstMass=0; nchk=0
for (n,p,kind) in [(20,8,'indep'),(30,8,'corr'),(8,12,'indep'),(10,12,'corr'),(40,12,'corr'),(15,10,'indep')]:
    X,y=design(n,p,kind); T=Target(X,y)
    # Lemma M(d): closed forms
    for _ in range(200):
        S=sorted(rng.choice(p,rng.integers(0,p+1),replace=False)); k=len(S)
        Q,lD=QD(X,y,S); M=X[:,S]@X[:,S].T if k else np.zeros((n,n))
        Qd=y@y/(n+1)+(n/(n+1))*y@np.linalg.solve(np.eye(n)+(n+1)*M,y)
        lDd=np.linalg.slogdet(np.eye(n)+(n+1)*M)[1]-np.linalg.slogdet(np.eye(n)+M)[1]
        worstM=max(worstM,abs(Q-Qd)/max(1,abs(Q)),abs(lD-lDd))
        # chain S subset S' : Q decreasing, D increasing (unrestricted |S'|, p>n allowed)
        extra=[j for j in range(p) if j not in S]
        if extra:
            S2=sorted(S+list(rng.choice(extra,rng.integers(1,len(extra)+1),replace=False)))
            Q2,lD2=QD(X,y,S2); worstQ=max(worstQ,Q2-Q); worstD=max(worstD,lD-lD2)
    # C4: boxes
    Fall=T.enum()
    if p<=8:
        boxes=[]
        for lab in itertools.product(range(3),repeat=p):   # 0 out, 1 free, 2 in L
            L=tuple(j for j in range(p) if lab[j]==2); U=tuple(j for j in range(p) if lab[j]>=1); boxes.append((L,U))
    else:
        boxes=[]
        for _ in range(4000):
            lab=rng.integers(0,3,p); L=tuple(j for j in range(p) if lab[j]==2); U=tuple(j for j in range(p) if lab[j]>=1); boxes.append((L,U))
    for L,U in boxes:
        if len(L)>T.K: continue
        free=[j for j in U if j not in L]
        mem=[tuple(sorted(L+c)) for r in range(0,min(len(free),T.K-len(L))+1) for c in itertools.combinations(free,r)]
        Fm=[Fall[S] for S in mem]
        worstPhi=max(worstPhi,max(Fm)-T.Phi(L,U)); worstMass=max(worstMass,lse(Fm)-T.M(L,U)); nchk+=1
print(f"Lemma M(d) closed-form max abs err {worstM:.2e}")
print(f"Lemma M(a) max increase of Q along chains {worstQ:.2e} (<=0 expected up to rounding)")
print(f"Lemma M(b) max decrease of log D along chains {worstD:.2e} (<=0 expected)")
print(f"C4: {nchk} boxes; max F - Phi = {worstPhi:.3e}; max logsum - M = {worstMass:.3e} (<=0 expected)")
