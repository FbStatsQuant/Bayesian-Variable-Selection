"""PKA validation of the replacements (rule 3 of COMMON.md / INFRA.md).  Usage: python validate.py OUT.json [part]
  V1 partition: fast_partition_cs(p,B) == bc.partition_from_corr(Sigma_CS, B)  (exact block lists), B = bc.block_size(n,p).
  V2 start:     fast_start_mode == bc.start_mode(TableAdapter(P), blocks, tie_tol=0): mode, size, log gamma0 (exact ==),
                per-block per-size maxima Mmax (exact ==), on the source partition.
  V3 path:      reference run_path (n1) from the DP start == dense fac_core.ls0_path (bvs_core scorer, explicit Gram):
                final set, move count, F after every move (|diff| < 1e-7); saturated/K-1/DP starts.
  V4 singleton: n3.singleton_start == bc.start_mode(TableAdapter(P), singleton blocks, tie_tol=0).
part in {all, v1, v2, v3, v4}; seeds from pka_lib.seed_for(99, ...) (validation-only keys)."""
import sys, os, math, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pka_lib import *
import fac_core as fc
from types import SimpleNamespace

out_path = sys.argv[1]
part = sys.argv[2] if len(sys.argv) > 2 else "all"
OUT = dict(provenance=provenance(), part=part)


def sigma_cs(p, rho):
    return (1 - rho) * np.eye(p) + rho * np.ones((p, p))


def theta_p1(p):
    th = np.zeros(p)
    th[[2, 26, 53, 75]] = .5 * np.array([1.4, 1, 1.8, 1.2])
    return th


if part in ("all", "v1"):
    rows = []
    for n in (100, 200, 400, 800, 1600):
        for c in (.6, .85, .98):
            p = math.floor(round(c * n, 9))
            B = bc.block_size(n, p)
            for rho in (.2, .5, .8):
                if p > 700 and rho != .5:
                    continue
                t0 = time.time()
                orig = bc.partition_from_corr(sigma_cs(p, rho), B)
                fast = fast_partition_cs(p, B)
                rows.append(dict(n=n, p=p, B=B, rho=rho, equal=orig == fast, nblocks=len(orig),
                                 digest=partition_digest(orig), secs=round(time.time() - t0, 2)))
                print(json.dumps(rows[-1]), flush=True)
                assert orig == fast
    OUT["V1_partition"] = rows

if part in ("all", "v2"):
    rows = []
    cases = [(n, c, rho, rep) for n in (200, 400, 800, 1600) for c in (.6, .85, .98) for rho in (.2, .5, .8)
             for rep in range(2)]
    cases += [(3200, c, .5, rep) for c in (.6, .98) for rep in range(2)] + [(6400, .98, .5, 0)]
    for (n, c, rho, rep) in cases:
        p = math.floor(round(c * n, 9))
        blocks = fast_partition_cs(p, bc.block_size(n, p))
        seed = seed_for(99, 2, n, round(c * 100), round(rho * 10), rep)
        P = cs.CS(rho, theta_p1(p), n, rng=np.random.default_rng(seed))
        t0 = time.time()
        f = fast_start_mode(P, blocks, want_tables=True)
        t1 = time.time()
        sys.setrecursionlimit(10000)
        info = bc.start_mode(TableAdapter(P), blocks, tie_tol=0)
        t2 = time.time()
        Mo = np.full_like(f["Mmax"], -np.inf)
        for bb, tb in enumerate(info.tabs):
            for kk, (idx, lr) in tb.items():
                if kk <= P.K:
                    Mo[bb, kk] = float(lr.max())
        eq = dict(mode=f["mode"] == info.mode, size=f["size"] == info.size,
                  logg0=f["log_gamma0_mode"] == info.log_gamma0_mode,
                  Mmax=bool(np.array_equal(Mo[:, :f["Mmax"].shape[1]], f["Mmax"])
                            and np.all(Mo[:, f["Mmax"].shape[1]:] == -np.inf)))
        rows.append(dict(n=n, p=p, rho=rho, rep=rep, seed=seed, K=P.K, size=f["size"], equal=eq,
                         fallback=f["fallback"], n_optimal_orig=info.n_optimal, fast_s=round(t1 - t0, 2),
                         orig_s=round(t2 - t1, 2)))
        print(json.dumps(rows[-1]), flush=True)
        assert all(eq.values()), eq
    OUT["V2_start"] = rows

if part in ("all", "v3"):
    rows = []
    for (n, p, rho) in ((30, 22, .5), (40, 39, .5), (36, 30, .2), (44, 40, .8), (90, 84, .5)):
        th = np.zeros(p)
        th[[2, 9, 14]] = [.7, .5, .9]
        for rep in range(8):
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
                den = fc.ls0_path(D, st, P.S0)
                ok = ref["final"] == den["final"] and len(ref["moves"]) == den["moves"]
                T = set(st)
                maxdiff = 0.0
                for mv, step in zip(ref["moves"], den["steps"]):
                    if mv[1] is not None: T.remove(mv[1])
                    if mv[2] is not None: T.add(mv[2])
                    maxdiff = max(maxdiff, abs(P.F(tuple(sorted(T))) - step["best"]))
                ok = ok and maxdiff < 1e-7
                rows.append(dict(n=n, p=p, rho=rho, rep=rep, start=kind, size=len(st), K=P.K, moves=len(ref["moves"]),
                                 swaps=sum(m[0].startswith("s") for m in ref["moves"]), ties=ref["info"]["ties"],
                                 match=bool(ok), max_F_diff=maxdiff))
                assert ok, rows[-1]
    OUT["V3_path"] = dict(cases=len(rows), mismatches=sum(not r["match"] for r in rows),
                          size_K_starts=sum(r["size"] == r["K"] for r in rows), swaps=sum(r["swaps"] for r in rows),
                          ties=sum(r["ties"] for r in rows), rows=rows)
    print(json.dumps({k: v for k, v in OUT["V3_path"].items() if k != "rows"}), flush=True)

if part in ("all", "v4"):
    rows = []
    for (n, c) in ((60, .85), (120, .6), (200, .98), (400, .85)):
        p = math.floor(round(c * n, 9))
        for s0c, th0 in ((1, [1.0]), (2, [1.0, -.1])):
            for rep in range(3):
                seed = seed_for(99, 4, n, round(c * 100), s0c, rep)
                th = np.zeros(p); th[:len(th0)] = th0
                P = cs.CS(.5, th, n, rng=np.random.default_rng(seed))
                a = singleton_start(P)
                info = bc.start_mode(TableAdapter(P), [[j] for j in range(p)], tie_tol=0)
                rows.append(dict(n=n, p=p, s0=s0c, rep=rep, size=len(a), equal=a == info.mode))
                assert a == info.mode
    OUT["V4_singleton_start"] = rows

json.dump(OUT, open(out_path, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("DONE", out_path)
