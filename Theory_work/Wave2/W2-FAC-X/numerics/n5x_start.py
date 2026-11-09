"""N5X: falsification of lemmas/X5 (start mode = [p] minus N0) for iid CS rows, exact sufficient statistics (Bartlett),
production partition (bvs_core.partition_from_corr on the sample correlation, B = block_size) and start-mode routine.
Output N5X_out.txt"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import math, json, numpy as np
from multiprocessing import Pool
import iid_core as ic, bvs_core as bc

def run(job):
    rho, n, p, layout, seed = job
    rng = np.random.default_rng(31 * seed + p + 5)
    beta = np.zeros(p)
    if layout == "spread":
        idx = np.linspace(2, p - 3, 4).astype(int); beta[idx] = [1.4, -1.0, 1.8, -1.2]
    elif layout == "s1":
        beta[7] = 1.2
    else:  # two strong truths, opposite signs
        beta[[3, 40]] = [1.5, -0.9]
    P = ic.IidData(math.sqrt(rho) * np.ones(p), beta, n, rng)
    R = P.XtX / (n - 1.0)
    B = bc.block_size(n, p)
    blocks = bc.partition_from_corr(R, B)
    S0 = set(P.S0)
    N0 = set()
    for C in blocks:
        if S0 <= set(C):
            N0 |= set(C) - S0
    info = bc.start_mode(P, blocks)
    St = set(info.mode)
    target = set(range(p)) - N0
    return dict(rho=rho, n=n, p=p, layout=layout, seed=seed, B=B, N0=len(N0), start_size=len(St),
                match=(St == target), has_S0=S0 <= St, missing_from_target=len(target - St), extra=len(St - target),
                n_optimal=getattr(info, "n_optimal", None), truncated=getattr(info, "truncated", None))

if __name__ == "__main__":
    J = [(rho, n, p, lay, s) for rho in (0.3, 0.7) for n in (10 ** 6, 10 ** 8) for p in (60, 150)
         for lay in ("spread", "s1", "pair") for s in range(2)]
    with Pool(7) as pool:
        res = pool.map(run, J)
    lines = [json.dumps(r) for r in res]
    ok = sum(r["match"] for r in res)
    big = [r for r in res if r["n"] == 10 ** 8]
    summ = (f"N5X: start mode == [p] minus N0 in {ok}/{len(res)} data sets; at n = 1e8: "
            f"{sum(r['match'] for r in big)}/{len(big)}; S0 contained in start: {sum(r['has_S0'] for r in res)}/{len(res)}")
    open("N5X_out.txt", "w").write(summ + "\n" + "\n".join(lines) + "\n")
    print(summ)
    for r in res:
        if not r["match"]: print(r)
