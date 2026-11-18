import math
viol=[];worst={}
def lc(n,k):
    return sum(math.log(n-i) for i in range(k))-math.lgamma(k+1)
    return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
for A in [1,1.3,1.5,2,3,5,7.7,10,20]:
  for s in range(1,40):
    j0=math.ceil((2*A+1)*s)+1
    for e in [math.log(3)]+[x/4 for x in range(5,140)]:
      n=math.exp(e); 
      if n<3: continue
      t=math.log(n); p=n**A
      if p<s+1: continue
      # B1.2
      if s+j0>(2*A+2)*s+2+1e-9: viol.append(('B1.2',A,s,n))
      # B1.3 using the [T03R] E2(ii) upper bound (without min K)
      msh=s+math.ceil((lc(p,s)+(s+1)/2*t+0.5*t)/math.log(2))
      if s+msh>3*(A+1)*(s+1)*t: viol.append(('B1.3',A,s,n))
      # B2.1
      mbar=math.ceil((s*(A*t+math.log(2))+math.log(2)+(s+2)/2*t)/math.log(1.5))
      kbar=min(p,s+max(j0,mbar))
      if kbar>5*(A+1)*(s+1)*t: viol.append(('B2.1',A,s,n))
      # B4.1
      if s+max(j0,msh)>3*(A+1)*(s+1)*t: viol.append(('B4.1',A,s,n))
      # B6.1
      if 16+s>5*(A+1)*(s+1)*t: viol.append(('B6.1',A,s,n))
      r=(s+mbar)/((A*s+1.5*s+2)*t*(1/math.log(1.5)))
      worst['B2.1ratio']=max(worst.get('B2.1ratio',0),r)
print('violations',len(viol),viol[:5]); print(worst)
