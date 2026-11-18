# REORG_PLAN — SMC-BVS material into the department roots (machines crew, leg 1)

> **Scope rule (owner via HQ, 2026-11-15):** Engineering works only inside `SMC_Engineering_Department` on each machine
> (plus its NOTS scratch link). Everything else in `/home/fb31` on Owls or NOTS is **out of scope**: not inventoried,
> moved, cleaned or touched. The only exceptions are the HQ-approved SMC-BVS moves and the home guard. Out-of-scope rows
> below are withdrawn.


SMC - Engineering, Opus 5.5 helper, 2026-11-15. **Plan only: nothing here has been executed.** Every step needs HQ's go
(and, where marked, Theory's or the owner's OK) and runs in a quiet window, one command at a time, under the
"be chill" rule (sequential ssh, `nice`, no loops). Inventory: `INVENTORY.md`. Daily crew: `CREW.md`.

## 0. Roots (fixed by the owner, POLICIES §12 rules 8–9)

```
ENG_ROOT_NOTS    = /home/fb31/SMC_Engineering_Department          # home: light files only (10 GB quota, guard 8 GB)
ENG_SCRATCH_NOTS = /scratch/fb31/SMC_Engineering_Department       # = ${ENG_ROOT_NOTS}/scratch (symlink, exists)
ENG_ROOT_OWLS    = /home/fb31/SMC_Engineering_Department          # Owls NFS home
```
Every move below is written `source → ${ENG_…}/subpath`. Paths under `${ENG_ROOT_NOTS}/scratch/…` and
`${ENG_SCRATCH_NOTS}/…` are the same place; moves of heavy data always name `${ENG_SCRATCH_NOTS}` so nobody copies into home by
mistake.

Both layouts were asked for. The owner has fixed **layout A**; layout B is kept as the fallback if home ever has to hold
nothing.
- **A (adopted): root in home with a `scratch` symlink.** Light: `INDEX.md`, `scripts/`, `results/` (< 50 MB in total),
  `crews/`. Heavy: everything under `scratch/`. Home gain from the reorg ≈ 0 (nothing heavy goes to home).
- **B (fallback): root wholly in scratch.** `ENG_ROOT_NOTS = ${ENG_SCRATCH_NOTS}`; `scripts/`, `results/`, `crews/` and
  `INDEX.md` move under `/scratch/fb31/SMC_Engineering_Department/`, and `~/SMC_Engineering_Department` becomes a single
  symlink. Cost: results of record live under the scratch purge policy. Every move in §3 is unchanged in B (they all
  target `${ENG_SCRATCH_NOTS}`).

**Purge risk (applies to both):** `/scratch` is subject to a purge policy whose terms are unknown (NOTS_STORAGE.md §1).
`archive/` in scratch is a holding place, not a safe archive. Anything of record must also exist in the repo (small) or on
the laptop (heavy, by the `staging/` transfer route once HQ sets it).

## 1. Target tree (extends the existing INDEX layout)

```
${ENG_ROOT_NOTS}/                      (home, light)
├── INDEX.md                            what lives where + provenance + old-path table (draft in §6)
├── scripts/<ticket>/                   job scripts, sbatch files, env files (versioned copies; hash in each run manifest)
├── results/<ticket>/                   small results of record (< 50 MB in total)
├── crews/                              crew scripts (daily check) and logs
└── scratch -> ${ENG_SCRATCH_NOTS}
${ENG_SCRATCH_NOTS}/                   (scratch, heavy)
├── code/<tree>_<commit>/               NEW: frozen code trees used by runs (read-only after copy; compile caches inside are TEMP)
├── runs/<ticket>/<run_id>/             run directories (inputs manifest, outputs, checkpoints, per-run slurm/)
├── slurm_out/                          %x_%A_%a.out|err of new jobs
├── data/                               generated or staged datasets (with hashes)
├── archive/<origin>/                   idle material moved in from older locations, one PROVENANCE.md per folder
│   ├── theory/theory_w2/               (if Theory agrees)
│   ├── home_guard/holding_<date>/      (home-guard holdings)
│   └── relocation_202610/              (Oct-21/22 relocation records)
└── tmp/                                TMPDIR for jobs (tmp/$SLURM_JOB_ID/); crew cleans leftovers > 7 d
${ENG_ROOT_OWLS}/                      (Owls)
├── INDEX.md, tmp/<YYYYMMDD>-<ticket>-<what>/, bench/<YYYYMMDD>-<ticket>-<what>/, crews/, logs/, staging/
```

## 2. What waits, and why

| Item | Reason it waits | Release condition |
|---|---|---|
| `/scratch/fb31/w3scale/` | **ACTIVE**: `code/v32dev_6866f57` is the code under test of the running P1M G0 leg; `out/b3_p*/res/census_p*.rds` are read by P1M REQUESTS R5/R6. Owner: Theory (W3-SCALE) | G0 leg closed **and** Theory/HQ OK |
| `/scratch/fb31/theory_w3/`, `~/projects/BVS/theory_w3/` | **ACTIVE**: RESUME_PLAN proposes resubmitting W3-P6 b1/b2 into these paths. Owner: Theory | Theory decides the resume (before or after it), Theory/HQ OK |
| Owls `/home/fb31/p1m_g0_dryrun/` | **IN USE** (Rscript pid 2754751 writes `stage/stage_p1000.rds`) | G0 helper finished |
| Owls `/home/fb31/bvs_tmp/engineering/20261115-g0-dryrun/` | G0 helper's TMPDIR (R temp dir inside) | G0 helper finished |
| Owls `/tmp/bvs-ci-sandboxes/` | **IN USE** (python pids hold the lock and cwd). Owner: CI | CI's call |

Nothing on NOTS is in use by a job (`squeue` empty; recent WorkDirs all finished). Re-check `squeue -u fb31` and `sacct`
(once) right before any move.

## 3. Ordered moves (NOTS)

Same-filesystem moves inside `/scratch` (VAST) are renames (`mv`, metadata only, near-instant), so no copy is made. Before
each move: `squeue -u fb31` empty for the path; `nice du -sh` and `find -type f | wc -l` recorded; after it, the same counts
at the target and the old path replaced by a symlink (`ln -s <target> <old>`), plus an INDEX row. One move per ssh call.

| # | Source | → Target | Old path keeps | Class | Needs | Note |
|---|---|---|---|---|---|---|
| N1 | `/scratch/fb31/home_holding_20261112/` (0.9 M, 1 tgz) | `${ENG_SCRATCH_NOTS}/archive/home_guard/holding_20261112/` | INDEX row (no symlink: no repo/job reference) | TEMP | HQ OK (HQ infra) | Codex DB backups; keep until HQ says they are not needed |
| N2 | `/scratch/fb31/home_holding_20261111/codex_db-backups_193124.tgz` (4.5 M) | `${ENG_SCRATCH_NOTS}/archive/home_guard/holding_20261111/` | INDEX row | TEMP | HQ OK | then N3 empties the folder |
| N3 | `/scratch/fb31/home_holding_20261111/ccd-cli_2.1.321-c6c6b562e837` (326 MB) | **delete** (see §4, T-N1) | INDEX row | TEMP | HQ OK | regenerable binary; not running (held since 11-11) |
| N4 | `/scratch/fb31/home_guard/` (empty) | `${ENG_SCRATCH_NOTS}/slurm_out/home_guard/` (created only when the guard job is started) | `rmdir` + INDEX row | TEMP | HQ OK | `~/bin/home_guard_job.sh` and `home_guard.sh` hold the paths `/scratch/fb31/home_guard/` and `/scratch/fb31/home_holding_<date>/`: **HQ edits both** to `${ENG_SCRATCH_NOTS}/slurm_out/home_guard/` and `${ENG_SCRATCH_NOTS}/archive/home_guard/holding_<date>/` in the same step |
| N5 | `/scratch/fb31/{scr_*_MOVED.md, qr_small_del2_MOVED.md, cksum_units.sh, del_unit.sh, mkchunks.sh, mkunits.sh}` (12 files) | `${ENG_SCRATCH_NOTS}/archive/relocation_202610/` | INDEX "old paths" table lists all 8 relocated paths + laptop destinations | UNKNOWN (owner's records) | **owner OK** | these files *are* the old-path index of the Oct relocations; copy their content into INDEX first. The checksum lists they cite (`/scratch/fb31/_relocation_manifests/`) are already gone |
| N6 | `/scratch/fb31/theory_w2/` (433 M, 5,957 files, idle since 11-09) | `${ENG_SCRATCH_NOTS}/archive/theory/theory_w2/` | **symlink** `/scratch/fb31/theory_w2 -> …` (19 repo files cite it) | IDLE-KEEP | **needs Theory/HQ OK** (Theory-owned) | not a move of ours unless Theory agrees; alternative: Theory keeps it and lists it in its own index |
| N7 | `/scratch/fb31/theory_w3/` (3.2 M) | `${ENG_SCRATCH_NOTS}/runs/W3-P6/` | **symlink** (5 repo files; resume scripts write here) | ACTIVE | **needs Theory/HQ OK**; waits (§2) | with the symlink in place a resume still works; never move while a W3-P6 job is queued |
| N8 | `/scratch/fb31/w3scale/` (434 M) | `${ENG_SCRATCH_NOTS}/runs/W3-SCALE/` (whole folder, one rename) | **symlink** (4 repo files; `nots/*.sh` and `submissions.jsonl` hold absolute paths) | ACTIVE | **needs Theory/HQ OK**; waits for G0 close | later, optional: copy `code/v32dev_6866f57` → `${ENG_SCRATCH_NOTS}/code/v32dev_6866f57/` (read-only) as Engineering's frozen copy of revision D; the original stays inside `runs/W3-SCALE/` with its runs |
| N9 | `~/projects/BVS/` (campaign-I space, ≈ 168 MB SMC-BVS in home) | **no move**; INDEX row pointing to it | — | IDLE-KEEP | — | self-indexed (`README.md`, `INDEX.tsv`, `tools/check_bvs.sh`, `Environment/path_allowlist.tsv`, 24 + repo files); moving breaks `check_bvs.sh` and the campaign records. It is light enough for home |
| N10 | `~/projects/BVS/Others/library_portable/` (102 M) + `Others/benchmark_releases_Oct2026/` (4.6 M) | `${ENG_SCRATCH_NOTS}/archive/projects_BVS_Others/` | symlinks at both old paths (the releases' `environment.sh` cite the library path) + update `projects/BVS/Others/INDEX.md` | IDLE-KEEP | **owner OK** (Others/INDEX: "owner decides") | optional; frees ≈ 107 MB of home. `library_portable` is mode r-x: the copy across filesystems (home NFS → scratch) is `rsync -a` + count/sha256 check + removal, not a rename. **Never** touch `Others/SMC_BVS_v3_history_Oct2026/` (contains the excluded `deploy/`) |
| N11 | `~/projects/BVS/theory_w2/`, `~/projects/BVS/theory_w3/` (code + task tables, 14 M) | no move | — | IDLE-KEEP / ACTIVE | Theory | Theory code trees and WorkDirs, light, home is fine |
| N12 | ~~`/scratch/fb31/.claude-science/`~~ | **withdrawn** | — | — | — | out of scope (owner, 11-15) |
| N13 | ~~loose non-SMC-BVS files at the scratch root~~ | **withdrawn** | — | — | — | out of scope (owner, 11-15) |

Old-path discipline: a symlink at the old scratch path keeps every hard-coded path (jobs, manifests, docs) working, so no
repo edit is forced. Repo files are updated afterwards by their ticket owners (§7).

## 4. TEMP: what is safe to clean, exact command, why

Run only after HQ's OK, one at a time, on NOTS. None is SMC-BVS research data.

| Id | Item | Bytes | Command | Why it is safe |
|---|---|---|---|---|
| T-N1 | `/scratch/fb31/home_holding_20261111/ccd-cli_2.1.321-c6c6b562e837` | 341,910,032 | `ssh nots 'pgrep -u fb31 -f ccd-cli_2.1.321 \|\| rm -v /scratch/fb31/home_holding_20261111/ccd-cli_2.1.321-c6c6b562e837'` | an old Claude CLI build the guard moved out of home on 11-11; not running; a newer build is in use; regenerable by the tool's own updater |
| T-N2 | `/scratch/fb31/home_guard/` | 0 | `ssh nots 'rmdir /scratch/fb31/home_guard'` (only when N4's script edit lands) | empty; the guard job was never submitted |
| T-N3 | `/scratch/fb31/home_holding_20261111/` (after N2, N3) | 0 | `ssh nots 'rmdir /scratch/fb31/home_holding_20261111'` | empty after the moves |
| T-O1 | ~~Owls /tmp item~~ | — | **withdrawn** | out of scope (owner, 11-15) |

The Codex DB backup tgz files (≈ 5.5 MB) are not proposed for deletion: they are small and HQ may want them.

## 5. Bytes per class (SMC-BVS)

| Class | Bytes | Of which moves in this plan |
|---|---|---|
| ACTIVE | ≈ 744 MB (NOTS 440 MB; Owls `/tmp/bvs-ci-sandboxes` 303 MB, `p1m_g0_dryrun` 0.6 MB) | N7, N8 (437 MB, waiting) |
| IDLE-KEEP | ≈ 601 MB (NOTS scratch `theory_w2` 433 MB; NOTS home `projects/BVS` ≈ 168 MB; Owls bench 0.2 MB) | N6 (433 MB, Theory OK), N10 (107 MB, owner OK) |
| TEMP | ≈ 332 MB (NOTS holdings) + 24 KB (Owls /tmp) | 326 MB deleted (T-N1), 5.5 MB archived (N1, N2) |
| UNKNOWN | ≈ 0.7 MB (NOTS scratch root files, `.claude-science`) | N5 (owner OK); rest listed only |

Home effect: none of the moves adds to home. N10 would free ≈ 107 MB. The home quota (6,761 MB) is driven by app builds
(VS Code server 2.7 G, T3 1.6 G, Codex 0.66 G, Claude 0.41 G), which are the guard's job, not this reorg's (`CREW.md` §3).

## 6. Owls moves

| # | Source | → Target | Old path keeps | Needs | Note |
|---|---|---|---|---|---|
| O1 | `/home/fb31/p1m_feas_bench/` (176 K) | `${ENG_ROOT_OWLS}/bench/20261115-P1M-feas-bench/` | INDEX row in `${ENG_ROOT_OWLS}/INDEX.md` (no symlink: a symlink in `/home/fb31` is itself clutter) | HQ go (Engineering-owned) | 7 repo files cite the old path (§7), all in prose or code comments (`build.sh` and `g0_bench.cpp` only in comments), so nothing reads from it |
| O2 | `/home/fb31/p1m_g0_dryrun/` | kept outputs → `${ENG_ROOT_OWLS}/bench/20261115-P1M-g0-dryrun/`; temporaries → removed | INDEX row | **waits** for the G0 helper | `${ENG_ROOT_OWLS}/tmp/20261115-g0-dryrun/` already exists (empty) for the helper's next run |
| O3 | `/home/fb31/bvs_tmp/engineering/20261115-g0-dryrun/` | removed by the G0 helper at job end (R temp dir) | — | waits | `bvs_tmp/` passes to Theory and CI; Engineering keeps nothing there |
| O4 | `/home/fb31/SMC_Engineering_Department/tmp/20261115-machines/` | removed at the end of this leg | — | — | this leg's TMPDIR |
| O5 | `/home/fb31/BVS-wt/*` | stay | — | — | worktrees are an allowed location; Engineering acts only on its own worktree(s) |
| O6 | ~~other `/home/fb31/*`~~ | **withdrawn** | — | — | out of scope (owner, 11-15) |

## 7. Repo files whose hard-coded paths would change (by ticket owner)

With symlinks at the old NOTS paths nothing breaks; update when the owner next touches the file.

| Old path | Owner | Files |
|---|---|---|
| `/scratch/fb31/w3scale` | Engineering (P1M) | `Docs/Experiments/P1M/REQUESTS.md`, `Docs/Experiments/P1M/REVIEW_fable.md`, `Docs/Experiments/P1M/briefs/BRIEF_opus_g0_scripts.md` |
| `/scratch/fb31/w3scale`, `/scratch/fb31/theory_w3`, `/scratch/fb31/home_holding*`, `/scratch/fb31/home_guard` | HQ / INFRA | `Theory_work/INFRA/NOTS_STORAGE.md`; on NOTS `~/bin/home_guard.sh`, `~/bin/home_guard_job.sh` |
| `/scratch/fb31/theory_w2` | Theory (W2-SIM) | 19 files under `Theory_work/Wave2/W2-SIM/` (INFRA.md, LOG.md, PK/PKA/X DESIGN.md, X/LOG.md, X/configs/*, X/nots/submit_table_x.sh, X/scripts/gen_grid.py, nots/run_table.sh, nots/submit_table.sh, results/*/manifest.json, results/S5P/pilot02/sacct_manifest.txt) |
| `/scratch/fb31/theory_w3` | Theory (W3-P6) | `Theory_work/Wave3/W3-P6/{LOG.md, nots/run_table.sh, nots/submit_table.sh}`, `Theory_work/Pause_2026-11/RESUME_PLAN.md` |
| `~/projects/BVS/Others/library_portable`, `benchmark_releases_Oct2026` (only if N10) | owner / HQ | `projects/BVS/Others/INDEX.md` on NOTS; repo: `Scripts/Campaigns/2026-10-28_New_Campaign/ops/{CLEANUP_LOG.md, CLEANUP_PLAN.md, transfer/verified_delete.sh}` (historical, may stay) |
| `/home/fb31/p1m_feas_bench` | Engineering (P1M) | `Docs/Experiments/P1M/{FEASIBILITY_fable.md, LOG.md, briefs/BRIEF_fable_feasibility.md, briefs/BRIEF_opus_g0_scripts.md, g0/kernel/build.sh, g0/kernel/g0_bench.cpp}` |
| `/home/fb31/p1m_g0_dryrun` | Engineering (P1M) | `Docs/Experiments/P1M/briefs/BRIEF_opus_g0_scripts.md` |
| `/home/fb31/projects/BVS/SMC_BVS_v3/deploy` (exclusion wording; path no longer exists) | HQ | `POLICIES.md`, `Docs/Experiments/P1M/BRIEF.md`, the P1M briefs (21 files cite it): the excluded tree is now `.../Others/SMC_BVS_v3_history_Oct2026/deploy/` |

## 8. Draft additions to `${ENG_ROOT_NOTS}/INDEX.md`

To be appended by the executing leg (HQ go). Kept as a draft here because this leg writes nothing on NOTS.

```markdown
| `scratch/code/<tree>_<commit>/` | frozen code trees used by runs (read-only; `.cpp_cache` inside is TEMP) | one PROVENANCE line per tree (repo, commit, sha256 list) |

## Moved in (reorg 2026-11, plan Docs/Experiments/P1M/machines/REORG_PLAN.md)
| old path | new path | moved | by | old path keeps | provenance |
|---|---|---|---|---|---|
| /scratch/fb31/home_holding_20261112/ | scratch/archive/home_guard/holding_20261112/ | <date> | Engineering | index row | home_guard 11-12 (Codex DB backups) |
| /scratch/fb31/home_holding_20261111/codex_db-backups_193124.tgz | scratch/archive/home_guard/holding_20261111/ | <date> | Engineering | index row | home_guard 11-11; ccd-cli binary deleted (T-N1) |
| /scratch/fb31/*_MOVED.md + relocation tools | scratch/archive/relocation_202610/ | <date> | Engineering (owner OK) | index row | Oct 21–22 relocations to the laptop (table below) |
| /scratch/fb31/theory_w2/ | scratch/archive/theory/theory_w2/ | <date> | Theory (OK <ref>) | symlink | W2-SIM, jobs 2632784–2634898 |
| /scratch/fb31/theory_w3/ | scratch/runs/W3-P6/ | <date> | Theory (OK <ref>) | symlink | W3-P6, jobs 2647903–2689423 |
| /scratch/fb31/w3scale/ | scratch/runs/W3-SCALE/ | <date> | Theory/HQ (OK <ref>) | symlink | W3-SCALE, jobs 2692663–2698180; code v32dev_6866f57 = P1M revision D |

## Relocated off NOTS earlier (record; content on the owner's laptop)
| old path (/scratch/fb31/…) | laptop destination | bytes | files | date |
|---|---|---|---|---|
| BVS | Documents/NOTS_BVS/NOTS_scratch | 35,047,732,354 | 26,528 | 2026-10-21 |
| v3_profiling_20261020 | Documents/NOTS_BVS/NOTS_scratch | 22,458,703,791 | 29,693 | 2026-10-22 |
| archive_staging | Documents/NOTS_BVS/NOTS_scratch | 10,141,716,480 | 4 | 2026-10-21 |
| Experiments_October_14_Mixture | Documents/NOTS_BVS/NOTS_scratch | 4,068,133,849 | 27,535 | 2026-10-21 |
| BVS_Paired_October_14 | Documents/NOTS_BVS/NOTS_scratch | 480,685,924 | 1,214 | 2026-10-21 |
| qr_data/*pmala* (8 dirs) | Documents/NOTS_scratch_other | 5,586,854,208 | 15,231 | 2026-10-22 |
| onizuka_air_runs_20260915 | Documents/NOTS_scratch_other | 1,963,193,378 | 4,820 | 2026-10-21 |
| backups | Documents/NOTS_scratch_other | 15,556,984 | 8 | 2026-10-21 |
(checksum lists were at /scratch/fb31/_relocation_manifests/, now gone on NOTS)

## Elsewhere on NOTS (not moved; pointers)
| path | what | owner |
|---|---|---|
| ~/projects/BVS/ | campaign-I space (frozen v2.2.1, benchmarks, studies, results); self-indexed: README.md, INDEX.tsv, tools/check_bvs.sh | owner / HQ |
| ~/projects/BVS/theory_w2, theory_w3 | Theory code trees and job WorkDirs | Theory |
| ~/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/ | EXCLUDED forever (former SMC_BVS_v3/deploy) | — |
| /projects/ml75 | EXCLUDED forever | — |
```

Owls `${ENG_ROOT_OWLS}/INDEX.md` entries to add on execution: `bench/20261115-P1M-feas-bench/` (from
`/home/fb31/p1m_feas_bench`, O1) and `bench/20261115-P1M-g0-dryrun/` (from `/home/fb31/p1m_g0_dryrun`, O2).
