# PREREG ADDENDUM 1: the T-arm N check accepts the calibration's escalated N

**Status: APPROVED by HQ (H-21, HQ_DECISIONS 8b48bb07, 2026-11-18 evening) as a scoring-bug fix only; IN FORCE from W1.** Conditions: committed with the sha256 below before any W1 read-back; every read-back shows the registered script's output AND v2's side by side; the registered sha stays reproducible. Date: 2026-11-18. Author: Sonnet builder (Engineering). Deviation class: OVERLAP_1e4_PREREG.md §9 (change to the registered comparison script).

## Reason
The pre-registration fixes the T arm as "law mode, N = 10^4, coded calibration with escalation (D-26)". Escalation is therefore part of the registered T method: when the calibration checks fail at tier k, N is raised by 4x and the fit is delivered at `N_final = N_plan x 4^tier_final`. The registered script's N check was written assuming tier 0: it requires `meta.N == 10000` for every T fit and marks any escalated fit "not delivered" (`arm settings: N = 40000, pre-registered 10000`), which drives criterion D, and with it the whole outcome, to INCOMPLETE. In W0, 1 of 2 T fits (4-AR-n200-r01-T-s1) escalated to tier 1, N_final = 40,000 (W0_READBACK.md §4-7); the engine and the driver now enforce the islands at the calibration's N (#86), so such fits are the expected case, not a failure.

## Change (and only this)
- T fits: the N check is `N == 10000 x 4^tier_final`, with `tier_final` = `fit.meta.tier` (the recorded tier, an integer >= 0). A T fit with no recorded tier keeps the registered N = 10^4; a T fit whose N does not match its own recorded tier is still "not delivered" (tests: tier 0 with N 40,000; tier 1 with N 10,000).
- `tier_final` and `N_final` are reported per fit in per_fit.csv, per_dataset.csv (`tier_final_<arm>_s<seed>`, `N_final_<arm>_s<seed>`) and verdict.json (`fits_tier_N`; also in wave_check.csv).
- V fits: unchanged (N = 2500, R' = 16, class A, island_isa). No threshold, metric, criterion, outcome rule or other check changed; `PREREG` is byte-identical.
- The registered script `compare_overlap.py` is NOT edited (sha stays reproducible); the new script is `compare_overlap_v2.py`.

## Hashes (sha256)
| file | sha256 |
|---|---|
| compare_overlap.py (registered, unchanged) | `311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea` |
| compare_overlap_v2.py (this addendum) | `4f402e5127efd4754cf25e4ade6ad799f697ebc28e1c657ff49f93fd2905b5c6` |
| tests/test_compare_overlap_v2.py | `a703e38a322d5597ff0e083a1ed52cfcbbeed7872bc41d8d87341f05f79d1706` |

## Exact diff (`diff -u compare_overlap.py compare_overlap_v2.py`, header lines dropped)
```diff
@@ -1,5 +1,9 @@
 #!/usr/bin/env python3
-"""compare_overlap.py -- 10^4 T-vs-V overlap rung: pre-registered comparison (OVERLAP_1e4_PREREG.md).
+"""compare_overlap_v2.py -- 10^4 T-vs-V overlap rung: pre-registered comparison (OVERLAP_1e4_PREREG.md).
+
+  v2 = compare_overlap.py (registered sha 311bbad8...) + ONE change, PREREG_ADDENDUM_1.md (pending HQ approval): a T fit's N check
+  accepts the fit's own calibration N_final = N_plan * 4^tier_final (coded calibration escalates by tier, D-26; the registered check
+  assumed tier 0).  tier_final / N_final are reported per fit (per_fit.csv, per_dataset.csv, verdict.json).  Nothing else differs.
 
 Python 3 standard library only (numpy is NOT used).  READ-ONLY on the run directories.
 
@@ -265,7 +269,16 @@
     rec.update({"N": N, "Rp": Rp, "mode": mode, "island_isa": isa, "tier": meta.get("tier"),
                 "flags": {k: v for k, v in (meta.get("flags") or {}).items() if v is True},
                 "binary_sha": dig(ev, "binary", "sha256"), "fit_binary_sha": dig(meta, "binary", "sha256")})
-    for lab, got, want in (("N", N, spec["N"]), ("Rp", Rp, spec["Rp"])):
+    tier_final = meta.get("tier")
+    # ADDENDUM_1: a T fit is delivered at its own calibration N_final = N_plan * 4^tier_final (D-26); the tier must be recorded.
+    # V fits (bounded plan, no tier) and a T fit with no recorded tier keep the registered N.
+    n_want = spec["N"]
+    if rec["arm"] == "T" and isinstance(tier_final, int) and not isinstance(tier_final, bool) and tier_final >= 0:
+        n_want = spec["N"] * 4 ** tier_final
+    rec["tier_final"] = tier_final
+    rec["N_final"] = N
+    rec["N_expected_at_tier"] = n_want
+    for lab, got, want in (("N", N, n_want), ("Rp", Rp, spec["Rp"])):
         if got is None:
             rec["warnings"].append("%s not found in eval/fit/manifest (unverified)" % lab)
         elif got != want:
@@ -524,6 +537,7 @@
                 row["logZ_%s_s%d" % (a, s)] = r["logZ"]
                 row["logZ_T_%s_s%d" % (a, s)] = r["logZ_T"]
                 row["se_isl_%s_s%d" % (a, s)] = r["se_logZ_isl"]
+                row["tier_final_%s_s%d" % (a, s)], row["N_final_%s_s%d" % (a, s)] = r.get("tier_final"), r.get("N_final")
         if full and dfV > 0 and dfT > 0:
             def arm_var(a, s2):
                 isl = [zs[(a, s)]["se_logZ_isl"] for s in seeds]
@@ -746,6 +760,7 @@
                 row["reasons_" + a] = " | ".join(r["reasons"])
                 row["core_h_" + a] = r["core_h"]
                 row["tier_" + a] = r.get("tier")
+                row["tier_final_" + a], row["N_final_" + a] = r.get("tier_final"), r.get("N_final")
                 row["flags_" + a] = ",".join(sorted(r.get("flags", {})))
         if v and t and v["delivered"] and t["delivered"]:
             row["X_y_sha_equal"] = (v["X_sha"], v["y_sha"]) == (t["X_sha"], t["y_sha"])
@@ -805,6 +820,7 @@
         r = recs[rid]
         out.append({"run_id": rid, "arm": r["arm"], "seed": r["seed"], "delivered": r["delivered"], "reasons": " | ".join(r["reasons"]),
                     "warnings": " | ".join(r["warnings"]), "N": r.get("N"), "Rp": r.get("Rp"), "mode": r.get("mode"), "tier": r.get("tier"),
+                    "tier_final": r.get("tier_final"), "N_final": r.get("N_final"),
                     "flags_true": ",".join(sorted(r.get("flags", {}))), "island_isa": r.get("island_isa"), "p_kept": r.get("p_kept"),
                     "hpm": ";".join(map(str, sorted(r["hpm"]))) if r.get("hpm") is not None else "", "F_hpm": r.get("F_hpm"),
                     "mpm": ";".join(map(str, sorted(r["mpm"]))) if r.get("mpm") is not None else "",
@@ -914,7 +930,10 @@
         return 0
     rows, C, summary, outcome = compare(recs, opts)
     verdict = {"schema": "overlap1e4.verdict/1", "script_sha256": script_sha, "prereg": PREREG, "records": a.records, "outcome": outcome["outcome"],
-               "reasons": outcome["reasons"], "incomplete": outcome["incomplete"], "criteria": C, "summary": summary}
+               "reasons": outcome["reasons"], "incomplete": outcome["incomplete"], "criteria": C, "summary": summary,
+               "fits_tier_N": {rid: {"arm": r["arm"], "tier_final": r.get("tier_final"), "N_final": r.get("N_final"),
+                                     "N_expected_at_tier": r.get("N_expected_at_tier"), "delivered": r["delivered"]}
+                               for rid, r in sorted(recs.items())}}
     write_csv(os.path.join(a.out, "per_dataset.csv"), rows)
     write_csv(os.path.join(a.out, "per_fit.csv"), per_fit_rows(recs))
     with open(os.path.join(a.out, "verdict.json"), "w") as fh:
```

## Tests
- `tests/test_compare_overlap.py` (registered script): ALL TESTS PASSED (13 cases), unchanged.
- `tests/test_compare_overlap_v2.py` (v2): ALL TESTS PASSED (18 cases) = the 13 registered cases + `escalated_T` (both seeds of AR r01 at tier 1, N 40,000: CLEAN, 40/40 delivered, tier/N reported in the three outputs; the registered script on the same fixture gives INCOMPLETE 38/40), `escalated_T_cost` (cost rule unchanged, MARGINAL), `T_N_not_tier`, `T_N_wrong_tier` and `V_N_escalated` (all INCOMPLETE: nothing else relaxed).

## W0 read-back re-run with v2 (`W0_readback/v2_run/`)
`--wave-check` on the W0 records (T2 + V2 views) with `--cross-file W0_readback/cross_vt.json`: all 4 fits delivered (AR-T tier_final 1, N_final 40,000; ADJ-OPP-T tier 0, N 10,000; both V tier 0, N 2,500). Every value is identical to the supplementary copy (`wave_check_SUPP_N40000.csv`, `per_fit_SUPP_N40000.csv`) except the new tier/N columns: ADJ-OPP dlogZ(V-T) = -0.0007 (0.06 s.e.), AR -0.0152 (2.41 s.e.), d_H(V,T)/d_H(T,f*) as in W0_READBACK.md §4. The supplementary copy accepted N in {10^4, 40,000} for any T fit; v2 accepts exactly the tier-consistent N.

## Approval
HQ decision: APPROVED, 2026-11-18 evening, HQ (H-21 (2), HQ_DECISIONS 8b48bb07); conditions (i) commit + sha256 before any W1 read-back, (ii) side-by-side registered vs v2 output in every read-back, (iii) registered sha 311bbad8… reproducible. Manager verification 2026-11-19 ~02:35Z: sha256 of compare_overlap.py / compare_overlap_v2.py / tests/test_compare_overlap_v2.py recomputed = the table above; test_compare_overlap.py 13/13 and test_compare_overlap_v2.py 18/18 PASS. (compare_overlap_v2.py's docstring still says "pending HQ approval"; left unedited so its sha stays the tested 4f402e51….)
