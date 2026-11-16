"""W3-PSHARP-R numerics N1: E delta_n on the exact orthogonal design X'X = (n-1)I_p with p FIXED (bounded null block,
the case the parent's expectation clause excludes), against
  Lambda^E_n = (s0+1) [2N/(2p-1-s0)] sqrt( log(p sqrt(n)/(s0+1)) / (pi n) ),  N = p - s0,
and against the parent's normaliser (s0+1) sqrt(log p/(pi n)).
Exact target pi (W3-POST STATEMENT section 0) on an orthogonal design: D_S = n^{|S|}, y'y = n-1,
Q_S = n-1 - sum_{j in S} z_j^2/n, z_j = x_j'y; all 2^p models enumerated (K = p since p <= n/2).
Truth: S0 = {0,...,s0-1}, theta*_j = 1 on S0, sigma* = 1. Scores: u_j' C y^r = sqrt(n-1) theta_j + g_j, g_j iid N(0,1);
residual chi^2_{n-1-p}. E over the null scores by importance sampling (proposal N(0, V) per null coordinate),
over signal scores and residual by plain Monte Carlo. Run: python3 ae_fixed_p.py [M]  (numpy is in the user site, so no -I)
"""
import math, itertools, sys
import numpy as np

B0 = 0.01


def lchoose(a, k):
    return math.lgamma(a + 1) - math.lgamma(k + 1) - math.lgamma(a - k + 1)


def run(n, p, s0, M, rng, V=4.0, chunk=200000):
    nu = 0.01 + n / 2
    subsets = [S for k in range(p + 1) for S in itertools.combinations(range(p), k)]
    S0 = tuple(range(s0))
    ind = np.zeros((len(subsets), p))
    for i, S in enumerate(subsets):
        ind[i, list(S)] = 1.0
    k = ind.sum(1)
    logw = np.array([-math.log(2) - lchoose(2 * p - 1, kk) for kk in k])
    prior_occam = logw - 0.5 * k * math.log(n)
    i0 = subsets.index(S0)
    vals = []
    done = 0
    while done < M:
        m = min(chunk, M - done)
        done += m
        g = rng.standard_normal((m, p))
        g[:, s0:] *= math.sqrt(V)                       # proposal for null scores
        logwt = np.sum(-0.5 * g[:, s0:] ** 2 * (1 - 1 / V) + 0.5 * math.log(V), axis=1)
        a = g.copy()
        a[:, :s0] += math.sqrt(n - 1) * 1.0              # u_j' C y^r
        R = rng.chisquare(n - 1 - p, size=m)
        ss = (a ** 2).sum(1) + R                         # ||C y^r||^2 = (n-1) s_y^2
        q = (n - 1) * a ** 2 / ss[:, None] * (n - 1) / n  # z_j^2/n with z_j = sqrt(n-1) a_j / s_y
        Qmat = (n - 1) - q @ ind.T                       # m x models
        ls = prior_occam[None, :] - nu * np.log(2 * B0 + Qmat)
        d = ls - ls[:, [i0]]
        mx = np.maximum(d.max(1), 0.0)
        tot = np.exp(-mx) + np.sum(np.exp(d - mx[:, None]), axis=1) - np.exp(-mx)  # sum incl. S0 (exp(0))
        delta = 1 - np.exp(-mx) / tot
        vals.append(delta * np.exp(logwt))
    v = np.concatenate(vals)
    return v.mean(), v.std() / math.sqrt(len(v))


def main():
    rng = np.random.default_rng(20261115)
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    print("n, p, s0, E delta (MC se), Lambda^E, ratio E delta/Lambda^E, parent normaliser, ratio, E delta / r_n")
    for p, s0 in [(2, 1), (3, 1), (5, 1), (5, 2)]:
        for n in [10**2, 10**3, 10**4, 10**5, 10**6]:
            if p > n // 2:
                continue
            Ed, se = run(n, p, s0, M, rng)
            N = p - s0
            lam = (s0 + 1) * (2 * N / (2 * p - 1 - s0)) * math.sqrt(math.log(p * math.sqrt(n) / (s0 + 1)) / (math.pi * n))
            old = (s0 + 1) * math.sqrt(math.log(p) / (math.pi * n))
            rn = math.sqrt(math.log(n) / n)
            print(f"{n:>8d} {p} {s0}  {Ed:.4e} ({se:.1e})  {lam:.4e}  {Ed/lam:.3f}  {old:.4e}  {Ed/old:.3f}  {Ed/rn:.4f}")


if __name__ == "__main__":
    main()
