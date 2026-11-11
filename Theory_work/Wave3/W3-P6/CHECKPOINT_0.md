# W3-P6 — CHECKPOINT 0 (resume leg A; lead Opus 5.5, Claude Work, effort high; 2026-11-11 14:05 CT)

Nothing was submitted, cancelled or written on NOTS (read-only: ls, sha256sum, sacct, squeue, scp from NOTS). No git state
changed. No `HOLD P6` in HOLDS.md at any step. Details: `CP0_SMOKE_MANIFEST.md`; heartbeat in `LOG.md`.

## 1. State reconciliation (read back from NOTS)
- **Queue:** empty. Every w3p6_ task in flight was cancelled 2026-11-09 20:57:50.
- **Integrity:**
  - All 4 frozen run manifests (b1, b2, probe01, smoke_v3) re-verify: every frozen file's sha256 matches its manifest.
  - Code dir `main_2252d57`: its 20 core files are sha256-identical to a fresh `git archive 2252d57`. The LOG's "SHA256SUMS"
    file does not exist on NOTS; this check replaces it.
- **b1** (job 2651495, v2 driver p6_fit.R `64d2d74b…`): 298/320 RDS, all `completed`, 0 `hpm_incomplete`.
  - The 22 missing keys are exactly the 22 sacct-CANCELLED tasks:
    - cs ρ=.5 s₀=4 p=500, reps 2, 4–8;
    - s5 p=250, reps 6, 17–20;
    - cs ρ=.5 s₀=8 p=250, reps 1, 5, 6, 9–11, 15–17, 19, 20.
  - No stray or duplicate RDS.
- **b2** (job 2652199, v3 driver p6_fit.R `ba5299fb…`, p6_common.R `2bf08d62…`, rederive.R `a94098bc…`): 0/240 RDS.
  - 34 tasks started and were cancelled at ≤ 1.20 h: (100,1000) × 20 and (150,150) reps 1–14.
  - 206 tasks never started.
- **probe01:** 10/25 RDS. The 15 long probes were cancelled at 4.73 h unfinished; s5 (100,250) completed in 3.86 h.
- **smoke_v3:** 2/2 RDS.
- **Measured time per fit:**
  - n = 50, p = 250–500 (b1): median 0.56–1.25 h, max 1.52 h. Calibration takes about 70% of the time at p ≥ 250.
  - (100,100): 1.79 h. s5 (100,250): 3.86 h.
  - No cs fit at n ≥ 100 with p ≥ 150 has finished: these cells have a lower bound of 4.73 h, and nothing more is known.
- **Remaining:** 22 b1 tasks (v2), 240 b2 tasks (v3), and the conditional probes ((50,2500), n = 200).
- **Logging defect:** `log/starts.jsonl` and `ends.jsonl` lost lines to concurrent appends (b1: 230 starts and 296 ends
  logged, against 298 completions). For reconciliation I use sacct and the RDS files, not these logs.

## 2. Core-hours used: 495.88 (CPUTimeRAW, all w3p6_ jobs since 2026-11-09)
| job | core-h |
|---|---|
| probe01 | 158.99 |
| b1 | 255.00 |
| smoke_v3 | 0.44 |
| b2 | 81.45 |

**Every one of the 381 allocations had AllocCPUS = 2**, although the scripts request `--cpus-per-task=1` (NOTS allocates a
whole core). So **1 task-hour = 2 core-h**, and a task's worst case is its time limit × 2.

## 3. Smoke manifest (5 tasks)
All 5 are production keys rerun under new RUN_IDs (same seeds, same frozen scripts), so each result counts as that key's
production record.

| # | driver | cell (cs ρ=.5, s₀=4) | rep | limit × CPUs | worst core-h |
|---|---|---|---|---|---|
| S1 | v2 | n=50, p=500 | 2 | 4 h × 2 | 8 |
| S2 | v3 | n=75, p=750 | 1 | 24 h × 2 | 48 |
| S3 | v3 (optional) | n=100, p=250 | 1 | 24 h × 2 | 48 |
| S4 | v3 | n=150, p=150 | 1 | 24 h × 2 | 48 |
| S5 | v3 | n=100, p=1000 | 1 | 24 h × 2 | 48 |

- **Coverage:** both drivers, and every remaining n level (50, 75, 100, 150) at its largest p.
- **S3 is optional:** it is the only way to cost the 7 b2 cells at (100,250).
- **Task tables:** `configs/smk1_v2_tasks.tsv` (`2d9cae2b…`) and `configs/smk1_v3_tasks.tsv` (`a208842c…`). Their command
  lines are byte-identical to the frozen originals.

## 4. Admission arithmetic
- **Worst case:** 495.88 used + 0 queued/running + 8 + 4 × 48 = **695.88 ≤ 1,400** (647.88 without S3).
- **Expected smoke cost:** ≈ 50–115 core-h.
- **Wall clock:** ≤ 24 h.

## 5. Release plan after CP1 (re-costed at CP1 from measured times)
- **Budget:** about 790–850 core-h will be left after the smoke. The watchdog line (`HOLD P6`) is at 1,200 core-h.
- **The rest of b2 does not fit.** At 2 CPUs per task it is expected to cost ≈ 2,800 core-h. The RESUME_PLAN's ≈ 1,240
  counted task-hours.
- **Recommended Plan A** keeps 20 seeds per cell and drops cells. Batches go in order, each admitted only if
  used + Σ(limit × 2) ≤ 1,400.

| batch | tasks | worst core-h | expected core-h |
|---|---|---|---|
| R1 | b1 remainder, 21 tasks | 126 | 33 |
| R2a | (75,75), (75,188), (100,100) × 20 each | 440 | 145 |
| R2b | (100,250) cs ρ=.5 × 19 | 456 | 266 |
| R3 | (75,750) × up to 19, sized to stay ≤ 1,200 | 380 | 228 |

  - Cumulative expected spend ≈ 1,250, so R3 will probably be cut to ≈ 12–15 seeds.
  - Dropped cells: (100,250) breadth variants, (100,1000), (150,150), (50,2500) and n = 200. Each of these has only its
    one smoke seed, if any.
- **Plan B** runs 10 seeds per cell and adds (150,150): ≈ 510 + 33 core-h expected.
- **At CP1 I report:**
  - per task: state, time, core-h, RSS, status, tier/escalation, phase timings;
  - invariants: manifest sha256, seeds, derivation status, F_direct = F_ledger, HPM = ledger max, rederive agreement;
  - outcome classes (descriptive only);
  - the re-costed batches with their Slurm limits.

## 6. Risks and decisions for HQ
1. **Ceiling unit (decision).** The 1,400 ceiling is in CPUTimeRAW core-hours. Because NOTS allocates 2 CPUs per task, it
   buys half the compute the earlier plan assumed: 1,400 core-h is about 700 task-hours. 496 core-h of it is already spent,
   before the resume. HQ or the owner chooses one of:
   - Plan A or Plan B under 1,400;
   - a higher ceiling;
   - counting from the resume only.

   The watchdog's 1,200 line also applies.
2. **Slurm limits shorter than the 22.5-h guard.** If a task hits such a limit, Slurm kills it and it leaves no RDS. Limits
   will be ≈ 1.5 × the measured maximum. A task killed this way is logged as a resource-limit outcome and rerun once,
   following DESIGN policy. The alternative is to lower `hours` in the commands, but that changes preflight and escalation
   admission, which is a design change. Not proposed.
3. **Untested v3 driver.** The v3 driver has never completed a fit at n ≥ 75; the smoke tests it. The (100,1000) and
   (150,150) costs are unknown beyond 4.73 h. S5 may come back `resource_limit` at 22.5 h, which is a valid outcome.
4. **Analysis tooling.** `summarize.py` aborts when one key is scheduled in two runs. Reruns therefore need b1's task table
   filtered to its 298 completed keys, or a rerun-aware loader. I am recording this now; it is fixed under rule 15 before
   analysis. The Group A header mislabel noted in the RESUME_PLAN is still open.
5. **Minor.** The commands pass `mem_gb=12` while Slurm grants 6–8 G. Peak RSS so far is ≤ 1.4 GB, so this is harmless.

**Awaiting HQ / owner approval of the CP0 smoke manifest (S3 in or out) and of decision 1 before anything is submitted.**
