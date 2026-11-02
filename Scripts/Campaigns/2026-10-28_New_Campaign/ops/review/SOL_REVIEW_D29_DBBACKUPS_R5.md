# Independent Sol review R5: D29 db-backups executor v5.1

Reviewer: Sol 6.1. Narrow fifth review; review only.

## Verdict: ACCEPT

**Accepted candidate list: 89 rows, 168,128 KB, 265 files.** No required fixes remain within this review's scope. These are reviewed list totals, not a prediction that the live executor will delete every row or free exactly that amount; its current-state gates still apply.

## Scope and evidence

I read R4, the submitted executor and harness, and the relevant saved v5.1 harness evidence. I independently checked local SHA-256 hashes, counted the saved PASS/FAIL assertions, and summed the unchanged list. I did not use SSH, connect to NOTS, execute either script, delete anything, or delegate. Only this review file was written.

HQ D34 and HQ's disposition of R4 F2 are accepted as instructed. This review does not reopen either accepted same-user race or require a different placement primitive. The prior archive verification is carried forward; remote archive contents were not rehashed here.

Locally checked SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `scaffold/d29_dbbackups_delete.sh` | `24bd5a586219a8fe189b9dc584e89664cd328348ff236d9380bc1b0c5bad0fae` |
| `scaffold/d29_test_harness.sh` | `832e2df0717396cf9a1390fd4af93b86110110c767dd1da6c98034aa5d84a105` |
| `evidence/ops4_dbbackups_delete_list.tsv` | `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c` |
| `evidence/ops4_d29_archive_manifest.sha256` | `d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816` |
| `evidence/ops4_d29_v51_harness_raw.txt` | `30022f62c0a12a39c269300eef12f30196844dc88529c7101b3f77b14d95b819` |

The saved run begins with the matching executor, harness, list, and manifest hashes. Its two printed test-copy diffs substitute only locations, the corresponding path-validation regex, expected hashes, and counts. Different runtime self-hashes for those substituted test copies are therefore expected. The evidence contains **58 PASS lines, zero FAIL lines**, `HARNESS RESULT: 58 pass, 0 fail`, `harness_rc=0`, and `ssh_rc=0`.

## Numbered findings

1. **R4 F1 resolved; no blocking finding.** In `open_scan`, executor lines 153-157 first establish that the process is still live, reject bad/empty producer classifications, and then abort on `cm=enoent`. The helper branch starts at line 158, so neither helper predicate can exempt vanished maps. Removing the former trailing `elif` leaves the intended independent producer rules intact: maps must be `ok` or an exempted helper's `eperm`; fd-only `enoent` remains allowable. No new acceptance path is introduced by the reordered gate.

   The new cat shim (harness lines 38-43) changes only the selected PID's maps read to an ENOENT diagnostic and status 1, delegating other reads to `/usr/bin/cat`. T5c selects the real `(sd-pam)` process and invokes the unmodified scan logic with that shim. Saved evidence lines 84-92 records PID **442640**, real fd-scan **status 1 / eperm**, maps **status 1 / enoent**, and `ABORT: maps of live process /proc/442640 vanished`. The summary records zero deletions; the four assertions confirm **rc 3**, the expected reason, all **11 fixture folders present**, and **no quarantine**. This exercises the combination that escaped v5's helper branch.

2. **R4 F3 resolved.** Harness line 12 now records each of the three fixture files as `name:device.inode:sha256`, using `stat -c %d.%i` and `cut -c1-64`. This preserves the full 64-digit digest rather than the former 16-digit prefix. Saved intact-file assertions display the device.inode identities and full digests, including T5b, T6, and T7-T7d. Existing comparisons continue to compare the complete per-file signatures.

3. **Accepted R4 F2 residual accurately disclosed; no fix requested.** Header lines 8-14 and the `place()` comment at lines 206-208 describe placement as **clobber-resistant** and explicitly state that another fb31 process's EMPTY replacement of the reservation can itself be replaced by rename. For that specified residual, replacement loses only the empty destination directory, not file contents. The wording no longer promises unconditional no-clobber placement. This is consistent with the supplied HQ disposition; the accepted residual is recorded and does not block execution.

4. **No new correctness bug found in the v5-to-v5.1 edits reviewed.** The reordered maps gate, removed old `elif`, harness signature change, targeted T5c shim/test, and revised comments/version output do not introduce a new correctness objection. No additional fix or remote rerun is required by this review before the planned live dry run.

## Disposition

Accept executor hash `24bd5a586219a8fe189b9dc584e89664cd328348ff236d9380bc1b0c5bad0fae` for the unchanged 89-row list under the stated HQ rules. Proceed with the planned absolute-path SSH dry run and inspect its saved output before the `--yes` invocation; preserve execution evidence and perform the planned disk guard and scratch cleanup. This review performs none of those operational steps.
