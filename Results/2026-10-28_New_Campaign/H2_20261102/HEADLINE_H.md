# p ≫ n headline: does each method recover the true model? (PROD-H rerun, v2.2.1)

n = 200; p = 500 and 1000; scenarios S1–S6; 100 datasets per cell. The truth has 14 variables. A method "recovers" when its selected set equals the true set exactly. Failed fits count as misses.

**What changed from `analysis/H_existing_20261030/HEADLINE_H.md`:**
1. **SMC-BVS rows now come from the PROD-H rerun** (run `20261030T0934Z_prodH`, frozen code v2.2.1). Same core, seeds and datasets as the 2026-10-23 fits.
   - All 2,400 records match the 10-23 records on the 11 compared fields: Ẑ, the island Ẑ, HPM, F(HPM), the RB PIPs (pooled and per island), the MPM and the status (`repro/`).
   - The 6 stopped fits match too, including their unavailable (empty) fields.
   - Every available estimate reproduces exactly, with max |diff| = 0.
   - So the HPM and RB-PIP rows are unchanged.
2. **New row: MPM from the plain (non-Rao–Blackwellised) PIPs.**
3. **Lasso family headline = `ebic1_K37`** (D35, D42 item 6), at both scales. The CV rules move to the sensitivity table and are disclosed there.
4. **Adaptive lasso:** the rows now come from the BENCH_F3_PROD rerun, which uses the lasso `cv_min` pilot (run `20261102T1252Z_bench_f3v2_prod`; D42 item 2, D86).
   - 2,400/2,400 fits, all rule rows ok, scored with the campaign scoring code.
   - Headline `ebic1_K37`; CV as sensitivity.
   - Old ridge-pilot → new pooled `ebic1_K37` /600:

     | | p500 | p1000 |
     |---|---|---|
     | c = 1 | 247 → 493 | 96 → 512 |
     | c = 0.5 | 36 → 253 | 12 → 197 |
5. Every other benchmark row is unchanged (same fits, same scoring).

**Scope (D22).** At p ≫ n there is no exact posterior to compare against. Only selection against the truth is reported.

**Rows.**
- **HPM:** SMC-BVS's highest-probability model (primary).
- **MPM (RB):** variables whose Rao–Blackwellised PIP exceeds 0.5.
- **MPM (plain):** variables whose plain PIP exceeds 0.5.
- **Benchmarks:** each method's registered rule, as in the earlier table. For MCP and ABESS (splicing heuristic), the primary is EBIC(γ = 1) at c = 1, and EBIC(γ = 1) with the size bound K = 37 at c = 0.5 (pre-registered).

**Caveats carried over:**
- The benchmark code is AI-written.
- Its frequentist reproduction check (G5) is partial.
- ABESS fails the independent same-size search check.
- Details: `../H_existing_20261030/HEADLINE_H.md` §6 and `BENCH_OPEN_ITEMS.md`.

## 1–2. Exact recovery against the truth (count out of 100 per scenario; pooled out of 600)

#### c = 1 (strong signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 95 | 96 | 94 | 91 | 89 | 94 | **559** | 95 | 95 | 97 | 93 | 84 | 96 | **560** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 92 | 97 | 93 | 93 | 90 | 94 | **559** | 94 | 95 | 97 | 94 | 85 | 96 | **561** |
| **SMC-BVS MPM (plain PIP > 0.5)** | secondary, new | 92 | 97 | 93 | 93 | 90 | 94 | **559** | 94 | 95 | 97 | 94 | 85 | 96 | **561** |
| SuSiE | primary | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 94 | 99 | **582** |
| SuSiE-refine | companion (R4); arm added after the c = 1 results were seen | 99 | 98 | 97 | 95 | 98 | 98 | **585** | 100 | 96 | 98 | 95 | 93 | 99 | **581** |
| Spike-and-slab lasso | primary | 99 | 99 | 97 | 84 | 93 | 97 | **569** | 100 | 96 | 98 | 92 | 97 | 99 | **582** |
| Horseshoe (95% CI) | primary | 92 | 98 | 100 | 87 | 98 | 99 | **574** | 91 | 95 | 100 | 91 | 98 | 100 | **575** |
| MCP `ebic1` | pre-declared primary | 39 | 69 | 77 | 44 | 78 | 70 | **377** | 18 | 28 | 60 | 32 | 49 | 48 | **235** |
| MCP `ebic1_K37` | post hoc | 69 | 79 | 77 | 44 | 78 | 70 | **417** | 66 | 74 | 80 | 32 | 69 | 65 | **386** |
| ABESS (splicing heuristic) `ebic1` | pre-declared primary | 66 | 77 | 71 | 26 | 76 | 49 | **365** | 40 | 63 | 76 | 24 | 66 | 54 | **323** |
| ABESS (splicing heuristic) `ebic1_K37` | post hoc | 68 | 77 | 71 | 26 | 76 | 49 | **367** | 63 | 72 | 76 | 24 | 67 | 54 | **356** |
| Lasso `ebic1_K37` | headline (D35/D42) | 67 | 29 | 2 | 0 | 9 | 4 | **111** | 48 | 28 | 4 | 0 | 5 | 4 | **89** |
| Elastic net `ebic1_K37` | headline (D35/D42); α disclosure §3 | 48 | 11 | 0 | 0 | 2 | 0 | **61** | 38 | 12 | 0 | 0 | 0 | 0 | **50** |
| Adaptive lasso `ebic1_K37` | headline (D42/D86); lasso `cv_min` pilot | 73 | 89 | 85 | 82 | 82 | 82 | **493** | 82 | 85 | 91 | 83 | 77 | 94 | **512** |

#### c = 0.5 (weak signal)

| Method / rule | role | p500 S1 | S2 | S3 | S4 | S5 | S6 | **/600** | p1000 S1 | S2 | S3 | S4 | S5 | S6 | **/600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SMC-BVS HPM** | primary | 79 | 84 | 64 | 25 | 59 | 59 | **370** | 71 | 75 | 67 | 35 | 31 | 61 | **340** |
| **SMC-BVS MPM (RB PIP > 0.5)** | secondary | 74 | 83 | 63 | 18 | 53 | 47 | **338** | 70 | 76 | 63 | 24 | 32 | 56 | **321** |
| **SMC-BVS MPM (plain PIP > 0.5)** | secondary, new | 74 | 83 | 63 | 18 | 53 | 47 | **338** | 70 | 76 | 62 | 24 | 32 | 56 | **320** |
| SuSiE | primary | 65 | 70 | 34 | 9 | 3 | 39 | **220** | 49 | 57 | 47 | 21 | 0 | 31 | **205** |
| SuSiE-refine | companion (R4), pre-registered | 66 | 71 | 43 | 17 | 6 | 46 | **249** | 49 | 57 | 49 | 22 | 3 | 32 | **212** |
| Spike-and-slab lasso | primary | 80 | 84 | 53 | 9 | 42 | 35 | **303** | 67 | 64 | 43 | 15 | 28 | 38 | **255** |
| Horseshoe (95% CI) | primary | 74 | 69 | 18 | 0 | 10 | 14 | **185** | 60 | 50 | 11 | 0 | 11 | 4 | **136** |
| MCP `ebic1_K37` | pre-registered primary | 62 | 71 | 42 | 1 | 45 | 19 | **240** | 49 | 59 | 45 | 1 | 20 | 18 | **192** |
| MCP `ebic1` | pre-declared, non-primary at c = 0.5 | 38 | 58 | 42 | 1 | 45 | 19 | **203** | 13 | 26 | 34 | 1 | 18 | 10 | **102** |
| ABESS (splicing heuristic) `ebic1_K37` | pre-registered primary | 67 | 72 | 34 | 4 | 48 | 31 | **256** | 54 | 64 | 42 | 3 | 23 | 28 | **214** |
| ABESS (splicing heuristic) `ebic1` | pre-declared, non-primary at c = 0.5 | 65 | 72 | 34 | 4 | 48 | 31 | **254** | 36 | 55 | 42 | 3 | 22 | 28 | **186** |
| Lasso `ebic1_K37` | headline (D35/D42), pre-registered | 17 | 5 | 0 | 0 | 1 | 1 | **24** | 11 | 3 | 1 | 0 | 0 | 0 | **15** |
| Elastic net `ebic1_K37` | headline (D35/D42), pre-registered; α disclosure §3 | 11 | 3 | 0 | 0 | 0 | 0 | **14** | 8 | 2 | 0 | 0 | 0 | 0 | **10** |
| Adaptive lasso `ebic1_K37` | headline (D42/D86); lasso `cv_min` pilot | 64 | 69 | 34 | 11 | 38 | 37 | **253** | 59 | 53 | 32 | 7 | 14 | 32 | **197** |

**Sensitivity rows** (all are 0/600 unless shown):

| Rule | role | c = 1: p500 /600 | p1000 /600 | c = 0.5: p500 /600 | p1000 /600 |
|---|---|---|---|---|---|
| Lasso `cv_min` | registered primary before D42 | 0 | 0 | 0 | 0 |
| Lasso `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 |
| Elastic net `cv_min` | registered primary before D42 | 0 | 0 | 0 | 0 |
| Elastic net `cv_1se` | companion (R2) | 0 | 0 | 0 | 0 |
| Adaptive lasso `cv_min` | registered primary before D42 | 0 | 0 | 0 | 0 |
| Adaptive lasso `cv_1se` | companion (R2) | 7 | 1 | 2 | 0 |

**Why the lasso family's CV rules are not the headline.** BENCH-AUDIT found no implementation fault.
- The CV rules' 0/2,400 is method behaviour: CV-min over-selects at p ≫ n by 30–80 false positives.
- EBIC with the K = 37 bound was a pre-registered companion at c = 0.5 and post hoc at c = 1.
- Felipe moved the headline to it (D35/D42), and that change is disclosed here.

Per-cell tables: `tables/headline_h2_tables.md`; long form: `tables/headline_h2_long.csv`.

## 3. Elastic-net α disclosure (PREREG R3)

CV chose α* = 0.9, the top edge of the frozen grid {0.1, 0.25, 0.5, 0.75, 0.9}, in **2,399 of 2,400 fits**: 100/100 in every p × c × scenario cell except p500, c = 0.5, S4 (99/100; one fit chose α* = 0.5).
- So the elastic net behaved as a near-lasso throughout.
- Whether a wider grid would change its EBIC rows is untested; that is disclosed, not ruled out (BENCH-AUDIT).
- Source: `bench_audit/mgr_checks/f2_alpha_table.csv`, copied to `tables/f2_alpha_disclosure.csv`.

**Adaptive lasso `cv_min` last-grid-point disclosure (D55).** In the rerun, `cv_min` selected the last (smallest) λ of the grid in **804 of 2,400 fits**. These are the rows flagged `lambda_last`:

| | c = 1 | c = 0.5 |
|---|---|---|
| p500 | 260/600 | 58/600 |
| p1000 | 391/600 | 95/600 |

`cv_min` is a sensitivity row only (0/600 everywhere); the `ebic1_K37` headline is not affected. Source: `tables/f3/f3_new_checks.txt`.

## 4. SMC-BVS: share of datasets where the selected model equals the truth

| | HPM = truth | MPM (RB) = truth | MPM (plain) = truth |
|---|---|---|---|
| p = 500, c = 1 | 93.2% (559/600) | 93.2% (559/600) | 93.2% (559/600) |
| p = 1000, c = 1 | 93.3% (560/600) | 93.5% (561/600) | 93.5% (561/600) |
| p = 500, c = 0.5 | 61.7% (370/600) | 56.3% (338/600) | 56.3% (338/600) |
| p = 1000, c = 0.5 | 56.7% (340/600) | 53.5% (321/600) | 53.3% (320/600) |

The Monte Carlo standard error of each pooled share is about 1–2 percentage points.

**RB and plain MPM agree in 2,391 of 2,394 completed fits.** The three disagreements:
- each involves a single variable whose two PIPs straddle 0.5, within 0.003 of each other;
- the plain MPM loses one recovery (p1000, c = 0.5, S3, r060) and gains none.

The largest |RB PIP − plain PIP| over all variables and fits is 0.0067.

## 5. Where SMC-BVS wins and loses

The SMC-BVS outcomes are identical to the 10-23 fits, so every paired comparison in `../H_existing_20261030/HEADLINE_H.md` §4 stands unchanged:
- **c = 0.5:** the HPM is first or tied-first in 11 of 12 cells. It leads the best benchmark (spike-and-slab lasso) by 67 datasets at p500 and 85 at p1000.
- **c = 1:** it ranks 4th, behind SuSiE, the spike-and-slab lasso and the horseshoe (about 93% against 95–97%). Almost every miss adds variables to the truth.
  - With the rerun adaptive lasso (493 and 512 /600), it is 4th of 9.

**Against the new lasso-family headline rows:** the HPM beats Lasso `ebic1_K37`, Elastic net `ebic1_K37` and Adaptive lasso `ebic1_K37` in all 24 scenario cells. The same holds for MCP `ebic1_K37` and ABESS `ebic1_K37`.

## 6. Accounting

**2,400 fits = 2,394 completed + 6 `resource_limit` + 0 missing.** This matches OPS's reconciliation and the 10-23 fits fit for fit.
- **The 6 stops:** all in S5, one at p500 c = 1, three at p1000 c = 1 and two at p1000 c = 0.5.
- **Runtime guard:** each hit it at its allocation (6,300 s at p500; 24,000 s at p1000).
- **Where they stopped:** five in the tier-1 calibration diagnostic, one in the final bridge.
- **P5 not run:** the same-seed retry at doubled allocation was not run (Felipe, D62). The 6 count as misses in every table.
- **Audit-only support:** in 3 of the 4 c = 1 stops, the support saved at the stop equals the truth. It is not counted.

Files: `tables/smc_h2_per_fit.csv` (one row per fit) and `tables/ev_stops.csv`.
