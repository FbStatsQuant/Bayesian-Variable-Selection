"""F-SHARE f1b: exact swap-exit margins of the superset class W(S°) and of W+(S°) on LH (exact Gram, p = 16 / 20).

For every x in W(S°) = {x : S° ⊆ x}, j in S° and l not in x, the uniform/neighbour swap x -> x - j + l leaves W(S°).
Its acceptance at any phi is <= max of the endpoint ratios (Lemma A).  We report
  s1 := max over (x, j, l) of F(x - j + l) - F(x)            (posterior endpoint; want <= -c n)
  s0 := max over (x, j, l) of lg0(x - j + l) - lg0(x)        (start endpoint)
split by whether l lies in unit(j) (proxies / partner) or in another unit, and in the latter case whether l is a
masked hub of another pair (the Remark 3.6 case of PROOF.md: x - j + b' can be posterior-better than x; it is in W+).
Then the exits of W+(S°) := W(S°) ∪ {x - j + b' : x in W(S°), j in S°, b' in M \\ x}: from y = x - j + b' the exits are
deletions of a second S°-member or swaps of one; we report the max endpoint odds of those (want e^{-cn}).
Seeds fixed; 10 noise replicates per n.  Output: results/f1b_swap_margins.txt (+ .json).
"""
import os, sys, json, time
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bvs_core import BVS, suff_stats
from lh_design import lh_config

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")


def unit_of(cfg):
    p, g = cfg["p"], cfg["g"]
    u = np.arange(p) // g
    for (a, b) in cfg["pairs"]:
        u[u == b // g] = a // g
    return u


def run(name, ns, reps=10, seed=20261102):
    cfg = lh_config(name); p = cfg["p"]; unit = unit_of(cfg)
    S0 = cfg["S0"]; Sref = cfg["Sref"]; M = cfg["M"]
    S0m = sum(1 << j for j in S0); Srm = sum(1 << j for j in Sref); Mm = sum(1 << j for j in M)
    rng = np.random.default_rng(seed)
    lines, raw = [], {}
    all_states = np.arange(1 << p, dtype=np.int64)
    for n in ns:
        rows = []
        for r in range(reps):
            z, yy = suff_stats(cfg["R"], cfg["theta"], 1.0, n, rng)
            m = BVS(cfg["R"], z, yy, n, S0)
            ok = np.isfinite(m.lg0) & np.isfinite(m.lg1)
            W = ((all_states & Srm) == Srm) & ok
            xs = all_states[W]
            res = {"n": n, "rep": r}
            # --- swaps out of W(S°)
            best = {"unit_1": -np.inf, "unit_0": -np.inf, "other_1": -np.inf, "other_0": -np.inf,
                    "hub_1": -np.inf, "hub_0": -np.inf}
            for j in Sref:
                xj = xs & ~np.int64(1 << j)
                for l in range(p):
                    if l == j: continue
                    sel = (xs & (1 << l)) == 0
                    if not sel.any(): continue
                    y = xj[sel] | np.int64(1 << l)
                    okk = ok[y]
                    if not okk.any(): continue
                    d1 = (m.lg1[y] - m.lg1[xs[sel]])[okk].max(); d0 = (m.lg0[y] - m.lg0[xs[sel]])[okk].max()
                    key = "unit" if unit[l] == unit[j] else ("hub" if (Mm >> l) & 1 else "other")
                    best[key + "_1"] = max(best[key + "_1"], d1); best[key + "_0"] = max(best[key + "_0"], d0)
            res.update({k: float(v) for k, v in best.items()})
            # --- exits from W+ : states y = x - j + b' (b' masked hub not in x); deletion of a second S° member,
            #     or swap of a second S° member, endpoint odds
            ex1, ex0 = -np.inf, -np.inf
            if len(M) >= 1:
                for j in Sref:
                    for bp in M:
                        sel = (xs & (1 << bp)) == 0
                        ys = (xs[sel] & ~np.int64(1 << j)) | np.int64(1 << bp)
                        ys = ys[ok[ys]]
                        for j2 in Sref:
                            if j2 == j: continue
                            y2 = ys & ~np.int64(1 << j2)
                            ex1 = max(ex1, float((m.lg1[y2] - m.lg1[ys]).max())); ex0 = max(ex0, float((m.lg0[y2] - m.lg0[ys]).max()))
                            for l in range(p):
                                sel2 = (ys & (1 << l)) == 0
                                if not sel2.any() or l == j2: continue
                                y3 = y2[sel2] | np.int64(1 << l)
                                okk = ok[y3]
                                if okk.any():
                                    ex1 = max(ex1, float((m.lg1[y3] - m.lg1[ys[sel2]])[okk].max()))
                                    ex0 = max(ex0, float((m.lg0[y3] - m.lg0[ys[sel2]])[okk].max()))
                        # also: is y = x - j + b' ever posterior-better than x + b'?  (should be <= -cn)
            res["Wplus_exit_1"] = ex1; res["Wplus_exit_0"] = ex0
            # return margin: F(x - j + b') - F(x + b')
            ret = -np.inf
            for j in Sref:
                for bp in M:
                    sel = (xs & (1 << bp)) == 0
                    xb = xs[sel] | np.int64(1 << bp); yb = xb & ~np.int64(1 << j)
                    okk = ok[xb] & ok[yb]
                    if okk.any(): ret = max(ret, float((m.lg1[yb] - m.lg1[xb])[okk].max()))
            res["swapped_minus_complete_1"] = ret
            rows.append(res)
        raw[str(n)] = rows
        def agg(k): return np.array([r[k] for r in rows])
        lines.append(f"== {name} n={n} ({reps} reps): max over x in W(S°), j in S°, l not in x of log-odds of the swap x -> x-j+l")
        for k in ("unit_1", "unit_0", "other_1", "other_0", "hub_1", "hub_0"):
            a = agg(k)
            lines.append(f"   {k:8s}: median {np.median(a):9.2f}  worst {a.max():9.2f}   (per n: {np.median(a)/n:+.4f})")
        for k in ("Wplus_exit_1", "Wplus_exit_0", "swapped_minus_complete_1"):
            a = agg(k)
            lines.append(f"   {k:26s}: median {np.median(a):9.2f}  worst {a.max():9.2f}")
        print("\n".join(lines[-10:]), flush=True)
    return lines, raw


if __name__ == "__main__":
    t0 = time.time()
    L, R = [], {}
    for name, ns in (("LH16", (400, 1600, 6400)), ("LH20", (1600, 6400))):
        l, r = run(name, ns, reps=10 if name == "LH16" else 4)
        L += l; R[name] = r
    L.append(f"total time {time.time()-t0:.0f}s")
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "f1b_swap_margins.txt"), "w").write("\n".join(L) + "\n")
    json.dump(R, open(os.path.join(OUT, "f1b_swap_margins.json"), "w"), indent=1)
    print(L[-1])
