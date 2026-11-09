"""s5_exact.py -- W2-SIM family PK, experiment S5PK (exact Gram): Sigma = 0.3*11' + 0.4*H + 0.3*I (groups of 5;
fac_core.s5_sigma), X'X = (n-1) Sigma exactly (fac_core.ExactGram sufficient statistics, factor pieces drawn), p > K.
  python s5_exact.py OUT.jsonl n frac LAYOUT REP [EXP (default S5PK_exact; seeds depend on it)]
p = min(round(frac*n), n-2).  Partition: s5_partition(p, B) (consecutive groups of 5 packed next-fit into blocks of size <= B)
which equals bvs_core.partition_from_corr(Sigma, B) -- checked in validate_s5_partition.py (for the p used there;
for p <= 1200 this script additionally recomputes bvs_core.partition_from_corr and asserts equality).
Start mode bvs_core.start_mode (exact block DP on the general scorer); uncapped LS0 path fac_core.ls0_path.
"""
import sys
import time
import numpy as np
import pk_common as pc
import bvs_core as bc
import fac_core as fc


def s5_partition(p, B):
    """consecutive groups of 5 (last one p mod 5) packed next-fit into blocks of size <= B."""
    groups = [list(range(s, min(s + 5, p))) for s in range(0, p, 5)]
    blocks, cur = [], []
    for g in groups:
        if len(cur) + len(g) <= B:
            cur = cur + g
        else:
            blocks.append(cur)
            cur = list(g)
    if cur:
        blocks.append(cur)
    return blocks


def run(n, frac, layout, rep, exp="S5PK_exact", max_moves=10 ** 6):
    p = min(int(round(frac * n)), n - 2)
    seed = pc.cell_seed(exp, n, frac, layout, rep)
    rng = np.random.default_rng(seed)
    th = pc.theta_vec(p, layout)
    S0 = tuple(int(j) for j in np.flatnonzero(th))
    t0 = time.time()
    Sigma, Lam, Psi = fc.s5_sigma(p)
    P = fc.ExactGram(Sigma, th, n, rng, Lam=Lam, Psi=Psi)
    K = P.K
    B = bc.block_size(n, p)
    blocks = s5_partition(p, B)
    checked = False
    if p <= 1200:
        assert bc.partition_from_corr(Sigma, B) == blocks
        checked = True
    t1 = time.time()
    info = bc.start_mode(P, blocks)
    start = tuple(int(j) for j in info.mode)
    info.tabs = None
    t2 = time.time()
    tr = pc.trace_general(P, start, S0, max_moves=max_moves)
    t3 = time.time()
    # kept-per-group profile of the start (groups of 5): histogram of kept counts over truth-free groups
    grp = np.arange(p) // 5
    kept = np.bincount(grp[list(start)], minlength=grp.max() + 1) if start else np.zeros(grp.max() + 1, int)
    truth_groups = set(int(grp[j]) for j in S0)
    kg = [int(kept[g]) for g in range(len(kept)) if g not in truth_groups]
    out = dict(exp=exp, design="s5_exact", n=n, frac=frac, p=p, B=B, n_blocks=len(blocks),
               partition_checked_direct=checked, layout=layout, rep=rep, seed=seed,
               start_n_optimal=info.n_optimal, start_truncated=info.truncated,
               start_kept_per_group_hist={str(v): kg.count(v) for v in sorted(set(kg))})
    out.update(pc.path_record(P, start, S0, tr, n, p))
    out.update(t_setup=round(t1 - t0, 2), t_start=round(t2 - t1, 2), t_path=round(t3 - t2, 2))
    return out


def _r(x):
    return None if (x is None or not np.isfinite(x)) else round(float(x), 6)


if __name__ == "__main__":
    outf, n, frac, layout, rep = sys.argv[1:6]
    res = run(int(n), float(frac), layout, int(rep), *(sys.argv[6:7]))
    pc.write_jsonl(outf, res)
    print({k: res[k] for k in ("n", "p", "rep", "layout", "start_size", "K", "lead_swaps", "m_star", "k_hit", "cap_MR1",
                               "final_is_S0", "limited", "max_direct_absdiff", "t_start", "t_path")}, flush=True)
