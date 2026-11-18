# OVERLAP_1e4_PREREG: pre-registration of the 10⁴ T-vs-V overlap analysis (Engineering, Sonnet analyst; Wed 2026-11-18)

**Status: FINAL for W0.** Written before any 10⁴ engine fit exists. HQ gate: DECISIONS H-18 (b)(c), plan §8. Any later change is a logged deviation (§9); nothing in the thresholds below is tuned on data.

| item | value |
|---|---|
| analysis script | `results/overlap1e4/compare_overlap.py` |
| **script sha256** | **`311bbad886fc61c679ac47d1c30faf8d8897e33681baf5711f1f268472632eea`** |
| script self-test | `tests/test_compare_overlap.py` (13 synthetic cases pass; sha256 `630582b702dabb60b1548d17085a9a1907ea02e8a4f9c60ad4ffac70d4f1161a`; fixtures use the real T5 `eval.bin.json` schema, `tests/template_eval.bin.json`) |
| thresholds | the `PREREG` dict at the top of the script (copied into every `verdict.json`) |
| evaluator | the engine `eval` command at the freeze commit F (`code_commit` in every `run_manifest.json`; F is not known today). Binding by reference: the script prints the set of `code_commit` and binary sha256 values per arm into `verdict.json`; `--expect-commit F` makes a different commit a warning. F and the two binary sha256 (V build `-DV4_ISLAND_ISA=sapphirerapids`, T default build) go into CAMPAIGN_FREEZE.md and the W0 manifests. |
| basis | OVERLAP_1e4_SUBMISSION_PLAN.md §1, §4, §8; ENGINEERING_SPEC §0-v2.7; EXPERIMENT_PLAN §2.3 (A1, G-A), §3.3; engine README_WP5 / INTERFACES v0.1.27 |

## 1. Designs, seeds, fits (40)

p = 10⁴, n = 200. Data seed = 4·10⁸ + D·10⁶ + 2·10⁴ + rep (D: IND 1, AR 2, AR-weak 3, ADJ-OPP 5, NULL 6). Engine seed s1 = data seed, s2 = data seed + 100. T and V share (data seed, engine seed). Run id `4-<design>-n200-r<rep>-<T|V>-s<1|2>`.

| dataset | design | data seed = s1 | s2 |
|---|---|---|---|
| 4-AR-n200-r01 … r04 | AR strong (a = 1) | 402020001 … 402020004 | 402020101 … 402020104 |
| 4-ARweak-n200-r01, r02 | AR weak (a = 0.6) | 403020001, 403020002 | 403020101, 403020102 |
| 4-ADJOPP-n200-r01, r02 | ADJ-OPP | 405020001, 405020002 | 405020101, 405020102 |
| 4-IND-n200-r01 | IND | 401020001 | 401020101 |
| 4-NULL-n200-r01 | NULL (a = 0, S₀ = ∅) | 406020001 | 406020101 |

10 datasets × 2 seeds × 2 arms = 40. Waves: W0 = AR r01 s1 and ADJ-OPP r01 s1 (T and V); W1 = IND, NULL, AR-weak r01 (s1, s2); W2 = AR-weak r02, ADJ-OPP r01 s2 + r02, AR r01 s2; W3 = AR r02–r04. **Pairing check (stop rule and criterion PAIR):** `truth.json` `X_sha256` and `y_sha256` must be equal across the 4 fits of a dataset (setup regenerates them per fit) and different across datasets.

## 2. Arms and settings

| | V | T |
|---|---|---|
| engine mode | V (class A, FMA family `sapphirerapids`) | law mode, **bit form** |
| N | 2,500 | max(2500, n, p) = 10⁴ |
| R′ (islands) | 16 | 4 |
| calibration | bounded | **coded calibration with escalation** (D-26; tier rule fixed at the freeze) |
| limits | setup 8 CPU 0:15; calibrate 16 CPU 0:30; islands 4 CPU 0:30 each; merge 8 CPU 0:15; eval 8 CPU 0:20 | setup 8 CPU 0:15; **calibrate 48 CPU 16 G, 3:00**; islands 24 CPU 0:45 each; merge 8 CPU 0:20; eval 8 CPU 0:30 |
| cost model per fit | 10 core-h (central 6) | 115 core-h (central 40) |
| version | registry pin v3.1 @ 4676af6 = method-v3.1.1-listpip core tree 61b0a582, engine freeze commit F | same |

**One-off exception recorded (HQ H-18 (b)):** the T calibrate task has a **3 h limit** (`max_task_hours = 3.0`) instead of the 2-h task rule. It applies to the T calibrate stage of the 10⁴ overlap rung only. W0 cap = 543 core-h (T 449 + V 93.3). A T calibrate that reaches the 3 h limit is a failed stage, not a reason to raise the limit again.

Evaluator settings (identical for every fit; eval record `params`): n_x = 4,000 x draws, n_gh = 64, n_draws = 10⁴, n_test = 10⁴, rel_cut = 10⁻¹², top_k = 1,000, tail_r = 1,000, tail_groups = 8, block_rows = 500, `eval` seed = the fit's engine seed. The script does not verify these (see §8, item 5); they are fixed by the plan and the driver.

The script checks, per fit, N, R′, mode and (V) `island_isa` against this table whenever the field exists in `eval.bin.json fit.meta` / the manifest. A mismatch makes the fit **not delivered (invalid)**.

## 3. Metrics, formulas, data fields, tolerances

Notation: A ∈ {V, T}, dataset d, engine seed s ∈ {1, 2}. "Delivered" fits only enter. JSON paths are in `eval.bin.json`.

### 3.1 D: delivered 40/40
A fit is delivered iff `status` and `fit_status` = completed, `fit.meta.status` = completed, the settings of §2 hold, `selection.hpm`, `evidence.logZ`, `evidence.logZ_T`, `dist.T.predictive.h2` are present and `fit.bin` is readable with all section hashes verified. Pass iff 40/40. Every failure is stated in `verdict.json`; none is dropped. G-B needs ≥ 95 % (36/40) for the 10⁵ gate; **this rung's clean needs 40/40**.

### 3.2 S1–S4: selection
- **S1 (HPM):** HPM_A,d,s = the set `selection.hpm` (original 1-based column indices). A dataset is *equal* iff HPM(V, s) = HPM(T, s) as sets for **both** s ∈ {1, 2} (seed-paired). Pass iff ≥ 9 of 10 datasets are equal.
- **S2 (higher F):** F_A = `selection.F_hpm`. Fail iff any seed pair has F_T > F_V + 10⁻⁶ (the guard is a floating-point allowance only; F values are ≈ −230).
- **S3 (MPM):** MPM = `selection.mpm`. Pass iff MPM(V, s) = MPM(T, s) in every one of the 20 seed pairs.
- **S4 (NULL):** `pip.eq.n_null_gt_0.5` = 0 in all 4 NULL fits (no model beyond ∅ has a column with PIP > 0.5).

### 3.3 P: PIP
`pip_primary` = the equal-weight island mean = `pip_eq` (fit.bin section `pip_eq`, indexed by the kept column; checked equal to the row mean of `pip_r` to 10⁻¹⁶ on T5). **The p-wide vector is only in `fit.bin`**, not in any JSON.
- P̄_A,j = mean over the two seeds of `pip_eq`_j. D_j = P̄_V,j − P̄_T,j.
- Island s.e. of one fit: se_f,j = sd_r(`pip_r`[r, j], ddof 1) / √R′_A (r over the R′_A islands; checked: max_j = `pip.island_spread.max_sd`/√R′ on T5).
- s.e. of the 2-seed mean: Var_A,j = (se²_s1,j + se²_s2,j) / 4; combined se_j = √(Var_V,j + Var_T,j).
- **Pass (per dataset) iff for all j: |D_j| ≤ max(0.01, 3·se_j).** This is the plan's "max_j |PIP_V − PIP_T| ≤ max(0.01, 3 combined s.e.") evaluated with the s.e. of each column (the script reports the worst ratio |D_j| / max(0.01, 3 se_j) and max_j |D_j|). Pass overall iff every dataset passes.
- Per-j seed-to-seed s.e. is not used for the threshold (two seeds per column are unstable); T's and V's own seed-to-seed max_j |ΔPIP| are reported (`pip_seed_range_V`, `pip_seed_range_T`). Also reported, not criteria: max_j |ΔPIP_T| (`pip_T`) and, if `fit.bin` carries it (engine v0.1.27+), max_j |Δpip_list|.

### 3.4 E1: evidence
log Ẑ_A,d,s = `evidence.logZ` (plain mean of the island Ẑ_r, `v3_run.R:155`).
- **Island s.e.** (one fit): se_isl = sd_r(Ẑ_r/Ẑ) / √R′ with Ẑ_r from `evidence.logZ_r` (delta method for log of the island mean; equals `sigma_hat`/√R′ to first order, 0.00871 vs 0.00869 on T5).
- **Seed-to-seed yardstick (pooled over the datasets):** s_A² = (1/m_A) Σ_d (logẐ_A,d,1 − logẐ_A,d,2)² / 2, over the m_A datasets with both seeds delivered (m_A = 10 when complete; 10 df). Pooling is pre-registered because 2 seeds give an unstable per-dataset s.e. (plan §4, §7 risk 3).
- **Per-arm variance of the 2-seed mean:** v_A,d = max( s_A²/2 , (se_isl,s1² + se_isl,s2²)/4 ). The island term is a floor (a pooled seed sd cannot be taken below the within-fit island spread).
- **Combined s.e.:** se_comb,d = √(v_V,d + v_T,d). Δ_d = mean_s logẐ_V − mean_s logẐ_T.
- **Pass iff |Δ_d| ≤ 3·se_comb,d for all 10 datasets.** Reported: Δ_d, se_comb,d, |Δ_d|/se_comb,d, s_V, s_T.

### 3.5 E2: log Z_T as a deterministic lower bound (replaces log Ẑ_occ; D-21, H-18)
log Z_T,A = `evidence.logZ_T` = log Σ_store e^F: a **deterministic lower bound** on log Z (`store.deterministic_bound`; no deterministic upper bound exists). The occupancy estimate log Ẑ_occ and its ≤ 0.05 criterion are **not** used (occupancy diagnostics deferred).
- Reported per fit and per dataset: log Z_T for each arm, their difference (T − V), and the gap log Ẑ − log Z_T.
- **Consistency check (pass iff all hold, per dataset):** (i) log Z_T,T ≤ mean_s log Ẑ_V + 3·se_comb,d; (ii) log Z_T,V ≤ mean_s log Ẑ_T + 3·se_comb,d; (iii) per fit, log Z_T ≤ log Ẑ + 3·se_isl (a lower bound cannot exceed the truth beyond estimation noise). A violation indicates a bug in a store or an evidence estimator; the check is one-sided by construction.
- `evidence.logZ_lower95` (Markov bound) and `store.pi_T_hat` are noisy diagnostics and are not criteria.

### 3.6 H: predictive (Hellinger)
Definition: d_H² (f, g) = 1 − ∫∫ √(f g) dy ν_x(dx) (affinity form, STATEMENT §0; the engine's `h2`), d_H = √max(h², 0).
- **d_H(T, f\*)** = √(`dist.T.predictive.h2`) of the T arm's fits, mean over the two seeds, where object T = the **store BMA** (truncated at relative weight 10⁻¹², dropped mass `dist.T.dropped_mass` reported). The object is the same for V fits (`dist.T` of a V fit is the V store BMA). The estimate is exact top-K (1,000) + stratified tail sample; `h2_se_x`, `h2_se_tail` are carried to `per_fit.csv`.
- **d_H(V, T)** = d_H between the V and T store-BMA predictive densities f̄_V, f̄_T, with the same 4,000 x draws and 64-node Gauss–Hermite grid as the eval; mean over the two seed pairs.
- **Pass (per dataset) iff d_H(V, T) ≤ 0.10 · d_H(T, f\*).** Pass overall iff every dataset passes; a miss on ≥ 2 datasets is not clean (§4).
- **Data-field status:** the engine `eval` is single-fit: it reports each arm's distance to f\* and **no V-vs-T distance**. d_H(V, T) therefore needs one extra evaluation of the two kept `law.bin` files (a unit of record) with the eval's x draws; the script reads its output from `--cross-file` (`{"schema": "overlap1e4.cross_vt/1", "pairs": {"<dataset>": {"1": {"h2": …}, "2": {"h2": …}}}}`). **Until that file exists, H is NOT_EVALUATED and the outcome cannot be CLEAN.** Without a cross value the script applies only the triangle screen |d_H(V, f\*) − d_H(T, f\*)| ≤ d_H(V, T): a screen value above 10 % of d_H(T, f\*) is a *certain* H failure for that dataset; a screen value below it proves nothing.
- **Reported per arm (not criteria):** plug-in h² of the HPM and MPM (`dist.H.plugin.h2`, `dist.M.plugin.h2`, closed form), weighted plug-in h², predictive h² and KL, posterior quantiles of d_H (`post_dH`), test MSE and mean log predictive density on 10⁴ fresh rows, ratios to the oracle (`dist.ratio_to_oracle`), each with the dataset-clustered intervals of MANIFEST §4 (computed in the comparison tables, not in this script).

### 3.7 C: cost
Billed core-h per fit = sum over its stages of sacct CPUTimeRAW/3600 (`p1m_cost.py` → `cost_<run_id>.json`, `billed_core_h`). **Pass iff every fit is ≤ 1.5 × its arm's model: V ≤ 15.0, T ≤ 172.5 core-h** (the same numbers as the plan's "during" stop rule: V fit > 15, T fit > 172). The rung total is reported against the quote (expected ≈ 1.0k, stop at 1.6k cumulative, ceiling 2.5k); it is not itself a criterion. A fit without a cost record makes C NOT_EVALUATED.

## 4. Outcome rules (the script computes them; the independent review is a separate human step)

Notation: **hpm_miss** = number of datasets with an HPM mismatch in any evaluable seed pair; **pred_fail** = number of datasets failing H (including certain screen failures).

1. **INVALID:** criterion PAIR fails (X/y sha not equal within a dataset). Stop; tell HQ.
2. **NOT CLEAN** (plan §4 "stop, HQ + Theory (V is not a faithful variant)") if any of: hpm_miss ≥ 2; any seed pair with F_T > F_V; pred_fail ≥ 2.
3. **MARGINAL** (plan §4: "the precision study is the diagnosis, run first; 10⁵ stays blocked") if not (2) and at least one other criterion fails: E1, E2, P, S3, S4, a single predictive miss (pred_fail = 1), or C. This is the residual class, so every case is classified (the plan's list names only evidence and PIP; S3, S4, a single H miss and C had no stated class: **resolution R3, §5**).
4. **INCOMPLETE** if not (1)–(3) and D fails or any criterion is NOT_EVALUATED (including H without a cross value). HQ decides on infrastructure reruns (one per fit, plan §4 "during"); no release.
5. **CLEAN** iff every criterion D, PAIR, S1–S4, P, E1, E2, H, C passes (S1 may have 1 equal-set miss), **and** the independent review (code + tables) of the comparison reports ACCEPT. CLEAN releases the precision study (64 islands) and the 10⁴ science; the 10⁵ stays gated by G-B.

Outcome rules 2–3 count only evaluable data: a dataset with a missing fit is not an HPM mismatch, it is a D failure.

## 5. Interpretations of the plan text that I fixed here (HQ may overrule BEFORE W0; none can be changed after W0 without a deviation)

- **R1 seed pairing.** The plan states "HPM(V) = HPM(T) in ≥ 9/10 datasets" without saying how two seeds combine. Fixed: seed-paired, both pairs must agree (strict). A looser reading (best-F HPM over the two seeds) would pass more datasets; the script reports per-pair `hpm_equal_s1/s2` so it can be recomputed.
- **R2 combined s.e.** "s.e. from the island spread / seed-to-seed pooled over the 10 datasets" is read as: seed-pooled sd per arm (yardstick = T's own and V's own seed spread, pooled over datasets) with the dataset's island s.e. as a floor (§3.4). PIP uses island s.e. per column only (§3.3).
- **R3 outcome partition** as in §4 (residual class MARGINAL). Under the plan's wording alone, an MPM mismatch, a single H miss or a cost miss would be unclassified.
- **R4 cost** is per fit (the plan's stop rule numbers), not the rung total.
- **R5 E2** is an operationalisation of "log Z_T reported as a deterministic lower bound": reported always, plus a one-sided consistency check (§3.5). It is not the log Ẑ_occ tolerance.
- **R6 PIP** tolerance applied per column (§3.3).

## 6. Procedure after each wave (details in README.md)
1. Offload verified (`sha256sum -c`), runs in `records/<batch>/<run_id>/`; `p1m_cost.py` cost files in the same dir or a `--cost-dir`.
2. `compare_overlap.py --wave-check` after W0, W1, W2 (partial; island-only s.e.; no verdict). `compare_overlap.py` (full) after W3, 40/40.
3. The verdict files (`per_fit.csv`, `per_dataset.csv`, `verdict.md`, `verdict.json`) are saved unedited next to this file; the review reads those.
4. Stop rules of plan §4 "during" remain with the manager; the script does not enforce them except PAIR and C.

## 7. What this analysis does not do
No selection of metrics or tolerances after seeing data; no re-weighting of datasets; no use of log Ẑ_occ; no extra seeds; no fits are dropped (undelivered fits are counted in D and shown).

## 8. Fields and checks that could NOT be located or verified in the engine outputs (flagged)
1. **V-vs-T cross predictive Hellinger: no engine field** (§3.6). Needs an extra evaluation of the two `law.bin` files; H stays NOT_EVALUATED until then. This is the only criterion that cannot be computed from the engine's JSON/binaries as they are today.
2. **sacct cost record in a collected run dir:** `p1m_cost.py` writes `cost_<run_id>.json` to a directory of its own choosing; neither the T5 nor the F1M example dir contains one (their `cost/` holds the engine's `cost_*.jsonl`, and `eval.bin.json.cost` has no sacct block). The script looks in the run dir, `run dir/cost/` and `--cost-dir`. If none is found, C is NOT_EVALUATED (never a pass).
3. **"bit form" (T), "coded calibration" (T), "bounded" (V):** these are in `calib.bin.json settings.rule` / driver plan, not in `eval.bin.json`, `fit.json` or the run manifest (calib.bin.json is not a collected unit). The script cannot verify them; N, R′, mode and island_isa are verified. The T `mode` string is assumed `law` (accepted: `law`, `T`, `theory`); the V one is `V` (seen on T5 and F1M).
4. **File names:** the plan and brief say `fit.json`/`eval.json`; the engine writes `fit.bin.json`/`eval.bin.json`. Both are accepted. The 10⁵ T5 run dir does not hold its `fit.bin` (kept in `records/fitbin_1117/<batch>_<run_id>.fit.bin`): `--fitbin-dir` handles that layout; the 10⁴ run dirs must hold `fit.bin` (unit of record).
5. **Evaluator settings** (n_x, n_gh, …) are read from the plan, not verified per fit (they are in `eval.bin.json params`; not checked by the script).
6. **`orig` (kept → original column map) and `pip_list`** exist only in fit.bin written by engine v0.1.27+; the 10⁵/10⁶ examples predate them. The script compares PIP vectors in the kept index space (valid because X is identical across the 4 fits of a dataset) and verifies the `orig` hashes when present; `pip_list` is reported only if present.
7. `fit.meta.mode` for law mode and the shape of a T run's `eval.bin.json` are untested on a real T fit (none exists); the 13-case fixture suite uses the V-mode T5 record as its template. W0 is the first test of the T-arm parsing; run `--wave-check` on W0 before anything else.

## 9. Deviation log
None. A change to any threshold, rule or field choice after the sha is recorded is a logged deviation with the reason, the date, and the new script sha256.
