"""E2: LH exact Gram.  g=9, p=108 (12 groups), c in {1,2}, v=1 visible, (rho,psi) in {(.4,.2),(.7,.5)}, beta=1, sigma^2=1."""
import json, time
import exp_common as ec, lh_common as lc

if __name__ == "__main__":
    t0 = time.time()
    NS = [200, 800, 3200]
    CFG = [(0.4, 0.2), (0.7, 0.5)]
    jobs = [(12, 9, rho, psi, c, n, seed, False) for (rho, psi) in CFG for c in (1, 2) for n in NS for seed in range(20)]
    rows = ec.pmap(lc.job_exact, jobs)
    ec.write_rows(rows, "E2")
    summ = ec.agg(rows, ["rho", "psi", "c", "n"])
    # population checks
    pops = []
    for (rho, psi) in CFG:
        for c in (1, 2):
            for n in NS:
                spec = lc.spec_cached(12, 9, rho, psi, c, n, False)
                d = lc.population_checks(spec, n)
                d.update(rho=rho, psi=psi, c=c)
                pops.append(d)
    json.dump(dict(summary=summ, population=pops), open("E2_summary.json", "w"), indent=1, default=str)
    with open("E2_summary.md", "w") as f:
        f.write("## E2 LH exact Gram -- route statistics (20 noise seeds per row)\n\n")
        f.write(ec.md_table(summ))
        f.write("\n### population checks (blocks = groups)\n\n")
        pp = [{k: (("%.3g" % v) if isinstance(v, float) else v) for k, v in d.items() if k != "Sstar_pop"} for d in pops]
        f.write(ec.md_table(pp, ["rho", "psi", "c", "n", "Sstar_eq_ref", "VIS_margin", "NL_leak", "zeta", "zeta_ratio", "dec", "dec_over_logn", "sep_exhaustive"]))
    print(open("E2_summary.md").read())
    print("secs", time.time() - t0)
