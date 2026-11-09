"""N1: exact-Gram S5 (and factor) designs: start mode composition + uncapped LS0 path statistics.
usage: python n1_run.py design p c n seed0 nseeds outcsv"""
import sys, time, math, json, numpy as np
import bvs_core as bc, fac_core as fc

def design(name, p):
    if name == "S5":
        return fc.s5_sigma(p)
    if name.startswith("F1"):   # one factor, loading^2 = r, diag Psi
        r = float(name[2:]) if len(name) > 2 else 0.3
        return fc.factor_sigma(p, math.sqrt(r) * np.ones(p), (1 - r) * np.ones(p))
    if name.startswith("F2"):   # two factors: alternating loadings
        r = 0.3
        L = np.zeros((p, 2)); L[:, 0] = math.sqrt(r); L[::2, 1] = math.sqrt(0.2); L[1::2, 1] = -math.sqrt(0.2)
        return fc.factor_sigma(p, L, (1 - r - 0.2) * np.ones(p))
    raise ValueError(name)

def run(name, p, c, n, seed):
    Sigma, Lam, Psi = design(name, p)
    th, S0 = fc.study_layout(p, c)
    rng = np.random.default_rng(1000 * seed + 7)
    P = fc.ExactGram(Sigma, th, n, rng, Lam=Lam, Psi=Psi)
    t0 = time.time()
    B = bc.block_size(n, p)
    blocks = bc.partition_from_corr(Sigma, B)
    info = bc.start_mode(P, blocks)
    St = info.mode
    t1 = time.time()
    S0s = set(S0)
    res = dict(design=name, p=p, c=c, n=n, seed=seed, B=B, nblocks=len(blocks), K=P.K,
               start_size=len(St), start_has_S0=S0s <= set(St), start_missing=len(S0s - set(St)),
               start_extras=len(set(St) - S0s), start_is_full=(len(St) == p), start_trunc=info.truncated,
               t_start=round(t1 - t0, 1))
    # extras per block
    bid = bc.block_id_array(blocks, p)
    per = np.bincount(bid[list(set(St) - S0s)], minlength=len(blocks)) if len(set(St) - S0s) else np.zeros(len(blocks), int)
    res["extras_per_block_min"] = int(per.min()); res["extras_per_block_max"] = int(per.max())
    path = fc.ls0_path(P, St, S0)
    st = path["steps"]
    mv = [s.get("move") for s in st if "move" in s]
    res.update(moves=path["moves"], final_is_S0=(path["final"] == tuple(sorted(S0))), scored_S0=path["scored_S0"],
               symdiff=len(set(St) ^ S0s),
               n_delN=mv.count("-N"), n_addN=mv.count("+N"), n_addT=mv.count("+T"), n_delT=mv.count("-T"),
               n_swap=sum(1 for m in mv if m.startswith("sw")),
               max_best_add=max(s["best_add"] for s in st),          # NA margin along path (<0 means NA held)
               max_best_add_over_logn=max(s["best_add"] for s in st) / math.log(n),
               min_best_delN_on_path=min((s["best_del_N"] for s in st if s["extras"] > 0), default=float("nan")),
               max_best_delT=max(s["best_del_T"] for s in st),      # TL margin (truth deletion), <0 good
               max_swapT=max(s["best_swap_T"] for s in st),
               ties=max(s.get("n_ties", 1) for s in st),
               t_path=round(time.time() - t1, 1))
    # where along the path (size) is the NA margin worst
    i = int(np.argmax([s["best_add"] for s in st]))
    res["worst_add_at_size"] = st[i]["size"]
    return res

if __name__ == "__main__":
    name, p, c, n, s0, ns, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(float(sys.argv[4])), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    import csv, os
    rows = []
    for sd in range(s0, s0 + ns):
        r = run(name, p, c, n, sd)
        print(json.dumps(r), flush=True)
        rows.append(r)
    new = not os.path.exists(out)
    with open(out, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new: w.writeheader()
        w.writerows(rows)
