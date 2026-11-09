"""R02 scratch: adapted CS path (n1_exact_grid.run_path) vs dense fac_core.ls0_path from SATURATED / arbitrary starts.
Run with -B and PYTHONPYCACHEPREFIX pointing into this scratch dir (no pyc read or written elsewhere)."""
import sys, math, itertools
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'numerics'))
import n1_exact_grid as g
import numpy as np, fac_core as fc, bvs_core as bc, cs_core as cs, inspect
from types import SimpleNamespace
src0 = inspect.getsource(cs.ls0_path_cs)
for s_ in ("def ls0_path_cs(P, max_moves=10 ** 7, record_every=0):", "inT = np.ones(p, bool)", "k = p\n    A = float(z @ z)\n    B = float(z.sum())"):
    assert src0.count(s_) == 1, ("replacement target missing", s_)
def dense(P, n, p, rho):
    D = SimpleNamespace(n=n, p=p, K=P.K, XtX=(n-1)*((1-rho)*np.eye(p)+rho*np.ones((p,p))), Xty=P.z, yty=n-1,
                        nu=P.nu, logw=P.lw, logm0=-P.nu*math.log(.02+n-1), cache={})
    return D
res = dict(cases=0, mism=0, swaps=0, sat_starts=0, at_K_add_blocked=0, ties=0)
for n, p, rho in ((30, 22, .5), (24, 20, .3), (40, 39, .7), (31, 29, .5)):
    for seed in range(20):
        rng = np.random.default_rng(1000+seed)
        theta = np.zeros(p); S0 = rng.choice(p, 3, replace=False); theta[S0] = rng.choice([-1, 1], 3)*rng.uniform(.2, 1.5, 3)
        P = cs.CS(rho, theta, n, rng=rng)
        D = dense(P, n, p, rho)
        for kind in ('K', 'Kminus1', 'rand'):
            if kind == 'K': k = P.K
            elif kind == 'Kminus1': k = P.K-1
            else: k = int(rng.integers(1, P.K+1))
            start = tuple(sorted(rng.choice(p, k, replace=False).tolist()))
            if rng.random() < .5:  # sometimes force truth inside
                start = tuple(sorted(set(start[:max(0, k-3)]) | set(S0.tolist())))[:P.K]
                start = tuple(sorted(start))
            dp = fc.ls0_path(D, start, P.S0)
            try: path = g.run_path(P, start)
            except TypeError:
                res['crash_empty'] = res.get('crash_empty', 0) + 1; res.setdefault('crash_dense_final', []).append(dp['final']); continue
            ok = path['final'] == dp['final'] and len(path['moves']) == dp['moves']
            T = set(start)
            for mv, st in zip(path['moves'], dp['steps']):
                if mv[1] is not None: T.remove(mv[1])
                if mv[2] is not None: T.add(mv[2])
                ok &= abs(P.F(tuple(sorted(T))) - st['best']) < 1e-7
                res['swaps'] += mv[0].startswith('s')
            res['ties'] += path['info']['ties']
            res['cases'] += 1; res['mism'] += (not ok); res['sat_starts'] += (len(start) == P.K)
print(res)
