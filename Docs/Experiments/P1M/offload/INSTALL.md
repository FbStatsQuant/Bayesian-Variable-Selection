# Desktop offload — install note (for HQ, on DESKTOP-955G53S)

Owner approval 11-16: primary destination `D:\SMC_Engineering_Department\` (2.8 TB free); hourly pulls through Windows
Task Scheduler. The laptop stays the mirror (same script, its own `-DestRoot` and `-Client laptop`). Rules: POLICIES §12.7
(one connection per pull, nothing bursty) and §12.13 (our data ≤ 70% of the drive).

## What runs where
- **Owls** (already installed by Engineering): `~/SMC_Engineering_Department/crews/offload/serve_pull.sh`. It reads the
  PC's verified list on stdin and streams a tar of the next pending units (oldest first, ≤ 50 GB per pull). It writes only
  `crews/offload/serve.log` and `crews/offload/<client>_verified.txt`. It deletes nothing.
- **Desktop**: `pull_desktop.ps1` (this folder). One ssh connection per pull. Every file is checked against the unit's
  SHA256SUMS, then the unit moves into `D:\SMC_Engineering_Department\records\` with a `verified.json`. Units that fail go
  to `quarantine\`. Logs go to `logs\pull_YYYYMMDD.log`. It skips 03:00–03:15 CT (BNP backups) and runs one pull at a
  time (a lock file). It refuses (exit 3) if our data plus the pull cap would pass 70% of D: or leave < 15% free.
- Freeing NOTS scratch is done later by the Engineering crew from Owls, never by this script.

## Steps (≈ 10 min)
1. Copy `pull_desktop.ps1` to `D:\SMC_Engineering_Department\scripts\pull_desktop.ps1`.
2. Add this block to `C:\Users\<you>\.ssh\config`, **between the markers, without touching the existing `owls` / `nots`
   entries**. Copy `HostName`, `User`, `IdentityFile` (and `ProxyJump`, if your `owls` entry has one) from your existing
   `owls` entry:
   ```
   # >>> SMC-Engineering offload (Engineering Dept; edit only inside these markers) >>>
   Host smc-eng-owls
       HostName <as in your owls entry>
       User fb31
       IdentityFile <as in your owls entry>
       BatchMode yes
       ConnectTimeout 30
       ServerAliveInterval 30
   # <<< SMC-Engineering offload <<<
   ```
3. Test, in PowerShell:
   `ssh smc-eng-owls true` (no prompt expected), then
   `powershell -NoProfile -ExecutionPolicy Bypass -File D:\SMC_Engineering_Department\scripts\pull_desktop.ps1 -DryRun`,
   then the same without `-DryRun`. Expected: the log shows `verified _offload_test/hello: 1 files`, and
   `D:\SMC_Engineering_Department\records\_offload_test\hello\verified.json` exists. A second run says `nothing pending`.
4. Task Scheduler: a task "SMC Engineering offload pull", hourly at minute 20, run whether the user is logged on or not.
   Do not run it if it is already running. Stop it after 2 h. Action:
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\SMC_Engineering_Department\scripts\pull_desktop.ps1`.
   Minute 20 never overlaps the BNP 03:00–03:15 window; the script skips that window anyway.
5. Tell Engineering the result of step 3 (log lines). Engineering then reads `crews/offload/desktop_verified.txt` on Owls
   in the daily machines line.

## Notes
- The script was written on Owls, which has no PowerShell. The Owls side (`serve_pull.sh`) is tested (pending selection,
  cap, CRLF lists, guard). **The PowerShell side is untested until step 3**: please send the step-3 output either way.
- If step 3 ends with exit 5 (tar), something on Owls printed text into the ssh stream (e.g. a login message in a
  non-interactive shell); send Engineering the log and the first bytes of the `.tar`.
- Exit codes: 0 ok / nothing / skipped; 3 disk guard; 4 ssh; 5 tar; 6 a unit failed verification; 7 unexpected error.
- Unit = a folder under Owls `records/` holding a `SHA256SUMS` file (sha256sum format, paths relative to the unit). NOTS
  job epilogues and the Owls crew produce these (OFFLOAD.md steps 1–2).
