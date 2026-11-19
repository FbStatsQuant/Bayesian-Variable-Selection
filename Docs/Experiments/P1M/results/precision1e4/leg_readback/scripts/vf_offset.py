#!/usr/bin/env python3
"""vf_offset.py: the `vf` row of the offset surface (ADDENDUM_2_VF) and the B1 point, computed with the REGISTERED reader precision_offset.py
(sha cbbc2301..., imported unchanged: parse, blocks_mean, jensen, summ, find_runs, eval_file).  The registered script's run-id pattern does not accept VF
and its arm check would call a VF fit ARM_MISMATCH (it wants I_max 3), so the VF fits are parsed here under the V name and their recorded arm is
verified HERE (N 2500, m 1, I_max 0, rule bounded, I_used 0).  Descriptive; no pass/fail; not part of the registered surface."""
import importlib.util, json, math, os, re, sys
P = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/precision1e4/precision_offset.py"
spec = importlib.util.spec_from_file_location("po", P); po = importlib.util.module_from_spec(spec); spec.loader.exec_module(po)
R = os.path.expanduser("~/SMC_Engineering_Department/records")
runs, dups = po.find_runs([R + "/overlap1e4/" + w for w in ("W0", "W1", "W2", "W3")])
recs = [po.parse(r, d) for r, d in sorted(runs.items())]
T = {}
for r in recs:
    if r["arm"] == "T" and not r["problems"]:
        T.setdefault(r["ds"], []).append(r)
Tbar = {d: po.mean([r["logZ"] for r in rs]) for d, rs in T.items()}
sT = math.sqrt(po.mean([(rs[0]["logZ"] - rs[1]["logZ"]) ** 2 / 2.0 for rs in (sorted(v, key=lambda r: r["seed"]) for v in T.values()) if len(rs) == 2]))
ovl = {r["run_id"]: r for r in recs if r["arm"] == "V" and not r["problems"]}
vf = {}
bad = []
for w in ("S1", "S2"):
    for n in sorted(os.listdir(R + "/precision1e4/" + w)):
        if re.match(r"^4-[A-Za-z]+-n200-r\d+-VF-s\d$", n):
            dp = R + "/precision1e4/%s/%s" % (w, n)
            vid = n.replace("-VF-", "-V-")
            o = po.parse(vid, dp)
            cm = json.load(open(dp + "/calib_meta.json"))["meta"]
            ok = (cm["N"], cm["refine_m"], cm["I_max"], cm["I_used"], cm["rule"]) == (2500, 1, 0, 0, "bounded")
            o["problems"] = [x for x in o["problems"] if not x.startswith("ARM_MISMATCH")]
            if not ok or o["problems"]:
                bad.append((n, o["problems"], cm["N"], cm["refine_m"], cm["I_max"], cm["I_used"], cm["rule"]))
            vf[vid] = o
assert len(vf) == 14 and not bad, bad
out = {"script": "vf_offset.py", "reader": "precision_offset.py cbbc2301 (imported)", "s_T": sT, "rows": {}}
def cell_rows(fits, ks):
    rows = []
    for rid, f in fits.items():
        for k in ks:
            L = f["logZ"] if k == f["Rp"] else po.blocks_mean(f["logZ_r"], k)
            jn, v = po.jensen(f["logZ_r"], k)
            rows.append((rid, f["ds"], int(rid.rsplit("-s", 1)[1]), k, L - Tbar[f["ds"]], jn))
    return rows
ks = (4, 8, 16)
def table(rows):
    res = {}
    for k in ks:
        byds = {}
        for rid, ds, s, kk, D, jn in rows:
            if kk == k: byds.setdefault(ds, []).append((D, jn))
        Dds = {d: po.mean([x[0] for x in v]) for d, v in byds.items()}
        sm = po.summ(list(Dds.values()))
        res[k] = {"datasets": len(Dds), "fits": sum(len(v) for v in byds.values()), "delta": sm["mean"], "se": sm["se"], "lo": sm["lo"], "hi": sm["hi"], "neg": sm["neg"],
                  "delta_over_sT": sm["mean"] / sT, "jensen_mean": po.mean([x[1] for v in byds.values() for x in v]), "per_dataset": {d: round(v, 6) for d, v in sorted(Dds.items())}}
    return res
rows_vf = cell_rows(vf, ks)
out["vf_all14"] = table(rows_vf)
# matched comparison: the SAME (dataset, seed) fits at I_max 3 (overlap) vs I_max 0 (VF), k = 16 (full pool)
twin = {rid: ovl[rid] for rid in vf}
rows_i3 = cell_rows(twin, ks)
out["ovl_I3_same14"] = table(rows_i3)
# paired by dataset: VF - I3 on the same fits (descriptive companion, NOT a registered contrast)
for k in ks:
    d0, d3 = {}, {}
    for rid, ds, s, kk, D, jn in rows_vf:
        if kk == k: d0.setdefault(ds, []).append(D)
    for rid, ds, s, kk, D, jn in rows_i3:
        if kk == k: d3.setdefault(ds, []).append(D)
    diffs = {d: po.mean(d0[d]) - po.mean(d3[d]) for d in d0}
    sm = po.summ(list(diffs.values()))
    out.setdefault("paired_VF_minus_I3_same_fits", {})[k] = {"datasets": sm["n"], "mean": sm["mean"], "se": sm["se"], "lo": sm["lo"], "hi": sm["hi"], "neg": sm["neg"], "per_dataset": {d: round(v, 6) for d, v in sorted(diffs.items())}}
# per fit differences VF - I3 in log Z (14)
pf = {}
for rid in sorted(vf):
    pf[rid] = {"logZ_VF": vf[rid]["logZ"], "logZ_I3": ovl[rid]["logZ"], "diff": vf[rid]["logZ"] - ovl[rid]["logZ"]}
out["per_fit_VF_minus_I3"] = pf
dd = [v["diff"] for v in pf.values()]
out["per_fit_VF_minus_I3_summary"] = {"n": len(dd), "mean": po.mean(dd), "sd": po.sd(dd), "min": min(dd), "max": max(dd)}
# B1 point (k = 16): mean over the 2 seeds of V - T log Z-hat
b1 = {}
for s in (1, 2):
    v = json.load(open(R + "/precision1e4/B1/4-ARweak-n100-r91-V-s%d/eval.bin.json" % s)); t = json.load(open(R + "/precision1e4/B1/4-ARweak-n100-r91-T-s%d/eval.bin.json" % s))
    b1[s] = {"V": v["evidence"]["logZ"], "T": t["evidence"]["logZ"], "diff": v["evidence"]["logZ"] - t["evidence"]["logZ"], "Rp_V": v["fit"]["meta"]["Rp"], "Rp_T": t["fit"]["meta"]["Rp"],
             "T_N": t["fit"]["meta"]["N"], "T_tier": t["fit"]["meta"]["tier"]}
out["B1_point"] = {"per_seed": b1, "delta": po.mean([b1[s]["diff"] for s in b1]), "over_sT": po.mean([b1[s]["diff"] for s in b1]) / sT,
                   "seed_sd": po.sd([b1[s]["diff"] for s in b1])}
json.dump(out, open("vf_offset.json", "w"), indent=1)
for k in ks:
    t = out["vf_all14"][k]; u = out["ovl_I3_same14"][k]; q = out["paired_VF_minus_I3_same_fits"][k]
    print("k=%d VF: delta %+.5f se %.5f CI %+.5f..%+.5f neg %d/%d (%+.2f sT) Jensen %+.1e | I3 same fits: %+.5f CI %+.5f..%+.5f | VF-I3 paired %+.5f CI %+.5f..%+.5f neg %d/%d" % (
        k, t["delta"], t["se"], t["lo"], t["hi"], t["neg"], t["datasets"], t["delta_over_sT"], t["jensen_mean"], u["delta"], u["lo"], u["hi"], q["mean"], q["lo"], q["hi"], q["neg"], q["datasets"]))
print("per-dataset VF k=16", out["vf_all14"][16]["per_dataset"])
print("per-dataset I3 same fits k=16", out["ovl_I3_same14"][16]["per_dataset"])
print("per-fit VF-I3", out["per_fit_VF_minus_I3_summary"])
print("B1", out["B1_point"])
