"""PC2: check of R1_C card D10 (K07/K06/K22): complete linkage + top-down size cut + next-fit packing (replica of
M §6.3) and the capped symmetric neighbour graph (M §6.4).
(1) strictly separated groups (sizes <= B, within distances < between distances, groups' indices shuffled):
groups never split; if every group > B/2, blocks = groups.  (2) arbitrary correlation matrices: ceil(p/B) <= J <=
2 ceil(p/B), sum 2^|C_b| <= p 2^B / B, |C_b| <= B.  (3) graph: <= pB edges, no isolated vertex for p > 1.
Seeds fixed; < 1 minute."""
import math
import numpy as np
from bvs_common import complete_linkage_tree, cut_tree, next_fit


def partition_from_R(R, B):
    t = complete_linkage_tree(1 - np.abs(R))
    return next_fit(cut_tree(t, B), B)


rng = np.random.default_rng(10)
split = eq_fail = 0
n1 = 0
for it in range(300):
    B = int(rng.integers(2, 10))
    big = it % 2 == 0
    sizes = []
    p = 0
    while p < int(rng.integers(B, 4 * B + 1)):
        s = int(rng.integers(B // 2 + 1, B + 1)) if big else int(rng.integers(1, B + 1))
        sizes.append(s)
        p += s
    gid = np.repeat(np.arange(len(sizes)), sizes)
    perm = rng.permutation(p)
    gid = gid[perm]
    lo_within = rng.uniform(0.3, 0.9)
    R = np.where(gid[:, None] == gid[None, :], rng.uniform(lo_within, 0.99, (p, p)),
                 rng.uniform(-lo_within + 0.01, lo_within - 0.01, (p, p)))
    R = np.triu(R, 1)
    R = R + R.T + np.eye(p)
    blocks = partition_from_R(R, B)
    n1 += 1
    for g in range(len(sizes)):
        members = set(np.where(gid == g)[0])
        hosts = {i for i, C in enumerate(blocks) if members & set(C)}
        if len(hosts) != 1:
            split += 1
            break
    if big:
        bs = sorted(sorted(C) for C in blocks)
        gs = sorted(sorted(np.where(gid == g)[0].tolist()) for g in range(len(sizes)))
        if bs != gs:
            eq_fail += 1
print(f"(1) separated-group instances {n1}: groups split = {split}; blocks != groups when all groups > B/2: {eq_fail}")

cnt_fail = 0
for it in range(300):
    p = int(rng.integers(1, 40))
    B = int(rng.integers(1, 17))
    A = rng.standard_normal((p, p + 3))
    C = A @ A.T
    d = np.sqrt(np.diag(C))
    R = C / np.outer(d, d)
    blocks = partition_from_R(R, B)
    J = len(blocks)
    ok = (math.ceil(p / B) <= J <= 2 * math.ceil(p / B)) and all(1 <= len(c) <= B for c in blocks) \
        and sum(2 ** len(c) for c in blocks) <= p * 2 ** B / B + 1e-9 and sorted(sum(blocks, [])) == list(range(p))
    if not ok:
        cnt_fail += 1
        print("  count fail", p, B, [len(c) for c in blocks])
print(f"(2) counting clauses on 300 random correlation matrices: failures = {cnt_fail}")

g_fail = 0
for it in range(300):
    p = int(rng.integers(2, 40))
    n = int(rng.integers(3, 500))
    B = min(math.isqrt(n), math.isqrt(p), 16)
    A = rng.standard_normal((p, p + 3))
    C = A @ A.T
    d = np.sqrt(np.diag(C))
    R = C / np.outer(d, d)
    rn = math.sqrt(2 * math.log(p) / n)
    Nb = np.zeros((p, p), bool)
    for j in range(p):
        a = np.abs(R[j]).copy()
        a[j] = -1
        order = sorted([l for l in range(p) if l != j], key=lambda l: (-a[l], l))
        part = [l for l in order if a[l] > rn][:B]
        if order[0] not in part:
            part = [order[0]] + part[:B - 1]
        for l in part:
            Nb[j, l] = Nb[l, j] = True
    edges = Nb.sum() // 2
    if edges > p * B or (Nb.sum(1) == 0).any():
        g_fail += 1
print(f"(3) neighbour graph on 300 random inputs: failures (edges > pB or isolated vertex) = {g_fail}")
