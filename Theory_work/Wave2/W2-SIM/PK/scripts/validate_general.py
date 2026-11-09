"""validate_general.py -- W2-SIM family PK: agreement of the closed-form (Schur) LS0 path tracer fac_core.ls0_path with
the direct reference bvs_core.local_search (every neighbour scored by Cholesky; uncapped) on small iid-row data,
designs CS (rho = 0.5) and S5, p from 0.8n to 3n (p >= 80 > max truth index 75), from the bvs_core start mode.  Writes one JSON line per case
(path-of-sets equality, final equality, number of moves, max |F_scan - F_direct| along the path).
usage: python validate_general.py OUT.jsonl"""
import sys
import json
import time
import numpy as np
import pk_common as pc
import bvs_core as bc
import fac_core as fc
from r3_iid import make_X

cases = []
for design in ("cs0.5", "s5"):
    for n, ratios in ((60, (1.5, 3.0)), (80, (1.0, 2.5)), (100, (0.8, 1.5, 3.0))):
        for r in ratios:
            for rep in range(2):
                cases.append((design, n, int(round(r * n)), rep))
outf = sys.argv[1]
open(outf, "w").close()
n_ok = 0
for design, n, p, rep in cases:
    layout = "aligned" if rep == 0 else "mixed"
    seed = pc.cell_seed("validate_general", design, n, p, layout, rep)
    rng = np.random.default_rng(seed)
    th = pc.theta_vec(p, layout)
    S0 = tuple(int(j) for j in np.flatnonzero(th))
    X = bc.standardize_X(make_X(design, n, p, rng))
    y = bc.make_y_std(X, th, 1.0, rng)
    P = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(P, blocks)
    start = tuple(info.mode)
    t0 = time.time()
    path_fc = []
    maxdiff = [0.0]

    def rec(P_, T, sc, inf):
        path_fc.append(tuple(int(t) for t in T))
        maxdiff[0] = max(maxdiff[0], abs(sc["FT"] - P.F(tuple(int(t) for t in T))))
    r_fc = fc.ls0_path(P, start, S0, max_moves=10 ** 6, record=rec)
    t1 = time.time()
    r_bc = bc.local_search(P, start, 10 ** 9)
    t2 = time.time()
    same_path = [tuple(s) for s in r_bc["path"]] == path_fc
    ok = (same_path and tuple(r_bc["final"]) == tuple(r_fc["final"]) and r_bc["certified"]
          and np.isfinite(maxdiff[0]) and maxdiff[0] < 1e-8)
    n_ok += ok
    d = dict(design=design, n=n, p=p, K=P.K, layout=layout, seed=seed, start_size=len(start), moves_fc=r_fc["moves"],
             moves_bc=r_bc["moves"], same_path=same_path, same_final=tuple(r_bc["final"]) == tuple(r_fc["final"]),
             final_is_S0=tuple(r_fc["final"]) == S0, bc_certified=r_bc["certified"], max_absdiff_F=maxdiff[0],
             t_fc=round(t1 - t0, 2), t_bc=round(t2 - t1, 2))
    pc.write_jsonl(outf, d)
    print(json.dumps(d), flush=True)
summary = dict(summary=True, cases=len(cases), agree=n_ok, module_sha=pc.module_sha())
pc.write_jsonl(outf, summary)
print(json.dumps(summary))
if n_ok != len(cases):
    sys.exit(1)
