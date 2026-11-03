# D74 VSIX erase review

**Verdict: ACCEPT WITH FIXES — do not execute the current script until the blocking finding is addressed.**

Local static review only, 2026-11-02. No server connection or script execution. The unrelated initial housekeeping block is excluded.

- **[note] (a) Confirmed.** The recorded deletion set is exactly these four regular files beneath `/home/fb31/.vscode-server/data/CachedExtensionVSIXs/`:
  - `anthropic.claude-code-2.1.312-linux-x64` — 137,332,422 bytes
  - `github.copilot-chat-0.48.1` — 20,337,888 bytes
  - `openai.chatgpt-26.51021.22027-linux-x64` — 428,092,046 bytes
  - `openai.codex-audio-26.1021.22027` — 1,901,878 bytes

  Total: **587,664,234 bytes**. Reconstructing the four tab-separated listing rows with LF endings and a final LF reproduces `c708bf0627cc2fe99c9a0b5e693e85491e4dcdc7f8386996df17db4d7873b2e5`. The listing reports zero non-fb31 entries and zero open-fd/cwd hits on `loginx2` at 17:34:24Z.

- **[note] (b) Confirmed for stable paths; absolute guarantee qualified below.** `T` and all four names are nonempty literals; quoted array expansion creates four exact operands. `rm -f -- "$T/$n"` has no glob, recursion, or directory operand. The directory is retained. Final-component symlinks are rejected before deletion; `rm` itself would unlink a substituted final symlink rather than follow it. There is no deletion operand under `cli/servers` or `.t3`.

- **[blocking] (c) Fail-closed claim is not fully met.** Missing/different SHA, an initially symlinked/noncanonical target, and initially nonregular/symlink entries are refused. However, `-O` means ownership by the effective UID, not specifically fb31: assert the execution identity is fb31 before relying on it. The `/proc` loop silently ignores failed `readlink` calls and unenumerable fd directories, so an inaccessible fb31 process can evade the advertised open-fd/cwd refusal. Make scan incompleteness a refusal, distinguishing vanished processes/fds from permission or enumeration failures. The `L=$(...)` listing command in both scripts **is byte-identical**, and both hash it with the same `printf` pipeline; that comparison is meaningful.

- **[should-fix] (b–d) Checks and deletion are not atomic.** A process can open a file after the scan, or replace an ancestor directory with a symlink after canonical validation; absolute-path `rm` could then unlink a same-named file outside the reviewed directory. Quiesce relevant writers and/or anchor operations to a validated directory handle. The hash covers names/types/sizes/mtime, not file contents or inode identity. Other login nodes are outside this node's `/proc` scan.

- **[should-fix] Result status can falsely indicate success.** The final `... || echo "ERASE INCOMPLETE"` normally exits zero even on a failed unlink or nonempty result. Return nonzero on incomplete deletion so SSH callers can detect failure.

- **[note] (d) Running-server dependency remains unverified.** The evidence does not establish whether the Oct-28 `code-e646868…` process will later access this cache. As a download cache, deletion is expected to require re-download on future installation/update rather than remove installed server/extension code; this is an operational expectation, not a dependency check. A zero-hit local scan does not establish absence of future access or safety on other nodes. No archive is required by D74; successful quota relief must be checked afterward.

## Round 2

**Verdict: ACCEPT WITH FIXES. Do not execute until the scan error handling below is addressed.**

2026-11-02; static review only. No server connection and no script execution. Line references are to R2 `ops/scaffold/vsix_erase_remote.sh`.

- **Round-1 identity finding: resolved (line 16).** Execution explicitly requires `id -un = fb31`, with a numeric UID/home-owner cross-check; file ownership is explicitly checked as fb31 (line 24).

- **Round-1 fail-closed scan finding: substantially improved, not completely resolved (lines 28, 30, 32, 35).** A failed fd-directory enumeration or cwd read for an extant PID now refuses before deletion. Vanished subshells/fds normally continue, so the script's own short-lived command substitutions do not inherently make every run refuse. However, line 28 conflates failed process-owner `stat` with a successfully identified different owner, and line 32 conflates two failed existence tests with a vanished fd. Permission/I/O failures can also make those tests false. Separate successful ownership mismatch from failed identification; distinguish ENOENT/ESRCH from EACCES/other errors (using an errno-aware helper if necessary), and refuse unknown/incomplete reads of live processes. Do not treat permission denial as disappearance. This closes the remaining fail-open error paths rather than only the common stable-permission case.

- **New operational stall risk: likely in a normal SSH environment, but not proven on this host.** A non-dumpable fb31 `ssh-agent`, or an sshd session child with similarly restricted proc access, can survive the owner filter yet fail `ls /proc/PID/fd`; line 30 then safely exits 3 with nothing deleted. Linux preserves effective ownership of the world-readable `/proc/PID` directory even when protected entries underneath become root-owned; do not assume such a process is filtered out. OpenSSH's agent explicitly disables tracing/dumpability on Linux. Thus persistent inaccessible infrastructure can make every attempt in that session refuse; the evidence's old zero-hit scan does not rule this out. Narrowest handling that preserves the all-process guarantee: retain refusal, diagnose the exact PID, quiesce only an identified optional agent where feasible, or obtain a privileged read-only scan for the specific inaccessible PID tied to its start time. Do not blanket-ignore EACCES, all ancestors, or names such as `sshd`/`ssh-agent`. If an infrastructure exception is operationally necessary, it must be an explicitly accepted weakening of the guarantee, confined to a verified executable and PID/start-time identity, logged, with every other unreadable process still refused. Sources: [Linux proc ownership implementation](https://github.com/torvalds/linux/blob/master/fs/proc/base.c) (`task_dump_owner`, `proc_pid_instantiate`); [OpenSSH agent](https://github.com/openssh/openssh-portable/blob/master/ssh-agent.c) and [tracing implementation](https://github.com/openssh/openssh-portable/blob/V_9_3_P1/platform-tracing.c).

- **Round-1 ancestor-swap finding: adequately addressed for redirection after anchoring (lines 41-43).** Successful `cd`, physical-path equality, and relative `./name` operands keep unlink operations in that cwd even if a later ancestor is replaced. Qualification: this is path validation, not proof of the same directory inode originally listed; replacement at the same canonical pathname before `cd` is not detected. Anchor before listing/validation, or compare directory device/inode identity, if that stronger guarantee is required. Accepted open-after-scan races remain residual.

- **Round-1 incomplete-deletion exit finding: resolved for reported unlink failures/nonempty results (lines 43, 47), with a remaining verification defect (line 44).** `rc=1` or nonzero `left` now exits 1. But `find . -mindepth 1 | wc -l` reports the status of `wc`, and the status is not checked anyway. A failed enumeration producing no output can still yield `left=0` and `ERASE VERIFIED`. Require successful enumeration as well as zero entries; otherwise exit nonzero. Keep verification relative to the anchored cwd.

- **Listing command: confirmed byte-identical.** The complete `L=$(...)` line in R2 and `vsix_list_remote.sh` compares equal as UTF-8 bytes, including its line-ending CR (112 bytes excluding LF); both hash `printf '%s\n' "$L"` identically. The saved evidence records `c708bf0627cc2fe99c9a0b5e693e85491e4dcdc7f8386996df17db4d7873b2e5` for the same four files, totaling 587,664,234 bytes. No remote listing was regenerated.

## Round 3

**Verdict: ACCEPT WITH FIXES. Resolve the deterministic self-hit before execution.**

2026-11-02; local static review only. No server connection or script execution. References are to R3 `ops/scaffold/vsix_erase_remote.sh` (SHA-256 `5fd7eb96eddebc8a5eef3af3d92c037908f4484665b0f365814736123e2cb3bd`).

- **[blocking] New deterministic self-hit (lines 20, 34, 50-57).** Anchoring now changes the shell's cwd to the target before starting Python; Python inherits that cwd. The scan reads both processes' cwd and treats either as an OPEN hit, so even an otherwise clear scan necessarily refuses with nothing deleted. `self_pids = {os.getpid(), os.getppid()}` is defined but never consulted. Narrowly exempt only the known anchoring cwd references of the scanner and its parent shell; retain their fd checks and all checks of other processes. This is distinct from the accepted possible non-dumpable-process refusal.

- **Round-2 fixes confirmed.** The Python scan distinguishes ENOENT/ESRCH from other stat/listdir/readlink errors and otherwise fails closed; the directory is anchored before listing, its device/inode is compared with the target afterward and rechecked with its physical path before deletion; final verification requires successful enumeration and empty output, otherwise exits 1.

- **Byte checks confirmed; prior CR remark corrected.** Direct local byte inspection finds **0 CR bytes in each script**. The complete `L=$(...)` lines are byte-identical, **112 bytes excluding LF**, with no CR. The round-2 claim that those 112 bytes included CR was erroneous; these files are pure LF. No remote listing was regenerated.

## Round 3 — OPS response (2026-11-02)
Blocking R3 finding fixed exactly as prescribed: the python scan skips only the cwd check for its own PID and its parent shell (os.getpid(), os.getppid()); their fds are still checked; every other process keeps the cwd check. One-line change; run under HQ D74 with this note (no fourth round, time box).
