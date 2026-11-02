"""Population grid rule of v3 (cpp/v3_calib.h build_grid / pilot_next_phi with V = Omega, H -> infinity).

Phi(u, v) = F(u) - 2F(v) + F(2v - u) = log(1 + chi^2(q_v || q_u)) = -log rho(u, v); step accepted iff rho >= 0.90.
Greedy rule: from u, v = 1 if rho(u, 1) >= 0.9, else 60 bisection halvings on (u, 1]; append lo.
"""
import numpy as np
from math import log, ceil
from scipy.special import logsumexp

THR = 0.90
C = -log(THR)          # log(10/9)


def greedy_grid(F, thr=THR, halvings=60, maxT=100000):
    """F: callable t -> log Zbar_t (convex). Returns the grid list or None on non-progress."""
    lt = log(thr)
    ok = lambda u, v: 2 * F(v) - F(u) - F(2 * v - u) >= lt
    g = [0.0]; u = 0.0
    while u < 1.0:
        if ok(u, 1.0):
            v = 1.0
        else:
            lo, hi = u, 1.0
            for _ in range(halvings):
                mid = 0.5 * (lo + hi)
                if ok(u, mid): lo = mid
                else: hi = mid
            v = lo
            if v >= 1.0 - 1e-12: v = 1.0
            if not v > u: return None
        g.append(v); u = v
        if len(g) > maxT: return None
    return g


def F_from(lg0, d):
    m = np.isfinite(lg0)
    a, b = lg0[m], d[m]
    return lambda t: float(logsumexp(a + t * b))


def F_two_state(A0, A1):
    """States S° and S0: log gamma_t(S0)/gamma_t(S°) = -A0 + t*(A0 + A1)."""
    D = A0 + A1
    return lambda t: float(np.logaddexp(0.0, -A0 + t * D))


def N_halving(wbar):
    """Minimal number of intervals of a grid on [0,1] whose every step satisfies 2v - u <= wbar."""
    if wbar >= 2: return 1
    if wbar <= 1: return None
    return max(1, ceil(log(wbar / (wbar - 1), 2) - 1e-12))
