"""extra p values for the growth table: python d123_run_extra.py <workers>; writes RAW_p200_raw.csv, RAW_p800_raw.csv incrementally"""
import sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import exp_common as ec
import d_common as d
W = int(sys.argv[1]) if len(sys.argv) > 1 else 4
spec = [  # (p, scen, c, n, seeds, do_empty)
    (200, 5, 1.0, 3200, 10, False), (200, 5, 1.0, 800, 10, True), (200, 5, 1.0, 200, 10, True), (200, 5, 0.5, 3200, 10, False), (200, 5, 0.5, 800, 10, True),
    (200, 2, 1.0, 3200, 10, True), (200, 2, 1.0, 800, 10, True), (200, 2, 1.0, 200, 10, True), (200, 2, 0.5, 3200, 5, True)]
J = [(s, p, c, n, seed, True, de) for p, s, c, n, ns, de in spec for seed in range(ns)]
def main():
    t0 = time.time(); rows = {200: [], 800: []}
    with ProcessPoolExecutor(max_workers=W) as ex:
        futs = {ex.submit(d.run, j): j for j in J}
        for f in as_completed(futs):
            j = futs[f]
            try:
                rows[j[1]].append(f.result())
            except Exception as e:
                print("FAILED", j, repr(e), flush=True); continue
            ec.write_rows(rows[j[1]], "RAW_p%d" % j[1])
            print(sum(len(v) for v in rows.values()), "/", len(J), j, round(time.time() - t0), "s", flush=True)
    print("done", round(time.time() - t0), flush=True)

if __name__ == '__main__':
    main()
