"""Aggregate run_study.py output. Usage: python analyse.py ../results/study_*.jsonl > ../results/summary.txt"""
import sys, json
import numpy as np

L10 = np.log(10); QF = 1e4   # Q_f = 4 islands x 2,500 final iid start draws
recs = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
print("records:", len(recs))
cells = sorted(set((r["p"], r["s"], r["c"]) for r in recs))
V = ("v3", "known_oracle", "known_mode1", "known_iter", "resid")

def med(xs): return float(np.median(xs))

print("\n== Table 1. v3 start, per cell (medians over replicates) ==")
print("%5s %2s %4s %3s | %8s %7s %9s %6s %6s %6s | %6s %6s %6s | %6s %6s" % (
    "p", "S", "c", "R", "lg10pi0", "pi0R2", "pi0Ham2", "Etr", "Enull", "modeT", "-V", "-C", "logA", "dS0", "R2S0"))
for cell in cells:
    rs = [r for r in recs if (r["p"], r["s"], r["c"]) == cell]
    v = [r["v3"] for r in rs]
    print("%5d %2d %4.1f %3d | %8.2f %7.3f %9.1e %6.1f %6.2f %6.1f | %6.1f %6.1f %6.1f | %6.0f %6.3f" % (
        *cell, len(rs), med([x["logpi0_S0"] / L10 for x in v]), med([x["pi0_R"]["2"] for x in v]),
        med([x["pi0_ham"]["2"] for x in v]), med([x["E_truths"] for x in v]), med([x["E_nulls"] for x in v]),
        med([x["mode_truths"] for x in v]), -med([x["vis"] for x in v]), -med([x["comp"] for x in v]),
        med([x["logA"] for x in v]), med([r["d_S0"] for r in rs]), med([r["R2_S0"] for r in rs])))

allv = [r["v3"] for r in recs]
print("\nPooled over all fits: median log10 pi0(S0) = %.2f ; median pi0(R2) = %.3f ; median pi0(R1) = %.3f ; "
      "median pi0(Hamming<=2) = %.1e ; favourable (Q_f pi0(S0) >= 1, Q_f = 1e4): %d of %d" % (
          med([x["logpi0_S0"] / L10 for x in allv]), med([x["pi0_R"]["2"] for x in allv]),
          med([x["pi0_R"]["1"] for x in allv]), med([x["pi0_ham"]["2"] for x in allv]),
          sum(QF * np.exp(x["logpi0_S0"]) >= 1 for x in allv), len(allv)))
for c in (1.0, 0.5):
    a = [r["v3"] for r in recs if r["c"] == c]
    print("  c=%.1f: median log10 pi0(S0) = %.2f, median pi0(R2) = %.3f" % (
        c, med([x["logpi0_S0"] / L10 for x in a]), med([x["pi0_R"]["2"] for x in a])))
cpb = [r for r in recs]
print("  exact = -V - C + logA (identity); median share of -log pi0(S0) from V: %.2f, from C: %.2f, from -logA: %.2f" % (
    med([x["vis"] / -x["logpi0_S0"] for x in allv]), med([x["comp"] / -x["logpi0_S0"] for x in allv]),
    med([-x["logA"] / -x["logpi0_S0"] for x in allv])))
print("  ceiling check (Cor. E2: logA <= -log P_t(N<=K) ~ 0): max logA over fits = %.3g" % max(x["logA"] for x in allv))

print("\n== Table 2. per-truth table vs posterior keep-j log-odds (all fits, truths alone in their block) ==")
print("beta | med LO0 (table) | frac LO0>0 | med LO1 (posterior) | frac LO1>0 | med ratio (G0+.5log n)/(G1+.5log n) | pop log(1-rho^2)/log(1-x_j)")
for c in (1.0, 0.5):
    for b in (1.8, -1.6, 1.4, -1.2, -1.0, 0.8):
        tt = [(t, r) for r in recs if r["c"] == c and r["s"] in (1, 3, 4, 6) for t in r["truths"]
              if abs(t["beta"] - b) < 1e-9 and t["alone"]]
        if not tt: continue
        LO0 = [t["LO0"] for t, _ in tt]; LO1 = [t["LO1"] for t, _ in tt]
        hl = 0.5 * np.log(200)
        ratio = [(t["G0"] + hl) / (t["G1"] + hl) for t, _ in tt]
        pop = [np.log1p(-t["rho2"]) / np.log1p(-t["x1"]) for t, _ in tt]
        print("c=%.1f beta=%5.2f | %7.2f | %.2f | %7.2f | %.2f | %.3f | %.3f" % (
            c, b, med(LO0), np.mean(np.array(LO0) > 0), med(LO1), np.mean(np.array(LO1) > 0), med(ratio), med(pop)))

print("\n== Table 3. variants (medians per cell): log10 pi0(S0) / pi0(R2) / E nulls / mode truths, mode size ==")
print("%5s %2s %4s | %-26s | %-26s | %-26s | %-26s | %-26s" % ("p", "S", "c", *V))
for cell in cells:
    rs = [r for r in recs if (r["p"], r["s"], r["c"]) == cell]
    row = []
    for k in V:
        v = [r[k] for r in rs]
        row.append("%8.1f %5.2f %5.1f %2.0f/%3.0f" % (med([x["logpi0_S0"] / L10 for x in v]), med([x["pi0_R"]["2"] for x in v]),
                                                     med([x["E_nulls"] for x in v]), med([x["mode_truths"] for x in v]),
                                                     med([x["mode_size"] for x in v])))
    print("%5d %2d %4.1f | %s" % (*cell, " | ".join(row)))
print("\nPooled variant medians: log10 pi0(S0), pi0(R2), pi0(Hamming<=2), favourable count (Q_f=1e4)")
for k in V:
    v = [r[k] for r in recs]
    print("  %-13s %8.2f %6.3f %9.2e %4d/%d" % (k, med([x["logpi0_S0"] / L10 for x in v]), med([x["pi0_R"]["2"] for x in v]),
                                               med([x["pi0_ham"]["2"] for x in v]),
                                               sum(QF * np.exp(x["logpi0_S0"]) >= 1 for x in v), len(v)))
print("  plug-in s2 values: median oracle %.3f, mode1 %.3f, iter-final %.3f" % (
    med([r["s2_oracle"] for r in recs]), med([r["s2_mode1"] for r in recs]), med([r["s2_iter_hist"][-1] for r in recs])))
best = [max(h["logpi0_S0"] for h in r["resid_hist"]) / L10 for r in recs]
print("  resid: median over fits of best-iteration log10 pi0(S0) = %.2f; by iteration: %s" % (
    med(best), [round(med([r["resid_hist"][i]["logpi0_S0"] / L10 for r in recs]), 2) for i in range(3)]))
nanW1 = sum(1 for r in recs if not np.isfinite(r["d_S0_W1"]))
fin = [(r["d_S0"], r["d_S0_W1"]) for r in recs if np.isfinite(r["d_S0_W1"])]
print("\nLemma W1 (exact BO) formula for d(S0) vs actual d(S0): undefined (sum xi_b >= 1, impossible under BO) in %d/%d fits;"
      " where defined, median actual %.0f vs W1 %.0f, median |diff| %.0f nats" % (
          nanW1, len(recs), med([a for a, b in fin]), med([b for a, b in fin]), med([abs(a - b) for a, b in fin])))
