import sys; sys.path.insert(0, sys.argv[1]); from common import *
exec(open(sys.argv[1]+'/c6_ls.py').read().split('rng=np.random')[0].split('from common import *')[1])
def path(c,F,p,K,ell):
    cur=c; pth=[c]; moves=0
    while True:
        best=max(nbrs(cur,p,K),key=lambda S:key(S,F))
        if better(best,cur,F) and moves<ell: cur=best; pth.append(cur); moves+=1
        else: return pth
rng=np.random.default_rng(20261106)
n=int(rng.integers(20,60)); p=8; K=min(p,n//2); ell=math.ceil(math.log2(n+p+1))
Xr=rng.standard_normal((n,p))
Xr[:,2]=Xr[:,0]+Xr[:,1]+rng.uniform(0.05,0.6)*rng.standard_normal(n)
Xr[:,3]=Xr[:,4]+rng.uniform(0.05,0.6)*rng.standard_normal(n)
yr=Xr[:,0]+Xr[:,1]+rng.uniform(0.2,1.0)*rng.standard_normal(n)
X,y=standardise(Xr,yr); F=enum_F(X,y,K)
keys=sorted(F,key=lambda S:key(S,F)); rank={S:i for i,S in enumerate(keys)}
LS={S:local_search(S,F,p,K,ell) for S in keys}
# maximal scored sets: R=4 scored = down-set {S ⪯ c4}; R' scored = down-set {S ⪯ c'}
cnt=0; ex=None
for a,c4 in enumerate(keys):
    h4=hpm(LS[c4][1]|{c4},F)
    for b in range(a+1,len(keys)):
        cp=keys[b]
        hp=hpm(LS[cp][1]|{cp},F)   # down-set ⪯ c' contributes nothing above c'
        if better(h4,hp,F):
            cnt+=1
            if ex is None or b==a+1: ex=(c4,cp,h4,hp)
print("n",n,"K",K,"ell",ell,"#(c4 ≺ c') pairs with post-search HPM(R') ≺ post-search HPM(4), down-set scored sets:",cnt,"of",len(keys)*(len(keys)-1)//2)
c4,cp,h4,hp=ex
print("example: c4",c4,round(F[c4],4)," c'",cp,round(F[cp],4)," adjacent in ≻ order:",rank[cp]==rank[c4]+1)
print("  path from c4:",[ (S,round(F[S],3)) for S in path(c4,F,p,K,ell)])
print("  path from c':",[ (S,round(F[S],3)) for S in path(cp,F,p,K,ell)])
print("  HPM(4)=",h4,round(F[h4],4),"  HPM(R')=",hp,round(F[hp],4), " S†=",keys[-1])
print("  local maxima (flip+swap):",[ (S,round(F[S],3)) for S in keys if not any(better(T,S,F) for T in nbrs(S,p,K))])
