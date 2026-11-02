#!/usr/bin/env python3
"""W3-VT38E: independent checks of W1-T38E's CF(c) family claims (PROOF.md sections 6, 8; REPORT evidence table).

Usage: python3 v3_cf_checks.py n c seed [tdmax]
  seed = -1 uses W1's own design (imports build() from W1's cf_family.py, path given by env W1DIR) so that numbers
  can be compared one to one; seed >= 0 uses this run's independent re-implementation of the design (cfi.build_cf).
Prints: lambda_min, block purity, pi0(S0), pi0(S^(0)), pi0(R_d), start mode, LS0 path, iid-miss lower bounds at
tier 0 and tier 1, E1 margins, TD(d,0) as worded in T37 with a classification of the failures, GP(d).
"""
import sys, os, math, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfi

n, c, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
tdmax = int(sys.argv[4]) if len(sys.argv) > 4 else 1

if seed < 0:
    sys.path.insert(0, os.environ.get('W1DIR', '.'))
    import cf_family as w1
    D = w1.build(n, c)
    X, y = D['X'], D['y']
    info = dict(n=n, p=D['p'], B=D['B'], S0=D['S0'], cl=D['cl'], c=c)
    src = "W1 design (cf_family.build, seed 0)"
else:
    X, y, info = cfi.build_cf(n, c, seed)
    src = "independent design, seed %d" % seed
M = cfi.Model(X, y, info)
p, B, S0 = info['p'], info['B'], info['S0']
nulls = [j for j in range(p) if j not in S0]
print("== CF(c=%d) n=%d p=%d B=%d K=%d [%s]" % (c, n, p, B, M.K, src))
blocks, R = cfi.complete_linkage_blocks(X, B)
lam = np.linalg.eigvalsh(R)[0]
bof = {j: b for b, C in enumerate(blocks) for j in C}
pure = all(set(blocks[bof[j]]) == set(np.flatnonzero(info['cl'] == j)) for j in S0)
print("lambda_min(full corr) = %.4f ; truth blocks pure: %s ; J = %d" % (lam, pure, len(blocks)))
st = cfi.Start(M, blocks, S0)
mass = st.mass_by_extras(4)
mode, lmode = st.mode()
print("pi0(S0) = %.3e ; pi0(S^(0)={1}) = %.4f ; pi0(R_d), d=0..3: %s ; start mode = %s (pi0 = %.4f)" % (
    math.exp(st.lpi0(S0)), math.exp(st.lpi0((0,))), np.round(np.cumsum(mass)[:4], 5), tuple(j + 1 for j in mode), math.exp(lmode)))
# budgets
N0 = max(2500, n, p); ell = math.ceil(math.log2(n + p + 1)); T0 = max(1000, ell ** 2); L = max(4, math.ceil(math.log2(n + 1)))
pi0S0 = math.exp(st.lpi0(S0))
Q0 = 4 * N0 * (T0 + L + 5); Q1 = 4 * (4 * N0) * (4 * T0 + L + 5)
print("ell=%d L=%d N0=%d T0=%d ; final-run iid miss (1-pi0(S0))^Qmax: tier0 %.3f, tier1 %.3f" % (
    ell, L, N0, T0, (1 - pi0S0) ** Q0, (1 - pi0S0) ** Q1))
# LS0
path, scored, term = cfi.local_search(M, mode, ell)
print("LS0 from start mode: path %s ; S0 scored: %s ; termination %s" % ([tuple(j + 1 for j in s) for s in path], S0 in scored, term))
# E1
FS0 = M.F(S0); Fm = M.F(mode)
gains = np.array([M.F(tuple(sorted(S0 + (l,)))) - FS0 for l in nulls])
for d in range(3):
    kap = (d + 1) * (math.log(2 * p) + 0.5 * math.log(n + 1))
    top = [nulls[i] for i in np.argsort(-gains)[:d + 1]]
    Fout = M.F(tuple(sorted(S0 + tuple(top))))
    print("E1 d=%d: F(S0)-F(S~0)=%.2f kappa_n(d)=%.2f ; F(S0 u top%d nulls)-F(S~0)=%.2f ; E1 bound check F(S0uP)-F(S0)=%.2f >= -kappa: %s" % (
        d, FS0 - Fm, kap, d + 1, Fout - Fm, Fout - FS0, Fout - FS0 >= -kap))
# TD(d,0) as worded in T37, and GP(d)
def dist(S): return len(set(S) ^ set(S0))
for d in range(tdmax + 1):
    states = []
    for k in range(len(S0) + 1):
        for U in itertools.combinations(S0, k):
            for m in range(d + 1):
                for P in itertools.combinations(nulls, m):
                    states.append(tuple(sorted(U + P)))
    tdfail = 0; tdfail_mixed = 0; mixed = 0; gpfail = 0; gp_reach = 0; tdfail_other = []
    lemma_pred = 0; lemma_ok = 0
    for S in states:
        nb = cfi.flips_swaps(S, p, M.K); Fv = M.F_many(nb); FS = M.F(S)
        gain = Fv - FS
        miss = [j for j in S0 if j not in S]; extras = [l for l in S if l not in S0]
        if S == S0:
            ok = gain.max() <= 0
        elif miss:
            adds = [i for i, x in enumerate(nb) if len(x) == len(S) + 1 and (set(x) - set(S)) <= set(S0)]
            # T37: some missing true j has g(S,j) >= gain of EVERY OTHER feasible move
            ok = any(all(gain[i] >= gain[q] for q in range(len(nb)) if q != i) for i in adds)
        else:
            dels = [i for i, x in enumerate(nb) if len(x) == len(S) - 1 and (set(S) - set(x)) <= set(nulls)]
            ok = any(all(gain[i] >= gain[q] for q in range(len(nb)) if q != i) for i in dels)
        if miss and extras:
            mixed += 1
            if not ok: tdfail_mixed += 1
            if len(miss) == 1 and len(extras) == 1:
                # structural lemma: S = (S0 - j) + l  fails TD whenever F(S0) > F(S0 + l)
                lemma_pred += M.F(S0) > M.F(tuple(sorted(S0 + (extras[0],))))
                lemma_ok += (M.F(S0) > M.F(tuple(sorted(S0 + (extras[0],))))) and (not ok)
        if not ok:
            tdfail += 1
            if not (miss and extras): tdfail_other.append(S)
        # GP(d): best move (max F, lexicographic ties) strictly improves, stays in R_d, reduces |S delta S0|
        mx = Fv.max(); b = min(nb[i] for i in np.flatnonzero(Fv == mx))
        if S == S0: g_ok = mx <= FS
        else: g_ok = mx > FS and len(set(b) - set(S0)) <= d and dist(b) < dist(S)
        if not g_ok:
            gpfail += 1
            pth, sc, _ = cfi.local_search(M, S, ell)
            gp_reach += S0 in sc
    print("TD(%d,0) [T37 wording]: states=%d failures=%d ; states with a missing truth AND an extra: %d, of which fail %d ; "
          "failures of other types: %d %s" % (d, len(states), tdfail, mixed, tdfail_mixed, len(tdfail_other),
                                              [tuple(j + 1 for j in s) for s in tdfail_other[:6]]))
    if d >= 1:
        print("   structural lemma at S=(S0-j)+l: F(S0)>F(S0+l) holds at %d states; TD fails at all of them: %s" % (lemma_pred, lemma_ok == lemma_pred))
    print("GP(%d): failures=%d ; of which the production local search from that centre still scores S0: %d" % (d, gpfail, gp_reach))
