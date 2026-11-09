"""Falsification run for the post-first-deletion conjectures (C1 no additions, C2 terminate only at S0,
C3 swap count W=o(n) / W<=K, C4 no truth moves). Output: exp_paths_out.jsonl (one row per run)."""
import math, json, sys, time
import numpy as np
from pathsim import Model, run

ns = [int(x) for x in sys.argv[1].split(',')]
cs = [float(x) for x in sys.argv[2].split(',')]
seeds = range(int(sys.argv[3]))
outf = sys.argv[4] if len(sys.argv) > 4 else 'exp_paths_out.jsonl'
with open(outf, 'a') as fh:
    for n in ns:
        for c in cs:
            for s0 in (1, 2):
                for seed in seeds:
                    t0 = time.time()
                    m = Model(n, c, s0, seed)
                    r = run(m)
                    ev = r.pop('events')
                    sw = [e for e in ev if e[1] == 's']
                    ks = [e[2] for e in sw]
                    after = [e for e in sw if r['first_del'] is not None and e[0] > r['first_del']]
                    xs = [e[3] for e in ev]; Ms = [e[4] for e in ev]
                    imp_xi = [e[7] for e in sw]; exp_xi = [e[6] for e in sw]
                    row = dict(n=n, c=c, s0=s0, seed=seed, K=m.K, **r,
                               W_over_n=r['nswap'] / n, W_le_K=r['nswap'] <= m.K,
                               initial_swaps=r['first_del'], swaps_after_first_del=len(after),
                               min_k_at_swap=min(ks) if ks else None,
                               swaps_k_le_sqrtn=sum(1 for k in ks if k <= math.sqrt(n)),
                               swaps_k_le_n075=sum(1 for k in ks if k <= n ** 0.75),
                               centre_min=min(xs), centre_max=max(xs), M_min=min(Ms), M_max=max(Ms),
                               min_abs_import_xi=min((abs(v) for v in imp_xi), default=None),
                               max_abs_export_xi=max((abs(v) for v in exp_xi), default=None),
                               n_pos_imports=sum(1 for v in imp_xi if v > 0),
                               min_del_gain=min((e[5] for e in ev if e[1] == 'd'), default=None),
                               secs=round(time.time() - t0, 1))
                    fh.write(json.dumps(row) + '\n'); fh.flush()
                    print(json.dumps({k: row[k] for k in ('n', 'c', 's0', 'seed', 'nswap', 'nadd', 'final_is_S0', 'initial_swaps', 'swaps_after_first_del', 'min_k_at_swap', 'reimports', 'centre_min', 'centre_max', 'M_max', 'secs')}))
