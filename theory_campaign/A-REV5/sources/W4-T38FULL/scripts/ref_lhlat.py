import numpy as np, itertools, sys
def build(G,g,rhos,pairs,vis):
    # rhos: list per group; pairs: list of (ga,gb,psi,beta); vis: list of (gh,theta)
    p=G*g; S=np.zeros((p,p))
    for h in range(G):
        idx=range(h*g,(h+1)*g); r=rhos[h]
        for i in idx:
            for j in idx: S[i,j]=1.0 if i==j else r
    hub=lambda h:h*g
    for (ga,gb,psi,beta) in pairs:
        A=list(range(ga*g,(ga+1)*g)); B=list(range(gb*g,(gb+1)*g))
        blk=psi*np.outer(S[A,hub(ga)],S[hub(gb),B])
        S[np.ix_(A,B)]=blk; S[np.ix_(B,A)]=blk.T
    th=np.zeros(p)
    for (ga,gb,psi,beta) in pairs: th[hub(ga)]=beta; th[hub(gb)]=-psi*beta
    for (gh,t) in vis: th[hub(gh)]=t
    return S,th
def Delta(S,th,T):
    T=sorted(T); tot=th@S@th
    if not T: return tot
    c=S[T,:]@th; return tot-c@np.linalg.solve(S[np.ix_(T,T)],c)
def run(G,g,rhos,pairs,vis,verbose=False):
    S,th=build(G,g,rhos,pairs,vis); p=G*g
    assert np.linalg.eigvalsh(S).min()>0
    S0=set(np.nonzero(th)[0]); M=[gb*g for (_,gb,_,_) in pairs]
    Sc=S0-set(M)
    R=[b**2*ps**2*(1-ps**2) for (_,_,ps,b) in pairs]
    kap=[rhos[gb]**2*(1-ps**2)/(1-ps**2*rhos[gb]**2) for (_,gb,ps,_) in pairs]
    m0=min([(1-max(kap))*min(R),min(R)]+[b**2*(1-ps**2)**2 for (_,_,ps,b) in pairs]+[t**2 for _,t in vis])
    worst=np.inf; arg=None
    for r in range(len(M)+1):
        for sub in itertools.combinations(range(len(M)),r):
            St=Sc|{M[i] for i in sub}
            I=[i for i in range(len(M)) if i not in sub]
            if len(I)<2: continue
            istar=max(I,key=lambda i:R[i]); A=St|{M[istar]}
            dA=Delta(S,th,A); dS=Delta(S,th,St)
            assert abs((dS-dA)-R[istar])<1e-9,(dS-dA,R[istar])
            phi=lambda T:len(set(T)^S0)
            nb=[]
            for l in range(p):
                if l not in St: nb.append(St|{l})
            for t in St:
                nb.append(St-{t})
                for l in range(p):
                    if l not in St: nb.append((St-{t})|{l})
            nb.append(St)
            for B in nb:
                if B is not St and phi(B)<phi(St): continue
                d=Delta(S,th,B)-dA
                if d<worst: worst=d; arg=(sorted(St),sorted(B))
    return m0,worst,arg
if __name__=="__main__":
    rng=np.random.default_rng(1)
    cases=[]
    cases.append((5,3,[.7]*5,[(0,1,.5,1.4),(2,3,-.4,-1.0)],[(4,1.0)]))
    cases.append((6,3,[.7,.6,.9,.8,.5,.7],[(0,1,.69,1.0),(2,3,-.79,2.0),(4,5,.49,0.7)],[]))
    cases.append((6,3,[.3,.95,.95,.3,.6,.6],[(0,1,-.29,1.0),(2,3,.29,1.0),(4,5,-.59,1.5)],[]))
    cases.append((5,3,[.99,.99,.5,.5,.5],[(0,1,.98,1.0),(2,3,-.49,1.0)],[(4,.3)]))
    cases.append((5,2,[.2,.9,.9,.2,.5],[(0,1,.01,3.0),(2,3,-.19,1.0)],[(4,2.)]))
    for _ in range(15):
        G=6;g=int(rng.integers(2,4)); rh=list(rng.uniform(.05,.97,G))
        pr=[]
        for k in range(3):
            a,b=2*k,2*k+1; mx=min(rh[a],rh[b]); ps=rng.uniform(.02,1)*mx*rng.choice([-1,1])
            pr.append((a,b,ps,rng.choice([-1,1])*rng.uniform(.3,3)))
        cases.append((G,g,rh,pr,[]))
    for cs in cases:
        m0,w,arg=run(*cs)
        print(f"G={cs[0]} g={cs[1]} m0={m0:.5g} min_margin={w:.5g} ok={w>=m0-1e-10} ratio={w/m0:.3f} argmin={arg}")
