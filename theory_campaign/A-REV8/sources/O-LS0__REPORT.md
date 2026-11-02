# O-LS0: REPORT. LS0 (production local search from the start mode S̃₀) on the 2,400 study fits

Run of 2026-11-02, branch `theory/O-LS0`. The compute was done by the original O-LS0 agent (jobs A and B on Owls, finished
rc = 0). That agent was cancelled by a T3 restart before it wrote anything up. This report was written by O-LS0-WRAP,
which only **aggregated** the stored per-fit records: it reran no fits and made no engine calls. Scripts are in
`scripts/`, small tables in `results/`. The per-fit CSVs are outside git (see §8).

Everything below is post hoc: LS0 was run on the side and its scored models were paired with the production ledger. It
is not a redeploy. Nothing here is reviewed.

## 1. Headline

1. **Coverage is complete.** LS0 ran on all **2,400 fits**: 1,200 regenerated datasets (p ∈ {500, 1000} × S1–S6 ×
   r = 1..100) × 2 scales, with 0 errors. The lattice subsample covers r = 1..20 per cell (480 fits), and its D_S
   check ran on the 297 fits with |Lat(S̃₀)| ≤ 1024. Job B reproduced job A's LS0 output exactly: 0 of 11 fields
   differ across 480 fits.
2. **LS0 does not change a single study outcome.** Each fit was paired with the production per-fit ledger (S-ELS,
   2,394 completed fits). LS0's best-scored model **never beats the production HPM**: 0 / 2,394. The smallest margin
   is 0.002 nats, while the two data copies agree on F(S₀) to 5·10⁻⁸. Exact recovery with LS0 equals exact recovery
   without it in every cell:
   - **1,119 / 1,200 at c = 1**;
   - **710 / 1,200 at c = 0.5**;
   - gain 0, harm 0.

   A gain was impossible from the start, because production has 0 search misses (S-ELS: every miss has F(S₀) < F(Ŝ)).
3. **It is safe on these data, and it can only move the HPM uphill.**
   - LS0 does find models better than S₀: 55 fits at c = 1 and 358 at c = 0.5. Every one of those fits is already a
     production posterior miss, and production had found a model at least as good.
   - In the 1,829 production-exact fits, LS0's endpoint and best model never beat S₀ (0 / 1,829).
   - The structural reason: "S₀ is not a flip/swap local maximum" implies a production miss, with 0 exceptions in
     559 fits.
4. **On its own, LS0 is weaker than the sampler.**
   - It scores S₀ in 1,087 fits (c = 1) and 796 fits (c = 0.5), and certifies it in 918 and 447.
   - Its own best model is S₀ in 1,032 and 553 fits, against production's 1,119 and 710.
   - It is an add-on, not a replacement.
5. **LS0 is cheap.** Its median cost is 0.17 s (p = 500) and 0.37 s (p = 1000), which is about 5·10⁴ and 1.1·10⁵
   score evaluations. That is under 0.1% of a production fit, whose median is 400–2,200 s.
6. **The T38(b1) premises mostly fail at n = 200, as W4-T38FULL §7 predicted; the observed outcomes contradict none
   of its implications.**
   - (M1), π₀(S̃₀) > ½, holds in 18 of 2,400 fits.
   - (M2), D_S on all of Lat(S̃₀), holds in 17 of 168 checked fits (c = 1) and 1 of 129 (c = 0.5).
   - (M3), λ_min > 0, holds everywhere: the minimum is 0.056.
   - The cap ℓ ≥ Φ(S̃₀) − 1 holds in 1,968 of 2,400 fits.
   - Lemma LS-score's deterministic implication (D_S on Lat ∩ {Φ ≥ 2} and the cap ⇒ S₀ scored) held in all
     18 fits that met its premise. LS0 succeeds far more often than its premises hold.
7. **What this means for the decision.** LS0 passes the "still performs well" half of the investment rule as strongly
   as a check can: the results are identical on the full study, not just on a pilot. Its value is purely theoretical:
   - it is the method change behind W4-T38FULL's (b1);
   - it is the only route that has a p ≫ n candidate (W3-PXN LH-iid, unverified).

   O-BGIBBS's BG3 now claims the masked theorem without LS0, but only on LH with p fixed, and its key
   proposition (LH-lock) is a PROOF SKETCH. So LS0 is no longer the only route for p fixed. It remains the only
   candidate route for p ≫ n (§7).

## 2. Coverage and data

| run | what | fits | status |
|---|---|---|---|
| **Job A** (`~/ls0_work/full/`) | spec `full`: all 1,200 datasets × {c100, c050}, 2 shards in one `owls_run -j 2` job | **2,400 / 2,400** RDS, 0 ERROR lines | first launch 12:27, killed at 12:37 (rc 143); relaunched 12:39 and resumed (files written atomically, skip-if-present); done 12:54, rc 0; 0.74 CPU-h |
| **Job B** (`~/ls0_work/full_lat/`) | `tasks_r1_20.csv`: r = 1..20 per p × scenario × scale (the **lattice subsample**), `LS0_LAT_MAX = 1024` | **480 / 480**, 0 ERROR | 12:54–13:38, rc 0; 433 fits computed, 47 r = 1 fits pre-seeded from the pilot (same settings); about 1.3 CPU-h (mostly lattice scans) |
| `agg_test/` | an earlier test aggregation of the 24-fit pilot | — | superseded, not used |

- **What is missing.**
  - No LS0 fits are missing.
  - The D_S lattice check exists only for r ≤ 20, and only where |Lat| = 2^{missed + extras} ≤ 1024: 297 of 480 fits
    (168 at c = 1, 129 at c = 0.5). This sample is biased towards starts closer to S₀.
  - Job A's own lattice columns are mixed: the killed first launch ran with cap 1024 and the relaunch with no lattice
    check. 20_aggregate.R therefore takes every lattice column from job B.
  - No production SMC fits were rerun with LS0 integrated (`ls0_enable_integrated` exists in `ls0_core.R` but was not
    used).
- **Data.**
  - `00_regen_data.sh` regenerated the 1,200 datasets on Owls with the repository generator, unchanged, pinned to
    FlexiBLAS OPENBLAS-OPENMP with 1 thread.
  - Gate-G2 checks: all 12 cells pass (`~/ls0_work/g2_1t.out`; at p = 500 the Oct-14 `/scratch` comparison was
    removed).
  - Byte-level hash check (`results/data_hash_check.csv`): the two Owls dev inputs are reproduced byte for byte. The
    NOTS dev and production inputs are **not**, because of last-bit BLAS differences between Owls and NOTS.
  - **What makes the pairing valid anyway:**
    - S₀ is identical in all 2,400 pairs;
    - F(S₀) on the Owls copy equals the production scorer's F(S₀) to ≤ 5·10⁻⁸. That is the rounding of the
      10-significant-digit CSV;
    - every cross-data comparison used has a margin ≥ 0.002. The tolerance is set at 5·10⁻⁵, and no comparison was
      undetermined.

    One limit remains: LS0's path on the NOTS bits could differ from its path on the Owls bits only at exact ties
    below 10⁻⁸. Such ties were not observed and cannot be excluded.
- **Production reference.**
  - Cell counts come from `Results/SMC_BVS_v3_production/p{0500,1000}/exact_recovery_long.csv` (SMCBVS, hpm, primary).
    20_aggregate.R reads them. The per-fit pairing reproduces them exactly: 1,119 and 710.
  - The per-fit pairing uses `theory/S-ELS` at 90423b1, file `theory_campaign/S-ELS/tables/ledger_per_fit.csv` (blob
    de03d21e). It gives Ŝ and F(Ŝ) per fit, F(S₀) from the fit's own scorer, and the class.

## 3. What a per-fit record contains

`scripts/10_ls0_fit.R` writes one RDS per fit: `row` (a one-row data frame) plus `detail`. Everything is computed by the
**production v3 core**: `ls0_core.R` copies `Scripts/SMC_BVS/core`, checks every file against the sha256 in
`source_manifest.json`, and appends only the test exports in `ls0_exports.cpp`. The fields:

- **Setup, exactly as in `v3_fit`.** `v3_preprocess` → `v3_context` → `v3_setup`, with the budgets K, B and
  ℓ = `v3_budgets(n, p)$ell`. Here ℓ = 10 at p = 500 and **ℓ = 11 at p = 1000**. (S-ELS §2 says ℓ = 10 at both p;
  that is a minor inaccuracy there.)
- **Start mode.** S̃₀ = the exact argmax of π₀ (`cpp_ls0_start_mode`, a max-plus convolution over block tables). It
  was unique in all 2,400 fits, so the HPM tie rule for argmax π₀ was never needed.
- **Start masses.** log π₀(S̃₀), log π₀(S₀), and log π₀(𝓡_d) for d = 0, 1, 2, all exact.
- **LS0.** `Engine::local_search(S̃₀, ℓ, emit_centre = TRUE)`. Recorded:
  - the termination (`no_improvement` = certified local maximum; `move_limit`), the moves, the accepted path, and
    every scanned centre;
  - `scored_S0`: S₀ is within one flip/swap of a scanned centre;
  - `certified_S0`: the search ended at S₀ certified;
  - `best_eq_S0`;
  - F(S₀), F(endpoint), F(best) = the HPM-rule best over LS0's scored models;
  - `endpoint_beats_S0` and `best_beats_S0`;
  - the path's Φ and maximum extras, giving path ⊂ 𝓡_d and path ⊂ Lat(S̃₀);
  - move types: +T and −N are progress, +N and −T are not.
- **One scan at S₀.** Whether S₀ is a strict flip/swap local maximum ((L)), and if not, the type of its best neighbour.
- **Lattice (job B only).** One scan at every S ∈ Lat(S̃₀) with Φ(S) ≥ 2. A state passes D_S when its best neighbour
  is a progress move. Failures are recorded by type.
- **(M3).** λ_min of the correlation matrix on S̃₀ ∪ S₀.
- **Timings.** Setup, mode, LS0, scan and lattice.

The R0/R1/R2 convention is 𝓡_d = {U ∪ P : U ⊆ S₀, P ⊆ S₀ᶜ, |P| ≤ d}, as in `00_COMMON.md` and S-ELS.

## 4. Tables (per p × scenario × scale)

Generated by `scripts/22_report_tables.py` → `results/report_tables.md`. The working tables of 20_aggregate.R (start
masses, the lattice failure types, cost) are in `results/tables.md`.

Note: the "harm possible" column of `tables.md` (3 fits at c = 0.5) is the cell-level upper bound. The per-fit
pairing in (b) resolves it to 0.

### (a) LS0 recovery rate, compared with production

- "prod HPM = S₀" is the production exact recovery: S-ELS per fit, equal to `exact_recovery_long.csv`.
- "prod + LS0" is the HPM after taking the union of the production ledger with LS0's scored models, under the
  production tie rule.

**(a) Recovery, scale c100 (c = 1), 100 fits per cell**

| cell | prod HPM = S₀ | LS0 scored S₀ | LS0 certified S₀ | LS0 best = S₀ (LS0 alone) | prod + LS0 HPM = S₀ |
|---|---|---|---|---|---|
| p500 S1 | 95 | 100 | 93 | 95 | 95 |
| p500 S2 | 96 | 99 | 92 | 95 | 96 |
| p500 S3 | 94 | 97 | 86 | 91 | 94 |
| p500 S4 | 91 | 77 | 64 | 73 | 91 |
| p500 S5 | 89 | 65 | 33 | 64 | 89 |
| p500 S6 | 94 | 95 | 83 | 90 | 94 |
| p1000 S1 | 95 | 99 | 93 | 94 | 95 |
| p1000 S2 | 95 | 98 | 90 | 93 | 95 |
| p1000 S3 | 97 | 99 | 94 | 97 | 97 |
| p1000 S4 | 93 | 81 | 60 | 76 | 93 |
| p1000 S5 | 84 | 86 | 47 | 77 | 84 |
| p1000 S6 | 96 | 91 | 83 | 87 | 96 |
| **all** | 1119 | 1087 | 918 | 1032 | 1119 |

**(a) Recovery, scale c050 (c = 0.5), 100 fits per cell**

| cell | prod HPM = S₀ | LS0 scored S₀ | LS0 certified S₀ | LS0 best = S₀ (LS0 alone) | prod + LS0 HPM = S₀ |
|---|---|---|---|---|---|
| p500 S1 | 79 | 95 | 66 | 78 | 79 |
| p500 S2 | 84 | 92 | 65 | 76 | 84 |
| p500 S3 | 64 | 84 | 40 | 54 | 64 |
| p500 S4 | 25 | 33 | 9 | 10 | 25 |
| p500 S5 | 59 | 25 | 5 | 18 | 59 |
| p500 S6 | 59 | 75 | 40 | 48 | 59 |
| p1000 S1 | 71 | 88 | 50 | 65 | 71 |
| p1000 S2 | 75 | 92 | 64 | 72 | 75 |
| p1000 S3 | 67 | 82 | 53 | 60 | 67 |
| p1000 S4 | 35 | 37 | 17 | 23 | 35 |
| p1000 S5 | 31 | 21 | 4 | 7 | 31 |
| p1000 S6 | 61 | 72 | 34 | 42 | 61 |
| **all** | 710 | 796 | 447 | 553 | 710 |

### (b) Could LS0 hurt exact recovery?

LS0 hurts a fit if it scores a model that beats S₀ under the HPM rule in a fit where the production HPM is S₀. Adding
LS0 can only raise F(Ŝ). So any change it makes is a move to a higher-posterior model, and a "harm" would be a
posterior miss that the production run happened not to find. The table reports:
- LS0's endpoint with F > F(S₀) that is not S₀, as the brief asks;
- the stronger "LS0 best beats S₀";
- both restricted to the production-exact fits.

"S₀ not a flip/swap local max" is the one-scan check at S₀. It implies a production miss, with 0 exceptions in 559
fits, because the production final local search scans the neighbours of its HPM.

**(b) Could LS0 hurt?, scale c100 (c = 1), 100 fits per cell**

| cell | LS0 endpoint F > F(S₀), ≠ S₀ | … in prod-exact fits | LS0 best beats S₀ | … in prod-exact fits (harm) | LS0 best = prod HPM | LS0 changes prod HPM | gain | S₀ not a flip/swap local max | prod misses |
|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 5 | 0 | 5 | 0 | 100 | 0 | 0 | 5 | 5 |
| p500 S2 | 4 | 0 | 4 | 0 | 99 | 0 | 0 | 4 | 4 |
| p500 S3 | 6 | 0 | 6 | 0 | 97 | 0 | 0 | 6 | 6 |
| p500 S4 | 4 | 0 | 4 | 0 | 77 | 0 | 0 | 9 | 9 |
| p500 S5 | 1 | 0 | 1 | 0 | 61 | 0 | 0 | 9 | 11 |
| p500 S6 | 5 | 0 | 5 | 0 | 94 | 0 | 0 | 6 | 6 |
| p1000 S1 | 5 | 0 | 5 | 0 | 99 | 0 | 0 | 5 | 5 |
| p1000 S2 | 5 | 0 | 5 | 0 | 98 | 0 | 0 | 5 | 5 |
| p1000 S3 | 2 | 0 | 2 | 0 | 99 | 0 | 0 | 2 | 3 |
| p1000 S4 | 5 | 0 | 5 | 0 | 80 | 0 | 0 | 7 | 7 |
| p1000 S5 | 9 | 0 | 9 | 0 | 83 | 0 | 0 | 14 | 16 |
| p1000 S6 | 4 | 0 | 4 | 0 | 91 | 0 | 0 | 4 | 4 |
| **all** | 55 | 0 | 55 | 0 | 1078 | 0 | 0 | 76 | 81 |

**(b) Could LS0 hurt?, scale c050 (c = 0.5), 100 fits per cell**

| cell | LS0 endpoint F > F(S₀), ≠ S₀ | … in prod-exact fits | LS0 best beats S₀ | … in prod-exact fits (harm) | LS0 best = prod HPM | LS0 changes prod HPM | gain | S₀ not a flip/swap local max | prod misses |
|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 17 | 0 | 17 | 0 | 91 | 0 | 0 | 20 | 21 |
| p500 S2 | 16 | 0 | 16 | 0 | 92 | 0 | 0 | 16 | 16 |
| p500 S3 | 32 | 0 | 32 | 0 | 81 | 0 | 0 | 35 | 36 |
| p500 S4 | 49 | 0 | 49 | 0 | 51 | 0 | 0 | 75 | 75 |
| p500 S5 | 20 | 0 | 20 | 0 | 33 | 0 | 0 | 40 | 41 |
| p500 S6 | 37 | 0 | 37 | 0 | 80 | 0 | 0 | 40 | 41 |
| p1000 S1 | 25 | 0 | 25 | 0 | 87 | 0 | 0 | 28 | 29 |
| p1000 S2 | 22 | 0 | 22 | 0 | 93 | 0 | 0 | 25 | 25 |
| p1000 S3 | 29 | 0 | 29 | 0 | 87 | 0 | 0 | 33 | 33 |
| p1000 S4 | 37 | 0 | 37 | 0 | 50 | 0 | 0 | 64 | 65 |
| p1000 S5 | 40 | 0 | 40 | 0 | 39 | 0 | 0 | 68 | 69 |
| p1000 S6 | 34 | 0 | 34 | 0 | 73 | 0 | 0 | 39 | 39 |
| **all** | 358 | 0 | 358 | 0 | 857 | 0 | 0 | 483 | 490 |

### (c) Does the path stay in 𝓡_d, and does it certify? (TD′ consistency)

- "progress-only path" means every accepted move lowers Φ.
- "hit move cap" means termination was `move_limit`. Every other run ended in a certified local maximum, which is not
  necessarily S₀.
- The "miss" columns classify the fits where LS0 did **not** score S₀:
  - S₀ is not a local maximum;
  - S̃₀ is itself a strict local maximum (0 moves; mostly S5 with S̃₀ = ∅);
  - a progress-only path ran out of ℓ;
  - the path took a non-progress move;
  - other (including 3 fits at c = 0.5 where LS0 found a better model and S₀ was a local maximum).

**(c) Path in 𝓡_d and certification, scale c100 (c = 1), 100 fits per cell**

| cell | S̃₀∈𝓡₀ | S̃₀∈𝓡₂ | path ⊂ 𝓡₀ | path ⊂ 𝓡₁ | path ⊂ 𝓡₂ | progress-only path | path ⊂ Lat(S̃₀) | hit move cap | endpoint certified (any model) | P(cert S₀ | scored S₀) | miss: S₀ not LM | miss: 0 moves | miss: cap | miss: non-progress | miss: other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 94 | 100 | 89 | 100 | 100 | 92 | 92 | 2 | 98 | 0.93 | 0 | 0 | 0 | 0 | 0 |
| p500 S2 | 65 | 99 | 62 | 95 | 99 | 92 | 92 | 6 | 94 | 0.93 | 0 | 0 | 1 | 0 | 0 |
| p500 S3 | 48 | 100 | 43 | 84 | 100 | 86 | 86 | 10 | 90 | 0.89 | 0 | 0 | 2 | 1 | 0 |
| p500 S4 | 17 | 80 | 10 | 30 | 60 | 41 | 41 | 32 | 68 | 0.83 | 5 | 0 | 0 | 18 | 0 |
| p500 S5 | 76 | 99 | 70 | 96 | 99 | 50 | 55 | 61 | 39 | 0.51 | 5 | 5 | 13 | 12 | 0 |
| p500 S6 | 37 | 93 | 33 | 74 | 92 | 84 | 84 | 13 | 87 | 0.87 | 0 | 0 | 2 | 3 | 0 |
| p1000 S1 | 93 | 100 | 89 | 99 | 100 | 95 | 95 | 3 | 97 | 0.94 | 0 | 0 | 1 | 0 | 0 |
| p1000 S2 | 78 | 100 | 73 | 98 | 100 | 90 | 91 | 4 | 96 | 0.92 | 0 | 1 | 1 | 0 | 0 |
| p1000 S3 | 56 | 96 | 50 | 89 | 96 | 87 | 88 | 3 | 97 | 0.95 | 0 | 1 | 0 | 0 | 0 |
| p1000 S4 | 25 | 85 | 15 | 32 | 67 | 44 | 44 | 35 | 65 | 0.74 | 1 | 0 | 2 | 16 | 0 |
| p1000 S5 | 80 | 95 | 71 | 91 | 95 | 53 | 56 | 43 | 57 | 0.55 | 2 | 2 | 7 | 3 | 0 |
| p1000 S6 | 36 | 97 | 28 | 75 | 95 | 79 | 79 | 15 | 85 | 0.91 | 0 | 0 | 2 | 7 | 0 |
| **all** | 705 | 1144 | 633 | 963 | 1103 | 893 | 903 | 227 | 973 | 0.84 | 13 | 9 | 31 | 60 | 0 |

**(c) Path in 𝓡_d and certification, scale c050 (c = 0.5), 100 fits per cell**

| cell | S̃₀∈𝓡₀ | S̃₀∈𝓡₂ | path ⊂ 𝓡₀ | path ⊂ 𝓡₁ | path ⊂ 𝓡₂ | progress-only path | path ⊂ Lat(S̃₀) | hit move cap | endpoint certified (any model) | P(cert S₀ | scored S₀) | miss: S₀ not LM | miss: 0 moves | miss: cap | miss: non-progress | miss: other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 96 | 100 | 86 | 99 | 100 | 86 | 86 | 19 | 81 | 0.69 | 0 | 0 | 3 | 2 | 0 |
| p500 S2 | 75 | 100 | 65 | 96 | 100 | 81 | 82 | 22 | 78 | 0.71 | 0 | 0 | 5 | 3 | 0 |
| p500 S3 | 59 | 100 | 25 | 80 | 96 | 49 | 49 | 31 | 69 | 0.48 | 3 | 0 | 3 | 9 | 1 |
| p500 S4 | 19 | 81 | 2 | 14 | 42 | 11 | 11 | 54 | 46 | 0.27 | 52 | 0 | 1 | 14 | 0 |
| p500 S5 | 80 | 99 | 52 | 91 | 99 | 32 | 42 | 61 | 39 | 0.20 | 31 | 8 | 14 | 21 | 1 |
| p500 S6 | 45 | 98 | 25 | 70 | 93 | 51 | 51 | 32 | 68 | 0.53 | 13 | 0 | 6 | 5 | 1 |
| p1000 S1 | 96 | 100 | 89 | 100 | 100 | 82 | 85 | 22 | 78 | 0.57 | 4 | 1 | 3 | 2 | 2 |
| p1000 S2 | 83 | 100 | 70 | 99 | 100 | 79 | 81 | 16 | 84 | 0.70 | 5 | 0 | 1 | 2 | 0 |
| p1000 S3 | 61 | 98 | 35 | 81 | 97 | 54 | 56 | 15 | 85 | 0.65 | 10 | 1 | 1 | 4 | 2 |
| p1000 S4 | 29 | 86 | 3 | 19 | 46 | 12 | 12 | 56 | 44 | 0.46 | 50 | 0 | 0 | 13 | 0 |
| p1000 S5 | 86 | 97 | 57 | 88 | 97 | 32 | 43 | 31 | 69 | 0.19 | 52 | 3 | 3 | 16 | 5 |
| p1000 S6 | 47 | 98 | 24 | 65 | 93 | 40 | 40 | 34 | 66 | 0.47 | 8 | 0 | 4 | 16 | 0 |
| **all** | 776 | 1157 | 533 | 902 | 1063 | 609 | 638 | 393 | 807 | 0.56 | 228 | 13 | 44 | 107 | 12 |

### (d) The empirical T38 premises

T38(b1) (W4-T38FULL) needs the following, with S° deterministic and Φ(S°) bounded:
- (M1) P(π₀(S°) > ½) → 1;
- (M2) POP-LAT, i.e. D_S on Lat(S°) ∩ {Φ ≥ 2} with a margin;
- (M3) λ_min(R_{S°∪S₀}) bounded below;
- the cap ℓ ≥ Φ(S°) − 1 (Lemma LS-score);
- OP-LS0.

The empirical stand-in here is S° = S̃₀. (M2) is checked in its no-margin form on the lattice subsample.

**(d) Empirical T38(b1) premises at S° = S̃₀, scale c100 (c = 1), 100 fits per cell**

| cell | med Φ(S̃₀) | ℓ ≥ Φ(S̃₀)−1 | (M1) π₀(S̃₀) > ½ | med π₀(S̃₀) | med π₀(𝓡₂) = b_n | med log₁₀π₀(S₀) | (M2) lattice fits checked | (M2) D_S on all of Lat | Φ=2 states failing D_S | (M3) min λ_min |
|---|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 8 | 100 | 0 | 0.108 | 0.95 | -12.4 | 20 | 1 | 0.00 | 0.48 |
| p500 S2 | 8 | 99 | 0 | 0.055 | 0.84 | -12.7 | 20 | 4 | 0.00 | 0.34 |
| p500 S3 | 9 | 93 | 0 | 0.038 | 0.69 | -13.2 | 15 | 3 | 0.00 | 0.19 |
| p500 S4 | 11 | 66 | 0 | 0.008 | 0.25 | -13.5 | 9 | 0 | 0.00 | 0.09 |
| p500 S5 | 11 | 68 | 0 | 0.114 | 0.88 | -19.6 | 9 | 0 | 0.00 | 0.21 |
| p500 S6 | 9 | 79 | 0 | 0.033 | 0.65 | -12.8 | 15 | 3 | 0.00 | 0.06 |
| p1000 S1 | 9 | 98 | 0 | 0.123 | 0.95 | -14.5 | 17 | 1 | 0.01 | 0.49 |
| p1000 S2 | 9 | 97 | 0 | 0.070 | 0.89 | -14.6 | 18 | 3 | 0.00 | 0.31 |
| p1000 S3 | 10 | 97 | 0 | 0.046 | 0.76 | -15.1 | 17 | 1 | 0.00 | 0.19 |
| p1000 S4 | 11 | 69 | 0 | 0.011 | 0.30 | -16.3 | 10 | 0 | 0.01 | 0.09 |
| p1000 S5 | 11 | 82 | 4 | 0.096 | 0.86 | -23.4 | 5 | 0 | 0.11 | 0.19 |
| p1000 S6 | 10 | 90 | 0 | 0.037 | 0.73 | -15.0 | 13 | 1 | 0.00 | 0.06 |
| **all** |  | 1038 | 4 |  |  |  | 168 | 17 |  | 0.06 |

**(d) Empirical T38(b1) premises at S° = S̃₀, scale c050 (c = 0.5), 100 fits per cell**

| cell | med Φ(S̃₀) | ℓ ≥ Φ(S̃₀)−1 | (M1) π₀(S̃₀) > ½ | med π₀(S̃₀) | med π₀(𝓡₂) = b_n | med log₁₀π₀(S₀) | (M2) lattice fits checked | (M2) D_S on all of Lat | Φ=2 states failing D_S | (M3) min λ_min |
|---|---|---|---|---|---|---|---|---|---|---|
| p500 S1 | 8 | 95 | 0 | 0.100 | 0.96 | -14.0 | 15 | 0 | 0.33 | 0.48 |
| p500 S2 | 9 | 92 | 0 | 0.058 | 0.89 | -14.3 | 17 | 0 | 0.18 | 0.34 |
| p500 S3 | 10 | 84 | 0 | 0.045 | 0.74 | -15.1 | 14 | 1 | 0.13 | 0.19 |
| p500 S4 | 11.5 | 50 | 0 | 0.010 | 0.28 | -15.4 | 6 | 0 | 0.17 | 0.10 |
| p500 S5 | 12 | 48 | 5 | 0.139 | 0.93 | -21.6 | 4 | 0 | 0.53 | 0.22 |
| p500 S6 | 10 | 71 | 0 | 0.045 | 0.70 | -14.8 | 15 | 0 | 0.24 | 0.07 |
| p1000 S1 | 10 | 96 | 0 | 0.124 | 0.97 | -16.8 | 14 | 0 | 0.32 | 0.53 |
| p1000 S2 | 10 | 96 | 1 | 0.089 | 0.92 | -16.7 | 14 | 0 | 0.28 | 0.37 |
| p1000 S3 | 10 | 96 | 0 | 0.064 | 0.80 | -17.1 | 13 | 0 | 0.29 | 0.19 |
| p1000 S4 | 12 | 58 | 0 | 0.017 | 0.40 | -18.5 | 9 | 0 | 0.37 | 0.08 |
| p1000 S5 | 12 | 62 | 8 | 0.184 | 0.94 | -25.6 | 1 | 0 | 1.00 | 0.18 |
| p1000 S6 | 11 | 82 | 0 | 0.056 | 0.77 | -17.3 | 7 | 0 | 0.23 | 0.06 |
| **all** |  | 930 | 14 |  |  |  | 129 | 1 |  | 0.06 |

## 5. Reading the tables

**(a) and (b): study outcomes.**
- The two columns "prod HPM = S₀" and "prod + LS0 HPM = S₀" are identical in all 24 cells.
- In 1,930 of the 2,394 completed fits, LS0's best model *is* the production HPM. In the other 464, it is strictly
  worse than the production HPM. (Column "LS0 best = prod HPM" in (b) also counts the 6 stopped fits against their
  partial HPM, which gives 1,935.)
- Where LS0 alone beats production on S₀ (for example c = 0.5, p500 S3: 84 scored against 64 exact), it does not
  change the HPM. Production's HPM already beats S₀ there, and it does so by at least 0.0049 nats (S-ELS).
- **LS0 cannot repair posterior misses, and the study has no other kind** (W4-T38FULL §7, S-ELS §1). These data
  confirm it on all 2,400 fits.
- One minor point. In 3 of the 6 resource-limit fits (all S5, c = 1), LS0 certifies S₀. Under the headline convention
  those fits have no output, so this is not a gain unless the stopped-fit convention changes. Production's partial HPM
  in those same 3 fits was already S₀ (S-ELS §3; checked per fit).

**(c): the path and TD′.**
- Lemma LS-score's implication was checked wherever its premise could be: D_S on all of Lat(S̃₀) ∩ {Φ ≥ 2}, plus
  ℓ ≥ Φ(S̃₀) − 1.
  - 17 fits at c = 1 and 1 at c = 0.5 meet the premise. In all 18, LS0 scored S₀, certified it, took a progress-only
    path and stayed in Lat(S̃₀).
  - No counterexample to the lemma or to the engine's scan-before-limit fact.
- The premise is far from necessary. D_S failed somewhere in 151 checked fits at c = 1 and 128 at c = 0.5, and LS0
  still scored S₀ in 149 and 112 of them.
- At the failing lattice states, the best neighbour is almost always a **truth-for-truth swap**: swT>T in 19,222 of
  20,164 failing states at c = 1, and 43,738 of 46,043 at c = 0.5. That is a size-neutral move that leaves Φ
  unchanged. It wastes moves, which is why "non-progress" and "cap" dominate the search failures (60 + 31 at c = 1,
  107 + 44 at c = 0.5).
- Paths mostly stay in 𝓡₂:
  - c = 1: S̃₀ ∈ 𝓡₂ in 1,144 fits, path ⊂ 𝓡₂ in 1,103;
  - c = 0.5: 1,157 and 1,063;
  - S4 is the exception (path ⊂ 𝓡₂ in 60, 67, 42 and 46 of 100). There S̃₀ carries the most extras (mean ≈ 1.5).
- Certification given scoring is 0.84 at c = 1 and 0.56 at c = 0.5. The rest splits into two causes:
  - S₀ is not a strict local maximum (63 and 255 fits);
  - S₀ was scored but the cap was hit before the search settled (106 and 94 fits).
- For comparison, the production final search made 0 moves in all 2,394 completed fits (S-ELS). LS0 from S̃₀ makes
  about 9 moves on average and hits the cap in 227 and 393 fits. At n = 200 it is a real search, not a certificate.

**(d): the T38 premises at n = 200.**
- **(M1) fails almost everywhere.** π₀(S̃₀) > ½ in 4 fits (c = 1) and 14 (c = 0.5), almost all S5 with S̃₀ of size
  0–3. The cell medians of π₀(S̃₀) are 0.008–0.18.
- The near-truth mass b_n = π₀(𝓡₂) is substantial: medians 0.25–0.97, lowest in S4. That is the T22(i) delivery
  input. LS0's deterministic centre, however, needs (M1) or a replacement for it.
- **(M2) (D_S on all of the lattice) fails in about 90% of checked fits at c = 1 and in all but one at c = 0.5.** This
  is in the biased subsample with |Lat| ≤ 1024.
- **(M3) holds:** λ_min ≥ 0.056, lowest in S4 and S6.
- **The cap ℓ ≥ Φ(S̃₀) − 1 fails in 162 fits (c = 1) and 270 (c = 0.5).** The median Φ(S̃₀) is 8–12 against
  ℓ = 10–11, the start missing 8–12 of the 14 truths.
- **So the study sits outside T38(b1)'s hypotheses**, which is exactly W4-T38FULL's own disclosure ("T38 explains the
  mechanism, not the n = 200 numbers"; dilution masking per W3-PXN Prop. W).
- **Where the premises do hold, the conclusion holds** (the 18 fits above). Where they fail, LS0 usually still scores
  S₀ (1,087 and 796 fits).
- This is consistent with W3-PXN's interim study sample (113/128 scored when |S̃₀ Δ S₀| ≤ ℓ + 1). On the full study,
  S̃₀ ∈ 𝓡₂ together with the cap gives "scored" in 1,000 of 1,023 fits (c = 1) and 754 of 928 (c = 0.5).

## 6. Method-change assessment (investment rule, `Docs/THEORY_PRIORITIES.md` §4)

The rule is: change the method and rerun *only if* both of these hold:
1. with the change, all or most of the key results are provable;
2. a pilot gives strong evidence that the method still performs well.

**Does LS0 change study outcomes?** No. The per-fit pairing over all 2,400 fits shows that exact recovery, the
reported HPM and the miss classes are all unchanged: LS0 changes the HPM in 0 of 2,394 completed fits. The paper's
tables would be byte-identical in their recovery columns.
- The only new outputs are LS0's own records: S̃₀, its path, and whether it certified.
- The runtime overhead is under 1 s per fit.

**Is LS0 safe?**
- **Empirically, yes.** It caused 0 harm in 1,829 production-exact fits, at both scales.
- **Structurally**, it adds scored models to the ledger and so can only raise F(Ŝ). It changes Ŝ only when it finds a
  strictly higher-posterior model, which is the HPM rule doing its job. It cannot lower recovery through any other
  channel. As integrated in `ls0_core.R`, LS0 runs after the final local search on the same ledger, and SMC dynamics
  are untouched.
- **The one way it could "hurt"** is by revealing a posterior miss that production happened not to score. That never
  occurred here: production's sampler always found the better model first.
- **This does not depend on a pilot.** It holds on the full study, not on a sample.

**Requirement (2) is therefore met as strongly as a check can meet it.** One caveat: the data are the Owls
regeneration, which agrees with production to the printed precision of F (§2), not to the bit.

**What does LS0 buy theoretically?** This is requirement (1).
- **W4-T38FULL.** (b1) is "PROVED-UNDER (M1)–(M3) + OP-LS0".
  - It is fully proved, with no open statistical input, on LH exact Gram with p < n. That is a new, same-family-checked
    result, still awaiting cross-family review.
  - Its §1 item 6 says: "Without LS0, the paper has no masked-regime consistency theorem whose premises are all
    proved on an explicit family."
  - LS0 also needs `emit_centre = true`, which this run used, and the HPM tie rule for argmax π₀, which never bound
    here (the mode was unique in all 2,400 fits).
- **W3-PXN.** It claims the p ≫ n family LH-iid, with S̃₀ = S° and the TD′ lattice condition, so that LS0 scores and
  certifies S₀ in c moves. That is a PROVED candidate, **unverified**. It is the only p ≫ n masked candidate, and it
  uses LS0. Its no-tweak route is PROVED only for c = 1 (with the NB step a PROOF SKETCH), and is OPEN for c ≥ 2.
- **O-BGIBBS** (theory/O-BGIBBS at 55679ee, unreviewed).
  - It claims Theorem BG3, PROVED: the final run alone discovers S₀ on LH for every fixed c, **without LS0**.
  - Its premises on LH come from Proposition LH-lock, which is a **PROOF SKETCH and holds for p fixed only**. For
    p → ∞ the gap uniformity is a CONJECTURE.
  - If verified, it removes LS0's necessity for the p-fixed LH theorem, the same family as W4-T38FULL (b1-LH).
  - It does not cover p ≫ n, and it does not cover posterior-barrier designs. On those designs O-BGIBBS records a
    finite-n counterexample to every local kernel, LS0 included.

**Net assessment for Felipe's conditional approval.**
1. **Pending check: passed.** LS0 is outcome-neutral and harmless on all 2,400 study fits, and costs under 0.1%.
   Nothing in these data argues against adopting it.
2. **No rerun is needed to report LS0-augmented results.** The production fits plus this post hoc LS0 run already are
   those results, because LS0 never changed the HPM. If LS0 is adopted, the only extra work is labelling it and
   storing LS0's per-fit records. A redeploy carrying LS0 is warranted only if it is bundled with other changes ("one
   redeploy carries all changes").
3. **Its theoretical value is real, but conditional.**
   - Today LS0 is the dependency of the only fully proved masked theorem (W4-T38FULL, p < n).
   - It is also the dependency of the only p ≫ n candidate (W3-PXN).
   - If O-BGIBBS's LH-lock is verified, the p-fixed theorem no longer needs LS0. LS0's remaining unique contribution
     would then be the p ≫ n route (W3-PXN), which is not yet verified.
   - The honest framing for the paper: LS0 is a cheap deterministic step that leaves the reported results unchanged
     and makes a masked-regime eligibility argument provable. It does **not** improve recovery at n = 200, where every
     miss is a posterior miss.
4. **Not established here.**
   - These data cannot show that LS0 is the *only* route: (M1) fails at n = 200, so the data neither support nor
     refute any asymptotic route.
   - They also cannot show that integrating LS0 inside the engine reproduces the post hoc union: that would need an
     integrated test fit, which was not run under the no-engine rule. It is a small check for whoever implements the
     adoption.

## 7. Limits and honest caveats

- **Owls regeneration ≠ NOTS bits.** The pairing rests on identical S₀ and on F(S₀) agreeing to 5·10⁻⁸, with every
  compared margin ≥ 0.002. I did not score the production HPM on the Owls data, because that would need an engine
  call. So "LS0 never beats production" compares F(LS0 best) on Owls with F(Ŝ) on NOTS. The 5·10⁻⁸ agreement is
  measured on S₀ only.
- **The lattice D_S check** is a subsample (r ≤ 20), restricted to |Lat| ≤ 1024 (297 of 480 fits), and uses the
  no-margin form of D_S. (M2) proper needs a margin m_n ≫ √(log n/n), which was not computed.
- **(M1)** is evaluated at S° = S̃₀ (data-dependent). T38 needs a deterministic S°, so (d) is an empirical stand-in.
- **Fixes to the scripts.** `20_aggregate.R` had two bugs, fixed here:
  - each production file has rows for both p (zeros for the other p) plus "pooled" rows, which duplicated every cell
    in the merge;
  - fits with 0 LS0 moves fell into an NA failure class.

  `21_paired.R` and `22_report_tables.py` are new and aggregation-only.

## 8. Files and reproduction

- `scripts/00–02`: data regeneration and checks (original agent).
- `scripts/10_ls0_fit.R`, `11_run.R`, `12_run2_owls.sh`, `13_launch_job.sh`, `ls0_core.R`, `ls0_exports.cpp`: the LS0
  driver (original agent; jobs A and B used them unchanged, from worktree t3-de01d90c at 2471709).
- `scripts/20_aggregate.R` (fixed): `Rscript 20_aggregate.R ~/ls0_work/full results ~/ls0_work/full_lat`. Writes
  `results/cell_summary.csv`, `results/tables.md`, `results/determinism_check.txt` and `results/ls0_per_fit.csv`. The
  last is not in git; there is a copy in `~/ls0_work/agg_final/`, sha256 29cdf283….
- `scripts/21_paired.R` (new): `Rscript 21_paired.R ~/ls0_work/full ~/ls0_work/sels_ledger_per_fit.csv results`.
  - Input: the S-ELS ledger extracted from `theory/S-ELS` 90423b1.
  - Writes `results/paired_cell_summary.csv` and `results/paired_totals.txt`.
  - Also writes `results/paired_per_fit.csv`, not in git; there is a copy in `~/ls0_work/agg_final/`, sha256 f1f4fec8….
- `scripts/22_report_tables.py` (new): `python3 -I 22_report_tables.py results` writes `results/report_tables.md`.
- Every aggregation ran through `owls_run -j 1`, with no engine calls.
