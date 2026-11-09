"""d_run.py -- W2-FAC-A diagnosis D1: start mode, uncapped LS0 path, MR1 cap, NA/TL along the path vs lattice.
usage: py -3.13 d_run.py <tag> <design> <mode> <ps comma> <ns comma> <seeds> [c]
writes D1_<tag>_raw.jsonl (one JSON row per run)."""
import sys, json, time, math
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import bvs_core as bc
import fac_common as fc


def run(job):
    design, mode, p, n, c, seed = job
    t0 = time.time()
    X, y, S0, th = fc.build(design, p, n, c, seed, mode)
    fs = fc.Fast(X, y)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    St = tuple(int(v) for v in info.mode)
    S0set = set(S0)
    extras = sorted(set(St) - S0set)
    missing = sorted(S0set - set(St))
    ell = bc.ell_cap(n, p)
    capMR1 = ell + len(St)
    r = dict(design=design, mode=mode, p=p, n=n, c=c, seed=seed, K=fs.K, B=bc.block_size(n, p), nblocks=len(blocks),
             ell_n=ell, start_size=len(St), n_extra=len(extras), n_missing=len(missing),
             frac_nulls_in=len(extras) / (p - len(S0)), start_is_all=(len(St) == p), start_at_K=(len(St) == fs.K),
             start_trunc=bool(info.truncated), t_start=round(time.time() - t0, 1))
    # nulls per block in start mode
    bid = bc.block_id_array(blocks, p)
    cnt = {}
    for j in extras:
        cnt[int(bid[j])] = cnt.get(int(bid[j]), 0) + 1
    nullblocks = [b for b in range(len(blocks)) if not (set(blocks[b]) & S0set)]
    r["nullblocks"] = len(nullblocks)
    r["nullblocks_with_extra"] = sum(1 for b in nullblocks if cnt.get(b, 0) > 0)
    r["extras_per_nullblock_mean"] = float(np.mean([cnt.get(b, 0) for b in nullblocks])) if nullblocks else 0.0
    t1 = time.time()
    tr = fc.ls0(fs, St, fc.BIG, S0, diag=True)
    toks = tr["toks"]
    r["unc_moves"] = tr["moves"]
    r["unc_final_eq_S0"] = (tr["final"] == S0)
    r["unc_certified"] = tr["certified"]
    for tkn in ("-N", "-T", "+N", "+T", "swN>N", "swN>T", "swT>N", "swT>T"):
        r["n" + tkn] = sum(1 for t in toks if t == tkn)
    r["path_pure_delN"] = all(t == "-N" for t in toks)
    # first index where S0 reached
    tau = tr["path"].index(S0) if S0 in tr["path"] else -1
    r["tau"] = tau
    r["MR1_cap"] = capMR1
    r["MR1_ok"] = (tau >= 0 and tau - 1 <= capMR1)  # S0 scanned as neighbour of state tau-1 (or is centre)
    r["ell_ok"] = (tau >= 0 and tau - 1 <= ell)
    r["tau_minus_extra_plus_missing"] = (tau - len(extras) - len(missing)) if tau >= 0 else None
    pdg = tr["pathdiag"]
    if pdg:
        nonS0 = [d for d in pdg if d["k"] > len(S0)]
        r["path_states_supS0"] = len(pdg)
        r["path_NA_fail"] = sum(1 for d in pdg if max(d["g_addN"], d["g_addT"]) > 0)
        r["path_TL_fail"] = sum(1 for d in pdg if max(d["g_delT"], d["g_swT"]) > 0)
        # margin: best null deletion minus best competing move (add, swap, truth move), on states with extras
        marg = [d["g_delN"] - max(d["g_addN"], d["g_addT"], d["g_swN"], d["g_delT"], d["g_swT"]) for d in nonS0]
        r["path_min_del_margin"] = float(min(marg)) if marg else None
        r["path_min_del_gain"] = float(min(d["g_delN"] for d in nonS0)) if nonS0 else None
        r["path_max_add_gain"] = float(max(max(d["g_addN"], d["g_addT"]) for d in pdg))
        r["path_max_sw_gain"] = float(max(d["g_swN"] for d in nonS0)) if nonS0 else None
        r["path_max_TL_gain"] = float(max(max(d["g_delT"], d["g_swT"]) for d in pdg))
        # where along the path does NA fail (k values)
        r["path_NA_fail_ks"] = json.dumps([d["k"] for d in pdg if max(d["g_addN"], d["g_addT"]) > 0][:20])
    r["t_ls"] = round(time.time() - t1, 1)
    # lattice NA: random sets between S0 and start mode (only when S0 subset of start)
    if not missing and extras:
        rng = np.random.default_rng(99 + seed)
        nfail = 0
        maxg = -np.inf
        nsamp = 30
        for _ in range(nsamp):
            mm = int(rng.integers(0, len(extras) + 1))
            E = rng.choice(extras, size=mm, replace=False) if mm else []
            T = tuple(sorted(set(S0) | set(int(e) for e in E)))
            FT, res = fs.scan(T)
            if res.get("add") is not None:
                g = float(res["add"].max() - FT)
                maxg = max(maxg, g)
                nfail += (g > 0)
        r["lat_NA_fail"] = nfail
        r["lat_nsamp"] = nsamp
        r["lat_max_add_gain"] = maxg
    r["t_total"] = round(time.time() - t0, 1)
    return r


if __name__ == "__main__":
    tag, design, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    ps = [int(v) for v in sys.argv[4].split(",")]
    ns = [int(v) for v in sys.argv[5].split(",")]
    seeds = int(sys.argv[6])
    c = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
    jobs = [(design, mode, p, n, c, s) for p in ps for n in ns for s in range(seeds) if not (mode == "exact" and p > n - 1)]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=int(sys.argv[8]) if len(sys.argv) > 8 else 7) as ex:
        rows = list(ex.map(run, jobs, chunksize=1))
    with open("D1_%s_raw.jsonl" % tag, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("rows", len(rows), "secs", round(time.time() - t0, 1))
