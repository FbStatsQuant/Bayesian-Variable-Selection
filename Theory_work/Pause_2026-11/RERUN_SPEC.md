# RERUN_SPEC: re-running the PROD-H SMC-BVS study (2,400 fits) on v3.1 / v3.2

Prepared 2026-11-10 by the research sub-agent. This spec only prepares the rerun. Nothing was run or submitted, there was no ssh, and no code, config or git state was changed.

**Abbreviations.** CAMP = `Scripts/Campaigns/2026-10-28_New_Campaign`. OLD = `CAMP/code/core/v2_2_1/core` (frozen v2.2.1). NEW = `Scripts/SMC_BVS/core` (v3.1). NEW is byte-equal to merge `4676af6`: `git diff 4676af6 HEAD -- Scripts/SMC_BVS/core` is empty, and 72785fe, the last core commit, is an ancestor of 4676af6. RES = `Results/2026-10-28_New_Campaign/H2_20261102`.

Every claim below cites a file. "UNVERIFIED" marks claims I could not check.

---

## 0. Bottom line

1. **Yes, the published study uses `pip_plain`.** HEADLINE_H has a row "SMC-BVS MPM (plain PIP > 0.5)" (`RES/HEADLINE_H.md:11,29,46,65,114,123–127`). EVIDENCE_H has a section on RB vs plain (`RES/EVIDENCE_H.md:29,194–197`; table `RES/tables/ev_pip_rb_plain.csv`). The tie-out claims also use it (`CAMP/analysis/H2_20261102/scripts/make_claims_h2.py:24,46–47`). v3.1 emits none of `pip_plain`, `pip_plain_r` or `mpm_plain`.
2. **Other study outputs also depend on fields v3.1 removed** (the v2.2 `fit$instrumentation` block and the scored-model registry):
   - the **cost table** (`ev_cost.csv`: distinct-model HLL column);
   - **EVIDENCE §8** (registry);
   - the **start-mass analysis** (T27: `n_stages_final`, inside `log_Qf`);
   - the **stop records** (`ev_stops.csv`);
   - before/after-local diagnostics.

   Section 2 says which of these can be derived from v3.1 output and which need code restored.
3. **The algorithmic diff is confirmed.** It is LS0, the TDP tie fallback, the tier-1 grid fallback and the LS0 preflight term. v3.1 also **removes** the v2.2 study instrumentation: plain PIPs, the registry and `instrumentation`.
   - Nothing changes the islands. `v3_score.h`, `v3_blocks.h`, `v3_calib.h`, `v3_util.h`, `v3_holder.h`, `v3_setup.R`, `v3_preprocess.R`, `v3_exact.R` and `v3.R` are byte-identical (CR stripped).
   - Expected under v3.1: bit-identical Ẑ, island Ẑ, RB PIPs and MPM, and an HPM with F_new ≥ F_old.
4. **Four comparability hazards** (§6):
   - **(H1)** The new LS0 preflight term can refuse fits at the PROD-H allocations (p500: 1.75 h). Its worst case was measured at 1.2–1.9 h at p = 500.
   - **(H2)** `local_limit` and `local_certified` change meaning, which changes `diag_flag`.
   - **(H3)** The v2.2.1 study adapter turns every v3.1 non-completed fit into an adapter error.
   - **(H4)** `score_counts` gains an `ls0` row, so the fresh-score totals shift.

---

## 1. Study grid (as run in PROD-H, run `20261030T0934Z_prodH`)

| Item | Value | Source |
|---|---|---|
| n | 200 | `RES/HEADLINE_H.md:3`; `ops/PRODH_COMPLETION_20261102.md:3` |
| p | 500, 1000 | `CAMP/conformance/jobs/PROD_H/JOB.md:7` |
| Designs | S1 independent; S2 AR(1) 0.5^\|j−k\|; S3 0.7H+0.3I; S4 0.85H+0.15I; S5 0.3J+0.4H+0.3I; S6 heterogeneous blocks ρ_b = 0.4+0.1((b−1) mod 6). Population blocks of 5 | `Docs/Methodology/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md:648–666` |
| s0 / truth | 14 signals; β = (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) cycled. Active p500: 3, 37, 74, 106, 145, 178, 213, 247, 284, 316, 355, 388, 423, 457. Active p1000: 3, 67, 134, 196, 265, 328, 393, 457, 524, 586, 655, 718, 783, 847 | MASTER `:621–646` |
| Signal | y_c = c·Xβ + ε, σ = 1, no intercept. c ∈ {1.00 (`c100`), 0.50 (`c050`)}, both scales on the same X and ε (paired). Nominal SNR at c = 1: 24.64 (S5: 17.44) | MASTER `:609–620, 667–686`; `PROD_H/JOB.md:7` |
| Reps | r001–r100 per (p, S) → 1,200 datasets × 2 scales = **2,400 fits** | `PROD_H/tables/units.tsv` (2,400 rows, 100 per p×S×c, checked by awk) |
| Data seed | 1,000,000 + 10,000·S + r + base offset: **p500 base 1,410,000, p1000 base 1,510,000**. Examples: p500 S1 r001 = 1,420,001; p1000 S6 r001 = 1,570,001 | MASTER `:704–716`; `units.tsv`; `OLD/../study/adapter.R:78–85` |
| Method seed | data seed + 4,000,000; the same for c100 and c050 | `units.tsv` (method − data = 4,000,000 in all rows); `adapter.R:120`; `PROD_H/JOB.md:7` |
| Inputs | NOTS `/projects/ml75/fb31/BVS/bench20261019` (`manifests/inputs_manifest.csv`, `inputs/p0500\|p1000/*.rds`). Local copy: `C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/inputs` | `PROD_H/JOB.md:12`; `analysis/H2_20261102/scripts/theory_runner.R:7`. That the NOTS tree still exists is **UNVERIFIED** (no ssh); `Docs/Records/DATA_INDEX.md` says the "benchmark-freeze trees are untouched" |
| Allocation | p500 `--hours 1.75` (L = 6,300 s), p1000 `--hours 6.666666667` (L = 24,000 s), `--mem-gb 2` | `PROD_H/JOB.md:16,194` |
| Environment | NOTS commons, `--constraint=sapphirerapids`, GCC/14.3.0, R/4.5.2, one thread | `PROD_H/JOB.md:13,18` |
| Old outcome | 2,394 completed (202 escalated) + 6 `resource_limit`: all S5, all escalated; 5 at p1000, 1 at p500 | `ops/PRODH_COMPLETION_20261102.md:9–26` |
| Old records | OneDrive "NOTS Data/New_Campaign/results/20261030T0934Z_prodH/{p0500,p1000}/<case>/SMCBVS.rds". Manifests p0500 `7893396c…`, p1000 `a0196198…` | `Docs/Records/DATA_INDEX.md:9,19`; `analysis/H2_20261102/scripts/make_lists.R:9` |

Benchmarks are not rerun. Their rows in HEADLINE_H come from separate fits (`RES/HEADLINE_H.md:16–21`).

---

## 2. Fields: what the analysis consumed, and whether v3.1 emits it

The analysis reads records only through `CAMP/code/scoring/R/extract_smc.R` (FIELD_MAP: `CAMP/code/scoring/FIELD_MAP.md`) and through direct reads in `analysis/H2_20261102/scripts/extract_h2.R:36–80`. The downstream consumers are `combine_h2.py`, `evidence_h2.py`, `build_headline_h2.py` and `make_claims_h2.py`.

### 2a. Emitted by v3.1 with the same meaning (no action)
- `native_status`, `estimates_available`, `runtime_s`, `method_seed`.
- `fit$log_Z`, `log_Z_r`, `log_Z_lower95`, `log_Z_rel_m0`, `log_m0`.
- `fit$pip_primary`: still the equal-weight island mean (`NEW/v3_run.R:162`).
- `fit$pip_r`, `fit$mpm` (`NEW/v3_run.R:163`), `fit$hpm`, `fit$hpm_F`, `fit$hpm_provenance`.
- `fit$preprocessing$kept`, `fit$blocks`, `fit$stage_table` (`min_ess`).
- `fit$flags$E1/E2/escalated/grid_unconverged/low_empirical_ESS/near_tie_truncated/checks_passed_final`.
- `fit$cut_group`, `fit$settings$tier`, `fit$timings$*`, `fit$hpm_before_local` (`NEW/v3_run.R:209`).
- `fit$local_search`, i.e. the *final* search (`NEW/v3_run.R:129–131`).

  These are not in the OLD→NEW diff (diffs of `v3_run.R` and `v3_fit.R`; §3).

### 2b. Emitted by v3.1 with a different meaning (re-derive on the old meaning)

| Field (consumer) | v2.2.1 | v3.1 | Substitute |
|---|---|---|---|
| `fit$flags$E3` | `hpm_F > hb$F` (`OLD/v3_run.R:151`) | `hpm_before_ls0$F > hb$F` (`NEW/v3_run.R:191`) | Same numbers by design: E3 excludes LS0 |
| `fit$local_limit`, `flags$local_limit` → adapter `diag_flag` (`adapter.R:141,268–289`) | final search only | final **or LS0** (`NEW/v3_run.R:197`) | Use `fit$final_local_limit` for the old meaning; report `ls0_local_limit` separately |
| `fit$local_certified` → adapter `local_certified_false` code (`adapter.R:295`) | final search | final **or LS0** (`NEW/v3_run.R:193–195`) | Use `local_certified_by %in% c("final","both")` |
| `fit$score_counts$fresh/logical` (`score_fresh_total`, `fresh_ph_*`; `ev_cost.csv`) | 10 phase rows | adds an `ls0` row (`NEW/cpp/v3_core.cpp` `counter_matrix(..., include_ls0)`) | Total = old total + `ls0` row; compare after excluding `ls0` |
| `fit$hpm`, `hpm_F`, `hpm_provenance` | best after final search | best after LS0 (provenance may be `ls0`) | Old-meaning HPM = `fit$hpm_before_ls0` |
| `runtime_s`, `t_total` | — | + LS0 time + LS0 preflight timing benchmark | Negligible: LS0 median 0.17 s (p500) and 0.37 s (p1000) post hoc (`Theory_work/Old_Projects/New_BVS_Headquarters/03_results_and_conclusions.md:188`) |

### 2c. NOT emitted by v3.1

| Field | Where v2.2.1 made it | Analysis use | Derivable from v3.1? |
|---|---|---|---|
| `fit$pip_plain`, `pip_plain_r`, `mpm_plain`; `record$pip_plain`, `mpm_plain` | `OLD/cpp/v3_engine.h:360,371`; `OLD/v3_run.R:167–169`; `adapter.R:524–525` | HEADLINE row "MPM (plain)"; EVIDENCE §7; `ev_pip_rb_plain.csv`; claims `make_claims_h2.py:46–47`; `extract_h2.R:38–56`; `extract_smc.R:13,23,132–168`; `metrics_smc.R:55–110`; `tables.R:11,54–99` | **No.** The particle inclusion counts are not exported. Needs `plain_acc` restored in the engine (pure bookkeeping, no RNG) |
| `instrumentation$scored` (registry: `mode`, `n_distinct_hll`, `after_calibration`, `log_sum_exp_F`, `first_scored`) | `OLD/cpp/v3_registry.h` (deleted in NEW); `OLD/v3_fit.R:88–91,144` | `ev_cost.csv` `distinct_hll_*`; EVIDENCE §8 (`RES/EVIDENCE_H.md:202–205`) and the "×2^1.5 distinct models" line (`:115`); claims `make_claims_h2.py:39–40` | **No.** Needs `v3_registry.h` and its ledger hook restored (`OLD/cpp/v3_ledger.h` `reg->insert`) |
| `instrumentation$stages$final` (`n_stages_final`) | `OLD/v3_fit.R:66–70` (= `length(fit$grid) − 1`) | `log_Qf = log(4 N_e (n_stages_final + 8 + 5))` (`evidence_h2.py:42`) → T27 start-mass result (`RES/EVIDENCE_H.md:23,37–44`) | **Yes, exactly:** `length(fit$grid) − 1` |
| `instrumentation$best_before_local` / `best_after_local` / `changed` | `OLD/v3_fit.R:72–75` | `before/after_local_eq_truth`, `local_changed` (`extract_h2.R:76–78`; `evidence_h2.py:35–36`; `combine_h2.py:66`) | **Yes:** before = `fit$hpm_before_local`; after (old meaning) = `fit$hpm_before_ls0` |
| `instrumentation$stop` | `OLD/v3_fit.R:76–82` | `stop_present`, `stop_*` → `ev_stops.csv`, EVIDENCE §5 (`evidence_h2.py:114–116`) | **Yes:** the same code over `fit$preflight$exceeds`, `fit$calibration$escalation_blocked` and `fit$runtime_guard$checkpoints` (all still emitted) |
| `instrumentation$escalation`, `cut_group_large`, `version` | `OLD/v3_fit.R:83–87` | `escalation_reasons`, `ins_version` extracted but not used downstream (grep of `analysis/H2_20261102/scripts/*.py`) | Yes (from `fit$calibration$flags$triggers_by_tier`; `cut_group_components` and `B`) |
| `instrumentation$scored_set`, `log_mass_scored`, truth trace | `OLD/v3_fit.R:90` (p ≤ 32 only) | Theory rows (`code/scoring/R/theory_measures.R:77–140`); **NA at p ≥ 500 by design** (`RES/EVIDENCE_H.md:149`) | Not needed for PROD-H |

**Not affected:** the theory runner reads only `sm$blocks`, `sm$hpm`, `sm$ok` and `sm$log_mass_scored` (NA at H) (`code/scoring/run_theory_H.R:15–21`; `R/theory_measures.R`).

**Outside this rerun's scope:** PROD-L (low p, also v2.2.1) uses plain PIPs in its headline too (`CAMP/analysis/L_20261102/scripts/render_headline.py:30,63,87,130–133`; `build_tables.py:63–150`).

---

## 3. Verified v2.2.1 → v3.1 differences (CR-stripped diff of OLD vs NEW)

| File | Changed lines | Content |
|---|---|---|
| `v3_score.h`, `v3_blocks.h`, `v3_calib.h`, `v3_util.h`, `v3_holder.h`, `Makevars.v3`, `v3.R`, `v3_setup.R`, `v3_preprocess.R`, `v3_exact.R`, `source_manifest.json` | **0** | Identical |
| `cpp/v3_registry.h` | only in OLD | Scored-model registry (v2.2 instrumentation) removed |
| `cpp/v3_start.h` (83) | `start_mode` refactored into `mode_dp` + the new `mode_tie_dp`. The tie-DP runs only when the enumeration is truncated (≥ 1e6 ties) and `tie_dp` is set (`NEW/cpp/v3_start.h:303`). `start_mode` is **called only by LS0** (`NEW/cpp/v3_core.cpp:469`). OLD defines it but never calls it (grep). So TDP cannot affect the islands |
| `cpp/v3_engine.h` (16) | Plain-PIP accumulation removed (`OLD:360,371`). `local_search` gains a `phase` argument (PH_LS0) |
| `cpp/v3_ledger.h` (10) | `PH_LS0` appended last (other phase indices unchanged); registry hook removed |
| `cpp/v3_runtime.h` (4) | `local_event` gains a phase argument |
| `cpp/v3_core.cpp` (101) | Registry exports removed; island list drops `pip_plain/plain_acc/plain_round`. LS0 block (`:457–480`): runs after the final local search when status is completed, reads no uniforms, shares the ledger and cache, cap ℓ_n + \|S̃₀\|. **The runtime guard is checked after LS0, and a stop there sets `resource_limit`** (`:480`) |
| `v3_run.R` (65) | LS0 settings; `v3_unavailable_estimates` (estimate fields set to NA on non-completed returns, `:109–116,147`). E3, `local_certified`, `local_limit`, `ls0_improved`, `ls0_hpm_changed` (`:186–207`). Plain PIPs removed |
| `v3_calib.R` (26) | Tier-1 grid fallback, instead of `schedule_limit` (`grid_fallback`). Unchanged when v2.2.1 did not return `schedule_limit`; PROD-H had none (`PRODH_COMPLETION:9–15`) |
| `v3_fit.R` (80) | LS0 worst-case preflight (`:26–66,115,145`); the instrumentation block is removed (`OLD:61–92`); `keep_scored_set` argument removed; `ls0 = getOption("v3.ls0", TRUE)` (`:73`); `ls0 = FALSE` reproduces v3 |

**Prior evidence that the islands are unchanged with LS0 on:**
- `Theory_work/Wave1C/C-ENG/REPORT.md:155–186`: p = 30 regression 48/48 identical for Ẑ, PIPs, MPM, streams and island bests; three p = 500 replays at 16/16 each.
- LS0 post hoc on all PROD-H fits: improvement in **0 / 2,394** fits, smallest margin 0.002 nats (`03_results_and_conclusions.md:186–188`).

  That post hoc run used cap ℓ_n. The shipped cap ℓ_n + \|S̃₀\| can only add moves, so the HPM is the same or higher. Whether any HPM actually changes under the larger cap is **UNVERIFIED**.

---

## 4. Metrics

**Primary (as published).** Exact recovery against S₀ (selected set = S₀) per p × S × c cell (/100) and pooled (/600) for:
- SMC-BVS **HPM** (primary);
- **MPM-RB** (strict PIP > 0.5 on `pip_primary`);
- **MPM-plain** (only if plain PIPs are restored).

Failed fits count as misses (`RES/HEADLINE_H.md:3,27–29`).

**Secondary:**
- FP/FN/k of the HPM;
- status counts (completed / escalated / resource_limit);
- `runtime_s` medians and p90;
- fresh scores, excluding `ls0`;
- `diag_flag` rates under the old meaning;
- HPM provenance;
- LS0 fields (`ls0_improved`, `ls0_hpm_changed`, `ls0_local_limit`, `start_mode$ties/truncated/tie_dp_used`);
- start-mass `log_Qf`;
- miss classes;
- stops.

---

## 5. Paired-by-seed comparison and acceptance criteria

Pairing: `case_id` = `p{p}_S{s}_r{rrr}_{c100|c050}`, with the same input `.rds` and the same `method_seed` as in `units.tsv`. Every comparison is new vs old **record**, per case.

### 5a. v3.1 (deterministic, so exact criteria)

v3.1 only adds a post-island, uniform-free LS0. Every criterion is therefore an identity, not a Monte Carlo band. The precondition is the same NOTS environment (sapphirerapids, GCC 14.3.0, R 4.5.2, 1 thread). That this environment gives bit-identical floating point was established for v2.2 by CONF_NOTS_IDENTITY (`CAMP/README.md` table; D20).

| # | Criterion (over all cases completed on both sides) | Tolerance |
|---|---|---|
| A1 | `log_Z`, `log_Z_r`, `log_Z_lower95`, `pip_primary`, `pip_r`, `mpm`, `stage_table`, `fit$grid`, `settings$tier`, `flags$E1/E2/E3/low_empirical_ESS/escalated` | `identical()`; max \|diff\| = **0** |
| A2 | HPM score: `hpm_F_new ≥ hpm_F_old`, compared as doubles | **0 violations** |
| A3 | `hpm_before_ls0_new == hpm_old` (model and F) | 0 violations |
| A4 | Where `hpm_new ≠ hpm_old`: `ls0_improved` is TRUE or it is an equal-F tie (`ls0_hpm_changed`), and provenance phase = `ls0` | Every such case is listed. Expected count 0 (§3) |
| A5 | Status: old completed ⇒ new completed | **0 new `resource_limit`** (see H1), else listed |
| A6 | The 6 old `resource_limit` fits: the new ones are also `resource_limit` | Expected; their estimate fields are NA by design (`NEW/v3_run.R:109–116`) |
| A7 | Recovery counts per cell (HPM, MPM-RB) | **Identical** to `RES/HEADLINE_H.md:44–65`, or higher for HPM only through A4 cases |
| A8 | `score_counts` rows other than `ls0` | identical |
| A9 | MPM-plain (only if restored) | `identical()` to the old `pip_plain` |

A check of the same kind already passed for v2.2.1 vs v2.1: 882/882 fields identical (`ops/PRODH_COMPLETION_20261102.md:53–55`).

### 5b. v3.2 (parallel; Monte Carlo criteria apply only if the island random streams change)

If v3.2 keeps the v3.1 streams and arithmetic, §5a applies unchanged. That has to be declared in its CHANGES file before the run; v3.2's design is **UNVERIFIED** (no v3.2 document found). If v3.2 changes the random draws, use the criteria below:

| # | Criterion | Threshold |
|---|---|---|
| B1 | Per cell (24 cells, n = 100 paired): exact McNemar test on HPM recovery (discordant pairs) | Holm-adjusted p > 0.05 in every cell, **and** pooled /600 change ≥ −2 points (−12 fits) per p × c pool. Monte Carlo SE of a cell rate ≈ 3 points at 0.9 |
| B2 | Same for MPM-RB | Same |
| B3 | Evidence: z = (logZ_new − logZ_old) / sqrt(se_new² + se_old²), with se = sd(log_Z_r)/2 | \|z\| ≤ 4 in ≥ 99% of fits; median z within ±0.5 |
| B4 | PIPs: max_j \|PIP_new − PIP_old\| ≤ max(0.02, 4·sqrt(se²_new,j + se²_old,j)), se_j = sd(pip_r[j,])/2 | ≥ 99% of fits; MPM-RB sets equal in ≥ 98% of fits |
| B5 | HPM score: F_new ≥ F_old − 1e-8 | ≥ 99% of fits; every lower case listed, and none may lose a recovery without a matching gain elsewhere in the same cell |
| B6 | Status | New resource_limit ≤ old + 2, all listed |

---

## 6. Hazards to comparability

- **H1. The LS0 preflight can refuse fits at the old allocations.**
  - v3.1 charges 2·(ℓ_n+K+1)·(p+p²/4)·ŝ_K seconds against `hours` (`NEW/v3_fit.R:43–46,65`), in both the initial and the escalation preflight (`:115,145`).
  - Measured worst cases: **1.2–1.9 h at p = 500 and 4.8–6.7 h at p = 1000** (Windows) (`Theory_work/Wave1C/C-ENG/REPORT.md:76–78`). The PROD-H allocations are **1.75 h and 6.667 h** (`PROD_H/JOB.md:16`).
  - The C-ENG test of "0 newly refused" used 24 h allocations (REPORT `:76`). How ŝ_K behaves on sapphirerapids is **UNVERIFIED**.
  - A refused fit stops at preflight with no output, and would be scored as a miss that v2.2.1 recovered.

  **Remedy (HQ choice; record it before the run):**
  - (i) Gate 0 (§8) runs the preflight alone for all 2,400 cases on NOTS with the PROD-H allocations.
  - (ii) If any case is refused, either rerun with `options(v3.ls0_cap = "ell_n")`, which restores the shipped preflight but changes the LS0 cap (method change, disclose), or raise `hours`.
  - Raising `hours` also moves the runtime guard (`NEW/cpp/v3_core.cpp` `cpp_runtime_new`). The 6 S5 guard stops might then complete, so report them separately.
- **H2. Flag semantics.** `local_limit` and `local_certified` now include LS0 (`NEW/v3_run.R:193–197`). The adapter's `diag_flag` uses `local_limit` (`adapter.R:141,287–289`), so flag-rate tables are not comparable. In the C-ENG replay, LS0 hit its move cap in S5 (REPORT `:179–181`). Re-derive the old meaning from `final_local_limit` and `local_certified_by`.
- **H3. The v2.2.1 adapter breaks on v3.1 non-completed fits.**
  - v3.1 sets `mpm` and `pip_primary` to `NA` on such returns (`NEW/v3_run.R:109–116`; `NEW/v3_fit.R:85`).
  - The adapter then calls `smcbvs_check_support(NA)`, which stops with "invalid original-index MPM" (`adapter.R:218–222,233`). The `!is.null(fit$pip_primary)` branch also stops (`adapter.R:237–246`).
  - Result: all 6 S5 stops (and any H1 refusals) would become `adapter_error`. Found by reading the code, **not executed**.

  A study adapter v3.x-R1 is required. It must treat a non-completed fit carrying NA fields as unavailable. Nothing else in it changes.
- **H4. Score totals.** The `ls0` counter row adds to `score_fresh_total` and `fresh_ph_*` (`NEW/cpp/v3_core.cpp` `counter_matrix`). Exclude it in the cost comparison.
- **H5. LS0 run time can trigger the guard.** A fit that finished within L − ε under v2.2.1 can stop at the post-LS0 guard check (`v3_core.cpp:480`). LS0 costs under 1 s typically, so the risk is limited to fits within about a second of L.
- **H6. Instrumentation not restored** means the plain-MPM row, `ev_pip_rb_plain.csv`, the registry section and the distinct-model cost column cannot be reproduced (§2c). Either restore them (§7) or drop them from the new report with a note.
- **H7. Environment drift.** Bit-identity (§5a) depends on the same toolchain and node type. NOTS module changes since 2026-10-30 are **UNVERIFIED**. Gate 0 detects drift.
- **H8. Allocation encoding.** The adapter hashes the `--hours` string into the unit identity (`PROD_H/JOB.md:194`). Use the identical strings `1.75` and `6.666666667` unless H1 forces a change.

---

## 7. Instrumentation to restore or substitute (study build only, never in production)

| Item | Action | Cost / risk |
|---|---|---|
| Plain PIPs (`pip_plain`, `pip_plain_r`, `mpm_plain`) | **Restore** as an opt-in study patch: port `plain_acc`/`plain_round` (`OLD/cpp/v3_engine.h:349–371`), the island export (`OLD/cpp/v3_core.cpp` `island_to_list`) and the assembly (`OLD/v3_run.R:167–169`). Gate it behind an option so production output is unchanged. **Alternative:** drop the row. It is secondary, and RB and plain agreed in 2,391/2,394 fits, max \|Δ\| 0.0067 (`RES/EVIDENCE_H.md:195–196`) | Counting only, no RNG use. Must be shown bit-neutral to A1 |
| Registry (HLL distinct counts) | **Restore** `v3_registry.h` + the ledger hook + exports (`OLD/cpp/v3_ledger.h`, `OLD/cpp/v3_core.cpp` `cpp_registry_*`, `OLD/v3_fit.R:144`, calibration snapshot). Under v3.1, decide whether `ls0` rows enter the count; recommendation: report the count with and without LS0. **Alternative:** drop EVIDENCE §8 and the distinct-model column | Memory and time overhead as in v2.2 |
| `n_stages_final` | Substitute `length(fit$grid) − 1` | Exact |
| `best_before_local` / `best_after_local` | Substitute `fit$hpm_before_local` and `fit$hpm_before_ls0` | Exact |
| `stop` record | Substitute: port `OLD/v3_fit.R:76–82` into the extractor | Exact |
| `escalation$reasons`, `cut_group_large` | Substitute from `calibration$flags$triggers_by_tier` and `cut_group_components`/`B` | Exact |
| Scoring extractor | Add v3.1 paths to `FIELD_MAP` (`extract_smc.R`); treat NA estimate fields as unavailable; read `final_local_limit` | — |

Any restored code is a new frozen study core (e.g. v3.1-study / v3.2-study). It needs its own SHA256SUMS, a CODE_LEDGER entry and a Sol review (`CAMP/README.md` "Rules for this code").

---

## 8. NOTS job plan (draft; do not submit)

Model it on `CAMP/conformance/jobs/PROD_H` (runner/, `submit.sh`, `reconcile.py`, `final_accounting.sh`). Only the code path, the adapter and the run ID change.

| Stage | Layout | Resources | Notes |
|---|---|---|---|
| Gate 0a: identity | 1 array of 126 units: p × S × r ∈ {1,25,50,75,100} × c, plus the 6 old stops (the `prodh_repro_check` grid, `PRODH_COMPLETION:53`) | 1 CPU, 2G, same walls | Run each unit twice, with `ls0 = FALSE` and `ls0 = TRUE`. Pass = §5a A1–A8 on all 126, and with `ls0 = FALSE` also HPM identical to old |
| Gate 0b: preflight scan | 1 job: preflight only (`v3_preflight` with the PROD-H allocations) over the 2,400 cases | 1 CPU, 4G, ≤ 2 h (estimate; preflight includes a timing benchmark of 200 size-K scores) | Settles H1 before any full run |
| Precompile | 1 job | 1 CPU, 4G, 1 h | As before |
| Primary p1000 | array tasks 1–600, one dataset each (c100 then c050) | 1 CPU, `--mem=2G`, wall 13:42:00 | `%30` (D49 throttle) |
| Primary p500 | array tasks 601–1200 | 1 CPU, 2G, 03:52:00 | `%30`; ≤ 192 billed CPUs over all campaign arrays (D47) |
| Rerun / P5 | as JOB.md §3 E–F | — | P5 not run last time (D62); decide in advance |

**CPU estimate (v3.1).**
- Last run: **906.49 elapsed core-h = 1,812.98 billed CPU-h** (p500 225.82, p1000 680.67) (`ops/PRODH_COMPLETION_20261102.md:32`).
- LS0 adds well under 0.1% (`03_results_and_conclusions.md:188`). The preflight timing benchmark adds seconds per fit.
- Expected **≈ 910 core-h (≈ 1,820 billed)**, plus Gate 0a ≈ 2 × 126/2,400 × 906 ≈ **95 core-h**, plus Gate 0b ≤ 2 h.
- Requested-wall ceiling unchanged: **10,541 core-h** (`PROD_H/JOB.md:170`).
- Wall-clock last time: submitted 2026-10-30 09:36Z, reconciled 2026-11-02 (`PRODH_COMPLETION:3,5`). That includes queue time.

**v3.2.** If a fit uses T threads, set `--cpus-per-task=T` and scale `mem` by the per-thread buffers. Core-hours should be about the same or higher (parallel overhead), while wall time per fit falls about T-fold. The throttle must be re-derived so that tasks × T × 2 ≤ 192 billed CPUs. The thread count and the determinism of v3.2 are **UNVERIFIED**.

**Outputs.** Write to a new run ID `<STAMP>_prodH_v31` (or `_v32`). Never overwrite the old results; the comparison needs both.

---

## 9. Analysis steps after the run

1. Extract with the patched `extract_smc.R` (§7).
2. Run the paired comparison script, new vs old, applying §5a (or §5b) with the outputs `repro_summary.csv` and `mismatches.tsv`, in the same form as `extract_h2.R:18–34`.
3. Rebuild the HEADLINE and EVIDENCE tables from the same scripts (`build_headline_h2.py`, `evidence_h2.py`). Use the old-meaning substitutes from §2b–2c, and add one "v3.1 LS0" section (LS0 counts, ties, `tie_dp_used`, cap hits).
4. Tie out the claims as before (`make_claims_h2.py`).
5. Get a Sol review, then the council.
