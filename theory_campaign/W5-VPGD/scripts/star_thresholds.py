"""Thresholds for the superset-state condition of Theorem W (STAR.md).  Deterministic (grid/bisection).

Families: nulls in groups of size k_n -> infinity, within-group equicorrelation r, groups mutually orthogonal and
orthogonal to the truths (C-LD is the single-group case).  For such a family and any fixed B', the LD-flat level at
|F| = k is rho_k(r) = r sqrt(k/(1+(k-1)r)) (neighbour lists cannot absorb a growing group).

Printed, for A = 1 (p ~ n; exact constructions need p <= n) and several d:
  r_orig  : largest r with (*)   : tau_d^2 < 1 + 1/(2A),  tau_k = (1 + rho_k sqrt(k)) / sqrt(1 - rho_k^2)
  r_ref_a : largest r with (*'a) : (tau_{d-1}^2 - 1) A < 1/2
  r_ref_b : largest r with (*'b) : (tau_{d-1}^2 + tau_d^2 - 2) A < 1
  r_ref   : min(r_ref_a, r_ref_b)
  r_CLD   : C-LD failure threshold (single group, d = 2): r > 1/(2A)
  r_grp   : grouped-family failure threshold from the explicit configuration of STAR.md Prop G
            (best group by factor, extreme pair within it): sup t^2/(2 log p) = (1+3r)/(1+r) for d = 2.
  r_grp_k : same family, chain of d-1 = k mates (sup t^2 from the explicit configuration, optimised over beta).
Also the LD-rate relaxation (constraints of STAR.md §4, heuristic) for d = 2.
"""
import numpy as np


def rho_k(r, k):
    return 0.0 if k == 0 else r * np.sqrt(k / (1 + (k - 1) * r))


def tau2(r, k):
    rk = rho_k(r, k)
    return (1 + rk * np.sqrt(k)) ** 2 / (1 - rk ** 2)


def largest(f, lo=0.0, hi=0.999999):
    """largest r in [lo, hi] with f(r) True, assuming monotone (True then False)."""
    if not f(lo):
        return 0.0
    if f(hi):
        return hi
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) else (lo, mid)
    return lo


def t2_chain(r, k, beta):
    """explicit configuration: group with the largest factor (level sqrt(1-beta)), l = top member, the k mates
    B = the k bottom members (levels -sqrt(beta)); t = Z_{S0 u B, l} / sqrt(2 log p) in the limit."""
    gam = r / (1 + (k - 1) * r)               # regression coefficient of x_l on each mate
    v = 1 - k * gam * r                       # residual variance
    cF = np.sqrt(r) * (1 - k * gam) / np.sqrt(v)
    cH = np.sqrt(1 - r) * (1 + k * gam) / np.sqrt(v)
    return (cF * np.sqrt(1 - beta) + cH * np.sqrt(beta)) ** 2


def t2_chain_opt(r, k):
    gam = r / (1 + (k - 1) * r); v = 1 - k * gam * r
    cF = np.sqrt(r) * (1 - k * gam) / np.sqrt(v); cH = np.sqrt(1 - r) * (1 + k * gam) / np.sqrt(v)
    return cF ** 2 + cH ** 2                  # Cauchy-Schwarz over beta


def t2_relaxed(r, grid=201):
    """LD-rate relaxation for d = 2 (pair in one group): maximise cF f + cl hl + cb hb subject to
    f^2 <= 1-beta, hl^2, hb^2 <= 1 - f^2, hl^2 + hb^2 <= 1 + beta - f^2 (heuristic counting constraints)."""
    cF = np.sqrt(r * (1 - r) / (1 + r)); cl = 1 / np.sqrt(1 + r); cb = r / np.sqrt(1 + r)
    best = 0.0
    for beta in np.linspace(0, 1, grid):
        for f in np.linspace(0, np.sqrt(1 - beta), grid):
            cap = 1 - f * f; tot = 1 + beta - f * f
            # maximise cl*hl + cb*hb with hl,hb in [0, sqrt(cap)], hl^2+hb^2 <= tot
            hb_grid = np.linspace(0, np.sqrt(min(cap, tot)), grid)
            hl = np.sqrt(np.clip(np.minimum(cap, tot - hb_grid ** 2), 0, None))
            val = cF * f + (cl * hl + cb * hb_grid).max()
            best = max(best, val)
    return best ** 2


lines = []
A = 1.0
kappa = 1 + 1 / (2 * A)
lines.append(f"A = {A}: superset penalty kappa = 1 + 1/(2A) = {kappa}")
for d in (2, 3, 4):
    r_orig = largest(lambda r: tau2(r, d) < kappa)
    r_a = largest(lambda r: (tau2(r, d - 1) - 1) * A < 0.5)
    r_b = largest(lambda r: (tau2(r, d - 1) + tau2(r, d) - 2) * A < 1)
    r_grp = largest(lambda r: t2_chain_opt(r, d - 1) <= kappa)
    lines.append(f"d={d}: (*) r < {r_orig:.4f} [rho*_d = {rho_k(r_orig, d):.4f}];  (*'a) r < {r_a:.4f};  (*'b) r < {r_b:.4f};  "
                 f"(*') r < {min(r_a, r_b):.4f};  grouped family FAILS for r > {r_grp:.4f}" + ("; C-LD fails for r > 0.5" if d == 2 else ""))
lines.append("")
lines.append("d = 2 detail: sup t^2/(2 log p) achievable in families vs the (*'a) bound tau_1^2 = (1+r)/(1-r)")
for r in (0.05, 0.1, 0.2, 0.25, 1 / 3, 0.4, 0.5, 0.7):
    lines.append(f"  r={r:.3f}: C-LD 1+r = {1 + r:.4f}; grouped (1+3r)/(1+r) = {(1 + 3 * r) / (1 + r):.4f}; "
                 f"LD-rate relaxation = {t2_relaxed(r, 61):.4f}; local/far bound (1+r)/(1-r) = {(1 + r) / (1 - r):.4f}")
lines.append("")
lines.append("first order in r (d = 2): grouped excess 2r/(1+r) ~ 2r; local/far excess 2r/(1-r) ~ 2r -> same slope.")
for d in (2, 3, 4):
    k = d - 1
    eps = 1e-4
    sl_grp = (t2_chain_opt(eps, k) - 1) / eps
    sl_bd = (tau2(eps, k) - 1) / eps
    lines.append(f"  d={d}: slope at r=0 of achievable excess {sl_grp:.4f}  vs  local/far bound {sl_bd:.4f}")
lines.append("")
lines.append("large-A asymptotics of the thresholds (d = 2): (*'a) r < 1/(4A+1); grouped fails for r > 1/(4A-1); ratio -> 1")
for A_ in (1, 2, 4, 8):
    k_ = 1 + 1 / (2 * A_)
    r_a = largest(lambda r: (tau2(r, 1) - 1) * A_ < 0.5)
    r_b = largest(lambda r: (tau2(r, 1) + tau2(r, 2) - 2) * A_ < 1)
    r_o = largest(lambda r: tau2(r, 2) < k_)
    r_g = largest(lambda r: t2_chain_opt(r, 1) <= k_)
    lines.append(f"  A={A_}: (*) {r_o:.4f}  (*'a) {r_a:.4f}  (*'b) {r_b:.4f}  grouped-fail {r_g:.4f}  C-LD-fail {1 / (2 * A_):.4f}"
                 f"   ratio grouped/(*'a) = {r_g / r_a:.3f}, C-LD/(*) = {1 / (2 * A_) / r_o:.2f}")
txt = '\n'.join(lines)
print(txt)
open('../results/star_thresholds.txt', 'w').write(txt + '\n')
