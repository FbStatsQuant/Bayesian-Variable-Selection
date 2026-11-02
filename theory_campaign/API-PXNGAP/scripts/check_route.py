"""End-to-end LS0 route on LH-iid (API-PXNGAP §10), exact objects (EX-A), p >> n.
Per replicate: blocks == groups? ; start mode == S°? ; 1 - pi0(S°) ; q, e ; LS0 path from the start mode ; S0 scored? ;
certified? ; min D_S margin over the lattice (best progress minus best non-progress neighbour, incl. S) ; (L) margin at S0.
Configs: c in {1,2}, v = 1, g = 10, rho = .7, psi = .5, beta = 1, sigma = 1. Seeds fixed per (config, n, rep).
Usage: python3 check_route.py [quick]"""
import json, math, sys, time
import numpy as np
from pxn_core import *
from lh_gen import gen_lh

quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
GRID = [(100, 300, 10), (200, 500, 10), (200, 1000, 6), (400, 1500, 4)] if not quick else [(100, 300, 3)]
CONFIGS = {"c1": dict(pairs=[(0, 1, 1.0)], visible=[(2, 1.0)]), "c2": dict(pairs=[(0, 1, 1.0), (2, 3, -1.0)], visible=[(4, 1.0)])}
g, rho, psi = 10, 0.7, 0.5
out = open("../results/route.jsonl", "a")

def lattice_margins(D, Sref, M, S0):
    """min over lattice states S != S0 of [best progress F - max(F(S), best non-progress neighbour F)]."""
    p, K = D.p, D.K
    worst = math.inf
    import itertools
    for r in range(len(M)):
        for Mp in itertools.combinations(M, r):
            S = tuple(sorted(set(Sref) | set(Mp)))
            missing = [j for j in M if j not in S]
            nb = neighbours(S, p, K)
            f = log_F(D, [list(x) for x in nb] + [list(S)])
            fS = f[-1]; f = f[:-1]
            prog = {tuple(sorted(S + (j,))) for j in missing}
            isprog = np.array([x in prog for x in nb])
            best_prog = f[isprog].max(); best_non = max(fS, f[~isprog].max())
            worst = min(worst, best_prog - best_non)
    return worst

for name, cfg in CONFIGS.items():
    for (n, p, reps) in GRID:
        G = p // g
        for rep in range(reps):
            t0 = time.time()
            rng = np.random.default_rng(int(1e6) + 7919 * n + 131 * p + rep + (0 if name == "c1" else 500000))
            X, y, groups, S0, Sref, M = gen_lh(n, G, g, rho, psi, cfg["pairs"], cfg["visible"], rng)
            D = Data(X, y)
            blocks = v3_blocks(D)
            rec = dict(cfg=name, n=n, p=p, rep=rep, B=D.B, ell=math.ceil(math.log2(n + p + 1)), c=len(M), s0=len(S0))
            rec["blocks_eq_groups"] = sorted(map(tuple, blocks)) == sorted(map(tuple, groups))
            T = Tables(D, blocks); SL = StartLaw(T)
            mode, lmode = SL.start_mode()
            rec["mode_eq_ref"] = (mode == Sref)
            rec["log_pi0_ref"] = float(SL.log_pi0(Sref)); rec["log_pi0_S0"] = float(SL.log_pi0(S0))
            q, loge = agg_q_e(T, Sref); rec["q"] = q; rec["log_e"] = loge
            rec["T22_bound_1mpi0"] = (len(Sref) + 1) * q / (1 - q) + len(Sref) * math.exp(loge) if q < 1 else None
            ls = local_search(D, mode, rec["ell"], S0=S0)
            rec["ls_path_len"] = len(ls["path"]) - 1; rec["ls_scored_S0"] = ls["scored_S0"]
            rec["ls_end_is_S0"] = (list(ls["path"][-1]) == S0); rec["ls_certified"] = ls["certified"]
            rec["ls_path_in_lattice"] = all(set(Sref) <= set(s) <= set(S0) for s in ls["path"])
            rec["min_DS_margin"] = float(lattice_margins(D, Sref, M, S0))
            # (L) margin at S0
            nb = neighbours(tuple(S0), p, D.K); f = log_F(D, [list(x) for x in nb] + [S0])
            rec["L_margin"] = float(f[-1] - f[:-1].max())
            rec["secs"] = round(time.time() - t0, 1)
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(json.dumps(rec)); sys.stdout.flush()
