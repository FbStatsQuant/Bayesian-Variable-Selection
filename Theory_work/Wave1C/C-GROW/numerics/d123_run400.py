"""p = 400 driver (incremental CSV writes, expensive jobs first).  python d123_run400.py"""
import time, csv, json
from concurrent.futures import ProcessPoolExecutor, as_completed
import exp_common as ec
import d_common as d

def jobs():
    J = []
    # (scen, c, n, seeds, do_empty)
    spec = [(5, 1.0, 3200, 7, False), (5, 0.5, 3200, 0, False), (5, 1.0, 800, 10, False), (5, 0.5, 800, 10, False),
            (5, 1.0, 200, 10, True), (5, 0.5, 200, 10, True),
            (2, 1.0, 12800, 5, True), (2, 1.0, 3200, 10, True), (2, 1.0, 800, 10, True), (2, 1.0, 200, 10, True),
            (2, 0.5, 3200, 10, True), (2, 0.5, 800, 10, True), (2, 0.5, 200, 10, True)]
    for scen, c, n, ns, de in spec:
        for seed in range(ns):
            J.append((scen, 400, c, n, seed, True, de))
    return J

if __name__ == "__main__":
    t0 = time.time()
    J = jobs()
    rows = []
    with ProcessPoolExecutor(max_workers=7) as ex:
        futs = {ex.submit(d.run, j): j for j in J}
        for f in as_completed(futs):
            try:
                rows.append(f.result())
            except Exception as e:
                print("FAILED", futs[f], repr(e), flush=True)
                continue
            ec.write_rows(rows, "RAW_p400")
            print(len(rows), "/", len(J), futs[futs and f] if False else futs[f], round(time.time() - t0), "s", flush=True)
    print("done", round(time.time() - t0), flush=True)
