"""Falsification of the start-uniform path theorem (P01 Theorem PB): from ANY start U0 with S0 in U0, |U0|<=K,
the uncapped exact path makes no additions, never removes truth, terminates at S0, and W (swaps) is o(n).
Starts: top (actual start), random, bottom (lowest xi nulls), twotail (largest |xi|), middle (smallest |xi|).
Output: exp_starts_out.jsonl."""
import math, json, sys, time
import numpy as np
from pathsim import Model, run

ns = [int(x) for x in sys.argv[1].split(',')]
cs = [float(x) for x in sys.argv[2].split(',')]
nseeds = int(sys.argv[3])
kinds = sys.argv[4].split(',') if len(sys.argv) > 4 else ['top', 'random', 'bottom', 'twotail', 'middle']
with open('exp_starts_out.jsonl', 'a') as fh:
    for n in ns:
        for c in cs:
            for s0 in (1, 2):
                for seed in range(nseeds):
                    m = Model(n, c, s0, seed); K = m.K; p = m.p
                    nul = np.arange(s0, p); xi = m.xi[s0:]
                    rng = np.random.default_rng(10_000 + seed)
                    for kind in kinds:
                        if kind == 'top':
                            st = None
                        elif kind == 'random':
                            st = list(range(s0)) + rng.choice(nul, K - s0, replace=False).tolist()
                        elif kind == 'bottom':
                            st = list(range(s0)) + nul[np.argsort(xi)[:K - s0]].tolist()
                        elif kind == 'twotail':
                            st = list(range(s0)) + nul[np.argsort(-np.abs(xi))[:K - s0]].tolist()
                        elif kind == 'middle':
                            st = list(range(s0)) + nul[np.argsort(np.abs(xi))[:K - s0]].tolist()
                        t0 = time.time()
                        r = run(m, start=st); ev = r.pop('events')
                        truth_moves = sum(1 for e in ev if e[1] in ('D_truth', 'S_truth'))
                        min_gain = min(e[5] for e in ev) if ev else None
                        row = dict(n=n, c=c, s0=s0, seed=seed, start=kind, K=K, moves=r['moves'], W=r['nswap'], A=r['nadd'],
                                   ndel=r['ndel'], final_is_S0=r['final_is_S0'], truth_moves=truth_moves,
                                   W_over_K=r['nswap'] / K, arrival_le_ell_2K=r['moves'] <= math.ceil(math.log2(n + p + 1)) + 2 * K + 1,
                                   reimports=r['reimports'], min_move_gain=min_gain, min_gain_over_logn=min_gain / math.log(n) if ev else None,
                                   secs=round(time.time() - t0, 1))
                        fh.write(json.dumps(row) + '\n'); fh.flush()
                        print(json.dumps(row))
