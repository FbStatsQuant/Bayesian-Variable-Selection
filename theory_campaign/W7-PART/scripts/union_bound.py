"""Theorem B numbers (PROOF.md §3): the margin union bound
     P(blocks != groups) <= sum_within P_rho(|r_hat| <= t_h) + sum_cross P_{Sigma_jk}(|r_hat| >= min(t_h, t_h'))
with EXACT pair laws (Hotelling density, pairlaw.py), thresholds optimised; and the closed-form bound of
Corollary B:  P <= (2/(sqrt(pi)(1-rho))) p^2 sqrt(n) exp(-(n-4) I*),  I* = I*(rho, psi_bar), plus the n0 at which
it falls below p^{-C}.  No randomness.  Output: results/union_bound.txt"""
import math, sys
import mpmath as mp
from pairlaw import *

mp.mp.dps = 30


def within_fail(t, rho, n):  # P(|r_hat| <= t), r = rho
    return float(lower(t, rho, n) - lower(-t, rho, n))


def cross_fail(t, r, n):  # P(|r_hat| >= t)
    return float(two_sided_upper(t, r, n))


def golden(f, a, b, it=40):
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(it):
        if fc < fd:
            b, d, fd = d, c, fc; c = b - gr * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd; d = a + gr * (b - a); fd = f(d)
    return (c, fc) if fc < fd else (d, fd)


def pair_types(design, n, p, g, rho, psi, nlink):
    """Returns (within list [(count, rho, cls)], cross list [(count, r, cls_pair)]), cls 'L' linked / '0' other."""
    G = p // g
    Nw = G * g * (g - 1) // 2
    if design == "indep":
        return [(Nw, rho, "0")], [(p * (p - 1) // 2 - Nw, 0.0, "00")]
    if design == "global":
        return [(Nw, rho, "0")], [(p * (p - 1) // 2 - Nw, psi, "00")]
    if design == "lh":
        gl = 2 * nlink  # linked groups
        wL = gl * g * (g - 1) // 2
        w0 = (G - gl) * g * (g - 1) // 2
        within = [(wL, rho, "L"), (w0, rho, "0")]
        cross = [(nlink, psi, "LL"), (nlink * 2 * (g - 1), rho * psi, "LL"), (nlink * (g - 1) ** 2, rho ** 2 * psi, "LL")]
        pL = gl * g
        n_LL_other = pL * (pL - 1) // 2 - wL - nlink * g * g  # cross pairs among linked groups, not in the same pair
        cross.append((n_LL_other, 0.0, "LL"))
        cross.append((pL * (p - pL), 0.0, "L0"))
        n00 = (p - pL) * (p - pL - 1) // 2 - w0
        cross.append((n00, 0.0, "00"))
        return within, cross
    raise ValueError


def bound(design, n, p, g, rho, psi, nlink=1):
    within, cross = pair_types(design, n, p, g, rho, psi, nlink)
    lo = max(r for (_, r, _) in cross) + 1e-6
    hi = rho - 1e-6

    def total(tL, t0):
        s = 0.0
        for (c, r, cl) in within:
            if c:
                s += c * within_fail(tL if cl == "L" else t0, r, n)
        for (c, r, cl) in cross:
            if not c:
                continue
            t = tL if cl == "LL" else (min(tL, t0) if cl == "L0" else t0)
            if t <= abs(r):
                return float("inf")
            s += c * cross_fail(t, r, n)
        return s

    if design != "lh":
        t, v = golden(lambda t: math.log(total(t, t) + 1e-300), lo, hi)
        return dict(t=t, bound=math.exp(v))
    # two thresholds: coordinate descent
    t0 = golden(lambda t: math.log(total(t, t) + 1e-300), lo, hi)[0]; tL = t0
    lo0 = 1e-6 + max(r for (_, r, cl) in cross if cl != "LL")
    for _ in range(3):
        tL = golden(lambda t: math.log(total(t, t0) + 1e-300), lo, hi, 30)[0]
        t0 = golden(lambda t: math.log(total(tL, t) + 1e-300), lo0, hi, 30)[0]
    return dict(tL=tL, t0=t0, bound=total(tL, t0))


def closed_form(n, p, rho, psibar):
    I = I_star(rho, psibar)
    return 2 / (math.sqrt(math.pi) * (1 - rho)) * p ** 2 * math.sqrt(n) * math.exp(-(n - 4) * I), I


def n0(A, C, rho, psibar):
    """smallest n with (2/(sqrt(pi)(1-rho))) n^{2A + 1/2} e^{-(n-4) I*} <= n^{-C A} (i.e. <= p^{-C} at p = n^A)."""
    I = I_star(rho, psibar)
    n = 5
    while (math.log(2 / (math.sqrt(math.pi) * (1 - rho))) + (2 * A + 0.5 + C * A) * math.log(n) - (n - 4) * I) > 0:
        n += 1
    return n


if __name__ == "__main__":
    out = []
    out.append("Theorem B, exact-pair-law margin union bound (rigorous; optimised thresholds) and closed form (Cor. B)")
    out.append("design  n     p     g   rho   psi   | thresholds            | exact-law bound | closed-form bound | I*")
    cfgs = []
    for (n, p) in [(200, 500), (200, 1000)]:
        for g in (8, 10, 14):
            cfgs.append(("indep", n, p, g, 0.7, 0.0, 0))
        cfgs += [("indep", n, p, 10, 0.85, 0.0, 0), ("indep", n, p, 10, 0.5, 0.0, 0),
                 ("lh", n, p, 10, 0.7, 0.5, 1), ("lh", n, p, 10, 0.7, 0.5, 2), ("global", n, p, 10, 0.7, 0.3, 0)]
    for (n, p) in [(400, 1790), (800, 4260), (1600, 10120)]:
        cfgs += [("indep", n, p, 10, 0.7, 0.0, 0), ("lh", n, p, 10, 0.7, 0.5, 1), ("global", n, p, 10, 0.7, 0.3, 0)]
    for (d, n, p, g, rho, psi, nl) in cfgs:
        b = bound(d, n, p, g, rho, psi, nl)
        psibar = psi if d != "indep" else 0.0
        cf, I = closed_form(n, p, rho, psibar)
        th = (f"t={b['t']:.4f}" if "t" in b else f"tL={b['tL']:.4f} t0={b['t0']:.4f}")
        lab = d + (f"(c={nl})" if d == "lh" else "")
        out.append(f"{lab:9s} {n:5d} {p:6d} {g:3d} {rho:5.2f} {psi:5.2f} | {th:21s} | {b['bound']:.3e}       | {cf:.3e}         | {I:.5f}")
        print(out[-1], flush=True)
    out.append("")
    out.append("Corollary B: n0(A, C) = smallest n with closed-form bound <= p^{-C} at p = n^A")
    for (rho, psi) in [(0.7, 0.0), (0.85, 0.0), (0.5, 0.0), (0.7, 0.3), (0.7, 0.5)]:
        row = [f"rho={rho} psibar={psi} I*={I_star(rho, psi):.5f} t*={t_star(rho, psi):.4f}:"]
        for A in (1.25, 2.0):
            for C in (1, 2):
                row.append(f"n0(A={A},C={C})={n0(A, C, rho, psi)}")
        out.append(" ".join(row))
    open("../results/union_bound.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(out[-6:]))
