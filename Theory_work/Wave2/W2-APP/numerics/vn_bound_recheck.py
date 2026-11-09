"""R07 #14: recompute the Lemma VN numerical bound as STATED in L5 (min(K - s0, |N| - 15 s0)) against the TOTAL number of
extras n_extra = |S~0 minus S0| (not visible nulls in the mode), from n3_merged.csv; V3b (sum theta = 0) is a no-claim
control (VNF fails) and is marked n/a. Descriptive only: VN is asymptotic; no onset is computed or certified."""
import csv, collections
rows = list(csv.DictReader(open("n3_merged.csv")))
agg = collections.defaultdict(list)
for r in rows:
    s0, K, nv, ne = int(r["s0"]), int(r["K"]), int(r["n_visible"]), int(r["n_extra"])
    b = None if r["design"] == "V3b" else min(K - s0, nv - 15 * s0)
    agg[(r["design"], int(r["n"]), int(r["p"]), s0)].append((ne, b, int(r["mode_size"]), r["ls_final_eq_S0"] == "True", r["ls_certified"] == "True"))
out = ["design n p s0 | n_extra (min..max) | stated VN bound | runs with n_extra >= bound | LS0 final=S0 & certified"]
for k in sorted(agg):
    v = agg[k]; b = v[0][1]
    met = "n/a (control)" if b is None else f"{sum(ne >= b for ne,*_ in v)}/{len(v)}"
    out.append(f"{k[0]} {k[1]} {k[2]} {k[3]} | {min(x[0] for x in v)}..{max(x[0] for x in v)} | {'n/a' if b is None else b} | {met} | {sum(x[3] and x[4] for x in v)}/{len(v)}")
tot = collections.Counter(r["design"] for r in rows)
out.append("runs per design: " + ", ".join(f"{d}={c}" for d, c in sorted(tot.items())))
out.append("V3b mode sizes (min..max over runs): " + str(min(int(r['mode_size']) for r in rows if r['design']=='V3b')) + ".." + str(max(int(r['mode_size']) for r in rows if r['design']=='V3b')))
open("vn_bound_recheck_out.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
