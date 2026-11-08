"""E7b (extra, beyond spec; lighter than first attempt p=300/d=200 which was too slow and was aborted): p=160, d=80, n in {800,3200}, 5 seeds."""
import time, json
import exp_common as ec, e7_proxy_flood as e7
if __name__ == "__main__":
    t0 = time.time()
    rows = ec.pmap(e7.job, [(160, 80, n, s) for n in (800, 3200) for s in range(5)])
    ec.write_rows(rows, "E7b")
    summ = e7.summarise(rows, ["p", "d", "n"])
    open("E7b_summary.md", "w").write("### E7b (extra, beyond the spec): p=160, d=80, 5 seeds per row\n\n" + ec.md_table(summ, e7.COLS))
    print(open("E7b_summary.md").read()); print("secs", time.time() - t0)
