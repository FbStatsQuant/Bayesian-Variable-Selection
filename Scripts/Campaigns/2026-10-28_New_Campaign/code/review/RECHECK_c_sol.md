# Independent LOWP re-check (c)

**Final verdict: ACCEPT WITH FIXES.** Four original findings are FIXED; finding 1 is PARTIAL because the requested rules are now present and select correctly, but follow-on condition/diagnostic defects remain in the new derived-rule stage. No new blocking selection defect was demonstrated. Resolve N1–N3 below before freezing the runner.

Reviewer: Sol 6.1, independently performed; no subagents. Review date 2026-10-28 America/Chicago; execution records use 2026-10-29 UTC. Local Windows R 4.4.1, with `<PC_TEMP_PATH>` prepended. Local execution was explicitly requested; no SSH. Reviewed files were not edited. Evidence root (`E`): `<PC_TEMP_PATH>`.

Scope: the named prior review/evidence, `bench_lowp/`, DECISIONS D3, the specified master sections, PREREG_c050, production originals under methods_dev, and LOWP INTERFACES. The supplied manager ruling settles LA-4's registry/roles for this re-check. I did not inspect unrelated campaign files or Git metadata, and do not independently certify the separate D3 commitment for LA-1–LA-3.

## Original findings

References are relative to `CAMP/code/bench_lowp/` unless qualified.

| Original finding | Re-check | Evidence and result |
|---|---|---|
| 1. Missing preregistered derived-rule registry | **PARTIAL** | `R/common.R:26–81` now emits every requested K37 companion, F4 `ebic1_lam005`, and F5 `sic_smax`, with the manager's roles and scale labels. Real F4/F5 results at both scales match independently reconstructed criteria/supports. Exact alias tests cover all five F methods at p=20 and p=30; ordinary errors, fit gates, and selected-point failures preserve missing selection and support audit correctly. The new stage still has N1/N2 below; applied LA-4 provenance is also missing (N3). `E/checks.csv`, `edge_probes.rds`, `derived_selected_failure.csv`, `adaptation_provenance.csv`. |
| 2. Production input/library bypass and unchecked resume environment | **FIXED** | `run_bench_case.R:53–57,95–130` rejects production `--no-manifest`, absent `--library`, ambient version override without `--test-library`, and a dependency outside the sealed library. Actual probe exits are all 1, with the expected refusal reasons. The original wrong-version assertion probe now rejects glmnet `0.0` despite the ambient override. Dependency paths/build metadata/runtime-file hashes and an environment identity are saved and checked before resume. A changed-library resume exits 1 with `Resume identity mismatch: environment_sha256`; unchanged resume exits 0. The explicit `--test-library` exception is marked in saved test rows/RDS; it is not a sealed production claim. `E/launches.csv`, matching stdout/stderr logs, `version_bypass.txt`. |
| 3. A3 rule-local warning/message provenance overwritten | **FIXED** | `run_bench_case.R:150–164` preserves native row fields and ignores A3's mixed legacy aggregate. Rerunning the original controlled wrapper probe gives `ci95=ok`, count 0, missing warnings/messages; `km2=warning`, count 2, warning text only in `warnings` and message text only in `messages`. Outer conditions are still captured in the forced-error run. `E/rule_condition_rows.csv`, `condition_code/`, `a3_rule_conditions.*.log`. N1 is a separate defect in the newly added F4 derivation, not a recurrence of this A3 flattening. |
| 4. Rounded F3 ridge grid differs from production | **FIXED** | `R/config_lowp.R:53` restores `10^seq(3,-6,length.out=61)`. All 61 entries are identical to production. The original paired F3 probe now gives bit-identical rule frames and ridge CV means. All 70 retained configuration bindings across eight methods compare exactly, with no exceptions. `E/config_comparison.csv`, `f3_rounding_probe.rds`, `checks.csv`. |
| 5. Missing unscored schema placeholders | **FIXED** | `run_bench_case.R:166` adds all 34 requested fields as NA. Both CSV and RDS carry the full master schema in successful and failed outputs; no truth was loaded or scored. The 32 real smoke rows and all 38 forced-failure rows pass the placeholder checks. `E/checks.csv`, `finalize.R`, saved output CSV/RDS. |

## LA-4 fidelity

- **Identifiers and roles:** F1–F3 keep `cv_min` primary, `cv_1se` S0, `ebic1_K37`/`ebic05_K37` S0, and both old cap rows secondary. F4/F5 have `ebic1_K37` primary, `ebic05_K37`/`bic_K37` S0, and all three old cap rows secondary. F4 `ebic1_lam005` and F5 `sic_smax` are S0. No S1 fit is added.
- **K and aliases:** `min(floor(n/log(n)),p)` is exactly `min(37,p)` at enforced n=200. Thus K=p for p=20/30. K37 rows copy every cap-row data field exactly, changing only `rule_id`, `role`, and `rule_label`. This is verified on the real p=20 fits and on all five methods' controlled p=20/30 frames at both scales; it also follows directly from the copy operation. No p=30 numerical smoke is claimed.
- **F4 lambda restriction:** candidate supports come from path points with lambda at least `0.05*max(path$lambda)`, plus the eligible null support. Selection minimises the saved OLS EBIC(1) with criterion/size/key radix ties. Independent OLS refits and criterion reconstruction agree at both scales. The diagnostic ceiling issue in N2 does not change the selected support.
- **F5 SIC:** `200*log(RSS/200) + k*log(p)*log(log(200))`, over valid sizes `0..min(p,floor(200/(log(p)*log(log(200)))))`. Nominal ceilings are 40 and 35; feasible ceilings are 20 and 30. Real p=20 paths contain every size 0..20; independently recomputed RSS/SIC and winners agree at both scales. This remains a distinct criterion from EBIC/BIC even though the feasible size ceilings coincide.
- **Labels:** derived c050 rows are `pre-registered`; c100 `ebic1_K37` has the full post-hoc headline label from PREREG, and other derived rows are `post hoc`. Original rows remain `pre-declared`. The additional `selected_k_gt_K37` is false for every successful LOWP selection. ADAPTATIONS explicitly preserves the original largest-candidate interpretation of `ebic_at_largest`; it must not be reported as evidence of an artificial cap.
- **Failure inheritance:** all 38 rows from the eight-method forced error are failed with missing support/k/audit and captured error/outer conditions. Controlled F4/F5 fit-gate failures preserve derived chosen support in `support_audit`; F4 selected-point failure does likewise. An unrelated old EBIC-rule failure does not incorrectly fail a successful new derived rule. The remaining warning-status issue is N1.

## New findings

**N1 — should-fix: a successful derived F4 rule can be labelled `ok` despite captured conditions.**

Location: `R/common.R:65`. The new row infers warning status from `any(orig$status=='warning')`. Failure takes precedence on original rows, so all three old EBIC rows can be `failed` even when they contain captured warnings. If the restricted rule selects a different, passing support, it becomes `ok` while retaining `n_warnings=1` and `warnings='package warning'`. This violates master §III.3.0 status semantics.

Reproducer: `E/edge_probes.R` constructs a valid saved-candidate/path fixture where all old rules select support `1;2`, whose path point fails, while the lambda-restricted rule selects passing support `1`. `E/derived_condition_probe.csv` records the new row as `ok` with a retained warning. This is a controlled boundary probe, not an observed condition in the real smoke. **Fix:** determine the successful derived row's condition status from captured warning/message provenance, independently of original rows' failure status. Keep failure precedence and the rule-specific error clearing already implemented.

**N2 — minor: F4 restricted-rule largest-candidate metadata uses the unrestricted candidate set.**

Location: `R/common.R:68–72`. `k_valid_max` is inherited from the old unrestricted EBIC row, and `ebic_at_largest` compares with all valid candidates instead of the rule's eligible subset. In the three-point fixture, the restricted set contains sizes 0 and 1 and selects size 1, but the emitted row says `k_valid_max=2` and omits `ebic_at_largest`. The master defines this diagnostic relative to a rule's valid candidates. **Fix:** compute its valid ceiling and boundary code from `eligible`, while preserving `k_path_max` as the full-path observation. Evidence: `E/restricted_candidate_probe.csv`, `edge_probes.rds`. Selection and criterion are correct.

**N3 — minor: rows applying LA-4 do not record LA-4 in `adaptation_ids`.**

Location: `run_bench_case.R:167,172`; LOWP INTERFACES I4. The emitted F4 derived rows contain only `LA-1`; F5 derived rows contain only `LA-1;LA-2`. LA-4 is absent despite being an applied, documented adaptation; F1–F3 use the same omission. **Fix:** include LA-4 for affected F-method outputs, including failure rows, consistent with the chosen per-fit provenance convention. Evidence: `E/adaptation_provenance.csv` from the actual smoke.

## Execution and source evidence

Reduced smoke: `dev_p0020_S1_r001`, n=200, F4/F5/A3, c100 and c050, method seed **6,220,001**, using the prior review's input fixture copied into E and checked against its manifest. No truth file is needed. Both invocations exit 0; **6/6 fits and 32/32 rows are ok**, with zero diagnostic flags. A3 retains burn-in 10,000, 15,000 saved draws, thin 5, one core, and the Rue branch. Local wrapper times were F4 0.10/0.14 s, F5 1.61/2.72 s, A3 26.47/42.92 s; these are smoke observations, not campaign performance estimates. The ordinary unchanged resume exits 0 and reports all three methods skipped.

The standard validation set passes **164/164** checks. Separate edge probes deliberately expose N1–N3 and are not included as passing acceptance checks. `finalize.R` validates A3 native conditions, the complete CSV/RDS schema, selected-point failure audit, source preservation, source/config equality, and recorded child exit codes; its exit is 0 and its saved log ends `FINAL EVIDENCE VALIDATION PASS`.

The source-hash/full-byte diff audit passes **19/19** declared copies against the first named production original: declared SHA-256 = copied SHA-256 = original SHA-256, with zero byte differences. No backup/sensitivity originals were required. All **70/70** retained production configuration bindings are exactly identical before documented runtime adaptations. The reviewed source closure stayed unchanged throughout. Real-smoke source identity:

`8d37745ea024f8c0d726620f2e5bdd0a547e57a4063fc018351dc917f68224ab`

Auditable records: `E/launches.csv` contains commands, UTC intervals, PIDs and exits for setup, both real scales, resume, the eight-method forced failure, guard probes, paired F3/config/schema validation, A3 condition probe, and changed-environment resume. Real-fit process IDs are **48736** (c100) and **31124** (c050); forced-failure PID **45172**, exit 2. All infrastructure refusals exit 1 with inspected reasons. `edge_launch.csv` and `finalize_launch.csv` record the final small checker processes. Source/config snapshots, package/build/file provenance, RNG/seed details, sessions, stdout/stderr, raw outputs, and SHA-256 evidence are saved under E. `evidence_sha256.csv` indexes the final saved evidence; `report_sha256.csv` binds this report.

Launcher setup initially encountered PowerShell's script policy and an exit-code handle issue; those occurred before fitting. The final launcher opens the process handle before waiting, records explicit child exits, and successfully completes. No larger supplied smoke or remote workload was run. These results do not certify remote deployment, sealed-library provisioning, active BLAS thread counts, scoring, or production-scale performance.

**Compact summary:** requested LA-4 selection rules/roles/labels and failure audit are implemented; original findings 2–5 are fixed. The independent smoke, forced failures, source/config fidelity and 164 standard checks pass. Retain **ACCEPT WITH FIXES** for one derived warning-status defect and two diagnostic/provenance corrections (N1–N3).
