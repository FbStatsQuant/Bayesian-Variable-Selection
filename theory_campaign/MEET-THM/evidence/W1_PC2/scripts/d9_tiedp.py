"""PC2: check of R1_C card D9 (K09, N3 tie-DP).  Random integer-valued block tables (exact comparisons, many
ties), size-only capped prior (integer log weights), blocks with interleaved original indices.  Compares
the card's procedure (smallest maximising total size; then for j = 0..p-1 include j iff some optimal completion
consistent with earlier choices contains j; feasibility by constrained max-plus convolution) with brute force under
the prescribed rule (max log pi0, then smallest |S|, then lexicographically smallest sorted index list).
Seeds fixed; < 1 minute."""
import itertools
import numpy as np

NEG = -10 ** 18


def brute(p, blocks, tab, lw, K):
    best = None
    for k in range(K + 1):
        for S in itertools.combinations(range(p), k):
            v = lw[k] + sum(tab[b][tuple(sorted(set(S) & set(C)))] for b, C in enumerate(blocks))
            key = (-v, k, S)
            if best is None or key < best:
                best = key
    return best[2], -best[0]


def maxplus(prof, K):
    acc = [0] + [NEG] * K
    for pr in prof:
        new = [NEG] * (K + 1)
        for i, a in enumerate(acc):
            if a == NEG:
                continue
            for k, v in enumerate(pr):
                if v == NEG or i + k > K:
                    continue
                new[i + k] = max(new[i + k], a + v)
        acc = new
    return acc


def card_dp(p, blocks, tab, lw, K):
    def profiles(fixed):  # fixed: dict index -> bool
        prof = []
        for b, C in enumerate(blocks):
            pr = [NEG] * (len(C) + 1)
            for k in range(len(C) + 1):
                for U in itertools.combinations(sorted(C), k):
                    if all((j in U) == v for j, v in fixed.items() if j in C):
                        pr[k] = max(pr[k], tab[b][U])
            prof.append(pr)
        return prof
    tot = maxplus(profiles({}), K)
    vals = [tot[k] + lw[k] if tot[k] != NEG else NEG for k in range(K + 1)]
    opt = max(vals)
    kstar = min(k for k in range(K + 1) if vals[k] == opt)
    fixed = {}
    for j in range(p):
        trial = dict(fixed)
        trial[j] = True
        t = maxplus(profiles(trial), K)
        fixed[j] = (t[kstar] != NEG and t[kstar] + lw[kstar] == opt)
    S = tuple(j for j in range(p) if fixed[j])
    assert len(S) == kstar
    return S, opt


rng = np.random.default_rng(9)
mism = 0
ntest = 0
for it in range(400):
    p = int(rng.integers(2, 10))
    K = int(rng.integers(1, p + 1))
    perm = rng.permutation(p)
    cuts = sorted(rng.choice(np.arange(1, p), size=int(rng.integers(0, p)), replace=False)) if p > 1 else []
    blocks = [sorted(map(int, c)) for c in np.split(perm, cuts)]
    tab = []
    for C in blocks:
        t = {}
        for k in range(len(C) + 1):
            for U in itertools.combinations(sorted(C), k):
                t[U] = 0 if k == 0 else int(rng.integers(-2, 3))   # many exact ties
        tab.append(t)
    lw = [int(-k * rng.integers(0, 2)) for k in range(K + 1)]
    a = brute(p, blocks, tab, lw, K)
    b = card_dp(p, blocks, tab, lw, K)
    ntest += 1
    if a != b:
        mism += 1
        if mism <= 5:
            print("MISMATCH", p, K, blocks, a, b)
print(f"D9 tie-DP: {ntest} random tied instances, mismatches vs brute force = {mism}")
