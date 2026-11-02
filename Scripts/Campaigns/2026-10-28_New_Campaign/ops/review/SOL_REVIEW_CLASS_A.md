# Independent review: class-A NOTS cleanup

Overall verdict: **REJECT (current plan and deletion tools).** Do not treat this as execution approval.
Scope: static review of the explicitly named files only; no SSH, source-data rehash, deletion, or tool execution.
The supplied no-jobs observation is accepted; it does not exclude later writes or establish file ownership.

## Per-item verdicts

| Item | Verdict | Assessment |
|---|---|---|
| A1.1 | APPROVE WITH FIXES; hold deletion | BVS scratch, outside both freezes; authorized production copy. 4,800 files / 1,097,537,311 B match locally, but the supplied list is not relative to the stated deletion base. Fix findings 1-6. |
| A1.2 | APPROVE WITH FIXES; hold deletion | Same scope/authorization; 4,800 files / 2,905,373,304 B match locally. Same list/base mismatch and tool blockers as A1.1. |
| A1.3 | APPROVE WITH FIXES; hold deletion | BVS home, not frozen; 55,024 files / 321,924,368 B match locally. Regular-file mapping is consistent. Bind and recheck the 34 symlinks, correct the dangling-link claim, and fix tool blockers. |
| A2.1 | APPROVE WITH FIXES; hold deletion | Named BVS scratch deployment, not frozen. Transfer-first is appropriate for the remainder, including test data; logs alone do not justify deleting the entire tree. Require a successful, saved, complete transfer receipt and fixed tools. |
| A2.2 | APPROVE WITH FIXES; hold deletion | BVS projects path, sibling of the frozen benchmark, not inside it. The old partC copy is insufficient; require the complete verified transfer, fixed tools, and the promised relocation pointer. |
| A3 | APPROVE WITH FIXES; classification only | /tmp is outside BVS, but this owned temporary bundle is explicitly listed, satisfying the listing condition. It is not frozen. Require exact expanded names, ownership and disposal evidence; no approval of an unbounded wildcard or retrospective execution claim. |

## Evidence tie-out

- Each JSON reports VERIFIED, zero mismatch/missing, empty problems, and no truncation; its file count and bytes agree with CLEANUP_PLAN.md:24-26.
- The three hash lists contain exactly 4,800 / 4,800 / 55,024 rows and the same numbers of unique paths (also unique under case-insensitive comparison). All rows have ordinary 64-hex sha256sum syntax; no spaces, backslashes, colons or traversal components occur in these supplied paths.
- Production lists start `./prod_p0500_20261023T1227Z/` and `./prod_p1000_20261023T1227Z/`. Combined with JSON local_base ending in `claude`, this maps correctly to OUTPUTS.md:18-20. Neither JSON strips a prefix. This validates the laptop mapping, not the planned remote BASE mapping.
- The Others list uses `./<legacy-subfolder>/...`, consistent with its JSON local_base. Symlink-list counts are 0 / 0 / 34. Regular-file hashes do not verify symlink identity, target existence, ownership, or complete remote enumeration.
- verify_against_local.py:11-16,30-46 computes real SHA-256 over each mapped file; the comparisons are sound for these ordinary, unique entries. It does not independently discover files omitted from the remote list.
- OUTPUTS.md:25 still records the older stop/no-go-ahead status. The current review brief explicitly supplies Felipe's later authorization; no renewed authorization is needed merely because that historical line is stale.

## Findings and concrete fixes

1. **blocking — Production list/base mismatch.** CLEANUP_PLAN.md:13,24-25; evidence/nots_hashes/prod_p0500_results.sha256:1; evidence/nots_hashes/prod_p1000_results.sha256:1; transfer/verified_delete.sh:18-20.
   With the stated BASE, the lists address `results/prod_<run>/p...`, rather than the documented run results layout. The intended removal of `results/` in the laptop mapping is not represented in the deletion invocation; expect refusal, not permission to broaden BASE.
   Fix: retain the laptop lists, create explicitly mapped BASE-relative lists removing exactly the matching run prefix, cross-check every mapped hash, record both digests and the mapping, and rerun laptop verification using each local run root before remote recheck/deletion.

2. **blocking — A1 entries can escape the guarded base or reach frozen files.** transfer/verified_delete.sh:12-24; verify_against_local.py:30-36.
   Only BASE is guarded. sha256sum and rm accept absolute/../ entries, and intermediate directory symlinks can lead outside BASE, including into frozen paths. The list hash authenticates bytes, not safe path semantics. The supplied lists contain no traversal, but the tool's safety claim is false.
   Fix: reject absolute paths, dot/dot-dot components, duplicates and unsupported encodings; require each entry to be a regular non-symlink file beneath an immutable canonical BASE with no symlink ancestors, and apply frozen/scope/ownership checks to resolved entries before any unlink.

3. **blocking — Failures can be hidden; tools do not fail closed.** transfer/verified_delete.sh:9,17-28; transfer/remote_pack.sh:9,29-31,41-44.
   Missing pipefail masks find/sort failures; A1's process substitutions cannot propagate their failures even with pipefail. A1 ignores rm/find errors and emits success with leftovers. A2 hashes manifest stdout without checking that manifest generation succeeded; recursive rm may partially delete before failing.
   Fix: use strict error handling plus explicit checked temporary inventory/manifest files and command statuses (including process producers); require all enumeration/hash steps to succeed before mutation; check every deletion and final state, log partial failures, and return nonzero on any failure or residue.

4. **blocking — Verification-to-deletion races permit loss of unverified data.** transfer/verified_delete.sh:17-25; transfer/remote_pack.sh:41-44; transfer/nots_pull.py:212-217.
   A1 rereads a mutable LIST after authenticating it and unlinks paths after hashing. A2 compares a newly computed manifest, then rm -rf removes the whole tree: a file created or changed in between is removed without a verified copy. Empty squeue does not enforce immutability or protect against other sessions.
   Fix: establish exclusive writer exclusion, preserve immutable manifest bytes, pin the target directory identity and recheck the quiesced tree; delete only enumerated verified entries and separately approved links, then remove empty directories. Refuse unexpected entries rather than recursively deleting them.

5. **blocking — A1 deletes every symlink without verifying its approved inventory.** transfer/verified_delete.sh:25; CLEANUP_PLAN.md:26.
   New or changed links are ignored by the extra-regular-file check and removed anyway. The claim that all 34 links are dangling is contradicted by evidence/nots_hashes/home_BVS_Others.symlinks:9-11: ../data and ../code resolve inside Experiments_oct_13, whose regular-file list contains 1,205 data files and 7 code files.
   Fix: preserve/hash the exact link-name/target list, compare it immediately before deletion under the same writer exclusion, remove only matching approved links without dereferencing, and correct the plan. Deleting these link objects does not itself delete their targets.

6. **blocking — Allowed roots exceed BVS scope; ownership is not checked.** transfer/verified_delete.sh:14; transfer/nots_pull.py:27,128-130; transfer/remote_pack.sh:19-22; CHARTER.md:61-62.
   Every child of /scratch/fb31 is accepted, including the explicitly non-BVS qr_data and relocation manifests. A path under fb31 is not proof that every entry belongs to fb31. A1 also permits protected dependencies such as library_portable. Direct canonical frozen targets are refused, but that is insufficient for the broader rules.
   Fix: restrict cleanup to an explicit allowlist of approved A targets; reject protected dependency/pointer/scaffold paths, non-fb31-owned entries and nested mounts; retain canonical freeze checks and reject path-identity changes. Do not infer authorization from --legacy alone.

7. **should-fix — Verification records are not bound to exact input bytes.** verify_against_local.py:25-47; evidence/verify/prod_p0500.json:2-12; evidence/verify/prod_p1000.json:2-12; evidence/verify/home_BVS_Others.json:2-12.
   Reports save a list pathname but no list digest, timestamp or verifier digest; matching counts cannot prove the current list is the one verified. Parsing also lacks strict syntax/confinement and duplicate checks for future inputs. GNU escaped filenames are incompatible with fixed cut -c67- parsing; ordinary spaces alone are handled by the current NUL-delimited rm pipeline.
   Fix: record list/verifier SHA-256, time, exact mapping and counts; strictly validate unique confined paths. Use a consistently parsed NUL-safe format, or explicitly refuse newline/backslash filenames. Keep the authenticated list outside the deletion tree and resolve its absolute path before cd.

8. **should-fix — A2 verifies regular files but silently skips other entry types.** transfer/nots_pull.py:92-102,166-205; transfer/remote_pack.sh:29-31,44.
   The regular-file count/hash gate and unchanged-manifest comparison are present. Symlink metadata is retained in receipts, but links are not copied; other types are skipped and not included in the manifest, yet rm -rf deletes them. The supplied review evidence does not include the A2 receipts or link inventories, so their stated counts/dangling status cannot be independently confirmed here.
   Fix: inventory all entry types, refuse unsupported ones, preserve and explicitly approve link metadata, and supply complete saved transfer/verification/delete receipts. Require zero unexpected skipped entries before delete; keep remote data on any incomplete verification.

9. **blocking — Plan presents execution as already complete, without reviewable execution evidence.** CLEANUP_PLAN.md:9,27-29; NOTS_INVENTORY.md:61.
   This conflicts with the requested pre-execution review. Named inputs establish A1 comparisons and one empty-queue observation, not the actual A2 transfer/delete outcomes or A3 glob expansion/ownership. Those actions cannot be retrospectively certified from this packet.
   Fix: distinguish planned/pending/completed items; before any remaining action, have OPS save exact commands, expanded paths, ownership, tool/list hashes, fresh queue status, timestamps, exit statuses and receipts. For already removed items, provide retained evidence and verify surviving copies; do not rerun deletion to manufacture evidence.

10. **should-fix — Host policy conflict must be reconciled.** CHARTER.md:56-57; NOTS_INVENTORY.md:5; CLEANUP_PLAN.md:29.
    Charter pins loginx3, while inventory says loginx2 and A3 is node-local there. Fix: have HQ reconcile the documented authorized host before OPS connects; enumerate A3 exact owned temporary paths on that approved host. This reviewer made no connection.

11. **should-fix — Disk guard can accept incomplete measurements.** guard.sh:24-31,35-38.
    quota/du pipeline statuses are unchecked, stderr is discarded, and partial du output can be numeric despite a failed traversal. Scratch measurement failure is not rejected; production can also inherit test limit overrides.
    Fix: capture and check each measurement command's status, validate numeric results and all required measurements, and reject test overrides in production. The 7 GiB campaign / 9 GiB home thresholds themselves match the stated guard policy; this guard does not protect deletion scope and is not invoked by remote_pack.sh.

12. **note — B/C retention is appropriately conservative.** CLEANUP_PLAN.md:33-63.
    Non-BVS caches are listed for Felipe; unverified code, paused-relocation data/manifests, frozen benchmarks and their library stay protected. Verified releases may safely remain B because references are unresolved; nothing needs promotion to A for safety. Fix: retain these holds and explicitly list A3 as the already-listed outside-BVS temporary exception.
