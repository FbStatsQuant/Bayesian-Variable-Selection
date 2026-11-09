# R02 — fresh plan re-check of PLAN v1.1 + lemmas/TDP_E.md (Codex gpt-6.1-sol, reasoningEffort high), verbatim reply

Reviewer: fresh delegate_task (Codex, gpt-6.1-sol, high), read-only, briefed on the committed PLAN v1.1 (commit 5c14c4e),
TDP_E.md, R01 raw reply and disposition; asked to verify each R01 finding is resolved and to find new problems.
Received 2026-11-08 ~22:17 CST. (The reviewer reviewed plan TEXT at 5c14c4e; the adapter change it asks for was already in
the code commit 9b9d234 — see R02_disposition.md.)

---

Reviewed committed `HEAD` documents and the original core at `f16ce15`; ignored the modified working-tree header. No files were edited.

Aliases: `PLAN` = `Theory_work/Wave1C/C-ENG/PLAN.md`; `LEMMA` = its `lemmas/TDP_E.md`; `SPEC` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`; `ADAPTER` = `Scripts/SMC_BVS/study/adapter.R`.

1. **MAJOR — Default-on NA fields break the existing study adapter and erase native stop classifications.**

   **Evidence:** `PLAN:87–91` adds exact-name NA `mpm` and `pip_primary` fields to every unavailable public fit. But `ADAPTER:192` unconditionally calls `smcbvs_check_support(fit$mpm, ...)`, whose validation rejects `anyNA(x)` (`ADAPTER:179`). Independently, `ADAPTER:196` treats any non-NULL `pip_primary` as supplied estimates and demands finite, named probabilities (`ADAPTER:203–206`).

   I exercised the committed adapter functions in R without loading or modifying the core:

   ```text
   old_absent: accepted
   NA_mpm: invalid original-index MPM
   NA_pip: primary PIPs must be finite, named by every retained original index
   NA_both: invalid original-index MPM
   ```

   Consequently, valid `resource_limit`, `schedule_limit`, numerical-failure and degenerate returns become `adapter_error` through `ADAPTER:387`. The audit retry retains the NA fields and encounters the same rejection (`ADAPTER:392–396`). Switch-off compatibility does not protect normal study calls: the adapter calls `v3_fit` without an LS0 argument, so the new default applies.

   **Concrete fix:** Include adapter compatibility in this plan. Define the unavailable-field representation and make the adapter recognize it before support/PIP validation. Preserve native status, unavailable PIPs and valid incomplete HPM audit information. Continue validating genuinely supplied audit estimates. Test old absent fields, new NA fields, legitimate empty supports and malformed supplied values.

2. **MAJOR — The required post-NA-fix forced-stop validation gate is omitted.**

   **Evidence:** `SPEC:400` explicitly requires “API-AUDIT’s forced-stop table (10 fits) after the `log_Z` NA fix.” `PLAN:185–190` instead specifies LS0 guard/numerical-failure injections in direct `cpp_final_run` fixtures. Those exercise neither every public-return path covered by the helper nor the existing consumer contract.

   This matters because `PLAN:88–89` promises NA fields on **every** unavailable public return, while the original `core/v3_fit.R` has separate early exits for invalid seed, preprocessing, preflight, exact enumeration, setup and calibration, besides final-run failure. Correct LS0 assembly alone cannot establish that promise.

   **Concrete fix:** Add the specified ten-fit API-AUDIT replay as an explicit gate, or record it as unmet. Exercise public `v3_fit` returns and adapter consumption; assert all eight exact-name fields, `$log_Z`, native status and archive separation. Include failures before final-run assembly. Retain the deterministic LS0 injections as additional tests.

3. **MINOR — The guard-stop test still contradicts the repaired output contract.**

   **Evidence:** `PLAN:172` expects “no log_Z/pip fields,” whereas `PLAN:87–91` requires those fields to exist with NA values. An implementation following the older assertion would fail the newly accepted #15 contract.

   **Concrete fix:** Replace absence assertions with exact-name presence and NA-value assertions for the complete helper field list. Assert that no finite final estimate leaks through `$` access. Keep absence assertions only in explicit switch-off compatibility tests.

4. **MINOR — The lemma overclaims byte identity after adding fallback metadata.**

   **Evidence:** `LEMMA:57–58` claims the result “is byte-identical” to the old result when untruncated, “and also when N = cap exactly.” However, `PLAN:126` adds `ModeResult$tie_dp_used`, and at `N == cap` the fallback executes, changing that metadata even though the selected model is unchanged.

   The mathematical reachability and greedy proof is sound **for E under the stated hypotheses**. This finding concerns the stated compatibility consequence, not the lex-min(E) proof.

   **Concrete fix:** State equality of the legacy result fields—`S`, `lg0`, `ties`, `truncated`—in those cases. Document `tie_dp_used` separately. Avoid byte-identity claims across the changed result structure.

The substantive R01 remedies are present in v1.1; this table assesses the plan text, not completed implementation or validation.

| R01 finding | Status | Evidence / qualification |
|---|---|---|
| #1 Exact-name unavailable estimates | RESOLVED | `PLAN:86–91` adds the shared helper across public unavailable returns. New consumer and validation issues are findings 1–3 above. |
| #2 Incorrect real-table oracle | RESOLVED | `PLAN:117–123,161–166` separates lex-min(E) from the exact-arithmetic S* contract and bounds the floating-point claim. |
| #3 Missing prototype replay | RESOLVED | `PLAN:179–184` adds prototype comparison, metadata normalization and an explicit unmet-gate outcome. Execution remains pending. |
| #4 Public `local_limit` | RESOLVED | R9 specifies final-cap OR LS0-cap, with attribution fields and the separate L1 rule. |
| #5 Weak integration fixtures | RESOLVED | `PLAN:185–190` adds an unscored winning centre, exact event count, strict-improvement cap fixture, tie/eviction cases and failure injection. |
| #6 Proof hypotheses/invariants | RESOLVED | `LEMMA:28–53` supplies encoding and execution hypotheses plus the feasibility/greedy argument; `PLAN:199–200` specifies root-feasibility failure. |
| #7 Switch-off compatibility | RESOLVED | `PLAN:174–176,195–200` specifies the old assembly branch and narrows regression equality to deterministic completed-run outputs. |

**Verdict: REJECT as written.** The LS0 integration design and bounded TDP-E proof are defensible, but the default-on interface change demonstrably breaks the production study adapter, and the required unavailable-output validation gate must be added.
