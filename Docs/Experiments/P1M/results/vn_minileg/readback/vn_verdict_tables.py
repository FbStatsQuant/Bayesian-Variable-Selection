#!/usr/bin/env python3
"""vn_verdict_tables.py -- DESCRIPTIVE tables of the V-N mini-leg read-back (MINILEG_READBACK.md). NOT a registered script, no rule, no threshold: it reads the records and prints what is in them,
and RE-DERIVES independently (by its own code) the per-dataset ratios and c_X that the registered freeze scripts computed, as a check on them. Stdlib, read-only, python3 -I.
  vn_verdict_tables.py --R ~/SMC_Engineering_Department/records > tables.md        (also writes tables.json next to --out)"""
import argparse, glob, json, math, os, re, sys

ap = argparse.ArgumentParser(); ap.add_argument("--R", required=True); ap.add_argument("--out", required=True); args = ap.parse_args()
R = os.path.expanduser(args.R)
jl = lambda p: json.load(open(p))
mean = lambda xs: sum(xs) / len(xs)


def find(rid):
    d = [p for p in glob.glob(os.path.join(R, "precision1e4", "*", rid)) + glob.glob(os.path.join(R, "vn_minileg", "*", rid)) if os.path.isdir(p)]
    assert len(d) == 1, (rid, d)
    return d[0]


def cost(rid, d):
    c = glob.glob(os.path.join(os.path.dirname(d), "_batch_*", "cost", "cost_%s.json" % rid))
    assert len(c) == 1, (rid, c)
    j = jl(c[0])["stages"]
    return {"islands": j["islands"]["billed_core_h"], "isl_wall": j["islands"]["wall_s_max"], "total": sum(v["billed_core_h"] for v in j.values()), "states": sorted({s for v in j.values() for s in v["states"]})}


def rec(rid):
    d = find(rid); ev = jl(os.path.join(d, "eval.bin.json")); fm = ev["fit"]["meta"]; ev_ = ev["evidence"]; cm = jl(os.path.join(d, "calib_meta.json")); m = cm.get("meta", cm)
    occ = next((e for e in fm.get("occ", []) if e.get("M") == 1000), {})
    isl = jl(os.path.join(d, "island_1.bin.json"))
    c = cost(rid, d)
    return {"rid": rid, "dir": d, "M1": occ.get("sd_log_Z_occ_r"), "M2": ev["pip"]["island_spread"]["max_sd"], "M3": ev_["sigma_hat"], "M3r": ev_.get("sigma_hat_robust"), "hpm": ev["selection"]["hpm"],
            "N": m["N"], "m": m["refine_m"], "I": m["I_max"], "I_used": m["I_used"], "gu": (m.get("flags") or {}).get("grid_unconverged"), "T": isl["T"], "Rp": fm["Rp"], "logZ": ev_["logZ"],
            "logZ_T": ev_["logZ_T"], "R_eff": ev_["R_eff"], "Reff_Rp": ev_["R_eff_over_Rp"], "flags": fm["flags"], "hpm_eq_S0": ev["selection"]["hpm_eq_S0"], "mpm_eq_S0": ev["selection"]["mpm_eq_S0"],
            "occ_inhom": fm["flags"].get("occ_inhomogeneous"), "sections": {s["name"]: s["sha256"] for s in cm["sections"]}, "cost": c,
            "xy": (lambda t: (t.get("X_sha256"), t.get("y_sha256")))(jl(os.path.join(d, "truth.json"))), "bin": cm["binary"].get("sha256") if isinstance(cm.get("binary"), dict) else None}


DS = {"AR": "4-AR-n200-r01", "ARweak": "4-ARweak-n200-r01", "ADJOPP": "4-ADJOPP-n200-r01"}
out = {}; L = []
rows = []
for d, base in DS.items():
    for I in (0, 3):
        for c in (1, 2):
            tw = "%s-P-N2500-m1%s-c%d-s1" % (base, "-I0" if I == 0 else "", c); nw = "%s-P-N10000-m1%s-c%d-s1" % (base, "-I0" if I == 0 else "", c)
            rows.append((d, I, c, rec(tw), rec(nw)))
L.append("## T1. Per fit: the 12 N = 10^4 fits and their N = 2,500 twins (same seed)")
L.append("| dataset | I_max | rep | arm | recorded (N, m, I_max, I_used) | T | M1 sd log Z_occ,r | M2 max PIP sd | M3 sigma-hat | sigma-hat robust | islands billed | islands wall s | fit billed | HPM |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for d, I, c, t, n in rows:
    for lab, r in (("N 2,500 (F)", t), ("**N 10^4 (F2)**", n)):
        L.append("| %s | %d | c%d | %s | (%d, %d, %d, %d) | %d | %.5f | %.6f | %.5f | %.5f | %.3f | %d | %.2f | %s |" % (d, I, c, lab, r["N"], r["m"], r["I"], r["I_used"], r["T"], r["M1"], r["M2"], r["M3"], r["M3r"], r["cost"]["islands"], r["cost"]["isl_wall"], r["cost"]["total"], r["hpm"]))
# independent re-derivation of the rule inputs
L.append("\n## T2. Independent re-derivation of the rule's inputs (this script's own code; compare freeze.json)")
res = {}
for I in (0, 3):
    per = {}
    for met in ("M1", "M2", "M3"):
        per[met] = {}
        for d in DS:
            x = mean([n[met] for dd, II, c, t, n in rows if dd == d and II == I]); b = mean([t[met] for dd, II, c, t, n in rows if dd == d and II == I]); per[met][d] = x / b
    num = [n["cost"]["islands"] for dd, II, c, t, n in rows if II == I]; den = [t["cost"]["islands"] for dd, II, c, t, n in rows if II == I]
    cx = mean(num) / mean(den); bar = 1 / math.sqrt(cx)
    hp = {d: {tuple(r["hpm"]) for dd, II, c, t, n in rows if dd == d and II == I for r in (t, n)} for d in DS}
    res[I] = {"c_X": cx, "bar": bar, "ratios": per, "gm": {m: math.exp(mean([math.log(v) for v in per[m].values()])) for m in per}, "hpm_identical": all(len(v) == 1 for v in hp.values())}
    L.append("**I_max %d** (N 10^4 vs N 2,500): c_X = mean islands billed(X) / mean islands billed(B) = %.4f; bar 1/sqrt(c_X) = %.4f; HPM identical in X u B: %s" % (I, cx, bar, res[I]["hpm_identical"]))
    L.append("| metric | AR | AR-weak | ADJ-OPP | geometric mean | <= bar | every dataset < 1 |"); L.append("|---|---|---|---|---|---|---|")
    for m in ("M1", "M2", "M3"):
        g = res[I]["gm"][m]; p = per[m]
        L.append("| %s | %.4f | %.4f | %.4f | **%.4f** | %s (margin %+.4f) | %s |" % (m, p["AR"], p["ARweak"], p["ADJOPP"], g, "yes" if g <= bar else "**NO**", bar - g, "yes" if all(v < 1 for v in p.values()) else "no"))
out["rule_inputs"] = res
# identity
L.append("\n## T3. Identity (MINILEG_PREREG section 2)")
L.append("| fit | recorded arm = plan | pairing: every calib.bin section except `meta` (calib_meta sections) equal to the twin's | grid sha256 equal | X/y sha equal to twin | binary sha | stages |"); L.append("|---|---|---|---|---|---|---|")
ok_all = True
for d, I, c, t, n in rows:
    secs = sorted((set(t["sections"]) | set(n["sections"])) - {"meta"}); diff = [s for s in secs if t["sections"].get(s) != n["sections"].get(s)]
    arm = (n["N"], n["m"], n["I"]) == (10000, 1, I) and n["I_used"] <= n["I"]
    ok_all &= arm and not diff and t["xy"] == n["xy"] and n["cost"]["states"] == ["COMPLETED"]
    L.append("| %s | %s (%d, %d, %d, I_used %d) | %d sections, %d differing | %s | %s | %s | %s |" % (n["rid"], "yes" if arm else "**NO**", n["N"], n["m"], n["I"], n["I_used"], len(secs), len(diff), "yes" if t["sections"].get("grid") == n["sections"].get("grid") else "NO", "yes" if t["xy"] == n["xy"] else "NO", (n["bin"] or "")[:12], ",".join(n["cost"]["states"])))
L.append("\nall 12: identity OK = %s; binary sha of the 12 N 10^4 fits: %s" % (ok_all, sorted({n["bin"][:12] for *_, n in rows})))
# f
L.append("\n## T4. Measured island factor f = N 10^4 / N 2,500 (same seed, same grid, same T)")
L.append("| fit pair | T | islands billed 2,500 -> 10^4 | f billed | islands wall (max task) 2,500 -> 10^4 | f wall |"); L.append("|---|---|---|---|---|---|")
fb = []; fw = []
for d, I, c, t, n in rows:
    a = n["cost"]["islands"] / t["cost"]["islands"]; w = n["cost"]["isl_wall"] / t["cost"]["isl_wall"]; fb.append(a); fw.append(w)
    L.append("| %s I_max %d c%d | %d | %.3f -> %.3f | %.2f | %d -> %d | %.2f |" % (d, I, c, t["T"], t["cost"]["islands"], n["cost"]["islands"], a, t["cost"]["isl_wall"], n["cost"]["isl_wall"], w))
L.append("\nmean f billed **%.3f** (min %.2f, max %.2f); mean f wall %.2f (min %.2f, max %.2f); the quote assumed 3.85 (3.2-4.6)." % (mean(fb), min(fb), max(fb), mean(fw), min(fw), max(fw)))
out["f"] = {"billed_mean": mean(fb), "billed_min": min(fb), "billed_max": max(fb), "wall_mean": mean(fw)}
# XB2
xb = rec("4-AR-n200-r01-P-N2500-m1-I0-XB2-s1"); lg = rec("4-AR-n200-r01-P-N2500-m1-I0-c1-s1")
ex = jl(os.path.join(xb["dir"], "eval.bin.json")); el = jl(os.path.join(lg["dir"], "eval.bin.json"))
lr_eq = ex["evidence"]["logZ_r"] == el["evidence"]["logZ_r"]
oh = lambda r: [jl(os.path.join(r["dir"], "island_%d.bin.json" % i))["output_hash"] for i in range(1, 65)]
L.append("\n## T5. XB2 (F2 vs the leg's F record, AR c1 I_max 0, N 2,500, R' 64)")
L.append("logZ_r (64 values) bit-equal: **%s**; HPM equal: %s; island output_hash 64/64 equal: **%s**; recorded arm (%d, %d, %d, I_used %d); binary %s vs %s; fit billed %.2f vs %.2f core-h. (The full `xb_check` comparison is in `xb_check_XB2_output.txt`.)"
         % (lr_eq, ex["selection"]["hpm"] == el["selection"]["hpm"], oh(xb) == oh(lg), xb["N"], xb["m"], xb["I"], xb["I_used"], (xb["bin"] or "")[:8], (lg["bin"] or "")[:8], xb["cost"]["total"], lg["cost"]["total"]))
out["XB2"] = {"logZ_r_equal": lr_eq, "island_hash_equal": oh(xb) == oh(lg)}
# r04
r0 = [p for p in glob.glob(os.path.join(R, "precision1e4", "S*", "4-ADJOPP-n200-r04-V-s1")) if os.path.isdir(p)]
assert len(r0) == 1
def rec_dir(rid, d):
    global find
    old = find
    find = lambda x: d
    try:
        return rec(rid)
    finally:
        find = old
# cost lookup for the original lives in its own wave dir
r04 = [("original r04 s1, I_max 0 (F, science S*)", rec_dir("4-ADJOPP-n200-r04-V-s1", r0[0])), ("**twin r04 s1, I_max 3 (F2)**", rec("4-ADJOPP-n200-r04-VI3-s1")), ("**r04 seed 2, I_max 0 (F2)**", rec("4-ADJOPP-n200-r04-V-s2"))]
L.append("\n## T6. r04 check (report-only): ADJ-OPP n = 200 rep 4, R' 16, N 2,500")
L.append("| fit | I_max / I_used | island T | sigma-hat = sd(log Z_r) | robust | R_eff/R' | E1 / E2 / E3 | low_empirical_ESS | log Z-hat - log Z_T | HPM = S0 / MPM = S0 | M1 | M2 | occ_inhomog. | fit billed |"); L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for lab, r in r04:
    f = r["flags"]
    L.append("| %s | %d / %d | %d | %.4f | %.4f | %.3f | %s / %s / %s | %s | %+.4f | %s / %s | %.5f | %.6f | %s | %.2f |" % (lab, r["I"], r["I_used"], r["T"], r["M3"], r["M3r"], r["Reff_Rp"], f.get("E1"), f.get("E2"), f.get("E3"), f.get("low_empirical_ESS"), r["logZ"] - r["logZ_T"], r["hpm_eq_S0"], r["mpm_eq_S0"], r["M1"], r["M2"], r["occ_inhom"], r["cost"]["total"]))
out["r04"] = {lab: {k: r[k] for k in ("I", "I_used", "T", "M3", "Reff_Rp", "logZ", "logZ_T", "hpm_eq_S0")} for lab, r in r04}
open(args.out + ".json", "w").write(json.dumps(out, indent=1, default=str))
print("\n".join(L))
