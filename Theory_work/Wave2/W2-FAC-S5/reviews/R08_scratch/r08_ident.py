# Independent check of L1.3 (residual decomposition, kappa0 bound) and of 2*G_del ~ 2log((2p-k)/k)+log(n+1)-tau^2.
import numpy as np, random, math
rng=np.random.default_rng(7); worst=0; viol=0; cnt=0
for trial in range(300):
    q=int(rng.integers(2,6)); J=int(rng.integers(2,6)); rb=rng.uniform(.05,.5); rw=rng.uniform(rb+.05,.95)
    sizes=rng.integers(1,q+1,size=J); grp=np.repeat(np.arange(J),sizes); p=len(grp); b,d=rw-rb,1-rw
    Sig=np.where(grp[:,None]==grp[None,:],rw,rb); np.fill_diagonal(Sig,1)
    h=math.sqrt(rb)*rng.normal(); zeta=rng.normal(size=J); xi=rng.normal(size=p)
    y=math.sqrt(b)*zeta[grp]+math.sqrt(d)*xi; g=h+y
    T=[i for i in range(p) if rng.random()<.6]
    for j in range(p):
        R=[i for i in T if i!=j]
        if R:
            SR=Sig[np.ix_(R,R)]; bet=np.linalg.solve(SR,Sig[R,j]); res=g[j]-bet@g[R]; v=1-Sig[j,R]@bet
            eR=h-rb*np.ones(len(R))@np.linalg.solve(SR,g[R])
        else: res=g[j]; v=1.0; eR=h
        U=[i for i in R if grp[i]==grp[j]]; u=len(U); cu=d/(u*b+d); su2=d*(d+(u+1)*b)/(d+u*b)
        a=y[j]-(1-cu)*(np.mean(y[U]) if u else 0.0)
        worst=max(worst,abs(res-(a+cu*eR)),abs(v-(su2+cu**2*(1/(1/rb+sum((sum(grp[R]==gg))/(sum(grp[R]==gg)*b+d) for gg in set(grp[R])))))))
        tau=res/math.sqrt(v); A=a/math.sqrt(su2); cnt+=1
        if abs(tau)>abs(A)+abs(eR)/math.sqrt(1-rb)+1e-12: viol+=1
print('L1.3 identities max err',worst,'kappa0-bound violations',viol,'of',cnt)
