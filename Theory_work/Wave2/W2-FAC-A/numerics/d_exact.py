"""d_exact.py -- W2-FAC-A diagnosis D2: exact-Gram designs at large n (n up to 1e7) via fac_exact.
usage: py -3.13 d_exact.py <tag> <design> <ps comma> <ns comma> <seeds> [c] [workers]
Records start mode, uncapped LS0 path, MR1 cap, NA/TL along path, NA on random and one-sided ("adversarial") lattice sets.
writes D2_<tag>_raw.jsonl"""
import sys, json, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import bvs_core as bc
import fac_common as fc
import fac_exact as fe


def run(job):
    design, p, n, c, seed = job
    t0 = time.time()
    Sigma = fc.sigma_of(design, p)
    act, beta = fc.study_truth(4, 5)
    th = np.zeros(p); th[act] = c * beta
    S0 = tuple(int(a) for a in sorted(act))
    rng = np.random.default_rng(424242 + 7 * seed + 13 * p + n % 100003)
    Sroot = fe.sym_sqrt(Sigma)
    z, g = fe.draw_z(Sigma, th, n, 1.0, rng, Sroot)
    noise = Sroot @ g
    fs = fe.ExactFast(Sigma, z, n)
    prob = fe.ExactProb(Sigma, z, n)
    blocks = fe.partition_exact(Sigma, n)
    info = bc.start_mode(prob, blocks)
    St = tuple(int(v) for v in info.mode)
    S0set = set(S0)
    extras = sorted(set(St) - S0set)
    missing = sorted(S0set - set(St))
    ell = bc.ell_cap(n, p)
    r = dict(design=design, mode="exactsim", p=p, n=n, c=c, seed=seed, K=fs.K, B=bc.block_size(n, p), nblocks=len(blocks),
             ell_n=ell, start_size=len(St), n_extra=len(extras), n_missing=len(missing),
             frac_nulls_in=len(extras) / (p - len(S0)), start_is_all=(len(St) == p), start_at_K=(len(St) == fs.K),
             start_trunc=bool(info.truncated), t_start=round(time.time() - t0, 1))
    tr = fc.ls0(fs, St, fc.BIG, S0, diag=True)
    toks = tr["toks"]
    r["unc_moves"] = tr["moves"]
    r["unc_final_eq_S0"] = (tr["final"] == S0)
    for tkn in ("-N", "-T", "+N", "+T", "swN>N", "swN>T", "swT>N", "swT>T"):
        r["n" + tkn] = sum(1 for t in toks if t == tkn)
    r["path_pure_delN"] = all(t == "-N" for t in toks)
    tau = tr["path"].index(S0) if S0 in tr["path"] else -1
    r["tau"] = tau
    r["MR1_cap"] = ell + len(St)
    r["MR1_ok"] = (tau >= 0 and tau - 1 <= ell + len(St))
    r["ell_ok"] = (tau >= 0 and tau - 1 <= ell)
    pdg = tr["pathdiag"]
    nonS0 = [d for d in pdg if d["k"] > len(S0)]
    if pdg:
        r["path_NA_fail"] = sum(1 for d in pdg if max(d["g_addN"], d["g_addT"]) > 0)
        r["path_TL_fail"] = sum(1 for d in pdg if max(d["g_delT"], d["g_swT"]) > 0)
        marg = [d["g_delN"] - max(d["g_addN"], d["g_addT"], d["g_swN"], d["g_delT"], d["g_swT"]) for d in nonS0]
        r["path_min_del_margin"] = float(min(marg)) if marg else None
        r["path_max_add_gain"] = float(max(max(d["g_addN"], d["g_addT"]) for d in pdg))
        r["path_max_sw_gain"] = float(max(d["g_swN"] for d in nonS0)) if nonS0 else None
        r["path_min_delN_gain"] = float(min(d["g_delN"] for d in nonS0)) if nonS0 else None
    # deletion order vs |noise - centre| (two-tail check, CS only meaningful)
    path = tr["path"]
    dels = [next(iter(set(path[i]) - set(path[i + 1]))) for i in range(len(path) - 1) if len(path[i + 1]) == len(path[i]) - 1]
    r["del_order_noise"] = json.dumps([round(float(noise[j]), 3) for j in dels[:400]])
    # lattice NA: random and one-sided sets (only if S0 in start)
    nulls = [j for j in range(p) if j not in S0set]
    if not missing:
        res_r, res_a = [], []
        for _ in range(20):
            m = int(rng.integers(0, len(nulls) + 1))
            E = rng.choice(nulls, size=m, replace=False) if m else []
            T = tuple(sorted(S0set | set(int(e) for e in E)))
            FT, res = fs.scan(T)
            if res.get("add") is not None and len(res["out"]):
                res_r.append(float(res["add"].max() - FT))
        order = sorted(nulls, key=lambda j: -noise[j])
        for m in sorted(set([1, 2, 4, 8, 16, 32, 64, 128, 256, len(nulls) // 2]) & set(range(1, len(nulls)))):
            T = tuple(sorted(S0set | set(order[:m])))
            FT, res = fs.scan(T)
            if res.get("add") is not None:
                res_a.append((m, float(res["add"].max() - FT)))
        r["lat_rand_NA_fail"] = sum(g > 0 for g in res_r)
        r["lat_rand_n"] = len(res_r)
        r["lat_rand_max_add"] = max(res_r) if res_r else None
        r["lat_adv"] = json.dumps(res_a)
        r["lat_adv_NA_fail"] = sum(g > 0 for _, g in res_a)
    r["t_total"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    tag, design = sys.argv[1], sys.argv[2]
    ps = [int(v) for v in sys.argv[3].split(",")]
    ns = [int(float(v)) for v in sys.argv[4].split(",")]
    seeds = int(sys.argv[5])
    c = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
    W = int(sys.argv[7]) if len(sys.argv) > 7 else 7
    jobs = [(design, p, n, c, s) for p in ps for n in ns for s in range(seeds) if p <= n // 2]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=W) as ex:
        rows = list(ex.map(run, jobs, chunksize=1))
    with open("D2_%s_raw.jsonl" % tag, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("rows", len(rows), "secs", round(time.time() - t0, 1))
