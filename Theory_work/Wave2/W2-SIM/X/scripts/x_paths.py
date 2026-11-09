"""x_paths.py (v2, after design review X_R01) -- W2-SIM family X: uncapped LS0 paths on iid-Gaussian-row one-factor
designs (exact sufficient statistics).

Scorer / path: the W2-FAC-X ticket modules iid_core.py (IidData = exact Bartlett sufficient statistics; PathState;
ls0_path = production LS0 move rule, uncapped, flip+swap neighbourhood, best strict improvement, exact ties ->
lexicographically smallest set) and bvs_core.py (production partition + block-DP start mode), imported UNCHANGED from the
deployed ticket snapshot ($TICKETS/Theory_work/Wave2/W2-FAC-X/numerics, tickets_20261109T0943; sha256 identical to the
repo files). This file only (i) draws data sets with recorded seeds, (ii) optionally computes the production start mode,
(iii) runs ls0_path from the start mode, from [p] (= S*(empty)) and, when N0 is nonempty, from the oracle S*(N0),
(iv) monitors every scan through ls0_path's diag hook (read-only: best gain, top-two gap) and validates the incremental
gains against a FRESH PathState recomputation at refresh boundaries and at the endpoint, (v) replays the move list for
diagnostics. Nothing here can change a path.

Replay diagnostics (one factor; X_T exact from the Bartlett coordinates eta = A[1,0], phi = A[1,1], N = n - 3,
whitened loadings l_j = lam_j/sqrt(1 - lam_j^2), kappa' = N/phi^2, varrho' = N eta/phi^2):
  X_T = (l_T' xi_T - varrho')/(|l_T|^2 + kappa');  CS: l X_T = x_T = (sum_T xi - varrho)/(k + kappa) (FAC-X s3).
  * 'xi' frame (CS only; item A): kept nulls K_T, deleted nulls D_T (start nulls not in T); a_T/b_T = nearest kept-null
    xi below/above x_T; excursion = max over D_T of distance outside (a_T, b_T)  [(C2)(iii) statistic];
    excess of each deletion |xi_j - x_T| - min_{K_T}|xi_l - x_T| [(C2)(i) statistic] and its rank; hull defect.
  * 'cls' frame (finite loading classes; item B): per class c, the same in the class's fixed xi coordinates around the
    class centre l_c X_T (valid for kept and deleted variables).
  * 'd' frame (any loadings): d_j = xi_j - l_j X_T (unnormalised variable-centre statistic, defined for every j);
    excursion of deleted nulls outside the kept-null hole in d. Descriptive only for continuous loadings.
  * s_j(T) = d_j / sqrt(1 - l_j^2/(|l_T|^2 + kappa')) is computed ONLY for j in T (deletion candidates); rank of the
    deleted null among kept nulls in |s| (variable-centre argmin check). Non-finite values are counted and flagged.
  Diagnostics are computed only while T contains S0 (C2-eligible states); states without S0 are counted.
  Distances are reported raw, / w0 (w0 = Hbar sqrt(p log n/n), Hbar^2 = 2 log(2(p - s0) + 2) + 2 log log n) and
  / (w0 + n^(-1/3)) (the FAC-X varpi_n with C0 = 1); the unknown constant C0(rho) stays explicit.
Usage: python x_paths.py OUT.jsonl item=A rho=0.3 n=10000 p=1000 seeds=0-19 [load=cs|two03_09|two05_095|unif02_09]
       [start=full|mode|both] [mode=iid|ref] [both_seeds=0-2] [A_target=0.75] [coef=std|rev] [lseed=0]
  both_seeds: seeds in this set run start=both, the others start=full (batch-2 policy).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, platform
TK = os.environ.get("TICKETS")
if TK:
    sys.path.insert(0, os.path.join(TK, "Theory_work/Wave2/W2-FAC-X/numerics"))
else:  # local use only
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../W2-FAC-X/numerics"))
import numpy as np
import iid_core as ic
import bvs_core as bc

COEF = {"std": [1.4, -1.0, 1.8, -1.2], "rev": [-1.0, 1.4, -1.2, 1.8]}   # rev: swaps the coefficient/loading-class pairing
ITEM_CODE = {"A": 1, "B": 2, "Q2E": 3, "K2": 4, "REAL": 5, "BS": 7}
LOAD_CODE = {"cs": 0, "two03_09": 1, "two05_095": 2, "unif02_09": 3}
REFRESH = 200          # iid_core.ls0_path default refresh (deletions between full recomputations)
MAX_MOVES = 10 ** 6    # iid_core.ls0_path default safety limit


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def parse_range(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def loadings(p, kind, rho, lseed=0):
    if kind == "cs":
        return np.full(p, math.sqrt(rho))
    if kind == "two03_09":
        return np.where(np.arange(p) % 2 == 0, 0.3, 0.9)
    if kind == "two05_095":
        return np.where(np.arange(p) % 2 == 0, 0.5, 0.95)
    if kind == "unif02_09":   # fixed per (p): n2x_loadings.py convention for lseed = 0
        return np.random.default_rng(99 + p + 100003 * lseed).uniform(0.2, 0.9, p)
    raise ValueError(kind)


def truth_beta(p, coef="std"):
    beta = np.zeros(p)
    idx = np.linspace(2, p - 3, 4).astype(int)
    beta[idx] = COEF[coef]
    return beta


def seed_entropy(item, rho, n, p, load, mode, seed, coef="std", lseed=0):
    e = [20261109, ITEM_CODE[item], int(round(rho * 1000)), int(n), int(p), LOAD_CODE[load], 0 if mode == "iid" else 1,
         int(seed)]
    if coef != "std" or lseed:            # sensitivity runs only; main-grid entropies unchanged
        e += [1 if coef == "rev" else 0, int(lseed)]
    return e


def _hole(kept_vals, cen):
    lo = kept_vals[kept_vals < cen]; hi = kept_vals[kept_vals > cen]
    return (lo.max() if lo.size else -np.inf), (hi.min() if hi.size else np.inf)


def replay(P, start, moves, S0, lam):
    n, p = P.n, P.p
    A = P.A
    eta, phi = float(A[1, 0]), float(A[1, 1])
    N = n - 3
    xi = P.xi
    ell = lam / np.sqrt(1.0 - lam ** 2)
    kap = N / phi ** 2
    rho_ = N * eta / phi ** 2
    S0set = set(S0)
    isnull = np.ones(p, bool); isnull[list(S0)] = False
    inT = np.zeros(p, bool); inT[list(start)] = True
    startnull = inT & isnull
    classes = np.unique(np.round(lam, 12))
    is_cs = len(classes) == 1
    finite_cls = 1 < len(classes) <= 4
    cls_masks = [np.isclose(lam, c) for c in classes] if finite_cls else []
    s0 = len(S0)
    Hbar = math.sqrt(2 * math.log(2 * (p - s0) + 2) + 2 * math.log(math.log(n)))
    w0 = Hbar * math.sqrt(p * math.log(n) / n)
    floor = n ** (-1.0 / 3.0)
    R = dict(xi_exc_max=None, xi_excess_max=None, xi_rank_max=None, xi_defect_max=None, xi_band_max=None,
             cls_exc_max=None, cls_excess_max=None, cls_rank_max=None,
             d_exc_max=0.0, s_excess_max=0.0, s_rank_max=0, common_rank_max=0,
             absX_max=0.0, states_not_eligible=0, nonnull_moves=0, nonfinite_s=0)
    if is_cs:
        R.update(xi_exc_max=0.0, xi_excess_max=0.0, xi_rank_max=0, xi_defect_max=0, xi_band_max=0.0)
    if finite_cls:
        R.update(cls_exc_max=0.0, cls_excess_max=0.0, cls_rank_max=0)
    traj = []
    every = max(1, len(moves) // 50)
    lmean = float(ell.mean())
    for i, mv in enumerate(moves + [None]):
        eligible = all(inT[j] for j in S0)
        if not eligible:
            R["states_not_eligible"] += 1
        T = np.flatnonzero(inT)
        kept = inT & isnull
        deln = startnull & ~inT
        if eligible:
            lt = ell[T]
            L2 = float(lt @ lt)
            XT = (float(lt @ xi[T]) - rho_) / (L2 + kap)
            R["absX_max"] = max(R["absX_max"], abs(XT * lmean))
            if i % every == 0 or mv is None:
                traj.append([i, round(XT * lmean, 6), int(kept.sum())])
            d = xi - ell * XT                              # defined for all j
            kd = d[kept]
            if deln.any() and kd.size:
                a, b = _hole(kd, 0.0)
                dd = d[deln]
                R["d_exc_max"] = max(R["d_exc_max"], float(max(a - dd.min(), dd.max() - b, 0.0)))
            if is_cs:
                xc = lmean * XT
                kx = xi[kept]
                if deln.any() and kx.size:
                    a, b = _hole(kx, xc)
                    dx = xi[deln]
                    R["xi_exc_max"] = max(R["xi_exc_max"], float(max(a - dx.min(), dx.max() - b, 0.0)))
                    lo, hi = dx.min(), dx.max()
                    inside = (kx > lo) & (kx < hi)
                    nd = int(inside.sum())
                    R["xi_defect_max"] = max(R["xi_defect_max"], nd)
                    if nd:
                        R["xi_band_max"] = max(R["xi_band_max"],
                                               float(np.max(np.minimum(kx[inside] - lo, hi - kx[inside]))))
            if finite_cls:
                for mc, c in zip(cls_masks, classes):
                    lc = c / math.sqrt(1 - c * c)
                    kc = xi[kept & mc]; dc = xi[deln & mc]
                    if kc.size and dc.size:
                        a, b = _hole(kc, lc * XT)
                        R["cls_exc_max"] = max(R["cls_exc_max"], float(max(a - dc.min(), dc.max() - b, 0.0)))
        if mv is None:
            break
        tag, jo, li, g = mv
        if tag == "delN" and eligible:
            j = jo
            rad = 1.0 - ell[T] ** 2 / (L2 + kap)
            sT = np.full(p, np.nan)
            with np.errstate(invalid="ignore"):
                sT[T] = d[T] / np.sqrt(rad)
            bad = ~np.isfinite(sT[T])
            R["nonfinite_s"] += int(bad.sum())
            sk = np.abs(sT[kept]); sj = abs(sT[j])
            if np.isfinite(sj) and np.isfinite(sk).all():
                R["s_excess_max"] = max(R["s_excess_max"], float(sj - sk.min()))
                R["s_rank_max"] = max(R["s_rank_max"], int((sk < sj - 1e-12).sum()))
            cm = np.abs(xi[kept] - lmean * XT)
            R["common_rank_max"] = max(R["common_rank_max"], int((cm < abs(xi[j] - lmean * XT) - 1e-12).sum()))
            if is_cs:
                xc = lmean * XT
                dk = np.abs(xi[kept] - xc); dj = abs(xi[j] - xc)
                R["xi_excess_max"] = max(R["xi_excess_max"], float(dj - dk.min()))
                R["xi_rank_max"] = max(R["xi_rank_max"], int((dk < dj - 1e-12).sum()))
            if finite_cls:
                mc = np.isclose(lam, lam[j]) & kept
                lc = ell[j]
                dk = np.abs(xi[mc] - lc * XT); dj = abs(xi[j] - lc * XT)
                R["cls_excess_max"] = max(R["cls_excess_max"], float(dj - dk.min()))
                R["cls_rank_max"] = max(R["cls_rank_max"], int((dk < dj - 1e-12).sum()))
        if tag != "delN":
            R["nonnull_moves"] += 1
        if jo is not None:
            inT[jo] = False
        if li is not None:
            inT[li] = True
    for k in ("xi_exc", "xi_excess", "xi_band", "cls_exc", "cls_excess", "d_exc", "s_excess"):
        v = R[k + "_max"]
        R[k + "_over_w0"] = None if v is None else v / w0
        R[k + "_over_varpi1"] = None if v is None else v / (w0 + floor)
    R.update(w0=w0, Hbar=Hbar, floor=floor, floor_over_w0=floor / w0, kappa_prime=kap, varrho_prime=rho_,
             kappa_cs=(kap / lmean ** 2 if is_cs else None), traj=traj)
    return R


class Monitor:
    """Read-only hook for ls0_path: per-scan best gain / top-two gap, and fresh-recomputation checks of the incremental
    gains at refresh boundaries (step % REFRESH in {REFRESH - 1, 0}, steps >= 1)."""

    def __init__(self, S0, xi, p, delta_every):
        self.S0 = list(S0); self.xi = xi
        self.delta_every = delta_every
        self.min_top2_gap = np.inf; self.min_top2_gap_step = None
        self.n_scans = 0; self.last_best = None; self.last_top2 = None
        self.val_max_absdiff = 0.0; self.val_argmax_disagree = 0; self.val_checks = 0
        self.dmax = 0.0

    def __call__(self, P, st, Gd, Ga, Gs, step):
        self.n_scans += 1
        vals = [a.ravel() for a in (Gd, Ga, Gs) if a.size]
        allg = np.concatenate(vals) if vals else np.zeros(0)
        allg = allg[np.isfinite(allg)]
        if allg.size >= 2:
            top2 = np.partition(allg, -2)[-2:]
            best, second = float(top2[1]), float(top2[0])
            if best > 0 and best - second < self.min_top2_gap:
                self.min_top2_gap = best - second; self.min_top2_gap_step = step
            self.last_best, self.last_top2 = best, best - second
        elif allg.size == 1:
            self.last_best, self.last_top2 = float(allg[0]), None
        if step >= 1 and (step % REFRESH in (REFRESH - 1, 0)):
            self.validate(P, st, Gd, Ga, Gs)
        if self.delta_every and step % self.delta_every == 0:
            self.delta_hat(st)

    def validate(self, P, st, Gd, Ga, Gs):
        fr = ic.PathState(P, st.T)
        G2 = fr.gains()
        diffs = [np.max(np.abs(a - b)) for a, b in zip((Gd, Ga, Gs), G2[:3]) if a.size and np.isfinite(a).all()]
        if diffs:
            self.val_max_absdiff = max(self.val_max_absdiff, float(max(diffs)))
        def am(arrs):
            best, where = -np.inf, None
            for t, a in enumerate(arrs):
                if a.size and np.max(a) > best:
                    best, where = float(np.max(a)), (t, int(np.argmax(a)))
            return where
        if am((Gd, Ga, Gs)) != am(G2[:3]):
            self.val_argmax_disagree += 1
        self.val_checks += 1

    def delta_hat(self, st):     # n1x proxy (copied logic)
        T = st.T
        isN = ~np.isin(T, self.S0)
        if isN.sum() < 4:
            return
        w1 = np.diag(st.W1)
        r = (st.u / np.sqrt(w1))[isN]
        xx = self.xi[T[isN]]
        Am = np.c_[xx, np.ones_like(xx)]
        coef, *_ = np.linalg.lstsq(Am, r, rcond=None)
        c, b = coef
        res = r / c - (xx + b / c)
        self.dmax = max(self.dmax, float(np.max(np.abs(res))))


def path_part(P, rec, start, S0, lam, n, p, do_replay=True):
    rec = dict(rec)
    S0set = set(S0)
    mon = Monitor(S0, P.xi, p, max(1, p // 60))
    t2 = time.time()
    out = ic.ls0_path(P, start, S0, diag_every=1, diag_fn=mon)
    t_path = time.time() - t2
    mv = out["moves"]
    # endpoint validation: fresh recomputation at the final set
    fin = ic.PathState(P, list(out["final"]))
    Gd, Ga, Gs, _ = fin.gains()
    fresh_best = max([float(a.max()) for a in (Gd, Ga, Gs) if a.size] + [-np.inf])
    types = {}
    for m in mv:
        types[m[0]] = types.get(m[0], 0) + 1
    ell_n = ic.ell_cap(n, p)
    cap = ell_n + len(start)
    cur = set(start); arrival = 0 if cur == S0set else None
    for i, m in enumerate(mv):
        tag, jo, li, g = m
        if jo is not None: cur.discard(jo)
        if li is not None: cur.add(li)
        if arrival is None and cur == S0set:
            arrival = i + 1
    t3 = time.time()
    if do_replay:
        D = replay(P, start, mv, S0, lam)
    else:                                   # k >= 2 or general Sigma: no scalar centre, no band diagnostics
        Hb = math.sqrt(2 * math.log(2 * (p - len(S0)) + 2) + 2 * math.log(math.log(n)))
        D = dict(w0=Hb * math.sqrt(p * math.log(n) / n), Hbar=Hb, floor=n ** (-1.0 / 3.0))
    t_replay = time.time() - t3
    info = out["info"]
    termination = "move_limit" if len(mv) >= MAX_MOVES else "stationary"
    numerically_ok = (termination == "stationary" and fresh_best <= 0.0 and mon.val_argmax_disagree == 0)
    rec.update(start_size=len(start), moves=len(mv), types=types, final_is_S0=out["final_is_S0"],
               final_size=len(out["final"]), final_extra=sorted(set(out["final"]) - S0set),
               final_missing=sorted(S0set - set(out["final"])), pure_deletion=all(m[0] == "delN" for m in mv),
               ell_n=ell_n, cap_mr1=cap, within_cap=len(mv) <= cap, arrival_move=arrival,
               S0_scored_within_cap=(arrival is not None and arrival <= cap + 1),
               max_add_gain_over_logn=info["max_add_gain"] / math.log(n), max_truth_move=info["max_truth_move"],
               max_swap_minus_del=info["max_swap_minus_del"], min_del_gain=info["min_del_gain"], ties=info["ties"],
               nondel_moves=[[m[0], m[1], m[2], round(m[3], 5), i] for i, m in enumerate(mv) if m[0] != "delN"],
               termination=termination, endpoint_best_gain_fresh=fresh_best, endpoint_best_gain_incr=mon.last_best,
               min_top2_gap_improving=(None if not np.isfinite(mon.min_top2_gap) else mon.min_top2_gap),
               min_top2_gap_step=mon.min_top2_gap_step, n_scans=mon.n_scans,
               val_checks=mon.val_checks, val_max_absdiff=mon.val_max_absdiff, val_argmax_disagree=mon.val_argmax_disagree,
               numerically_ok=bool(numerically_ok),
               delta_hat_max=mon.dmax, t_path=round(t_path, 1), t_replay=round(t_replay, 1))
    rec["delta_hat_over_w0"] = mon.dmax / D["w0"]
    rec.update(D)
    return rec


def run_one(item, rho, n, p, load, mode, seed, start_kind, A_target=None, coef="std", lseed=0):
    ent = seed_entropy(item, rho, n, p, load, mode, seed, coef, lseed)
    rng = np.random.default_rng(np.random.SeedSequence(ent))
    lam = loadings(p, load, rho, lseed)
    beta = truth_beta(p, coef)
    t0 = time.time()
    P = ic.IidData(lam, beta, n, rng, mode=mode)
    t_data = time.time() - t0
    S0 = P.S0
    A_actual = math.log(p) / math.log(n)
    rec = dict(item=item, rho=rho, n=n, p=p, A=round(A_actual, 4), A_actual=A_actual, A_target=A_target,
               p_capped_n2=(A_target is not None and p == n // 2 and round(n ** A_target) > n // 2),
               load=load, mode=mode, coef=coef, lseed=lseed, seed=seed, seed_entropy=ent, s0=len(S0), S0=list(S0),
               truth_loadings=[float(lam[j]) for j in S0], truth_beta_raw=[float(beta[j]) for j in S0],
               start_kind=start_kind, t_data=round(t_data, 1))
    paths = []
    if start_kind in ("mode", "both"):
        t1 = time.time()
        R = P.XtX / (n - 1.0)
        B = bc.block_size(n, p)
        blocks = bc.partition_from_corr(R, B)
        S0s = set(S0)
        N0 = set()
        for C in blocks:
            if S0s <= set(C):
                N0 |= set(C) - S0s
        info = bc.start_mode(P, blocks)
        St = sorted(int(v) for v in info.mode)
        Sts = set(St)
        target = sorted(set(range(p)) - N0)
        rec.update(B=B, nblocks=len(blocks), N0=len(N0), mode_size=len(St), C1_start_eq_Sstar=(St == target),
                   start_has_S0=S0s <= Sts, start_missing=len(set(target) - Sts), start_extra=len(Sts - set(target)),
                   start_n_optimal=info.n_optimal, start_truncated=info.truncated, t_start=round(time.time() - t1, 1),
                   start_partial_blocks=[[len(C), sum(1 for v in C if v in Sts), sum(1 for v in C if v in S0s)]
                                         for C in blocks if any(v not in Sts for v in C)],
                   start_log_gamma0_mode=info.log_gamma0_mode,
                   start_log_gamma0_Sstar=(float(bc.log_gamma0(P, blocks, target)) if len(target) <= P.K else None))
        paths.append(("mode", St))
        if N0:
            paths.append(("oracle_SstarN0", target))      # (C2) with N = N0, independent of (C1)
    if start_kind in ("full", "both"):
        paths.append(("full", list(range(p))))            # (C2) with N = empty
    return [path_part(P, dict(rec, path_from=nm), st, S0, lam, n, p) for nm, st in paths]


if __name__ == "__main__":
    outf = sys.argv[1]
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    item = kv.get("item", "A"); rho = float(kv.get("rho", 0.5)); n = int(float(kv["n"])); p = int(kv["p"])
    load = kv.get("load", "cs"); mode = kv.get("mode", "iid"); start_kind = kv.get("start", "full")
    A_target = float(kv["A_target"]) if "A_target" in kv else None
    coef = kv.get("coef", "std"); lseed = int(kv.get("lseed", 0))
    seeds = parse_range(kv.get("seeds", "0"))
    both_seeds = set(parse_range(kv["both_seeds"])) if "both_seeds" in kv else None
    prov = dict(x_paths_sha256=sha(os.path.abspath(__file__)), iid_core_sha256=sha(ic.__file__),
                bvs_core_sha256=sha(bc.__file__), numpy=np.__version__, python=platform.python_version(),
                host=platform.node(), slurm_job=os.environ.get("SLURM_ARRAY_JOB_ID", os.environ.get("SLURM_JOB_ID")),
                slurm_task=os.environ.get("SLURM_ARRAY_TASK_ID"), run_id=os.environ.get("RUN_ID"))
    for s in seeds:
        sk = start_kind
        if both_seeds is not None:
            sk = "both" if s in both_seeds else "full"
        for r in run_one(item, rho, n, p, load, mode, s, sk, A_target, coef, lseed):
            r["prov"] = prov
            with open(outf, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(item, rho, n, p, load, coef, lseed, mode, s, r["path_from"], r["start_size"], r["types"],
                  "S0" if r["final_is_S0"] else "MISS", r["termination"], "numok" if r["numerically_ok"] else "NUMCHECK",
                  "add/logn %.3f xi_exc/w0 %s cls_exc/w0 %s valdiff %.2e t_path %.0f t_start %s" % (
                      r["max_add_gain_over_logn"], r["xi_exc_over_w0"], r["cls_exc_over_w0"], r["val_max_absdiff"],
                      r["t_path"], r.get("t_start")), flush=True)
