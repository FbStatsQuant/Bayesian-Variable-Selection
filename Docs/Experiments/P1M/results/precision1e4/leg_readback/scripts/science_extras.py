#!/usr/bin/env python3
"""science_extras.py -- descriptive extras written AFTER the first read of science.py's output (logged): flag identification, mid-range reliability totals,
d_H^2 standard errors, cost / n-scaling / G-B criterion tables.  Read-only.  Uses science.load_fits (same reader)."""
import importlib.util, json, math, os, sys
import numpy as np
sp = importlib.util.spec_from_file_location("science", os.path.join(os.path.dirname(os.path.abspath(__file__)), "science.py")); sc = importlib.util.module_from_spec(sp); sp.loader.exec_module(sc)
OPS = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/precision1e4/ops_tools/stop_rules_prec.py"
s2 = importlib.util.spec_from_file_location("srp", OPS); srp = importlib.util.module_from_spec(s2); s2.loader.exec_module(srp)
R = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4")
costs = json.load(open("costs.json"))
fits = sc.load_fits(R, costs)
sci = [f for f in fits if f["tag"] in ("V", "VF")]
out = []
P = out.append
P("## X1. Fits with a final-stage flag or an island spread sd(log Z_r) > 0.3")
for f in sorted(sci, key=lambda f: (f["design"], f["n"], f["rep"])):
    fl = [k for k in ("E1", "E2", "E3", "low_empirical_ESS", "occ_inhomogeneous", "local_limit", "final_local_limit", "near_tie_truncated") if f["flags"].get(k) is True]
    sdl = float(np.std(f["logZ_r"], ddof=1))
    if fl or sdl > 0.3 or not f["flags"].get("checks_passed_final", True):
        lr = sorted(f["logZ_r"])
        P("- %s: flags %s, checks_passed_final %s, sd(log Z_r) %.3f, sigma_hat %.3f (robust %.3f), R_eff/R' %.3f, max-median %.3f, log Z_r range %.2f..%.2f (median %.2f), HPM=S0 %s, cost %.2f" % (
            f["run_id"], fl, f["flags"].get("checks_passed_final"), sdl, f["sigma_hat"], f["sigma_rob"], f["R_eff"] / f["Rp"], f["max_minus_med"], lr[0], lr[-1], lr[len(lr) // 2], f["hpm_eq"], f["core_h"]))
P("")
P("## X2. Same quantities for the other designs' worst fits (largest sigma-hat per cell with sigma_hat > 0.1)")
for f in sorted(sci, key=lambda f: -f["sigma_hat"])[:6]:
    P("- %s: sigma_hat %.3f, R_eff/R' %.3f, max-median %.3f, flags %s" % (f["run_id"], f["sigma_hat"], f["R_eff"] / f["Rp"], f["max_minus_med"], [k for k, v in f["flags"].items() if v is True]))
P("")
P("## X3. Reliability, AR-weak: bins 0.05-0.95 pooled (the mid-range)")
tot = {"n": 0, "true": 0, "exp": 0.0}
for f in sci:
    if f["design"] != "ARweak":
        continue
    for b in f["reliability"]:
        if 0.05 <= b["lo"] < 0.95 - 1e-9 and b["n"] > 0:
            tot["n"] += b["n"]; tot["true"] += b["n_true"]; tot["exp"] += b["n"] * b["mean_pip"]
P("variables with PIP in [0.05, 0.95): %d; active among them %d; expected active count (sum of PIP) %.1f" % (tot["n"], tot["true"], tot["exp"]))
for nn in (100, 200, 400, 800):
    t = {"n": 0, "true": 0, "exp": 0.0}
    for f in sci:
        if f["design"] != "ARweak" or f["n"] != nn:
            continue
        for b in f["reliability"]:
            if 0.05 <= b["lo"] < 0.95 - 1e-9 and b["n"] > 0:
                t["n"] += b["n"]; t["true"] += b["n_true"]; t["exp"] += b["n"] * b["mean_pip"]
    P("  n = %d: %d variables, %d active, expected %.1f" % (nn, t["n"], t["true"], t["exp"]))
P("")
P("## X4. Store-BMA predictive d_H^2: s.e. and exactness")
ex = sum(1 for f in sci if f["pred_exact"]); P("exact mixture (no tail sample): %d of %d fits; max h2_se_x %.2e; max h2_se_tail %.2e; max omitted store mass %s; max dropped_mass %s" % (
    ex, len(sci), max(f["h2_T_se_x"] for f in sci), max(f["h2_T_se_tail"] for f in sci), max(f["omitted_mass"] for f in sci), max(f["dropped_mass_T"] for f in sci)))
P("largest relative s.e. (h2_se_x / h2): %.3f" % max(f["h2_T_se_x"] / f["h2_T"] for f in sci if f["h2_T"] > 0))
P("")
P("## X5. Cost by class (committed model E; G-B criterion: class mean <= 1.5 E AND no fit > 2.5 E; every fit > 1.5 E listed)")
cl = {}
for r in costs:
    cl.setdefault(r["klass"], []).append(r)
P("| class | fits | mean | max | E | mean/E | max/E | class mean <= 1.5E | no fit > 2.5E | fits > 1.5E |")
P("|---|---|---|---|---|---|---|---|---|---|")
allp = True; over15 = []
for k, rs in sorted(cl.items()):
    t = srp.TABLE.get(k)
    if not t:
        P("| %s | %d | %.2f | %.2f | (no class: T fits, report line 172.5) | - | - | - | - | - |" % (k, len(rs), np.mean([r["core_h"] for r in rs]), max(r["core_h"] for r in rs))); continue
    E = t[0]; m = float(np.mean([r["core_h"] for r in rs])); mx = max(r["core_h"] for r in rs)
    o = [r for r in rs if r["core_h"] > 1.5 * E]
    over15 += [(r["rid"], k, r["core_h"], E) for r in o]
    ok1, ok2 = m <= 1.5 * E, mx <= 2.5 * E
    allp = allp and ok1 and ok2
    P("| %s | %d | %.2f | %.2f | %.2f | %.2f | %.2f | %s | %s | %d |" % (k, len(rs), m, mx, E, m / E, mx / E, "yes" if ok1 else "NO", "yes" if ok2 else "NO", len(o)))
P("")
P("G-B cost criterion on the %d model classes: %s; fits above 1.5 x their committed model: %d %s" % (len([k for k in cl if srp.TABLE.get(k)]), "PASS in every class" if allp else "NOT PASSED somewhere", len(over15), over15))
P("")
P("## X6. n-scaling (V arm, I_max = 0 frozen fits; mean billed core-h per fit; ratio to the same design's n = 200 mean; the planning model's nf(n) ratio 0.7 / 1.0 / 1.6 / 2.8)")
P("| design | n=100 | n=200 | n=400 | n=800 | ratio 100/200 | ratio 400/200 | ratio 800/200 | mean island T (100/200/400/800) | mean islands core-h (100/200/400/800) |")
P("|---|---|---|---|---|---|---|---|---|---|")
byc = {}
for f in sci:
    byc.setdefault((f["design"], f["n"]), []).append(f)
for d in ("AR", "ARweak", "IND", "BLK", "ADJOPP", "NULL"):
    row = {}
    for n in (100, 200, 400, 800):
        fs = byc.get((d, n))
        if fs:
            row[n] = (float(np.mean([f["core_h"] for f in fs])), float(np.mean([f["island_T"] for f in fs])), float(np.mean([f["stage_h"]["islands"] for f in fs])), len(fs))
    g = lambda n, i: ("%.2f" % row[n][i]) if n in row else "-"
    rt = lambda n: ("%.2f" % (row[n][0] / row[200][0])) if (n in row and 200 in row) else "-"
    P("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (sc.NAMES[d], g(100, 0), g(200, 0), g(400, 0), g(800, 0), rt(100), rt(400), rt(800),
       "/".join(g(n, 1) for n in (100, 200, 400, 800)), "/".join(g(n, 2) for n in (100, 200, 400, 800))))
allf = {n: [f["core_h"] for f in sci if f["n"] == n] for n in (100, 200, 400, 800)}
P("")
P("All science V fits pooled by n (design mix differs by n): mean %s; n = 200 excluding NULL: %.2f" % (", ".join("n%d %.2f (%d fits)" % (n, np.mean(v), len(v)) for n, v in allf.items()), np.mean([f["core_h"] for f in sci if f["n"] == 200 and f["design"] != "NULL"])))
P("Fits that cost more than the design's n = 200 mean: n = 400: %s" % ", ".join("%s %d/%d" % (sc.NAMES[d], sum(1 for f in byc[(d, 400)] if f["core_h"] > np.mean([g["core_h"] for g in byc[(d, 200)]])), len(byc[(d, 400)])) for d in ("AR", "ARweak", "IND", "BLK", "ADJOPP") if (d, 400) in byc))
P("")
P("## X7. Stage split, wall and memory (science V fits, by n: mean core-h per stage; max wall s; max RSS MB)")
P("| n | fits | setup | calibrate | islands | merge | eval | max wall s cal / isl / merge | max RSS MB (setup / cal / isl / merge / eval) |")
P("|---|---|---|---|---|---|---|---|---|")
for n in (100, 200, 400, 800):
    fs = [f for f in sci if f["n"] == n]
    sm = {s: float(np.mean([f["stage_h"][s] for f in fs])) for s in ("setup", "calibrate", "islands", "merge", "eval")}
    wl = {s: max(f["wall"][s] for f in fs) for s in ("calibrate", "islands", "merge")}
    rs = {s: max(f["rss"][s] for f in fs) / 1e6 for s in ("setup", "calibrate", "islands", "merge", "eval")}
    P("| %d | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %d / %d / %d | %s |" % (n, len(fs), *[sm[s] for s in ("setup", "calibrate", "islands", "merge", "eval")], wl["calibrate"], wl["islands"], wl["merge"], " / ".join("%.0f" % rs[s] for s in ("setup", "calibrate", "islands", "merge", "eval"))))
a3 = [f for f in fits if f["tag"] in ("A3", "A3F")]
P("")
P("A3 fits (exact partition): mean cost %.2f core-h; setup stage mean %.3f core-h, max setup wall %s s; max RSS setup %.0f MB" % (np.mean([f["core_h"] for f in a3]), np.mean([f["stage_h"]["setup"] for f in a3]), max(f["wall"].get("setup", 0) for f in a3), max(f["rss"]["setup"] for f in a3) / 1e6))
print("\n".join(out))
open("sci_out/science_extras.md", "w").write("\n".join(out) + "\n")
