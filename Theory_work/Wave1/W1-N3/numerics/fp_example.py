"""fp_example.py -- clause (e): in binary64 the lexicographic part can fail relative to the code's own float
evaluation ghat = Start::log_gamma0. Blocks (in order): C_0 = {0}, rho = 1000.0; C_1 = {1,2}, rho{1} = 1e-14,
rho{2} = 2e-14, rho{1,2} = -5. K = 2, lambda = (0, -1, 0).
fl(1000 + 1e-14) = fl(1000 + 2e-14) = 1000 (half-ulp of 1000 is 2^-44 ~ 5.7e-14), so ghat({0,1}) = ghat({0,2}) = 1000
= max ghat, and the float size-then-lex choice is {0,1}; the code follows only the per-block exact maximiser {2}
and returns {0,2}. (Under EX-A, {0,2} is the unique maximiser, so clause (c) itself is not contradicted.)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import Inst, run_tables, ghat, all_sets, prescribed
I = Inst(3, 2, [[0], [1, 2]], [0.0, -1.0, 0.0], [{0: 0, 1: 1000.0}, {0: 0, 1: 1e-14, 2: 2e-14, 3: -5.0}], 10**6, "fp")
R = run_tables([I])[0]
best = max(ghat(I, S) for S in all_sets(I))
Af = sorted(S for S in all_sets(I) if ghat(I, S) == best)
print("code:", R)
print("max ghat =", best, " float argmax sets:", Af, " float size-then-lex choice:", min(Af, key=lambda S: (len(S), S)))
print("ghat(code S) == lg0 == max ghat:", ghat(I, R["S"]) == R["lg0"] == best)
print("exact-real prescribed (EX-A):", prescribed(I)[3])

# Second example (from the statement-lock reviewer R01): rounding at the PRIOR addition.
# One block {0,1}, K = 1, lambda = (0, 2^54), rho{0} = 1, rho{1} = 2: ghat({0}) = fl(2^54 + 1) = 2^54 = fl(2^54 + 2)
# = ghat({1}); the float size-then-lex choice is {0}; the code's per-block exact maximiser is {1}.
I2 = Inst(2, 1, [[0, 1]], [0.0, 2.0**54], [{0: 0, 1: 1.0, 2: 2.0, 3: float("nan")}], 10**6, "fp2")
R2 = run_tables([I2])[0]
best2 = max(ghat(I2, S) for S in all_sets(I2))
Af2 = sorted(S for S in all_sets(I2) if ghat(I2, S) == best2)
print("example 2 code:", R2, " float argmax:", Af2, " ghat(code S)==lg0==max:", ghat(I2, R2["S"]) == R2["lg0"] == best2)
