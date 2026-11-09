"""W2-SIM family PKA -- shared library (informs W2-FAC-PKA; independent of W2-FAC-PK).

Reference code is imported READ-ONLY, never modified:
  * W2-FAC-B scorers  $CODE/Theory_work/Wave2/W2-FAC-B/numerics/{cs_core,bvs_core,fac_core}.py   (main @ 11dc9b7)
  * W2-FAC-PKA numerics $TICKETS/Theory_work/Wave2/W2-FAC-PKA/numerics/{n1_exact_grid,n3_singletons}.py
    (snapshot tickets_20261109T0943; n1 gives TableAdapter + run_path = cs_core.ls0_path_cs patched to accept a start,
    n3 gives singleton_start).
Locally (no env vars) both roots default to this repository checkout.

Replacements written here (validated against the originals by validate.py, output saved):
  * fast_partition_cs(p, B): the FAC-B source partition bc.partition_from_corr(Sigma_CS, B) has O(p^3) cost; under exact
    CS all linkage distances are tied and the source tie rule (tolerance 1e-10, smallest-min-index pair, lexicographic
    union) builds a caterpillar, giving consecutive index blocks of size B.  LABEL: this is the FAC-B *baseline source
    partition* (population Sigma, tie tolerance 1e-10, own complete linkage) -- NOT the production partition, whose
    linkage on a floating-point sample Gram breaks the exact ties by round-off.
  * fast_start_mode(P, blocks): identical arithmetic to bc.start_mode(TableAdapter(P), blocks, tie_tol=0) (same
    combination index arrays, same F_stats call, same max-plus loop), but combinations are cached per block size and the
    tie enumeration is an iterative backtrack (the source uses a generator recursion of depth #blocks).  If any backtrack
    level has more than one optimal option (exact float tie) we fall back to the source enumeration and flag it.
  * certified_path(P, start): the LS0 path.  It evaluates exactly the reference run_path candidates with the same
    doubles, and in addition certifies (or completes by full-row scoring) the interior swaps the reference skips by
    convexity, so exact floating-point ties in the COMPLETE neighbourhood are resolved by the production rule
    (lexicographically smallest resulting set).  Validated move-by-move against run_path and against brute-force
    complete scoring (validate.py V3/V5).  tie_rule='antilex' is a sensitivity re-run only.
Bytecode: sys.dont_write_bytecode is set before any import; jobs also export PYTHONDONTWRITEBYTECODE=1.
"""
import sys, os
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import math, json, hashlib, inspect, itertools, time
from pathlib import Path

_REPO = Path(__file__).resolve().parents[5]          # local checkout root (W2-SIM/PKA/scripts -> repo)
CODE = os.environ.get("CODE") or str(_REPO)
TICKETS = os.environ.get("TICKETS") or str(_REPO)
FACB_DIR = os.path.join(CODE, "Theory_work", "Wave2", "W2-FAC-B", "numerics")
PKA_DIR = os.path.join(TICKETS, "Theory_work", "Wave2", "W2-FAC-PKA", "numerics")
sys.path.insert(0, FACB_DIR)
sys.path.insert(1, PKA_DIR)

import numpy as np
import bvs_core as bc
import cs_core as cs

# R02-F3: the n1 adapter patches cs_core.ls0_path_cs by str.replace; assert each target occurs exactly once.
_SRC = inspect.getsource(cs.ls0_path_cs)
for _t in ("def ls0_path_cs(P, max_moves=10 ** 7, record_every=0):", "inT = np.ones(p, bool)",
           "k = p\n    A = float(z @ z)\n    B = float(z.sum())"):
    assert _SRC.count(_t) == 1, ("n1 replacement target not unique", _t)
import n1_exact_grid as n1        # TableAdapter, run_path (reference, unmodified)
import n3_singletons as n3        # singleton_start (reference, unmodified)
assert os.path.dirname(os.path.abspath(cs.__file__)) == os.path.abspath(FACB_DIR), cs.__file__
assert os.path.dirname(os.path.abspath(n1.__file__)) == os.path.abspath(PKA_DIR), n1.__file__

run_path = n1.run_path
TableAdapter = n1.TableAdapter
singleton_start = n3.singleton_start
NEG = -np.inf


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def provenance(extra=None):
    import scipy
    files = {os.path.relpath(m.__file__, CODE if m in (bc, cs) else TICKETS).replace("\\", "/"): sha256(m.__file__)
             for m in (bc, cs, n1, n3)}
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(os.listdir(here)):
        if f.endswith(".py"):
            files["PKA/scripts/" + f] = sha256(os.path.join(here, f))
    env = {k: os.environ.get(k) for k in ("RUN_ID", "SLURM_ARRAY_JOB_ID", "SLURM_ARRAY_TASK_ID", "SLURM_JOB_ID",
                                          "HOSTNAME", "OMP_NUM_THREADS", "PYTHONDONTWRITEBYTECODE")}
    d = dict(code=CODE, tickets=TICKETS, files=files, python=sys.version.split()[0], numpy=np.__version__,
             scipy=scipy.__version__, platform=sys.platform, argv=sys.argv, env=env)
    if extra:
        d.update(extra)
    return d


def write_provenance(path, extra=None):
    """Write a provenance sidecar; return its sha256 digest (first 16 hex) for reference in every row."""
    d = provenance(extra)
    txt = json.dumps(d, indent=1, sort_keys=True)
    open(path, "w").write(txt)
    return hashlib.sha256(txt.encode()).hexdigest()[:16]


def seed_for(*key):
    """Deterministic, cell-distinct seed: SeedSequence over (20261109, family code 7, *key) -> 63-bit int."""
    ss = np.random.SeedSequence([20261109, 7] + [int(k) for k in key])
    return int(ss.generate_state(2, dtype=np.uint64)[0] >> np.uint64(1))


# ------------------------------------------------------------------------------------------- partition
def fast_partition_cs(p, B):
    return [list(range(s, min(s + B, p))) for s in range(0, p, B)]


def partition_digest(blocks):
    return hashlib.sha256(json.dumps([list(map(int, b)) for b in blocks]).encode()).hexdigest()[:16]


# ------------------------------------------------------------------------------------------- start mode
_COMB = {}


def _combs(m, k):
    key = (m, k)
    if key not in _COMB:
        _COMB[key] = np.array(list(itertools.combinations(range(m), k)), dtype=np.int64)
    return _COMB[key]


def fast_start_mode(P, blocks, tie_tol=0.0, want_tables=False):
    """Same result as bc.start_mode(TableAdapter(P), blocks, tie_tol) for the mode (see module doc)."""
    adp = TableAdapter(P)
    K = adp.K
    J = len(blocks)
    kmax = min(max(len(C) for C in blocks), K)   # Mmax[b, j] = -inf for j > kmax (source stores the full width)
    Mmax = np.full((J, kmax + 1), NEG)
    ties = []
    for b, C in enumerate(blocks):
        Carr = np.array(C, dtype=np.int64)
        m = len(C)
        tb = {0: [()]}
        Mmax[b, 0] = 0.0                      # source: k=0 table is lr = [0.0]
        for k in range(1, min(m, K) + 1):
            idx = Carr[_combs(m, k)]
            lr = adp.logm_idx(idx) - adp.logm0
            mx = float(lr.max())
            Mmax[b, k] = mx
            sel = np.flatnonzero(lr >= mx - tie_tol)
            tb[k] = [tuple(int(v) for v in idx[i]) for i in sel[:20000]]
        ties.append(tb)
    Fm = np.full((J + 1, K + 1), NEG)
    Fm[0, 0] = 0.0
    for b in range(J):
        for j in range(0, min(len(blocks[b]), K) + 1):
            if not np.isfinite(Mmax[b, j]):
                continue
            cand = Mmax[b, j] + Fm[b, :K + 1 - j]
            Fm[b + 1, j:] = np.maximum(Fm[b + 1, j:], cand)
    vals = adp.logw + Fm[J]
    best_k, best_v = None, NEG
    for k in range(K + 1):
        if vals[k] > best_v:
            best_k, best_v = k, vals[k]
    r, acc, ambiguous = best_k, [], False
    for b in range(J - 1, -1, -1):
        target = Fm[b + 1, r]
        opts = []
        for j in range(0, min(r, kmax) + 1):
            if not np.isfinite(Mmax[b, j]) or not np.isfinite(Fm[b, r - j]):
                continue
            if abs(Mmax[b, j] + Fm[b, r - j] - target) <= tie_tol:
                for U in ties[b].get(j, []):
                    opts.append((j, U))
        if len(opts) != 1:
            ambiguous = True
            break
        j, U = opts[0]
        acc.extend(U)
        r -= j
    out = dict(size=best_k, log_gamma0_mode=float(best_v), fallback=False)
    if ambiguous:                             # exact tie somewhere: use the source enumeration
        sys.setrecursionlimit(max(10000, 4 * J + 100))
        info = bc.start_mode(adp, blocks, tie_tol=tie_tol)
        out.update(mode=info.mode, size=info.size, log_gamma0_mode=info.log_gamma0_mode, fallback=True,
                   n_optimal=info.n_optimal)
    else:
        out["mode"] = tuple(sorted(acc))
    # margin of the selected size over the best other size (for saturation diagnostics)
    other = np.delete(vals, best_k)
    out["size_margin"] = float(best_v - other.max()) if other.size and np.isfinite(other.max()) else None
    out["best_below_K_gap"] = float(best_v - vals[:K].max()) if best_k == K and K > 0 else None
    if want_tables:
        out["Mmax"] = Mmax
    return out


# ------------------------------------------------------------------------------------------- path analysis
def centre_consts(P):
    """null z_j = b + d xi_j  (sigma=1):  b = [(n-1) rho thetabar + sqrt((n-1) rho) eta]/s,  d = sqrt((n-1)(1-rho))/s."""
    n, rho = P.n, P.rho
    tb = float(P.theta.sum())
    b = ((n - 1.0) * rho * tb + math.sqrt((n - 1.0) * rho) * P.eta) / P.s
    d = math.sqrt((n - 1.0) * (1 - rho)) / P.s
    return b, d


def tag_of(typ, jo, li, S0):
    if typ == "s":
        if jo in S0 and li in S0:
            return "sTT"
        if jo in S0:
            return "sTo"         # truth out, null in
        if li in S0:
            return "sTi"         # null out, truth in
        return "sNN"
    if typ == "-":
        return "-T" if jo in S0 else "-N"
    return "+T" if li in S0 else "+N"


def certified_path(P, start, max_moves=10 ** 7, tie_rule="lex", tau_rel=1e-8, stop=None, trace=True):
    """Complete-scan LS0 path from `start` (R01 finding 1).  Evaluates exactly the candidates of the reference
    run_path (all deletions, all additions if k<K, swaps against the min/max outside z), with the SAME F_stats calls
    and the same incremental (A,B) updates, so its doubles coincide with the reference's.  In addition it certifies
    the omitted interior swaps: for each swap-out j the exact swap score is a convex function of z_l, so every
    interior l is bounded (exactly) by the second-extreme outside values; if max over those second extremes is not
    < best - tau (tau = tau_rel*max(1,|best|)), the full rows of the affected j are scored with the same formula and
    any exactly tied (or larger) interior candidate is added.  The chosen move is the lexicographically smallest
    resulting set among all exactly tied candidates (tie_rule='lex', production rule) or the largest ('antilex',
    sensitivity only).  stop(moves) -> True ends the run early (termination 'stop').
    Returns moves [(tag, out, in)], final, termination in {'certified','limit','stop'}, info, trace rows
    (t, out, in, F_best, gain, n_tied, gap2), tie records."""
    n, p, K = P.n, P.p, P.K
    z = P.z
    S0 = set(P.S0)
    S0mask = np.zeros(p, bool)
    S0mask[list(S0)] = True
    inT = np.zeros(p, bool)
    inT[list(start)] = True
    k = len(start)
    A = float(z[inT] @ z[inT])
    B = float(z[inT].sum())
    moves, tr, tie_recs = [], [], []
    info = dict(max_add_gain=-np.inf, max_swap_minus_del=-np.inf, min_del_gain=np.inf, ties=0, max_truth_move=-np.inf,
                interior_checks=0, interior_ties=0, interior_exceeds=0, min_gap2=np.inf, near_ties=0)
    termination = None
    while True:
        FT = float(P.F_stats(k, A, B))
        idx_in = np.flatnonzero(inT)
        idx_out = np.flatnonzero(~inT)
        zin, zout = z[idx_in], z[idx_out]
        Fd = P.F_stats(np.full(len(idx_in), k - 1), A - zin ** 2, B - zin) if k >= 1 else np.array([])
        Fa = P.F_stats(np.full(len(idx_out), k + 1), A + zout ** 2, B + zout) if (k < K and len(idx_out)) else np.array([])
        if len(idx_out) and len(idx_in):
            ext = np.unique([int(np.argmin(zout)), int(np.argmax(zout))])
            zl = zout[ext]
            Fs = P.F_stats(np.full((len(idx_in), len(ext)), k), (A - zin ** 2)[:, None] + zl[None, :] ** 2,
                           (B - zin)[:, None] + zl[None, :])
        else:
            ext = np.array([], dtype=np.int64)
            Fs = np.zeros((len(idx_in), 0))
        best = max([FT] + ([float(Fd.max())] if len(Fd) else []) + ([float(Fa.max())] if len(Fa) else []) +
                   ([float(Fs.max())] if Fs.size else []))
        tau = tau_rel * max(1.0, abs(best))
        # ---- certification of the interior swaps
        extra = []                                    # (j_pos, l_pos) interior candidates with F >= best
        others = []                                   # values used for the second-best gap
        no = len(idx_out)
        if Fs.size and no > len(ext):
            if no <= 4:
                cand2 = np.setdiff1d(np.arange(no), ext)
            else:
                part = np.argpartition(zout, (1, no - 2))
                cand2 = np.setdiff1d(np.array([part[0], part[1], part[no - 2], part[no - 1]]), ext)
            z2 = zout[cand2]
            Fs2 = P.F_stats(np.full((len(idx_in), len(cand2)), k), (A - zin ** 2)[:, None] + z2[None, :] ** 2,
                            (B - zin)[:, None] + z2[None, :])
            others.append(float(Fs2.max()))
            rows = np.flatnonzero(Fs2.max(axis=1) >= best - tau)
            if len(rows):
                info["interior_checks"] += 1
                interior = np.setdiff1d(np.arange(no), ext)
                zi = zout[interior]
                for jp in rows:
                    Fr = P.F_stats(np.full(len(interior), k), (A - zin[jp] ** 2) + zi ** 2, (B - zin[jp]) + zi)
                    for q in np.flatnonzero(Fr >= best):
                        extra.append((int(jp), int(interior[q]), float(Fr[q])))
        if extra:
            mx = max(v for _, _, v in extra)
            if mx > best:
                info["interior_exceeds"] += 1
                best = mx
        # ---- second-best distinct value (gap diagnostic)
        vals = np.concatenate([np.array([FT]), Fd, Fa, Fs.ravel(), np.array(others)])
        below = vals[vals < best]
        gap2 = float(best - below.max()) if below.size else np.inf
        # ---- diagnostics as in the reference
        isN_in = ~S0mask[idx_in]
        if len(Fa):
            info["max_add_gain"] = max(info["max_add_gain"], float(Fa.max()) - FT)
        if (~isN_in).any():
            tm = float(Fd[~isN_in].max()) - FT
            if Fs.size:
                tm = max(tm, float(Fs[~isN_in].max()) - FT)
            info["max_truth_move"] = max(info["max_truth_move"], tm)
        if isN_in.any() and Fs.size:
            info["max_swap_minus_del"] = max(info["max_swap_minus_del"], float(Fs[isN_in].max()) - float(Fd[isN_in].max()))
        if not best > FT:
            termination = "certified"
            break
        opts = []
        for i in np.flatnonzero(Fd == best):
            opts.append(("-", int(idx_in[i]), None))
        if len(Fa):
            for i in np.flatnonzero(Fa == best):
                opts.append(("+", None, int(idx_out[i])))
        if Fs.size:
            for i, e in zip(*np.nonzero(Fs == best)):
                opts.append(("s", int(idx_in[i]), int(idx_out[ext[e]])))
        n_int = 0
        for jp, lp, v in extra:
            if v == best:
                o = ("s", int(idx_in[jp]), int(idx_out[lp]))
                if o not in opts:
                    opts.append(o)
                    n_int += 1
        if n_int:
            info["interior_ties"] += 1
        info["min_gap2"] = min(info["min_gap2"], gap2)
        if gap2 < tau:
            info["near_ties"] += 1
        if len(opts) > 1:
            info["ties"] += 1
            cur = idx_in.tolist()

            def _res(o):
                t_, jo_, li_ = o
                st = [v for v in cur if v != jo_] if jo_ is not None else list(cur)
                if li_ is not None:
                    st = sorted(st + [li_])
                return tuple(st)
            opts.sort(key=_res)
            chosen = opts[0] if tie_rule == "lex" else opts[-1]
            tie_recs.append(dict(t=len(moves), n_tied=len(opts), n_interior=n_int, chosen=list(chosen),
                                 options=[list(o) for o in opts[:12]], gap2=gap2))
        else:
            chosen = opts[0]
        typ, jo, li = chosen
        if typ == "-":
            info["min_del_gain"] = min(info["min_del_gain"], best - FT)
        if jo is not None:
            inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]
        if li is not None:
            inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]
        tag = typ + ("T" if (jo in S0 or li in S0) else "N")
        moves.append((tag, jo, li))
        if trace:
            tr.append((len(moves) - 1, jo, li, best, best - FT, len(opts), gap2))
        if len(moves) >= max_moves:
            termination = "limit"
            break
        if stop is not None and stop(moves):
            termination = "stop"
            break
    final = tuple(int(j) for j in np.flatnonzero(inT))
    return dict(moves=moves, final=final, final_is_S0=(set(final) == S0), info=info, termination=termination,
                trace=tr, tie_records=tie_recs)


WINDOW_C = (0.5, 1.0, 1.5, 2.0, 3.0)      # fixed C for windows ceil(C log n); 1.5 > 1/log 2


def analyse_path(P, start, res, ell, caps):
    """Replays a path (moves of certified_path or run_path) from `start`.  Scan t = scan of C_t (t=0: start).
    With cap a the scans are t = 0..min(a, m*).  If res['termination'] != 'certified' the path is a PREFIX: cap
    outcomes are decided only when the prefix already settles them (scored within the prefix, or a <= prefix length
    for arrival/terminal); otherwise None.  Late-path fields are then labelled prefix-only."""
    z = P.z
    S0 = set(P.S0)
    s0 = len(S0)
    n, p, K = P.n, P.p, P.K
    b, d = centre_consts(P)
    inT = np.zeros(p, bool)
    inT[list(start)] = True
    k = len(start)
    A = float(z[inT] @ z[inT])
    B = float(z[inT].sum())
    T = set(int(j) for j in start)
    moves = res["moves"]
    nm = len(moves)
    complete = res.get("termination", "certified") == "certified"

    def nbhd_has_S0(T):
        missing = len(S0 - T)
        extra = len(T - S0)
        if missing == 0 and extra == 0:
            return True
        if missing + extra == 1:
            return not (extra == 0 and len(T) >= K)
        return missing == 1 and extra == 1

    def gam(k):
        return P.be / (P.al + k * P.be)

    def xcentre(k, B):
        return (gam(k) * B - b) / d if k > 0 else float("nan")

    def Qof(k, A, B):
        return (n - 1.0) - n * ((A - gam(k) * B * B) / P.al) if k > 0 else n - 1.0

    def Mmul(Q):
        return P.nu * n * d * d / (P.al * (0.02 + Q))

    has_all_truth = lambda T: S0 <= T
    first_score = 0 if nbhd_has_S0(T) else None
    first_arrival = 0 if T == S0 else None
    x0 = xcentre(k, B)
    Q0 = Qof(k, A, B)
    M0 = Mmul(Q0)
    xs_abs_max, xs_abs_arg = abs(x0), 0
    # per-move series needed for windows
    tags, xs, Qs, Ms, alltruth = [], [x0], [Q0], [M0], [has_all_truth(T)]
    rec, del_run = [], 0
    entered, left = set(), set()
    reentries = in_then_out = 0
    sizes_min = k
    sizes = [k]
    for t, (tg, jo, li) in enumerate(moves):
        typ = tg[0]
        tag = tag_of(typ, jo, li, S0)
        tags.append(tag)
        if jo is not None:
            inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]; T.discard(int(jo))
            if int(jo) in entered:
                in_then_out += 1
            left.add(int(jo))
        if li is not None:
            inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]; T.add(int(li))
            if int(li) in left:
                reentries += 1
            entered.add(int(li))
        sizes_min = min(sizes_min, k)
        sizes.append(k)
        x = xcentre(k, B)
        Q = Qof(k, A, B)
        xs.append(x); Qs.append(Q); Ms.append(Mmul(Q)); alltruth.append(has_all_truth(T))
        if abs(x) > xs_abs_max:
            xs_abs_max, xs_abs_arg = abs(x), t + 1
        if tag == "-N":
            del_run += 1
        else:
            if del_run:
                rec.append(["-N*", del_run]); del_run = 0
            F = float(P.F_stats(k, A, B))
            rec.append([t, tag, None if jo is None else int(jo), None if li is None else int(li), round(F, 6)])
        if first_score is None and nbhd_has_S0(T):
            first_score = t + 1
        if first_arrival is None and T == S0:
            first_arrival = t + 1
    if del_run:
        rec.append(["-N*", del_run])
    final = set(int(j) for j in np.flatnonzero(inT))
    cnt = {}
    for tg in tags:
        cnt[tg] = cnt.get(tg, 0) + 1
    first_nonswap = next((t for t, tg in enumerate(tags) if tg[0] != "s"), None)
    first_del = next((t for t, tg in enumerate(tags) if tg[0] == "-"), None)
    first_truth_out = next((t for t, tg in enumerate(tags) if tg in ("sTo", "-T", "sTT")), None)
    first_non_nn = next((t for t, tg in enumerate(tags) if tg != "sNN"), None)
    last_swap = max((t for t, tg in enumerate(tags) if tg[0] == "s"), default=None)
    init_swaps = first_nonswap if first_nonswap is not None else (nm if complete else None)
    init_null_swaps = first_non_nn if first_non_nn is not None else (nm if complete else None)
    swaps_after_first_del = sum(1 for t, tg in enumerate(tags) if tg[0] == "s" and first_del is not None and t > first_del)
    # fixed C log n windows (moves 0..L-1, centres C_0..C_L)
    windows = {}
    for Cw in WINDOW_C:
        L = math.ceil(Cw * math.log(n))
        avail = nm >= L or complete
        Lw = min(L, nm)
        windows[str(Cw)] = dict(
            L=L, available=avail, path_shorter_than_L=complete and nm < L,
            all_null_null=(all(tg == "sNN" for tg in tags[:L]) and nm >= L) if avail else None,
            all_size_preserving=(all(tg[0] == "s" for tg in tags[:L]) and nm >= L) if avail else None,
            all_truth_retained=all(alltruth[:Lw + 1]) if avail else None,
            centre_drift_max=max(abs(x - x0) for x in xs[:Lw + 1]) if avail else None,
            Q_min=min(Qs[:Lw + 1]) if avail else None, Q_max=max(Qs[:Lw + 1]) if avail else None,
            M_min=min(Ms[:Lw + 1]) if avail else None)
    # whole initial swap phase (descriptive)
    ph = init_swaps if init_swaps is not None else nm
    phase = dict(centre_drift_max=max(abs(x - x0) for x in xs[:ph + 1]), Q_min=min(Qs[:ph + 1]),
                 M_min=min(Ms[:ph + 1]), M_min_alltruth=min([Ms[i] for i in range(ph + 1) if alltruth[i]], default=None))
    cap_out = {}
    for name, a in caps.items():
        a = int(a)
        decided = complete or a <= nm
        stop = min(a, nm)
        Tc = set(int(j) for j in start)
        for (tg, jo, li) in moves[:stop]:
            if jo is not None: Tc.discard(int(jo))
            if li is not None: Tc.add(int(li))
        sc = first_score is not None and first_score <= a
        cap_out[name] = dict(a=a, decided=decided,
                             scored=sc if (decided or sc) else None,
                             arrived=(first_arrival is not None and first_arrival <= a) if decided else None,
                             terminal_is_S0=(Tc == S0) if decided else None,
                             local_limit=(nm > a) if decided else None,
                             terminal_size=len(Tc) if decided else None,
                             terminal_missing=sorted(S0 - Tc) if decided else None, scans=stop + 1 if decided else None)
    out = dict(
        termination=res.get("termination", "certified"), path_complete=complete, moves_run=nm,
        m_star=nm if complete else None,
        final_is_S0=(final == S0) if complete else None,
        final_missing=sorted(S0 - final) if complete else None, final_extra=len(final - S0) if complete else None,
        counts=cnt, initial_swaps=init_swaps, initial_null_swaps=init_null_swaps,
        initial_swaps_over_logn=(init_swaps / math.log(n)) if init_swaps is not None else None,
        first_nonswap_index=first_nonswap, first_deletion_index=first_del, first_truth_out_index=first_truth_out,
        end_of_swap_index=last_swap, end_of_swap_index_prefix_only=not complete,
        swaps_after_first_deletion=swaps_after_first_del, swaps_reappear=swaps_after_first_del > 0,
        reentries=reentries, in_then_out=in_then_out, min_size=sizes_min,
        first_scoring_scan=first_score, first_arrival=first_arrival, caps=cap_out,
        centre_x0=x0, max_abs_centre=xs_abs_max, max_abs_centre_at=xs_abs_arg, max_abs_centre_prefix_only=not complete,
        Q0=Q0, M0=M0, windows=windows, init_phase=phase,
        ties=res["info"]["ties"], max_add_gain=res["info"]["max_add_gain"],
        max_swap_minus_del=res["info"]["max_swap_minus_del"], max_truth_move=res["info"]["max_truth_move"])
    for key in ("interior_checks", "interior_ties", "interior_exceeds", "min_gap2", "near_ties"):
        if key in res["info"]:
            out[key] = res["info"][key]
    out["tie_scans"] = [r["t"] for r in res.get("tie_records", [])]
    out["moves_compact"] = rec
    return out


def start_summary(P, start, blocks=None):
    S0 = set(P.S0)
    st = set(int(j) for j in start)
    nulls = np.array(sorted(st - S0), dtype=np.int64)
    xi = P.xi[nulls] if len(nulls) else np.array([np.nan])
    qs = [0, .05, .25, .5, .75, .95, 1]
    out = dict(start_size=len(st), K=P.K, start_is_K=len(st) == P.K, truth_in_start=S0 <= st,
               truth_missing_from_start=sorted(S0 - st), n_null_retained=int(len(nulls)),
               retained_null_xi_mean=float(np.mean(xi)),
               retained_null_xi_q={str(q): float(np.quantile(xi, q)) for q in qs},
               all_null_xi_mean=float(np.mean(np.delete(P.xi, list(S0)))))
    if blocks is not None:
        prof = {}
        for C in blocks:
            c = sum(1 for j in C if j in st)
            prof[c] = prof.get(c, 0) + 1
        out["start_block_profile"] = {str(k): v for k, v in sorted(prof.items())}
    return out


def git_like_json(obj):
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, set):
            return sorted(o)
        raise TypeError(type(o))
    return json.dumps(obj, default=conv)
