# PREREG: precision study (Sol F6) + 10⁴ science, criteria, outcome rules, the pre-declared V − T log Ẑ offset measurement (Engineering, Sonnet plan writer; Thu 2026-11-19)

**DRAFT, pending one Opus plan review (H-25).** Written before any fit of this leg exists. Companion: `LEG_PLAN.md` (feasibility, scope, quote, waves, ops). Format follows `results/overlap1e4/OVERLAP_1e4_PREREG.md`. Nothing here is committed; the commit (with the shas below) is HQ's gate (H-25 (3)).

## Summary (≤ 10 lines)
1. **Registered:** `precision_offset.py` (the ONE offset measurement, §4) and `precision_freeze.py` (the freeze rule, §3), with the sha256 in §1 and synthetic self-tests (7 cases pass). Thresholds live in the scripts and are quoted here; none is tuned on data.
2. **Precision study outcome = a recorded configuration** (N, m, I_max, resampling): m = 4 and I_max = 0 are ADOPT/KEEP by a cost-aware rule; **N = 10⁴ is NOT RUN (blocker B2)** so N stays 2,500 (D-1); **resampling stays OFF, untested (B3)**. The §0-v2.3 targets are reported per fit and never switch estimators.
3. **Freeze rule:** a cost-raising knob is adopted only if its island-sd ratio beats 1/√(cost ratio) on every one of three precision metrics (it must beat spending the same extra cost on more islands) and in every dataset; I_max = 0 is adopted only if not worse than I_max = 3 by more than 15 % (30 % per dataset).
4. **Offset measurement (no pass/fail):** δ(N, m, I_max, k) = mean over datasets of [V block-mean log Ẑ − T reference]; k = islands pooled (4…64) from disjoint blocks of existing and new islands; contrasts in m, I_max, N, k with the T reference cancelling; dataset-clustered intervals; companion Jensen term and log Ẑ_occ. Reader validated against the published −0.00394.
5. **10⁴ science:** descriptive report per the spec (C2, C4, C5, C7, cost, A3, second seed, null); the only gate quantity is **completion ≥ 95 %**; its script is registered by addendum with its sha **before the first science read-back**.
6. **Disclosure (§7):** the reader check printed the full-pool offset on the overlap (−0.00394) and, in the same table, its tier-0-reference sensitivity (−0.00431); nothing else of the R′ / contrast surface was computed on real data.

## 1. What is registered
| item | value |
|---|---|
| offset script | `results/precision1e4/precision_offset.py`, sha256 **`df221026011d0b6b538c65b3dbe5328e9350077e1d417becedacfcb65073c10d`** (`python3 -I`, stdlib, deterministic, no randomness) |
| freeze-rule script | `results/precision1e4/precision_freeze.py`, sha256 **`f2e0b230c67fc6a7bce286238ab645052b9242bee769b732b857cdff45c301bb`** |
| self-tests | `tests/test_precision_offset.py` (4 cases, sha256 `42155aba770fd960f40964dfb6084203bc85b137eae8ed5d16f4557d702184a6`), `tests/test_precision_freeze.py` (3 cases, sha256 `6b0037ed7002ebf19071e23bc4d54a0b3e25a7223dc912b6aed453aaa5545abc`); synthetic records only |
| plan, quote, stops | `LEG_PLAN.md` (quote script `quote_model.py`) |
| evaluator | the engine `eval` command of the frozen build F = `eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463`; evaluator parameters as the overlap (n_x 4,000, n_gh 64, n_draws 10⁴, n_test 10⁴, rel_cut 1e-12, top_k 1,000, tail_r 1,000, tail_groups 8, block_rows 500). **Eval seed = the dataset's data seed, as in the overlap** (the driver's default; overlap verdict deviation 8 is thereby the standing rule, recorded in each eval record's `params.seed`): all fits of a dataset share the x draws; the scripts do not depend on it |
| binary | ONE build for the leg, sha256 recorded in `deploy_leg.log` before A0; every record's `binary.sha256` must equal it (read-back check) |

## 2. Data, arms, delivery (D)
- **Datasets and seeds:** `LEG_PLAN.md` §2 and `waves.json` (run ids, data seeds, engine seeds). Precision datasets are overlap rep 1 of AR-strong, AR-weak, ADJ-OPP (same data seeds as the overlap); each precision arm has one seed = its final seed (k = 10 + a; B1: F requires calibration seed = final seed).
- **Arm identity** is verified from `calib.bin.json settings` (`refine_m`, `I_max`, `tiers[tier_final].N_final`, `rule = bounded`); a fit whose settings differ from its run id is **ARM_MISMATCH** and is not used (`precision_offset.py` lists it; the monitor stops, LEG_PLAN §5.3).
- **Data identity:** `truth.json` X/y sha256 equal across all fits of a dataset and equal to the overlap records for the shared datasets.
- **D (delivered):** `status` and `fit_status` completed, the arm identity verified, `evidence.logZ_r` of length R′ (all finite), `fit.bin` readable with its section hashes verified, one build sha256. A precision fit that is not delivered after one infrastructure rerun makes the precision outcome INCOMPLETE (§6). Science: **≥ 95 % of the 156 new fits delivered** (≥ 149) and no unexplained non-delivery (EXPERIMENT_PLAN G-B wording); every failure is listed, none dropped.

## 3. Precision study: criteria and the freeze rule (G-A: "the precision study freezes (N, m, resampling, I_max)")
### 3.1 Per-fit quantities (engine eval record; R′ = 64, n = 200, p = 10⁴)
| symbol | field | spec reference |
|---|---|---|
| M1 | `fit.meta.occ[M = 1000].sd_log_Z_occ_r` (sd over islands of log Ẑ_occ,r) | §0-v2.3: ≤ 0.05 |
| M2 | `pip.island_spread.max_sd` (max over variables of the sd over islands of the PIP) | §0-v2.3: ≤ 0.005 (`target_met`) |
| M3 | `evidence.sigma_hat` (island sd of Ẑ_r / Ẑ) | §0-v2.3: goal ≤ 0.5, reported |
| HPM | `selection.hpm` | §0-v2.3: merged HPM, certified by the final local search (`local_certified`) |
| flags | `fit.meta.flags.occ_inhomogeneous` (χ² homogeneity of top-M occupancies across islands, I7) | §0-v2.3: flag only |
| log Ẑ vs occupancy | `|evidence.logZ − occ[1000].log_Z_occ| ≤ 3 √(se_Z² + se_occ²)`, se = (sd over islands)/√R′ | §0-v2.3: "SMC log Ẑ within 3 s.e. of log Ẑ_occ" (my operationalisation of "s.e.") |
**Reported per fit, for every arm, never used to switch estimators** (§0-v2.3 wording): all rows above. **Not computable at F:** "the same best model in 16 of 16 islands" (no per-island HPM in the collected records; `occ_inhomogeneous` and the M = 1 occupancy are reported instead). A target miss is reported as a miss.

### 3.2 The rule (exactly what `precision_freeze.py` computes)
Baseline B = (N 2,500, m 1, I_max 3), the spec defaults. Per (dataset, cell) value of each metric = the mean of the 2 replicates (both must be delivered). **r_X** = geometric mean over the three datasets of value(X)/value(B), per metric; **c_X** = mean billed `islands` core-h of the arm's fits / the baseline's (cost files).
- **Cost-raising knob X ∈ {m = 4, N = 10⁴}:** **ADOPT iff for each of M1, M2, M3: r_X ≤ 1/√c_X, and r_X < 1 in every dataset, and the HPM set is the same in every fit of every dataset** (X and B). Otherwise KEEP the baseline value. *Reason:* for the island-pooled estimator the sd falls as 1/√R′, so spending a factor c_X more on islands buys a factor 1/√c_X; a refinement is worth adopting only if it beats that. With the planned costs (m = 4 ≈ 2.3×) the limit is ≈ 0.66; for N = 10⁴ (4×) it is 0.5; the script uses the **measured** c_X.
- **Cost-saving knob I_max = 0:** **ADOPT iff for each of M1, M2, M3: r ≤ 1.15, and r ≤ 1.30 in every dataset, and HPM identical as above.** Otherwise KEEP I_max = 3 (the spec default).
- **Resampling:** systematic resampling is not available in the frozen binary (B3): **frozen OFF (D-14 default), recorded as "not tested"**. N = 10⁴ arms: **NOT RUN** while B2 is held, N frozen at 2,500 (D-1); if HQ authorises the engine change, the same rule applies to the 12 held fits with their measured c_X.
- **Resolution:** an sd estimated from 63 degrees of freedom has ≈ 9 % relative error; an arm mean over 6 fits ≈ 4 %. The thresholds (0.5–0.7, 1.15, 1.30) sit well outside that; the rule is a decision rule, not a significance test, and it never rests on one dataset.
- **Interaction not tested:** m × I_max are not crossed (each knob is compared with the baseline). If both are adopted the frozen configuration (m 4, I_max 0) is a combination the study did not run; the first science wave after FZ is then a 7-fit pilot of that combination before the rest (LEG_PLAN §4 rule: re-quote).

### 3.3 What "frozen" means and the outcome classes (precision study)
| outcome | condition | action |
|---|---|---|
| **COMPLETE** | 18/18 released precision fits delivered (D), arm identity verified, canary clean, both scripts run (shas verified), **independent review ACCEPT** (one Opus child re-derives the rule from the raw records) | record (N, m, I_max, resampling) in a CAMPAIGN_FREEZE addendum with its hash; science plans regenerated in that configuration (LEG_PLAN §3) |
| **INCOMPLETE** | a precision fit not delivered after one rerun, or ARM_MISMATCH | HQ decides (rerun or hold); no freeze |
| **NOT EVALUATED** | a metric missing for a dataset (e.g. `occ` absent) | the knob is reported NOT EVALUATED, baseline kept, reported to HQ |
| **FINDING** (not a failure) | any m / I_max / N contrast of §4 with a 95 % clustered interval excluding zero (the offset moves with a tuning knob, i.e. a possible bias) | listed in the leg report, sent to HQ + Theory; **does not change the freeze rule's output** |
The freeze is by the rule; judgement is not substituted for it after the data are seen. G-A's other conditions (overlap CLEAN: done, H-25) are not re-opened.

## 4. THE pre-declared measurement: the V − T log Ẑ offset against N, m, I_max and R′ (H-25 (3): ONE measurement)
### 4.1 Why and what
The overlap verdict reported, post hoc and outside every criterion, V − T log Ẑ = −0.00394 over the 10 overlap datasets (t(9) −2.80, p 0.021; 7/10 negative; every dataset inside its own 3-s.e. bound) and could not tell whether it is noise, a T-escalation effect, a finite-N / finite-R′ effect, or a systematic difference between the arms. This measurement is the plan's answer. It is **a MEASUREMENT, not a pass/fail criterion**; the spec makes no criterion of it (E1 of the overlap is closed; §0-v2.3 evidence targets are §3).

### 4.2 Estimand (all log Ẑ on the same dataset d)
- **V block mean.** For a V fit f with R′_f islands and an integer k that divides R′_f: L_f(k) = the mean over the R′_f/k **disjoint consecutive blocks** of [log Σ_{r∈block} exp(log Ẑ_r) − log k] (a block's Ẑ is the mean of its islands' Ẑ_r). k = R′_f is the fit's own `evidence.logZ`. k ∈ {4, 8, 16} on the overlap V fits (R′ = 16) and {4, 8, 16, 32, 64} on the leg's fits (R′ = 64). **No extra run is needed: this is a re-reading of the stored `evidence.logZ_r`.**
- **T reference** T̄_d = the mean over the two T seeds of `evidence.logZ` of the overlap T fit(s) (R′ = 4; tier 0 N = 10⁴, tier 1 N = 4 × 10⁴: AR r01 s1, ARweak r01 s1 and IND r01 s2 are tier 1). The tier mix is printed; a **sensitivity with the tier-0 T fits only** is a column of every row.
- **Offset** D_{cell,k,d} = mean over the cell's fits on d of [L_f(k) − T̄_d]; **δ_{cell,k}** = mean over the datasets of D_{cell,k,d} (datasets weighted equally; the dataset is the independent unit). **cell = (N, m, I_max, src)** from `calib.bin.json`; src = `ovl` (the overlap's V fits, 10 datasets) or `prec` (the leg's fits, 3 datasets: AR, ARweak, ADJ-OPP).
- **Contrasts (the T reference cancels), paired by dataset:** R′ slope D_{cell,k2} − D_{cell,k1} for consecutive k; **m**: (2,500, 4, 3) − (2,500, 1, 3) at k = 64; **I_max**: (2,500, 1, 0) − (2,500, 1, 3) at k = 64; **N**: (10⁴, m, 3) − (2,500, m, 3) at k = 64 (only if the N = 10⁴ fits exist).
- **Companions, reported with no inference:** the Jensen term −v̂/(2k) (v̂ = the relative variance of Ẑ_r over the fit's islands; the first-order prediction of the R′ slope if Ẑ is unbiased), and the full-pool offset of log Ẑ_occ (M = 1,000) V − T.

### 4.3 Yardsticks and what is reported
- **Yardsticks:** s_T = pooled seed-to-seed sd of T's log Ẑ over the datasets with two T seeds (overlap: 0.00324, 10 df); s_rep = pooled sd of the two replicates of a precision cell at k = 64; the island-based sd. Every δ is also printed in units of s_T.
- **Uncertainty:** dataset-clustered: mean, sd over datasets, 95 % t-interval (df = datasets − 1; t table in the script), negative counts, and **every per-dataset value** (3 datasets give a very wide interval: say so).
- **Reported tables** (`offset_report.md`, `offset.json`, `offset_per_fit.csv`): (a) δ for every cell × k with the interval; (b) the contrast table; (c) T tiers; (d) dropped fits and duplicates resolved. **Three headline lines, fixed now (no other result is headlined):**
  **P1** δ(ovl, 2,500, 1, 3, k = 16) on the 10 overlap datasets (must reproduce −0.00394; it is the continuity check);
  **P2** the R′ slope: δ(ovl, k = 4) → δ(ovl, k = 16) on the 10 overlap datasets, and δ(prec, 2,500, 1, 3, k = 4 … 64) on the 3 leg datasets, each next to the Jensen prediction;
  **P3** the three knob contrasts (m, I_max, N) at k = 64 on the 3 datasets.

### 4.4 How the result may be read (declared in advance; no post-hoc reading)
- *If δ is the same at k = 4 and k = 64 within the Jensen term and the knob contrasts include 0:* the offset is **not** a finite-R′, finite-N, grid or calibration effect at these settings; it is either noise or a difference between the V and T arms that none of the studied knobs changes (the arms differ in the kernel arithmetic, the calibration rule, N, R′, escalation).
- *If the R′ slope departs from the Jensen prediction by more than its interval:* the pooled estimator has an R′-dependent bias beyond the log-of-mean term.
- *A knob contrast whose interval excludes 0* is a FINDING (§3.3): the log Ẑ of V moves with a tuning knob although each Ẑ_r is unbiased for a frozen grid; it goes to HQ and Theory. With 3 contrast families the expected number of false flags at 5 % is ≈ 0.15–0.3; the report states it.
- No statement of the form "V is biased low" is made from δ alone: no truth for log Z exists, and T carries its own noise and tier effect.

### 4.5 Resolution (so the measurement is not over-read)
T̄_d has se s_T/√2 ≈ 0.0023; a V fit's log Ẑ at R′ = 64 has sd ≈ 0.003 (seed-to-seed at R′ = 16 is 0.0058, /2 for 64 islands); a precision cell (2 replicates) ≈ 0.002. A dataset offset therefore has se ≈ 0.003, and **3 datasets with t(2) = 4.30 give a 95 % half-width of ≈ 0.008: the leg's 3-dataset cells can only resolve an offset roughly twice the overlap's −0.0039.** The R′ slope and the knob contrasts do not carry the T noise (it cancels) and are far tighter; the 10-dataset overlap cell has df 9 (half-width 0.003). A third T replicate would sharpen the V − T level; it is not in this leg.

## 5. The 10⁴ science: what it reports (per the spec; descriptive; no pass/fail except completion)
Cells: `LEG_PLAN.md` §2.2; **run in the frozen configuration** (§3.3). Conventions (MANIFEST_CELLS §4): dataset-clustered intervals everywhere; method differences on paired datasets and seeds; the PIP reliability curve is a repeated-sampling diagnostic under a fixed truth (active / null counts, bin counts, clustered uncertainty); the store law's omitted mass is reported with every distance.
| spec item | what is reported per cell (design × n) |
|---|---|
| **C2** reported model = S₀ | P̂(HPM = S₀), outcome class counts (posterior / search / correct), Hamming, TP/FP of HPM and MPM; the provenance phase of the HPM |
| **C4** PIP consistency | sup_{j∉S₀} PIP, min_{j∈S₀} PIP (equal-weight primary and PIP_Z), P̂(MPM = S₀), Brier, #null with PIP > 0.1 / 0.5, pooled reliability curve for the AR-weak arm (bins 0.05–0.95) |
| **C5** distribution | d_H² of the HPM / MPM plug-ins (closed form), store-BMA predictive d_H², n·d_H², n·d_H²/(s₀ log p), the fitted slope of log d_H² on log n with a dataset-clustered bootstrap interval, ratios to the oracle, posterior quantiles of d_H, test MSE and mean log predictive density on 10⁴ fresh rows |
| **C7** evidence / merge | σ̂(log Ẑ_r) and robust σ̂, max − median, R_eff/R′, max_j \|PIP_Z − PIP_eq\|, log Ẑ against log Z_T (omitted mass), `grid_unconverged` / E1–E3 / `occ_inhomogeneous` frequencies (V has no escalation: the frequency input to OD-2 / G-B) |
| **A3** exact vs truncated | the 15 pairs (paired by dataset and seed): HPM equality, max_j \|ΔPIP\|, Δ log Ẑ, d_H, cost; **π₀(S₀) not available (B4)** |
| second seed | AR n = 200, seeds 1 and 2 on 10 datasets: seed-to-seed agreement of HPM, PIP, log Ẑ (the yardstick for every other V comparison) |
| null control | NULL n = 200: `n_null_gt_0.5 = 0` in every fit (reported; a violation is stated, not a stop) |
| **cost** | billed core-h per fit by design and n (the n-scaling the quote assumed, now measured: feeds the 10⁵ / 10⁶ re-size), peak RSS per stage, wall per stage, against the class models |
| **G-B inputs** | completion %, cost per fit against the model, memory against the request, flag frequencies (EXPERIMENT_PLAN §2.3 G-B); the 10⁵ pilot itself is not in this leg |
**The science analysis script is not written yet.** It is registered by a short addendum (script, sha256, self-test on synthetic records) **before the first science read-back (S1)**, as the overlap did; its thresholds, if any, are none: this block has no pass/fail rule other than completion (§2).

## 6. Leg outcome and review
1. After A0, after each wave and at FZ: the manager's read-back against the stops (LEG_PLAN §5.3), ≤ 10 lines.
2. **FZ:** both registered scripts run on the 18 precision fits (script shas verified first); `freeze.json`, `offset.json`, `offset_report.md` saved unedited next to this file; one Opus child reviews the code, the tables and the rule's output against this file (the review is a separate human-style step, as `OVERLAP_1e4_PREREG` §4 rule 5); HQ informed.
3. **Leg report** after S9 (≤ 12 lines) + one Opus review of the science read-back against §5; G-A closes with: precision COMPLETE (§3.3), science completion ≥ 95 % (§2), the frozen configuration recorded by hash.
4. A stop rule of LEG_PLAN §5.3 → stop submitting and tell HQ (soft per-fit trips are report-and-continue as pre-declared there).

## 7. Disclosures, limits, fields not verified
- **What I looked at on real data before registering.** (i) The overlap records for parsing and cost (`measured_V_costs.csv`, island T, stage costs). (ii) **`precision_offset.py --only-full` on the 40 overlap records, as a reader check:** it printed δ(ovl, 2,500, 1, 3, k = 16) = **−0.00394**, CI −0.00712…−0.00076, 7/10 negative, s_T = 0.00324 (all equal to the published verdict values), and, in the same row, the sensitivity with the tier-0 T fits only, **−0.00431 (10 datasets)**, the Jensen mean −1.5 × 10⁻⁵ and the log Ẑ_occ offset +0.00029 (`reader_check_output.txt`). (iii) Nothing else of the surface: **no R′ subset (k = 4, 8), no contrast and no precision fit exists or was computed on real data**; the full-k code path was tested on synthetic records only.
- **Fields I could not verify:** (a) per-island best model (§3.1); (b) the `occ` list and `sd_log_Z_occ_r` exist in the overlap V records (inspected) and `fit.meta.occ` parsed for both arms by the reader check, but their definition rests on the engine's D-13 wording: log Ẑ_occ is "consistent in N, no theorem yet"; (c) `calib.bin.json` is a collected unit in the overlap (checked on W0, W3) and must be in this leg's collection list (LEG_PLAN §6.5); (d) the cost files are read by `precision_freeze.py` from `cost_<run_id>.json` (stage `islands`), as written by `p1m_cost.py`; (e) run-dir discovery skips `_batch_*`, `manifests`, `scripts`, `cost`, `log`, and requires an `evidence` block: a driver manifest named `eval.json` is not an eval record (a flaw a first draft of the discovery had, caught on the real tree).
- **Known limits of the design:** 3 datasets for the leg's cells (§4.5); T reference with a tier-1 mixture on two of the three datasets; V and T differ in several respects at once, so no single cause can be assigned from δ; the overlap T and V arms both used the truncated partition (LEG_PLAN §1.2 observation); the n-scaling and R′ = 64 merge costs are quoted, not measured, until A0 / S6 / S8.
- **Choices I fixed that HQ or the reviewer may overrule before the commit** (each is one line in a script constant): the freeze thresholds (1/√c_X; 1.15; 1.30), M = 1,000 for the occupancy sd, equal dataset weights, disjoint consecutive blocks (not random subsets), the 95 % t interval with dataset clusters, the FINDING definition.

## 8. Deviation log
None. A change to any threshold, rule, field choice or script after the shas above are committed is a logged deviation with the reason, the date and the new sha256.
