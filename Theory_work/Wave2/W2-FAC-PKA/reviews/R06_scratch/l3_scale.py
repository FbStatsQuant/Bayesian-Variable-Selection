"""R06 scratch: large-n initial-phase length W_n (extreme-swap shortcut, exact by convexity; validated in l3_diag).
Writes only l3_scale_out.jsonl next to this file."""
import sys, json, math, time
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'numerics'))
import numpy as np
from n3_singletons import singleton_start, cs

def phase(P, S, max_steps=10**6):
    n, p, K = P.n, P.p, P.K; z = P.z; S0 = set(P.S0)
    inT = np.zeros(p, bool); inT[list(S)] = True
    isNull = np.ones(p, bool); isNull[list(S0)] = False
    k = K; A = float(z[inT] @ z[inT]); B = float(z[inT].sum())
    W = 0; Ms = []; imports = set(); reexp = False
    while W < max_steps:
        FT = float(P.F_stats(k, A, B))
        gam = P.be / (P.al + k * P.be); Q = (n - 1.0) - n * (A - gam * B * B) / P.al
        d2 = (n - 1.0) / 2 / P.s ** 2; Ms.append(P.nu * n * d2 / (P.al * (0.02 + Q)))
        idx_in = np.flatnonzero(inT); idx_out = np.flatnonzero(~inT)
        zin = z[idx_in]; zout = z[idx_out]
        Fd = P.F_stats(np.full(len(idx_in), k - 1), A - zin ** 2, B - zin)
        ext = idx_out[[int(np.argmin(zout)), int(np.argmax(zout))]]
        zl = z[ext]
        Fs = P.F_stats(np.full((len(idx_in), 2), k), (A - zin ** 2)[:, None] + zl[None, :] ** 2, (B - zin)[:, None] + zl[None, :])
        bd, bs = float(Fd.max()), float(Fs.max())
        if not max(bd, bs) > FT: return dict(W=W, first='stop', M=Ms, reexport=reexp)
        if bd >= bs:
            j = int(idx_in[int(np.argmax(Fd))])
            return dict(W=W, first='-N' if isNull[j] else '-T', M=Ms, reexport=reexp, swap_minus_del=bs - bd)
        i, e = np.unravel_index(int(np.argmax(Fs)), Fs.shape)
        jo, li = int(idx_in[i]), int(ext[e])
        if not (isNull[jo] and isNull[li]): return dict(W=W, first='sT', M=Ms, reexport=reexp)
        reexp |= jo in imports; imports.add(li)
        inT[jo] = False; inT[li] = True; A += z[li] ** 2 - z[jo] ** 2; B += z[li] - z[jo]; W += 1
    return dict(W=W, first='max', M=Ms, reexport=reexp)

if __name__ == '__main__':
    out = (HERE / 'l3_scale_out.jsonl').open('w', encoding='utf8')
    for n in (2000, 8000, 32000, 128000):
        for c in (.6, .75, .9):
            for seed in range(4 if n < 128000 else 2):
                t0 = time.time(); p = int(c * n); theta = np.zeros(p); theta[0] = 1
                P = cs.CS(.5, theta, n, rng=np.random.default_rng(100 + seed))
                S = singleton_start(P); r = phase(P, S)
                eta0 = (1 - c) / 80
                M = float(np.mean(r['M']))
                row = dict(n=n, c=c, seed=100 + seed, W=r['W'], first=r['first'], reexport=r['reexport'],
                           W_over_n=r['W'] / n, logW_over_logn=math.log(max(r['W'], 1)) / math.log(n),
                           bound_n_1_eta0=n ** (1 - eta0), M_mean=M, M_min=min(r['M']), M_max=max(r['M']),
                           heuristic_exp=1 - 1 / (4 * M), Mbar=2 / (1 - c), secs=round(time.time() - t0, 1))
                out.write(json.dumps(row) + '\n'); out.flush(); print(json.dumps(row), flush=True)
