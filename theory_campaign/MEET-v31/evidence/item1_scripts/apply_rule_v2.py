"""Apply the item-1 decision rule (SYNTH_R2 §2 + SYNTH_R3 R3-6 conventions) to ABL-START per_fit.csv.
Version 2 (HQ correction, 2026-11-04, after the SOL2 audit F04): enforces the recorded absolute gate "fewer than 9 conclusive designs => Outcome 2" (R3_B:42). v1 (apply_rule.py, f53d0af) is kept unchanged as the pre-registered evidence.
Operationalisation (chair, declared here):
 - arms A, B, C only (D is v2 evidence).
 - design conclusive iff all of A, B, C have status 'completed' AND range of the three arms' log Z <= 1 nat.
 - depth_A_ok: T_final_A <= min(T_B, T_C) AND rebuilds_total_A <= min(rebuilds_B, rebuilds_C).
 - accuracy uses |dlogZ| (leave-one-arm-out reference) with tolerance sigma = SD of the worse-scoring arm's 4 log Zhat_r:
     A 'not worse' than X  iff |dlogZ_A| <= |dlogZ_X| + sd_A ;  X 'beats' A iff |dlogZ_X| + sd_X < |dlogZ_A|.
   Ẑ-weighted PIP max-error vs reference is reported, with 'worse' meaning > 0.05 absolute (reported, not decisive).
 - Outcome 1: depth_A_ok on >= 3/4 of conclusive designs (9/12) AND A not worse than both B and C on >= 3/4.
 - Outcome 3: B or C beats A on >= 3/4 of conclusive designs, the conclusive set includes both S4 and both S5 designs and
   the winner beats A on all of them, and the winner is not worse on depth (T, rebuilds) on any S4/S5 design.
 - else, or if fewer than 9 designs are conclusive (with 12 complete) / fewer than 3/4 of completed: Outcome 2.
"""
import csv, sys, math, collections
rows = [r for r in csv.DictReader(open(sys.argv[1])) if r["arm"] in "ABC"]
D = collections.defaultdict(dict)
for r in rows: D[(r["id"], r["scale"])][r["arm"]] = r
f = lambda x: float("nan") if x in ("", "NA") else float(x)
out = []; concl = []
for k in sorted(D):
    a = D[k]; rec = {"design": f"{k[0]} {k[1]}", "scen": k[0].split("_")[1]}
    complete = all(x in a and a[x]["status"] == "completed" for x in "ABC")
    rec["complete"] = complete
    if complete:
        lz = [f(a[x]["log_Z"]) for x in "ABC"]; rec["logZ_range"] = max(lz) - min(lz)
        rec["conclusive"] = rec["logZ_range"] <= 1.0
        T = {x: f(a[x]["T_final"]) for x in "ABC"}; Rb = {x: f(a[x]["rebuilds_total"]) for x in "ABC"}
        rec.update({f"T_{x}": T[x] for x in "ABC"}); rec.update({f"reb_{x}": Rb[x] for x in "ABC"})
        rec["depth_A_ok"] = T["A"] <= min(T["B"], T["C"]) and Rb["A"] <= min(Rb["B"], Rb["C"])
        e = {x: abs(f(a[x]["dlogZ"])) for x in "ABC"}; s = {x: f(a[x]["sd_logZ_r"]) for x in "ABC"}
        rec.update({f"absdlogZ_{x}": e[x] for x in "ABC"}); rec.update({f"sd_{x}": s[x] for x in "ABC"})
        rec["A_not_worse"] = all(e["A"] <= e[x] + s["A"] for x in "BC")
        rec["B_beats_A"] = e["B"] + s["B"] < e["A"]; rec["C_beats_A"] = e["C"] + s["C"] < e["A"]
        rec.update({f"pipzw_{x}": f(a[x]["pip_zw_maxerr"]) for x in "ABC"})
        for x in "BC": rec[f"{x}_depth_not_worse"] = T[x] <= T["A"] and Rb[x] <= Rb["A"]
        rec.update({f"sec_{x}": f(a[x]["sec_cal"]) + f(a[x]["sec_final"]) for x in "ABC"})
        rec.update({f"hpmS0_{x}": a[x]["hpm_eq_S0"] for x in "ABC"})
    else: rec["conclusive"] = False
    out.append(rec)
C = [r for r in out if r["conclusive"]]; n = len(C); ncomp = sum(r["complete"] for r in out)
print(f"designs: {len(out)}  complete(A,B,C): {ncomp}  conclusive: {n}")
need = max(9, math.ceil(0.75 * max(ncomp, 1)))  # v2: absolute 9-conclusive gate
o1 = n >= need and sum(r["depth_A_ok"] for r in C) >= math.ceil(.75*n) and sum(r["A_not_worse"] for r in C) >= math.ceil(.75*n)
o3 = False
for x in "BC":
    beats = sum(r[f"{x}_beats_A"] for r in C)
    hard = [r for r in C if r["scen"] in ("S4", "S5")]
    if n >= need and beats >= math.ceil(.75*n) and len(hard) == 4 and all(r[f"{x}_beats_A"] for r in hard) \
       and all(r[f"{x}_depth_not_worse"] for r in hard): o3 = True; print("Outcome 3 triggered by arm", x)
print("counts: depth_A_ok", sum(r["depth_A_ok"] for r in C), "A_not_worse", sum(r["A_not_worse"] for r in C),
      "B_beats_A", sum(r["B_beats_A"] for r in C), "C_beats_A", sum(r["C_beats_A"] for r in C), "of", n)
print("OUTCOME:", 3 if o3 else (1 if o1 else 2))
w = csv.DictWriter(open(sys.argv[2], "w"), fieldnames=sorted({k for r in out for k in r})); w.writeheader(); w.writerows(out)
