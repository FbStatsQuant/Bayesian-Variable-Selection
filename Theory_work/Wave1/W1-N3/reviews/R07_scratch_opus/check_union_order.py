"""Exhaustive check of L1(iii): for equal-size X != Y subsets of {0..p-1}, p <= 8:
sorted(X) < sorted(Y) (Python list order = std::lexicographical_compare) iff min(X ^ Y) in X."""
from itertools import combinations
n = bad = 0
for p in range(1, 9):
    for k in range(0, p + 1):
        S = [frozenset(c) for c in combinations(range(p), k)]
        for X in S:
            for Y in S:
                if X == Y: continue
                n += 1
                if (sorted(X) < sorted(Y)) != (min(X ^ Y) in X): bad += 1
print("pairs", n, "violations", bad)
