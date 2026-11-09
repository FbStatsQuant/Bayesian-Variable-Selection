import itertools
import numpy as np

def ts(alpha, K, a):
    # Algebraically identical stable form of a-log(1+u).
    b = alpha / (4*K)
    v = np.expm1(a)
    return np.log1p(b*v*v/(1+v+b*v))

rng = np.random.default_rng(20261109)
p = 8
pos = rng.permutation(np.array([0, 1, 3, 6, 7, 11, 12, 18]))
d = abs(pos[:,None]-pos[None,:])
off = ~np.eye(p,dtype=bool)
B = rng.uniform(-.3,.3,(p,p))*np.exp(-.4*d)
B = np.triu(B,1); B += B.T
T = B + np.diag(abs(B).sum(axis=1)+.8)
S = np.linalg.inv(T)
sd = np.sqrt(np.diag(S)); S /= np.outer(sd,sd)
T = np.linalg.inv(S)
c,C = np.linalg.eigvalsh(S)[[0,-1]]
lines=[]
for name,A,alpha,a in [('Sigma',S,c,.4),('Theta',T,1/C,.4)]:
    K = np.max(abs(A[off])*np.exp(a*d[off]))
    t=ts(alpha,K,a)
    Ai=np.linalg.inv(A)
    ratio=np.max(abs(Ai)*np.exp(t*d)/(2/alpha))
    series=2*K*(1/np.expm1(a-t)-1/np.expm1(a))
    assert abs(series-alpha/2)<1e-10
    assert ratio <= 1+1e-10
    t2=ts(1/C,2/c,t) if name=='Sigma' else ts(1/C,K,a)
    worst=0.; vmin=1.; vmax=0.
    for mask in range(1<<p):
        U=[i for i in range(p) if mask>>i&1]
        V=[i for i in range(p) if i not in U]
        if not V: continue
        Cv=np.linalg.inv(T[np.ix_(V,V)])
        ev=np.linalg.eigvalsh(Cv)
        assert ev[0]>=c-1e-10 and ev[-1]<=C+1e-10
        vmin=min(vmin,np.diag(Cv).min()); vmax=max(vmax,np.diag(Cv).max())
        dv=d[np.ix_(V,V)]
        oo=~np.eye(len(V),dtype=bool)
        if oo.any(): worst=max(worst,np.max(abs(Cv[oo])*np.exp(t2*dv[oo])/(2*C)))
        if U:
            schur=S[np.ix_(V,V)]-S[np.ix_(V,U)]@np.linalg.solve(S[np.ix_(U,U)],S[np.ix_(U,V)])
            assert np.max(abs(Cv-schur))<1e-10
    assert worst<=1+1e-10 and vmin>=c-1e-10 and vmax<=1+1e-10
    lines.append(f'{name}: CT ratio={ratio:.8g}, all 256 conditioning sets CD ratio={worst:.8g}, variance=[{vmin:.8g},{vmax:.8g}], c={c:.8g}, C={C:.8g}')

# Counterexample to global LSF(i) necessity, including LSF(ii).
n=10**8; delta=n**(-.25); r=(-1+delta)/4
S=np.eye(6); S[1:,1:]=(1-r)*np.eye(5)+r*np.ones((5,5))
anchored=min(np.linalg.eigvalsh(S[np.ix_([0]+list(J),[0]+list(J))])[0]
             for k in range(5) for J in itertools.combinations(range(1,6),k))
global5=np.linalg.eigvalsh(S[1:,1:])[0]
assert anchored>=.25-1e-10 and abs(global5-delta)<1e-10
lines.append(f'Necessity counterexample n={n}: anchored j0=4 floor={anchored:.8g}; five-null minimum={global5:.8g}; unnormalised full floor={(n-1)*delta:.8g}.')
print('\n'.join(lines))
