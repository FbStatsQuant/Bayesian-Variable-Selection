"""API-FAVIID audit: recompute every number in W5-FAVIID REPORT.md §1, §4.1, §4.3-4.5 and §8 from the raw
results (sweep.jsonl, pilot.jsonl) at W5-FAVIID commit 31695b1.  Deterministic (no randomness, no seed needed).
Usage: python3 audit_w5faviid.py <path to theory_campaign/W5-FAVIID/results>"""
import json, math, sys
from collections import defaultdict
import statistics
class np:  # stdlib stand-in (no numpy on owls python)
    median = staticmethod(statistics.median)
    mean = staticmethod(lambda a: sum(a) / len(a))

R = sys.argv[1]
sw = [json.loads(l) for l in open(R + "/sweep.jsonl") if l.strip()]
pr = list({(r["scen"], r["p"], r["scale"], r["n"], r["rep"]): r
           for r in (json.loads(l) for l in open(R + "/pilot.jsonl") if l.strip())}.values())
out = []
P = out.append
P("# API-FAVIID audit of W5-FAVIID results (commit 31695b1)")
P("sweep rows: %d ; pilot rows (deduped): %d" % (len(sw), len(pr)))

# ---------------- sweep ----------------
cell = defaultdict(list)
for r in sw:
    cell[(r["scen"], r["p"], r["scale"], r["n"])].append(r)
pi0 = lambda r: 10 ** r["log10_pi0_S0"]
P("\n## S1 unions (Q_n held): %d/%d ; failures: %s" % (
    sum(r["unions"] for r in sw), len(sw),
    sorted({(r["scen"], r["p"], r["scale"], r["n"]) for r in sw if not r["unions"]})))
viol = [r for r in sw if r["T22i_bound"] < 1 - pi0(r) - 1e-12]
P("## S2 T22(i) bound >= 1-pi0: %d/%d (violations %d)" % (len(sw) - len(viol), len(sw), len(viol)))
P("## S3 median T22(i) bound per cell (vacuous if > 1):")
for s in (1, 3, 4, 6):
    line = []
    for n in (200, 400, 800, 1600, 3200):
        meds = [np.median([r["T22i_bound"] for r in cell[(s, p, sc, n)]]) for p in (500, 1000) for sc in (0.5, 1.0)]
        line.append("n=%d [%.3g, %.3g]" % (n, min(meds), max(meds)))
    P("  S%d: %s" % (s, "; ".join(line)))
    fr = [r for r in sw if r["scen"] == s and r["n"] == 3200]
    P("     S%d n=3200: rows with bound<=1: %d/%d" % (s, sum(r["T22i_bound"] <= 1 for r in fr), len(fr)))

def xi(r):  # xi_n with eps0 = 0
    return math.sqrt(math.log(max(2 ** r["B"] * r["p"], r["n"])) / (r["n"] + 1))
meds = {k: np.median([r["q"] / xi(r) for r in v]) for k, v in cell.items()}
allr = [r["q"] / xi(r) for r in sw]
P("## S4 q/xi_n(eps0=0): cell medians in [%.3f, %.3f]; row range [%.3f, %.3f]" % (
    min(meds.values()), max(meds.values()), min(allr), max(allr)))
qq = [r for r in sw if r["Qreal"] is not None]
P("## S5 rows with Qreal: %d ; max q/Qreal = %.4f" % (len(qq), max(r["q"] / r["Qreal"] for r in qq)))
m6 = [np.median([r["Q0"] / r["Qreal"] for r in v if r["Qreal"]]) for k, v in cell.items() if k[0] != 1]
a6 = [r["Q0"] / r["Qreal"] for r in qq]
P("## S6 Q0/Qreal: cell medians [%.4f, %.4f]; row range [%.4f, %.4f]" % (min(m6), max(m6), min(a6), max(a6)))
P("## S7 max m_real in S3/S4/S6: %d ; in S1: %d" % (
    max(r["m_real"] for r in sw if r["scen"] != 1), max(r["m_real"] for r in sw if r["scen"] == 1)))
P("## S8 table 4.4 (p=500, scale 1): med log10 pi0 ; frac pi0>1/2 at 1600/3200")
for s in (1, 3, 4, 6):
    v = [np.median([r["log10_pi0_S0"] for r in cell[(s, 500, 1.0, n)]]) for n in (200, 400, 800, 1600, 3200)]
    f = [np.mean([pi0(r) > 0.5 for r in cell[(s, 500, 1.0, n)]]) for n in (1600, 3200)]
    P("  S%d: %s | %.2f / %.2f" % (s, " ".join("%.2f" % x for x in v), f[0], f[1]))
P("## S9 empirical first n with median pi0 > 1/2 (by p, scale)")
for s in (1, 3, 4, 6):
    for p in (500, 1000):
        fn = []
        for sc in (0.5, 1.0):
            ns = [n for n in (200, 400, 800, 1600, 3200) if np.median([pi0(r) for r in cell[(s, p, sc, n)]]) > 0.5]
            fn.append(min(ns) if ns else None)
        P("  S%d p=%d: scale0.5 %s, scale1 %s" % (s, p, fn[0], fn[1]))
q32 = [np.median([r["q"] for r in v]) for k, v in cell.items() if k[3] == 3200]
P("## S10 median q at n=3200: [%.3f, %.3f]" % (min(q32), max(q32)))
P("## S11 (1-pi0)/(1-exp(-N_add)), cell medians, by n (N_add = exp(log_Nadd))")
for n in (800, 1600, 3200):
    mm = {k: np.median([(1 - pi0(r)) / (1 - math.exp(-math.exp(r["log_Nadd"]))) for r in v]) for k, v in cell.items() if k[3] == n}
    P("  n=%d: [%.3f, %.3f]" % (n, min(mm.values()), max(mm.values())))
    if n == 1600:
        sub = [v for k, v in mm.items() if k[0] in (1, 3) and k[1] == 500]
        P("    S1/S3 p=500 at 1600: [%.3f, %.3f]" % (min(sub), max(sub)))
        sub = [v for k, v in mm.items() if k[0] in (4, 6)]
        P("    S4/S6 at 1600: max %.3f" % max(sub))
P("## S12 median sqrt(n/log n)(1-pi0) per scenario")
for s in (1, 3, 4, 6):
    P("  S%d: " % s + " ".join("n=%d %.2f" % (n, np.median([math.sqrt(n / math.log(n)) * (1 - pi0(r))
        for r in sw if r["scen"] == s and r["n"] == n])) for n in (800, 1600, 3200)))

# ---------------- pilot ----------------
P("\n## P1 pilot table by n (recomputed)")
byn = defaultdict(list)
for r in pr:
    byn[r["n"]].append(r)
tot_le3200 = cnt_le3200 = 0
for n in sorted(byn):
    rs = byn[n]
    g = [(r["T_grid"] + 1) * r["Delta_est"] for r in rs]
    gl = [(r["T_grid"] + 1) * r["Delta_lb"] for r in rs]
    P("  n=%5d runs=%2d Tp med %.1f [%d,%d] Tg med %.1f [%d,%d] Delta med %.3f (Tg+1)D med %.3f <1: %d/%d ; with Delta_lb <1: %d/%d" % (
        n, len(rs), np.median([r["T_pilot"] for r in rs]), min(r["T_pilot"] for r in rs), max(r["T_pilot"] for r in rs),
        np.median([r["T_grid"] for r in rs]), min(r["T_grid"] for r in rs), max(r["T_grid"] for r in rs),
        np.median([r["Delta_est"] for r in rs]), np.median(g), sum(x < 1 for x in g), len(g), sum(x < 1 for x in gl), len(gl)))
    if n <= 3200:
        tot_le3200 += len(g); cnt_le3200 += sum(x < 1 for x in g)
P("  runs n<=3200 with (Tg+1)Delta_est < 1: %d/%d" % (cnt_le3200, tot_le3200))
P("  borderline rows (0.95 < (Tg+1)D < 1.05):")
for r in sorted(pr, key=lambda r: (r["n"], r["scen"], r["p"])):
    v = (r["T_grid"] + 1) * r["Delta_est"]
    if 0.95 < v < 1.05:
        P("    S%d p=%d sc=%.1f n=%d rep=%d: T_grid=%d Delta_est=%.5f -> %.5f" % (
            r["scen"], r["p"], r["scale"], r["n"], r["rep"], r["T_grid"], r["Delta_est"], v))
P("  per scenario at n=6400, range of (Tg+1)Delta_est:")
for s in (1, 3, 4, 6):
    v = [(r["T_grid"] + 1) * r["Delta_est"] for r in pr if r["n"] == 6400 and r["scen"] == s]
    P("    S%d: %.2f-%.2f (%d runs)" % (s, min(v), max(v), len(v)))
P("  first-stage ESS frac range: [%.4f, %.4f]; forced stages total: %d; grid_status: %s" % (
    min(r["ess_first"] for r in pr), max(r["ess_first"] for r in pr), sum(r["forced"] for r in pr),
    sorted({r["grid_status"] for r in pr})))
P("  delta1_est/(1-pi0) at n>=3200: median %.3f [%.3f, %.3f]" % tuple(
    (lambda a: (np.median(a), min(a), max(a)))([r["delta1_est"] / r["one_minus_pi0"] for r in pr if r["n"] >= 3200])))
P("  runs where Delta_est is set by delta1 (delta1_est > 1-pi0): %d/%d" % (
    sum(r["delta1_est"] > r["one_minus_pi0"] for r in pr), len(pr)))
open("audit_out.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
