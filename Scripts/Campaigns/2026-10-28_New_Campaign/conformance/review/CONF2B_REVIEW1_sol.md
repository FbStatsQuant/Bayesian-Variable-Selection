# CONF-2b review 1 — independent Sol review

Reviewer: Sol 6.1, 2026-10-29. Read CHARTER.md and DECISIONS.md, including D10/D11/D16/D19/D20/D21. No subagents, SSH, NOTS contact, submissions, compilation, or new SMC/benchmark fits. Shell submissions in the test suite use local stubs. Reviewed files were not edited. Only this review and scratch files were written.

Scratch evidence **E**: `<PC_TEMP_PATH>`. Paths below are relative to **C**, the New Campaign folder.

## Verdicts

| Deliverable | Verdict | Reason |
|---|---|---|
| 1. v2.2.1 H/L merge | **ACCEPT WITH FIXES** | Core identity and normal H/L behavior are supported; H input validation weakened (F2). P5 is assessed separately below. |
| 2. P5 retry implementation | **REJECT** | F1 breaks the one-retry guarantee under overlapping callers. F3/F4 also need repair. Ordinary saved cycles work, doubling is correct, and retry files do not enter the primary scoring scan. |
| 3. Regression evidence | **ACCEPT WITH FIXES** | Saved numerical comparisons reproduce under the documented exclusions. Harden the forced-stop classifier (F5) and add the newly exposed edge cases before declaring full P5 conformance. |
| 4. cmp2 D20 amendment | **ACCEPT** | Exactly the authorized functional change; downloaded-file acceptance, 101 self-test assertions and 16 real-record controls pass. |
| 5. LOWP pilot revision 7 | **ACCEPT WITH FIXES** | Prior gates and requests remain intact, and the new CSV/native-status check is sound. The frozen-tree check misses unlisted symlinks (F6). |

**The combined package is not ready to freeze/ship: F1 is blocking.** Repair the identified code, regenerate its manifest/diff, and rerun the affected checks. The pilot scripts read the manifest dynamically, so no file-count/hash constant needs updating.

## Findings

### F1 — blocking — a retry committed between the completion check and lock acquisition can be overwritten

**Location:** `code/core/v2_2_1/study/adapter.R:442`, `:446`, `:449`.

The only valid-completion/identity checks occur before acquiring the unit lock. Caller A can see no completed retry and be descheduled; B then acquires the lock, finishes the retry, writes its valid sidecar/done files and releases the lock. A resumes, successfully creates the now-free lock, deletes B's done marker and executes another fit/write. Thus the lock prevents simultaneous writers but does not guarantee one retry or preserve an already completed outcome. The same inherited window also exists on the primary path.

**Reproduction:** `E/scan_probes.R` injects a competing valid scratch retry immediately at A's lock-acquisition boundary. The actual validator reports `competing commit valid at lock acquisition TRUE`; A nevertheless reaches `SECOND STUB FIT EXECUTED`, `SECOND WRITE REQUESTED OVER VALID RETRY`, and returns `skipped FALSE`. No numerical fit was run. Only the core/input loading and final writer were stubbed; the production control flow and validity check were used. The final probe uses byte copies of the saved primary/retry files and matches their recorded LC_CTYPE locale; no primary/retry identity was altered.

**Fix:** after acquiring the lock, repeat identity validation and completion validation before unlinking anything or loading/calling the core. Return the completed unit if it now exists; refuse a newly observed identity mismatch. Keep cleanup of the caller-owned lock on every exit. Add a deterministic two-caller/interleaving test for both primary and retry paths that proves the completed files remain byte-unchanged and no second core call occurs.

### F2 — should-fix — regime H no longer rejects named NULL n/kind/scales fields

**Location:** `code/core/v2_2_1/study/adapter.R:175`, `:181`, `:187`, `:191`.

The H required-name list still contains these three fields, but the merged value checks now all skip NULL, as the LOWP fork did. A list can contain a named NULL element, so presence in `names(d)` does not preserve v2.2's stricter contract.

**Reproduction:** `E/edge_checks.R` builds a hash-consistent deterministic H input and manifest. The control is accepted by both versions. Individually replacing `n`, `kind`, or `scales` with a named NULL is rejected by v2.2 (dimensions, kind, scale respectively) but accepted by v2.2.1. This is an input-validation regression, not an observed change to correctly sealed campaign fits.

**Fix:** apply each value check when `rg$extras_required || !is.null(d[[field]])`. Preserve the fork's optional-extras behavior in L. Add H missing-name and named-NULL controls for each field, plus L controls proving its behavior is unchanged.

### F3 — should-fix — the P5 scanner counts a retry belonging to another seed/unit as this primary's completed retry

**Location:** `code/core/v2_2_1/tools/p5_scan.R:30`, `:31`, `:52`, `:62`, `:66`.

`status_of()` uses `smcbvs_done_valid(prefix, list())`: this verifies the local rds/csv hashes and two rule rows, but supplies no expected identity and never verifies `record$p5` against the primary. A checksum-valid misplaced retry therefore suppresses this primary's eligibility and contaminates the retry-outcome count.

**Reproduction:** `E/scan_probes.R` copies the saved repeat-1 retry into the scratch primary retry slot and writes its correct renamed checksum sidecar. Primary method seed is 5,220,001; the retry's is 5,221,001. The scanner still reports `retry_state=done`, `retried=1`, `eligible=FALSE`. Its saved `p5$primary` also belongs to the repeat, not this primary.

**Fix:** bind the retry to the primary's run/case/seed/source/policy/input identity, exactly doubled allocation, and `p5$primary$files_sha256`/role/factor before counting it as done. Report a mismatched record as invalid and requiring inspection rather than silently treating it as the authorized retry. Cross-check CSV/RDS native status as well. Add wrong-seed, wrong-primary-sidecar and wrong-allocation controls.

### F4 — should-fix — resumed resource-limit units lose their stop phase in CLI reporting

**Location:** `code/core/v2_2_1/study/adapter.R:442`; `study/run_case.R:55`.

The skip return includes only prefix/skipped/rows. The CLI consequently prints `stop=NA` for a valid resumed primary or retry even when its saved fit has a populated runtime-guard/preflight stop. This weakens the promised stop-phase log precisely during resume.

**Reproduction:** `E/scan_probes.log`: `resume skipped TRUE stop missing TRUE saved stop runtime_guard pilot`. The existing saved c5 second-retry stdout independently shows `v3_status=resource_limit ... stop=NA`.

**Fix:** on the valid skip path read the saved record and return its native status and `fit$instrumentation$stop`, using the same structure as the fresh-fit return. Test primary/retry runtime-guard and preflight resumes; compare their final stdout stop text with the saved record.

### F5 — should-fix — forced-stop exemptions admit structural/type/status errors beyond D10

**Location:** `conformance/work/v2_2_1_regression/scripts/a2_compare.R:20`, `:22`, `:26`.

Two gaps remain after the otherwise reasonable stop-timing/island amendments:

* `timing_only` tests only the differing path names. A change in the type, dimensions or attributes of a stop-time field is accepted as if only its clock reading changed.
* Different stop keys yield PASS regardless of statuses or non-allowlisted additions. D10 excludes wall-clock stop-dependent numerical identity; it is not permission for arbitrary output-schema or native-status corruption.

**Reproduction:** `E/regression_probes.R` applies the classifier's actual expressions to saved fits. Setting `stop$elapsed_seconds = "not-a-number"` yields `identical_except_stop_timing / PASS`, although cmp2 reports `[typeof]`. On a different-checkpoint pair, changing status to `completed` and appending `fit$unexpected_scientific_field` still yields PASS and an unallowlisted addition.

**Fix:** retain type/shape/attribute validation when exempting those two timing values, as cmp2 does for its other timing exemptions. Require valid resource-limit/runtime-guard outcomes and enforce invariant schema/allowlist checks before allowing the different-checkpoint exception; do not compare checkpoint-dependent partial-list layouts as though identical progress were guaranteed. Classify those cases explicitly as timing-excluded/non-identity evidence. Add the above negative controls. The four actual saved pairs have valid resource-limit statuses and no additions, so this finding does not show their saved comparisons were falsely reported.

### F6 — should-fix — the frozen-tree check ignores unlisted symlinks

**Location:** `code/lowp/pilot/frozen_check.sh:15`.

`find . -type f` does not list symbolic links. The function therefore returns success for a tree containing an unlisted linked file or directory outside the tolerated cache, contradicting its exact-file-set gate. All four integration points reuse this function.

**Reproduction:** `E/link_probe.py` copies only the 27 manifest-listed files into scratch and creates a real unlisted `study/unlisted_adapter.R` symlink. `E/frozen_link.log` shows the link and `unlisted_symlink_frozen_check_rc=0`. The ordinary actual source tree also passed its checker; this probe exposes a missing refusal, not a hash mismatch in the delivered tree.

**Fix:** enumerate links as well as regular files in the file-set comparison (and reject unlisted special entries), or explicitly reject symlinks outside the compile cache before comparing. Include linked directories, not just linked files. Add refusal tests for an unlisted file symlink and directory symlink, with the ordinary cache tolerance still passing.

### F7 — minor — partial retry files can be reported as no retry evidence

**Location:** `code/core/v2_2_1/tools/p5_scan.R:51`.

`retry_present` checks only done/rds/lock, omitting csv, sha256 and temporary files. A CSV-only scratch retry is reported `retry_state=none, incomplete=0` by `E/scan_probes.R`. A lock-only retry is reported incomplete but also eligible; the latter follows the current documented entitlement definition, but should not be mistaken for a ready-to-launch unit.

**Fix:** detect all unit artifacts for incomplete-state reporting. Expose lock/in-progress/operator-inspection state separately from P5 entitlement, and document which rows can be launched immediately.

## What the evidence supports

**Merge and identities.** Independently recomputed v2.2's 25 hashes and v2.2.1's 27: all match, with no unlisted non-cache regular files. All 21 core files are byte-identical. Harness source copies match those trees. The diff names exactly the six changed/new files. All five retired-fork hashes match the full CODE_LEDGER digests, resolving the limitation in Terra's earlier verifier report. Static diff inspection confirms the regime-specific manifests, fold-hash columns, bases, record ordering and L repeat rule. My independent boundary/grid comparisons add 576 H and 3,456 L case-spec comparisons (prod/dev; p; scenarios; r=1,50,100; both scales, numeric/character and bare/suffixed forms; L primary plus repeats 1–5): zero mismatches, including list order/types. F2 is the exception to the broad unchanged-H-input-check claim.

**Regression (a).** Independently reran cmp2 on all 34 asserted saved/fresh core comparisons: zero differences and zero additions. Independently compared the p500 study record with both fresh and saved v2.2: 199,884 paths each, zero differences/additions, same top-level names, no p5, equal core hashes and non-provenance CSV cells. Forced-stop raw comparator counts reproduce 2/102/72/142; the first pair's two visible differences are precisely its stop clock readings, and the island-aware checkpoint key is correct. The other three are D10 exclusions and prove no numerical identity beyond their differing progress. F5 concerns future false-PASS possibilities in the classifier.

**Regression (b).** Independently reran full comparator checks on all six merged/fork record pairs, plus direct RB/plain PIP/support/case equality, core hashes, CSV cells and rds/csv sidecar verification: all pass under the stated timing/provenance exclusions. log Z matches the actual smoke note at its four displayed decimals. This supports identical non-exempt paired outputs and reproduction of the recorded precision, not historical full-precision or whole-RDS-byte identity. REGRESSION.md now makes this distinction; Terra's qualifications are appropriate.

**Regression (c).** Independently inspected c1–c4 records and verified exactly doubled memory/hours, same method seed, primary-sidecar binding, primary stop binding and both output sidecars. All four current primary rds/csv/sidecar/done hashes equal the saved pre-retry snapshot hashes. c2 completed after preflight failure; the other saved retries remain resource-limited. Inspected c5 negatives and snapshots/ledger: the completed/missing/wrong-allocation refusals and ordinary sequential second-call skip are supported. Independently ran scoring scan on c6: exactly three primaries/repeats, zero retry paths. These saved cycles support the normal path, not the missing concurrent/mismatched/incomplete cases in F1/F3/F4/F7.

**D20.** Functional diff against `work/regression2/cmp2.R` is only the command-vector length condition, plus comments. Before/after hashes reproduce `947f6803...edfa82` and `f2662113...efa048`. Reran the complete acceptance script on the downloaded identity files and environment log: ACCEPT. The separate environment/input/allocation/escalation/instrumentation checks remain enforced. Reran the amended comparator self-test: 101 assertions pass; the real-record negative-control script: all 16 outcomes as expected. Read the saved whole-pipeline dry controls and original review/log; no wider D20 exemption was introduced.

**Pilot.** Diffed revision 7 against the reviewed revision-6 baseline and read the earlier pilot/final-confirmation reviews. Twenty-three files, including guard, cleanup, recovery, truth-wave scripts, lists, most sbatch files and the fabricated-posterior builder, are byte-identical. Existing summarizer gates remain; its substantive additions are the native-status consistency test and informative P5 block. The consistency test correctly rejects a present mismatching/NA status and leaves an absent column alone as documented. Inspected stage/submit/build/task wiring: the full tree and manifest are staged and rechecked, the fork is retired, CLI flags match run_case.R, and task 24+ uses repeat 1. No automatic P5 retry is introduced. Actual-tree frozen check passes; the 46-case shell suite independently passes, including prior gates, new ordinary frozen-tree controls and primary/repeat CLI dry runs. F6 is outside those tests.

Requested CPU × wall ceilings independently sum to **311.0 core-hours**, for 67 jobs/tasks across 12 steps. Listed expected-cost components sum to **10.45 core-hours**, consistent with “about 10” after rounding. Sources and startup/scaling assumptions are disclosed; this is an estimate from local measurements, not observed NOTS consumption or a production sizing result. Real Slurm, Linux truth permissions, modules/pinned libraries, compiler identity and NOTS timing remain execution gates, as previously reviewed.

## Checks and execution record

* `E/audit.py`, `audit.log`: independent manifest/core/harness/fork hash checks, diff-path coverage, revision-6 file comparison and core-hour arithmetic; changed source diffs saved in E.
* `E/saved_check.R`, `saved_check.log`: all 34 core pairs, six LOWP pairs, CSV/sidecar checks, P5 metadata, forced-stop counts and scoring scan.
* `E/a3_and_snapshots.R`, `a3_and_snapshots.log`: both p500 record comparisons and all four current-primary versus pre-retry snapshot checks.
* `E/edge_checks.R`, `edge_checks.log`: H valid/NULL input controls and preliminary stubbed lock interleaving.
* `E/scan_probes.R`, `scan_probes.log`, `active_lock.tsv`, `orphan_csv.tsv`, `foreign_retry.tsv`: scanner state/identity probes, saved-unit resume and the stronger valid-competing-commit interleaving.
* `E/regression_probes.R`, `regression_probes.log`: independent H/L spec grid and forced-stop false-PASS controls.
* `E/identity.log`: complete downloaded-file acceptance. `d20_controls.log`: 16/16 controls. `d20_selftest.log`: 101/101 assertions.
* `E/shell.log`, `shell/SHELL_TESTS.md`: independently reran `tests/test_shell.sh` without MSYS_NO_PATHCONV; **46/46 pass**.
* `E/negative.log`, `negative/NEGATIVE_TESTS.md`: independently reran the full `tests/run_negative_tests.R` suite with MSYS_NO_PATHCONV=1; **88/88 cases behave as expected, exit 0**. This includes the new CSV/native-status and P5 informational-report controls. The counterexamples in F1–F7 are additional to the shipped suites.
* `E/actual_frozen.log`, `link_probe.py`, `frozen_link.log`: actual tree accepts; unlisted native symlink also incorrectly accepts.

R executable: `C:/Program Files/R/R-4.4.1/bin/Rscript.exe`; Git Bash and `py -3`. R locale-setting startup warnings are retained. Scratch probe setup errors and their corrected reruns are not production failures: an initial source-loader call lacked ofile context; scratch output was initially nested beneath its input root; and the default C locale changed serialization-based policy/allocation hashes. `E/hash_locale.R` confirms the saved allocation hash reproduces under its recorded English_United States.utf8 LC_CTYPE. The final resume/interleaving probe sets that locale and uses untouched saved-file copies; the earlier scratch re-signing attempt is retained in `scan_probes_setup_attempt.log`. All conclusions above refer to the corrected saved outputs.
