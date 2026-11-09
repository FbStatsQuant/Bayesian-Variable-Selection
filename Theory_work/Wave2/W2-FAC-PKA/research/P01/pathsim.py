"""P01 exact-score LS0 path simulator for the singleton exact-CS subclass (research, not a lemma input).

Setting (SINGLETON_TARGET v2): rho=1/2, sigma=1, singleton blocks, S0={0..s0-1}, theta=1 on S0,
p=floor(c n), K=floor(n/2), h=n-1.  Enlarged-space representation g=(eta 1+xi)/sqrt2, r~chi2(n-1-p).

Score: F(U)=log w(k)-L_k/2-nu*log(.02+Q_U), Q_U=h-n*quad_U, quad_U=(sum z^2-gamma_k (sum z)^2)/alpha.
quad is evaluated in the centred form z_j=b+d*w_j (w_j=xi_j+(f/d)theta_j) to avoid cancellation:
  sum z^2-gamma(sum z)^2 = alpha*(k b^2+2 b d W1)/(alpha+k beta) + d^2 (W2-gamma W1^2).
Best-move search is exact: deletion -> null nearest the centre c_T (t-space), addition -> outside extreme,
swap -> V convex in t_l (outside extreme) and concave in t_j (nearest inside null to gamma t_l/(1+gamma)).
Candidates' scores are computed directly from sums; truth deletions/truth-out swaps are scored too.
Validated against brute-force complete scans in validate.py.
"""
import math, sys, json
import numpy as np
from sortedcontainers import SortedList


class Model:
    def __init__(self, n, c, s0, seed, xi=None, eta=None, r=None):
        self.n = n; h = n - 1; self.h = h
        p = int(math.floor(c * n)); self.p = p; self.K = n // 2; self.s0 = s0
        rng = np.random.default_rng(seed)
        self.eta = float(rng.standard_normal()) if eta is None else eta
        self.xi = rng.standard_normal(p) if xi is None else np.asarray(xi, float)
        self.r = float(rng.chisquare(n - 1 - p)) if r is None else r
        g = (self.eta + self.xi) / math.sqrt(2)
        G = g.sum()
        PXe = float((2 * (g @ g - G * G / (p + 1))))  # g' Sigma^-1 g, Sigma^-1=2(I-J/(p+1))
        self.e2 = PXe + self.r
        tSt = 0.5 * s0 + 0.5 * s0 * s0
        YY = h * tSt + 2 * math.sqrt(h) * float(g[:s0].sum()) + self.e2
        self.s = math.sqrt(YY / h)
        s = self.s
        self.b = (h * s0 / 2 + math.sqrt(h / 2) * self.eta) / s
        self.d = math.sqrt(h / 2) / s
        self.f = h / (2 * s)
        self.w = self.xi.copy(); self.w[:s0] += self.f / self.d
        self.alpha = (n * n - 1) / 2 + 1; self.beta = (n * n - 1) / 2
        self.alp = h / 2 + 1; self.bep = h / 2
        self.nu = 0.01 + n / 2
        K = self.K
        ks = np.arange(0, K + 2)
        lw = -math.log(2) - (np.array([math.lgamma(2 * p) - math.lgamma(k + 1) - math.lgamma(2 * p - k) for k in ks]))
        L = np.zeros(len(ks))
        L[1:] = (ks[1:] - 1) * math.log(self.alpha / self.alp) + np.log((self.alpha + ks[1:] * self.beta) / (self.alp + ks[1:] * self.bep))
        self.pen = lw - L / 2  # log w(k) - L_k/2

    def gam(self, k):
        return self.beta / (self.alpha + k * self.beta)

    def psi(self, k, W1, W2):
        if k == 0:
            return 0.02 + self.h  # Q_empty = y'y = h
        a, be, b, d = self.alpha, self.beta, self.b, self.d
        g = be / (a + k * be)
        core = a * (k * b * b + 2 * b * d * W1) / (a + k * be) + d * d * (W2 - g * W1 * W1)
        return 0.02 + self.h - self.n * core / a

    def F(self, k, W1, W2):
        return self.pen[k] - self.nu * math.log(self.psi(k, W1, W2))

    def centre_w(self, k, W1):
        """x_T in w/xi units: t_j = d*(w_j - x_T)."""
        a, be = self.alpha, self.beta
        g = be / (a + k * be)
        off = (self.b * (a / (a + k * be)) - g * 0.0) / self.d  # b(1-k gamma)/d ; truth part in W1 via w
        return g * W1 - off

    def start(self):
        z2 = (self.b + self.d * self.w) ** 2
        order = np.argsort(-z2, kind='stable')
        T = set(int(j) for j in order[:self.K])
        assert all(j in T for j in range(self.s0)), "truth not in start"
        return T


def run(model, cap=None, record=True, start=None):
    m = model; s0 = m.s0; K = m.K; p = m.p
    T = m.start() if start is None else set(start)
    assert all(j in T for j in range(s0)) and len(T) <= K
    ins = SortedList((m.xi[j], j) for j in T if j >= s0)
    out = SortedList((m.xi[j], j) for j in range(s0, p) if j not in T)
    k = len(T)
    W1 = float(sum(m.w[j] for j in T)); W2 = float(sum(m.w[j] ** 2 for j in T))
    Fcur = m.F(k, W1, W2)
    hist = []
    moves = 0; nswap = 0; nadd = 0; ndel = 0
    imported = {}  # j -> number of imports
    events = []
    first_del = None
    while True:
        if cap is not None and moves >= cap:
            break
        x = m.centre_w(k, W1)
        g = m.gam(k)
        best = (0.0, None)
        # deletions of nulls: nearest to centre in xi units
        cand = []
        if len(ins):
            i = ins.bisect_left((x, -1))
            for ii in (i - 1, i, i + 1):
                if 0 <= ii < len(ins):
                    cand.append(ins[ii][1])
        for j in set(cand):
            Fn = m.F(k - 1, W1 - m.w[j], W2 - m.w[j] ** 2)
            if Fn - Fcur > best[0]:
                best = (Fn - Fcur, ('d', j, None))
        # truth deletions
        for j in range(s0):
            Fn = m.F(k - 1, W1 - m.w[j], W2 - m.w[j] ** 2)
            if Fn - Fcur > best[0]:
                best = (Fn - Fcur, ('D_truth', j, None))
        if len(out):
            ext = [out[0][1], out[-1][1]]
            if k < K:
                for l in ext:
                    Fn = m.F(k + 1, W1 + m.w[l], W2 + m.w[l] ** 2)
                    if Fn - Fcur > best[0]:
                        best = (Fn - Fcur, ('a', None, l))
            for l in ext:
                tl = m.xi[l] - x
                target = x + g * tl / (1 + g)
                cand = []
                if len(ins):
                    i = ins.bisect_left((target, -1))
                    for ii in (i - 1, i, i + 1):
                        if 0 <= ii < len(ins):
                            cand.append(ins[ii][1])
                for j in set(cand) | set(range(s0)):
                    Fn = m.F(k, W1 - m.w[j] + m.w[l], W2 - m.w[j] ** 2 + m.w[l] ** 2)
                    if Fn - Fcur > best[0]:
                        best = (Fn - Fcur, ('s' if j >= s0 else 'S_truth', j, l))
        if best[1] is None:
            break
        typ, j, l = best[1]
        if record:
            M = m.nu * m.n * m.d ** 2 / (m.alpha * m.psi(k, W1, W2))
            events.append((moves, typ, k, x, M, best[0], None if j is None else float(m.xi[j]), None if l is None else float(m.xi[l])))
        if typ in ('d', 'D_truth'):
            if typ == 'd':
                ins.remove((m.xi[j], j)); out.add((m.xi[j], j))
            W1 -= m.w[j]; W2 -= m.w[j] ** 2; k -= 1; ndel += 1
            if first_del is None:
                first_del = moves
        elif typ == 'a':
            out.remove((m.xi[l], l)); ins.add((m.xi[l], l)); W1 += m.w[l]; W2 += m.w[l] ** 2; k += 1; nadd += 1
            imported[l] = imported.get(l, 0) + 1
        else:
            if typ == 's':
                ins.remove((m.xi[j], j)); out.add((m.xi[j], j))
            out.remove((m.xi[l], l)); ins.add((m.xi[l], l))
            W1 += m.w[l] - m.w[j]; W2 += m.w[l] ** 2 - m.w[j] ** 2; nswap += 1
            imported[l] = imported.get(l, 0) + 1
        Fcur = m.F(k, W1, W2)
        moves += 1
        if typ in ('D_truth', 'S_truth'):
            break
        if moves % 2000 == 0:  # refresh sums
            idx = [j for _, j in ins] + list(range(s0))
            W1 = float(math.fsum(m.w[idx])); W2 = float(math.fsum(m.w[idx] ** 2)); Fcur = m.F(k, W1, W2)
    final_nulls = [j for _, j in ins]
    return dict(moves=moves, nswap=nswap, nadd=nadd, ndel=ndel, first_del=first_del, final_k=k,
                final_is_S0=(k == s0 and len(final_nulls) == 0), reimports=sum(v - 1 for v in imported.values() if v > 1),
                n_distinct_imports=len(imported), events=events)


if __name__ == '__main__':
    n = int(sys.argv[1]); c = float(sys.argv[2]); s0 = int(sys.argv[3]); seed = int(sys.argv[4])
    m = Model(n, c, s0, seed)
    res = run(m)
    ev = res.pop('events')
    print(json.dumps(res))
