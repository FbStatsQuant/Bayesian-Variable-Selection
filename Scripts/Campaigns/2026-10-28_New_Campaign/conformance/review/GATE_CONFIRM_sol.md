# CONF NOTS minimal-fix confirmation — Sol 6.1

Reviewed 2026-10-28, approximately 23:39 America/Chicago. **Bundle verdict: ACCEPT WITH FIXES.** The three specifically named counterexamples are rejected, and the updated synthetic positive control reaches ACCEPT. The precompile mechanism and terminal-status fix are correct on static inspection. One required-output gap remains in fix 1: per-tier diagnostic stage reports may still be empty or have arbitrary types while the stage check passes.

This is a narrow submission review, not a production identity result. No SSH/network, compilation, fit, simulation, or remote execution was performed. Only the requested review file was written.

## Per-fix status

| Fix | Status | Finding |
|---|---|---|
| 1 — populated instrumentation, checked against fit fields | **PARTIAL; one blocking follow-up** | Both original named-NULL counterexamples now fail. Best-before/after checks match the R emitter; stages and cut-group types accept actual R-side output. However, `diag_grid_intervals` is checked only as an outer list of the expected length. NULL, empty, and wrongly typed per-tier reports pass. Pilot counts are also not compared with retained schedules. |
| 2 — visible precompile and retained audit evidence | **RESOLVED for code, static review** | Precompile's final-expression guard matches the named frozen entry point. Compiler output is redirected to a persistent log; key/SO hashes and precompile source hash are recorded. Fresh-cache refusal, sequential reuse, and EXIT failure recording are correctly arranged. JOB.md now requires sacct, compile log, bundle hashes, and acceptance stdout/stderr/status retention. Its transfer ordering has a small documentation correction described below. |
| 3 — unambiguous terminal job record | **RESOLVED for the requested counterexample and required records** | Conflicting and duplicate final statuses are rejected. One header/end, `failed_case none`, both launches, both success lines, a compiled key and an SO hash are required. The previous five-line evidence is rejected. |

## Executed controls

Used `C:/Program Files/R/R-4.4.1/bin/Rscript.exe --vanilla -`, with the harness supplied through a PowerShell literal here-string. R reported `R version 4.4.1 (2024-06-14 ucrt)`. Both deterministic harness processes exited 0. No random draws or seeds were needed. R emitted startup warnings because inherited C.UTF-8 locale settings are unavailable on this Windows runtime.

The first harness parsed the actual `compare_identity.R` and evaluated its expressions from `PIN` through its final acceptance/failure branch. File existence, RDS/CSV reads, checksums, and job evidence were in-memory fixtures; `quit()` was intercepted to capture the requested gate exit. Both case fixtures had 500 named plain PIPs, a 500-by-4 matrix, consistent MPMs, pinned provenance, matching environment/seeds/allocation, and the two expected escalation states. For instrumentation, the harness extracted and executed the actual nested `finish()` function from parsed `v3_fit.R`, supplying synthetic retained calibration/fit fields and a stub registry report. This exercised the real R-side instrumentation construction without invoking a fit or C++.

**Scope qualification:** `cmp2.R` was not a named readable file in this request. It was neither read nor sourced; `cmp2_run()` was replaced with a passing stub. Thus the positive result verifies the revised acceptance predicates and final ACCEPT branch under a passing comparator result, not a newly executed full comparator control. The earlier comparator review remains separate evidence. The C++ registry-report producer was also outside scope; the HLL report fixture used the three-field order required by this script.

The job fixture included the exact version/CPU evidence plus:

```text
job 123 host synthetic start 2026-10-28T00:00:00Z
compiled_key <64 lowercase hex>
so_sha256 <64 lowercase hex>  /synthetic/cache.so
run Rscript --vanilla /synthetic/run_case.R --case p0500_S3_r044_c100 --scale c100
case p0500_S3_r044_c100 exit 0
run Rscript --vanilla /synthetic/run_case.R --case p0500_S5_r059_c100 --scale c100
case p0500_S5_r059_c100 exit 0
failed_case none
end 2026-10-28T00:01:00Z
final_status 0
```

The actual fixture used 64 `a` characters for the key and 64 `b` characters for the SO digest, not literal angle-bracket placeholders. Mutations of fit instrumentation below were also copied to record instrumentation, so record/fit equality could not cause the rejection. Instrumentation mutations affected both cases.

| Control | Failed criteria | Requested gate exit | ACCEPT printed? |
|---|---:|---:|---|
| Updated positive, actual R `finish()` instrumentation, double tier_final | 0 | 0 | Yes |
| Named NULL `scored$after_calibration` | 2 | 1 | No |
| Named NULL `best_before_local` | 2 | 1 | No |
| Append conflicting `final_status 1` | 1 | 1 | No |
| Append duplicate `final_status 0` | 1 | 1 | No |
| Previous five-line job evidence | 3 | 1 | No |
| Remove S5 launch | 1 | 1 | No |
| Remove S5 success line | 1 | 1 | No |
| Remove compiled key | 1 | 1 | No |
| Remove SO hash | 1 | 1 | No |
| Positive with integer rather than double tier_final | 0 | 0 | Yes |

The supplied `DRYRUN_negative_controls.log` reports 30 failed criteria and `exit=1`, consistent with JOB.md. That log was inspected, not regenerated against historical files. It contains the historical-as-new negative run; it does not itself show a separate conflicting-final-status run. The latter was independently exercised above.

## Remaining blocking issue: stage reports can still be placeholders

At `compare_identity.R:76–78`, the stage predicate validates the outer `diag_grid_intervals` list and its number of tiers, but never validates its elements or compares them with `f$calibration$tiers`. The actual emitter at `v3_fit.R:65–69` constructs an integer vector per tier from the retained diagnostic iteration grids.

A second read-only R harness extracted and evaluated this exact `chk()` expression, with S5's `p$escalated = TRUE`, `final = 2L`, `pilot = c(2L, 2L)`, and `tier_final = 1`. Observed results:

```text
baseline list(2L, 2L):                         ACCEPTED
diag_grid_intervals = list(NULL, NULL):        ACCEPTED
diag_grid_intervals = list(integer(), integer()): ACCEPTED
diag_grid_intervals = list("not an interval report", NA_real_): ACCEPTED
pilot = c(999L, 999L), retained schedules unchanged: ACCEPTED
```

These are stage-predicate tests, not additional full-branch/comparator executions. The other new-field predicates do not inspect those stage elements; keeping the record instrumentation equal to the fit instrumentation also bypasses the equality check. The defect therefore leaves the original requirement to check populated stage reporting incomplete.

**Minimal required follow-up:** derive the expected stage list directly from retained calibration tiers using the emitter's `intervals()`/`vapply()`/`lapply()` logic, then compare `pilot` and `diag_grid_intervals` with those values. Preserve the existing integer interval representation and numeric-compatible tier comparison. Validate the underlying retained schedules/grids as needed for these completed cases so an empty source plus empty report cannot satisfy a population requirement. Add the NULL/empty per-tier diagnostic counterexamples and retain both escalation-state positives. This needs only an acceptance-script change, not a sampler change.

## Compatibility with actual v2.2 instrumentation

- Executing the actual R `finish()` on retained-field fixtures produced integer scalar `stages$final`, integer `stages$pilot` of length one for S3 and two for S5, double `stages$tier_final`, and integer scalar `cut_group_large`. Both positives passed. The integer-tier variant also passed. In `v3_calib.R`, the default `tier = 0` and escalation assignment `e <- 1` explain why final tier can be double; the acceptance check correctly converts it to integer rather than requiring integer storage.
- The best-before/after checks reproduce the emitter's assignment from `hpm_before_local`, `hpm`, `hpm_F`, and its model-identity changed flag. Legitimate NULL `stop`, escalation `blocked`, and absent `scored_set` remain accepted for these completed p500 SMC cases.
- `cut_group_large` uses the same `sum(vapply(..., FALSE))` expression as the emitter, yielding integer here. Its boolean companion is compared consistently.
- `v3_fit.R:157` snapshots the registry immediately after calibration, before the final run; its final report is obtained at line 89. The HLL fixture with NA exact count/log-sum, positive scalar estimates, positive memory estimate, and calibration estimate no larger than final passed. **Exact C++ report names/order and estimator behavior cannot be independently confirmed from these named R files:** the report is returned by `.v3cpp$cpp_registry_report()`. The script requires the order `n_distinct`, `n_distinct_hll`, `log_sum_exp_F`; this review confirms that expectation is satisfiable, not that the uninspected C++ producer emits that order. No demonstrated R-side type mismatch was found.

## Precompile and job-side audit review

`precompile.R` parses successfully (eight expressions), and its guard evaluates TRUE against the actual final parsed expression of `v3.R`, `V3_CPP_KEY <- v3_compile()`. It sets `V3_CORE_DIR`, evaluates the preceding expressions, and invokes `v3_compile(quiet = FALSE)` once explicitly. Under the direct Rscript invocation there is no enclosing `source()` call supplying an `ofile`, so the entry point's directory discovery uses the supplied environment variable. The preceding source loop defines the R layer; it does not execute the omitted final compile assignment. No frozen source bytes are edited.

`v3_compile()` builds the shared cache under its key/lock and writes READY, then loads a private copy. `quiet = FALSE` makes both sourceCpp calls use `showOutput = TRUE`; stdout and stderr go to `compile_<jobid>.log`. The later units source the normal entry point and find the same source-derived READY cache, loading private copies instead of rebuilding the shared cache. This is the intended one-build/cache-reuse path; no real build or reuse was executed in this review.

The wrapper refuses an existing `.cpp_cache` before precompile. It sets `CASE=precompile`, invokes precompile before either unit, extracts the full 64-hex key, and records shared-cache `.so` SHA-256 lines. `precompile.R` itself is included in the bundle SHA-256 record. Under `set -euo pipefail`, a failed precompile exits before unit launches; a failed unit exits before its success line. The already-installed EXIT trap captures the original status and writes the active case, UTC end, and final status. Success resets `CASE=none`. Hard scheduler kills can prevent a trap; such missing terminal evidence will fail acceptance. Static control-flow review found no additional precompile/job blocker.

JOB.md now retains scheduler final state/exit information, compiler output, submitted bundle bytes/hashes, and acceptance stdout/stderr/status. **Small documentation correction:** transfer step 4 currently deletes scratch and step 5 runs/saves acceptance. Swap those steps to make its stated “audit trail first, then deletion” sequence include the ACCEPTANCE log before deletion. Downloaded result copies and checksums already precede deletion, so this ordering issue is distinct from the demonstrated false acceptance above. Preserve the frozen submitted source tree along with its manifest; this review did not inspect that manifest or verify its entries.

## Reviewed byte identities

SHA-256 values were computed read-only from the named files:

| File | SHA-256 |
|---|---|
| compare_identity.R | `d2120ab3ad087de81279cf7bcef308982b25a0f9e725fd01ae025dc25cf15cfc` |
| job.sh | `37f3360eefdc94fb13e3b5ec78cbf5b4e36a53a312eb0fb7ff1de0b22f2e748c` |
| precompile.R | `d328b852204ef56ebbaa23c119364a6db1fead9d2e8dd2c3ad47004833066293` |
| JOB.md | `08b4c00868759dbe20f76214103ca1f7ca1f4bf7b33d45436f5de49823ef50a1` |
| DRYRUN_negative_controls.log | `d28ece82fe939eeaaf1871a273f5522a8e3c10dde3ac91b5300c16533dd93074` |
| v3.R | `951ffb3476c38e24de8b532827e83590a40d02fe0d0525beb1d025fb33b4eaed` |
| v3_fit.R | `2675e06e79a293cabe7f3317a9006f294dec9567a4d6f27f25e156bcd645a6d5` |
| v3_calib.R | `6df71bd2a003b27ef28421bceb5b02b6e9995b17ae2efd3307016d80793c420d` |

Only the named prior gate review, five named bundle files, and three named core R files were read. No comparator, environment script, C++ source, manifest, historical outputs, or other project file was read. The in-memory harnesses were piped directly to R; no harness/log file was created. Only this review was written.

## Five-line summary

01. Bundle verdict: ACCEPT WITH FIXES; validate per-tier diagnostic stage contents before submission.
02. Both original named-NULL counterexamples and conflicting/duplicate final statuses are rejected.
03. Updated synthetic positives pass for double and integer final tiers, with the unchanged comparator stubbed.
04. Precompile/cache reuse and failure recording are statically correct; place acceptance-log retention before scratch deletion.
05. No R-side type mismatch found; C++ HLL field order remains outside scope; only this review was written, with no SSH/network or fits.
