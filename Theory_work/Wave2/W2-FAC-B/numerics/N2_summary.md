## N2: size-saturated start (p > n/2), exact Gram, one factor r = 0.5 (compound symmetry rho = 0.5), aligned truths
Script n2_saturated.py (args 0.5 600 500 1.0 0); output reproduced verbatim:

    {"n": 600, "p": 500, "K": 300, "B": 16, "start": 300, "has_S0": true, "t": 35.9}
    {"moves": 315, "counts": {"swN>N": 19, "-N": 296}, "final_is_S0": true, "symdiff": 296, "cap_MR1": 311, "excess": 19, "first_del_at": 19, ...}

Reading: |S~0| = K = 300 (saturated). The uncapped path makes 19 null-null swaps first (noise fitting: outside nulls
with large residual statistic replace kept nulls with small ones; at |T| = n/2 the residual degrees of freedom halve,
doubling the RSS effect of each swap), then 296 deletions; it reaches S0 after 315 moves. The MR1 cap is
ell_n + |S~0| = 11 + 300 = 311 < 315 - 1, so LS0 with MR1 makes 311 moves; its last scanned centre (after 19 swaps and 292
deletions) has 4 extras, its complete final scan returns the improving neighbour with 3 extras (local_limit), and S0 is
not scored (R07 item 10). One data set; an obstruction illustration for the LS0 route, not a statement about the full method.
