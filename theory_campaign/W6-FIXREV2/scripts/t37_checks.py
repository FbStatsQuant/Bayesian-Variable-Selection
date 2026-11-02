"""W6-FIXREV2: independent checks for the T37 items of A-REV2 (seed 20261102 where randomness is used).

(1) CEX-1 (positivity): literal strict TD(0,0) holds on R_0 but the search from the empty model certifies empty.
(2) CEX-2 (posterior miss with E_LS true): search starts below the truth, climbs to a superset, certifies it.
(3) Exact-tie counterexample (A-REV2 §4.3): TD'_P(R_0) holds via the tie-broken map M, strict D_empty fails.
(4) Inferior local maximum with E_LS true (A-REV2 §4.2): the (E_LS^c) / (E_LS and F_post >= F(S0)) dichotomy omits it.
(5) Exhaustive logic checks on random small designs (some with duplicate columns, so exact ties occur):
    (a) D_lex(S) <=> M(S) != bottom and M(S) is a progress move   [the repaired equivalence]
    (b) D_strict(S) => D_lex(S)                                   [strict D_S is sufficient]
    (c) count states with D_lex true and D_strict false            [the 'iff' fails only through exact ties]
    (d) three-way failure partition of the final local search: categories I / II / III all occur; exhaustive by
        construction; category II = search miss (F_post < F(S0)), I ∪ III = posterior miss.
"""
import itertools, json, sys
import numpy as np
from core import BVS, frame, phi, is_progress, D_strict, D_lex, TDP_via_M, region

OUT = {}


def gains_literal_TD0(m, S0):
    """Literal strict TD(0,0) on R_0 = subsets of S0 (d = 0): clause 1 at S ⊊ S0, clause 3 at S0."""
    S0 = tuple(sorted(S0)); bad = 0
    for k in range(len(S0) + 1):
        for U in itertools.combinations(S0, k):
            S = tuple(sorted(U)); FS = m.F(S)
            nb = m.neighbours(S)
            if S == S0:
                if max(m.F(T) for T in nb) - FS >= 0:  # clause 3 strict: every move gain < 0
                    bad += 1
                continue
            miss = [j for j in S0 if j not in S]
            adds = [tuple(sorted(S + (j,))) for j in miss] if len(S) < m.K else []
            if not adds:
                bad += 1; continue
            best_add = max(adds, key=lambda T: m.F(T))
            others = [T for T in nb if T != best_add]
            if not (m.F(best_add) > max(m.F(T) for T in others)):
                bad += 1
    return bad


def cex1():
    n, rng = 100, np.random.default_rng(1)
    E = frame(n, 13, rng)
    r = 0.95
    X = np.column_stack([E[:, 0], r * E[:, 0] + np.sqrt(1 - r * r) * E[:, 1]] + [E[:, j] for j in range(2, 12)])
    y = 3 * X[:, 0] - 2.8 * X[:, 1] + E[:, 12]
    m = BVS.from_data(X, y); S0 = (0, 1)
    gains = {T: m.F(T) - m.F(()) for T in m.neighbours(())}
    best = max(gains.values())
    allS = [S for k in range(m.p + 1) for S in itertools.combinations(range(m.p), k)]
    F = np.array([m.F(S) for S in allS]); F -= F.max(); P = np.exp(F); P /= P.sum()
    post = float(P[allS.index(S0)])
    ls = m.local_search((), 10)
    res = dict(literal_TD00_failing_clauses=gains_literal_TD0(m, S0), best_gain_at_empty=best,
               truth_gain_over_empty=m.F(S0) - m.F(()), posterior_S0=post,
               global_HPM=list(allS[int(np.argmax(P))]),
               search_from_empty=dict(returned=list(ls['returned']), certified=ls['certified']))
    OUT['cex1_positivity'] = res
    return res


def cex2():
    """Same structure as W3-VT37R CEX-2 but rebuilt independently: truths x0, x1; null x2 receives part of the noise."""
    n, rng = 100, np.random.default_rng(3)
    q = 6
    E = frame(n, q + 4, rng)
    X = E[:, :q + 3]
    al = 0.45
    y = 0.5 * (E[:, 0] + E[:, 1]) + (al * E[:, 2] + np.sqrt(1 - al * al) * E[:, q + 3])
    m = BVS.from_data(X, y); S0 = (0, 1); Sc = (0, 2)
    ls = m.local_search(Sc, 10)
    Fpost = max(m.F(T) for T in ls['scanned'])
    res = dict(F_Sc_minus_F_S0=m.F(Sc) - m.F(S0), F_S0plus2_minus_F_S0=m.F((0, 1, 2)) - m.F(S0),
               path=[list(s) for s in ls['path']], returned=list(ls['returned']), certified=ls['certified'],
               E_LS=bool(m.F(S0) > m.F(Sc)), F_post_minus_F_S0=Fpost - m.F(S0), category='III')
    OUT['cex2_postmiss_with_ELS'] = res
    return res


def tie_example():
    """A-REV2 §4.3 via sufficient statistics: n=100, x1 = x2, S0={0}, y^r = .5 x1 + e, e ⟂ x1, ||e||^2 = 99."""
    n = 100; N = n - 1
    # contrast-scale: Y = .5 x + e, ||x||^2 = N, ||e||^2 = N, x ⟂ e  =>  ||Y||^2 = .25N + N, s_y^2 = 1.25
    sy = np.sqrt(1.25)
    G = N * np.ones((2, 2)); z = np.full(2, 0.5 * N / sy); yy = N
    m = BVS(G, z, yy, n); S0 = (0,)
    res = dict(F1_minus_F2=m.F((0,)) - m.F((1,)), gain_empty_to_0=m.F((0,)) - m.F(()),
               gain_add_duplicate_at_truth=m.F((0, 1)) - m.F((0,)),
               swap_tie_at_truth=m.F((1,)) - m.F((0,)),
               M_empty=m.M(()), M_truth=m.M((0,)), TDP_R0=TDP_via_M(m, [(), (0,)], S0),
               D_strict_empty=D_strict(m, (), S0), D_lex_empty=D_lex(m, (), S0))
    OUT['tie_counterexample'] = res
    return res


def inferior_local_max():
    """CEX-1 design viewed through the failure partition: pre-search ledger = {empty}; E_LS true; F_post < F(S0)."""
    n, rng = 100, np.random.default_rng(1)
    E = frame(n, 13, rng); r = 0.95
    X = np.column_stack([E[:, 0], r * E[:, 0] + np.sqrt(1 - r * r) * E[:, 1]] + [E[:, j] for j in range(2, 12)])
    y = 3 * X[:, 0] - 2.8 * X[:, 1] + E[:, 12]
    m = BVS.from_data(X, y); S0 = (0, 1)
    ls = m.local_search((), 10)
    Fpre = m.F(()); Fpost = max(max(m.F(T) for T in ls['scanned']), Fpre)
    res = dict(E_LS=bool(m.F(S0) > Fpre), F_post_minus_F_S0=Fpost - m.F(S0), certified=ls['certified'],
               returned=list(ls['returned']),
               in_R2_dichotomy=bool((not (m.F(S0) > Fpre)) or (Fpost >= m.F(S0))), category='II')
    OUT['inferior_local_max'] = res
    return res


def random_design(rng, n, p, dup):
    E = frame(n, p + 1, rng)
    A = rng.standard_normal((p, p)) * 0.6 + np.eye(p)
    X = E[:, :p] @ A.T
    if dup:
        X[:, 1] = X[:, 0]          # exact duplicate -> exact score ties
    s0 = 2
    th = rng.choice([-1, 1], s0) * rng.uniform(0.2, 0.8, s0)
    y = X[:, :s0] @ th + rng.uniform(1.0, 3.0) * E[:, p]
    return BVS.from_data(X, y), tuple(range(s0)) if not dup else (0, 2)


def exhaustive(ndesign=300, seed=20261102):
    rng = np.random.default_rng(seed)
    cnt = dict(states=0, a_viol=0, b_viol=0, lex_not_strict=0, designs_TDP=0, designs_TDP_strict=0,
               cat=dict(I=0, II_cert=0, II_limit=0, III=0, success=0), partition_viol=0, R2_misses=0)
    for d in range(ndesign):
        dup = (d % 3 == 0)
        n = int(rng.choice([20, 30, 60])); p = 7
        m, S0 = random_design(rng, n, p, dup)
        R = region(p, S0, 2, 1, m.K)
        all_lex = True; all_strict = True
        for S in R:
            if S == tuple(sorted(S0)):
                continue
            cnt['states'] += 1
            T = m.M(S)
            lhs = D_lex(m, S, S0); rhs = (T is not None) and is_progress(S, T, S0)
            cnt['a_viol'] += int(lhs != rhs)
            st = D_strict(m, S, S0)
            cnt['b_viol'] += int(st and not lhs)
            cnt['lex_not_strict'] += int(lhs and not st)
            all_lex &= lhs; all_strict &= st
        L0 = m.M(tuple(sorted(S0))) is None
        cnt['designs_TDP'] += int(all_lex and L0)
        cnt['designs_TDP_strict'] += int(all_strict and L0)
        # failure partition: pre-search ledger = a random handful of models incl. a random centre in R
        allS = [S for k in range(m.K + 1) for S in itertools.combinations(range(p), k)]
        for rep in range(4):
            pre = [allS[i] for i in rng.choice(len(allS), 3, replace=False)] + [R[int(rng.integers(len(R)))]]
            Fs = [m.F(S) for S in pre]; Fpre = max(Fs)
            centre = sorted([S for S, f in zip(pre, Fs) if f == Fpre])[0]
            ell = int(rng.choice([1, 2, 10]))
            ls = m.local_search(centre, ell)
            scored = set(pre) | set(ls['scanned'])
            Fpost = max(m.F(S) for S in scored)
            # reported HPM: max F, ties smallest size then lexicographic (00_COMMON)
            hpm = min([S for S in scored if m.F(S) == Fpost], key=lambda S: (len(S), S))
            FS0 = m.F(tuple(sorted(S0)))
            if hpm == tuple(sorted(S0)):
                cnt['cat']['success'] += 1; continue
            if Fpre >= FS0:
                c = 'I'
            elif Fpost < FS0:
                c = 'II_cert' if ls['certified'] else 'II_limit'
                if tuple(sorted(S0)) in scored:
                    cnt['partition_viol'] += 1   # impossible: S0 scored => F_post >= F(S0)
            else:
                c = 'III'
            cnt['cat'][c] += 1
            ELS = (tuple(sorted(S0)) not in pre) and FS0 > Fpre
            if ELS and Fpost < FS0:
                cnt['R2_misses'] += 1         # failures outside V37's two-way dichotomy
    OUT['exhaustive'] = cnt
    return cnt


if __name__ == '__main__':
    for f in (cex1, cex2, tie_example, inferior_local_max, exhaustive):
        r = f(); print(f.__name__, json.dumps(r, default=str))
    with open(sys.argv[1] if len(sys.argv) > 1 else 't37_checks.json', 'w') as fh:
        json.dump(OUT, fh, indent=1, default=str)
