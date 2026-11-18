# INVENTORY — SMC-BVS material on NOTS and Owls (machines crew, leg 1)

> **Scope rule (owner via HQ, 2026-11-15):** Engineering works only inside `SMC_Engineering_Department` on each machine
> (plus its NOTS scratch link). Everything else in `/home/fb31` on Owls or NOTS is **out of scope**: not inventoried,
> moved, cleaned or touched. The only exceptions are the HQ-approved SMC-BVS moves and the home guard. Out-of-scope rows
> below are withdrawn.


SMC - Engineering, Opus 5.5 helper, 2026-11-15 ~20:00–20:35 CT. **Read-only.** Nothing was moved, deleted or written on NOTS.
No sbatch or srun. Brief: `../briefs/BRIEF_opus_machines_inventory.md`. Companion files: `REORG_PLAN.md`, `CREW.md`.

Department roots (owner, POLICIES §12 rules 8–9, fixed 2026-11-15):
- `ENG_ROOT_NOTS = ~/SMC_Engineering_Department/` (home, light only: `INDEX.md`, `scripts/`, `results/`, `crews/`) with
  `scratch -> /scratch/fb31/SMC_Engineering_Department/` (`runs/ slurm_out/ tmp/ data/ archive/`, all empty at reading).
- `ENG_ROOT_OWLS = /home/fb31/SMC_Engineering_Department/` (`tmp/ bench/ crews/ logs/ staging/`, `INDEX.md`).

Classes: **ACTIVE** (in use, or referenced by a live ticket) · **IDLE-KEEP** (results of record, frozen code, manifests) ·
**TEMP** (caches, holdings, temporaries) · **UNKNOWN** (owner unclear: listed, never proposed for deletion).

## 0. Headline numbers

| Item | Value | Command |
|---|---|---|
| NOTS home quota | **6,761 MB of 10,240 MB (66%)**, 90,394 files; guard 8,192 MB not reached | `quota -s \| grep -A1 export/nots/home \| tail -1` (loginx2) |
| NOTS `/scratch/fb31` total | **1.2 GB** (after the Oct 21–22 relocations to the laptop) | `nice du -sh /scratch/fb31` |
| NOTS queue | **empty** (`squeue -u fb31`: no jobs) → nothing on NOTS is IN USE by a job | `squeue -u fb31` |
| Owls root `/` | **61 G of 70 G used (87%), 9.6 G free — above the 85% alert line** | `df -h /` |
| Owls `/tmp` (fb31, excluding `claude-*`) | 995 entries, **1.58 GB**; `/tmp/claude-71711` a further 2.0 GB (shared, never touched) | see §4.4 |

SMC-BVS totals by class (NOTS + Owls strays; worktrees and the main checkout are listed separately in §4):

| Class | NOTS scratch | NOTS home (SMC-BVS) | Owls strays | Total |
|---|---|---|---|---|
| ACTIVE | 437 MB (`w3scale` 434 M, `theory_w3` 3.2 M) | 3.4 MB (`projects/BVS/theory_w3`) | 0.6 MB (`p1m_g0_dryrun`) + 303 MB (`/tmp/bvs-ci-sandboxes`, CI, in use) | **≈ 744 MB** |
| IDLE-KEEP | 433 MB (`theory_w2`) | ≈ 168 MB (`projects/BVS` excl. deploy and theory_w3: campaign-I tree ≈ 40 M, `Others` ≈ 117 M, `theory_w2` 11 M) | 0.2 MB (`p1m_feas_bench`) | **≈ 601 MB** |
| TEMP | 332 MB (`home_holding_20261111` 331 M, `home_holding_20261112` 0.9 M, `home_guard/` 0) | — | 24 KB (`/tmp/smcbvs_B_verify_20261022_dev`) | **≈ 332 MB** |
| UNKNOWN | ≈ 0.7 MB (loose files at the `/scratch/fb31` root, `.claude-science/` 44 K) | — | see §4.3 (≈ 1 GB of unclear dirs in `/home/fb31`, not counted as SMC-BVS) | **≈ 0.7 MB** |
| EXCLUDED | — | `Others/SMC_BVS_v3_history_Oct2026/deploy/` (not measured; ≈ 42 MB by Others/INDEX.md arithmetic) | — | — |

## 1. Exclusions (not descended)

- `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/` **does not exist at that path** (`ls -ld` → "No such file or directory").
  The 2026-11-04 reorganisation (BVS-REORG, D99) moved `SMC_BVS_v3/` whole to
  **`/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/`**, so the excluded tree now sits at
  **`.../Others/SMC_BVS_v3_history_Oct2026/deploy/`** (found by a depth-5 `find ... -prune` that stops at the name,
  without listing inside). I treated that path as excluded: no `ls`, `du` or `find` inside it. Its siblings `core/` and
  `prototype_profiling/` were measured one by one. **The briefs and POLICIES quote the old path; HQ should update the
  exclusion wording** (21 repo files cite `SMC_BVS_v3/deploy`).
- `/projects/ml75`: not visited.
- Non-SMC-BVS projects on NOTS, sized only: `~/projects/Quant_Reg` 101 M, `~/projects/Large Prior_ Sims` 2.7 M,
  `/scratch/fb31/qr_data/` (empty `inner_joint/`).

## 2. NOTS `/scratch/fb31` (all of it)

All directories show `4096` in `ls` and `total 0` (VAST); sizes are `du -sh`. "Newest" is the newest file mtime inside.

### 2.1 Top level

| Path | Size | Files | Newest | What it is | Repo files citing it | Class |
|---|---|---|---|---|---|---|
| `w3scale/` | 434 M | 1,553 | 11-12 | Theory ticket **W3-SCALE** (`Theory_work/Wave3/W3-SCALE`) profiling and B3 census jobs (p = 1k…20k), jobs 2692663–2698180. **`code/v32dev_6866f57` is the code under test of the live P1M G0 leg; `out/b3_p*/res/census_p*.rds` are read by P1M REQUESTS R5/R6** | 4: `Docs/Experiments/P1M/{REQUESTS.md, REVIEW_fable.md, briefs/BRIEF_opus_g0_scripts.md}`, `Theory_work/INFRA/NOTS_STORAGE.md` | **ACTIVE** (live ticket refs) |
| `theory_w3/` | 3.2 M | 1,858 | 11-14 | Theory **W3-P6** run outputs (b1, b2, probe01, s1_*, smoke) and Slurm logs; jobs 2647903–2689423. `Theory_work/Pause_2026-11/RESUME_PLAN.md` plans a resubmission of b1-remainder and b2 (needs owner greenlight) | 5: `Theory_work/Wave3/W3-P6/{LOG.md, nots/run_table.sh, nots/submit_table.sh}`, `Theory_work/Pause_2026-11/RESUME_PLAN.md`, `Theory_work/INFRA/NOTS_STORAGE.md` | **ACTIVE** (pending resume; Theory) |
| `theory_w2/` | 433 M | 5,957 | 11-09 | Theory **W2-SIM** run outputs (pilots and production probes, FAC-PK, LOC, S5, X); jobs 2632784–2634898, all finished 11-09 | 19, all `Theory_work/Wave2/W2-SIM/**` (INFRA, LOG, DESIGN files, configs, `nots/run_table.sh`, `nots/submit_table.sh`, results manifests) | **IDLE-KEEP** (Theory) |
| `home_holding_20261111/` | 331 M | 2 | 11-11 | home-guard holding: old Claude CLI binary `ccd-cli_2.1.321-…` (326 MB) and `codex_db-backups_193124.tgz` (4.5 MB) | `Theory_work/INFRA/NOTS_STORAGE.md` | **TEMP** (HQ infra) |
| `home_holding_20261112/` | 947 K | 1 | 11-12 | home-guard holding: `codex_db-backups_160748.tgz` | same | **TEMP** (HQ infra) |
| `home_guard/` | 0 | 0 | — | output dir of the prepared, never-submitted `~/bin/home_guard_job.sh` | same | **TEMP** (empty) |
| `.claude-science/jobs/` | 44 K | 12 | 09-25 | three job UUID folders of an old agent tool | none | **UNKNOWN** |
| `qr_data/inner_joint/` | 0 | 0 | — | Quant_Reg project (not SMC-BVS) | 2 (campaign ops cleanup docs) | out of scope |
| `SMC_Engineering_Department/` | 0 | 0 | 11-15 | new department scratch root (empty skeleton) | brief only | ACTIVE (new) |
| loose files at the root (40 files, ≈ 0.65 MB) | | | 09-29…10-22 | (a) **relocation records of 10-21/22**: eight `scr_*_MOVED.md` / `qr_small_del2_MOVED.md` (each names the laptop destination, bytes, and a checksum list) and the tools `cksum_units.sh`, `del_unit.sh`, `mkchunks.sh`, `mkunits.sh`; (b) older QR/other-project files: `air_*`, `k2_seed10_ids.txt`, `sqrtn_*`, `uext_*`, `spod_proc.log`, `submit_p1only*`, `patch_sqrtn.sh`, `diagnose_cycle1.R`, `final_tab.R`; (c) `fsb_deploy{,_v2,_v3}.tar.gz`, `h1v1_deploy_v1.tar.gz`, `h1v1_*.sh`, `SOURCE_SHA256SUMS_h1v1_v1` (project not identifiable from names) | none for the individual files | **UNKNOWN** (a: owner's records; b, c: probably not SMC-BVS) |

**Finding:** every `*_MOVED.md` says its checksum list is at `/scratch/fb31/_relocation_manifests/*.sha256`; **that
directory no longer exists** (`ls -d` → No such file). The checksums survive only on the laptop, if at all.

The relocations they record (all off NOTS to the owner's laptop, 10-21/22): `BVS` 35.0 GB, `v3_profiling_20261020`
22.5 GB, `archive_staging` 10.1 GB, `Experiments_October_14_Mixture` 4.1 GB, `qr_data/*pmala*` 5.6 GB,
`onizuka_air_runs_20260915` 2.0 GB, `BVS_Paired_October_14` 0.48 GB, `backups` 16 MB.

### 2.2 Second level (size · files · newest)

`w3scale/`: `out/` 425 M · 854 · 11-12 · `code/` 7.1 M · 113 · 11-12 · `runs/` 2.0 M · 391 · `stage/` 614 K · 190 ·
`nots/` 5 K · 3 (`env_scale.sh`, `run_task.sh`, `submit.sh`) · `tasks/` 1 K · 1 · `submissions.jsonl` 15 K (last entries:
b3_p10000 job 2698179 and b3_p20000 job 2698180, submitted 11-12 13:31Z).

`theory_w2/` (all newest 11-09): `loc_pilot02` **377 M** · 42 (one array task cancelled) · `fam_X` 38 M · 105 ·
`prod_diag02` 5.4 M · `x_Q5pilot01` 3.6 M · `x_A1` 2.5 M · `loc_pilot01` 2.2 M · `pk_r1_01` 1.2 M · 2,162 ·
`pk_r3_01` 1.1 M · `pk_s5iid_01` 961 K · `pk_s5ex_01` 752 K · `x_BS1` 339 K · `x_B1` 287 K · `s5_pilot02` 180 K ·
`loc_pilot03`, `pk_pilot01`, `pk_val01`, `prod_probe01`, `s5_pilot01`, `s5_pilot03`, `smoke01`, `x_Cpilot_a/b`,
`x_pilot02`, `x_pilot_k01` (each < 100 K) · `prod_diag01` empty (cancelled).

`theory_w3/`: `b1` 1.8 M · 1,261 · `probe01` 642 K · `analysis` 192 K · `s1_b1r` 134 K · `s1_b_hw`, `s1_c_hw` 64 K ·
`s1_h1`, `s1_h2`, `s1_g1`, `s1_g2`, `s1_d1`, `s1_d2`, `smk1_v3`, `b2` (19 K, cancelled 11-09), `smoke_v3`, `smk1_v2`,
`s1_b`, `s1_c`, `s1_d1hw` (each < 40 K). Newest file 11-14 (`s1_d2`).

## 3. NOTS `/home/fb31`

### 3.1 Top level (`nice du -sh`, mtime of the directory)

| Path | Size | Mtime | What | Class |
|---|---|---|---|---|
| `.vscode-server` | 2.7 G | 11-15 | VS Code server builds + extensions (largest home item) | not SMC-BVS; guard-managed |
| `.t3` | 1.6 G | 11-02 | T3 runtime builds | not SMC-BVS; guard-managed |
| `.codex` | 662 M | 11-15 | Codex releases, sessions, db-backups | not SMC-BVS; guard-managed |
| `.claude` | 406 M | 11-15 | Claude CLI remote builds | not SMC-BVS; guard-managed |
| `projects/` | ≈ 0.27 G | 10-01 | `BVS` (§3.2), `Quant_Reg` 101 M, `Large Prior_ Sims` 2.7 M | see §3.2 |
| `R` | 212 M | 09-25 | user R library | keep (never touch) |
| `.local` | 73 M | 09-11 | pip user site | keep |
| `.t3-recovery` | 12 M | 10-22 | T3 recovery | not SMC-BVS |
| `archive` | 5.1 M | 09-26 | older home archive | UNKNOWN |
| `.cache` | 188 K | 11-02 | caches (guard cleans files > 2 d) | TEMP (guard) |
| `bin` | 44 K | 11-11 | `home_guard.sh`, `home_guard_job.sh`, `check_project_paths.py`, `prepare_nots.sh`, `codex` symlink | keep (HQ infra) |
| `SMC_Engineering_Department` | small | 11-15 | new department root: `INDEX.md`, `scripts/`, `results/`, `crews/`, `scratch` symlink | ACTIVE (new) |
| others (`.dotnet`, `.copilot`, `.ipython`, `.config`, `.ssh`, `.conda`, `.nv`, `.mozilla`, `lib`, `Python`, `archive_control`, …) | each < 300 K | | | not SMC-BVS |
| `home_guard.log` | 3.3 K | 11-12 | guard log (last run 11-12 16:07: 8,333 → 6,704 MB) | keep |

No `.cpp_cache` or R compile cache shows at the home top level; the frozen trees carry their own `.cpp_cache` (excluded
from `INDEX.tsv`). The sum of the measured items is ≈ 5.9 GB against 6,761 MB on the quota line: the server-side block
accounting runs ≈ 0.6 GB above `du` (NOTS_STORAGE.md §1), plus the excluded `deploy/` (≈ 42 MB).

### 3.2 `/home/fb31/projects/BVS` (excluding `Others/SMC_BVS_v3_history_Oct2026/deploy`)

The campaign-I research space, already reorganised and self-indexed on 2026-11-04 (`README.md`, `INDEX.tsv` 1.0 MB with
sha256 per file, `tools/check_bvs.sh`, `Records/reorg_20261104/MAP_old_to_new.tsv`).

| Path | Size | Files | Mtime | What | Class |
|---|---|---|---|---|---|
| `Benchmarks/` | 9.2 M | 604 | 11-04 | 8 competing methods (frozen p >> n tree + bench_v2, bench_lowp, scoring) | IDLE-KEEP (frozen) |
| `Studies/` | 5.1 M | 528 | 11-04 | frozen run bundles of campaign I (high_p 2.0 M, low_p 3.0 M, conformance) | IDLE-KEEP |
| `SMC_BVS/core/` | 2.0 M | 37 | 11-04 | **frozen v2.2.1 code** (27-file SHA256SUMS; DO NOT EDIT) | IDLE-KEEP (frozen) |
| `Methodology/` | 2.1 M | 17 | 11-04 | method documents, conformance, Theory | IDLE-KEEP |
| `Data_Generation/` | 1.7 M | 24 | 11-04 | generators + input manifests (data itself on the laptop) | IDLE-KEEP |
| `Records/` | 1.5 M | 31 | 11-04 | campaign records, reorg map | IDLE-KEEP |
| `Main_Results/` | 700 K | 23 | 11-04 | headline results | IDLE-KEEP |
| `Analysis/` | 596 K | 61 | 11-04 | scoring + analysis scripts | IDLE-KEEP |
| `Exact/lowp_enum/` | 400 K | 47 | 11-04 | exact enumerator | IDLE-KEEP |
| `Environment/` | 88 K | 13 | 11-04 | env scripts, path allowlist | IDLE-KEEP |
| `tools/` | 52 K | 4 | 11-04 | `check_bvs.sh`, `make_index.sh`, … | IDLE-KEEP |
| `README.md`, `INDEX.tsv` | 1.06 M | 2 | 11-04 | index of the space | IDLE-KEEP |
| `theory_w2/` | 11 M | 461 | 11-09 | Theory W2-SIM code (8.2 M), runs (task tables, 1.1 M), sim (WorkDir of all W2 jobs) | IDLE-KEEP (Theory) |
| `theory_w3/` | 3.4 M | 235 | 11-09…11-13 | Theory W3-P6 code, configs, runs (task tables), sim (WorkDir of W3 jobs) | ACTIVE (pending resume; Theory) |
| `Others/library_portable/` | 102 M | 3,620 | 10-07 | legacy R library (mode r-x) for the Oct-4 releases only | IDLE-KEEP (Others/INDEX: "safe to delete with releases", owner decides) |
| `Others/benchmark_releases_Oct2026/` | 4.6 M | 432 | 10-04 | three hash-named Oct-4 benchmark releases | IDLE-KEEP (same) |
| `Others/SMC_BVS_v3_history_Oct2026/core` | 3.3 M | 157 | 10-22 | v2.1 cores (`v2_frozen` = identity baseline) | IDLE-KEEP |
| `Others/SMC_BVS_v3_history_Oct2026/prototype_profiling` | 7.4 M | 498 | 10-22 | Oct 20–22 profiling study | IDLE-KEEP |
| `Others/SMC_BVS_v3_history_Oct2026/deploy` | not measured | — | 10-22 | **EXCLUDED** | EXCLUDED |
| `Others/superseded_code/v2_2/` | 312 K | 25 | 10-28 | v2.2 (needed by CONF_NOTS_IDENTITY reruns) | IDLE-KEEP |

Repo files citing `projects/BVS/SMC_BVS`: 24 (P1M BRIEF and briefs, POLICIES.md, HQ history, SMC_BVS_v3_deploy records,
campaign conformance/ops docs, `Scripts/Exact/tinyp_check/tinyp_job.sh`, …). `projects/BVS/theory_w2`: 36 files
(`Theory_work/Wave2/W2-SIM/**`). `projects/BVS/theory_w3`: 6 files. `projects/BVS/Others`: 3 (campaign ops cleanup).

## 4. Owls

### 4.1 Strays and department folders (SMC-BVS)

| Path | Size | Last change | What | In use? | Class |
|---|---|---|---|---|---|
| `/home/fb31/p1m_g0_dryrun/` | 556 K (growing) | 11-15 20:25 | P1M G0 dry run: `revD/` code copy, `stage/`, `kernel/`, `work/`, hash files | **YES**: `Rscript stage_measure.R --core-dir /home/fb31/p1m_g0_dryrun/revD/... --out /home/fb31/p1m_g0_dryrun/stage/stage_p1000.rds` (pid 2754751, nice 19, started ≈ 20:24) | ACTIVE |
| `/home/fb31/p1m_feas_bench/` | 176 K | 11-15 20:02 | P1M feasibility micro-bench (Fable): `feas_bench.cpp`, binary, `core_copy/`, run1/run2 logs, README | no | IDLE-KEEP (small) |
| `/home/fb31/bvs_tmp/` | 4 K + `engineering/20261115-g0-dryrun/RtmpjaTTB8` | 11-15 20:26 | Theory/CI temp convention (README). Engineering **no longer uses it**; the G0 helper's `engineering/20261115-g0-dryrun/` (an R temp dir) is still there | G0 helper's TMPDIR (likely live) | ACTIVE (G0) |
| `/home/fb31/SMC_Engineering_Department/` | small | 11-15 20:26 | `ENG_ROOT_OWLS`: `INDEX.md`, `tmp/{20261115-g0-dryrun (empty), 20261115-machines (this leg's TMPDIR)}`, `bench/`, `crews/`, `logs/`, `staging/` | yes | ACTIVE |
| `/home/fb31/Bayesian-Variable-Selection/` | 652 M | 11-15 | main checkout (`main`) | yes | keep |

This leg's own temporaries: I first created `/home/fb31/bvs_tmp/engineering/20261115-machines/` (as instructed at the
time), then moved it to `/home/fb31/SMC_Engineering_Department/tmp/20261115-machines/` when the root was fixed. It holds
one file (`tmp_du.tsv`, the `/tmp` size list) and is removed at the end of this leg.

### 4.2 `/home/fb31/BVS-wt/*` (17 worktrees, ≈ 5.4 GB without `.git`)

Size = `du -sh --exclude=.git`; last use = last commit time (all 11-15); dirty = `git status --porcelain | wc -l`.

| Worktree | Branch | Size | Last commit | Dirty |
|---|---|---|---|---|
| `record-1115` | `recorder/staging-1115` | **608 M** (incl. ignored `_scratch/` **538 M**) | 19:57 | 0 |
| `W3-DIST` | `theory/W3-DIST` | 365 M | 20:15 | 0 |
| `W3-READER` | `theory/W3-READER` | 306 M | 20:25 | 4 |
| `WRITING` | `writing/main` | 306 M | 19:47 | 0 |
| `citefix` | `theory/W3-EDIT-citefix` | 304 M | 20:15 | 0 |
| `LEAN` | `lean/BVSCert` | 304 M | 19:21 | 0 |
| `PSMC-S0` | `theory/PSMC-S0` | 304 M | 19:57 | 0 |
| `rec-main` | `hq/record-main` | 304 M | 20:18 | 0 |
| `THEORY-DEPT` | `dept/theory` | 304 M | 20:24 | 0 |
| `W3-EDIT` | `theory/W3-EDIT` | 304 M | 20:22 | 0 |
| `W3-MISR-R` | `theory/W3-MISR-R` | 304 M | 19:27 | 0 |
| `W3-PSHARP-R` | `theory/W3-PSHARP-R` | 304 M | 20:06 | 8 |
| `W3-RM2-R` | `theory/W3-RM2-R` | 304 M | 20:18 | 1 |
| `W3-START2-R` | `theory/W3-START2-R` | 304 M | 19:46 | 0 |
| `POST2-diff` | `theory/W3-POST2-diff` | 298 M | 17:43 | 11 |
| `P1M` | `exp/P1M` | 296 M | 20:22 | 0 |
| `actions-ci` | `infra/actions-ci` | 295 M | 16:30 | 0 |

All are live today. Worktrees are allowed locations; Engineering owns only `P1M`. Note for HQ: each worktree is a
≈ 300 MB full checkout on NFS `/home` (≈ 3 TB free, so not urgent).

### 4.3 Other `/home/fb31/*` directories: **WITHDRAWN** (owner, 11-15: not Engineering's; not inventoried)

### 4.4 Owls `/tmp` (SMC-BVS only) — **out of scope** after the owner's rule; kept as a record of the 11-15 crew job (HQ-commissioned)

- fb31 owns 1,037 top-level entries in `/tmp`; excluding `claude-*`, 995 entries, 1,619,036 KB (≈ 1.58 GB).
- **Clearly BVS-named:**
  - `/tmp/bvs-ci-sandboxes/` 303 MB (`sb-w91e8vqb/` + `.lock`), newest file 11-15 20:26. **IN USE**: `lsof` shows python
    pid 2708093 holding the lock and python pid 2755511 with its cwd inside the sandbox. Owner: CI department. Its
    `/tmp` placement contradicts the new convention; CI should move it to `/home/fb31/bvs_tmp/ci/` (CI's call).
  - `/tmp/smcbvs_B_verify_20261022_dev/` 24 KB (a `venv/`), newest 10-22: idle, BVS-named, > 24 h → TEMP candidate
    under CREW rule T2.
- **Not clearly BVS-named (report only):** ≈ 60 `Rtmp*` (10-01 … 10-18), 17 `fb31_strat_*` + `strat_cpp_fb31_0_0`,
  `fb31_s6m`, `fb31_nots_in`, `fb31_rt`, `gtest_fb31` (all 10-13), `v6bench_*`, `c5-b5fix-*` (≈ 355 MB), `final-pool-*`,
  `b7-/b8-/b9-*-r1` paper-review folders, `torchinductor_fb31`, `mcp-*`, `node-compile-cache`, `cursor-agent-logs-71711`.
- **BNP files (never touched):** `bnp-*`, `bnp_*` (≈ 360 MB, incl. `bnp-c3-sol-batch6c-*` 165 MB, `bnp-c5-sol-*` 136 MB).
- **Shared Claude folders (never touched):** `/tmp/claude-71711` 2.0 GB, `claude-skill-*.zip`.

## 5. In-use check (NOTS)

- `squeue -u fb31`: **empty** (no queued or running jobs at ≈ 20:30 CT).
- `sacct -u fb31 -S now-7days -X --format=JobID,JobName%30,State,WorkDir%80` (run once): WorkDirs of the last 7 days are
  only `/home/fb31/projects/BVS/theory_w2/sim`, `/home/fb31/projects/BVS/theory_w3/sim`, `/home/fb31/projects/BVS/theory_w3`
  and `/scratch/fb31/w3scale`. All finished, failed, timed out or cancelled. So **nothing is IN USE by a job**; `w3scale` and
  `theory_w3` are ACTIVE only through live-ticket references (P1M G0/R5/R6; W3-P6 resume plan).
- The home guard is **not scheduled** (scrontab disabled; `home_guard_job.sh` never submitted; last run 11-12 by hand).

## 6. Commands used (all read-only; NOTS calls sequential, one connection)

NOTS, 9 sequential `ssh nots` calls in total, each batching several commands, all `du`/`find` run with `nice` and `timeout`,
one `du` at a time, squeue/sacct once:
```
hostname; quota -s | grep -A1 export/nots/home | tail -1; ls -la /scratch/fb31 /home/fb31 /home/fb31/projects/BVS
cat /scratch/fb31/*_MOVED.md; ls -la /home/fb31/projects; ls -ld /home/fb31/projects/BVS/SMC_BVS_v3; ls -la <scratch subdirs>
ls -la /home/fb31/projects/BVS/SMC_BVS /home/fb31/projects/BVS/SMC_BVS/*/
nice find /home/fb31 -maxdepth 5 \( -name SMC_BVS_v3 -o -name deploy -o -path <big dot-dirs> \) -prune -print
for d in <home top dirs>: timeout 60 nice du -sh "$d"; stat -c %y "$d"
for d in <projects/BVS */ and */*/, Others children, history/core, history/prototype_profiling>: timeout 60 nice du -sh; timeout 60 nice find "$d" -type f | wc -l
cd /scratch/fb31; ls -d _relocation_manifests; timeout 120 nice du -sh .; for d in */ */*/: nice du -sh; nice find -type f | wc -l; newest mtime
squeue -u fb31; sacct -u fb31 -S now-7days -X --format=JobID,JobName%30,State,WorkDir%80
tail ~/home_guard.log; head projects/BVS/README.md, Others/INDEX.md, SMC_BVS/README.md; ls w3scale/{nots,tasks}; ls ~/bin
ls -la ~/SMC_Engineering_Department /scratch/fb31/SMC_Engineering_Department; cat ~/SMC_Engineering_Department/INDEX.md
```
Owls (`nice -n 19`, `TMPDIR` set to the department tmp folder): `df -h /`; `ls -la /home/fb31 /home/fb31/BVS-wt`;
`du -sh` per stray and per worktree (`--exclude=.git`), `git -C <wt> branch --show-current / log -1 / status --porcelain`;
`find /tmp -maxdepth 1 -user fb31 ! -name 'claude-*' -print0 | xargs -0 du -s`; `lsof +D /tmp/bvs-ci-sandboxes`;
`ps -eo pid,etime,args | grep p1m_g0_dryrun`; repo: `git grep -l --untracked -F <path>` for each old path.
