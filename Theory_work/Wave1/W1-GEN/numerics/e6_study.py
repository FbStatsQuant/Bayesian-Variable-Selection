"""E6: study generator S1..S6 at small scale (p=100: 20 groups of 5, s0=4, step 5), c in {1,.5}, iid rows, n in {200,800,3200};
population checks and route statistics.  Plus population VIS margin at the real study size (p=500, s0=14, step 7, n=200)."""
import json, math, time
import numpy as np
import bvs_core as bc, exp_common as ec, study_common as sc

if __name__ == "__main__":
    t0 = time.time()
    NS = [200, 800, 3200]
    CS = [1.0, 0.5]
    SCEN = [1, 2, 3, 4, 5, 6]
    P, S0N, STEP = 100, 4, 5
    # ---- population: SEP/decrement (unit scale, once per scenario)
    pu = ec.pmap(sc.population_unit, [(s, P, S0N, STEP) for s in SCEN])
    pu = {r["scen"]: r for r in pu}
    # ---- population: blocks (small)
    pb = ec.pmap(sc.population_blocks, [(s, P, S0N, STEP, c, n) for s in SCEN for c in CS for n in NS])
    pop_rows = []
    for r in pb:
        u = pu[r["scen"]]
        c, n = r["c"], r["n"]
        spec = sc.spec_cached(r["scen"], P, S0N, STEP, c)
        thmin = min(abs(spec["theta"][j]) for j in spec["S0"])
        zeta = u["zeta"] * c * c * (n - 1)
        dec = u["dec"] * c * c * (n - 1)
        pop_rows.append(dict(scen=r["scen"], c=c, n=n, B=r["B"], J=r["J"], blocks_eq_groups=r["blocks_eq_groups"],
                             Sstar_size=r["Sstar_size"], Sstar_eq_S0=r["Sstar_eq_S0"], Sstar_missing=r["Sstar_missing"], Sstar_extra=len(r["Sstar_extra"]),
                             Sstar_noise_size=r["Sstar_noise_size"], Sstar_noise_eq_S0=r["Sstar_noise_eq_S0"],
                             blocks_with_2plus_truths=r["blocks_with_2plus_truths"],
                             VIS_margin="%.3g" % r["VIS"], NL_leak="%.3g" % r["NL"],
                             VIS_noise="%.3g" % r["VIS_noise"], NL_noise="%.3g" % r["NL_noise"],
                             zeta="%.3g" % zeta, zeta_over_n_th2="%.3g" % (zeta / (n * thmin ** 2)),
                             dec_over_logn="%.3g" % (dec / math.log(n)), sep_exhaustive=u["exhaustive"]))
    # ---- real study size (population only)
    pr = ec.pmap(sc.population_blocks, [(s, 500, 14, 7, c, 200) for s in SCEN for c in CS])
    real_rows = []
    for r in pr:
        real_rows.append(dict(scen=r["scen"], c=r["c"], n=r["n"], p=r["p"], s0=r["s0"], B=r["B"], J=r["J"],
                              blocks_eq_groups=r["blocks_eq_groups"], Sstar_size=r["Sstar_size"], Sstar_eq_S0=r["Sstar_eq_S0"],
                              Sstar_missing=len(r["Sstar_missing"]), Sstar_extra=len(r["Sstar_extra"]), K=r["K"],
                              Sstar_noise_size=r["Sstar_noise_size"], Sstar_noise_eq_S0=r["Sstar_noise_eq_S0"],
                              VIS_noise="%.3g" % r["VIS_noise"], NL_noise="%.3g" % r["NL_noise"],
                              blocks_with_2plus_truths=r["blocks_with_2plus_truths"],
                              VIS_margin="%.3g" % r["VIS"], NL_leak="%.3g" % r["NL"], VIS_arg=r["VIS_arg"]))
    # ---- route statistics (iid rows)
    jobs = [(s, P, S0N, STEP, c, n, seed, "iid") for s in SCEN for c in CS for n in NS for seed in range(20)]
    rows = ec.pmap(sc.job_study, jobs)
    ec.write_rows(rows, "E6")
    summ = ec.agg(rows, ["scen", "c", "n"])
    for s in summ:
        rs = [r for r in rows if (r["scen"], r["c"], r["n"]) == (s["scen"], s["c"], s["n"])]
        s["start=S0"] = "%d/%d" % (sum(1 for r in rs if r["start_extra_vs_S0"] == 0 and r["start_missing_vs_S0"] == 0), len(rs))
        s["final=S0"] = ec.frac(rs, "final_eq_S0")
        s["|start\\S0| max"] = max(r["start_extra_vs_S0"] for r in rs)
        s["|S0\\start| max"] = max(r["start_missing_vs_S0"] for r in rs)
        s["moves med"] = int(np.median([r["moves"] for r in rs]))
    json.dump(dict(pop_small=pop_rows, real=real_rows, route=summ, unit=pu), open("E6_summary.json", "w"), indent=1, default=str)
    with open("E6_summary.md", "w") as f:
        f.write("## E6 study generator, small scale: p=100 (20 groups of 5), s0=4, active in groups 1,6,11,16 at positions 3,2,4,1, beta=(1.4,-1.0,1.8,-1.2), y = c*X*beta + eps, sigma=1\n\n")
        f.write("### population checks (blocks from the population correlation matrix with B=min(floor sqrt n, floor sqrt p, 16)=10; V = union of the 4 signal groups)\n\n")
        f.write(ec.md_table(pop_rows))
        f.write("\n### route statistics, iid rows, 20 seeds per row\n\n")
        f.write(ec.md_table(summ, ["scen", "c", "n", "N", "blocks=groups", "start=S*", "start=S0", "final=S0", "|start| (min-max)", "|S*|", "start=S*noise", "|S*noise|", "|start\\S0| max", "|S0\\start| max", "path in V", "moves (max)", "moves med", "ell", "S0 scored", "certified", "HPM=S0", "max(1-pi0(S*))"]))
        f.write("\n## E6 real study size (population only, Sigma only): p=500 (100 groups of 5), s0=14, step 7, n=200, B=%d\n\n" % bc.block_size(200, 500))
        f.write(ec.md_table(real_rows))
    print(open("E6_summary.md").read())
    print("secs", time.time() - t0)
