import itertools,math,json
from pathlib import Path
n,p,K=8,7,4;truth=frozenset(range(4))
def F(S):
 t=len(S&truth);k=len(S);return -math.log(math.comb(2*p-1,k))-.5*k*math.log(8)-4.01*math.log(.02+7-1.53125*t)
def phi(S):return len(S^truth)
region=[frozenset(s) for k in range(K+1) for s in itertools.combinations(range(p),k) if len(truth-set(s))<=1 and len(set(s)-truth)<=1]
rows=[]
for S in region:
 N=set()
 for j in range(p):
  T=S^{j}
  if len(T)<=K:N.add(T)
 for j in S:
  for l in set(range(p))-S:N.add((S-{j})|{l})
 best=min(N,key=lambda T:(-F(T),tuple(sorted(T))))
 ok=(F(best)<=F(S)) if S==truth else (F(best)>F(S) and phi(best)<phi(S))
 rows.append({'state':sorted(S),'best':sorted(best),'gain':F(best)-F(S),'ok':ok})
assert all(x['ok'] for x in rows)
Path('cap_witness.json').write_text(json.dumps({'n':n,'p':p,'K':K,'G':'7 I_7','y':'(x1+x2+x3+x4)/2','truth':[1,2,3,4],'region_size':len(region),'rows_zero_based':rows},indent=2))
print('all TD-P clauses pass; literal lattice of {1,2,3,5} contains infeasible {1,2,3,4,5}')
