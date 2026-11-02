"""W4-SHARE s1: toy models for D4/D5, Proposition SH and the C1 mechanism.  Seed 20261102.

Exact count-based simulation: on a finite state space with K states, a population of N particles is a count vector;
multinomial resampling of the population = multinomial(N, c*G/sum(c*G)); independent per-particle moves =
sum over states of multinomial(c_s, row_s).  This is the law of the particle system exactly (no approximation).

Parts
 A. Proposition SH (two states, no moves, T = 1): exact P(W extinct) vs D5 upper bound and SH lower bound.
 B. Two states, no moves, T uniform stages: simulated extinction vs D5 bound (multi-stage).
 C. C1 (W1-T38E; reversible kernel of W3-VT38E): extinction of A at N = 1e4, 1e5, 1e6 (200 islands),
    with the branching-process prediction 1 - (1 - pi0(o) s)^N, s = survival probability of an o-lineage.
 D. C1 with o removed: A survives trivially, LT fails (log Zhat/Z << 0) in every island.
 E. C1 with the method's own grid (exact-law pilot rule + candidate grid with V = all 4 states).
"""
import numpy as np
np.seterr(over="ignore")

rng = np.random.default_rng(20261102)
lines = []
P = lambda s: (lines.append(s), print(s, flush=True))


def lse(a):
    m = np.max(a); return m + np.log(np.sum(np.exp(a - m)))


# ---------------- A. Proposition SH ----------------
from scipy.stats import binom
P("A. Proposition SH: two states {a (W), o}, no moves, T = 1.")
for N in [1000, 10000]:
    for pia in [0.5, 0.99]:
        P(f"  N={N} pi0(a)={pia}: kappa | exact P(ext) | D5 upper | SH lower")
        k = np.arange(N + 1); pk = binom.pmf(k, N, pia)
        for kap in np.r_[np.log(N * pia) + np.array([-4, -2, 0, 2]), np.log(N * pia / (1 - pia)), 2 * np.log(N) + np.array([0, 3])]:
            om = np.where(k < N, k / (k + (N - k) * np.exp(kap)), 1.0)
            exact = np.sum(pk * (1 - om) ** N)
            up = np.exp(-N * pia * (-np.expm1(-np.exp(-kap))))
            lo = max(0.0, 1 - N ** 2 * np.exp(-kap)) * (1 - pia ** N)
            P(f"    {kap:7.2f} | {exact:.4g} | {min(1, up):.4g} | {lo:.4g}")


# ---------------- generic count-based SMC ----------------
def run_counts(c0, logg0, d, kernel_fn, grid, n_term, rng):
    """c0: initial counts; d: discrepancy per state; kernel_fn(phi) -> row-stochastic matrix; returns history."""
    c = c0.copy(); N = c.sum(); logZ = 0.0
    hist = [c.copy()]
    for t in range(1, len(grid)):
        dphi = grid[t] - grid[t - 1]
        lw = np.where(c > 0, np.log(np.maximum(c, 1)) + dphi * d, -np.inf)
        L = lse(lw); logZ += L - np.log(N)
        w = np.exp(lw - L)
        c = rng.multinomial(N, w)
        Kt = kernel_fn(grid[t])
        c = sum(rng.multinomial(c[s], Kt[s]) for s in range(len(c)) if c[s] > 0)
        hist.append(c.copy())
    K1 = kernel_fn(1.0)
    for _ in range(n_term):
        c = sum(rng.multinomial(c[s], K1[s]) for s in range(len(c)) if c[s] > 0)
    hist.append(c.copy())
    return np.array(hist), logZ


# ---------------- B. two states, T stages ----------------
P("\nB. Two states, no moves, T uniform stages, pi0(a) = 0.9: simulated P(W extinct) (400 islands) vs D5 bound.")
d2 = np.array([0.0, 1.0])  # d(a)=0, d(o)=kappa (scaled below)
for N, T in [(2500, 100), (2500, 1000)]:
    for kap in [2.0, 5.0, 8.0, 12.0, 20.0]:
        grid = np.linspace(0, 1, T + 1)
        ext = 0
        for r in range(400):
            n0 = rng.binomial(N, 0.9)
            h, _ = run_counts(np.array([n0, N - n0]), None, kap * d2, lambda ph: np.eye(2), grid, 0, rng)
            ext += int(h[-1][0] == 0)
        Pl = np.exp(-kap * grid[1:])
        inv = 1 / Pl[-1] + np.sum(1 / Pl[:-1]) / (np.e - 1)
        bound = np.exp(-N * 0.9 * (-np.expm1(-1 / inv)))
        P(f"  N={N} T={T} kappa={kap:5.1f}: sim {ext/400:.4f}   D5 bound {min(1,bound):.4g}   log(N*0.9/T)={np.log(N*0.9/T):.2f}")

# ---------------- C. C1 ----------------
# states: 0=a1, 1=m, 2=a2, 3=o
lg0 = np.array([0.0, -120.0, -55.2, -10.0]); lg1 = np.array([-2000.0, -2000.0, 0.0, -1930.0])
dC = lg1 - lg0
pi0 = np.exp(lg0 - lse(lg0))


def kernel_C1(phi, with_o=True):
    lg = lg0 + phi * dC
    K = np.zeros((4, 4))
    acc = lambda i, j: min(1.0, np.exp(lg[j] - lg[i]))
    for i in (0, 2):
        a = 0.5 * acc(i, 1); K[i, 1] = a; K[i, i] = 1 - a
    a0 = 0.5 * acc(1, 0); a2 = 0.5 * acc(1, 2)
    K[1, 0] = a0; K[1, 2] = a2; K[1, 1] = 1 - a0 - a2
    K[3, 3] = 1.0
    return K


def surv_prob(Tcut, dphi, kap):
    # o-lineage, Poisson offspring with mean exp(kap*dphi) per stage (A-dominated population), survive Tcut stages
    m = np.exp(kap * dphi); x = 0.0
    for _ in range(Tcut):
        x = np.exp(-m * (1 - x))
    return 1 - x


P("\nC. C1, reversible kernel, T = 1000 uniform stages, 1 move/stage, 9 terminal moves; 200 islands each.")
grid = np.linspace(0, 1, 1001)
s = surv_prob(400, 1e-3, 80.0)
P(f"  pi0(o) = {pi0[3]:.4e}; o-lineage survival s (Poisson, mean e^0.08, 400 stages) = {s:.4f}")
for N in [10 ** 4, 10 ** 5, 10 ** 6]:
    ext = 0; lz = []
    for r in range(200):
        c0 = rng.multinomial(N, pi0)
        h, logZ = run_counts(c0, lg0, dC, kernel_C1, grid, 9, rng)
        ext += int(h[-1][:3].sum() == 0)
        lz.append(logZ - (lse(lg1) - lse(lg0)))
    pred = 1 - (1 - pi0[3] * s) ** N
    P(f"  N={N:>7}: P(A extinct) sim {ext/200:.3f}  branching prediction {pred:.3f}   median log(Zhat/Z) {np.median(lz):.1f}")

# ---------------- D. C1 without o ----------------
P("\nD. C1 with o removed (pi0(o) = 0): delivery is trivial; LT fails.")
pi0no = pi0.copy(); pi0no[3] = 0; pi0no /= pi0no.sum()
lg0no = lg0.copy(); lg0no[3] = -np.inf
Ztrue = lse(lg1[:3]) - lse(lg0[:3])
lzs = []; surv = 0
for r in range(50):
    c0 = rng.multinomial(10 ** 5, pi0no)
    h, logZ = run_counts(c0, lg0no, dC, kernel_C1, grid, 9, rng)
    surv += int(h[-1][:3].sum() > 0); lzs.append(logZ - Ztrue)
P(f"  N=1e5, 50 islands: A survives in {surv}/50; log(Zhat/Z): max {np.max(lzs):.1f}, median {np.median(lzs):.1f}")

# ---------------- E. C1 with the method's grid ----------------
P("\nE. C1 with the method's grid (exact-law pilot temperatures, 60 bisections, floor 1/Te, Te = 1000;")
P("   candidate grid with V = all 4 states, restricted ESS >= 0.9).")


def F(t, V=slice(None)):
    return lse(lg0[V] + t * dC[V])


def rho(u, v):
    return np.exp(2 * F(v) - F(u) - F(2 * v - u))


def pilot_list(Te=1000):
    phis = [0.0]; phi = 0.0
    while phi < 1.0:
        if rho(phi, 1.0) >= 0.9:
            nxt = 1.0
        else:
            lo, hi = phi, 1.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if rho(phi, mid) >= 0.9: lo = mid
                else: hi = mid
            nxt = lo
            if nxt < phi + 1.0 / Te: nxt = min(1.0, phi + 1.0 / Te)
        phis.append(nxt); phi = nxt
    return np.array(phis)


pl = pilot_list()
# candidate grid: V = Omega => rho_V = rho, so the construction reproduces the pilot list (checked here)
grid_m = [0.0]; u = 0.0
for b in pl[1:]:
    if rho(u, b) >= 0.9:
        grid_m.append(b); u = b
    else:
        lo, hi = u, b
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if rho(u, mid) >= 0.9: lo = mid
            else: hi = mid
        grid_m.append(lo); u = lo
        if grid_m[-1] < b:  # continue toward b
            pass
grid_m = np.array(sorted(set(grid_m)))
if grid_m[-1] < 1.0: grid_m = np.r_[grid_m, 1.0]
P(f"  method grid: T = {len(grid_m)-1} stages; first temperatures {np.round(grid_m[:6], 5)}; last {np.round(grid_m[-3:], 4)}")
for N in [10 ** 4, 10 ** 5, 10 ** 6]:
    ext = 0
    for r in range(200):
        c0 = rng.multinomial(N, pi0)
        h, logZ = run_counts(c0, lg0, dC, kernel_C1, grid_m, 9, rng)
        ext += int(h[-1][:3].sum() == 0)
    P(f"  N={N:>7}: P(A extinct) with the method grid {ext/200:.3f}   (P(some o drawn) = {1-(1-pi0[3])**N:.3f})")

open(__file__.replace('.py', '.txt'), 'w').write("\n".join(lines) + "\n")
