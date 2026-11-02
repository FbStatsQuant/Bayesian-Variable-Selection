# CONF NOTS bundle gate check — Sol 6.1

Reviewed 2026-10-28 (America/Chicago). **Bundle verdict: ACCEPT WITH FIXES.** The specifically requested historical counterexamples are now rejected and a positive synthetic control passes. F1, F2, F4 and PATCHES line 4 are resolved. F3's PIP defects are resolved, but required instrumentation can still be empty. F5's fresh-run refusals and EXIT trap are repaired, but its audit requirements are not yet complete. Apply the minimal fixes below before submission.

This is a narrow pre-submission gate review, not a production execution result or approval of the conditional identity contract in place of the original brief.

## Status table

| Item | Status | Evidence / remaining fix |
|---|---|---|
| F1 — numerical environment | **RESOLVED for the requested gate** | Exact R string, tokenized module equality, selected historical session lines including Rcpp/BLAS/LAPACK, all five recorded thread settings and RNGkind are checked. Wrong Rcpp, BLAS, MKL threads and R 4.5.20 are rejected. Saved job evidence is now consumed. The wrapper also exports BLIS/FlexiBLAS thread limits. |
| F2 — checksum coverage | **RESOLVED** | Requires exactly two well-formed, unique basename entries, precisely RDS and CSV, and verifies both hashes. Empty, one-entry, duplicate, path-component and malformed-digest manifests are rejected. |
| F3 — required new outputs | **PARTIAL** | Empty/missing fit PIPs and missing record PIP/MPM/instrumentation are rejected; 500-vector/500-by-4 shape, names, range, island mean and MPM are enforced. However, named NULL placeholders for required instrumentation outputs still pass. See fix 1. |
| F4 — list-hash scalar attributes | **RESOLVED** | `cmp2_hash_ok()` requires list hash scalars to have NULL attributes. Marker, class and names mutations each give one comparator difference. Both comparator copies have the same SHA-256. |
| F5 — fresh execution and audit | **PARTIAL** | Cache/output refusals, bundle hashes, launch commands and final status/end/failed-case trap are present and correctly placed. Actual compile command/output capture and explicit post-job scheduler/acceptance retention remain absent. Terminal-status parsing also accepts contradictory statuses. See fixes 2–3. |
| PATCHES line 4 | **RESOLVED** | Now says “The conditional guarantee tested here” and explicitly leaves acceptance in place of the brief's literal wording to HQ. Reviewer authority is no longer implied. |

## Executed counterexamples

R 4.4.1 was invoked through a PowerShell literal here-string piped to `"C:/Program Files/R/R-4.4.1/bin/Rscript.exe" --vanilla -`. The harness parsed the revised acceptance script and evaluated its actual expressions from `PIN` through the final ACCEPT/failure branch. Only file existence, reads, hashes, CSV reads and `quit()` were replaced with in-memory fixtures/interception; the comparator and acceptance predicates were unchanged. A failure `quit(status=1)` was intercepted to observe its requested exit without terminating the remaining checks. Counts below cover mutations applied to both cases, except job-evidence mutations, which are evaluated once. The harness process itself exited 0.

The positive fixture contains both expected escalation cases, matching old fields, pinned input/source/file hashes, exact synthetic historical numerical environment, 500 named PIPs, a 500-by-4 island matrix, matching original-index record summaries, required instrumentation and the registry provenance insertion. It tests satisfiability of this acceptance script, not real production files or production numerical identity.

| In-memory test | Failed criteria | Requested gate exit | Result |
|---|---:|---:|---|
| Positive synthetic control | 0 | 0 | **PASS; actual ACCEPT branch printed** |
| Rcpp session line changed to Rcpp_9.9.9 | 2 | 1 | Rejected |
| BLAS session line changed to `BLAS: wrong` | 2 | 1 | Rejected |
| MKL_NUM_THREADS changed to 8 | 2 | 1 | Rejected |
| R version changed to `R version 4.5.20` | 2 | 1 | Rejected |
| RNGkind changed | 2 | 1 | Rejected |
| Empty checksum manifest | 2 | 1 | Rejected |
| One-entry checksum manifest | 2 | 1 | Rejected |
| Duplicate RDS entries | 2 | 1 | Rejected |
| Manifest entry with `../SMCBVS.rds` | 2 | 1 | Rejected |
| Manifest with short non-64-hex digest | 2 | 1 | Rejected |
| Empty fit plain-PIP vector, 0-by-4 matrix and integer MPM | 4 | 1 | Rejected |
| Missing fit `pip_plain` | 4 | 1 | Rejected |
| Missing fit `pip_plain_r` | 2 | 1 | Rejected |
| Missing fit `mpm_plain` | 4 | 1 | Rejected |
| Missing fit `instrumentation` | 8 | 1 | Rejected |
| Missing record `pip_plain`, separately | 2 | 1 | Rejected |
| Missing record `mpm_plain`, separately | 2 | 1 | Rejected |
| Missing record `instrumentation`, separately | 2 | 1 | Rejected |
| Empty record plain-PIP vector and MPM | 2 | 1 | Rejected |
| Island PIP matrix entry changed to 2 | 2 | 1 | Rejected |
| Missing instrumentation version, with matching fit/record copies | 2 | 1 | Rejected |
| Named NULL `scored$after_calibration`, matching fit/record copies | **0** | **0** | **False accept; fix 1** |
| Named NULL `best_before_local`, matching fit/record copies | **0** | **0** | **False accept; fix 1** |
| Job evidence contains only `final_status 1` as its status | 1 | 1 | Rejected |
| Job evidence contains `final_status 0` and then `final_status 1` | **0** | **0** | **False accept; fix 3** |

| Comparator-only test | n_diff | Result |
|---|---:|---|
| List-typed hashes, unadorned scalar values, registry inserted | 0 | Positive control passes |
| Marker attribute on an old list hash scalar | 1 | Rejected |
| Class attribute on a list hash scalar | 1 | Rejected |
| Names attribute on a list hash scalar | 1 | Rejected |

The saved `cmp2_selftest_final.txt` reports **101 assertions passed**, including its four F4 assertions. I inspected the named self-test and log; I did not execute the full self-test because it reads saved RDS inputs outside this review's named paths. The named negative-control log reports **21 failed criteria, exit=1**, as JOB.md states; it is inspected supplied evidence, not a newly executed historical-file dry run.

## Minimal fixes before submission

1. **Reject empty required instrumentation (F3).** At `compare_identity.R:64–70`, name membership alone accepts NULL values for outputs that must be populated on these completed SMC fits. Preserve legitimate NULL `stop`, `escalation$blocked` and `scored_set`, but validate the populated instrumentation against retained fit outputs and its emitted schema. In particular, compare `best_before_local` with `f$hpm_before_local`, compare `best_after_local` with `f$hpm`/`f$hpm_F` and the derived changed flag, and require a populated `scored$after_calibration` with its three emitted fields (`n_distinct`, `n_distinct_hll`, `log_sum_exp_F`) and appropriate HLL scalar/NA values. Check required stages and cut-group reporting values as well. No sampler modification is needed. Add the two demonstrated empty-placeholder controls and a positive control. A minimal reproduction of the false accepts, after constructing any passing fixture, is:

   ```r
   b$fit$instrumentation$scored["after_calibration"] <- list(NULL)
   b$instrumentation <- b$fit$instrumentation
   # Separately, starting again from the passing fixture:
   b$fit$instrumentation["best_before_local"] <- list(NULL)
   b$instrumentation <- b$fit$instrumentation
   ```

2. **Complete compile and post-job evidence retention (F5).** The job still invokes the frozen loader with `v3_compile(quiet=TRUE)`, which calls `sourceCpp(showOutput=FALSE, verbose=FALSE)`; the actual compile command/output is not preserved by this bundle. Capture it through a job-side logging/precompile mechanism without silently changing the frozen source pins. JOB.md should explicitly require saving the scheduler's final state/exit information and the acceptance command, stdout/stderr and exit status with the downloaded bundle/environment/source manifest. Its current transfer list mentions only results, the Slurm log and run_env, and then scratch deletion; add these audit artifacts before that deletion step. Preserve the submitted bundle/source bytes corresponding to the recorded hashes.

3. **Make terminal audit evidence unambiguous (F5).** Replace `any(ev == "final_status 0")` at `compare_identity.R:83` with a requirement for exactly one well-formed terminal-status line equal to zero. Require the expected job header/end, both recorded launch commands and both successful per-case status lines before claiming that this evidence establishes fresh execution. The five-line synthetic evidence `Flags: amx_tile`, the three exact version lines, and `final_status 0` currently passes despite containing none of that audit trail. Reject conflicting/duplicate final statuses. This does not require incidental host/PID/timestamp equality.

These are gate/audit fixes. They do not require a local fit, a change to statistical code, or an owner waiver of the original identity requirement. Until applied, an ACCEPT line still overstates required-new-output and audit completeness.

## job.sh / env.sh static review

Static Bash syntax/control-flow review found no syntax defect in the current scripts. This is `bash -n`-level reasoning; no Bash execution, module loading, compilation or Slurm submission was performed.

- `set -euo pipefail` is active. The EXIT trap is installed before bundle hashing, environment setup, freshness checks and case execution. It captures `$?` immediately in `rc`, then writes `failed_case`, UTC `end` and `final_status`. A nonzero case command exits before the following success echo; the trap retains the case name and failing status. The shell retains the original failing exit status after a successful EXIT trap. Success ends after `CASE=none`, so the trap writes `failed_case none` and `final_status 0`.
- Cache refusal is at the loader's actual path, `$CODE/core/.cpp_cache`. Output refusal is at the adapter's actual run directory, `$OUT/results/conf_identity`. Both precede execution, preserve existing evidence and exit 65. Thus normal prior outputs cannot reach the adapter's saved-unit skip path in this job. The second case may reuse the cache freshly compiled by the first, as intended.
- The Bash array and quoted `"${cmd[@]}"` preserve CLI arguments. Both case IDs, c100 scale, study root, output root, run ID, 2 GB and 1.75 hours match the documented layout/allocation. Each successful command is followed by `.done` existence and strict checksum verification. Under `pipefail`, failures in the environment-recording pipelines abort as well.
- Exact producer/consumer text agrees: `echo "gcc $(gcc -dumpfullversion)"` produces **`gcc 14.3.0`** under env.sh's version assertion. `cat(R.version.string, "\n", sep="")` produces **`R version 4.5.2 (2025-10-31)`** under the intended runtime; `cat("Rcpp ", ..., "\n", sep="")` produces **`Rcpp 1.1.0`**, without an extra space. The trap produces **`final_status 0`** on success. These exactly match the strings read at acceptance lines 82–83. Rcpp is recorded here and enforced at acceptance; env.sh itself asserts GCC/G++ and R, not Rcpp.
- env.sh temporarily disables nounset for module initialization, restores it, sets all declared numerical thread limits, pins module libraries/locale and unsets user compiler overrides. The RDS gate enforces the five thread variables actually recorded by the adapter. Both shell files have LF endings, zero CR bytes and a final LF.
- The fixed evidence filename is truncated at job start and keyed by Slurm job ID; contradictory statuses are not expected from this normal one-shot wrapper. Nevertheless, the downloaded-evidence parser must reject them rather than rely on that assumption. Scheduler hard kills may prevent the EXIT trap; missing terminal success is correctly rejected and must be treated as incomplete.

## Source and artifact verification

I sourced only each named tree's `study/adapter.R` into an isolated R environment and called its source-record function; this does not load the core or compile. Both source-pin pairs recomputed exactly:

| Tree | source_sha256 | v3_source_sha256 |
|---|---|---|
| v2_1_baseline | `b28719e65383bd23b29f1ae496c2bd83668e6aee318061e852b9ee33dc394e23` | `8d03d3649cffe68527ed71efb824c644d3a6245a6109f2929029f1c86cace1f8` |
| v2_2 | `2e39575aa31d82797bac4f80108dd4340c9b6eac96a1b70a53c68c2918108d9c` | `c0aebe86bfd07525bc97e2fd2bcacf4608142c778d25d584a38119e96ef82517` |

All **25** source-manifest entries verify against the named v2.2 tree, with **0 mismatches**. The two comparator copies are byte-identical.

| Reviewed artifact | SHA-256 |
|---|---|
| job.sh | `2b6da4ac0bbfc517c39be2fbcb35a070d42e0582b04386a5008ae30b6b7327f9` |
| env.sh | `c26ececc27edcaa7ab66ca1291ab53398cdafc81c52b76144438a706af487e60` |
| compare_identity.R | `b7434573dd55b7055b7aafa8d4dd396c9cdfb0ce58181ae99e56292ce3daaeed` |
| cmp2.R, both copies | `947f6803fe75893f5d6a6ddf7db509940cdf41b0e6132efd4694f46bb0edfa82` |
| v2_2.SHA256SUMS | `d76c0579f5c28b3bf0236752b7382aa3e151191441533936d7b012fe7881e6e2` |
| JOB.md | `79dc3b030af30fc295b9666baa8d54b16998985be77ab904d67e1b6a6372b140` |
| DRYRUN_negative_controls.log | `30585f3ce5268045691f5bc90b23f0638ba760ac6ed82b07c2a82610f7b9958d` |

Scope was restricted to the named prior review, named bundle files, named comparator/self-test/log, PATCHES.md and the two permitted core trees. No historical output files outside this scope were read. No SSH/network, simulations, fits, benchmarks or compilation were performed. Only this review file was written. R emitted Windows startup warnings for the inherited C.UTF-8 locale; source hashing uses radix order. No random draws or seeds were needed for the deterministic fixtures. Production execution and scheduler evidence remain pending.

## Five-line summary

01. Bundle verdict: ACCEPT WITH FIXES; apply the listed gate/audit fixes before submission.
02. F1, F2, F4 and PATCHES line 4 are resolved; every specifically requested counterexample is now rejected.
03. The synthetic positive control passes; empty required instrumentation still passes and keeps F3 partial.
04. Fresh-run refusals and EXIT-trap text are correct; compile, scheduler and terminal-audit gaps keep F5 partial.
05. Both source-pin pairs and all 25 manifest entries verify; only this review was written, with no SSH/network or fits.
