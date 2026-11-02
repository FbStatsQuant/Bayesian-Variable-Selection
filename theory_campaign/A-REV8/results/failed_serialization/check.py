import numpy as np, json, itertools, pathlib, platform, sys
from scipy.special import gammaln, logsumexp
ROOT=pathlib.Path(__file__).resolve().parents[1]; out=ROOT/'results'; out.mkdir(exist_ok=True)
rng=np.random.default_rng(20261102)
def family(g,groups,rhos,psis,betas):
 p=g*groups; C=np.eye(p); theta=np.zeros(p)
 for h in range(groups): C[h*g:(h+1)*g,h*g:(h+1)*g]=rhos[h]+(1-rhos[h])*np.eye(g)
 for i,(psi,beta) in enumerate(zip(psis,betas)):
  a,b=2*i*g,(2*i+1)*g; V=psi*np.outer(C[a:a+g,a],C[b,b:b+g]); C[a:a+g,b:b+g]=V; C[b:b+g,a:a+g]=V.T; theta[a]=beta;theta[b]=-psi*beta
 theta[2*len(psis)*g]=1
 return C,theta
def neighbors(S,p,K):
 S=frozenset(S)
 return {S^{j} for j in range(p) if j in S or len(S)<K}|{(S-{j})|{l} for j in S for l in range(p) if l not in S}
rows=[]
for trial in range(40):
 g=2;groups=6;rho=rng.uniform(.35,.95,groups);psi=[rng.uniform(.1,min(rho[2*i:2*i+2])*.95) for i in range(2)];beta=rng.uniform(.3,2,2)
 C,t=family(g,groups,rho,psi,beta); truth=frozenset(np.flatnonzero(t)); masked=[2,6];ref=truth-set(masked);v=C@t
 def delta(S):
  ix=sorted(S);return float(t@v-(v[ix]@np.linalg.solve(C[np.ix_(ix,ix)],v[ix]) if ix else 0))
 R=np.array(beta)**2*np.array(psi)**2*(1-np.array(psi)**2);kap=np.array([rho[2*i+1]**2*(1-psi[i]**2)/(1-psi[i]**2*rho[2*i+1]**2) for i in range(2)])
 m0=min((1-max(kap))*min(R),min(np.array(beta)**2*(1-np.array(psi)**2)**2),1.)
 A=ref|{masked[int(np.argmax(R))]};margin=min(delta(B)-delta(A) for B in neighbors(ref,12,12)|{ref} if len(B^truth)>=2)
 assert margin+1e-10>=m0
 rows.append(dict(trial=trial,rho=rho.tolist(),psi=psi,beta=beta.tolist(),bound=m0,margin=margin))
(out/'population.json').write_text(json.dumps(rows,indent=2))
records=[]
for n in [200,800]:
 for rep in range(3):
  g=9;p=108;C,t=family(g,12,[.7]*12,[.5,.5],[1.4,-1.]);G=(n-1)*C;L=np.linalg.cholesky(G);u=rng.normal(size=p);zraw=G@t+L@u; yy=float(t@G@t+2*t@L@u+u@u+rng.chisquare(n-1-p)); z=zraw/np.sqrt(yy/(n-1));K=min(p,n//2);truth=frozenset(np.flatnonzero(t));ref=truth-{9,27}
  np.savez_compressed(out/f'input_{n}_{rep}.npz',G=G,zraw=zraw,yy=yy,theta=t)
  cache={}
  def lm(S):
   key=tuple(sorted(S))
   if key not in cache:
    ix=list(key); k=len(ix)
    if k:
     GS=G[np.ix_(ix,ix)];H=(n+1)*GS+np.eye(k);D=np.linalg.slogdet(H)[1]-np.linalg.slogdet(GS+np.eye(k))[1];Q=n-1-n*z[ix]@np.linalg.solve(H,z[ix])
    else:D=0;Q=n-1
    cache[key]=-.5*D-(n/2+.01)*np.log(.02+Q)
   return cache[key]
  def prior(k):return gammaln(k+1)+gammaln(2*p-k)-gammaln(2*p)
  def F(S):return prior(len(S))+lm(S)
  base=lm([]); prof=np.array([0.]); modes={0:(0.,frozenset())}; tables=[]
  for h in range(12):
   table=[(frozenset(h*g+j for j in range(g) if mask>>j&1),mask.bit_count()) for mask in range(1<<g)];table=[(S,k,lm(S)-base) for S,k in table];tables.append(table)
   local=np.array([logsumexp([f for S,k,f in table if k==j]) for j in range(g+1)])
   new=np.full(min(K,len(prof)-1+g)+1,-np.inf)
   for k in range(len(new)):new[k]=logsumexp([prof[k-j]+local[j] for j in range(g+1) if 0<=k-j<len(prof)])
   prof=new;nmode={}
   for k,(val,S) in modes.items():
    for T,j,f in table:
     if k+j<=K and (k+j not in nmode or val+f>nmode[k+j][0]):nmode[k+j]=(val+f,S|T)
   modes=nmode
  mode=max(modes.items(),key=lambda kv:kv[1][0]+prior(kv[0]))[1][1];norm=logsumexp(prof+np.array([prior(k) for k in range(len(prof))]));logmass=prior(len(ref))+sum(lm(ref&set(range(h*g,(h+1)*g)))-base for h in range(12))-norm
  cur=mode;scored={cur};ell=int(np.ceil(np.log2(n+p+1)));moves=0
  while True:
   nb=neighbors(cur,p,K);scored|=nb;best=max(nb,key=lambda S:(F(S),tuple(-j for j in sorted(S))))
   if F(best)<=F(cur) or moves>=ell:break
   cur=best;moves+=1
  # Only Phi>=2 is required; for c=2 this is the reference alone.
  nb=neighbors(ref,p,K);progress=[F(S) for S in nb if len(S^truth)<2];bad=[F(S) for S in nb|{ref} if len(S^truth)>=2]
  records.append(dict(n=n,rep=rep,mode=sorted(mode),reference=sorted(ref),reference_mass=float(np.exp(logmass)),scores_truth=truth in scored,moves=moves,min_required_margin=max(progress)-max(bad),truth_best=F(truth)>=max(map(F,scored))))
(out/'ls0.json').write_text(json.dumps(records,indent=2))
print(json.dumps(dict(seed=20261102,python=sys.version,platform=platform.platform(),numpy=np.__version__,population_cases=len(rows),ls0=records),indent=2))
