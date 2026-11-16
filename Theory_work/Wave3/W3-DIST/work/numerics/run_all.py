import sys, time, csv, numpy as np
from multiprocessing import Pool
from reps import run_rep
NW = int(sys.argv[1]) if len(sys.argv) > 1 else 7
R = int(sys.argv[2]) if len(sys.argv) > 2 else 40
ND = 4000
NS = [50, 100, 200, 400, 800]
tasks = []
def add(eid, name, kind, beta, ns, p=12, family="exact", taufun=None, mfresh=20000):
    for n in ns:
        for rep in range(R):
            pp = p(n) if callable(p) else p
            tau2 = taufun(n) if taufun else None
            tasks.append(dict(eid=eid, name=name, kind=kind, beta=beta, n=n, p=pp, rep=rep, family=family, tau2=tau2,
                              ndraw=ND, mfresh=mfresh))
# N7 first (most expensive), then big n
for kind, nm in (("ar", "N7_ar"), ("t25", "N7_t25")):
    add(70 if kind == "ar" else 71, nm + "_p4n", kind, "sparse", [50, 100, 200], p=lambda n: 4 * n, family="restricted")
    add(72 if kind == "ar" else 73, nm + "_p15", kind, "sparse", [50, 100, 200], p=lambda n: min(int(n ** 1.5), 600), family="restricted")
add(1, "N1", "ar", "sparse", NS)
add(21, "N2a_t25", "t25", "sparse", NS)
add(22, "N2b_pareto", "pareto", "sparse", NS)
add(23, "N2c_spike", "spike", "sparse", NS, mfresh=40000)
add(3, "N3", "ar", "nobetamin", NS)
add(5, "N5", "ar", "approx", NS)
for j, (lab, f) in enumerate([("n-2", lambda n: n ** -2.0), ("n-1", lambda n: 1.0 / n), ("logn_n", lambda n: np.log(n) / n), ("1", lambda n: 1.0)]):
    add(40 + j, "N4_tau2=" + lab, "collin", "sparse", NS, taufun=f)
tasks.sort(key=lambda t: -(t["n"] if t["family"] == "exact" else 10 ** 4) )
print(len(tasks), "tasks", flush=True)
t0 = time.time()
rows = []; store = {}
with Pool(NW) as pool, open("raw_reps.csv", "w", newline="") as fh:
    w = None
    for i, (out, d2, rho) in enumerate(pool.imap_unordered(run_rep, tasks, chunksize=1)):
        if w is None:
            w = csv.DictWriter(fh, fieldnames=list(out.keys())); w.writeheader()
        w.writerow(out); fh.flush()
        store.setdefault((out["name"], out["n"]), {})[out["rep"]] = (d2, rho)
        if i % 100 == 0:
            print(i, "done", round(time.time() - t0), "s", flush=True)
for (nm, n), dct in store.items():
    reps = sorted(dct)
    np.savez_compressed(f"arrays/{nm}_n{n}.npz", d2=np.stack([dct[r][0] for r in reps]), rho=np.stack([dct[r][1] for r in reps]))
print("finished", round(time.time() - t0), "s", flush=True)
