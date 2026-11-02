# Independent CONF review: regression round 2

Reviewer: Sol 6.1. Review date: 2026-10-28 (session date; some supplied ledger entries are dated 2026-10-29). Paths below are relative to `02_Experiments/I_2026-10-28_New_Campaign` (C).

Scope: the earlier review, the two named current source files, supplied diff and ledger, REGRESSION/PATCHES/OUTPUT_FIELDS, the named regression2 comparator, self-test, reg2 drivers, evidence and saved logs, and the three named NOTS bundle files. No SSH/network, R invocation, compilation, new fits, or numerical experiments. I inspected saved text evidence rather than deserializing/recomparing RDS files. Only this review file was written. Static counterexamples below are source deductions, not newly executed mutation tests.

## Final verdicts

| Deliverable | Verdict | Reason / release condition |
|---|---|---|
| Code v2.2 | **ACCEPT WITH FIXES** | Both requested code fixes are correct; no new statistical side effect was found. Finish the previously requested scored-set export size-limit guard/documentation, and settle the narrowed observer contract explicitly. Production-platform acceptance is still pending. |
| Regression | **ACCEPT WITH FIXES** | Saved logs support the reported matched comparisons and extra checks. The strict numeric comparison is substantially repaired, but two list-comparison holes and the custom provenance shape check still contradict the full comparator claim. Repair, add assertions, and recompare saved outputs. |
| OUTPUT_FIELDS | **ACCEPT WITH FIXES** | Most semantic corrections are complete. Remove the claim that stage plus stage count distinguishes the last bridge event from terminal rounds in pilot/diagnostic phases. |
| PATCHES | **ACCEPT WITH FIXES** | Useful proposals and substantially better qualifications remain. Remove the surviving zero-runtime-cost claim; qualify P5 replay and label historical facts as supplied background. |
| CONF_NOTS_IDENTITY job bundle | **REJECT** | Suitable case selection, but not yet an enforceable acceptance gate: reasons are printed rather than asserted, failure exits successfully, and exempt source/environment provenance is not independently pinned by the acceptance script. Repair before treating an ACCEPT line as release authorization. |

These are review verdicts, not production GO. In particular, acceptance of the two code fixes does not certify literally unchanged wall-clock guard decisions. Historical comparison targets are **v2.1 on NOTS**, as specified in the brief; they should not be treated as an unspecified older algorithm requiring an invented numerical tolerance.

## Status of the original 16 findings

RESOLVED means the original correction is supported within this review's source/saved-text scope. PARTIAL includes a disclosed but unclosed validation or contract requirement; it does not imply an observed sampler regression.

| # | Status | Reason and remaining action |
|---|---|---|
| 1 | **PARTIAL** | REGRESSION now discloses timing-dependent stops and retains unmatched cases; evidence sections 2.1/6 correctly separate common-stop comparisons from identical stopping outcomes. Literal guard invariance is still not achieved or waived by a documented authority in the supplied files. PATCHES:116 and JOB:3 still overstate reproduction. Use the explicitly qualified statistical-observer contract consistently; do not attribute authorization of that contract change to the reviewer. |
| 2 | **PARTIAL** | `leaf_identical()` now checks strict numeric/NA/attribute semantics and double/complex payload bytes; container types are checked. Saved self-test assertions cover signed zero, NaN payloads, and ordinary attribute-order mutations. However, `cmp2_attrs()` deletes the `names` attribute before checking attribute order, hiding movement of that attribute relative to others (N2). |
| 3 | **PARTIAL** | Exact-path allowlists, old-name prefixes, extra checkpoint/near-tie rejection and insertion/order assertions are implemented. An empty **named** baseline list bypasses addition validation because `ny[-seq_along(nx)]` is empty when `nx` has length zero (N2). Fix this corner case and recompare. |
| 4 | **RESOLVED** | `core/v3_fit.R:55-62` appends all old finish fields first, removes/re-appends each present plain field in the specified order, then adds instrumentation. Empty integer MPMs survive because they are not NULL. Saved common-stop/completed comparisons enforce the old-name prefix. |
| 5 | **RESOLVED** | `core/cpp/v3_core.cpp:587-617` holds `registry_keep` in `CalState` before assigning the raw pointer. Member destruction retains owners until after engine/ledger destruction. `reg2_extra.R:123-132` actually passes a temporary registry, forces five full GCs, then runs a calibration tier; its saved log reports PASS. |
| 6 | **PARTIAL** | O(M) unbounded exact storage, retained-p thresholds, export-only suppression, estimated storage and pre-export measurement timing are now documented. The narrowing `int n = (int)keys.size()` remains (`v2_2.diff:37`) with neither an explicit M <= INT_MAX limit nor a guard in the supplied current documentation. Add a checked conversion or document this export limit; p <= 32 does not establish it. |
| 7 | **PARTIAL** | Timing exemptions are now enumerated paths; exact-preflight estimates are exempt only on exact fits; SMC NAs are checked; non-data handling is disclosed in the evidence. Whole environment/code exemptions are now explicit rather than silently minimal. But the custom `record$code` case does not enforce its advertised shape contract (N3), and the NOTS gate needs independent verification of exempt code/environment values (N5). |
| 8 | **PARTIAL** | Manifest checks now fail on missing expected outputs. Saved extra checks cover p32/33/64/65, dropped columns, export suppression, retained-position lookup, old optional signatures, GC lifetime and all nine stop fields. Real escalation, a real escalation-preflight stop, schedule_limit and numerical_failure remain unexercised, explicitly disclosed. Synthetic finish tests are useful but do not exercise tier-1 execution. The proposed successful-escalation NOTS job does not close the other failure gates. |
| 9 | **RESOLVED** | REGRESSION, PATCHES P6 and round-2 evidence consistently label p30 as a size <= 12 reference. `reg2_r3.R:23` computes max scored size for every seed; the saved log reports 12,12,12 with zero larger models. Evidence:176 gives the correct full-coverage formula and labels tail continuation as an extrapolation, not a bound. No full-p30 posterior/HPM certification follows. |
| 10 | **PARTIAL** | OUTPUT_FIELDS:103-112 now lists phase-dependent stage meanings and omitted coordinates. But line 113 says stage plus stage count can distinguish bridge from terminal rounds in pilot/diag. Both the last bridge stage and terminal rounds carry stage T, with subphase overridden; that distinction cannot generally be recovered (N4). |
| 11 | **RESOLVED** | OUTPUT_FIELDS:119-125 now distinguishes ledger events, held states, cache-evicted repeats, table replay, inherited rescoring and calibration V rescoring; union cardinality is explicitly not a fresh-counter sum. |
| 12 | **RESOLVED** | OUTPUT_FIELDS now distinguishes preflight/setup failures and report availability, planned versus executed final stages, checkpoint-derived NAs, allocation sources, component count versus logical flag, and registry-only memory. These address the original availability/type qualifications. |
| 13 | **PARTIAL** | Algorithmic and measured costs, unisolated p500 timing, scored-set-only storage and pre-export time/memory sampling are mostly corrected. PATCHES:75 still says `Cost: none in runtime`, contradicting the same document's O(M log M) export and registry work. Delete/replace that sentence (N6). |
| 14 | **RESOLVED** | The earlier positive production-fit registry/HLL/LSE assessment is retained; the supplied diff shows no change to that logic. OUTPUT_FIELDS:86 states nominal HLL s.e.; line 117 explicitly excludes unseen externally inherited models in a standalone low-level call. This is not new independent execution of the registry or support for arbitrary unchecked low-level metadata. |
| 15 | **RESOLVED** | The plain-PIP definition, original/retained index mapping and adapter additions remain intact in the diff; top-level order is now fixed. Saved adapter logs report the same ordered 88-column CSV schema, 0 non-provenance cell differences, and the appended record fields. |
| 16 | **PARTIAL** | P4's heuristic/report-only restrictions and P6's smoke/readiness limits are much clearer. P5:116 still promises exact reproduction of the stopped run from seed/allocation alone, and P4/P5 historical counts are mostly headed `Facts` without identifying them as supplied, unverified background. Keep the proposals, qualify reproduction and label provenance (N6). |

Status count: **7 RESOLVED, 9 PARTIAL, 0 OPEN**. The partial entries identify concrete remaining work; they must not be summarized as all 16 resolved.

## Comparator and self-test assessment

The core repair is sound for ordinary numeric/data objects encountered in the reported cases: `typeof()` is checked, strict `identical()` options and double/complex byte checks distinguish the original signed-zero/NaN holes, unexpected additions are normally differences, and the complete old name vector must normally remain a prefix. Unnamed event lists cannot grow. Exact preflight decision flags and SMC estimated-time NAs remain compared. No tolerance is substituted for bit comparison.

I inspected `logs/cmp2_selftest.txt`: all **55 assertions** report ok and the final PASS is present. `expect()` calls `stop()` on a missed expectation, so this self-test really fails the process. These are 55 assertions including positive controls, not 55 distinct mutations. The signed-zero and NaN cases are discriminating, and accepted same-payload/changed-time controls are present. Line 40 of the self-test compares an expression to itself and is tautological; replace it with a direct assertion that the two payload byte vectors differ. The surrounding NaN construction checks and detection assertion mean this tautology does not invalidate that test's reported detection.

The self-test does **not** cover N2/N3 below. Consequently I cannot endorse the blanket claim that all ordered attributes and all unauthorized additions/shapes are certified. The reported 0 differences are evidence under the current comparator, not evidence that its remaining blind spots were absent. The remedy is comparator-only repair plus mutations and saved-output recompares; new statistical fits are not needed for that repair.

Saved evidence spot-checks:

- `logs/reg2_r1.txt`: expected manifest 92/92; 28 matched comparisons; 0 differing paths and 0 bad additions; three unmatched single comparisons plus 20/10 unmatched repeated runs disclosed.
- `logs/reg2_r1e.txt`: manifest 8/8; p500 record 199,750 paths and 0 differences; CSV 2 x 88 with only 12 provenance/time cell differences; input content hashes equal; saved baseline source hashes checked against the worker's baseline tree.
- `logs/reg2_extra.txt`: all 100 checks report PASS, including temporary-registry GC, old signatures, boundaries, dropped-column keys, stop fields and synthetic finish triggers. These checks mostly collect booleans rather than aborting on failure; see N7.
- `logs/reg2_r3.txt`: all six smoke fits completed without escalation; p30 max scored sizes 12,12,12; reference labels and relative-coverage calculations agree with the rewritten account.

Integrity checked independently using SHA-256: the two supplied `cmp2.R` copies are byte-identical, hash `e733b3631e31c2c5d04a94a55502d5d2e61a42cd783a9907f9d14489531c469e`. The supplied diff hash is `5d7ce9cd4809a1dcae499637de2c0cba9c241c4b8602ab2bf0d1a82fb517bc04`, matching the ledger. I did not read the unnamed SHA256SUMS manifests or certify every source-tree file against them.

## The two code fixes

**Plain-field order: correct.** The re-append is after old memory/timing/runtime/numerical-route finishing work. It changes only the location of the three new fields, preserves their values, preserves old field order/positions, and places instrumentation last. On paths without plain fields it does nothing. A zero-length `mpm_plain` is re-appended. There is no draw, fit decision or numerical calculation in the new loop. Extra list copying/lifetime work is operational overhead under the declared exceptions.

**Registry ownership: correct.** `RObject registry_keep` uses the same owner-retention pattern as setup/runtime, preventing the external-pointer finalizer from freeing the registry while the state uses its raw pointer. Optional NULL calls leave the observer absent. Holding the owner changes lifetime/memory, intentionally; it does not change registry insert logic, sampler RNG or old output values. The saved forced-GC check directly targets the earlier dangling-pointer scenario. I found no new pre-existing-output side effect in either fix beyond allowed operational measurements.

## New / remaining actionable findings

### N1 — HIGH: the NOTS escalation gate can falsely print ACCEPT and failure has exit status zero

`jobs/CONF_NOTS_IDENTITY/compare_identity.R:10-12` prints `escalated` and reasons but never includes them in `ok`. Instrumentation is an allowed added subtree and its contents are not compared to a v2.1 counterpart. Thus absent or incorrect new reasons can pass all existing comparisons and print ACCEPT. The final line only prints FAIL; an ordinary comparison failure still finishes R successfully. JOB:28 claims stronger acceptance than this code implements.

Fix: assert the two cases' identities, expected successful status/SMC branch, non-escalation for S3 and real escalation for S5, the selected tier(s), `identical(reasons, "E2")` for S5, and no blocked escalation. Assert required new fields and equality of record versus fit instrumentation. Require old trigger evidence to support the expected E2 event. Make any failed criterion end in `stop()` or a nonzero `quit(status=...)`; print ACCEPT only after every criterion passes. Mutation-test missing/wrong/extra reasons, a missing new subtree, wrong escalation state, changed old output and CSV mismatch. Keep local root input validation and explicit missing-file checks.

### N2 — MEDIUM: two remaining list-comparison blind spots

1. **Empty named lists.** `cmp2.R:168` uses negative indexing to take the suffix. If `nx` is `character(0)`, `-seq_along(nx)` is `integer(0)`, so the extracted `extra` is empty even when `ny` is nonempty. For example, the source logic accepts a previously `setNames(list(), character())` container replaced by `list(unexpected = 1)` at an otherwise disallowed list path: the empty prefix succeeds, no extras are checked and no old elements are visited. Use an explicit suffix such as `ny[seq.int(length(nx) + 1L, length(ny))]` inside the existing positive-length-difference branch. Add the empty-named-list mutation at an unallowlisted path and an allowed empty-list control if that case is supported.
2. **Order of the names attribute.** `cmp2_attrs():116` removes `names` before comparing attribute-name order. A nonempty named list with attributes ordered `names, marker` compares equal to the same list ordered `marker, names`. Element names/values and the remaining marker all agree. This contradicts the recursive ordered-attribute claim even though ordinary reordering of marker attributes is detected. Check the full attribute-name vector first; compare the changing names value separately using the prefix/additions rule. Add a mutation that moves only the names attribute around another attribute.

Both defects are comparator holes, not observations of changed saved fit values. Apply repairs to both comparator copies, rerun self-tests and recompare saved pairs before restating the general certification.

### N3 — MEDIUM: custom code provenance does not satisfy the advertised shape-only check

`cmp2.R:124-134` checks only the parent `typeof`/names and, for `files`, membership/set difference. It does not compare parent attributes, file-vector length, multiplicity, order, attributes or per-element shape. Duplicating an existing file name/hash or duplicating the new registry entry leaves the set difference unchanged and can pass. If `files` is a list, an old hash element can change structure without a check. Conversely, `cmp2_run(record, record, "record")` fails for an ordinary record because this branch requires exactly one newly added registry name; only fit self-identity is tested.

Fix: enforce unique expected file names and a deterministic expected name vector (the registry header can be inserted in the source list's established sorted position), compare length and attributes, and shape-check each old/new hash value as an appropriate scalar. Check parent attributes too. Decide whether self-identity is supported; either allow zero new file entries for identity/control use, or explicitly restrict the API to cross-version records and test that contract. Ignoring changing hash **values** for output regression does not require ignoring their structure.

### N4 — MEDIUM: OUTPUT_FIELDS still promises unrecoverable phase information

`OUTPUT_FIELDS.md:113` suggests distinguishing bridge from terminal rounds in a pilot/diag island by pairing `first_stage` with the island's stage count. At stage T the last bridge event and terminal-round events share that coordinate and the overridden phase. There is no stored round/phi/subphase to break that ambiguity.

Fix: say that stages below T identify earlier bridge coordinates, while stage T generally cannot distinguish the final bridge stage, burn-in or measured rounds. Keep this a documentation repair; do not change sampler event handling for this patch.

### N5 — HIGH for release: pin what the production gate's comparator deliberately exempts

JOB specifies the correct production destination, historical units, original allocation, CPU family and named software versions, and requests a source-manifest verification after upload. That is a reasonable plan, but `compare_identity.R` ignores all code hash values and environment values and performs no independent source/version/environment verification. It cannot certify that the historical files really match the intended v2.1 baseline, that the new result came from the frozen current v2.2 tree, or that the production numerical environment was reproduced. Wrong current snapshots or mislabeled/copy-derived outputs can therefore be evaluated under the same exemptions. The historical files themselves were outside this review's allowed reads.

Fix the job handoff and acceptance evidence as follows:

- Pin the two historical **v2.1** record/CSV checksums, case/data hashes, seeds, allocations and baseline source identity. Use the historical records' saved provenance; do not require equality of changing source hashes between versions. Separately verify the expected v2.2 source snapshot and its recorded per-file/aggregate hashes.
- Provide an executable Slurm wrapper or exact submission command with actual module setup, compiler/build flags, R/Rcpp and BLAS/thread settings, CPU constraint, working directory and per-case exit checks. Record session/compiler/CPU details rather than relying on the shape-only comparator to establish them. The shown JOB command uses `--mem-gb`, while the supplied regression evidence shows `--mem_gb`; the runner parser was not an authorized source read, so validate the exact proposed CLI before dispatch rather than assuming compatibility.
- Save scheduler ID/status, start/end times, launch commands, stdout/stderr, build output, code/config checksums, result checksums and acceptance output/exit status. Verify the expected two-case file manifest and checksums before acceptance and preserve this evidence before scratch cleanup. Existing `.done` files alone are not sufficient.
- State conditional identity: same inputs/seed/code definitions and numerical environment, completed execution or the same operations reached, with the enumerated operational/provenance exceptions. JOB:3's RDS `bit for bit` assertion is literally false for timestamps/timings/new fields and too strong as a deterministic proof from seed alone.
- Keep the real escalation-preflight stop, schedule_limit and numerical_failure gates separately pending or supply controlled isolated validation. Two historical completed units cannot establish these failure paths. If historical environment/source identity cannot be established, a controlled same-environment v2.1/v2.2 pair is an appropriate diagnostic follow-up; do not relabel unexplained differences PASS or silently introduce a tolerance.

The expected 272 + 828 seconds makes the proposed 90-minute wall plausible for these two completed units. It does not accommodate the full two sequential 6,300-second per-fit allocations plus compilation/unguarded work; either state that exceeding the shorter outer wall is a failed/incomplete gate, or size the wall to permit that worst case. These are gate preparation requirements, not a request to launch jobs during this review.

### N6 — MEDIUM: surviving PATCHES overclaims and incomplete historical attribution

`PATCHES.md:75` still says `Cost: none in runtime`. Replace with the actual observer/export costs and measured, unisolated timing evidence. Its own table and OUTPUT_FIELDS already provide the necessary qualifications.

`PATCHES.md:116` still says a doubled-allocation rerun reproduces the stopped run exactly from (X,y,seed). Restrict this to the common statistical prefix under the same code, preprocessing, numerical environment and operations reached; exclude timing, memory, provenance and time-dependent termination/partial output. Larger allocation also changes allocation/checkpoint fields, so whole-output identity is not the claim. P4's counts and P5's six-stop history should be labeled supplied historical background, not independently verified facts within this review. The explicit qualification attached only to the truth-scored count at line 105 does not label the other historical counts.

### N7 — LOW: saved comparison drivers report failures without failing the process

Unlike `cmp2_selftest.R`, `reg2_extra.R:180-182` saves/prints failures and returns normally. `reg2_r1.R` summarizes comparisons without asserting zero differences in the matched subset, and `reg2_r1e.R` prints record/CSV failures without a final assertion. This does not erase the inspected passing logs, but these scripts are not reliable unattended gates from exit status alone.

Fix: keep diagnostic output, then fail nonzero on any extra-check failure, any matched comparison failure, non-allowlisted addition, or non-exempt CSV/schema difference. Preserve the intended informational treatment of unmatched wall-clock stop cases. Assert the p500 current source hash check rather than merely printing its boolean. Give the self-test's tautological payload check the small correction described above.

## Required disposition

Accept the two implementation fixes as reviewed. Finish N2/N3 comparator repairs and assertion coverage, then recompare the existing saved fits/records and update the certification text; no new sampler run is needed for that step. Repair the small OUTPUT_FIELDS/PATCHES statements and the export-limit documentation/guard. Replace the NOTS acceptance script and make its source/environment/audit checks concrete before dispatch. A successful repaired NOTS gate would close the production-platform and real successful-escalation evidence gaps for the two selected units, not all untested statuses or universal guard invariance.

## Ten-line summary
01. Code: ACCEPT WITH FIXES; both requested order/lifetime fixes are correct.
02. Original findings: 7 RESOLVED, 9 PARTIAL, 0 OPEN; pending gates remain explicit.
03. Saved logs support 28 matched comparisons plus the p500 record with zero reported differences.
04. Strict numeric leaves are repaired, and all 55 saved self-test assertions pass.
05. Comparator still misses empty-named-list additions and movement of the names attribute.
06. Custom code-provenance shape checking also needs repair and stronger controls.
07. OUTPUT_FIELDS: ACCEPT WITH FIXES; stage T does not identify terminal versus last-bridge events.
08. PATCHES: ACCEPT WITH FIXES; remove zero-cost/exact-replay overclaims and label historical facts.
09. NOTS bundle: REJECT as a release gate until escalation assertions, failure exit and provenance pins exist.
10. Only this review file was written; no R, compilation, new fits, SSH or network was used.
