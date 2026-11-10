import numpy as np,itertools,math
for n in [1000,10000,100000]:
 p=4; G=np.eye(p)*(n-1); G[1,2]=G[2,1]=(n-1)*math.cos(3/n)
 for z in [3.,5.,8.]:
  v=np.array([n-1,0,math.sqrt(n-1)*math.sin(3/n)*z,0]); yy=2*(n-1)+z*z
  def F(S):
   k=len(S); g=G[np.ix_(S,S)]; h=(n+1)*g+np.eye(k); t=v[list(S)]*math.sqrt((n-1)/yy)
   Q=n-1-n*(t@np.linalg.solve(h,t)) if k else n-1
   return -math.log(2*math.comb(7,k))-.5*np.linalg.slogdet(h)[1]+.5*np.linalg.slogdet(g+np.eye(k))[1]-(n/2+.01)*math.log(.02+Q)
  S=(0,1,2); neighbors=set()
  for j in S:
   neighbors.add(tuple(i for i in S if i!=j))
   neighbors.add(tuple(sorted(tuple(i for i in S if i!=j)+(3,))))
  neighbors.add((0,1,2,3))
  diffs=[(T,F(T)-F(S)) for T in sorted(neighbors)]
  print(n,z,diffs)
