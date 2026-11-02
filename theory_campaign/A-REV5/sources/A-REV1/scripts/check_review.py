"""Independent, small deterministic/enumerative referee checks. Run via owls_run.

No campaign code is imported. Small-p SMC is a component test: production
would enumerate these instances. Floating arithmetic checks do not prove EX-A.
"""
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20261102)


def pop(x):
    return bin(int(x)).count("1")


def softmax(x):
    w = np.exp(x - np.max(x))
    return w / w.sum()


def score_instance(n, corr, theta, seed):
    p = len(theta)
    rng = np.random.default_rng(seed)
    # Exact contrast-coordinate realisation; avoids allocating an n by n matrix.
    G = (n - 1) * corr
    chol = np.linalg.cholesky(G)
    eps = rng.normal(size=n - 1)
    signal = chol.T @ theta
    raw = eps.copy()
    raw[:p] += signal
    yy = float(raw @ raw)
    z = chol @ raw[:p] * math.sqrt((n - 1) / yy)
    lm, rss = [], []
    for mask in range(1 << p):
        ix = [j for j in range(p) if mask >> j & 1]
        g = G[np.ix_(ix, ix)]
        zz = z[ix]
        H = (n + 1) * g + np.eye(len(ix))
        logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(g + np.eye(len(ix)))[1]
        Q = n - 1 - n * float(zz @ np.linalg.solve(H, zz))
        lm.append(-0.5 * logD - (n / 2 + .01) * math.log(.02 + Q))
        rss.append(n - 1 - float(zz @ np.linalg.solve(g, zz)))
    return np.array(lm), np.array(rss), G, z, yy


def ess_checks():
    worst = 1.0
    for _ in range(2000):
        H = int(RNG.integers(2, 31))
        w = np.exp(RNG.normal(size=H) * 2)
        k = int(RNG.integers(1, H))
        e = float(w.sum() ** 2 / (H * (w @ w)))
        f = k / H
        lower = f - math.sqrt(f * (1 - f) * (1 / e - 1))
        worst = min(worst, float(np.sort(w)[:k].sum() / w.sum()) - lower)
    rstar = (11 + 2 * math.sqrt(10)) / 9
    # Exact finite multiplicities giving the Kantorovich minimum at r=77/40.
    w = np.array([1.] * 77 + [77 / 40] * 40)
    old_ess = float(w.sum() ** 2 / (len(w) * (w @ w)))
    assert old_ess < .9
    f = 1 / 20
    lower = f - math.sqrt(f * (1 - f) / 9)
    assert lower < 0
    f2 = .4
    w2 = np.array([1 - math.sqrt((1 - f2) / f2) / 3] * 4
                  + [1 + math.sqrt(f2 / (1 - f2)) / 3] * 6)
    tight_slack = float(w2[:4].sum() / w2.sum()) - (f2 - math.sqrt(f2 * (1 - f2)) / 3)
    assert abs(tight_slack) < 1e-14 and worst > -1e-12
    return dict(cases=2000, worst_slack=worst, rstar=rstar,
                old_ratio=77 / 40, old_ratio_ess=old_ess,
                corrected_ratio_ess=4 * rstar / (1 + rstar) ** 2,
                f_005_lower=lower, invalid_low_weight=lower / f,
                valid_tight_slack=tight_slack)


def stream_check():
    # Two particles, two rounds; a block reads its first bit and, if zero,
    # reads a second bit. State = last bit read. Max total length is 8.
    joint = np.zeros((4, 4))
    for bits in itertools.product((0, 1), repeat=8):
        pos, paths = 0, [0, 0]
        for h in range(2):
            for i in range(2):
                b = bits[pos]
                pos += 1
                if b == 0:
                    b = bits[pos]
                    pos += 1
                paths[i] = paths[i] * 2 + b
        joint[tuple(paths)] += 1 / 256
    residual = float(np.max(np.abs(joint - np.outer(joint.sum(1), joint.sum(0)))))
    assert residual == 0
    return dict(enumerated_streams=256, independence_residual=residual,
                completion_counterexample="Independent fair bits conditioned equal: P(00|equal)=1/2, product marginals=1/4")


def lemma_u_checks():
    p, k = 8, 3
    corr = .5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    theta = np.array([1., 0, -.8, 0, 0, .6, 0, 0])
    phi02 = float(np.linalg.eigvalsh(corr).min())
    M = float(theta @ corr @ theta) + 1
    cE = 1 / (8 * (M + 2))
    rows = []
    for n in (200, 800):
        lm, rss, _, _, _ = score_instance(n, corr, theta, 701 + n)
        kap = (1 + 1 / phi02) / (2 * phi02 * (n - 1)) + (n / 2 + .01) * (1.02 + 1 / (n * phi02)) / (cE * n)
        vals = []
        for T in range(1 << p):
            if pop(T) >= k:
                continue
            for j in range(p):
                if not T >> j & 1:
                    U = T | 1 << j
                    vals.append(float(lm[U] - lm[T] + .5 * math.log(n + 1)
                                      + (n / 2 + .01) * math.log(rss[U] / rss[T])))
        mx = max(map(abs, vals))
        assert mx < kap
        rows.append(dict(n=n, pairs=len(vals), max_abs_remainder=mx, kappa=kap))
    return dict(rows=rows, correct_limit=.51 / cE, printed_limit=.52 / cE)


class TinyRound:
    def __init__(self, n=200, one_truth=False):
        self.p, self.B, self.K = 4, 2, 4
        self.m, self.size = 8, 16
        corr = np.array([[1., .7, 0, 0], [.7, 1, 0, 0],
                         [0, 0, 1, .5], [0, 0, .5, 1.]])
        theta = np.array([1.2, 0, 0 if one_truth else .9, 0])
        self.truth = 1 if one_truth else 5
        lm, _, _, _, _ = score_instance(n, corr, theta, 91)
        prior = np.array([-math.log(2) - math.log(math.comb(7, pop(x))) for x in range(16)])
        self.F = lm + prior
        self.lg0 = prior + (lm[np.arange(16) & 3] - lm[0]) + (lm[np.arange(16) & 12] - lm[0])
        self.pi0, self.pi = softmax(self.lg0), softmax(self.F)
        self.d = self.F - self.lg0
        self.nb = [{1}, {0}, {3}, {2}]

    @lru_cache(None)
    def outcomes(self, e, x, phi=1.):
        """(next state, probability, target scored), including rejected proposals."""
        logw = (1 - phi) * self.lg0 + phi * self.F
        if e < self.p:
            y = x ^ (1 << e)
            prob = float(1 / (1 + np.exp(logw[x] - logw[y])))
            hit = x == self.truth or y == self.truth
            return ((y, prob, hit), (x, 1 - prob, hit))
        inc = [j for j in range(self.p) if x >> j & 1]
        exc = [j for j in range(self.p) if not x >> j & 1]
        if e == self.m - 1:
            proposals = [(y, float(self.pi0[y]), phi * float(self.d[y] - self.d[x])) for y in range(16)]
        elif not inc or (e == self.p and not exc):
            return ((x, 1., x == self.truth),)
        else:
            proposals = []
            for j in inc:
                cand = exc if e == self.p else sorted(self.nb[j].intersection(exc))
                if not cand:
                    proposals.append((x, 1 / len(inc), 0.))
                for l in cand:
                    y = x ^ (1 << j) ^ (1 << l)
                    ratio = float(logw[y] - logw[x])
                    if e != self.p:
                        back = len([q for q in self.nb[l] if not y >> q & 1])
                        ratio += math.log(len(cand) / back)
                    proposals.append((y, 1 / (len(inc) * len(cand)), ratio))
        out = []
        for y, pr, la in proposals:
            acc = math.exp(min(0., la))
            hit = x == self.truth or y == self.truth
            out += [(y, pr * acc, hit), (x, pr * (1 - acc), hit)]
        return tuple(out)

    def nohit_matrix(self, phi=1., allowed=None):
        @lru_cache(None)
        def rec(rem, x):
            if x == self.truth or (allowed is not None and x not in allowed):
                return np.zeros(16)
            if rem == 0:
                v = np.zeros(16)
                v[x] = 1
                return v
            ans = np.zeros(16)
            for e in range(self.m):
                if rem >> e & 1:
                    for y, pr, hit in self.outcomes(e, x, phi):
                        if not hit and pr:
                            ans += pr * rec(rem ^ (1 << e), y) / pop(rem)
            return ans
        return np.array([rec(255, x) for x in range(16)])

    def constants(self, x):
        s0 = self.truth
        missing = s0 & ~x
        A = set().union(*(self.nb[j] for j in range(4) if missing >> j & 1)) if missing else set()
        A = sum(1 << j for j in A if not s0 >> j & 1)
        junk = 15 & ~(s0 | A)
        c = pop(x & junk)
        a = pop(A) + c if missing else pop(x & ~s0)
        sup = [w for w in range(16) if w & s0 == s0 and pop(w & ~s0) <= a]
        z = [w for w in range(16) if w & (x & s0) == (x & s0) and pop(w & junk) <= c and w & s0 != s0] if missing else []
        fam = set(z + sup)
        def V(w):
            return pop(s0 & ~w) + a if w & s0 != s0 else pop(w & ~s0)
        def bad(w, y):
            return y not in fam or V(y) > V(w) or (y & (w & s0)) != (w & s0)
        def eta(states):
            return sum(max((sum(pr for y, pr, _ in self.outcomes(e, w) if bad(w, y)) for w in states), default=0.) for e in range(8))
        def incprob(w, j):
            plus, minus = w | 1 << j, w & ~(1 << j)
            return float(1 / (1 + np.exp(self.F[minus] - self.F[plus])))
        epsadd = 0.
        for M in set(s0 & ~w for w in z):
            epsadd = max(epsadd, min(max(1 - incprob(w, j) for w in z if s0 & ~w == M)
                                    for j in range(4) if M >> j & 1))
        proper = [w for w in sup if w != s0]
        epsdel = max((incprob(w, l) for w in proper for l in range(4) if (w & ~s0) >> l & 1), default=0.)
        hiding = {}
        for l in range(4):
            if s0 >> l & 1:
                continue
            hiding[l] = .5 * sum(max((sum(pr for y, pr, _ in self.outcomes(e, w)
                                           if not bad(w, y) and V(y) == V(w) and not y >> l & 1)
                                     for w in sup if w >> l & 1), default=0.) for e in range(4, 8))
        Ha = max((min(min(hiding[l] for l in range(4) if (w & ~s0) >> l & 1),
                      4 / (pop(w & ~s0) + 4)) for w in proper), default=0.)
        cstar = min(1 - epsadd, 1 - epsdel - Ha) if missing else 1 - epsdel - Ha
        return cstar, eta(z) + eta(proper), V(x)


def round_checks():
    model = TinyRound()
    Q = model.nohit_matrix()
    gx, gw = np.polynomial.legendre.leggauss(8)
    ts, ws = (gx + 1) / 2, gw / 2
    p1 = []
    for j in range(4):
        x = model.truth ^ (1 << j)
        q = [sum(pr for y, pr, _ in model.outcomes(e, x) if y != x) for e in range(8) if e != j]
        a1 = float(ws @ np.prod(1 - ts[:, None] * np.array(q), axis=1))
        hit = float(1 - Q[x].sum())
        assert hit + 1e-12 >= a1
        p1.append(dict(start=x, a1=a1, exact_round_hit=hit))
    cases, nonvacuous, worst = 0, 0, -1.
    theorem_rows = []
    for H in (1, 2, 4):
        failure = np.linalg.matrix_power(Q, H) @ np.ones(16)
        for x in range(16):
            if x == model.truth:
                continue
            c, eta, v = model.constants(x)
            if c <= 0:
                continue
            tail = sum(math.comb(H, j) * c ** j * (1 - c) ** (H - j) for j in range(min(v, H + 1)))
            bound = tail + H * eta
            cases += 1
            nonvacuous += bound < 1
            worst = max(worst, float(failure[x]) - bound)
            assert failure[x] <= bound + 1e-11
            theorem_rows.append(dict(start=x, H=H, cstar=c, eta=eta, v=v, bound=bound, exact_failure=float(failure[x])))
    # D2 one-particle ingredient, across three temperatures. Then exact iid
    # multinomial-resampling/independent-round probability given a population.
    x, j = 1, 2
    excluded = {3}
    dep = sum(max(math.exp(float(model.lg0[x ^ (1 << l)] - model.lg0[x])),
                  math.exp(float(model.F[x ^ (1 << l)] - model.F[x])))
              for l in range(4) if l not in excluded | {j})
    beta = max(0., 1 - dep) / (len(excluded) + model.B + 3)
    d2 = []
    for phi in (0., .3, 1.):
        hit = float(1 - model.nohit_matrix(phi)[x].sum())
        assert hit + 1e-12 >= beta
        d2.append(dict(phi=phi, exact_hit=hit, beta=beta))
    # Detailed balance for all eight elementary kernels, target phi=1.
    residual = 0.
    for e in range(8):
        K = np.zeros((16, 16))
        for x in range(16):
            for y, pr, _ in model.outcomes(e, x):
                K[x, y] += pr
        flow = model.pi[:, None] * K
        residual = max(residual, float(np.max(np.abs(flow - flow.T))))
        assert np.max(np.abs(K.sum(1) - 1)) < 1e-12
    assert residual < 1e-12
    return dict(p=4, labels=8, permutations=math.factorial(8), p1=p1,
                theorem_B_cases=cases, nonvacuous_cases=nonvacuous, worst_lhs_minus_rhs=worst,
                theorem_B_rows=theorem_rows, d2_dep=dep, d2_round=d2, detailed_balance_residual=residual)


def ce1_check():
    # One truth, one proxy, independent junk. Y={junk}, d=1.
    # An exact first-state-change exit event lower-bounds first exit.
    rows = []
    gx, gw = np.polynomial.legendre.leggauss(8)
    t, weights = (gx + 1) / 2, gw / 2
    for n in (200, 800):
        model = TinyRound(n, one_truth=True)
        Y, truth = 4, 1
        s, q = [], []
        for e in range(8):
            outcomes = model.outcomes(e, Y)
            q.append(sum(pr for y, pr, _ in outcomes if y != Y))
            s.append(sum(pr for y, pr, _ in outcomes if pop(y & ~truth) > 1))
        first_exit = sum(s[e] * float(weights @ np.prod(1 - t[:, None] * np.delete(q, e), axis=1)) for e in range(8))
        oproxy = sum(pr for y, pr, _ in model.outcomes(1, Y) if y == Y | 2)
        lower = oproxy / 7  # B+d+4 = 7; no present truths, Q_T=0.
        assert first_exit + 1e-12 >= lower
        rows.append(dict(n=n, proxy_add_probability=oproxy, first_change_exit=first_exit, lemma_E_lower=lower))
    return rows


def e3_check():
    # Admissible BVS data: p=2, n=20, orthogonal centred columns, y=x_2.
    # Actual method B=1, hence both start blocks are singletons. Reference {1}.
    n, p = 20, 2
    G, z = (n - 1) * np.eye(2), np.array([0., n - 1.])
    lm = []
    for mask in range(4):
        ix = [j for j in range(p) if mask >> j & 1]
        g, zz = G[np.ix_(ix, ix)], z[ix]
        h = (n + 1) * g + np.eye(len(ix))
        logD = np.linalg.slogdet(h)[1] - np.linalg.slogdet(g + np.eye(len(ix)))[1]
        Q = n - 1 - n * float(zz @ np.linalg.solve(h, zz))
        lm.append(-.5 * logD - (n / 2 + .01) * math.log(.02 + Q))
    r1, r2 = math.exp(lm[1] - lm[0]), math.exp(lm[2] - lm[0])
    q, e = r2, 4 / r1
    purported = (1 - q) ** 2 / (1 + e)
    prior = np.array([-math.log(2 * math.comb(3, pop(x))) for x in range(4)])
    lg0 = prior + np.array([0., math.log(r1), math.log(r2), math.log(r1 * r2)])
    mass = float(softmax(lg0)[1])
    assert purported > 1 and mass < .5
    # The E3 main deterministic implication includes centre scoring and the
    # last scan: with ell=0, starting one flip away must score the target.
    tiny = TinyRound()
    centre = 1
    scanned = {centre} | {centre ^ (1 << j) for j in range(4)}
    assert tiny.truth in scanned
    return dict(n=n, p=p, B=1, reference="{1}", y="x_2", q=q, e=e,
                false_lower_bound=purported, true_reference_mass=mass,
                actual_start_mode_mask=int(np.argmax(lg0)),
                final_scan_scores_truth_at_zero_moves=True)


if __name__ == "__main__":
    results = dict(seed=20261102, ess=ess_checks(), streams=stream_check(),
                   lemma_u=lemma_u_checks(), rounds=round_checks(), ce1=ce1_check(), e3=e3_check())
    out = ROOT / "results" / "independent_checks.json"
    out.write_text(json.dumps(results, indent=2) + "\n")
    summary = {k: v for k, v in results.items() if k != "rounds"}
    summary["rounds"] = {k: v for k, v in results["rounds"].items() if k != "theorem_B_rows"}
    print(json.dumps(summary, indent=2))
