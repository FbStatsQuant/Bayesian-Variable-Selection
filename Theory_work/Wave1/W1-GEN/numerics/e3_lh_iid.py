"""E3: LH-iid (iid Gaussian rows with Sigma_LH), p=108 (12 groups) and p=396 (44 groups of 9; 'p=400' rounded to a multiple of 9)."""
import json, time, sys
import exp_common as ec, lh_common as lc

if __name__ == "__main__":
    t0 = time.time()
    NS = [200, 800, 3200]
    CFG = [(0.4, 0.2), (0.7, 0.5)]
    Gs = [12, 44]
    jobs = [(G, 9, rho, psi, c, n, seed, False) for G in Gs for (rho, psi) in CFG for c in (1, 2) for n in NS for seed in range(20)]
    rows = ec.pmap(lc.job_iid, jobs)
    ec.write_rows(rows, "E3")
    summ = ec.agg(rows, ["p", "rho", "psi", "c", "n"])
    json.dump(summ, open("E3_summary.json", "w"), indent=1, default=str)
    with open("E3_summary.md", "w") as f:
        f.write("## E3 LH-iid -- route statistics (20 seeds per row; iid N(0,Sigma_LH) rows, then standardised)\n\n")
        f.write(ec.md_table(summ))
    print(open("E3_summary.md").read())
    print("secs", time.time() - t0)
