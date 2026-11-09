import numpy as np, itertools
rng=np.random.default_rng(1)
def ccov(S,i,j,U):
    U=list(U)
    if not U: return S[i,j]
    return S[i,j]-S[i,U]@np.linalg.solve(S[np.ix_(U,U)],S[U,j])
# STAR
m=27;p=m+10;r=1/(2*np.sqrt(m));S=np.eye(p);S[0,1:m+1]=r;S[1:m+1,0]=r
print("STAR eig",np.round(np.unique(np.round(np.linalg.eigvalsh(S),8)),6))
U=list(rng.choice(range(2,p),15,replace=False)); l=1 if 1 not in U else 2
U=[u for u in U if u!=l]
print("STAR cov l,1|U",ccov(S,l,0,U),"=r",r,"var",ccov(S,l,l,U))
# V2/V3 equicorrelated Schur
g=30;rho=0.4;S=(1-rho)*np.eye(g)+rho*np.ones((g,g))
for u in [0,1,5,15]:
    U=list(range(2,2+u)); print("equi u",u,ccov(S,0,1,U),rho*(1-rho)/(1+(u-1)*rho))
# V4 one factor
p=40;b=rng.uniform(-1,1,p)*0.9;psi=1-b**2;S=np.outer(b,b)+np.diag(psi)
U=list(range(5,20));Vf=1/(1+np.sum(b[U]**2/psi[U]))
print("V4",ccov(S,0,1,U),b[0]*b[1]*Vf)
# F3(iv)
S=np.array([[1,.5],[.5,1]]);print("F3iv",S@np.array([1,-2]))
# b_j=2^-j
p=60;b=2.0**-np.arange(1,p+1);S=np.outer(b,b)+np.diag(1-b**2);e=np.linalg.eigvalsh(S);print("2^-j spec",e.min(),e.max())
# S5
G=20;p=5*G;H=np.kron(np.eye(G),np.ones((5,5)));S=0.3*np.ones((p,p))+0.4*H+0.3*np.eye(p);print("S5 diag",S[0,0],"min eig",np.linalg.eigvalsh(S).min())
# R06-2: theta=(1,1) on S0={0,1}, b=(.5,-.5), nulls .5, psi=.75
p=8;b=np.array([.5,-.5]+[.5]*(p-2));S=np.outer(b,b)+0.75*np.eye(p)
th=np.zeros(p);th[:2]=1
for l in range(2,p):
  for U in [[],[l%6+2] if l%6+2!=l else []]:
    print("R06-2 null",l,U,round(ccov(S,l,l,U)*0+ (S[l]@th - (S[l,U]@np.linalg.solve(S[np.ix_(U,U)],S[U]@th) if U else 0)),12)); break
print("Sigma theta",S@th)
# MIS AR1 cancel
rho=.5;S=np.array([[rho**abs(i-j) for j in range(3)] for i in range(3)]);print("MIS gamma2",(S[1,0]*1+S[1,2]*-1)/S[1,1])
