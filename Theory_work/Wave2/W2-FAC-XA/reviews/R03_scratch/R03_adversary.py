"""R03 scratch: worst-case (adversarial) oracle paths for L2's UP(zeta) hypothesis.

The reference is FAC-B's exact-CS problem (cs_core, imported read-only, no bytecode).
At each state every move whose reference gain g satisfies g >= max_ref - 2*zeta and
g + zeta > 0 can be made the actual winner by some per-scan perturbation |e|<=zeta.
The adversary (i) takes any feasible UNSAFE move (truth move, addition, swap) if one
exists, else (ii) picks a feasible null deletion by a policy:
  push  : maximise the signed centre x_new (pushes the centre to +),
  far   : delete the feasible null with the LARGEST |tau| (creates left-behinds),
  exact : reference argmax (zeta irrelevant; control).
Records: endpoint, unsafe moves, max |x|/Hbar on bulk states (m >= m_e),
retained-magnitude spread at end-phase entry, entry |I|/q, and the L2 bulk
relaxed margin check (see review section 5.3).
Per-scan oracle perturbations need not integrate to a score; this is a SUPERSET
of UP(zeta) adversaries, so survival is evidence and failure is only suggestive.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, math
import numpy as np

SOURCE = Path(r'C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-FAC-B/numerics')
sys.path.insert(0, str(SOURCE))
import cs_core as cc

RHO = .5


def run_path(P, zeta, policy, m_e):
    n, p = P.n, P.p
    k1 = math.sqrt((n-1)*(1-RHO))/P.s
    kc = ((n-1)*RHO*P.theta.sum()+math.sqrt((n-1)*RHO)*P.eta)/P.s
    kap = P.al/P.be
    nu = P.nu
    S0 = set(P.S0)
    inT = np.ones(p, bool)
    isnull = np.ones(p, bool); isnull[list(S0)] = False
    Hbar = math.sqrt(2*math.log(2*(p-len(S0))+2)+2*math.log(math.log(n)))
    def L(u):
        if u == 0: return 0.
        return (u-1)*math.log(P.al/P.al2)+math.log((P.al+u*P.be)/(P.al2+u*P.be2))
    def delta(u):
        return math.log((2*p-u)/u)+.5*(L(u)-L(u-1))
    rec = dict(unsafe=None, max_bulk_x_over_H=0., min_relaxed_margin_over_logn=math.inf,
               entry=None, moves=0)
    zs = P.z
    for step in range(p+2):
        idx = np.flatnonzero(inT); out = np.flatnonzero(~inT)
        k = len(idx); q = k+kap; m = k-len(S0)
        zz = zs[idx]
        tau = (zs - zz.sum()/q)/k1        # centre-relative, truths include signal
        # centre in xi-units: x_T with tau_j = xi_j - x_T for nulls
        jn = idx[isnull[idx]][0] if m > 0 else (out[0] if len(out) else None)
        x = (P.xi[jn]-tau[jn]) if jn is not None else 0.
        quad = (zz@zz-zz.sum()**2/q)/P.al
        psi = .02+n-1-n*quad
        M = nu*n*k1*k1/(P.al*psi)
        c, b = M*q/(q-1), M*q/(q+1)
        # vectorised gains
        gdel = delta(k)-nu*np.log1p(c*tau[idx]**2/nu)
        tdel = np.where(isnull[idx], 0, 1)          # 0 null, 1 truth
        gadd = (-delta(k+1)-nu*np.log1p(-b*tau[out]**2/nu)) if (len(out) and k < P.K) else np.array([])
        if len(out):
            tl = tau[out]; ends = np.array([tl.max(), tl.min()])
            tj = tau[idx][:, None]
            V = ends[None, :]**2-tj**2-(ends[None, :]-tj)**2/q
            gsw = (-nu*np.log1p(-M*V/nu)).max(axis=1)
        else:
            gsw = np.array([])
        G = max(gdel.max(), gadd.max() if len(gadd) else -math.inf, gsw.max() if len(gsw) else -math.inf)
        thr = lambda g: (g >= G-2*zeta) & (g+zeta > 0)
        fdel = thr(gdel); fadd = thr(gadd) if len(gadd) else np.array([], bool)
        fsw = thr(gsw) if len(gsw) else np.array([], bool)
        if m >= m_e:
            rec['max_bulk_x_over_H'] = max(rec['max_bulk_x_over_H'], abs(x)/Hbar)
            bd = gdel[tdel == 0].max()
            oth = max(gadd.max() if len(gadd) else -math.inf,
                      gsw[tdel == 0].max() if len(gsw) else -math.inf)
            rec['min_relaxed_margin_over_logn'] = min(rec['min_relaxed_margin_over_logn'], float(bd-oth)/math.log(n))
        if m == m_e-1 and rec['entry'] is None:
            kept = idx[isnull[idx]]
            I = int((P.xi[kept] > 0).sum()-(P.xi[kept] < 0).sum())
            rec['entry'] = dict(I_over_q=abs(I)/q, min_kept_abs_over_H=float(abs(P.xi[kept]).min()/Hbar),
                                x_over_H=x/Hbar)
        if not (fdel.any() or fadd.any() or fsw.any()):
            break
        if (fdel & (tdel == 1)).any() or fadd.any() or fsw.any():
            typ = 'delT' if (fdel & (tdel == 1)).any() else ('add' if fadd.any() else 'swap')
            rec['unsafe'] = dict(type=typ, m=m)
            break
        cands = idx[fdel]
        if policy == 'exact':
            j = idx[int(np.argmax(np.where(tdel == 0, gdel, -np.inf)))]
        elif policy == 'push':
            j = cands[int(np.argmin(tau[cands]))]          # x_new = x - tau_j/(q-1)
        else:
            j = cands[int(np.argmax(np.abs(tau[cands])))]
        choice = (None, None, j)
        inT[choice[2]] = False
        rec['moves'] += 1
    rec['endpoint_S0'] = set(np.flatnonzero(inT)) == S0
    rec['m0'] = p-len(S0)
    return rec


def main():
    results = []
    for p in (1000, 4000):
        for seed in range(3):
            rng = np.random.default_rng(1000+seed)
            P = cc.CS(RHO, np.r_[1., 1.3, np.zeros(p-2)], 10**12, rng=rng)
            for zeta in (0., .01, .1, .3, 1., 3., 10.):
                for policy in (('exact',) if zeta == 0 else ('push', 'far')):
                    r = run_path(P, zeta, policy, m_e=20)
                    r.update(p=p, seed=1000+seed, zeta=zeta, policy=policy)
                    results.append(r)
                    print(json.dumps(r), flush=True)
    Path(__file__).with_name('R03_adversary_out.json').write_text(json.dumps(results, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
