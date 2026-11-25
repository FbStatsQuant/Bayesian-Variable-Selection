# CREW — daily machines check (design; machines crew, leg 1)

> **Scope rule (owner via HQ, 2026-11-15):** Engineering works only inside `SMC_Engineering_Department` on each machine
> (plus its NOTS scratch link). Everything else in `/home/fb31` on Owls or NOTS is **out of scope**: not inventoried,
> moved, cleaned or touched. The only exceptions are the HQ-approved SMC-BVS moves and the home guard. Out-of-scope rows
> below are withdrawn.

> For the daily crew this means: checks and cleanup **only inside the department folders**. Machine-wide metrics stay
> (Owls `df -h /`, NOTS home quota line) as read-only numbers. The home guard keeps running as before. No scans of `/tmp`
> or of other `/home/fb31` folders.


SMC - Engineering, Opus 5.5 helper, 2026-11-15. **Design only, nothing is installed.** The crew script would live at
`${ENG_ROOT_OWLS}/crews/daily_check.sh` and run from Owls. It writes its log to `${ENG_ROOT_OWLS}/crews/logs/daily_<date>.md`.
Roots and terms are as in `REORG_PLAN.md` §0. Inventory baseline: `INVENTORY.md`.

## 0. Conduct (owner rule, POLICIES §12 rule 7: "be chill, do not swarm")

- NOTS sees calm, ordinary usage. **One `ssh nots` call per daily run** (the multiplexed ControlMaster connection),
  never parallel, never backgrounded, never in a loop. All remote commands are batched into that one heredoc and run with `nice`.
- At most one `du` at a time, each with `timeout 120`. No recursive `find` over all of scratch: only depth-limited
  listings and `du -s` of known top-level folders.
- `squeue`/`sacct` once per run (well under the 5-minute limit).
- No unusual tools or scans on NOTS (no `lsof`, `ps` of other users, port or file-system scans). Anything that might look
  odd to Rice IT is left out and reported instead.
- Owls: `nice -n 19`, `ionice -c3`, `TMPDIR=${ENG_ROOT_OWLS}/tmp/<date>-crew-daily/`, removed at the end of the run.
- Once a day, at a quiet hour (suggested 07:30 CT, before the morning brief). Started by HQ's scheduler, not a login loop.

## 1. What the daily check runs

### 1.1 NOTS (one ssh call, read-only except the deletions allowed in §2)

| Check | Command (inside the single ssh call) | Report |
|---|---|---|
| Home quota | `quota -s \| grep -A1 export/nots/home \| tail -1` (exactly this line; the last line of plain `quota -s` is another filesystem) | MB used of 10,240; **WARN ≥ 7,000 MB; GUARD ≥ 8,192 MB → §3** |
| Queue | `squeue -u fb31 -h -o '%i %j %T %Z'` | jobs and WorkDirs: these paths are IN USE today; nothing under them is touched |
| Scratch tree vs INDEX | `ls -1 /scratch/fb31/SMC-BVS/{runs,archive,slurm_out}` and `ls -1 ~/SMC-BVS/{_local/*,_wt}` (depth 2) compared with `~/SMC-BVS/INDEX.md` (NOTS ROOT, REORG 11-25) | folders on disk without an INDEX row, and INDEX rows whose folder is missing |
| Stray folders (scratch) | `ls -1A /scratch/fb31` compared with the allowlist {`SMC-BVS`, and not ours: `BQTF`, `qr_data`, `.claude-science`, `qr_small_del2_MOVED.md`, `scr_backups_MOVED.md`, `scr_onizuka_MOVED.md`, `cksum_units.sh`, `del_unit.sh`, `mkchunks.sh`, `mkunits.sh`} (REORG 11-25) | any new name = **stray**: report with size, mtime, owner guess |
| Stray folders (home) | `ls -1A ~` compared with the inventory list (INVENTORY §3.1) | new top-level names, and any SMC-BVS output in home (names matching `run*`, `out*`, `slurm*`, `*.rds`, `*.out`) |
| Home growth | `timeout 120 nice du -s ~/.vscode-server ~/.t3 ~/.codex ~/.claude` one at a time, `sleep 5` between them | per-item MB and day-on-day change (app-build churn ≈ 0.4–0.9 GB/day when auto-update is on) |
| Scratch size | `timeout 120 nice du -s /scratch/fb31/SMC-BVS` | total, and `tmp/` size |
| Department tmp | `find ~/SMC-BVS/_local/tmp -mindepth 1 -maxdepth 1 -mtime +7` | leftovers > 7 d (deleted under rule N-T1 when their job is gone) |
| Home guard | `tail -3 ~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.log` | last guard run and its result |

### 1.2 Owls

| Check | Command | Report / threshold |
|---|---|---|
| **Root filesystem** | `df -h /` (and `df -h /home` for context) | **ALERT above 85% use** (on 11-15 at 20:30 CT it was already **87%**, 9.6 G free; `/` holds `/tmp` and filled up on 11-15 ~20:19). ALERT goes to HQ in the morning brief, at once if ≥ 95% |
| Owls footprint | `du -sh` (nice 19) of `${ENG_ROOT_OWLS}/{tmp,bench,crews,logs,staging}`, `/home/fb31/BVS-wt/*` (`--exclude=.git`), the main checkout | sizes and day-on-day change; worktree branch and last commit (`git -C`) |
| Strays in `/home/fb31` | `ls -1A /home/fb31` compared with the known list (INVENTORY §4) | new SMC-BVS-looking names (`p1m_*`, `*bvs*`, `*smc*`, `w3*`, `g0*`) = **stray**; the owner of the folder gets a note; Engineering strays go to `${ENG_ROOT_OWLS}` |
| `bvs_tmp` | `find /home/fb31/bvs_tmp/{theory,ci,engineering} -mindepth 1 -maxdepth 1 -mtime +7` | report folders untouched > 7 d to their owners (Theory, CI). Engineering keeps nothing there any more: anything under `bvs_tmp/engineering/` is reported as an Engineering stray |
| Department tmp | `find ${ENG_ROOT_OWLS}/tmp -mindepth 1 -maxdepth 1 -mtime +7` | leftovers > 7 d (rule O-T1) |
| `/tmp` SMC-BVS items | §4 | report; remove only under rule T2 |
| INDEX consistency | `ls -1 ${ENG_ROOT_OWLS}/{bench,staging}` compared with `${ENG_ROOT_OWLS}/INDEX.md` | missing rows or missing folders |

## 2. What the crew may delete automatically, and what it only reports

**Deletes automatically (only these, each logged with path, bytes, rule id and the check that cleared it):**

| Rule | Where | What | Conditions (all must hold) |
|---|---|---|---|
| N-T1 | `~/SMC-BVS/_local/tmp/<entry>` | job TMPDIR leftovers | mtime > 7 d; the entry's name is a Slurm job id not in `squeue -u fb31`, or a dated job folder whose job is not running; not a symlink target of anything in `runs/` |
| N-T2 | inside `/scratch/fb31/SMC-BVS/runs/**` and `~/SMC-BVS/_wt/**` | named compile caches only: `.cpp_cache/`, `__pycache__/`, `*.o` beside a built `.so` | parent run not in `squeue`; mtime > 7 d; frozen code trees under `code/` keep their sources (only the cache folder goes) |
| O-T1 | `${ENG_ROOT_OWLS}/tmp/<entry>` | job TMPDIR leftovers | mtime > 7 d; no process has a file open or its cwd there (`lsof +D <entry>` empty, Owls only); entry is not today's crew folder |
| O-T2 | `${ENG_ROOT_OWLS}/**` | named compile caches: `.cpp_cache/`, `__pycache__/`, `Rtmp*` inside `tmp/` | as O-T1 |
| T2 | Owls `/tmp` | clearly BVS-named items (§4) | all §4 conditions |

**Only reports (never deletes):** anything outside the department `tmp/` folders and the named caches; anything under an
IN USE path; home files on NOTS (that is the guard's job, §3); `runs/`, `archive/`, `data/`, `results/`, `bench/`,
`staging/` content; other departments' folders (`bvs_tmp/theory`, `bvs_tmp/ci`, worktrees); UNKNOWN items; anything in
`~/projects/BVS`; the excluded `.../SMC_BVS_v3_history_Oct2026/deploy/` and `/projects/ml75` (never listed inside);
strays (reported to their owner, moved only by a REORG step with HQ's go).

A dry-run flag (`--dry-run`) prints the deletions without doing them; the first week runs in dry-run only.

## 3. The 8 GB guard action (NOTS home)

- **≥ 7,000 MB (WARN):** report the line and the per-item growth in the morning brief.
- **≥ 8,192 MB (GUARD):** in the same single ssh call, run the existing guard: `~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.sh` (it acts only above
  8,192 MB, safe actions only, logged to `~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.log`; it never touches `~/.ssh`, credentials, `~/projects`, `~/R`,
  run output, or anything a running fb31 process references). Then re-read the quota line once.
  - If still ≥ 8,192 MB: **report to HQ at once** (not just in the brief) with the top items; the usual remaining live
    items need a quiet window and a restart (NOTS_STORAGE.md §6: Codex `0.167.0`, old T3 runtime, second VS Code server
    build, the `openai.chatgpt` extension). The crew does not restart services or delete live builds.
  - **≥ 9,500 MB:** report at once as a big problem (the 10,240 MB hard quota breaks ssh, T3, VS Code server and Slurm
    writes) and recommend that no new job be submitted until it is fixed.
- The guard's holding path is `/scratch/fb31/SMC-BVS/archive/home_guard/holding_<date>/` (REORG 11-25). The crew reports holdings older
  than 14 days; deleting them (regenerable binaries only) needs HQ's OK.
- The guard is not scheduled on NOTS (scrontab disabled, the self-resubmitting job never submitted). Running it from this
  daily check, inside the one ssh call, is the schedule; nothing else is installed on NOTS.

## 4. Owls `/tmp` check (SMC-BVS items)

**Never touch:** the shared `/tmp/claude-*` folders and files (incl. `/tmp/claude-71711`, `claude-skill-*.zip`); BNP files
(`bnp-*`, `bnp_*`, anything with `bnp` in the name); other users' files (`find -user fb31` only); anything not clearly
BVS-named (e.g. `Rtmp*`, `fb31_strat_*`, `tmp*`, `v6bench_*`, `c5-*`, paper-review folders): those are reported only.

**Report:** every top-level `/tmp` entry owned by fb31 whose name matches, case-insensitively,
`^(smcbvs|smc-bvs|smc_bvs|bvs[-_]|p1m[-_]|psmc[-_]|w3[-_]?(scale|p6|dist)|g0[-_])` (the "clearly BVS-named" list; the
pattern is in the crew script and extended only by a logged HQ/Engineering decision), with size, newest mtime inside,
and the `lsof` result.

**Remove (rule T2) only if all hold:**
1. owned by fb31 and matches the BVS name pattern above, and does not match `claude-` or `bnp`;
2. idle: the newest mtime of any file inside is older than 24 h (`find <entry> -newermt '-24 hours' -print -quit` empty);
3. no process has it open or as cwd: `lsof +D <entry>` (or `lsof <file>` for a plain file) returns nothing, and no fb31
   process has an argument containing the path (`pgrep -u fb31 -f <entry>` empty);
4. not a lock: entries named `*.lock`, or folders that contain a `*.lock` file, are reported, never removed (a lock can
   outlive its holder only by mistake; its owner decides);
5. owner check: if the name points to a department that is not Engineering (e.g. `bvs-ci-*` → CI, `w3-*` → Theory), the
   item is reported to that owner and removed only after its owner agrees or after 7 days idle with no answer and HQ's OK;
6. command: `rm -rf --one-file-system -- "/tmp/<entry>"` after a `realpath` check that the target is a direct child of
   `/tmp` and not a symlink; one entry per command; logged with bytes.

At the 11-15 reading: `/tmp/bvs-ci-sandboxes` (303 MB) is **in use** by CI (lock held, cwd inside): report only.
`/tmp/smcbvs_B_verify_20261022_dev` (24 KB, idle since 10-22) meets rules 1–4 and is Engineering's old B_verify venv:
first candidate for T2, after the dry-run week.

## 5. Morning brief section (format)

```
Machines (daily check <date> <time>):
- NOTS home: <MB> / 10,240 MB (<pct>%) [OK|WARN|GUARD]; top growth: <item> +<MB>
- NOTS scratch dept: <size>; tree vs INDEX: <n> unindexed, <n> missing; strays: <list or none>
- NOTS queue: <n> jobs (<paths>)
- Owls /: <pct>% [OK|ALERT >85%]; dept footprint <size>; strays: <list or none>
- /tmp SMC-BVS: <n> items reported, <n> removed (<bytes>), <n> in use
- Deleted today: <n> items, <bytes> (rules N-T1/N-T2/O-T1/O-T2/T2); log: crews/logs/daily_<date>.md
- Needs a decision: <list>
```

## 6. Commands this leg used to calibrate the design

`quota -s | grep -A1 export/nots/home | tail -1` → `6761M 10240M 10240M 90394`; `df -h /` (Owls) → `70G 61G 9.6G 87%`;
`find /tmp -maxdepth 1 -user fb31 ! -name 'claude-*' -print0 | xargs -0 du -s` → 995 entries, 1,619,036 KB;
`lsof +D /tmp/bvs-ci-sandboxes` → 2 python processes; `tail ~/home_guard.log` (NOTS) → last run 11-12, 8,333 → 6,704 MB.

## HQ notices, 11-16
- **Crontab / authorized_keys freeze on Owls:** no edits today 10:05–10:30 CT, and 11:05–11:30 CT on BNP's backup-install
  day (date TBC). BNP is installing a watchdog that kills only runaway VS Code bundled-rg processes.
- **Cleanliness sweep:** add BNP's watchdog alert file (path to follow from HQ) to the Owls sweep in the daily report;
  report any hits to HQ.
- **BNP watchdog (HQ, 11-16):** alert file `/home/fb31/.config/bnp-eng/guard/ALERT`, with `guard.log` beside it (one line
  per action). **NOT installed** (HQ correction 11-17: BNP cancelled the 11-16 ~10:13 CT install, board pause; not re-scheduled). READ ONLY, never edit (an HQ-named exception to the folder scope). The daily
  report shows new lines since the last report. Last seen guard.log line count: 0 (before install). Daily check 2026-11-17 08:40 CST: 0 (ALERT and guard.log still absent; not installed).
- **Update (HQ, 11-16):** the 10:05–10:30 CT crontab freeze today is CANCELLED. BNP postponed the guard install (new slot
  TBA); the ALERT file does not exist yet, so the daily sweep reports "not installed" until it appears.
- **VS Code ripgrep paths** (only if the sweep ever matches on rg): both
  `~/.vscode-server/cli/servers/<build>/server/node_modules/@vscode/ripgrep-universal/bin/linux-x64/rg` (current builds)
  and `.../@vscode/ripgrep/bin/rg` (older). Engineering's sweep does not match on rg today; read only either way.

## owls_guard check (HQ request, 11-16; READ ONLY: ~/.config/bvs-hq/owls/owls_tool.py, guard.log, `systemctl --user` unit owls-guard)
- **What it acts on:** fb31 processes it classifies as "compute":
  - comm matches R/Rscript/Rterm/python*/julia/make/gmake/ninja/cmake/cc1plus/cc1/gcc/g++/c++/cc/gfortran/f951/collect2/ld/as,
    or cmd/cwd under /home/fb31/ls0_work or /tmp/*/work;
  - EXCLUDING protected comm (claude, codex, node, sshd*, tmux*, t3*, bash/sh/zsh/fish/dash, systemd*, cloudflared, code*,
    owls_guard*, sleep, ps, dbus*, ssh, scp, rsync, git, …) and protected cmd (.t3, .claude, .codex, .vscode-server,
    .config/bvs-hq/owls, t3code, cloudflared, mcp).
- **Actions:**
  - when total compute CPU > the budget (OWLS_BUDGET_CORES = 8): renice all compute processes to 19;
  - when > 2× the budget for 3 consecutive samples: SIGSTOP the top compute processes (resume = SIGCONT).
  - Nothing else: no kills.
- **VS Code: never.** rg's comm is not a compute name, its cmd contains `.vscode-server` (protected), and node/code* are
  protected.
- **BNP's guard: NOT guaranteed.** `.config/bnp-eng` is not in the protected list. If BNP's guard runs as python3 (comm
  python3), it is classified as compute. It would then be reniced to 19 whenever fb31 compute exceeds 8 cores, and could
  in principle be SIGSTOPped, although only if it were itself among the heaviest CPU users above 16 cores for 3 samples,
  which a watchdog is not. Fix (HQ's tool): add `\.config/bnp-eng` to PROTECTED_CMD.
- **03:40–04:00 spike:** it did NOT fire. state=OK throughout; compute 0–1% (rg is not compute); load1 9,777 → 40,046 →
  1,926; samples stretched to ~4 min; guard_cpu ≤ 0.39%. Its only action today was at 00:58:35 (compute 1046% > 800%:
  reniced 6 procs to 19). It could not have helped with the rg storm, by design.
- Freezes today: no crontab or ~/.vscode-server/data/Machine/settings.json edits 10:05–10:30 and 11:05–11:30 CT
  (Engineering has none). BNP ALERT file from 10:14 (not present at 05:5x).
- **Fixed by HQ (11-16):** PROTECTED_CMD now also covers `.config/bnp-eng`, `Bayesian-Nonparametric-Lean-Library`,
  `bnp_backups`, `bnp_tmp` and `bnp_worktrees`; the owls-guard service was restarted and is active. **owls_guard is
  SMC-compute-only from now on**: it never acts on BNP's processes or guard, nor on VS Code.

## Standing NOTS home hygiene job (HQ 2026-11-18; supersedes the scope rule above for these two items only)
The owner lets HQ manage NOTS. HQ ordered a standing job in the daily crew: `~/SMC_Engineering_Department/crews/home_hygiene/nots_home_prune.sh --apply` on Owls (one ssh call; dry run without `--apply`).
- **`~/.t3/runtime/versions/<v>`:** keep only the newest (version sort and mtime must agree, otherwise nothing is deleted) plus empty `.staging-*` dirs (a non-empty one is reported).
- **`~/.vscode-server/cli/servers/<name>`:** keep only the first entry of `lru.json` plus any server a live fb31 process uses.
- **Live processes:** a version or server in use is skipped (pgrep sees only the login node the call lands on).
- **Logging:** every removal goes to `crews/home_hygiene/removals.tsv`; full output in `runs.log`.
- **Never:** anything else in `.vscode-server` (extensions/, data/) without asking HQ, anything else in home, anything outside fb31's own data.
- **First run** (dry run 2026-11-18 ~07:00 CT, loginx2): quota 6,947 MB; one T3 version, three empty .staging dirs, one VS Code server (the lru first): nothing to remove (HQ had cleaned up).
- **Refinement (HQ 2026-11-18 afternoon):** keep the newest version + ANY version/server a live fb31 process uses on ANY login node; delete only versions with no live process and older than the newest.
  - **Liveness:** one gentle, read-only, sequential direct login to each NOTS login node (the A records of nots.rice.edu: loginx1–3), reading /proc/<pid>/{exe,cwd,cmdline} of fb31 processes only. If any node is unreadable, nothing is deleted.
  - **PROTECT.txt:** next to the script; HQ-protected names, always kept. It holds 0.1.11-nightly.20261117.4851 and 0.1.11-nightly.20261118.4877 per HQ "delete neither".
  - **Dry run 11-18:** all 3 nodes read; both versions kept.
- **Durable rule (HQ 0d4af23d, 2026-11-18 evening; replaces the per-name nightly protections):** the **newest 2** T3 nightlies (version sort) are always kept. An older one is pruned once it is superseded and no fb31 process on ANY login node references it (fail-closed: any unreadable node → nothing deleted). PROTECT.txt now carries no nightly names (comment only); it stays available for HQ one-off protections. Script: `newest2` in nots_home_prune.sh (backup .bak_20261118b).
  - **Applied 11-18 ~20:30 CST:** 4890 (504.8 MB; old rule) then 4851 (496.1 MB; unprotected by HQ) removed; 3/3 nodes read, no live reference; home 8,472 → 7,500 MB. Kept: 4877 + 4903 (newest 2). Note: a process on loginx3 still references the long-deleted 0.1.9-nightly.20261110.4465 (no files; harmless).
  - **VS Code extensions:** only a Haiku DRY-RUN listing of old duplicate versions goes to HQ (vscode_ext_dryrun_20261118.tsv); no deletion without HQ GO.
