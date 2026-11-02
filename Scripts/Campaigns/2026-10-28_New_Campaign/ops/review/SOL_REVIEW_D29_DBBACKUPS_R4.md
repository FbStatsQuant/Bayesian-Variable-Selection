# Independent Sol review R4: D29 db-backups executor v5

Reviewer: Sol 6.1. Narrow, independent, review-only fourth review.

## Verdict: REJECT

**Accepted for execution with this executor: 0 rows, 0 KB.** The unchanged list contains **89 valid candidate rows, 168,128 KB, 265 files**. There is no new row-specific objection; the remaining objections concern executor behavior.

R3 F2 is substantially improved but has one explicit acceptance-rule bypass. R3 F3 is fixed for the reviewed removal paths. The reservation implementation passes the two supplied collision cases but does not provide the claimed unconditional no-clobber property. The focused tests are useful and their saved results are authentic to the checked source hashes, subject to the gaps below.

## Scope and evidence

I read R3, all 320 executor lines, all 136 harness lines, the complete saved v5b harness output, the previous run's failing assertions and summary, and the saved NFS probe. I performed read-only local hashes, list arithmetic, and evidence inspection. I did not use SSH, connect to NOTS, execute either script, delete anything, or delegate work. Only this review file was written.

D34 is accepted exactly as instructed. Header lines 11 and 25-27 accurately distinguish blocking opens through the old pathname from the accepted same-user quarantine-path/descriptor residual. R3 F1 is closed by that decision and is not reopened here. No writer exclusion or stopping Codex is requested. The prior independent archive verification remains accepted; archive contents were not rehashed in this review.

Locally checked SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `scaffold/d29_dbbackups_delete.sh` | `a343ca33fa431fc562f1d86c56b3559cf17ffa803fad9c02567ce728d4bf0fd9` |
| `scaffold/d29_test_harness.sh` | `3ada57a6abe9492f49c2cfb619ff6c0fc8eefba888f9d9cf1e05045c5ee58dd1` |
| `evidence/ops4_dbbackups_delete_list.tsv` | `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c` |
| `evidence/ops4_d29_archive_manifest.sha256` | `d2a67f0dd6e0a695ba5a8e92ad5788e9b540417bb6c9374500b17acddba81816` |
| `evidence/ops4_d29_v5b_harness_raw.txt` | `eb5414d6ba8b7ac309f31679029aaf6fe0102e1a2ce4833f286c97ba9ecae030` |
| `evidence/ops4_d29_v5_harness_raw.txt` | `629abc12b28e2e8cc33c846405ef7a186d81a0f939c3c8cef03e8851b4fe77f6` |
| `evidence/ops4_noreplace_probe_raw.txt` | `0baf49aa4f8716e5bf30ac17dc260f08ede75c9870542688f2c06cb86de3b2a4` |

The v5b evidence begins with the matching submitted executor/harness hashes and records exactly **54 PASS lines, zero FAIL lines, `HARNESS RESULT: 54 pass, 0 fail`, `harness_rc=0`, `ssh_rc=0`**. Both printed test-copy diffs change only locations, their path-validation regex, expected hashes, and counts. The earlier evidence records 50 pass/2 fail, specifically T7c/T7d expecting 1 instead of the actual 3. The corrected expectations agree with the next-row foreign-entry aborts; they do not conceal a successful run misreported as failure.

## Numbered findings and concrete fixes

1. **BLOCKING — a live helper's vanished maps can bypass the maps-ENOENT refusal (executor lines 153-165).** Consider `cf=eperm`, `cm=enoent`, with the process still live and satisfying either strictly identified helper predicate. The `eperm` branch is entered, the helper is accepted, and the `elif [ "$cm" = enoent ]` is never evaluated. Stable start times then allow the scan to complete. Thus ENOENT is accepted for the maps producer in this combination, contrary to the explicit R4 rule that ENOENT is acceptable only for the fd producer and vanished maps of a live process must abort. The independent classifier correctly identifies both classes; the caller combines them incorrectly. T5b proves the silent-status-1 case, but does not cover this combination.

   **Concrete fix:** after confirming the process is still live and rejecting bad/empty classes, reject `cm=enoent` unconditionally, before helper exemption handling. Then independently require each producer to satisfy its own allowed classes: fd `ok`/`enoent`, or `eperm` for a verified helper; maps `ok`, or `eperm` for a verified helper. Add a focused regression for a verified helper with fd EACCES and maps ENOENT, asserting abort/nonzero and no deletion. Retain the successful silent-failure test and the status-0/1-only classifier restrictions.

2. **SHOULD-FIX — reservation plus replacing rename still can clobber a different empty directory (executor lines 203-217).** `mkdir "$dst"` exclusively creates a directory at one instant, but it does not reserve that pathname against removal/replacement. A concrete interleaving is: our mkdir succeeds; `rid` is captured; another same-user operation removes the empty reservation and recreates an empty directory at `dst`; `prename` replaces that new directory. The postcheck verifies the moved source's ID and absence of `src`, so `place` returns success after the foreign empty directory has been destroyed. Even an additional pre-rename identity check would leave the same check/rename gap. The cleanup at line 213 likewise has a stat/rmdir gap in its claim to remove only its own reservation. T7c covers a destination existing before mkdir, and T7d covers a nonempty reservation; neither exercises replacement by a different empty directory. This is a destination replacement issue in R3 F4, outside D34's accepted opens/passed-descriptor residual.

   **Concrete fix:** do not advertise this as atomic no-clobber placement. Use a filesystem-supported atomic no-replace operation for any destination exposed to replacement; when no such operation is available, fail closed and retain the source at its known location instead of performing an overwrite-capable automatic restore. The saved EINVAL probe justifies refusing an unsupported primitive, not substituting replacing rename as an equivalent guarantee. Apply the same guarantee or conservative refusal to quarantine placement. Avoid pathname cleanup that can remove a replacement directory. Add a synchronized test that replaces the successfully created reservation with a different empty directory before rename, and assert that its device/inode survives and the original source remains intact. No writer-exclusion request is part of this fix.

3. **MINOR — the new intact-file assertions compare truncated hashes (harness line 12).** `fsig` visits all three fixture files and records their inodes, but `cut -c1-16` retains only 16 hexadecimal digits of each SHA-256. Consequently the description that intact assertions compare every file's SHA-256 is stronger than the actual check. This does not invalidate the observed PASS results or suggest actual corruption.

   **Concrete fix:** retain the full 64-digit digest in `fsig`; preferably record `%d.%i` as well, matching the executor's identity convention. Keep the per-file comparisons in T5b, T6, T7, T7b, T7c, and T7d.

## Resolved behavior and disposition

The original R3 F2 nonzero-silent failure is fixed: each producer's status and diagnostics are classified separately; status 1 with empty stderr and statuses greater than 1 are bad. Mixed ENOENT/EACCES lines from one producer are bad. The outstanding finding is specifically the caller's helper/maps combination above.

R3 F3 is fixed in the reviewed ordinary execution paths. `CUR_MUT=1` precedes `rm`, successful-command progress increments immediately, and post-removal recreation produces PARTIAL without restoration or a KEPT increment. The inspected T8 output shows exactly that behavior after one successful rm, quarantine residue, and exit 1. Failed/indeterminate rm is conservatively PARTIAL. `abort()` also has an explicit mutated-row PARTIAL branch rather than restoring it, and residue output includes its own listing status. The header documents global abort status 3 separately. No further removal-loop bug was found that reports an executor-mutated row as kept.

The device.inode transition is internally consistent in directory IDs, file snapshots, verification, pass-2 comparisons, and final rmdir checks. The dot separator does not conflict with the colon-delimited file snapshot parser. Unlinks remain limited to the pinned list's validated names and the manifest's allowed file basenames; no new path-expansion or recursive-removal route outside the list was found in the changed deletion code.

R3 F4 is improved for the tested preexisting-destination and nonempty-reservation cases, but remains incomplete as described in finding 2. R3 F5's requested silent failure, immediate recreation after rm, and two supplied restore collisions are now exercised with outcome/status assertions; add the classifier combination and empty-reservation replacement cases above. No post-last-scan quarantine-open test is demanded under D34.

**Do not proceed to `--yes` for executor hash `a343ca33...` on this review.** Resolve the remaining classifier gate and placement guarantee, then preserve fresh source hashes, substitution diffs, and remote focused-test evidence for review. This review performs none of the planned execution, disk guard, or scratch cleanup.
