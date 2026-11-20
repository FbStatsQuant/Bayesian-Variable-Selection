# NOTS_HYGIENE_INVENTORY — pass of 2026-11-20 (before the 10⁵ rung outputs)

Sonnet worker, Owls → NOTS. Scope: fb31's own SMC Engineering trees only (`~/SMC_Engineering_Department`, `/scratch/fb31/SMC_Engineering_Department`).
Never touched: SMC_BVS_v3 deploy, /projects/ml75, $WORK, BNP, riboflavin inputs, F2 (`code_ws/VN_e993ece2_code`, every `bin/smcbvs4` with sha `da0cf85b…`), `GB_G1a/G1b/G2a/G2b`, `RG_*`, `T5_1e5`, `FREEZE_CHECK_1e5`, PROTECT.txt.
Method: 6 read-only ssh passes (find/du/sha, niced), then 3 delete calls (one ssh at a time, rung jobs untouched). Sizes are apparent bytes, GB = 10⁹. The older companion `machines/NOTS_HYGIENE_INVENTORY.md` is the 11-17 pass.
Removal log (path, bytes, sha, Owls unit, reason): `~/SMC_Engineering_Department/crews/home_hygiene/nots_scratch_removals.tsv` (730 rows) and `removals.tsv` (home prune).

## 1. Headline

| Area | Before | After | Note |
|---|---|---|---|
| NOTS **home** quota | 7,224 MB of 10,240 (71%) | **6,086 MB (59%)** | standing prune (2 superseded T3 nightlies, 1,009 MB) + 12 duplicate `build/` dirs (159 MB); deploy guard 7,900, HQ guard 8,192 |
| scratch `runs/` | 235.1 GB (31,969 files) | **211.3 GB** | 705 collected+verified files deleted (23.8 GB); `runs/` was 227.8 GB at the final `du` because RG_* kept writing |
| scratch other (code_ws 3.5, overlap1e4 0.17, vn_minileg 0.16, archive 0.34, slurm_out ~0, probes 0.12 MB) | ≈ 4.2 GB | ≈ 4.2 GB | 13 probe files (0.13 MB) removed; live `probe_out_R1.*` kept |
| `/scratch` filesystem | 887 T, 86% used (11-15) | 889 T, **78% used, 196 T free** | shared VAST, no per-user quota; **purge 14 d on atime** |

Growth since the last pass (11-17 → now): scratch dept 79 GB → 235 GB (the overlap, precision, vn_minileg, G-B legs: 4 families of run dirs); home 8,086 MB → 7,224 MB (the 11-18 prunes, T3 nightlies refill ≈ 0.5 GB/day). No core dumps anywhere (`find` on code_ws, runs, home dept: none). `squeue`: only RG_* jobs; nothing else queued.

## 2. Inventory (before the deletes), per area

Status codes: **C** collected to Owls records, unit sha-verified on Owls and in `desktop_verified.txt` · **N** needed on NOTS (rung / PROTECT / running) · **R** regenerable intermediate, not collected by design (LEG_PLAN §6.5, OFFLOAD §Volumes: "island files are not kept") · **U** unique copy, not on Owls.

### 2.1 scratch `runs/` by batch family (GB: before → after)

| Family | Dirs | Total | island | setup | calib | law | fit+eval | data+raw | After | Status / action |
|---|---|---|---|---|---|---|---|---|---|---|
| PL (precision 1e4: A0,B1,P1–P4,S1–S10) | 39 | 153.8 → **139.6** | 83.9 | 15.4 | 14.9 | 26.4 | 4.5 | 8.7 | 139.6 | fit/eval **C → deleted**; law 7.2 and setup 2.2 (A3 pairs) **C → deleted**; data 0.26 C deleted. Remainder = R (islands 83.9, calib 14.9, raw 4.3, setup 13.2, data 4.1) + **U law.bin 19.2 GB (142 files)** → pending |
| OV (overlap W0–W3, T/V/T2/V2) | 10 | 25.0 → **17.6** | 9.2 | 4.4 | 3.3 | 5.7 | 0.9 | 1.4 | 17.6 | fit/eval/law/data **C → deleted** (all law on Owls); rest R (islands 9.2, setup 4.4, calib 3.3, raw 0.7) |
| VN (vn_minileg V0–V2, ID) | 9 | 25.4 → **23.2** | 19.3 | 1.6 | 1.3 | 2.3 | 0.4 | 0.6 | 23.2 | fit/eval/law(13/16) **C → deleted**; rest R (islands 19.3, setup 1.6, calib 1.3); **U law.bin 0.5 GB (3 files)** |
| GB (G-B pilots G1a/G1b/G2a/G2b) | 4 | 25.2 | 14.3 | 4.0 | 3.2 | 1.5 | 0.9 | 1.3 | 25.2 | **N, PROTECT.** RG_T6 reuses `5-AR-n200-r01-V-s1` data/setup/calib; the twins reuse the pilots' data. fit/law/data are on Owls, but nothing deleted. |
| RG (10⁵ rung, running) | RG_1a, RG_1b (+RG_T6) | 3.3 and growing | | | | | | | 3.3 | **N**, untouched |
| T5_1e5 (old 10⁵ test) | 1 | 2.2 | 0.2 | 1.0 | 0.8 | – | – | 0.2 | 2.2 | U (not on Owls: setup/calib/data); fit.bin already offloaded 11-17/18. **Pending** HQ/ops (is it a rung fallback input? no reference found in RG/GB scripts) |
| FREEZE_CHECK_1e5 | 1 | 0.22 | 0.22 | | | | | | 0.22 | one freeze-check island (+ json); cited by the freeze gate → keep |
| tiny (F1M_pilot 7 files, P7, T6, g0, pmath, rerun2400, wp3_*, wp6_k3, sacct dumps ×40) | | < 0.01 | | | | | | | | keep (`*_sacct.txt` are cited cost sources) |

Grand total of the remaining non-protected intermediates (PL+OV+VN): islands 112.5, law 19.7 (U), setup 19.1, calib 19.4, raw 5.2, data 4.4 → ≈ 180 GB, none collected by design (R), 19.7 GB of it also unique (U).

### 2.2 other scratch trees

| Path | Size | Status | Proposed action |
|---|---|---|---|
| `code_ws/VN_e993ece2_code` | 347 MB / 11.2k files | **F2, never delete** | keep |
| `code_ws/{FREEZE_CHECK_1e5_code_freeze, OV_W0_T/T2/V/V2_code, PL_Feefcbc4a_code, W1/W2/W3_Feefcbc4a_code}` | 9 × 347 MB = 3.12 GB, 100k files | frozen code of finished batches; no script, no queued job references them (`grep code_ws` in scripts/ empty; `scontrol` WorkDir/Command) | **pending**: reproducible from git, but "frozen code" is on OFFLOAD's never-free list → delete only after a per-tree manifest equals `git archive <commit>` (verify on Owls, then one NOTS call) or an HQ waiver |
| `overlap1e4/`, `vn_minileg/` (scratch root) | 167 MB, 159 MB | not in INDEX.md (flagged by the 11-19 daily); contents not opened | **keep, ask** (cross-evaluator / law-data staging?) |
| `archive/home_guard/holding_*/ccd-cli_2.1.321…` | 342 MB | 11-09 holding copy; HQ "do not delete" | keep |
| `slurm_out/` | 12,738 files, 34 KB | finished-wave logs, bytes negligible, wave logs also in records `_batch_*/slurm_out` | keep (file count only; propose tar-and-drop at wave end, §5) |
| `tmp/` | empty (transient srun dirs) | – | none |
| probe_out_{G1,G2,V1,V2}.\*, probe_debug_V1.err | 0.13 MB | monitor scratch of finished legs | **deleted** (copy + SHA256SUMS: Owls `records/hygiene_20261120_nots/probe_out/`) |
| `probe_out_R1.*` | 0.05 MB | **live** (rung monitor) | keep |

### 2.3 home (`/home/fb31`, 7,224 MB before → 6,086 MB)

| Path | Size | Action |
|---|---|---|
| `.vscode-server` | 3.1 GB | standing prune only (`nots_home_prune.sh`; vscode LRU keeps 1) — not hand-deleted |
| `.t3` | 2.2 GB → ≈ 1.2 GB | standing prune removed nightlies 4877 + 4903 (1,009 MB); newest 2 (4941, 4954) kept |
| `.codex` 0.70 GB, `.claude` 0.42 GB, `R` 0.22 GB, `projects` 0.27 GB, `.local` 0.08 GB | | not ours to prune here |
| `SMC_Engineering_Department` (scripts/ 385 MB) | 386 → 227 MB | 12 duplicate `build/` dirs deleted (OV_W0_T/T2/V/V2, OV_W1–W3 T/V, PL_A0_1, PL_B1_2; `bin/smcbvs4` of identical sha kept in each). **`VN_ID_1/build` = F2 sha `da0cf85b` kept.** `FREEZE_CHECK_1e5/build_freeze` (16 MB) kept (freeze gate). |

### 2.4 binaries (all `smcbvs4` under home scripts, by sha)

F2 `da0cf85b` in GB_G1a/G1b/G2a/G2b, RG_1a/1b/T6, VN_ID_1 (+`build/`), VN_V0_1/2/3, V1_1/2, V2_1/2/3 — all kept. `d0c30b65` (PL_A0…PL_S10, 48 batches), the OV builds, `2197fd5b` (F1M), `b39754d6` (freeze) are old-build copies in `bin/` (2.3 MB each): kept, not worth the risk for 0.1 GB. Only the duplicate `build/` copies went.

## 3. What was deleted (and why it is safe)

730 deletions, **24.0 GB** in all, every one logged with bytes + sha:
1. **705 run-dir files, 23.83 GB** (PL/OV/VN: fit.bin, eval.bin, law.bin, data.bin, and the A3-pair setup.bin that the plan kept). Rule: Owls unit `records/<top>/<wave>/<run_id>` is in `crews/offload/desktop_verified.txt`; the file is in the unit's `SHA256SUMS`; the Owls copy was re-verified by `sha256sum -c` (705/705 OK, 0 mismatch); on NOTS the file was re-hashed and had to equal the manifest sha and size before `rm`. A `HYGIENE_REMOVED_20261120.tsv` tombstone sits next to the removals in each run dir. Excluded: GB, RG, T5, F1M, FREEZE; the guard script also aborts if any RG/GB script references an old run dir (none do).
2. **13 probe files (0.13 MB)** — copied to Owls first (own SHA256SUMS), sha re-checked on NOTS before `rm`.
3. **12 duplicate `build/` dirs (159 MB home)** — `build/smcbvs4` sha == `bin/smcbvs4` sha, not F2.
4. **Home prune** (standing job, `--apply`, fail-closed, 3/3 nodes readable): 2 T3 nightlies, 1,009 MB; logged in `removals.tsv`.

Moved-to-local-then-deleted: nothing needed a *new* transfer; the deletes relied on units that were already on Owls and desktop-verified. Only the 13 probes were copied (unverified on the desktop; they are trash, the Owls copy is a courtesy).

## 4. Pending (left in place on purpose)

| Item | Size | Why pending | What would close it |
|---|---|---|---|
| **U `law.bin`** of PL (142 files), VN (3) | **19.7 GB** | not collected by design (science reads d_H from `eval.bin.json`) but a unique copy; the 14-day purge will take it from 11-30 | HQ: (a) waive, or (b) one rsync unit `records/hygiene_20261120_nots/law/` (19.7 GB, SHA256SUMS), desktop pull, then delete |
| R islands (112.5 GB), calib (19.4), setup (19.1), raw (5.2), data (4.4) of PL/OV/VN | ≈ 160 GB | regenerable intermediates, not collected by design (LEG_PLAN/OFFLOAD "island files are not kept"); owner rule says copy-first when in doubt, and 160 GB would saturate the desktop 70% cap and the Owls 200 GB staging limit | HQ waiver ("regenerable bulk, bit-reproducible from manifests", the 11-17 D1 option) → delete; else keep until the 14-day purge |
| `T5_1e5` | 2.2 GB | setup/calib/data not on Owls | ops confirms not a rung input → delete after waiver, or move |
| 9 old `code_ws` trees | 3.1 GB | frozen code (see §2.2) | manifest-vs-`git archive` check, or waiver |
| `GB_*` (25.2 GB) | | PROTECT (rung RG_T6 + twins) | delete after the rung read-back closes |
| `overlap1e4/`, `vn_minileg/` at scratch root | 0.33 GB | contents unidentified | owner of the cross-evaluator confirms |
| `FREEZE_CHECK_1e5` | 0.22 GB | freeze gate evidence | keep until G-C |

## 5. Headroom

| | per fit (NOTS scratch, before any offload) | fits | total |
|---|---|---|---|
| 10⁵ (G-B pilot, N 10⁴, I_max 0) | **6.3 GB** (islands 3.55, setup 1.0, calib 0.78, law 0.37, fit 0.23, data+raw 0.32) | 10 rung + 2 T6 batches + 2 twins at N 2,500 (smaller: ≤ 6.3) | **≈ 90 GB** (RG_1a/1b already 3.3 GB) |
| 1M (F1M_pilot: islands 34.2, setup 10.1, calib 8.1, fit 2.4, data+raw 3.2, law 0.34 → 58.3 GB, 11-17 pass) | **≈ 58 GB** | 22 (S2) + 20 conditional seeds | **1.28 TB** (S2) / **+1.17 TB** (conditional) = **≈ 2.45 TB** |

- **Scratch**: 196 T free, no per-user quota → fits easily, even if nothing leaves. The binding constraints are the **14-day purge** (atime-based; the oldest unmoved file is dated 11-18 → purge from ≈ 12-02; the 19.7 GB unique law.bin is the only real loss risk) and the offload path.
- **Offload**: records of record at 1M ≈ 5–8 GB/fit → 22 fits ≈ 110–180 GB (42 fits ≈ 210–340 GB): fits the desktop 700 GB cap and Owls 200 GB staging only with the standing trim (OFFLOAD step 6). **1M islands (34 GB/fit) must not be offloaded**; they have to be deleted on NOTS after the merge (a rule decision for HQ before the 1M S2 starts, else 22 × 58 = 1.28 TB sits on scratch until it is purged or cleaned).
- **Home**: 6,086 of 10,240 MB. 7,900 (deploy guard) is 1.8 GB away; the T3 nightly refill is ≈ 0.5 GB/day, so the standing prune must run daily; the rung and 1M write nothing to home.

## 6. Standing rule proposal: wave-end hygiene check (report-only)

1. **Trigger**: after each wave's/leg's read-back (and at the daily 08:45 machines check): one niced ssh, `find -printf` on `runs/<batch>` only (no whole-tree `du`; it timed out at 540 s on 220 GB).
2. **Report line** (into `machines/DAILY_*.md`): `$HOME quota`, scratch dept GB by family, GB deleted since the last pass, files not collected to Owls (U), run dirs with units not yet desktop-verified, core dumps, stale probes, duplicate `build/`, `code_ws` trees not referenced, oldest atime (purge in N days).
3. **Worker auto-deletes only clear trash**: core dumps, finished-wave `probe_out*`, duplicate `build/` (sha == `bin/`, not F2/PROTECT/rung), temp/`.staging` dirs, and run-dir files that satisfy *all* of: unit in `desktop_verified.txt`, listed in the unit's SHA256SUMS, NOTS sha == manifest sha, batch not in PROTECT/rung/queued. Everything logged in `nots_scratch_removals.tsv` (+ tombstone).
4. **Everything else is reported, never deleted**: unique copies, R intermediates (islands/setup/calib), `code_ws`, GB/RG/T5, anything unmapped. Those go to HQ with a size and a proposed action; HQ/owner decides (waiver, move, or purge).
5. **Hard fences in the script**: allow-list of roots (the two dept trees), refuse symlinks, refuse names matching PROTECT, F2 sha, `GB_*`, `RG_*` while a job of that batch is queued/running, and abort if any live script references the target.
6. **Home**: the standing `nots_home_prune.sh --apply` daily at the machines check; the worker never hand-deletes in `.t3`/`.vscode-server`.
7. **Purge alarm**: any file not on Owls with atime older than 7 days is listed daily (NOTS_FACTS rule); 12 days → escalate to HQ.

### 6.1 Invocation (approved by HQ, H-41; script written 11-20)

- Script: `~/SMC_Engineering_Department/crews/home_hygiene/nots_wave_hygiene_check.py` (runs on **Owls**; stdlib Python; 2 niced ssh calls, ≈ 1 min; never run two at once or alongside a transfer).
  - **Report-only (default):** `python3 -I ~/SMC_Engineering_Department/crews/home_hygiene/nots_wave_hygiene_check.py` → stdout + `crews/home_hygiene/wave_check_<UTC>.md`.
  - **Clear-trash delete:** add `--apply-trash`. It deletes only (T1) core dumps, (T2) duplicate home `build/` dirs (sha == `bin/`, not F2), (T3) non-island run-dir files whose NOTS re-hash equals a line of a desktop-verified Owls unit's SHA256SUMS, in an unprotected batch with no live job. Every deletion is appended to `nots_scratch_removals.tsv`.
  - **Fences:** protected batches `^(GB_|RG_|T5_|F1M|FREEZE_CHECK)` + extra regexes in `NOTS_SCRATCH_PROTECT.txt` (HQ/ops add the next rung's batches there); batches named by any queued/running job; F2 sha `da0cf85b`; `code_ws/` and the clones are never deleted by the script; no symlinks; allow-listed roots only.
  - **Never automated:** unique copies, islands/setup/calib/raw, `code_ws`, probes, home (the standing `nots_home_prune.sh --apply` does home, daily).
- Report fields: home quota; live batches; scratch GB by family; files not in any desktop-verified unit by kind with days to the 14-day purge and U/R tag; core dumps; T3 candidate count (size-match upper bound); duplicate build dirs; `code_ws` trees and which script `code` symlinks point to them.
- Wiring (HQ): daily machines check → report-only; each wave end after the read-back → report, then `--apply-trash` once the wave's units are in `desktop_verified.txt`.
- First run 2026-11-20 14:11 UTC (report-only): 276.0 GB in `runs/` (RG 68.0 and growing), home 6,091 MB, 0 core dumps, 0 duplicate builds; the U list showed PL law.bin 18.9 GB + RG fit/law 5.5 GB still unique at that moment (RG fit/law are the rung's own, to be collected by its read-back).

## 7. Execution of HQ H-41 (2026-11-20, same day)

| Item | Result |
|---|---|
| Unique `law.bin` (PL 142 + VN 3 = 145 files, 19.69 GB) | NOTS sha256 (computed on NOTS) = Owls sha (3 m 06 s `sha256sum -c`, 0 mismatch) → 26 units `records/hygiene_20261120_nots/law_<batch>/<run_id>/law.bin` (one SHA256SUMS per unit, none nested; one rsync, staging outside `records/` emptied) → all 26 desktop-verified at the 09:20 pull → NOTS re-hash = sha → 145 deleted |
| `T5_1e5` (2.2 GB, 16 files) | unit `records/hygiene_20261120_nots/T5_1e5`, per-file sha equal on both sides, desktop-verified, run dir deleted (file count and every sha re-checked on NOTS first) |
| 9 old `code_ws` trees (3.1 GB) + `overlap1e4/clone_eefcbc4a` (0.17 GB) | streamed from NOTS as 10 tarball units `records/hygiene_20261120_nots/code/<name>/<name>.tar.gz` (stream sha on NOTS = file sha on Owls; `gzip -t` OK; 12,761 entries in a sample listing), desktop-verified, deleted. Tarballs are ≈ 172 MB each (the repo snapshot, so a tree can be re-created by `tar -xzf`) |
| **Kept, F2** | `code_ws/VN_e993ece2_code` and **`vn_minileg/clone_e993ece2`**: the second is the git clone that backs the live F2 worktree (`.git` pointer `…/vn_minileg/clone_e993ece2/.git/worktrees/VN_e993ece2_code`); deleting it would break F2. Both fb31-owned, created 11-19 11:46 (matches the VN leg log). Re-checked present after the deletes. |
| `overlap1e4/` | fb31-owned, created 11-18 09:16 (matches the overlap freeze log); contained only the shallow git clone eefcbc4a that backed the 6 old worktrees → offloaded, deleted, empty dir removed |
| Side effect | the home `scripts/{OV_W0_T,T2,V,V2,OV_W1..3_T/V,PL_A0_1,PL_B1_2}/code` symlinks now dangle (those batches are finished and collected; the tarballs restore them) |

Totals this item: 156 deletions, 25.2 GB, home 6,091 MB unchanged (these were scratch). Log: `nots_scratch_removals.tsv`.
