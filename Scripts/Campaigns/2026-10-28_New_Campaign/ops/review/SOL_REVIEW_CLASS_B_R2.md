APPROVE WITH FIXES — deletion remains blocked by F1, F2 and F4; revised guard/wrapper are acceptable by static review.

Independent round-2 review, local files only, read in the requested order. No SSH, NOTS contact, shell-artifact execution or runtime validation. Line numbers refer to v2 unless specified.

- **F1: open [blocking].** `evidence/clsB_delete.sh:4-5,12,14,58`; `review/OPS_RESPONSE_CLASS_B_R1.md:8,17-21,38`.
  Six hours without an mtime change is a documented age threshold, not the documented, coordinated quiescent interval requested in R1. Reads/execution need not change mtime; noatime removes even the access-time signal. It does not exclude an already-running process elsewhere or prevent a new start.
  Probe3 fixes the pid.txt collection, but absence of those PIDs on loginx2 says nothing about their originating host. "New EH opened, aborting shutdown" proves cancellation, not successful automatic shutdown; "waiting before shutting down" is still not server-exit evidence. Activity/logging outside the target tree is also possible (probe1:15,17).
  **585eba7c remains unacceptable for deletion. The other two (2d0b7506 and 6d62b1d5) also may not proceed on this evidence:** their older timestamps improve plausibility, not host-aware proof. An orphaned live process losing program files would still violate the unused-version rule.
  Fix: retain all three until existing permitted evidence establishes termination/no use, or document and enforce a coordinated interval that excludes existing users and new starts across users of this shared installation. Do not contact other nodes or kill servers to obtain it. If that cannot be established, omit these versions from deletion.

- **F2: open [blocking], with the Bash/SIGPIPE defect resolved.** `evidence/clsB_delete.sh:25-47`, especially `:41-43`.
  Each normal used/unknown branch prints its state and bare `return` inherits echo's successful status; unused ends with successful echo. Thus `u=$(in_use "$p")` at :59 succeeds and the separate equality test rejects used/unknown. Captured producer failures are handled explicitly even when command substitution clears errexit. There is no early-exit match pipeline or regex interpretation of the target path.
  However, root ownership of /proc/PID identifies an inspection restriction, not an sshd-only identity. A same-user process can become non-dumpable; the supplied probe only establishes readability of particular VS Code processes at that moment. If such a process's argv does not expose the target, :42 bypasses unavailable exe/cwd/maps/fd evidence and :47 can incorrectly report unused. The claim that this exception cannot hide VS Code use is unproved.
  Fix: remove the blanket root-owned exception and return unknown for surviving unreadable processes. Any necessary exception needs independently trustworthy identity/provenance evidence excluding target use; argv or /proc ownership alone is insufficient.

- **F3: resolved.** `evidence/clsB_delete.sh:52-58,68`.
  Canonical path, ownership, mount, traversal and du inspections now capture output with explicit failure branches. Mount matching uses exact target/descendant boundaries and consumes the full findmnt output. No successful outer test masks a failed inspection.

- **F4: open [blocking], mount/re-gate portions resolved.** `evidence/clsB_delete.sh:55-59,63-70`.
  Every target, including pip, receives mount rejection before -xdev recursive ownership/quiescence inspections and a full gate immediately before rm. gate is called directly at top level (:64-65,69), not in a conditional/substitution; die's exit 3 exits the main script. Its here-string mount loop also runs in that shell.
  Shared-home coordination remains F1. Separately, the pip-process check at :63 is only preflight: a pip process starting during version deletions can reach the final pip rm without another pip-argv check. Generic in_use need not see an implicit cache path between file accesses.
  Fix: factor the captured, failure-checked pip-process test into gate for PIP so it also runs at :69; coordinate against new cache users through deletion. This narrows the local race without claiming to solve F1.

- **F5: resolved.** `guard.sh:14-20,25-30,36,43-44`.
  Anchored MB regex accepts 0 or 1..9999999 with no leading zeros; KB regex permits at most 15 decimal digits. Maximum multiplication and usage-plus-addition remain below signed 64-bit range. Invalid nonempty overrides return 2; excessive valid planned additions refuse under production limits. Runtime boundary checks were not repeated here.

- **F6: resolved.** `disk_check.sh:7-10`.
  Local bounded decimal validation precedes SSH; only validated digits enter the remote command. Injection/leading-zero inputs return 2 and remote status is preserved. No SSH was invoked in this review.

- **F7: resolved.** `guard.sh:18-27`.
  Each nonempty override requires explicit opt-in and changes only its own constant; zero is nonempty and accepted. One-sided overrides retain the other's exact production KiB value. TEST_LIMITS marks applied overrides; empty/unset values leave defaults unchanged.

- **F8: resolved.** `evidence/clsB_delete.sh:11-13,67-70`.
  lru.json and .locks remain outside explicit rm operands; no lock inode is unlinked by this artifact. Their presence is not treated as proof of live use.

- **F9: resolved.** `evidence/clsB_delete.sh:11-13,17-18,67-74`; `guard.sh:18-19,43-46`.
  Explicit scope, KEEP checks, no-kill rule and loginx2 restriction remain intact. No operands name ~/.claude/remote, ~/.t3 or ~/.t3-recovery. Production limits remain 524288 and 10066329 KiB, compared with -gt; scratch remains informational.

**New findings:** none beyond the revised F2 exception and residual F1/F4 issues recorded above. Approval of guard/wrapper does not authorize execution of the deletion artifact.

Reviewed SHA-256 snapshots:
- evidence/clsB_delete.sh: 7E1AA648DFBB43FDFA12DAC4708161639145770B1C684B232BE03F427E62D713
- guard.sh: 29C1D07CB9E1DDFA51C74139A8EE0C0ED6D9E8DB46433DA6D22092023350D897
- disk_check.sh: D32D5957DBBAFD06543C8A15A52C4F469F640EEBDF8B41EECEED43F0F5D98FAF
- evidence/clsB_probe3_raw.txt: 0FD37F1901A68A315C9E6CEBE7C96249A166AAFAC857D55BF4F39E83FD2E88F3
