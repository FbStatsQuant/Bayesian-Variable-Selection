# Campaign run plan: freeze → 10⁴ → 10⁵ → 10⁶ (Engineering, 2026-11-18)

Executes H-14 (timeline approved, 20 AR-strong 1M replicates, within the H-9 envelope **28.3k core-h**) from the campaign
freeze. Sources: results/CAMPAIGN_PLAN_1117.md (timeline, 440/fit re-costing), MANIFEST_CELLS v0.4 (cells, plan values),
H-9 / H-14 (DECISIONS), F1M_PILOT_FIT.md and T5_1e5.md (measured costs). Freeze: `engine_v4/CAMPAIGN_FREEZE.md`
(method `method-v3.1.1-listpip`, core tree 61b0a582, engine commit F). **Nothing here is submitted without HQ's GO per stage.**

## 1. Basis of the numbers
- **MEASURED:** 1M fit 6-AR-n200-r01-V-s1 = **437.44** core-h (billed; plan 1,188); T5 10⁵ fit 5-AR-n200 = **42.18** (plan 96; T5 gate
  200 → 42.2). Used here: 1M fit = **440**; 10⁵ n = 200 fit = 42.18.
- **ESTIMATES** (no measurement yet): every 10⁴ cost (overlap T at 115/fit is the *upper* end of 52–115; at 52 the block is ≈ 1.24k, −1.26k); the
  10⁵ n = 400 fit (42.18 × 1.6 from the n-scaling c(n), 67.5), IND and ADJ-OPP at 10⁵ (taken as the AR n = 200 value); the 1M self-check
  N = 5,000 (≈ 730, ≈ 2× the island cost); option D (n = 1,000, ×3.43 of a fit: 1,509); ablations (6 % of a V fit per distinct dataset); competitors;
  gates + benchmarks (400, plan value, spend not re-read) and T8 (50).
- **Contingency:** +25 % on the estimates only; measured-cost fits (the 1M AR-strong, ADJ-OPP, AR-weak) at 440 with none, as in CAMPAIGN_PLAN_1117 §2.
  A stress line (§4) puts +25 % on them as well.
- Columns: **v0.4** = MANIFEST_CELLS planning value (sums to 18,014 excl. D, 4,072 D); **basis** = measured where available, else the plan value;
  **+cont** = basis with the contingency. Competitors' 400 block is split 250 (10⁴) / 150 (10⁵) by me; 1M competitors (lasso + 1 variational + SIS on
  20 datasets, ≈ 100–200) taken as 170 on top.

## 2. Stages, gates, core-h (running total in the last three columns)
| # | stage | dates (CT) | v0.4 | basis | +cont | run Σ v0.4 | run Σ basis | run Σ +cont |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 0 | **freeze check** + gates (T5 credited, T8) | Wed 11-18 (today) | 650 | 494 | 607 | 650 | 494 | 607 |
| 1 | **10⁴ T-vs-V overlap** (20 T + 20 V fits), 5k anchor, ablations | Wed 11-18 – ≈ Sat 11-21 (owner pulled the start forward from Thu) | 2,806 | 2,806 | 3,508 | 3,456 | 3,300 | 4,115 |
| 2 | **precision study** (64 islands, 24 fits) + **10⁴ science** (156 fits) + competitors 10⁴ | ≈ Sat 11-21 – Wed 11-25 (H-14: 11-22..26; ≈ 1 day slack) | 4,485 | 4,485 | 5,606 | 7,941 | 7,785 | 9,721 |
| 3 | **10⁵ rung** (12 fits) + ablations + competitors 10⁵ | Fri 11-27 – Mon 11-30 | 1,554 | 767 | 959 | 9,496 | 8,552 | 10,680 |
| 4 | **1M** (below), 22 new fits (+ the pilot) + competitors | Tue 12-01 – ≈ Tue 12-08 | 8,518 | 11,158 | 11,528 | 18,014 | 19,710 | 22,208 |
| D | **option D** (AR-strong n = 1,000), gated | after 4's gate; ≈ 12-08 – 12-10 | 4,072 | 1,509 | 1,886 | 22,086 | 21,220 | **24,095** |

Envelope 28.3k: **margin 6.1k without D, 4.2k with D** (running Σ +cont). CAMPAIGN_PLAN_1117's headline (no 10⁵/T5 credit, its own
contingency rule) was 24.6k without D and 26.5k with D; both are under 28.3k. v0.4 stage 4 has 3 AR reps; stage 4 basis has 20 (the +17 fits).

| stage | what runs | gate **to start** | gate **to pass** (HQ reads) |
|---|---|---|---|
| 0 | Owls reproduction check (done: CAMPAIGN_FREEZE.md §6); NOTS 10⁵ island-hash check (≈ 2 core-h, one island, `tools/slurm/freeze_check_1e5.sh`); T6 restart test on NOTS (≤ 40, inside the 400) | freeze commit F merged into exp/P1M-engine and the PR to main open with CI green (HQ merges it); HQ GO for the 2 core-h submission (given 11-18, together with the overlap) | quick suite all PASS; T3 hashes equal §4.4; NOTS island hash = `0xc4fb97717604869d` (T5 island 1). **A pass makes the pilot replicate 1.** A fail: the pilot stays evidence and a fresh rep 1 is run (+440) |
| 1 | `overlap 1e4` plans (5 generated: V 3, T 2; T = N 10⁴, R′ 4; wave plans are cut from them), T and V on the same 10 datasets, 2 seeds; 5k anchor | stage 0 passed (the NOTS check runs first, then the overlap batches); HQ GO (given 11-18) | T-vs-V overlap clean (the theory link, §0-v2.7); no stage-2 batch is submitted before this |
| 2 | `precision` (3 datasets × 8 arms, own seeds) and `science 1e4` (incl. A3 15, ADJ-OPP, NULL) | stage 1 clean | precision study read out **without changing a frozen V setting** (a change breaks the pilot rule: see stage 0); science cells complete |
| 3 | `rung 1e5`: AR n = 200 ×5, AR n = 400 ×3, IND ×2, ADJ-OPP ×2 | stage 2 done (owner priority over Thanksgiving, 11-26) | **option D gate:** π̂(S₀) and P(HPM = S₀) at n = 200 (5 reps) and the n = 400 trend; 10⁵ cost per fit vs 42 (a re-cost of stage 4 if > 1.25×) |
| 4 | 1M, **2 fits at a time**, each batch pre-announced: (a) AR-strong reps 2–3 + ADJ-OPP + self-check (N = 5,000 on AR rep 1); (b) AR reps 4–20; (c) AR-weak, **last released**; competitors at 1M | stage 3 trend; HQ GO per batch | every fit completed with HPM/MPM reported; AR-weak runs only if the running Σ +cont incl. it ≤ 28.3k |
| D | `option D` plan (1 fit, n = 1,000) | the 10⁵ π̂(S₀) trend (H-1) and the running Σ +cont incl. D ≤ 28.3k | one fit complete; cost vs 1,509 (> 2× → HQ) |

## 3. Stage 4 (1M) in detail, core-h
| cell | fits | v0.4 | basis | cost basis |
|---|---:|---:|---:|---|
| AR-strong, reps 1–20 (rep 1 = the pilot, spent: 437.44) | 20 | 3,565 (3) | 8,797 | MEASURED 437.44 + 19 × 440 |
| ADJ-OPP ×1 | 1 | 1,188 | 440 | MEASURED per fit; the design may differ |
| self-check N = 5,000 on AR rep 1 | 1 | 2,221 | 730 | ESTIMATE |
| AR-weak ×1, gated | 1 | 1,188 | 440 | MEASURED per fit |
| ablations (22 datasets × 6 %) | | 356 | 581 | ESTIMATE |
| competitors at 1M (20 datasets) | | in the 400 | 170 | ESTIMATE |
| **total** | 23 | **8,518** | **11,158** (+cont **11,528**) | |
Pacing (CAMPAIGN_PLAN_1117 §2): one fit ≈ 3 h wall (≈ 8 SPR nodes ≈ 1 h of islands, 1 node ≈ 1.5 h calibration); 2 at a time ≈ 4 fits per day, so 22 fits
≈ 5.5 working days: from Tue 12-01, 20 AR reps by ≈ 12-08. Merge request stays 128G until WP4's plan lands; `p1m_stage_cost.py` on 10⁶ island files
(≈ 1 h on the login node) is the reporting step, not a stage gate.

## 4. Risks priced, and the stop rules
- **Stress:** +25 % on the 21 measured-basis 1M fits (+2.3k) → 26.4k with D, still under 28.3k. A +50 % drift would not fit (≈ 28.7k): that is the trigger below.
- **Pilot rule fails** (stage 0 or a later change to a V setting): +440 for a fresh rep 1, replicate count unchanged.
- **10⁴ T cost** (115 vs 52): stage 1 is the biggest unmeasured block; at 52, −1.26k (−1.6k with contingency). Stage 1 is measured in its first
  batch; re-cost the remaining stages from it before stage 2.
- **Stop rules (H-14):** any projection above 28.3k → the 20 replicates go back to HQ before any other cut; option D stays gated; AR-weak is released last;
  each stage's measured core-h replaces its row here before the next GO (the ledger row is the manager's).
- **Not in the total (named):** the second seed on AR rep 1 (≈ 440), ablations for option D, a 10⁶ re-run after a failed fit (440 per fit).
- The NOTS freeze check is 2 core-h, in stage 0 above. No NOTS submission is made by Engineering helpers; the manager submits after HQ's GO.
