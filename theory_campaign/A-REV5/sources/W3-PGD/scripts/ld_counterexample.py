"""Counterexample C-LD (PROOF.md §5): without LD, TD'_P(R_{0,2}) fails w.p. -> 1 for equicorrelated nulls, r > 1/2.

Exact design in contrast coordinates (N = n-1): orthonormal v0, f, g_1..g_m (m = N-2, p = m+1);
truth x_1 = sqrt(N) v0 (s0 = 1, theta = 1, sigma = 1); nulls x_{1+i} = sqrt(N)(sqrt(r) f + sqrt(1-r) g_i).
The noise is simulated in these coordinates (E0, F0, G_i iid N(0,1), plus an independent chi^2 remainder), so no
N x p matrix is formed and n can be large.  F is the exact 00_COMMON score (g-prior + IG(0.01,0.01) + BB(1,p)),
evaluated from (G_T, z_T, y'y) on the standardised response.
For each replicate we take a = argmax G, b = argmin G, S = S0 u {a,b} and record
  fail2  : F(S) >= max(F(S-a), F(S-b))           (D_S fails: no progress move beats staying; TD'_P(R_{0,2}) fails)
  locmax : additionally S beats every add / swap / delete neighbour (spurious local max: TD'_inf fails too)
and the d = 1 check (Theorem W (H1)):
  ok1    : F(S0) > F(S0+l) for all l, and F(S0) > F(S0+e+l) for all pairs (e,l) (max over pairs computed exactly:
           for fixed e the best partner maximises |Z_l - r Z_e|, i.e. is argmax or argmin of Z).
Seeds: numpy default_rng(20261102 + 1000*k + rep).  Output: results/ld_counterexample.txt
"""
import numpy as np
from math import lgamma, log

A0 = B0 = 0.01


def lchoose(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


class CoordScorer:
    """F(T) for the C-LD design from coordinates. Columns: 0 = truth, 1..m = nulls."""
    def __init__(self, n, r, theta, E0, F0, G, rest):
        self.n, self.N, self.r = n, n - 1, r
        self.m = len(G); self.p = self.m + 1
        N = self.N
        # raw contrast response coordinates: Y = (theta sqrt N + E0) v0 + F0 f + sum G_i g_i + rest
        yv0 = theta * np.sqrt(N) + E0
        YY = yv0 ** 2 + F0 ** 2 + np.sum(G ** 2) + rest
        sy = np.sqrt(YY / N)
        self.yty = N * 1.0                                  # standardised y has ||y||^2 = N
        zt = np.sqrt(N) * yv0 / sy                          # x_1' y
        zn = np.sqrt(N) * (np.sqrt(r) * F0 + np.sqrt(1 - r) * G) / sy   # x_{1+i}' y
        self.z = np.concatenate([[zt], zn])
        self.nu = A0 + n / 2
        self.logCn = A0 * log(2 * B0) + lgamma(A0 + n / 2) - (n / 2) * log(np.pi) - lgamma(A0)
        K = min(self.p, n // 2)
        logw = np.array([-log(2) - lchoose(2.0 * self.p - 1, k) for k in range(K + 1)])
        terms = np.array([lchoose(self.p, k) for k in range(K + 1)]) + logw
        mx = terms.max(); self.logprior = logw - (mx + log(np.exp(terms - mx).sum()))

    def gram(self, T):
        T = np.asarray(T)
        R = np.where(T[:, None] == T[None, :], 1.0, np.where((T[:, None] > 0) & (T[None, :] > 0), self.r, 0.0))
        return self.N * R

    def F_batch(self, Ts):
        """Ts: (B, k) array of column index sets of equal size k >= 1."""
        Ts = np.asarray(Ts); B, k = Ts.shape
        a = Ts[:, :, None]; b = Ts[:, None, :]
        R = np.where(a == b, 1.0, np.where((a > 0) & (b > 0), self.r, 0.0))
        G = self.N * R
        zs = self.z[Ts]
        n = self.n
        H = (n + 1) * G + np.eye(k)[None]
        ldH = np.linalg.slogdet(H)[1]; ldA = np.linalg.slogdet(G + np.eye(k)[None])[1]
        Q = self.yty - n * np.einsum('bi,bi->b', zs, np.linalg.solve(H, zs[:, :, None])[:, :, 0])
        return self.logCn - 0.5 * (ldH - ldA) - self.nu * np.log(2 * B0 + Q) + self.logprior[k]

    def F(self, T):
        return float(self.F_batch(np.array([sorted(T)]))[0])


def one_rep(n, r, rng, theta=1.0, check_locmax=True):
    N = n - 1; m = N - 2
    E0, F0 = rng.standard_normal(2); G = rng.standard_normal(m)
    rest = rng.chisquare(N - m - 2) if N - m - 2 > 0 else 0.0
    sc = CoordScorer(n, r, theta, E0, F0, G, rest)
    a = 1 + int(np.argmax(G)); b = 1 + int(np.argmin(G))
    S = [0, a, b]
    FS, Fa, Fb = sc.F(S), sc.F([0, b]), sc.F([0, a])
    fail2 = FS >= max(Fa, Fb)
    locmax = None
    if fail2 and check_locmax:
        others = np.array([l for l in range(1, m + 1) if l not in (a, b)])
        best = -np.inf
        for chunk in np.array_split(others, max(1, len(others) // 20000)):
            best = max(best, sc.F_batch(np.column_stack([np.zeros_like(chunk), np.full_like(chunk, a), np.full_like(chunk, b), chunk])).max())
            best = max(best, sc.F_batch(np.column_stack([np.zeros_like(chunk), np.full_like(chunk, a), chunk])).max())  # swap b->l
            best = max(best, sc.F_batch(np.column_stack([np.zeros_like(chunk), np.full_like(chunk, b), chunk])).max())  # swap a->l
            best = max(best, sc.F_batch(np.column_stack([np.full_like(chunk, a), np.full_like(chunk, b), chunk])).max())  # swap 0->l
        best = max(best, sc.F([a, b]), Fa, Fb)
        locmax = FS > best
    # d = 1 check at S0
    F0s = sc.F([0])
    allnull = np.arange(1, m + 1)
    add1 = sc.F_batch(np.column_stack([np.zeros(m, int), allnull])).max()
    Zs = np.sqrt(r) * F0 + np.sqrt(1 - r) * G
    jmax, jmin = int(np.argmax(Zs)), int(np.argmin(Zs))
    # for each e the best partner is argmax or argmin of Z (excluding e); score is monotone in W
    W = np.maximum((Zs[jmax] - r * Zs) ** 2, (Zs[jmin] - r * Zs) ** 2) / (1 - r ** 2) + Zs ** 2
    e_best = int(np.argmax(W)); l_best = jmax if (Zs[jmax] - r * Zs[e_best]) ** 2 >= (Zs[jmin] - r * Zs[e_best]) ** 2 else jmin
    if l_best == e_best:
        l_best = jmin if l_best == jmax else jmax
    add2 = sc.F([0, 1 + e_best, 1 + l_best])
    ok1 = (F0s > add1) and (F0s > add2)
    return fail2, locmax, ok1, FS - max(Fa, Fb)


if __name__ == '__main__':
    out = open('../results/ld_counterexample.txt', 'w')
    def pr(*a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); out.write(s + '\n')
    pr("C-LD: exact equicorrelated-null design, s0=1, theta=1, sigma=1, p = n-2, S = S0+{argmax G, argmin G}")
    pr("cols: n r reps | frac D_S fails (TD'_P(R_{0,2}) fails) | frac spurious local max (of those checked) | frac d=1 OK | median F(S)-max F(S-e)")
    k = 0
    for r in (0.3, 0.55, 0.7, 0.9):
        for n in (200, 2000, 20000, 200000):
            reps = 200 if n <= 20000 else 60
            res = []
            for rep in range(reps):
                rng = np.random.default_rng(20261102 + 1000 * k + rep)
                res.append(one_rep(n, r, rng, check_locmax=(n <= 20000 and rep < 40)))
            k += 1
            f2 = np.mean([x[0] for x in res]); lm = [x[1] for x in res if x[1] is not None]
            ok1 = np.mean([x[2] for x in res]); md = np.median([x[3] for x in res])
            pr(f"n={n:7d} r={r:.2f} reps={reps:3d} | fail2={f2:.3f} | locmax={np.mean(lm) if lm else float('nan'):.3f} (k={len(lm)}) | d1_ok={ok1:.3f} | median margin={md:+.2f}")
    out.close()
