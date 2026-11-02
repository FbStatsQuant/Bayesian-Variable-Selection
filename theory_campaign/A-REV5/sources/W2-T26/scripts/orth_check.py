"""Joint non-vacuity of Theorem B's hypotheses on the ORTH family (00_COMMON: G = (n-1) I_p), p = n/2.

Under ORTH every score is closed form: for |T| = k, D_T = n^k (H_T = n^2 I, G_T + I = n I) and
Q_T = y'y - ||z_T||^2 / n, with z = X'y. Standardised RSS: rho_T = y'y - ||z_T||^2/(n-1), x_{T,l} = z_l^2/((n-1) rho_T).
This script, for each n:
  (1) computes the EXP' remainder R = log r_b(T+l)/r_b(T) + (1/2)log(n+1) + nu*log(1 - x_{T,l}) for EVERY within-block
      addition (b, T, l) and reports max |R| (claim, PROOF SKETCH in REPORT: max|R| = O(1));
  (2) computes 1 - pi0(S0) exactly by convolution of block size profiles (METHODOLOGY 6.3) and (T^max+1)(1 - pi0(S0)),
      i.e. the EXP-dependent half of premise (P1).
Blocks: contiguous index blocks of size B (with exact orthogonality all 1-|r| distances tie; lexicographic tie-breaking
gives index-ordered merges, so contiguous blocks are the natural reading; this is a documented simplification).
Seed: default_rng(20261102 + n + seed).
"""
import sys
import numpy as np
from math import lgamma, log, floor, sqrt, ceil
from scipy.special import logsumexp

THETA = 0.6


def run(n, seed):
    rng = np.random.default_rng(20261102 + n + seed)
    p = n // 2
    s0 = 3
    S0 = [0, p // 3, 2 * p // 3]
    G0 = rng.standard_normal((n, p))
    G0 -= G0.mean(0)
    Q, _ = np.linalg.qr(G0)
    X = np.sqrt(n - 1) * Q  # centred, ||x_j||^2 = n-1, X'X = (n-1)I
    theta = np.zeros(p); theta[S0] = THETA
    yr = X @ theta + rng.standard_normal(n)
    y = (yr - yr.mean()) / (yr - yr.mean()).std(ddof=1)
    z = X.T @ y
    yy = float(y @ y)
    nu = 0.01 + n / 2
    K = min(p, n // 2)
    B = min(floor(sqrt(n)), floor(sqrt(p)), 16)
    ell = ceil(log(n + p + 1, 2)); Tmax = 4 * max(1000, ell ** 2)
    blocks = [list(range(i, min(i + B, p))) for i in range(0, p, B)]
    maxR = 0.0
    prof = np.array([0.0])  # log of convolved size profile
    logr_S0 = 0.0
    for blk in blocks:
        b = len(blk)
        masks = np.arange(1 << b)
        bits = ((masks[:, None] >> np.arange(b)) & 1).astype(float)
        k = bits.sum(1)
        sz = bits @ (z[blk] ** 2)
        logr = -0.5 * k * np.log(n) - nu * (np.log(0.02 + yy - sz / n) - np.log(0.02 + yy))
        rho = yy - sz / (n - 1)
        for i in range(b):
            T = masks[(masks >> i) & 1 == 0]
            Tl = T | (1 << i)
            x = (z[blk[i]] ** 2 / (n - 1)) / rho[T]
            R = logr[Tl] - logr[T] + 0.5 * np.log(n + 1) + nu * np.log1p(-x)
            maxR = max(maxR, float(np.abs(R).max()))
        # block size profile log e_b(j)
        eb = np.array([logsumexp(logr[k == j]) for j in range(b + 1)])
        new = np.full(len(prof) + b, -np.inf)
        for j in range(b + 1):
            new[j:j + len(prof)] = np.logaddexp(new[j:j + len(prof)], prof + eb[j])
        prof = new
        U = sum(1 << blk.index(j) for j in S0 if j in blk)
        logr_S0 += logr[U]
    logw = np.array([log(0.5) - (lgamma(2 * p) - lgamma(kk + 1) - lgamma(2 * p - kk)) for kk in range(K + 1)])
    logZ0 = logsumexp(prof[:K + 1] + logw)
    lpi0 = logw[s0] + logr_S0 - logZ0
    om = -np.expm1(lpi0)
    return dict(n=n, p=p, B=B, Tmax=Tmax, maxR=maxR, one_minus_pi0=om, P1start=(Tmax + 1) * om)


if __name__ == '__main__':
    ns = [int(v) for v in sys.argv[1].split(',')] if len(sys.argv) > 1 else [200, 400, 800, 1600]
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print('n,p,B,Tmax,seed,maxR,one_minus_pi0,P1start')
    for n in ns:
        for s in range(seeds):
            r = run(n, s)
            print(f"{r['n']},{r['p']},{r['B']},{r['Tmax']},{s},{r['maxR']:.4f},{r['one_minus_pi0']:.3e},{r['P1start']:.3e}",
                  flush=True)
