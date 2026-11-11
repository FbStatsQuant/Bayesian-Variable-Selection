"""Adversarial finite enumeration; run from repository root with py -3.13 -B -I."""
import importlib.util
import math
from pathlib import Path
import numpy as np

root = Path.cwd()
spec = importlib.util.spec_from_file_location('post2', root / 'Theory_work/Wave3/W3-POST2/numerics/post2_checks.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rng = np.random.default_rng(931771)
count = 0
min_den_slack = float('inf')
max_theta = 0.0
max_q_violation = -float('inf')
max_transfer_logratio = -float('inf')
for n in [8, 30, 100, 1000]:
    N, p = n-1, 4
    for kind in ['iid', 'duplicates', 'near_collinear']:
        X = mod.stdcols(rng.normal(size=(n,p)))
        if kind == 'duplicates':
            X[:,1] = X[:,0]
        if kind == 'near_collinear':
            X[:,1] = X[:,0] + 1e-3 * X[:,1]
            X = mod.stdcols(X)
        z = rng.normal(size=n); z -= z.mean()
        z -= X @ np.linalg.lstsq(X,z,rcond=None)[0]
        z /= np.linalg.norm(z)
        for T in [(), (0,), (0,1)]:
            vt = np.array([0.7,-0.7][:len(T)])
            fit = X[:,T] @ vt if T else np.zeros(n)
            for residual_norm in [0.0, 1.0, 3.0]:
                mu = fit + residual_norm*z
                r = mu-fit
                B = float(r@r + (fit@fit+vt@vt)/n)
                M = float(mu@mu/n)
                bm = 0.005
                bp = .01*(2*(1+M)+1)
                a = .51
                def logig(v):
                    return a*math.log(bp)-math.lgamma(a)-(a+1)*math.log(v)-bp/v
                logcig = min(logig(1),logig(2))
                kappa = (bp/bm)**a
                for rep in range(20):
                    eps = rng.normal(size=n)
                    e = eps-eps.mean()
                    yr = mu+eps
                    y, sy = mod.stdy(yr)
                    P = mod.Post(X,y)
                    iT = P.index[T]
                    E = float(e@e)
                    excess = B+2*abs(float(eps@r))
                    Qc = P.Q*sy**2
                    max_q_violation = max(max_q_violation, Qc[iT]-E-excess)
                    Lam = abs(E-N)/(2*math.sqrt(n))+E/(2*n)+excess/2
                    # Exact closed form, contrast density divided by true Gaussian density.
                    logmc = (-N/2*math.log(2*math.pi)+a*math.log(bp)
                             +math.lgamma(P.nu)-math.lgamma(a)-P.logD[iT]/2
                             -P.nu*math.log(bp+Qc[iT]/2))
                    logf0 = -N/2*math.log(2*math.pi)-E/2
                    loglower = -P.logD[iT]/2+logcig-.5*math.log(n)-Lam
                    min_den_slack = min(min_den_slack,logmc-logf0-loglower)
                    logmc_minus = (-N/2*math.log(2*math.pi)+a*math.log(bm)
                                   +math.lgamma(P.nu)-math.lgamma(a)-P.logD/2
                                   -P.nu*np.log(bm+Qc/2))
                    for m in range(-1,P.K):
                        mask = P.size>m
                        tail = float(P.pi[mask].sum())
                        R = sum(math.comb(p,k)*math.exp(P.logw[k]-P.logw[len(T)])
                                for k in range(max(m+1,0),P.K+1))
                        A = R*math.exp(P.logD[iT]/2)*math.sqrt(n)
                        max_theta = max(max_theta,tail/A)
                        if .5 <= sy**2 <= 2*(1+M)+1:
                            logs = P.logw[ P.size[mask] ]+logmc_minus[mask]
                            mx = float(logs.max())
                            logsum = mx+math.log(float(np.exp(logs-mx).sum()))
                            logbound = 2*math.log(kappa)+logsum-P.logw[len(T)]-logmc
                            max_transfer_logratio = max(max_transfer_logratio,math.log(tail)-logbound)
                    count += 1
print(f'draws={count}; all cutoffs -1 <= m < K; sigma*=1; seeds=931771')
print(f'max Qc_T-(E+excess)={max_q_violation:.9g} (must <=0)')
print(f'min log(exact denominator/lower bound)={min_den_slack:.9g} (must >=0)')
print(f'max log(posterior tail/mixed endpoint bound)={max_transfer_logratio:.9g} (must <=0)')
print(f'max Theta={max_theta:.9g}; empirical support only, not a tail-law proof')
