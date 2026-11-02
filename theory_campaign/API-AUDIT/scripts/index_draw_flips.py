"""Exact count, for each integer k, of the 53-bit uniforms u = x 2^-53 (x in [0, 2^53)) for which the double-precision
index draw floor(fl(u*k)) differs from the exact floor(x k / 2^53).  The long-double core computes u*k exactly
(x k < 2^64 for k < 2^11), so this is exactly the set of uniforms on which an index draw floor(u*k)
(v3_engine.h:150,151,167,171,199) can differ between the two cores.  fl(u*k) can only differ from floor by rounding UP
to an integer k' in 1..k-1, i.e. x k = k' 2^53 - d with 1 <= d <= half-ulp below k' (in units of 2^-53).
Usage: python3 index_draw_flips.py KMAX   -> CSV k,count,prob"""
import sys
from fractions import Fraction
KMAX = int(sys.argv[1]); T = 2 ** 53
print("k,count,prob")
for k in range(1, KMAX + 1):
    cnt = 0
    for kp in range(1, k):
        e = (kp - 1).bit_length() - 1 if kp > 1 else -1      # kp in (2^e, 2^(e+1)]
        dmax = 2 ** e if e >= 0 else 0                       # half-ulp below kp, in units of 2^-53 (kp=1: none)
        for d in range(1, dmax + 1):
            num = kp * T - d
            if num % k: continue
            x = num // k
            if not (0 <= x < T): continue
            u = x * 2.0 ** -53
            if int(u * float(k)) != (x * k) // T: cnt += 1     # python float product = IEEE double RN
    print(f"{k},{cnt},{cnt / T:.3e}")
