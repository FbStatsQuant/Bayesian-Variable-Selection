"""run_checks.py -- brute-force falsification of Theorem N3-code (a)-(e) and of TDP (f) on small instances.

Usage: python -I run_checks.py [seed]   (writes results to stdout; summary table at the end)
Every instance is enumerated completely (all S with |S| <= K, p <= 12).
"""
import random
import sys
import math
from itertools import permutations, product
from fractions import Fraction

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from n3lib import Inst, predict, prescribed, run_tables, run_data, ghat, f_exact, dfs_key
from tdp import tdp

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20261108
rng = random.Random(SEED)
stats = {}


def bump(fam, key, n=1):
    stats.setdefault(fam, {}).setdefault(key, 0)
    stats[fam][key] += n


def rand_partition(p, maxb):
    idx = list(range(p))
    rng.shuffle(idx)
    blocks = []
    i = 0
    while i < p:
        m = rng.randint(1, min(maxb, p - i))
        blocks.append(sorted(idx[i:i + m]))
        i += m
    rng.shuffle(blocks)
    return blocks


def rand_tables(blocks, K, vals):
    rho = []
    for C in blocks:
        m = len(C)
        d = {0: 0}
        for c in range(1, 1 << m):
            d[c] = rng.choice(vals) if bin(c).count("1") <= min(m, K) else float("nan")
        rho.append(d)
    return rho


def check_table_batch(fam, insts):
    res = run_tables(insts)
    for I, R in zip(insts, res):
        P = predict(I)
        bump(fam, "instances")
        ok_a = (R["lg0"] == float(P["lg0"])) and (len(R["S"]) == P["kstar"]) and f_exact(I, R["S"]) == P["lg0"]
        ok_b = (R["ties"] == P["ties"]) and (R["truncated"] == P["truncated"])
        ok_d = (R["S"] == P["S"])  # exact predicted output, including under truncation
        ok_c = (R["S"] == P["Sstar"]) if P["nA"] <= I.cap else True
        for k, ok in (("a_fail", ok_a), ("b_fail", ok_b), ("c_fail", ok_c), ("d_pred_fail", ok_d)):
            if not ok:
                bump(fam, k)
                print("FAIL", fam, k, I.iid, I.p, I.K, I.blocks, R, {x: P[x] for x in ("S", "Sstar", "nA", "ties")})
        if P["nA"] > 1:
            bump(fam, "ties>1")
        if P["truncated"]:
            bump(fam, "truncated")
            if R["S"] != P["Sstar"]:
                bump(fam, "trunc_wrong(S!=S*)")
        if I.K < sum(len(C) for C in I.blocks) and P["kstar"] == I.K:
            bump(fam, "K_binding(k*=K<p)")
        # (f) TDP
        V, ks, S = tdp(I)
        if not (V == P["lg0"] and ks == P["kstar"] and S == P["Sstar"]):
            bump(fam, "f_fail")
            print("FAIL f", I.iid, S, P["Sstar"])


def fam_random(fam, N, pmax, maxb, vals, lamvals, caps, Kmode="any"):
    insts = []
    for t in range(N):
        p = rng.randint(1, pmax)
        blocks = rand_partition(p, maxb)
        if Kmode == "small":
            K = rng.randint(0, max(0, min(p, 3)))
        else:
            K = rng.randint(0, p)
        lam = [rng.choice(lamvals) for _ in range(K + 1)]
        rho = rand_tables(blocks, K, vals)
        insts.append(Inst(p, K, blocks, lam, rho, rng.choice(caps), f"{fam}-{t}"))
    for i in range(0, len(insts), 500):
        check_table_batch(fam, insts[i:i + 500])


def fam_constructed():
    fam = "constructed"
    insts = []
    # (1) all tables zero, prior constant: every set of every size ties; k* = 0, S* = [] ; and prior increasing in k
    for p in range(1, 9):
        for K in range(0, p + 1):
            blocks = rand_partition(p, 4)
            rho = [{c: (0 if bin(c).count("1") <= min(len(C), K) else float("nan")) for c in range(1 << len(C))} for C in blocks]
            insts.append(Inst(p, K, blocks, [0] * (K + 1), rho, 10**6, f"zero-{p}-{K}"))
            insts.append(Inst(p, K, blocks, list(range(K + 1)), rho, 10**6, f"zeroinc-{p}-{K}"))  # S* = [0..K-1]
    # (2) code order != lex order inside a block: block (a<b<c<d) with rho{a,d} = rho{b,c} = 5 best size-2
    for perm_seed in range(40):
        p = 8
        idx = list(range(p)); rng.shuffle(idx)
        B1 = sorted(idx[:4]); rest = idx[4:]
        blocks = [sorted(rest[:2]), B1, sorted(rest[2:])]
        rng.shuffle(blocks)
        K = rng.choice([2, 3, 4, 8])
        rho = []
        for C in blocks:
            d = {0: 0}
            for c in range(1, 1 << len(C)):
                d[c] = -3 if bin(c).count("1") <= min(len(C), K) else float("nan")
            if C == B1:
                d[0b1001] = 5; d[0b0110] = 5
            rho.append(d)
        lam = [0] * (K + 1)
        insts.append(Inst(p, K, blocks, lam, rho, 10**6, f"codelex-{perm_seed}"))
        insts.append(Inst(p, K, blocks, lam, rho, 1, f"codelex-cap1-{perm_seed}"))
    # (3) allocation ties across blocks: singletons all equal value 1, pairs 2, prior forces size k
    for t in range(60):
        p = rng.randint(2, 10)
        blocks = rand_partition(p, 3)
        K = rng.randint(1, p)
        rho = [{c: (bin(c).count("1") if bin(c).count("1") <= min(len(C), K) else float("nan")) for c in range(1 << len(C))} for C in blocks]
        k0 = rng.randint(0, K)
        lam = [(-1000 if k != k0 else 0) for k in range(K + 1)]
        for cap in (10**6, 1, 2, 3, 7):
            insts.append(Inst(p, K, blocks, lam, rho, cap, f"alloc-{t}-{cap}"))
    # (4) cross-size ties: lam(k) + k*c constant -> every size ties; smallest size wins
    for t in range(40):
        p = rng.randint(1, 10)
        blocks = rand_partition(p, 4)
        K = rng.randint(0, p)
        rho = [{c: (2 * bin(c).count("1") if bin(c).count("1") <= min(len(C), K) else float("nan")) for c in range(1 << len(C))} for C in blocks]
        lam = [-2 * k for k in range(K + 1)]
        insts.append(Inst(p, K, blocks, lam, rho, 10**6, f"xsize-{t}"))
    # (5) K binding inside a block (K < |C_b|): one block of size 5, K in {1,2}, big positive tables
    for t in range(40):
        p = rng.randint(5, 12)
        blocks = rand_partition(p, 5)
        K = rng.choice([1, 2])
        rho = [{c: (rng.choice([3, 4, 4]) * bin(c).count("1") if bin(c).count("1") <= min(len(C), K) else float("nan")) for c in range(1 << len(C))} for C in blocks]
        lam = [0] * (K + 1)
        insts.append(Inst(p, K, blocks, lam, rho, 10**6, f"Kbind-{t}"))
    check_table_batch(fam, insts)


def ordered_partitions(items):
    """all ordered set partitions of a list (blocks sorted internally)"""
    if not items:
        yield []
        return
    n = len(items)
    # assign labels via restricted growth strings, then permute block order
    def rgs(i, a, mx):
        if i == n:
            yield list(a)
            return
        for v in range(mx + 2):
            a.append(v)
            yield from rgs(i + 1, a, max(mx, v))
            a.pop()
    for a in rgs(0, [], -1):
        nb = max(a) + 1
        blocks = [sorted(items[i] for i in range(n) if a[i] == b) for b in range(nb)]
        for perm in permutations(range(nb)):
            yield [blocks[q] for q in perm]


def fam_exhaustive():
    """p <= 3: every ordered partition, every K, every table with values in {0,1} on feasible sub-models,
    prior in {0,1}^{K+1}, caps {1, 2, 10^6}."""
    fam = "exhaustive_p<=3"
    insts = []
    t = 0
    for p in (1, 2, 3):
        for blocks in ordered_partitions(list(range(p))):
            for K in range(0, p + 1):
                cells = [(b, c) for b, C in enumerate(blocks) for c in range(1, 1 << len(C)) if bin(c).count("1") <= min(len(C), K)]
                for tv in product((0, 1), repeat=len(cells)):
                    rho = [{c: float("nan") for c in range(1 << len(C))} for C in blocks]
                    for b in range(len(blocks)):
                        rho[b][0] = 0
                    for (b, c), v in zip(cells, tv):
                        rho[b][c] = v
                    for lam in product((0, 1), repeat=K + 1):
                        for cap in (1, 2, 10**6):
                            insts.append(Inst(p, K, blocks, list(lam), rho, cap, f"ex{t}"))
                            t += 1
    for i in range(0, len(insts), 2000):
        check_table_batch(fam, insts[i:i + 2000])


def standardise(v):
    n = len(v)
    mu = sum(v) / n
    c = [x - mu for x in v]
    ss = math.sqrt(sum(x * x for x in c) / (n - 1))
    return [x / ss for x in c]


def fam_data(N):
    fam = "data(code scorer, real prior)"
    cases = []
    meta = []
    for t in range(N):
        n = rng.choice([2, 2, 3, 3, 4, 6, 10, 20])
        p = rng.randint(1, 10 if n > 2 else 12)
        cols = []
        for j in range(p):
            if j > 0 and rng.random() < 0.35:
                cols.append(list(cols[rng.randrange(j)]))  # exact duplicate column -> exact table ties
            else:
                while True:
                    c = [rng.gauss(0, 1) for _ in range(n)]
                    if max(c) != min(c):
                        break
                cols.append(c)
        cols = [standardise(c) for c in cols]
        beta_on = rng.randrange(p)
        y = [cols[beta_on][i] * rng.choice([0.0, 1.0, 3.0]) + rng.gauss(0, 1) for i in range(n)]
        if max(y) == min(y):
            y[0] += 1.0
        y = standardise(y)
        Bmax = max(1, min(int(math.isqrt(n)), int(math.isqrt(p)), 16))
        B = rng.choice([Bmax, min(p, 4)]) if n > 2 else 1
        X = [v for c in cols for v in c]
        cases.append((f"data-{t}", n, p, B, rng.choice([10**6, 10**6, 1, 2]), X, y))
    out = run_data(cases)
    for I, R in out:
        bump(fam, "instances")
        # (a)-(d) under the EX-A reading of the code's own double tables (Fraction of each double)
        P = predict(I)
        ok = (R["S"] == P["S"]) and R["ties"] == P["ties"] and R["truncated"] == P["truncated"]
        if not ok:
            bump(fam, "exact_reading_mismatch")
            print("NOTE data exact-reading mismatch", I.iid, R, P["S"], P["Sstar"])
        if P["nA"] <= I.cap and R["S"] != P["Sstar"]:
            bump(fam, "c_fail_exact_reading")
        if P["nA"] > 1:
            bump(fam, "ties>1")
        if P["truncated"]:
            bump(fam, "truncated")
        if I.K == 1:
            bump(fam, "K=1 (n<=3)")
        # (e) floating clause: code's own float evaluation ghat
        best = max(ghat(I, S) for S in __import__("n3lib").all_sets(I))
        kmin = min(len(S) for S in __import__("n3lib").all_sets(I) if ghat(I, S) == best)
        ok_e = (R["lg0"] == best) and (ghat(I, R["S"]) == R["lg0"]) and len(R["S"]) == kmin
        if not ok_e:
            bump(fam, "e_fail")
            print("FAIL e", I.iid, R, best, kmin)
        # float lex part (not claimed)
        Af = sorted(S for S in __import__("n3lib").all_sets(I) if ghat(I, S) == best and len(S) == kmin)
        if len(Af) <= I.cap and R["S"] != Af[0]:
            bump(fam, "float_lex_differs(not claimed)")


def fam_capedge(Ninst):
    """N = |A*| known by brute force; rerun the same instance with cap in {N-1, N, N+1} (cap >= 1)."""
    fam = "cap_edge(N-1,N,N+1)"
    base = []
    while len(base) < Ninst:
        p = rng.randint(1, 10)
        blocks = rand_partition(p, 4)
        K = rng.randint(0, p)
        I = Inst(p, K, blocks, [rng.choice([0, -1]) for _ in range(K + 1)], rand_tables(blocks, K, [0, 1, 1]), 10**6, "")
        base.append(I)
    insts = []
    for t, I in enumerate(base):
        N = predict(I)["nA"]
        for cap in sorted({max(1, N - 1), N, N + 1}):
            insts.append(Inst(I.p, I.K, I.blocks, I.lam, I.rho, cap, f"capedge-{t}-N{N}-cap{cap}"))
    for K in range(0, 4):  # K = 0 with cap = 1 (N = 1: only the empty set)
        insts.append(Inst(3, K, [[0, 2], [1]], [0] * (K + 1), [{0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0}], 1, f"K{K}-cap1"))
    check_table_batch(fam, insts)


def fam_fp_stress(N):
    """clause (e) only (native doubles): tables mixing large magnitudes with sub-ulp perturbations so that rounding
    creates ties at block, prefix and prior additions."""
    fam = "fp_stress(e only)"
    from n3lib import all_sets
    insts = []
    for t in range(N):
        p = rng.randint(1, 9)
        blocks = rand_partition(p, 4)
        K = rng.randint(0, p)
        big = rng.choice([1000.0, 2.0**52, 2.0**40, 1.0])
        tiny = [0.0, 1e-14, 2e-14, 0.25, 0.5, 1.0, 2.0]
        rho = []
        for C in blocks:
            d = {0: 0.0}
            for c in range(1, 1 << len(C)):
                d[c] = (rng.choice([big, -big, 0.0]) + rng.choice(tiny)) if bin(c).count("1") <= min(len(C), K) else float("nan")
            rho.append(d)
        lam = [rng.choice([0.0, -big, big, 0.5, -0.5]) for _ in range(K + 1)]
        insts.append(Inst(p, K, blocks, lam, rho, 10**6, f"fp-{t}"))
    res = run_tables(insts)
    for I, R in zip(insts, res):
        bump(fam, "instances")
        sets = list(all_sets(I))
        best = max(ghat(I, S) for S in sets)
        kmin = min(len(S) for S in sets if ghat(I, S) == best)
        ok_e = (R["lg0"] == best) and (ghat(I, R["S"]) == R["lg0"]) and len(R["S"]) == kmin
        if not ok_e:
            bump(fam, "e_fail")
            print("FAIL e", I.iid, R, best, kmin)
        Af = sorted(S for S in sets if ghat(I, S) == best and len(S) == kmin)
        if len(Af) > 1:
            bump(fam, "float_ties>1")
        if R["S"] != Af[0]:
            bump(fam, "float_lex_differs(not claimed)")


if __name__ == "__main__":
    fam_exhaustive()
    fam_constructed()
    fam_random("random_int_heavyties", 4000, 12, 5, [-1, 0, 1, 1, 2], [-2, -1, 0], [10**6])
    fam_random("random_int_01", 3000, 12, 4, [0, 1], [0, 0, -1], [10**6])
    fam_random("random_trunc_smallcap", 3000, 12, 5, [0, 1, 1], [0], [1, 2, 3, 5])
    fam_random("random_Ksmall", 2000, 12, 5, [-1, 0, 1, 2], [-1, 0], [10**6, 2], Kmode="small")
    fam_random("random_wide", 1000, 12, 5, list(range(-30, 31)), list(range(-5, 1)), [10**6])
    fam_data(400)
    fam_capedge(800)
    fam_fp_stress(3000)
    print("\nSEED", SEED)
    for fam, d in stats.items():
        print(fam, d)
