"""Read-only falsification checks for the R03 L0/L1/L2 review. Run with python -B."""
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "Theory_work/Wave2/W2-FAC-PK/numerics"))
import numpy as np
from scipy.special import gammaln
import cs_core as cc


def exact_checks():
    summary = []
    for rho, sigma2 in [(0.2, 0.7), (0.95, 2.3)]:
        n, p = 14, 13  # p = n-1: zero residual degrees of freedom for the full design.
        theta = np.zeros(p)
        theta[[0, 1, 2]] = [1.4, -1.0, 1.8]
        P = cc.CS(rho, theta, n, sigma2=sigma2, rng=np.random.default_rng(19))
        K = P.K
        Sigma = (1-rho)*np.eye(p) + rho*np.ones((p,p))
        scores = {}
        direct_error = 0.0
        for k in range(K+1):
            for T in itertools.combinations(range(p), k):
                if k:
                    G = (n-1)*Sigma[np.ix_(T,T)]
                    H = (n+1)*G + np.eye(k)
                    z = P.z[list(T)]
                    Q = n-1-n*float(z@np.linalg.solve(H,z))
                    L = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G+np.eye(k))[1]
                else:
                    Q, L = n-1, 0.0
                scores[T] = float(P.lw[k] - .5*L - P.nu*math.log(.02+Q))
                direct_error = max(direct_error, abs(scores[T]-P.F(T)))
        gain_error = 0.0
        center_error = 0.0
        cases = {"missing_truth": 0, "contains_truth": 0}
        n_gains = 0
        for T in itertools.combinations(range(p), K):
            Ts = set(T)
            idx = list(T)
            outside = [j for j in range(p) if j not in Ts]
            B = float(P.z[idx].sum())
            A = float(P.z[idx]@P.z[idx])
            gam = lambda k: P.be/(P.al+k*P.be)
            t = P.z-gam(K)*B
            psi = .02+n-1-n*(A-gam(K)*B*B)/P.al
            def L(k):
                if k == 0:
                    return 0.0
                return ((k-1)*math.log(P.al/P.al2)
                        + math.log((P.al+k*P.be)/(P.al2+k*P.be2)))
            Delta = math.log((2*p-K)/K)+.5*(L(K)-L(K-1))
            for j in T:
                U = tuple(sorted(Ts-{j}))
                gain = Delta-P.nu*math.log1p(n*(1+gam(K-1))*t[j]**2/(P.al*psi))
                gain_error = max(gain_error,abs(scores[U]-scores[T]-gain))
                n_gains += 1
                for ell in outside:
                    U = tuple(sorted((Ts-{j})|{ell}))
                    V = t[ell]**2-t[j]**2-gam(K)*(t[ell]-t[j])**2
                    gain = -P.nu*math.log1p(-n*V/(P.al*psi))
                    gain_error = max(gain_error,abs(scores[U]-scores[T]-gain))
                    n_gains += 1
            has_truth = set(P.S0) <= Ts
            cases["contains_truth" if has_truth else "missing_truth"] += 1
            if has_truth:
                sig = math.sqrt(sigma2)
                k1 = sig*math.sqrt((n-1)*(1-rho))/P.s
                lam = (n-1)*(1-rho)/P.s
                varrho = (math.sqrt(n-1)*rho*theta.sum()/(sig*math.sqrt(1-rho))
                           + math.sqrt(rho/(1-rho))*P.al*P.eta)/P.be
                x = (P.xi[idx].sum()-varrho)/(K+P.al/P.be)
                center_error = max(center_error,float(np.max(np.abs(t-(k1*(P.xi-x)+lam*theta)))))
        assert direct_error < 1e-9 and gain_error < 1e-9 and center_error < 1e-9
        summary.append(dict(rho=rho,sigma2=sigma2,n=n,p=p,K=K,sets=len(scores),
                            size_K_cases=cases,gains_checked=n_gains,
                            max_score_error=direct_error,max_gain_error=gain_error,
                            max_center_error=center_error))
    return summary


def population_checks():
    # Work with the exact 0.02-adjusted population term, dropping the linear
    # determinant penalty (its second differences are O(1/n)).
    worst = -math.inf
    checks = 0
    for rho in [.001,.05,.2,.5,.95,.999]:
        for A in [.0001,.01,.2,.8,.9999]:
            for n in [10**4,10**8]:
                kappa = (1-rho)/rho+1/(rho*(n*n-1))
                u = np.arange(17,dtype=float)
                population = -(n/2+.01)*np.log(.02+(n-1)*(1-A*u/(u+kappa)))
                dd = np.diff(population, n=2)
                # Subtracting the shared constant first avoids cancellation
                # when the curvature is tiny.
                h = -(n/2+.01)*np.log1p(-(n-1)*A*u/((.02+n-1)*(u+kappa)))
                assert np.max(np.diff(h,n=2)) < 0
                worst = max(worst,float(np.max(np.diff(h,n=2))))
                checks += 15
    return dict(second_differences_checked=checks,max_second_difference=worst)


def inspect_existing():
    base=ROOT/"Theory_work/Wave2/W2-FAC-PK/numerics"
    rows=[json.loads(s) for s in (base/"L12_check.jsonl").read_text().splitlines() if s.strip()]
    l1=[r for r in rows if r.get("test")=="L1"]
    l2=[r for r in rows if r.get("test")=="L2"]
    chains=[json.loads(s) for s in (base/"L2_chain.jsonl").read_text().splitlines() if s.strip()]
    return dict(l1_rows=len(l1),l1_all_pass=all(r['a_size_is_K'] and r['b_order'] and r['c_spread']<=1 and r['d_no_full'] for r in l1),
                l2_rows=len(l2),l2_del_all_pass=all(r['i_del_le_DeltaK'] for r in l2),
                l2_missing_truth_rows=sum(not r['S0_in_T'] for r in l2),
                l2_extreme_outside_rows=sum(r['extreme_outside'] for r in l2),
                chain_rows=len(chains),
                chain_x_all_pass=all(abs(r['xT'])<=2 for r in chains),
                chain_j_all_pass=all(r['min_abs_tau_ret']<=3.5 for r in chains),
                chain_M_all_pass=all(r['MT']>=r['MT_bound'] for r in chains))


print(json.dumps(dict(exact=exact_checks(),population=population_checks(),existing=inspect_existing()),indent=2))
