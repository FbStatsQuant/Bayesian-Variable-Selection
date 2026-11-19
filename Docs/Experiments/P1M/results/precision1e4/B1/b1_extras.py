#!/usr/bin/env python3
"""B1 extras (stdlib, read-only): xeval self-check vs engine h2 (bit-exact), HPM / spread table, offset cell delta_B1 (ADDENDUM_1_BOUNDARY 'Offset cell'; a point, no test)."""
import json, math, os, glob
R = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4/B1"); here = os.path.dirname(os.path.abspath(__file__)); ds = "4-ARweak-n100-r91"; sT = 0.00324
out = []
nb = 0
for a in "VT":
    for s in (1, 2):
        x = json.load(open("%s/cross/selfchk_%s_%s_s%d.json" % (here, ds, a, s)))["xeval"]["h2"]; e = json.load(open("%s/%s-%s-s%d/eval.bin.json" % (R, ds, a, s)))["dist"]["T"]["predictive"]["h2"]
        out.append("selfcheck %s s%d xeval %r engine %r %s" % (a, s, x, e, "BIT-EQUAL" if x == e else "DIFFERENT %.3e" % (x - e))); nb += (x == e)
out.append("%d of 4 self-checks bit-equal" % nb)
out.append("\nfit | HPM (size) | HPM = S0 | F_hpm | F_S0 | F_hpm-F_S0 | HPM mass exp(F_hpm-logZ) | occ M=1 | sup_null PIP | min_true PIP | island PIP max sd | logZ | store models | core-h | tier / N_final")
rows = {}
for a in "VT":
    for s in (1, 2):
        d = "%s/%s-%s-s%d" % (R, ds, a, s); e = json.load(open(d + "/eval.bin.json")); sel = e["selection"]; fm = e["fit"]["meta"]; c = json.load(open(glob.glob("%s/_batch_*/cost/cost_%s-%s-s%d.json" % (R, ds, a, s))[0]))
        occ1 = [o for o in fm["occ"] if o["M"] == 1][0]["occ"]
        mass = math.exp(sel["F_hpm"] - e["evidence"]["logZ"]); sp = e["pip"]["island_spread"]["max_sd"] if "island_spread" in e["pip"] else None
        rows[(a, s)] = dict(logZ=e["evidence"]["logZ"], mass=mass, core=c["billed_core_h"])
        out.append("%s s%d | %s (%d) | %s | %.6f | %.4f | %+.3f | %.4f | %.4f | %.5f | %.2e | %.5f | %.4f | %d | %.2f | %s / %s" % (a, s, sel["hpm"], sel["hpm_size"], sel["hpm_eq_S0"], sel["F_hpm"], sel["F_S0"], sel["F_hpm_minus_F_S0"], mass, occ1,
              e["pip"]["T"]["sup_null"], e["pip"]["T"]["min_true"], sp, e["evidence"]["logZ"], e["store"].get("law_models", 0) if isinstance(e["store"], dict) else 0, c["billed_core_h"], fm.get("tier"), fm.get("N")))
d1, d2 = rows[("V", 1)]["logZ"] - rows[("T", 1)]["logZ"], rows[("V", 2)]["logZ"] - rows[("T", 2)]["logZ"]; dl = (d1 + d2) / 2; spread = abs(d1 - d2) / math.sqrt(2)
out.append("\nOFFSET CELL bnd (N 2,500, m 1, I_max 3, k = 16; ONE dataset, a point, not tested; no offset-vs-p):")
out.append("  per seed pair V - T: s1 %+.5f (%+.2f s_T), s2 %+.5f (%+.2f s_T)" % (d1, d1 / sT, d2, d2 / sT))
out.append("  delta_B1 = mean over the 2 seeds = %+.5f = %+.2f s_T (s_T = %.5f); seed spread (sd of the 2 pair differences) %.5f = %.2f s_T" % (dl, dl / sT, sT, spread, spread / sT))
for a in "VT":
    for s in (1, 2):
        e = json.load(open("%s/%s-%s-s%d/eval.bin.json" % (R, ds, a, s)))["evidence"]; out.append("  island se of logZ %s s%d: %.5f (sigma_hat %.4f)" % (a, s, e["sigma_hat"] / math.sqrt(len(e["logZ_r"])), e["sigma_hat"]))
tot = sum(r["core"] for r in rows.values()); out.append("\ncore-h: V %.4f / %.4f, T %.4f / %.4f; B1 total %.2f (quote 115, wave stop 230, T report line 172.5)" % (rows[("V", 1)]["core"], rows[("V", 2)]["core"], rows[("T", 1)]["core"], rows[("T", 2)]["core"], tot))
print("\n".join(out)); open(here + "/b1_extras_output.txt", "w").write("\n".join(out) + "\n")
