# Independent Sol re-review: D29 Codex db-backups deletion list

Review date: 2026-10-30 UTC. Reviewer: Sol 6.1, independent review only. Scope: the unchanged D29 list, D30/D31 evidence, the complete 200-line v3 executor, and the supplied harness and saved outputs.

## Verdict: REJECT

**Accepted for execution using the submitted v3 executor: 0 rows, 0 KB. All deletion-list data rows 1-89 remain KEEP pending the blocking fixes below.** The candidate scope remains correct: all 89 rows, totaling **168,128 KB**, are valid candidates, with no row-specific exclusions. After the blocking fixes, those exact rows can be reconsidered subject to fresh run-time keeps; this review does not authorize their deletion now.

D30 resolves the cross-node evidence objection in the earlier finding 1. D31 establishes recovery of the archived snapshot, independently verified below. Neither statement establishes that local writers cannot open or change an old folder between the executor's scan and unlink. That remaining part of earlier finding 4 is a different issue from cross-node visibility. The revised executor also retains some fail-open error paths and an incorrect partial-deletion classifier.

Only this review file was written. No SSH or NOTS connection, executor/harness execution, deletion, or modification of reviewed inputs was performed. Local actions were read-only inspection, hashing, and comparison of the supplied files and the explicitly permitted laptop archive. No simulation, benchmark, or numerical workload was run.

## Input identity and archive verification

The following SHA-256 values were independently checked locally:

| Input | SHA-256 |
|---|---|
| `scaffold/d29_dbbackups_delete.sh` | `d302de842137fff4b66f6ee1b65a61da3247f882d1a7682ea20a4c06b5c81eca` |
| `scaffold/d29_test_harness.sh` | `910454e520d83ed8bb37e57945f30d0e4f343c9c6c5aadf26bf8b60100800911` |
| `evidence/ops4_dbbackups_delete_list.tsv` | `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c` |
| `evidence/ops4_dbbackups_keep_list.tsv` | `ec1eb02e525cf5e907563cff41547027c31c0de621a5b268a2d6cd51ac31a30e` |
| `evidence/ops4_dbbackups_list_raw.txt` | `32050e263f399c51b542db8236944e306c0c3d1e4571ee3774fe9a3f3e3bbffe` |
| `evidence/ops4_d29_archive_manifest.sha256` | `d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816` |
| `evidence/ops4_d29_ARCHIVE_VERIFY.json` | `0d7fcc092cbb1d6918ca516466b3bf154b6516203e88cd20ce5a92b1d3862619` |
| `evidence/ops4_d29_v3d_harness_raw.txt` | `cb3c1fc0e098aaaed2273c5ef0c8edadf49c2b600665cdc1e255200670e51291` |

The inventory, delete list, and keep list are byte-identical to the first review, so its partition/scope PASS stands. I also re-parsed the delete TSV: 89 rows, sum of `du_kb` = 168,128.

At **2026-10-30T01:07:11Z**, I independently hashed every archived data file under:

`<PC_NOTS_DATA>\NOTS_home_archive\codex_db_backups_20261030\`

Result: **265/265 hashes match; 171,442,312 bytes; zero missing, extra, or mismatching data files.** The archive's own manifest has the same pinned manifest hash. A separate join confirmed exact equality of the TSV's 265 file paths and manifest paths, and every archived file's byte size equals its TSV size. Root-level archive metadata (`archive_manifest.sha256`, `ARCHIVE_VERIFY.json`, `names.txt`) is not counted as extra database data. This independently corroborates the saved verification JSON and remote-stderr manifest count/hash.

D30 is accepted as Felipe's owner attestation, as supplied in the review request; I did not independently contact other nodes. The mode-700 header evidence supports the stated ordinary-other-user access restriction. D31 makes the **verified archived bytes** recoverable; it does not capture later writes automatically or waive the keep-open rule.

## Disposition of the earlier findings

| Earlier finding | R2 assessment |
|---|---|
| 1. Cross-node non-use | **Resolved for this review by D30.** No further cross-node probe is requested. D31 separately resolves absence of a verified recovery copy. |
| 2. Fail-open discovery | **Partly resolved.** Full-tree `find` status/stderr handling is good; `/proc` scan failures generally propagate. Remaining unchecked guards are blocking finding 2 below. |
| 3. Cached retention | **Resolved in the ordinary successful-scan path.** `scan` is called before each row; top-three ties and the inclusive 24-hour predicate are correct. Atomicity and error propagation remain separate findings. |
| 4. Replacement/live-writer races | **Substantially improved, not resolved.** No recursive target deletion; working-directory binding, inode checks, and `rmdir` limit scope. No exclusion of new opens or same-inode writes: blocking finding 1. |
| 5. Reviewed-input binding/schema | **Resolved for these exact inputs.** Private `mktemp` copies, pinned hashes, exact header/count/path validation, final newline/CR checks, and list/manifest set equality prevent using another ordinary TSV. Verify the deployed executor's hash externally before invocation; its self-hash is logged, not enforced. |
| 6. Partial/failure status | **Partly resolved.** Refusal/abort and detected-partial exits are nonzero. Entry-count-based KEEP can still hide partial deletion: finding 3. Some accounting errors remain unchecked under finding 2. |
| 7. Invocation/host/user | **Host, user, and exact arguments resolved.** No embedded-list claim remains. The header's unassigned `$D` example is a minor documentation issue (finding 6); the proposed absolute-path invocation avoids it. |
| 8. Aggregate mtime versus content | **Content identity materially resolved by the archive SHA check before any unlink.** The historical integer aggregate mtime is accurately treated as that limited snapshot value. Content stability after hashing is still finding 1. |

## Numbered findings and concrete fixes

1. **BLOCKING — new local opens and same-inode writes remain possible after the eligibility/hash checks (executor lines 118-139, 158-180).** A scan enumerates processes and their references at different instants. A readable fb31 process can open a candidate after its turn in `open_scan`, or a new process can start after the `/proc` glob was expanded. Opening for reading need not change the folder's mtime, size, inode, or hash, so all later checks can pass and the script can unlink a folder that must be kept under the open-file rule. Separately, after pass 1 hashes a file, a process can write it in place; pass 2 checks only the inode, which remains unchanged, and erases bytes absent from the verified archive. D30 restricts the node; it does not exclude this local activity. The two-pass change correctly prevents a pre-existing third-file hash mismatch from deleting files 1 and 2, but lengthens the interval between the earlier hashes and their unlinks. The header's claim of a hash check immediately before each unlink is therefore also inaccurate.

   **Fix:** establish and record a writer-respected exclusion interval spanning inventory, open checks, content checks, and unlink. For example, all relevant Codex processes must honor a common lock, or an explicitly authorized maintenance interval must prevent relevant processes from opening these folders or changing the tree until cleanup finishes. A cleanup-only flock, extra scans, or hashing again without writer coordination does not close this race. Do not stop processes under this review's authority. If such exclusion cannot be established, keep the candidates unless Felipe explicitly changes the applicable keep-open/live-write rule with the residual risk described. Retain descriptor-relative/nonrecursive deletion and verify `(device,inode)` identities within that interval. Adjust the header to describe the two actual passes.

2. **BLOCKING — the keep decision still treats command failure as a negative result (lines 42, 92, 110, 120-130, 141).** The decisive `printf ... | grep -qxF` at line 141 has only an `&&` branch: grep's error status 2 (or command-not-found status 127) is treated exactly like no match. Thus an old, unchanged candidate that `open_scan` correctly put in KEEPSET can still be erased when the membership command fails. `grep` is also absent from the required-tool list. In addition, the `bad`, `INV`, and `KEEPSET` assignments have no explicit failure branch; `set -u` and `pipefail` do not abort the surrounding script. A nonempty partial inventory/keep set can pass the current cardinality check. The grouped KEEPSET producer can mask failure of its first awk pipeline with the subsequent successful printf. Inside `open_scan`, line 92 captures the group's final `cat` status, not the preceding `find` status; stderr catches normal find errors but does not substitute for checking both statuses. Per-process output-parser failures can likewise be overwritten by later loop iterations.

   **Fix:** explicitly check each safety-critical producer/transform status before consuming output, with complete stderr preserved. Split the `/proc` find and maps reads so both statuses are captured. Build retention and open sets separately with checked commands, then combine with checked commands. Use a shell associative set for membership, or capture the complete membership-command status and accept only 0 = KEEP, 1 = absent; abort on any other status. Avoid early-consumer/SIGPIPE ambiguity. Check all required external tools, including grep. Also check `du` and the final remaining-folder scan statuses (lines 161 and 196): plausible numeric stdout does not prove those commands succeeded. These last two affect accounting rather than the core open-file gate, but should not produce a clean success report after an operational failure.

3. **SHOULD-FIX — the PARTIAL classifier equates entry count with “nothing unlinked” (lines 182-186).** Suppose a three-file row passes pass 1, the first rm succeeds, a new entry appears, and a later inode check/rm fails. Three entries can remain despite an unlink. Line 185 then reports KEEP, increments no failure counter, and permits exit 0. Replacements or a renamed/replaced pathname can produce the same false conclusion. The residue find also ignores status/stderr. The ordinary third-file hash-mismatch case in v3d is correctly KEEP because pass 2 never started; that does not validate the general count-based test.

   **Fix:** report mutation phase and successful unlink progress explicitly from the deletion worker. A failure after pass 2 starts must conservatively be FAILED/PARTIAL and nonzero unless trustworthy progress evidence proves no unlink occurred. Distinguish known no-unlink preflight exits 10-14 from mutation exits 16/17 and unknown/signal exits; do not infer progress from count. Inspect residue through the held directory object with checked status, and compare exact names/identities where claiming unchanged state. A checked residue listing is evidence of what remains, not proof of what the script removed.

4. **SHOULD-FIX — helper exceptions are broader than the documented parent identities (lines 95-104).** The sshd exception checks child comm `sshd` and parent owner root, but never requires the parent comm to be sshd even though `pc` is read. The `(sd-pam)` exception checks parent comm/systemd ancestry but never requires parent owner fb31, despite the comment saying “the user's systemd manager.” These mutable names/ancestry predicates should not be presented as authentication of arbitrary future unreadable processes. `continue` also discards any candidate references already present in the partial output for an exempt process.

   **Fix:** at minimum require the stated parent owner **and** parent comm for each role, validate numeric parent identity and process start identity consistently across reads, and preserve any positively observed references even for an approved helper. Bind exceptions to the documented trusted session-helper roles, log their exact identities, and refuse on an unverified exception. If sufficient identity cannot be read, obtain appropriate trusted evidence or keep/refuse rather than broadening the exception. The current saved output supports the observed helper cases, not every process that could match these loose predicates.

5. **SHOULD-FIX — harness evidence does not exercise the remaining guarantees, and later exit statuses are not asserted (harness lines 27-37).** The saved v3d output supports the eight scenarios as described below. However, T8 adds a folder **between separate script invocations**; it does not test retention changing between rows within one invocation. Every top-three folder in the fixture is already younger than 24 hours, and there is no third-place tie, so top-three protection is never isolated from the age rule. No case injects a keep-membership error, partial-output scan error, post-hash write/open, same-count partial residue, or an unrecognized unreadable process. The harness prints expected outcomes rather than asserting them; T6-T8 pipe to grep without preserving/asserting the executor status. In fact the saved v2 T7 shows an ABORT summary alongside `rc=0`, illustrating why a pipeline's status is insufficient.

   **Fix:** add focused fake-tree tests with synchronized mutation/error injection for findings 1-4; include old top-three/tied folders and a mid-invocation retention change. Assert exact row outcomes, untouched file identities/content, residue, and executor exit statuses. Capture `PIPESTATUS[0]` immediately where filtering output, or save raw output and status before filtering. Preserve fresh script/harness hashes and raw results. Run any additional execution tests only on the authorized remote destination; none were run during this review.

6. **MINOR — the header examples refer to an unassigned remote `$D` (lines 8-9).** The parenthetical text does not set the variable in the remote shell, so copying either example literally can select `/d29_dbbackups_delete.sh` instead of the scratch script. This fails safely, and the fully expanded invocation in the review request avoids it. **Fix:** use complete absolute paths in both examples, or explicitly assign the remote variable before using it.

## What the saved tests support

The final raw file begins with the exact submitted executor and harness hashes. Its diff shows only the fake BASE/path-regex/ancestor path and input hash/count substitutions. The fake script's different self-hash is therefore expected.

- T1: unknown `--force` refused, rc 3.
- T2: modified list refused by the pinned hash, rc 3.
- T3: dry run selects only sqlite-100-0 and sqlite-200-0; seven rows kept; rc 0.
- T4: stray base symlink aborts before mutation, rc 3; all eleven fixture folders remain.
- T5: only 100/200 deleted; wrong-hash 150 retains all three original names; fd-held 300, cwd-held 250, size-changed 400, mtime-changed 500, and recent 600/700 kept; rc 0.
- T6: absent 100/200 reported as such; zero new deletions and summary OK. The executor's raw exit status is not recorded independently of the filter.
- T7: after releasing the two holders, 250/300 deleted; summary OK. Same exit-status limitation.
- T8: the next invocation sees new 950 and retains recent 700; summary OK. Same exit-status limitation; no tie or within-run retention-change test.

Earlier outputs explain the iteration: v2 refused on lsof rc 1; v3/v3b refused on previously unhandled unreadable helpers; v3c exposed the third-file hash mismatch after two prior unlinks and returned PARTIAL/rc 1; v3d's two-pass preflight fixes that specific defect. The outputs are useful positive evidence, but do not establish the additional race/error guarantees listed above.

## Scope and next gate

On a stable tree with successful tools, the loop uses only the 89 pinned paths and the manifest's fixed basenames. The mutation rm is nonrecursive and directory-relative, so an added subdirectory or symlink is not recursively erased; `rmdir` preserves unexpected remaining entries. The top-three expression updates its threshold through row three and then retains every equal/newer timestamp, so boundary ties are handled conservatively. The age comparison keeps equality at 24 hours. Private-copy hashing and manifest membership are appropriate for the reviewed files.

These improvements and the verified archive remove substantial earlier objections, but do not override findings 1-2. **Do not proceed to `--yes` with hash d302de84... under this review.** Fix the blockers, correct partial reporting, and supply focused evidence for re-review. Preserve the deployed script/list/manifest hashes, complete dry-run and execution logs and statuses, and any failure residue evidence before removing scratch artifacts. A dry run alone cannot close the check-to-unlink interval. No narrower row subset avoids these executor-wide defects.
