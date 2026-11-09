"""n1_approx_innov.py -- approximate innovations (NA lemma) numerics.
For design in L1,L2,L3,L4; n in {500,2000,8000}; p=200; seeds 1..5.
Q = S0 u {l: min_k |l-k|<=6}; 300 lattice sets T (S0 <= T <= Q): random subsets (prob 1/2 each element of Q\\S0) + T=S0 + T=Q.
Candidates l not in T: l in Q or within distance 10 of Q, plus 50 random far l (distance>10 from Q).
For r in {0,1,2,3,5,8}: T' = {t in T: |t-l|<=r}; e = W_l - W_T' beta_T' (beta from Sigma); g = C e;
Z' = g'eps/||g||  (sigma=1);  Z = u'eps, u = normalised residual of x_l on X_T (exact).
Uses Gram identities (M = centred raw design, A = M'M, c = M'eps):  r_{T,l}=M_l-M_T b,  u'ghat = ||r||/||g||,
 ||u-ghat||^2 = 2-2||r||/||g||  (sd of Z-Z' given the design),  Z-Z' realised with a fixed eps.
Population quantity: Var(E[W_l|W_T]-E[W_l|W_T']) = v(T')-v(T), v(T)=Sigma_ll-Sigma_lT Sigma_TT^-1 Sigma_Tl.
"""
import sys, os, time, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n0_common import *
from multiprocessing import Pool

P = 200
NS = (500, 2000, 8000)
SEEDS = (1, 2, 3, 4, 5)
DESIGNS = ("L1", "L2", "L3", "L4")
RS = (0, 1, 2, 3, 5, 8)
NT = 300


def lattice(did, seed, S0, p):
    rng = rng_for(2, did, 0, p, seed)       # same T-sets for all n
    S0a = np.array(S0)
    dist = np.abs(np.arange(p)[:, None] - S0a[None, :]).min(axis=1)
    Q = np.flatnonzero(dist <= 6)
    near = np.flatnonzero(dist <= 16)        # Q or within 10 of Q  (Q has radius 6)
    far = np.flatnonzero(dist > 16)
    rest = np.array([j for j in Q if j not in set(S0)])
    Ts = [tuple(S0), tuple(Q.tolist())]
    for _ in range(NT - 2):
        m = rng.random(len(rest)) < 0.5
        Ts.append(tuple(sorted(S0 + tuple(rest[m].tolist()))))
    cand = []
    for T in Ts:
        Tset = set(T)
        L = [l for l in near if l not in Tset]
        fr = [l for l in far if l not in Tset]
        sel = rng.choice(fr, size=min(50, len(fr)), replace=False).tolist()
        cand.append((np.array(L + sel, dtype=np.int64), len(L)))
    return Ts, cand


def job(args):
    did, n, seed = args
    t0 = time.time()
    p = P
    Sigma, _ = sigma_of(did, n, p)
    idx, th = truths_of(did, n, p)
    S0 = tuple(sorted(idx))
    rng = rng_for(1, did, n, p, seed)
    W = bc.iid_design_raw(Sigma, n, rng)
    M = W - W.mean(axis=0)
    eps = rng.standard_normal(n)
    A = M.T @ M
    ce = M.T @ eps
    Ts, cands = lattice(did, seed, S0, p)
    pop_cache = {}

    def popbeta(Tp, l):
        key = (Tp, l)
        v = pop_cache.get(key)
        if v is None:
            if len(Tp) == 0:
                v = (np.zeros(0), 1.0)
            else:
                ta = np.array(Tp)
                b = np.linalg.solve(Sigma[np.ix_(ta, ta)], Sigma[ta, l])
                v = (b, 1.0 - float(Sigma[ta, l] @ b))
            pop_cache[key] = v
        return v

    # records[r] -> lists
    rec = {r: dict(dz=[], sd=[], pv=[], near=[], rat=[], nout=[]) for r in RS}
    for T, (L, nnear) in zip(Ts, cands):
        ta = np.array(T)
        ATT = A[np.ix_(ta, ta)]
        ATL = A[np.ix_(ta, L)]
        B = np.linalg.solve(ATT, ATL)
        rr2 = A[L, L] - (ATL * B).sum(axis=0)
        zex = (ce[L] - ce[ta] @ B) / np.sqrt(rr2)
        # population v(T)
        PB = np.linalg.solve(Sigma[np.ix_(ta, ta)], Sigma[np.ix_(ta, L)])
        vT = 1.0 - (Sigma[np.ix_(ta, L)] * PB).sum(axis=0)
        for k, l in enumerate(L):
            dl = np.abs(ta - l)
            for r in RS:
                Tp = tuple(ta[dl <= r].tolist())
                beta, vTp = popbeta(Tp, int(l))
                if len(Tp):
                    tp = np.array(Tp)
                    gn2 = A[l, l] - 2.0 * beta @ A[tp, l] + beta @ A[np.ix_(tp, tp)] @ beta
                    ge = ce[l] - beta @ ce[tp]
                else:
                    gn2 = A[l, l]
                    ge = ce[l]
                zp = ge / math.sqrt(gn2)
                ratio = min(1.0, math.sqrt(rr2[k] / gn2))
                sd = math.sqrt(max(0.0, 2.0 - 2.0 * ratio))
                R = rec[r]
                R["dz"].append(abs(zex[k] - zp))
                R["sd"].append(sd)
                R["pv"].append(max(0.0, vTp - vT[k]))
                R["near"].append(k < nnear)
                nout = len(ta) - len(Tp)
                R["nout"].append(nout)
                R["rat"].append(sd / math.sqrt(max(nout, 1) / n) if nout > 0 else 0.0)
    rows = []
    for r in RS:
        R = rec[r]
        dz, sd, pv, nr, rat, nout = (np.array(R[q]) for q in ("dz", "sd", "pv", "near", "rat", "nout"))
        row = dict(design=did, n=n, seed=seed, r=r, npairs=len(dz),
                   max_dz=dz.max(), med_dz=float(np.median(dz)), q99_dz=float(np.quantile(dz, 0.99)),
                   max_sd=sd.max(), med_sd=float(np.median(sd)), q99_sd=float(np.quantile(sd, 0.99)),
                   max_pv=pv.max(), med_pv=float(np.median(pv)),
                   max_dz_near=dz[nr].max(), max_sd_near=sd[nr].max(), max_pv_near=pv[nr].max(),
                   max_dz_far=dz[~nr].max(), max_sd_far=sd[~nr].max(), max_pv_far=pv[~nr].max(),
                   max_sd_over_sqrt_nout_n=rat.max(), med_sd_over_sqrt_nout_n=float(np.median(rat[nout > 0])) if (nout > 0).any() else 0.0,
                   mean_nout=float(nout.mean()),
                   secs=round(time.time() - t0, 1))
        rows.append(row)
    return rows


if __name__ == "__main__":
    t00 = time.time()
    jobs = [(d, n, s) for n in NS[::-1] for d in DESIGNS for s in SEEDS]
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        jobs = [("L4", 500, 1)]
    with Pool(7) as pool:
        out = []
        for rows in pool.imap_unordered(job, jobs):
            out.extend(rows)
            print(rows[0]["design"], rows[0]["n"], rows[0]["seed"], "done", rows[0]["secs"], flush=True)
    here = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(here, "n1_test.csv" if len(sys.argv) > 1 else "n1_results.csv")
    keys = list(out[0].keys())
    out.sort(key=lambda r: (r["design"], r["n"], r["seed"], r["r"]))
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(out)
    print("total secs", round(time.time() - t00, 1))
