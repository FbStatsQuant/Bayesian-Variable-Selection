# R02 ? independent review of summarize.py v3

Reviewed the supplied brief, v3, frozen v2, unified diff, all five supplied data/task fixtures, both frozen production task tables, and DESIGN.md. No network or NOTS access was used. No git commands or source edits were made. Executable checks used script copies and synthetic files in automatically removed temporary directories, with bytecode writing disabled.

The reviewed LF-normalized SHA-256 values match the brief: v3 `ae47e03204741617610b69f992197cd7936d0abf32f192db951dc275539e79ed`; v2 `8011253eec0e1590a89f839c15b2ce5b1292bee526b2c9eb016a131f0b7835be`.

Line references below are to `scripts/summarize.py` unless otherwise identified.

## Findings

1. **MAJOR ? Reused TAG values bypass per-input task-table ownership checks; the new two-pass loader introduces a no-rerun acceptance regression.**

   **Evidence:** Lines 74?87 never require unique tags across `--run` and `--rerun`. Lines 88?99 reconcile records against the global final `sched[k] == tag`, rather than membership in the task table paired with that particular JSONL. Reading every table first makes a record from an earlier input eligible under a different input's table if their tags coincide.

   **Reproduction:** Let `T1` contain the first b2 task (`cs, rho=.5, n=100, p=1000, s0=4, rep=1, wide`), `T2` the second (rep=2), `J1` the first JSON line of `smk1_v3_derived.jsonl` (rep=1), and `E` an empty file. Invoke:

   ```text
   --run shared J1 T2 --run shared E T1
   ```

   Frozen v2 exits 1 with `record not in task table of shared`; v3 exits 0 and reports `2 scheduled tasks, 1 records, 1 without a record`. The record is absent from its paired table. With reruns, the following also produces no reconciliation problems and accepts J1 from the unrelated ordinary-run input:

   ```text
   --run origin E T1 --run release J1 T2 --rerun release E T1
   ```

   Two disjoint rerun tables under a shared tag also accept swapped record inputs. Separately, `--run b2 E b2_tasks.tsv --rerun b2 E T1` succeeds and logs a transfer from b2 to itself, violating the documented new-RUN_ID requirement.

   **Impact:** A misconfigured invocation can silently accept records from the wrong input/run attempt. No-rerun output compatibility holds for the supplied valid inputs, but equivalence of fail-closed behavior does not hold for all inputs.

   **Suggested fix:** Reject any repeated TAG across the entire parsed invocation, before loading tables or records; specifically reject origin/rerun tag equality. If multiple input shards under one TAG must be supported, define that explicitly and retain each input's local table-membership check as well as the global owner check. Add the above regression cases.

2. **MAJOR ? Rerun ownership is checked against the CLI tag, but the record's explicit run provenance is ignored.**

   **Evidence:** The supplied JSONL records contain a `run` field. Lines 92?99 calculate the key and assign `_run = tag` without checking `r["run"]`. The origin-record guard at lines 95?96 only detects an origin record when it appears in an input tuple carrying the origin CLI tag.

   **Reproduction:** Keep the first record of `smk1_v3_derived.jsonl`, but set its `run` to `b2`; call that file `Jold`. Use its matching first b2 task as `T1` and an empty file as `E`:

   ```text
   --run b2 E b2_tasks.tsv --rerun release Jold T1
   ```

   v3 exits 0, reports `240 scheduled tasks, 1 records, 239 without a record`, and logs `b2 -> release: 1`. The accepted record explicitly identifies the origin run, yet `_run` becomes `release`. Thus an accidentally selected/stale derived file can supply the result for a different attempt, while the actual rerun remains missing.

   **Impact:** The claim that a record is accepted only from the run currently owning its key is conditional on trusting every CLI file/tag pairing. The code does not enforce that claim using the provenance already present in the supplied data. Ignoring `run` predates v3; rerun ownership makes the gap directly relevant to this change's contract.

   **Suggested fix:** Before accepting a record, require a present, valid `run` field equal to the associated TAG (or an explicit, validated mapping if these identifiers legitimately differ). Continue to enforce the final owner and origin-record checks. Reject mismatches rather than rewriting their provenance.

3. **MAJOR ? A first release of a never-run b2 key consumes the only rerun slot, preventing the later Slurm retry required by intended use 2.**

   **Evidence:** Lines 85?87 permit exactly one transfer per key, regardless of whether the transfer represents a first execution released from the b2 manifest or a retry of a failed execution. Reproduce with `T1` as above, empty origin/release JSONLs, and a final retry JSONL `J1`:

   ```text
   --run b2 E b2_tasks.tsv --rerun release E T1 --rerun retry J1 T1
   ```

   The loader reports `key rerun twice` and `record not in task table of retry`; `main()` then exits 1 without producing analytical tables. Swapping the two rerun entries still fails; there is no supported attempt chain.

   **Impact and acceptability:** This is fail-closed, not silent mis-counting. It is consistent with a literal limit of one `--rerun` per original key and DESIGN.md:80?81's one-retry policy. However, using the same mechanism for a never-started release consumes that retry before an execution failure occurs. Intended uses 1 and 3 work, and disjoint first releases in use 2 work; its explicitly requested release-then-retry case does not. This does not block summarizing the current supplied data. It requires a fix or an explicit narrowing of the operational plan before analyzing that later case.

   **Suggested fix:** Distinguish initial releases of never-started tasks from actual failure retries, retaining one immutable denominator key and an auditable current owner. Represent attempt ancestry explicitly and allow the documented release-then-single-retry path only when superseded attempts have no records and groups/seeds agree. Update policy documentation if the retry budget changes. Do not silently discard intermediate manifests to make the invocation pass.

4. **MINOR ? The report's ?same seeds? statement is not validated for rerun records (an inherited validation gap).**

   **Evidence:** `tkey()` and `rkey()` at lines 46?53 identify a task by design/rho/n/p/s0/rep/arm, without comparing recorded `data_seed` or `method_seed` to the deterministic formula in DESIGN.md:18?19. Lines 122?128 compare seeds only within available mr1/wide validation pairs. The newly added line 113 nevertheless describes every transfer as ?same seeds?.

   **Reproduction:** Starting with the first supplied smk1_v3 record, set `run="release"` and increment both seed fields by one, leaving its key unchanged. With `--run b2 E b2_tasks.tsv --rerun release Jwrong T1`, v3 exits 0 and counts that record, still reporting ?same seeds?. This key has no mr1 validation partner.

   **Impact:** The tested supplied reruns are not shown to have wrong seeds by this finding. However, key equality alone does not prove that a rerun used the scheduled realization. This gap existed in v2; it is separate from the new two-pass regression and should be treated as validation hardening unless seed provenance is already verified upstream.

   **Suggested fix:** Validate both recorded seeds against the frozen deterministic seed specification, or a frozen per-key expected-seed manifest, for every accepted record. Otherwise state that seed identity is an upstream precondition rather than a loader guarantee.

## Verification and answers to the brief

- **Intended use 1:** Supplied b1 plus smk1_v2 exits 0: **320 scheduled, 299 records, 21 missing**, exactly one transfer. The 40 mr1/wide validation pairs have zero disagreements.
- **Intended uses 2?3:** Supplied empty b2 plus smk1_v3 exits 0: **240 scheduled, 4 records, 236 missing**. All 236 unreleased keys remain owned by b2. An additional disjoint one-key release with no record also reconciles, preserves 240 scheduled/4 records/236 missing, and transfers that key without removing it from the denominator. A second transfer of the same key fails as described in finding 3.
- **Combined supplied data:** **560 scheduled, 303 records, 257 missing**, with five transfers. No denominator loss or duplicate counting was observed on these valid inputs.
- **No-rerun compatibility:** Full report text from v2 and v3 is identical for b1 alone and for b1 plus empty b2. The two-pass change does alter acceptance of invalid reused-tag inputs (finding 1), so an unconditional compatibility claim is false.
- **Order:** Placing a rerun before its origin CLI entry yields identical output in the supplied b2 case. Reversing every supplied task table and JSONL preserves the logical schedule, records, origins, and problem list in the combined case. Distinct-tag records supplied with the wrong task table are rejected in either ordinary-run argument order. Multiple same-key reruns fail in either order. Arbitrary Markdown byte-order invariance is not claimed: existing Counter/dict presentation can depend on record insertion order.
- **Fail-closed checks:** Synthetic unscheduled rerun keys, duplicate ordinary schedule keys, repeated rerun table rows, duplicate records, records in an origin input for a transferred key, and A-to-B group changes all produced reconciliation problems. Lines 106?108 prevent analytical output when problems exist. A B-to-B transfer succeeds and retains group B. Merely treating all problem-free inputs as trustworthy still encounters findings 1?2.
- **Other numeric changes in the diff:** Cell construction, rate/bounds calculations, validation-pair calculations, and outcome statistics are unchanged. For distinct, correctly labelled tags and valid records, the transfer preserves the key set, retains group/cell identity, counts each key once, and excludes origin-input records. The only new successful-output line is rerun provenance; the meaningful changes to which records can be accepted are discussed above. No silent record loss or double-counting was found for the tested valid distinct-tag cases; incorrect acceptance/attribution is reproducible with malformed provenance/tag inputs.

The current fixtures support the core transfer algorithm, but the ownership-validation gaps should be repaired before relying on fail-closed reconciliation, and the release/retry semantics should be settled before that workflow is needed.

R02-VERDICT: ACCEPT-WITH-FIXES
