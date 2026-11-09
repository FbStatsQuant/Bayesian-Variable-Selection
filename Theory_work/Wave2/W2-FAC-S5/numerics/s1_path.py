"""S1: diagnostic of the uncapped LS0 path from the full model on exact-Gram BCS (default S5: q=5, rb=.3, rw=.7).
Records per step: move type, gains, noise-space tau statistics, global error e_T, within-group jumps of deleted nulls.
usage: py -3.13 s1_path.py p n seed [q rb rw s0 c] >> S1_raw.jsonl"""
import sys, math, json, time, numpy as np
import bcs_core as B

def run(p, n, seed, q=5, rb=.3, rw=.7, s0=4, c=1.0, J=12, exhaustive=False):
    rng = np.random.default_rng(10007 * seed + p)
    grp = np.arange(p) // q
    th = B.layout(p, q, s0=s0, c=c)
    P = B.BCS(n, grp, rb, rw, th, rng)
    S0 = set(P.S0.tolist())
    isnull = np.ones(p, bool); isnull[P.S0] = False
    path = B.Path(P, np.ones(p, bool))
    logn = math.log(n)
    tau_at_del = np.full(p, np.nan)
    del_level = np.full(p, np.nan)     # d_T at deletion time
    mv = []
    worst = dict(exact_ties=0, add_over_logn=-1e9, swapmargin_over_logn=-1e9, f_ratio=0.0, jump_max=0.0, eT_over_H=0.0,
                 out2_minus_d2_over_logn=-1e9, nonargmin=0, sameg_swap_best=-1e9)
    H = math.sqrt(2 * math.log(2 * p))
    trace = []
    t0 = time.time()
    step = 0
    while True:
        G = path.gains(swaps=True, J=J, exhaustive=exhaustive)
        Tidx, gdel, Oidx, gadd = G["Tidx"], G["gdel"], G["Oidx"], G["gadd"]
        sw, sj, sl = G["swap"]
        best_del = float(gdel.max()) if len(gdel) else -np.inf
        best_add = float(gadd.max()) if len(gadd) else -np.inf
        bestv = max(best_del, best_add, sw)
        nt = path.noise_tau()
        tau = nt["tau"]
        retN = Tidx[isnull[Tidx]]
        outN = Oidx
        dT = float(np.min(np.abs(tau[retN]))) if len(retN) else np.nan
        if len(outN):
            Dout = float(np.max(np.abs(tau[outN])))
            ratio = Dout / dT if len(retN) else np.nan
            jumps = np.abs(tau[outN]) - np.abs(tau_at_del[outN])
            jm = float(np.nanmax(jumps))
        else:
            Dout, ratio, jm = 0.0, 0.0, 0.0
        m = len(retN)
        rec = dict(step=step, k=path.k, m=m, best_del=best_del, best_add=best_add, best_swap=sw,
                   dT=dT, Dout=Dout, eT=float(nt["e_T"]), jump=jm)
        worst["add_over_logn"] = max(worst["add_over_logn"], best_add / logn)
        if m > 0:
            worst["swapmargin_over_logn"] = max(worst["swapmargin_over_logn"], (sw - best_del) / logn)
        if m > 0 and len(outN):
            worst["f_ratio"] = max(worst["f_ratio"], ratio)
            worst["out2_minus_d2_over_logn"] = max(worst["out2_minus_d2_over_logn"], (Dout ** 2 - dT ** 2) / logn)
        worst["jump_max"] = max(worst["jump_max"], jm)
        worst["eT_over_H"] = max(worst["eT_over_H"], abs(nt["e_T"]) * math.sqrt(1 / (1 - rb)) / H)
        if step % max(1, p // 40) == 0 or m < 30:
            trace.append(rec)
        if not bestv > 0:
            break
        # exact ties (R06 item 9): count them; among tied deletions pick the lexicographically smallest resulting set
        nt_types = (best_del == bestv) + (best_add == bestv) + (sw == bestv)
        n_tied_del = int(np.sum(gdel == best_del)) if len(gdel) else 0
        if nt_types > 1 or n_tied_del > 1:
            worst["exact_ties"] = worst.get("exact_ties", 0) + 1
        if bestv == best_del:
            j = int(Tidx[gdel == best_del].max())   # removing the largest tied index gives the lex-smallest set
            if isnull[j] and len(retN):
                jmin = int(retN[np.argmin(np.abs(tau[retN]))])
                if jmin != j:
                    worst["nonargmin"] += 1
                tau_at_del[j] = tau[j]
                del_level[j] = dT
            mv.append("-N" if isnull[j] else "-T")
            path.apply("del", j=j)
        elif bestv == best_add:
            l = int(Oidx[int(np.argmax(gadd))])
            mv.append("+N" if isnull[l] else "+T")
            path.apply("add", l=l)
        else:
            mv.append("sw")
            tau_at_del[sj] = tau[sj]
            path.apply("swap", j=sj, l=sl)
        step += 1
        if step > 3 * p:
            break
    final = set(np.flatnonzero(path.inT).tolist())
    return dict(p=p, n=n, seed=seed, exhaustive_swaps=exhaustive, q=q, rb=rb, rw=rw, s0=s0, c=c, alpha=math.log(p) / math.log(n),
                moves=len(mv), n_delN=mv.count("-N"), n_addN=mv.count("+N"), n_delT=mv.count("-T"),
                n_addT=mv.count("+T"), n_swap=mv.count("sw"), final_is_S0=(final == S0),
                pure_deletion=(mv.count("-N") == len(mv)), secs=round(time.time() - t0, 1), **worst,
                trace=trace)

if __name__ == "__main__":
    a = sys.argv[1:]
    p, n, seed = int(a[0]), int(float(a[1])), int(a[2])
    kw = {}
    if len(a) > 3: kw["q"] = int(a[3])
    if len(a) > 4: kw["rb"] = float(a[4])
    if len(a) > 5: kw["rw"] = float(a[5])
    if len(a) > 6: kw["s0"] = int(a[6])
    if len(a) > 7: kw["c"] = float(a[7])
    if len(a) > 8: kw["exhaustive"] = (a[8] == "exh")
    r = run(p, n, seed, **kw)
    print(json.dumps(r))
