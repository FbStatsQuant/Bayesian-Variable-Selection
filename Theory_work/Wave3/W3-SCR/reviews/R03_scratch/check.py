import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import itertools, math
import numpy as np

rng = np.random.default_rng(3109703)
counts = dict(models=0, additions=0, bridges=0, dadd=0, selfadd=0)
worst = 0.0
for n in (3, 4, 7, 15):
    for p in (1, 2, 5):
        for duplicate in (False, True):
            X = rng.normal(size=(n,p)); X -= X.mean(axis=0)
            X *= np.sqrt(n-1)/np.linalg.norm(X,axis=0)
            if duplicate and p > 1:
                X[:,1] = X[:,0]
            theta = rng.normal(size=p)
            theta[::2] *= -3
            mu = X @ theta
            sig = 0.7
            yc = mu + sig*rng.normal(size=n); yc -= yc.mean()
            tau2 = yc@yc/(n-1); y = yc/np.sqrt(tau2)
            lam = 1/(n+1); nu = n/2+.01
            K = min(p,n//2)
            def quantities(S):
                A = X[:,S]; G = A.T@A
                R = np.eye(n)-A@np.linalg.solve(G+lam*np.eye(len(S)),A.T)
                Q = y@y-n*(A.T@y)@np.linalg.solve((n+1)*G+np.eye(len(S)), A.T@y)
                F = -math.log(2)-math.log(math.comb(2*p-1,len(S)))-.5*np.linalg.slogdet((n+1)*G+np.eye(len(S)))[1]+.5*np.linalg.slogdet(G+np.eye(len(S)))[1]-nu*math.log(.02+Q)
                return R,Q,F
            for k in range(K):
                for St in itertools.combinations(range(p),k):
                    S=list(St); R,Q,F=quantities(S); counts['models']+=1
                    assert (n-1)/(n+1)-1e-9 <= Q <= n-1+1e-9
                    T=[t for t in range(p) if t not in S]
                    gains=[]
                    for t in T:
                        Rt,Qt,Ft=quantities(S+[t]); a=X[:,t]@R@X[:,t]+lam
                        A=X[:,S]; G=A.T@A
                        a1=n-(X[:,t]@A)@np.linalg.solve(G+np.eye(k),A.T@X[:,t])
                        D=(n+1)*a/a1; gy=(X[:,t]@R@y)**2/a
                        assert 1-1e-9 <= D <= n+1+1e-9
                        err=abs((Q-Qt)-n/(n+1)*gy)
                        worst=max(worst,err); assert err < 1e-7
                        predicted=-math.log((2*p-1-k)/(k+1))-.5*math.log(D)+nu*math.log((.02+Q)/(.02+Qt))
                        assert abs((Ft-F)-predicted)<1e-7
                        assert np.linalg.norm(Rt-(R-np.outer(R@X[:,t],R@X[:,t])/a))<1e-7
                        Tn=(1+1/n)*(2*math.log(2*p-1)+math.log(n+1))
                        if gy>=Tn:
                            assert Ft>F; counts['dadd']+=1
                        rhobar=(2*math.log(2*p-1)+math.log(n+1))/(n+.02)
                        qyc=tau2*Q
                        if gy*tau2>=rhobar*(n+1)/n*(.02*tau2+qyc):
                            assert Ft>F; counts['selfadd']+=1
                        gains.append((X[:,t]@R@mu)**2/a)
                        counts['additions']+=1
                    A=X[:,S]; residual=mu-A@np.linalg.lstsq(A,mu,rcond=None)[0]
                    delta=residual@residual; c=np.linalg.norm(theta)/np.sqrt(n+1)
                    if np.sqrt(delta)>=c:
                        bound=delta*(np.sqrt(delta)-c)**2/(n*np.abs(theta[T]).sum()**2)
                        assert max(gains)+1e-8>=bound
                        counts['bridges']+=1
                    Z=X[:,T]-A@np.linalg.lstsq(A,X[:,T],rcond=None)[0]
                    kap=max(0,np.linalg.eigvalsh(Z.T@Z).min()/(n-1))
                    b=np.abs(theta).min()
                    if kap>1e-10 and np.sqrt(kap*(n-1))*b>=2*c:
                        bound=(n-1)**2/n*kap**2*b*b/(4*sig*sig+9*kap*p*b*b)
                        actual=max(gains)/(sig*sig+mu@R@mu/(n-1))
                        assert actual+1e-8>=bound
print(counts)
print('maximum quadratic decrement error:',worst)
