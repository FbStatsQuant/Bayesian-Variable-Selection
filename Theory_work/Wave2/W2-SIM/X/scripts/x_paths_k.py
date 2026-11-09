"""x_paths_k.py -- W2-SIM family X, brief questions 3 (k = 2, 3 factors) and 4 (real-data-like covariances).
Same exact sufficient-statistic simulation and production LS0 path as x_paths.py (ticket iid_core / bvs_core imported
unchanged); designs with general loading matrices Lam (p x k), psi_j = 1 - |Lam_j|^2. The one-factor band diagnostics of
x_paths.py do not apply (no scalar centre) and are not computed. Recorded: production start mode (size, == [p] minus N0,
partially selected blocks), and the uncapped LS0 path from the start mode and from [p]: move types, final == S0, moves vs
MR1 cap, max addition gain / log n, ties.
Designs (load=):
  k2blk  : two classes (j mod 2), Lam_j = (sqrt(.5), 0) / (0, sqrt(.5))  [two independent CS blocks]
  k2glob : Lam_j = (0.5, +-0.45) by class j mod 2                         [global + contrast factor]
  k3glob : Lam_j = (0.5, 0.45 cos(2 pi c/3), 0.45 sin(2 pi c/3)), c = j mod 3
  k2gen  : Lam_j1 ~ U(0, .6), Lam_j2 ~ U(-.4, .4), fixed per p (rng 99 + p + 1000 k)
  k3gen  : Lam_j1 ~ U(.2, .6), Lam_j2, Lam_j3 ~ U(-.4, .4), fixed per p
  real:<name> : Sigma = (1 - delta) R + delta I, R = sample correlation of W2-APP data set <name> (riboflavin, fred_md,
                fred_qd), factor form L L' + delta I from make_real_lambda.R (X/data/<name>_L.csv, k = rank R, delta = .1);
                p < p_data: column subset drawn once per (name, p) with SeedSequence([20261109, 77, p, code]) (fixed design,
                rows random), kept in its original order.
Usage: python x_paths_k.py OUT.jsonl load=k2glob n=100000 p=1000 seeds=0-19 [start=both|full|mode] [datadir=...]"""
import os, sys, json, math, time, platform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x_paths as xp           # sets OMP threads, ticket path; provides truth_beta, parse_range, sha
import numpy as np
import iid_core as ic
import bvs_core as bc

LOADS = {"k2blk": 11, "k2glob": 12, "k3glob": 13, "k2gen": 14, "k3gen": 15,
         "real:riboflavin": 21, "real:fred_md": 22, "real:fred_qd": 23}


def loading_matrix(load, p, datadir):
    j = np.arange(p)
    if load == "k2blk":
        L = np.zeros((p, 2)); L[j % 2 == 0, 0] = math.sqrt(.5); L[j % 2 == 1, 1] = math.sqrt(.5); return L, None
    if load == "k2glob":
        return np.c_[np.full(p, .5), np.where(j % 2 == 0, .45, -.45)], None
    if load == "k3glob":
        c = j % 3
        return np.c_[np.full(p, .5), .45 * np.cos(2 * np.pi * c / 3), .45 * np.sin(2 * np.pi * c / 3)], None
    if load == "k2gen":
        g = np.random.default_rng(99 + p + 2000)
        return np.c_[g.uniform(0, .6, p), g.uniform(-.4, .4, p)], None
    if load == "k3gen":
        g = np.random.default_rng(99 + p + 3000)
        return np.c_[g.uniform(.2, .6, p), g.uniform(-.4, .4, p), g.uniform(-.4, .4, p)], None
    if load.startswith("real:"):
        name = load.split(":", 1)[1]
        Lfull = np.loadtxt(os.path.join(datadir, name + "_L.csv"), delimiter=",", ndmin=2)
        pd = Lfull.shape[0]
        if p > pd:
            raise SystemExit(f"p {p} > p_data {pd}")
        if p == pd:
            sub = np.arange(pd)
        else:
            g = np.random.default_rng(np.random.SeedSequence([20261109, 77, p, LOADS[load]]))
            sub = np.sort(g.choice(pd, size=p, replace=False))
        return Lfull[sub], sub
    raise ValueError(load)


def run_one(load, n, p, seed, start_kind, datadir):
    ent = [20261109, 6, LOADS[load], int(n), int(p), int(seed)]
    rng = np.random.default_rng(np.random.SeedSequence(ent))
    Lam, sub = loading_matrix(load, p, datadir)
    beta = xp.truth_beta(p)
    t0 = time.time()
    P = ic.IidData(Lam, beta, n, rng)
    S0 = P.S0; S0s = set(S0)
    psi = 1 - (Lam ** 2).sum(1)
    rec = dict(item="K" if not load.startswith("real") else "REAL", load=load, n=n, p=p, kf=Lam.shape[1],
               A=round(math.log(p) / math.log(n), 4), seed=seed, seed_entropy=ent, s0=len(S0), S0=list(S0),
               psi_min=float(psi.min()), subset_sha=(None if sub is None else xp.hashlib.sha256(sub.tobytes()).hexdigest()),
               t_data=round(time.time() - t0, 1))
    starts = {}
    if start_kind in ("mode", "both"):
        t1 = time.time()
        R = P.XtX / (n - 1.0)
        B = bc.block_size(n, p)
        blocks = bc.partition_from_corr(R, B)
        N0 = set()
        for C in blocks:
            if S0s <= set(C):
                N0 |= set(C) - S0s
        info = bc.start_mode(P, blocks)
        St = sorted(int(v) for v in info.mode)
        Sts = set(St)
        target = sorted(set(range(p)) - N0)
        rec.update(B=B, nblocks=len(blocks), N0=len(N0), mode_size=len(St), C1_start_eq_Sstar=(St == target),
                   start_has_S0=S0s <= Sts, start_missing=len(set(target) - Sts), start_extra=len(Sts - set(target)),
                   start_n_optimal=info.n_optimal, start_truncated=info.truncated, t_start=round(time.time() - t1, 1),
                   start_partial_blocks=[[len(C), sum(1 for v in C if v in Sts), sum(1 for v in C if v in S0s)]
                                         for C in blocks if any(v not in Sts for v in C)],
                   start_log_gamma0_mode=info.log_gamma0_mode,
                   start_log_gamma0_Sstar=(float(bc.log_gamma0(P, blocks, target)) if len(target) <= P.K else None))
        starts["mode"] = St
        if N0:
            starts["oracle_SstarN0"] = target
    if start_kind in ("full", "both"):
        starts["full"] = list(range(p))
    return [xp.path_part(P, dict(rec, path_from=nm), st, S0, None, n, p, do_replay=False) for nm, st in starts.items()]


if __name__ == "__main__":
    outf = sys.argv[1]
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    load = kv["load"]; n = int(float(kv["n"])); p = int(kv["p"])
    seeds = xp.parse_range(kv.get("seeds", "0")); sk = kv.get("start", "both")
    datadir = kv.get("datadir", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
    prov = dict(x_paths_k_sha256=xp.sha(os.path.abspath(__file__)), x_paths_sha256=xp.sha(xp.__file__),
                iid_core_sha256=xp.sha(ic.__file__), bvs_core_sha256=xp.sha(bc.__file__), numpy=np.__version__,
                python=platform.python_version(), host=platform.node(),
                slurm_job=os.environ.get("SLURM_ARRAY_JOB_ID", os.environ.get("SLURM_JOB_ID")),
                slurm_task=os.environ.get("SLURM_ARRAY_TASK_ID"), run_id=os.environ.get("RUN_ID"))
    if load.startswith("real:"):
        prov["L_sha256"] = xp.sha(os.path.join(datadir, load.split(":", 1)[1] + "_L.csv"))
    for s in seeds:
        for r in run_one(load, n, p, s, sk, datadir):
            r["prov"] = prov
            with open(outf, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(load, n, p, s, r["path_from"], r.get("start_size"), r["types"], "S0" if r["final_is_S0"] else "MISS", r["termination"], "numok" if r["numerically_ok"] else "NUMCHECK",
                  "add/logn %.3f t_path %.0f t_start %s" % (r["max_add_gain_over_logn"], r["t_path"], r.get("t_start")),
                  flush=True)
