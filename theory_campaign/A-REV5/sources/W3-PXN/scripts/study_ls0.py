"""LS0 on the study design at n = 200: production local search (best strictly improving flip/swap, <= ell moves,
then one scan) started from the exact start mode S~0.  Does it reach / score S0?  Is S0 the endpoint?
Same data as study_n200.py (same seeds; reps 0..R-1).  Output results/study_ls0.jsonl."""
import json, math, sys, time
import numpy as np
from pxn_core import *
import study_n200 as sd


def run(s, p, cc, rep):
    seed = 30000000 + 100000 * s + 1000 * (p == 1000) + 10 * [1.0, 0.5].index(cc) + rep
    rng = np.random.default_rng(seed)
    X = sd.gen_X(s, p, rng)
    act, beta = sd.truth(p)
    th = np.zeros(p); th[act] = beta
    y = cc * (X @ th) + rng.standard_normal(200)
    D = Data(X, y)
    blocks = v3_blocks(D)
    T = Tables(D, blocks)
    L = StartLaw(T)
    S0 = sorted(act.tolist())
    mode, _ = L.start_mode()
    ell = math.ceil(math.log2(D.n + p + 1))
    ls = local_search(D, mode, ell, S0)
    end = list(ls["path"][-1])
    FS0 = log_F(D, [S0])[0]
    return dict(scen=s, p=p, cc=cc, rep=rep, seed=seed, ell=ell, start_dist=len(set(mode) ^ set(S0)),
                moves=len(ls["path"]) - 1, end_is_S0=end == S0, scored_S0=ls["scored_S0"],
                certified=ls["certified"], end_minus_S0_F=float(ls["F"] - FS0),
                end_missing=sorted(set(S0) - set(end)), end_extras=sorted(set(end) - set(S0)),
                path_dist=[len(set(x) ^ set(S0)) for x in ls["path"]])


if __name__ == "__main__":
    scen = [int(a) for a in sys.argv[1].split(",")]
    R = int(sys.argv[2])
    out = open("../results/study_ls0.jsonl", "a")
    for s in scen:
        for p in (500, 1000):
            for cc in (1.0, 0.5):
                for rep in range(R):
                    t0 = time.time()
                    r = run(s, p, cc, rep)
                    out.write(json.dumps(r) + "\n"); out.flush()
                    print(s, p, cc, rep, "dist0", r["start_dist"], "moves", r["moves"], "end=S0", r["end_is_S0"],
                          "scored", r["scored_S0"], "F(end)-F(S0) %.1f" % r["end_minus_S0_F"],
                          "%.0fs" % (time.time() - t0), flush=True)
