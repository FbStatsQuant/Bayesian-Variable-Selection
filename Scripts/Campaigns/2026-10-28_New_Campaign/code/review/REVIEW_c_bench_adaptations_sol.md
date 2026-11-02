# Independent review (c): LOWP benchmark adapters

**Verdict: ACCEPT WITH FIXES. Production release is held pending the blocking finding below.**

Reviewer: Sol 6.1, independently performed, no subagents. Reviewed 2026-10-28 America/Chicago (saved smoke timestamps 2026-10-29 UTC). Only the named review inputs and the explicitly requested installed-package functions were inspected. No SSH, no edits to reviewed files. All probes and source snapshots are under `<PC_TEMP_PATH>` (abbreviated `SCRATCH` below).

File references below are relative to `CAMP/code/bench_lowp/` unless qualified. This verdict accepts LA-1–LA-3 technically; it does not supply HQ's committed D3 decision. `ADAPTATIONS.md:3` expressly calls them proposals. No Git metadata was read, so commit status was not independently verified.

## Numbered findings

1. **blocking — The emitted rule registry does not implement the supplied preregistration.**

   **Location:** `ADAPTATIONS.md:12,16`; `R/config_lowp.R:19,40,81,126,145`; `run_bench_case.R:108,120`.

   **Evidence:** `PREREG_c050.md:7–14,18` makes `ebic1_K37` primary for F4/F5, retains the original cap-100 rules as secondary, and requires the K37 companion rows for F1–F3. The adapter emits only the earlier identifiers/roles and explicitly acknowledges that no K37 or `sic_smax` rows are emitted. It also omits the preregistered F4 S0 `ebic1_lam005` row. The source tree under review has no derived-rule stage. At n=200, K37=37 exceeds both p values: the K37 and original-cap EBIC supports and scores therefore coincide on the same fit, but their registered identities and roles still need a defined mapping. Numerical equivalence is not a reason to silently retain an obsolete primary label.

   F5 SIC is not rendered meaningless by its size ceiling exceeding p. Its nominal ceilings are 40 (p=20) and 35 (p=30); feasible ceilings are p. Its criterion `n*log(RSS/n) + k*log(p)*log(log(n))` remains different from EBIC/BIC, so omitting it is a missing S0 rule, not an infeasibility adaptation. The F4 lambda-restricted derived rule also remains computable from the saved path. D3 authorizes omitting separate S1 fits from this eight-primary-method task; that does not itself settle these free derived rules.

   **Fix:** Implement the preregistered derived-rule stage for both scales, with explicit `min(K,p)` feasibility, registered identifiers/roles, preserved original rows, and inherited failure/audit behavior. K37 aliases can reuse exactly the same computed values. Emit SIC on sizes `0..min(p,smax)` and the F4 lambda-restricted row. Alternatively obtain a specific committed HQ ruling that the LOWP panel deliberately uses only the earlier master rows, including explicit treatment of each omitted S0 rule. Do not characterize the current omission as approved or infeasible.

2. **should-fix — Production execution can bypass the sealed-input and pinned-library contract.**

   **Location:** `run_bench_case.R:13,74,95–105,134,140–144`; `R/common.R:8–14`; master §III.3.0, lines 994–995.

   **Evidence:** `--no-manifest` is accepted for production IDs; “tests only” in README is not enforced. My scratch production-layout fixture with no manifest reached the forced wrapper and saved failed rows (exit 2), rather than refusing the input (expected infrastructure exit 1). `LOWP_SMOKE_ALLOW_VERSION_MISMATCH=1` also operates without any development-mode check: calling the loaded assertion with glmnet version `0.0` was accepted with a warning. There is no sealed-library argument/path assertion. The normal local library can supply a package of the same declared version. Resume checks source/input/seed identity but skips before package assertions, and does not bind completion to a package-library/environment fingerprint.

   **Fix:** Reject both bypasses for production IDs. Make the production library an explicit required input and verify loaded namespaces against the sealed library; preserve the separately authorized local development-smoke path. Store library paths/build provenance and an environment identity, and validate it before a completed unit is skipped. Evidence: `SCRATCH/targeted_launches.csv`, `unmanifested_production.log`, `version_bypass.txt`, `installed_source.txt`.

3. **should-fix — The runner changes A3's per-rule condition behavior and loses warning/message classification.**

   **Location:** `run_bench_case.R:122–129`; compare `R/methods/fit_A3_horseshoe.R:213–250`, `R/production_helpers/common_A3.R:73–96`, and production `DEV/A3_Horseshoe/code/run_case.R:198–211`.

   **Evidence:** The production A3 helper creates rule-specific `status`, `n_warnings`, `warnings`, and `messages`: a kmeans-only condition belongs to `km2`. Its fit-level `warnings` aggregate also contains message strings. The LOWP runner treats that aggregate as warnings for the entire fit, changes every `ok` rule to `warning`, and unconditionally replaces all four per-rule fields. A controlled scratch wrapper returning a valid saved A3 fit with a km2-only warning/message yielded **both** rows `warning`, both with `n_warnings=2`, both with the message text in `warnings`, and empty `messages`. The native frame had `ci95=ok` with zero conditions. This is an undocumented behavioral change from the production runner; it does not change supports but corrupts condition provenance/status.

   **Fix:** Preserve existing per-rule condition fields. Append truly outer captured conditions separately and apply only those outer conditions method-wide. Do not infer warning versus message type from A3's legacy aggregate; use its native row fields. Add this targeted regression check. Evidence: `SCRATCH/rule_condition_rows.csv`, `targeted.R`, and `targeted_outputs/results/rule_condition/`.

4. **minor — Freezing F3 by rounded decimal expansion changes the production ridge grid.**

   **Location:** `R/config_lowp.R:53–72`; production `DEV/F3_AdaptiveLasso/config.R` (`F3$kappa`).

   **Evidence:** The original computes `10^seq(3,-6,length.out=61)`. The copied configuration spells rounded decimal constants. Exact comparison changes **52/61 entries**, maximum absolute difference `4.547474e-13`, mean relative difference about `9.14e-16`. On the one dev fixture, supports were identical, but complete rule frames were not bit-identical and ridge CV means differed by up to `6.217249e-15`. This is small, with no demonstrated selection consequence, but it is neither infrastructure nor LA-1–LA-3 and contradicts exact unchanged-setting fidelity.

   **Fix:** Restore the production expression, or serialize numeric constants with full round-trip precision. Add an exact configuration comparison. Evidence: `SCRATCH/config_diff.txt`, `f3_rounding_probe.rds`, `final_checks.log`.

5. **should-fix — The output omits the master schema's unscored placeholder columns.**

   **Location:** `run_bench_case.R:131–144`; master §IV.1.2, lines 2338–2339; compare production `DEV/F1_Lasso/run_case.R:214–215` and `DEV/A3_Horseshoe/code/run_case.R:36–44`.

   **Evidence:** The saved CSV/RDS rule rows contain the fitting frame and provenance but omit `tp`, `fp`, `fn`, `exact`, `error_type`, `sel_a01..sel_a14`, `pip_a01..pip_a14`, and `max_pip_null` (34 fields). Production runners emit them as NA for later scoring. Fitting must not populate them from truth, but omitting them is an output-schema change not documented in I4 or ADAPTATIONS. The reduced smoke's narrow required-column check does not detect this discrepancy.

   **Fix:** Emit these columns as NA, or establish a versioned LOWP schema/contract explicitly permitting their creation by scoring. Validate the full agreed schema, including failure rows, rather than only the small fitting-column subset.

## Fidelity and adaptation conclusions

`SCRATCH/hash_audit.csv` checks **all 19** entries in `R/SOURCES_SHA256.txt`: each declared digest equals both the copied file and its first named production original. This covers eight wrappers, three method-specific glmnet helpers, and eight production common helpers. There are no copied-file diffs. Extra backup/sensitivity paths listed after `|` were not needed or read; the production originals alone establish identity. `R/common.R` and the runner are new integration code rather than copies of a single compatible upstream runner.

Every retained configuration binding was compared against its corresponding production `config.R`, with tolerance zero. All compared values match except the F3 decimal rounding in finding 4. Omitted config-construction functions (`make_settings`/`study_settings`) are replaced by the assembled settings lists; their omission is infrastructure. Method-registry filtering removes S1 fits as documented. All three runtime cap changes are at `R/common.R:19–21`.

The new runner also changes infrastructure: the CLI and input layout, per-method settings isolation, the RDS envelope (`record$fit`), output compression, locks/partial-file refusal, provenance hashing, and package-loading/timing boundaries. In particular, it does not preload method namespaces before starting the fit timer, whereas the F1 production runner does (`DEV/F1_Lasso/run_case.R:167–168`). Thus cold namespace-load cost can enter LOWP `runtime_s`, and method order can affect that cost. This does not tune a selection rule, but it should be documented or aligned before comparing runtimes with historical production measurements. The undocumented selection/diagnostic differences found are specifically findings 1, 3 and 4; production guard/schema differences are findings 2 and 5.

| Adaptation | Review conclusion |
|---|---|
| LA-1, EBIC cap `min(100,p)` | Correct feasible-set restatement. The original inequality k<=100 already admits every possible support at these p values, so this is a mathematical no-op rather than a necessary tuning change. It removes no feasible support. |
| LA-2, ABESS `0..min(100,p)` | Required and minimal. Sizes above p cannot exist; the production wrapper itself rejects `max(S)>ncol(X)` at `fit_F5_abess.R:71–72`. Including size p is valid because p<n; all original consistency checks remain. |
| LA-3, SuSiE `L=min(50,p)` | Correct explicit expression of pinned implementation capacity, not a new selected tuning value. Installed `susieR:::init_setup` deparse lines 23–24 say `if (p < L) L = p`; `susie` calls this function. With `s_init=NULL`, `null_weight=0`, the relevant p is exactly the design's p. Requesting 50 is accepted by the API but internally reduced, so a new explicit argument is not required to prevent an error. |

Installed source evidence is saved in `SCRATCH/installed_source.txt` (susieR 0.14.2). My explicit-L20 versus requested-L50 probe gave bit-identical PIPs and rule frames, both with effective L=20 (`susie_capacity_probe.rds`). `L_saturated` uses `sum(V>1e-9)==nrow(alpha)` at `fit_A1_susie.R:132–133`, not the original requested 50. It correctly means **all available effects active**, with the PREREG R4 weak-effect/possible-overfitting interpretation; it is not proof that a selected support is truncated or that additional effects would improve it. Record requested/effective L and use that label in reporting. No replacement L=10, truth-sized capacity, BIC primary, OLS pilot, or exact-leaps F5 from the dropped §III.4.5 settings is justified by D3.

The other low-p checks do not require further tuning adaptations:

- F1–F3 supply their full 200-point lambda vectors (ratio 1e-4), so glmnet's n/p-dependent default `lambda.min.ratio` cannot change them. The full/fold path, convergence, finite-value, and KKT checks remain defined at p<n, including a fully active support. F4 retains its compensated MCP path and original checks.
- `k_path_max` remains the observed maximum, bounded by p. Under the original master definition, `ebic_at_largest` remains informational when k=p: the full feasible model has been reached, not an unsearched larger support. Do not use its frequency as evidence of an artificial size restriction. PREREG R1's additional k>K37 condition is impossible at these p values; any retained cap-hit/largest-candidate condition needs an explicit reporting definition when implementing finding 1.
- F3's ridge SVD and 61-point CV pilot are feasible at p<n, use the actual thin-SVD dimension, and need no OLS substitution. The original accepted fixed-weight CV policy remains unchanged; rounding is the separate finding above.
- A2 resolves `A=1`, `B=p` and keeps lambda1=1, 100 lambda0 points from 1 to n=200, the patched 15-parameter native call, and unknown-variance updates. Neither the Beta prior nor the ladder becomes infeasible at p=20/30. Retuning them would exceed D3.
- A3 keeps 10,000 burn-in, 15,000 saved draws, thin=5, one core, and the CI/ESS rules. The package's existing p/n rule chooses **Rue** at low p, rather than Bhattacharya. The wrapper already labels this and correctly skips the `mu.beta==rowMeans(draws)` check in Rue's Rao–Blackwellized-mean branch (`fit_A3_horseshoe.R:46–55,177`); summaries/selection still use the draws. No budget/prior change is required. Cross-scale RNG terminal-state reconciliation remains a scoring responsibility; this one-scale smoke does not certify it.
- Ten common folds still give 180 training and 20 test observations, so p<=30 introduces no fold feasibility problem. Supplied folds are reused, never reselected by method. The existing S0 rows are otherwise coherent and share their fit runtime; omitted preregistered rows are finding 1.

## Runner and independent smoke evidence

Normal-path review passed ID/dev-mode/replicate bounds, dimensions and Y-column identity, prescribed data/fold/method seeds, and manifest file/X/all-five-Y/fold hashes. The RNG kind and method seed are reset immediately before every method at `run_bench_case.R:109`; method seed is data+4,000,000. No wrapper or helper opens truth/holdout files or reads input truth fields; the runner opens only the selected input and input manifest. Its path-component refusal is additional protection. Truth-directory permissions and wave reconciliation remain deployment responsibilities.

Outputs use same-directory temporary files and rename, a per-method directory lock, RDS/CSV checksums, and a `.done` written last. Completed units verify both payload hashes and source/run/case/method/input/seed identity. Incomplete files are refused for manual repair. Ordinary uncaught errors become registered failed rows with missing support/k; the independent forced-error test covered **all eight methods and all 24 registered rule rows**, including captured outer warning/message/error text. No null-model substitution occurred. Allocation failures/process deaths still require the external timeout/not-run reconciliation described by master §III.3.0, so fitting output alone cannot certify the final /100 and /600 denominators.

The runner requires an explicit outroot. It does not enforce `/scratch/fb31/New_Campaign` on NOTS, and sets thread environment strings inside R rather than demonstrating the active BLAS thread count. The local reference/default matrix-product run showed all five recorded thread variables equal to 1; that is not NOTS OpenBLAS validation. The OPS launch bundle must export thread limits **before R starts**, verify the actual BLAS/thread setup and sealed library, select the charter's scratch root, and perform missing-unit reconciliation. Those deployment artifacts were outside this review's permitted paths; no remote certification is claimed.

I generated one dev fixture by literal transcription of the allowed S1 smoke generator, with `dev_p0020_S1_r001`, n=200, method seed 6,220,001, a matching manifest, and no truth file. R 4.4.1 prepended the requested `lowp_Rlib`; no version override was used for real fits. Two independent runner invocations fit F1, F5 and A3, followed by a resume invocation: **all three process exits were 0**. Across the two invocations all 18 rule rows were `ok`, no diagnostic flags fired, and all 24 smoke checks passed. Fits and rows were bit-identical after removing timing and the deliberately different run IDs. Resume left all four F1 artifact hashes unchanged. A3 used its full 85,000-iteration budget and saved 15,000-draw summaries, with sampler `rue`.

Auditable evidence in `SCRATCH`:

- `launches.csv`, `first.log`, `repeat.log`, `resume.log`, and `outputs/results/{first,repeat}/`: actual commands, UTC intervals, exit statuses, payloads, hashes and completion markers; fit times were about 2.1 s F1, 0.1 s F5, and 20.2 s A3 per invocation. These are local smoke observations, not campaign resource estimates.
- `smoke_checks.csv`, `smoke_environment.rds`, `installed_source.txt`: reproducibility, schema-subset checks, driver PID, sessions, loaded package versions and library paths. Some packages resolve from the normal local library after the supplied directory; this is local smoke evidence, not sealed-library certification.
- `targeted_launches.csv`, `failure_checks.csv`, `targeted_outputs/`: eight-method forced failures; dev/prod mismatch and input-hash tampering each refused with exit 1; condition and production-bypass probes.
- `config_diff.txt`, `hash_audit.csv`, `f3_rounding_probe.rds`, `susie_capacity_probe.rds`, `source_snapshot/`, review scripts and their hash manifests. `reviewed_sources_unchanged.txt` confirms the reviewed files were unchanged throughout. The final evidence checker exited 0 and printed `FINAL EVIDENCE VALIDATION PASS`.

Windows startup locale warnings appear outside method capture. The original PowerShell driver wrappers reported shell exit 1 when redirecting that native stderr, despite the recorded child runner exits above being 0 and all R assertions completing; the final checker used C locale and explicitly propagated R's exit 0. No fit failure is hidden by that launcher distinction. I did not rerun the larger supplied smoke or certify p=30/NOTS execution; p=30 was reviewed statically, including feasibility arithmetic.

**Compact summary:** 19/19 copied files match production hashes; LA-1–LA-3 are technically acceptable and minimal/no-op as described. The reduced smoke and every forced-failure probe pass. Resolve one blocking preregistration/row-mapping issue, three should-fix runner/schema issues, and one minor numeric-fidelity issue; then record the D3 ruling and complete NOTS deployment validation before production release.
