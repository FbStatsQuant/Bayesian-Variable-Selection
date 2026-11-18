# IMPL-LIST code-read: core v3.1 list fields against SPEC_LIST_PIP (Engineering manager, 2026-11-18)

Code of record: `main` at e9bac478 (tag `method-v3.1-listpip`, annotated), `Scripts/SMC_BVS/core/` tree 8ff2d876 (= exp/P1M-engine after #68, 03921ae0).
Spec: Docs/Experiments/P1M/briefs/SPEC_LIST_PIP.md (a copy of theory/W3-AUDIT 523dda23).

| spec | code (main e9bac478) | verdict |
|---|---|---|
| §1 list = returned `top_store` | completed path: `v3_fit.R:176` passes `fit$top_store`, `ctx$orig`, `names(pip_primary)` | OK |
| §2 pip_list, strict mpm_list in original indices, log_Z_list | `v3_run.R:245-271`: num/den over u = exp(F − Fmax); `orig[pip > 0.5]`; `Fmax + log(den)` | OK |
| §3 numerics: max subtracted, sums last→first in plain double, no clamp | explicit `for (i in m:1L)` loop (avoids R's long-double `sum`); no clamp | OK |
| §4 completed | as above | OK |
| §4 exact | `v3_fit.R:131` → `v3_exact_list_last` (`v3_run.R:274`): pip_list = pip_primary, mpm_list = mpm, log_Z_list from the enumeration's store, source "exact" | OK |
| §4 other statuses: fields absent | admission refusal, invalid input, no_predictors, y_constant, setup/calibration failure return before the list code: absent, OK. **A final-run stop** (`raw$status != "completed"`, `v3_run.R:143`, e.g. a wall-clock guard stop) returns from `v3_assemble_final` without `top_store`; then `v3_fit.R:176` still calls `v3_list_fields(NULL, …)` → m = 0 → the fields are set to NA with `pip_list_flag = "empty_list"` (`v3_run.R:249`) instead of being absent | **DEVIATION (minor)** |
| §4 duplicates stop; NaN/+Inf → NA + flag; −Inf weight 0; empty list → flag | `v3_run.R:249-256` (duplicates checked before the non-finite flags) | OK |
| §5 names | pip_list (named as pip_primary), mpm_list, log_Z_list, list_size, list_full, pip_list_source, pip_list_flag | OK |
| §7 A: nothing existing moves | A/B: 39/39 units identical on 991787ef (34 PROD-H production + 5 status paths; fingerprint, field order, attributes, new fields last), and 15/15 fast units on the final tree 8ff2d876 (the C++ key is equal; 991787ef → 8ff2d876 is an R relocation only). Tables: results/listpip_ab/ and the #69/#68 PR comments | OK |
| §7 B: by-hand cases, v3 vs v4 | v3 list tests 124/124; WP4 golden incl. B10 permutation and B12 v3-vs-v4 (568,269 checks, 0 failures) | OK (Engineering tests, not re-run in this read) |

**Deviation.** It affects only fits whose FINAL run did not complete (wall-clock stop, numerical failure in the final run): they carry 7 extra fields (NA, flag "empty_list") where the spec says absent. Completed and exact fits, and every legacy field, are unaffected: the A/B shows this on tie_dp_p400's earlier load stop (resource_limit at 7,305 s, `pip_list_flag` present). The fix is one guard, `if (identical(fit$status, "completed"))`, at `v3_fit.R:176`. It is a core change after the tag, so it needs HQ's decision: fix + re-tag, or accept + document.
