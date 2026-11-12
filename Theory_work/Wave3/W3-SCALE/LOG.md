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
