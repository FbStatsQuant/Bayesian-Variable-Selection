# W3-SCALE leg A — log (times CT)

Agents so far: lead = Claude Fable 5.2, effort high, Claude Work (`claudeAgent`). Reviewers: R01 = Codex gpt-6.1-sol,
reasoningEffort high (code review, done); R02 = Codex gpt-6.1-sol, high (blind re-read of the final code, running).
No Claude helper agents.

## NOTS admission ledger (hard cap 150 task-hours)

| # | time (CT) | job | tasks × limit | worst case admitted (h) | cumulative worst case (h) | actual (sacct, h) |
|---|---|---|---|---|---|---|
| 1 | 11-11 19:27 | 2692663 `w3scale_smoke01` (scavenge) | 1 × 0.5 h | 0.5 | 0.5 | 0.00 (FAILED at start, rc 2: task line mangled by shell quoting; scancel sent) |
| 2 | 11-11 19:27 | 2692676 `w3scale_smoke02` (scavenge) | 1 × 0.5 h | 0.5 | 1.0 | 0.02 |
| 3 | 11-11 19:28 | 2692688 `w3scale_prof_p1k` (commons, 8G) | 1 × 2 h | 2 | 3.0 | 0.29 |
| 4 | 11-11 19:28 | 2692689 `w3scale_prof_p2k` (commons, 8G) | 1 × 5 h | 5 | 8.0 | 0.92 |
| 5 | 11-11 19:28 | 2692690 `w3scale_prof_p5k` (commons, 12G) | 1 × 24 h | 24 | 32.0 | running (3.8 h at 23:15) |
| 6 | 11-11 19:28 | 2692691 `w3scale_prof_p20k` (commons, 40G) | 1 × 12 h | 12 | 44.0 | 1.31 |
| 13 | 11-11 23:10 | 2695321 `w3scale_bitid_supp_C` (commons, 8G) | 5 × 1 h | 5 | 47.1 = 18.1 actual + 24 (p5k) + 5 | |
| 14 | 11-11 23:10 | 2695332 `w3scale_setup_cmp_C` (commons, 48G) | 6 × 0.5 h | 3 | 50.1 | |
| 15 | 11-11 23:11 | 2695333 `w3scale_bitid_p500_C` (commons, 4G) | 10 × 0.75 h | 7.5 | 57.6 | |
| 16 | 11-11 23:11 | 2695334 `w3scale_bitid_p500_S5_C` (commons, 4G) | 2 × 0.75 h | 1.5 | 59.1 | |
| 17 | 11-11 23:11 | 2695335 `w3scale_bitid_p1000_C` (commons, 4G) | 10 × 1 h | 10 | 69.1 | |
| 18 | 11-11 23:11 | 2695336 `w3scale_bitid_p1000_S5_C` (commons, 4G) | 2 × 2 h | 4 | 73.1 | |
| 7 | 11-11 19:44 | 2693103 `w3scale_bitid_supp` (commons, 4G) | 3 × 1 h | 3 | 47.0 | 1.47 |
| 8 | 11-11 19:44 | 2693104 `w3scale_setup_cmp` (commons, 40G) | 6 × 0.5 h | 3 | 50.0 | 0.08 |
| 9 | 11-11 19:44 | 2693105 `w3scale_bitid_p500` (commons, 4G) | 20 × 0.75 h | 15 | 65.0 | 3.33 |
| 10 | 11-11 19:44 | 2693106 `w3scale_bitid_p500_S5` (commons, 4G) | 4 × 2 h | 8 | 73.0 | 0.77 |
| 11 | 11-11 19:45 | 2693139 `w3scale_bitid_p1000` (commons, 4G) | 20 × 1.5 h | 30 | 103.0 | 7.03 |
| 12 | 11-11 19:45 | 2693141 `w3scale_bitid_p1000_S5` (commons, 4G) | 4 × 7 h | 28 | 131.0 | 2.88 |

From row 13 on, "cumulative" = sacct actuals of finished jobs + worst case of the jobs still queued or running.

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
- 19:50 — Sol R01 started (Codex gpt-6.1-sol, high; delegate task): code review of the bit-identity claims and of the
  test coverage. Old PROD-H records: the OneDrive mirror is on the PC "Felipe_Bedoya", which T3 reports unreachable;
  Owls holds no copy. The repo keeps only medians of sd(log Z_r) by p x scale (`ev_pip_rb_plain.csv`).
- 19:55 — NOTS: unit harness with the NOTS compiler: dumps byte-identical (sha256 05530354...), 0 reference mismatches.
  Setup-only comparison (v3.1 vs v3.2-dev A) at p = 5k / 10k / 20k: blocks, tables, start, neighbour graph, dup
  components, cut group identical; setup 4.2 -> 1.6 s, 16.3 -> 4.6 s, 85.6 -> 23.1 s; setup peak 0.71 -> 0.52 GB,
  2.49 -> 1.73 GB, 9.46 -> 6.41 GB; neighbour graph 59.1 -> 3.6 s at 20k. Gram only 16.4 -> 14.3 s at 20k (strided
  writes dominate), so the Gram kernel was rewritten: row-major tiles, 16 vector lanes, one triangle + blocked mirror
  (v3.2-dev revision B, 23baba7; locally 2.42 -> 0.63 s at p = 4,001, dumps identical).
- ~20:42 — Run interrupted (Claude Work 5-hour rate limit). Resumed 23:00 on HQ's note. Nothing was lost: commits up to
  a641312, NOTS jobs unaffected.
- 23:02 — Round A (v3.2-dev e5afee7) finished on NOTS: **34 of 34 units IDENTICAL** between v3.1 and v3.2-dev
  (24 PROD-H units, one per p x S x c cell, replicate r001; 10 supplementary units), fingerprint version 1. Two
  escalated fits (`p1000_S5_r001_c100`, `tie_dp_p400`); every score of every fit on the Cholesky route; no fit refused
  by the v3.1 preflight at the PROD-H allocations. Profiles: p1k 1,028 s (calibration 520 s, 5 rebuilds, T = 26),
  p2k 3,293 s (calibration 2,049 s, 8 rebuilds, T = 33), 20k single island N = 2,500: pilot 2,184 s (T = 22), final
  island 2,392 s (T = 29), peak 9.45 GB. p5k still in calibration after 3.6 h.
- 23:03 — Sol R01 returned: **BROKEN for the raw header/export scope**, no difference found on valid fits, scan bound
  valid. Two concrete counterexamples (NaN payloads in the Gram; NaN correlations in the neighbour graph), fingerprint
  too permissive, coverage gaps. All five findings accepted: `reviews/R01_disposition.md`.
- 23:08 — v3.2-dev revision C (bbdfea0): non-finite fallbacks to the v3.1 code in `gram_fill`, `complete_linkage`,
  `neighbour_graph`; fingerprint version 2 (path-specific; guard decisions, allocation and attributes hashed) with a
  mutation self-test (14 mutations detected, 6 timing changes ignored, on 4 fits); unit harness with required-branch
  flags (49 cases locally: dumps identical, 0 reference mismatches, 0 branches missed; refactor route now reached);
  `scripts/export_units.R` (R exports on 11 raw contexts: identical under both cores locally, including the failure
  return of `cpp_setup`); `bitid_compare.R` fails closed.
- 23:11 — HOLDS read (none). Deployed `code/v32dev_bbdfea0`. Round C submitted: 2695321 (unit harness, supplementary
  units under both cores, export test, re-fingerprint of round A's saved fits with version 2, self-test), 2695332
  (setup-only with Gram hash, both cores, 5k/10k/20k), 2695333/4/5/6 (the 24 PROD-H units under revision C only; the
  v3.1 records of round A are reused). Limits from round A's measured walls. Ledger: 73.1 of 150 task-hours.
- 23:12 — Sol R02 started (Codex gpt-6.1-sol, high): blind first read of the final code and tests (told not to open
  `reviews/`).
