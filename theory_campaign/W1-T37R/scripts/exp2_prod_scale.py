"""Exp 2 — production scale n = 200, p = 500, s0 = 14 (truth() of gen_dev_data.R), S1-S6, c in {1, 0.5}.

Per dataset (Python re-generation with numpy seeds, NOT the R streams of the benchmark):
  A. scan at S0: is S0 a flip/swap local max? if not, which move class beats it (weak-truth deletion,
     null addition, swap). Greedy from S0 (unbounded) -> local max S* with F(S*) - F(S0) (a lower bound on
     the posterior-miss margin; F(S*) > F(S0) certifies a posterior miss: S0 is not the HPM of Omega).
  B. all d = 0 states with m <= 2 (1 + 14 + 91 = 106): class of the greedy move M(S), best progress gain vs best
     non-progress gain (literal TD(0) and TD'_P restricted to R_{2,0}).
  C. sampled masked-type centres S = (S0 - A) + P, |A| = a in {1,2}, |P| = e in {0,1,2}, P drawn from the
     same correlation group as a missing truth ('look-alikes') or uniformly: production local search with
     ell = ceil(log2(n+p+1)) = 10: reached S0? certified? all moves progress? #moves vs Phi; and PD at S
     (F(S) < F(S0)), which by Lemma 0 is necessary.
Seed of dataset = 7_000_000 + 10000*scenario + 1000*int(10*c) + rep; centre sampling rng seed = dataset seed + 1.
Usage: python3 exp2_prod_scale.py <reps> [p] > out.json
"""
import sys, json, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from td_core import Scorer, make_dataset, scenario_covariance


class Fast(Scorer):
    def scan_fast(self, S):
        S = np.array(sorted(S), dtype=int); k = len(S); p = self.p
        mask = np.ones(p, bool); mask[S] = False; out = np.nonzero(mask)[0]
        F0 = self.F(tuple(S))
        blocks = []  # (kind array, i_out, j_in, idx)
        res_g, res_i, res_j = [], [], []
        if k < self.K and len(out):
            idx = np.concatenate([np.repeat(S[None, :], len(out), 0), out[:, None]], 1)
            res_g.append(self.F_batch(idx) - F0); res_i.append(np.full(len(out), -1)); res_j.append(out)
        if k > 0:
            idx = np.array([np.delete(S, t) for t in range(k)]).reshape(k, k - 1)
            res_g.append(self.F_batch(idx) - F0); res_i.append(S.copy()); res_j.append(np.full(k, -1))
            for t in range(k):
                rest = np.delete(S, t)
                idx = np.concatenate([np.repeat(rest[None, :], len(out), 0), out[:, None]], 1)
                res_g.append(self.F_batch(idx) - F0); res_i.append(np.full(len(out), S[t])); res_j.append(out)
        return np.concatenate(res_g), np.concatenate(res_i), np.concatenate(res_j)

    def best(self, S):
        g, i, j = self.scan_fast(S)
        t = int(np.argmax(g))
        if not g[t] > 0:
            return None, g, i, j
        return t, g, i, j


def apply(S, i, j):
    S = set(S)
    if i >= 0: S.discard(int(i))
    if j >= 0: S.add(int(j))
    return tuple(sorted(S))


def lab(i, j, S0set):
    ti = None if i < 0 else (i in S0set)
    tj = None if j < 0 else (j in S0set)
    if ti is None: return "add_truth" if tj else "add_null"
    if tj is None: return "del_truth" if ti else "del_extra"
    if ti and tj: return "swap_truth->truth"
    if ti and not tj: return "swap_truth->null"
    if not ti and tj: return "swap_extra->truth"
    return "swap_null->null"


PROG = {"add_truth", "del_extra", "swap_extra->truth"}


def greedy(sc, S, S0set, ell=None, maxit=60):
    path = [S]; labs = []
    it = 0
    while True:
        t, g, i, j = sc.best(S)
        if t is None:
            return dict(final=S, certified=True, labs=labs, n=len(labs), path=path)
        if ell is not None and len(labs) >= ell:
            return dict(final=S, certified=False, labs=labs, n=len(labs), path=path)
        labs.append(lab(i[t], j[t], S0set)); S = apply(S, i[t], j[t]); path.append(S)
        it += 1
        if it > maxit:
            return dict(final=S, certified=False, labs=labs, n=len(labs), path=path)


def main():
    reps = int(sys.argv[1]); p = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    n = 200
    out = []; t0 = time.time()
    for scen in range(1, 7):
        for c in (1.0, 0.5):
            for rep in range(reps):
                seed = 7_000_000 + 10000 * scen + 1000 * int(10 * c) + rep
                X, y, S0, beta = make_dataset(p, scen, c, n=n, seed=seed)
                sc = Fast(X, y)
                S0t = tuple(int(x) for x in S0); S0set = set(S0t)
                rec = dict(scenario=scen, c=c, rep=rep, seed=seed, ell=sc.ell)
                # A
                t, g, i, j = sc.best(S0t)
                rec["S0_local_max"] = t is None
                if t is not None:
                    rec["S0_beaten_by"] = lab(i[t], j[t], S0set); rec["S0_beaten_gain"] = float(g[t])
                    gr = greedy(sc, S0t, S0set)
                    rec["S0_greedy_end_gain"] = sc.F(gr["final"]) - sc.F(S0t)
                    rec["S0_greedy_end"] = dict(m=len(S0set - set(gr["final"])), e=len(set(gr["final"]) - S0set))
                # weakest truth deletion and best null addition at S0
                dels = [(float(g[q]), int(i[q])) for q in range(len(g)) if j[q] < 0]
                adds = [float(g[q]) for q in range(len(g)) if i[q] < 0]
                rec["S0_best_del_gain"] = max(dels)[0]; rec["S0_best_add_gain"] = max(adds)
                # B: d = 0 states with m <= 2
                classes = {}; gaps = []
                miss_lists = [()] + [(a,) for a in S0t] + [(a, b) for ii, a in enumerate(S0t) for b in S0t[ii + 1:]]
                for A in miss_lists:
                    if not A: continue
                    S = tuple(x for x in S0t if x not in A)
                    t, g, i, j = sc.best(S)
                    L = "local_max" if t is None else lab(i[t], j[t], S0set)
                    classes[L] = classes.get(L, 0) + 1
                    labs_all = [lab(a, b, S0set) for a, b in zip(i, j)]
                    gp = max(gg for gg, l in zip(g, labs_all) if l in PROG)
                    gn = max(gg for gg, l in zip(g, labs_all) if l not in PROG)
                    gaps.append(float(gp - gn))
                rec["d0_classes"] = classes; rec["d0_min_prog_gap"] = min(gaps)
                rec["d0_frac_prog"] = sum(v for k, v in classes.items() if k in PROG) / sum(classes.values())
                # C: sampled masked-type centres
                rng = np.random.default_rng(seed + 1)
                group = (np.arange(p) // 5)
                cents = []
                for a in (1, 2):
                    for e in (0, 1, 2):
                        for kind in ("look", "unif"):
                            if e == 0 and kind == "unif": continue
                            for _ in range(2):
                                A = list(rng.choice(S0t, a, replace=False))
                                nulls = [q for q in range(p) if q not in S0set]
                                if kind == "look":
                                    cand = [q for q in nulls if group[q] in {group[x] for x in A}]
                                else:
                                    cand = nulls
                                P = list(rng.choice(cand, min(e, len(cand)), replace=False)) if e else []
                                S = tuple(sorted([x for x in S0t if x not in A] + [int(q) for q in P]))
                                cents.append((a, e, kind, S))
                cres = []
                for a, e, kind, S in cents:
                    gr = greedy(sc, S, S0set, ell=sc.ell)
                    cres.append(dict(a=a, e=e, kind=kind, PD=sc.F(S) < sc.F(S0t),
                                     reached=gr["final"] == S0t, certified=gr["certified"],
                                     allprog=all(l in PROG for l in gr["labs"]), n=gr["n"], labs=gr["labs"],
                                     end_gain=sc.F(gr["final"]) - sc.F(S0t),
                                     end_m=len(S0set - set(gr["final"])), end_e=len(set(gr["final"]) - S0set)))
                rec["centres"] = cres
                out.append(rec)
                print(f"S{scen} c={c} rep={rep} {time.time()-t0:.0f}s S0lm={rec['S0_local_max']} "
                      f"reach={sum(r['reached'] for r in cres)}/{len(cres)}", file=sys.stderr, flush=True)
    json.dump(out, sys.stdout, default=float)


if __name__ == "__main__":
    main()
