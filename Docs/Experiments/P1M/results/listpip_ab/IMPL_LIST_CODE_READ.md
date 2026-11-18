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

## INV-SCORE-BITS: one model, one score (named invariant; manager-verified 2026-11-18; trace: SCORE_PATH_TRACE.md)
**Statement (core v3.1, main e9bac478 / v3.1.1):** every score offered to the top and leader stores for a model S is the binary64 value `D.logprior[|S|] + Scorer::score(S).logm`. It is computed by one deterministic function of the sorted model S on the immutable target D, within one process and one build. Hence a model never reaches a store with two different values. The store's dedup on (value, S) (`cpp/v3_ledger.h`, `TopStore::offer`, `s.count(e)`) is then exact dedup by model, and the list-PIP duplicate `stop()` (`v3_run.R:253`) is unreachable.
**Why (code lines at main):**
- single scorer `Scorer::score` (`cpp/v3_score.h:227`): routes Cholesky → refactor → QR, a pure function of S, no rank-1 or incremental updates, fixed summation order;
- tables: `build_tables` scores each block subset U with the same scorer (`cpp/v3_start.h:93`); blocks hold sorted internal indices (`v3_start.h:37`), so U is sorted; the event uses `logprior + logm_tab` (`cpp/v3_core.cpp:382`);
- particles, proposals, Gibbs flips, local scans, LS0: `Engine::eval` → cache or `sc.score(q.S)`, with S kept sorted (`cpp/v3_engine.h:89-101`);
- inherited models are RE-SCORED by the same scorer, not copied (`cpp/v3_core.cpp:426-427`);
- the cache stores the bits of the first fresh evaluation (`v3_score.h:255-294`; clear-when-full only causes a re-score by the same function);
- the build has no FMA contraction (`cpp/Makevars.v3`: `-ffp-contract=off`).
**Residual assumptions:** the same binary and libm within a run (true by construction: setup, calibration and final run share one process and `setup$ptr`), and the build through `Makevars.v3`.
**Test:** `Scripts/SMC_BVS/tests/list_pip_units.R` "INV-SCORE-BITS" (PR #80). Every top-store and leader-store model of an SMC fit with inherited models and LS0 is recomputed through `cpp_score` and must be `identical()`; every block-table entry must be `identical()` to a fresh score; no duplicate keys.
**Engine v4 (the 1M engine):** the invariant does NOT hold in V mode (the class-A `flip8_A` kernel is path-dependent, ≤ 1e-9 relative to bit form, `kernel.h:11-13,249-262`). But every v4 store dedups by (hash, model) and keeps the maximum value (`island/store.h:235-249,302-309`; `store.cpp:127-153`; `load_unique_sorted` `store.cpp:233-267`). So the merged top store cannot hold one model twice, and `require_distinct` (`list_pip.cpp:20-35`) fires only on a code bug. The list's F for a multi-path model is the max class-A value: deterministic, order-independent. No v4 change is needed.
