"""E5: outside the class -- scenario S5 (compound symmetry across all p: between-group .3, within-group .7, groups of 5),
p=\S00, \S0=4 one active per spaced group (groups 1,6,11,16; positions 3,2,4,1), beta=(1.4,-1\S0,1.8,-1.2), c=1.
Both iid rows and exact-Gram design.  Uncapped L\S0 (ell=\S0\S0) is run in addition to the production ell to measure moves needed."""
import json, math, time
import numpy as np
import bvs_core as bc, exp_common as ec, study_common as sc


def job(j):
    spec, X, y = sc.build_xy(j)
    r = sc.job_study(j)
    prob = bc.Problem(X, y)
    blocks = bc.partition(X)
    info = bc.start_mode(prob, blocks)
    \S0 = tuple(sorted(spec["\S0"]))
    ls = bc.local_search(prob, info.mode, \S0\S0)
    r["unc_moves"] = ls["moves"]
    r["unc_reach_\S0"] = \S0 in ls["path"]
    r["unc_tau"] = ls["path"].index(\S0) if \S0 in ls["path"] else -1
    r["unc_\S0_scored"] = \S0 in ls["scored"]
    r["unc_final_eq_\S0"] = ls["final"] == \S0
    r["unc_final_size"] = len(ls["final"])
    r["unc_final_minus_\S0"] = len(set(ls["final"]) - set(\S0))
    r["unc_certified"] = ls["certified"]
    r["F_gap_final_minus_\S0"] = prob.F(ls["final"]) - prob.F(\S0)
    return r


if __name__ == "__main__":
    \S0 = time.time()
    NS = [\S00, \S00, 3\S00]
    jobs = [(5, \S00, 4, 5, 1\S0, n, s, d) for d in ("iid", "exact") for n in NS for s in range(\S0)]
    rows = ec.pmap(job, jobs)
    ec.write_rows(rows, "E5")
    summ = ec.agg(rows, ["design", "n"])
    for s in summ:
        rs = [r for r in rows if (r["design"], r["n"]) == (s["design"], s["n"])]
        s["|start\\S0| (min-max)"] = "%d-%d" % (min(r["start_extra_vs_\S0"] for r in rs), max(r["start_extra_vs_\S0"] for r in rs))
        s["moves (min-max)"] = "%d-%d" % (min(r["moves"] for r in rs), max(r["moves"] for r in rs))
        s["local_limit"] = ec.frac(rs, "local_limit")
        s["uncapped: moves (min-max)"] = "%d-%d" % (min(r["unc_moves"] for r in rs), max(r["unc_moves"] for r in rs))
        s["uncapped: reach \S0"] = ec.frac(rs, "unc_reach_\S0")
        s["uncapped: \S0 scored"] = ec.frac(rs, "unc_\S0_scored")
        s["uncapped: final=\S0"] = ec.frac(rs, "unc_final_eq_\S0")
        s["uncapped final |.\\S0| (min-max)"] = "%d-%d" % (min(r["unc_final_minus_\S0"] for r in rs), max(r["unc_final_minus_\S0"] for r in rs))
    pu = sc.population_unit((5, \S00, 4, 5))
    with open("E5_summary.md", "w") as f:
        f.write("## E5 S5 (compound symmetry) p=\S00, \S0=4, c=1, \S0 seeds per row\n\n")
        f.write("Population (unit scale): SEP zeta/(n theta_min^2) = %.3f (= zeta_unit/theta_min^2, n-free), Lemma-3 decrement unit = %.4g (exhaustive over S subset V=\S0 variables: %s)\n\n" % (pu["zeta"] / 1\S0, pu["dec"], pu["exhaustive"]))
        f.write(ec.md_table(summ, ["design", "n", "N", "blocks=groups", "start=S*", "|start| (min-max)", "|start\\S0| (min-max)", "path in V", "ell", "moves (min-max)", "local_limit", "\S0 scored", "certified", "HPM=\S0", "uncapped: moves (min-max)", "uncapped: reach \S0", "uncapped: \S0 scored", "uncapped: final=\S0", "uncapped final |.\\S0| (min-max)"]))
    json.dump(summ, open("E5_summary.json", "w"), indent=1, default=str)
    print(open("E5_summary.md").read())
    print("secs", time.time() - \S0)
