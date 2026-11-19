"""Self-test of the statistical helpers of science.py on synthetic inputs (the reader itself is cross-checked by hand against the eval records, see LEG_READBACK)."""
import importlib.util, math, sys, os
import numpy as np
sp = importlib.util.spec_from_file_location("science", os.path.join(os.path.dirname(os.path.abspath(__file__)), "science.py")); sc = importlib.util.module_from_spec(sp); sp.loader.exec_module(sc)
ok = 0
def check(name, cond):
    global ok
    assert cond, name
    ok += 1; print("PASS", name)
# t interval: [1,2,3,4,5] -> mean 3, sd sqrt(2.5), df 4, t=2.776445
t = sc.tci([1, 2, 3, 4, 5]); check("tci mean/sd", abs(t["mean"] - 3) < 1e-12 and abs(t["sd"] - math.sqrt(2.5)) < 1e-12)
check("tci half-width", abs((t["hi"] - t["lo"]) / 2 - 2.776445 * math.sqrt(2.5) / math.sqrt(5)) < 1e-5)
check("tci n=1 has no interval", sc.tci([7.0])["lo"] is None); check("tci drops None / nan", sc.tci([1, None, float("nan"), 3])["n"] == 2)
# Wilson: p = 0.5, n = 10 -> [0.2366, 0.7634]
lo, hi = sc.wilson(0.5, 10); check("wilson 0.5/10", abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3)
lo, hi = sc.wilson(1.0, 10); check("wilson 10/10 upper = 1 (float tol), lower in (0.65, 0.75)", abs(hi - 1.0) < 1e-9 and 0.65 < lo < 0.75)
lo, hi = sc.wilson(0.0, 20); check("wilson 0/20 lower = 0", lo == 0.0 and 0.0 < hi < 0.2)
# slope: exact power law d = 3 / n  -> slope -1, bootstrap interval degenerate at -1
check("ols slope exact", abs(sc.ols_slope([math.log(n) for n in (100, 200, 400, 800)], [math.log(3 / n) for n in (100, 200, 400, 800)]) + 1) < 1e-12)
rng = np.random.default_rng(1)
s = sc.boot_slope({n: [3 / n] * 6 for n in (100, 200, 400, 800)}, rng, B=200); check("boot slope degenerate", abs(s["slope"] + 1) < 1e-9 and abs(s["lo"] + 1) < 1e-9 and abs(s["hi"] + 1) < 1e-9)
# slope with noise: interval contains truth and is not degenerate
r2 = np.random.default_rng(2); by = {n: list(3 / n * np.exp(r2.normal(0, 0.2, 40))) for n in (100, 200, 400, 800)}
s = sc.boot_slope(by, np.random.default_rng(3), B=400); check("boot slope covers -1, non-degenerate", s["lo"] < -1 < s["hi"] and s["hi"] - s["lo"] > 0.01)
check("boot slope refuses a zero cell", sc.boot_slope({100: [0.0, 0.0], 200: [1.0]}, rng, B=10) is None)
# cluster bootstrap ratio: every dataset has ratio 0.25 -> degenerate at 0.25
c = sc.cluster_boot_ratio([(1, 4), (5, 20), (2, 8)], np.random.default_rng(4), B=200); check("cluster ratio degenerate", abs(c["obs"] - 0.25) < 1e-12 and abs(c["lo"] - 0.25) < 1e-12 and abs(c["hi"] - 0.25) < 1e-12)
c = sc.cluster_boot_ratio([(0, 10), (10, 10), (5, 10), (2, 10)], np.random.default_rng(5), B=500); check("cluster ratio point and interval", abs(c["obs"] - 17 / 40) < 1e-12 and c["lo"] < c["obs"] < c["hi"])
check("cluster ratio, empty bin -> None", sc.cluster_boot_ratio([(0, 0), (0, 0)], np.random.default_rng(6), B=10) is None)
# proportion aggregation: dataset 1 has 2 fits (1 hit), dataset 2 one fit (hit) -> p = (0.5 + 1)/2
fits = [{"rep": 1, "x": True}, {"rep": 1, "x": False}, {"rep": 2, "x": True}]
pr = sc.prop(fits, lambda f: f["x"]); check("prop dataset-level", abs(pr["p"] - 0.75) < 1e-12 and pr["n_ds"] == 2 and pr["k_fits"] == 2 and pr["n_fits"] == 3)
check("by_dataset averages seeds", sc.by_dataset([{"rep": 1, "v": 1.0}, {"rep": 1, "v": 3.0}, {"rep": 2, "v": 5.0}], "v") == {1: 2.0, 2: 5.0})
print("ALL %d PASS" % ok)
