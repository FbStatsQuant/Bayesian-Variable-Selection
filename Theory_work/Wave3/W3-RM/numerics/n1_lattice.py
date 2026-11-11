r"""n1_lattice.py -- W3-RM sharpness probe N1: the lattice condition (N): whole-lattice NA versus the greedy path.
FALSIFICATION PROBE: OBSERVATIONS ONLY, NOT A PROOF; every theorem is asymptotic.  Run:  py -3.13 n1_lattice.py
Imports (does not edit) the ported method objects (bvs_core via rm_common.py).  Output: n1_results.csv.
Seeds fixed: BASE = 20261204; seeds 1..20 per cell (1..10 for C = 8 with n >= 1600, see nseeds_cell()); design rng =
SeedSequence([BASE, ci, n, seed]) (ci = index of C), column-permutation rng = SeedSequence([BASE, 99, ci, seed]),
random-lattice rng = SeedSequence([BASE, 7, ci, n, seed]).

DESIGN (fixed design with EXACT Gram: bc.exact_gram_design, centred columns, X'X = (n-1) Sigma; p = 300 <= n-1).
  S0 = 2 truths (theta = (1, -1)), orthogonal to everything.  P = m columns, mutually orthogonal and orthogonal to S0.
  Every other column l (p - 2 - m of them): x_l = cos(a) w_l + sin(a) m^{-1/2} sum_{t in P} x_t with w_l orthonormal
  innovations, so Corr(x_l, x_t) = sin(a)/sqrt(m), Corr(x_l, x_l') = sin^2(a); tan(a) = 0.64 sqrt(m)/sqrt(2 log p).
  Sigma = V V' for the explicit row-vectors V (hence positive definite; lam_min(Sigma) is recorded: `lam_min`;
  `gram_err` = max |X'X/(n-1) - Sigma| of the realised design).  m = ceil(C log n), C in {0.5, 1, 2, 4, 8}; n in {400, 1600, 6400}.
  Q := S0 u P, lattice L = [S0, Q] (all T with S0 <= T <= Q).  Columns permuted at random per seed.  y = standardised X theta + eps,
  eps ~ N(0, I_n) (sigma = 1), eps kept for the Z statistics.
(i) LATTICE SUP.  Z_{T,l} = u_{T,l}' eps / sigma, u_{T,l} = normalised residual of x_l on X_T, computed exactly from the Gram
  matrix; l ranges over the 'others' (l not in Q), T in the searched family:
    adversarial: for s in {+1,-1}: T_tau = S0 u {t in P : s*ehat_t <= tau}, ehat_t = x_t'eps/||x_t||, tau over ALL m+1 nested
      breakpoints (tau = -inf, then each sorted value s*ehat_t)  -> 2(m+1) sets;
    random: 2000 sets T = S0 u (each P column kept with prob 1/2).
  maxZ2_adv / maxZ2_rand = max over that family and over l of Z^2;  maxZ2_all = max of the two.  c_n' = log(n+1) + 2 log p -
  2 log(|Q|+1) (`cn`);  lat_fail := maxZ2_all > c_n';  lat_fail_2logp := maxZ2_all > 2 log p.
  DIRECT CHECK on the port's F: F-gain of (T, l) for (a) the best l of every adversarial T and (b) the 60 best-Z^2 (T,l) pairs of
  the random family (distinct pairs); na_F_fail := max gain F(T u l) - F(T) > 0 (true NA violation for l not in Q);
  na_F_maxgain = that max.
(ii) [BUDGET: for C = 8 with n >= 1600 only the best adversarial centre A1 is run (A2, A3 columns empty there).]
  LS0 (bc.local_search, COMPLETE scans, shipped cap ell_cap(n,p)+|centre| and, derived from the same path, OLD cap ell_cap(n,p))
  from the centres: Q (prefix Q_), the 3 adversarial T_tau with the largest max_l Z^2 (A1_, A2_, A3_; distinct sets, the
  empty-P set T = S0 is allowed), and the coded start mode (prefix st_; the design has no signal leakage, so the start mode is expected
  to be S0).  Columns per centre: centre_size, moves, final_eq_S0, certified, S0_scored, S0_is_max, move-type counts
  (del_extra / add_truth / add_null / del_truth / swap...), all_del_extra (every move a deletion of a non-truth).
  Definitions in rm_common.py.  `reach_all_del_extra_Q` etc. = final_eq_S0 AND all_del_extra.
"""
import os, sys, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rm_common import bc, np, HERE, start_record, ls_record, write_csv, json   # noqa: E402
from multiprocessing import Pool

BASE = 20261204
CS = [0.5, 1, 2, 4, 8]
P = 300
THETA = (1.0, -1.0)
NSEEDS = 20


def nseeds_cell(C, n):
    """20 seeds per cell, REDUCED to 10 (the minimum) for C = 8 with n >= 1600 (m = 60, 71): complete LS0 scans from centres of
    size ~m+2 are slow (one seed of (C=8, n=6400) took ~290 s single-process), 20 seeds would exceed the ~15-minute budget."""
    # Lead's change after the 17:15 server restart (first full run lost with its log): 10 seeds for every C >= 4 cell
    # (was: 10 only for C = 8, n >= 1600), to keep the re-run within the time budget. 10 is the SPEC's minimum.
    return 10 if C >= 4 else NSEEDS


class Lat:
    """exact Gram algebra for Z_{T,l}"""

    def __init__(self, X, eps, others):
        self.G = X.T @ X
        self.e = X.T @ eps
        self.O = np.array(others, dtype=np.int64)
        self.GO = self.G[:, self.O]
        self.dO = np.diag(self.G)[self.O]
        self.eO = self.e[self.O]

    def z2(self, T):
        T = np.asarray(sorted(T), dtype=np.int64)
        if len(T) == 0:
            return self.eO ** 2 / self.dO
        L = np.linalg.cholesky(self.G[np.ix_(T, T)])
        A = np.linalg.solve(L, self.G[T][:, self.O])
        b = np.linalg.solve(L, self.e[T])
        d = self.dO - (A ** 2).sum(0)
        c = self.eO - A.T @ b
        return c ** 2 / np.maximum(d, 1e-300)


def job(args):
    ci, n, seed = args
    t0 = time.time()
    C = CS[ci]
    p = P
    m = math.ceil(C * math.log(n))
    tana = 0.64 * math.sqrt(m) / math.sqrt(2 * math.log(p))
    a = math.atan(tana)
    sa, ca = math.sin(a), math.cos(a)
    q = 2 + m
    # rows of V: canonical order [S0 (2), P (m), others]
    V = np.zeros((p, p))
    for i in range(q):
        V[i, i] = 1.0
    for l in range(q, p):
        V[l, l] = ca
        V[l, 2:q] = sa / math.sqrt(m)
    Sig0 = V @ V.T
    lam_min = float(np.linalg.eigvalsh(Sig0)[0])
    lab0 = np.array(["truth"] * 2 + ["P"] * m + ["other"] * (p - q))
    lrng = np.random.default_rng(np.random.SeedSequence([BASE, 99, ci, seed]))
    perm = lrng.permutation(p)
    inv = np.empty(p, dtype=int); inv[perm] = np.arange(p)
    Sig = Sig0[np.ix_(perm, perm)]
    lab = lab0[perm]
    S0 = tuple(sorted([int(inv[0]), int(inv[1])]))
    Pidx = [int(inv[i]) for i in range(2, q)]
    others = [int(inv[i]) for i in range(q, p)]
    theta = np.zeros(p); theta[int(inv[0])] = THETA[0]; theta[int(inv[1])] = THETA[1]
    rng = np.random.default_rng(np.random.SeedSequence([BASE, ci, n, seed]))
    X = bc.exact_gram_design(Sig, n, rng)
    gram_err = float(np.abs(X.T @ X / (n - 1.0) - Sig).max())
    eps = rng.standard_normal(n)
    y = bc.standardize_y(X @ theta + eps)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    mode, info, r = start_record(prob, blocks, S0, lab)
    Q = tuple(sorted(set(S0) | set(Pidx)))
    cn = math.log(n + 1) + 2 * math.log(p) - 2 * math.log(len(Q) + 1)
    r.update(dict(C=C, m=m, n=n, p=p, seed=seed, q=len(Q), sin_a=sa, tan_a=tana, lam_min=lam_min, gram_err=gram_err,
                  cn=cn, two_log_p=2 * math.log(p), log_n=round(math.log(n), 3), S0=json.dumps(list(S0)), n_others=len(others)))
    # ---------------- (i) lattice sup
    lat = Lat(X, eps, others)
    ehat = np.array([float(X[:, t] @ eps) / math.sqrt(float(X[:, t] @ X[:, t])) for t in Pidx])
    advT = []
    for s in (+1.0, -1.0):
        vals = s * ehat
        taus = [-np.inf] + sorted(vals.tolist())
        seen = set()
        for tau in taus:
            keep = tuple(sorted(set(S0) | {Pidx[i] for i in range(m) if vals[i] <= tau}))
            if keep in seen:
                continue
            seen.add(keep)
            advT.append((keep, s))
    adv_stats = []                                # (maxZ2, T, l)
    for T, s in advT:
        z2 = lat.z2(T)
        i = int(np.argmax(z2))
        adv_stats.append((float(z2[i]), T, int(others[i])))
    rr = np.random.default_rng(np.random.SeedSequence([BASE, 7, ci, n, seed]))
    rand_stats = []
    for _ in range(2000):
        keep = rr.random(m) < 0.5
        T = tuple(sorted(set(S0) | {Pidx[i] for i in range(m) if keep[i]}))
        z2 = lat.z2(T)
        i = int(np.argmax(z2))
        rand_stats.append((float(z2[i]), T, int(others[i])))
    mz_adv = max(s[0] for s in adv_stats)
    mz_rand = max(s[0] for s in rand_stats)
    mz_all = max(mz_adv, mz_rand)
    zQ = float(lat.z2(Q).max())
    zS0 = float(lat.z2(S0).max())
    r.update(dict(maxZ2_adv=mz_adv, maxZ2_rand=mz_rand, maxZ2_all=mz_all, Z2_at_Q=zQ, Z2_at_S0=zS0, n_adv_sets=len(adv_stats),
                  lat_fail=mz_all > cn, lat_fail_2logp=mz_all > 2 * math.log(p), adv_fail=mz_adv > cn))
    # direct F check
    pairs = {}
    for z, T, l in adv_stats:
        pairs[(T, l)] = z
    for z, T, l in sorted(rand_stats, key=lambda s: -s[0])[:60]:
        pairs.setdefault((T, l), z)
    best_gain, best_z, best_adv = -np.inf, float("nan"), False
    advkeys = {(T, l) for z, T, l in adv_stats}
    n_pos = 0
    for (T, l), z in pairs.items():
        g = prob.F(tuple(sorted(set(T) | {l}))) - prob.F(T)
        n_pos += g > 0
        if g > best_gain:
            best_gain, best_z, best_adv = g, z, (T, l) in advkeys
    r.update(dict(na_F_maxgain=float(best_gain), na_F_fail=bool(best_gain > 0), na_F_n_pairs=len(pairs), na_F_n_pos=int(n_pos),
                  na_F_argmax_Z2=best_z, na_F_argmax_is_adv=bool(best_adv)))
    # ---------------- (ii) LS0 from centres
    centres = [("Q_", Q)]
    top = []
    seenT = set()
    for z, T, l in sorted(adv_stats, key=lambda s: -s[0]):
        if T in seenT:
            continue
        seenT.add(T)
        top.append((z, T))
        if len(top) == 3:
            break
    if C == 8 and n >= 1600:
        top = top[:1]          # budget: only the best adversarial centre A1 is run for C = 8, n >= 1600 (A2, A3 not run)
    for i, (z, T) in enumerate(top):
        centres.append(("A%d_" % (i + 1), T))
        r["A%d_Z2" % (i + 1)] = z
        r["A%d_nP" % (i + 1)] = len(set(T) - set(S0))
    centres.append(("st_", mode))
    skip = set(os.environ.get("N1_SKIP", "").split(",")) - {""}
    for pre, T in centres:
        if pre in skip:
            continue
        t1 = time.time()
        rec, res = ls_record(prob, T, S0, pre)
        r[pre + "centre_size"] = len(T)
        r.update(rec)
        r[pre + "reach_all_del"] = bool(rec[pre + "final_eq_S0"] and rec[pre + "all_del_extra"])
        r[pre + "secs"] = round(time.time() - t1, 1)
    r["secs"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    t_start = time.time()
    only = os.environ.get("N1_ONLY")                # "ci,n"
    cfgs = []
    for ci in range(len(CS)):
        for n in (400, 1600, 6400):
            if only and only != "%d,%d" % (ci, n):
                continue
            for s in range(1, nseeds_cell(CS[ci], n) + 1):
                cfgs.append((ci, n, s))
    cfgs.sort(key=lambda c: -(CS[c[0]] * math.log(c[1])) ** 3)          # heaviest first
    if os.environ.get("N1_TEST"):
        cfgs = cfgs[:int(os.environ["N1_TEST"])]
    print("BASE seed", BASE, "runs", len(cfgs), flush=True)
    jl = os.path.join(HERE, "n1_rows.jsonl")          # incremental store (resume): one JSON row per finished run
    rows = []
    if os.path.exists(jl) and not os.environ.get("N1_TEST"):
        with open(jl) as f:
            rows = [json.loads(l) for l in f if l.strip()]
        done = {(r["C"], r["n"], r["seed"]) for r in rows}
        cfgs = [c for c in cfgs if (CS[c[0]], c[1], c[2]) not in done]
        print("resuming: %d rows already stored, %d runs left" % (len(rows), len(cfgs)), flush=True)
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        for r in pool.imap_unordered(job, cfgs):
            rows.append(r)
            if not os.environ.get("N1_TEST"):
                with open(jl, "a") as f:
                    f.write(json.dumps(r, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + chr(10))
            print("C", r["C"], "n", r["n"], "seed", r["seed"], "m", r["m"], "mode", r["start_size"], "maxZ2", round(r["maxZ2_all"], 1), "cn", round(r["cn"], 1),
                  "naF", r["na_F_fail"], "Q->S0", r.get("Q_final_eq_S0"), "A1->S0", r.get("A1_final_eq_S0"), "secs", r["secs"], flush=True)
    rows.sort(key=lambda r: (r["C"], r["n"], r["seed"]))
    out = os.environ.get("N1_OUT", "n1_results.csv")
    if os.environ.get("N1_TEST"):
        out = "n1_results_test.csv"
    write_csv(os.path.join(HERE, out), rows)
    print("total runtime %.1f s" % (time.time() - t_start))
