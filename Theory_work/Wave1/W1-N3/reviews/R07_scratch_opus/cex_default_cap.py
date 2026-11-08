"""cex_default_cap.py -- explicit instance on which the FROZEN start_mode with its default cap 10^6 returns a set
different from the prescribed start mode S* (STATEMENT clause (d)).

Instance (p = 44, K = 22, J = 21 blocks, block order = increasing minimum index, lambda = 0):
  inner blocks C_i = {2i, 2i+1}, i = 0..19:   rho({2i}) = rho({2i+1}) = 1, rho({2i,2i+1}) = -10
  last block   C_20 = {40, 41, 42, 43}:       rho({40,43}) = rho({41,42}) = 5 (codes 9 and 6), every other
                                               nonempty sub-model -3.
Max f = 25, attained exactly by: one element from each inner pair and {40,43} or {41,42} from the last block.
So k* = 22, |A*| = 2 * 2^20 = 2,097,152 > 10^6, and S* = {0,2,4,...,38} u {40,43}.
The coded DFS iterates the LAST block outermost with codes in increasing order, so code 6 = {41,42} comes first and
its 2^20 = 1,048,576 >= 10^6 completions exhaust the cap before code 9 = {40,43} is reached.
Predicted output: {0,2,...,38} u {41,42}, ties = 10^6, truncated = 1.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import Inst, run_tables, f_exact
from tdp import tdp

p, K = 44, 22
blocks = [[2 * i, 2 * i + 1] for i in range(20)] + [[40, 41, 42, 43]]
rho = [{0: 0, 1: 1, 2: 1, 3: -10} for _ in range(20)]
last = {0: 0}
for c in range(1, 16):
    last[c] = -3
last[9] = 5
last[6] = 5
rho.append(last)
I = Inst(p, K, blocks, [0] * (K + 1), rho, 10**6, "cex-default-cap")
R = run_tables([I])[0]
Vstar, kstar, Sstar = tdp(I)
expected_code = list(range(0, 40, 2)) + [41, 42]
print("frozen start_mode:", R)
print("TDP (prescribed S*): V* =", Vstar, "k* =", kstar, "S* =", Sstar)
print("f(code output) =", f_exact(I, R["S"]), " f(S*) =", f_exact(I, Sstar))
print("code output == predicted {0,2,..,38,41,42}:", R["S"] == expected_code)
print("code output == S*:", R["S"] == Sstar)
print("closed-form S* == TDP S*:", Sstar == list(range(0, 40, 2)) + [40, 43])
