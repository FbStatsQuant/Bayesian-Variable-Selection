import sys; sys.path.insert(0, sys.argv[1]); from common import *
def key(S,F): return (F[S], -len(S), tuple(-i for i in S))   # larger key = better (≻): larger F, smaller |S|, lex smallest
def better(a,b,F): return key(a,F)>key(b,F)
def nbrs(S,p,K):
    s=set(S); out=[]
    for j in range(p):
        T=tuple(sorted(s^{j}))
        if len(T)<=K: out.append(T)
    for i in S:
        for j in range(p):
            if j not in s: out.append(tuple(sorted((s-{i})|{j})))
    return out
def local_search(c,F,p,K,ell):
    evaluated={c}; cur=c; moves=0
    while True:
        nb=nbrs(cur,p,K); evaluated.update(nb)
        best=max(nb,key=lambda S:key(S,F))
        if better(best,cur,F) and moves<ell: cur=best; moves+=1
        else: break   # stop: no improvement, or after ell moves the further scan
    return cur, evaluated
def hpm(Sset,F): return max(Sset,key=lambda S:key(S,F))
rng=np.random.default_rng(20261106); found=0
for rep in range(400):
    n=int(rng.integers(20,60)); p=8; K=min(p,n//2); ell=math.ceil(math.log2(n+p+1))
    Xr=rng.standard_normal((n,p))
    Xr[:,2]=Xr[:,0]+Xr[:,1]+rng.uniform(0.05,0.6)*rng.standard_normal(n)  # proxy for {0,1}
    Xr[:,3]=Xr[:,4]+rng.uniform(0.05,0.6)*rng.standard_normal(n)
    yr=Xr[:,0]+Xr[:,1]+rng.uniform(0.2,1.0)*rng.standard_normal(n)
    X,y=standardise(Xr,yr); F=enum_F(X,y,K)
    keys=sorted(F,key=lambda S:key(S,F))   # ascending
    LS={S:local_search(S,F,p,K,ell) for S in keys}
    # find c4 < c' (c' ≻ c4) with best(LS(c4) ∪ {c4}) ≻ best(LS(c') ∪ {c4,c'})
    for a in range(len(keys)):
        c4=keys[a]; h4=hpm(LS[c4][1]|{c4},F)
        for b in range(a+1,len(keys)):
            cp=keys[b]; hp=hpm(LS[cp][1]|{c4,cp},F)
            if better(h4,hp,F):
                S0dag=keys[-1]
                print(f"rep={rep} n={n} p={p} K={K} ell={ell}")
                print(f"  c4={c4} F={F[c4]:.4f}   c'={cp} F={F[cp]:.4f}  (c' ≻ c4)")
                print(f"  post-search HPM R=4: {h4} F={F[h4]:.4f}; post-search HPM R'(no extra LS): {hp} F={F[hp]:.4f}")
                print(f"  global HPM S†={S0dag} F={F[S0dag]:.4f}; S† in LS(c')? {S0dag in LS[cp][1]}  S† in LS(c4)? {S0dag in LS[c4][1]}")
                print(f"  with extra LS from c4 in R' run: {hpm(LS[cp][1]|LS[c4][1]|{c4,cp},F)}")
                found+=1; break
        if found: break
    if found: break
print("found",found)
