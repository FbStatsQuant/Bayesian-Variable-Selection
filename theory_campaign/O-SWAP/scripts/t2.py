"""Predictor T2 (REPORT Prop. 6): one-move posterior-miss probability with the two dominant
dependencies handled exactly (under PA):
  * the common residual E (chi2_{n-1-s0}) shared by all one-move events -> outer integral over E;
  * for each truth j, the shared coordinate A_j of drop_j and all swaps (j,l):
      B_jl = rho_jl A_j + sqrt(1-rho_jl^2) Z_jl,  Z_jl ~ N(0,1) independent of A_j  -> integral over A_j.
Remaining approximations (stated in the report): Z_jl independent across l given (A_j, E); clusters
(truths j; the add block) independent given E; ||v||^2 ~ A^2 + 1 inside the O(lambda-1) term.
Usage: python t2.py p s [nrep] -> ../out/t2_p{p}_S{s}.csv"""
import os, sys
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import csv, numpy as np
from multiprocessing import Pool
from scipy.special import ndtr
from scipy.stats import chi2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oswap_lib import Neighbourhood, log_prior_table, A0, B0
from rgen import generate
from run_cells import geometry
from run_local import chol, SCALES, N, NU, SIG

UE = (np.arange(24) + 0.5) / 24
GX, GW = np.polynomial.hermite_e.hermegauss(32); GW = GW / GW.sum()


def t2_probs(n, s0, kap_add, gam, kap_sw, delta, rho, om0, omT):
    """returns P(miss), P(add-type event), P(drop/swap-type event) under T2."""
    nu = NU; k = n / (n + 1)
    E = chi2.ppf(UE, n - 1 - s0)                                  # [e]
    lam_a = np.exp(kap_add / nu)                                  # [m]
    t2a = (lam_a[None, :] - 1) * (E[:, None] + om0) / (1 - lam_a[None, :] / (n + 1))
    logkeep_add = np.log(np.clip(1 - 2 * ndtr(-np.sqrt(np.maximum(t2a, 0))), 1e-300, 1)).sum(1)   # [e]
    Lam = np.exp(gam / nu); lam_s = np.exp(kap_sw / nu)           # [j], [j,m]
    s = np.sqrt(1 - rho ** 2)
    logkeep_j = np.zeros((len(E), len(gam)))
    for jj in range(len(gam)):
        A = np.abs(delta[jj]) + GX                                # [a]
        # drop region: A^2 (1 - Lam/(n+1)) < (Lam-1)(E + omT)
        nodrop = (A[None, :] ** 2 * (1 - Lam[jj] / (n + 1)) >= (Lam[jj] - 1) * (E[:, None] + omT[jj]))   # [e,a]
        lj = lam_s[jj][None, :]; r = rho[jj][None, :]; sj = s[jj][None, :]
        Aa = A[:, None]; Em = n - 1 - s0          # swaps: E at its mean (error O((lam-1) sd E), see report)
        thr = (k * Aa ** 2 + (lj - 1) * (Em + Aa ** 2 + 1 + omT[jj])) / (lj * k)
        st = np.sqrt(np.maximum(thr, 0))
        pin = ndtr((st - r * Aa) / sj) - ndtr((-st - r * Aa) / sj)              # P(B^2 <= thr | A)  [a,m]
        keep = np.exp(np.log(np.clip(pin, 1e-300, 1)).sum(1))[None, :] * nodrop  # [e,a]
        pj = 1 - (keep * GW[None, :]).sum(1)                                     # [e]
        logkeep_j[:, jj] = np.log(np.clip(1 - pj, 1e-300, 1))
    keep_all = np.exp(logkeep_add + logkeep_j.sum(1))
    return 1 - keep_all.mean(), 1 - np.exp(logkeep_add).mean(), 1 - np.exp(logkeep_j.sum(1)).mean()


def one(args):
    p, s, r = args
    X, eps, S0, b = generate(p, s, r, chol(p, s))
    n = N; s0 = len(S0)
    lp = log_prior_table(p, n)
    nb = Neighbourhood(X, S0, lp)
    rj2, rho = geometry(X, S0)
    signal = X[:, S0] @ b
    ldD0 = nb.ldH0 - nb.ldG0
    kap_add = (lp[s0] - lp[s0 + 1]) + 0.5 * (np.log(nb.sH_add) - np.log(nb.sG_add))
    gam = np.empty(s0); kap_sw = np.empty((s0, len(nb.nulls)))
    for jj, d in enumerate(nb.drop):
        ldDT = d['ldHT'] - d['ldGT']
        gam[jj] = (lp[s0 - 1] - lp[s0]) + 0.5 * (ldD0 - ldDT)
        kap_sw[jj] = 0.5 * (ldDT + np.log(d['sH']) - np.log(d['sG']) - ldD0)
    rows = []
    for key, c in SCALES.items():
        theta = c * b; mu = c * signal; mu2 = mu @ mu
        bt = 2 * B0 * (mu2 + (n - 1) * SIG ** 2) / (n - 1)
        om0 = ((mu2 + s0 * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        delta = theta * np.sqrt(rj2) / SIG
        omT = ((mu2 - theta ** 2 * rj2 + (s0 - 1) * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        pm, pa, pds = t2_probs(n, s0, kap_add, gam, kap_sw, delta, rho, om0, omT)
        # Le Cam pairwise floor (Prop. 5): max over (j,l) of Phi(-|delta_j| sqrt(1-rho^2)/2)
        floor = ndtr(-np.abs(delta)[:, None] * np.sqrt(1 - rho ** 2) / 2).max()
        rows.append(dict(p=p, scenario=s, rep=r, scale=key, T2=pm, T2_add=pa, T2_dropswap=pds, lecam_floor=floor,
                         om0=om0, mean_kap_add=kap_add.mean(), min_gam=gam.min()))
    return rows


if __name__ == '__main__':
    p, s = int(sys.argv[1]), int(sys.argv[2]); nrep = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    with Pool(int(os.environ.get('OSWAP_CORES', '4'))) as pool:
        res = pool.map(one, [(p, s, r) for r in range(1, nrep + 1)], chunksize=1)
    rows = [x for rr in res for x in rr]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
    fn = os.path.join(out, f't2_p{p}_S{s}.csv' if nrep == 100 else f't2test_p{p}_S{s}.csv')
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('wrote', fn, len(rows))
