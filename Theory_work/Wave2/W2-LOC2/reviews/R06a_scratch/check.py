import numpy as np
rng=np.random.default_rng(0)
def make(p,alpha,first=0.4,signs=False):
    d=np.abs(np.subtract.outer(np.arange(p),np.arange(p)))
    K=first*2**alpha
    S=K*(1.0+d)**(-alpha); np.fill_diagonal(S,1.0)
    if signs:
        sg=rng.choice([-1,1],size=(p,p)); sg=np.triu(sg,1); sg=sg+sg.T+np.eye(p)
        S=S*sg
    return S,d,K
for alpha in [2.5,3.0,5.0,8.6]:
  for signs in [False,True]:
    p=600
    S,d,K=make(p,alpha,signs=signs)
    ev=np.linalg.eigvalsh(S)
    Si=np.linalg.inv(S)
    # max |inv| at distance dd, central rows
    out=[]
    for dd in [4,8,16,32,64,128]:
        i=np.arange(100,p-200); v=np.abs(Si[i,i+dd]).max()
        out.append(v*(1+dd)**alpha)
    # slope
    ds=np.array([16,32,64,128]); vs=[np.abs(Si[np.arange(100,p-200),np.arange(100,p-200)+x]).max() for x in ds]
    sl=np.polyfit(np.log(1+ds),np.log(vs),1)[0]
    print(f"alpha={alpha} signs={signs} spec=[{ev.min():.3f},{ev.max():.3f}] inv*(1+d)^a:",np.round(out,3)," slope",round(sl,2))
# BC: conditional covariance given |U|<=15, adversarial U between j,k (chain) and near j,k
def condcov(S,j,k,U):
    U=list(U); idx=[j,k]
    if not U: return S[j,k]
    A=S[np.ix_(idx,idx)]-S[np.ix_(idx,U)]@np.linalg.solve(S[np.ix_(U,U)],S[np.ix_(U,idx)])
    return A[0,1]
for alpha in [3.0,8.6]:
    S,d,K=make(400,alpha,signs=False)
    j=100
    for dd in [10,20,40,80,160]:
        k=j+dd; best=0
        for trial in range(300):
            mode=trial%3
            if mode==0: U=np.linspace(j+1,k-1,15).astype(int)
            elif mode==1: U=np.r_[np.arange(j+1,j+8),np.arange(k-7,k)]
            else: U=rng.choice([x for x in range(max(0,j-30),min(400,k+30)) if x not in (j,k)],15,replace=False)
            U=sorted(set(U)-{j,k})
            best=max(best,abs(condcov(S,j,k,U)))
        print(f"BC alpha={alpha} d={dd}: max|condcov|*(1+d)^a={best*(1+dd)**alpha:.3f}  marginal*(1+d)^a={S[j,k]*(1+dd)**alpha:.3f}")
