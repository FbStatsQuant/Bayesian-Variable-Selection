APPROVE — the reviewed pip-only script may run as `ssh nots 'bash -s' < evidence/clsB_delete_pip.sh`.

Independent R3 review: local reads and static analysis only; no SSH, NOTS contact, script execution, or computational validation. Read R1, R2, the R2 response, and all seven requested evidence/script files. Line references below are to evidence/clsB_delete_pip.sh v3.1.

- **F1: moot for this artifact.** Lines 8-9,82-83 fix the sole rm operand to /home/fb31/.cache/pip. VS Code appears only in comments; no version, lock, binary, or other VS Code path is an operand. This approval does not extend to the archived VS Code deletion script.
- **F2: closed as a blocking issue for this cache-only operation, with the limitations below.** Lines 43-64 retain used/unused/unknown handling and abort on surviving unreadable processes outside E1-E3. Argv is still checked for exempt processes. E1 is consistent with the saved SSH ancestry; E2 uses an actual parent relationship plus root-owned parent identity, rather than the rejected blanket /proc-owner exception. Probe4 identifies the observed unreadable processes; the first dry run refused (sd-pam), and dry2 reports the corresponding E1/E2/E3 exemptions and PASS.
- **F4: resolved for the requested local recheck.** Lines 66,75 put the captured, failure-checked pip-process test inside gate. Gate runs at 79 and again at 82, before rm at 83. Dry2 demonstrates the first gate only; the second invocation is verified statically. A new process, imported pip API, or another node can still escape this snapshot check. That residual race is acceptable for this explicitly approved regenerable cache; an affected concurrent installation can lose cache entries or need a retry/download. It is not evidence of global non-use.

**Nonblocking findings / precise hardening suggestions**

1. **[low; F2 qualification] E3 is a heuristic, not unforgeable provenance.** Lines 31-35: a user-manager service started within the same 100-tick window could present argv '(sd-pam) ' and become non-dumpable. Kernel start time is genuine but does not uniquely identify the PAM helper. Thus E3 can, in principle, conceal cache use; the response's absolute claim is too strong. Fix: document this accepted cache-only heuristic; for any future artifact requiring proof of non-use, remove E3 and refuse unknown unless stronger identity evidence is available. No fix is required before this pip-only run because the plausible consequence stays within the approved disposable cache.
2. **[low; robustness] Raw stat field splitting is not general.** Line 18 (also clsB_probe4.sh:7): awk '{print $4}' assumes comm contains no whitespace. The supplied dry-run ancestry is plausible, but a differently named ancestor could truncate or misdirect the chain; a failed while numeric test need not terminate the script under errexit. Fix: read stat with an explicit failure branch, strip through its final ') ' as at line 26, extract suffix field 2, validate it as a decimal PID, and die on malformed data. This is nonblocking for the fixed launch and observed ancestry; do not describe E1's parser as universally reliable.

**Bash and deletion scope**

- Lines 26,34 correctly parse suffix field 2 as PPid and field 20 as starttime after stripping the final ') '. The E3 numeric regex precedes arithmetic.
- At line 59, `why=$(sys_helper ...)` is an elif condition: a nonmatch does not trigger errexit. sys_helper uses explicit failure returns and ultimately returns 1 on rejection, so conditional errexit suppression does not turn rejection into exemption.
- Lines 66,75 explicitly exit on pgrep failure despite the function being tested by if. Lines 69-76 reject failed inspections/unknown use; the full-output matching avoids the former grep/SIGPIPE defect.
- Lines 69-74 check canonical directory, ownership, and mount boundaries; rm has one quoted fixed operand, --, and --one-file-system. Descendant symlinks are unlinked rather than followed. There is no command intentionally removing anything outside /home/fb31/.cache/pip. As with the prior review, check-to-rm namespace/mount replacement is not atomically excluded; no such concurrent replacement is evidenced here.
- Saved background evidence reports 130724 KiB, no pip argv match, unset cache overrides/no pip.conf, and newest write 2026-10-21. These support proportionality, not a guarantee against future activity.

Blocking items: none for the reviewed pip-only artifact.
Reviewed source SHA-256: DD3C18F3B37B1F6CEBE9ADF51FBBACF1540D99AA8790054C87761C5DAE62B2A0.
