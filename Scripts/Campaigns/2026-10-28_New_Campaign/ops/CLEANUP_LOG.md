# NOTS clean-up log (class A only; UTC)

Plan: `CLEANUP_PLAN.md`. Reviews: `review/SOL_REVIEW_CLASS_A.md` (R1 REJECT), `review/OPS_RESPONSE_R1.md`, `review/SOL_REVIEW_CLASS_A_R2.md` (R2 APPROVE WITH FIXES), `review/OPS_RESPONSE_R2.md` (F1–F3 done).
Staged tools (sha256 verified on NOTS before use): remote_pack.sh `16d21e07…1965`, verified_delete.sh `aeb43c40…a6a`, guard.sh `53103663…de3e`.
Before any deletion (02:02:08Z): `squeue -u fb31` empty; home 9.29 GiB (guard REFUSE above 9 GB).

| Time | Item | Path | Size | Reason | Verification | Result |
|---|---|---|---|---|---|---|
| 01:09Z | A3 | `/tmp/fb31_ops_20261028/`, `/tmp/fb31_ops_20261028.tgz` (loginx2) | 3.7 MB | OPS's own temporary hash bundle | contents kept locally as `evidence/nots_hashes/` (23 files) | removed by explicit two-path `rm` in the scaffold command |
| 02:02–02:04Z | A1.1 | `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_p0500_20261023T1227Z/results` | 1,097,537,311 B (1,073,352 KB on disk) | Campaign-2 production outputs (Felipe authorised) | laptop `NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p0500_…`: 4,800/4,800 sha256 match (`evidence/verify/prod_p0500.json`, list sha `fa82a53f…`); re-checked on NOTS by `sha256sum -c` right before deletion | `VERIFIED_DELETE files=4800 symlinks=0 left=0 base_removed=yes` (`evidence/exec_A1_raw.txt`) |
| 02:04–02:05Z | A1.2 | `…/claude/prod_p1000_20261023T1227Z/results` | 2,905,373,304 B (2,838,848 KB) | same | 4,800/4,800 (`evidence/verify/prod_p1000.json`, list sha `e1c84805…`); NOTS re-check passed | `VERIFIED_DELETE files=4800 left=0 base_removed=yes` |
| 02:05Z | A1.3 (pass 1) | `/home/fb31/projects/BVS/Others` | 321,924,368 B | legacy experiments (D6) | 55,024/55,024 (`evidence/verify/home_BVS_Others.json`, list sha `3205717b…`); all gates and the NOTS re-check passed | **Partial, failed closed**: 55,017 verified files removed; `rm` was denied on 7 files inside 2 read-only snapshot dirs (`Experiments_oct_13/code`, `…/code/engine_copy`); script stopped, so no links or dirs were touched (rc 123) |
| 02:06Z | A1.3 (pass 2) | same | 7 files (3,420 KB incl. dirs) + 34 symlinks | finish A1.3 | Residual list `evidence/A13_residual.sha256` (sha `de884b9f…`) = the 7 remaining files. Built on NOTS and checked locally: every line is byte-identical to a line of the authenticated 55,024-line list, and the paths equal the remaining files exactly. The 34 remaining links equal the approved list (`42f3bb5b…`). `chmod u+w` was applied only to the 2 read-only dirs. | `VERIFIED_DELETE files=7 symlinks=34 left=0 base_removed=yes` (`evidence/exec_A13b_raw.txt`); a note was appended to `/home/fb31/projects/BVS/README.md` |
| 02:07–02:21Z | A2.1 | `/scratch/fb31/smcbvs_v3_deploy_20261022` (remainder: prod attempts/slurm logs, readiness/test runs, n0, A_build logs, readiness tarball, transfer bookkeeping) | 123,303,115 B (123,857 KB) | finished jobs' logs and test outputs | `chmod u+w` was first applied to 2 read-only Rtmp dirs (`evidence/A2_chmod_dirs.txt`). `nots_pull.py` then copied the folder to `NOTS_BVS\smcbvs_v3_deploy_20261022\nots_scratch_remainder_20261029\`: 13,453/13,453 sha256 match, local count 13,453, 3 symlinks recorded. Manifest `6719f4b7…b3d4`; receipt `transfer/receipts/20261029T020717Z_scratch__fb31__smcbvs_v3_deploy_20261022.verify.json`. | `DELETED … files=13453 symlinks=3` after the remote manifest re-check |
| 02:25–02:41Z | A2.2 | `/projects/ml75/fb31/BVS/v3_profiling_20261020` | 70,317,604 B (114,712 KB) | v3 profiling folder (its code is already copied to `SMC_BVS_v3/`) | `chmod u+w` was first applied to 12 read-only snapshot dirs. The folder was then copied to `NOTS_BVS\NOTS_projects_ml75\BVS\v3_profiling_20261020\`: 16,436/16,436 match, 5 symlinks recorded. Manifest `c1afde26…f15f`; receipt `transfer/receipts/20261029T022504Z_projects__ml75__fb31__BVS__v3_profiling_20261020.verify.json`. | `DELETED … files=16436 symlinks=5`; pointer `/projects/ml75/fb31/BVS/v3_profiling_20261020_MOVED.md` written |

**Totals.** 4,518,455,702 B ≈ **4.52 GB (4.21 GiB)** of verified data was deleted from NOTS (about 4.4 GiB on disk):
- home: 0.32 GB;
- scratch: 4.13 GB;
- projects/ml75: 0.07 GB.

After A1 (02:06:12Z): home **9,060 MB = 8.85 GiB** (quota), guard OK.

After A2 (02:42Z):
- Home: **9,063 MB = 8.85 GiB**, guard OK.
- No jobs queued or running.
- /scratch/fb31: 195 G, almost all of it qr_data (class B).
- /projects/ml75/fb31: 3.5 G, the frozen bench20261019 only.
- /home/fb31/projects/BVS: 168 M (Benchmarks, library_portable, releases, SMC_BVS_v3, README, New_Campaign).

Evidence: `evidence/final_state_raw.txt`.

## Class B (Felipe approved 2026-10-29: `~/.vscode-server` and the pip cache only)

Reviews:
- `review/SOL_REVIEW_CLASS_B.md`: R1, APPROVE WITH FIXES (6 blocking).
- `review/OPS_RESPONSE_CLASS_B_R1.md`.
- `review/SOL_REVIEW_CLASS_B_R2.md`: R2, deletion still blocked (F1, F2, F4).
- `review/OPS_RESPONSE_CLASS_B_R2.md`.
- `review/SOL_REVIEW_CLASS_B_R3.md`: R3, **APPROVE** for the pip-only script, sha256 `DD3C18F3…62B2A0`, which was checked to match before the run.

Probes, all read-only: `evidence/clsB_probe{,2,3,4}.sh` with their `_raw.txt` outputs. Dry runs: `evidence/clsB_delete_pip_dry_raw.txt` (refused, fail-closed) and `evidence/clsB_delete_pip_dry2_raw.txt` (passed).

| Time | Item | Path | Size | Reason | Checks | Result |
|---|---|---|---|---|---|---|
| 03:16Z | B1 | `/home/fb31/.cache/pip` | 130,724 KB (128 MiB) | Felipe approved 2026-10-29, regenerable cache | `PIP_CACHE_DIR` unset, no pip.conf; last write 2026-10-21. Gate run twice, pre-check and again right before rm: plain canonical dir owned by fb31; no foreign entries; no mount; no pip process; no fb31 process on loginx2 references the path (unreadable processes exempt only as own ancestor / sshd session / (sd-pam), listed in output) | `DELETED kb=130724` (`evidence/clsB_delete_pip_exec_raw.txt`); quota 9,282,988 → 9,152,264 KB |
| — | B2 | `/home/fb31/.vscode-server` | 5,036,044 KB (4.8 GiB) | Felipe approved | **Live VS Code servers found on loginx2** (12 processes, started 2026-10-28 13:57 CDT), using `cli/servers/Stable-2c33b50b…` and `Stable-e6468682…`. So the whole folder was not deleted, and nothing was killed. Three versions have no process on loginx2: `Stable-2d0b7506…` (656,100 KB, quiet since 10-23), `Stable-6d62b1d5…` (643,408 KB, quiet since 10-21), `Stable-585eba7c…` (227,504 KB, quiet since 10-28 16:25Z). Sol R2 blocked them: /home is NFS-shared, so a server on another login node cannot be excluded without contacting that node, which charter §3 forbids. | **NOT DELETED; decision escalated to Felipe via HQ.** No `bin/` folder exists. |

Not touched: `~/.claude/remote`, `~/.t3`, `~/.t3-recovery`, VS Code `data/`, `extensions/`, `lru.json`, `.locks`, `code-*` binaries.

After B1 (03:16Z): home **9,152,264 KB = 8.73 GiB** (was 9,282,988 KB = 8.85 GiB), guard OK under the new limits.

## D28 (HQ, 2026-10-30): ~/.codex old-log clean-up — inventory (OPS-4), STOPPED before any deletion

Inventory 2026-10-30T00:24-00:27Z, `du -k` on `/home/fb31/.codex` only, depth 1-2 (raw: evidence/ops4_codex_du_raw.txt, ops4_codex_du2_raw.txt). Home quota 9,808 MB.

| Path (~/.codex) | KB | Category under D28 |
|---|---|---|
| packages/standalone/releases | 1,818,240 | Codex CLI binary releases — NOT logs; not deletable under D28 |
| db-backups/ (about 50 `sqlite-<epoch>-0` folders, 0.8–7.5 MB each) | 188,344 | database backups — excluded by D28 rule 3 ("any database") |
| cache/ (remote_plugin_catalog 53 MB, codex_apps_tools 2.6 MB) | 55,768 | cache — not in the D28 category |
| plugins/ (plugins/cache 49 MB) | 49,324 | plugins — never touch |
| tmp/ (arg0-linux 1.2 MB) | 1,388 | not in category |
| skills/ | 500 | never touch |
| .tmp/ | 312 | not in category |
| **sessions/** (2026/) | **288** | **D28 category** (only the files older than 7 days) |
| repair-20261016/ | 96 | not in category |
| **archived_sessions/** | **56** | **D28 category** |
| app-server-control, thread-writer-locks, shell_snapshots, rollout-migrations, ipc | 4 each | not in category |
| top-level files: models_cache.json 456 KB; state_5/thread_history_1/logs_2/memories_1/queue_1/goals_1 `.sqlite` (+ -shm/-wal); auth.json; config.toml; session_index.jsonl; installation_id | ~1,100 | databases/credentials/config — never touch. No `log/` folder and no `*.log` file at depth 1; Codex logs live in `logs_2.sqlite` (a database, excluded) |
| **Total ~/.codex** | **2,115,472** | |

**Result:** the whole D28-eligible category (sessions/ + archived_sessions/) is at most **344 KB**, before the 7-day filter. The guard needs about 8 MB more headroom (9,808 MB + 30 MB planned > 9,830 MB = 9.6 GiB), so the authorised deletion cannot clear blocker 1. **No deletion list was built, no Sol review was requested, and nothing was deleted.** The growth since 2026-10-29 (+~0.9 GB) is in `packages/standalone/releases` (Codex binaries; 931 MB for all of `packages` on 2026-10-29). Escalated to HQ for a new decision.

## D29 (Felipe via HQ, 2026-10-30): delete old Codex log-database backups in ~/.codex/db-backups — DELETION LIST (pending Sol review)

Listing 2026-10-30T00:35:44Z (raw: evidence/ops4_dbbackups_list_raw.txt; now_epoch 1793320544; 24 h cut 1793234144 = 2026-10-29T00:35:44Z). 109 folders `sqlite-<epoch>-0`, each holding only `logs_2.sqlite` (+ `-shm`, `-wal` in 108 of them); no symlinks. `lsof +D` on loginx2: the newest folder `sqlite-1793319865-0` is OPEN by a live `codex` process (pid 550200) — it is Codex's active logs database, not a backup. "mtime" below = newest mtime of the folder and its files.

Rule applied: KEEP the 3 newest by mtime, KEEP anything modified in the last 24 h, KEEP anything open; DELETE the rest. Result: **DELETE 89 folders, 168,128 KB (164.2 MiB); KEEP 20 folders, 20,212 KB** (3 newest 804 KB incl. the open one; 17 modified < 24 h 19,408 KB). Keep list: evidence/ops4_dbbackups_keep_list.tsv.

Machine list: `evidence/ops4_dbbackups_delete_list.tsv`, sha256 `b5a2f47d5ff1537d305211b26738551e91d6fee51422f494a1e43c0c84571e9c`. Executor: `scaffold/d29_dbbackups_delete.sh` (dry run first, then `--yes`); per folder it re-checks at delete time: exact path pattern, real dir (no symlink), only the three logs_2.sqlite files, mtime unchanged since listing and older than now − 24 h, not among the 3 newest at that moment, no open file (lsof); any failure keeps the folder.

| # | Path (/home/fb31/.codex/db-backups/) | KB | newest mtime (UTC) | files |
|---|---|---|---|---|
| 1 | sqlite-1793233767-0 | 196 | 2026-10-29T00:30:08Z | 3 |
| 2 | sqlite-1793231660-0 | 568 | 2026-10-29T00:25:19Z | 3 |
| 3 | sqlite-1793230757-0 | 356 | 2026-10-28T23:49:38Z | 3 |
| 4 | sqlite-1793227748-0 | 536 | 2026-10-28T23:18:47Z | 3 |
| 5 | sqlite-1793226245-0 | 504 | 2026-10-28T22:46:39Z | 3 |
| 6 | sqlite-1793224137-0 | 680 | 2026-10-28T22:16:38Z | 3 |
| 7 | sqlite-1793223232-0 | 2568 | 2026-10-28T21:46:38Z | 3 |
| 8 | sqlite-1793215425-0 | 816 | 2026-10-28T19:46:38Z | 3 |
| 9 | sqlite-1793213318-0 | 1684 | 2026-10-28T19:16:38Z | 3 |
| 10 | sqlite-1793202488-0 | 520 | 2026-10-28T16:16:37Z | 3 |
| 11 | sqlite-1793200982-0 | 444 | 2026-10-28T15:56:18Z | 3 |
| 12 | sqlite-1793199175-0 | 504 | 2026-10-28T15:21:41Z | 3 |
| 13 | sqlite-1793197369-0 | 392 | 2026-10-28T14:46:37Z | 3 |
| 14 | sqlite-1793196165-0 | 360 | 2026-10-28T14:16:37Z | 3 |
| 15 | sqlite-1793193756-0 | 5084 | 2026-10-28T13:46:37Z | 3 |
| 16 | sqlite-1793142154-0 | 580 | 2026-10-27T23:34:27Z | 3 |
| 17 | sqlite-1793140350-0 | 400 | 2026-10-27T22:46:37Z | 3 |
| 18 | sqlite-1793137943-0 | 648 | 2026-10-27T22:26:07Z | 3 |
| 19 | sqlite-1793136438-0 | 480 | 2026-10-27T21:57:57Z | 3 |
| 20 | sqlite-1793135536-0 | 1752 | 2026-10-27T21:16:37Z | 3 |
| 21 | sqlite-1793127428-0 | 1188 | 2026-10-27T19:26:07Z | 3 |
| 22 | sqlite-1793123526-0 | 788 | 2026-10-27T18:16:37Z | 3 |
| 23 | sqlite-1793119924-0 | 556 | 2026-10-27T17:16:37Z | 3 |
| 24 | sqlite-1793118114-0 | 488 | 2026-10-27T16:45:37Z | 3 |
| 25 | sqlite-1793116009-0 | 404 | 2026-10-27T16:20:57Z | 3 |
| 26 | sqlite-1793115407-0 | 1296 | 2026-10-27T16:01:47Z | 3 |
| 27 | sqlite-1793111806-0 | 300 | 2026-10-27T14:56:07Z | 3 |
| 28 | sqlite-1793110300-0 | 276 | 2026-10-27T14:26:07Z | 3 |
| 29 | sqlite-1793108794-0 | 364 | 2026-10-27T14:16:37Z | 3 |
| 30 | sqlite-1793108192-0 | 5380 | 2026-10-27T13:36:46Z | 3 |
| 31 | sqlite-1793049686-0 | 308 | 2026-10-26T21:43:17Z | 3 |
| 32 | sqlite-1793048782-0 | 408 | 2026-10-26T21:35:27Z | 3 |
| 33 | sqlite-1793047278-0 | 432 | 2026-10-26T21:03:27Z | 3 |
| 34 | sqlite-1793045170-0 | 2052 | 2026-10-26T20:27:57Z | 3 |
| 35 | sqlite-1793037663-0 | 384 | 2026-10-26T18:21:07Z | 3 |
| 36 | sqlite-1793035558-0 | 312 | 2026-10-26T17:46:37Z | 3 |
| 37 | sqlite-1793034355-0 | 4332 | 2026-10-26T17:27:36Z | 3 |
| 38 | sqlite-1793020247-0 | 4464 | 2026-10-26T13:11:00Z | 3 |
| 39 | sqlite-1792970441-0 | 4460 | 2026-10-25T23:20:55Z | 3 |
| 40 | sqlite-1792939381-0 | 7236 | 2026-10-25T15:00:26Z | 3 |
| 41 | sqlite-1792778744-0 | 280 | 2026-10-23T18:28:26Z | 3 |
| 42 | sqlite-1792776635-0 | 936 | 2026-10-23T17:47:56Z | 3 |
| 43 | sqlite-1792771786-0 | 1412 | 2026-10-23T16:22:16Z | 3 |
| 44 | sqlite-1792763732-0 | 384 | 2026-10-23T14:15:36Z | 3 |
| 45 | sqlite-1792761925-0 | 448 | 2026-10-23T13:48:26Z | 3 |
| 46 | sqlite-1792761022-0 | 580 | 2026-10-23T13:21:56Z | 3 |
| 47 | sqlite-1792758320-0 | 376 | 2026-10-23T12:46:36Z | 3 |
| 48 | sqlite-1792757417-0 | 1280 | 2026-10-23T12:27:26Z | 3 |
| 49 | sqlite-1792751669-0 | 4468 | 2026-10-23T11:00:56Z | 3 |
| 50 | sqlite-1792722312-0 | 412 | 2026-10-23T02:46:36Z | 3 |
| 51 | sqlite-1792720506-0 | 412 | 2026-10-23T02:18:06Z | 3 |
| 52 | sqlite-1792719000-0 | 352 | 2026-10-23T01:47:56Z | 3 |
| 53 | sqlite-1792716893-0 | 3316 | 2026-10-23T01:19:26Z | 3 |
| 54 | sqlite-1792705788-0 | 460 | 2026-10-22T22:14:36Z | 3 |
| 55 | sqlite-1792703982-0 | 580 | 2026-10-22T21:45:36Z | 3 |
| 56 | sqlite-1792700973-0 | 792 | 2026-10-22T20:50:26Z | 3 |
| 57 | sqlite-1792697671-0 | 324 | 2026-10-22T20:05:26Z | 3 |
| 58 | sqlite-1792695868-0 | 2296 | 2026-10-22T19:19:46Z | 3 |
| 59 | sqlite-1792686263-0 | 468 | 2026-10-22T16:45:26Z | 3 |
| 60 | sqlite-1792685059-0 | 212 | 2026-10-22T16:16:36Z | 3 |
| 61 | sqlite-1792683557-0 | 6416 | 2026-10-22T16:04:56Z | 3 |
| 62 | sqlite-1792589626-0 | 5544 | 2026-10-21T14:05:16Z | 3 |
| 63 | sqlite-1792534163-0 | 2524 | 2026-10-20T22:11:00Z | 3 |
| 64 | sqlite-1792527208-0 | 4788 | 2026-10-20T20:27:45Z | 3 |
| 65 | sqlite-1792508750-0 | 5160 | 2026-10-20T15:15:06Z | 3 |
| 66 | sqlite-1792459140-0 | 4508 | 2026-10-20T01:50:05Z | 3 |
| 67 | sqlite-1792444783-0 | 764 | 2026-10-19T21:55:05Z | 3 |
| 68 | sqlite-1792441646-0 | 824 | 2026-10-19T20:57:05Z | 3 |
| 69 | sqlite-1792438045-0 | 416 | 2026-10-19T19:58:25Z | 3 |
| 70 | sqlite-1792437744-0 | 520 | 2026-10-19T19:48:09Z | 3 |
| 71 | sqlite-1792436541-0 | 856 | 2026-10-19T19:22:25Z | 3 |
| 72 | sqlite-1792435487-0 | 4600 | 2026-10-19T19:09:47Z | 3 |
| 73 | sqlite-1792423937-0 | 1028 | 2026-10-19T16:03:35Z | 3 |
| 74 | sqlite-1792421828-0 | 1632 | 2026-10-19T15:27:55Z | 3 |
| 75 | sqlite-1792420022-0 | 1096 | 2026-10-19T14:38:25Z | 3 |
| 76 | sqlite-1792416411-0 | 3056 | 2026-10-19T13:53:45Z | 3 |
| 77 | sqlite-1792406784-0 | 5044 | 2026-10-19T10:46:35Z | 3 |
| 78 | sqlite-1792350407-0 | 1820 | 2026-10-18T19:29:37Z | 3 |
| 79 | sqlite-1792348902-0 | 4476 | 2026-10-18T18:45:35Z | 3 |
| 80 | sqlite-1792341697-0 | 2284 | 2026-10-18T16:56:05Z | 3 |
| 81 | sqlite-1792339588-0 | 4344 | 2026-10-18T16:19:05Z | 3 |
| 82 | sqlite-1792329450-0 | 4928 | 2026-10-18T13:28:25Z | 3 |
| 83 | sqlite-1792279552-0 | 2592 | 2026-10-17T23:45:34Z | 3 |
| 84 | sqlite-1792276241-0 | 1492 | 2026-10-17T22:58:34Z | 3 |
| 85 | sqlite-1792274135-0 | 1508 | 2026-10-17T22:12:45Z | 3 |
| 86 | sqlite-1792270223-0 | 4416 | 2026-10-17T21:00:56Z | 3 |
| 87 | sqlite-1792267955-0 | 5220 | 2026-10-17T20:12:46Z | 3 |
| 88 | sqlite-1792176120-0 | 7492 | 2026-10-16T19:09:45Z | 3 |
| 89 | sqlite-1792105282-0 | 4492 | 2026-10-15T23:01:33Z | 1 |

**D29 review result (2026-10-30T00:40Z): Sol 6.1 (high) REJECT — 0 of 89 rows accepted, 0 KB** (review/SOL_REVIEW_D29_DBBACKUPS.md). Partition, sizes and scope verified correct (A, B PASS: 109 folders, 89 delete / 20 keep, 168,128 KB). Blocking: (1) lsof on loginx2 cannot prove the old SQLite sets are not open by a Codex process on another NFS client (same limit as the 2026-10-29 VS Code deferral); (2) executor's lsof/find/du failures fail open; (3) top-3/cutoff cached once instead of per row; (4) path-replacement / live-writer races before rm -rf. Should-fix: bind to TSV hash + schema, nonzero exit on failure/partial deletes, fix usage text + enforce loginx2/fb31; minor: mtime check weaker than a manifest. **Nothing deleted; no executor run on NOTS.** Escalated to HQ.

**D29 DONE (2026-10-30T03:13Z), under HQ D34.** Executor v5.1 (sha 24bd5a58…0fae; Sol R5 ACCEPT 89 rows / 168,128 KB, review/SOL_REVIEW_D29_DBBACKUPS_R5.md; harness 58/58). Dry run 02:54Z: would_delete 89. Erase 02:54–03:13Z: **DELETED 89 folders, 168,128 KB, kept 0, failed 0**, every file's sha256 = verified archive before unlink, quarantine removed (evidence/ops4_d29_dryrun_raw.txt, ops4_d29_erase_raw.txt). Archive kept at `NOTS Data\NOTS_home_archive\codex_db_backups_20261030` (reversible). Home 9.58 → 9.41 GiB. Scratch run folder removed. Residuals accepted by D34: R3 F1, R4 F2 (header of the executor).

**D29/D30/D31 status (2026-10-30T01:35Z).** The 89 folders are ARCHIVED and verified (265/265 files, manifest d2a67f0d…1816; `NOTS Data\NOTS_home_archive\codex_db_backups_20261030`; Sol R2 re-hashed it independently). Executor rounds: v2 (Sol R1 REJECT), v3 (Sol R2 REJECT), v4 quarantine-by-rename (36/36 NOTS fake-tree tests; Sol R3 REJECT: the residual same-user race, i.e. a process of fb31 opening the private quarantine path or receiving a passed descriptor after its last scan, is not excluded; plus a fail-open on nonzero producer status with empty stderr). **Nothing deleted from ~/.codex.** Escalated to HQ: Sol's conditions are writer exclusion (e.g. Codex closed on loginx2 for the ~15-min run) or an explicit rule change by Felipe for these residuals.

## D31 (standing authority) 2026-10-30: /home/fb31/backups — archive-then-erase for PROD-L staging headroom (OPS-6)
Why: PROD-L's submit-time guard_check (planned 110 MB, counted again after the 74 MB stage is extracted) refused at home 9.51 GiB (+110 MB > 9.6 GiB); D40's 9.70 GiB cannot be used (the bundle's guard_check requires the guard's home limit <= 9.6 GiB). Need >= ~25 MB.
Listing 2026-10-30T18:13:46Z (evidence/ops6_d31_backups_listing.txt): 2 regular files, owner fb31, no symlinks, not open on loginx2; du 46,860 KB.
| File (/home/fb31/backups/) | Bytes | mtime | sha256 |
|---|---|---|---|
| Extreme_individual_pkgs_before_tau90_93_20261021.tar.gz | 47,930,054 | 2026-10-21 16:34 | c9d0f4614ea15cb70f78a2981d5b6e9584251b83c0fec189f96177927c2327d2 |
| Extreme_Joint_Sampler_before_b0005_15k3k_20261022.tar.gz | 46,774 | 2026-10-22 09:48 | c56bb68ccf6a5181ded7c4aff747cb920096f7d68989c17cc3655dec59b3ce9e |
Archive: `NOTS Data\NOTS_home_archive\backups_20261030\backups\` — ARCHIVE VERIFIED 2/2 (REMOTE_SHA256.txt). Category: package backup tarballs (Quant_Reg), not program installs in use, credentials, config or open files (D31 exclusions).
Planned erase (one ssh): `cd /home/fb31/backups && printf '<sha>  <file>\n' x2 | sha256sum -c - && rm -- <file1> <file2> && cd / && rmdir /home/fb31/backups`; then guard. Status: PENDING Sol review.
- 2026-11-02T17:45:55Z HQ D74 option A ERASE ~/.vscode-server/data/CachedExtensionVSIXs: 4 regular files (anthropic.claude-code-2.1.312-linux-x64 137,332,422 B; github.copilot-chat-0.48.1 20,337,888 B; openai.chatgpt-26.51021.22027-linux-x64 428,092,046 B; openai.codex-audio-26.1021.22027 1,901,878 B; total 587,664,234 B), directory kept; NO archive (D74: regenerable cache). Listing evidence/ops_d74_vsix_list_20261102.txt (LISTING_SHA c708bf06…b2e5, re-verified at erase; anchored dir 54:257690479). Executor ops/scaffold/vsix_erase_remote.sh R4 (Sol rounds 1–3 ACCEPT WITH FIXES, review/SOL_REVIEW_D74_VSIX_ERASE.md; R3 cwd fix + D29-accepted sd-pam/sshd helper exemption applied without a 4th round, noted there). First run 17:44:59Z REFUSED (sd-pam unreadable; nothing deleted; evidence/ops_d74_vsix_erase_20261102_R3_refused_sdpam.txt). Second run: 21 processes scanned, 7 helpers skipped (1 sd-pam, 6 sshd), 0 open; ERASE VERIFIED, enumeration ok, 0 left (evidence/ops_d74_vsix_erase_20261102.txt). Not touched: cli/servers (B), ~/.t3 (C).
- 2026-11-02T21:14:39Z HQ D79 (Felipe's authority: caches + old installs) ERASE VERIFIED, no archive (regenerable): ~/.cache/pip, ~/.cache/matplotlib, contents of ~/.vscode-server/data/CachedExtensionVSIXs (folder kept), ~/.t3/runtime/versions/0.1.6, ~/.vscode-server/cli/servers/Stable-{6d62b1d5…,2d0b7506…,585eba7c…}, ~/.vscode-server/code-{6d62b1d5…,2d0b7506…,585eba7c…}; listed 2,017.8 MB (LIST_SHA b8afe515…39c8). du ~ 10,096 -> 7,908 MB. Kept: Stable-2c33b50… (live/newest), Stable-e646868… (its CLI = running agent host), T3 0.1.7-nightly (live/newest), ~/.cache/Microsoft, ~/.cache/copilot, ~/.cache/conda (changed between list and first erase attempt = in use; dropped). Executor ops/scaffold/d79_home_clean_remote.sh R3.1 (Sol R1-R3 ACCEPT WITH FIXES, review/SOL_REVIEW_D79_HOME_CLEAN.md; last one-line fix per R3 without a 4th round); helpers: D29 sd-pam/sshd + HQ-accepted pinned sftp-server 3742644:559291281; 51 processes scanned, 0 references, 129 mounts checked. First erase 21:12Z REFUSED (conda listing changed; nothing deleted). Evidence: ops/evidence/ops_home_du2_20261102T2051Z.txt, ops_d79_list_20261102*.txt, ops_d79_erase_20261102*.txt.
- 2026-11-02T22:43Z HQ D82 failed PROD_L_BENCH run 20261102T1311Z_lowp_bench removed: scratch logs/20261102T1311Z_lowp_bench pulled to NOTS Data/New_Campaign/logs/20261102T1311Z_lowp_bench (VERIFIED 22:14:20Z, 30 files, 328,425 B, receipt manifest e38e7a28…) then deleted by remote_pack.sh delete (re-hashed; 22:42:19Z; the 22:14Z delete attempt was refused while F3 cell 4 ran); cleanup_bench.sh 20261102T1311Z dry run + --yes (run from memory): removed HOME runs/20261102T1311Z_lowp_bench (64,072 KB) and SCR runs/20261102T1311Z_lowp_bench_tmp (0 KB), _cache absent; residue none; CLEANUP VERIFIED; receipt /scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt. Evidence ops/evidence/ops9_plb_failed_pull.txt, ops9_plb_failed_cleanup.txt.
- 2026-11-03T00:04:27Z HQ D65/JOB.md BENCH_F3 dev+prod scratch DELETED (list ops/F3_DELETION_LIST_20261102.md; Sol R1 ACCEPT WITH FIXES + R2 ACCEPT, review/SOL_REVIEW_F3_DELETION_20261102.md; executor f3_delete_remote_v2.sh, D79 proc scan 49 procs / 0 references, helpers incl. HQ-accepted pinned sftp-server): remote_pack.sh delete (re-hashed vs receipt transfer manifests) results/20261102T1252Z_bench_f3v2_prod/p0500 (4,801 files, 55,990 KB), …/p1000 (4,801, 57,363 KB), logs/20261102T1252Z_bench_f3v2_prod (4,823, 3,554 KB), upload/20261102T1252Z_bench_f3v2_prod (35, 175 KB), results/20261030T1855Z_bench_f3v2_dev/p0500 (49, 564 KB), …/p1000 (57, 662 KB), logs/20261030T1855Z_bench_f3v2_dev (65, 53 KB), upload/20261030T1855Z_bench_f3v2_dev (35, 173 KB); rmdir both empty results parents; final check: none remaining. Local copies in NOTS Data/New_Campaign/{results,logs,upload}/. Evidence ops/evidence/ops8_f3_delete.txt.
- 2026-11-03T13:22:36Z PROD_L_BENCH rev 2 (STAMP 20261102T2309Z) closed: results/20261102T2309Z_lowp_benchres pulled to NOTS Data/New_Campaign/results/ (76,801 files, 1,628,950,554 B VERIFIED; bundle MANIFEST 0dd8ced3… OK) and DELETED from scratch (remote manifest re-checked 9679ad96…); logs/20261102T2309Z_lowp_bench pulled (7,811 files VERIFIED; MANIFEST 0b8bc30d… OK) and DELETED (f893b61a…); home manifests + inventory_final copied to runs/20261102T2309Z_lowp_bench/home_summary/; cleanup_bench.sh --yes (from memory): removed HOME runs/20261102T2309Z_lowp_bench (64,592 KB) + SCR runs/…_tmp, _cache absent, CLEANUP VERIFIED, receipt /scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T2309Z_lowp_bench.txt. Evidence ops/evidence/ops9_plb_pulls.txt, ops9_plb_cleanup.txt.
- 2026-11-03T13:59:00Z HQ D92 FINAL NOTS SWEEP (list ops/FINAL_NOTS_DELETION_LIST_20261103.md; Sol R1+R2 ACCEPT WITH FIXES, R2 fix applied, review/SOL_REVIEW_FINAL_NOTS_SWEEP.md; executor final_delete_remote_v2.sh, one direct control ssh under timeout 270; D79 proc scan 23 procs / 0 references; pinned sftp-server 1859878:565440633 = HQ-accepted pattern, identity in ops/evidence/ops_final_sftp_identity.txt; first run 13:58:39Z REFUSED on that new sftp session, nothing deleted). Archive first (verified): NOTS Data/New_Campaign/nots_home_final/{code/{core,v2_2,bench_v2,ops},jobs/CONF_NOTS_IDENTITY,runs/20261030T0934Z_prodH,README.md} and nots_scratch_final/{upload/ops_bg,upload/cleanup_receipt_*.txt,README.md,SHA256SUMS_remote.txt}; PROD-H tar = local bundle copy 845de40e…. DELETED: home jobs/CONF_NOTS_IDENTITY (8 files, remote_pack 1428212c…), home runs/20261030T0934Z_prodH (54 files, efd3abe3…; HQ D92 PROD-H prune), scratch upload/ops_bg (46 files, d283478e…), scratch README.md + 3 clean-up receipts + upload/prodH_bundle_20261030T0934Z.tar (720 KB; HQ D92) by sha256 gate, scratch /scratch/fb31/New_Campaign (empty dirs only) REMOVED, home jobs/ runs/ logs/ results/ rmdir. Kept: home README.md, code/{bench_v2,core,ops,v2_2} (2,432 KB), empty inputs/ manifests/. Guard after: home 8.42 GB of 10.00, campaign_home 0.00 GB, OK. Evidence ops/evidence/ops_final_delete.txt, ops_final_state_20261103.txt.
