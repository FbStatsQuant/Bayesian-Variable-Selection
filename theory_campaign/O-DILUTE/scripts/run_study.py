"""O-DILUTE study run: regenerated study-like datasets (n = 200, p in {500, 1000}, S1-S6, c in {1, 0.5}).

Datasets follow gen_prod_data.R exactly in law (Sigma, truth, standardisation, y = c*X beta + eps, sigma = 1) but use
numpy's RNG (R is not available), so they are not bit-identical to the study files.
Seeds: data seed = 20261102 + 100000*(p==1000) + 1000*s + r.
Usage: python run_study.py <reps> <out.jsonl> [p list] [s list]
"""
import sys, json, time
import numpy as np
import dilute as D

n = 200; B = 14; K = 100; s0 = 14; NU = D.A0 + n / 2

def tables_from(stats, yy, kind, s2=None):
    out = []
    for sz, ld, t in stats:
        lr = D.log_r_v3(ld, t, yy, n) if kind == "v3" else D.log_r_known(ld, t, s2)
        out.append((sz, lr))
    return out

def summarise(tabs, tms, blocks, S0set, p):
    o = D.start_summary(tabs, tms, p, s0, K)
    mode = D.start_mode(tabs, p, K)
    Sm = sorted(sum((D.mask_to_cols(blocks[b], m) for b, m in mode), []))
    o.pop("P")
    o["mode_size"] = len(Sm); o["mode_truths"] = len(S0set & set(Sm)); o["mode_ham"] = len(S0set ^ set(Sm))
    o["mode"] = Sm
    return o

def rss(X, y, S):
    if not S: return float(y @ y)
    b, *_ = np.linalg.lstsq(X[:, S], y, rcond=None); r = y - X[:, S] @ b; return float(r @ r)

def run_one(p, s, r, chol):
    seed = 20261102 + 100000 * (p == 1000) + 1000 * s + r
    X, Ys, act, beta, eps = D.gen_dataset(p, s, seed, n=n, chol=chol)
    blocks = D.make_blocks(X, B)
    S0 = sorted(act.tolist()); S0set = set(S0)
    tms = [sum(1 << i for i, c in enumerate(blk) if c in S0set) for blk in blocks]
    blk_of = {c: bi for bi, blk in enumerate(blocks) for c in blk}
    Sig = D.scenario_covariance(s, p)
    res = []
    ys = {}; sy = {}
    for c in (1.0, 0.5):
        ys[c], sy[c] = D.std_y(Ys[c])
    Ymat = np.c_[ys[1.0], ys[0.5]]
    stats_all = [D.block_stats(X, blk, Ymat, n) for blk in blocks]
    for ci, c in enumerate((1.0, 0.5)):
        y = ys[c]; yy = float(y @ y)
        stats = [(sz, ld, t[:, ci]) for sz, ld, t in stats_all]
        rec = dict(p=p, s=s, r=r, c=c, seed=seed, J=len(blocks),
                   truths_per_block=sorted([bin(m).count("1") for m in tms if m], reverse=True))
        # ---- v3 start
        tabs = tables_from(stats, yy, "v3")
        rec["v3"] = summarise(tabs, tms, blocks, S0set, p)
        # ---- per-truth quantities
        lbf_S0 = D.log_bf_full(X, y, S0, n)
        lw_ratio = float(D.log_w(s0, p) - D.log_w(s0 - 1, p))
        bSig = Sig @ beta; vary = c * c * beta @ bSig + 1.0
        per = []
        for j in S0:
            bi = blocks[blk_of[j]]; mS = tms[blk_of[j]]; ij = bi.index(j)
            lr = tabs[blk_of[j]][1]
            G0 = float(lr[mS] - lr[mS & ~(1 << ij)])              # table keep-j gain
            G1 = lbf_S0 - D.log_bf_full(X, y, [k for k in S0 if k != j], n)   # posterior keep-j gain
            rjy = float(X[:, j] @ y / (n - 1))
            rho2 = float((c * bSig[j]) ** 2 / vary)
            rest = [k for k in S0 if k != j]
            Srr = Sig[np.ix_(rest, rest)]; sjr = Sig[j, rest]
            cv = 1.0 - sjr @ np.linalg.solve(Srr, sjr)           # Var(x_j | x_rest)
            x1 = float(c * c * beta[j] ** 2 * cv / (1.0 + c * c * beta[j] ** 2 * cv))  # pop partial R2 (posterior)
            per.append(dict(j=int(j), beta=float(beta[j]), alone=bin(mS).count("1") == 1, rjy=rjy, rho2=rho2,
                            x1=x1, G0=G0, G1=float(G1), LO0=G0 + lw_ratio, LO1=float(G1) + lw_ratio))
        rec["truths"] = per
        rec["logBF_S0"] = lbf_S0
        rec["d_S0"] = lbf_S0 - rec["v3"]["logr_S0"]
        # Lemma W1 BO formula for d(S0) (uses block t's of S0 only)
        cc = 2 * D.B0 + yy
        xi = [stats[b][2][tms[b]] / cc for b in range(len(blocks)) if tms[b]]
        rec["d_S0_W1"] = float(NU * (np.sum(np.log1p(-np.array(xi))) - np.log1p(-np.sum(xi))))
        rec["R2_S0"] = 1.0 - rss(X, y, S0) / yy
        # ---- common plug-in sigma^2 variants (F-DRAFT candidate)
        s2_or = 1.0 / sy[c] ** 2                                     # oracle sigma^2 on standardised scale
        rec["s2_oracle"] = s2_or
        tk = tables_from(stats, yy, "known", s2_or)
        rec["known_oracle"] = summarise(tk, tms, blocks, S0set, p)
        Sm = rec["v3"]["mode"]; s2 = rss(X, y, Sm) / (n - 1 - len(Sm))
        rec["s2_mode1"] = s2
        tk = tables_from(stats, yy, "known", s2)
        rec["known_mode1"] = summarise(tk, tms, blocks, S0set, p)
        s2i = s2; hist = [s2i]
        for it in range(8):
            Sm_i = rec.get("_tmp", rec["known_mode1"])["mode"]
            if len(Sm_i) >= n - 2: break
            s2n = rss(X, y, Sm_i) / (n - 1 - len(Sm_i))
            hist.append(s2n)
            if abs(s2n - s2i) < 1e-6 * s2i: break
            s2i = s2n
            rec["_tmp"] = summarise(tables_from(stats, yy, "known", s2i), tms, blocks, S0set, p)
        rec["known_iter"] = rec.pop("_tmp", rec["known_mode1"]); rec["s2_iter_hist"] = hist
        # ---- backfit (partial-residual) v3 tables, pilot only
        Sm = rec["v3"]["mode"]; hist = []
        for it in range(3):
            if Sm:
                bh, *_ = np.linalg.lstsq(X[:, Sm], y, rcond=None); bfull = np.zeros(p); bfull[Sm] = bh
            else:
                bfull = np.zeros(p)
            tabs_r = []
            for bi, blk in enumerate(blocks):
                bb = bfull.copy(); bb[blk] = 0.0
                yb = y - X @ bb
                sz, ld, t = D.block_stats(X, blk, yb[:, None], n)
                tabs_r.append((sz, D.log_r_v3(ld, t[:, 0], float(yb @ yb), n)))
            o = summarise(tabs_r, tms, blocks, S0set, p); Sm = o["mode"]
            hist.append(dict(logpi0_S0=o["logpi0_S0"], pi0_R2=o["pi0_R"][2], mode_truths=o["mode_truths"],
                             mode_size=o["mode_size"]))
        rec["resid"] = o; rec["resid_hist"] = hist
        for key in ("v3", "known_oracle", "known_mode1", "known_iter", "resid"):
            rec[key].pop("mode", None)
        res.append(rec)
    return res

if __name__ == "__main__":
    reps = int(sys.argv[1]); out = sys.argv[2]
    plist = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [500, 1000]
    slist = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [1, 2, 3, 4, 5, 6]
    with open(out, "a") as f:
        for p in plist:
            for s in slist:
                chol = np.linalg.cholesky(D.scenario_covariance(s, p))
                for r in range(1, reps + 1):
                    t0 = time.time()
                    for rec in run_one(p, s, r, chol):
                        f.write(json.dumps(rec) + "\n")
                    f.flush()
                    print(p, s, r, "%.1fs" % (time.time() - t0), flush=True)
