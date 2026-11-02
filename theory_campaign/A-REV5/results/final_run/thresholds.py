import math,json
from pathlib import Path
# Independent stdlib exact-prior recurrence, log suffix sums; no large matrices.
def logadd(a,b):
 if a == -math.inf:return b
 m=max(a,b);return m+math.log1p(math.exp(min(a,b)-m))
def calc(n,A):
 p=round(n**A); K=min(p,n//2); s=14; end=min(K,2014)
 t=sum(math.log(p-i)-math.log(i+1) for i in range(s)); terms=[t]
 for k in range(s,end): terms.append(terms[-1]+math.log(p-k)-math.log(2*p-1-k))
 tail=-math.inf; sums={end:-math.inf}
 for k in range(end,s,-1):tail=logadd(tail,terms[k-s]);sums[k-1]=tail
 target=-8*math.log(n);m=next(k for k in range(s,end+1) if sums[k]<=target)
 # Tail after end is at most its last term; assert truncation cannot change m.
 if end<K: assert logadd(sums[m],terms[-1])<=target and sums[m-1]>target
 C=8+3*A;d=3*math.sqrt(math.log(n)/(n-1))+C*(m+s)*math.log(n)/(n-1)
 if d>=1:return {'m':m,'delta':d,'q':math.inf,'exp2eps':math.inf}
 u=(1+(.02*n+1)/(n*n-1))/(1-d);eps=(u-1)*C*math.log(n)/2
 return {'m':m,'delta':d,'q':math.sqrt(math.e*C*math.log(n)/(4*(n+1)))*math.exp(eps),'exp2eps':math.exp(2*eps)}
rows=[]
for p0,pts in [(500,[130328,2116047,2116048,25571896,25571897]),(1000,[130328,2457024,2457025,29755301,29755302])]:
 A=math.log(p0)/math.log(200)
 for n in pts:rows.append(dict(p0=p0,n=n,**calc(n,A)))
Path('thresholds.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
