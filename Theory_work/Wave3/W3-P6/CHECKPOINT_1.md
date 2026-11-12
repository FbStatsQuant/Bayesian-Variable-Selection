# W3-P6 — CHECKPOINT 1: smoke gate (lead Opus 5.5, Claude Personal, effort high; 2026-11-12 10:25 CT)

**Gate result: PASS.** All 5 smoke tasks completed and every invariant holds. Nothing was submitted beyond the smoke;
NOTS was read-only this leg (ls, sha256sum, sacct, squeue, scp from NOTS). No git state was changed. There was no
`HOLD P6` at any step. The `w3p6_` queue is empty.

## 1. Smoke read-back (sacct + fit records + RDS)
| # | cell (cs ρ=.5, s₀=4), rep 1 unless noted | driver | Elapsed | core-h (CPUTimeRAW) | MaxRSS | calibration share | tier / triggers | HPM = S₀ (MR1 / cap2 / wide) |
|---|---|---|---|---|---|---|---|---|
| S1 | (50,500) rep 2 | v2 | 1.962 h | 3.925 | 253 MB | 72% | 1 / E2, grid | yes / yes / yes |
| S2 | (75,750) | v3 | 6.609 h | 13.217 | 380 MB | 72% | 1 / E2, grid | yes / yes / yes |
| S3 | (100,250) | v3 | 8.056 h | 16.113 | 250 MB | 70% | 1 / grid | yes / yes / yes |
| S4 | (150,150) | v3 | 9.898 h | 19.797 | 239 MB | 70% | 1 / grid | yes / yes / yes |
| S5 | (100,1000) | v3 | 16.470 h | 32.940 | 484 MB | 74% | 1 / E2, grid | yes / yes / yes |

- **Smoke total:** 85.99 core-h. Every task ended `COMPLETED 0:0` with status `completed`, `hpm_incomplete = false`,
  `cal_status = ok` and no grid fallback.
- **Run time:** calibration takes 70–74% of each fit. LS0 takes 0.5–19 s. The preflight LS0 estimate is 14–50× too high,
  which is harmless.
- **S1 against its b1 cell:** S1 ran longer (1.96 h) than the cell's previous maximum (1.52 h over 14 completed seeds).
  This is consistent with this seed having already run 1.55 h, unfinished, before the 2026-11-09 cancellation. Its
  outcome (S₀) is within the cell's range (8 S₀ / 6 posterior). Timing is not an invariant, but the b1 timings are biased
  downward because the cancelled seeds were the long ones. §3 limits account for this.
- **Outcomes (descriptive only):** in all 5 fits S₀ became the running HPM in the calibration pilot (`pilot/gibbs_flip`,
  φ = .83–.92), and LS0 returned S₀ with termination `no_improvement`. No search failures and no posterior failures.

## 2. Invariants (any failure would stop everything) — all PASS
- **Run manifests:** smk1_v2 and smk1_v3 `manifest.json` match the CP0 sha256 values for both task tables (2d9cae2b…,
  a208842c…), all frozen scripts (p6_fit v2 64d2d74b… / v3 ba5299fb…, p6_common 2bf08d62…, rederive a94098bc…, make_tasks,
  summarize v2 frozen 8011253e…), run_table.sh and env_sim.sh. Code commit is 2252d57. The copies read back from NOTS
  re-hash identically.
- **Seeds:** data and method seeds equal the DESIGN §1 formula for all 5 fits.
- **Derivation:** MR1 and cap2 status are `ok` (no tie, no censoring) for all 5. Running the frozen `rederive.R` on the
  5 RDS reproduces every in-run field: HPM, F, eq_S0 per cap, LS0-scores-S0 per cap, caps, and classes (v3).
- **Ledger:** |F_direct − F_ledger| = 0 for all 5. HPM F equals the maximum over the whole recorded ledger (LS0 centre,
  path, scans and returned model, pre-LS0, pre-local, F(S₀)). HPM equals the LS0-returned model. All LS0 scans are complete.
- **Job identity:** the fit records carry per-element Slurm ids 2689427/28/29 for array tasks 1–3 and 2689423 for task 4.
  This matches sacct JobIDRaw.

## 3. Ledger and stage-1 release plan (HQ_DECISIONS "W3-P6 CP0")
**Used:** 581.868 core-h (sacct CPUTimeRAW, 386 allocations of all `w3p6_` jobs since 2026-11-09). That is 495.876 before
the resume plus 85.99 for the smoke. Limits: ceiling 1,896; watchdog `HOLD P6` at 1,700.

**Admission ledger (proposed precise reading of rule 10):**
- L = CPUTimeRAW of *finished* allocations + Σ(time limit × 2) over queued and running tasks.
- Release only if L ≤ 1,896.
- Counting the elapsed time of running tasks in both terms would double-count it. L as defined is an upper bound on the
  final spend.
- Second check before each release: the projected total (finished + measured median × 2 for every running, queued and
  remaining stage-1 task) must be ≤ 1,700. If it is not, stop releasing and return to HQ.

**Task tables:** 98 tasks, written to `configs/s1_*_tasks.tsv` (LF).
- Each line is byte-identical to its frozen NOTS line (b1 `70d6c1ee…`, b2 `53b5a762…`), renumbered.
- Seeds are unchanged and each key is released once.
- Submission uses `sim/submit_table.sh <tag> <table> runs/b{1|2}/scripts commons <limit> <6G|8G> <n>`.

| run | cell / tasks | costed by | Slurm limit | worst core-h | expected core-h | sha256 (table) |
|---|---|---|---|---|---|---|
| s1_d1 | (100,1000) reps 2–6 (5) | S5 16.47 h | 24:00:00 (1.5× = 24.7 h > 24; the in-fit 22.5-h guard returns `resource_limit` first) | 240 | 165 | b8fff366… |
| s1_d2 | (100,1000) reps 7–10 (4), after d1 ends | S5 + d1 | 24:00:00 | 192 | 132 | 765196fc… |
| s1_h1 | (100,250) cs ρ=.7, reps 1–5 | uncosted (S3 proxy 8.06 h) | 24:00:00 | 240 | ≈ 81 | d3a3a1e4… |
| s1_h2 | (100,250) cs ρ=.5 s₀=8, reps 1–5 | uncosted | 24:00:00 | 240 | ≈ 81 | d70b7f62… |
| s1_h1b / s1_h2b | the same cells, reps 6–10 (5 + 5), after h1 / h2 | h1 / h2 max | 1.5 × measured max | ≈ 121 each | ≈ 81 each | 9ebd736f… / 987099dd… |
| s1_c | (100,250) cs ρ=.5 s₀=4, reps 2–10 (9) | S3 8.056 h | 12:10:00 | 219 | 145 | be43d066… |
| s1_b | (75,750) reps 2–10 (9) | S2 6.609 h | 10:00:00 | 180 | 119 | 5afdb30b… |
| s1_g1 → s1_g2 | (75,188) reps 1–5 → 6–10 | uncosted → g1 max | 24:00:00 → 1.5 × max | 240 → small | ≈ 30 total | 76b732cc… / 72ff6f60… |
| s1_e | (100,100) reps 1–10 (10) | probe01, 1 seed, 1.783 h | 02:45:00 | 55 | 36 | c27637f0… |
| s1_f1 → s1_f2 | (75,75) reps 1–5 → 6–10 | uncosted → f1 max | 24:00:00 → 1.5 × max | 240 → small | ≈ 10 total | 6fd13aac… / 6b54a604… |
| s1_b1r | b1 remainder, 21 tasks (v2 scripts, 6G) | b1 + S1 (max 1.96 h, incl. censored) | 03:00:00 (≥ 1.5 × each cell's max) | 126 | ≈ 40 | 8326f445… |

**Expected stage-1 cost:** ≈ 1,000 core-h, giving a projected total of ≈ **1,580** (ceiling 1,896, watchdog 1,700).
- The main uncertainty is the two breadth cells (≈ 320 expected, ± 30%) and (75,188).
- If the first sub-batch of h1/h2 measures more than ≈ 10 h per fit, the projection check above stops releases before
  1,700 is reached.

**Release order (longest first; each step only if L ≤ 1,896):**
- **Wave 1, at go:** d1, h1, h2, c, b, e, b1r. Reserved 1,300, so L = **1,881.9**.
- **Then, as runs finish, in this order:** d2 (after d1), h1b/h2b (after h1/h2), g1, g2 (after g1), f1, f2 (after f1).
  The longest-first rule holds the short uncosted cells until reservations free up. Wall clock is unaffected: stage 1 is
  bounded by the two sequential (100,1000) sub-batches, ≈ 33–36 h.
- At most 98 tasks are ever concurrent (≤ 150). Each run's throttle equals its size. Every release is logged with its
  ledger in LOG.md.

**Policy:**
- A Slurm TIMEOUT or node failure is rerun once, same seed, new RUN_ID, at 24:00:00. It is logged and not counted as a
  failure.
- An in-fit `resource_limit` is an outcome, not rerun.
- Every scheduled seed stays in the denominator.
- **Kept, not released:** (150,150) is deferred (smoke seed only).
- **Dropped:** (100,250) cs ρ=.3, fac2 and s5; n = 200; (50,2500). These are budget cuts, reported as scheduled-not-run.

**Stage 2 (pre-declared):** reps 11–20 on (75,750), (100,1000), (75,188) and (100,250) cs ρ=.5, plus any kept cell with
1–3 failures among reps 1–10.
- Projected cost: ≈ 650 core-h, which would bring the total to ≈ 2,230, above 1,896. **The ceiling binds:** after stage 1
  only ≈ 120 (to 1,700) or ≈ 320 (to 1,896) remains.
- I stop at the end of stage 1 and return to HQ with measured costs. No stage-2 task is released without an HQ go.

## 4. Analysis tooling (rule 15)
- **Sol review R02 of summarize.py v2 → v3:** **ACCEPT-WITH-FIXES** (`reviews/R02_summarize_v3_sol.md`; brief
  `reviews/BRIEF_R02_summarize_v3_sol.md`).
  - Supplied data reconcile correctly, and no silent mis-count occurs on valid inputs.
  - Three MAJOR findings, none of which affects any NOTS run:
    - a reused TAG bypasses table membership;
    - the record `run` field is unchecked;
    - one transfer slot per key blocks a retry of a released b2 key.
  - One MINOR finding: seeds are not validated.
  - All four are accepted (`reviews/R02_disposition.md`).
- **summarize v4** fixes all four, including an explicit release/retry attempt chain. It is written locally during
  stage 1 and gets a fresh Sol review before any analysis or retry summary.
- The Group A header mislabel is still open and is fixed in v4.

## 5. Decisions for HQ
1. **GO for stage-1 wave 1** as in §3: d1, h1, h2, c, b, e, b1r; L = 1,881.9 ≤ 1,896. Subsequent waves are released by
   the lead under the ledger rule.
2. **b1 remainder (my reading).** "Kept: b1 remainder" means all 21 tasks, completing the three n = 50 cells to 20/20 for
   ≈ 40 core-h. The literal reps ≤ 10 reading would be 11 tasks and save ≈ 20 core-h.
3. **Admission reading.** L counts finished allocations plus limits of queued and running tasks (§3).
4. **Stage-2 trigger.** I propose that "failure" means a completed fit whose as-coded (MR1) HPM ≠ S₀, of class posterior
   or search. Resource-limit outcomes do not count.
5. **(100,100) is costed from one probe seed (limit 2:45).** A kill there is rerun at 24 h. Alternatively, treat it as
   uncosted: 5 + 5 at 24 h, which pushes it out of wave 1.
