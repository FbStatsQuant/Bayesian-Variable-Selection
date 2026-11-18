# R2 seat opus: re-check B2.1 harmonised constant and Thm 7 (A5)(b) C_Q => (BM-Q-flat) arithmetic; B3.8 inequality.
import math
viol=0; worst=0
for A in [1,1.5,2,3,5,8,13,20]:
  for s in range(1,40):
    for e in [1.1,1.5,2,3,5,8,12,20,35]:
      n=math.exp(e)
      if n<3: continue
      L=math.log(n)
      j0=math.ceil((2*A+1)*s)+1
      mbar=math.ceil((s*(A*L+math.log(2))+math.log(2)+(s+2)/2*L)/math.log(1.5))
      kbar=s+max(j0,mbar)   # p large (min with p only lowers it)
      rhs=(2.4664*A*s+3.6996*s+4.9327)*L
      worst=max(worst,kbar/rhs)
      if kbar>=rhs: viol+=1
      if rhs>5*(A+1)*(s+1)*L: viol+=1
print("B2.1 violations",viol,"worst ratio",round(worst,5))
# B3.8 step 3 identity
bad=0
for s in range(1,60):
  for p in range(s+1,400):
    if (s+1)*(p-s)-(2*p-1-s)!=(s-1)*(p-s-1): bad+=1
    if 2*(s+1)*(p-s)/(2*p-1-s)<2-1e-12: bad+=1
    if 2*s<=p and 2*(p-s)/(2*p-1-s)<0.5-1e-12: bad+=1
print("B3.8 identity/inequality failures",bad)
# Thm7 (A5)(b): C_Q > max(32, 64A + c) with c>max(16,cTL0) gives BM-Q-flat for large n (p<=n^A, |Q|>=1)
def ok(A,c,CQ,q,n):
  L=math.log(n); lam=CQ*(n-1)/n*(q+L)  # lambda_n >= this under (A5)(b)
  return lam >= 32*(q+1)+64*math.log(2*n**A)+c*L
fails=[]
for A in [1,2,5]:
  for c in [16.01,40,100]:
    CQ=1.05*max(32,64*A+c)
    for q in [1,10,1000,10**5]:
      n_ok=None
      for e in range(2,80):
        n=math.exp(e)
        if ok(A,c,CQ,q,n): n_ok=e; break
      fails.append((A,c,q,n_ok))
print("C_Q check (A,c,|Q|, first log n where BM-Q-flat holds):",fails)
