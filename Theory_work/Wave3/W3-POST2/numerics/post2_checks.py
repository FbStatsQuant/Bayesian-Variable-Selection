"""W3-POST2 numerics: exact coded posterior by full enumeration (p <= 10) — sharpness-gate boundary-violation
experiments and falsification checks for Claims A2, B, C, D (STATEMENT.md v1.0).

Target pi exactly as coded (Scripts/SMC_BVS/core/cpp/v3_score.h:40-71, 196-224; same formulas as
W3-POST/numerics/post_exact.py): X, y centred and scaled to ||.||^2 = n-1; H = (n+1)G + I, A = G + I,
Q = y'y - n z'H^{-1}z, nu = 0.01 + n/2, b0 = 0.01; log m(S) = -0.5(logdet H - logdet A) - nu log(2 b0 + Q);
log w(k) = -log 2 - log C(2p-1, k); K = min(p, n // 2).
Truth: mu = X[:, S0] theta (X already standardised, so theta is the literal theta*), sigma* = 1.
Run: py -3.13 -I post2_checks.py [N1 N2 N4 N5 N6 N6b N7 N8] > post2_checks_out.txt
v2 (sweep S01): exact a_J weights incl. 2^{j/2}; Occam range j <= min(m#_n, p - s0) with m#_n computed; full (ID)/(ID^M)
minima over all S in Omega with S0 not in S and |S minus S0| <= j0; min A2 slack and violation counts; N8 (F0 boundary);
N6 with a mean outside col X and a growing-cost reference.
"""
import sys, itertools, math
import numpy as np

B0, A0 = 0.01, 0.01
P_DEF = 10
NS = [100, 400, 1600, 6400]
SEEDS = 20


def lchoose(a, k):
    return math.lgamma(a + 1) - math.lgamma(k + 1) - math.lgamma(a - k + 1)


def stdcols(Xr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0)
    return X / np.sqrt((X ** 2).sum(0) / (n - 1))


def stdy(yr):
    n = len(yr)
    y = yr - yr.mean()
    sy = math.sqrt((y ** 2).sum() / (n - 1))
    return y / sy, sy


class Post:
    """Exact posterior over Omega; per-model log D, Q, rank, tr(M), fitted coefficient a_S = n H^{-1} z."""

    def __init__(self, X, y):
        n, p = X.shape
        self.n, self.p, self.K = n, p, min(p, n // 2)
        G = X.T @ X
        z = X.T @ y
        yty = float(y @ y)
        self.nu = nu = A0 + n / 2.0
        self.logw = np.array([-math.log(2) - lchoose(2 * p - 1, k) for k in range(self.K + 1)])
        self.models = []  # tuples
        lF, lD, Qs, rk, trM, coef = [], [], [], [], [], []
        for k in range(self.K + 1):
            subs = list(itertools.combinations(range(p), k))
            if k == 0:
                self.models.append(()); lF.append(self.logw[0] - nu * math.log(2 * B0 + yty)); lD.append(0.0)
                Qs.append(yty); rk.append(0); trM.append(0.0); coef.append(np.zeros(0)); continue
            idx = np.array(subs)
            Gs = G[idx[:, :, None], idx[:, None, :]]
            zs = z[idx]
            I = np.eye(k)
            H = (n + 1) * Gs + I
            _, ldH = np.linalg.slogdet(H)
            _, ldA = np.linalg.slogdet(Gs + I)
            sol = np.linalg.solve(H, zs[:, :, None])[:, :, 0]
            Q = np.maximum(yty - n * np.einsum('ij,ij->i', zs, sol), 0.0)
            ev = np.linalg.eigvalsh(Gs)
            r = (ev > 1e-8 * max(1.0, n)).sum(1)
            tm = (n * ev / ((n + 1) * ev + 1)).clip(min=0).sum(1)
            for i, s in enumerate(subs):
                self.models.append(s); coef.append(n * sol[i])
            lF.extend(self.logw[k] - 0.5 * (ldH - ldA) - nu * np.log(2 * B0 + Q))
            lD.extend(ldH - ldA); Qs.extend(Q); rk.extend(r); trM.extend(tm)
        self.logF = np.array(lF); self.logD = np.array(lD); self.Q = np.array(Qs)
        self.rank = np.array(rk); self.trM = np.array(trM); self.coef = coef
        self.size = np.array([len(s) for s in self.models])
        self.index = {s: i for i, s in enumerate(self.models)}
        w = np.exp(self.logF - self.logF.max())
        self.pi = w / w.sum()
        self.G = G

    def mass(self, S):
        return float(self.pi[self.index[tuple(sorted(S))]])

    def pip(self):
        return np.array([sum(self.pi[i] for i, s in enumerate(self.models) if j in s) for j in range(self.p)])

    def msharp(self, s0):
        """m#_n = min{m >= s0 : R_m <= n^{-(s0+1)/2} n^{-1/2}} ([W3P] section 0)."""
        n, p, K = self.n, self.p, self.K
        lw = lambda k: -math.log(2) - lchoose(2 * p - 1, k)
        for m in range(s0, K + 1):
            Rm = sum(math.exp(lchoose(p, k) + lw(k) - lw(s0)) for k in range(m + 1, K + 1))
            if Rm <= n ** (-(s0 + 2) / 2):
                return m
        return K

    def occam(self, S0):
        """O0_n (no weights, j <= K - s0) and O_n^{>0}, O_n^{>j0} with the exact weights
        a_J = 2^{j/2} (e C_A j log n / max(d,1))^{d/2} (STATEMENT v1.2), j <= min(m#_n, p - s0); A = max(1, log p/log n).
        Here K = p (p = 10 <= n/2), so every comparison union S0 u J lies in Omega and is enumerated."""
        n, p = self.n, self.p
        assert self.K == p
        s0 = len(S0); S0s = set(S0)
        A = max(1.0, math.log(p) / math.log(n))  # R1 takes A >= 1
        CA = 8 + 3 * A
        j0 = math.ceil((2 * A + 1) * s0) + 1
        jmax = min(self.msharp(s0), p - s0)
        i0 = self.index[tuple(sorted(S0))]
        r0 = self.rank[i0]
        O0 = Ow = Ow_j0 = 0.0
        for i, s in enumerate(self.models):
            if len(s) <= s0 or not S0s.issubset(s):
                continue
            j = len(s) - s0
            base = math.exp(self.logw[len(s)] - self.logw[s0] + 0.5 * (self.logD[i0] - self.logD[i]))
            O0 += base
            if j > jmax:
                continue
            d = self.rank[i] - r0
            a = 2 ** (j / 2) * (math.e * CA * j * math.log(n) / max(d, 1)) ** (d / 2)
            Ow += base * a
            if j > j0:
                Ow_j0 += base * a
        return O0, Ow, Ow_j0 * (2 * p) ** s0 * (n + 1) ** (s0 / 2)

    def margins(self, S0, X, mu):
        """min over S in Omega, S0 not subset of S, |S minus S0| <= j0, of Delta_S and L_S (sigma* = 1), via Gram matrices."""
        n, p = self.n, self.p
        s0 = len(S0); S0s = set(S0)
        A = max(1.0, math.log(p) / math.log(n))
        j0 = math.ceil((2 * A + 1) * s0) + 1
        b_all = X.T @ mu; mm = float(mu @ mu)
        dmin = lmin = float('inf')
        for s in self.models:
            if S0s.issubset(s) or len(set(s) - S0s) > j0:
                continue
            if not s:
                dmin = min(dmin, mm); lmin = min(lmin, mm); continue
            idx = list(s); G = self.G[np.ix_(idx, idx)]; b = b_all[idx]
            ev, V = np.linalg.eigh(G)
            keep = ev > 1e-9 * max(1.0, ev.max())
            proj = float(((V[:, keep].T @ b) ** 2 / ev[keep]).sum())
            ridge = float(n * b @ np.linalg.solve((n + 1) * G + np.eye(len(idx)), b))
            dmin = min(dmin, mm - proj); lmin = min(lmin, mm - ridge)
        return dmin, lmin


def gen(design, theta, S0, n, sd):
    rng = np.random.default_rng(1000 * n + sd)
    X = stdcols(design(n, rng))
    mu = X[:, S0] @ theta
    yr = mu + rng.standard_normal(n)
    y, sy = stdy(yr)
    return X, y, sy, mu - mu.mean()


def iid(n, rng, p=P_DEF):
    return rng.standard_normal((n, p))


def rn(n):
    return math.sqrt(math.log(n) / n)


def table(name, rows, cols):
    print(f"\n== {name}")
    print("    n  " + "  ".join(f"{c:>14s}" for c in cols) + "   [median over seeds; prefix mean/P = mean, min = minimum, sum = count]")
    for n in sorted(set(r['n'] for r in rows)):
        rr = [r for r in rows if r['n'] == n]
        out = []
        for c in cols:
            v = np.array([r[c] for r in rr], dtype=float)
            if c.startswith('mean') or c.startswith('P('):
                out.append(np.mean(v))
            elif c.startswith('min'):
                out.append(np.min(v))
            elif c.startswith('sum'):
                out.append(np.sum(v))
            else:
                out.append(np.median(v))
        print(f"{n:6d}  " + "  ".join(f"{x:14.4e}" for x in out))


def basic(P, S0):
    d = 1 - P.mass(S0)
    hpm = P.models[int(np.argmax(P.logF))] == tuple(sorted(S0))
    O0, Ow, Owj0 = P.occam(S0)
    return dict(delta=d, ratio=d / rn(P.n), sqrtn=d * math.sqrt(P.n), meandsqrtn=d * math.sqrt(P.n),
                **{'P(HPM=S0)': float(hpm)}, O0=O0, Ow_over_rn=Ow / rn(P.n), Owj0_over_rn=Owj0 / rn(P.n),
                minA2slack=d - O0 / (1 + O0), sumA2viol=float(d - O0 / (1 + O0) < -1e-9))


# ---------------------------------------------------------------- experiments
def N1():
    """Null x3 = x1 + x2 + s r, s = n^{-kappa/2}: unnormalised residual of x3 on col X_S0 ~ n^{1-kappa}.
    kappa = 0.5: (F_lambda) fails (phi0^2 ~ n^{-1/2}) but DG(j=1) and ID hold. kappa = 1: (F_lambda) fails (phi0^2 ~ 1/n) and (ID) fails (swap margin ~ 0.3 log n) while DG(j=1) holds
    (unnormalised residual O(1), the (F_w) scale).
    exact (s = 0): x3 in col X_S0, d_J = 0 (OS j=1 term of order 1/p). S0={0,1}, theta=(1,-1)."""
    for kappa in [None, 1.0, 0.5]:
        def des(n, rng, kappa=kappa):
            Z = rng.standard_normal((n, P_DEF))
            s = 0.0 if kappa is None else n ** (-kappa / 2)
            Z[:, 2] = Z[:, 0] + Z[:, 1] + s * math.sqrt(2) * Z[:, 2]
            return Z
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                X, y, sy, mu = gen(des, np.array([1.0, -1.0]), [0, 1], n, sd)
                P = Post(X, y)
                r = basic(P, [0, 1])
                dmin, lmin = P.margins([0, 1], X, mu)   # full minima over the (ID) family
                r['IDmin_over_logn'] = dmin / math.log(n); r['IDMmin_over_logn'] = lmin / math.log(n)
                r['n'] = n; rows.append(r)
        lab = 'exact (x3 in span S0)' if kappa is None else f'kappa={kappa}'
        table(f"N1 anchored dependence, {lab}; A2 lower bound slack must be >= 0", rows,
              ['delta', 'ratio', 'O0', 'Ow_over_rn', 'minA2slack', 'sumA2viol', 'IDmin_over_logn',
               'IDMmin_over_logn', 'P(HPM=S0)'])


def N2():
    """Null duplicate pair x6 = x7 (not in span S0): (F_lambda), pointwise DG and ADG (fixed p) fail; OS holds?"""
    def des(n, rng):
        Z = rng.standard_normal((n, P_DEF)); Z[:, 7] = Z[:, 6]; return Z
    rows = []
    for n in NS:
        for sd in range(SEEDS):
            X, y, sy, mu = gen(des, np.array([1.0, -1.0]), [0, 1], n, sd)
            P = Post(X, y)
            r = basic(P, [0, 1]); r['n'] = n; rows.append(r)
    table("N2 null duplicate pair (F_lambda, DG, ADG fail at fixed p)", rows,
          ['delta', 'ratio', 'O0', 'Ow_over_rn', 'Owj0_over_rn', 'minA2slack', 'sumA2viol', 'P(HPM=S0)'])


def N4():
    """Margin experiment: s0 = 1, iid design, coefficient scale theta^2 = c log n / n (c is a coefficient-scale
    parameter, not the (ID) constant); the achieved full (ID)/(ID^M) minima are reported."""
    for c in [1.0, 2.0, 4.0, 8.0]:
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                th = math.sqrt(c * math.log(n) / n)
                X, y, sy, mu = gen(iid, np.array([th]), [0], n, sd)
                P = Post(X, y)
                r = basic(P, [0]); dmin, lmin = P.margins([0], X, mu)
                r['IDmin_over_logn'] = dmin / math.log(n); r['IDMmin_over_logn'] = lmin / math.log(n); r['n'] = n
                rows.append(r)
        table(f"N4 coefficient scale c={c} (theta^2 = c log n/n)", rows,
              ['delta', 'ratio', 'IDmin_over_logn', 'IDMmin_over_logn', 'P(HPM=S0)'])


def N5():
    """Claim C: E delta (mean over seeds) * sqrt(n) at the E0 baseline and an s0=1 strong-signal case."""
    for th, S0 in [(np.array([1.0, -1.0]), [0, 1]), (np.array([0.5]), [0])]:
        rows = []
        for n in NS + [25600]:
            for sd in range(SEEDS):
                X, y, sy, mu = gen(iid, th, S0, n, sd)
                P = Post(X, y)
                d = 1 - P.mass(S0)
                rows.append(dict(n=n, meandelta=d, meandsqrtn=d * math.sqrt(n), meanbound=d * math.sqrt(n) /
                                 math.exp(2 * math.sqrt(2 * math.log(n)))))
        table(f"N5 expectation rate, theta={th.tolist()}: mean delta*sqrt(n) (Claim C v2 proves E delta = O(r_n))", rows, ['meandelta', 'meandsqrtn', 'meanbound'])


def N6():
    """Claim B falsification: Theta'' = pi(|S|>m) / A^T_m over m (t <= m < K), for references T with B_T bounded."""
    cases = [("s0=3, theta=(1,-1,n^-1/2): T=S0 (t=3)", [0, 1, 2], lambda n: np.array([1, -1, n ** -0.5]), 'S0'),
             ("s0=3, theta=(1,-1,n^-1/2): T=S0 minus weak (t=2)", [0, 1, 2], lambda n: np.array([1, -1, n ** -0.5]),
              'drop'),
             ("s0=2, theta=n^-1/2 (1,1): T=empty (t=0)", [0, 1], lambda n: n ** -0.5 * np.array([1.0, 1.0]), 'empty')]
    for name, S0, thf, mode in cases:
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                X, y, sy, mu = gen(iid, thf(n), S0, n, sd)
                P = Post(X, y)
                if mode == 'S0':
                    T, vt = S0, thf(n)
                elif mode == 'drop':
                    T, vt = S0[:2], thf(n)[:2]
                else:
                    T, vt = [], np.zeros(0)
                t = len(T)
                fit = X[:, T] @ vt if t else np.zeros(n)
                Bcost = float((mu - fit) @ (mu - fit) + (fit @ fit + vt @ vt) / n)
                lDT = P.logD[P.index[tuple(T)]]
                lw = P.logw
                th = []
                for m in range(t, P.K):
                    Rm = sum(math.exp(lchoose(P.p, k) + lw[k] - lw[t]) for k in range(m + 1, P.K + 1))
                    A = Rm * math.exp(0.5 * lDT) * math.sqrt(n)
                    tail = float(P.pi[P.size > m].sum())
                    th.append(tail / A)
                rows.append(dict(n=n, maxTheta=max(th), B=Bcost))
        table(f"N6 Claim B: {name}; max over t<=m<K of Theta'' (must stay O(1))", rows, ['maxTheta', 'B'])


def N7():
    """Claim D: posterior expectations of ||mu_hat - mu||^2 and n (v/sigma*^2 - 1)^2 (sigma* = 1), original scale."""
    designs = [("D(a) BM: iid, s0=2, theta=(1,-1)", iid, lambda n: np.array([1.0, -1.0]), [0, 1]),
               ("D(b) no BM: iid, s0=2, theta^2=0.5 log n/n (weak)", iid,
                lambda n: math.sqrt(0.5 * math.log(n) / n) * np.array([1.0, -1.0]), [0, 1])]
    for name, des, thf, S0 in designs:
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                X, y, sy, mu = gen(des, thf(n), S0, n, sd)
                P = Post(X, y)
                Xtmu = X.T @ mu; mumu = float(mu @ mu)
                Em = Ev = 0.0
                for i, s in enumerate(P.models):
                    if P.pi[i] < 1e-14:
                        continue
                    beta = (B0 + P.Q[i] / 2) * sy ** 2          # v | S ~ IG(nu, b0 s_y^2 + Q^c/2), Q^c = s_y^2 Q
                    Evs = beta / (P.nu - 1); Varv = beta ** 2 / ((P.nu - 1) ** 2 * (P.nu - 2))
                    if s:
                        a = sy * P.coef[i]; idx = list(s)
                        err = float(a @ P.G[np.ix_(idx, idx)] @ a - 2 * a @ Xtmu[idx] + mumu)
                    else:
                        err = mumu
                    Em += P.pi[i] * (err + Evs * P.trM[i])
                    Ev += P.pi[i] * (Varv + (Evs - 1) ** 2)
                rows.append(dict(n=n, Emu=Em, Emu_over_logn=Em / math.log(n), nEv=n * Ev,
                                 nhbar2_bound=n * Ev + Em / 4))
        table(f"N7 {name}: posterior E||mu_hat-mu||^2, n E(v-1)^2, n * E[h-bar^2 bound]", rows,
              ['Emu', 'Emu_over_logn', 'nEv', 'nhbar2_bound'])



def thetas_tail(P, T, n):
    """max over t <= m < K of pi(|S| > m) / A^T_m (Claim B normalisation, exact determinant)."""
    t = len(T); lDT = P.logD[P.index[tuple(T)]]; lw = P.logw; th = []
    for m in range(t, P.K):
        Rm = sum(math.exp(lchoose(P.p, k) + lw[k] - lw[t]) for k in range(m + 1, P.K + 1))
        th.append(float(P.pi[P.size > m].sum()) / (Rm * math.exp(0.5 * lDT) * math.sqrt(n)))
    return max(th)


def N6b():
    """Claim B outside the earlier N6 cases: (i) mean with a component g orthogonal to col X (G' only), ||g||^2 = 2,
    reference T = S0 with theta (cost B = ||g||^2 + O(1)); (ii) growing cost: s0 = 1, theta = 1, reference T = empty
    (B = ||mu||^2 = n - 1) -- outside the bounded-cost hypothesis."""
    for case in ['orth', 'grow']:
        rows = []
        for n in NS:
            for sd in range(SEEDS):
                rng = np.random.default_rng(7000 * n + sd)
                X = stdcols(iid(n, rng))
                if case == 'orth':
                    S0, th = [0, 1], np.array([1.0, -1.0])
                    g = rng.standard_normal(n); g -= g.mean()
                    g -= X @ np.linalg.lstsq(X, g, rcond=None)[0]
                    g *= math.sqrt(2.0) / np.linalg.norm(g)
                    mu = X[:, S0] @ th + g; T, vt = S0, th
                else:
                    S0, th = [0], np.array([1.0])
                    mu = X[:, S0] @ th; T, vt = [], np.zeros(0)
                y, sy = stdy(mu + rng.standard_normal(n))
                P = Post(X, y)
                fit = X[:, T] @ vt if T else np.zeros(n)
                B = float((mu - fit) @ (mu - fit) + (fit @ fit + vt @ vt) / n)
                rows.append(dict(n=n, maxTheta=thetas_tail(P, T, n), B=B))
        lab = ('mean outside col X (||g||^2 = 2), T = S0' if case == 'orth'
               else 'growing cost: T = empty under strong signal (B = n - 1)')
        table(f"N6b Claim B: {lab}; max over t<=m<K of Theta''", rows, ['maxTheta', 'B'])


def N8():
    """(F0) boundary: s0 = 2, x2 = x1 + n^{-1/4} z (so lambda_min(R_S0) ~ n^{-1/2}/2 -> 0), theta = (1, 1).
    (E) holds; the ridge cost L_S0 stays bounded; report delta/r_n and the full (ID)/(ID^M) minima."""
    def des(n, rng):
        Z = rng.standard_normal((n, P_DEF)); Z[:, 1] = Z[:, 0] + n ** (-0.25) * Z[:, 1]; return Z
    rows = []
    for n in NS:
        for sd in range(SEEDS):
            X, y, sy, mu = gen(des, np.array([1.0, 1.0]), [0, 1], n, sd)
            P = Post(X, y)
            r = basic(P, [0, 1]); dmin, lmin = P.margins([0, 1], X, mu)
            G0 = X[:, :2].T @ X[:, :2] / (n - 1)
            r['lmin_RS0'] = float(np.linalg.eigvalsh(G0)[0])
            r['IDmin_over_logn'] = dmin / math.log(n); r['IDMmin_over_logn'] = lmin / math.log(n); r['n'] = n
            rows.append(r)
    table("N8 (F0) boundary: near-collinear truths, theta = (1, 1)", rows,
          ['delta', 'ratio', 'lmin_RS0', 'IDmin_over_logn', 'IDMmin_over_logn', 'minA2slack', 'P(HPM=S0)'])

if __name__ == '__main__':
    exps = sys.argv[1:] or ['N1', 'N2', 'N4', 'N5', 'N6', 'N6b', 'N7', 'N8']
    for e in exps:
        globals()[e]()
        sys.stdout.flush()
