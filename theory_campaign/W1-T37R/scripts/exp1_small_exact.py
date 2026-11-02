"""Exp 1 — exact enumeration of R_2 on small designs mimicking S1-S6 (n = 200).

Design: scenario_covariance(s, p) and truth pattern of gen_dev_data.R with p = 20, s0 = 4, step = 1
(truths 2, 6, 13, 15 (0-based), beta = c*(1.4, -1.0, 1.8, -1.2)), or p = 25, s0 = 5 (adds 0.8).
For every S in R_2 we compute the greedy move M(S) (production rule) and record:
  * literal TD(0,0) strict on R_0, TD(1,0) (sanity: Prop 1 says never),
  * TD'_inf(R_{a,d}) : no spurious local max in R_{a,d} + closure + S0 local max,
  * TD'_P(R_{a,d})   : every greedy move from R_{a,d}\\S0 is a progress move (Phi decreases), S0 local max,
  * path-wise: unbounded greedy from every S in R_{a,d} ends at S0 (and #moves),
  * PD(R_d): S0 strict max of F over R_d,
  * which move class beats the best progress move, with gap and residual-projection coordinates.
p_prior: None (true p) or 500 (penalty-matched to the production p = 500; flagged 'pm500').
Seeds: dataset seed = 1000*scenario + 100000*int(100*c) + rep (+ 7 for p = 25).
Usage: python3 exp1_small_exact.py <p> <reps> <pm(0/1)> > out.json
"""
import sys, json, itertools, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from td_core import Scorer, make_dataset, classify, move_label

PROG = {"add_truth", "del_extra", "swap_extra->truth"}


def region_states(S0, p, d):
    S0 = list(S0)
    nulls = [j for j in range(p) if j not in S0]
    out = []
    for r in range(len(S0) + 1):
        for U in itertools.combinations(S0, r):
            for e in range(d + 1):
                for P in itertools.combinations(nulls, e):
                    out.append(tuple(sorted(U + P)))
    return out


def analyse(X, y, S0, mu, p_prior=None, d=2):
    sc = Scorer(X, y, p_prior=p_prior)
    p = sc.p
    S0t = tuple(sorted(S0)); S0set = set(S0t); s0 = len(S0t)
    states = region_states(S0t, p, d)
    info = {}
    for S in states:
        t, moves, gains = sc.best_move(S)
        labs = [move_label(m, S0set) for m in moves]
        gp = max([g for g, l in zip(gains, labs) if l in PROG], default=-np.inf)
        gn = max([g for g, l in zip(gains, labs) if l not in PROG], default=-np.inf)
        bn = None
        if gn > -np.inf:
            k = max((i for i in range(len(moves)) if labs[i] not in PROG), key=lambda i: gains[i])
            bn = (labs[k], moves[k][1], moves[k][2])
        info[S] = dict(next=None if t is None else moves[t][3], lab=None if t is None else labs[t],
                       gp=float(gp), gn=float(gn), bn=bn, F=sc.F(S),
                       m=len(S0set - set(S)), e=len(set(S) - S0set))
    res = {}
    # literal TD(0,0) strict on R_0 and S0 strict local max
    loc_max = info[S0t]["next"] is None
    res["S0_local_max"] = bool(loc_max)
    if not loc_max:
        res["S0_beaten_by"] = info[S0t]["lab"]
    lit0 = loc_max and all(info[S]["lab"] == "add_truth" and info[S]["gp"] > info[S]["gn"]
                           for S in states if info[S]["e"] == 0 and S != S0t)
    res["literal_TD0"] = bool(lit0)
    # sanity for Prop 1: literal TD(1,0) at S0-j+l
    lit1 = loc_max and all(info[S]["lab"] == "add_truth" and
                           info[S]["gp"] > info[S]["gn"]  # add_truth unique best over all moves
                           for S in states if info[S]["e"] <= 1 and info[S]["m"] >= 1)
    res["literal_TD1_any"] = bool(lit1)
    # first literal-TD0 failures: what beats add-truth at d = 0 states
    fails0 = {}
    for S in states:
        if info[S]["e"] == 0 and S != S0t and info[S]["lab"] != "add_truth":
            fails0[info[S]["lab"] or "local_max"] = fails0.get(info[S]["lab"] or "local_max", 0) + 1
    res["TD0_fail_classes"] = fails0
    # regions
    for (a, dd) in [(s0, 0), (s0, 1), (s0, 2), (1, 1), (2, 1), (2, 2), (1, 2)]:
        R = [S for S in states if info[S]["m"] <= a and info[S]["e"] <= dd]
        Rset = set(R)
        tdinf = loc_max and all(info[S]["next"] is not None and info[S]["next"] in Rset for S in R if S != S0t)
        tdp = loc_max and all(info[S]["lab"] in PROG for S in R if S != S0t)
        pd = all(info[S]["F"] < info[S0t]["F"] for S in R if S != S0t)
        # path-wise: greedy from each S (unbounded, may leave R_2: then compute on the fly)
        ok = 0; maxmoves = 0; tot = 0; badmoves = {}
        for S in R:
            cur, k = S, 0
            while True:
                nx = info[cur]["next"] if cur in info else None
                if cur not in info:
                    t, moves, gains = sc.best_move(cur)
                    nx = None if t is None else moves[t][3]
                if nx is None: break
                cur, k = nx, k + 1
                if k > 200: break
            tot += 1
            if cur == S0t:
                ok += 1; maxmoves = max(maxmoves, k)
                phi = info[S]["m"] + info[S]["e"]
                if k > phi:
                    badmoves["over_phi"] = badmoves.get("over_phi", 0) + 1
        nonprog = {}
        for S in R:
            if S != S0t and info[S]["lab"] not in PROG:
                key = info[S]["lab"] or "local_max"
                nonprog[key] = nonprog.get(key, 0) + 1
        res[f"a{a}_d{dd}"] = dict(n_states=len(R), TDinf=bool(tdinf), TDP=bool(tdp), PD=bool(pd),
                                  path_ok_frac=ok / tot, max_moves=maxmoves, nonprog=nonprog,
                                  over_phi=badmoves.get("over_phi", 0))
    # residual-projection diagnosis of non-progress best moves at states with m >= 1
    diag = []
    G = X.T @ X
    for S in states:
        I = info[S]
        if S == S0t or I["lab"] in PROG or I["m"] == 0 or I["bn"] is None:
            continue
        lab, i_out, j_in = I["bn"]
        T = [x for x in S if x != i_out] if i_out is not None else list(S)
        def delta(T, l):
            if len(T):
                XT = X[:, T]; r = X[:, l] - XT @ np.linalg.lstsq(XT, X[:, l], rcond=None)[0]
            else:
                r = X[:, l]
            u = r / np.linalg.norm(r)
            return float(u @ mu), float(u @ (y - mu))
        mis = sorted(S0set - set(S))
        dj = [delta(list(S), j) for j in mis]
        dl = delta(T, j_in) if j_in is not None else (None, None)
        diag.append(dict(S=list(map(int, S)), lab=lab, gap=I["gn"] - I["gp"], m=I["m"], e=I["e"],
                         delta_missing=[(int(j), a, b) for j, (a, b) in zip(mis, dj)],
                         delta_in=(None if j_in is None else int(j_in), dl[0], dl[1]),
                         out=None if i_out is None else int(i_out)))
    res["diag_examples"] = sorted(diag, key=lambda r: -r["gap"])[:5]
    res["n_nonprog_m_ge1"] = len(diag)
    return res


def main():
    p = int(sys.argv[1]); reps = int(sys.argv[2]); pm = int(sys.argv[3])
    s0 = {20: 4, 25: 5}[p]
    out = []
    t0 = time.time()
    for scen in range(1, 7):
        for c in (1.0, 0.5, 0.25):
            for rep in range(reps):
                seed = 1000 * scen + 100000 * int(100 * c) + rep + (7 if p == 25 else 0)
                X, y, S0, beta = make_dataset(p, scen, c, n=200, seed=seed, s0=s0, step=1)
                # mu on the standardised-y scale: y = C(c X beta + eps)/s_y
                yr = None
                rng = np.random.default_rng(seed)
                # recover mu exactly by re-generating: signal and scale
                from td_core import scenario_covariance
                L = np.linalg.cholesky(scenario_covariance(scen, p))
                Xr = rng.standard_normal((200, p)) @ L.T
                Xs = (Xr - Xr.mean(0)) / Xr.std(0, ddof=1)
                eps = rng.standard_normal(200)
                yraw = c * (Xs @ beta) + eps
                sy = (yraw - yraw.mean()).std(ddof=1)
                sig = c * (Xs @ beta); mu = (sig - sig.mean()) / sy
                r = analyse(X, y, S0, mu, p_prior=(500 if pm else None))
                r.update(scenario=scen, c=c, rep=rep, seed=seed, sigma_star_std=float(1 / sy))
                out.append(r)
        print(f"scenario {scen} done {time.time()-t0:.0f}s", file=sys.stderr)
    json.dump(out, sys.stdout, default=float)


if __name__ == "__main__":
    main()
