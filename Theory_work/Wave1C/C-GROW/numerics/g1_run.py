"""g1_run.py -- falsification test G1 of C-GROW lemma L6 (iid-row AR(1), p up to >> n).
Imports bvs_core (unchanged).  One data set per call of run(job); job = (rho, n, p, seed).
Usage: py -3.13 g1_run.py [--rows 0,1,2,3] [--procs 3] [--seeds 10]
Writes G1_raw.csv (append, resumable).  Generator conventions follow study_common.build_xy (iid rows, standardise X,
y = X theta + eps, then centred/scaled), with Sigma = AR(1) rho.
Truth indices (0-based), s0=4, evenly spaced: round((k+0.5) p/4), k=0..3 ; theta = (1.4,-1.0,1.8,-1.2).
"""
import os, sys, math, time, json, csv, itertools
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.linalg import cho_factor, cho_solve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvs_core as bc

THETA4 = np.array([1.4, -1.0, 1.8, -1.2])
ROWS = [(200, 1000), (400, 2000), (800, 800), (800, 4000)]
RHOS = [0.5, 0.8]
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "G1_raw.csv")


def truths(p):
    return [int(round((k + 0.5) * p / 4)) for k in range(4)]


def d_n(rho, n):
    return math.ceil(math.log(n) / (2 * math.log(1 / abs(rho))))


def dist_to(S0, j):
    return min(abs(j - t) for t in S0)


def tok(Sa, Sb, S0):
    a, b = set(Sa), set(Sb)
    T = set(S0)
    if len(b) == len(a) + 1:
        j = next(iter(b - a))
        return "+T" if j in T else "+N"
    if len(b) == len(a) - 1:
        j = next(iter(a - b))
        return "-T" if j in T else "-N"
    o = next(iter(a - b)); i = next(iter(b - a))
    return "sw" + ("T" if o in T else "N") + ">" + ("T" if i in T else "N")


# ------------------------------------------------------------------ (b) NA: all F(T+l)-F(T) at once
def F_of_T(prob, T):
    return prob.F(tuple(sorted(T)))


def dF_add_all(prob, T):
    """F(T u {l}) - F(T) for all l (nan for l in T), via Schur complements of the exact Problem.logm_idx arithmetic."""
    n, nu, G, z = prob.n, prob.nu, prob.XtX, prob.Xty
    T = np.array(sorted(T), dtype=np.int64)
    t = len(T)
    GT = G[np.ix_(T, T)]
    H = (n + 1.0) * GT + np.eye(t)
    A = GT + np.eye(t)
    cH = cho_factor(H, lower=True)
    cA = cho_factor(A, lower=True)
    ldH = 2 * np.log(np.diag(cH[0])).sum()
    ldA = 2 * np.log(np.diag(cA[0])).sum()
    zT = z[T]
    solz = cho_solve(cH, zT)
    quadT = float(zT @ solz)
    GTl = G[T, :]                       # t x p
    hl = (n + 1.0) * GTl
    Gll = np.diag(G)
    sH = (n + 1.0) * Gll + 1.0 - (hl * cho_solve(cH, hl)).sum(axis=0)
    sA = Gll + 1.0 - (GTl * cho_solve(cA, GTl)).sum(axis=0)
    num = z - hl.T @ solz
    quad_new = quadT + num ** 2 / sH
    Q = prob.yty - n * quad_new
    logm_new = -0.5 * ((ldH + np.log(sH)) - (ldA + np.log(sA))) - nu * np.log(0.02 + Q)
    k1 = t + 1
    Fnew = prob.logw[k1] + logm_new if k1 <= prob.K else np.full(prob.p, np.nan)
    FT = prob.logw[t] + (-0.5 * (ldH - ldA) - nu * math.log(0.02 + prob.yty - n * quadT))
    out = Fnew - FT
    out[T] = np.nan
    return out, FT


def na_family(prob, S0, Qset, rng, n_random=100):
    Qr = sorted(Qset - set(S0))
    fam = {}
    fam[tuple(sorted(S0))] = "bottom:S0"
    for e in Qr:
        fam[tuple(sorted(set(S0) | {e}))] = "bottom:S0+1"
    fam[tuple(sorted(Qset))] = "top:Q"
    for e in Qr:
        fam[tuple(sorted(Qset - {e}))] = "top:Q-1"
    for _ in range(n_random):
        pin = rng.random()
        inc = [e for e in Qr if rng.random() < pin]
        fam.setdefault(tuple(sorted(set(S0) | set(inc))), "random")
    return fam


def na_test(prob, S0, Qset, rng):
    p = prob.p
    fam = na_family(prob, S0, Qset, rng)
    Qarr = np.zeros(p, dtype=bool)
    Qarr[sorted(Qset)] = True
    best_near, best_far = -np.inf, -np.inf
    arg_near = arg_far = None
    nT = nskip = 0
    maxdisc = 0.0
    checks = 0
    vals_by_kind = {}
    bysz = {}
    npos_near = npos_far = 0
    for T, kind in fam.items():
        if len(T) + 1 > prob.K:
            nskip += 1
            continue
        nT += 1
        d, FT = dF_add_all(prob, T)
        Tm = np.zeros(p, dtype=bool); Tm[list(T)] = True
        near = np.where(Qarr & ~Tm, d, -np.inf)
        far = np.where(~Qarr, d, -np.inf)
        i = int(np.argmax(near)); j = int(np.argmax(far))
        mnear = float(near[i]); mfar = float(far[j]) if (~Qarr).any() else -np.inf
        npos_near += int((near > 0).sum()); npos_far += int((far > 0).sum())
        bk = "T<=5" if len(T) <= 5 else ("T6-15" if len(T) <= 15 else "T>15")
        bz = bysz.setdefault(bk, [-np.inf, -np.inf, 0])
        bz[0] = max(bz[0], mnear); bz[1] = max(bz[1], mfar); bz[2] += 1
        v = vals_by_kind.setdefault(kind, [-np.inf, -np.inf])
        v[0] = max(v[0], mnear); v[1] = max(v[1], mfar)
        if mnear > best_near:
            best_near, arg_near = mnear, (kind, len(T), i, dist_to(S0, i))
        if mfar > best_far:
            best_far, arg_far = mfar, (kind, len(T), j, dist_to(S0, j))
        # cross-check a few l against Problem.F (production scorer)
        if nT % 25 == 1:
            cand = [int(i), int(j)] + [int(x) for x in rng.integers(0, p, 4)]
            for l in cand:
                if Tm[l]:
                    continue
                dd = prob.F(tuple(sorted(T + (l,)))) - prob.F(T)
                maxdisc = max(maxdisc, abs(dd - d[l]))
                checks += 1
    return dict(nT=nT, nT_skipped_size=nskip, na_max_near=best_near, na_max_far=best_far,
                na_arg_near=json.dumps(arg_near), na_arg_far=json.dumps(arg_far),
                na_npos_near=npos_near, na_npos_far=npos_far,
                na_by_size=json.dumps({k: [round(a, 4), round(b, 4), c] for k, (a, b, c) in bysz.items()}),
                na_by_kind=json.dumps({k: [round(a, 4), round(b, 4)] for k, (a, b) in vals_by_kind.items()}),
                na_schur_vs_F_maxdiff=maxdisc, na_schur_checks=checks)


# ------------------------------------------------------------------ (d) far-null h statistics
class HStat:
    def __init__(self, prob):
        self.prob = prob

    def rss_batch(self, idx):
        prob = self.prob
        idx = np.asarray(idx, dtype=np.int64)
        m, k = idx.shape
        if k == 0:
            return np.full(m, prob.yty)
        G = prob.XtX[idx[:, :, None], idx[:, None, :]]
        z = prob.Xty[idx]
        sol = np.linalg.solve(G, z[..., None])[..., 0]
        return prob.yty - (z * sol).sum(axis=1)

    def h_pairs(self, pairs):
        """pairs: list of (l, U tuple). returns array of h."""
        n = self.prob.n
        out = np.empty(len(pairs))
        by = {}
        for i, (l, U) in enumerate(pairs):
            by.setdefault(len(U), []).append(i)
        for k, ids in by.items():
            U = np.array([pairs[i][1] for i in ids], dtype=np.int64).reshape(len(ids), k)
            l = np.array([pairs[i][0] for i in ids], dtype=np.int64)[:, None]
            r0 = self.rss_batch(U)
            r1 = self.rss_batch(np.concatenate([U, l], axis=1))
            out[ids] = n * (r0 - r1) / r0
        return out


def far_test(prob, blocks, Qset, S0, k0, rng, n_sample=2000):
    n, p = prob.n, prob.p
    hs = HStat(prob)
    bid = bc.block_id_array(blocks, p)
    far_l = [l for l in range(p) if l not in Qset]
    res = {}
    # U = empty, all l
    h0 = hs.h_pairs([(l, ()) for l in far_l])
    res["h_empty_max"] = float(h0.max())
    # |U| <= 1 full enumeration
    pairs1 = [(l, (u,)) for l in far_l for u in blocks[bid[l]] if u != l]
    h1 = hs.h_pairs(pairs1) if pairs1 else np.array([0.0])
    res["h_U1_max"] = float(h1.max()); res["n_pairs_U1"] = len(pairs1)
    # random sample of (l,U): U random subset of block\{l}, size uniform 0..min(15,|block|-1)
    pairs_r = []
    for _ in range(n_sample):
        l = far_l[int(rng.integers(len(far_l)))]
        rest = [u for u in blocks[bid[l]] if u != l]
        k = int(rng.integers(0, len(rest) + 1))
        U = tuple(sorted(rng.choice(rest, size=k, replace=False).tolist())) if k else ()
        pairs_r.append((l, U))
    hr = hs.h_pairs(pairs_r)
    res["h_rand_max"] = float(hr.max()); res["n_pairs_rand"] = len(pairs_r)
    # full block complement for every far l (U = block\{l}, size <= 15)
    pairs_f = [(l, tuple(u for u in blocks[bid[l]] if u != l)) for l in far_l]
    hf = hs.h_pairs(pairs_f)
    res["h_fullblock_max"] = float(hf.max())
    # hill-climb search for max_U h_{U,l}: 150 random l + 50 top l by h_U1
    top = {}
    for (l, U), v in zip(pairs1, h1):
        top[l] = max(top.get(l, -1.0), float(v))
    toplist = sorted(top, key=lambda l: -top[l])[:50]
    randl = [far_l[int(i)] for i in rng.integers(0, len(far_l), 150)]
    best_h, best_arg = -1.0, None
    allh = []
    for l in toplist + randl:
        rest = [u for u in blocks[bid[l]] if u != l]
        for rs in range(2):
            cur = set(rng.choice(rest, size=int(rng.integers(0, len(rest) + 1)), replace=False).tolist()) if rest else set()
            hc = hs.h_pairs([(l, tuple(sorted(cur)))])[0]
            while True:
                cands = [cur ^ {u} for u in rest]
                if not cands:
                    break
                hv = hs.h_pairs([(l, tuple(sorted(c))) for c in cands])
                i = int(np.argmax(hv))
                if hv[i] > hc + 1e-12:
                    cur, hc = cands[i], float(hv[i])
                else:
                    break
            allh.append(hc)
            if hc > best_h:
                best_h, best_arg = hc, (l, sorted(cur), dist_to(S0, l))
    res["h_climb_max"] = float(best_h); res["h_climb_arg"] = json.dumps(best_arg)
    res["h_overall_max"] = max(res["h_empty_max"], res["h_U1_max"], res["h_rand_max"], res["h_fullblock_max"], res["h_climb_max"])
    T1 = 2 * math.log(p) + 0.5 * math.log(n)
    T2 = math.log(n + 1) + 2 * math.log(p / max(k0, 1))
    res["thr_2logp_halflogn"] = T1
    res["thr_junk"] = T2
    allv = np.concatenate([h0, h1, hr, hf, np.array(allh)])
    res["n_h_total"] = int(len(allv))
    res["n_h_above_T1"] = int((allv > T1).sum())
    res["n_h_above_junk"] = int((allv > T2).sum())
    return res


# ------------------------------------------------------------------ main per-dataset run
def run(job):
    rho, n, p, seed = job
    t00 = time.time()
    rng = np.random.default_rng(9000 * seed + 31 * n + 17 * p + int(round(rho * 100)))
    idx = np.arange(p)
    Sigma = rho ** np.abs(idx[:, None] - idx[None, :])
    Xr = bc.iid_design_raw(Sigma, n, rng)
    X = bc.standardize_X(Xr)
    S0 = truths(p)
    th = np.zeros(p); th[S0] = THETA4
    y = bc.make_y_std(X, th, 1.0, rng)
    S0 = tuple(S0)
    prob = bc.Problem(X, y)
    dn = d_n(rho, n)
    Qset = set(S0)
    for t in S0:
        Qset |= set(range(max(0, t - dn), min(p - 1, t + dn) + 1))
    Q_replaced = False
    if p < 2 * len(Qset) + 32 * 4 + 1:
        Qset = set(range(p)); Q_replaced = True
    t1 = time.time()
    blocks = bc.partition(X)
    t_part = time.time() - t1
    t1 = time.time()
    info = bc.start_mode(prob, blocks)
    t_start = time.time() - t1
    mode = tuple(info.mode)
    ell_n = bc.ell_cap(n, p)
    extras = sorted(set(mode) - set(S0))
    missing = sorted(set(S0) - set(mode))
    outQ = [j for j in mode if j not in Qset]
    r = dict(rho=rho, n=n, p=p, seed=seed, B=bc.block_size(n, p), K=prob.K, nblocks=len(blocks), d_n=dn, Q_size=len(Qset),
             Q_replaced=Q_replaced, S0=json.dumps(list(S0)),
             start=json.dumps(list(mode)), start_size=len(mode), n_extra=len(extras), n_missing=len(missing),
             a_S0_in_start=(len(missing) == 0), a_start_in_Q=(len(outQ) == 0),
             missing=json.dumps(missing), outQ=json.dumps(outQ),
             outQ_dist=json.dumps([dist_to(S0, j) for j in outQ]), extras_dist=json.dumps([dist_to(S0, j) for j in extras]),
             n_optimal_start=info.n_optimal, start_truncated=info.truncated,
             t_part=round(t_part, 1), t_start=round(t_start, 1))
    # ---- (c) LS0 paths
    FS0 = prob.F(S0); Fmode = prob.F(mode)
    r["F_S0_minus_F_start"] = FS0 - Fmode
    r["ell_n"] = ell_n
    for name, cap in (("ell", ell_n), ("ellplus", ell_n + len(mode))):
        ls = bc.local_search(prob, mode, cap)
        path = ls["path"]
        toks = [tok(path[i], path[i + 1], S0) for i in range(len(path) - 1)]
        r["c_%s_cap" % name] = cap
        r["c_%s_moves" % name] = ls["moves"]
        r["c_%s_final_eq_S0" % name] = (ls["final"] == S0)
        r["c_%s_S0_scored" % name] = (S0 in ls["scored"])
        r["c_%s_certified" % name] = ls["certified"]
        r["c_%s_local_limit" % name] = ls["local_limit"]
        r["c_%s_only_delN" % name] = all(t == "-N" for t in toks)
        r["c_%s_moves_eq_extras" % name] = (ls["moves"] == len(extras))
        r["c_%s_seq" % name] = " ".join(toks)
        r["c_%s_final_size" % name] = len(ls["final"])
    r["c_unc_final"] = ""; r["c_unc_moves"] = ""
    # also unconstrained-length path (cap 1000) to see where the search ends if the capped ones fail
    if not (r["c_ellplus_final_eq_S0"] and r["c_ellplus_certified"]):
        ls = bc.local_search(prob, mode, 1000)
        r["c_unc_final"] = json.dumps(list(ls["final"])); r["c_unc_moves"] = ls["moves"]
    # ---- (b) NA
    t1 = time.time()
    r.update(na_test(prob, S0, Qset, rng))
    r["t_na"] = round(time.time() - t1, 1)
    # ---- (d) far nulls
    t1 = time.time()
    r.update(far_test(prob, blocks, Qset, S0, max(len(mode), 1), rng))
    r["t_far"] = round(time.time() - t1, 1)
    r["t_total"] = round(time.time() - t00, 1)
    return r


def key_of(r):
    return (float(r["rho"]), int(r["n"]), int(r["p"]), int(r["seed"]))


def main():
    import argparse
    from multiprocessing import Pool
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default="0,1,2,3")
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--out", default="G1_raw.csv")
    a = ap.parse_args()
    global RAW
    RAW = os.path.join(HERE, a.out)
    rows = [ROWS[int(i)] for i in a.rows.split(",")]
    done = set()
    if os.path.exists(RAW):
        with open(RAW, newline="") as f:
            for rr in csv.DictReader(f):
                done.add(key_of(rr))
    jobs = [(rho, n, p, s) for (n, p) in rows for rho in RHOS for s in range(a.seeds) if (rho, n, p, s) not in done]
    print("jobs:", len(jobs), flush=True)
    header = None
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(run, jobs):
            new = not os.path.exists(RAW)
            with open(RAW, "a", newline="") as f:
                if new:
                    w = csv.DictWriter(f, fieldnames=list(r.keys())); w.writeheader()
                    header = list(r.keys())
                else:
                    with open(RAW, newline="") as g:
                        header = next(csv.reader(g))
                    w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
                w.writerow(r)
            print("done", key_of(r), "t=%.0fs" % r["t_total"], "start", r["start_size"], "viol_in", r["a_S0_in_start"], r["a_start_in_Q"],
                  "naF %.2f %.2f" % (r["na_max_near"], r["na_max_far"]), "h %.1f/%.1f" % (r["h_overall_max"], r["thr_2logp_halflogn"]), flush=True)


if __name__ == "__main__":
    main()
