#!/usr/bin/env python3
"""List GP(d) failures for CF(c) (see cf_family.py). Usage: python3 gp_fail_probe.py n c d"""
import sys, itertools, numpy as np
sys.argv = sys.argv[:1] + sys.argv[1:]
import cf_family as cf
n, c, d = map(int, sys.argv[1:4])
D = cf.build(n, c); sc = cf.Scorer(D); p = D['p']; S0 = D['S0']; K = sc.K
nulls = [j for j in range(p) if j not in S0]
def moves(S):
    out = []
    for j in range(p):
        if j in S: out.append(tuple(x for x in S if x != j))
        elif len(S) < K: out.append(tuple(sorted(S + (j,))))
    for j in S:
        for l in range(p):
            if l not in S: out.append(tuple(sorted(tuple(x for x in S if x != j) + (l,))))
    return out
lab = lambda S: tuple((j + 1, int(D['cl'][j]) + 1 if D['cl'][j] >= 0 else 0) for j in S)
for k in range(len(S0) + 1):
    for U in itertools.combinations(S0, k):
        for m in range(d + 1):
            for P in itertools.combinations(nulls, m):
                S = tuple(sorted(U + P))
                if S == S0: continue
                nb = moves(S); Fv = sc.F_many(nb); i = int(np.argmax(Fv)); b = min(nb[q] for q in range(len(nb)) if Fv[q] == Fv[i])
                dist = lambda x: len(set(x) ^ set(S0))
                ok = Fv[i] > sc.F(S) and len(set(b) - set(S0)) <= d and dist(b) < dist(S)
                if not ok:
                    # does the greedy path from S still reach S0 within ell+1 moves?
                    cur = S; path = [S]
                    for _ in range(12):
                        nb2 = moves(cur); F2 = sc.F_many(nb2); i2 = int(np.argmax(F2))
                        if F2[i2] <= sc.F(cur): break
                        cur = min(nb2[q] for q in range(len(nb2)) if F2[q] == F2[i2]); path.append(cur)
                    print("fail at", lab(S), "best move ->", lab(b), "gain %.2f" % (Fv[i] - sc.F(S)),
                          "| greedy path reaches S0:", S0 in path, "in", len(path) - 1, "moves; path:", [lab(x) for x in path])
