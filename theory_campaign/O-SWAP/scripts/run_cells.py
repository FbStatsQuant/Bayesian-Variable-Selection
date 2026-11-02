"""For every study dataset (p, S, r) and scale c in {1, 0.5}:
 (R) realised one-move scan of S0 on the actual y (exact scores);
 (A) analytic per-event probabilities (REPORT Props 1-3) and combinations;
 (M) conditional Monte Carlo over fresh noise given the actual X (exact scores), R draws.
Usage: run_cells.py p scenario [R] -> ../out/cells_p{p}_S{s}.csv"""
import sys, os, csv, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oswap_lib import *
from analytic import p_add, p_drop, p_swap, p_swap_closed

N = 200; SIG = 1.0
SCALES = {'c100': 1.0, 'c050': 0.5}


def geometry(Xs, S0):
    n = Xs.shape[0]
    s0 = len(S0)
    nulls = np.setdiff1d(np.arange(Xs.shape[1]), S0)
    G0 = Xs[:, S0].T @ Xs[:, S0]
    C = Xs[:, S0].T @ Xs[:, nulls]
    rj2 = np.empty(s0); rl2 = np.empty((s0, len(nulls))); rjl = np.empty((s0, len(nulls)))
    for jj in range(s0):
        keep = np.delete(np.arange(s0), jj)
        GTi = np.linalg.inv(G0[np.ix_(keep, keep)])
        gTj = G0[keep, jj]
        rj2[jj] = G0[jj, jj] - gTj @ GTi @ gTj
        CT = C[keep]
        rl2[jj] = (n - 1) - np.einsum('im,ij,jm->m', CT, GTi, CT)
        rjl[jj] = C[jj] - gTj @ GTi @ CT
    rho = rjl / np.sqrt(rj2[:, None] * rl2)
    return rj2, rho


def one(args):
    p, s, r, R = args
    X, Y, S0, beta, eps = load(p, s, r)
    Xs, _, _ = standardise(X, Y[:, 0])
    n = N; s0 = len(S0); nu = 0.01 + n / 2
    lp = log_prior_table(p, n)
    nb = Neighbourhood(Xs, S0, lp)
    rj2, rho = geometry(Xs, S0)
    signal = Xs[:, S0] @ beta[S0]
    rng = np.random.default_rng(1000003 * p + 10007 * s + r)
    # deterministic log-determinant ratios (exact)
    ldD0 = nb.ldH0 - nb.ldG0
    kap_add = (lp[s0] - lp[s0 + 1]) + 0.5 * (np.log(nb.sH_add) - np.log(nb.sG_add))
    gam_drop = np.empty(s0); kap_swap = np.empty((s0, len(nb.nulls)))
    for jj, d in enumerate(nb.drop):
        ldDT = d['ldHT'] - d['ldGT']
        gam_drop[jj] = (lp[s0 - 1] - lp[s0]) + 0.5 * (ldD0 - ldDT)
        kap_swap[jj] = 0.5 * (ldDT + np.log(d['sH']) - np.log(d['sG']) - ldD0)
    rows = []
    for key, c in SCALES.items():
        theta = c * beta[S0]
        mu = c * signal
        mu2 = mu @ mu
        sy2 = (mu2 + (n - 1) * SIG ** 2) / (n - 1)
        bt = 2 * 0.01 * sy2
        # ---- analytic
        lam_a = np.exp(kap_add / nu)
        om0 = ((mu2 + s0 * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        pa = p_add(lam_a, n - 2 - s0, om0, n)
        delta = theta * np.sqrt(rj2) / SIG
        Lam = np.exp(gam_drop / nu)
        omT = ((mu2 - theta ** 2 * rj2 + (s0 - 1) * SIG ** 2) / (n + 1) + bt) / SIG ** 2
        pd = p_drop(Lam, delta, n - 1 - s0, omT, n)
        lam_s = np.exp(kap_swap / nu)
        c0 = (n - 2 - s0) + omT[:, None] * np.ones_like(rho)
        ps = p_swap(lam_s.ravel(), np.repeat(delta, rho.shape[1]), rho.ravel(), c0.ravel(), n).reshape(rho.shape)
        ps1 = p_swap_closed(delta[:, None], rho)
        ind = lambda q: 1 - np.exp(np.log1p(-np.clip(q, 0, 1 - 1e-15)).sum())
        A_add_sum, A_drop_sum, A_swap_sum = pa.sum(), pd.sum(), ps.sum()
        # per-truth cluster probability for swaps+drop (independence within cluster), then independence
        A_ind = ind(np.concatenate([pa, pd, ps.ravel()]))
        # ---- realised
        y = mu + eps
        y = y - y.mean(); y = y / np.sqrt(y @ y / (n - 1))
        F0, Fa, Fd, Fs = nb.scores(y)
        ga, gd, gs = Fa.max() - F0, Fd.max() - F0, Fs.max() - F0
        best = max(ga, gd, gs)
        btype = ['add', 'drop', 'swap'][int(np.argmax([ga, gd, gs]))] if best > 0 else 'none'
        # ---- conditional MC over fresh noise
        mc = {'add': 0, 'drop': 0, 'swap': 0}
        mcany = 0
        for _ in range(R):
            yy = mu + SIG * rng.standard_normal(n)
            yy = yy - yy.mean(); yy = yy / np.sqrt(yy @ yy / (n - 1))
            F0m, Fam, Fdm, Fsm = nb.scores(yy)
            g = [Fam.max() - F0m, Fdm.max() - F0m, Fsm.max() - F0m]
            if max(g) > 0:
                mcany += 1
                mc[['add', 'drop', 'swap'][int(np.argmax(g))]] += 1
        # cluster-max lower bracket: clusters = {add events of nulls in one generator group of 5}
        # and, per truth j, {drop_j} U {swap_jl : all l}; perfect dependence inside, independence across
        grp = nb.nulls // 5
        ug, inv = np.unique(grp, return_inverse=True)
        amax = np.zeros(len(ug)); np.maximum.at(amax, inv, pa)
        jclu = np.maximum(pd, ps.max(1))
        A_lo = ind(np.concatenate([amax, jclu]))
        A_lo_add, A_lo_ds = ind(amax), ind(jclu)
        jmax, lmax = np.unravel_index(np.argmax(ps), ps.shape)
        rows.append(dict(p=p, scenario=s, rep=r, scale=key,
                         real_best_gap=best, real_type=btype,
                         real_n_add=int((Fa > F0).sum()), real_n_drop=int((Fd > F0).sum()), real_n_swap=int((Fs > F0).sum()),
                         A_add=A_add_sum, A_drop=A_drop_sum, A_swap=A_swap_sum,
                         A_swap_lam1=ps1.sum(), A_ind=A_ind, A_lo=A_lo, A_lo_add=A_lo_add, A_lo_dropswap=A_lo_ds,
                         A_ind_add=ind(pa), A_ind_drop=ind(pd), A_ind_swap=ind(ps.ravel()),
                         A_max_swap=ps.max(), A_max_swap_rho=rho[jmax, lmax], A_max_swap_delta=delta[jmax],
                         A_min_delta=np.abs(delta).min(), A_mean_kappa_add=kap_add.mean(),
                         MC_R=R, MC_any=mcany / R, MC_add=mc['add'] / R, MC_drop=mc['drop'] / R, MC_swap=mc['swap'] / R))
    return rows


if __name__ == '__main__':
    p, s = int(sys.argv[1]), int(sys.argv[2]); R = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    reps = range(1, 101) if len(sys.argv) <= 4 else range(1, int(sys.argv[4]) + 1)
    nproc = int(os.environ.get('OWLS_JOB_CORES', '1'))
    with Pool(nproc) as pool:
        res = pool.map(one, [(p, s, r, R) for r in reps])
    rows = [x for rr in res for x in rr]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f'cells_p{p}_S{s}.csv' if len(sys.argv) <= 4 else f'test_p{p}_S{s}.csv')
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('wrote', fn, len(rows))
