# Copied verbatim from theory/W1-T37R:theory_campaign/W1-T37R/scripts/td_core.py (scorer, generator port).
"""Core objects for W1-T37R (Python reimplementation; R not available).

Target (00_COMMON.md §1): standardised X (||x_j||^2 = n-1), y (||y||^2 = n-1);
  G_S = X_S'X_S, z_S = X_S'y, H_S = (n+1)G_S + I, D_S = det H_S / det(G_S + I),
  Q_S = y'y - n z_S' H_S^{-1} z_S, nu = a0 + n/2,
  log m(S) = log C_n - 1/2 log D_S - nu log(2 b0 + Q_S),
  F(S) = log w(|S|) - log W_K + log m(S), w(k) = 1/2 / C(2p-1, k), K = min(p, floor(n/2)).
`p_prior` lets the size prior use a different p (penalty-matched small designs; flagged wherever used).

Local search (METHODOLOGY_v3 §6.10; engine v3_core.cpp: started from the global best led.hpmS):
scan every feasible flip and swap of the centre, move to the best strict improvement, <= ell moves,
then one further scan; local_certified iff the returned centre has no improving neighbour.
"""
import numpy as np
from math import lgamma, log, ceil, log2

A0 = B0 = 0.01


def lchoose(a, k):
    return lgamma(a + 1) - lgamma(k + 1) - lgamma(a - k + 1)


# ----------------------------------------------------------------------------- data
def scenario_covariance(scenario, p):
    """Verbatim port of gen_dev_data.R::scenario_covariance."""
    group = np.ceil(np.arange(1, p + 1) / 5).astype(int)
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if scenario == 1:
        return I
    if scenario == 2:
        idx = np.arange(p)
        return 0.5 ** np.abs(idx[:, None] - idx[None, :])
    if scenario == 3:
        return 0.7 * H + 0.3 * I
    if scenario == 4:
        return 0.85 * H + 0.15 * I
    if scenario == 5:
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if scenario == 6:
        rho = 0.4 + 0.1 * ((group - 1) % 6)
        # R: H * matrix(rho, p, p) fills column-wise => entry (i,j) = rho[i] (= rho[j] within a group)
        S = H * rho[:, None]
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError(scenario)


def truth(p, s0=None, step=None):
    """Port of gen_dev_data.R::truth; for small p choose s0/step explicitly (0-based indices returned)."""
    table = {30: (5, 1), 500: (14, 7), 1000: (14, 13)}
    if s0 is None:
        s0, step = table[p]
    pos = [3, 2, 4, 1, 5, 3]
    pattern = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0)
    block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k])
    beta = np.array([pattern[i % 6] for i in k])
    return active - 1, beta


def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0)
    X = X / X.std(0, ddof=1)
    y = yr - yr.mean()
    y = y / y.std(ddof=1)
    return X, y


def make_dataset(p, scenario, c, n=200, seed=0, s0=None, step=None):
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(scenario_covariance(scenario, p))
    Xr = rng.standard_normal((n, p)) @ L.T
    Xs = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)   # generator scales X before forming the signal
    act, b = truth(p, s0, step)
    beta = np.zeros(p); beta[act] = b
    eps = rng.standard_normal(n)
    yr = c * (Xs @ beta) + eps
    X, y = standardise(Xs, yr)
    return X, y, np.sort(act), beta


# ----------------------------------------------------------------------------- scorer
class Scorer:
    def __init__(self, X, y, p_prior=None):
        self.X, self.y = X, y
        self.n, self.p = X.shape
        n, p = self.n, self.p
        self.K = min(p, n // 2)
        self.G = X.T @ X
        self.z = X.T @ y
        self.yty = float(y @ y)
        self.nu = A0 + n / 2.0
        self.logCn = A0 * log(2 * B0) + lgamma(A0 + n / 2) - (n / 2) * log(np.pi) - lgamma(A0)
        pp = p if p_prior is None else p_prior
        self.p_prior = pp
        Kp = min(pp, n // 2)
        logw = np.array([-log(2) - lchoose(2.0 * pp - 1, k) for k in range(Kp + 1)])
        terms = np.array([lchoose(pp, k) for k in range(Kp + 1)]) + logw
        mx = terms.max()
        self.logWK = mx + log(np.exp(terms - mx).sum())
        self.logprior = logw - self.logWK
        self.ell = ceil(log2(n + p + 1))
        self.cache = {}

    def F_batch(self, idx):
        """idx: (N, k) int array of distinct indices per row (k >= 0). Returns F for each row."""
        idx = np.asarray(idx, dtype=int)
        N, k = idx.shape
        n = self.n
        if k == 0:
            logm = self.logCn - self.nu * np.log(2 * B0 + self.yty)
            return np.full(N, logm + self.logprior[0])
        Gs = self.G[idx[:, :, None], idx[:, None, :]]
        zs = self.z[idx]
        I = np.eye(k)
        H = (n + 1) * Gs + I
        A = Gs + I
        LH = np.linalg.cholesky(H)
        LA = np.linalg.cholesky(A)
        ldH = 2 * np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(1)
        ldA = 2 * np.log(np.diagonal(LA, axis1=1, axis2=2)).sum(1)
        w = np.linalg.solve(LH, zs[:, :, None])[:, :, 0]
        Q = self.yty - n * (w * w).sum(1)
        logm = self.logCn - 0.5 * (ldH - ldA) - self.nu * np.log(2 * B0 + Q)
        return logm + self.logprior[k]

    def F(self, S):
        key = tuple(sorted(S))
        v = self.cache.get(key)
        if v is None:
            v = float(self.F_batch(np.array([key], dtype=int).reshape(1, len(key)))[0])
            self.cache[key] = v
        return v

    # ------------------------------------------------------------- neighbourhood
    def neighbours(self, S):
        """All feasible flips and swaps of S. Returns list of (kind, out, in, sorted tuple)."""
        S = tuple(sorted(S))
        Sset = set(S)
        out = [j for j in range(self.p) if j not in Sset]
        moves = []
        if len(S) < self.K:
            for j in out:
                moves.append(("add", None, j, tuple(sorted(S + (j,)))))
        for i in S:
            moves.append(("del", i, None, tuple(x for x in S if x != i)))
        for i in S:
            rest = tuple(x for x in S if x != i)
            for j in out:
                moves.append(("swap", i, j, tuple(sorted(rest + (j,)))))
        return moves

    def scan(self, S):
        """Score every neighbour of S. Returns (moves, gains) with gains = F(S') - F(S)."""
        moves = self.neighbours(S)
        F0 = self.F(S)
        gains = np.empty(len(moves))
        by_size = {}
        for t, m in enumerate(moves):
            by_size.setdefault(len(m[3]), []).append(t)
        for k, ts in by_size.items():
            arr = np.array([moves[t][3] for t in ts], dtype=int).reshape(len(ts), k)
            vals = self.F_batch(arr)
            for t, v in zip(ts, vals):
                gains[t] = v - F0
                self.cache[moves[t][3]] = float(v)
        return moves, gains

    def best_move(self, S):
        moves, gains = self.scan(S)
        if len(moves) == 0:
            return None, moves, gains
        mx = gains.max()
        if not mx > 0:
            return None, moves, gains
        # lexicographic tie rule on the resulting index set
        cands = [t for t in range(len(moves)) if gains[t] == mx]
        t = min(cands, key=lambda t: moves[t][3])
        return t, moves, gains

    def local_search(self, centre, ell=None, record=False):
        """Production local search. Returns dict(path, final, certified, limit, n_moves)."""
        ell = self.ell if ell is None else ell
        S = tuple(sorted(centre))
        path = [S]
        kinds = []
        for _ in range(ell):
            t, moves, gains = self.best_move(S)
            if t is None:
                return dict(path=path, kinds=kinds, final=S, certified=True, limit=False, n_moves=len(path) - 1)
            kinds.append(moves[t][:3])
            S = moves[t][3]
            path.append(S)
        t, moves, gains = self.best_move(S)   # the one further scan
        return dict(path=path, kinds=kinds, final=S, certified=(t is None), limit=(t is not None),
                    n_moves=len(path) - 1)


def classify(move, S0set):
    """Progress class of a move w.r.t. Phi = |S Delta S0|: returns (dm, de) changes in (#missing, #extras)."""
    kind, i, j = move[:3]
    dm = de = 0
    if j is not None:
        if j in S0set: dm -= 1
        else: de += 1
    if i is not None:
        if i in S0set: dm += 1
        else: de -= 1
    return dm, de


def move_label(move, S0set):
    dm, de = classify(move, S0set)
    kind = move[0]
    names = {("add", -1, 0): "add_truth", ("add", 0, 1): "add_null",
             ("del", 1, 0): "del_truth", ("del", 0, -1): "del_extra",
             ("swap", -1, -1): "swap_extra->truth", ("swap", 0, 0): "swap_neutral",
             ("swap", 1, 1): "swap_truth->null"}
    lab = names.get((kind, dm, de))
    if lab == "swap_neutral":
        i, j = move[1], move[2]
        lab = "swap_truth->truth" if i in S0set else "swap_null->null"
    return lab or f"{kind}{dm,de}"
