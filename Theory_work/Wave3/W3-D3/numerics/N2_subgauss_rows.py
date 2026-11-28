"""W3-D3 numerics N2 (sanity, not evidence for a claim): exact coded posterior (full enumeration, p = 10) on random
designs with NON-Gaussian rows x = L xi, L = chol(Sigma), Sigma_jk = 0.5^|j-k| (AR(1) correlation), xi i.i.d. Gaussian /
Rademacher / uniform[-sqrt3, sqrt3] (all satisfy (A4) with L = 1, Proposition ExSG). Truth: s0 = 2, beta = (1, -1, 0, ...),
sigma = 1, intercept 0. Reports mean delta_n * sqrt(n / log n) and the frequency of HPM = MPM = S0 over R replicates.
The Post class is copied verbatim from Theory_work/Wave3/W3-POST/numerics/post_exact.py (exact target as coded).
Run: /home/fb31/SMC_Theory_Department/ci/venv-numerics/bin/python -I N2_subgauss_rows.py > N2_out.txt"""
import sys, itertools, math
import numpy as np

B0, A0 = 0.01, 0.01


def lchoose(a, k):
    return math.lgamma(a + 1) - math.lgamma(k + 1) - math.lgamma(a - k + 1)


def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0)
    X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    y = yr - yr.mean()
    y = y / np.sqrt((y ** 2).sum() / (n - 1))
    return X, y


class Post:
    """Exact posterior over Omega = {|S| <= K}. Stores log pi and the subsets as bit masks."""

    def __init__(self, X, y):
        n, p = X.shape
        self.n, self.p, self.K = n, p, min(p, n // 2)
        G = X.T @ X
        z = X.T @ y
        yty = float(y @ y)
        nu = A0 + n / 2.0
        logw = np.array([-math.log(2) - lchoose(2 * p - 1, k) for k in range(self.K + 1)])
        masks, logF, sizes = [], [], []
        for k in range(self.K + 1):
            subs = list(itertools.combinations(range(p), k))
            if k == 0:
                masks.append(np.array([0], dtype=np.int64)); sizes.append(np.array([0]))
                logF.append(np.array([logw[0] - nu * math.log(2 * B0 + yty)]))
                continue
            idx = np.array(subs)
            Gs = G[idx[:, :, None], idx[:, None, :]]
            zs = z[idx]
            I = np.eye(k)
            H = (n + 1) * Gs + I
            Am = Gs + I
            _, ldH = np.linalg.slogdet(H)
            _, ldA = np.linalg.slogdet(Am)
            sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
            Q = yty - n * np.einsum('ij,ij->i', zs, sol)
            Q = np.maximum(Q, 0.0)
            lf = logw[k] - 0.5 * (ldH - ldA) - nu * np.log(2 * B0 + Q)
            logF.append(lf)
            masks.append((np.left_shift(1, idx)).sum(1).astype(np.int64))
            sizes.append(np.full(len(subs), k))
        self.logF = np.concatenate(logF)
        self.mask = np.concatenate(masks)
        self.size = np.concatenate(sizes)
        m = self.logF.max()
        w = np.exp(self.logF - m)
        self.pi = w / w.sum()

    def mass(self, S):
        mk = sum(1 << j for j in S)
        return float(self.pi[self.mask == mk].sum())

    def pip(self):
        return np.array([self.pi[(self.mask >> j) & 1 == 1].sum() for j in range(self.p)])

    def hpm_mask(self):
        return int(self.mask[np.argmax(self.logF)])

    def mpm_mask(self):
        pip = self.pip()
        return int(sum(1 << j for j in range(self.p) if pip[j] > 0.5))


def run():
    rng = np.random.default_rng(20261117)
    p, R = 10, 100
    Sig = np.array([[0.5 ** abs(j - k) for k in range(p)] for j in range(p)])
    L = np.linalg.cholesky(Sig)
    beta = np.zeros(p); beta[0], beta[1] = 1.0, -1.0
    S0 = 0b11
    laws = {
        "gaussian": lambda size: rng.standard_normal(size),
        "rademacher": lambda size: rng.choice([-1.0, 1.0], size=size),
        "uniform": lambda size: rng.uniform(-math.sqrt(3), math.sqrt(3), size=size),
    }
    print("law         n     mean(delta*sqrt(n/log n))   freq(HPM=MPM=S0)")
    for name, draw in laws.items():
        for n in [50, 100, 200, 400, 800]:
            dl, ok = [], 0
            for _ in range(R):
                Xr = draw((n, p)) @ L.T
                yr = Xr @ beta + rng.standard_normal(n)
                X, y = standardise(Xr, yr)
                P = Post(X, y)
                d = 1.0 - P.mass([0, 1])
                dl.append(d * math.sqrt(n / math.log(n)))
                ok += int(P.hpm_mask() == S0 and P.mpm_mask() == S0)
            print(f"{name:10s} {n:5d}   {np.mean(dl):10.4f}                  {ok / R:.2f}")


if __name__ == "__main__":
    run()
