# REORG Owls plan (Phase 0, read-only), Opus-OWLS, 2026-11-25

Spec: `REORG_SPEC.md` (binding). ROOT = `/home/fb31/Bayesian-Variable-Selection` (the shared root clone on `main`; its branch
and tracked tree are never touched). Inventory taken 2026-11-25 ~16:35–17:20Z, read-only (`du --apparent-size`, `git status`,
`git rev-list`, the T3 state DB read in `mode=ro`). One `git fetch --prune origin` refreshed remote refs before the
unpushed counts. Raw tables (Owls scratchpad): `wtstat.tsv`, `ign.tsv`, `live.tsv`, `tmp_sizes.tsv`, `theory_du.tsv`.

**Same filesystem.** `~`, `~/.t3`, `~/BVS-wt`, all departments and ROOT are on the same NFS export (`stat -c %d` = 51 for
all). Every `mv` below is a rename: metadata only, seconds, mtimes and atimes kept. `/tmp` is the local root fs (`/dev/sde3`,
70 GB, **92 % full**).

## 1. Inventory (apparent bytes)

| source | size | content / note |
|---|---:|---|
| `~/SMC_Engineering_Department/` | **≈ 435 GB** | `records/` 413.73 GB (21 groups, 715 desktop-verified units), `tmp/` 17.21 GB (incl. 16 git worktrees ≈ 5.3 GB, ribo 0.04 GB), `staging/` 4.03 GB (4 git worktrees), `envs/` 0.32, `Rlib/` 0.11, `crews/` 0.01, `scripts/` (NOTS batch-script copies), `bench/`, `logs/`, `7d/`, `INDEX.md` |
| ↳ `tmp/20261118-riboflavin/` | 0.04 GB | **exception 1** (ribo-s1..5 running; @reboot line); untouched |
| `~/SMC_Theory_Department/` | **≈ 81 GB** | `tmp/` ≥ 18 GB (11-16…11-23 recorder clones/probes: RL 4.10, RD 3.57, TA 3.46, D95 2.38, RD2 1.78, …; **20 standalone git clones**), `ci/` (sandboxes, venv-numerics, `bvs_r06_*/LF` clone), `records/` (theory_w2/w3, w3_* numerics: data of record, kept), `refs/` (2 PDFs), `recorder/20261116-T` (a clone), `helpers/`, `logs/`, `BENCH_*`, `SMC_LIT*` |
| `~/SMC_Writing_Department/` | 1.4 MB | `SAM_STYLE_papers/` (2 PDFs) |
| `~/Papers_local/` | 63 MB | `Papers/{Benchmark_methods,Core_bibliography,Priors_and_decision_rules,SMC}` (copyrighted PDFs) |
| `~/BVS-wt/` (28 worktrees) | 9.0 GB | ≈ 0.30 GB each (tracked checkout); ignored 0.97 GB in total (live ones included) |
| `~/.t3/worktrees/Bayesian-Variable-Selection/` (100 + 1 nested) | 32 GB | ≈ 0.3 GB checkout each + ignored 8.63 GB (`.rc_tmp/` review dirs 7.4 GB, `.venv`/`.uv-cache` 0.43 GB, `theory_campaign/A-DRAFT/reading/` 289 MB) |
| ENG nested worktrees (16 in `tmp/`, 4 in `staging/`) | ≈ 6.5 GB | detached or `exp/P1M-*` branches, 0 unpushed |
| `~/theory_campaign/` | 21 MB | Nov-2 SMC theory campaign (A-REV3…8): SMC, orphaned |
| `~/bvs_tmp/` | 1 KB | retired Theory tmp (README + empty `ci/`) |
| `~/.cache/bvs_ci_out_dept_cite`, `~/.cache/bvs_sweep_ci` | 3.5 KB | SMC CI caches (the rest of `~/.cache`, 16 GB uv/hf/pip/mathlib, is shared tooling: untouched) |
| `/tmp` SMC items | 151 MB | `bm_check` 8.1, `bm_check2` 4.5, `cite_A/B/C` 4.8, `claude-d18c` 133.7 (scratch .py + `S.npy`), `litsmc`, `smcbvs_B_verify_20261022_dev`, `bvs-ci-sandboxes` (empty) |
| `/tmp/claude-71711/*BVS*\|*Bayesian-Variable*` | 231 MB | live cwd dirs: THEORY-DEPT 119.5, ROOT 75.2, P1M 26.6, WRITING 8.0; stale (t3 worktrees, W3-*, PSMC-S0, BVS-GH*) ≈ 2 MB |
| `~/.config/bvs-hq/` | 5.1 MB | **exception 4** (snap cron, owls guard, gh/API tokens); references only |
| crontab | — | 13 snapshot lines, owls-guard @reboot, BNP usage line, ribo @reboot |
| systemd --user | — | `ribo-s1..5` (transient; exception 1), `owls-guard` (HQ), `t3code`, BNP timer: no SMC unit to edit |

Not SMC (or mixed / owner's), untouched: `/tmp/b7-*`, `b8-*`, `b9-*`, `XX2019*`, `v6bench*`, `gbp2018*`, `absrows-*` (all
BNP-Lean PhaseB: `TRUTH_AUDITOR`, `PhaseB`, `bnp_stage` inside), `govbench_*`, `census_*`, `fb31_strat_*`, `Rtmp*`, `mcp-*`,
`t3-token-*`, `snap_*.lock` (HQ cron locks, live), `par.pdf`/`pe.html`/`pmc.html`/`s2w` (unknown owner, today), `~/Misc`
(mixed: BNP bundles + old SMC `*_work`; owner's folder), `~/data`, `~/envs`, `~/tools`, `~/repo_backups` (BNP bundle),
`~/R` (ribo uses it), BNP/BQTF/Large-Prior/lhv/e03 folders, the v3 deploy folder, `~/.ssh`.

## 2. Move table

| # | source | target | method | why |
|---|---|---|---|---|
| M0 | — | `ROOT/_local/{engineering,theory,writing,papers,tmp}`, `ROOT/_wt/` | `mkdir`; add `/_local/ /_wt/ /scratch` to `$GIT_COMMON_DIR/info/exclude` first | layout; the root clone stays on `main` (no new .gitignore until HQ merges), so the exclude keeps `git status` clean in ROOT and in every worktree at once |
| W1 | 4 worktrees with unpushed commits (§3) | origin | `git push` (new branches only; no force) | never lose a commit |
| W2 | 144 stale worktrees (§3) | — | residue → tar unit (A1), then `git worktree remove` (`--force` only after A1 holds the diff + untracked); nested `t3-002f6236/.rc_tmp/base` before its parent; then `git worktree prune` | stale, all commits on origin |
| W3 | `~/BVS-wt/LEAN` (D2), `~/.t3/…/campaign` | `ROOT/_wt/LEAN`, `ROOT/_wt/campaign` | `git worktree move` | LEAN: HQ snapshot cron still pushes it (last 11-24); campaign: `launch_cloud.sh` REPO |
| W4 | `~/BVS-wt/{THEORY-DEPT,WRITING,P1M}` | `ROOT/_wt/{THEORY-DEPT,WRITING,P1M}` | `git worktree move`, **last**, after HQ's go; P1M last of all | live threads |
| E1 | `~/SMC_Engineering_Department/{INDEX.md,records,crews,staging,scripts,bench,envs,Rlib,logs,7d}` | `ROOT/_local/engineering/` | `mv` per entry (after W2 emptied `staging/` of worktrees) | spec |
| E2 | `~/SMC_Engineering_Department/tmp/*` except `20261118-riboflavin` | A2 unit, then deleted | tar (caches excluded) → `tar -d` check → `rm` | tmp; one tmp area only |
| E3 | `~/SMC_Engineering_Department/README.md` | new | write (4 lines: moved to ROOT/_local/engineering, ribo stays until DONE) | exception 1 |
| E4 | old `crews/offload/serve_pull.sh` path | 3-line shim `exec bash <new>/serve_pull.sh "$@"` | write | D4: the desktop keeps pulling until HQ applies §5 |
| T1 | `~/SMC_Theory_Department/` | `ROOT/_local/theory/` | one `mv` (rename) + symlink back (D3) | spec; 36 open Theory threads |
| T2 | `_local/theory/{tmp,ci,recorder}/*` idle > 24 h, no open handle | A3 unit, then deleted | 22 standalone clones checked: only `tmp/20261116-recorder-CI/dry` (2 refs) and `tmp/20261123-recorder-A12/clone` (1 ref) have commits absent from ROOT's object store → `git bundle create` of those refs; every clone's untracked/ignored non-cache residue + all non-git files → tar; tracked checkouts and `.git` of the other 20 (all commits in ROOT) deleted; `records/`, `refs/`, `BENCH_*`, `SMC_LIT*` kept | tmp; never lose a commit |
| R1 | `~/SMC_Writing_Department/` | `ROOT/_local/writing/` | `mv` + symlink back (D3) | spec |
| P1 | `~/Papers_local/Papers/*` | `ROOT/_local/papers/` | `mv`; `rmdir` the shells; symlink back (D3) | spec |
| L1 | `~/theory_campaign/` | `ROOT/_local/theory/legacy/theory_campaign_202611/` | `mv` | orphaned SMC |
| X1 | `/tmp` SMC items (§1), `~/bvs_tmp/` | A4 unit, then deleted | tar → check → `rm` | wipe |
| X2 | `~/.cache/bvs_*`, `ENG/tmp/uv-cache`, `__pycache__`, `.venv`, `.uv-cache`, `.lake`, `_build`, `build*/`, `.cpp_cache` | — | `rm` | regenerable caches |
| X3 | stale `/tmp/claude-71711` SMC dirs; session subdirs > 48 h in the 4 live-cwd dirs | — | `rm` | exception 6 keeps live ones |

**Archive units** (in `ROOT/_local/engineering/records/reorg_20261125_owls/`, picked up by the hourly desktop pull):
`A1_wt_residue/` (per worktree: `git diff HEAD` patch + tar of untracked/ignored non-cache files: ≈ 0.5 GB), `A2_eng_tmp/`
(≈ 11.2 GB, 61k files → a few tars), `A3_theory_tmp/` (bundles + tars, ≤ 18 GB), `A4_tmp_misc/` (≈ 0.15 GB). Each unit holds
**tars + bundles + SHA256SUMS only**: no loose files, so a `SHA256SUMS` inside the archived data can never be seen as a
nested unit by `serve_pull.sh`. Sources are deleted after `tar -df` (and `git bundle verify`) pass; the unit itself leaves
Owls only once it is in `desktop_verified.txt` (D1).

## 3. Worktrees (149 registered + 1 nested)

Live = has an open (unarchived, unsettled) T3 thread whose `worktreePath` is the worktree (T3 state DB). Only three:
`BVS-wt/P1M` (3 open: ENG v2, REORG Opus-OWLS, Opus-NOTS), `BVS-wt/THEORY-DEPT` (36 open), `BVS-wt/WRITING` (4 open). All
100 `.t3/worktrees` ones have 0 open threads. No process has a cwd in a stale worktree.

Unpushed commits (commits not reachable from any `origin/*` ref): only four worktrees.

| worktree | HEAD | commits | push |
|---|---|---:|---|
| `.t3/…/t3-50893b55-…` | detached `e9f90ce9` (WP2 setup, 11-15; on no local branch) | 4 | `git push origin e9f90ce9:refs/heads/infra/reorg-archive/t3-50893b55` |
| `.t3/…/t3-866f4a87-…` | `exp/P1M-wp3-arch` `5750a903` (WP3 architect review) | 9 | `git push origin exp/P1M-wp3-arch` |
| `BVS-wt/RECORDER2` | detached `f2259f3f` (= local `recorder2/plb-dry-A2`) | 1 | `git push origin recorder2/plb-dry-A2` |
| `BVS-wt/record-1115` | `recorder/staging-1115` `ac5754d3` | 3 | `git push origin recorder/staging-1115` |

All other 145 have 0 unpushed commits (their HEAD is on `origin/main` or another origin branch), so removing them loses no
commit; local branches are kept (`git worktree remove` does not delete branches). Dirty ones (residue goes to A1 first):
`t3-7c9d334a` (19 modified, 1 untracked), `t3-ebd7fab9` (4/2), `BVS-wt/rec-main` (2/0), `ENG/tmp/20261119-m2check/wt_m2`
(1/0), `BVS-wt/POST2-diff` (0/11), `t3-147b528e` (0/2), `t3-5cf0fa2e`, `t3-d52f81e9`, `t3-e4afeca8` (0/1 each).

Full per-worktree table: **Appendix A** (class, push, dirty, ignored residue split cache/keep, method).

## 4. Path references to update (Owls, untracked files)

| file:line | old | new |
|---|---|---|
| `~/.config/bvs-hq/snap/snapshot_ticket.sh:9` | `WT=/home/fb31/BVS-wt/$T` | `WT=/home/fb31/Bayesian-Variable-Selection/_wt/$T; [ -d "$WT" ] \|\| WT=/home/fb31/BVS-wt/$T  # REORG 11-25 fallback; dropped after the live moves` |
| crontab (backup to `snap/crontab.bak-20261125-*` first) | 9 lines `snapshot_ticket.sh {W3-DIST,W3-READER,W3-START2-R,W3-RM2-R,W3-PSHARP-R,W3-MISR-R,PSMC-S0,W3-EDIT,W3-T03ACC}` | prefixed `# REORG 11-25 retired (worktree removed; branch on origin): ` (last pushes 11-16…11-19). P1M, WRITING, THEORY-DEPT, LEAN lines unchanged (the script resolves `_wt/`). owls-guard, BNP, **ribo lines untouched** |
| `~/.config/bvs-hq/launch_cloud.sh:5` | `REPO=/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/campaign` | `REPO=/home/fb31/Bayesian-Variable-Selection/_wt/campaign` |
| `~/.config/bvs-hq/owls/*` (owls_guard.sh, owls_tool.py, env.sh) | no SMC path | no change |
| `_local/engineering/crews/offload/serve_pull.sh:7,9` | `~/SMC_Engineering_Department/crews/offload/serve_pull.sh`; `DEPT=/home/fb31/SMC_Engineering_Department` | `~/Bayesian-Variable-Selection/_local/engineering/crews/offload/serve_pull.sh`; `DEPT=/home/fb31/Bayesian-Variable-Selection/_local/engineering` |
| `_local/engineering/crews/offload/pull_desktop.ps1:57` (Owls copy) | as §5 | as §5 |
| `_local/engineering/crews/rootfs_watch/watch.sh:5` | `OUT=/home/fb31/SMC_Engineering_Department/crews/rootfs_watch` | `OUT=/home/fb31/Bayesian-Variable-Selection/_local/engineering/crews/rootfs_watch` |
| `_local/engineering/crews/home_hygiene/gc_tier1.py:6` | `H = "/home/fb31/SMC_Engineering_Department"` | `H = "/home/fb31/Bayesian-Variable-Selection/_local/engineering"` |
| `_local/engineering/crews/home_hygiene/nots_wave_hygiene_check.py:23` (Owls side) | `H = '/home/fb31/SMC_Engineering_Department'` | `H = '/home/fb31/Bayesian-Variable-Selection/_local/engineering'`; lines 27-28 (NOTS paths) per `REORG_NOTS_PLAN.md` (`/scratch/fb31/SMC-BVS`, `/home/fb31/SMC-BVS/_local/engineering`) |
| `_local/engineering/crews/nots_cleanup_20261124/nots_delete_verified.py:13` | `DEPT = "/home/fb31/SMC_Engineering_Department"` | `DEPT = "/home/fb31/Bayesian-Variable-Selection/_local/engineering"`; line 20 (NOTS fence) per NOTS plan |
| `_local/engineering/crews/home_hygiene/gc_fence.py:8`, `test_gc_fence.py:6,20`, `nots_home_prune.sh` | NOTS-side paths | per NOTS plan (Opus-NOTS); no Owls change |
| `_local/engineering/INDEX.md:1,5,18` | `SMC_Engineering_Department (Owls)`; `/home/fb31/BVS-wt/`; `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/<job>` | `ROOT/_local/engineering (Owls; was ~/SMC_Engineering_Department)`; `ROOT/_wt/`; `TMPDIR=/home/fb31/Bayesian-Variable-Selection/_local/tmp/<job>` + a dated "REORG 11-25" line |
| `_local/theory/INDEX.md:4,8,9,27` | `/home/fb31/BVS-wt/`, `…/SMC_Theory_Department/tmp/…`, `…/ci` | `ROOT/_wt/`, `ROOT/_local/tmp/<…>`, `ROOT/_local/theory/ci` + a dated line (Theory's file: paths only) |
| `_local/engineering/scripts/*/{build,submit*}.sh`, `scripts/*/manifests/*.json`, `bench/*/build_info.txt`, `crews/nots_cleanup_20261124/usage_*.txt`, `_local/theory/ci/bvs-ci-sandboxes/**` | NOTS paths / historical evidence (hashed) | **not edited** (records) |
| `/home/fb31/.claude/projects/-home-fb31-BVS-wt-*` | Claude CLI project keys derive from the cwd | not edited; after W4 the new cwds get new keys: HQ re-points the threads (memory under `-home-fb31-Bayesian-Variable-Selection/` is unaffected) |
| ribo: `rb_relaunch.sh`, `rb_unit.sh` (ROOT untracked `Docs/Experiments/realdata_riboflavin/`), units, @reboot | — | **untouched** (exception 1; ribo uses `~/R`, not ENG `Rlib/`) |

Tracked repo files (D5): `git grep` finds old paths in 666 files / 2,119 lines on `main` (431 / 1,940 on `exp/P1M`; most are
NOTS paths, frozen evidence, BRIEFs, `POLICIES.md` §4/§12, `Docs/Experiments/P1M/offload/{serve_pull.sh,pull_desktop.ps1,INSTALL.md}`,
`Scripts/SMC_BVS/engine_v4/tools/{nots_guard.sh,slurm/p1m_driver.py,…}`). Spec: the only tracked change is `.gitignore` +
`LAYOUT.md`, so none is edited here; LAYOUT.md carries the old → new map. Follow-up per department (their branches).

## 5. Desktop `pull_desktop.ps1` change (HQ applies on the desktop)

File: `D:\SMC_Engineering_Department\scripts\pull_desktop.ps1`, line 57.

old:
```
  $remote = "bash /home/fb31/SMC_Engineering_Department/crews/offload/serve_pull.sh $Client $MaxPullGB"
```
new:
```
  $remote = "bash /home/fb31/Bayesian-Variable-Selection/_local/engineering/crews/offload/serve_pull.sh $Client $MaxPullGB"
```
Nothing else changes: `DestRoot` (`D:\SMC_Engineering_Department`), `verified_units.txt`, the ssh alias. Unit names are
relative to `records/`, which moves as one directory, so the desktop's verified list matches 715/715 and nothing is re-sent.
Until HQ applies it, the old path is a shim (E4) that execs the new script: the :20 pulls keep working either way.
Test (Phase 1, after E1): `cat desktop_verified.txt | bash <new>/serve_pull.sh reorgtest 1 | tar -tvf - | wc -l` and the
same through the shim → only the new `reorg_20261125_owls/*` units pending (or none before they exist); then remove
`reorgtest_verified.txt` and its serve.log lines are labelled. `desktop_verified.txt` is never edited by hand.

## 6. `.gitignore` diff and LAYOUT.md draft

```diff
--- a/.gitignore
+++ b/.gitignore
@@ (end of file)
+
+# --- REORG 2026-11-25 (LAYOUT.md): machine-local trees under ROOT; never in git ---
+/_local/
+/_wt/
+/scratch
```

LAYOUT.md (ROOT; committed on Owls; NOTS gets a verbatim copy):
````markdown
# SMC-BVS layout (REORG 2026-11-25, owner greenlight via HQ)

One ROOT per machine, same names below it. A path relative to ROOT means the same thing on both machines.
- Owls ROOT: `/home/fb31/Bayesian-Variable-Selection` (the shared root clone; stays on `main`)
- NOTS ROOT: `/home/fb31/SMC-BVS`

```
ROOT/
  LAYOUT.md          this file (committed on Owls; a verbatim copy on NOTS)
  _local/            gitignored. Never in git.
    engineering/     was ~/SMC_Engineering_Department (INDEX.md, records/, crews/, staging/, scripts/, bench/, envs/, Rlib/, logs/)
    theory/          was ~/SMC_Theory_Department
    writing/         was ~/SMC_Writing_Department
    papers/          was ~/Papers_local (PDFs; copyrighted, never in git)
    tmp/             the ONLY tmp/cache area (TMPDIR=ROOT/_local/tmp/<YYYYMMDD>-<owner>-<what>); empty when idle
  _wt/<name>/        Owls: git worktrees (`git worktree add/move` only, never mv). NOTS: code clones and builds
  scratch            NOTS only: symlink to /scratch/fb31/SMC-BVS/{runs,archive,_wt}
```

## Old → new paths
| old | new |
|---|---|
| `~/SMC_Engineering_Department/…` | `ROOT/_local/engineering/…` |
| `~/SMC_Theory_Department/…` | `ROOT/_local/theory/…` |
| `~/SMC_Writing_Department/…` | `ROOT/_local/writing/…` |
| `~/Papers_local/Papers/…` | `ROOT/_local/papers/…` |
| `~/BVS-wt/<name>` (Owls) | `ROOT/_wt/<name>` |
| `/scratch/fb31/SMC_{Engineering,Theory}_Department/…` (NOTS) | `ROOT/scratch/…` = `/scratch/fb31/SMC-BVS/…` |
| `/tmp/…`, `~/bvs_tmp/…`, `<dept>/tmp/…` | `ROOT/_local/tmp/…` |

## Rules
- Nothing SMC outside ROOT except the exceptions below. New worktrees: `git worktree add ROOT/_wt/<name>`.
- Never `git clean -x` / `-ff` in ROOT (it would reach `_local/` and the nested `_wt/` worktrees). Tools that honour
  .gitignore (rg, fd) skip `_local/`; plain `grep -r`/`find` from ROOT walk ~0.5 TB of records: scope them.
- Data, records, PDFs, logs and secrets never enter git; `git status` must be clean of them before any commit.

## Exceptions (stay where they are)
1. Riboflavin: Owls `~/SMC_Engineering_Department/tmp/20261118-riboflavin/`, units ribo-s1..5, its @reboot crontab line, and
   its scripts in ROOT `Docs/Experiments/realdata_riboflavin/` (untracked), until DONE (≈ 11-27 02:46 CST). That folder plus a
   README.md is all that remains of ~/SMC_Engineering_Department.
2. The SMC_BVS_v3 deploy folders (Owls `/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`, the NOTS one
   under `~/projects/`) and `/projects/ml75`: never touched (POLICIES §4).
3. T3-managed worktrees of live threads under `~/.t3/worktrees/` (T3 creates them there; stale ones are removed).
4. HQ infrastructure `~/.config/bvs-hq/` (snapshot cron, owls guard, tokens): references updated, folder not moved.
5. `~/.ssh` and credentials: never touched.
6. Live Claude session scratchpads in `/tmp/claude-<uid>/` of live threads; HQ snapshot locks `/tmp/snap_*.lock`.
7. (transitional, until <date set by HQ>) symlinks `~/SMC_Theory_Department`, `~/SMC_Writing_Department`, `~/Papers_local`
   → `ROOT/_local/…`, and the offload shim at the old `serve_pull.sh` path, so running threads and the desktop pull keep
   working while HQ re-briefs.
````

## 7. Exceptions (Owls specifics)
1. Ribo: `~/SMC_Engineering_Department/tmp/20261118-riboflavin/` (0.04 GB), `ribo-s1..5`, its @reboot line, **and** ROOT's
   untracked `Docs/Experiments/realdata_riboflavin/scripts/` (`rb_unit.sh` runs from there): untouched.
2. v3 deploy folder: untouched (not read).
3. T3 dir `~/.t3/worktrees/Bayesian-Variable-Selection/` stays (T3 creates new thread worktrees there); after W2 it holds
   no stale SMC worktree. (`t3-469a6ca4…` is referenced by one archived thread but no longer exists: nothing to do.)
4. `~/.config/bvs-hq/`: lines in §4 only. `/tmp/snap_*.lock`: HQ's, kept.
5. `~/.ssh`, `gh_token`, `api/anthropic_key`: never opened.
6. `/tmp/claude-71711/{-home-fb31-BVS-wt-P1M,-THEORY-DEPT,-WRITING,-home-fb31-Bayesian-Variable-Selection}`: only session
   subdirs older than 48 h go.
7. Transitional (D3/D4): the three symlinks and the shim; removed when HQ says the departments are re-briefed.
8. ROOT's own dirty state (`M Theory_work/Wave3/W3-DIST/LOG.md`, untracked `Docs/Experiments/{LOG.md,realdata_riboflavin/}`,
   ignored `W3-DIST/work/…` numerics): the root clone's tracked tree is HQ's; untouched.

## 8. Bytes

| action | bytes | items |
|---|---:|---|
| **move** (rename, same FS) | ≈ 500 GB | ENG ≈ 418.6 GB (records 413.73, staging 4.03 − wts, envs/Rlib/crews/…), Theory ≈ 63 GB after T2 (records/ci/refs/BENCH…), Writing 1.4 MB, Papers 63 MB, theory_campaign 21 MB, 5 worktrees ≈ 1.6 GB (P1M, THEORY-DEPT, WRITING, LEAN, campaign) |
| **copy, then delete source** (tar/bundle into reorg units, `tar -d` / `git bundle verify`; the unit later goes to the desktop) | ≈ 30 GB | A2 ENG tmp 11.2 GB, A3 Theory tmp/ci/recorder ≤ 18 GB, A1 worktree residue ≈ 0.5 GB, A4 /tmp + bvs_tmp 0.15 GB |
| **delete** (regenerable; every commit on origin) | ≈ 48 GB | 144 stale worktree checkouts ≈ 44 GB (100 T3 + 1 nested ≈ 31, 20 ENG nested ≈ 6.5, 24 BVS-wt ≈ 7.3; caches included), caches ≈ 8 GB (`.rc_tmp/base`+`build_*`, `.venv`, `.uv-cache`, ENG `uv-cache` 0.29), `/tmp/claude-71711` stale ≈ 0.01 GB, `~/.cache/bvs_*` 3.5 KB |
| **push** | 17 commits | 4 refs (§3) |
| frees on `/` (local /tmp) | ≈ 0.16 GB | `/tmp` is 92 % full mostly from non-SMC items |

## Decisions for the manager / HQ
- **D1 records.** Default: `records/` (413.73 GB, 715 desktop-verified units) moves and stays on Owls (POLICIES §12.12:
  Owls copy until the laptop mirror). Only the new `reorg_20261125_owls/*` units are deleted from Owls after they appear in
  `desktop_verified.txt`. Option: also delete desktop-verified record units (frees ≈ 400 GB) — owner/HQ call.
- **D2 LEAN.** Default: `git worktree move` to `_wt/LEAN` (HQ cron still snapshots `ROOT/Lean` into it; pushed 11-24). Option: remove + retire its cron line.
- **D3 transitional symlinks** for Theory, Writing, Papers (36 + 4 open threads write those paths). Default yes, ≤ 48 h.
- **D4 offload shim** at the old `serve_pull.sh` path until HQ confirms §5. Default yes.
- **D5 tracked references** stay (spec); LAYOUT.md carries the map; per-department follow-up.
- **D6 Theory tmp/ci/recorder (T2).** Default: archive + delete entries idle > 24 h with no open handle; the Theory
  manager may veto a path before Phase 1 step T2. `records/` never touched.

## Phase 1 order (after GO)
1. M0 (dirs, `info/exclude`) → W1 pushes → A1 residue + W2 removals (T3, BVS-wt stale, ENG nested; `git worktree prune`) → W3.
2. Crontab: retire the 9 lines; `snapshot_ticket.sh` fallback; `launch_cloud.sh`.
3. E2 archive ENG tmp → E1 moves → E3 README → E4 shim → §4 edits → §5 offload test (new path + shim).
4. T1/R1/P1/L1 moves + symlinks → T2 → X1–X3 wipe. One LOG line per deletion batch with sizes.
5. `.gitignore` + `LAYOUT.md` commit on `exp/P1M` (`git status` checked first; no push to main).
6. Live worktrees W4, only after HQ's go relayed by the manager: THEORY-DEPT, WRITING, then P1M last; drop the
   `snapshot_ticket.sh` fallback; LOG path becomes `ROOT/_wt/P1M/Docs/Experiments/P1M/LOG.md`.

## Appendix A. Per-worktree table

Residue "cache" = `.rc_tmp/`, `.venv/`, `.uv-cache/`, `__pycache__/`, `.lake/`, `_build/`, `build*/` (deleted with the
worktree, except `.rc_tmp/` review notes and probe outputs, which go to A1 minus `base/` and `build_*`); "keep" = other ignored
files (A1). Untracked files always go to A1.

| # | worktree | branch / HEAD | class | unpushed → action | dirty (mod/untracked) | ignored residue (cache / keep) | method |
|---|---|---|---|---|---|---|---|
| 1 | `T3/campaign` | theory/campaign 401a6139 | keep (launch_cloud.sh) | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree move` → `_wt/campaign` |
| 2 | `T3/t3-002f6236-97230bd4ef26b98a` | DETACHED 32f862c0 | stale | none (all commits on origin) | 0/0 | 1513 MB / 0.0 MB | `git worktree remove` |
| 3 | `T3/t3-002f6236-97230bd4ef26b98a/.rc_tmp/base` | DETACHED 423decb5 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 4 | `T3/t3-01ef7ca9-a854d6229f7e70df` | DETACHED f44ff58d | stale | none (all commits on origin) | 0/0 | 35 MB / 0.0 MB | `git worktree remove` |
| 5 | `T3/t3-0370c317-ad7a84d5fc1df177` | t3/review-pr20-recheck 38604282 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 6 | `T3/t3-091fee5d-d7c2651b2f620736` | DETACHED fe8fda63 | stale | none (all commits on origin) | 0/0 | 180 MB / 0.0 MB | `git worktree remove` |
| 7 | `T3/t3-096e5f63-6dd6de921222f974` | DETACHED 9fa534e7 | stale | none (all commits on origin) | 0/0 | 335 MB / 0.0 MB | `git worktree remove` |
| 8 | `T3/t3-0c7ed901-44e74864cdb473d5` | theory/sweep-2026-11 2ebd0408 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.1 MB | tar keep-residue; `git worktree remove` |
| 9 | `T3/t3-0e18a33f` | theory/LH-LOCK 581e4bae | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 10 | `T3/t3-10da0fc9-539d3be99572e6ca` | DETACHED db58db70 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 11 | `T3/t3-147b528e` | theory/O-SWAP 5adb21a5 | stale | none (all commits on origin) | 0/2 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 12 | `T3/t3-15826e2d-7786c9ceeefff80d` | DETACHED c1a8016e | stale | none (all commits on origin) | 0/0 | 19 MB / 0.0 MB | `git worktree remove` |
| 13 | `T3/t3-17191395-9ae309c93cc86d45` | theory/PRE-LEAN-walkD b5a87cd2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 14 | `T3/t3-1751a409-921890b85bc746db` | DETACHED 9c3d56e5 | stale | none (all commits on origin) | 0/0 | 869 MB / 0.0 MB | `git worktree remove` |
| 15 | `T3/t3-1a473017-673ec19297812798` | DETACHED bf7daa23 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 16 | `T3/t3-1da14bf6-e16df64bedbcf902` | DETACHED ecabdcfc | stale | none (all commits on origin) | 0/0 | 66 MB / 0.0 MB | `git worktree remove` |
| 17 | `T3/t3-2138bde7` | theory/S-REGISTRY 1540bb3e | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 18 | `T3/t3-215eb534-a080473e9c42fff9` | theory/PRE-LEAN ed9ff033 | stale | none (all commits on origin) | 0/0 | 1005 MB / 0.0 MB | `git worktree remove` |
| 19 | `T3/t3-2b8bab6d-e8bfd7a12835c878` | DETACHED e7afdd11 | stale | none (all commits on origin) | 0/0 | 259 MB / 0.0 MB | `git worktree remove` |
| 20 | `T3/t3-2c070586` | theory/O-LS0 d9b3d318 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 21 | `T3/t3-2c50ca8d` | theory/A-DRAFT dbf47f7a | stale | none (all commits on origin) | 0/0 | 0 MB / 288.9 MB | tar keep-residue; `git worktree remove` |
| 22 | `T3/t3-32a0187b-3d8f682b1c689dcf` | DETACHED 89366d4a | stale | none (all commits on origin) | 0/0 | 338 MB / 0.0 MB | `git worktree remove` |
| 23 | `T3/t3-32c38f4e-ada324935577a280` | t3/review-pr19-recheck b69476ea | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 24 | `T3/t3-33a0d4b7-87b90d3e85e5421e` | DETACHED b5afcc61 | stale | none (all commits on origin) | 0/0 | 330 MB / 0.0 MB | `git worktree remove` |
| 25 | `T3/t3-3411b82b-fa3fdf4171c61017` | DETACHED e3ca4716 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 26 | `T3/t3-36dd9684-a815257d2f776d9b` | theory/PRE-LEAN-walkB dc2e7174 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 27 | `T3/t3-3a94a30e-ff68ec68111df2b8` | t3/review-pr24-pr26 38604282 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 28 | `T3/t3-3b32d183` | theory/A-REV1 26815e84 | stale | none (all commits on origin) | 0/0 | 90 MB / 0.0 MB | `git worktree remove` |
| 29 | `T3/t3-3d20ff7b-00c2d8ced2e83172` | DETACHED 9344737d | stale | none (all commits on origin) | 0/0 | 676 MB / 0.0 MB | `git worktree remove` |
| 30 | `T3/t3-4173f9f8` | theory/S-PAPER 556be301 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | tar keep-residue; `git worktree remove` |
| 31 | `T3/t3-495186b5-dcbbe30304fdb02b` | DETACHED f6567dc0 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 32 | `T3/t3-4a82c812-fd473931a489c73e` | exp/P1M-wp1-store-perf ea06916c | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 33 | `T3/t3-4b8f8d6e-7f80be394c7c6a05` | DETACHED 099e8ac6 | stale | none (all commits on origin) | 0/0 | 678 MB / 0.0 MB | `git worktree remove` |
| 34 | `T3/t3-5023b19b-781c9af46f34d273` | DETACHED 75cef83c | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 35 | `T3/t3-50893b55-414751f1bc1cce3a` | DETACHED e9f90ce9 | stale | push e9f90ce9 → infra/reorg-archive/t3-50893b55 (4 commits, WP2 setup) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 36 | `T3/t3-56594e23-e1d0fc7129e5cbc3` | DETACHED 89c75320 | stale | none (all commits on origin) | 0/0 | 36 MB / 0.0 MB | `git worktree remove` |
| 37 | `T3/t3-5676de1e-ec729dd2fe01f5ca` | t3/review-pr47-island-store-validation a7fc5093 | stale | none (all commits on origin) | 0/0 | 63 MB / 0.0 MB | `git worktree remove` |
| 38 | `T3/t3-58e249fb` | DETACHED c20059db | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 39 | `T3/t3-597aa222-a2c223e7fb3a9c2d` | theory/PRE-LEAN-walkC 4cdb915e | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 40 | `T3/t3-5b84b7ab` | theory/F-SHARE e05b832b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 41 | `T3/t3-5cf0fa2e-bfa44467eae425ed` | t3/review-pr21-island-kernel b69476ea | stale | none (all commits on origin) | 0/1 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 42 | `T3/t3-5d6fdad5-5fa0d5cabeb4d2f9` | t3/review-pr21-pr24-smc b69476ea | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 43 | `T3/t3-5f895410-4443f4165a1281e4` | DETACHED 85530b12 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 44 | `T3/t3-63861fea-aab6123260635e0d` | eng/xeval dc0474eb | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 45 | `T3/t3-6650c0f6-4f3b6d12e45d22f8` | DETACHED a7d76e58 | stale | none (all commits on origin) | 0/0 | 75 MB / 0.0 MB | `git worktree remove` |
| 46 | `T3/t3-6af24577-68ce94317be1bef4` | exp/P1M-wp6-k6 44055be8 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 47 | `T3/t3-6c5b8683-95a83838f856e027` | theory/PRE-LEAN-walkA a919948a | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 48 | `T3/t3-6dd7854b-f72d15fd10150e5a` | exp/P1M-list-pip fff3453f | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 49 | `T3/t3-6fcd9794-da1e086bbeb489d7` | t3/review-pr26-recheck 38604282 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 50 | `T3/t3-76b20e33` | t3/refine-theory-confidence-cards-1 db708ca9 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 51 | `T3/t3-78f96d69-2f0effb599191e18` | DETACHED 9344737d | stale | none (all commits on origin) | 0/0 | 96 MB / 0.0 MB | `git worktree remove` |
| 52 | `T3/t3-7c9d334a-bdd389eba13a7741` | DETACHED 12931094 | stale | none (all commits on origin) | 19/1 | 254 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 53 | `T3/t3-7de86665-e07bdeb625b66ae6` | t3/pr40-store-dedupe-review d2b600ba | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 54 | `T3/t3-7e1aad3a-37ce904b15d20298` | DETACHED 33fd9dd9 | stale | none (all commits on origin) | 0/0 | 51 MB / 0.0 MB | `git worktree remove` |
| 55 | `T3/t3-8214bd63-1f63efd85cf914ad` | DETACHED 1d79974e | stale | none (all commits on origin) | 0/0 | 271 MB / 0.0 MB | `git worktree remove` |
| 56 | `T3/t3-82162602` | theory/MEET-THM-REG b1600857 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 57 | `T3/t3-82988d67` | theory/F-DRAFT 4de6e4c7 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | tar keep-residue; `git worktree remove` |
| 58 | `T3/t3-85c766ee-cf9abaf943992d2b` | DETACHED f00a3c78 | stale | none (all commits on origin) | 0/0 | 88 MB / 0.0 MB | `git worktree remove` |
| 59 | `T3/t3-863eeb22-98b148d98256ea8d` | exp/P1M-wp5-competitors 50649897 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 60 | `T3/t3-8660d5af` | theory/O-CERT ff42c703 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 61 | `T3/t3-866f4a87-fad2d8cf623cf330` | exp/P1M-wp3-arch 5750a903 | stale | push exp/P1M-wp3-arch (9 commits) | 0/0 | 0 MB / 0.1 MB | tar keep-residue; `git worktree remove` |
| 62 | `T3/t3-869c2a55-3f292ab6d75e3c9d` | exp/P1M-wp7-info-meta b7e9028d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 63 | `T3/t3-88018eff-7a7e040d1bfb1a49` | exp/P1M-freeze 06122a96 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 64 | `T3/t3-8fb74020-0759c2fe806d60d4` | t3/review-pr16-merge-tail b69476ea | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 65 | `T3/t3-95809045` | o-ls0-wrap 02348e28 | stale | none (all commits on origin) | 0/0 | 0 MB / 2.3 MB | tar keep-residue; `git worktree remove` |
| 66 | `T3/t3-95bf60de-6725a572cfc55dc8` | exp/P1M-wp5-guard2 2b4d741e | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 67 | `T3/t3-98786ad6-94151b2187883372` | exp/P1M-core-v3.1.1 b6ff7058 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 68 | `T3/t3-991ebdff-1fd60b73563f9583` | t3/review-wp3-stacked-prs d2b600ba | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 69 | `T3/t3-9a57de5a-f0a30490a6bc2f4a` | DETACHED 4b84e585 | stale | none (all commits on origin) | 0/0 | 3 MB / 0.0 MB | `git worktree remove` |
| 70 | `T3/t3-9b2df505-c8c851377fe40229` | exp/P1M-wp3-startview ecabdcfc | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 71 | `T3/t3-a66a6195-1525c05cd04d97af` | theory/prelean-blind b6950652 | stale | none (all commits on origin) | 0/0 | 1 MB / 1.6 MB | tar keep-residue; `git worktree remove` |
| 72 | `T3/t3-a9f56b63-eacaea0aa5421cc0` | theory/W3-READER-ED 84ce4f08 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.4 MB | tar keep-residue; `git worktree remove` |
| 73 | `T3/t3-b2362d00` | theory/F-REFINE e05b832b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 74 | `T3/t3-b274580e-9e18dde5b0be9256` | DETACHED 5f2b4777 | stale | none (all commits on origin) | 0/0 | 93 MB / 0.0 MB | `git worktree remove` |
| 75 | `T3/t3-b8c44b19` | t3/b8c44b19 e05b832b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 76 | `T3/t3-ba918c58-7eb408df9d89e5c9` | DETACHED fe86e6df | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 77 | `T3/t3-bbbf99c1-eb6944baac481075` | exp/P1M-wp2-setup 6bea3d86 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 78 | `T3/t3-c3e3cc0e` | theory/ABL-CONF c0730fe9 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 79 | `T3/t3-c4af14f4` | t3/review-smc-bvs-proofs 00c7b340 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 80 | `T3/t3-cb149a9d` | theory/A-REV2 09dc2307 | stale | none (all commits on origin) | 0/0 | 345 MB / 10.2 MB | tar keep-residue; `git worktree remove` |
| 81 | `T3/t3-ce42a416` | theory/T38-RECORD c785bc02 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 82 | `T3/t3-d3b0edd3-6d57d84494497161` | DETACHED 45fcd32d | stale | none (all commits on origin) | 0/0 | 36 MB / 0.0 MB | `git worktree remove` |
| 83 | `T3/t3-d3fadba7-ec4a2133fdcc2bcf` | theory/W3-FAMC 24a9ee25 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 84 | `T3/t3-d52f81e9` | theory/O-BGIBBS 432fb125 | stale | none (all commits on origin) | 0/1 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 85 | `T3/t3-d564bfee-1f02cc5f2c9bd325` | t3/review-pr37-calibration 85cf8c4b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 86 | `T3/t3-d5a7a1ad` | t3/masked-delivery-theorem-1 56b401f1 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 87 | `T3/t3-d64c1567-903814251f8eb18d` | exp/P1M-VN 09fc8fa2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 88 | `T3/t3-d897ca46-913181e54646d6ba` | DETACHED a72a7777 | stale | none (all commits on origin) | 0/0 | 39 MB / 0.0 MB | `git worktree remove` |
| 89 | `T3/t3-de01d90c` | o-ls0 24717090 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 90 | `T3/t3-e1ff52ea-fbdf745449b4936e` | t3/review-wp4-calibration-pipeline d2b600ba | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 91 | `T3/t3-e4afeca8-0704067c93008e7f` | t3/review-misr-statement-change 79355e9d | stale | none (all commits on origin) | 0/1 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 92 | `T3/t3-e6b1c192-b631bd96da0879b1` | t3/review-list-renormalized-pip d063cc3e | stale | none (all commits on origin) | 0/0 | 113 MB / 0.0 MB | `git worktree remove` |
| 93 | `T3/t3-e77ec337-a781f908c5e51fbc` | t3/review-wp5-prs b69476ea | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 94 | `T3/t3-ebcba51c` | theory/F-PXN e05b832b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 95 | `T3/t3-ebd7fab9` | theory/O-WSTAB e309e149 | stale | none (all commits on origin) | 4/2 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 96 | `T3/t3-f0b86bba-a61fe313022e5440` | DETACHED 04302f89 | stale | none (all commits on origin) | 0/0 | 340 MB / 0.0 MB | `git worktree remove` |
| 97 | `T3/t3-f88c0e0b` | theory/E-SPINE cec16803 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 98 | `T3/t3-f8ad9ba2-fdea03dfd2a50ccc` | DETACHED 769fe59b | stale | none (all commits on origin) | 0/0 | 31 MB / 0.0 MB | `git worktree remove` |
| 99 | `T3/t3-fe4730e2-97d720eff3279fbd` | exp/P1M-driver-law-N 9a25842a | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 100 | `T3/theory-MEET-THM` | theory/MEET-THM 37b4d2bd | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 101 | `T3/theory-MEET-v31` | theory/MEET-v31 e82e097e | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 102 | `WT/LEAN` | lean/BVSCert 39a758c0 | keep (D2) | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree move` → `_wt/LEAN` |
| 103 | `WT/P1M` | exp/P1M 79cb2c74 | LIVE | none (all commits on origin) | 0/1 | 0 MB / 0.2 MB | `git worktree move` → `_wt/P1M` (LAST, HQ go) |
| 104 | `WT/POST2-diff` | theory/W3-POST2-diff 3333e0c4 | stale | none (all commits on origin) | 0/11 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 105 | `WT/PSMC-S0` | theory/PSMC-S0 69871dfe | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 106 | `WT/RECORDER` | DETACHED 51705bc0 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 107 | `WT/RECORDER2` | DETACHED f2259f3f | stale | push recorder2/plb-dry-A2 (f2259f3f, 1 commit) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 108 | `WT/THEORY-DEPT` | dept/theory 2d5fa3ca | LIVE | none (all commits on origin) | 0/0 | 10 MB / 0.0 MB | `git worktree move` → `_wt/THEORY-DEPT` (LAST, HQ go) |
| 109 | `WT/W3-AUDIT` | theory/W3-AUDIT 0211dca4 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 110 | `WT/W3-D2` | theory/W3-D2 6d5dbe96 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 111 | `WT/W3-D3` | theory/W3-D3 f07c4cf5 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 112 | `WT/W3-D5P` | theory/W3-D5P 6166e7f5 | stale | none (all commits on origin) | 0/0 | 6 MB / 0.0 MB | `git worktree remove` |
| 113 | `WT/W3-DIST` | theory/W3-DIST a6fbe7ef | stale | none (all commits on origin) | 0/0 | 0 MB / 69.5 MB | tar keep-residue; `git worktree remove` |
| 114 | `WT/W3-EDIT` | theory/W3-EDIT a5e7fe92 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 115 | `WT/W3-MISR-R` | theory/W3-MISR-R 174f65b4 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 116 | `WT/W3-PSHARP-R` | theory/W3-PSHARP-R 8e22c756 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 117 | `WT/W3-READER` | theory/W3-READER 0b5da012 | stale | none (all commits on origin) | 0/0 | 0 MB / 2.3 MB | tar keep-residue; `git worktree remove` |
| 118 | `WT/W3-RM2-R` | theory/W3-RM2-R e78a1055 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.4 MB | tar keep-residue; `git worktree remove` |
| 119 | `WT/W3-SCR-R2` | theory/W3-SCR-R2 048b6b23 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 120 | `WT/W3-START2-R` | theory/W3-START2-R ec37ab2e | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 121 | `WT/W3-T03ACC` | theory/W3-T03ACC 940e4199 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 122 | `WT/WRITING` | writing/main f772bf6c | LIVE | none (all commits on origin) | 0/0 | 35 MB / 4.0 MB | `git worktree move` → `_wt/WRITING` (LAST, HQ go) |
| 123 | `WT/actions-ci` | infra/actions-ci 84eec64d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 124 | `WT/ci-cite-cwd` | infra/ci-cite-cwd d2855068 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.1 MB | tar keep-residue; `git worktree remove` |
| 125 | `WT/citefix` | infra/accept-identity-case-nb 5cc7786b | stale | none (all commits on origin) | 0/0 | 0 MB / 0.3 MB | tar keep-residue; `git worktree remove` |
| 126 | `WT/eng-offload` | infra/P1M-offload 88e39125 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 127 | `WT/manifest-verify-ci` | theory/manifest-verify-ci ec452bbb | stale | none (all commits on origin) | 0/0 | 845 MB / 0.0 MB | `git worktree remove` |
| 128 | `WT/rec-main` | rec/q2-manifest 029bb748 | stale | none (all commits on origin) | 2/0 | 0 MB / 0.5 MB | save diff+untracked → tar unit; tar keep-residue; `git worktree remove --force` |
| 129 | `WT/record-1115` | recorder/staging-1115 ac5754d3 | stale | push recorder/staging-1115 (3 commits) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 130 | `ENG/staging/overlap1e4/wt_21f6e2b5` | DETACHED 21f6e2b5 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 131 | `ENG/staging/overlap1e4/wt_eefcbc4a` | DETACHED eefcbc4a | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 132 | `ENG/staging/overlap1e4/wt_ffa00d9c` | DETACHED ffa00d9c | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 133 | `ENG/staging/vn_minileg/wt_e993ece2` | DETACHED e993ece2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 134 | `ENG/tmp/20261115-wp3/wt-split` | exp/P1M-wp3-m3fix 8d584649 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 135 | `ENG/tmp/20261116-wp7-o1/wt_errors` | exp/P1M-polish-errors 3c7e308f | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 136 | `ENG/tmp/20261116-wp7-o1/wt_freeze` | exp/P1M-wp7-driver-merge128 3c20a0a2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 137 | `ENG/tmp/20261116-wp7-o1/wt_o2` | exp/P1M-wp7-o5 e57fbbc2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 138 | `ENG/tmp/20261116-wp7-o1/wt_o4b` | exp/P1M-wp7-o3-leaders f823593c | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 139 | `ENG/tmp/20261116-wp7-o1/wt_polish` | exp/P1M-polish 2b6dac51 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 140 | `ENG/tmp/20261116-wp7-o1/wt_req` | exp/P1M-driver-required cf670fdd | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 141 | `ENG/tmp/20261116-wp7-o1/wt_test` | exp/P1M-polish-p6 8955f63d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 142 | `ENG/tmp/20261116-wp7-o1/wt_val` | exp/P1M-driver-validate a06bbac2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 143 | `ENG/tmp/20261119-m2check/wt_base` | DETACHED b89cba4d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 144 | `ENG/tmp/20261119-m2check/wt_head` | DETACHED 09fc8fa2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 145 | `ENG/tmp/20261119-m2check/wt_m2` | DETACHED b89cba4d | stale | none (all commits on origin) | 1/0 | 0 MB / 0.0 MB | save diff+untracked → tar unit; `git worktree remove --force` |
| 146 | `ENG/tmp/20261119-opusreview/wt` | DETACHED b89cba4d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 147 | `ENG/tmp/20261119-precplan/wt_b89cba4d` | DETACHED b89cba4d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 148 | `ENG/tmp/20261119-vnplan/wt_F2` | DETACHED e993ece2 | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
| 149 | `ENG/tmp/20261119-w2/wt_b89cba4d` | DETACHED b89cba4d | stale | none (all commits on origin) | 0/0 | 0 MB / 0.0 MB | `git worktree remove` |
