#!/usr/bin/env python3
"""fz_tables.py -- FZ read-back tables from the collected records (stdlib, read-only): per-fit quantities, cost vs the committed class model,
G-B cost criterion check, R'=16 cost estimate of the I_max=0 saving, log Z vs occupancy 3-se check. python3 -I fz_tables.py"""
import glob, json, math, os, re
R = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4")
RUN = re.compile(r"^4-(ARweak|AR|ADJOPP)-n200-r01-P-N2500-m(\d)(?:-I(\d))?-c([12])-s1$")
# committed class table (LEG_PLAN 5.3): E, soft, hard
MODEL = {(1, 3): (6.28, 9.4, 15.7), (1, 0): (5.76, 8.6, 14.4), (4, 3): (12.36, 18.5, 30.9)}
rows = []
for d in sorted(glob.glob(R + "/*/4-*-P-*")):
    rid = os.path.basename(d); g = RUN.match(rid).groups(); m = int(g[1]); I = int(g[2]) if g[2] is not None else 3
    ev = json.load(open(d + "/eval.bin.json")); fm = ev["fit"]["meta"]; occ = [e for e in fm["occ"] if e["M"] == 1000][0]
    ex = ev["evidence"]; lr = ex["logZ_r"]; n = len(lr); mu = sum(lr) / n; sdz = math.sqrt(sum((x - mu) ** 2 for x in lr) / (n - 1))
    se_z = sdz / math.sqrt(n); se_o = occ["sd_log_Z_occ_r"] / math.sqrt(n); diff = ex["logZ"] - occ["log_Z_occ"]; bound = 3 * math.sqrt(se_z ** 2 + se_o ** 2)
    c = [p for p in glob.glob(R + "/*/_batch_*/cost/cost_%s.json" % rid)][0]; cj = json.load(open(c)); st = cj["stages"]
    cm = json.load(open(d + "/calib_meta.json")); cm = cm.get("meta", cm)
    rows.append(dict(rid=rid, ds=g[0], m=m, I=I, c=int(g[3]), M1=occ["sd_log_Z_occ_r"], M2=ev["pip"]["island_spread"]["max_sd"], M2ok=ev["pip"]["island_spread"].get("target_met"), M3=ex["sigma_hat"],
                     M3r=ex.get("sigma_hat_robust"), hpm=ev["selection"]["hpm"], eqS0=ev["selection"]["hpm_eq_S0"], inh=fm["flags"].get("occ_inhomogeneous"), dz=diff, bound=bound, ok3=abs(diff) <= bound,
                     tot=cj["billed_core_h"], setup=st["setup"]["billed_core_h"], cal=st["calibrate"]["billed_core_h"], isl=st["islands"]["billed_core_h"], mer=st["merge"]["billed_core_h"], ev=st["eval"]["billed_core_h"],
                     isl_wall=st["islands"]["wall_s_max"], merge_rss=st["merge"]["max_rss_bytes"] / 1e9, T=json.load(open(d + "/island_1.bin.json"))["T"], Iused=cm.get("I_used"), gu=cm["flags"]["grid_unconverged"],
                     wave=d.split("/")[-2]))
rows.sort(key=lambda r: (r["m"], r["I"], r["ds"], r["c"]))
o = []
o.append("## per-fit quantities (R'=64; engine eval record; targets M1<=0.05, M2<=0.005, M3<=0.5)")
o.append("| fit | wave | M1 | M2 | M3 (robust) | HPM = S0 | occ_inhom | logZ - logZ_occ (3 se bound) | T | I_used | grid_unconv |")
o.append("|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    o.append("| %s | %s | %.4f | %.5f | %.4f (%.4f) | %s | %s | %+.4f (%.4f) %s | %d | %s | %s |" % (r["rid"].replace("4-", "").replace("-n200-r01-P-N2500", ""), r["wave"], r["M1"], r["M2"], r["M3"], r["M3r"], r["eqS0"], r["inh"], r["dz"], r["bound"], "ok" if r["ok3"] else "MISS", r["T"], r["Iused"], r["gu"]))
o.append("\n## cost per fit vs the committed class model (billed core-h; setup / calibrate / islands(64) / merge / eval)")
o.append("| fit | total | x model E | setup | calib | islands | merge | eval | soft | hard | verdict |")
o.append("|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    E, S, H = MODEL[(r["m"], r["I"])]
    v = "HARD" if r["tot"] > H else "soft" if r["tot"] > S else "ok"
    o.append("| %s | %.3f | %.2f | %.3f | %.3f | %.3f | %.3f | %.3f | %.1f | %.1f | %s |" % (r["rid"].replace("4-", "").replace("-n200-r01-P-N2500", ""), r["tot"], r["tot"] / E, r["setup"], r["cal"], r["isl"], r["mer"], r["ev"], S, H, v))
o.append("\n## class means vs the committed model (G-B criterion: mean <= 1.5 E and no fit > 2.5 E)")
o.append("| class | fits | mean total | E | mean/E | max fit | max/E | calib mean | islands mean | merge mean | G-B |")
o.append("|---|---|---|---|---|---|---|---|---|---|---|")
for k, (E, S, H) in MODEL.items():
    rr = [r for r in rows if (r["m"], r["I"]) == k]; mt = sum(r["tot"] for r in rr) / len(rr); mx = max(r["tot"] for r in rr)
    o.append("| m%d I%d | %d | %.2f | %.2f | %.2f | %.2f | %.2f | %.3f | %.3f | %.3f | %s |" % (k[0], k[1], len(rr), mt, E, mt / E, mx, mx / E, sum(r["cal"] for r in rr) / len(rr), sum(r["isl"] for r in rr) / len(rr), sum(r["mer"] for r in rr) / len(rr), "PASS" if (mt <= 1.5 * E and mx <= 2.5 * E) else "FAIL"))
tot = sum(r["tot"] for r in rows)
o.append("\nsum of the 18 precision fits = %.2f core-h" % tot)
# all 20 units incl A3 + XB
allc = 0.0
for c in glob.glob(R + "/*/_batch_*/cost/cost_4-*.json"):
    allc += json.load(open(c))["billed_core_h"]
o.append("sum of all 20 fits (18 + A3 canary + XB) = %.2f core-h" % allc)
o.append("\n## ratios by dataset of cell means (islands only; c_X of the rule)")
for ds in ("AR", "ARweak", "ADJOPP"):
    b = [r["isl"] for r in rows if r["ds"] == ds and (r["m"], r["I"]) == (1, 3)]; x = [r["isl"] for r in rows if r["ds"] == ds and (r["m"], r["I"]) == (4, 3)]; z = [r["isl"] for r in rows if r["ds"] == ds and (r["m"], r["I"]) == (1, 0)]
    o.append("- %s islands mean: m1I3 %.3f, m4I3 %.3f (x%.2f), m1I0 %.3f (x%.2f)" % (ds, sum(b) / 2, sum(x) / 2, sum(x) / sum(b), sum(z) / 2, sum(z) / sum(b)))
# R'=16 estimate of the I_max saving (model merge scaling 0.3+0.7*R'/16 -> merge16 = merge64/3.1)
def r16(rr):
    return sum(r["setup"] + r["cal"] + r["isl"] / 4.0 + r["mer"] / 3.1 + r["ev"] for r in rr) / len(rr)
b = [r for r in rows if (r["m"], r["I"]) == (1, 3)]; z = [r for r in rows if (r["m"], r["I"]) == (1, 0)]; x = [r for r in rows if (r["m"], r["I"]) == (4, 3)]
o.append("\n## R'=16 cost per fit estimated from the R'=64 stage costs (islands/4, merge/3.1 per quote_model.py): m1 I3 %.2f, m1 I0 %.2f (saving %.0f%%), m4 I3 %.2f (x%.2f of m1 I3)" % (r16(b), r16(z), 100 * (1 - r16(z) / r16(b)), r16(x), r16(x) / r16(b)))
o.append("calibration share of a fit at R'=64: m1 I3 %.1f%%, m1 I0 %.1f%%; calibration I0 / I3 = %.3f (%.3f / %.3f core-h); quote model assumed U(0.2, 0.5)" % (100 * sum(r["cal"] for r in b) / sum(r["tot"] for r in b), 100 * sum(r["cal"] for r in z) / sum(r["tot"] for r in z), sum(r["cal"] for r in z) / sum(r["cal"] for r in b), sum(r["cal"] for r in z) / len(z), sum(r["cal"] for r in b) / len(b)))
print("\n".join(o))
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fz_tables.json"), "w"), indent=1, default=str)
