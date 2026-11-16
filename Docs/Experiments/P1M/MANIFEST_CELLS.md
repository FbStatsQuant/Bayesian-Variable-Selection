# MANIFEST_CELLS — the executable cell / seed manifest of the P1M experiment (DRAFT v0.1, WP5, 2026-11-16)

**Status: DRAFT for the Engineering manager.** It answers Sol F7 and the F3 disposition: "one costed cell/seed manifest
replaces the tier totals". Sources:
- EXPERIMENT_PLAN v0.2 (errata, §2.3);
- OD-14 / D-10 (1M cells);
- D-21 (descopes);
- H-1 (envelope A + D ≈ 24.6k);
- ENGINEERING_SPEC §0-v2.5, §0-v2.7, §0-v2.8;
- REVIEW_disposition_sol (F3, F6, F7, F8).

**Every cost is a PLANNING VALUE** (§0-v2.5 per-fit costs; n-scaling c(n) = 3c_s + 30 ns with c_s = 30 + 60·n/200 ns, from
the owner sheet). The manager re-costs after the SPR sweep and gate T5 replace them with measured core-h per fit.

**Executable form:** `Scripts/SMC_BVS/engine_v4/tools/slurm/p1m_cells.py` (PR #19) holds this table as code.
- It expands the table into **265 fits**, one row each: run id, data seed, engine seed, mode, N, R′, parameters,
  planning cost (`--tsv`).
- It also writes **48 Slurm-driver plans**: ≤ 150 tasks each, one resource shape each, all validated by `p1m_driver.py`
  (`--plans`).
- `p1m_cells.py --summary` prints the totals below.

## 1. Seeds, run ids, reuse
- **Data seed** = R·10⁸ + D·10⁶ + (n/100)·10⁴ + rep, where:
  - R = log₁₀ p (1 marks the p ≤ 25 exact block);
  - D: 1 IND, 2 AR-strong, 3 AR-weak, 4 BLK, 5 ADJ-OPP, 6 NULL.

  The rule is deterministic and collision-free, and every seed is < 2³¹ − 1.
- **Engine seed**: seed 1 = the data seed; seed 2 = data seed + 50 (same data). **Calibration seed** (precision study) =
  data seed + 70 + c.
- **Run id**: `<rung>-<design>-n<n>-r<rep>-<arm>-s<seed>`, e.g. `6-AR-n200-r01-V-s1` (the 1M pilot).
- **Shared datasets are run once.** The 10⁴ overlap datasets are replicates 1–4 (AR), 1–2 (AR-weak, ADJ-OPP) and 1 (IND,
  NULL) of the 10⁴ science cells; their V fits are costed to the overlap. The precision study runs on overlap rep 1 of
  AR, AR-weak and ADJ-OPP. The 1M N = 10⁴ fit runs on the data of AR rep 1.
- **Pilot rule (Sol F7).** The 1M pilot is replicate 1 only if the frozen configuration is unchanged after it. Otherwise
  it is kept as pilot evidence, and a fresh replicate 1 (`…-r04-…`, +963) is run.

## 2. Cells
Modes:
- **V** = V-1M class A, precise: N = 2,500, R′ = 16, bounded calibration;
- **T** = the theory mode in the new engine (law mode, bit form, N = max(2500, n, p), coded calibration).

### Exact reference and gates
| block | cells | fits | core-h |
|---|---|---|---|
| T8 exact reference | p ≤ 25, 20 fixtures × 400 islands, SMC branch forced, every Δ/C change on | 20 | 50 |
| gates + benchmarks | T1–T11 on NOTS, G0 | — | 400 |
| T5 end-to-end NOTS gate (Sol F3) | one full stage at 10⁵ with all moves, RB, stores and checkpoints; setup and calibration timed | — | 200 |
| 5k anchor (§0-v2.7) | revision D unmodified vs new-engine T (compat) vs V, 3 datasets; 20-seed law test at 2k | — | 300 |

### 10⁴ overlap (§0-v2.7): T vs V on the same 10 datasets, 2 seeds each, n = 200
| design | datasets | T fits | V fits | core-h (T + V) |
|---|---|---|---|---|
| AR-strong | 4 | 8 | 8 | 920 + 80 |
| AR-weak | 2 | 4 | 4 | 460 + 40 |
| ADJ-OPP (WP1 layout: truths 1–2 adjacent, β = a(1, −0.8, 0.9, −0.7, 0.6)) | 2 | 4 | 4 | 460 + 40 |
| IND | 1 | 2 | 2 | 230 + 20 |
| NULL (a = 0) | 1 | 2 | 2 | 230 + 20 |
| **total** | 10 | 20 | 20 | **2,500** (T at 115 per fit, the upper end of 52–115; at 52 the block is ≈ 1,240) |

### Precision study (Sol F6, mandatory, before G-B): 64 islands
| datasets | arms | fits | core-h |
|---|---|---|---|
| overlap rep 1 of AR-strong, AR-weak, ADJ-OPP | N ∈ {2,500, 10⁴} × grid refinement m ∈ {1, 4} × 2 independent calibration seeds (final seeds independent) | 24 | 2,117 (N = 2,500 ≈ 35 per fit; N = 10⁴ ≈ 141) |

The engine parameter names (`grid_refine_m`, `calib_seed`) are placeholders until WP4 fixes them. I_max ∈ {0, 3} and
systematic resampling (D-2, D-14) are compared on the N = 2,500 arms. The settings are frozen from this study before
the final runs.

### 10⁴ science (n-trend, designs, null, second seed, A3 partition), V
| design | n | reps | note | fits | core-h |
|---|---|---|---|---|---|
| AR-strong | 100 / 200 / 400 / 800 | 10 each | seed 2 on all 10 at n = 200 | 10 / 12 + (8 in overlap) / 10 / 10 | 70 / 120 / 160 / 280 |
| AR-weak | 100 / 200 / 400 / 800 | 20 / 20 / 10 / 10 | weak arm at 20 reps for n ≤ 200 (OD-6) | 20 / 18 + (2) / 10 / 10 | 140 / 180 / 160 / 280 |
| IND | 100 / 200 / 400 | 5 | | 5 / 4 + (1) / 5 | 35 / 40 / 80 |
| BLK(20, 0.5) | 100 / 200 / 400 | 5 | | 5 / 5 / 5 | 35 / 50 / 80 |
| ADJ-OPP | 200 / 400 | 5 | mandatory at 10⁴ (Sol F7) | 3 + (2) / 5 | 30 / 80 |
| NULL | 200 | 5 | null control | 4 + (1) | 40 |
| A3 partition | 200 | 10 AR + 10 BLK | exact complete linkage on the same data as the 1M rule (`partition = exact_linkage`) | 20 | 200 |
| **total** | | | | **161** | **2,060** |

### 10⁵ rung, V (12 fits)
| design | n | reps | core-h |
|---|---|---|---|
| AR-strong | 200 | 5 | 480 (π̂(S₀) and P(HPM = S₀) at n = 200: the gate of option D) |
| AR-strong | 400 | 3 | 461 |
| IND | 200 | 2 | 192 |
| ADJ-OPP | 200 | 2 | 192 (mandatory at 10⁵, Sol F7) |
| **total** | | **12** | **1,325** |

### 10⁶ rung, V, n = 200 (OD-14 / D-10)
| cell | fits | core-h |
|---|---|---|
| AR-strong × 3 (rep 1 = pilot, see §1) | 3 | 2,889 |
| ADJ-OPP × 1 | 1 | 963 |
| AR-weak × 1 | 1 | 963 |
| self-check: N = 10⁴ on AR rep 1's data | 1 | 3,600 |
| **total** | **6** | **8,415** |
| *named, NOT in the total (Sol F7):* second seed on AR rep 1 | (1) | (963) |
| **option D** (H-1, conditional on the 10⁵ π̂(S₀) trend): AR-strong, n = 1,000 | 1 | 3,300 |

### Other blocks
| block | core-h |
|---|---|
| ablations (start mode / + LS0 / pilot + local), once per distinct 10⁴–10⁶ dataset (ESTIMATE: 6% of its V fit) | 485 |
| competitors at all rungs + the acceptance runs (Sol F8; `tools/competitors/ACCEPTANCE.md`; 1M = lasso + 1 variational + SIS, D-21) | 400 |

## 3. Totals (PLANNING VALUES) against H-1
| | core-h |
|---|---|
| planned, excluding option D | 18,252 |
| with 25% contingency | 22,815 |
| option D (with contingency) | 3,300 (4,125) |
| **A + D with contingency** | **26,940**, against the H-1 envelope ≈ 24.6k: **+9.5%** |

The excess is below H-1's 15% report threshold, but it is reported here. Sources of the excess:
1. The precision study is now mandatory at 64 islands with 2 calibration seeds: 2,117, against 950 in §0-v2.8.
2. The overlap T fits are costed at the upper end of 52–115.
3. The second 10⁴ seed, A3 and the null control are now explicit rows.

**Trims, if the envelope must hold (largest first):**
- T costed at the measured lower end, 52: −1.26k (−1.6k with contingency).
- The second calibration seed only on the N = 2,500 precision arms: −0.85k.
- AR-weak at n = 400 / 800 with 5 reps: −0.22k.
- AR-strong at n = 800 with 5 reps: −0.14k.

The first two alone give ≈ 24.5k.

## 4. Analysis conventions fixed with the manifest (Sol F7)
- **PIP reliability curve**: labelled a *repeated-sampling diagnostic* under a fixed truth, not Bayesian calibration.
  Report active/null components, bin counts, and dataset-clustered uncertainty. Exact-PIP approximation error comes from
  the T8 fixtures at small p.
- **Intervals**: dataset-clustered everywhere. Method differences use paired datasets and seeds.
- **C2 at 1M**: 3/3 gives a one-sided 95% lower bound of 0.37 (two-sided 0.29). Stated as feasibility plus agreement
  with the lower-rung trend.
- **C5 at 1M**: an out-of-sample accuracy point consistent with the 10⁴ / 10⁵ trend, not a decay statement.
- **The store law Π̂^𝒯** is a truncated approximation; its omitted mass is reported with every distance (D-17, Sol F9).

## 5. Batching and submission (driver conventions)
- Plans are grouped by (block, p, n, mode, N, R′), at most ⌊150 / (R′ + 4)⌋ fits per batch: 7 fits at R′ = 16, 2 at
  R′ = 64.
- Batches are released stage by stage at the gates G-A → G-B → G-C → G-C2. Each batch gets a ledger row with its
  worst case = Σ allocated CPUs × time limit.
- At the driver's planning time limits the 48 plans sum to ≈ 53k worst case, against 18k planned. Those limits are
  deliberately generous until T5. Tighten them from measured stage times before submitting; otherwise the admission
  check reserves too much of the envelope.
- **Memory moves** (REVIEW_disposition_sol): island tasks 24–32 GB, calibration 48–64 GB at 10⁶. Option D (n = 1,000):
  X 8 GB and logr ≤ 9.4 GB under D-19, so 64 GB per island task.

## 6. Open (for the manager)
1. Engine parameter names for the precision arms (grid refinement, calibration seed, I_max, resampling): WP4.
2. Pilot-replacement rule wording, and whether the 1M second seed (963) is bought from the trims.
3. Re-cost after the SPR sweep / T5: replace the per-fit planning values in `p1m_cells.py` (COST_V, COST_T, n-scaling)
   and regenerate.
