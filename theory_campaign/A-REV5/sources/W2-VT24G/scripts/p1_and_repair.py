"""W2-VT24G: (a) Cor. P1 re-check: a1(x) = int_0^1 prod_{e != G_j}(1 - t q_e(x)) dt at the 20 distance-one states,
plus the simulated one-round scoring frequency (10000 reps); (b) repair from raw pi_0 draws (3000, not S0),
12 terminal rounds at phi = 1, with the production block packing (v3_blocks.h rule); (c) Theorem-B bookkeeping
at the pi_0 draws: distribution of v = |M| + |A| + c and the fraction with v > H (bound trivially >= 1).
Data seed 1 (W1's datasets). RNG seed 99.
"""
import sys, json, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import make_data, Model, mask_to_list
from exact_laws import label_laws, indep_accept, first_change_prob


def a1(M, x, j):
    q = []
    for name, law in label_laws(M, x):
        if name == 'G%d' % j:
            continue
        q.append(sum(pr for yy, pr in law.items() if yy != x))
    a = indep_accept(M, x); a[x] = 0
    q.append(float(a.sum()))
    return first_change_prob([1.0] + [0.0] * len(q), [0.0] + q)


def vstat(M, x):
    S0 = M.S0
    miss = [j for j in range(M.p) if S0 >> j & 1 and not x >> j & 1]
    if not miss:
        return M.sizes[x & ~S0]
    A = set()
    for j in miss:
        A |= {l for l in M.Nb[j] if not S0 >> l & 1}
    c = sum(1 for l in range(M.p) if x >> l & 1 and not S0 >> l & 1 and l not in A)
    return len(miss) + len(A) + c


def main(out):
    rng = np.random.default_rng(99)
    recs = []
    for scen in [1, 2, 3, 4, 5, 6]:
        for c in [1.0, 0.5]:
            X, y, S0 = make_data(scen, c, seed=1)
            M = Model(X, y, S0)
            H = M.L + 4
            rows = []
            for j in range(M.p):
                x = S0 ^ (1 << j)
                v = a1(M, x, j)
                _, sc, _ = M.round(np.full(10000, x, dtype=np.int64), rng, target=S0)
                rows.append((v, float(sc.mean()), j, 'del-truth' if S0 >> j & 1 else 'extra'))
            rows.sort()
            # repair from raw pi_0 draws (not S0)
            draws = np.searchsorted(M.cdf0, rng.random(20000), side='right').astype(np.int64)
            draws = draws[draws != S0][:3000]
            S = draws.copy(); done = np.zeros(len(S), dtype=bool); first = np.full(len(S), -1)
            for h in range(H):
                S, sc, _ = M.round(S, rng, target=S0)
                newly = sc & ~done; first[newly] = h + 1; done |= sc
            vs = np.array([vstat(M, int(x)) for x in draws])
            mode = int(M.pi0.argmax())
            rec = dict(scen=scen, c=c, blocks=M.blocks, pi_S0=float(M.post[S0]), pi0_S0=float(M.pi0[S0]),
                       pi0_mode=mask_to_list(mode), pi0_mode_mass=float(M.pi0[mode]),
                       pi0_mode_missing=[j for j in mask_to_list(S0) if not mode >> j & 1],
                       pi0_mode_extras=[j for j in mask_to_list(mode) if not S0 >> j & 1],
                       a1_min=rows[0][0], a1_min_state=[rows[0][2], rows[0][3]], a1_min_sim=rows[0][1],
                       a1_mean=float(np.mean([r[0] for r in rows])), sim_min=min(r[1] for r in rows),
                       a1_le_sim_all=all(r[0] <= r[1] + 3 * math.sqrt(r[1] * (1 - r[1]) / 10000) + 1e-9 for r in rows),
                       repair_round1=float((first == 1).mean()), repair_by2=float(((first >= 1) & (first <= 2)).mean()),
                       repair_byH=float(done.mean()), H=H,
                       v_median=float(np.median(vs)), v_max=int(vs.max()), frac_v_gt_H=float((vs > H).mean()))
            recs.append(rec)
            print(json.dumps(rec), flush=True)
    json.dump(recs, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
