"""r3_iid.py -- W2-SIM family PK, experiments R3 (iid-row compound symmetry, incl. p >> n) and S5PK-iid.

One data set per call:
  python r3_iid.py OUT.jsonl EXP DESIGN n p LAYOUT REP [max_moves]
DESIGN: cs<rho> (rows iid N(0, (1-rho)I + rho 11')), or s5 (rows iid N(0, 0.3*11' + 0.4*H + 0.3*I), H = groups of 5).
Pipeline (general scorer, ticket modules unchanged):
  X raw -> bvs_core.standardize_X; y = X theta + N(0,1) -> standardize_y (bvs_core.make_y_std);
  P = bvs_core.Problem(X, y)  [K = min(p, floor(n/2)), BB(1,p)-type prior log w(k) = -log(2 binom(2p-1,k))];
  blocks = bvs_core.partition(X)  (complete linkage on 1-|r|, cut at B = min(isqrt n, isqrt p, 16), next-fit packing);
  start = bvs_core.start_mode(P, blocks)  (exact block DP);
  uncapped LS0 path = fac_core.ls0_path(P, start)  (production local search M6.10: flip+swap neighbourhood, best strict
  improvement, exact float ties -> lexicographically smallest set; every scan in closed form by Schur complements;
  validated against bvs_core.local_search in validate_general.py), wrapped by pk_common.trace_general (executed-move
  accounting, censoring flag, NaN guards, winner margins, direct Cholesky re-scoring of the top neighbours at checkpoints).
"""
import sys
import time
import math
import numpy as np
import pk_common as pc
import bvs_core as bc
import fac_core as fc


def make_X(design, n, p, rng):
    if design.startswith("cs"):
        rho = float(design[2:])
        eta = rng.standard_normal(n)
        Z = rng.standard_normal((n, p))
        return math.sqrt(rho) * eta[:, None] + math.sqrt(1 - rho) * Z
    if design == "s5":
        G = (p + 4) // 5
        eta = rng.standard_normal(n)
        zeta = rng.standard_normal((n, G))
        Z = rng.standard_normal((n, p))
        grp = np.arange(p) // 5
        return math.sqrt(0.3) * eta[:, None] + math.sqrt(0.4) * zeta[:, grp] + math.sqrt(0.3) * Z
    raise ValueError(design)


def run(exp, design, n, p, layout, rep, max_moves=10 ** 6):
    seed = pc.cell_seed(exp, design, n, p, layout, rep)
    rng = np.random.default_rng(seed)
    t0 = time.time()
    th = pc.theta_vec(p, layout)
    S0 = tuple(int(j) for j in np.flatnonzero(th))
    X = bc.standardize_X(make_X(design, n, p, rng))
    y = bc.make_y_std(X, th, 1.0, rng)
    P = bc.Problem(X, y)
    K = P.K
    t1 = time.time()
    B = bc.block_size(n, p)
    blocks = bc.partition(X, B)
    t2 = time.time()
    info = bc.start_mode(P, blocks)
    start = tuple(int(j) for j in info.mode)
    info.tabs = None
    t3 = time.time()
    tr = pc.trace_general(P, start, S0, max_moves=max_moves)
    t4 = time.time()
    out = dict(exp=exp, design=design, n=n, p=p, B=B, n_blocks=len(blocks),
               block_sizes_hist=_hist([len(b) for b in blocks]), layout=layout, rep=rep, seed=seed,
               start_n_optimal=info.n_optimal, start_truncated=info.truncated)
    out.update(pc.path_record(P, start, S0, tr, n, p))
    out.update(t_data=round(t1 - t0, 2), t_partition=round(t2 - t1, 2), t_start=round(t3 - t2, 2), t_path=round(t4 - t3, 2))
    return out


def _r(x):
    return None if (x is None or not np.isfinite(x)) else round(float(x), 6)


def _hist(v):
    from collections import Counter
    return {str(k): c for k, c in sorted(Counter(v).items())}


if __name__ == "__main__":
    outf, exp, design, n, p, layout, rep = sys.argv[1:8]
    mm = int(sys.argv[8]) if len(sys.argv) > 8 else 10 ** 6
    res = run(exp, design, int(n), int(p), layout, int(rep), mm)
    pc.write_jsonl(outf, res)
    print({k: res[k] for k in ("exp", "design", "n", "p", "rep", "start_size", "K", "lead_swaps", "m_star", "k_hit",
                               "cap_MR1", "final_is_S0", "limited", "max_direct_absdiff", "min_margin", "t_partition", "t_start", "t_path")}, flush=True)
