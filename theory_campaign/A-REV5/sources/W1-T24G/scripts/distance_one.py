"""Cor. P1: one-round scoring lower bound at Hamming distance one from S0.
For x = S0 xor {j}: G_j executed at x scores S0 whatever its draw (R4); by Lemma P with Good = {G_j's step},
  P_x(S0 scored during the round) >= a1(x) := int_0^1 prod_{e != G_j} (1 - t q_e(x)) dt,
q_e(x) = P_x(label e changes the state). Exact (Gauss-Legendre, 40 nodes; integrand is a polynomial of degree m-1).
Also MC check of the actual one-round scoring probability (10000 reps, seed 5)."""
import json, sys, math
import numpy as np
from bvs_engine import *
from round_analysis import label_laws, GL_T, GL_W
from simulate import simulate

def a1(M, x, j):
    q = []
    for typ, jj, law in label_laws(M, x):
        if typ == 'G' and jj == j:
            continue
        q.append(sum(pr for dst, pr in law if dst != x))
    acc = M.ind_accept_vector(x); acc[x] = 0
    q.append(acc.sum())
    q = np.clip(np.array(q), 0, 1)
    return float(GL_W @ np.prod(1 - GL_T[:, None] * q[None, :], axis=1))

out = []
rng = np.random.default_rng(5)
for scen in [1, 2, 3, 4, 5, 6]:
    for c in [1.0, 0.5]:
        X, y, S0, b = gen_design(scen, p=20, n=200, c=c, seed=1)
        M = Model(X, y, S0)
        inR, V, miss, extra = region_arrays(M, 20, 4)
        vals = []
        for j in range(M.p):
            x = S0 ^ (1 << j)
            v = a1(M, x, j)
            r = simulate(M, np.full(10000, x, dtype=np.int64), 1, 10000, rng, inR, V)
            vals.append(dict(j=j, kind='del-truth' if S0 >> j & 1 else 'extra', a1=v, sim=float((r['first'] == 0).mean())))
        mn = min(vals, key=lambda d: d['a1'])
        rec = dict(scen=scen, c=c, a1_min=mn['a1'], a1_min_state=mn, a1_mean=float(np.mean([d['a1'] for d in vals])),
                   sim_min=min(d['sim'] for d in vals), all=vals)
        out.append(rec)
        print('S%d c=%.1f a1_min=%.3f (%s j=%d, sim %.3f) a1_mean=%.3f sim_min=%.3f' % (scen, c, mn['a1'], mn['kind'], mn['j'], mn['sim'], rec['a1_mean'], rec['sim_min']), flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
