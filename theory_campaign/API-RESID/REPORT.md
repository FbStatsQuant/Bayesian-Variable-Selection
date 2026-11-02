# API-RESID: RESID-STEP0, the post hoc start-table check on the 2,400 PROD-H fits

Synthesis task 8 (`W8-SYNTH · SYNTHESIS.md §8`), from `F-SIGMA · REPORT.md §10` Step 0 (and Step 2, the residualised
alternative). **No SMC runs. No regenerated data. No refits.** Every number below is a post hoc recomputation of the
start law π₀ from the production setup (blocks + v3 tables) of the same 2,400 fits that O-LS0 used.

## 0. Answer in brief

- **Common σ̂² (§4.5): settled on the real fits, against.** None of the three feasible plug-ins gives one favourable fit
  (0/2,400 each). The F-SIGMA §10 stop rule fires: C-fix floods to the cap K = 100 in 2,113/2,400 fits, and the oracle and
  s²(S₀) plug-ins flood in essentially all fits. The other two plug-ins do not flood, but they do not help either:
  σ̃²_{S̃₀} destroys π₀(R₂) (median 0.81 → 5·10⁻⁶), and s_y² reproduces v3 to within half a decade. **No SMC pilot for
  common σ̂².**
- **Residualised (backfit) tables, 3 sweeps: the O-DILUTE pilot replicates on the real fits.** Median log₁₀π₀(S₀) goes
  from −15.65 (v3) to −1.07. 1,888/2,400 fits are favourable (O-DILUTE criterion π₀(S₀) ≥ 10⁻⁴), against O-DILUTE's
  378/480 on regenerated data (78.7% vs 78.8%). The start mode equals S₀ in 1,245/2,400 fits, and there is no flooding.
  It is weak in S5 (1–44 favourable per 100) and in S4 at c = 0.5 (74 and 47).
- **But a start change cannot move the study's headline accuracy.** In the study, 1,829 fits recovered S₀ exactly, 565
  were posterior misses (S₀ was scored and lost on the posterior, so no start or search change can report S₀ there), and
  6 stopped on a resource limit, all in S5. The most any start change can add to HPM = S₀ is those 6 fits (0.25%).
  Backfit puts its start mode on S₀ in 2 of the 6.
- **Is it worth an investment-rule pilot?** Only if what Felipe wants is (a) a start that is favourable at the study size
  (for the theorem side: T22(iii)/T38 regime claims), or (b) cheaper or more stable SMC runs. It is **not** worth a pilot
  for the reported recovery numbers. Step 0 caps that gain at 6/2,400, and the change can also cost: in principle it can
  turn an exact recovery into a posterior-mode correction (the same asymmetry S-ELS found for LS0). Two caveats should be
  resolved free, post hoc, before any pilot:
  - 3 sweeps is not shown to be a fixed point (§3.4).
  - Backfit lowers π₀(R₂) sharply in S5 (§3.3).
- **Status, unchanged:** residualised tables remain an **unproven candidate**. No theorem covers them, and T22(iii) would
  need restating. This run adds the real-fit start-law evidence only.

## 1. What was computed, and the reproduction check

**Data.** These are the 2,400 PROD-H fits: p ∈ {500, 1000} × scenarios S1–S6 × 100 replicates × c ∈ {1, 0.5}, with n = 200,
s₀ = 14, B = 14 and K = 100. They are read from O-LS0's copy (`/home/fb31/ls0_work/study`). For each fit,
`scripts/resid_step0.R` runs the production path up to the setup (`v3_preprocess → v3_context → v3_setup`), exactly as in
O-LS0's `10_ls0_fit.R`. It then computes every table entry's (log D_U, t_U) (`scripts/block_stats.cpp`) and rebuilds the
start with the production `v3_start`/`cpp_ls0_*` engine from each alternative table set:

| key | tables | feasible? |
|---|---|---|
| `v3re` | v3 tables rebuilt from (log D_U, t_U): the method | yes |
| `C_mode` | common σ̂² = σ̃²_{S̃₀} = (2b₀ + Q_{S̃₀})/(2ν), with S̃₀ the v3 start mode | yes |
| `C_fix` | C-fix: σ̂² ← σ̃²(mode of π₀^C[σ̂²]) from σ̃²_{S̃₀}, until the mode repeats (≤ 20 iterations; 1–10 used, median 3) | yes |
| `C_sy2` | common σ̂² = (2b₀ + yᵀy)/(2ν) (null plug-in s_y²) | yes |
| `C_S0` | common σ̂² = σ̃²_{S₀} | no (uses S₀); extra |
| `C_orc` | common σ̂² = sample var(ε) on the standardised scale | no (oracle); extra |
| `resid1`, `resid3` | O-DILUTE `resid`: v3 tables of block b on y − X_{−b}β̂_{−b}, with β̂ the OLS fit of the current start mode (from the v3 mode), after 1 and 3 sweeps | yes |

Per variant and fit, the script records log π₀(S₀), log π₀(R_d) for d = 0, 1, 2 (R_d = models with at most d non-truths,
any subset of S₀; engine `cpp_ls0_pi0_Rd`), and the start mode (engine `cpp_ls0_start_mode`) with its size and truth
count. Wall time was about 0.5 s per fit at p = 500 and 1 s at p = 1,000 for all eight variants together.

**Reproduction (all 2,400 fits).**
- The rebuilt v3 tables match the engine's to 3.1·10⁻¹³ (natural-log units).
- The rebuilt log π₀(S₀) matches O-LS0's per-fit record to 1.6·10⁻¹².
- The start-mode size equals O-LS0's record in 2,400/2,400 fits.
- No fit errored.

So the v3 row below *is* the study's start law, not an approximation of it.

**Files.**
- `results/per_fit.csv`: merged, 2,400 rows; the shards are kept.
- `results/tables.md`: pooled and per-cell tables for every variant (`scripts/aggregate.py`).
- `results/extra_tables.md`: favourable counts, the flooding check, and the cross-tab against the study outcome
  (`scripts/report_extra.py`). The study outcome comes from O-LS0's `agg_final/paired_per_fit.csv`.

## 2. Common σ̂²: Step 0 result (settles W8-SYNTH §4.5 on the real fits)

Pooled over the 2,400 fits (`tables.md`, "Pooled"; `extra_tables.md` (a), (b)):

| variant | med log₁₀π₀(S₀) [IQR] | med π₀(R₂) | med start mode: truths + extras | favourable (≥ 10⁻⁴) | mode ≥ 10 extras | mode at K | paired vs v3: up / down > 1 decade |
|---|---|---|---|---|---|---|---|
| v3 (method) | −15.65 [−18.5, −13.4] | 0.813 | 4 + 0 | 0 | 1 | 0 | — |
| σ̃²_{S̃₀} | −18.59 [−27.4, −13.9] | 4.6·10⁻⁶ | 9 + 7 | 0 | 949 | 35 | 1,041 / 1,114 |
| C-fix | −887.91 [−1375, −591] | 0 | 11 + 88 | 0 | 2,125 | 2,113 | 193 / 2,147 |
| s_y² | −16.12 [−18.9, −13.9] | 0.848 | 4 + 0 | 0 | 0 | 0 | 6 / 49 |
| σ̃²_{S₀} (extra) | −737.05 | 0 | 11 + 89 | 0 | 2,400 | 2,373 | 0 / 2,400 |
| oracle σ² (extra) | −710.15 | 0 | 11 + 89 | 0 | 2,400 | 2,339 | 0 / 2,400 |

(The truths + extras column gives the medians of each count separately.)

The plug-in values explain the three behaviours (`tables.md`, "Plug-in values"; a = σ²_orc/σ̂²):
- **s_y² ≈ 0.995**, so a = 0.04–0.19. It sits far above σ², at the null scale the v3 integration already uses. The start
  is v3's to within a median 0.44 decades: no flooding and no gain.
- **σ̃²_{S̃₀} = 0.35–0.80**, so a = 0.07–0.31. It shrinks the null scale part of the way. Nulls are over-rewarded enough
  to add a median 7 extras (≥ 10 extras in 949 fits), which collapses π₀(R₂), but not enough to reach the cap. The
  median π₀(S₀) falls by 0.42 decades. The paired split is even (1,041 up, 1,114 down), and no fit becomes favourable.
- **C-fix** iterates down to a ≈ 0.7–2.1 outside S5, i.e. to σ̂² near σ². There it floods exactly as F-SIGMA Theorem S6
  predicts: the mode hits K = 100 in 97–100 of 100 fits in every non-S5 cell, at both c. In S5 it stops early
  (σ̂² ≈ 0.5–0.8, a ≈ 0.1–0.26) and floods in only 17–49 of 100. The oracle and σ̃²_{S₀} plug-ins (a ≈ 1) flood in
  every cell. Their medians (−710, −737) match O-DILUTE's −690 on regenerated data.

**Reading.**
- F-SIGMA §10's expected outcome, "flooding (mode size ≈ K) in S1/S3/S4/S6 at c = 1 for every plug-in near σ²", is
  observed, and in fact in every non-S5 cell at both scales.
- The two plug-ins that are not near σ² either reproduce v3 (s_y²) or trade π₀(R₂) for nothing (σ̃²_{S̃₀}).
- The stop rule applies: **no SMC pilot is needed for common σ̂²**.
- W8-SYNTH §4.5 is confirmed on the real fits in the direction O-DILUTE and F-SIGMA gave. This confirms a rejection. It
  changes no theorem status (F-SIGMA S6 stays PROVED as before; O-MIX's block-orthogonal-toy evidence is not
  contradicted, it just does not transfer).

## 3. Residualised (backfit) tables: Step 0 / Step 2 result

### 3.1 Pooled

| variant | med log₁₀π₀(S₀) [IQR] | med π₀(R₂) | med start mode: truths + extras | mode = S₀ | π₀(S₀) > 0.1 | favourable (≥ 10⁻⁴) | mode ≥ 10 extras | mode at K |
|---|---|---|---|---|---|---|---|---|
| v3 (method) | −15.65 [−18.5, −13.4] | 0.813 | 4 + 0 | 0 | 0 | 0 | 1 | 0 |
| resid, 1 sweep | −8.22 [−12.2, −5.3] | 0.589 | 9 + 1 | 27 | 12 | 351 | 156 | 0 |
| resid, 3 sweeps | −1.07 [−3.2, −0.7] | 0.713 | 14 + 0 | 1,245 | 1,142 | 1,888 | 52 | 0 |
| O-DILUTE pilot, resid (480 regenerated fits) | −1.0 | 0.71 | "14/14 in most cells" | — | — | 378/480 | — | — |

Compared fit by fit with v3, resid3 is more than 1 decade higher in 2,289 fits and more than 1 decade lower in 75
(median +13.2 decades).

**The O-DILUTE pilot replicates on the study's own fits.** The median, π₀(R₂) and the favourable share (78.7% vs 78.8%)
agree to the reported precision. This is the first time the backfit start has been evaluated on the PROD-H data rather
than on regenerated data that is equal in law.

### 3.2 Per cell (resid3; `tables.md` "Per cell", `extra_tables.md` (a))

| cell (p, S, c) | med log₁₀π₀(S₀) [IQR] | med π₀(R₂) (v3) | mode = S₀ | π₀(S₀) > 0.1 | favourable |
|---|---|---|---|---|---|
| 500 S1 0.5 / 1 | −0.87 / −0.66 | 0.77 / 0.79 (0.96 / 0.95) | 69 / 89 | 62 / 85 | 100 / 100 |
| 500 S2 0.5 / 1 | −0.89 / −0.66 | 0.77 / 0.79 (0.89 / 0.84) | 62 / 89 | 57 / 85 | 97 / 100 |
| 500 S3 0.5 / 1 | −1.46 / −0.63 | 0.65 / 0.81 (0.74 / 0.69) | 36 / 90 | 32 / 90 | 94 / 100 |
| 500 S4 0.5 / 1 | −2.76 / −0.68 | 0.28 / 0.79 (0.28 / 0.25) | 9 / 83 | 3 / 73 | 74 / 100 |
| 500 S5 0.5 / 1 | **−16.27 / −5.39** | **0.027 / 0.33** (0.93 / 0.88) | 0 / 23 | 0 / 18 | **4 / 44** |
| 500 S6 0.5 / 1 | −1.53 / −0.66 | 0.66 / 0.80 (0.70 / 0.65) | 40 / 89 | 32 / 83 | 95 / 100 |
| 1000 S1 0.5 / 1 | −1.42 / −0.74 | 0.78 / 0.74 (0.97 / 0.95) | 35 / 91 | 31 / 86 | 78 / 100 |
| 1000 S2 0.5 / 1 | −1.75 / −0.74 | 0.74 / 0.74 (0.92 / 0.89) | 37 / 79 | 30 / 79 | 83 / 96 |
| 1000 S3 0.5 / 1 | −2.18 / −0.70 | 0.65 / 0.77 (0.80 / 0.76) | 22 / 90 | 18 / 87 | 77 / 99 |
| 1000 S4 0.5 / 1 | −4.12 / −0.70 | 0.18 / 0.77 (0.40 / 0.30) | 7 / 81 | 1 / 77 | 47 / 100 |
| 1000 S5 0.5 / 1 | **−23.03 / −9.60** | **0.00014 / 0.054** (0.95 / 0.86) | 0 / 14 | 0 / 15 | **1 / 30** |
| 1000 S6 0.5 / 1 | −2.54 / −0.68 | 0.58 / 0.78 (0.77 / 0.70) | 22 / 88 | 14 / 84 | 70 / 99 |

Each cell has 100 fits; entries are c = 0.5 / c = 1.

- **At c = 1, outside S5,** the backfit start is favourable in 96–100 of 100 fits per cell. Its mode is S₀ in 79–91, and
  the median π₀(S₀) is 10^{−0.6}–10^{−0.75}: the start essentially lands on S₀.
- **At c = 0.5 the picture is graded.** p = 500 S1/S2/S3/S6 are 94–100 favourable. p = 1,000 is 70–83. S4 is 74 and 47,
  with mode = S₀ in only 9 and 7.
- **S5 (global equicorrelation 0.3) is where backfit does not work.** It is favourable in 1–44 of 100, with mode = S₀
  in 0–23. It is also the only scenario where the backfit mode carries ≥ 10 extras (6–19 per 100). This matches O-DILUTE §9
  ("weak in S5 … 10^{−4.6} to 10^{−19}").

### 3.3 What backfit costs: π₀(R₂)

Pooled π₀(R₂) falls only modestly (0.81 → 0.71), but the loss is concentrated where it matters:
- In S5, π₀(R₂) collapses from 0.86–0.95 under v3 to 0.0001–0.33. The backfit start in S5 is neither on S₀ nor near
  it: the median mode has 7–12 truths plus 0–3 extras.
- In S4 at p = 1,000, c = 0.5, it falls from 0.40 to 0.18.
- In the 565 fits the study got wrong (posterior misses), median π₀(R₂) falls from 0.77 to 0.47 (`extra_tables.md` (c)).

T38(b)'s eligibility premise is π₀(R_d) ≥ b_n, which O-DILUTE showed holds for v3 at the study size. For backfit tables
it would hold in most cells but **fail visibly in S5**. So backfit is not a pure improvement of the start law. It trades
near-truth mass for exact-truth mass, and the trade goes badly in S5.

*(Sections 3.4–5 follow.)*
