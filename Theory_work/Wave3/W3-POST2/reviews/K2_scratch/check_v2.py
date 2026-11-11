"""Independent small falsification checks; no repository imports or bytecode writes."""
import itertools
import math
import numpy as np
from scipy.special import gammaln
from scipy.integrate import quad

rng = np.random.default_rng(72123)
worst_f, worst_curv, min_den_ratio = 0., 0., float('inf')
for n in [16, 17, 32, 100, 1000, 10000]:
    N = n-1
    for ep in np.linspace(0, 2*N, 41):
        us = np.linspace(1, 1+1/math.sqrt(n), 301) if ep >= N else np.linspace(1-1/math.sqrt(n), 1, 301)
        fs = -N/2*np.log(us)+ep/2*(1-1/us)
        worst_f = min(worst_f, float(fs.min()))
        worst_curv = max(worst_curv, float(np.max(np.abs(N/(2*us**2)-ep/us**3)))/N)
        assert fs.min() >= -3-1e-9
        assert np.max(np.abs(N/(2*us**2)-ep/us**3)) <= 6*N+1e-9
        if n <= 100:
            # sigma^2=1, M=2, phi0=1/2: rhobar=6, bplus=.07.
            rho, a, b = 6., .51, .07
            logig = lambda u: a*math.log(b)-gammaln(a)-(a+1)*math.log(u)-b/u
            # IG has a single maximum; minimum on the compact interval is at an endpoint.
            igmin = math.exp(min(logig(.5), logig(2)))
            val = quad(lambda u: math.exp(-N/2*math.log(u)+ep/2*(1-1/u)-rho/(2*u)+logig(u)), us[0], us[-1], epsabs=1e-13)[0]
            ratio = val/(igmin*math.exp(-3-rho)/math.sqrt(n))
            min_den_ratio = min(min_den_ratio, ratio)
            assert ratio >= 1-1e-8

checks = 0
max_identity_error = 0.
min_mean_slack = float('inf')
min_gain_slack = float('inf')
for n in [16, 32, 100]:
    N, p = n-1, 6
    for kind in ['regular', 'duplicate', 'near_duplicate', 'dependent']:
        for rep in range(10):
            X = rng.normal(size=(N,p))
            if kind == 'duplicate': X[:,3] = X[:,0]
            if kind == 'near_duplicate': X[:,3] = X[:,0]+1e-7*X[:,3]
            if kind == 'dependent': X[:,3] = X[:,0]+X[:,1]
            X *= math.sqrt(N)/np.linalg.norm(X,axis=0)
            mu = X[:,:2] @ rng.normal(size=2)
            e = rng.normal(size=N)
            y = mu+e
            def mats(s):
                if not s: return np.zeros((N,N)), np.zeros((N,N))
                Z = X[:,s]
                # SVD avoids cancellation in inversion at exact rank loss.
                u,d,_ = np.linalg.svd(Z, full_matrices=False)
                h = n*d*d/((n+1)*d*d+1)
                M = (u*h)@u.T
                P = u[:,d>1e-10]@u[:,d>1e-10].T
                return M,P
            M0,P0 = mats((0,1))
            gamma = (1+1/np.linalg.eigvalsh(X[:,:2].T@X[:,:2]).min())/(n+1)
            R = gamma*np.linalg.norm(P0@y)**2
            for k in range(p+1):
                for s in itertools.combinations(range(p),k):
                    M,P = mats(s)
                    a = (np.eye(N)-M)@mu
                    L = float(mu@a)
                    Q = float(y@(y-M@y))
                    decomp = e@e-e@M@e+2*e@a+L
                    err = abs(Q-decomp)
                    max_identity_error = max(max_identity_error,err)
                    assert err < 1e-8
                    assert a@a <= L+1e-8
                    slack = 2*np.linalg.norm(P@e)**2+2*L-np.linalg.norm(M@y-mu)**2
                    min_mean_slack = min(min_mean_slack,slack)
                    assert slack >= -1e-8
                    sp = tuple(sorted(set(s)|{0,1}))
                    Mp,Pp = mats(sp)
                    gain = Q-float(y@(y-Mp@y))
                    lower = L-2*abs(e@a)-np.linalg.norm((Pp-P0)@e)**2-R
                    min_gain_slack = min(min_gain_slack,gain-lower)
                    assert gain >= lower-1e-8
                    checks += 1
print('Taylor minimum F:',worst_f,'maximum |Fsecond|/N:',worst_curv)
print('Minimum C1 window integral / claimed lower bound:',min_den_ratio)
print('D1/E1 model checks:',checks,'maximum decomposition error:',max_identity_error)
print('Minimum D1(b) slack:',min_mean_slack,'minimum E1 gain slack:',min_gain_slack)
