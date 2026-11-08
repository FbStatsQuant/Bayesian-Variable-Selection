"""cex_family.py -- the deviation family D_m of lemmas/L6 through the frozen start_mode, m = 0..12,
caps {1, 2^m, 2^m + 1, 2^(m+1)}. Expected (closed form, L6): N = 2^(m+1); cap <= 2^m -> res.S = E u {b,c} != S*;
cap = 2^m + 1 or 2^(m+1) -> res.S = S* = E u {a,d} (first code-9 element is S*); ties = min(N, cap); truncated = [N >= cap].
Brute-force cross-check of A*, S*, the DFS-prefix prediction for m <= 4 (p <= 12)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import Inst, run_tables, predict
from tdp import tdp
def Dm(m, cap):
    p, K = 2 * m + 4, m + 2
    blocks = [[2 * i, 2 * i + 1] for i in range(m)] + [[2 * m, 2 * m + 1, 2 * m + 2, 2 * m + 3]]
    rho = [{0: 0, 1: 1, 2: 1, 3: -10} for _ in range(m)]
    last = {0: 0}
    for c in range(1, 16):
        last[c] = -3 if bin(c).count("1") <= min(4, K) else float("nan")
    last[9] = 5; last[6] = 5
    rho.append(last)
    return Inst(p, K, blocks, [0] * (K + 1), rho, cap, f"D{m}-cap{cap}")
insts = [Dm(m, cap) for m in range(0, 13) for cap in sorted({1, 2**m, 2**m + 1, 2**(m + 1)})]
fails = 0
for I, R in zip(insts, run_tables(insts)):
    m = (I.p - 4) // 2; N = 2**(m + 1); E = list(range(0, 2 * m, 2))
    Sstar = E + [2 * m, 2 * m + 3]; Sbc = E + [2 * m + 1, 2 * m + 2]
    exp_S = Sbc if I.cap <= 2**m else Sstar
    ok = R["S"] == exp_S and R["ties"] == min(N, I.cap) and R["truncated"] == int(N >= I.cap) and R["lg0"] == m + 5
    ok = ok and tdp(I)[2] == Sstar
    if m <= 4:
        P = predict(I); ok = ok and P["Sstar"] == Sstar and P["nA"] == N and P["S"] == exp_S
    fails += not ok
    print(I.iid, "N=%d" % N, "res.S==S*" if R["S"] == Sstar else "res.S!=S*", "ties=%d trunc=%d" % (R["ties"], R["truncated"]), "OK" if ok else "FAIL")
print("instances", len(insts), "fails", fails)
