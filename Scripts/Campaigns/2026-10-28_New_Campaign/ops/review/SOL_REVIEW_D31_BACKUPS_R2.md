# Independent Sol re-review R2: D31 backups executor

**Verdict: REJECT. F2 is resolved; F1's local scan remains blocking because of the reference-detection defect below.**

Reviewer: Sol 6.1. Reviewed 2026-10-30, approximately 18:19 UTC. Narrow review only: no SSH, remote probes, executor execution, deletion, or delegation. Only this review file was written. Findings below are from static inspection and saved evidence; no reproduction was run.

## Scope and evidence

Read the complete `scaffold/d31_backups_erase_remote.sh`, the original D31 review, `review/SOL_REVIEW_D29_DBBACKUPS_R5.md`, the relevant d29 v5.1 scan implementation and header, the D31 cleanup-log entry, and `evidence/ops6_d31_backups_dryrun.txt`. The original independent archive PASS is carried forward; the archive files were not rehashed in this narrow review.

Locally checked SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `scaffold/d31_backups_erase_remote.sh` | `7996634605e7ae0403e5a1ef51c07245bac9fc417c2480776b55f45d16080379` |
| `evidence/ops6_d31_backups_dryrun.txt` | `f2fb2f97e7b5c0e14d94160ac5c0756d90aea49de052d7d046848f4a96d06d40` |

The supplied invocation is `ssh nots "MODE=yes bash -s" < scaffold/d31_backups_erase_remote.sh`, through the OPS SSH shim and its global connection lock. This review does not execute or independently validate that shim.

## Findings

1. **F2 resolved: concrete, bounded deletion operands.** Lines 11-23 hard-code the two previously verified names and complete SHA-256 values, enforce loginx2/fb31, require the real directory at its canonical home-relative location, require an exact two-entry regular-file inventory, reject target symlinks, and verify both hashes before any target unlink. Each failed gate explicitly refuses; absence of `set -e` does not bypass those gates. Line 57 uses only the two quoted fixed paths with nonrecursive `rm --`; line 58 removes only the empty parent with `rmdir --`. There is no glob, recursive removal, or deletion list derived from unchecked command output.

2. **BLOCKING: F1 local reference detection can miss an actual reference (lines 8, 39).** The executor enables `pipefail`, then tests `printf '%s\n%s\n' "$fo" "$mo" | grep -qF "$D"` as a single pipeline. When grep finds a reference early in sufficiently large fd/maps output, it exits successfully without consuming the remaining input. The upstream Bash printf can then receive SIGPIPE. With `pipefail`, that makes the pipeline nonzero despite grep finding the reference, so the `then` branch does not increment `hits`. Both original find/cat producers can still have status zero and empty diagnostics, allowing the subsequent classification gates to pass. With no other counted hit, execution can print `no reference` and proceed to unlink an open target. A grep error is also treated as a negative match by the same conditional. This is a new implementation defect, not the accepted cross-client visibility residual.

   **Required fix:** check the reference matcher's own status independently of an early-exiting pipe producer: zero means a hit, one means no match, and any other status must refuse. For example, search a successfully written file or use a here-string rather than this printf pipeline, and explicitly classify grep's status. Preserve any reference already observed even when helper inspection is exempted. Before resubmission, save focused evidence showing that an early matching reference followed by output larger than a pipe buffer refuses, and that a matcher error refuses. The existing no-reference dry run does not exercise either case.

3. **F1 producer-status and helper rules are otherwise substantially addressed.** Lines 28-52 distinguish clean producers, all-ENOENT diagnostics, all-EACCES diagnostics, and invalid statuses/diagnostics; reject vanished maps for a still-live process before helper exemptions; and use the stated sshd / `(sd-pam)` parent predicates. fd-only ENOENT remains allowable. However, these rules cannot repair the lost match in finding 2, so the local portion of F1 is not resolved. The saved dry run reports exact content/hash gates, no reference on loginx2, eight skipped helpers, and `RESULT DRY_RUN_OK (nothing erased)`; it supports that observed run, not correctness of the positive-reference path.

4. **D34 residual accepted for this review as supplied.** I accept the instructed application of HQ D34 to the inability to prove absence of an fb31 process holding these archived, SHA-256-verified, long-untouched tarballs open on another NFS client. This is an application of the supplied precedent, not a new HQ statement or a claim of cluster-wide visibility. No additional node contact, technical fix for that visibility limit, or new HQ statement is requested here. The rejection is solely the local implementation defect above.

5. **Partial-result handling passes static review.** Failed `rm` reports `RESULT PARTIAL` and exits 1; failed `rmdir` after successful unlink also reports partial and exits 1, without broadening deletion. `RESULT ERASED` is reached only after successful removal commands and the final absence test. No new partial-as-success path was found within the stated scope. The previously disclosed concurrent path-replacement limitation is not converted into an atomicity guarantee by this review.

## Disposition

Do not use this executor hash for erasure. Fix the local reference matcher and submit the changed concrete executor and focused saved evidence for narrow re-review. Archive identity and F2 remain accepted; the supplied D34 application is not being reopened.
