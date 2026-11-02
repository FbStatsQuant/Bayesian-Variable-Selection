"""Independent reviewer checks for Theorem W (REPORT §3.6): order-statistic / Chernoff / Mills constants of W(e),
an independent large-(n,p) evaluation of the W(e) multi-extra lower bound (counterexample row n=1e16, A=0.95, r=0.9),
and the arithmetic behind the W(d) gap.  Seed 20261102, single core."""
import math
import numpy as np
from scipy import stats
from scipy.special import gammaln

rng = np.random.default_rng(20261102)
out = []

# (A) Mills lower bound P(Z^2>=t) >= (2pi)^{-1/2} t^{-1/2} e^{-t/2} for t >= 1 (claimed for t >= 2)
ts = np.linspace(1, 400, 4000)
lhs = stats.chi2.logsf(ts, 1); rhs = -0.5 * math.log(2 * math.pi) - 0.5 * np.log(ts) - ts / 2
out.append(f"(A) Mills: min_t [log P(Z^2>=t) - log bound] over t in [1,400] = {np.min(lhs - rhs):.4f} (>=0 required)")

# (B) Chernoff P(Bin(m, 2k/m) <= k-1) <= e^{-k/4}, and tau_k/2 >= log(m/(2k)) - 0.5 log(4 pi log m), tau_k <= 2 log m
worst_ch = -1e9; worst_tau = 1e9; worst_up = 1e9
for m in [10**3, 10**5, 10**8, 10**12]:
    for k in [1, 2, 5, 10, 50, 200, int(0.05 * m)]:
        if k < 1 or 2 * k > m: continue
        worst_ch = max(worst_ch, stats.binom.logcdf(k - 1, m, 2 * k / m) + k / 4)
        tau = stats.chi2.isf(2 * k / m, 1)
        worst_tau = min(worst_tau, tau / 2 - (math.log(m / (2 * k)) - 0.5 * math.log(4 * math.pi * math.log(m))))
        worst_up = min(worst_up, 2 * math.log(m) - tau)
out.append(f"(B) Chernoff: max [log P(Bin<=k-1) + k/4] = {worst_ch:.4f} (<=0 required); "
           f"min [tau_k/2 - claimed lower] = {worst_tau:.4f} (>=0); min [2log m - tau_k] = {worst_up:.4f} (>=0)")

# (C) Independent large-(n,p) lower bound: s0=2, r=0.9, s=r, zeta=0, singleton blocks, n=1e16, p=n^0.95.
def lower_bound(n, A, r, s0=2, K=20000):
    p = n ** A; m0 = p - s0; nu = 0.01 + n / 2; s = r
    G = np.cumsum(rng.exponential(size=K))              # top-K uniforms U_(i) = Gamma_i / Gamma_{m0+1}, Gamma_{m0+1} ~ m0
    U = G / m0
    Z2 = stats.chi2.isf(U, 1)                           # decreasing
    x = Z2 * (1 - s) / (2 * nu)                         # nu x_j/(1-s) = Z_j^2/2
    XE = np.cumsum(x)
    k = np.arange(1, K + 1)
    i = np.arange(K)
    logprior = np.cumsum(np.log((s0 + i + 1) / (2 * p - 1 - s0 - i)))
    ratio = logprior - k / 2 * math.log(n) + 2 * nu * (-np.log1p(-XE / (1 - s))) - nu * np.cumsum(-np.log1p(-x))
    kstar = int(np.argmax(ratio)) + 1
    LB = max(0.0, ratio.max()) + math.log1p(math.exp(-abs(ratio.max())))
    FD = max(0.0, r * math.log(p) - 0.5 * math.log(n))
    L = r * math.log(p) - 0.5 * math.log(n) - (1 + r) / 2 * math.log(math.log(p))
    C1 = 1 + math.log(2) + (1 + r) * math.log(4) + (1 + r) / 2 * math.log(4 * math.pi)
    We = math.exp((L - C1 - 1) / r)
    return LB, kstar, FD, L, We, math.exp(L / r)
out.append("(C) log10 n, A, r | LB=log(1+max_k ratio) | k* | FD W(c) | L_n | W(e) bound e^{(L_n-C1-1)/r} | e^{L_n/r}")
for (ln, A, r) in [(16, 0.95, 0.9), (12, 0.95, 0.9), (16, 0.85, 0.9), (16, 0.70, 0.9), (14, 0.40, 0.9)]:
    LB, ks, FD, L, We, eL = lower_bound(10.0 ** ln, A, r)
    out.append(f"    {ln} {A} {r} | {LB:.4g} | {ks} | {FD:.4g} | {L:.3f} | {We:.4g} | {eL:.4g}")

# (D) W(d) gap: sequences with p^r/sqrt(n) -> 0 but p^r sqrt(log p)/sqrt(n) -> infinity (r = 0.9)
out.append("(D) p^r = sqrt(n)/loglog n, r=0.9: log10 n | rho_n(2)=p^r/sqrt n | rho_n(2)*sqrt(log p) (W(b)'s bound / V_n)")
for ln in [10, 20, 40, 80, 160]:
    n = 10.0 ** ln; rho = 1 / math.log(math.log(n)); p = (math.sqrt(n) * rho) ** (1 / 0.9)
    out.append(f"    {ln} | {rho:.4f} | {rho * math.sqrt(math.log(p)):.3f}")

# (E) HT looseness at fixed a = 1+r: E[sum_N e^{a Z^2/2} 1{Z^2 <= 2 log m}] vs the HT bound m^a sqrt(log m)
out.append("(E) a=1.9: m | exact m*E[e^{aZ^2/2}1{Z^2<=2log m}] / m^a | HT bound factor sqrt(4 log m/pi) | 1/sqrt(log m)")
a = 1.9
for m in [1e3, 1e6, 1e12, 1e24]:
    tau = 2 * math.log(m); zs = np.linspace(0, math.sqrt(tau), 200001)
    # E = 2 int_0^{sqrt tau} phi(z) e^{a z^2/2} dz, computed relative to m^{a-1} to avoid overflow
    f = np.exp((a - 1) * zs ** 2 / 2 - (a - 1) * math.log(m)) / math.sqrt(2 * math.pi)
    E_rel = 2 * np.trapz(f, zs)
    out.append(f"    {m:.0e} | {E_rel:.4f} | {math.sqrt(4 * math.log(m) / math.pi):.3f} | {1 / math.sqrt(math.log(m)):.3f}")
print("\n".join(out))
