"""Exact population grid on the two-state family (Theorem M). Deterministic; no randomness."""
import numpy as np
from math import log2, log
from grid_core import greedy_grid, F_two_state

print("A0 = start masking depth log[pi0(S°)/pi0(S0)], A1 = log[pi(S0)/pi(S°)]")
print(f"{'A0':>9} {'A1':>9} {'T*':>4} {'log2 A0':>8} {'T*-log2A0':>9}  grid head")
for A1 in [5.0, 50.0, 1e3, 1e5]:
    for A0 in [0.5, 2.0, 8.0, 32.0, 94.0, 128.0, 336.0, 1e3, 1e4, 1e5, 1e6]:
        g = greedy_grid(F_two_state(A0, A1))
        T = len(g) - 1
        print(f"{A0:9.4g} {A1:9.4g} {T:4d} {log2(A0):8.3f} {T-log2(A0):9.3f}  {' '.join(f'{x:.4f}' for x in g[:5])}")
# D -> infinity at fixed t* (W''): count grows like log2(D t*)
print("\nfixed t* = 1/2 (A0 = A1 = D/2): W'' predicts O(1); Theorem M predicts log2(D/2) + O(1)")
for D in [10, 100, 1e3, 1e4, 1e5, 1e6, 1e7]:
    g = greedy_grid(F_two_state(D / 2, D / 2)); T = len(g) - 1
    # stages inside the crossing window |s| <= 3 (s = D(t - t*))
    s = [(x - 0.5) * D for x in g]
    win = sum(1 for a in s if abs(a) <= 3)
    print(f"D={D:9.3g}  T*={T:3d}  log2(D/2)={log2(D/2):6.2f}  T*-log2(D/2)={T-log2(D/2):6.2f}  grid points with |s|<=3: {win}")
