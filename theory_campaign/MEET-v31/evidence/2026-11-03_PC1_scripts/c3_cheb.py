import numpy as np
rng=np.random.default_rng(20261104)
# W lognormal mean 1, H dependent on W; mu = E[W H]
for s,R,eps in [(0.5,2000,0.1),(1.0,400,0.5),(0.8,300,0.4)]:
    reps=4000
    W=rng.lognormal(-s*s/2,s,(reps,R)); U=rng.random((reps,R))
    H=(U< 1/(1+W)).astype(float)   # H in {0,1}, correlated with W
    M=np.exp(s*s); 
    Wb=rng.lognormal(-s*s/2,s,4_000_000); mu=np.mean(Wb/(1+Wb))   # E[W*P(H=1|W)]
    muhat=(W*H).sum(1)/W.sum(1)
    emp=np.mean(np.abs(muhat-mu)>eps)
    bound=min(1,4*(M-1)/R+4*M/(R*eps**2))
    Y=Wb*((rng.random(Wb.size)<1/(1+Wb))-mu); 
    print(f"s={s} R={R} eps={eps}: M={M:.3f} EY^2={np.mean(Y**2):.3f}<=M:{np.mean(Y**2)<=M} P_emp={emp:.4f} bound={bound:.4f} ok={emp<=bound}")
