"""science_extras3.py (post-review, logged): per-cell min/max of log Z-hat - log Z_T and the ADJ-OPP n200 r04 record details; A3-pair d_H from a3x/."""
import importlib.util, json, os, math, glob
import numpy as np
sp = importlib.util.spec_from_file_location("science", "science.py"); sc = importlib.util.module_from_spec(sp); sp.loader.exec_module(sc)
fits = sc.load_fits(os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4"), json.load(open("costs.json")))
sci = [f for f in fits if f["tag"] in ("V", "VF")]
L = ["| design | n | log Z-hat - log Z_T: mean | min | max | fits < 0 |", "|---|---|---|---|---|---|"]
cells = {}
for f in sci: cells.setdefault((f["design"], f["n"]), []).append(f)
for d in sc.DESIGNS:
    for n in (100, 200, 400, 800):
        fs = cells.get((d, n))
        if not fs: continue
        v = [f["logZ_minus_T"] for f in fs]
        L.append("| %s | %d | %.4f | %.4f | %.4f | %d |" % (sc.NAMES[d], n, np.mean(v), min(v), max(v), sum(1 for x in v if x < 0)))
neg = [(f["run_id"], f["logZ"], f["logZ_T"], f["logZ_minus_T"]) for f in sci if f["logZ_minus_T"] < 0]
L.append("")
L.append("negative: %s" % neg)
r4 = [f for f in sci if f["run_id"] == "4-ADJOPP-n200-r04-V-s1"][0]
lr = np.array(r4["logZ_r"]); med = np.median(lr)
ev = json.load(open(r4["dir"] + "/eval.bin.json"))
L.append("r04: logZ_r - median: min %.3f max %.3f; islands >= 0.8 below the median: %d; max_W %.3f; sd(log Z_r) %.6f; sd(Z_r/mean Z_r) %.3f; HPM=MPM=S0 %s/%s; M1 %.4f; M2 %.5f; local_certified_by %s" % (
    (lr - med).min(), (lr - med).max(), int(((lr - med) <= -0.8).sum()), ev["evidence"]["max_W"], np.std(lr, ddof=1), np.std(np.exp(lr - lr.max()) / np.mean(np.exp(lr - lr.max())), ddof=1),
    r4["hpm_eq"], r4["mpm_eq"], r4["occ_sd1000"], r4["isl_pip_max_sd"], ev["fit"]["meta"].get("local_certified_by")))
L.append("")
L.append("## A3 pair d_H (exact-partition law vs default-partition `VF` law; same seed; both with the VF data.bin)")
L.append("| pair | d_H(A3F, VF) | h2 (s.e.) | d_H(VF, f*) | ratio |")
L.append("|---|---|---|---|---|")
for r in ("01", "02", "03", "04"):
    j = json.load(open("a3x/cross_r%s.json" % r)); c = list(j["pairs"].values())[0]["1"]
    ve = [f for f in sci if f["run_id"] == "4-AR-n200-r%s-VF-s1" % r][0]
    dv = math.sqrt(ve["h2_T"]); dh = math.sqrt(max(c["h2"], 0))
    L.append("| AR n200 r%s | %.3e | %.2e (%.1e) | %.4f | %.4f |" % (r, dh, c["h2"], c["se"], dv, dh / dv))
print("\n".join(L)); open("sci_out/science_extras3.md", "w").write("\n".join(L) + "\n")
