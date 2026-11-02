"""W1-EXP Task 4: exact computation of pi0(S0), pi0(S°), pi0(R_d), pi(S0) on the LH family as n grows.

Usage: python3 exp_family.py <config> <design> <reps> <post_reps> <out.json>
  config in {A, A85, B};  design in {gram, random}.
Seeds fixed: seed = 20261102 + 1000*config_id + n_index (one numpy Generator per (config, design, n)).
"""
import json
import math
import sys
import time

import numpy as np

from bvs_exact import (aggregation, block_size_B, exp_prime_remainders, make_blocks, posterior_logmass_all,
                       start_logmass, start_masses, tables, log_w)
from family import lh_sigma, lh_truth, suff_exact_gram, suff_random_design

CONFIGS = {
    # c = 1: groups of 4 (= B at p = 16), S3 within-group 0.7, hub link psi = 0.5
    "A": dict(G=4, g=4, rho=0.7, links=[(0, 1, 0.5)], visible={0: 1.4, 2: 1.8}),
    # same with S4 within-group correlation 0.85
    "A85": dict(G=4, g=4, rho=0.85, links=[(0, 1, 0.5)], visible={0: 1.4, 2: 1.8}),
    # c = 2: p = 20, two linked pairs
    "B": dict(G=5, g=4, rho=0.7, links=[(0, 1, 0.5), (2, 3, 0.5)], visible={0: 1.4, 2: 1.8}),
}
NS = [50, 100, 200, 400, 800, 1600, 3200, 6400, 25600, 102400, 409600, 1638400]
SIGMA = 1.0


def run(cfg_name, design, reps, post_reps, out):
    cfg = CONFIGS[cfg_name]
    G, g = cfg["G"], cfg["g"]
    p = G * g
    Sig, groups = lh_sigma(G, g, cfg["rho"], 0, cfg["links"])
    th, S0, M, Sref = lh_truth(G, g, 0, cfg["links"], cfg["visible"])
    c, s = len(M), len(Sref)
    v = SIGMA ** 2 + th @ Sig @ th
    res = dict(config=cfg_name, design=design, p=p, S0=S0, masked=M, Sref=Sref, c=c, s=s,
               theta=th.tolist(), v=v, lam_min_Sigma=float(np.linalg.eigvalsh(Sig).min()),
               groups=groups, rows=[])
    suff = suff_exact_gram if design == "gram" else suff_random_design
    cid = {"A": 1, "A85": 2, "B": 3}[cfg_name] + (0 if design == "gram" else 10)
    for ni, n in enumerate(NS):
        if design == "gram" and p > n - 1:
            continue
        rng = np.random.default_rng(20261102 + 1000 * cid + ni)
        B = block_size_B(n, p)
        t0 = time.time()
        rows = []
        for rep in range(reps):
            R, r = suff(Sig, th, n, SIGMA, rng)
            bl = make_blocks(R, B) if (design == "random" or rep == 0) else bl
            tabs = tables(bl, R, r, n)
            sm = start_masses(bl, tabs, p, n, S0)
            l0 = start_logmass(bl, tabs, p, n, S0, sm["logZ0"])
            lref = start_logmass(bl, tabs, p, n, Sref, sm["logZ0"])
            q, u, e = aggregation(bl, tabs, Sref, p)
            bound = (1 - q) ** (s + 1) / (1 + e) ** s if q < 1 else 0.0
            Rexp = exp_prime_remainders(bl, R, r, n)
            # chain ratios: masked variables are the only true variables of their blocks, T_i = empty
            blk = {j: b for b, C in enumerate(bl) for j in C}
            chainE = []
            for j in M:
                b = blk[j]
                Ti = frozenset(set(bl[b]) & set(Sref))
                chainE.append(tabs[b][Ti | {j}] - tabs[b][Ti] + 0.5 * math.log(n))
            row = dict(rep=rep, blocks_are_groups=sorted(map(sorted, bl)) == sorted(map(sorted, groups)),
                       log_pi0_S0=l0, Mstat=l0 + c * math.log(p) + 0.5 * c * math.log(n),
                       one_minus_pi0_Sref=-math.expm1(lref), pi0_R0=sm["R"][0], pi0_R1=sm["R"][1],
                       pi0_R2=sm["R"][2], q=q, u=u, e=e, T22i_bound=bound, pi0_Sref=math.exp(lref),
                       exp_max_absR=float(np.abs(Rexp).max()), chainE=chainE)
            if rep < post_reps:
                lp = posterior_logmass_all(R, r, n)
                row["pi_S0"] = math.exp(lp[frozenset(S0)])
            rows.append(row)
        dt = time.time() - t0
        def med(k):
            return float(np.median([x[k] for x in rows]))
        def qt(k, a):
            return float(np.quantile([x[k] for x in rows], a))
        summ = dict(n=n, B=B, reps=reps, seconds=dt,
                    frac_blocks_are_groups=float(np.mean([x["blocks_are_groups"] for x in rows])),
                    med_log10_pi0_S0=med("log_pi0_S0") / math.log(10),
                    Mstat_q05=qt("Mstat", .05), Mstat_med=med("Mstat"), Mstat_q95=qt("Mstat", .95),
                    med_one_minus_pi0_Sref=med("one_minus_pi0_Sref"),
                    q95_one_minus_pi0_Sref=qt("one_minus_pi0_Sref", .95),
                    sqrt_n_times_med_1m_pi0Sref=med("one_minus_pi0_Sref") * math.sqrt(n),
                    med_pi0_R0=med("pi0_R0"), q05_pi0_R0=qt("pi0_R0", .05), med_pi0_R1=med("pi0_R1"),
                    med_pi0_R2=med("pi0_R2"),
                    med_q=med("q"), med_u=med("u"), max_e=float(max(x["e"] for x in rows)),
                    med_T22i_bound=med("T22i_bound"), q05_T22i_bound=qt("T22i_bound", .05),
                    bound_holds_all=bool(all(x["T22i_bound"] <= x["pi0_Sref"] + 1e-12 for x in rows)),
                    max_exp_absR=float(max(x["exp_max_absR"] for x in rows)),
                    chainE_q05=float(np.quantile([max(x["chainE"]) for x in rows], .05)),
                    chainE_q95=float(np.quantile([max(x["chainE"]) for x in rows], .95)))
        pis = [x["pi_S0"] for x in rows if "pi_S0" in x]
        if pis:
            summ.update(med_pi_S0=float(np.median(pis)), min_pi_S0=float(np.min(pis)))
        res["rows"].append(dict(summary=summ, reps=rows))
        print(cfg_name, design, json.dumps({k: (round(v_, 4) if isinstance(v_, float) else v_)
                                            for k, v_ in summ.items()}), flush=True)
        with open(out, "w") as f:
            json.dump(res, f)
    # predicted limit law of Mstat for c = 1 (PROOF SKETCH in REPORT): log[(s+1)p/(2p-s-1)] + (sigma^2/(2v)) chi2_1
    res["Mstat_limit_c1"] = dict(const=math.log((s + 1) * p / (2 * p - s - 1)), scale=SIGMA ** 2 / (2 * v))
    with open(out, "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
