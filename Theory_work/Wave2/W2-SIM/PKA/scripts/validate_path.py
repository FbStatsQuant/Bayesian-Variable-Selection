"""PKA path validation after design review R01 (finding 1).  Usage: python validate_path.py OUT.json part
  v3b: certified_path == reference n1 run_path == brute-force COMPLETE scan, MOVE BY MOVE, plus dense fac_core
       (explicit-Gram bvs_core scorer) final set / move count / F after every move (< 1e-7); DP, size-K, size-(K-1)
       starts.
  v5 : (a) reviewer R01 interior-tie fixture (eps sweep): certified first move == brute force;
       (b) tie-prone designs (z rounded to 0/1 decimals): certified == brute force over the whole path, move by move.
  v6 : P1 production seeds (rho=.5) at n=1600 (all c) and 3200 (c=.85,.98), reps 0-4: brute-force complete scan at
       every tied or near-tied scan (gap2 < 1e-6 max(1,|F|)) of the certified path agrees with the chosen move.
Brute force = all deletions, additions (k<K) and ALL k(p-k) swaps with the same F_stats expressions, exact-equality
ties -> lexicographically smallest resulting set."""
import sys, os, math, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pka_lib import *
import fac_core as fc
from types import SimpleNamespace

out_path, part = sys.argv[1], sys.argv[2]
OUT = dict(provenance=provenance(), part=part)


def sigma_cs(p, rho):
    return (1 - rho) * np.eye(p) + rho * np.ones((p, p))


def theta_p1(p):
    th = np.zeros(p)
    th[[2, 26, 53, 75]] = .5 * np.array([1.4, 1, 1.8, 1.2])
    return th


def brute_choice(P, inT, k, A, B):
    z = P.z
    idx_in, idx_out = np.flatnonzero(inT), np.flatnonzero(~inT)
    zin, zout = z[idx_in], z[idx_out]
    FT = float(P.F_stats(k, A, B))
    Fd = P.F_stats(np.full(len(idx_in), k - 1), A - zin ** 2, B - zin) if k >= 1 else np.array([])
    Fa = P.F_stats(np.full(len(idx_out), k + 1), A + zout ** 2, B + zout) if (k < P.K and len(idx_out)) else np.array([])
    if len(idx_in) and len(idx_out):
        Fs = P.F_stats(np.full((len(idx_in), len(idx_out)), k), (A - zin ** 2)[:, None] + zout[None, :] ** 2,
                       (B - zin)[:, None] + zout[None, :])
    else:
        Fs = np.zeros((0, 0))
    best = max([FT] + [float(x.max()) for x in (Fd, Fa, Fs) if x.size])
    if not best > FT:
        return None, best, 0
    opts = [("-", int(idx_in[i]), None) for i in np.flatnonzero(Fd == best)]
    if len(Fa):
        opts += [("+", None, int(idx_out[i])) for i in np.flatnonzero(Fa == best)]
    if Fs.size:
        opts += [("s", int(idx_in[i]), int(idx_out[j])) for i, j in zip(*np.nonzero(Fs == best))]
    cur = idx_in.tolist()

    def _res(o):
        st = [v for v in cur if v != o[1]] if o[1] is not None else list(cur)
        return tuple(sorted(st + [o[2]])) if o[2] is not None else tuple(st)
    opts.sort(key=_res)
    return opts[0], best, len(opts)


def brute_path(P, start, max_moves=10 ** 6):
    z = P.z
    inT = np.zeros(P.p, bool)
    inT[list(start)] = True
    k = len(start); A = float(z[inT] @ z[inT]); B = float(z[inT].sum())
    moves = []
    while len(moves) < max_moves:
        mv, best, nt = brute_choice(P, inT, k, A, B)
        if mv is None:
            break
        typ, jo, li = mv
        if jo is not None:
            inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]
        if li is not None:
            inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]
        moves.append((jo, li))
    return moves


def pairs(moves):
    return [(m[1], m[2]) for m in moves]


if part == "v3b":
    rows = []
    for (n, p, rho) in ((30, 22, .5), (40, 39, .5), (36, 30, .2), (44, 40, .8), (90, 84, .5), (200, 196, .5)):
        th = np.zeros(p)
        th[[2, 9, 14]] = [.7, .5, .9]
        for rep in range(8 if n < 200 else 4):
            seed = seed_for(99, 3, n, p, round(rho * 10), rep)
            rng = np.random.default_rng(seed)
            P = cs.CS(rho, th, n, rng=rng)
            D = SimpleNamespace(n=n, p=p, K=P.K, XtX=(n - 1) * sigma_cs(p, rho), Xty=P.z, yty=n - 1, nu=P.nu,
                                logw=P.lw, logm0=-P.nu * math.log(.02 + n - 1), cache={})
            D.logm_idx = lambda idx, D=D: bc.Problem.logm_idx(D, idx)
            D.logm_many = lambda sets, D=D: bc.Problem.logm_many(D, sets)
            blocks = fast_partition_cs(p, bc.block_size(n, p))
            dp = fast_start_mode(P, blocks)["mode"]
            starts = dict(dp=dp, K=tuple(sorted(rng.choice(p, P.K, replace=False).tolist())),
                          Km1=tuple(sorted(rng.choice(p, P.K - 1, replace=False).tolist())))
            for kind, st in starts.items():
                ref = run_path(P, st)
                cer = certified_path(P, st)
                bru = brute_path(P, st)
                den = fc.ls0_path(D, st, P.S0)
                T = set(st)
                maxdiff = 0.0
                for mv, step in zip(cer["moves"], den["steps"]):
                    if mv[1] is not None: T.remove(mv[1])
                    if mv[2] is not None: T.add(mv[2])
                    maxdiff = max(maxdiff, abs(P.F(tuple(sorted(T))) - step["best"]))
                r = dict(n=n, p=p, rho=rho, rep=rep, start=kind, size=len(st), K=P.K, moves=len(cer["moves"]),
                         swaps=sum(m[0].startswith("s") for m in cer["moves"]), ties=cer["info"]["ties"],
                         interior_checks=cer["info"]["interior_checks"], termination=cer["termination"],
                         cert_eq_ref=pairs(cer["moves"]) == pairs(ref["moves"]), cert_eq_brute=pairs(cer["moves"]) == bru,
                         dense_final_eq=cer["final"] == den["final"] and len(cer["moves"]) == den["moves"],
                         max_F_diff_dense=maxdiff)
                r["match"] = r["cert_eq_ref"] and r["cert_eq_brute"] and r["dense_final_eq"] and maxdiff < 1e-7
                rows.append(r)
                assert r["match"], r
    OUT["V3b_path"] = dict(cases=len(rows), mismatches=sum(not r["match"] for r in rows),
                           size_K_starts=sum(r["size"] == r["K"] for r in rows), swaps=sum(r["swaps"] for r in rows),
                           ties=sum(r["ties"] for r in rows), rows=rows)
    print(json.dumps({k: v for k, v in OUT["V3b_path"].items() if k != "rows"}), flush=True)

if part == "v5":
    fx = []
    for eps in [1e-15, 3e-15, 1e-14, 3e-14, 1e-13, 3e-13, 1e-12]:
        P = cs.CS(.5, np.r_[1., np.zeros(39)], 60, rng=np.random.default_rng(1))
        P.z[:] = 18.; P.z[:30] = 5.; P.z[0] = 25.; P.z[39] -= eps; P.z[38] += eps
        st = tuple(range(30))
        ref = run_path(P, st, max_moves=1)
        cer = certified_path(P, st, max_moves=1)
        inT = np.zeros(P.p, bool); inT[:30] = True
        bmv, best, nt = brute_choice(P, inT, 30, float(P.z[:30] @ P.z[:30]), float(P.z[:30].sum()))
        fx.append(dict(eps=eps, ref=list(ref["moves"][0]), cert=list(cer["moves"][0]), brute=list(bmv),
                       brute_n_tied=nt, cert_eq_brute=(cer["moves"][0][1], cer["moves"][0][2]) == (bmv[1], bmv[2])))
        print(json.dumps(fx[-1]), flush=True)
        assert fx[-1]["cert_eq_brute"]
    tp = []
    for (n, p) in ((40, 30), (60, 50), (90, 80)):
        for dec in (0, 1):
            for rep in range(6):
                th = np.zeros(p); th[[1, 5]] = [1., .8]
                P = cs.CS(.5, th, n, rng=np.random.default_rng(seed_for(99, 5, n, p, dec, rep)))
                P.z[:] = np.round(P.z, dec)
                rng = np.random.default_rng(rep)
                st = tuple(sorted(rng.choice(p, P.K, replace=False).tolist()))
                cer = certified_path(P, st)
                bru = brute_path(P, st)
                tp.append(dict(n=n, p=p, dec=dec, rep=rep, moves=len(cer["moves"]), ties=cer["info"]["ties"],
                               interior_ties=cer["info"]["interior_ties"], equal=pairs(cer["moves"]) == bru))
                assert tp[-1]["equal"], tp[-1]
    summ = dict(tie_prone_cases=len(tp), with_ties=sum(r["ties"] > 0 for r in tp),
                tie_scans=sum(r["ties"] for r in tp), interior_tie_scans=sum(r["interior_ties"] for r in tp))
    print(json.dumps(summ), flush=True)
    OUT["V5_ties"] = dict(fixture=fx, tie_prone=tp, summary=summ)

if part == "v6":
    rows = []
    cases = [(1600, c, r) for c in (.6, .85, .98) for r in range(5)] + [(3200, c, r) for c in (.85, .98) for r in range(5)]
    for (n, c, rep) in cases:
        p = math.floor(round(c * n, 9))
        blocks = fast_partition_cs(p, bc.block_size(n, p))
        seed = seed_for(1, n, round(c * 100), 5, rep)          # the P1 (rho=.5) production seed of this cell
        P = cs.CS(.5, theta_p1(p), n, rng=np.random.default_rng(seed))
        st = fast_start_mode(P, blocks)["mode"]
        cer = certified_path(P, st)
        ref = run_path(P, st)
        flagged = {tr[0] for tr in cer["trace"] if tr[5] > 1 or tr[6] < 1e-6 * max(1.0, abs(tr[3]))}
        z = P.z
        inT = np.zeros(p, bool); inT[list(st)] = True
        k = len(st); A = float(z[inT] @ z[inT]); B = float(z[inT].sum())
        agree = 0
        for t, (tg, jo, li) in enumerate(cer["moves"]):
            if t in flagged:
                bmv, best, nt = brute_choice(P, inT, k, A, B)
                assert (bmv[1], bmv[2]) == (jo, li), (n, c, rep, t, bmv, (jo, li))
                agree += 1
            if jo is not None:
                inT[jo] = False; k -= 1; A -= z[jo] ** 2; B -= z[jo]
            if li is not None:
                inT[li] = True; k += 1; A += z[li] ** 2; B += z[li]
        rows.append(dict(n=n, p=p, c=c, rep=rep, seed=seed, moves=len(cer["moves"]), ties=cer["info"]["ties"],
                         interior_checks=cer["info"]["interior_checks"], interior_ties=cer["info"]["interior_ties"],
                         near_ties=cer["info"]["near_ties"], flagged_scans=len(flagged), brute_agree=agree,
                         min_gap2=cer["info"]["min_gap2"], cert_eq_ref=pairs(cer["moves"]) == pairs(ref["moves"])))
        print(json.dumps(rows[-1]), flush=True)
    OUT["V6_pilot_scale_ties"] = rows

json.dump(OUT, open(out_path, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("DONE", out_path)
