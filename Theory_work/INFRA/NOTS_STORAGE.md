# NOTS storage: quota, layout, guard (2026-11-11)

## 1. Quota

| Filesystem | Limit | Notes |
|---|---|---|
| `/home/fb31` (nfs1:/export/nots/home) | **10,240 MB hard** (soft = hard, no grace) | Read with `quota -s -w`. Server-side block accounting runs ~0.6 GB above `du -sh ~`; trust `quota`, not `du`. |
| `/rhf/allocations/ea14` (data191) | shown as 16,384G, 99% full cluster-wide | **Not usable by fb31**: dir is `root:ea14 770`, fb31 is not in group `ea14` (groups: ml75, hpcusers, nots). |
| `/scratch/fb31` (vast) | no per-user quota, **purge policy applies** | Used for all Slurm output and for the cleanup holding folder. |
| `/projects/ml75` | group dir (setgid, group ml75) | Shared with the group; not used here. |

Hitting the hard quota breaks SSH, T3, VS Code server and Slurm output writes.

## 2. What lives where (home, 2026-11-11 after cleanup; `du`)

| Path | Size | Live? | Grows by |
|---|---|---|---|
| `~/.vscode-server` | 3.2 G | yes (server `c4453f8e…` + CLI in use) | new server build every VS Code update (~670 MB each); `extensions/openai.chatgpt` 1.2 G |
| `~/.t3` | 1.5 G | yes (`runtime/versions/0.1.9-nightly.20261110.4465` running) | **T3 nightly builds, ~440 MB each, several per day**; `userdata/logs` ~100 MB (rotated traces) |
| `~/.codex` | 1.2 G | yes (release 0.167.0 running; `current` -> 0.167.1) | new release ~516 MB each; `db-backups` |
| `~/.claude` | 0.4 G | yes | `remote/ccd-cli` 327 MB per version |
| `~/projects` | 301 M | code, never touch | |
| `~/R` | 212 M | libraries, never touch | |
| `~/.local` | 73 M | pip user site | |

Session logs/transcripts are small (`~/.codex/sessions` 132 KB, `~/.claude/projects` 2.7 MB). **The growth is app-build churn (T3, Codex, VS Code, Claude CLI), not logs or simulations.**

## 3. Jobs: nothing writes into `$HOME`

Checked 2026-11-11 with `scontrol show job`:

- W3-P6 smoke `2689423_[1-4]` (RUNNING): WorkDir `~/projects/BVS/theory_w3` (code only); StdOut/StdErr `/scratch/fb31/theory_w3/smk1_v3/slurm/`. OK.
- W3-SCALE `2692676` (PENDING): WorkDir `/scratch/fb31/w3scale`; StdOut/StdErr `/scratch/fb31/w3scale/out/smoke02/slurm/`. OK.

Rules for every job:
1. `#SBATCH --output/--error` and all result/run/checkpoint dirs under `/scratch/fb31/...` (never `$HOME`, never relative paths when submitting from `$HOME`).
2. `--chdir` / WorkDir may be the code tree in `~/projects`, but set `TMPDIR`, R/Python caches, and output roots to `/scratch/fb31/...`.
3. Keep results that must outlive the purge in a copied archive (the ea14 allocation is not available; ask for a group dir if needed).
4. Before submitting a large array, check `quota -s -w` shows > 2 GB headroom.

## 4. Cleanup done (2026-11-11)

Start (HQ report) 10,026 MB; after HQ's deletion of two old VS Code servers 8,714 MB.

| Action | Size |
|---|---|
| deleted `~/.vscode-server/data/CachedExtensionVSIXs` (VSIX download cache, incl. `.trash` 715 MB) | 875 MB |
| deleted Codex release `0.166.0` (not current, not running) | 517 MB |
| deleted T3 runtime `0.1.9-nightly.20261111.4515` (not running, not newest) + ~65 stale `.staging-*` dirs | 439 MB |
| **moved** old Claude CLI `ccd-cli/2.1.321-c6c6b562e837` (not running) to `/scratch/fb31/home_holding_20261111/` | 327 MB |
| deleted obsolete extensions (`openai.codex-audio-26.1021…`, `github.vscode-pull-request-github-0.176.1`, per `.obsolete`) | small |
| guard run: 2 stale `code-*` CLIs, old VS Code logs, 7 old Claude `srv` builds (>7 d), `.cache` files >2 d, 1 rotated T3 trace, 75 old Codex DB backups archived (tgz) to holding | ~176 MB |

Result: quota **8,714 MB -> 7,554 MB** (10,026 -> 7,554 overall). Below the 8.0 GB guard line, but not yet below the ~7 GB target: the rest is live (see section 6).

Holding folder `/scratch/fb31/home_holding_20261111/` (ccd-cli build + Codex DB backup tgz) is subject to the scratch purge; delete when confident.

## 5. Guard

- Script: `~/bin/home_guard.sh` on NOTS. Prints `home usage: X MB of 10240 MB hard quota (Y%)`. Does nothing more unless usage > 8192 MB (override `THRESH_MB=...`); `--force` runs cleanup regardless, `--dry-run` only logs.
- Safe actions only, idempotent, each logged to `~/home_guard.log` (rotated at 200 KB with one `.log.1`, so at most ~400 KB; log write errors ignored; lock file in `/tmp`, so the guard cannot fill home):
  - `~/.cache` files > 2 d, pip/npm caches
  - VS Code: `CachedExtensionVSIXs`, `data/logs` and `CachedData` > 2 d, server builds beyond the newest 2 (and not referenced by a running process), stale `code-*` CLIs (keep newest 1 + running)
  - T3: `.staging-*` > 1 d, runtime versions beyond newest 2 and not running, rotated `server.trace.ndjson.N` > 2 d
  - Codex: releases other than `current` and not running; `db-backups` > 7 d (keep newest 3) archived to `/scratch/fb31/home_holding_<date>/`
  - Claude: `remote/ccd-cli` beyond newest 1 and not running (moved to holding), `remote/srv` > 7 d beyond newest 2 and not running
- Never touches: `~/.ssh`, auth/config/credentials, `~/projects`, `~/R`, run output, anything a running fb31 process references.
- Tested: dry run, then one real `--force` run (freed ~176 MB; live T3, Codex, VS Code processes unaffected).

### Schedule

- **`scrontab` is disabled on NOTS** ("scrontab is disabled on this cluster"). `crontab` exists but ssh lands on different login nodes (loginx1/x3), and per-node cron on shared login nodes is unreliable, so it was **not** installed.
- Fallback prepared but **not submitted**: `~/bin/home_guard_job.sh`, a self-resubmitting Slurm job (1 CPU, 100 MB, 2 min, `commons`, output to `/scratch/fb31/home_guard/`) that re-queues itself with `--begin=now+30minutes` before running the guard. Start: `sbatch ~/bin/home_guard_job.sh`. Stop: `touch /scratch/fb31/home_guard/STOP; scancel -n home_guard`. Not yet tested on a compute node (needs `quota` to work there). Until started, run the guard manually (`ssh nots ~/bin/home_guard.sh`) or start it at the beginning of every session.

## 6. Needs a quiet window (live now, cannot move)

| Item | Size | Action when quiet |
|---|---|---|
| Codex release `0.167.0` (running pid, `current` already -> 0.167.1) | 516 MB | restart Codex app-server, then rerun guard (it will delete 0.167.0) |
| T3 runtime `0.1.9-nightly.20261110.4465` (running t3 server) | 439 MB | restart T3 server onto the newest build, then guard removes the old one |
| VS Code server `69047191…` (newest, kept) vs live `c4453f8e…` | 675 MB | after the client settles on one build, delete the other |
| `~/.vscode-server/extensions/openai.chatgpt-…` (webview 723 MB, bin 430 MB) | 1.2 GB | uninstall the extension on NOTS if the Codex VS Code extension is not used remotely |
| `~/.claude/remote/ccd-cli` live build | 327 MB | in use by Claude Remote |

Doing the first two alone takes quota to ~6.6 GB. T3 nightlies add ~440 MB each, so if auto-update stays on and a guard schedule is not running, usage will climb ~0.9 GB/day.

## 7. Verified commands

```
ssh nots 'quota -s -w'                 # usage vs quota
ssh nots '~/bin/home_guard.sh'         # report (cleanup only if > 8 GB)
ssh nots '~/bin/home_guard.sh --force --dry-run; tail ~/home_guard.log'
```
