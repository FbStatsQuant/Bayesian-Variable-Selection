"""Laptop runner (no server data needed): regenerates every study dataset with rgen.py (exact port of
gen_prod_data.R) and, for c in {1, 0.5}, computes
 (A) analytic one-move probabilities (REPORT Props 1-3, exact kappas) and the T1 / T1-lo combinations;
 (R) the realised posterior-miss check on the study's own y: is S0 beaten by a one-move neighbour or a
     double drop (exact F)? if so, hill-climb (best-improvement add/drop/swap, exact F) and classify the
     end point vs S0 as extra-only / missed-only / mixed (the study's categories);
 (M) the same check over R fresh noise draws given the actual X (conditional MC).
Usage: python run_local.py p s [R] [nrep]  -> ../out/local_p{p}_S{s}.csv"""
import os, sys
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import csv, itertools, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oswap_lib import Neighbourhood, log_prior_table, log_C, A0, B0
from analytic import p_add, p_drop, p_swap, p_swap_closed
from rgen import generate, scenario_covariance
from run_cells import geometry

N = 200; SIG = 1.0; NU = A0 + N / 2
SCALES = {'c100': 1.0, 'c050': 0.5}
_L = {}


def chol(p, s):
    if (p, s) not in _L: _L[(p, s)] = np.linalg.cholesky(scenario_covariance(s, p)).T
    return _L[(p, s)]


class DoubleDrop:
    def __init__(self, nb):
        self.items = []
        s0 = nb.s0
        for a, b in itertools.combinations(range(s0), 2):
            keep = np.array([i for i in range(s0) if i not in (a, b)])
            HT = nb.H0[np.ix_(keep, keep)]; GT = nb.Gi0[np.ix_(keep, keep)]
            self.items.append((keep, np.linalg.inv(HT), np.linalg.slogdet(HT)[1] - np.linalg.slogdet(GT)[1]))
        self.c = nb.lprior[s0 - 2] + log_C(N)

    def scores(self, zS, yy):
        return np.array([self.c - 0.5 * ld - NU * np.log(2 * B0 + yy - N * zS[k] @ Hi @ zS[k])
                         for k, Hi, ld in self.items])


def climb(X, y, S, lp, maxit=30):
    S = np.array(sorted(S))
    for _ in range(maxit):
        nb = Neighbourhood(X, S, lp)
        F0, Fa, Fd, Fs = nb.scores(y)
        g = [Fa.max() - F0, Fd.max() - F0, Fs.max() - F0]
        t = int(np.argmax(g))
        if g[t] <= 0: break
        if t == 0: S = np.sort(np.append(S, nb.nulls[np.argmax(Fa)]))
        elif t == 1: S = np.delete(S, np.argmax(Fd))
        else:
            j, l = np.unravel_index(np.argmax(Fs), Fs.shape)
            S = np.sort(np.append(np.delete(S, j), nb.nulls[l]))
    return S


def classify(S, S0):
    ex = len(np.setdiff1d(S, S0)) > 0; mi = len(np.setdiff1d(S0, S)) > 0
    return 'mixed' if ex and mi else ('extra' if ex else ('missed' if mi else 'none'))


def check(X, y, nb, dd, lp):
    """posterior-miss check. returns (one_move_flag, miss_flag, type, end_size)."""
    S0 = nb.S0
    F0, Fa, Fd, Fs = nb.scores(y)
    zS = X[:, S0].T @ y
    Fdd = dd.scores(zS, y @ y)
    g = np.array([Fa.max(), Fd.max(), Fs.max(), Fdd.max()]) - F0
    if g.max() <= 0: return 0, 0, 'none', len(S0)
    t = int(np.argmax(g))
    if t == 0: start = np.append(S0, nb.nulls[np.argmax(Fa)])
    elif t == 1: start = np.delete(S0, np.argmax(Fd))
    elif t == 2:
        j, l = np.unravel_index(np.argmax(Fs), Fs.shape); start = np.append(np.delete(S0, j), nb.nulls[l])
    else: start = S0[dd.items[int(np.argmax(Fdd))][0]]
    S = climb(X, y, start, lp)
    return int(g[:3].max() > 0), 1, classify(S, S0), len(S)


def std(y):
    y = y - y.mean(); return y / np.sqrt(y @ y / (N - 1))


def one(args):
    p, s, r, R = args
    X, eps, S0, b = generate(p, s, r, chol(p, s))
    n = N; s0 = len(S0); nu = NU
    lp = log_prior_table(p, n)
    nb = Neighbourhood(X, S0, lp); dd = DoubleDrop(nb)
    rj2, rho = geometry(X, S0)
    signal = X[:, S0] @ b
    rng = np.random.default_rng(1000003 * p + 10007 * s + r)
    ldD0 = nb.ldH0 - nb.ldG0
    kap_add = (lp[s0] - lp[s0 + 1]) + 0.5 * (np.log(nb.sH_add) - np.log(nb.sG_add))
    gam = np.empty(s0); kap_sw = np.empty((s0, len(nb.nulls)))
    for jj, d in enumerate(nb.drop):
        ldDT = d['ldHT'] - d['ldGT']
        gam[jj] = (lp[s0 - 1] - lp[s0]) + 0.5 * (ldD0 - ldDT)
        kap_sw[jj] = 0.5 * (ldDT + np.log(d['sH']) - np.log(d['sG']) - ldD0)
    ind = lambda q: 1 - np.exp(np.log1p(-np.clip(q, 0, 1 - 1e-15)).sum())
    rows = []
    for key, c in SCALES.items():
        theta = c * b; mu = c * signal; mu2 = mu @ mu
        bt = 2 * B0 * (mu2 + (n - 1) * SIG ** 2) / (n - 1)
        om0 = ((mu2 + s0 * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        pa = p_add(np.exp(kap_add / nu), n - 2 - s0, om0, n)
        delta = theta * np.sqrt(rj2) / SIG
        omT = ((mu2 - theta ** 2 * rj2 + (s0 - 1) * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        pd = p_drop(np.exp(gam / nu), delta, n - 1 - s0, omT, n)
        c0 = ((n - 2 - s0) + omT[:, None] * np.ones_like(rho)).ravel()
        ps = p_swap(np.exp(kap_sw / nu).ravel(), np.repeat(delta, rho.shape[1]), rho.ravel(), c0, n).reshape(rho.shape)
        grp = nb.nulls // 5
        ug, inv = np.unique(grp, return_inverse=True)
        amax = np.zeros(len(ug)); np.maximum.at(amax, inv, pa)
        jclu = np.maximum(pd, ps.max(1))
        # realised
        y = std(mu + eps)
        r1, rm, rt, rk = check(X, y, nb, dd, lp)
        # conditional MC
        cnt = {'one': 0, 'miss': 0, 'extra': 0, 'missed': 0, 'mixed': 0}
        for _ in range(R):
            o1, om, ot, ok = check(X, std(mu + SIG * rng.standard_normal(n)), nb, dd, lp)
            cnt['one'] += o1; cnt['miss'] += om
            if om: cnt[ot] += 1
        jm, lm = np.unravel_index(np.argmax(ps), ps.shape)
        rows.append(dict(p=p, scenario=s, rep=r, scale=key,
                         real_one=r1, real_miss=rm, real_type=rt, real_size=rk,
                         A_ind=ind(np.concatenate([pa, pd, ps.ravel()])),
                         A_lo=ind(np.concatenate([amax, jclu])),
                         A_ind_add=ind(pa), A_ind_drop=ind(pd), A_ind_swap=ind(ps.ravel()),
                         A_lo_add=ind(amax), A_lo_dropswap=ind(jclu),
                         A_sum=pa.sum() + pd.sum() + ps.sum(), A_swap_lam1=ind(p_swap_closed(delta[:, None], rho).ravel()),
                         A_max_swap=ps.max(), A_max_swap_rho=rho[jm, lm], A_max_swap_delta=delta[jm],
                         A_max_drop=pd.max(), A_min_absdelta=np.abs(delta).min(), A_mean_pa=pa.mean(),
                         A_mean_kap_add=kap_add.mean(), A_mean_gam=gam.mean(), A_max_abs_kap_swap=np.abs(kap_sw).max(),
                         MC_R=R, MC_one=cnt['one'] / R, MC_miss=cnt['miss'] / R, MC_extra=cnt['extra'] / R,
                         MC_missed=cnt['missed'] / R, MC_mixed=cnt['mixed'] / R))
    return rows


if __name__ == '__main__':
    p, s = int(sys.argv[1]), int(sys.argv[2])
    R = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    nrep = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    ncore = int(os.environ.get('OSWAP_CORES', '4'))
    with Pool(ncore) as pool:
        res = pool.map(one, [(p, s, r, R) for r in range(1, nrep + 1)], chunksize=1)
    rows = [x for rr in res for x in rr]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f'local_p{p}_S{s}.csv' if nrep == 100 else f'localtest_p{p}_S{s}.csv')
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('wrote', fn, len(rows))
