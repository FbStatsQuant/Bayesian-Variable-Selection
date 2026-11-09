"""W3-SAMP numerics: an exact implementation of T12's frozen island (STATEMENT §1-§2 of
Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md) on a small state space, vectorised over many
independent islands. Used for the falsification / boundary-violation checks of W3-SAMP (Lemma ST, Theorem LT#,
Theorem C, Theorem D).

The kernels are those of T12 §1 for arbitrary positive gamma_0 and d (the identities need nothing else):
Gibbs coordinate j (pre-draw recording o_j), uniform swap, B copies of the neighbour swap (ring graph), independence
proposal from pi_0. A round applies the m = p + B + 2 labels in a uniformly random order. Stage 0: N iid pi_0 draws;
stage t: weights exp((phi_t - phi_{t-1}) d), log-increment, multinomial resampling, one round at phi_t; then L rounds
at phi = 1 and 4 measured rounds at phi = 1 with RB recording.

Run with Python >= 3.10 and numpy.
"""
import itertools
import numpy as np


class Model:
    def __init__(self, p, K, lg0, d, B=1, S0=None):
        self.p, self.K, self.B = p, K, B
        self.states = [s for s in range(1 << p) if bin(s).count("1") <= K]
        self.idx = {s: i for i, s in enumerate(self.states)}
        self.n = len(self.states)
        self.size = np.array([bin(s).count("1") for s in self.states])
        self.lg0 = np.asarray(lg0, float)
        self.d = np.asarray(d, float)
        self.pi0 = np.exp(self.lg0 - self.lg0.max()); self.pi0 /= self.pi0.sum()
        self.cum0 = np.cumsum(self.pi0); self.cum0[-1] = 1.0
        l1 = self.lg0 + self.d
        self.pi = np.exp(l1 - l1.max()); self.pi /= self.pi.sum()
        # Z_phi / Z_0 (normalisers relative to gamma_0's), used for W = Zhat / Z
        self.S0 = self.idx[S0] if S0 is not None else int(np.argmax(self.pi))
        self.nb = [[(j - 1) % p, (j + 1) % p] for j in range(p)]  # ring neighbour graph (symmetric)
        self.m = p + B + 2
        # Gibbs tables
        self.plus = np.zeros((p, self.n), int); self.minus = np.zeros((p, self.n), int); self.capped = np.zeros((p, self.n), bool)
        for j in range(p):
            for i, s in enumerate(self.states):
                sp, sm = s | (1 << j), s & ~(1 << j)
                self.minus[j, i] = self.idx[sm]
                if bin(sp).count("1") > K: self.capped[j, i] = True; self.plus[j, i] = i
                else: self.plus[j, i] = self.idx[sp]
        self._cache = {}

    def logZratio(self, phi):  # log(Zbar_phi / Zbar_0)
        a = self.lg0 + phi * self.d
        b = self.lg0
        return (a.max() + np.log(np.exp(a - a.max()).sum())) - (b.max() + np.log(np.exp(b - b.max()).sum()))

    def q(self, phi):
        a = self.lg0 + phi * self.d; w = np.exp(a - a.max()); return w / w.sum()

    def oj(self, phi):
        lg = self.lg0 + phi * self.d
        lp = lg[self.plus]; lm = lg[self.minus]
        o = 1.0 / (1.0 + np.exp(lm - lp))
        o[self.capped] = 0.0
        return o  # shape (p, n): o_j(S, phi)

    def kernels(self, phi):
        """Exact transition matrices of every label at phi (rows = from)."""
        if phi in self._cache: return self._cache[phi]
        n, p = self.n, self.p
        lg = self.lg0 + phi * self.d
        o = self.oj(phi)
        Ks = []
        for j in range(p):
            Kj = np.zeros((n, n))
            for i in range(n):
                Kj[i, self.plus[j, i]] += o[j, i]
                Kj[i, self.minus[j, i]] += 1 - o[j, i]
            Ks.append(Kj)
        # uniform swap
        U = np.zeros((n, n))
        for i, s in enumerate(self.states):
            k = self.size[i]
            if k == 0 or k == p: U[i, i] = 1; continue
            ins = [j for j in range(p) if s >> j & 1]; outs = [l for l in range(p) if not s >> l & 1]
            for j in ins:
                for l in outs:
                    t = self.idx[(s & ~(1 << j)) | (1 << l)]
                    a = min(1.0, np.exp(lg[t] - lg[i])) / (len(ins) * len(outs))
                    U[i, t] += a; U[i, i] += 1 / (len(ins) * len(outs)) - a
        Ks.append(U)
        # neighbour swap (B identical copies)
        Nm = np.zeros((n, n))
        for i, s in enumerate(self.states):
            ins = [j for j in range(p) if s >> j & 1]
            if not ins: Nm[i, i] = 1; continue
            for j in ins:
                cand = [l for l in self.nb[j] if not s >> l & 1]
                if not cand: Nm[i, i] += 1 / len(ins); continue
                for l in cand:
                    sp = (s & ~(1 << j)) | (1 << l); t = self.idx[sp]
                    back = len([x for x in self.nb[l] if not sp >> x & 1])
                    a = min(1.0, np.exp(lg[t] - lg[i]) * len(cand) / back) / (len(ins) * len(cand))
                    Nm[i, t] += a; Nm[i, i] += 1 / (len(ins) * len(cand)) - a
        for _ in range(self.B): Ks.append(Nm)
        # independence
        I = np.zeros((n, n))
        for i in range(n):
            a = self.pi0 * np.minimum(1.0, np.exp(phi * (self.d - self.d[i])))
            I[i] = a; I[i, i] += 1 - a.sum()
        Ks.append(I)
        cums = [np.cumsum(K, axis=1) for K in Ks]
        for c in cums: c[:, -1] = 1.0
        self._cache[phi] = (Ks, cums, o)
        return self._cache[phi]


def run_islands(M, grid, N, L, I, rng, Hm=4):
    """Simulate I independent islands. Returns dict of per-island arrays."""
    p, n, m = M.p, M.n, M.m
    T = len(grid) - 1
    X = np.searchsorted(M.cum0, rng.random((I, N)), side="right")  # iid pi_0
    X = np.minimum(X, n - 1)
    draws_hit = (X == M.S0).sum(axis=1)  # number of pi_0 draws equal to S0
    logW = np.zeros(I)  # log(Zhat_t / Z_0)
    Abr = [(X == M.S0).mean(axis=1)]
    Wstage = [np.ones(I)]
    rows = np.arange(I)[:, None]

    def one_round(X, phi, rb=None):
        nonlocal draws_hit
        Ks, cums, o = M.kernels(phi)
        order = np.argsort(rng.random((I, N, m)), axis=2)  # uniform random permutation per particle
        away = np.zeros((I, N), bool); start = X.copy()
        for k in range(m):
            lab = order[:, :, k]
            u = rng.random((I, N))
            newX = X.copy()
            for l in range(m):
                sel = lab == l
                if not sel.any(): continue
                xs = X[sel]
                if l < p:  # Gibbs, with pre-draw recording
                    if rb is not None:
                        np.add.at(rb[:, l], np.nonzero(sel)[0], o[l, xs])
                    newX[sel] = np.where(u[sel] < o[l, xs], M.plus[l, xs], M.minus[l, xs])
                elif l == m - 1:  # independence: explicit proposal, then accept
                    prop = np.minimum(np.searchsorted(M.cum0, rng.random(xs.size), side="right"), n - 1)
                    np.add.at(draws_hit, np.nonzero(sel)[0], (prop == M.S0).astype(int))
                    acc = u[sel] < np.minimum(1.0, np.exp(phi * (M.d[prop] - M.d[xs])))
                    newX[sel] = np.where(acc, prop, xs)
                else:
                    c = cums[l][xs]
                    newX[sel] = np.minimum((c < u[sel][:, None]).sum(axis=1), n - 1)
            X = newX
            away |= (start == M.S0) & (X != M.S0)
        return X, away

    phi_prev = grid[0]
    for t in range(1, T + 1):
        phi = grid[t]; lw = (phi - phi_prev) * M.d[X]
        mx = lw.max(axis=1, keepdims=True); w = np.exp(lw - mx)
        logW += np.log(w.mean(axis=1)) + mx[:, 0]
        c = np.cumsum(w, axis=1); c /= c[:, -1:]; c[:, -1] = 1.0
        u = rng.random((I, N))
        anc = np.minimum((c[:, None, :] < u[:, :, None]).sum(axis=2), N - 1)
        X = X[rows, anc]
        X, _ = one_round(X, phi)
        Abr.append((X == M.S0).mean(axis=1))
        Wstage.append(np.exp(logW - M.logZratio(phi)))
        phi_prev = phi
    W = np.exp(logW - M.logZratio(1.0))
    for _ in range(L):
        X, _ = one_round(X, 1.0)
    A = [(X == M.S0).mean(axis=1)]
    rb = np.zeros((I, p)); Lam = []; ends = []
    for q in range(Hm):
        X, away = one_round(X, 1.0, rb)
        Lam.append(away.mean(axis=1)); A.append((X == M.S0).mean(axis=1)); ends.append(X.copy())
    rb /= (N * Hm)
    return dict(W=W, Abr=np.array(Abr).T, Wstage=np.array(Wstage).T, A=np.array(A).T, rb=rb,
                Lam=np.array(Lam).T, draws_hit=draws_hit, ends=ends, D=N * (1 + T + L + Hm))


def exact_quantities(M):
    o = M.oj(1.0)
    S0s = M.states[M.S0]
    ind = np.array([(S0s >> j) & 1 for j in range(M.p)])
    kap_vec = np.abs(o[:, M.S0] - ind)
    Ks, _, _ = M.kernels(1.0)
    leave = [1 - K[M.S0, M.S0] for K in Ks]
    delta = 1 - M.pi[M.S0]; o1 = delta / (1 - delta)
    delta0 = 1 - M.pi0[M.S0]; o0 = delta0 / (1 - delta0)
    pip = np.array([M.pi[[i for i, s in enumerate(M.states) if s >> j & 1]].sum() for j in range(M.p)])
    inv = max(np.abs(M.pi @ K - M.pi).max() for K in Ks)
    return dict(kappa_vec=kap_vec, kappa0=kap_vec.max(), kappa_sum=kap_vec.sum(), leave=np.array(leave),
                lambda0=sum(leave), delta=delta, o1=o1, o0=o0, dbar=max(o0, o1), ind=ind, pip=pip, inv_err=inv)
