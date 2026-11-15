import math, itertools, json
from fractions import Fraction
import numpy as np

rng = np.random.default_rng(271828)
out = {}
# Exact combinatorial simplification and constants, including s=0,p-1.
count=0
for p in range(2,61):
    for s in range(p):
        c=Fraction((s+1)*(p-s),2*p-1-s)
        assert s>p/2 or c>=Fraction(s+1,3)
        assert s==0 or c>=1
        prod=Fraction(1)
        for j in range(1,p-s+1):
            prod*=Fraction(p-s-j+1,2*p-s-j)
            assert Fraction(math.comb(p-s,j)*math.comb(2*p-1,s),math.comb(2*p-1,s+j))==math.comb(s+j,j)*prod
            count+=1
out['exact_B_coefficients']=count

# Independent dense posterior enumeration, duplicate columns included.
worst=math.inf; identities=0; maxerr=0.0
for n,p in [(3,2),(4,3),(6,4),(10,5),(16,6)]:
    for arm in range(4):
        X=rng.normal(size=(n,p)); X-=X.mean(axis=0)
        if arm==1: X[:,1]=X[:,0]
        X*=np.sqrt(n-1)/np.linalg.norm(X,axis=0)
        y=rng.normal(size=n); y-=y.mean(); y*=np.sqrt(n-1)/np.linalg.norm(y)
        K=min(p,n//2); vals={}; aux={}
        for s in range(K+1):
            for S in itertools.combinations(range(p),s):
                A=X[:,S]; G=A.T@A; H=(n+1)*G+np.eye(s); z=A.T@y
                q=float(y@y-n*z@np.linalg.solve(H,z))
                ld=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(s))[1]
                theta=n*np.linalg.solve(H,z)
                v=float(np.linalg.norm(y-A@theta)**2+theta@(G+np.eye(s))@theta/n)
                maxerr=max(maxerr,abs(q-v))
                vals[S]=-math.log(math.comb(2*p-1,s))-ld/2-(.01+n/2)*math.log(.02+q)
                aux[S]=(q,ld)
        for S,ls in vals.items():
            s=len(S)
            if s>=K: continue
            odds=sum(math.exp(v-ls) for T,v in vals.items() if T!=S)
            lb=0.0; term=1.0
            for j in range(1,K-s+1):
                term*=(s+j)/j/math.sqrt(n)*(p-s-j+1)/(2*p-s-j)
                lb+=term
            worst=min(worst,odds/lb)
            for j in set(range(p))-set(S):
                T=tuple(sorted(S+(j,))); A=X[:,S]; G=A.T@A; H=(n+1)*G+np.eye(s)
                g=A.T@X[:,j]; sch=n*n-(n+1)**2*g@np.linalg.solve(H,g)
                den=n-g@np.linalg.solve(G+np.eye(s),g)
                q,ld=aux[S]; qt,ldt=aux[T]
                residual=y-(n+1)*A@np.linalg.solve(H,A.T@y)
                maxerr=max(maxerr,abs(math.exp(ldt-ld)-sch/den),abs(q-qt-n*(X[:,j]@residual)**2/sch))
                assert math.exp(ldt-ld)<=n+1e-9
                identities+=1
assert worst>=1-1e-9 and maxerr<1e-8
out['random_dense']={'one_step_pairs':identities,'minimum_odds_over_lb':worst,'maximum_identity_error':maxerr}

# Ceiling scan; tail weights only depend on k, hence cache their exact recurrence.
cache={}
def tail(k):
    if k not in cache:
        p=k+2; m=k//2; q=.5; total=0.
        for j in range(1,p+1):
            q*= (p-j+1)/(2*p-j)
            if j>m: total+=q
        cache[k]=total*(2*p-1)*(2*p-2)
    return cache[k]
mxR=(0,0); mxA=(0,0); mxD=(0,0); minDelta=(1,0)
for start in range(200,2000001,100000):
    n=np.arange(start,min(start+100000,2000001),dtype=float); L=np.log(n)
    k=np.ceil(12*L).astype(int); p=k+2; m=k//2
    assert np.all(p<=np.floor(n/2))
    R=np.array([tail(int(t)) for t in k])
    det=(n-1)**2*(k/n**4)/(1+k/n**4)
    DT=(1+2*(n+1)*(n-1)+(n+1)**2*det)/(2*n-1+det)
    delta=(n-1)/(8*n)-4*(k+1)/(1200*L**2)-1/n
    assert np.all(R*n*n<=1) and np.all(DT<=2*n)
    assert np.all(R*np.sqrt(DT*n)<=2/n) and np.all(delta>=.1)
    assert np.all((3*p-1)*math.log(2)+k/2*L<=12*L**2)
    for arr,key in [(R*n*n,'R'),(R*np.sqrt(DT*n)*n,'A'),(DT/n,'D')]:
        idx=int(np.argmax(arr)); val=(float(arr[idx]),int(n[idx]))
        if key=='R' and val[0]>mxR[0]: mxR=val
        if key=='A' and val[0]>mxA[0]: mxA=val
        if key=='D' and val[0]>mxD[0]: mxD=val
    idx=int(np.argmin(delta))
    if delta[idx]<minDelta[0]: minDelta=(float(delta[idx]),int(n[idx]))
out['scan_200_to_2000000']={'max_n2R':mxR,'max_nA':mxA,'max_DT_over_n':mxD,'min_Delta_over_nb2_bound':minDelta}
out['nonmonotone_n2R']={n:n*n*tail(math.ceil(12*math.log(n))) for n in [200,201]}
assert .975/40>1/42 and 1/42-1/100>1/73
out['constants']={'tail_envelope_at_200':3.78*(12*math.log(200)+3)**2*200**(-2.158),'noise_coefficient':(48*math.log(200)+8)/(1200*math.log(200)**2),'exponent_margin':1/42-1/100-1/73}

# Lemma P: dense minimization for all membership patterns, including empty S.
minratio=math.inf; tested=0
for n,k in [(20,4),(200,6)]:
    M=rng.normal(size=(n,k+1)); M-=M.mean(axis=0)
    U=np.linalg.qr(M)[0]*math.sqrt(n-1)
    for eta in [n**-2,.05]:
        c=1/math.sqrt(1+k*eta**2)
        X=np.column_stack([U[:,0],c*(U[:,0]-eta*U[:,1:].sum(axis=1)),U[:,1:]])
        mu=U[:,1:].sum(axis=1)/math.sqrt(k)
        for mask in range(1<<(k+2)):
            S=[j for j in range(k+2) if mask>>j&1]; d=k-sum(j>=2 for j in S)
            if not d: continue
            A=X[:,S]; reg=np.zeros(len(S))
            if 1 in S: reg[S.index(1)]=1/n
            # least-squares augmented system avoids subtractive loss at tiny eta.
            aug=np.vstack([A,np.diag(np.sqrt(reg))]); target=np.r_[mu,np.zeros(len(S))]
            theta=np.linalg.lstsq(aug,target,rcond=None)[0]
            cost=np.linalg.norm(target-aug@theta)**2
            bound=(n-1)*d/k/(1+n*(n-1)*d*c*c*eta*eta)
            minratio=min(minratio,cost/bound); tested+=1
assert minratio>=1-1e-9
out['lemma_P']={'cases':tested,'minimum_cost_over_bound':minratio}
print(json.dumps(out,indent=2))
