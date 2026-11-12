# W3-SCALE leg A — log (times CT)

Agents so far: lead = Claude Fable 5.2, effort high, Claude Work (`claudeAgent`). Reviewers: none started yet.

## NOTS admission ledger (hard cap 150 task-hours)

| # | time (CT) | job | tasks × limit | worst case admitted (h) | cumulative worst case (h) | actual (sacct, h) |
|---|---|---|---|---|---|---|
| 1 | 11-11 19:27 | 2692663 `w3scale_smoke01` (scavenge) | 1 × 0.5 h | 0.5 | 0.5 | 0.0 (cancelled by lead while pending: task line mangled by shell quoting) |
| 2 | 11-11 19:27 | 2692676 `w3scale_smoke02` (scavenge) | 1 × 0.5 h | 0.5 | 1.0 | |
| 3 | 11-11 19:28 | 2692688 `w3scale_prof_p1k` (commons, 8G) | 1 × 2 h | 2 | 3.0 | |
| 4 | 11-11 19:28 | 2692689 `w3scale_prof_p2k` (commons, 8G) | 1 × 5 h | 5 | 8.0 | |
| 5 | 11-11 19:28 | 2692690 `w3scale_prof_p5k` (commons, 12G) | 1 × 24 h | 24 | 32.0 | |
| 6 | 11-11 19:28 | 2692691 `w3scale_prof_p20k` (commons, 40G) | 1 × 12 h | 12 | 44.0 | |
| 7 | 11-11 19:44 | 2693103 `w3scale_bitid_supp` (commons, 4G) | 3 × 1 h | 3 | 47.0 | |
| 8 | 11-11 19:44 | 2693104 `w3scale_setup_cmp` (commons, 40G) | 6 × 0.5 h | 3 | 50.0 | |
| 9 | 11-11 19:44 | 2693105 `w3scale_bitid_p500` (commons, 4G) | 20 × 0.75 h | 15 | 65.0 | |
| 10 | 11-11 19:44 | 2693106 `w3scale_bitid_p500_S5` (commons, 4G) | 4 × 2 h | 8 | 73.0 | |
| 11 | 11-11 19:45 | 2693139 `w3scale_bitid_p1000` (commons, 4G) | 20 × 1.5 h | 30 | 103.0 | |
| 12 | 11-11 19:45 | 2693141 `w3scale_bitid_p1000_S5` (commons, 4G) | 4 × 7 h | 28 | 131.0 | |

## Entries

- 2026-11-11 19:05 — Started. `git switch -c theory/W3-SCALE` at 613f063. Read BRIEF, SCALING_DESIGN_v0, RERUN_SPEC,
  scaling_scratch (RESULTS, bench.cpp), Wave3 PROTOCOL, HOLDS (main checkout: no holds), and the whole v3.1 core
  (R drivers and C++ headers).
- 19:16 — NOTS reconnaissance (`ssh nots`, read-only). Only fb31 jobs: W3-P6 smoke `w3p6_smk1_v3` (4 tasks, commons).
  Partitions: commons 24 h (sapphirerapids 192 CPUs / 257 GB; cascadelake), scavenge 1 h. Home quota 10,026 of
  10,240 MB used, so the W3-SCALE workspace goes to `/scratch/fb31/w3scale`.
- 19:20 — PROD-H inputs and results were relocated off NOTS on 2026-11-03 (`bench20261019/RELOCATED_20261103.md`); the
  OneDrive mirror "NOTS Data" is not on this PC (DESKTOP-955G53S). The generator (`Scripts/Data_generators/gen_prod_data.R`)
  and the input manifest with x/y sha256 (`~/projects/BVS/Data_Generation/manifests/high_p/inputs_manifest.csv`) are on
  NOTS, so PROD-H inputs can be regenerated there and checked against the manifest. The old v2.2.1 records (needed for
  A1–A8 against the old study and for the sd(log Ẑ_r) table) are not reachable from here yet.
- 19:25 — PLAN.md written.
- 19:26 — Profiling driver `scripts/profile_fit.R` + `scripts/ws_common.R` (phase timers, VmHWM reset per phase, stage
  counts, fit fingerprint); job scripts `nots/{env_scale,run_task,submit}.sh` (PROD-H toolchain: GCC 14.3.0, R 4.5.2,
  one thread; `--constraint=sapphirerapids`). Local smoke (Windows, R 4.6.1, Rtools GCC 14.3): p = 70 full fit and
  island mode run end to end (T_pilot 18, T_grid 23, 2 rebuilds, HPM = truth).
- 19:27 — Deployment to `/scratch/fb31/w3scale`: v3.1 core = `git archive 613f063 Scripts/SMC_BVS/core` with
  `core.autocrlf=false` (LF). Finding: plain `git archive` on this Windows checkout writes CRLF (the W3-P6 deploy
  `theory_w3/code/main_2252d57` is CRLF); the W3-SCALE deploy equals the P6 deploy file by file after removing CR
  (sha256 check). The frozen study generators on NOTS (`~/projects/BVS/Data_Generation/high_p`) equal the repo's modulo
  CR; the drivers use the NOTS copies.
- 19:28 — HOLDS read (none). Submitted the v3.1 profile: jobs 2692688 (p1k = PROD-H `p1000_S3_r001_c100`, full fit saved),
  2692689 (p2k), 2692690 (p5k), 2692691 (p20k, island mode N = 2,500), all commons / sapphirerapids, 1 task each; plus
  the scavenge smoke 2692676 (environment check + p = 70). Worst case admitted so far: 44 task-hours of 150.
  All five started within a minute (no queue wait); W3-P6 has 4 running tasks, nothing pending.
- 19:30 — Smoke 2692676 done (70 s). Environment checks on a sapphirerapids node (Xeon Platinum 8468): compile line
  `-fpic -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2` (pinned flags in force); VmHWM reset works; PROD-H
  datasets regenerated with the frozen generator match the frozen input manifest (x and y sha256) for
  `p1000_S3_r001`, `p0500_S1_r001`, `p1000_S5_r100`, `p0500_S6_r050` at c100 and c050.
- 19:32 — First profile numbers: setup total 0.18 s (1k), 0.61 s (2k), 3.3 s (5k), 85 s (20k); setup peak RSS 9.45 GB at
  20k (24 p^2 = 9.6 GB, as the v0 memory model says).
- 19:38 — v3.2-dev written: `Scripts/SMC_BVS/core_v32dev/` (copy of the v3.1 core; changes in `v3_score.h` (Gram lanes),
  `v3_blocks.h` (distance straight from the Gram; neighbour graph by partial selection), `v3_start.h` (tables by DFS with
  a bordered Cholesky; fallbacks call the production scorer; failure path reruns the block by the v3.1 loop),
  `v3_fit.R` (LS0 preflight scan bound p + k*(p - k*))). The other 14 files are identical to v3.1 modulo CR.
- 19:40 — Header-level harness `tests/bitid_units.cpp` (same source compiled against each core, production flags, Rtools
  GCC 14.3 locally): 30 cases, dumps byte-identical (236 MB with the large cases), 0 in-process reference mismatches.
  Branches reached: augmented-QR route (444 / 248 / 126 table scores in three un-standardised duplicate designs),
  Q recomputation (2 to 32 per case in five cases), NumericalFailure while scoring the tables (2 cases), sub-models
  above K (2 cases), exact ties (duplicated, sign-flipped and integer designs), p = 1..17. The refactor route
  (Cholesky on a Gram recomputed from X) never succeeds in either core: the recomputed Gram has the same bits as the
  stored one, so it fails whenever the first route fails. Local times at p = 4,001 (v3.1 -> v3.2-dev): Gram 1.91 -> 0.70 s,
  neighbour graph 2.89 -> 0.16 s, tables 0.56 -> 0.08 s.
- 19:43 — Fit-level runner `scripts/bitid_fit.R` + `scripts/bitid_compare.R`. Local run (Windows) of the supplementary
  units under both cores: 9 of 9 finished units have identical fingerprints (3 exact-branch fits, 4 SMC fits with
  duplicates / integers / near-constant columns, `y_constant`, `no_predictors`); `tie_dp_p400` still running.
- 19:45 — HOLDS read (none). v3.2-dev deployed to NOTS (`code/v32dev_e5afee7`, LF). Submitted: 2693103 (units harness
  with the NOTS compiler + supplementary units under each core), 2693104 (setup-only, v3.1 vs v3.2-dev at p = 5k, 10k,
  20k), 2693105/2693106/2693139/2693141 (24 PROD-H units = one per p x S x c cell, replicate r001, each under both cores,
  PROD-H allocation passed to `v3_fit`; Slurm limits 0:45 / 2:00 (S5) at p = 500 and 1:30 / 7:00 (S5) at p = 1000).
  Worst case admitted so far: 131 task-hours of 150 (smokes used 0.02 h).
