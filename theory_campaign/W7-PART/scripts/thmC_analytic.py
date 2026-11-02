"""Corollary C (PROOF.md §4.3): fully analytic, rigorous version of Theorem C for independent groups
(within |Sigma_jl| >= rho), by peeling on mu = min(m_h, m_h'):
   E[S_L + S_N] <= K_g [ H0(tau_0) + sum_i H0(tau_{i+1}) min{1, g(g-1) P_rho(|r_hat| < tau_i)} ],
   K_g = (2g-1) g + (g-1)^2,   tau_i = tau_0 - i*step, last tau = 0;
   P(blocks != groups) <= G(G-1) * (that)     [+ linked-pair terms for LH].
For LH with c linked pairs the c dependent pairs are bounded (rigorously) by the local margin restricted to the
pair (exact pair laws, optimised t), and also given as a Monte Carlo Clopper-Pearson 95% bound (0 failures in the
20,000 direct simulations of sharp_bound.py).  Also: the exponent kappa_C(rho) = min_tau [I(tau;0) + I(tau;rho)]
versus Theorem B's I*(rho, 0).  No randomness.  Output: results/thmC_analytic.txt"""
import math
import numpy as np
from scipy.special import betainc
from scipy.optimize import minimize_scalar
from pairlaw import lower, two_sided_upper, rate, I_star, t_star


def H0(s, n):
    if s >= 1:
        return 0.0
    if s <= 0:
        return 1.0
    return float(betainc((n - 2) / 2, 0.5, 1 - s * s))


def Pw_below(t, rho, n, cache):
    k = (round(t, 7), rho, n)
    if k not in cache:
        cache[k] = float(lower(t, rho, n) - lower(-t, rho, n)) if t > 0 else 0.0
    return cache[k]


def EC_bound(n, g, rho, step=0.0025, cache=None):
    cache = {} if cache is None else cache
    K = (2 * g - 1) * g + (g - 1) ** 2
    best = None
    for tau0 in np.arange(0.30, rho, 0.025):
        taus = list(np.arange(tau0, 0, -step)) + [0.0]
        tot = H0(tau0, n)
        for i in range(len(taus) - 1):
            pb = min(1.0, g * (g - 1) * Pw_below(taus[i], rho, n, cache))
            tot += H0(taus[i + 1], n) * pb
            if pb < 1e-200:
                break
        tot *= K
        if best is None or tot < best[0]:
            best = (tot, tau0)
    return best


def linked_pair_margin(n, g, rho, psi):
    """local margin restricted to one LH linked pair: within 2*C(g,2) at rho; cross 1@psi, 2(g-1)@rho psi,
    (g-1)^2 @ rho^2 psi."""
    def f(t):
        v = 2 * (g * (g - 1) // 2) * float(lower(t, rho, n) - lower(-t, rho, n))
        for (c, r) in [(1, psi), (2 * (g - 1), rho * psi), ((g - 1) ** 2, rho * rho * psi)]:
            v += c * float(two_sided_upper(t, r, n))
        return math.log(v)
    res = minimize_scalar(f, bounds=(psi + 1e-4, rho - 1e-4), method="bounded", options=dict(xatol=1e-4))
    return math.exp(res.fun), res.x


def kappa_C(rho):
    res = minimize_scalar(lambda t: rate(0.0, t) + rate(rho, t), bounds=(1e-6, rho - 1e-6), method="bounded")
    return res.fun, res.x


if __name__ == "__main__":
    out = ["Corollary C (analytic, rigorous): P(blocks != groups) for independent equicorrelated groups",
           "n     p     g   rho  | E-bound per ordered pair (tau0) | total = G(G-1) x E-bound",
           ]
    cache = {}
    res = {}
    for (n, p) in [(200, 500), (200, 1000), (400, 1790), (800, 4260)]:
        for g in ((8, 10, 14) if n == 200 else (10,)):
            for rho in ((0.5, 0.6, 0.7, 0.85) if g == 10 else (0.7,)):
                G = p // g
                e, tau0 = EC_bound(n, g, rho, cache=cache)
                res[(n, p, g, rho)] = (e, G)
                out.append(f"{n:4d} {p:6d} {g:3d} {rho:5.2f} | {e:.3e} ({tau0:.3f})                | {G*(G-1)*e:.3e}")
                print(out[-1], flush=True)
    out.append("")
    out.append("LH-iid (g = 10, rho = 0.7, psi = 0.5, c linked pairs; all other group pairs independent):")
    out.append("n     p     c | independent part | linked part, rigorous (local margin, t) | rigorous total | linked part, MC CP95 | total with MC CP95")
    for (n, p) in [(200, 500), (200, 1000)]:
        lm, t = linked_pair_margin(n, 10, 0.7, 0.5)
        e, G = res[(n, p, 10, 0.7)]
        for c in (1, 2):
            ind = (G * (G - 1) - 2 * c) * e
            cp = 1.498e-4  # 0/20000 (sharp_bound.py, linked_pair_mc), Clopper-Pearson 95% upper bound
            out.append(f"{n:4d} {p:6d} {c:2d} | {ind:.3e}        | {c*lm:.3e} (t = {t:.3f})                 | {ind + c*lm:.3e}      | {c*cp:.3e}           | {ind + c*cp:.3e}")
    out.append("")
    out.append("Exponents (per observation): Theorem B I*(rho,0) vs Corollary C kappa_C(rho) = min_tau [I(tau;0) + I(tau;rho)]")
    for rho in (0.4, 0.5, 0.6, 0.7, 0.85):
        k, tk = kappa_C(rho)
        out.append(f"rho={rho:4.2f}: I*={I_star(rho, 0.0):.5f} (t*={t_star(rho, 0.0):.3f})   kappa_C={k:.5f} (tau={tk:.3f})   ratio={k/I_star(rho,0.0):.2f}")
    open("../results/thmC_analytic.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(out[-12:]))
