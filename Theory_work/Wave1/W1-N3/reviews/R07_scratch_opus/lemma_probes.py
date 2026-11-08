"""lemma_probes.py -- black-box falsification of the intermediate claims L2-L5 through the frozen start_mode.

L2 probe: single-block instance, lambda(j) = 0 and lambda(k) = -BIG for k != j  =>  res.lg0 = mu(j) = max_{|U|=j} rho(U),
          res.ties = #maximisers of size j (if < cap), res.S = lex-min maximiser.
L3/L4 probe: for every prefix b = 1..J (instance restricted to blocks 0..b-1, indices relabelled order-preservingly)
          and every feasible prefix size k <= min(K, |C_0 u..u C_{b-1}|): lambda = 0 at k, -BIG elsewhere
          =>  res.lg0 = V_b(k). (Black-box output checks, not inspection of internal M cells; row b = 0 and
          infeasible cells k > prefix size are not probed.)
L5 probe: for every cap = 1..min(N,60): (res.S, ties, truncated) == predicted (lex-min of the DFS-first cap elements,
          min(N,cap), [N >= cap]). Output/count/flag checks only: non-record visits are not observed, so this does
          not recover the full visiting order.
Integer tables, |values| <= 10^4, BIG = 10^9: all sums exact in binary64.
"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import combinations
from n3lib import Inst, run_tables, predict, dfs_key, prescribed

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
BIG = 10**9
fails = {"L2": 0, "L3": 0, "L5": 0}
counts = {"L2": 0, "L3": 0, "L5": 0}

def rand_inst(pmax=9, maxb=4, vals=(0, 1, 1, 2, -1)):
    p = rng.randint(1, pmax); idx = list(range(p)); rng.shuffle(idx)
    blocks = []; i = 0
    while i < p:
        m = rng.randint(1, min(maxb, p - i)); blocks.append(sorted(idx[i:i + m])); i += m
    rng.shuffle(blocks)
    K = rng.randint(0, p)
    rho = [{c: (rng.choice(vals) if c and bin(c).count("1") <= min(len(C), K) else (0 if c == 0 else float("nan"))) for c in range(1 << len(C))} for C in blocks]
    return Inst(p, K, blocks, [rng.choice([0, -1]) for _ in range(K + 1)], rho)

# L2
insts, exp = [], []
for t in range(1500):
    m = rng.randint(1, 6); K = rng.randint(0, m); C = list(range(m))
    rho = {c: (rng.choice([0, 1, 2, 2]) if c and bin(c).count("1") <= K else (0 if c == 0 else float("nan"))) for c in range(1 << m)}
    j = rng.randint(0, K)
    lam = [0 if k == j else -BIG for k in range(K + 1)]
    I = Inst(m, K, [C], lam, [rho], 10**6, f"L2-{t}")
    vals = {c: rho[c] for c in range(1 << m) if bin(c).count("1") == j}
    mu = max(vals.values()); maxi = sorted(c for c in vals if vals[c] == mu)
    # if mu - BIG ... other sizes are -BIG + something < mu as long as values small
    sets = sorted([sorted(x for x in range(m) if c >> x & 1) for c in maxi])
    insts.append(I); exp.append((mu, len(maxi), sets[0]))
for I, R, (mu, nmax, S) in zip(insts, run_tables(insts), exp):
    counts["L2"] += 1
    if not (R["lg0"] == mu and R["ties"] == nmax and R["S"] == S):
        fails["L2"] += 1; print("FAIL L2", I.iid, R, mu, nmax, S)

# L3/L4 (prefix instances, all k)
insts, exp = [], []
for t in range(300):
    I0 = rand_inst()
    for b in range(1, len(I0.blocks) + 1):
        blocks = I0.blocks[:b]; members = sorted(x for C in blocks for x in C); rel = {x: i for i, x in enumerate(members)}
        nb = [[rel[x] for x in C] for C in blocks]; pb = len(members); Kb = min(I0.K, pb)
        for k in range(Kb + 1):
            rho = [{c: (I0.rho[q][c] if bin(c).count("1") <= min(len(C), Kb) else float("nan")) for c in range(1 << len(C))} for q, C in enumerate(blocks)]
            lam = [0 if kk == k else -BIG for kk in range(Kb + 1)]
            I = Inst(pb, Kb, nb, lam, rho, 10**6, f"L3-{t}-{b}-{k}")
            # V_b(k) by direct enumeration of choice tuples = subsets of size k
            V = max(sum(rho[q][sum(1 << nb[q].index(x) for x in S if x in nb[q])] for q in range(b) if any(x in nb[q] for x in S)) for S in combinations(range(pb), k))
            insts.append(I); exp.append(V)
for I, R, V in zip(insts, run_tables(insts), exp):
    counts["L3"] += 1
    if R["lg0"] != V:
        fails["L3"] += 1; print("FAIL L3", I.iid, R, V)

# L5: predicted prefix outputs for cap = 1..min(N,60)
insts, preds = [], []
for t in range(400):
    I0 = rand_inst(vals=(0, 1, 1))
    N = predict(I0)["nA"]
    for cap in range(1, min(N, 60) + 1):
        I = Inst(I0.p, I0.K, I0.blocks, I0.lam, I0.rho, cap, f"L5-{t}-{cap}")
        insts.append(I); preds.append(predict(I))
for I, R, P in zip(insts, run_tables(insts), preds):
    counts["L5"] += 1
    if not (R["S"] == P["S"] and R["ties"] == P["ties"] and R["truncated"] == P["truncated"]):
        fails["L5"] += 1; print("FAIL L5", I.iid, R, P)
print("probes:", counts, "fails:", fails)
