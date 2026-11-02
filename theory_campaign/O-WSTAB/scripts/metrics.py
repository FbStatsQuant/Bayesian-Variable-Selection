"""Per-data-set metrics used by every O-WSTAB experiment (exact; see PROOF.md for definitions)."""
import math

import numpy as np

from wstab_core import cross_eps, leakage, lse


def greedy_grid(P, thr=0.9, tol=1e-6, max_stages=10000):
    """Full-space (V = Omega) T13 grid: from u, the largest v <= 1 with rho_Omega(u, v) = 1/(1+chi2(q_v||q_u)) >= thr.
    log(1+chi2) is nondecreasing in v (convexity of Lambda), so bisection is exact.  Returns the number of stages."""
    u, T = 0.0, 0
    lim = -math.log(thr)
    while u < 1.0 - 1e-12 and T < max_stages:
        if P.log1pchi2(u, 1.0) <= lim:
            return T + 1
        lo, hi = u, 1.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if P.log1pchi2(u, mid) <= lim:
                lo = mid
            else:
                hi = mid
            if hi - lo < tol * max(1e-3, hi - u):
                break
        if lo <= u:
            return float("inf")
        u, T = lo, T + 1
    return T


def row_metrics(P, S0, theta=None, ref=None, grid=True, eps_models=True):
    """Exact divergences between pi0 = q_0 and pi = q_1 and related quantities."""
    i0 = P.space.idx(S0)
    lq0, lq1, lq2 = P.logq(0.0), P.logq(1.0), P.logq(2.0)
    out = {}
    out["pi0_S0"] = math.exp(lq0[i0])
    out["pi_S0"] = math.exp(lq1[i0])
    out["q2_S0"] = math.exp(lq2[i0])
    c = P.log1pchi2(0.0, 1.0)
    out["log1p_chi2"] = c
    out["chi2"] = math.expm1(c) if c < 700 else float("inf")
    out["ess_frac"] = math.exp(-c)
    out["kl_pi_pi0"] = P.kl(1.0, 0.0)
    out["kl_pi0_pi"] = P.kl(0.0, 1.0)
    out["tv"] = P.tv(0.0, 1.0)
    out["renyi_1.5"] = P.renyi(1.5, 1.0, 0.0)
    out["tv_bound"] = max(1 - out["pi0_S0"], 1 - out["pi_S0"])
    # sandwich of WS2: pi0(S0) q2(S0)/pi(S0)^2 <= ESS_frac <= pi0(S0)/pi(S0)^2  (equality on the left by WS1(a))
    out["ess_upper"] = out["pi0_S0"] / out["pi_S0"] ** 2
    out["var_d_pi0"] = P.var_d(0.0)
    out["var_d_pi"] = P.var_d(1.0)
    if ref is not None:
        out["pi0_ref"] = math.exp(lq0[P.space.idx(ref)])
        out["pi_ref"] = math.exp(lq1[P.space.idx(ref)])
    if grid:
        out["T_grid"] = greedy_grid(P)
    if theta is not None:
        lk = leakage(P.blocks, P.R, theta, S0, P.n)
        tt = [abs(x) for b in lk for x in b["theta_tilde"]]
        out["min_abs_theta_tilde"] = min(tt) if tt else float("nan")
        out["max_Lambda"] = max(b["Lambda"] for b in lk)          # per (n-1)
        out["max_kappa"] = max(b["kappa"] for b in lk)            # per (n-1)
        out["max_abs_alpha"] = max([abs(x) for b in lk for x in b["alpha"]] or [0.0])
    if eps_models:
        out["eps_S0"] = cross_eps(P.R, P.blocks, S0)
    blk_of = {j: b for b, C in enumerate(P.blocks) for j in C}
    out["truth_blocks"] = sorted({blk_of[j] for j in S0})
    out["blocks"] = P.blocks
    return out
