"""W3-POST numerics: exact coded posterior by full enumeration (small p) — falsification of Lemma 1a/1a', and
boundary-violation experiments for the sharpness gate (ASSUMPTION_MAP.md).

Target pi exactly as coded (Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224): X, y centred and scaled to
||.||^2 = n-1; H = (n+1)G + I, A = G + I, Q = y'y - n z'H^{-1}z, nu = 0.01 + n/2, b0 = 0.01,
log m(S) = -0.5(logdet H - logdet A) - nu log(2 b0 + Q) (+ const), log w(k) = -log 2 - log C(2p-1, k),
K = min(p, n // 2). Enumeration is batched by model size (all C(p,k) subsets at once).
Run: py -3.13 -I post_exact.py [experiment ...]  -> prints to stdout (redirect to post_exact_out.txt).
"""
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

    def size_tail(self, m):
        return float(self.pi[self.size > m].sum())


def Rm(p, K, t, m):
    """R_m = sum_{k=m+1}^K C(p,k) w(k) / w(t) (data-free)."""
    lw = lambda k: -math.log(2) - lchoose(2 * p - 1, k)
    return sum(math.exp(lchoose(p, k) + lw(k) - lw(t)) for k in range(m + 1, K + 1))


def summarise(name, rows):
    """rows: list of dicts per (n, seed)."""
    ns = sorted(set(r['n'] for r in rows))
    print(f"\n== {name}")
    print("   n   med(1-pi(S0))  med((1-pi)/r_n)  P(HPM=S0)  P(MPM=S0)  med max_{j notin S0} PIP  med min_{j in S0} PIP"
          "   [medians/frequencies over seeds]")
    for n in ns:
        rr = [r for r in rows if r['n'] == n]
        d = np.array([r['delta'] for r in rr]); rn = math.sqrt(math.log(n) / n)
        print(f"{n:5d}   {np.median(d):12.3e}   {np.median(d) / rn:12.3e}   {np.mean([r['hpm'] for r in rr]):7.2f}"
              f"   {np.mean([r['mpm'] for r in rr]):7.2f}   {np.median([r['fp'] for r in rr]):10.3e}"
              f"   {np.median([r['tp'] for r in rr]):10.3e}")


def run(design, theta_fn, S0, ns, seeds, name, extra=None):
    rows = []
    for n in ns:
        for sd in range(seeds):
            rng = np.random.default_rng(1000 * n + sd)
            Xr = design(n, rng)
            theta = theta_fn(n)
            X, _ = standardise(Xr, rng.standard_normal(n))  # standardise X first, so theta is the literal theta*
            yr = X[:, S0] @ theta + rng.standard_normal(n)  # (C1-A F5): mu = X theta*, sigma* = 1
            X, y = standardise(X, yr)
            P = Post(X, y)
            pip = P.pip()
            S0m = sum(1 << j for j in S0)
            notS0 = [j for j in range(P.p) if j not in S0]
            row = dict(n=n, delta=1 - P.mass(S0), hpm=P.hpm_mask() == S0m,
                       mpm=set(np.where(pip > .5)[0]) == set(S0),
                       fp=max(pip[notS0]) if notS0 else 0.0, tp=min(pip[S0]))
            if extra:
                row.update(extra(P, X, y, n))
            rows.append(row)
    summarise(name, rows)
    return rows


# ---------------------------------------------------------------- designs
P_DEF = 10  # Wave1 PROTOCOL compute rule: exact enumeration p <= 10 (C1-A F6)


def iid(n, rng, p=P_DEF):
    return rng.standard_normal((n, p))


def exp_baseline():
    run(iid, lambda n: np.array([1.0, -1.0]), [0, 1], NS, SEEDS, "E0 baseline: iid design, s0=2, theta=(1,-1)")


def exp_betamin():
    # theta^2 = c log n / n, s0 = 1, iid design (phi0 ~ 1). Fixed p=P_DEF=10 (A -> 0 effectively).
    for c in [0.5, 1.0, 2.0, 4.0, 8.0]:
        run(iid, lambda n, c=c: np.array([math.sqrt(c * math.log(n) / n)]), [0], NS, SEEDS,
            f"E1 beta-min boundary: theta^2 = {c} log n / n (c0 >= 32[s0(A+1)+2] >= 128)")
    run(iid, lambda n: np.array([math.sqrt(math.log(math.log(n)) / n)]), [0], NS, SEEDS,
        "E1' beta-min below rate: theta^2 = log log n / n")


def dep_nulls(n, rng, p=P_DEF):
    X = rng.standard_normal((n, p))
    X[:, p - 1] = X[:, 2] + X[:, 3] + X[:, 4] + X[:, 5]  # exact dependence among 5 null columns (x_10 = x_3+..+x_6)
    return X


def dup_nulls(n, rng, p=P_DEF):
    X = rng.standard_normal((n, p))
    X[:, p - 1] = X[:, p - 2]  # exact duplicate nulls
    X[:, p - 3] = X[:, p - 4] + rng.standard_normal(n) * n ** -0.5  # near-duplicate nulls
    return X


def exp_floors():
    th = lambda n: np.array([1.0, -1.0])
    run(dep_nulls, lambda n: np.array([1.0]), [0], NS, SEEDS,
        "E2 (F_w) violated, F_lambda kept: s0=1 (j0=4 at A=1), null x_10 = x_3+x_4+x_5+x_6 exactly (S0 u J singular at |J|=5)")
    run(dup_nulls, th, [0, 1], NS, SEEDS, "E3 (F_lambda) violated on null-only directions: exact + near-duplicate nulls")


def mask_design(gamma):
    def d(n, rng, p=P_DEF):
        X = rng.standard_normal((n, p))
        e2 = n ** (-gamma)  # 1 - rho^2
        X[:, 1] = math.sqrt(1 - e2) * X[:, 0] + math.sqrt(e2) * X[:, 1]  # null x_2 near-duplicates truth x_1
        return X
    return d


def exp_masking():
    for g in [0.5, 0.8, 1.0]:
        run(mask_design(g), lambda n: np.array([1.0]), [0], NS, SEEDS,
            f"E4 anchored floor -> 0: null x_2 with 1-corr^2 = n^-{g} to truth x_1 (theta=1); lambda_min(R_S0uJ) ~ n^-{g}/2")


def proxy_design(b2, s0):
    def d(n, rng, p=P_DEF):
        X = rng.standard_normal((n, p))
        a = math.sqrt((1 - b2) / s0)
        X[:, s0] = a * X[:, :s0].sum(1) + math.sqrt(b2) * X[:, s0]  # null proxy of s0 weak truths
        return X
    return d


def exp_specificity():
    # s0 = 4 weak truths (each below the single-inclusion threshold c = 1), null proxy x_5 carrying (1-b2) of their
    # joint signal; lambda_min(R_{S0 u {5}}) is fixed (b2 = 0.2), so (E), (F_lambda), (F_w) hold; only BM fails.
    for c in [0.5, 0.8]:
        run(proxy_design(0.2, 4), lambda n, c=c: np.full(4, math.sqrt(c * math.log(n) / n)), [0, 1, 2, 3], NS_BIG,
            SEEDS, f"E5 specificity without beta-min: 4 weak truths theta^2 = {c} log n/n, null proxy "
            "x_5 = a(x_1+..+x_4)+sqrt(.2)z (fixed anchored floor)", extra=lambda P, X, y, n: {})

def exp_size_tail():
    """Falsification of Lemma 1a/1a': Theta^T_{n,m} = pi(|S|>m) / (R_m (n+1)^{t/2} sqrt n) must be tight, sup over m."""
    def extra_for(T):
        def ex(P, X, y, n):
            t = len(T)
            th = []
            for m in range(t, P.K):
                R = Rm(P.p, P.K, t, m)
                if R > 0:
                    th.append(P.size_tail(m) / (R * (n + 1) ** (t / 2) * math.sqrt(n)))
            return dict(theta_sup=max(th) if th else 0.0)
        return ex

    cases = []
    # (a) p identical columns (Prop D of [T03R]): G and R hold with s0=1.
    def alldup(n, rng, p=P_DEF):
        x = rng.standard_normal(n)
        return np.tile(x[:, None], (1, p))
    cases.append(("L1a(a) all-duplicate design (T03R Prop D), S0={1}, theta=1", alldup, lambda n: np.array([1.0]), [0], [0]))
    # (b) singular S0 with bounded coefficients: x_2 = x_1 exactly, theta=(1,1): R fails; L1a' with T={1}.
    def dupS0(n, rng, p=P_DEF):
        X = rng.standard_normal((n, p)); X[:, 1] = X[:, 0]; return X
    cases.append(("L1a'(b) truth duplicated: x_2 = x_1, theta=(1,1), T={1}", dupS0, lambda n: np.array([1.0, 1.0]), [0, 1], [0]))
    # (c) near-singular S0, bounded theta (normalised lambda_min(R_S0) ~ n^-2, unnormalised ~ n^-1): T = S0.
    def nearS0(n, rng, p=P_DEF):
        X = rng.standard_normal((n, p)); X[:, 1] = X[:, 0] + X[:, 1] / n; return X
    cases.append(("L1a'(c) near-singular S0 (1-corr ~ n^-2), theta=(1,1), T=S0", nearS0, lambda n: np.array([1.0, 1.0]), [0, 1], [0, 1]))
    # (d) iid baseline, T=S0
    cases.append(("L1a(d) iid, s0=2, theta=(1,-1), T=S0", iid, lambda n: np.array([1.0, -1.0]), [0, 1], [0, 1]))
    # (e) cancelling huge coefficients (outside L1a': ||theta||^2 >> n): x_2 = x_1 + n^-1 z, theta = (L,-L), L = n
    def cancel(n, rng, p=P_DEF):
        X = rng.standard_normal((n, p)); X[:, 1] = X[:, 0] + X[:, 1] / n; return X
    cases.append(("L1a'(e) OUTSIDE hypothesis: theta=(n,-n), corr(x1,x2)=1-O(n^-2); T=S0 (||theta||^2/n = 2n)",
                  cancel, lambda n: np.array([float(n), -float(n)]), [0, 1], [0, 1]))
    for name, des, thf, S0, T in cases:
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                rng = np.random.default_rng(7000 * n + sd)
                Xr = des(n, rng)
                X, _ = standardise(Xr, rng.standard_normal(n))
                yr = X[:, S0] @ thf(n) + rng.standard_normal(n)
                X, y = standardise(X, yr)
                P = Post(X, y)
                rows.append(dict(n=n, **extra_for(T)(P, X, y, n)))
        print(f"\n== {name}")
        print("   n   median sup_m Theta   90% quantile   max")
        for n in NS:
            v = np.array([r['theta_sup'] for r in rows if r['n'] == n])
            print(f"{n:5d}   {np.median(v):10.3e}   {np.quantile(v, .9):10.3e}   {v.max():10.3e}")


NS = [100, 400, 1600, 6400]
NS_BIG = [100, 400, 1600, 6400, 25600]
SEEDS = 20
EXPS = dict(baseline=exp_baseline, betamin=exp_betamin, floors=exp_floors, masking=exp_masking,
            specificity=exp_specificity, sizetail=exp_size_tail)

if __name__ == "__main__":
    names = sys.argv[1:] or list(EXPS)
    print(f"post_exact.py: p={P_DEF}, seeds={SEEDS}, ns={NS} (NS_BIG={NS_BIG} for E5); exact enumeration of coded pi")
    for nm in names:
        EXPS[nm]()
        sys.stdout.flush()
