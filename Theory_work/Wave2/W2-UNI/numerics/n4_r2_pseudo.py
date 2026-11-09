r"""n4_r2_pseudo.py -- W2-UNI falsification probe of the "R2 interface" of Theorem UNI-0 (STATEMENT §3(ii), §4 R2; proof
lemmas/L2_k0.md) on designs whose pseudometric has ZERO distances and SMALL POSITIVE distances (< 1).

THIS IS A FALSIFICATION PROBE: OBSERVATIONS ONLY, NOT A PROOF. All claims in UNI-0 are asymptotic; n in {500, 2000} here
(plus an n = 8000 supplementary run).  Nothing below is a certificate of any asymptotic statement.

Adapted (copied, not edited) from W2-LOC2/numerics/d1_diag.py. Imports (does NOT edit) the ported method objects:
C-GROW bvs_core via W2-APP/numerics/n0_common.py (score F, prior, partition, start mode, COMPLETE local search
bc.local_search) and, for a COMPARISON ONLY, W2-APP/numerics/n3b_fastls.py::ls_fast.

Designs (raw rows iid N(0, Sigma), unit diagonal; y = X theta + eps on standardised X, sigma = 1; s0 = 3,
theta = (1, -0.8, 1.2) on three truths placed far apart in distinct clusters, one of them inside a multi-index cluster
so that a zero-distance null neighbour exists). The layout (cluster sizes/gaps/jitter, truth positions) is re-drawn
per seed (layout rng separate from the data rng).  Layouts, seeds and data are IDENTICAL to the previous version.
  PC1 "clustered line": p = 300 sites on a line in clusters of 1-3 indices at mutual distance 0; gaps between consecutive
      clusters drawn uniformly from {0.3, 0.6, 1.5}; Sigma_jk = 0.5 exp(-delta_jk/phi), phi = 1.0 (j != k), diagonal 1.
  PC2 "2-D jittered clusters": cluster centres on a 14 x 14 grid (spacing 1) jittered by U(-0.45, 0.45) per coordinate
      (many centre distances < 1); clusters of 1-3 indices at distance 0 (first p indices filled); p = 300;
      Sigma_jk = 0.45 exp(-delta_jk/1.0) (j != k), diagonal 1 (delta = Euclidean distance; within cluster 0.45).
  (Both: Sigma = a K + (1 - a) I with K = exp(-delta) positive semidefinite, hence lambda_min >= 1 - a; computed lambda_min
  is reported, as are the mean per-site counts of neighbours with delta = 0 and with 0 < delta < 1.)
Grid of runs: n in {500, 2000}, 20 seeds per (design, n)  (2 designs x 2 n x 20 seeds = 80 runs); supplementary n = 8000
(20 seeds per design, 40 runs) via N4_NLIST="8000" N4_TAG="_n8000".

WHAT IS COMPUTED PER RUN (exact definitions)
(a) Start mode: composition vs the sandwich S0 <= start mode <= Q_R with Q_R := S0 u {l : min_{j in S0} delta(l, j) <= R};
    primary R = 2.0, also R = 1 and R = 3 reported (sand_R* := S0 <= mode AND mode <= Q_R).
(b) LS0, COMPLETE SEARCH (finding 5 of R05b): bc.local_search (C-GROW port), which scores EVERY feasible add / delete / swap
    at each visited centre, cap ell_cap(n,p) + |start|.  "LS0 ends at S0" (ls_final_eq_S0) and "certified" (ls_certified: the
    complete-neighbourhood scan found no improving move; ls_local_limit = move cap hit) are therefore complete-scan
    observations of the ported rule.  ALL runs (all n, both designs) use the complete search.
    The SCREENED search ls_fast (n3b_fastls.py; swap scores pre-screened with a 1e-5 window, its `certified` flag is NOT a
    complete-scan certificate) is ALSO run on the same data, labelled "screened-search endpoint" (scr_*), and compared with
    the complete endpoint (scr_final_eq_complete, scr_path_eq_complete).  Only the complete search feeds any "LS0" count.
(c) Add statistic h_{T,l} = (n-1)(RSS_T - RSS_{T+l})/RSS_T (l ranges over ALL indices not in T), compared with 2 log p and the
    GROW L2.2 threshold proxy c_n' = log(n+1) + 2 log p - 2 log(|Q_lat|+1).
    LATTICE sup (finding 7 of R05b): lattice_sup_h := sup over states T with S0 <= T <= Q_lat ONLY, Q_lat := S0 u start-mode
    extras u the <= 60 nearest nulls within R = 2 (a LOWER estimate): T = S0, T = Q_lat, 200 random T (each extra in with
    prob 1/2) and adversarial coordinate ascent over T (5 restarts, 3 sweeps) for the <= 15 worst l.  Path states are NEVER
    mixed into lattice_sup_h.  "lattice NA proxy fails" := lattice_sup_h > c_n' (na_fail_lat; also > 2 log p).
    PATH statistic (kept separate): path_max_h := max_l h over the complete-search path states T with S0 <= T (T need not
    be inside Q_lat); n_path_out_lattice counts those path states T not <= Q_lat; path_na_fail := path_max_h > c_n'.
(d) Direct NA check on the actual score: for the 40 highest-h lattice pairs (T, l) found above (T inside [S0, Q_lat]), the actual
    gain F(T u l) - F(T) is computed; "NA(F) fails" := max gain > 0.
(e) TL margins (finding 6 of R05b), using the ACTUAL score F, at sampled T with S0 <= T: the path states of the complete LS0
    (those containing S0), T = S0, T = Q_lat, and 40 random lattice points.  At each T:
      sampled truth-deletion margin := min_{i in S0} [F(T) - F(T \ {i})]                         (tl_del_*)
      sampled TL margin (deletions + swaps) := min over ALL feasible truth-losing neighbours A of F(T) - F(A), i.e. the
          deletions T \ {i} AND all swaps (T \ {i}) u {l}, i in S0, l not in T                   (tl_*)
    (sampled minima only -- NOT a proof of TL; TL is positive iff the margin > 0 at every T.)  tl_swap_binding := the swap
    margin is strictly below the deletion margin at some sampled T.  *_path / *_lat give the path / lattice-point parts.
Output: n4_r2_pseudo_results{TAG}.csv (per run), stdout; the aggregate counts/summary are generated PROGRAMMATICALLY from the
result CSV files (function summarize(), also `py -3.13 n4_r2_pseudo.py summarize`) and written to n4_r2_pseudo_summary.txt
(covers every n4_r2_pseudo_results*.csv that exists)."""
import sys, os, time, csv, json, math, glob
HERE = os.path.dirname(os.path.abspath(__file__))
APP = "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-APP/numerics"
sys.path.insert(0, APP)
from n0_common import bc, np            # noqa: E402  (bc = C-GROW bvs_core)
from n3b_fastls import ls_fast          # noqa: E402  (screened search: comparison only)
from multiprocessing import Pool

BASE = 20261112
THETA = np.array([1.0, -0.8, 1.2])
DIDS = {"PC1": 1, "PC2": 2}
R_MAIN = 2.0
R_ALT = (1.0, 3.0)
P = 300
NSEEDS = 20


# ------------------------------------------------------------------------------------------------ designs
def make_sizes(rng, p):
    sizes, tot = [], 0
    while tot < p:
        s = int(rng.choice([1, 2, 3], p=[0.4, 0.35, 0.25]))
        s = min(s, p - tot)
        sizes.append(s)
        tot += s
    return sizes


def pick_truths(cl_pos, sizes, targets, dist_fn):
    """cl_pos: cluster coordinates (nc x dim); targets: list of 3 target coordinates (same space).
    truth 0 forced into a cluster with size >= 2; the others nearest cluster (distinct)."""
    chosen = []
    for k, tgt in enumerate(targets):
        d = dist_fn(cl_pos, tgt)
        order = np.argsort(d)
        for c in order:
            if c in chosen:
                continue
            if k == 0 and sizes[c] < 2:
                continue
            chosen.append(int(c))
            break
    return chosen


def design(did, p, rng):
    """returns Sigma, S0 (sorted tuple), dist (p x p pseudometric), lam_min, frac0, frac01"""
    sizes = make_sizes(rng, p)
    nc = len(sizes)
    cid = np.repeat(np.arange(nc), sizes)                     # cluster id per index
    first = np.concatenate([[0], np.cumsum(sizes)[:-1]])
    if did == "PC1":
        gaps = rng.choice([0.3, 0.6, 1.5], size=nc - 1)
        cx = np.concatenate([[0.0], np.cumsum(gaps)])
        pos = cx[cid][:, None]
        L = cx[-1]
        tg = [np.array([f * L]) for f in (0.15, 0.5, 0.85)]
        ch = pick_truths(cx[:, None], sizes, tg, lambda a, t: np.abs(a[:, 0] - t[0]))
        off, phi = 0.5, 1.0
    elif did == "PC2":
        m = 14
        gx, gy = np.meshgrid(np.arange(m), np.arange(m), indexing="ij")
        cen = np.stack([gx.ravel(), gy.ravel()], 1).astype(float) + rng.uniform(-0.45, 0.45, size=(m * m, 2))
        assert nc <= m * m
        cen = cen[:nc]            # row-major fill of the first nc centres
        pos = cen[cid]
        # truth targets in the filled region (rows 0..ceil(nc/m)-1)
        rows = math.ceil(nc / m) - 1
        tg = [np.array([a * rows, b * (m - 1)]) for a, b in ((0.2, 0.2), (0.5, 0.75), (0.78, 0.25))]
        ch = pick_truths(cen, sizes, tg, lambda a, t: np.sqrt(((a - t) ** 2).sum(1)))
        off, phi = 0.45, 1.0
    else:
        raise ValueError(did)
    diff = pos[:, None, :] - pos[None, :, :]
    D = np.sqrt((diff ** 2).sum(-1))
    D[cid[:, None] == cid[None, :]] = 0.0                     # zero distance within a cluster (exact)
    Sg = off * np.exp(-D / phi)
    np.fill_diagonal(Sg, 1.0)
    lam_min = float(np.linalg.eigvalsh(Sg)[0])
    # truth indices: truth 0 = a non-first index of its (size>=2) cluster; others = first index of cluster
    S0 = []
    for k, c in enumerate(ch):
        idx = int(first[c]) + (1 if k == 0 else 0)
        S0.append(idx)
    S0 = tuple(sorted(S0))
    iu = np.triu_indices(p, 1)
    dd = D[iu]
    return Sg, S0, D, lam_min, float((dd == 0).mean()), float(((dd > 0) & (dd < 1)).mean()), \
        float(np.min(D[np.ix_(S0, S0)] + np.eye(3) * 1e9))


class Stat:
    """add statistics from the standardised Gram (exact algebra)."""

    def __init__(self, X, y):
        self.n = X.shape[0]
        self.G = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)

    def h_all(self, T):
        T = np.asarray(sorted(T), dtype=np.int64)
        G, z = self.G, self.z
        if len(T) == 0:
            d = np.diag(G).copy(); c = z.copy(); rss = self.yy
        else:
            L = np.linalg.cholesky(G[np.ix_(T, T)])
            A = np.linalg.solve(L, G[T, :])
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
    """sup of max_l h_{T,l} over T with S0 <= T <= S0 u Qx ONLY (every T generated here is S0 + a subset of Qx; l is any
    index not in T).  Returns (best, cands) with cands = (h, T, l) lattice pairs for the direct F-gain check."""
    S0 = list(S0)
    Qx = list(Qx)
    best = -1.0
    cands = []          # (h, T, l) candidates for the direct F-gain check
    fixed = [list(S0), list(S0) + Qx]      # deterministic extreme lattice points (no rng use)
    for _ in range(nrand):
        fixed.append(S0 + [v for v in Qx if rng.random() < 0.5])
    for T in fixed:
        hh = st.h_all(T)
        l_ = int(np.nanargmax(hh))
        cands.append((float(hh[l_]), tuple(sorted(T)), l_))
        best = max(best, float(np.nanmax(hh)))
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
            cands.append((cur, tuple(sorted(S0 + [u for u in pool if inc[u]])), int(l)))
    return best, cands


def tl_margins(prob, S0, T, p):
    """T contains S0.  Returns (sampled truth-deletion margin, sampled TL margin over deletions + truth-removing swaps) at T,
    both with the actual score F:
      del  = min_{i in S0} F(T) - F(T \\ i)
      full = min over deletions AND swaps (T \\ i) u {l}, i in S0, l not in T, of F(T) - F(A)."""
    T = tuple(sorted(T))
    Tset = set(T)
    FT = prob.F(T)
    outs = [l for l in range(p) if l not in Tset]
    dels, sws = [], []
    for i in S0:
        base = tuple(v for v in T if v != i)
        dels.append(base)
        for l in outs:
            sws.append(tuple(sorted(base + (l,))))
    Fd = np.asarray(prob.F_many(dels))
    Fs = np.asarray(prob.F_many(sws)) if sws else np.array([-np.inf])
    return float(FT - Fd.max()), float(FT - max(Fd.max(), Fs.max()))


def job(args):
    did, n, p, seed = args
    t0 = time.time()
    lrng = np.random.default_rng(np.random.SeedSequence([BASE, 77, DIDS[did], seed]))     # layout rng (n-independent)
    S, S0, dist, lam_min, f0, f01, min_truth_d = design(did, p, lrng)
    nb0 = float(((dist == 0).sum(1) - 1).mean()); nb01 = float(((dist > 0) & (dist < 1)).sum(1).mean())   # mean per-site counts
    rng = np.random.default_rng(np.random.SeedSequence([BASE, DIDS[did], n, p, seed]))
    theta = np.zeros(p); theta[list(S0)] = THETA
    Wr = bc.iid_design_raw(S, n, rng)
    X = bc.standardize_X(Wr)
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    mode = tuple(info.mode)
    ell = bc.ell_cap(n, p) + len(mode)
    t_ls0 = time.time()
    res = bc.local_search(prob, mode, ell)                    # COMPLETE search (production rule)
    t_complete = time.time() - t_ls0
    t_ls0 = time.time()
    scr = ls_fast(prob, mode, ell, tmax=1500.0)               # SCREENED search, comparison only
    t_screened = time.time() - t_ls0
    path = res["path"]
    extras = sorted(set(mode) - set(S0))
    dS0 = dist[:, list(S0)].min(1)
    st = Stat(X, y)
    S0set = set(S0)
    # lattice [S0, Q_lat]
    sand = {}
    for R in (R_MAIN,) + R_ALT:
        QR = S0set | set(np.flatnonzero(dS0 <= R).tolist())
        sand[R] = (S0set <= set(mode), set(mode) <= QR, len(QR))
    Rm = R_MAIN
    QRm = sorted(set(np.flatnonzero(dS0 <= Rm).tolist()) - S0set)
    Qx = list(QRm)
    if len(Qx) > 60:
        Qx = sorted(Qx, key=lambda v: (dS0[v], v))[:60]
    Qx = sorted(set(Qx) | set(extras))
    Qlat = S0set | set(Qx)
    # path statistics (complete-search path states T with S0 <= T); kept separate from the lattice sup
    path_max_h, path_argmax = [], []
    path_states_S0 = [T for T in path if S0set <= set(T)]
    n_path_out_lattice = 0
    for T in path_states_S0:
        h = st.h_all(T)
        path_max_h.append(float(np.nanmax(h)))
        path_argmax.append(int(np.nanargmax(h)))
        if not set(T) <= Qlat:
            n_path_out_lattice += 1
    pmh = max(path_max_h) if path_max_h else float("nan")
    hS0 = st.h_all(list(S0))
    worst = list(np.argsort(-np.nan_to_num(hS0, nan=-1))[:10])
    worst += path_argmax                                        # only supplies candidate l (an index); T stays in the lattice
    worst = list(dict.fromkeys(int(v) for v in worst))[:15]
    lsup, cands = lattice_sup(st, S0, Qx, worst, rng)
    cands = sorted(cands, key=lambda c: -c[0])
    seen, na_gain, na_h_at = set(), -np.inf, float('nan')
    for hval, Tc, lc in cands:
        if (Tc, lc) in seen:
            continue
        seen.add((Tc, lc))
        if len(seen) > 40:
            break
        assert S0set <= set(Tc) <= Qlat and lc not in Tc
        g = prob.F(tuple(sorted(set(Tc) | {lc}))) - prob.F(Tc)
        if g > na_gain:
            na_gain, na_h_at = g, hval
    q = len(Qlat)
    # TL margins: deletion-only and deletions+swaps, along the complete path (T >= S0) and at lattice points
    tl_del_path = tl_path = np.inf
    for T in path_states_S0:
        a, b = tl_margins(prob, S0, T, p)
        tl_del_path, tl_path = min(tl_del_path, a), min(tl_path, b)
    lat_pts = [list(S0), sorted(Qlat)]
    for _ in range(40):
        lat_pts.append(list(S0) + [v for v in Qx if rng.random() < 0.5])
    tl_del_lat = tl_lat = np.inf
    swap_binding = False
    for T in lat_pts:
        a, b = tl_margins(prob, S0, T, p)
        tl_del_lat, tl_lat = min(tl_del_lat, a), min(tl_lat, b)
        swap_binding |= (b < a - 1e-12)
    tl_del_min, tl_min = min(tl_del_path, tl_del_lat), min(tl_path, tl_lat)
    cn = math.log(n + 1) + 2 * math.log(p) - 2 * math.log(q + 1)
    tlp = 2 * math.log(p)
    nanf = lambda v: v if np.isfinite(v) else float("nan")
    out = dict(design=did, n=n, p=p, seed=seed, lam_min=round(lam_min, 4), frac0=round(f0, 4), frac01=round(f01, 4), nb0=round(nb0, 2), nb01=round(nb01, 2),
               min_truth_dist=min_truth_d, mode_size=len(mode), n_extra=len(extras),
               max_extra_dist=(float(max(dS0[extras])) if extras else -1.0),
               extras_by_dist=json.dumps({("%.2f" % k): int(c) for k, c in zip(*np.unique(np.round(dS0[extras], 2), return_counts=True))}) if extras else "{}",
               n_zero_dist_extras=int((dS0[extras] == 0).sum()) if extras else 0,
               S0_in_mode=sand[R_MAIN][0],
               sand_R1=sand[1.0][0] and sand[1.0][1], sand_R2=sand[2.0][0] and sand[2.0][1], sand_R3=sand[3.0][0] and sand[3.0][1],
               absQ_R1=sand[1.0][2], absQ_R2=sand[2.0][2], absQ_R3=sand[3.0][2],
               # complete search (bc.local_search)
               ls_moves=res["moves"], ls_final_eq_S0=(res["final"] == S0), ls_certified=bool(res["certified"]), ls_local_limit=bool(res["local_limit"]),
               ls_S0_on_path=(S0 in path),
               # screened search, comparison only
               scr_moves=scr["moves"], scr_final_eq_S0=(scr["final"] == S0), scr_certified=bool(scr["certified"]), scr_timeout=bool(scr["timed_out"]),
               scr_final_eq_complete=(scr["final"] == res["final"]), scr_path_eq_complete=(scr["path"] == path),
               # path statistic (separate from lattice)
               path_max_h=pmh, n_path_states=len(path_states_S0), n_path_out_lattice=n_path_out_lattice,
               path_na_fail=bool(np.isfinite(pmh) and pmh > cn), path_na_fail_2logp=bool(np.isfinite(pmh) and pmh > tlp),
               # lattice sup (T in [S0, Q_lat] only)
               h_at_S0=float(np.nanmax(hS0)), lattice_sup_h=lsup, q=q,
               two_log_p=tlp, c_n=cn, na_fail_lat=bool(lsup > cn), na_fail_2logp_lat=bool(lsup > tlp),
               na_true_maxgain=na_gain, na_true_fail=bool(na_gain > 0), na_h_at=na_h_at, ls_final=json.dumps(sorted(int(v) for v in res['final'])),
               scr_final=json.dumps(sorted(int(v) for v in scr['final'])), S0=json.dumps(list(S0)),
               # TL margins
               tl_del_path=nanf(tl_del_path), tl_del_lat=tl_del_lat, tl_del_min=tl_del_min,
               tl_path=nanf(tl_path), tl_lat=tl_lat, tl_min=tl_min, tl_swap_binding=bool(swap_binding),
               t_complete=round(t_complete, 1), t_screened=round(t_screened, 1), secs=round(time.time() - t0, 1))
    return out


def fmt(v):
    return round(v, 2) if isinstance(v, float) else v


# ------------------------------------------------------------------------------------------------ summary from CSVs
def _conv(v):
    if v in ("True", "False"):
        return v == "True"
    try:
        return float(v)
    except ValueError:
        return v


def load_rows(path):
    with open(path, newline="") as f:
        rows = [{k: _conv(v) for k, v in r.items()} for r in csv.DictReader(f)]
    for r in rows:
        r["n"] = int(r["n"]); r["seed"] = int(r["seed"])
    return rows


def summarize(csv_paths):
    """All aggregate counts below are computed here from the result CSV files (no hand transcription)."""
    rows = []
    for pth in csv_paths:
        rows += load_rows(pth)
    rows.sort(key=lambda r: (r["design"], r["n"], r["seed"]))
    L = []
    P_ = L.append
    P_("n4_r2_pseudo SUMMARY -- generated programmatically from: " + ", ".join(os.path.basename(p) for p in csv_paths))
    P_("FALSIFICATION PROBE: observations only, not a proof.  All 'LS0' counts use the COMPLETE search (bc.local_search);")
    P_("scr_* columns are the screened-search endpoint (ls_fast), comparison only.")
    groups = []
    for did in ("PC1", "PC2"):
        for n in sorted({r["n"] for r in rows if r["design"] == did}):
            groups.append((f"{did} n={n}", [r for r in rows if r["design"] == did and r["n"] == n]))
    for did in ("PC1", "PC2"):
        groups.append((f"{did} ALL n", [r for r in rows if r["design"] == did]))
    groups.append(("TOTAL", rows))

    def cnt(rr, f):
        return "%d/%d" % (sum(1 for r in rr if f(r)), len(rr))

    cols = [
        ("S0<=mode", lambda r: r["S0_in_mode"]),
        ("sandR1", lambda r: r["sand_R1"]), ("sandR2", lambda r: r["sand_R2"]), ("sandR3", lambda r: r["sand_R3"]),
        ("LS0(compl)->S0", lambda r: r["ls_final_eq_S0"]),
        ("compl.certified", lambda r: r["ls_certified"]),
        ("latNA(sup>c_n')FAIL", lambda r: r["na_fail_lat"]),
        ("latsup>2logp", lambda r: r["na_fail_2logp_lat"]),
        ("NA(F)FAIL(gain>0)", lambda r: r["na_true_fail"]),
        ("TLmargin(del+swap)>0", lambda r: r["tl_min"] > 0),
        ("truth-del margin>0", lambda r: r["tl_del_min"] > 0),
        ("pathNA(>c_n')fail", lambda r: r["path_na_fail"]),
        ("scr->S0", lambda r: r["scr_final_eq_S0"]),
        ("scr_final==compl", lambda r: r["scr_final_eq_complete"]),
        ("scr_path==compl", lambda r: r["scr_path_eq_complete"]),
    ]
    P_("")
    P_("TABLE A -- counts k/N (N = runs in group)")
    w = max(len(c[0]) for c in cols) + 1
    P_("%-14s %s" % ("group", " ".join("%*s" % (len(c[0]), c[0]) for c in cols)))
    for name, rr in groups:
        P_("%-14s %s" % (name, " ".join("%*s" % (len(c[0]), cnt(rr, c[1])) for c in cols)))
    P_("")
    P_("TABLE B -- extremes / means")
    hdr = ["group", "lam_min(min)", "|Q_R2|mean", "extras mean", "max lat.sup h", "min c_n'", "2logp", "max path_max_h",
           "max NA(F) gain", "min truth-del margin", "min TL margin(del+swap)", "swapbinding", "pathStates outLat"]
    P_("  ".join(hdr))
    for name, rr in groups:
        P_("%-14s  %.3f  %.1f  %.2f  %.2f  %.2f  %.2f  %.2f  %.3f  %.2f  %.2f  %s  %d" % (
            name, min(r["lam_min"] for r in rr), np.mean([r["absQ_R2"] for r in rr]), np.mean([r["n_extra"] for r in rr]),
            max(r["lattice_sup_h"] for r in rr), min(r["c_n"] for r in rr), rr[0]["two_log_p"],
            np.nanmax([r["path_max_h"] for r in rr]), max(r["na_true_maxgain"] for r in rr),
            min(r["tl_del_min"] for r in rr), min(r["tl_min"] for r in rr),
            cnt(rr, lambda r: r["tl_swap_binding"]), sum(r["n_path_out_lattice"] for r in rr)))
    P_("")
    P_("Per-run flags (sandwich R2 fail / S0 not in mode / complete LS0 not at S0 or not certified / lattice NA proxy fail / NA(F) fail / "
       "TL<=0 / path NA flag / screened-vs-complete disagreement):")
    for r in rows:
        fl = []
        if not r["S0_in_mode"]: fl.append("S0notinmode")
        if not r["sand_R2"]: fl.append("sandR2fail(max_extra_dist=%.2f)" % r["max_extra_dist"])
        if not r["ls_final_eq_S0"] or not r["ls_certified"]:
            fl.append("LS0complete(final=%s,S0=%s,certified=%s,limit=%s)" % (r["ls_final"], r["S0"], r["ls_certified"], r["ls_local_limit"]))
        if r["na_true_fail"]: fl.append("NA(F)FAIL(gain=%.2f at h=%.2f)" % (r["na_true_maxgain"], r["na_h_at"]))
        if r["na_fail_lat"]: fl.append("latNAfail(sup=%.2f>c_n'=%.2f)" % (r["lattice_sup_h"], r["c_n"]))
        if r["tl_min"] <= 0: fl.append("TLfail(%.2f)" % r["tl_min"])
        if r["path_na_fail"]: fl.append("pathNAfail(path_max_h=%.2f>c_n'=%.2f)" % (r["path_max_h"], r["c_n"]))
        if not r["scr_final_eq_complete"] or not r["scr_path_eq_complete"]:
            fl.append("SCREENED!=COMPLETE(scr_final=%s,compl_final=%s,path_eq=%s)" % (r["scr_final"], r["ls_final"], r["scr_path_eq_complete"]))
        if fl:
            P_("  %s n=%d seed=%d : %s" % (r["design"], r["n"], r["seed"], "; ".join(fl)))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "summarize":
        paths = sorted(glob.glob(os.path.join(HERE, "n4_r2_pseudo_results*.csv")))
        txt = summarize(paths)
        print(txt)
        with open(os.path.join(HERE, "n4_r2_pseudo_summary.txt"), "w") as f:
            f.write(txt + "\n")
        sys.exit()
    t_start = time.time()
    NLIST = tuple(int(v) for v in os.environ.get("N4_NLIST", "500,2000").split(","))     # supplementary runs: N4_NLIST=8000 N4_TAG=_n8000
    TAG = os.environ.get("N4_TAG", "")
    cfgs = [(did, n, P, seed) for did in ("PC1", "PC2") for n in NLIST for seed in range(1, NSEEDS + 1)]
    nproc = min(6, os.cpu_count() or 2)
    rows = []
    with Pool(nproc) as pool:
        for r in pool.imap_unordered(job, cfgs):
            rows.append(r)
            print(" ".join("%s=%s" % (k, fmt(v)) for k, v in r.items()), flush=True)
    rows.sort(key=lambda r: (r["design"], r["n"], r["seed"]))
    with open(os.path.join(HERE, "n4_r2_pseudo_results%s.csv" % TAG), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("\n================ SUMMARY (generated from the result CSV files) ================")
    paths = sorted(glob.glob(os.path.join(HERE, "n4_r2_pseudo_results*.csv")))
    txt = summarize(paths)
    print(txt)
    with open(os.path.join(HERE, "n4_r2_pseudo_summary.txt"), "w") as f:
        f.write(txt + "\n")
    print("total runtime %.1f s (this invocation, %d runs, %d processes)" % (time.time() - t_start, len(rows), nproc))
