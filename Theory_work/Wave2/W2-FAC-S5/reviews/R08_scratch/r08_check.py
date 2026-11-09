# R08 independent check (Opus seat). Direct SoP score in mpmath (no reuse of bcs_core).
import mpmath as mp, random, math, itertools, sys
mp.mp.dps = 60
def run(seed, p=20, q=5, rb=0.3, rw=0.7, n=mp.mpf(10)**int(sys.argv[1]) if len(sys.argv)>1 else mp.mpf(10)**20, truths=(0,7), vt=(1.0,-0.8), sigma=1.0):
    rnd = random.Random(seed)
    b, d = rw-rb, 1-rw
    grp = [j//q for j in range(p)]
    Sig = mp.matrix(p,p)
    for i in range(p):
        for j in range(p):
            Sig[i,j] = 1 if i==j else (rw if grp[i]==grp[j] else rb)
    eta = rnd.gauss(0,1); zeta=[rnd.gauss(0,1) for _ in range(p//q+1)]; xi=[rnd.gauss(0,1) for _ in range(p)]
    h = math.sqrt(rb)*eta; y=[math.sqrt(b)*zeta[grp[j]]+math.sqrt(d)*xi[j] for j in range(p)]
    g = mp.matrix([h+y[j] for j in range(p)])
    th = mp.matrix(p,1); 
    for t,v in zip(truths,vt): th[t]=v
    S0=set(truths)
    nm1 = n-1
    r = (n-1-p) + mp.sqrt(2*(n-1-p))*rnd.gauss(0,1)
    E2 = sigma**2*((g.T*mp.inverse(Sig)*g)[0] + r)
    Sth = Sig*th
    s2 = (nm1*(th.T*Sth)[0] + 2*sigma*mp.sqrt(nm1)*(th.T*g)[0] + E2)/nm1
    s = mp.sqrt(s2)
    z = (nm1*Sth + sigma*mp.sqrt(nm1)*g)/s
    nu = mp.mpf('0.01')+n/2
    def logw(k): return -mp.log(2) - (mp.loggamma(2*p) - mp.loggamma(k+1) - mp.loggamma(2*p-k))
    cache={}
    def F(T):
        T=tuple(sorted(T))
        if T in cache: return cache[T]
        k=len(T)
        if k==0:
            v = logw(0) - nu*mp.log(mp.mpf('0.02')+nm1)
        else:
            G = mp.matrix(k,k); zz=mp.matrix(k,1)
            for a,i in enumerate(T):
                zz[a]=z[i]
                for c,j in enumerate(T): G[a,c]=nm1*Sig[i,j]
            H = (n+1)*G + mp.eye(k)
            quad = (zz.T*mp.lu_solve(H,zz))[0]
            Q = nm1 - n*quad
            v = logw(k) - (mp.log(mp.det(H)) - mp.log(mp.det(G+mp.eye(k))))/2 - nu*mp.log(mp.mpf('0.02')+Q)
        cache[T]=v; return v
    def eR(R):
        R=sorted(R)
        if not R: return h
        SR = mp.matrix([[Sig[i,j] for j in R] for i in R]); gR = mp.matrix([g[i] for i in R])
        return h - (mp.matrix([[rb]*len(R)])*mp.lu_solve(SR,gR))[0]
    logn = mp.log(n); k0 = 1/math.sqrt(1-rb)
    Hq = math.sqrt(2*math.log(2**q*p)+2*math.log(float(logn)))
    T=set(range(p)); steps=0; out=[]
    worst={'del_min':1e9,'add_minus_best':-1e9,'swapnull_minus_best':-1e9,'truthmove_over_n':-1e9,'CCmargin':1e9}
    while True:
        k=len(T); base=F(T)
        moves=[]
        for j in T: moves.append((F(T-{j})-base,'del',j,None))
        for l in set(range(p))-T: moves.append((F(T|{l})-base,'add',None,l))
        for j in T:
            for l in set(range(p))-T: moves.append((F((T-{j})|{l})-base,'swap',j,l))
        best=max(moves,key=lambda m:m[0])
        nulldel=[m for m in moves if m[1]=='del' and m[2] not in S0]
        # CC margin at delta=0 (normalised by log n)
        Lam = logn + 2*mp.log(mp.mpf(2*p-k)/(k+1))
        Tps=[T]+[T-{j} for j in T-S0]
        emax=max(abs(eR(Tp)) for Tp in Tps)
        worst['CCmargin']=min(worst['CCmargin'], float((Lam-(Hq+k0*emax)**2)/logn))
        if T!=S0:
            G = max(m[0] for m in nulldel)
            worst['del_min']=min(worst['del_min'],float(G/logn))
            adds=[m[0] for m in moves if m[1]=='add']
            if adds: worst['add_minus_best']=max(worst['add_minus_best'],float((max(adds)-G)/logn))
            sw=[m[0] for m in moves if m[1]=='swap' and m[2] not in S0]
            if sw: worst['swapnull_minus_best']=max(worst['swapnull_minus_best'],float((max(sw)-G)/logn))
        tm=[m[0] for m in moves if m[2] in S0]
        worst['truthmove_over_n']=max(worst['truthmove_over_n'],float(max(tm)/n))
        if best[0]<=0: break
        if best[1]!='del' or best[2] in S0: return dict(seed=seed,pure=False,move=best[1:],T=sorted(T))
        T=T-{best[2]}; steps+=1
    return dict(seed=seed,pure=True,end_is_S0=(T==S0),steps=steps,**worst)
if __name__=='__main__':
    for sd in range(int(sys.argv[2]) if len(sys.argv)>2 else 3):
        print(run(sd), flush=True)
