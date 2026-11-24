# HANDOFF to the SMC Engineering Department v2 manager (from v1, 2026-11-24)

## 1. State (2026-11-24)
- **BREAK, HQ H-54.** SMC-BVS is paused; nothing new starts. Only the daily report, NOTS hygiene and riboflavin run.
- **1M block: STOPPED after W2** (owner, H-53). W2 is done (collected, V4 pass, desktop-verified). The summary is `results/gc1m/GC_1M_BLOCK_SUMMARY.md` (6b5f3134): 7 fits, HPM = MPM = S₀ in 7/7.
  Engine F2 = tag `p1m-freeze-F2` (e993ece2). Read-backs: `GC_P_READBACK.md`, `GC_D_READBACK.md`. Pre-registration and deviations: `GC_PREREG.md` §10.
- **Next-block notes (H-55)**, for when the break ends:
  - base both K2 clauses on engine `seconds.total`;
  - fix the verify_inputs I/O contention (the %8 throttle, H-52, or node-local staging);
  - fix the monitor's "other islands" logic in the K2 elapsed clause.
- **NOTS budget (LEDGER.md):** closed ≈ 6,042 core-h of the ≈ 28.3k envelope (H-9). SMC has used 0 core-h since 11-21. Other fb31 sacct rows (BQTF, /projects/ml75) are NOT ours.
- **RIBOFLAVIN (H-58).** The 11-18 fits died in the Owls reboot of 11-22 00:24. Relaunched 2026-11-22 02:46 CST:
  - systemd user units `ribo-s1..5`, cores 15–19, nice 19, frozen `rb_unit.sh`, 120-h cap; no duplicates;
  - ETA ≈ **11-27 02:46 CST**;
  - work dir `~/SMC_Engineering_Department/tmp/20261118-riboflavin/` (`out/DONE_seed<s>`, `out/fit_seed<s>.rds`, `log/seed<s>.log`, `log/relaunch.log`);
  - the @reboot line in the Owls crontab runs `rb_relaunch.sh` (restarts any seed without DONE; Linger=yes); crontab backup `crontab.bak.20261122`;
  - README draft: main clone `Docs/Experiments/realdata_riboflavin/README.md` (`<<...>>` placeholders), scripts in `scripts/`.
  - **When all 5 are DONE**, send the riboflavin agent "H-58 fits DONE: collect the fits and finish the README", then remove the @reboot line and its comment (back up the crontab first). Send HQ one line on delivery. If a seed fails, report it with the log tail; relaunch only with HQ's GO.

## 2. Open items / owed reports
- Daily report to HQ by 09:00 CT (≤ 10 lines). The riboflavin delivery line is owed ≈ 11-27.
- NOTS Tier 2 (≈ 111–167 GB of regenerable *.bin): HQ ruled "let the purge take them" (H-41 (4), H-56); the purge starts ≈ 12-05. Do nothing.
- Kept strays, all indexed: NOTS `vn_minileg/clone_e993ece2` (until the VN leg closes), `gcd_*/gct2_*` sha files; Owls `envs/ci-py313`, `Rlib/` (owner unknown), `scripts/`.
- Untracked `Docs/Experiments/data_apps/` (SHORTLIST.md) in the worktree is not mine; leave it.
- Owls / is at 89 %; the growth is not SMC (BNP-Lean, lhv, e03 in fb31's /tmp). HQ told the owner; never touch them.

## 3. Paths
- Dept folder: **`/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/`** (worktree, branch `exp/P1M`). Commit there. The main clone's `Docs/Experiments/P1M` is a tracked copy: don't write it.
  Main clone `/home/fb31/Bayesian-Variable-Selection` (read HOLDS.md and HQ_DECISIONS.md there; `git pull --ff-only`).
- Owls `~/SMC_Engineering_Department/` (INDEX.md):
  - `records/<unit>/` (SHA256SUMS per unit);
  - `crews/offload/serve.log` + `desktop_verified.txt` (the desktop pulls hourly at :20; verified units appear on the NEXT pull);
  - `crews/home_hygiene/` (`nots_home_prune.sh`, `nots_wave_hygiene_check.py`, `removals.tsv`, `nots_scratch_removals.tsv`);
  - `staging/gc1m/`, `tmp/` (the only scratch; never /tmp, POLICIES §14).
- NOTS (`ssh nots`; you are ON Owls, never `ssh owls`): `~/SMC_Engineering_Department/` (INDEX.md, scripts/<batch>/env.sh), scratch `/scratch/fb31/SMC_Engineering_Department/` (INDEX.md, `runs/`, `archive/home_guard/`). Home guard `~/bin/home_guard.sh`.

## 4. Live threads
- Riboflavin agent (Sonnet, idle, waiting for DONE): `thread:delegated-task:command%3Amcp%3A3b799f3d-3ff0-40af-9f34-b6a918f97d53%3Adelegate-task%3Ae5106e3a-1ec0-4a7f-804b-b0a43cbb4bf5`.
- HQ v2: `mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e`, env `1fde6176-4453-43b0-82cc-70fda5110037` (t3_thread_send, mode queue). The old 647bfd65 thread is retired.
- No other live children; the daily Haiku children are settled after each report.

## 5. Scheduled tasks
- `scheduled-task:f9847b84-cc7a-4469-8903-0911f683756b`: the daily report at 08:40 CT. Its prompt already has the H-58, v2-address and ±3 rules. It is to be re-bound to v2.
- No other live task: everything else is disabled or a spent one-shot, and the 3-h riboflavin check is deleted.

## 6. Daily rules
- Check states directly. For any worker-dependent step, schedule your own check ≤ 30 min later; never end a turn waiting on a worker.
- **Hygiene route** (HQ a5e1ddc8 / f6263005 / H-57):
  1. rsync from NOTS to a new Owls unit `records/hygiene_<date>_nots/<name>/` with SHA256SUMS; check Owls = NOTS.
  2. Wait for the desktop pull to list the unit in `desktop_verified.txt`.
  3. Re-hash on NOTS, then `rm` by full literal paths (no globs).
  4. Add rows to `nots_scratch_removals.tsv`, a DELETED line in the NOTS INDEX, and one LOG line.
  Already-verified units are never re-sent, so new files need a new unit. Delete nothing without HQ.
- Owls `/`: alert on a ±3-point change from the last value, or > 95 %. SMC files live on NFS home, not on `/`.
- NOTS etiquette:
  - one ssh call per check;
  - a QOSMaxCpuPerUserLimit pending is INFO;
  - scancel only by exact job id;
  - home < 7 GiB (the daily prune; home_guard acts above 8,192 MB by its own rules);
  - the scratch purge is 14 days.
- Lean staffing (H-54, f2d52b22): Opus = manager only; Haiku for checks; Sonnet for real work. No Fable; no Codex without HQ. Reports ≤ 10 lines. Never touch BNP.

## 7. Read first
`POLICIES.md` (repo root) → HQ_DECISIONS.md (latest) → this file → `DECISIONS.md` (H-41…H-58) → `LOG.md` (last ~40 lines) → `LEDGER.md` (Totals) → `results/gc1m/GC_1M_BLOCK_SUMMARY.md` → `machines/DAILY_2026-11-24.md`.
