r"""d1_diag.py -- W2-LOC2 diagnosis (falsification-first numerics, component port of the method).

Imports (does NOT edit) the ported method objects: C-GROW/numerics/bvs_core.py (score, prior, partition, start mode)
and W2-APP/numerics/n3b_fastls.py::ls_fast (LS0 search rule = bc.local_search, validated there).

Designs (raw rows iid N(0, Sigma), unit diagonal; y = X theta + eps on standardised X, sigma = 1; s0 = 3,
theta = (1, -0.8, 1.2)):
  G2E   2-D grid m x m (p = m^2), Sigma_jk = exp(-|x_j - x_k|_2 / phi), phi = 1.2      (d = 2, exponential decay)
  G2A   2-D grid, separable AR(1): rho^{|di|+|dj|}, rho = 0.6                           (d = 2, GMRF-type)
  TP15  Toeplitz gamma(h) = (1+h)^{-1.5}                                               (polynomial decay, alpha = 1.5)
  TP3   Toeplitz gamma(h) = (1+h)^{-3}                                                 (polynomial decay, alpha = 3)
  EBM   equicorrelated blocks, rho = 0.5, size g = ceil(3 log n), one truth per block  (middle regime)
Per run: start mode composition; LS0 path (cap ell_cap + |start|); along the path and over the lattice [S0, Q]
(Q := S0 u start u {l : dist(l, S0) <= R}) the add statistic h_{T,l} = (n-1)(RSS_T - RSS_{T+l})/RSS_T
(= Z^2_{T,l} up to 1 + o(1) for T containing S0), compared with 2 log p and the GROW L2.2 threshold proxy
c_n' = log(n+1) + 2 log p - 2 log(|Q|+1); lattice sup estimated by random T (200) + adversarial coordinate ascent
(5 restarts) for the 10 worst l; TL margin along the path (min truth-deletion loss in F).
Output: d1_results.csv, d1_out.txt."""
import sys, os, time, csv, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-APP/numerics"
sys.path.insert(0, APP)
from n0_common import bc, np            # noqa: E402  (bc = C-GROW bvs_core)
from n3b_fastls import ls_fast          # noqa: E402
from multiprocessing import Pool

BASE = 20261110
THETA = np.array([1.0, -0.8, 1.2])
DIDS = {"G2E": 1, "G2A": 2, "TP15": 3, "TP3": 4, "EBM": 5}


def grid_xy(m):
    i = np.arange(m * m)
    return np.stack([i // m, i % m], axis=1).astype(float)


def design(did, n, p):
    """Sigma, positions (for distances), truth indices, metric description"""
    if did in ("G2E", "G2A"):
        m = int(round(math.sqrt(p)))
        assert m * m == p
        xy = grid_xy(m)
        D2 = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
        D1 = np.abs(xy[:, None, :] - xy[None, :, :]).sum(-1)
        S = np.exp(-D2 / 1.2) if did == "G2E" else 0.6 ** D1
        f = [(0.2, 0.2), (0.5, 0.75), (0.78, 0.25)]
        S0 = tuple(sorted(int(round(a * (m - 1))) * m + int(round(b * (m - 1))) for a, b in f))
        dist = np.abs(xy[:, None, :] - xy[None, :, :]).max(-1)       # l_inf grid distance
        return S, S0, dist
    i = np.arange(p)
    H = np.abs(i[:, None] - i[None, :]).astype(float)
    if did == "TP15":
        return (1 + H) ** -1.5, tuple(int(round(p * f)) for f in (0.15, 0.5, 0.85)), H
    if did == "TP3":
        return (1 + H) ** -3.0, tuple(int(round(p * f)) for f in (0.15, 0.5, 0.85)), H
    if did == "EBM":
        g = int(math.ceil(3 * math.log(n)))
        S = np.eye(p)
        gid = np.full(p, -1)
        s, b = 0, 0
        while s < p:
            e = min(p, s + g)
            S[s:e, s:e] = 0.5 * np.eye(e - s) + 0.5
            gid[s:e] = b
            s, b = e, b + 1
        nb = b
        blocks = [int(round(x)) for x in np.linspace(1, nb - 2, 3)]
        S0 = tuple(sorted(int(np.flatnonzero(gid == bb)[g // 2]) for bb in blocks))
        dist = np.where(gid[:, None] == gid[None, :], 0.0, 99.0)
        return S, S0, dist
    raise ValueError(did)


class Stat:
    """add statistics from the standardised Gram (exact algebra)."""

    def __init__(self, X, y):
        self.n = X.shape[0]
        self.G = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)

    def h_all(self, T):
        """h_{T,l} for all l (np.nan for l in T); RSS_T."""
        T = np.asarray(sorted(T), dtype=np.int64)
        G, z = self.G, self.z
        if len(T) == 0:
            d = np.diag(G).copy(); c = z.copy(); rss = self.yy
        else:
            L = np.linalg.cholesky(G[np.ix_(T, T)])
            A = np.linalg.solve(L, G[T, :])          # |T| x p
            b = np.linalg.solve(L, z[T])
            d = np.diag(G) - (A ** 2).sum(0)
            c = z - A.T @ b
            rss = self.yy - float(b @ b)
        gain = c ** 2 / np.maximum(d, 1e-300)
        h = (self.n - 1) * gain / rss
        if len(T):
            h[T] = np.nan
        return h

    def h_one(self, T, l):
        T = list(T)
        if not T:
            return (self.n - 1) * self.z[l] ** 2 / self.G[l, l] / self.yy
        Ti = np.array(T)
        Gi = self.G[np.ix_(Ti, Ti)]
        sol = np.linalg.solve(Gi, np.stack([self.G[Ti, l], self.z[Ti]], 1))
        d = self.G[l, l] - self.G[l, Ti] @ sol[:, 0]
        c = self.z[l] - self.G[l, Ti] @ sol[:, 1]
        rss = self.yy - self.z[Ti] @ sol[:, 1]
        return (self.n - 1) * c * c / d / rss


def lattice_sup(st, S0, Qx, worst_l, rng, nrand=200, restarts=5):
    """estimate sup_{T in [S0, S0 u Qx]} max_l h_{T,l}: random T's (all l) + coordinate ascent for worst l."""
    S0 = list(S0)
    Qx = list(Qx)
    best = -1.0
    for _ in range(nrand):
        T = S0 + [v for v in Qx if rng.random() < 0.5]
        best = max(best, float(np.nanmax(st.h_all(T))))
    for l in worst_l:
        pool = [v for v in Qx if v != l]
        for r in range(restarts):
            inc = {v: (rng.random() < 0.5) for v in pool}
            T = S0 + [v for v in pool if inc[v]]
            cur = st.h_one(T, l)
            for sweep in range(3):
                improved = False
                for v in rng.permutation(pool):
                    inc[v] = not inc[v]
                    T2 = S0 + [u for u in pool if inc[u]]
                    val = st.h_one(T2, l)
                    if val > cur + 1e-12:
                        cur = val; improved = True
                    else:
                        inc[v] = not inc[v]
                if not improved:
                    break
            best = max(best, cur)
    return best


def job(args):
    did, n, p, seed = args
    t0 = time.time()
    rng = np.random.default_rng(np.random.SeedSequence([BASE, DIDS[did], n, p, seed]))
    S, S0, dist = design(did, n, p)
    theta = np.zeros(p); theta[list(S0)] = THETA
    Wr = bc.iid_design_raw(S, n, rng)
    X = bc.standardize_X(Wr)
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    mode = tuple(info.mode)
    ell = bc.ell_cap(n, p) + len(mode)
    res = ls_fast(prob, mode, ell, tmax=1500.0)
    path = res["path"]
    extras = sorted(set(mode) - set(S0))
    dS0 = dist[:, list(S0)].min(1)
    st = Stat(X, y)
    # path NA / TL
    path_max_h, path_argmax = [], []
    tl_min = np.inf
    all_dels = True
    for t, T in enumerate(path):
        if set(S0) <= set(T):
            h = st.h_all(T)
            path_max_h.append(float(np.nanmax(h)))
            path_argmax.append(int(np.nanargmax(h)))
            FT = prob.F(T)
            for i in S0:
                Tm = tuple(v for v in T if v != i)
                tl_min = min(tl_min, FT - prob.F(Tm))
        if t > 0:
            dset = set(path[t - 1]) - set(T)
            if not (len(T) == len(path[t - 1]) - 1 and dset and dset.pop() not in S0):
                all_dels = False
    # lattice Q: S0 u extras u radius-R neighbourhood (R = max extra distance + 1, at least 2)
    R = (max(dS0[extras]) if extras else 0) + 1
    R = max(R, 2)
    Qx = sorted(set(np.flatnonzero(dS0 <= R).tolist()) - set(S0))
    if len(Qx) > 60:      # keep lattice search tractable: keep the 60 nearest
        Qx = sorted(Qx, key=lambda v: (dS0[v], v))[:60]
    Qx = sorted(set(Qx) | set(extras))
    hS0 = st.h_all(list(S0))
    worst = list(np.argsort(-np.nan_to_num(hS0, nan=-1))[:10])
    worst += [path_argmax[t] for t in range(len(path_argmax))]
    worst = list(dict.fromkeys(int(v) for v in worst))[:15]
    lsup = lattice_sup(st, S0, Qx, worst, rng)
    q = len(set(S0) | set(Qx))
    cv = S @ theta / math.sqrt(theta @ S @ theta + 1.0)
    vis = int(sum(1 for l in range(p) if l not in S0 and n * cv[l] ** 2 >= math.log(n)))
    cn = math.log(n + 1) + 2 * math.log(p) - 2 * math.log(q + 1)
    out = dict(design=did, n=n, p=p, seed=seed, mode_size=len(mode), n_extra=len(extras),
               S0_in_mode=set(S0) <= set(mode), max_extra_dist=(float(max(dS0[extras])) if extras else -1),
               extras_by_dist=json.dumps({str(int(k)): int(c) for k, c in zip(*np.unique(dS0[extras], return_counts=True))}) if extras else "{}",
               ls_moves=res["moves"], ls_all_extra_deletions=all_dels, ls_final_eq_S0=(res["final"] == S0),
               ls_certified=res["certified"], ls_limit=res["local_limit"], ls_timeout=res["timed_out"],
               path_max_h=max(path_max_h) if path_max_h else float("nan"),
               h_at_S0=float(np.nanmax(hS0)), lattice_sup_h=lsup, q=q, two_log_p=2 * math.log(p), c_n=cn,
               tl_min=tl_min, vis_marg=vis, secs=round(time.time() - t0, 1))
    return out


if __name__ == "__main__":
    cfgs = []
    for did, p in (("G2E", 400), ("G2A", 400), ("TP15", 400), ("TP3", 400), ("EBM", 400)):
        for n in (800, 3200, 12800):
            for seed in (1, 2, 3, 4):
                cfgs.append((did, n, p, seed))
        for seed in (1, 2):
            cfgs.append((did, 51200, p, seed))
    for seed in (1, 2):
        cfgs.append(("G2E", 12800, 900, seed))
        cfgs.append(("G2A", 12800, 900, seed))
    with Pool(6) as pool:
        rows = []
        with open(os.path.join(HERE, "d1_out.txt"), "w") as fo:
            for r in pool.imap_unordered(job, cfgs):
                rows.append(r)
                line = " ".join("%s=%s" % (k, (round(v, 2) if isinstance(v, float) else v)) for k, v in r.items())
                print(line, flush=True)
                fo.write(line + "\n"); fo.flush()
    rows.sort(key=lambda r: (r["design"], r["p"], r["n"], r["seed"]))
    with open(os.path.join(HERE, "d1_results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
