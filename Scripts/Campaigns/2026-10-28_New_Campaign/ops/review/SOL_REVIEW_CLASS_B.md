APPROVE WITH FIXES — do not execute the deletion script until the blocking findings are resolved.

Static, local-only independent review. Read CHARTER.md, DECISIONS.md D7, both scripts, disk_check.sh, the previous guard, and both saved probes. No SSH, cluster contact, or shell-artifact execution. Line numbers below refer to the reviewed files.

1. **[blocking] Shared-home inactivity is not established.**
   Exact lines: `evidence/clsB_delete.sh:9` (DEL), `:13` (loginx2 only), `:20-24` (local process inspection).
   Probe2's timestamp is 2026-10-29T02:58:01Z. Its lines 42-44 say the 585eba7c extension host exited and the server was *waiting before shutting down*, not that the server exited. Lines 84-87 show client disposal, not server termination; lines 98-99 contain no host hints. Older versions likewise have no conclusive server-exit evidence (lines 31-33 and 53-55). Critically, `clsB_probe2.sh:6` checks `pid`, but the listings show `pid.txt`; the actual PID contents were never collected. Local absence on loginx2 cannot exclude another node using these NFS directories. Age and silent logs are insufficient.
   Fix: remove 585eba7c from DEL, and retain any other version whose inactivity is similarly unproven. Establish host-aware termination evidence or a documented, coordinated quiescent interval before reconsidering them. Do not connect to other login nodes or kill processes to obtain that evidence.

2. **[blocking] `in_use()` can return unused after detecting use.**
   Exact lines: `evidence/clsB_delete.sh:20-25`, called at `:36`, `:41`, `:46` as the left side of `&&`.
   With `pipefail`, `grep -qF` may exit on a match while the producer group is still writing; a producer then gets SIGPIPE and the pipeline is nonzero, skipping `return 0`. This affects exe/cwd/fd/maps-only matches that the argv check does not catch. The conditional function calls suppress reliance on `errexit` inside the function. `pgrep` errors are also treated like no match, and unreadable live-process metadata is silently ignored.
   Fix: implement explicit used/unused/unknown results; abort on unknown. Consume the full producer stream (no early-exit grep), check inspection statuses separately, and distinguish vanished PIDs from inaccessible surviving processes. Use literal matching for argv as well. Under the stated `bash -s` launch, the shell argv does not contain the target and pgrep excludes itself, so there is no inherent self-match blocker; incidental monitoring commands may conservatively cause refusal.

3. **[blocking] Ownership and mount gates silently accept inspection failure.**
   Exact lines: `evidence/clsB_delete.sh:34`, `:35`, `:39`.
   In `[ "$(find ... | wc -l)" = 0 ]`, the substitution can print zero despite find failing; the successful outer test discards the pipeline status. `findmnt ... | grep -qF ... && die` similarly treats a findmnt error as no mount; early grep termination can also make a real match fail under pipefail.
   Fix: capture each complete inspection using an assignment with an explicit failure branch, then inspect its output separately. For example, capture `find` output with `|| die`, then require it to be empty. Capture findmnt successfully before checking exact target/descendant boundaries; distinguish grep no-match from errors and avoid early-exit pipelines.

4. **[blocking] Mount protection is incomplete, and the final pip deletion lacks the promised use recheck.**
   Exact lines: `evidence/clsB_delete.sh:35`, `:38-41`, `:43`, `:47`, `:51-52`.
   VS Code gets a mount check, pip gets none. `rm --one-file-system` does not protect a command-line target that is itself a mount, or a same-device bind mount beneath it. Ownership traversal also crosses mounts before the current mount gate. Pip is inspected only before all version deletions; it may become active before line 52.
   Fix: apply the corrected mount-root/descendant rejection to every target before recursive inspection; use non-crossing inspection where appropriate. Revalidate canonical path/type/ownership, mounts, and use immediately before each rm, including pip. Coordinate against new VS Code starts using its actual locking protocol or a verified quiescent interval; a local check alone cannot remove the NFS race. Do not remove shared lock files to force access.

5. **[blocking] The guard's arithmetic accepts overflowing inputs (pre-existing defect).**
   Exact lines: `guard.sh:13`, `:18`, `:22`, `:39-40`.
   The digits-only ADD check does not bound Bash integers. On 64-bit Bash, ADD_MB=9007199254740992 makes multiplication by 1024 wrap negative, allowing an impossible planned addition to pass. Leading zeros invoke octal parsing. Override values are not validated as decimal integers or bounded before arithmetic.
   Fix: validate and normalize decimal inputs before evaluating arithmetic; reject excessive length/range and use checked multiplication/addition. Reject invalid overrides with exit 2, and ensure excessive planned additions refuse. Apply this to parsed usage values as well. No execution was used to validate these cases in this review.

6. **[blocking] The laptop wrapper embeds its argument as remote shell code (pre-existing defect).**
   Exact line: `disk_check.sh:7` — `... guard.sh ${1:-0}` inside the SSH command string.
   A single argument such as `0; <another command>` is interpreted by the remote shell before guard.sh can validate it. Remote validation therefore does not constrain the wrapper to the authorized operation.
   Fix: validate/bound the first argument locally as a decimal integer before SSH and pass only that normalized value. Preserve the remote return code as lines 7-10 currently do. No SSH or injection test was performed.

7. **[non-blocking] One-sided test overrides subtly change the other default.**
   Exact lines: `guard.sh:17`, `:22`.
   Production home limit is 10066329 KiB, but a campaign-only override silently sets home to 9830 MiB = 10065920 KiB, 409 KiB lower. Ordinary numeric overrides still work in static inspection; the explicit opt-in and TEST_LIMITS marker remain. Invalid inputs require finding 5's fix.
   Fix: override each limit independently only when its variable is supplied, retaining the exact production KiB value for the other limit. Verify zero, one-sided and two-sided overrides, unauthorized override refusal, and limit boundaries in the authorized validation environment.

8. **[non-blocking] Preserve CLI metadata; stale names do not establish activity.**
   Exact lines: `evidence/clsB_delete.sh:7-9`, `:47`; `evidence/clsB_probe2_raw.txt:3`, `:8-16`.
   The rm targets leave lru.json and .locks untouched. Existing .locks already contains names with no corresponding version directory in the saved listing, so mere file presence is not evidence of a running server. Stale LRU entries are cache bookkeeping, not proof of a live process; leaving these names is not itself a deletion-safety blocker. Automatic repair/reinstallation behavior for this exact CLI build was not verified from the supplied artifacts. A held lock is different from a stale filename.
   Fix: leave both metadata locations untouched; do not unlink lock inodes while another CLI may hold them. If a later CLI launch encounters a missing installation, use its normal installation workflow rather than broadening this cleanup.

9. **[non-blocking] Target scope and production threshold change are correct.**
   Exact lines: `evidence/clsB_delete.sh:6-10`, `:30-33`, `:38`, `:47`, `:52`; `guard.sh:16-17`, `:29-35`, `:39-42`; `disk_check.sh:6-10`.
   Explicit rm operands are only the three named version directories and /home/fb31/.cache/pip. KEEP versions, top-level code-* binaries, data/, extensions/, ~/.claude/remote, and .t3* are not operands; there are no kill commands. Canonical root checks reject symlink ancestors at check time, and normal rm does not follow descendant symlinks. The remaining mount/use races are covered above.
   Campaign limit is exactly 524288 KiB (0.5 GiB). Home limit is floor(9.6*1048576) = 10066329 KiB, the correct largest integer below 9.6 GiB for quota's 1-KiB blocks. `-gt` permits the campaign ceiling and keeps integer home usage below 9.6 GiB. Ordinary over-limit cases return 1; quota parse and du failures return 2. Scratch has no size threshold; its measurement failure still returns 2 as documented. disk_check.sh preserves the remote status and updates its header; the header updates only for a new log.
   Fix: retain these production constants and explicit operand scope while applying the blocking fixes. Re-review the revised deletion artifact before execution.

Reviewed SHA-256 snapshots:
- evidence/clsB_delete.sh: A242A7A0007B05B145766065FE287414E3807C85F0DAB69B1A05080B793ABD1B
- guard.sh: D2FA5AC9D0E630F5D0ACFDCB66E3CFCFC5C6AB67E858C18E87AF304AEC96160D
- evidence/guard_prev_20261029.sh: 531036630081AC6E48227DABDF132356FF777004E88A9CB3FB7822FBB76FDE3E
- disk_check.sh: 457C73C728BD8FEA7DF87E2197E69445535FC03DB4142703AFABE718E27E692A
