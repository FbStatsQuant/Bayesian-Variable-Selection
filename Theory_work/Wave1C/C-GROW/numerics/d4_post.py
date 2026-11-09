"""D4 post-processing: reads d4_out/sum_*.json (production core, no LS0) + d4_data (same X, y as Python) -> D4_raw.csv, D4_summary.md"""
import glob, json, os, sys
import numpy as np, pandas as pd
import bvs_core as bc, d_common as dc, study_common as sc

def arr(v):
    if v is None: return []
    return [int(x) for x in np.atleast_1d(v)]

rows = []
for f in sorted(glob.glob("d4_out/sum_*.json")):
    J = json.load(open(f))
    scen, n, seed = J["scen"], J["n"], J["seed"]
    spec, X, y = sc.build_xy((scen, 100, 4, 5, 1.0, n, seed, "iid"))
    # data check: exported CSV equals regenerated data
    if os.path.exists("d4_data/X_S%d_n%d_s%d.csv" % (scen, n, seed)):  # input CSVs were deleted after use; regenerate with d4_export.py to re-check
        Xc = np.loadtxt("d4_data/X_S%d_n%d_s%d.csv" % (scen, n, seed), delimiter=",", max_rows=3)
        assert np.allclose(Xc, X[:3], rtol=1e-12, atol=1e-12)
    S0 = tuple(sorted(spec["S0"]))
    prob = bc.Problem(X, y)
    hpm = tuple(sorted(i - 1 for i in arr(J["hpm"])))
    FR = float(J["hpm_F"])
    off = FR - prob.F(hpm)
    tops = [tuple(sorted(i - 1 for i in arr(m))) for m in J["top_models"]]
    tv = np.array(J["top_values"], float)
    chk = [abs((tv[i] - prob.F(tops[i])) - off) for i in range(min(40, len(tops)))]
    FS0_R = prob.F(S0) + off
    in_top = S0 in set(tops)
    tmin = float(tv.min()); full = bool(J["top_full"])
    ls_c = tuple(sorted(i - 1 for i in arr(J["ls_centre"])))
    ls_path = [tuple(sorted(i - 1 for i in arr(m))) for m in (J["ls_path"] or [])]
    ls_scanned = [tuple(sorted(i - 1 for i in arr(m))) for m in (J["ls_scanned_centres"] or [])]
    centres = set([ls_c] + ls_path + ls_scanned)
    ls_adj = any(dc.is_nb_or_eq(c, S0) for c in centres)
    if hpm == S0 or in_top or ls_adj:
        scored, why = True, ("HPM" if hpm == S0 else "top_store" if in_top else "final-LS neighbour")
    elif full and FS0_R > tmin:
        scored, why = False, "F(S0) above top-store minimum but S0 not in store"
    elif FS0_R > FR + 1e-9:
        scored, why = False, "F(S0) > F(HPM)"
    else:
        scored, why = None, "undecidable"
    rows.append(dict(scen=scen, n=n, seed=seed, status=J["status"], branch=J["branch"], secs=round(J["secs"], 1),
                     hpm=json.dumps(list(hpm)), hpm_size=len(hpm), hpm_eq_S0=(hpm == S0), hpm_contains_S0=set(S0) <= set(hpm),
                     hpm_extra=len(set(hpm) - set(S0)), hpm_missing=len(set(S0) - set(hpm)),
                     hpm_F_minus_FS0=FR - FS0_R, hpm_before_local_eq_S0=(tuple(sorted(i - 1 for i in arr(J["hpm_before_local"]))) == S0),
                     ls_moves=J["ls_moves"], ls_termination=J["ls_termination"], ls_certified=J["local_certified"],
                     S0_in_top_store=in_top, top_full=full, top_min_minus_FS0=tmin - FS0_R, S0_scored=scored, S0_scored_reason=why,
                     scorer_offset=off, scorer_offset_maxdev=max(chk) if chk else None,
                     n_distinct_hll=J["n_distinct_hll"], registry_mode=J["registry_mode"], hpm_phase=J["hpm_prov"]["phase"], hpm_mech=J["hpm_prov"]["mechanism"],
                     near_ties=len(arr(J["near_ties"])) if not isinstance(J["near_ties"], list) else len(J["near_ties"]),
                     E1=J["flags"].get("E1"), E3=J["flags"].get("E3")))
df = pd.DataFrame(rows)
df.to_csv("D4_raw.csv", index=False)
out = []
df["set"] = np.where(df.seed >= 10, "targeted seed %s" % "(Python best model != S0)", "seeds 0-4")
for (scen, n, st), g in df.groupby(["scen", "n", "set"]):
    prov = ", ".join("%s/%s x%d" % (a, b, k) for (a, b), k in g.groupby(["hpm_phase", "hpm_mech"]).size().items())
    out.append("| S%d p=100 c=1 n=%d (%s) | %d | %d/%d | %d/%d | %d/%d | %s | %s | %s | %s | %d/%d | %.0f (%.0f-%.0f) | %.1e |" % (
        scen, n, st, len(g), g.hpm_eq_S0.sum(), len(g), g.hpm_contains_S0.sum(), len(g), g.hpm_before_local_eq_S0.sum(), len(g),
        "%d scored / %d not / %d undecidable" % ((g.S0_scored == True).sum(), (g.S0_scored == False).sum(), g.S0_scored.isna().sum()),
        "%d/%d" % (g.S0_in_top_store.sum(), len(g)), "%d (max %d)" % (g.hpm_extra.sum(), g.hpm_extra.max()), prov, g.ls_certified.sum(), len(g),
        g.secs.median(), g.secs.min(), g.secs.max(), g.scorer_offset_maxdev.max()))
hdr = ("| design | fits | HPM = S0 | HPM contains S0 | HPM before final LS = S0 | S0 in scored set (decided) | S0 in top store | extras in HPM (total, max) | "
       "HPM first scored in (phase/mechanism) | final LS from global best certified | secs med (min-max) | max dev. of R-vs-Python score offset (top-40) |\n"
       + "|" + "---|" * 12 + "\n")
intro = ("## D4: production core WITHOUT LS0 (R 4.4.1, `v3_fit`, allocation 8 GB / 1 h), same (X, y) as the Python runs\n\n"
         "Scripts: `d4_export.py` (writes X, y from the Python generator) -> `d4_run.R` / `d4_batch.py` (fits; the core was copied to `d4_core/` and compiled there, 28 s) -> `d4_post.py` (this table, `D4_raw.csv`). "
         "Fields used: `hpm` (reported HPM), `top_store` (top 4001 scored models by F), `local_search` (final local-search archive), `instrumentation$scored` (distinct-model count, HLL), `hpm_before_local`, `hpm_provenance`.\n\n"
         "**Is the scored set observable?** Not exactly. `v3_fit` exports the per-model scored set (`cpp_registry_scored_set`) only for p <= 32; at p = 100 the registry is in HLL mode (`n_distinct_hll` = approximate number of distinct scored models, no model list). "
         "What is exact: (i) the HPM (best F over all scored models, so F(S0) > F(HPM) would prove that S0 was never scored); (ii) the top store (the 4001 best scored models; full in every fit); (iii) the final local-search archive (centre, path, scanned centres, `scan_size`). "
         "'S0 in scored set (decided)': scored if HPM = S0, or S0 in the top store, or S0 adjacent to a final-LS centre; not scored if F(S0) is above the top-store minimum yet S0 is absent; otherwise undecidable (count shown). "
         "The R scores equal the Python F up to one additive constant per data set (last column), so F(S0) is taken from the Python scorer. R seed = 1000 + data seed. c = 1, p = 100.\n\n")
open("D4_summary.md", "w").write(intro + hdr + "\n".join(out) + "\n")
print(open("D4_summary.md").read()[-3000:])
