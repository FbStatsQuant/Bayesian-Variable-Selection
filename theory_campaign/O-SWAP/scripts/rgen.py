"""Python port of Scripts/Data_generators/gen_prod_data.R (+ gen_dev_data.R helpers).
Reproduces R's RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed); rnorm()
bit-for-bit up to the final qnorm (scipy ndtri vs R qnorm5, both ~1e-16), so X and eps are the
study's own (up to floating-point rounding in chol / matmul, ~1e-14)."""
import numpy as np
from scipy.special import ndtri

N = 200
DATA_BASE = {500: 1410000, 1000: 1510000}
BIG = 134217728.0  # 2^27
I2_32M1 = 2.328306437080797e-10


class RMT:
    def __init__(self, seed):
        s = np.uint32(seed & 0xFFFFFFFF)
        with np.errstate(over='ignore'):
            for _ in range(50):
                s = np.uint32(np.uint32(69069) * s + np.uint32(1))
            key = np.empty(625, np.uint32)
            for j in range(625):
                s = np.uint32(np.uint32(69069) * s + np.uint32(1))
                key[j] = s
        # key[0] is R's dummy[0] (mti), overwritten to 624 by FixupSeeds; mt = key[1:]
        self.bg = np.random.MT19937()
        self.bg.state = {'bit_generator': 'MT19937', 'state': {'key': key[1:].copy(), 'pos': 624}}

    def unif(self, k):
        u = self.bg.random_raw(k).astype(np.float64) * 2.3283064365386963e-10
        u = np.where(u <= 0.0, 0.5 * I2_32M1, u)
        u = np.where(1.0 - u <= 0.0, 1.0 - 0.5 * I2_32M1, u)
        return u

    def rnorm(self, k):
        u = self.unif(2 * k).reshape(k, 2)
        v = np.floor(BIG * u[:, 0]) + u[:, 1]
        return ndtri(v / BIG)


def scenario_covariance(s, p):
    group = (np.arange(1, p + 1) + 4) // 5          # ceiling(j/5)
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if s == 1: return I
    if s == 2:
        idx = np.arange(p); return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if s == 3: return 0.7 * H + 0.3 * I
    if s == 4: return 0.85 * H + 0.15 * I
    if s == 5: return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if s == 6:
        rho = 0.4 + 0.1 * ((group - 1) % 6)
        S = H * rho[None, :]          # R: H*matrix(rho,p,p) -> column j carries rho[row]? see note
        S = H * np.broadcast_to(rho[:, None], (p, p))
        np.fill_diagonal(S, 1.0); return S
    raise ValueError(s)
# note on S6: matrix(rho,p,p) fills column-major, so entry (i,j) = rho[i]; within a group rho[i]=rho[j]
# because rho depends on the group only, so the orientation is immaterial (H zeroes cross-group entries).


def truth(p):
    s0 = 14; step = {500: 7, 1000: 13}[p]
    pos = np.array([3, 2, 4, 1, 5, 3]); pattern = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
    k = np.arange(s0); block = 1 + step * k
    active = 5 * (block - 1) + pos[k % 6]            # 1-based
    return active - 1, pattern[k % 6]                 # 0-based


def generate(p, s, r, L=None):
    """Returns X (R-scaled, sd n-1), eps, active (0-based), beta_active."""
    rng = RMT(DATA_BASE[p] + 10000 * s + r)
    if L is None: L = np.linalg.cholesky(scenario_covariance(s, p)).T   # upper, Sigma = L'L
    Z = rng.rnorm(N * p).reshape(p, N).T                                # column-major fill
    raw = Z @ L
    X = raw - raw.mean(0)
    X = X / np.sqrt((X ** 2).sum(0) / (N - 1))
    eps = rng.rnorm(N)
    act, b = truth(p)
    return X, eps, act, b


if __name__ == '__main__':
    print('set.seed(1); rnorm(5):', RMT(1).rnorm(5), ' R: -0.6264538 0.1836433 -0.8356286 1.5952808 0.3295078')
    print('set.seed(42); rnorm(3):', RMT(42).rnorm(3), ' R: 1.3709584 -0.5646982 0.3631284')
    X, eps, act, b = generate(500, 1, 1)
    print(X.shape, act + 1, b)
