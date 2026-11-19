"""science_extras2.py (post-read addition, logged): posterior quantiles of d_H (PREREG section 5 C5) per cell: mean over datasets of the posterior q05 / q50 / q95 of d_H (store-BMA law) with the true-model oracle's beside it."""
import importlib.util, json, os
sp = importlib.util.spec_from_file_location("science", "science.py"); sc = importlib.util.module_from_spec(sp); sp.loader.exec_module(sc)
fits = sc.load_fits(os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4"), json.load(open("costs.json")))
sci = [f for f in fits if f["tag"] in ("V", "VF")]
cells = {}
for f in sci: cells.setdefault((f["design"], f["n"]), []).append(f)
L = ["| design | n | post. d_H q05 | q50 | q95 (mean over datasets) | true d_H of the BMA = sqrt(d_H^2 BMA) |", "|---|---|---|---|---|---|"]
for d in sc.DESIGNS:
    for n in (100, 200, 400, 800):
        fs = cells.get((d, n))
        if not fs: continue
        m = lambda k: sum(sc.by_dataset(fs, k).values()) / len(sc.by_dataset(fs, k))
        import math
        dh = sum(sc.by_dataset(fs, None, lambda f: math.sqrt(f["h2_T"])).values()) / len(sc.by_dataset(fs, None, lambda f: math.sqrt(f["h2_T"])))
        L.append("| %s | %d | %.4f | %.4f | %.4f | %.4f |" % (sc.NAMES[d], n, m("post_q05"), m("post_q50"), m("post_q95"), dh))
print("\n".join(L)); open("sci_out/science_extras2.md", "w").write("\n".join(L) + "\n")
