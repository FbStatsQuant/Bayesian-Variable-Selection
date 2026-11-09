"""fac_common.py -- W2-FAC-A diagnostics: factor / equicorrelated designs, start mode, fast exact LS0.

Score, prior, partition, block tables and start mode: bvs_core.py (copied unchanged from
Theory_work/Wave1C/C-GROW/numerics/bvs_core.py; sources SoP 04_theory.tex 69-74, 02_method.tex 180-250, 459-510).
The local search here is a FAST re-implementation of M 6.10 (bvs_core.local_search semantics: scan all feasible
additions (|S|<K), deletions, swaps; move to the best scanned neighbour iff strictly better; exact float ties ->
lexicographically smallest sorted tuple; at most `cap` moves, then one further scan).  Scores of all neighbours are
computed exactly (same formula as bvs_core.Problem.logm_idx) by Schur-complement up/down-dates; cross-checked
against bvs_core.Problem.F in selftest().
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import math, json, time
import numpy as np
import bvs_core as bc

BIG = 10 ** 6

# ------------------------------------------------------------------------------------------------
# designs
# ------------------------------------------------------------------------------------------------
POS = (3, 2, 4, 1, 5, 3)
PATTERN = (1.4, -1.0, 1.8, -1.2, 0.8, -1.6)


def study_truth(s0, step):
    k = np.arange(s0)
    block = 1 + step * k
    pos = np.array([POS[i % 6] for i in k])
    active = 5 * (block - 1) + pos
    beta = np.array([PATTERN[i % 6] for i in k])
    return active - 1, beta


def sigma_of(design, p):
    """design names:
       S5   : 0.3*11' + 0.4*H + 0.3*I  (groups of 5)  -- study scenario 5
       CS3  : 0.3*11' + 0.7*I                          -- compound symmetry, one factor, a = 0.3
       CS5  : 0.5*11' + 0.5*I                          -- compound symmetry, a = 0.5
       F2   : two-factor model, loadings lam_j1 = 0.55, lam_j2 = 0.45*(-1)^j, Psi = 1 - |lam_j|^2
       F2r  : two-factor model, random loadings (fixed seed 4242) lam_j1 ~ U(.3,.7), lam_j2 ~ U(-.5,.5)
    """
    idx = np.arange(1, p + 1)
    I = np.eye(p)
    if design == "S5":
        group = np.ceil(idx / 5).astype(int)
        H = (group[:, None] == group[None, :]).astype(float)
        return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    if design == "CS3":
        return 0.3 * np.ones((p, p)) + 0.7 * I
    if design == "CS5":
        return 0.5 * np.ones((p, p)) + 0.5 * I
    if design in ("F2", "F2r"):
        if design == "F2":
            L = np.column_stack([np.full(p, 0.55), 0.45 * (-1.0) ** idx])
        else:
            r = np.random.default_rng(4242)
            L = np.column_stack([r.uniform(.3, .7, size=p), r.uniform(-.5, .5, size=p)])
        S = L @ L.T
        np.fill_diagonal(S, 1.0)
        return S
    raise ValueError(design)


def build(design, p, n, c, seed, mode="iid", s0=4, step=5):
    Sigma = sigma_of(design, p)
    act, beta = study_truth(s0, step)
    assert act.max() < p
    th = np.zeros(p)
    th[act] = c * beta
    rng = np.random.default_rng(1000003 * seed + 7919 * n + 104729 * p + hash(design) % 9973 + (0 if mode == "iid" else 17))
    if mode == "iid":
        X = bc.standardize_X(bc.iid_design_raw(Sigma, n, rng))
    else:
        X = bc.exact_gram_design(Sigma, n, np.random.default_rng(555 + n + p))
    y = bc.make_y_std(X, th, 1.0, rng)
    return X, y, tuple(int(a) for a in sorted(act)), th


# ------------------------------------------------------------------------------------------------
# fast scorer for one centre and all its neighbours
# ------------------------------------------------------------------------------------------------
class Fast:
    def __init__(self, X, y, K=None):
        self.n, self.p = X.shape
        self.K = min(self.p, self.n // 2) if K is None else K
        self.XtX = X.T @ X
        self.Xty = X.T @ y
        self.yty = float(y @ y)
        self.nu = 0.01 + self.n / 2.0
        self.logw = bc.log_prior_w(self.p, self.K)
        self.diag = np.diag(self.XtX).copy()

    def _logm(self, ldH, ldA, q):
        Q = self.yty - self.n * q
        return -0.5 * (ldH - ldA) - self.nu * np.log(0.02 + Q)

    def F_of(self, S):
        S = list(S)
        k = len(S)
        if k == 0:
            return float(self.logw[0] + self._logm(0.0, 0.0, 0.0))
        G = self.XtX[np.ix_(S, S)]
        H = (self.n + 1.0) * G + np.eye(k)
        A = G + np.eye(k)
        z = self.Xty[S]
        ldH = np.linalg.slogdet(H)[1]
        ldA = np.linalg.slogdet(A)[1]
        q = float(z @ np.linalg.solve(H, z))
        return float(self.logw[k] + self._logm(ldH, ldA, q))

    def scan(self, T):
        """T sorted tuple. Returns F(T) and dict of arrays:
           dele: (k,) F(T - T[i]);  add: (m,) F(T + out[l]) (or None if |T|>=K);  swp: (k,m) F(T - T[i] + out[l])."""
        n, p = self.n, self.p
        T = list(T)
        k = len(T)
        Tset = set(T)
        out = np.array([j for j in range(p) if j not in Tset], dtype=np.int64)
        m = len(out)
        gl = self.diag[out]
        zl = self.Xty[out]
        res = {"out": out}
        if k == 0:
            FT = float(self.logw[0] + self._logm(0.0, 0.0, 0.0))
            sH = (n + 1.0) * gl + 1.0
            sA = gl + 1.0
            q = zl ** 2 / sH
            res["add"] = self.logw[1] + self._logm(np.log(sH), np.log(sA), q) if self.K >= 1 else None
            res["dele"] = np.zeros(0)
            res["swp"] = np.zeros((0, m))
            return FT, res
        Ta = np.array(T, dtype=np.int64)
        G = self.XtX[np.ix_(Ta, Ta)]
        H = (n + 1.0) * G + np.eye(k)
        A = G + np.eye(k)
        Hi = np.linalg.inv(H)
        Ai = np.linalg.inv(A)
        Hi = 0.5 * (Hi + Hi.T)
        Ai = 0.5 * (Ai + Ai.T)
        z = self.Xty[Ta]
        Hz = Hi @ z
        q = float(z @ Hz)
        ldH = np.linalg.slogdet(H)[1]
        ldA = np.linalg.slogdet(A)[1]
        FT = float(self.logw[k] + self._logm(ldH, ldA, q))
        dH = np.diag(Hi)
        dA = np.diag(Ai)
        # deletions
        ldH_i = ldH + np.log(dH)
        ldA_i = ldA + np.log(dA)
        q_i = q - Hz ** 2 / dH
        res["dele"] = self.logw[k - 1] + self._logm(ldH_i, ldA_i, q_i)
        if m == 0:
            res["add"] = None
            res["swp"] = np.zeros((k, 0))
            return FT, res
        bA = self.XtX[np.ix_(Ta, out)]          # k x m
        uH = Hi @ bA * (n + 1.0)                # Hi bH
        uA = Ai @ bA
        sH = (n + 1.0) * gl + 1.0 - (n + 1.0) * (bA * uH).sum(axis=0)
        sA = gl + 1.0 - (bA * uA).sum(axis=0)
        cr = zl - (n + 1.0) * (bA.T @ Hz)       # z_l - bH' Hi z
        if k < self.K:
            res["add"] = self.logw[k + 1] + self._logm(ldH + np.log(sH), ldA + np.log(sA), q + cr ** 2 / sH)
        else:
            res["add"] = None
        # swaps: i out, l in
        sH2 = sH[None, :] + uH ** 2 / dH[:, None]
        sA2 = sA[None, :] + uA ** 2 / dA[:, None]
        cr2 = cr[None, :] + uH * Hz[:, None] / dH[:, None]
        qq = q_i[:, None] + cr2 ** 2 / sH2
        res["swp"] = self.logw[k] + self._logm(ldH_i[:, None] + np.log(sH2), ldA_i[:, None] + np.log(sA2), qq)
        return FT, res


def _neigh_set(T, kind, i, l, out):
    T = list(T)
    if kind == "dele":
        S = T[:i] + T[i + 1:]
    elif kind == "add":
        S = sorted(T + [int(out[l])])
    else:
        S = sorted(T[:i] + T[i + 1:] + [int(out[l])])
    return tuple(S)


def best_neighbour(fs, T, res):
    """max F over scanned neighbours, ties -> lexicographically smallest tuple."""
    cands = []
    mx = -np.inf
    for kind in ("dele", "add", "swp"):
        a = res.get(kind)
        if a is None or a.size == 0:
            continue
        v = float(a.max())
        if v > mx:
            mx = v
    for kind in ("dele", "add", "swp"):
        a = res.get(kind)
        if a is None or a.size == 0:
            continue
        hits = np.argwhere(a == mx)
        for h in hits:
            if kind == "dele":
                cands.append(_neigh_set(T, kind, int(h[0]), None, res["out"]))
            elif kind == "add":
                cands.append(_neigh_set(T, kind, None, int(h[0]), res["out"]))
            else:
                cands.append(_neigh_set(T, kind, int(h[0]), int(h[1]), res["out"]))
    return mx, min(cands)


def move_token(a, b, S0):
    a, b = set(a), set(b)
    T = set(S0)
    if len(b) == len(a) + 1:
        return "+T" if next(iter(b - a)) in T else "+N"
    if len(b) == len(a) - 1:
        return "-T" if next(iter(a - b)) in T else "-N"
    o = next(iter(a - b)); i = next(iter(b - a))
    return "sw" + ("T" if o in T else "N") + ">" + ("T" if i in T else "N")


def path_diag(fs, T, FT, res, S0set):
    """At centre T (supposed to contain S0): gains (F(nb)-F(T)) of the best move in each class."""
    T = list(T)
    out = res["out"]
    isnullT = np.array([j not in S0set for j in T])
    istrueT = ~isnullT
    d = {}
    de = res["dele"] - FT
    d["g_delN"] = float(de[isnullT].max()) if isnullT.any() else -np.inf
    d["g_delT"] = float(de[istrueT].max()) if istrueT.any() else -np.inf
    if res.get("add") is not None and len(out):
        ad = res["add"] - FT
        isTo = np.array([j in S0set for j in out])
        d["g_addN"] = float(ad[~isTo].max()) if (~isTo).any() else -np.inf
        d["g_addT"] = float(ad[isTo].max()) if isTo.any() else -np.inf
    else:
        d["g_addN"] = d["g_addT"] = -np.inf
    sw = res["swp"] - FT
    if sw.size:
        d["g_swN"] = float(sw[isnullT, :].max()) if isnullT.any() else -np.inf
        d["g_swT"] = float(sw[istrueT, :].max()) if istrueT.any() else -np.inf
    else:
        d["g_swN"] = d["g_swT"] = -np.inf
    return d


def ls0(fs, centre, cap, S0, diag=True, maxmoves=BIG):
    """Production local search (M 6.10) from centre, cap moves, then one further scan.  Also traces diagnostics."""
    S0set = set(S0)
    S = tuple(sorted(centre))
    path = [S]
    toks = []
    moves = 0
    limit = False
    certified = False
    S0_scored = (S == tuple(S0))
    pd = []
    while True:
        FT, res = fs.scan(S)
        if diag and S0set <= set(S):
            dd = path_diag(fs, S, FT, res, S0set)
            dd["k"] = len(S)
            pd.append(dd)
        # is S0 a scanned neighbour of S?
        if not S0_scored and len(set(S) ^ S0set) <= 2 and (len(S) - len(S0set)) in (-1, 0, 1):
            a, b = set(S), S0set
            if (len(a) == len(b) + 1 and b <= a) or (len(b) == len(a) + 1 and a <= b and len(a) < fs.K) or (len(a) == len(b) and len(a - b) == 1):
                S0_scored = True
        mx, nxt = best_neighbour(fs, S, res)
        if mx > FT:
            if moves >= cap or moves >= maxmoves:
                limit = True
                break
            toks.append(move_token(S, nxt, S0))
            S = nxt
            moves += 1
            path.append(S)
            if S == tuple(S0):
                S0_scored = True
        else:
            certified = True
            break
    return dict(final=S, moves=moves, limit=limit, certified=certified, S0_scored=S0_scored, toks=toks,
                pathdiag=pd, path=path)


def selftest(seed=1):
    rng = np.random.default_rng(seed)
    n, p = 60, 12
    X, y, S0, th = build("CS3", p, n, 1.0, seed) if False else (None, None, None, None)
    Sigma = sigma_of("F2r", p)
    X = bc.standardize_X(bc.iid_design_raw(Sigma, n, rng))
    y = bc.standardize_y(X[:, :3] @ np.array([1., -1., .5]) + rng.standard_normal(n))
    prob = bc.Problem(X, y)
    fs = Fast(X, y)
    err = 0.0
    for T in [(), (0,), (0, 3, 7), (1, 2, 5, 8, 11), tuple(range(6))]:
        FT, res = fs.scan(T)
        err = max(err, abs(FT - prob.F(T)))
        out = res["out"]
        for i in range(len(T)):
            Sd = _neigh_set(T, "dele", i, None, out)
            err = max(err, abs(res["dele"][i] - prob.F(Sd)))
        if res.get("add") is not None:
            for l in range(len(out)):
                Sa = _neigh_set(T, "add", None, l, out)
                err = max(err, abs(res["add"][l] - prob.F(Sa)))
        for i in range(len(T)):
            for l in range(len(out)):
                Ss = _neigh_set(T, "swp", i, l, out)
                err = max(err, abs(res["swp"][i, l] - prob.F(Ss)))
    # local search equivalence
    for C in [(0, 3, 7, 9), tuple(range(p // 2))]:
        a = ls0(fs, C, 50, (0, 1, 2), diag=False)
        b = bc.local_search(prob, C, 50)
        assert a["final"] == b["final"] and a["moves"] == b["moves"], (a["final"], b["final"])
    return err


if __name__ == "__main__":
    print("max |F_fast - F_ref| =", selftest())
