# Independent Sol review: PROD-L, round 2 (last full round; HQ D53)

**Verdict: REJECT this revision for staging.** The original unsafe unlock, missing-P5 closure reproduction, and automatic-requeue overwrite are repaired. Three remaining **class (i)** findings below concern a lost required P5 retry, an erased reconciliation exception, and an incomplete scientific-status summary. Fix those with regression tests and obtain **one narrow Sol check of I1–I3 only**. The two **class (ii)** recoveries need the exact operating notes below and HQ acceptance; the two **minor** items need fixes/tests without another review round. No third full round is requested.

Reviewer: Sol 6.1, independent review, 2026-10-30 UTC. `B` means `CAMP/jobs/PROD_L`. Read `review/R1_RESPONSE.md`, the binding `R1_FIX_PLAN.md`, `R1_FIX_NOTES.md`, the R1 review, the requested changed scripts, all Slurm wrappers/common code, JOB/DESIGN/CORE_HOURS/env, test sources and saved final/live evidence. Cross-checked D16/D19/D22/D36/D38/D42/D44/D46/D47/D53, D49 in PROGRESS, accepted pilot/reuse contracts, sizing, the frozen SMC CLI/adapter/scanner, enumeration CLI, and transfer-tool contract. No SSH, NOTS connection, network, scientific fit, simulation, or benchmark was run. One local R process only checked the text formatting of an empty table; it did not read data or run scientific code. Only this review is written in the campaign.

Offline evidence root: `<PC_TEMP_PATH>` (abbreviated `W`). It contains the immutable bundle snapshot, initial byte hashes, copied test sources, every reproduction, outputs, suite logs/exit files, and syntax/audit results. The only changes in the copied test sources are the literal `prodl_tests` → `prodl_sol`; operational code under test is unchanged. The three R1 reproduction copies redirect their old work-directory literal to W. No original reproduction or historical result was overwritten.

## Remaining findings and required disposition

### I1 — class (i): the immutable P5 list can omit a later-completed primary, yet closure reports complete

Locations: `make_p5_list.sh:70` and `:84`; `make_manifests.sh:67`, `:74`, `:84`; `submit_prodl.sh:14`; `reconcile_prodl.py:94` and `:234`.

The initial list contains only eligible rows present in that scan. The frozen scanner intentionally visits valid committed primaries, not missing ones (`CAMP/code/core/v2_2_1/tools/p5_scan.R:67`). List creation does not prove that every expected primary/repeat has been inspected, and the driver still permits ordinary `rN` waves after that list is sealed. Reconciliation trusts the old expected set. An empty set makes closure require only the old `scan_initial.ok`; the nonempty branch likewise checks that every *listed* retry is done, without rejecting newly eligible units outside the list. Its freshness check compares final scan ID only with P5-wave IDs, not later primary/repeat waves.

**Inspected reproduction:** `W/repro_r2_late_complete_scan.sh` and `.out`, fixture under `W/late_scan_with_nonempty_tables/`. Both initial scan tables contain a valid completed unit; a second primary is missing and therefore absent from that scan. List creation writes zero expected P5 units. A later recorded `r1` job commits the missing primary with native `resource_limit`. A newer successful final scan explicitly reports `retry_state=none`, `eligible=TRUE`, `launchable=TRUE`. Nevertheless reconciliation exits **0**, SMC closure exits **0**, and `smc.CLOSED` says `incomplete_units=0 allow_incomplete=0`. No P5 unit exists in the expected inventory. Closure then prevents the required retry from being submitted. This is a lost scientific fit, not a safe halt. The fixture's result bytes and scanner tables are synthetic; it exercises the real bundle control flow without R. The earlier reduced late-primary fixture in `repro_r2.sh` independently gives the same failing gate outcomes.

**Concrete fix:** bind the initial scan/expected inventory to a complete, immutable set of primary/repeat outputs (or explicitly recorded HQ exceptions). Refuse primary/repeat fitting waves after that snapshot unless an explicit versioned recovery reopens the P5 inventory while preserving consumed attempts and prior receipts. At closure validate the complete current scanner population, including *zero*-expected runs: no newly eligible/unaccounted unit, unsafe retry state, or later primary/P5 mutation may be hidden by the old list. A final scan must follow every relevant fitting wave. Preserve the initial receipt/scan hashes and check their binding. Do not weaken or edit the frozen scanner.

**Required tests / narrow check:** the reproduced empty-initial → later resource-limit primary → final-eligible path must refuse closure and remain nonzero in reconciliation; repeat it with a nonempty initial list plus an additional later eligible unit. Cover late ordinary `rN` submission and the zero-eligible unchanged control. Retain the existing interrupted/never-started P5 tests.

### I2 — class (i): per-piece closure converts an unresolved unexpected output into a clean final inventory

Locations: `make_manifests.sh:53` and `:55`; `reconcile_prodl.py:117`, `:122`, `:208` and `:234`.

Accepting reconcile exit 1 is necessary when other pieces are unfinished. But the close gate then checks only the selected piece's expected-unit outcomes. It ignores the selected piece's unexpected-folder/exception verdict. CLOSED saves only expected rows, and subsequent reconciliation skips that piece's scratch scan, without restoring its unresolved exceptions. Consequently an extra scientific output can be archived with no acknowledged exception and disappear from the final report.

**Inspected reproduction:** the first fixture in `W/repro_r2.sh` starts with four valid units (one per piece), a zero-eligible P5 inventory, and reconcile exit 0. Adding `enum20/p0020/UNEXPECTED_UNIT/EXACT.rds` makes reconcile exit **1**. `make_manifests.sh --piece enum20` still exits **0** without `--allow-incomplete`; its manifest includes the extra file. After moving that CLOSED folder to the simulated download tree, reconciliation exits **0** and reports no unexpected folder. All four pieces can subsequently close and remain a clean pass. Saved reports/manifests are under `W/r2_repros/`.

**Concrete fix:** expose machine-readable exceptions/unexpected outputs *per piece* from reconciliation. Normal closure must reject any such unresolved item for the selected piece, independently of unfinished unrelated pieces. If HQ explicitly accepts an exception, archive its full identity/reason in a hash-bound closing snapshot and carry it into later inventories; never turn an acknowledged exception into an unqualified clean pass. Preserve valid scientific failures as operationally `done`.

**Required tests / narrow check:** unexpected scientific output with every expected unit done must block ordinary closure; an unfinished unrelated piece must still permit a clean selected piece to close. Exercise close → simulated pull/delete → later reconciliation, including explicitly acknowledged exception preservation. The standalone strict validator and its malformed-file negative controls already work; keep them.

### I3 — class (i): CLOSED pieces lose their scientific-status counts in the final report

Locations: `reconcile_prodl.py:118`, `:122`, `:137` and `:228`.

The CLOSED branch rebuilds operational outcome counts, but not `native`. All native-status counting occurs in the live CSV branch, which CLOSED pieces skip. Thus the final `INVENTORY.md` scientific-status table describes only pieces still on scratch. Once both SMC pieces close it is empty, even though the saved unit details retain the statuses. This does not delete the fits, but it does produce an incomplete scientific-status record, so D53's “wrong record” route is class (i).

**Inspected reproduction:** `W/r2_repros/inv_baseline/INVENTORY.md` contains `smc | completed | 1` and `smcrep | completed | 1`. After real per-piece closure and simulated pulls, `inv_all_closed/INVENTORY.md` has the same heading/header and **no status rows**, with reconciliation exit 0. See `NATIVE_BEFORE` / `NATIVE_AFTER` in `W/repro_r2.out`.

**Concrete fix:** persist hash-bound structured native-status summaries at closing, or reconstruct them from validated saved unit details; aggregate closed and live pieces together. Preserve unit counting (not two CSV-rule rows per unit), and do not silently lose `resource_limit`/failure categories.

**Required test / narrow check:** scientific-status counts and operational unit coverage must be invariant across closing/pulling one piece and then all pieces. Include a valid committed scientific failure, multiple native categories, and a nonempty P5 inventory. No refit is needed.

### II1 — class (ii): a failed initial scan has no documented consumable recovery phase

Locations: `make_p5_list.sh:4`, `:56` and `:63`; `JOB.md:43` and `:117`.

Fresh scan phases work, but only `--from-scan initial` is accepted for inventory creation. After an initial failure, a successful `r1` phase cannot be consumed (`--from-scan r1` exits 2), while the initial path still refuses its missing ok marker. The current note to repeat under a fresh phase stops short of the required promotion. This halts safely: no fit or retry is silently launched.

Evidence: `W/repro_r2_ops.out` records the two refusals (2 for the successful recovery phase's name; 1, “missing initial scan receipt”, for initial). The positive new-phase scan behavior is also covered by SC07/SC08.

**Exact manual-resolution text for JOB.md §14** (a supported `--from-scan <phase>` enhancement can replace this procedure later):

> Failed **initial** P5 scan, before any expected inventory exists: after all run jobs are terminal and truth is verified open, submit `bash "$B/submit_prodl.sh" --p5-scan --phase r1 --profile withH` (use the next unused rN phase). Wait for its successful completion and both tables plus `scan_r1.ok`. A fresh phase alone does not replace initial. Only if BOTH `RUN_HOME/p5/expected.tsv` and `RUN_HOME/p5/scan_initial.receipt` are absent, HQ may promote that successful scan as the initial snapshot. Preserve the failed initial tables, marker if present, and launch/job-ID evidence in a new scratch incident directory; copy `scan_r1_smc.tsv` and `scan_r1_smcrep.tsv` to `scan_initial_smc.tsv` and `scan_initial_smcrep.tsv`, verify each copy with `cmp`, then copy `scan_r1.ok` to `scan_initial.ok` LAST. In the incident record name the source phase and recorded job ID, record the promotion UTC time, and save SHA-256 values of source and promoted files. Then run `bash "$B/make_p5_list.sh" "$STAMP" --from-scan initial`, inspect its inventory/receipt, and continue with `--wave p5`. If either home inventory/receipt already exists, stop for HQ's versioned recovery; never overwrite it, erase a P5 attempt, or relaunch an attempted unit. All primary/repeat reconciliation and snapshot-binding requirements still apply.

This promotion is a documented operator action on scratch scan evidence, not permission to mark a failed scan successful or change a scientific output.

### II2 — class (ii): truth recovery does not recreate the receipt required to resume the workflow

Locations: `recover_truth.sh:30`–`:35`; `JOB.md:35` and `:116`; `slurm/s9_collect.sbatch:23`.

Recovery properly requires terminal scheduler evidence and reopens/verifies the trees. It writes its result to stdout and creates no `WAVE_UNLOCK_VERIFIED` receipt. JOB §5 nevertheless requires that receipt before proceeding, and the collector correctly refuses without it. The existing §14 instruction to recover and hash-check does not state how to obtain the missing wave receipt. This is a safe operational halt, not an unlock bypass.

**Exact manual-resolution text for JOB.md §14:**

> If the scheduled unlock never produced `WAVE_UNLOCK_VERIFIED`, first wait for complete terminal accounting, run `bash "$B/recover_truth.sh" "$STAMP"` and retain its stdout/stderr. Require exit 0. Set `WAVE` to that failed wave and use the confirmed LOWP R module/library environment. Ensure `LOG_RUN/truthlock/$WAVE` exists. Run `env RSCRIPT=Rscript bash "$B/truth_wave.sh" unlock "$RUN_HOME/study" "$RUN_HOME/code/lowp/R" "$LOG_RUN/truthlock/$WAVE/WAVE_UNLOCK.txt" "$LOG_RUN/truthlock/$WAVE/evidence"` and retain its output/exit status. This verifies 755/444, counts and the wave's pre-lock hashes; when both pre-lock lists are absent it uses the B2 staged-truth verification. Require exit 0 and the newly appended `WAVE_UNLOCK_VERIFIED` with equal/staged-equal hashes before guard, reconciliation, cleanup of stale files, or another wave. A missing single pre-lock list or hash mismatch remains STOP for HQ. Never create the verified marker by hand. Preserve the failed scheduled-unlock evidence and report the recovery to HQ.

### M1 — minor: retune admission omits the still-live plain enum20 job

Locations: `retune_throttle.sh:33`–`:43`; `tests/test_retune.sh:37`–`:45`.

The plan includes only arrays, but `--own-ids` excludes *every* recorded job from the “others” calculation. Main enum20 is a plain four-CPU job, so its contribution disappears during retune. The regression fixture contains that job but does not test the distinguishing boundary.

**Inspected reproduction:** `W/repro_r2_ops.sh` raises live enum30/SMC arrays to alone while enum20 is RUNNING and other work bills 64 CPUs. It admits and applies the updates, writes a CONFIRMED record, and returns 0 using `prod_l_peak=128 combined=192`. The actual admitted potential is 4 + 64 + 64 + 64 = **196**. This is a resource/fair-share policy defect; under HQ D50 it is **minor**, not a scientific correctness blocker and not class (ii) (it does not halt).

**Concrete fix/test:** include all still-live non-array own allocations in the retune plan while updating only arrays. Keep the SMC/repeat serialization and withH drain requirement. Test 60 other billed CPUs admitted and 62/64 refused with live enum20; verify the record's plan/combined numbers include it. The current positive record does retain before/after queue, admission and applied updates, and pending-throttle mismatch correctly returns nonzero.

### M2 — minor: the reuse/design/test audit text still describes removed behavior

Locations: `REUSE.md:19` (claims invalid-job-ID tolerance is kept); `REUSE.md:8` and `:25` (omit new guards); `DESIGN.md:82`, `:85` and `:87` (old unrestricted checksum/stale patterns); `tests/TESTS.md:173` (now-tested wrappers still listed as untested).

**Concrete fix/test:** refresh these statements for the implemented fail-closed queue/accounting proof, restart/noclobber guard, shared strict verifier, `*.tmp*` stale definition, and actual expanded suites. Add a small documentation-consistency check to the existing static documentation suite for the obsolete unlock-tolerance claim and current recovery commands. Preserve historical build notes and R1 snapshots. This is documentation drift; the executable checks are assessed separately above.

## R1 finding-by-finding disposition

The D53 labels below describe each issue's route; “RESOLVED” means no remaining defect from that stated mechanism. The narrower residuals/new integration failures are identified explicitly.

| R1 | D53 label | Disposition and inspected evidence |
|---|---|---|
| F1 unlock/recovery fail open | class (i) | **RESOLVED.** Full-user queue query, parse checks, all-wave fitting IDs and terminal-accounting coverage now fail closed. Original mixed-query repro: exit 1, unlock not called. UN60–67 / S8-01–14 cover old active waves, missing IDs, errors and terminal controls; B2 checks retained. |
| F2 missing P5 phase/outcomes/closure | class (i) | **PARTIALLY RESOLVED.** Original missing-P5 closure now exits 6 and reconcile exits 1. Expected inventory, P5 states, attempt exceptions, fresh scans and p5rN lists are implemented. Nonempty P5 closed-piece flow works. **I1** remains; failed-initial-phase operation also needs **II1**. |
| F3 requeue overwrites attempts | class (i) | **RESOLVED for the reported mechanism.** Every driver vector has `--no-requeue`; restart guards run before initialization/ledger writes; same-ID starts and inventories refuse clobber. Original restart repro: second exit 71, one start, byte-identical original end. RQ and driver controls also cover restart 0/1/2 and same-ID refusal. |
| F4 collector guard after failed unlock | class (ii) | **RESOLVED.** Receipt plus both 755 trees precede guard. Original collector repro: nonzero, guard not called; accounting kept. CO controls cover missing/failed/cancelled/locked and verified controls. Receipt recovery documentation is the separate **II2**. |
| F5 real enumeration temp names | class (ii) | **RESOLVED.** Shared stale helper is used by cleanup/resubmit/closure. Original `EXACT.rds.tmp4242` is moved, exit 0, no residue; hidden temporary, sidecar temporary, `.lock` and adapter names covered. |
| F6 unrestricted output verification | class (i) | **PARTIALLY RESOLVED.** The original unrelated-payload verifier now returns `(False, 'wrong checksum file set')`. Exact sets, marker/CSV shape, scientific-failure retention and standalone unexpected-folder nonzero work. **I2** remains in the closure/closed-inventory integration. |
| F7 CLOSED pieces forgotten after pull | class (i) | **PARTIALLY RESOLVED.** Hash-bound saved rows preserve units after actual close/move, including nonempty P5 snapshots; tampered saved inventories fail. **I3** remains for native summaries. The old R1 post-pull script no longer tests a CLOSED piece, because its preceding unsafe closure is now refused; new valid-closure controls replace that inference. |
| F8 literal OPS sequence | class (ii) | **PARTIALLY RESOLVED.** Absolute transfer paths, home-folder pulls without deletion, four lists before one round submission, and waiter 0/4 completion semantics are fixed. The static suite checks these, but does not execute a remote transfer. **II1–II2** need exact recovery notes. |
| F9 retune admission/drain | minor | **PARTIALLY RESOLVED.** Fresh ceiling check, one applied-update record, confirmation and 68-CPU drain check exist; raising with excessive other work refuses in tested cases. **M1** remains at the plain-job boundary. D50 makes this policy defect minor. |
| F10 waiter partial accounting | class (ii) | **RESOLVED.** Missing/malformed ID coverage remains UNKNOWN; default failure triage remains exit 3. `--until-terminal` waits through failures, exits 4 only with complete terminal evidence, 0 for all completed. WT40 is inverted and UT controls pass. |
| F11 reconcile diagnostics in home | minor | **RESOLVED.** Diagnostics are under scratch `LOG_RUN/reconcile`; home holds small inventories/markers. They precede logs-manifest creation. |
| F12 P5 cost wording | minor | **RESOLVED.** Both documents distinguish 16 nominal, 29,160 s/16.2 wrapper and 18 requested-wall core-hours. |
| F13 script-time production fallback | class (i) | **RESOLVED.** Numeric scheduler environment then parsed `squeue %e`; no-source production defers every unit and exits 1, local fallback is explicitly limited. Starts/deferred records carry end source/epoch; near-end and malformed/missing-source controls cover the admission branch. |

## Validation evidence and limits

- **Independent full-suite rerun: 14 suites, 1,333 passed, 0 failed; all suite exit statuses 0.** Inspected `W/suite/SUMMARY.txt`, every suite log and `.rc`. Counts match the supplied `tests/SUMMARY_r2_final.txt`. The existing checks do not cover the failing cross-phase/closure scenarios I1–I3; the separate reproductions expose those gaps. No test/source edit occurred during this rerun.

- **54 syntax/compatibility checks passed**: shell `bash -n`; Python `py_compile` with generated bytecode directed into W; Python 3.9 grammar parsing. Local Python is 3.13, so this is not a claim that the suite ran under Python 3.9/RHEL. See `W/syntax_checks.txt`.
- Re-ran copied `repro_r1.sh`, `repro_restart_r1.sh`, and `audit_r1.py` against this revision. See `repro_r1.out`, `repro_restart_r1.out`, `audit.txt`. Their scripts deliberately print outcomes rather than assert every modern contract, so the interpretation above matters.
- Independent fixtures: `repro_r2.sh` / `.out` establish I1–I3 and exercise actual closure of all four reduced pieces, then simulated pulls and final reconciliation; `repro_r2_late_complete_scan.sh` / `.out` also establishes I1 with populated initial tables. `repro_r2_ops.sh` / `.out` establish M1 and II1's refusals. `repro_r2_closed_p5.sh` / `.out` provides the **nonempty P5 positive control**: two base pieces close/move in sequence, P5 saved rows remain done, final accounting and logs closure pass, downloaded manifests verify, cleanup returns 0 with `CLEANUP VERIFIED` and an outside-tree receipt. This latter small fixture synthesizes empty CLOSED enum inventories to meet logs' four-piece prerequisite; it does not claim to have run production enum closure there (the four-piece zero-P5 fixture tests that separately). All artifacts and home summaries needed to inspect these controls are retained under W.
- Excluded false lead: `repro_r2_late_scan.sh` supplies a literal quoted-empty header and safely refuses it. A read-only R 4.4.1 formatting probe of the scanner's exact empty `write.table` call showed that its real output is a **blank** header, which the parser already accepts. The quoted variant is not a finding against the frozen scanner. See `W/empty_table_format_probe.txt`; only one R process was used, solely for this formatting check. I1 is independently reproduced with both initial tables populated, so it does not depend on empty-table formatting.
- Read the retained real-CLI integration `tests/live/live.sh` and `live_r1fix.out`; **did not rerun it**. Its four units complete, a new-job-ID resume skips, and a repeated same ID refuses while preserving the ledger/inventory. It uses a Windows GNU-time shim (CPU/RSS placeholders), no real Slurm or Linux permission enforcement, and no real P5 fit. It does not establish performance, NFS cleanup, or current cluster state.
- The frozen manifest is **`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`**, all **27** listed files match. Reused `frozen_check.sh`, `guard_check.sh`, `truth_lib.sh`, `truth_wave.sh` and `R/pilot_build.R` still match the accepted pilot after LF normalization. No change to the frozen tree or scientific allocation is requested.
- The deterministic list generator still checks 600 enum20, 600 enum30, 2,400 primary SMC and 12,000 repeats, with correct grouping and all five additional seeds. Commands retain explicit enum core/thread settings and frozen SMC allocation 2 GiB/4 h; P5 passes the primary allocation plus `--p5-retry`, so the frozen adapter supplies the doubled allocation and same seed. Benchmark entry remains gated. Expanded repeat cost arithmetic still ties out. These are source/saved-evidence checks, not new production measurements.

Under D53, the manager should repair **I1–I3**, attach their targeted regressions and request a **narrow** Sol verification of those three fixes only. HQ can accept **II1–II2** once their operating notes are included. Fix/test **M1–M2** without another round. This revision is not yet “PROD_L READY for OPS.”

## Reference and evidence SHA-256 anchors

```text
727d30fe968b7031ce40cf511a22f4cb00fd85d4201a02a225e6bf8328adcec8  CAMP/DECISIONS.md
d583eeebccbc388b5278ff85cb1eb5a79fe927408a69d82fb4f19616a12f8928  CAMP/CHARTER.md
9bb0da4fe4c2d38d0568526b876c742457057114eae729149643453d25c279b5  CAMP/ops/PROD_L_SIZING_20261030.md
f1dc1365084c1f24be261b537a651a395f9c71ff3694127cd7e7c5207f401ead  CAMP/ops/review/SOL_REVIEW_PILOT_20261030T0712Z.md
d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1  CAMP/code/core/v2_2_1.SHA256SUMS
241815a512a90fbcd4a8684a5f317547d85e60e3d94e1cdb3d3bd6f9f5d5442c  CAMP/code/core/v2_2_1/study/run_case.R
a398c11221f8745efda2583eca211f09d43236c56569022656e3b9984f701518  CAMP/code/core/v2_2_1/study/adapter.R
0580336bedfda60d0f4b2bc32614948999336f40ce9ebb464a45879c6f14fa8e  CAMP/code/core/v2_2_1/tools/p5_scan.R
1490643ed17d113921a4c95bed883dbf849408df13cc67f54c693d9bc4730cf1  CAMP/code/lowp/enum/run_enum_dataset.R
9c49594727b9c6cc00d31c4efa283dba9218f5ce81395cae857769a7a494606b  CAMP/code/lowp/R/lowp_verify_nots.R
f46fe38edcc35b8d0c266a19daf44c6fa8ee1c9e1e6766163c76806e04ae8827  CAMP/ops/transfer/nots_pull.py
ae1aacc23c1ff7c9cea7b9c0016872e805f415c1a839163abe2a9665c9ebbf72  CAMP/code/lowp/pilot/frozen_check.sh
3625033365a168dd4e255f4a74453a46378aaf5bfcdcb160ef614923d9232384  CAMP/code/lowp/pilot/guard_check.sh
a4b4ddcd5b8b680cda3c8b30738949cab46a6baaba267e3dccb9acdd6c2436ae  CAMP/code/lowp/pilot/truth_lib.sh
0fd6b1c80dcefca4b6ab37f1a9b4242cb4ebe46d2102ab3945a42a692ea24e5d  CAMP/code/lowp/pilot/truth_wave.sh
6363e3466bb038a86564ea8093999d99418338a2b6d71ae0d269e5a8490ff02b  CAMP/code/lowp/pilot/R/pilot_build.R
a2c2316a755c4b60409e7f0caef5d9fc0f1250365bc8343141b56c8eb2207a06  CAMP/code/lowp/pilot/slurm/common.sh
11f936c7394fc435925c86b557b741293b0d3dec4d6516acec2b38e900946a6d  W/repro_r1.sh
36ac898b6a59b674551668eed5b6005ba88a7e9c3ad486604a88bfed0dcf963e  W/repro_r1.out
e65b0faaf7e6b39a4ddd53f6b803d0f9146c7db5c95301ac16ca55fa22c5b437  W/repro_restart_r1.sh
12dde36cc683fa07fbd7bce8b35f3f7c4224260e89a1e5b8185c0e0fb0464040  W/repro_restart_r1.out
bedf51463cf5ef3be9791d25058377ed66ce75ddcd2a1addf61f0f5a92fa9164  W/audit_r1.py
8ae4bf9c2ebee31e2184ca3b0def043981ae82d47a9570dd224b9252bea2289f  W/audit.txt
ee890b9c0a6a7165db651a7ce88c8c9c08bbc1136de91f167b97ae66cd379a17  W/repro_r2.sh
c396650f59a96292392c7fa4843314b58551e3de36a08649530c67a528908d9d  W/repro_r2.out
5329cdfd1d40531775f8344c3b63f1062baae6e003552b53b787db2e219b02d0  W/repro_r2_late_complete_scan.sh
96bd73d0baf3c4ad645d3f8d9c6eddf14a6eab01f4f50a9b1edea79347d50462  W/repro_r2_late_complete_scan.out
d77bda20456ae5ec2eea6d60ae27ba420e15af71586be73f71c0f8cbc914eb9a  W/repro_r2_late_scan.sh
f345b8df3e8e716fc709b0b8ff41dc22eae2e66d68aa3b9c1d986804a000ac42  W/repro_r2_late_scan.out
200e5da07a472dea998d0225366371bbf01d12d0658e457944f2c0f54fc3f3fe  W/empty_table_format_probe.txt
a7146a9422c918dc7983a6cf9dfa2a30b6bf1f3c06a5ccfa49f03ee2a34ea7e4  W/repro_r2_ops.sh
eb233ea7b96864484f1500339d4a7f41aaa27d93ef6443d3f0ae0a4fb75e80a3  W/repro_r2_ops.out
6e7f4edc708cd9d89ea279a16c288051a5abe8b8cf3f26126cef77c7814eab9a  W/repro_r2_closed_p5.sh
a2c821464c68b0b6e82502dc52795a5810cbfda10890dbddadec60bf2f3661a8  W/repro_r2_closed_p5.out
33baa3409d846e3569497209d5bf4dbf8313dc8d402dc0bc734c4b9dee37da55  W/syntax_checks.txt
493a8ea8c9ece1449709a73f1e08e5e5b7320a22c5f39ecd10458310fa4e5a11  W/snapshot_audit.json
94898506b72bb8761279d17a56289300416666327bdd010e5413fd68a758b653  W/suite/SUMMARY.txt
d9ae6545259b04a10629cd406cfe0a463dc29de8bbed20fbb6c633e7a24cf1c4  W/suite_inspection.txt
7286918bddd892d676a370ce9d2a4fd1a3fbafe32c6bc5e678c8b6f569356812  W/final_environment.json
```

## Bundle SHA-256 appendix

Byte-level SHA-256 values from the pre-test snapshot, checked again against the campaign at review finalization. This intentionally inventories every non-cache file in that bundle snapshot, including historical evidence in addition to the files examined in depth, so every reviewed bundle file is covered. Paths are relative to B. Generated `__pycache__` files and this new review itself are excluded; the latter cannot include its own hash.

```text
abb1fc008565d1065ac3791efd505875b17334336970bcf90bc9b360ddffa828  BUILD_NOTES.md
9bdc199041cc2ad479d31c1bb8024c57ecc74b25058e28d6cf1e5a338e530b08  BUILD_NOTES_A.md
ae777dcf597e0a52c265fc10d2276fb961e06daad486684f954b0e411981891a  BUILD_NOTES_B.md
fd769bc89bbb79467122e149cecbd6ae2e800b5e2e60fe8abd65c396d2372c31  BUILD_NOTES_C.md
c94a22df3bd3997cf453a82151b9b8925f52e6ec351cdae67708bc493ad8b156  CORE_HOURS.md
bd1df47218bcb7f4528c266b1abb4f4c3ccb24f4f286c697d64746c1735c6211  DESIGN.md
a7a0d2ed6f2109729471ad582bc4e08ce7ba188e6ab971364c1c0ad1386a94d0  JOB.md
d61fb256bc2ff0e252ffe0406dea67d7e148aed7c4371e0bd728825777d3e7b0  PROGRESS.md
6363e3466bb038a86564ea8093999d99418338a2b6d71ae0d269e5a8490ff02b  R/pilot_build.R
d7bf0d48dd345a58c70baa9c3574aa968102fe640ba7296f962a134e73ece1f3  R/prodl_inputs_check.R
a1e85423b18af699aa7ad1891bc9b9d1ca205b88d4b284d79f8ec7913b7d6fd8  REUSE.md
0d92991e94e30c9dcb4b50425f84050adb3904cd78a59bb234321e402bb50982  batch_runner.sh
150dd20ba6e1e3160da3ed9a20cc8e70cdabf87dbdd69142c2cfd54b259329d4  bench_hook/README.md
d89febae16b27714cd6bd097a4b6407bc4bc4bfdce0fc178790235724514d001  ceiling_check.py
5400e033c99889bdc1d532ad999e3852c40a2a2113347c3aaeb4b53cd0c77661  cleanup_prodl.sh
b3a1f90b2061ac93f9b06540086da843700ff9570e982adbf128a5c0b1618fce  clear_stale.sh
f34c53c72d2d2421eb7f48dfa30d01a2bb56c35aa98f42c4310475de8ddd0d51  final_accounting.sh
f29dc13185aad63d5e0fe1bc8ab8022cd942cbeb7d9d29f43e42f9d7ffac51d5  fixtures/empty.receipt
be41889ec09802b4eea3dd4643ca75a0649fe62c529c46807d0d5ce5c1586278  fixtures/plan_alone.tsv
ab941f22e9430d4407b801280f63cfc07fc7dbb1a594b81f77a1c0343abf4e02  fixtures/prodh.receipt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  fixtures/squeue_empty.txt
953d792ff3eb150dfb736dcd94530c1ebcbf9c68dff073e15d83d28bc28fa7ca  fixtures/squeue_prodh.txt
ae1aacc23c1ff7c9cea7b9c0016872e805f415c1a839163abe2a9665c9ebbf72  frozen_check.sh
3625033365a168dd4e255f4a74453a46378aaf5bfcdcb160ef614923d9232384  guard_check.sh
df21f1d702abae64fa5510f1a6997dd45cd607694886b3e4e7e2fc54f33581be  lists/units.tsv
0fd3bb67aea8cdf77f7761afca05c85a622a1014362a0d340c06f1506cf0471c  make_manifests.sh
a5e2b105441eb9a8d3e7eb3b90ab71a08284eb08b2917656415359fa7bc1b418  make_p5_list.sh
0436f719a3c65dd1358a501f3d28b89c294c0581fadc236cfd0551db25f418b3  make_resubmit.sh
c2d735bfc7d106f52613e78200906c437d5df83f4f6f93b37d5b5114c131855a  prodl.env
73079e42dc8d914b3c112822512b1aa368b240f6df1f0b7816c04f2a4ef5ce55  prodl_verify.py
9388f5b89af9d44356e42155c324e75fe446e51a2db8f9aa0fba4ecff6be9650  reconcile_prodl.py
c026d4dfddf88e1aaea8fdd4bf98db61cd7a019bf8a8099abf4b3a790b45e772  recover_truth.sh
1bebaf8490432e79768208d687651193410e96f56dea797c175569d7b06204da  retune_throttle.sh
0d1151a2e3f570dfaf5c044b1333e84b1d8a5865f994cb0c2adee2d038a36a95  review/R1_FIX_NOTES.md
ebe109a3e8a4ce0585eee420054148ed9fd4720c7373c07addcab5d3c053b6d3  review/R1_FIX_PLAN.md
952869a5feae7db4245417a6695c8fc4d05e0ca8883fab1df9187856802a0235  review/R1_RESPONSE.md
91e14e58978290863f41ded849cd1da07fba8d87617c67f1d75f22cfd03b4f5a  review/SOL_REVIEW_PRODL_R1.md
d3cacab7428f23328448a91b067a619338af443e0e01cd8bc2a490420bfdbf32  slurm/common.sh
4810abea2c3121d20301d15cd8e57a7496e7255a0e5ff25f6cbb6f488dccf582  slurm/s0_build.sbatch
b7afea638bfdd0992e82ac3052b6d9df1c486a19cf86a013cce21b7ff70a79f4  slurm/s0_lock.sbatch
d892b7baaa8d125ca464d8e9ec091f0d311e62b046a8688ad7f4f085a6d9c4d9  slurm/s0_truthlock.sbatch
0220a5624e9d94e935c529cfb7a18dd2c2ce3cc13bdcfff48c8a383fabaa492f  slurm/s0_verify.sbatch
87bd4eb0144e30a822d289e64b6f10f8ea04c1dc0150406eb115cea9bbfac39d  slurm/s1_enum20.sbatch
20072a45ddcc9eb84ab6a66c6c2108c91b0f5d9487039063ff46bab4457dac84  slurm/s1_enum30.sbatch
55f2b69b30eefbf6fadb5410bc541ea4dbaab64270fb4364bf7aaae43a56cdf6  slurm/s2_smc.sbatch
4a5f828a73ba55fff4d5da0dd3be6a5b4c8b89fadd4e851f7ce1c9d1c5bfe51e  slurm/s3_smcrep.sbatch
024e4e9329f0dd6f4b9838f1f79ec7bc95e1eb89629a72f85bacc41eb8739f95  slurm/s4_p5.sbatch
03955153056c160b494d0f436251be0f6ba70b8d2e0df88200753deb3bc8e4e3  slurm/s5_p5scan.sbatch
69949e417128c5e4c7f6f37d4d907852c0a59833942227fb5906e259a6560090  slurm/s8_unlock.sbatch
8d26b2b2c6c68954087de86f55bfa12828456ccea0527ffb196baf43171a348a  slurm/s9_collect.sbatch
167b2906dc98396e8c2c2d345793c46e5f98975dc82c0d2754a4236cfc731316  stage_local.sh
187a61a4775bdcf68eb8523b99751b43e281b4f1b2d20fd777ea89a9afc67958  stale_lib.sh
5152ff76348e0844e2ad3b932c7bacec7b0a34d988d63f5dee9e774ae0292974  submit_prodl.sh
94898506b72bb8761279d17a56289300416666327bdd010e5413fd68a758b653  tests/SUMMARY_r2_final.txt
45e97aece1f82248938588dd57113a265bb7fa6a861cd7a182aa391f287ce93b  tests/SUMMARY_run4.txt
eac5cf75114418d230b617b8ebf9e49fd034e7aa466db1d3718fe0c144967d4e  tests/TESTS.md
5adff612095ebc95f1097745be88dcb21b7def8ead6b406d299993a51b177cd6  tests/lib.sh
f2deab792ed7d744ecf2781a2ca13192f8094382b2db1df88b725c19d7f8b796  tests/live/gnutime_shim.sh
da530ccecd11abdb84d35bbabf297896485188ad200782eadffe0faf661c8653  tests/live/live.sh
4c29a6dc50e4e603cfea347f52571bc3d49bd09d78ed8356e799a67b8a694e45  tests/live/live_20261030T0956Z.out
2733047c7166bd3f4308b70b383a3a17a92d379523262928b2d69bb56bb71c11  tests/live/live_r1fix.out
f79cd14affd062fd7b919f27dbf0fc55e5c47e34c728c321e317c61a792d124a  tests/run_all.sh
493655757ca2020af042798c79be785cca56fa85b154c2291f0df328bf3a7146  tests/test_ceiling.py
96c44fd12090e88a4bf050b0363ce6c5a318fa71d99083d3553d89d8f71e0b76  tests/test_cleanup.sh
658c57c3c3fff937f78c05b3a7f5bee96f6d8b7b5695e5ea7d1ce4cc4f561099  tests/test_collect.sh
27c361bf3cb20cb793f548ed5106e3635b07a5ee4482010d8c07f78d4b406af4  tests/test_deadline.sh
285b20c2aa4d92da57a849ea420f48472f194fcd900eda87a98ffb0915a7bc67  tests/test_driver.sh
f6c5a5bce849f670b1db32a2d45a37b80b584c6dbb12b3837022a87351244472  tests/test_jobmd.sh
16f02f98f9becc5c4b63fb604a6c40e1a251a562d72017ef5dcbcdd2f89f7295  tests/test_lists.py
9f40972499c8d4625513473267c882599819a6f43e0c90e456e29271ba823f9a  tests/test_manifests.sh
5841f9d26e753021ae6d09f9de225210f4770ef0f3f01f7527f2ce76e1d22a04  tests/test_p5.sh
86439ab9764027c2c78d9888bd19f1978d18cbe6b2cb191076f4a184ce97c870  tests/test_reconcile.py
edb623d8fb0f79144798f3e6470e68db301f4814afc957a9997f0b068191d130  tests/test_resubmit.sh
95534c59aa59ab430d1201859a6b9ef6581ad5cc8669fc42eae34c4c557c1e9b  tests/test_retune.sh
fed87e1557009567c8bc9539707e9e7dcf9779b6fc67795e221b1363b2d54a4d  tests/test_unlock.sh
8e99b88d338430d7791f3a1a21611e0e729af531800008d3993bfe8f521d30b6  tests/test_waiter.sh
f498e45b2656142f1812157baf56d42a3c332d468d75fa516ad81f174f826d07  tests/vec_check.py
cfdf0ba05fc3a94f70516ce9cd8d5e8e60e89d215fc969ea7e6b6b1dbe73912e  tools/make_lists.py
a4b4ddcd5b8b680cda3c8b30738949cab46a6baaba267e3dccb9acdd6c2436ae  truth_lib.sh
0fd6b1c80dcefca4b6ab37f1a9b4242cb4ebe46d2102ab3945a42a692ea24e5d  truth_wave.sh
5c5913af964987500aad87a606f8a7422ca2cf3894753006d875a86f4c8af127  waiter.sh
```
