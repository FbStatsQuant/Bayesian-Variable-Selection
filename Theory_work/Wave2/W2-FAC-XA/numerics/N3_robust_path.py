"""Falsification of L2's conditional algebra; not an iid transfer experiment.
Only N3_robust_path_output.json is written. Twenty seeds total, imports read-only.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'W2-FAC-B' / 'numerics'
sys.path.insert(0, str(SOURCE))
import cs_core as cc


def run():
    hashes = {f: hashlib.sha256((SOURCE/f).read_bytes()).hexdigest()
              for f in ('cs_core.py',)}
    out = dict(seeds=list(range(20)), n=10**8, p=64, rho=.5,
               perturbation=.001, scans=0, safe_deletions=0, swaps=0,
               additions=0, truth_losses=0, endpoints_S0=0,
               finite_certificates_checked=0, finite_certificate_failures=0,
               aa_checks=0, aa_failures=0, reordered_deletions=0, max_direct_gain_error=0.,
               balance_checks=0, balance_failures=0, fuzzy_gap_checks=0, fuzzy_gap_failures=0,
               majority_checks=0, majority_failures=0,
               weighted_checks=0, max_weighted_identity_error=0.,
               geometry_not_proved=True, iid_gain_coupling_not_tested=True,
               oracle_errors_need_not_integrate_to_model_scores=True)
    records = []
    for seed in range(20):
        rng = np.random.default_rng(seed)
        p, n, zeta = out['p'], out['n'], out['perturbation']
        theta = np.r_[1., 1.3, np.zeros(p-2)]
        P = cc.CS(.5, theta, n, rng=rng)
        k1 = math.sqrt((n-1)*.5)/P.s
        kc = ((n-1)*.5*theta.sum()+math.sqrt((n-1)*.5)*P.eta)/P.s
        kap = P.al/P.be
        T = tuple(range(p))
        tags = []
        min_certificate_slack = math.inf
        for step in range(p+5):
            k = len(T)
            O = sorted(set(range(p))-set(T))
            nulls = [j for j in T if j>=2]
            q = k+kap
            centre = (sum(P.z[list(T)])/q-kc)/k1
            tau = (P.z-kc)/k1-centre
            zz = P.z[list(T)]
            quad = (zz@zz-zz.sum()**2/q)/P.al
            psi = .02+n-1-n*quad
            M = P.nu*n*k1*k1/(P.al*psi)
            # Compute Delta from the determinant/prior part only.
            def L(u):
                if u == 0:
                    return 0.
                return ((u-1)*math.log(P.al/P.al2)
                        +math.log((P.al+u*P.be)/(P.al2+u*P.be2)))
            def delta(u):
                return math.log((2*p-u)/u)+.5*(L(u)-L(u-1))
            c, b = M*q/(q-1), M*q/(q+1)
            FT = P.F(T)
            gains, targets, types = [], [], []
            for j in T:
                gains.append(delta(k)-P.nu*np.log1p(c*tau[j]**2/P.nu))
                targets.append(tuple(t for t in T if t!=j))
                types.append('-N' if j>=2 else '-T')
            if k<P.K:
                for l in O:
                    gains.append(-delta(k+1)-P.nu*np.log1p(-b*tau[l]**2/P.nu))
                    targets.append(tuple(sorted(T+(l,))))
                    types.append('+N')
            for j in T:
                for l in O:
                    v=tau[l]**2-tau[j]**2-(tau[l]-tau[j])**2/q
                    gains.append(-P.nu*np.log1p(-M*v/P.nu))
                    targets.append(tuple(sorted(tuple(t for t in T if t!=j)+(l,))))
                    types.append('swN' if j>=2 else 'swT')
            gains=np.array(gains)
            # Every candidate gets checked by direct F, for first 2 scans/seed.
            if step<2:
                errors=[abs(P.F(U)-FT-g) for U,g in zip(targets,gains)]
                out['max_direct_gain_error']=max(out['max_direct_gain_error'],max(errors))
            actual=gains+rng.uniform(-zeta,zeta,len(gains))
            best=int(np.argmax(actual))
            if nulls:
                d=min(abs(tau[j]) for j in nulls)
                R=max([abs(tau[l]) for l in O],default=0.)
                lower=delta(k)-c*d*d
                upper_add=(-delta(k+1)+b*R*R/(1-b*R*R/P.nu)
                           if O and k<P.K else -math.inf)
                v=max(0.,R*R-d*d)
                upper_swap=M*v/(1-M*v/P.nu) if O else -math.inf
                truth=max([g for g,tag in zip(gains,types) if tag in ('-T','swT')],default=-math.inf)
                if lower>zeta and lower-upper_add>2*zeta and lower-upper_swap>2*zeta and truth<-zeta:
                    out['finite_certificates_checked']+=1
                    out['finite_certificate_failures']+=int(actual[best]<=0 or types[best]!='-N')
                    min_certificate_slack=min(min_certificate_slack,lower-zeta,lower-upper_add-2*zeta,lower-upper_swap-2*zeta)
                if actual[best]>0 and types[best]=='-N':
                    out['reordered_deletions']+=int(best!=int(np.argmax(gains)))
                    j=next(j for j in T if j not in targets[best])
                    bound=d*d+np.expm1(2*zeta/P.nu)*(P.nu/c+d*d)
                    out['aa_checks']+=1
                    out['aa_failures']+=int(tau[j]**2>bound+1e-10)
            out['scans']+=1
            if actual[best]<=0:
                break
            tags.append(types[best])
            if types[best]=='-N': out['safe_deletions']+=1
            if types[best].startswith('sw'): out['swaps']+=1
            if types[best].startswith('+'): out['additions']+=1
            T=targets[best]
            if not {0,1}.issubset(T):
                out['truth_losses']+=1
                break
        out['endpoints_S0']+=int(T==(0,1))
        records.append(dict(seed=seed,moves=len(tags),endpoint=list(T),
                            min_certificate_slack=min_certificate_slack))

        # BAL: arbitrary two tails + up to 3 adversarial symmetric-difference points.
        for trial in range(100):
            xi=rng.normal(size=256)
            H=float(max(abs(xi)))
            a=-float(rng.uniform(.1,1.5)); b0=float(rng.uniform(.1,1.5))
            K0=set(np.flatnonzero((xi<=a)|(xi>=b0)))
            K=set(K0)
            changes=rng.choice(len(xi),size=3,replace=False)
            for j in changes:
                if j in K: K.remove(j)
                else: K.add(j)
            m=len(K); r=len(K.symmetric_difference(K0)); q=m+2+1.
            # Pick x inside (a,b), and set the anchor to make the centre exact.
            x=float(rng.uniform(a,b0)); B=q*x-sum(xi[list(K)])
            order=np.argsort(-abs(xi)); pref=np.cumsum(xi[order]); J=np.arange(1,len(xi)+1)
            neg=np.cumsum(xi[order]<0)
            lower=max(1,m-r)
            beta=max(float(max(abs(pref[lower-1:])/(J[lower-1:]*H))),
                     float(max(abs(neg[lower-1:]/J[lower-1:]-.5))))
            if beta>=.5: continue
            delta0=abs(a+b0-2*x)
            bound=max(delta0/2,(abs(B)+beta*H*(m+r)/(.5-beta)+r*H)/q)
            out['balance_checks']+=1
            out['balance_failures']+=int(abs(x)>bound+1e-11)
            w=.05
            Kband=set(K0)
            band=np.flatnonzero((abs(xi-a)<=w)|(abs(xi-b0)<=w))
            for j in band[::2]:
                if j in Kband: Kband.remove(j)
                else: Kband.add(j)
            xb=(a+b0)/2
            deleted=set(range(len(xi)))-Kband
            if Kband and deleted:
                d=min(abs(xi[j]-xb) for j in Kband)
                R=max(abs(xi[j]-xb) for j in deleted)
                out['fuzzy_gap_checks']+=1
                out['fuzzy_gap_failures']+=int(R>d+abs(a+b0-2*xb)+2*w+1e-11)

        # MAJ/MG: synthetic tail configurations, both signs, variable q and anchor.
        for trial in range(100):
            m=int(rng.integers(2,60)); nplus=int(rng.integers(0,m+1)); I=2*nplus-m
            H=8.; w=1e-5; B=float(rng.uniform(-.01,.01)); q=m+2+1.
            values=np.r_[H-rng.uniform(0,w,nplus),-H+rng.uniform(0,w,m-nplus)]
            x=(B+values.sum())/q; e=abs(B)+m*w
            if not I or not nplus or nplus==m: continue
            sign=1 if I>0 else -1
            majority=(values*sign>0)
            tau2=(values-x)**2
            gap=float(min(tau2[~majority])-min(tau2[majority]))
            Jgap=(2*(H-e)/q-w)*(2*H-w)
            c=.5*q/(q-1); nu=5e5
            costs=nu*np.log1p(c*tau2/nu)
            gain_gap=float(min(costs[~majority])-min(costs[majority]))
            MG=c*Jgap/(1+4*c*H*H/nu)
            out['majority_checks']+=1
            out['majority_failures']+=int(gap<Jgap-1e-10 or gain_gap<MG-1e-10)

        # Exact finite-n unequal loading Schur loss and centre update identities.
        for trial in range(20):
            size=12; nn=100.; lam=rng.uniform(.3,.9,size)
            A=(nn*nn-1)*(1-lam*lam)+1
            v=math.sqrt(nn*nn-1)*lam/np.sqrt(A); u=rng.normal(size=size)
            Hmat=np.diag(A)+(nn*nn-1)*np.outer(lam,lam)
            z=np.sqrt(A)*u
            base=float(z@np.linalg.solve(Hmat,z))
            C=float(v@u/(1+v@v)); j=int(rng.integers(size)); keep=np.arange(size)!=j
            reduced=float(z[keep]@np.linalg.solve(Hmat[np.ix_(keep,keep)],z[keep]))
            predicted=(u[j]-v[j]*C)**2/(1-v[j]*v[j]/(1+v@v))
            Cnew=float(v[keep]@u[keep]/(1+v[keep]@v[keep]))
            predicted_C=C-v[j]*(u[j]-v[j]*C)/(1+v@v-v[j]*v[j])
            out['max_weighted_identity_error']=max(out['max_weighted_identity_error'],
                                                    abs(base-reduced-predicted),abs(Cnew-predicted_C))
            out['weighted_checks']+=1
    out['runs']=records
    out['source_hashes']=hashes
    out['source_hashes_unchanged']=all(hashlib.sha256((SOURCE/f).read_bytes()).hexdigest()==h for f,h in hashes.items())
    # The exact-hole implication fails at any positive nearest-distance tolerance.
    out['exact_hole_counterexample']=dict(x=0.,kept=[.1,.1001,2.],
        epsilon=.001,allowed_deleted=.1001,retained_in_deleted_hull=.1,
        meaning='deleted interval containing x and .1001 must contain retained .1')
    failures=sum(out[key] for key in ('finite_certificate_failures','aa_failures','balance_failures','fuzzy_gap_failures','majority_failures'))
    assert failures==0
    # Direct F subtracts numbers of order n log n; stable gains use log1p.
    assert out['max_direct_gain_error']<2e-5
    assert out['max_weighted_identity_error']<1e-10
    assert out['source_hashes_unchanged']
    (HERE/'N3_robust_path_output.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))


if __name__=='__main__':
    run()
