#!/usr/bin/env python3
"""W5-LOCKBOOK: evaluate the T32(i) score-evaluation ceiling (PROOF.md, Theorem T32(i)) at given (n, p).

Deterministic; no randomness (SEED fixed for protocol form). Budgets copied from v3_preprocess.R:19-33.
Compares the proved ceiling C_eval with the conjectured T32(i) right-hand side (theorems/T32_T23C_resource_counts.md),
and checks numerically (for a grid of (n, p)) the slack inequality used in Corollary T32(i-lit).
"""
import math, sys, json

SEED = 0

def isqrt(x):
    return math.isqrt(int(x))

def ceil_log2(x):
    c = 0
    while 2 ** c < x:
        c += 1
    return c

def budgets(n, p):
    K = min(p, n // 2)
    B = min(isqrt(n), isqrt(p), 16)
    ell = ceil_log2(n + p + 1)
    L = max(4, ceil_log2(n + 1))
    N0 = max(2500, n, p)
    H0 = (512 * N0 + 2499) // 2500
    T0 = max(1000, ell ** 2)
    return dict(K=K, B=B, ell=ell, L=L, N=[N0, 4 * N0], H=[H0, 4 * H0], T=[T0, 4 * T0])

def kstar(p, K):
    return min(K, p // 2)

def table_bound(p, B):
    # sum_b 2^{|C_b|} <= p 2^B / B (2^c/c nondecreasing on c >= 1); exact value depends on the partition
    return p * 2 ** B // B

def ceiling(n, p, tiers=(0, 1), final_tier=1):
    b = budgets(n, p)
    K, B, ell, L = b["K"], b["B"], b["ell"], b["L"]
    m = p + B + 2
    ks = kstar(p, K)
    Mp = p + ks * (p - ks)
    tab = table_bound(p, B)
    cal = 0
    for e in tiers:
        H, T = b["H"][e], b["T"][e]
        cal += (1 + 4 * ell) * H * (1 + m * (T + L + 4))      # pilot + <= 4 ell diagnostic islands
        cal += (ell + 1) * (1 + (ell + 1) * Mp)               # <= ell + 1 local searches (centre + <= ell + 1 scans)
        cal += (ell + 1) * (40 * p + 1)                       # <= ell + 1 V rescorings, |V| <= 40p + 1
    N, T = b["N"][final_tier], b["T"][final_tier]
    fin = 4 * N * (1 + m * (T + L + 4)) + (80 * p + 1) + 1 + (ell + 1) * Mp
    total = tab + cal + fin
    # conjectured RHS (theorem file): both tiers, 2m per round, (8 ell + 3)(ell + 1) scans
    conj = tab + sum((1 + 4 * ell) * b["H"][e] * (1 + 2 * m * (b["T"][e] + L + 4)) for e in (0, 1)) \
        + 4 * b["N"][1] * (1 + 2 * m * (b["T"][1] + L + 4)) + (8 * ell + 3) * (ell + 1) * Mp
    parts = dict(tables=tab, calibration=cal, final=fin, local_search_scans=(2 * ell + 3) * (ell + 1) * Mp,
                 rounds=None)
    return dict(n=n, p=p, budgets=b, m=m, Mp=Mp, C_eval_ceiling=total, conjectured_rhs=conj,
                conj_minus_proved=conj - total, parts=parts)

def slack_check():
    """Corollary T32(i-lit): conj - proved >= 0 for every (n, p) on the SMC branch. Check on a grid."""
    worst = None
    for n in [3, 5, 10, 20, 50, 100, 200, 400, 1000, 5000, 10 ** 5, 10 ** 7]:
        for p in [1, 2, 5, 18, 50, 100, 500, 1000, 5000, 10 ** 5, 10 ** 7]:
            r = ceiling(n, p)
            ratio = r["conj_minus_proved"]
            if worst is None or ratio < worst[0]:
                worst = (ratio, n, p)
            assert ratio >= 0, (n, p)
    return worst

if __name__ == "__main__":
    out = {}
    for (n, p) in [(200, 500), (200, 1000), (800, 1000), (10 ** 4, 10 ** 5)]:
        r = ceiling(n, p)
        r0 = ceiling(n, p, tiers=(0,), final_tier=0)
        out[f"n={n},p={p}"] = dict(m=r["m"], Mp=r["Mp"], ell=r["budgets"]["ell"], L=r["budgets"]["L"],
                                   C_eval_both_tiers=r["C_eval_ceiling"], C_eval_tier0_only=r0["C_eval_ceiling"],
                                   conjectured_rhs=r["conjectured_rhs"],
                                   ratio_conj_over_proved=r["conjectured_rhs"] / r["C_eval_ceiling"],
                                   local_searches=2 * r["budgets"]["ell"] + 3,
                                   scan_evals_all_LS=(2 * r["budgets"]["ell"] + 3) * (1 + (r["budgets"]["ell"] + 1) * r["Mp"]))
    w = slack_check()
    out["slack_check_min_conj_minus_proved"] = dict(value=w[0], n=w[1], p=w[2])
    print(json.dumps(out, indent=1, default=float))
