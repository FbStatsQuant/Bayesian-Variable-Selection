# OPS response to SOL_REVIEW_CLASS_B.md (round 1, APPROVE WITH FIXES)

Revised artifacts: `evidence/clsB_delete.sh` (v2; v1 kept as `evidence/clsB_delete_r1.sh`), `guard.sh`, `disk_check.sh`.
New read-only evidence: `evidence/clsB_probe3.sh` / `evidence/clsB_probe3_raw.txt` (2026-10-29T03:05Z).

**F1 (shared-home inactivity). Partly accepted. All three versions stay in DEL, behind a quiescence gate.**
- Probe 2 did check `pid` instead of `pid.txt`; probe 3 reads `pid.txt`. Values: 2d0b7506 → 1598664, 585eba7c → 1543178, 6d62b1d5 → 162917. None is alive on loginx2.
- Other nodes cannot be inspected (charter §3). So v2 uses the reviewer's alternative, a documented quiescent interval. Every target must have **no mtime change anywhere inside it for ≥ 360 min**, checked in `gate()` before any deletion and again right before its own rm. (/home is mounted `noatime`, so only mtime is usable.)
- Probe 3 measured the last write per version:

  | Version | Last write (UTC) | Quiet for | Last log line |
  |---|---|---|---|
  | 2d0b7506 | 2026-10-23 00:23Z | 6 days | client disconnected gracefully, EH exited |
  | 6d62b1d5 | 2026-10-21 09:57Z | 7.5 days | — |
  | 585eba7c | 2026-10-28 16:25Z | 10.7 h | "Last EH closed, waiting before shutting down" |

- Why 585eba7c is safe after 10.7 h of silence:
  - It runs with `--enable-remote-auto-shutdown`, and its log already shows that cycle working ("New EH opened, aborting shutdown" at 11:18).
  - A server still alive and in use would have logged every new connection or extension host to this `log.txt`. It has written nothing for 10.7 h.
  - The client moved to Stable-2c33b50… at 11:25 (new lock, new server dir, new log dirs). This is a VS Code client update replacing 585eba7c.
- Residual risk is bounded. At worst, an orphaned, client-less process on another node loses its program files. VS Code user state (`data/`, `extensions/`) is not touched, and Felipe approved deleting the whole folder.
- `lru.json` and `.locks` are left untouched (F8).

**F2 (in_use). Fixed.**
- `in_use` is tri-state: used / unused / unknown, and the gate aborts unless the answer is `unused`.
- For every fb31 process it captures argv, exe, cwd, maps and fd targets into a variable (no early-exit pipeline), then matches the literal path with `[[ == *"$p"* ]]`.
- A process that vanished is skipped. A process that is alive but unreadable gives `unknown`, with one exception: non-dumpable processes (`/proc/PID` owned by root, e.g. the sshd session helper). Their argv is still matched and they are listed on stderr. VS Code server processes are ordinary dumpable user processes (probe 1 read their exe and cwd).
- A `pgrep` failure gives `unknown`.

**F3 (inspection failures). Fixed.**
- Every inspection (`readlink`, `stat`, `findmnt`, owner `find`, quiet `find`, `du`) is captured by assignment with an explicit `|| die`, then tested separately.
- The mount check compares the captured `findmnt` targets for exact equality or the `$p/` prefix.

**F4 (mounts / pip recheck). Fixed.**
- `gate()` (plain dir, canonical, owner, mount at/under, foreign owners with `-xdev`, quiescence, use) applies to all four targets, pip included.
- It runs once for all targets before any rm, then again immediately before each rm, pip included.
- A pip-process check uses captured `pgrep -a` output.
- On the NFS race with a new VS Code start: a new client would start one of the KEEP versions, or download a new one. It would not start a version that is 6+ days old or one it replaced 10.7 h ago, and the quiescence gate is re-run right before each rm.

**F5 (guard arithmetic). Fixed.**
- `PLANNED_ADD_MB` and both test overrides must match `^(0|[1-9][0-9]{0,6})$`: decimal, no leading zeros, < 10^7 MB, so no octal parsing and no overflow.
- Parsed KB values must match `^(0|[1-9][0-9]{0,14})$`.
- Local tests: `007`, `99999999`, `1;id`, `-5` → rc 2; override without opt-in → rc 2; override `01` → rc 2.

**F6 (disk_check injection). Fixed.** The argument is validated locally with the same regex before ssh. Tests: `"0; id"` → rc 2 with no ssh; `08` → rc 2.

**F7 (one-sided overrides). Fixed.**
- Each override replaces only its own limit; the other keeps its exact production KB value.
- The TEST_LIMITS marker now prints KB.

**F8.** Agreed: no metadata is touched.

**F9.** No change.
