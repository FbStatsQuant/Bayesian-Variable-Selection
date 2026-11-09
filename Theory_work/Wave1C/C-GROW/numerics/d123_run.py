"""Driver: python d123_run.py <p> <seeds> <ns comma> <tag>  -> RAW_<tag>.csv (all D1/D2/D3 fields, one row per run)"""
import sys, time
import exp_common as ec
import d_common as d
if __name__ == "__main__":
    p = int(sys.argv[1]); seeds = int(sys.argv[2]); ns = [int(x) for x in sys.argv[3].split(",")]; tag = sys.argv[4]
    t0 = time.time()
    jobs = [(s, p, c, n, seed, True) for s in (2, 5) for c in (1.0, 0.5) for n in ns for seed in range(seeds)]
    rows = ec.pmap(d.run, jobs)
    ec.write_rows(rows, "RAW_" + tag)
    # ec.write_rows appends _raw.csv
    print("rows", len(rows), "secs", round(time.time() - t0, 1))
