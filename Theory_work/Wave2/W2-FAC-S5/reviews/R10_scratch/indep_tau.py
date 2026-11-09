# R10: independent check of L1.3 identity tau = (sqrt(psi)A + a_u e_R)/sqrt(psi + a_u^2 V_R), V_R formula, and bound.
import numpy as np
rng=np.random.default_rng(7); worst=0; worstV=0; viol=0
for trial in range(300):
    rb,rw=sorted(rng.uniform(.05,.95,2)); b=rw-rb; d=1-rw
    sizes=rng.integers(1,6,rng.integers(2,7)); grp=np.repeat(np.arange(len(sizes)),sizes); p=len(grp)
    Sig=rb+np.where(grp[:,None]==grp[None,:],b,0)+d*np.eye(p)
    h=np.sqrt(rb)*rng.standard_normal(); y=np.sqrt(b)*rng.standard_normal(len(sizes))[grp]+np.sqrt(d)*rng.standard_normal(p); g=h+y
    R=[i for i in range(p) if rng.random()<.5]; outs=[i for i in range(p) if i not in R]
    if not outs: continue
    l=outs[0]
    if R:
        beta=np.linalg.solve(Sig[np.ix_(R,R)],Sig[R,l]); v=Sig[l,l]-Sig[l,R]@beta; tau=(g[l]-beta@g[R])/np.sqrt(v)
        e=h-rb*np.ones(len(R))@np.linalg.solve(Sig[np.ix_(R,R)],g[R]); Vn=rb-rb*rb*np.ones(len(R))@np.linalg.solve(Sig[np.ix_(R,R)],np.ones(len(R)))
    else: v=1; tau=g[l]; e=h; Vn=rb
    U=[j for j in R if grp[j]==grp[l]]; u=len(U)
    au=d/(d+u*b); psi=d*(d+(u+1)*b)/(d+u*b); A=(y[l]-b*y[U].sum()/(d+u*b))/np.sqrt(psi)
    ug=np.bincount(grp[R],minlength=len(sizes)) if R else np.zeros(len(sizes))
    V=1/(1/rb+sum(x/(d+b*x) for x in ug))
    tau2=(np.sqrt(psi)*A+au*e)/np.sqrt(psi+au**2*V)
    worst=max(worst,abs(tau-tau2)); worstV=max(worstV,abs(V-Vn))
    if abs(tau)>abs(A)+(1-rb)**-.5*abs(e)+1e-12: viol+=1
print("max |tau - identity| =",worst," max |V - V_formula| =",worstV," bound violations =",viol)
