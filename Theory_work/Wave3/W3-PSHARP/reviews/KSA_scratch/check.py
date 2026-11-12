"""Independent KSA falsification checks. Writes only its sibling results file."""
from pathlib import Path
import math
import itertools
import numpy as np
import mpmath as mp

rng = np.random.default_rng(12062026)
out = []
def note(s):
    out.append(s)
    print(s)

mp.mp.dps = 60
count = 0
for d in [3, 4, 5, 6, 10, 100, 1000, 100000]:
    dm = mp.mpf(d)
    c = mp.gamma(dm/2)/(mp.sqrt(mp.pi*dm)*mp.gamma((dm-1)/2))
    assert 1-1/dm <= c*mp.sqrt(2*mp.pi) <= 1
    for tau in [mp.mpf('0.001'), 2*mp.log(2), dm/2]:
        if tau > dm/2:
            continue
        for q in range(101):
            t2 = tau*q/100
            f = mp.exp(t2/2)*(1-t2/dm)**((dm-3)/2)
            assert mp.exp(-tau*tau/(2*dm)) <= f <= mp.exp(3*tau/(2*dm))*(1+mp.mpf('1e-55'))
            count += 1
        # Scaled integral avoids enormous exp(tau/2) in second moment.
        m1 = 2*c*mp.sqrt(tau)*mp.quad(lambda u: mp.exp(tau*u*u/2)*(1-tau*u*u/dm)**((dm-3)/2), [0, 1])
        m2scaled = 2*c*mp.sqrt(tau)*mp.quad(lambda u: mp.exp(tau*(u*u-mp.mpf('0.5')))*(1-tau*u*u/dm)**((dm-3)/2), [0, 1])
        assert m1 >= mp.sqrt(2*tau/mp.pi)*(1-1/dm)*mp.exp(-tau*tau/(2*dm))
        assert m2scaled <= mp.sqrt(2*tau/mp.pi)*mp.exp(3*tau/(2*dm))
note(f'Sphere: {count} pointwise bounds; Gamma ratios and 24 truncated moment pairs PASS (60 digits; includes d=3, tau=d/2).')

eps = np.linspace(1e-8, 1-1e-8, 100001)
assert np.all(np.exp(eps/2) <= 1+eps/2+eps**2/4+1e-15)
assert np.all((1-eps)*np.exp(eps/2) <= 1-eps/2+1e-15)
assert np.all(1-eps/2 <= (1-eps/4)**2+1e-15)
note('Reduction R: epsilon chain PASS on 100001 points, including near 0 and 1.')

def stats(X, y, S):
    n = len(y)
    Z = X[:, list(S)]
    G = Z.T@Z
    H = (n+1)*G+np.eye(len(S))
    A = G+np.eye(len(S))
    z = Z.T@y
    th = n*np.linalg.solve(H, z)
    Q = y@y-n*z@np.linalg.solve(H, z)
    lD = np.linalg.slogdet(H)[1]-np.linalg.slogdet(A)[1]
    obj = np.linalg.norm(y-Z@th)**2+th@A@th/n
    assert abs(obj-Q) < 1e-9
    return G,H,A,z,Q,lD

maxdet = maxgain = maxrho = maxvar = 0.
cnt = oddschecks = 0
for n in [3,4,5,8,20,80]:
    p = 5
    for kind in ['iid','duplicate','near','rank1']:
        for rep in range(8):
            X = rng.normal(size=(n,p)); X -= X.mean(axis=0)
            if kind=='duplicate': X[:,1] = X[:,0]
            if kind=='near': X[:,1] = X[:,0]+1e-9*X[:,1]
            if kind=='rank1': X = X[:,[0]]@np.array([[1.,-1.,2.,-3.,4.]])
            X *= math.sqrt(n-1)/np.linalg.norm(X,axis=0)
            rawy = rng.normal(size=n); rawy -= rawy.mean()
            sy = np.linalg.norm(rawy)/math.sqrt(n-1)
            y = rawy/sy
            for k in range(p):
                for S in itertools.combinations(range(p), k):
                    G,H,A,z,Q,lD = stats(X,y,S)
                    Z=X[:,list(S)]
                    rho=y-(n+1)*Z@np.linalg.solve(H,z)
                    PH=(n+1)*Z@np.linalg.solve(H,Z.T)
                    identity=y@PH@y/(n+1)+y@PH@(np.eye(n)-PH)@y
                    maxrho=max(maxrho,abs(Q-rho@rho-identity))
                    assert abs(Q-rho@rho-identity)<1e-9
                    assert Q>=-1e-9
                    for j in set(range(p))-set(S):
                        _,_,_,_,Qj,lDj=stats(X,y,S+(j,))
                        g=Z.T@X[:,j]
                        s=n*n-(n+1)**2*g@np.linalg.solve(H,g)
                        den=n-g@np.linalg.solve(A,g)
                        det=math.exp(lDj-lD)
                        gain=n*(X[:,j]@rho)**2/s
                        maxdet=max(maxdet,abs(det-s/den)/det)
                        maxgain=max(maxgain,abs(Q-Qj-gain)/max(Q,1))
                        assert 0<s<=n*n*(1+1e-10)
                        assert det<=n*(1+1e-9)
                        assert abs(det-s/den)<1e-7
                        assert abs(Q-Qj-gain)<1e-7
                        assert Q-Qj>=(X[:,j]@rho)**2/n-1e-8
                        if k+1<=min(p,n//2):
                            nu=.01+n/2
                            gam=(Q-Qj)/(.02+Q)
                            assert -1e-9<=gam<1
                            lr=math.log((k+1)/(2*p-1-k))-.5*(lDj-lD)-nu*math.log1p(-gam)
                            lb=math.log((k+1)/(2*p-1-k))-.5*math.log(n)+nu*gam
                            assert lr>=lb-1e-8
                            oddschecks+=1
                        cnt+=1
note(f'V/S: {cnt} one-step pairs (all subset sizes, including beyond K); {oddschecks} admissible posterior-ratio bounds PASS.')
note(f'Max relative determinant error {maxdet:.3e}; gain error/Q_or_1 {maxgain:.3e}; residual identity absolute error {maxrho:.3e}.')

cnt = 0
for n in [3,4,8,40,200]:
    C=np.eye(n)-np.ones((n,n))/n
    for kind in ['empty','iid','duplicate','near']:
        k=0 if kind=='empty' else min(3,n//2-1)
        for rep in range(30):
            Z=rng.normal(size=(n,k)); Z-=Z.mean(axis=0)
            if k:
                if k>=2 and kind=='duplicate': Z[:,1]=Z[:,0]
                if k>=2 and kind=='near': Z[:,1]=Z[:,0]+1e-9*Z[:,1]
                Z*=math.sqrt(n-1)/np.linalg.norm(Z,axis=0)
            theta=rng.normal(size=k)*math.sqrt(n/max(k,1))
            mu=Z@theta
            err=rng.normal(size=n)
            yc=mu+C@err; sy2=yc@yc/(n-1); y=yc/math.sqrt(sy2)
            G,H,A,z,Q,lD=stats(Z,y,tuple(range(k)))
            PH=(n+1)*Z@np.linalg.solve(H,Z.T)
            rho=(np.eye(n)-PH)@y
            U,sv,_=np.linalg.svd(Z,full_matrices=False)
            rank=int(np.sum(sv>1e-12))
            P0=U[:,:rank]@U[:,:rank].T
            E1=err@P0@err; E2=err@(C-P0)@err
            M=mu@mu/n; Mp=theta@theta/n
            V=sy2*(.02+Q)
            assert V<=err@C@err*(1+.04/(n-1))+1.06*M+Mp+1e-8
            second=sy2*y@PH@(np.eye(n)-PH)@y
            assert second<=2*Mp+.5*E1+1e-7
            assert sy2*Q>=E2-1e-7
            kapp=2*(.01+n/2)*(rho@rho)/(n*(.02+Q))
            bound=(1.02*sy2+2*Mp+.5*E1)/E2
            assert 1-kapp<=bound+1e-7
            assert n-1-rank>=n/2
            cnt+=1
note(f'V, rank-only sphere bounds: {cnt} cases PASS, including empty truth, exact rank deficiency, near singular truth, and n=3.')

# Existing numerical implementations: rerun only validation entry points.
import sys
sys.dont_write_bytecode=True
numerics=Path(__file__).resolve().parents[2]/'numerics'
sys.path.insert(0,str(numerics))
import b_check, a_sph, a_orth
b_check.F1(np.random.default_rng(20261112))
a_sph.V1(np.random.default_rng(20261113))
a_orth.V1(np.random.default_rng(20261111))
note('Existing F1, spherical V1, orthogonal V1 rerun; see stdout.txt for their printed errors.')
Path(__file__).with_name('results.txt').write_text('\n'.join(out)+'\n',encoding='utf-8')
