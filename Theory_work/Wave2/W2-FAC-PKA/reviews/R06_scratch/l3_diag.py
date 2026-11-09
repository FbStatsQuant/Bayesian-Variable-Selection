"""R06 scratch: independent L3 initial-phase diagnostics (full swap matrix, no extreme shortcut).
Writes only l3_diag_out.jsonl next to this file. Imports PKA/FAC-B numerics read-only."""
import sys, os, json, math
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'numerics'))
import numpy as np
from n3_singletons import singleton_start, run_path, replace_once, source, cs

# reproduce n6 initial_path (cs_core extreme-swap code) for fidelity comparison
ps = replace_once(source, 'def run_path(', 'def initial_path(')
ps = replace_once(ps, 'moves.append((tag, jo, li))', 'moves.append((tag, jo, li))\n        if typ != "s": break')
ns = dict(cs.__dict__); exec(ps, ns); initial_path = ns['initial_path']

def my_phase(P, S, full=True, max_steps=10**6):
    n, p, K = P.n, P.p, P.K
    z, xi = P.z, P.xi
    S0 = set(P.S0); s0 = len(S0)
    h = n - 1.0; s = P.s
    d = math.sqrt(h / 2) / s; f = h / (2 * s); b = (h * s0 / 2 + math.sqrt(h / 2) * P.eta) / s
    zz = b + d * xi + f * P.theta
    assert np.allclose(zz, z, rtol=1e-10, atol=1e-8), 'z representation'
    al, be, nu = P.al, P.be, P.nu
    inT = np.zeros(p, bool); inT[list(S)] = True
    k = int(inT.sum()); A = float(z[inT] @ z[inT]); B = float(z[inT].sum())
    assert k == K and S0 <= set(S)
    c = p / n; Mbar = 2 / (1 - c); logn = math.log(n)
    a_thr = math.sqrt((1 - c) / 20 * logn)
    xT0 = None; rec = []; imports = []; exports = []; first_other = None
    for step in range(max_steps):
        FT = float(P.F_stats(k, A, B))
        gam = be / (al + k * be)
        xT = gam * xi[inT].sum() - (b * (1 - k * gam) - gam * f * s0) / d
        if xT0 is None: xT0 = xT
        Q = (n - 1.0) - n * (A - gam * B * B) / al; psi = 0.02 + Q
        M = nu * n * d * d / (al * psi)
        idx_in = np.flatnonzero(inT); idx_out = np.flatnonzero(~inT)
        zin, zout = z[idx_in], z[idx_out]
        Fd = P.F_stats(np.full(len(idx_in), k - 1), A - zin ** 2, B - zin)
        isN = np.array([j not in S0 for j in idx_in], bool)
        Fa = P.F_stats(np.full(len(idx_out), k + 1), A + zout ** 2, B + zout) if k < K else np.array([])
        if full:
            Fs = P.F_stats(np.full((len(idx_in), len(idx_out)), k), (A - zin ** 2)[:, None] + zout[None, :] ** 2,
                           (B - zin)[:, None] + zout[None, :])
        bestd = float(Fd.max()); bests = float(Fs.max())
        besta = float(Fa.max()) if len(Fa) else -np.inf
        best = max(bestd, bests, besta)
        r = dict(step=step, k=k, xT=xT, drift=abs(xT - xT0), M=M, Mbar=Mbar,
                 best_null_del_gain=float(Fd[isN].max()) - FT,
                 truth_del_gain=float(Fd[~isN].max()) - FT,
                 truth_out_swap_gain=float(Fs[~isN].max()) - FT,
                 best_swap_gain=bests - FT, logn=logn)
        # near-centre retained null exists?
        tau_in = xi[idx_in] - xT
        r['near_centre_null'] = bool((np.abs(tau_in[isN]) <= 1).any())
        if not best > FT:
            first_other = 'stop'; rec.append(r); break
        if best != bests or besta == best:
            # non-swap chosen (deletion preferred on ties only if lexicographic would; record)
            first_other = '-N' if bestd == best and isN[int(np.argmax(Fd))] else ('-T' if bestd == best else '+')
            r['tie_swap_vs_other'] = bests == best
            rec.append(r); break
        i, e = np.unravel_index(int(np.argmax(Fs)), Fs.shape)
        jo, li = int(idx_in[i]), int(idx_out[e])
        nties = int((Fs == best).sum())
        taul = xi[li] - xT; tauj = xi[jo] - xT
        # fixed-incoming best outgoing among retained nulls by square completion
        target = gam * taul / (1 + gam)
        cand = idx_in[isN]
        jstar = int(cand[np.argmin(np.abs(xi[cand] - xT - target))])
        r.update(jo=jo, li=li, tau_l2=taul ** 2, tau_l2_req=(1 - c) * logn / 10, tau_j=tauj,
                 xi_l=float(xi[li]), xi_j=float(xi[jo]), jstar_matches=(jstar == jo), nties=nties,
                 import_in_pool=abs(xi[li]) >= a_thr)
        rec.append(r)
        imports.append(li); exports.append(jo)
        inT[jo] = False; inT[li] = True
        A += z[li] ** 2 - z[jo] ** 2; B += z[li] - z[jo]
    reexport = any(j in set(imports[:t]) for t, j in enumerate(exports))
    return dict(W=len(imports), first_other=first_other, reexport=reexport, rec=rec, imports=imports, exports=exports)

if __name__ == '__main__':
    out = (HERE / 'l3_diag_out.jsonl').open('w', encoding='utf8')
    for n in (800, 2000, 4000):
        for c in (.6, .75, .9, .98):
            for s0 in (1, 2):
                for seed in range(6 if n < 4000 else 3):
                    p = int(c * n); theta = np.zeros(p); theta[:s0] = 1
                    P = cs.CS(.5, theta, n, rng=np.random.default_rng(seed))
                    S = singleton_start(P)
                    res = my_phase(P, S)
                    ref = initial_path(P, S)['moves']
                    ref_sw = []
                    for m in ref:
                        if not m[0].startswith('s'): ref_first = m[0]; break
                        ref_sw.append((m[1], m[2]))
                    else: ref_first = 'stop'
                    same = ref_sw == list(zip(res['exports'], res['imports'])) and ref_first == res['first_other']
                    rec = res['rec']; sw = [r for r in rec if 'jo' in r]
                    row = dict(n=n, p=p, c=c, s0=s0, seed=seed, W=res['W'], first_other=res['first_other'],
                               same_as_cs_core=same, reexport=res['reexport'],
                               M_min=min(r['M'] for r in rec), M_max=max(r['M'] for r in rec), Mbar=rec[0]['Mbar'],
                               max_drift=max(r['drift'] for r in rec),
                               min_best_null_del_over_logn=min(r['best_null_del_gain'] for r in rec) / math.log(n),
                               max_truth_del_gain=max(r['truth_del_gain'] for r in rec),
                               max_truth_out_swap_gain=max(r['truth_out_swap_gain'] for r in rec),
                               all_near_centre=all(r['near_centre_null'] for r in rec),
                               min_tau_l2_over_req=min((r['tau_l2'] / r['tau_l2_req'] for r in sw), default=None),
                               max_abs_tau_j=max((abs(r['tau_j']) for r in sw), default=None),
                               all_jstar_match=all(r['jstar_matches'] for r in sw),
                               any_swap_ties=any(r['nties'] > 1 for r in sw),
                               swap_gain_ge_null_del=all(r['best_swap_gain'] >= r['best_null_del_gain'] for r in sw),
                               all_imports_in_pool=all(r['import_in_pool'] for r in sw),
                               mean_M=float(np.mean([r['M'] for r in rec])))
                    out.write(json.dumps(row) + '\n'); out.flush(); print(json.dumps(row), flush=True)
