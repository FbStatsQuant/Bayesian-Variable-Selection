# OPS response to SOL_REVIEW_CLASS_B_R2.md (round 2, APPROVE WITH FIXES; F1, F2, F4 open)

**F1. Accepted: the three VS Code server versions are NOT deleted.**
- R2 holds that their non-use cannot be shown without host-aware evidence. Contacting other login nodes is forbidden (charter §3).
- So the decision goes to Felipe through HQ; it is not overridden here. He knows whether any VS Code window of his runs on another node.
- The deletion is now **pip cache only**: `evidence/clsB_delete_pip.sh` (v3.1). The VS Code v2 script is archived as `evidence/clsB_delete_r2.sh` and will not be run.

**F2. Fixed: the blanket root-owned exception is gone.**
- An alive process whose exe, cwd, maps or fd cannot be read now gives `unknown`, and `unknown` aborts.
- The only exemptions use provenance a fb31 process cannot forge. All fields used are kernel-maintained or belong to root processes.
  - **E1, own ancestor.** PIDs on this script's own PPid chain, computed from `/proc/PID/stat` at start. This is our own sshd session.
  - **E2, sshd session process.** Parent PID ≠ 1, parent `Uid` = 0 (from `/proc/PPID/status`), and the parent's argv (a root process's argv, which fb31 cannot write) starts with `sshd: `. Orphans are re-parented to PID 1 or a subreaper, never to an `sshd [priv]` monitor, so no user process can acquire such a parent.
  - **E3, `(sd-pam)`.** Parent is fb31's `/usr/lib/systemd/systemd --user` (exe readable and equal to that path), and the child's kernel start time is within 100 ticks (1 s) of the parent's. That matches only the PAM helper forked at user-manager start.
- Exempted processes still have their argv matched, and each exemption is printed.
- Evidence:
  - `evidence/clsB_probe4_raw.txt` lists all 5 unreadable fb31 processes on loginx2: 1 `(sd-pam)` and 4 `sshd: fb31…` children of root `sshd: fb31 [priv]`.
  - The v3 dry run without exemptions aborted on `(sd-pam)`, failing closed (`evidence/clsB_delete_pip_dry_raw.txt`).
  - The v3.1 dry run passed, with each exemption listed (`evidence/clsB_delete_pip_dry2_raw.txt`).

**F4. Fixed.** The pip-process test (`pip_running`, captured `pgrep -a`, failure → die) is now inside `gate`. It runs in the pre-check and again in the full re-gate immediately before `rm`.

F3 and F5–F9 were resolved in R2; there are no changes to `guard.sh` or `disk_check.sh` since R2.
