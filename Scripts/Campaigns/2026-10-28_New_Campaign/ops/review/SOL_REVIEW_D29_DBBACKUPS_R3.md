# Independent Sol review R3: D29 db-backups executor v4

Review time: 2026-10-30T01:30Z. Reviewer: Sol 6.1, independent review only.

## Verdict: REJECT

**Accepted for execution with the submitted executor: 0 rows, 0 KB. All deletion-list data rows 1-89 remain KEEP pending resolution of the blocking findings.** The unchanged list still contains **89 valid candidates, 168,128 KB, 265 files**; there is no new row-specific scope objection.

Atomic rename substantially improves protection against opens using the original pathname. It does not establish the claimed exclusion of subsequent opens or writes. In particular, a mode-0700 directory owned by fb31 remains accessible to other fb31 processes. The supplied T7b actually demonstrates opening the quarantine pathname. Its successful detection during the scans does not exclude an open after the relevant process's last scan. There are also remaining fail-open scan-status and partial-reporting defects.

Only this review file was written. I read R1 and R2 first, all 281 executor lines, all 91 harness lines, both complete v4/v4b saved outputs, and the saved archive verification evidence. Local checks were read-only hashing, TSV parsing/arithmetic, and evidence inspection. No SSH, NOTS connection, executor/harness run, deletion, simulation, or benchmark occurred. No subagents were used.

## Identity and evidence

Locally checked SHA-256 values:

| Input | SHA-256 |
|---|---|
| `scaffold/d29_dbbackups_delete.sh` | `4bb5703577430ca640cf6c8f5ccd60929c785bed0ca19d2911a53e4f1a273865` |
| `scaffold/d29_test_harness.sh` | `b68e40576d7e708fba6474d4e23bfe8581f30edaea38fffc1dbf3139059dec3d` |
| `evidence/ops4_dbbackups_delete_list.tsv` | `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c` |
| `evidence/ops4_d29_archive_manifest.sha256` | `d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816` |
| `evidence/ops4_d29_ARCHIVE_VERIFY.json` | `0d7fcc092cbb1d6918ca516466b3bf154b6516203e88cd20ce5a92b1d3862619` |
| `evidence/ops4_d29_v4b_harness_raw.txt` | `288bc58d950daef455f634665ce198ac2134bf5367184106aca2d46d5a9230fa` |
| `evidence/ops4_d29_v4_harness_raw.txt` | `22c9c13b30cf767e59c167eeb28fe2c4c0d65943c2770625567f141de3b0e41d` |

D30 remains accepted as Felipe's attestation resolving the cross-node objection. D31 and R2's independent laptop verification remain accepted: 265/265 archived files, 171,442,312 bytes, no mismatches/missing/extra data files. I did not rehash the archive contents in R3. The unchanged verification JSON and manifest support continuity with R2; they do not preserve subsequent writes automatically.

The v4b output contains exactly **36 PASS lines, zero FAIL lines, `HARNESS RESULT: 36 pass, 0 fail`, and `harness_rc=0`**. Its leading hashes match the submitted artifacts. Both printed test-copy diffs change only the paths, path-validation regex, and expected input hashes/counts. The earlier v4 output records 30/0 with the same executor but an earlier harness hash. These are inspected saved results, not tests rerun by this reviewer.

## Numbered findings and concrete fixes

1. **BLOCKING — quarantine is a pathname relocation, not exclusion of other fb31 processes (lines 18-21, 191-192, 242-259).** Mode 0700 excludes other ordinary users, not other processes with owner credentials fb31. The fixed pathname `~/.ops4_d29_quarantine/<name>` remains openable throughout hashing and unlinking. T7b's watcher opens exactly that pathname and is caught at Q-pass1/Q-pass2. Change its timing so the open occurs after its final scan, and neither pass detects it. A reader can then be unlinked despite the keep-open rule; a writer can modify a previously hashed inode before pass 2, whose inode-only check still passes. This requires an ordinary pathname open, not Unix-socket descriptor passing. Two scans one second apart do not make either scan an exclusion interval.

   The proposed fd-passing residual is also real: a descriptor can move from a not-yet-scanned process to an already-scanned process, with the sender closing its copy. Existence somewhere before rename does not imply observation during a sequential scan. An open already resolving the old path at rename time is another case not ruled out by the argument. I have no evidence these occur in the actual Codex workload; equally, the supplied evidence does not justify the universal claim that no later writable descriptor is possible. The >24-hour age and verified archive lower the practical consequence, but do not satisfy the unchanged keep-open/live-write rule.

   **Fix:** either establish a writer-respected exclusion spanning the scans, hashes, and unlinks, or obtain an explicit change to the keep-open/live-write rule covering these actual residuals, including same-UID quarantine-path opens. A cooperating lock can leave Codex running if all relevant writers honor it; a deletion helper isolated by different credentials can provide pathname access exclusion, but inherited descriptors still require treatment. A cleanup-only flock, random quarantine name, extra scan, or another hash is not proof of exclusion. Do not stop Codex under this review's authority. Until one of these routes is established, retain the folders. Correct header lines 19-21 to distinguish blocking opens by the **old** pathname from guaranteeing absence of all subsequent opens/writes. This is a substantive unresolved gate, so the verdict is not ACCEPT WITH FIXES.

2. **BLOCKING — unexpected nonzero `/proc` producer statuses can still be accepted (lines 118-143).** Capturing `frc` and `mrc` separately is correct, but their values are not subsequently validated. For a live process, if `find` fails with empty stderr and partial/empty stdout while `cat maps` succeeds, both greps return 1; execution falls through the comment claiming “only ENOENT lines.” There may be no ENOENT line at all. A killed producer can take this path. Partial descriptor output can therefore be treated as a completed negative scan. The helper branch likewise accepts any mixed error set containing “Permission denied” once the helper predicates match, including unrelated errors.

   **Fix:** classify each producer independently. Accept status 0 with empty stderr; otherwise require a specifically allowed status and a nonempty diagnostic set consisting entirely of the permitted transient ENOENT errors, or entirely of the explicitly permitted helper-access errors for a verified helper. Abort for signal/other unexpected statuses, nonzero status without diagnostics, or mixed/unrecognized diagnostics. Preserve both status values and both stderr files in refusal evidence. The existing explicit grep 0/1/>1 handling and associative KEEP membership are good and should remain.

3. **SHOULD-FIX — the progress counter is still late enough to report an actual unlink as intact KEEP (lines 257-266).** `rm` can successfully unlink the first file at line 260, another process can create an entry at the same pathname, and line 261 then breaks before line 262 increments `unl`. Line 265 consequently restores the folder with “nothing unlinked,” increments KEPT, and can finish with exit 0 even though an original file was removed. This is the same classification problem R2 F3 sought to eliminate, in a narrower form.

   **Fix:** record successful removal-command progress immediately after successful `rm`, before any post-removal check. Conservatively classify every later failure as PARTIAL/nonzero once a removal succeeded. For an interrupted or otherwise indeterminate removal, use FAILED/PARTIAL rather than asserting unchanged KEEP; a mutation-started flag is suitable. Do not describe `rm -f` success as proof that a file existed and was actually unlinked. Check and report residue-listing status separately; current lines 266/272 can present failed/partial `find` output as a remaining-entry list.

4. **SHOULD-FIX — restoration can overwrite a concurrently recreated empty directory (lines 180-186).** The `! -e "$BASE/$n"` test and subsequent plain `rename` are separate operations. If Codex recreates that pathname as an empty directory between them, POSIX rename can replace it. The later source-inode check succeeds while the fresh destination directory has been removed. No malicious process is required for a pathname to be recreated after quarantine.

   **Fix:** use an atomic no-replace rename for restoration, e.g. a checked `renameat2(..., RENAME_NOREPLACE)` helper on a supporting filesystem, with no copy or overwriting fallback. If the destination exists or the operation is unsupported, leave the original quarantined, report its exact location, and return failure. Retain identity verification and use `(device,inode)` pairs consistently; current post-rename/restore checks record inode alone despite the header's pair claim. Apply the no-replace primitive to quarantine entry creation as well for consistent collision handling.

5. **SHOULD-FIX — add focused assertions for the unresolved paths; existing PASS results do not cover them.** The new harness materially resolves R2's missing exit assertions, isolates old top-three/tie retention, and supplies useful non-dumpable-process and during-run-open cases. However, T7b opens immediately on quarantine appearance and holds the descriptor, so it tests detection during scans, not exclusion afterward. The “files intact” assertions at harness lines 58/72 check file count, not every file's inode/content. There are no injected silent scan failures or failed-unlink-progress/restoration-collision cases.

   **Fix:** on the authorized remote fake trees only, add synchronized cases for (a) a quarantine-path open after that process's final scan, (b) partial/empty descriptor output with nonzero producer status and empty stderr, (c) recreation immediately after the first successful unlink and before the postcheck, and (d) a restore destination created immediately before rename. Assert executor status, exact outcomes, source file hashes/identities where claiming unchanged KEEP, and quarantine residue. Use deterministic synchronization rather than another fixed sleep. Case (a) must either demonstrate effective exclusion or document the explicitly authorized changed risk model; a test that merely reproduces the existing race is not a fix. Preserve fresh hashes, substitution diff, raw output, and statuses.

## Disposition and execution boundary

R2's membership-grep defect is resolved by the associative array; inventory aggregation/sort/keep producers now have explicit failure branches; separate fd/maps status capture and PID start-time checks are improvements. The helper parent comm/owner predicates and preservation of positive helper references implement the specific R2 minimum corrections. Absolute-path usage resolves R2 F6. Archive-before-unlink checks, fresh per-row retention, conservative ties, nonrecursive file removal, and checked final inventory remain appropriate.

These improvements do not close findings 1-2. **Do not proceed to `--yes` for executor hash `4bb57035...` under this review.** A successful dry run cannot establish the missing exclusion interval. Preserve the current artifacts and failure/recovery evidence; if quarantine or failed/partial rows remain after any future execution, inspect and recover them before removing scratch evidence. No connection, disk guard, or scratch cleanup was performed or authorized anew by this review.
