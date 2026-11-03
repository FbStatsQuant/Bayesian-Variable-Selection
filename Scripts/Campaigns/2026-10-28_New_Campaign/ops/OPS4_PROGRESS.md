# OPS-4 progress: LOWP pilot (JOB.md rev 7) — resume from here after any crash

Rules: one ssh at a time via `ssh nots`; 15-min back-off after a timeout; check `squeue -u fb31` and `HOME/runs/<PID>/JOBIDS.tsv` BEFORE any resubmission. Never submit twice.

**STATE (2026-10-30 08:20Z): OPS-4 LOWP PILOT COMPLETE. Sol: pilot YES WITH CAVEATS, sizing ACCEPT WITH FIXES (review/SOL_REVIEW_PILOT_20261030T0712Z.md); all 8 findings dispositioned (review/OPS_RESPONSE_PILOT_20261030T0712Z.md); clean-up evidence + retrospective check in evidence/ops4_pilot_20261030T0712Z_cleanup.txt; sizing revised (ops/PROD_L_SIZING_20261030.md). Reported to HQ. Nothing running on NOTS.**
**Earlier (2026-10-30 08:10Z): COLLECT DONE (all folders pulled+VERIFIED+deleted; scale_t32 re-pulled after back-off, duplicate identical and removed); cleanup_pilot --yes CLEANUP VERIFIED; NOTS empty, home 9.42 GiB. summarize_pilot.R: OVERALL PASS 259/259, 16/16 verdicts (code/lowp/pilot/summary_20261030T0712Z_lowp_pilot). Measured 2.80 charged core-h (est ~10). Sizing written: ops/PROD_L_SIZING_20261030.md. NEXT: Sol review (delegate_task) -> save in ops/review/ -> report HQ.**
**Earlier (07:37Z): ALL 67 jobs/tasks COMPLETED (07:34:37Z); WAVE_UNLOCK_VERIFIED sha=equal; final_accounting 201 rows. Collect: enum20, enum30, scale_t08, scale_t16 pulled+VERIFIED+deleted. ssh TIMEOUT at scale_t32 remote delete (pulled+verified; local copy moved to ..._scale_t32.pull1; remote still present). Background resume (task b43wokaju) waits 900 s then pulls scale_t32, smc, bench, logs (--delete). If it dies: rerun `bash ops/scaffold/pilot_collect_resume.sh 20261030T0712Z 0 <remaining>`. Then: compare scale_t32 manifests -> drop .pull1; cleanup_pilot.sh dry/--yes; summarize_pilot.R.**
**Earlier (07:15Z): rev 7d SUBMITTED, STAMP=20261030T0712Z, submit_rc 0. JOB IDS: build 2469168, verify 2469169, truthtest 2469170, lock 2469171, enum20 2469172, enum30 2469173[0-5], scale 2469174, bitid 2469175, smc 2469176[0-27], bench 2469177[0-23], unlock 2469178, collect 2469179. NEVER resubmit. Gates: squeue clean, GNU time 1.9, guard OK 9.42 GiB, 1447 staged sha OK, frozen 27/27, GUARD_CHECK_OK. Monitor: pilot_monitor.sh v2 -> evidence/ops4_pilot_20261030T0712Z_monitor.log (exit 0 all terminal, 3 early failure, 2 restart). No guard/du on campaign home until unlock 2469178 terminal. After ALL_TERMINAL: `bash ops/scaffold/pilot_collect.sh 20261030T0712Z` (final_accounting + 7 results pulls + logs pull, --delete), then cleanup_pilot.sh dry/--yes, then summarize_pilot.R. On EARLY_FAILURE (exit 3): recover_truth, pull logs, cleanup, diagnose, report.**
**Pre-submit note (07:12Z): HQ D45 rev 7d READY -> staging+submitting with STAMP=20261030T0712Z (PID 20261030T0712Z_lowp_pilot). Before ANY resubmission: squeue + HOME/runs/<PID>/JOBIDS.tsv. Evidence ops/evidence/ops4_pilot_20261030T0712Z_*.txt.**
**Previous (2026-10-30 04:20Z): pilot 20261030T0313Z STOPPED at P0a (bundle design issue B1, see ops/PILOT_FAIL_20261030T0313Z.md); NOTS cleaned; waiting for HQ/CONF-2b. Next run needs a fresh STAMP and the fixed bundle; use pilot_monitor.sh v2 (args: LOG JOBIDS [MAX]).**
**Earlier state (2026-10-30 02:25Z): D34 path — v5 tested 54/54, Sol R4 running; then dry run, erase, guard. Tooling rule (HQ): Edit/Write for files; Bash one simple command, absolute paths; multi-step shell work via a script in ops/scaffold run as `bash <abs path>`. Pilot: Sol review 4 READY; wait for HQ "pilot READY for OPS" before staging.**
**Previous state (2026-10-30 01:35Z): BLOCKED on HQ/Felipe. D29 erase: archive DONE+VERIFIED; executor v4 36/36 tests; Sol R3 REJECT (residual same-UID race needs exclusion or explicit rule change). Nothing deleted in ~/.codex; home 9,809 MB. Scratch /scratch/fb31/New_Campaign/runs/ops4_d29 holds script+list+manifest (~100 KB) for the eventual run. B2 still with CONF-2b: do NOT stage the pilot until HQ says the GNU time fix landed.**

| Step | State | Notes |
|---|---|---|
| 0 Read brief/charter/D20-D26/JOB rev 7 | DONE | |
| 1a Local frozen check v2_2_1 | DONE | manifest sha256 d880afdbd0c1b783…2e13e1 (27 files) = D26; pilot_check_frozen rc 0 |
| 1b Seal study locally | DONE | `lowp_seal.R` (R 4.4.1) -> `<PC_NOTS_DATA>\New_Campaign\inputs\lowp_study` (1,200 + 60 datasets, 2,524 files, 72 MB; read-only). Use as `--sealed` at staging. |
| 1c NOTS pre-checks | DONE, 2 BLOCKERS | evidence/ops4_probe{1..4}_raw.txt |
| 2 Stage, upload, verify | BLOCKED (B1, B2) | do NOT stage before the bundle fix for B2 (the stager copies code as it is at that moment) |
| 3 Submit | NOT STARTED | job ids: none (only probe job 2466301, debug, COMPLETED 0:0, 0 s, wrote nothing) |
| 4-6 | NOT STARTED | JOB.md banner NOT replaced (pilot not submitted) |

## Pre-check results
- Guard (`disk_check.sh 30`): **REFUSE** — home 9,807 MB = 9.58 GiB (quota -s), +30 MB > 9.6 GiB. Campaign home 0.00, scratch empty. Growth since 2026-10-29 03:16Z (8.73 GiB) is Felipe's tool state, mainly `~/.codex` 1.2 G -> 2.1 G (+~0.9 GB); `.vscode-server` 4.9 -> 5.0 G; `projects` 728 -> 278 M (down). Not campaign data; OPS does not delete it.
- SPR: `sapphirerapids,ib` 70 nodes on commons. OK.
- Modules (login test-load): `GCC/14.3.0 R/4.5.2` -> gcc 14.3.0, R 4.5.2, lib `/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library` with Rcpp 1.1.0, digest 0.6.37, jsonlite 2.0.0 (= CONF identity build env.sh). Login R_LIBS_USER empty.
- Bench library R452: readable, 47 packages, all Built under R 4.5.2.
- **/usr/bin/time absent** on loginx2 AND on an SPR compute node (bb2u11c1, srun job 2466301). GNU time exists only as module `time/1.9` (needs `GCCcore/13.3.0`): `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time`.
- squeue -u fb31: empty (no jobs of ours).

## pilot.env values to fill at submission (decided)
MODULES="GCC/14.3.0 R/4.5.2"; R_LIBS_LOWP=""; R_LIBS_USER_LOWP="/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library" (as CONF); MODULES_BENCH="GCC/14.3.0 R/4.5.2".

## Blockers for HQ
- B1 (disk): need >= ~30 MB headroom under 9.6 GiB total home (currently ~9.58). Felipe/HQ must free space (e.g. ~/.codex growth) or rule otherwise. OPS will not shrink the planned add to squeeze under the guard.
- B2 (bundle): `slurm/common.sh` uses /usr/bin/time only; on NOTS it is missing, so every enumeration unit gets user/sys = NA -> summarize_pilot.R:254 marks all 36 enum units absent -> pilot INCOMPLETE (exit 3) by design; running now would spend ~10 core-h for a non-acceptable pilot. Needs a LOWP fix + Sol narrow review (e.g. common.sh: use /usr/bin/time if executable, else the pinned `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time` after checking `--version` reports GNU time; record which in env/).

## D28 ~/.codex clean-up (HQ)
| Sub-step | State |
|---|---|
| C1 du inventory ~/.codex depth 1-2 | DONE (CLEANUP_LOG.md D28) |
| C2-C4 list, Sol review, delete | STOPPED: eligible category <= 344 KB (sessions + archived_sessions); growth is packages/standalone/releases 1.8 GB (not authorised). Nothing deleted. Waiting for HQ. |
| C5 guard | not rerun (nothing freed); last quota 9,808 MB at 00:27Z |

## D29 ~/.codex/db-backups clean-up (HQ): delete all but the 3 newest by mtime; also keep anything modified in the last 24 h
| Sub-step | State |
|---|---|
| E1 list db-backups | DONE (evidence/ops4_dbbackups_list_raw.txt; 109 folders; newest is OPEN by live codex pid 550200) |
| E2 deletion list | DONE: 89 folders, 168,128 KB; list sha b5a2f47d…71e9c; executor scaffold/d29_dbbackups_delete.sh |
| E3 Sol review | DONE: REJECT, 0 rows accepted (review/SOL_REVIEW_D29_DBBACKUPS.md); blocking F1 = cross-node non-use unprovable from loginx2 |
| E3b D30/D31 | Felipe: Codex only on loginx2; archive-then-erase. ARCHIVE DONE+VERIFIED 265/265 files (manifest d2a67f0d…1816) in `NOTS Data/NOTS_home_archive/codex_db_backups_20261030` |
| E3c script v3 | DONE: scaffold/d29_dbbackups_delete.sh sha d302de84…1eca; harness d29_test_harness.sh 910454e5…0911: 8/8 tests pass on NOTS fake tree (evidence/ops4_d29_v3d_harness_raw.txt); /proc scan replaces lsof; archive gate; 2-pass erase |
| E3d Sol R2 | REJECT 0/89 (review/SOL_REVIEW_D29_DBBACKUPS_R2.md): F1 local open/write race, F2 grep-failure fail-open; F3-F6 should-fix/minor |
| E3e script v4 | DONE: quarantine-by-rename + 2 post-rename /proc scans + archive-hash pass + progress-tracked unlink; sha 4bb57035…3865; harness v4 b68e4057…ec3d 36/36 PASS on NOTS (evidence/ops4_d29_v4b_harness_raw.txt) |
| E3f Sol R3 | REJECT 0/89 (review/SOL_REVIEW_D29_DBBACKUPS_R3.md): F1 same-UID quarantine-path open / fd passing not excluded -> needs writer exclusion or explicit Felipe rule change; F2 nonzero producer status with empty stderr; F3-F5 should-fix. STOPPED, escalated to HQ. Nothing deleted in ~/.codex. |
| E3g HQ D34 | residual same-user race ACCEPTED by HQ (Felipe delegated storage, D31); Codex not stopped; fix R3 F2 + should-fixes; narrow R4 |
| E3h script v5 | DONE: sha a343ca33…0fd9 (classify() per producer; CUR_MUT; reservation-based no-clobber place(); device.inode ids). NOREPLACE unsupported on NOTS NFS (evidence/ops4_noreplace_probe_raw.txt). Harness v5 3ada57a6…8dd1: 54/54 PASS (evidence/ops4_d29_v5b_harness_raw.txt) |
| E3i Sol R4 | REJECT 0/89 (review/SOL_REVIEW_D29_DBBACKUPS_R4.md): F1 blocking (helper exemption bypassed maps-ENOENT abort) -> FIXED in v5.1; F2 should-fix (empty-reservation substitution by a same-user process) -> RECORDED as D34-class residual, header wording corrected (HQ rule: record and proceed); F3 minor full hashes -> FIXED |
| E3j script v5.1 | sha 24bd5a58…0fae; harness v5.1 832e2df0…a105: 58/58 PASS incl. T5c (evidence/ops4_d29_v51_harness_raw.txt) |
| E3k Sol R5 (narrow: R4 F1 + F3) | ACCEPT 89 rows / 168,128 KB (review/SOL_REVIEW_D29_DBBACKUPS_R5.md) |
| E4a dry run | DONE 02:54Z: would_delete 89, kb 168128, kept 0, failed 0, rc 0 (evidence/ops4_d29_dryrun_raw.txt) |
| E4b erase (--yes) | DONE 03:13Z: deleted 89, kb 168128, kept 0, failed 0, quarantine removed, rc 0 (evidence/ops4_d29_erase_raw.txt) |
| E5 guard + cleanup | DONE: guard 30 MB OK, home 9.41 GiB (03:13Z); scratch ops4_d29 removed; no quarantine left; db-backups now 25 folders |
| P2 stage + submit pilot (HQ D39) | DONE 03:14Z: SUBMITTED, submit_rc 0. JOB IDS: build 2467487, verify 2467488, truthtest 2467489, lock 2467490, enum20 2467491, enum30 2467492[0-5], scale 2467493, bitid 2467494, smc 2467495[0-27], bench 2467496[0-23], unlock 2467497, collect 2467498. NEVER resubmit. Gates: squeue clean, GNU time 1.9, guard 30 OK (9.41 GiB), 1444 staged files sha OK, pilot.env sha 7b98516d…, GUARD_CHECK_OK. Bundle tar sha e9ebd81c… kept in NOTS Data runs/<PID>/bundle. JOB.md banner updated. Do NOT run guard/du on campaign home until job 2467497 (unlock) is terminal. |
| P3 RESULT | **EARLY STOP at P0a (job 2467488 FAILED 1:0, MISMATCH 10092/11340 hashes)**; unlock 2467497 FAILED (lock never ran, B2); build/collect COMPLETED; 8 CANCELLED. ROOT CAUSE = bundle/design (B1): rnorm/qnorm bits differ R4.4.1-Windows vs R4.5.2-Linux (libm), ulp-level (eps rel <= 5.5e-16, foldid identical), not BLAS (NETLIB also differs), not staging (generator unchanged since 10-28). NOT resubmitted. Write-up: ops/PILOT_FAIL_20261030T0313Z.md (B1 blocking, B2 unlock-without-lock, B3 cleanup on NFS). Truth RECOVERED + TRUTH_SHA_OK (1260). Logs pulled 59/59 VERIFIED + deleted; cleanup_pilot UNVERIFIED (B3) -> 4 empty dirs rmdir'd, verified. NOTS clean; home 9.42 GiB. Waiter v2 fixed + offline-tested. WAITING for HQ / CONF-2b fix + Sol check, then fresh STAMP. |
| P3-old monitor | STOPPED (broken waiter v1): ops/scaffold/pilot_monitor.sh (log evidence/ops4_pilot_monitor.log; exits on ALL_TERMINAL or after 11 checks -> restart it); stop rules per JOB.md; if unlock 2467497 fails -> JOB.md §6 recover_truth.sh |
| P4 next | final_accounting.sh -> nots_pull.py each results folder + logs (--delete) -> cleanup_pilot.sh (dry, then --yes) -> summarize_pilot.R -> sizing (bench arm separately, D36) -> Sol review -> report |
| P2-old | STAMP=20261030T0313Z (PID 20261030T0313Z_lowp_pilot); evidence ops/evidence/ops4_pilot_20261030T0313Z_{stage,upload,submit}.txt; bash ops/scaffold/pilot_stage_and_submit.sh <STAMP>; BEFORE any resubmission check squeue + HOME/runs/<PID>/JOBIDS.tsv |
| E4 delete | TODO after Sol re-review |
| E5 | guard not rerun (nothing freed; quota 9,809 MB at 00:35Z); reported to HQ; STOPPED |
