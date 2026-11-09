import sys
sys.dont_write_bytecode = True
from pathlib import Path
import math, json, hashlib
import numpy as np
ROOT = Path.cwd()
PK = ROOT / 'Theory_work/Wave2/W2-FAC-PK'
OUT = PK / 'reviews/R08_scratch'
rng = np.random.default_rng(8179)
max_gain_error = 0.0
checks = 0
for rho in (0.2, 0.8):
    n, p = 24, 23
    S = (1-rho)*np.eye(p)+rho*np.ones((p,p))
    Z = rng.normal(size=(n,p)); Z -= Z.mean(axis=0)
    O = np.linalg.qr(Z)[0]
    X = math.sqrt(n-1)*O@np.linalg.cholesky(S).T
    th = np.zeros(p); th[[0,4]] = [1.1,-0.7]
    eps = rng.normal(size=n); eps -= eps.mean()
    Y = X@th+eps; y=Y/math.sqrt(Y@Y/(n-1))
    z = X.T@y; G=X.T@X; nu=n/2+0.01
    alpha=(n*n-1)*(1-rho)+1; beta=(n*n-1)*rho
    def score(T):
        T=sorted(T); k=len(T)
        lw = math.lgamma(k+1)+math.lgamma(2*p-k)-math.lgamma(2*p)
        if not T: return lw-nu*math.log(0.02+y@y)
        A=G[np.ix_(T,T)]; H=(n+1)*A+np.eye(k)
        L=np.linalg.slogdet(H)[1]-np.linalg.slogdet(A+np.eye(k))[1]
        q=y@y-n*z[T]@np.linalg.solve(H,z[T])
        return lw-L/2-nu*math.log(0.02+q)
    for k in (1,2,5,12):
        for _ in range(5):
            T=set(rng.choice(p,k,replace=False).tolist()); ts=sorted(T)
            gam=beta/(alpha+k*beta); B=z[ts].sum()
            t=z-gam*B
            quad=(z[ts]@z[ts]-gam*B*B)/alpha
            psi=0.02+n-1-n*quad
            def L(u):
                if not u:return 0.0
                ap=(n-1)*(1-rho)+1; bp=(n-1)*rho
                return (u-1)*math.log(alpha/ap)+math.log((alpha+u*beta)/(ap+u*bp))
            def delta(u):return math.log((2*p-u)/u)+(L(u)-L(u-1))/2
            f=score(T)
            for j in sorted(T):
                gd=delta(k)-nu*math.log1p(n*(1+beta/(alpha+(k-1)*beta))*t[j]**2/(alpha*psi))
                max_gain_error=max(max_gain_error,abs(score(T-{j})-f-gd)); checks+=1
                for l in sorted(set(range(p))-T):
                    v=t[l]**2-t[j]**2-gam*(t[l]-t[j])**2
                    gs=-nu*math.log1p(-n*v/(alpha*psi))
                    max_gain_error=max(max_gain_error,abs(score(T-{j}|{l})-f-gs)); checks+=1
            if k<n//2:
                for l in sorted(set(range(p))-T):
                    ga=-delta(k+1)-nu*math.log1p(-n*(1-beta/(alpha+(k+1)*beta))*t[l]**2/(alpha*psi))
                    max_gain_error=max(max_gain_error,abs(score(T|{l})-f-ga)); checks+=1
print(json.dumps({'direct_neighbor_checks':checks,'max_gain_error':max_gain_error}))
assert max_gain_error<1e-9
# REPORT G1: an orthogonal extra with zero response inner product has no likelihood change.
n,p,rho=101,60,0.5
f=lambda lam: math.log(((n*n-1)*lam+1)/((n-1)*lam+1))
cs_L2=f(1-rho)+f(1+rho)
excess=0.5*(2*math.log(n)-cs_L2)
print(json.dumps({'G1_exact_budget_excess_orthogonal_over_CS':excess,'positive':excess>0}))
assert excess>0
# REPORT G2: K orthogonal planes, n angular dictionary columns in each, p=Kn.
# First selected column is the fixed truth; other planes use their nearest grid direction.
n=1001; K=(n-1)//2; ratios=[]; upper_violations=0
for seed in range(20):
    e=np.random.default_rng(seed).normal(size=(K,2))
    theta=np.mod(np.arctan2(e[:,1],e[:,0]),math.pi)
    theta_hat=np.round(theta*n/math.pi)*math.pi/n
    r2=np.sum(e*e,axis=1)
    rss=e[0,1]**2+np.sum(r2[1:]*np.sin(theta[1:]-theta_hat[1:])**2)
    bound=e[0,1]**2+(math.pi/(2*n))**2*np.sum(r2[1:])
    upper_violations+=int(rss>bound+1e-12)
    ratios.append(rss/n)
print(json.dumps({'G2_dictionary_n':n,'p':K*n,'seeds':20,'max_RSS_over_n':max(ratios),'bound_violations':upper_violations}))
assert upper_violations==0
for filename in ('N1_raw.jsonl','N3_raw_final360.jsonl'):
    rows=[json.loads(l) for l in (PK/'numerics'/filename).read_text(encoding='utf-8-sig').splitlines() if l.strip()]
    print(json.dumps({'file':filename,'rows':len(rows),'first_row_keys':list(rows[0])}))
# Read and execute only citecheck's registry/loop, redirecting its documented output to this seat's scratch.
src=(PK/'reviews/citecheck.py').read_text(encoding='utf-8-sig')
src=src.replace('os.path.join(os.path.dirname(__file__), "CITECHECK.txt")','os.path.join(os.path.dirname(__file__), "R08_scratch/CITECHECK_rerun.txt")')
exec(compile(src,str(PK/'reviews/citecheck.py'),'exec'),{'__file__':str(PK/'reviews/citecheck.py')})
