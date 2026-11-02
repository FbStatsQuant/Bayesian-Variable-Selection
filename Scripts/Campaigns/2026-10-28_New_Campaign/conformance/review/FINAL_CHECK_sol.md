# CONF final targeted check — Sol 6.1

Reviewed 2026-10-28, America/Chicago. All paths below are relative to C, the campaign directory named in the brief. This is an independent review, not production release authorization.

**Decision: the requested documentation repairs are present, but not every finding is resolved. The job bundle remains REJECT as an enforceable acceptance gate.** Its source pins and escalation/failure-exit repairs are substantial and correct, but its acceptance criteria still admit evidence that the brief requires it to reject. Make the small gate repairs below before submission as the final CONF gate. No sampler change or new local fit is needed.

## Scope and verdicts

I read only the named prior review, bundle directory, comparator/self-test/reg2 drivers, evidence section 8 and round-3 logs, three conformance documents, and the named v2.1/v2.2 source trees. I used R 4.4.1 read-only to compute adapter source records and exercise comparator/acceptance expressions on in-memory synthetic records. No compilation, fits, SSH, network, or other output-file writes were performed. Historical NOTS files and the production runner environment outside these paths were not read; their identity is supported here by the supplied pins/dry-run log, not independently re-read historical bytes. Only this review file was written.

| Deliverable | Final verdict | Meaning / remaining condition |
|---|---|---|
| Code v2.2 | **ACCEPT** | The reviewed plain-field order and registry ownership fixes remain correct. The export-size documentation now closes original item 6. Acceptance is for the implementation under the stated conditional statistical guarantee; it is not certification of identical time-dependent stops or production-platform execution. |
| Regression | **ACCEPT WITH FIXES** | Round-3 source/logs support the reported passing comparisons and fatal driver gates. Close the small remaining N3 list-hash attribute hole and qualify the broad shape claim accordingly. Production and unexercised status gates remain pending. |
| OUTPUT_FIELDS | **ACCEPT** | Stage-T ambiguity and the 32-bit export limit are now explicit. |
| PATCHES | **ACCEPT WITH FIXES** | N6's cost, historical attribution, and statistical-prefix corrections are complete. Remove the remaining implication at line 4 that the reviewer defined/authorized the narrowed contract; original item 1 is still not an owner-approved waiver. |
| CONF_NOTS_IDENTITY bundle | **REJECT** | Environment, checksum-manifest, and required-new-field checks still have false-accept paths. Complete the small audit/freshness provisions as well. The repaired core checks are useful, but an ACCEPT line does not yet establish all the intended evidence. |

## Per-item status

RESOLVED means the requested correction is supported in this review's scope. PARTIAL identifies a remaining requirement, not an observed sampler regression.

| New finding | Status | Assessment |
|---|---|---|
| N1 — escalation assertions and failure exit | **PARTIAL** | The original missing/wrong/extra-reason and exit-zero defects are repaired: exact reasons, tier-0 trigger evidence, state/tier, completed SMC status, unblocked escalation, and record/fit instrumentation equality are asserted; accumulated failures exit 1. However, the requested required-new-field validation is incomplete: empty fit plain-PIP fields and missing record plain summaries can still pass. See F3. |
| N2 — empty named lists / names-attribute order | **RESOLVED** | Explicit suffix indexing fixes the empty-prefix case. Full attribute-name order is checked before dropping the names value. New saved assertions discriminate; independent in-memory mutations each produce a difference. |
| N3 — code provenance shape / identity mode | **PARTIAL** | Unique names, expected insertion position, lengths, parent/vector attributes, scalar 64-hex values and explicit cross/identity modes are repaired and tested. List-typed hash elements still lose their own attributes from the shape check. See F4. Actual adapter output uses a named character vector, so this residual does not invalidate the saved real-record comparison. |
| N4 — stage T | **RESOLVED** | OUTPUT_FIELDS:113 explicitly says the last bridge stage, burn-in and measured rounds cannot be distinguished at T in pilot/diag records. |
| N5 — pinned source/environment/audit gate | **PARTIAL** | Both source identities independently recompute correctly; all 25 v2.2 manifest entries verify. Historical file/input pins, allocations, seeds, environment setup, Slurm resources and per-unit checks are now concrete. The acceptance environment check is incomplete, the local checksum parser permits incomplete manifests, and launch/failure/freshness evidence is not fully enforced. See F1, F2, F5. |
| N6 — PATCHES cost/history/replay | **RESOLVED** | P3:75 now states registry work plus O(M log M) export and unisolated timing. P4/P5 identify counts as supplied historical background. P5:116 limits replay to the statistical prefix and excludes whole-record identity. |
| N7 — driver failure exits / tautology | **RESOLVED** | reg2_r1/reg2_r1e now accumulate failures and quit 1; extra checks have a fatal gate and saved-only mode. Source-hash/CSV failures are asserted. The NaN assertion now compares the two different byte vectors directly. Inspected round-3 logs agree with section 8. |

For completeness, the original findings retain these dispositions; the four specifically named documentation items are all resolved.

| Original item | Status | Final targeted disposition |
|---|---|---|
| 1 | **PARTIAL** | Conditional/common-operation identity is disclosed consistently in REGRESSION/JOB. Literal guard invariance is not established; no owner waiver is supplied. PATCHES:4 still says “as defined by the review.” |
| 2 | **RESOLVED** | Strict numeric/payload and ordinary container attribute-order repairs retained; N2 is closed. The custom provenance exception is tracked under 7/N3. |
| 3 | **RESOLVED** | Allowlist/order enforcement now handles the empty named-list corner case. |
| 4 | **RESOLVED** | Old finish fields precede re-appended plain fields and instrumentation. |
| 5 | **RESOLVED** | CalState retains the registry owner before storing its pointer; destruction order preserves its lifetime. |
| 6 | **RESOLVED** | OUTPUT_FIELDS:115 documents the export limit M <= 2^31 - 1, satisfying the requested guard-or-documentation remedy. This is documentation, not a newly added checked conversion. |
| 7 | **PARTIAL** | N3's remaining list-element attribute hole and N5's environment gate remain. |
| 8 | **PARTIAL** | Real successful escalation and production identity await the remote gate. Real escalation-preflight stop, schedule_limit and numerical_failure are expressly still unexercised. |
| 9 | **RESOLVED** | Retained prior disposition: p30 reference and extrapolation are qualified. |
| 10 | **RESOLVED** | Stage-T ambiguity is explicit (N4). |
| 11 | **RESOLVED** | Retained prior disposition: ledger events, repeats and union cardinality are distinguished. |
| 12 | **RESOLVED** | Retained prior disposition: availability and type qualifications are present. |
| 13 | **RESOLVED** | The surviving zero-runtime-cost statement is replaced (N6). |
| 14 | **RESOLVED** | Retained prior disposition; no new broad registry certification is claimed. |
| 15 | **RESOLVED** | Retained prior disposition; round-3 p500 log again reports ordered 88-column schema and zero non-exempt CSV differences. |
| 16 | **RESOLVED** | Supplied-history labels and qualified statistical-prefix replay address the remaining requests (N6). |

Original status count: **13 RESOLVED, 3 PARTIAL, 0 OPEN**. N-series status count: **4 RESOLVED, 3 PARTIAL, 0 OPEN**. The new residual counterexamples are described below, not hidden by these counts.

## Remaining fixes, ordered by gate impact

### F1 — HIGH: wrong numerical environment can pass (N5)

`jobs/CONF_NOTS_IDENTITY/compare_identity.R:31-32` checks a substring in R.version.string, a substring in LOADEDMODULES, and only OMP_NUM_THREADS/OPENBLAS_NUM_THREADS. The comparator exempts every environment value. It does not enforce Rcpp 1.1.0, BLAS/LAPACK identity, the remaining numerical thread settings, or RNG kind. The wrapper prints Rcpp but does not assert its version; the acceptance script never reads run_env. Thus a package/BLAS change under the same R/GCC module names can escape the promised environment gate. Even R string `R version 4.5.20` satisfies the current substring test.

**Executed counterexample:** preserving record shape and the checked R/module/two-thread values, replace the two session-info strings with `Rcpp 9.9.9` and `BLAS wrong`, and set MKL_NUM_THREADS to `8`. The actual script's criteria loop returns zero failed criteria for both cases. This demonstrates missing validation, not that the supplied historical or future production environment is wrong.

**Minimal fix:** assert exact runtime versions in the wrapper, including Rcpp; record and validate the expected BLAS/LAPACK implementation and relevant numerical configuration against the historical environment. Require every applicable numerical thread variable to be 1, and verify RNG kind. Parse an exact R version rather than a substring and tokenize module names. Have acceptance consume/check the saved job-environment evidence, including CPU identity/constraint, instead of merely transferring it. Do not require incidental host/PID/timestamp equality.

### F2 — MEDIUM: local checksum acceptance does not require the two output entries (N5)

`compare_identity.R:24-25` applies `all(vapply(...))` to whatever lines are present. An empty SMCBVS.sha256 gives `all(logical(0)) == TRUE`; a single valid entry or duplicate entries can leave an output unchecked. The four-file existence check does not enforce checksum coverage.

**Executed counterexample:** with all virtual unit files present, return `character(0)` from reading each new checksum file. All acceptance criteria pass. The Slurm-side sha256sum command would reject an empty file during the original job; that does not repair the independent local/download verification claimed by JOB.md.

**Minimal fix:** require exactly two well-formed lines, exactly the unique basenames `SMCBVS.rds` and `SMCBVS.csv`, each with a 64-hex digest, and verify both actual files. Reject path components, duplicates and missing entries. The production adapter's `smcbvs_done_valid()` already illustrates the manifest-length/name checks. Add empty/one-entry/duplicate negative controls.

### F3 — MEDIUM: required new outputs are not fully required (N1)

`compare_identity.R:44-45` admits `pip_plain = numeric(0)`, `pip_plain_r = matrix(numeric(0), 0, 4)` and `mpm_plain = integer(0)`: the range predicate is vacuously true, dimensions match the zero vector, and the derived empty MPM agrees. The comparator allows new fields without comparing their contents. The script also never requires `record$pip_plain` or `record$mpm_plain`; removing either/both remains an allowed subset of additions.

**Executed counterexample:** replace the three new fit plain-PIP fields with the empty values above; all criteria pass. A synthetic positive control already establishes that the loop is otherwise satisfiable. This is not evidence that current v2.2 emits empty PIPs.

**Minimal fix:** require all mandatory new fit/record fields for these completed SMC cases. Check fit vector/matrix dimensions against retained p and retained-index names, finite [0,1] values in both vector and matrix, and record summaries against their original-index mapping. Require the instrumentation version and expected required subfields. Add empty/missing-field negative controls; keep the existing exact escalation-reason checks.

### F4 — LOW: attributes on list hash scalars are ignored (N3)

`work/regression2/cmp2.R:131-133,144-159` validates a list element with is.character/length/hex checks but never checks its attributes. Adding `attr(fy[["core/a.R"]], "marker") <- 1` preserves all those predicates. The outer list's attributes are unchanged.

**Executed counterexample:** compare `record$code$files` lists containing scalar 64-hex strings, with the required registry entry inserted in the new list. The control has n_diff=0. Add a marker attribute to an old hash scalar: n_diff remains 0. This contradicts the advertised full shape check for the expressly supported list-typed case; it is not a hole in the actual character-vector provenance used by the adapter.

**Minimal fix:** require list hash elements to be unadorned scalar strings (add `is.null(attributes(v))` to the scalar predicate), or compare each old scalar's attributes by its file-name mapping and specify the new scalar's shape. Add marker/class/names attribute mutations and a positive control. Apply to both comparator copies; rerun the self-test and saved comparisons only. No refit is needed.

### F5 — MEDIUM: complete the audit and fresh-build handoff (N5)

`job.sh` records job ID/start and adds an end timestamp only after both cases succeed. It has no EXIT trap that records a failed case's command/status/end, and it does not enforce the instruction to upload without `.cpp_cache`. The loader's cache key covers source bytes, not compiler/R/Rcpp environment; accepting an old cache would therefore weaken the environment evidence. The adapter also explicitly skips an existing valid unit before loading the core, while the fixed output/run ID is reused. A resumed/skipped unit should not be presented as a fresh execution by the current Slurm job. Neither issue proves a bad current result, but the wrapper should enforce the supplied fresh-run assumptions.

**Minimal fix:** fail before execution if a cache or pre-existing unit outputs are present for this fresh gate; preserve them and use a new location/run ID rather than deleting evidence. Record the exact launch command and per-case exit status; add an EXIT trap with final UTC/status and failed case. Archive the submitted bundle/config hashes and capture the actual compile command/output (the core loader defaults to quiet compilation). After completion, save the scheduler final state/exit information and acceptance stdout/exit code with the downloaded evidence. These are audit changes, not requests to execute remotely during this review.

One additional text-only fix closes the original contract-attribution issue: change PATCHES:4 from “as defined by the review (Sol finding 1)” to “the conditional guarantee tested here,” and leave any acceptance of a weakened original requirement to the owner. Successful submission/execution of two completed units cannot certify universal stop invariance or the expressly untested failure paths.

## Inspected and executed evidence

Saved text evidence supports the claimed repairs: `logs/cmp2_selftest_round3.txt` ends with **97 assertions passed**; `reg2_r1_round3.txt` reports **28 matched comparisons, 0 differing paths, 0 non-allowlisted additions**; `reg2_r1e_round3.txt` reports **199,750 record paths, 0 differing, CSV 2 x 88 with 0 non-exempt cell differences**; `reg2_extra_saved_round3.txt` reports **100/100**; the round-1 saved comparison log flags only the documented old field-order violation. These are inspected saved logs, not freshly rerun fits or a claim that I executed the entire 97-assertion file. Its saved-fit dependencies fall outside the named-file read scope.

The supplied historical-as-new dry run reports FAIL on 14 criteria (seven per unit), exit=1, with source/adapter/new-field/cross-version provenance failures and passing old-data checks. It is a useful negative control. It does not mutate the unchecked environment, checksum coverage or new-field dimensions, and cannot establish those properties.

Independent R checks were invoked through stdin with `"C:/Program Files/R/R-4.4.1/bin/Rscript.exe" --vanilla -` (exit 0). The harness parsed the named acceptance script; evaluated its actual PIN assignment, CSV exemption assignment and complete per-case loop; supplied synthetic historical/new records; and replaced only file reads/hashes/existence with in-memory fixtures. It captured failed chk predicates instead of running the final quit. Thus “ACCEPT” below means zero failed actual criteria, not a real production-file acceptance or a separate execution of the final process-exit branch. No random draws/seeds or sampler loading were needed. Startup emitted C.UTF-8 locale warnings on Windows; the source hash routine uses radix sorting.

| In-memory check | Result |
|---|---|
| Positive synthetic control | 0 failed criteria |
| Wrong aggregate source hash | Rejected, 2 failed criteria |
| Wrong input hash | Rejected, 4 failed criteria |
| Missing escalation reasons (both cases) | Rejected, 2 failed criteria |
| Changed old pip_primary value | Rejected, 2 failed criteria |
| Changed Rcpp/BLAS session information plus MKL threads=8 | **0 failed criteria — F1** |
| R version string 4.5.20 | **0 failed criteria — F1** |
| Empty checksum manifests | **0 failed criteria — F2** |
| Empty new fit PIP vector/matrix/MPM | **0 failed criteria — F3** |
| Empty named-list unauthorized addition | n_diff=1, correctly rejected |
| Movement of names attribute around marker | n_diff=1, correctly rejected |
| List-hash marker attribute mutation | **n_diff=0 — F4** |

The comparator counterexample can be reproduced using only the named comparator and in-memory values:

```r
H <- function(x) strrep(x, 64)
a <- list(code = list(files = as.list(c("core/a.R" = H("1")))))
b <- list(code = list(files = as.list(c("core/a.R" = H("2"),
                                       "core/cpp/v3_registry.h" = H("3")))))
cmp2_run(a, b, "record")$n_diff             # 0: control
attr(b$code$files[[1]], "marker") <- 1
cmp2_run(a, b, "record")$n_diff             # 0: attribute change missed
```

Adapter-only sourcing and `smcbvs_source_record()` independently produced the exact pins:

| Tree | source_sha256 | v3_source_sha256 |
|---|---|---|
| v2_1_baseline | `b28719e65383bd23b29f1ae496c2bd83668e6aee318061e852b9ee33dc394e23` | `8d03d3649cffe68527ed71efb824c644d3a6245a6109f2929029f1c86cace1f8` |
| v2_2 | `2e39575aa31d82797bac4f80108dd4340c9b6eac96a1b70a53c68c2918108d9c` | `c0aebe86bfd07525bc97e2fd2bcacf4608142c778d25d584a38119e96ef82517` |

All **25** entries in the bundle's v2_2.SHA256SUMS match the named local v2.2 tree (0 mismatches). The two comparator copies are byte-identical by SHA-256. job.sh/env.sh/manifest have LF line endings, no CR bytes. Reviewed artifact hashes:

| Artifact | SHA-256 |
|---|---|
| cmp2.R, both copies | `5c7ad65c733253a45367aea8de644da02620538ecfc1d1657d52e07bc7ad8b3f` |
| compare_identity.R | `e9a9761f25cdeb21e7db1aeba3e10fcdd2c116f202ab7d99210e9871093119de` |
| job.sh | `aad1d7a1706a60c7c72b41c048aa0bae42203a59a955e377805ae70af97485c7` |
| env.sh | `c26ececc27edcaa7ab66ca1291ab53398cdafc81c52b76144438a706af487e60` |
| v2_2.SHA256SUMS | `d76c0579f5c28b3bf0236752b7382aa3e151191441533936d7b012fe7881e6e2` |

## Six-line summary

01. Code ACCEPT; OUTPUT_FIELDS ACCEPT; original items 6, 10, 13 and 16 are resolved.
02. Regression ACCEPT WITH FIXES: N2/N7 pass; close N3's list-hash scalar attribute hole.
03. PATCHES ACCEPT WITH FIXES: N6 is resolved; remove reviewer-authority wording for the narrowed contract.
04. Job bundle REJECT as the final gate: wrong environment, empty checksum manifests and empty new PIPs can pass.
05. Source pins/25-file manifest verify; escalation assertions and nonzero failure exits are repaired; production gates remain pending.
06. Only this review was written; read-only R checks used synthetic memory fixtures; no fits, compilation, SSH or network.
