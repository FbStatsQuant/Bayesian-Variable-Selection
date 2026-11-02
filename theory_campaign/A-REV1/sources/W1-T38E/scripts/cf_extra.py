#!/usr/bin/env python3
"""E1 margins and SE eigenvalue for CF(c). F(S0)-F(S0 minus cancelled) vs kappa_n(d) = (d+1)[log 2p + 0.5 log(n+1)];
also the best scored-type outside state S0 u P (|P| = d+1, P = top nulls) vs F({1}). Usage: python3 cf_extra.py n c d"""
import sys, math, numpy as np
import cf_family as cf
n, c, d = map(int, sys.argv[1:4])
D = cf.build(n, c); sc = cf.Scorer(D); p = D['p']; S0 = D['S0']
R = np.corrcoef(D['X'].T); lam = np.linalg.eigvalsh(R)[0]
kap = (d + 1) * (math.log(2 * p) + 0.5 * math.log(n + 1))
Fs0 = sc.F(S0); Fref = sc.F((0,))
nulls = [j for j in range(p) if j not in S0]
gains = np.array([sc.F(S0 + (l,)) - Fs0 for l in nulls]); top = [nulls[i] for i in np.argsort(-gains)[:d + 1]]
Fout = sc.F(tuple(sorted(S0 + tuple(top))))
print(f"CF(c={c}) n={n} p={p}: lambda_min(R_full)={lam:.4f}; F(S0)-F(S°={{1}})={Fs0-Fref:.1f}; kappa_n({d})={kap:.1f}; "
      f"F(S0 u top{d+1} nulls)-F(S°)={Fout-Fref:.1f} (>0 => outside-R_{d} state beats S°)")
