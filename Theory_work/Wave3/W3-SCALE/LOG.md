# W3-SCALE leg A — log (times CT)

Agents so far: lead = Claude Fable 5.2, effort high, Claude Work (`claudeAgent`). Reviewers: R01 = Codex gpt-6.1-sol,
reasoningEffort high (code review, done); R02 = Codex gpt-6.1-sol, high (blind re-read of the final code, done);
R03 = Codex gpt-6-astra, high (break review of DESIGN_v1, done).
No Claude helper agents.

## NOTS admission ledger (hard cap 150 task-hours)

| # | time (CT) | job | tasks × limit | worst case admitted (h) | cumulative worst case (h) | actual (sacct, h) |
|---|---|---|---|---|---|---|
| 1 | 11-11 19:27 | 2692663 `w3scale_smoke01` (scavenge) | 1 × 0.5 h | 0.5 | 0.5 | 0.00 (FAILED at start, rc 2: task line mangled by shell quoting; scancel sent) |
| 2 | 11-11 19:27 | 2692676 `w3scale_smoke02` (scavenge) | 1 × 0.5 h | 0.5 | 1.0 | 0.02 |
| 3 | 11-11 19:28 | 2692688 `w3scale_prof_p1k` (commons, 8G) | 1 × 2 h | 2 | 3.0 | 0.29 |
| 4 | 11-11 19:28 | 2692689 `w3scale_prof_p2k` (commons, 8G) | 1 × 5 h | 5 | 8.0 | 0.92 |
| 5 | 11-11 19:28 | 2692690 `w3scale_prof_p5k` (commons, 12G) | 1 × 24 h | 24 | 32.0 | RUNNING: 8.58 h at 11-12 04:03 (limit 24 h) |
| 6 | 11-11 19:28 | 2692691 `w3scale_prof_p20k` (commons, 40G) | 1 × 12 h | 12 | 44.0 | 1.31 |
| 13 | 11-11 23:10 | 2695321 `w3scale_bitid_supp_C` (commons, 8G) | 5 × 1 h | 5 | 47.1 = 18.1 actual + 24 (p5k) + 5 | 1.94 (one task TIMEOUT at 1 h: v3.1 run of the tie-DP unit) |
| 14 | 11-11 23:10 | 2695332 `w3scale_setup_cmp_C` (commons, 48G) | 6 × 0.5 h | 3 | 50.1 | 0.11 |
| 15 | 11-11 23:11 | 2695333 `w3scale_bitid_p500_C` (commons, 4G) | 10 × 0.75 h | 7.5 | 57.6 | 1.68 |
| 16 | 11-11 23:11 | 2695334 `w3scale_bitid_p500_S5_C` (commons, 4G) | 2 × 0.75 h | 1.5 | 59.1 | 0.38 |
| 17 | 11-11 23:11 | 2695335 `w3scale_bitid_p1000_C` (commons, 4G) | 10 × 1 h | 10 | 69.1 | 4.16 |
| 18 | 11-11 23:11 | 2695336 `w3scale_bitid_p1000_S5_C` (commons, 4G) | 2 × 2 h | 4 | 73.1 | 1.39 |
| 19 | 11-11 23:25 | 2695486 `w3scale_units_final` (commons, 4G) | 1 × 0.33 h | 0.33 | 73.4 | 0.01 |
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
- 23:20 — DESIGN_v1.md revision 1 written from the measured numbers; analysis scripts and result tables
  (`analysis/`, `results/`). Astra R03 started (Codex gpt-6-astra, high): break review of DESIGN_v1.
- 23:22 — Sol R02 returned: NOT ESTABLISHED; no numerical mismatch (49 + 116 private cases, 20,000 Gram cases, exports,
  four fits); the comparison script was not fail-closed, the NaN wording too strong, the "unreachable" A-pivot branch
  reachable, the self-test counted inert mutations. All fixed in scripts, tests and README (`reviews/R02_disposition.md`,
  commit 51cce67); no core file changed. Negative tests of `bitid_compare.R` run locally (version-1 records, wrong
  count, same label twice, unpaired record, changed admission): all exit 1.
- 23:25 — HOLDS read (none). Job 2695486: final unit harness with the NOTS compiler (50 cases): dumps identical
  (sha256 964091b0...), 0 reference mismatches, 0 branches missed.
- 23:28 — Astra R03 returned: DESIGN_v1 UNSOUND (18 findings). All accepted; DESIGN_v1 rewritten as revision 2 with
  auditable source tables (`reviews/R03_disposition.md`, commit 7719b9e). Revision 2 is not re-reviewed.
- ~00:41 (11-12) — Run interrupted again (Claude Work rate limit). Resumed 04:00 on HQ's note.
- 11-12 04:03 — sacct: every job finished except the 5k profile (8.58 h, running). Round C records pulled. Fail-closed
  comparisons, fingerprint version 2: round A v3.1 vs v3.2-dev e5afee7: 34 of 34 IDENTICAL; v3.1 vs v3.2-dev bbdfea0
  on the 24 PROD-H units: 24 of 24 IDENTICAL; supplementary units vs bbdfea0: 10 of 10 IDENTICAL (the round-C v3.1
  run of the tie-DP unit hit its 1 h limit, so its round-A v3.1 record is used). Exports identical (11 contexts),
  self-test passed, setup objects and the whole Gram identical at 5k, 10k, 20k.
- 04:05 — 5k profile so far: calibration 19,444 s; tier 0: pilot T = 23, 11 rebuilds (converged), sd(log Z_r) of the
  diagnostic islands 0.49-2.52, E2 fired at the last rebuild -> escalation; tier 1: 1 rebuild, sd 1.56; the tier-1
  final run (N = 20,000, T = 33) started 00:53 CT and is running. No 10k fit admitted. Tables regenerated; DESIGN_v1
  updated with the 5k evidence.
- 04:15 — CHECKPOINT_1.md written. Ledger: 27.77 task-hours by finished jobs; with the 5k job at its limit at most
  51.8 of 150. Stop: end of leg A; the 5k result is reported as pending (HQ instruction).

## Leg B (HQ-approved 2026-11-12 ~10:40 UTC; new cap 150 task-hours; bit-identical work only; stop at CP2)

HQ decision recorded in `Wave3/HQ_DECISIONS.md` ("W3-SCALE CP1"): CP1 ACCEPTED; leg B = B1-B5; order: fold in 5k, B5
before B2, B4 and B1 in parallel, B3 after B1; O17 ruling (output-identical covers every statistical output and every
quantity in a published table or theorem check; `fresh`/cache counters may differ only if none feeds a published
table, or if serial-equivalent totals are reported that match exactly); reserved items stay with Felipe.

### Leg B admission ledger (cap 150 task-hours; leg A's 5k job 2692690 stays on leg A's ledger)

| # | time (CT) | job | tasks x limit | worst case (h) | cumulative: actual of finished + worst case of open (h) | actual (sacct, h) |
|---|---|---|---|---|---|---|
| B1 | 11-12 04:24 | 2697743 `w3scale_bench_D` (20G) | 3 x 0.67 h | 2.0 | 2.0 | 0.501 |
| B2 | 11-12 04:24 | 2697744 `w3scale_bitid_supp_D` | 5 x 1.5 h | 7.5 | 9.5 | 1.497 |
| B3 | 11-12 04:24 | 2697745 `w3scale_setup_cmp_D` (48G) | 6 x 0.5 h | 3.0 | 12.5 | 0.089 |
| B4 | 11-12 04:24 | 2697746 `w3scale_bitid_p500_D` | 10 x 0.75 h | 7.5 | 20.0 | 1.227 |
| B5 | 11-12 04:24 | 2697747 `w3scale_bitid_p500_S5_D` | 2 x 0.75 h | 1.5 | 21.5 | 0.351 |
| B6 | 11-12 04:24 | 2697748 `w3scale_bitid_p1000_D` | 10 x 1 h | 10.0 | 31.5 | 2.619 |
| B7 | 11-12 04:24 | 2697749 `w3scale_bitid_p1000_S5_D` | 2 x 2 h | 4.0 | 35.5 | 0.890 |
| B8 | 11-12 07:31 | 2698177 `w3scale_b3_p2000` (12G) | 1 x 9 h | 9.0 | 7.17 + 9 = 16.2 | |
| B9 | 11-12 07:31 | 2698178 `w3scale_b3_p5000` (16G) | 1 x 16 h | 16.0 | 32.2 | |
| B10 | 11-12 07:31 | 2698179 `w3scale_b3_p10000` (20G) | 1 x 11 h | 11.0 | 43.2 | |
| B11 | 11-12 07:31 | 2698180 `w3scale_b3_p20000` (36G) | 1 x 16 h | 16.0 | 59.2 | |

### Leg B entries

- 11-12 04:08 — Leg B started. HOLDS read (none). The 5k job is still running (final run at N = 20,000), so the fold-in
  waits for it; the other items start. Agents: R04 = Codex gpt-6-astra, high (second break review of DESIGN_v1).
- 04:10 — B5: Astra R04 started (blind first read of DESIGN_v1 revision 2, with the O17 ruling in the brief).
- 04:20 — B1 (engine, bit-identical), in `core_v32dev`: joint Cholesky of H and A with the v3.1 operand order
  (`chol2_inplace`), lower triangles only, sub-Gram in a member buffer, dead copy removed (`v3_score.h`); Gibbs / swap
  proposals and local-search neighbours formed in the particle and undone on rejection, reused buffers
  (`v3_engine.h`); `TopStore::offer` without an allocation on the quick reject (`v3_ledger.h`; an addition to the B1
  list, same class). New test `tests/engine_bench.cpp` (two islands + both local searches, every output byte dumped).
  Local: dump identical to v3.1 at every step; 4.16 -> about 2.7 us per step (noisy PC).
- 04:22 — B4 (admission only): `v3_preflight_ls0` charges LS0 after the setup with the actual start mode;
  `cpp_start_mode_size`; the start mode is cached in the setup holder and reused by LS0; the initial preflight keeps
  its memory verdict. Option `v3.ls0_preflight = "worst_case"` restores leg A's rule. `tests/preflight_b4.R`: passed
  locally (formula, exhaustive scan-bound check for p <= 40, refusal after setup, same estimates under both rules).
  Fingerprint: the v3.2-only record `preflight_ls0` goes to the delivery record; the comparison counts it as an
  admission decision. Unit harness (50 cases) against the new core: dumps identical to v3.1.
- 04:24 — v3.2-dev revision D = 6866f57 deployed (`code/v32dev_6866f57`). HOLDS read (none). Gate round D submitted
  (ledger B1-B7): engine benchmark at p = 2k and 20k, preflight tests, unit harness, exports, supplementary units,
  setup comparison, and the 24 PROD-H units under revision D (v3.1 records of round A reused).
- 04:27 — Astra R04 returned: DESIGN_v1 revision 2 UNSOUND as a build specification (4 CRITICAL, 5 MAJOR, 1 MINOR):
  `fresh` counts feed published tables and cannot be rebuilt from worker summaries (shared cache cleared when full);
  N1 does not cover the RB PIP; leader stores are outputs; merge memory bound wrong. Verified the first in
  `evidence_h2.py:98-105,139-141`. All accepted: DESIGN_v1 revision 3 (worker-equivalence contract at R' = 4),
  `reviews/R04_disposition.md`, commit 747cc6e. **B2 is not built**: under the O17 ruling case (a) fails and case (b)
  needs a lookup-trace replay (about 6 GB at 1k, 15 GB at 2k for the final run); goes to HQ at CP2.
- 04:29 — First NOTS results of round D: engine benchmark at p = 2k: v3.1 1.69 us per step, revision D 1.21-1.23
  (dumps identical); preflight tests passed; unit harness dumps identical.
- 04:33 — B3 driver `scripts/census_measure.R` (measurement only: tier-0 calibration at the fixed-size budget
  N0 = 2,500 / H0 = 512, frozen grid, then R islands per N on that grid); local smoke passed. To be submitted after
  the gate verdict (B3 after B1).
- 11-12 07:27 — Resumed on Claude Personal (Opus 5.5, high) after the Claude Work limit; HOLDS read in the main
  checkout (none). HQ: change no git state in this run (files edited, nothing committed).
- 07:30 — **Gate round D: PASS.** All 38 round-D tasks rc = 0 (sacct COMPLETED). Records pulled read-only; fail-closed
  comparison (fingerprint version 2), v3.1 records of round A vs revision D (core dd37d323a353): PROD-H 24 of 24
  IDENTICAL, 0 DIFFERENT / ADMISSION_DIFFERS / INVALID / MISSING; supplementary units (both cores in round D) 10 of 10
  IDENTICAL (the tie-DP v3.1 run finished this time). Setup comparison at 5k / 10k / 20k: tables, setup objects, Gram,
  routes identical; v3.2 setup 1.05 / 5.41 / 22.8 s vs v3.1 4.27 / 16.8 / 85.8 s. Engine benchmark p = 20k: v3.1
  1.756-1.766 us per step, revision D 1.257-1.287 (dumps identical, same HPM and F); p = 2k as at 04:29. Preflight B4
  tests passed on NOTS. Tables: `results/bitid_prodh_v31_vs_v32D.tsv`, `results/bitid_supp_v31_vs_v32D.tsv`,
  `results/leg_b_setup_compare_roundD.tsv`. Leg B actual so far 7.17 task-hours (ledger B1-B7 filled).
- 07:31 — HOLDS read (none); W3-P6 has one job running (2689423_4), B3 is 4 single tasks. B3 submitted on revision D
  (bit-identical to v3.1, so the measurement is the v3.1 measurement, faster), staged as `stage/s8` from HEAD 1da2ff6:
  ledger B8-B11, worst case 52 h (CP1 estimate 50; Slurm limit = driver budget + 0.5 h), cumulative 59.2 of 150.
- 07:32 — Submitted: 2698177-2698180 (B3 at 2k, 5k, 10k, 20k; one task each, commons, sapphirerapids), pending on
  priority. The 5k profile 2692690 has been in its final run since 00:53 CT; job wall 12.0 h of a 24 h limit (ends by
  about 19:30 CT). Neither finishes within an hour, so the run ends here (HQ rule). Open for CP2: B3 read-back and
  tables (sigma-hat against p and N); 5k fold-in (CHECKPOINT_1 / DESIGN_v1 §5); B2 options under O17 (DESIGN_v1 §4.1
  "Counters"); ledger actuals for B8-B11. Nothing committed in this run (HQ: change no git state).
- 07:34 — All four B3 tasks RUNNING (started 07:32 CT on Sapphire Rapids); no stderr and no end record. Their logs stay
  empty until the tier-0 calibration ends (the driver's first line is printed then), which is expected.
