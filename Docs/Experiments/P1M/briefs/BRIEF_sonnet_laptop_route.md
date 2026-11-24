# BRIEF — laptop transfer route setup (one-off agent on the owner's laptop "Felipe_Bedoya", Windows). SMC - Engineering, 2026-11-15

You run on the owner's personal Windows laptop. HQ and the owner approved this setup (POLICIES §12 rule 3). **Touch nothing
else on this machine**: no other folders, no settings changes, no installs. If something must be installed, STOP and say
so in your report; do not install it. Use only built-in tools: Windows OpenSSH client (`ssh`, `ssh-keygen`, `scp`) and
PowerShell (`Get-FileHash`). Calm NOTS use (owner rule): one ssh connection at a time, no loops of logins, no scans.

## Phase 1 (do now; then stop and report)
1. Check that `ssh`, `ssh-keygen` and `scp` exist (`Get-Command`). Do not install anything.
2. Create a dedicated key: `ssh-keygen -t ed25519 -C "laptop-bvs-transfer" -f $env:USERPROFILE\.ssh\id_ed25519_bvs_transfer -N '""'`.
   Create `.ssh` only if missing. If the key file already exists, do not overwrite it: report it.
3. Known hosts: append exactly this line (the NOTS host key, verified from Owls) to `$env:USERPROFILE\.ssh\known_hosts`,
   only if no line for notsx.crc.rice.edu is present:
   `notsx.crc.rice.edu ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBMqg8mec5lIJ17rAxtc/c4NMlG75VJKQAk9Vz7ixuN+`
4. Append a host entry to `$env:USERPROFILE\.ssh\config` (create the file if missing; never change existing entries; if a
   `Host nots` entry already exists, stop and report):
   ```
   Host nots
       HostName nots.rice.edu
       HostKeyAlias notsx.crc.rice.edu
       User fb31
       IdentityFile ~/.ssh/id_ed25519_bvs_transfer
       IdentitiesOnly yes
       ServerAliveInterval 60
   ```
   Windows OpenSSH does not support ControlMaster (no Unix sockets), so it is left out. The pull script uses a single
   connection per step instead. Say so in the report.
5. Create the destination folder `C:\Users\felip\Documents\SMC_Engineering_Department\` with the subfolders `incoming\`,
   `logs\` and `scripts\`. Nothing outside it.
6. Write `scripts\pull.ps1` (PowerShell). Parameters: `-Remote` (an absolute path on NOTS, file or directory), `-Name`
   (a destination subfolder under `incoming\`), and the switch `-DeleteSourceAfterVerify` (default OFF). Behaviour:
   - log every step with a timestamp to `logs\transfers.log`;
   - fetch a SHA-256 manifest from NOTS **first**, in one ssh call: for a directory,
     `cd <parent> && find <dir> -type f -print0 | sort -z | xargs -0 sha256sum`; for a file, `sha256sum`. Save it as
     `incoming\<Name>\SHA256SUMS_nots.txt`;
   - copy with `scp -r -p nots:<Remote> incoming\<Name>\` (one call);
   - verify every file with `Get-FileHash -Algorithm SHA256` against the manifest (paths relative; compare lowercase hex).
     Write `incoming\<Name>\verify.txt` and log `OK n files` or `FAILED k of n`;
   - if and only if all files verify AND `-DeleteSourceAfterVerify` was given: ask for an interactive "yes"
     (Read-Host), then remove the source on NOTS with one `ssh nots rm -rf -- '<Remote>'` call, and log it. Otherwise never
     delete anything anywhere;
   - exit code 0 on success, non-zero on any failure.
7. Print the **public** key (`id_ed25519_bvs_transfer.pub`) in your report, so that the Engineering manager can authorise it
   on NOTS. Then STOP and report Phase 1.

## Phase 2 (only when the Engineering manager messages you that the key is authorised)
- Run `ssh nots hostname` once.
- Run `scripts\pull.ps1 -Remote /home/fb31/SMC_Engineering_Department/crews/laptop_route/test/hello.txt -Name test`
  (the manager creates that tiny file). Report the log lines and the verify result.
- Do not delete the source (no switch).

## Report (each phase): at most 10 lines
Tools found; files created (full paths); anything already present that you did not change; the public key line
(phase 1); the test result (phase 2); and anything that would need an install.
