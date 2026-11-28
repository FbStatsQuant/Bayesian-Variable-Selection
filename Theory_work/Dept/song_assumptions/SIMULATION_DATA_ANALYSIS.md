# SIMULATION DATA ANALYSIS — S1/S2 evidence for the TH-SONG assumptions

Computations: worker D1 (Sonnet 5.5), 2026-11-27, read-only on Engineering data; Lead synthesis, notes and E9: Task Lead (Opus 5.5). **v1.4 (senior review: completeness, generality and naturalness; see COUNCIL_RECORD.md and council/V14_CHANGESPEC.md).**

Mechanical data analysis for the Task Lead. No theorems are written here. Evidence against an assumption is reported as found.
Every number below is in a table under `tables/` (file named in the section) and is produced by a script under `scripts/`.

## Lead synthesis — what the data say about each target (read this first)

1. **TD (distribution).** d_H < ε_n in all 136 settings (median ratio 0.10–0.56; q90 ≤ 0.63; E7). S2 has
   little resolution (ε_n = 0.83). The cap never binds (E7), so K = n/2 costs nothing empirically.
   *Qualification:* E7 is a predictive-summary diagnostic. It reports across-replicate quantiles of a predictive distance at
   posterior-mean coefficients, with a different radius, and does not measure within-data posterior mass. It is consistent with TD, not a test of it.
2. **TS-b (exact selection) — the margin.**
   - *Necessity of the constant 2 is visible:* κ_del > 1 (equivalently min t² > 2·price) has sensitivity 1.000 on S1 and on
     S2 (population); the sample P1 check has sensitivity 0.985 on S2. When the check fails, exact recovery is 0 on both suites for the population κ_del ≤ 1 row, and 0/800 (S1) and 9/10,666 = 0.00084 (S2) for the sample P1 row. Consistent with the TS-b converse (which is a population/asymptotic statement; this is a per-setting check).
   - *S1 brackets κ = 1 from both sides:* κ_pop 0.64–0.70 at SNR 1 (0/100 exact in every cell) vs 2.54–2.80 at SNR 2
     (92–96/100) (E1, `e1_s1_cells.tsv`). The fixed-ratio (κ_n) framing covers S1's deletion classes (mixed classes: E9); a fixed beta-min (FSb) does not (E4).
     *Qualification:* E1's MPM recovery and its restricted-search κ do not test exact posterior mass or all active mixed classes.
   - *Multi-deletions bind on S1* (κ_multi < κ_del in all 16 settings): the margin must quantify over all D ⊆ S0 (E1).
   - *The "sufficiency gap" on S1 is consistent with the superset term:* 40/41 S1 failures at SNR ≥ 2 are S0 plus nulls
     (E1/E7). The heuristic diagnostic E K₁ ≈ (s0+1)/√(2πL(n+1)) (expected number of one-null extensions beating S0, idealised
     χ² scores; FABLE_R1 Q1(3f)) is 0.031–0.050 at S1's (n, p) by the displayed formula (0.033–0.056 under Fable's exact-Beta
     tail), the same order as the observed 2–8% shortfall; 39 of the 41 failures add exactly one null. This is
     **consistent with**, not a proved ceiling: P(K₁ ≥ 1) ≤ E K₁ bounds one failure type only (Astra R2 Q3). It is a mode-type
     diagnostic (rivals beating S0 in exact score, an HPM event; MPM failure is separate; Sol R2) and does **not** match the order of the TS-b mass-rate term (s0+1)√(log p/n), which is 0.87–1.44 at
     S1's sizes and therefore not informative there (Opus R1).
   - *U2a check (population form; Lead, `.rc_tmp/lead_v14/u2a_check.py`, no fits):* the minimum of R_n(B)/(2σ²Pr_n(d)) over
     all 1,023 D and over B = (S0∖D) ∪ (up to 2 inside proxies from the 5 nearest nulls) **equals the exact κ_n**. The binding D retain x_10,
     which screens every null. So (U2a) is no tighter than (U1) on S1 at these proxy sets:

     | cell | SNR 1 | SNR 2 | SNR 3 |
     |---|---|---|---|
     | (500, 500) | 0.653 | 2.613 | 5.878 |
     | (500, 5000) | 0.693 | 2.771 | 6.234 |
     | (1000, 500) | 0.626 | 2.505 | 5.635 |
     | (1000, 5000) | 0.670 | 2.679 | 6.028 |

   - *Leakage decay (AR(1), ρ = 0.6):* with Q_n = T plus the L_n nearest nulls, the outside leakage at distance k is
     ρ^{2k}(1−ρ²)/(1−ρ^{2k+2}) = 0.265, 0.087, 0.030, 0.011 (k = 1–4), so special case (ii) of the population form applies along the S1 sequence. Estimated on S1's AR(1) designs, not a property of correlated designs in general.
   - *The structure-free fallback* (ā ≡ 1, unit-vector bound): on the evaluated classes (d ≤ 3, selected D for d ≥ 2; m ≤ 2 at p = 500, m = 1 at p = 5,000) at η = 0, it fails at SNR 2 (minimum surplus −0.692 at d = 1, m = 1; −2.008 at m = 2) and holds at SNR 3 (minimum 1.412, d = 1, m = 2); m up to m̄_d is not evaluated (population computation on `tables/e9b_width_ext_s1.tsv` with the combinatorial width √(2 log C(p−s, m))).
   - *Mixed rivals (E9/E9b) are diagnostics of the refined design-conditional form only.* They are not diagnostics of the population form. On
     simulated S1 designs the estimated conditional width of the added nulls is 0.10–0.47 (m = 1) and 0.22–0.59 (m = 2), far below the worst-case
     √(2 log C(p−s0, m)) = 3.5–4.8. E9b's 3 D per (cell, d, m) are **selected examples** (chosen by population residual); four designs at zero slack
     establish no 1 − o(1) event. Exact minima over all evaluated classes, at δ = γ = t_n = 0 (never rounded upward): at SNR 2, 3.2896 (C = 1), 2.3862 (C = 121,
     a **sensitivity setting**, not an implied constant) and 2.4889 (no credit); at SNR 3, 5.8065 (C = 121). m = 2 at p = 5,000 and m ≥ 3 are not evaluated.
   - *Swap-aware heuristics are not improvements* (κ_pop AUC 0.958 vs κ_del 0.980 on S2): consistent with the advisors'
     finding that proxy swaps cost only a Gaussian-width allowance, not d·price (E1).
   - *S2 is not asymptotic* (s0 log p/n = 0.69); its transition is fitted by the saturating gain (n/2)log(1+R/(nσ²))
     (P(exact) = ½ at κ_adj_full ≈ 1.0–1.5 across both suites; post hoc). Used only in the finite-n diagnostics.
3. **Eigenvalues.** Population floors hold analytically (n × floor ≥ 8.8; slack relative to c_ψ/n is this divided by c_ψ); sample sparse floors are vacuous on
   S2 at the theorem's set sizes (1e−5–2e−4; E5). Supports dropping sample floors and keeping A-NEC.
4. **Bounded signal** holds everywhere (max |β|sd/σ ≈ 1.17 (1.175), ν ≤ 6; E4).
5. **Dimension.** A = 0.90–1.77; p ≤ n² everywhere incl. typical user regimes; log p/√n ≤ 0.98 (E6). Consistent with A-DIM
   (and with A-DIM′, though TD′ itself is a high-risk conjecture).
6. **Misspecification (TM).** σ² posterior vs σ_C²: median 0.99 (S1), 0.84–0.98 (S2) (E7). This illustrates variance inflation for a
   fitted (selected-MPM) subset and does not verify a prespecified-candidate theorem. Hidden-column tests need refits (not run; HQ approval required).
7. **SL's own conditions on our data.** SL Condition 3 holds in population (δ_SL = 0.23–0.42) but ε_n² = o(δ_SL) is weak/fails
   numerically (E3); SL Cor S1's κ_eff = log p/(log n)² is 0.13–0.22 on S1 (< ¼) and 0.33–0.45 on S2 (> ¼) (E6).

Caveat on evidence strength: S1 has two non-trivial SNR levels per cell, so the transition is bracketed, not located; all
"post hoc" items are flagged in the body. Cheap strengthening (needs fits, HQ approval): S1 at SNR 1.25/1.5.

---

## 0. Provenance, definitions, cost

**Sources (read only).**
- Engineering `…/_local/engineering/reports/S1S2/theory_checks/` (`P1.md`, `P2.md`, `p1_per_fit.tsv`, `p1_by_setting.tsv`, `p2_by_setting.tsv`, `p2_per_fit.tsv`, `p2_betabar_sparse.tsv.gz`, `cache/records.rds`), `diagnostics/bt2_diagnostic_per_rep.tsv`, `final/README.md`, `perf/` (E8).
- Harness `/home/fb31/BVS-wt/P1M/Experiments/S1S2/{harness/generate.R, specs/settings.tsv}`. Read-only copies are staged for Codex workers under `.rc_tmp/song/s1s2_ro/` (see its `SOURCES.md`).
- Theory's d_H table `Theory_work/Dept/prep/TH_PREP_support/E4E6/e4_dh_by_setting.tsv` (used only for the E7 re-tabulation).

**Population quantities.** β, support, Σ = AR(1)(ρ) and σ² come from `gen_beta`, `quad_ar1` and the σ² rule in `generate.R` (sourced verbatim; β is deterministic, so no seeds are needed). Σ has unit variance, so the standardised coefficient equals β.
- t²_j = nβ_j²/[(Σ_S0)⁻¹]_jj/σ² = R(S0∖j)/σ². R(S) = n·Var(xᵀβ | x_S) = n·β_Dᵀ Σ_{DD·S} β_D, D = S0∖S.
- **price = log((2p−1−s0)/s0) + ½ log(n+1)** is P1's price, kept for replication (range 7.60–10.36 nats over all settings). *Lead correction (council R1, Sol):* the exact last-variable price is price(s0−1) = log((2p−s0)/s0) + ½ log(n+1); P1's numerator is one off (difference log((2p−s0)/(2p−1−s0)) ≤ 0.002 nats), and the brief's price(s0) = log((2p−1−s0)/(s0+1)) + ½log(n+1) is *smaller*, not larger. The theorem's κ_n uses Pr_n(d) = Σ_{k=s0−d}^{s0−1} price(k) (adjacent prices); since price(k) decreases in k, κ_n ≤ the data κ = R/(2σ²·d·price), and over all 1,023 nonempty D the exact κ_n on S1 is 0.626–0.693 at SNR 1 and 2.505–2.771 at SNR 2, 1.1–1.7% below the restricted proxy (minimum at d = 6 for p = 500, d = 3 for p = 5,000; Sol R2, reproduced by the Lead); the S1 bracket (0.64–0.70 vs 2.54–2.80 for the proxy) is unchanged. On S1, κ_pop = κ_multi because κ_swap = κ_del.
- κ(S) = R(S)/(2σ² d·price), d = |S0∖S|. Λ(S) = ½R(S)/σ² − (d−m)·price − m·log p (m = |S∖S0| added nulls), the heuristic log posterior odds S0 : S.
- **Rival classes.**
  - Brief class (the column names without a suffix): deletions |D| ≤ 3 (exhaustive); swaps |D| ≤ 2 with N ⊆ nulls within distance 3 of D, |N| ≤ 4, chosen greedily. κ_del, κ_multi (|D| = 2, 3), κ_swap, κ_pop = min of the three, Λ_min.
  - **Added by me, not requested:**
    - `kappa_adj`/`Lambda_adj`: the gain ½R/σ² is replaced by (n/2)·log(1 + R/(σ²(n−s0))), the saturating gain when σ² is estimated (population version).
    - `*_full`: the same with exhaustive deletions of **any** size 4..s0 (including S = ∅, D = S0).
    - `omega_add`: the superset margin price − log p of S0 ∪ {null}.
    - `passprob`: Π_j P(χ²₁(t²_j) > 2·price), the chance that all s0 sample t² clear 2·price.

**Validation (all pass).**
- κ_del vs P1's population min t² (`p1_by_setting.tsv`: `med_min_t2_pop`, `price`): max relative difference 5.6e-15 over 136 settings (`tables/validation_kappa_del_vs_P1.tsv`).
- R(S) by brute force, 2×10⁵ simulated rows: S2_080 (D = {223}, N = {222, 224}) 78.17 vs 78.33; S1_03 (D = {1,2}, N = {11,12}) 115.18 vs 115.57; S2_117 (D = {1,2,3}) 442.99 vs 443.70. Relative differences 0.16–0.33%, which is the Monte Carlo error (`validation_RS_bruteforce.tsv`).
- R(S) on actual `gen_data` draws (S1_03, reps 1–20): 115.16 ± 2.0 (SE) vs formula 115.18 (`validation_RS_gendata.tsv`).
- Greedy N versus exhaustive N (m ≤ 2) over every D in every setting: max difference 0 (`e1_greedy_check.tsv`).
- Pool width: distance 3 of D, 3/6/10 of S0, on 12 settings: identical κ_swap and Λ (`e1_pool_check.tsv`).

**Scripts** (`scripts/`; `bash scripts/run_all.sh` rebuilds everything): `pop_lib.R`, `e1_margin.R`, `e1_fitlevel.R`, `e0_e3_e4_e5_e6.R`, `e7_retab_proxy.R`, `e7_bt2diag_crosscheck.R`, `e1_pool_check.R`, `make_summary_tables.R`. Logs in `logs/`.
**Cost.** Final full pipeline 0.108 CPU-h (`logs/cpu_times.tsv`; 16 forked R workers, `nice -n 19`, thread variables exported in the shell). About 0.7 CPU-h with development reruns. No Slurm, no fits.

## E0. Regime table (`tables/e0_regime_by_setting.tsv`, 136 rows; `summ_E0.tsv`; `e0_failure_totals.tsv`)

| | S1 (16 settings) | S2 (120 settings) |
|---|---|---|
| n, p, s0 | n ∈ {500, 1000}, p ∈ {500, 5000}, s0 = 10 | n ∈ {50, 100}, p = 1000, s0 = 5 / 10 |
| signal | SNR ∈ {0.5, 1, 2, 3}; ν_pop 0.04–3.94; ρ = 0.6 | ν ∈ {0.05 … 6}; ρ ∈ {0, 0.35, 0.7}; bt 1, 2 |
| A = log p/log n | 0.90–1.37 | 1.50 (n = 100), 1.77 (n = 50) |
| s0 log p/n = ε_n² | 0.062–0.170 | 0.691 |
| ε_n = √(s0 log p/n) | 0.249–0.413 | 0.831 |
| log p/n | 0.0062–0.0170 | 0.069 (n = 100), 0.138 (n = 50) |
| (log p)²/n | 0.039–0.145 | 0.477, 0.954 |
| log log p/log n | 0.26–0.35 | 0.42–0.49 |
| √(log n/n) | 0.083–0.111 | 0.215 (n = 100), 0.280 (n = 50) |
| exact recovery (MPM = S0) | 759/1600 (0/800 at SNR ≤ 1; 92–98 per 100 at SNR ≥ 2) | 606/12000 |
| failure type | 837 statistical, 4 search | 11,253 statistical, 141 search |

Exact recovery in S1 by cell: 0/100 at SNR 0.5 and 1, 92–98/100 at SNR 2 and 3, with Wilson 95% interval 0.85–0.99 (`e0_regime_by_setting.tsv`: `exact_lo`, `exact_hi`). In S2 it is 0 at ν ≤ 1.22 (8,400 fits), 2/1,200 at ν = 2.07, and at ν = 3.52 it is 0.03–0.13 (n = 50) and 0.05–0.07 (n = 100) pooled by beta type. At ν = 6, bt1 gives 0.64 (both n) and bt2 gives 0.24 (n = 50: 71/300; n = 100: 69/300).
Reading: S1 sits at s0 log p/n ≈ 0.06–0.17, S2 at 0.69 for every cell. S2 is therefore never in an "ε_n → 0" regime, and S2 failures cannot by themselves contradict an asymptotic theorem.

## E1. Residual-signal margin (the key test)

**Per-setting population margins** (`tables/e1_margin_by_setting.tsv`; ranges in `summ_E1_E2.tsv`). Ranges (min–max) over settings:

| group | κ_del | κ_multi | κ_swap | κ_pop (brief) | κ_adj_full (mine) |
|---|---|---|---|---|---|
| S1 (16) | 0.18–7.20 | 0.16–6.30 | = κ_del | 0.16–6.30 | 0.16–4.68 |
| S2 bt1 ρ = 0 | 0.031–3.95 | = κ_del | = κ_del | 0.031–3.95 | 0.034–1.34 |
| S2 bt1 ρ = 0.35 | same as bt1 ρ = 0 | = κ_del | 0.025–3.09 | 0.025–3.09 | 0.027–1.34 |
| S2 bt1 ρ = 0.7 | same as bt1 ρ = 0 | = κ_del | 0.011–1.35 | 0.011–1.35 | 0.012–1.24 |
| S2 bt2 ρ = 0 | same as bt1 ρ = 0 | = κ_del | = κ_del | 0.031–3.95 | 0.034–1.34 |
| S2 bt2 ρ = 0.35 | 0.013–1.69 | = κ_del | = κ_del | 0.013–1.69 | 0.015–1.15 |
| S2 bt2 ρ = 0.7 | 0.0027–0.42 | = κ_del | = κ_del | 0.0027–0.42 | 0.0030–0.41 |

How the minimum is reached (`kappa_arg`, `kappa_adj_full_arg`):
- S1: κ_pop is attained by a 3-variable deletion in all 16 settings (κ_multi < κ_del, because the signs alternate). Λ_min is attained by the 3-variable deletion at SNR ≤ 1 and by the single deletion at SNR ≥ 2 (a positive Λ shrinks with fewer deleted variables).
- S2 bt1, ρ > 0: κ_pop is attained by a swap of one true variable for neighbouring nulls (`swap1`, all 40 settings).
- S2 bt2, ρ = 0.35: the single or 3-variable deletion (20 of 20). bt2, ρ = 0.7: 2-variable deletions (10) and swaps (10).
- S2 at ν ≥ 2.07 under κ_adj_full (36 settings): the binding rival is the **empty model** (D = S0) in 21, a deletion of 4 of 5 true variables in 3, a swap in 9, a 3-variable deletion in 3. The ν at which S0 beats ∅ under the saturating gain is `nu_crit_empty` = 3.22 (n = 100, s0 = 10) and 3.52 (n = 50, s0 = 5).

**Per S1 cell, κ at the empirical recovery transition** (`tables/e1_s1_cells.tsv`): the transition lies between SNR 1 and SNR 2 in all four (n, p) cells.

| (n, p) | κ_pop at SNR 1 (exact 0/100) | κ_pop at SNR 2 (exact) | κ_adj_full at SNR 2 |
|---|---|---|---|
| (500, 500) | 0.66 | 2.66 (0.92) | 2.24 |
| (500, 5000) | 0.70 | 2.80 (0.94) | 2.22 |
| (1000, 500) | 0.64 | 2.54 (0.96) | 2.34 |
| (1000, 5000) | 0.68 | 2.71 (0.94) | 2.40 |

At SNR 3, κ_pop = 5.7–6.3 and exact recovery is 0.95–0.98. So the S1 transition is bracketed by κ_pop ∈ (0.70, 2.54). A logistic fit on log κ_adj_full puts P(exact) = 0.5 at κ_adj_full = 1.50 and 0.9 at 2.36 (`e1_logistic_kappa.tsv`). The S1 transition itself has only two non-trivial SNR levels, so it is not located more tightly than this bracket.

**Fit level: does the swap-aware margin close the sufficiency gap?** 13,600 fits; predictors are per-setting constants, so 2×2 tables are over fits (`tables/e1_2x2_predictors.tsv`; AUCs `e1_auc.tsv`). "yes" = predictor true.

| predictor | group | yes: exact / not | no: exact / not | sensitivity | P(exact ∣ yes) | P(exact ∣ no) |
|---|---|---|---|---|---|---|
| P1 sample min t² > 2·price | S1 | 759 / 41 | 0 / 800 | 1.000 | 0.949 | 0 |
| | S2 | 597 / 737 | 9 / 10657 | 0.985 | 0.448 | 0.00084 |
| P1 population min t² > 2·price (= κ_del > 1) | S1 | 759 / 41 | 0 / 800 | 1.000 | 0.949 | 0 |
| | S2 | 606 / 1994 | 0 / 9400 | 1.000 | 0.233 | 0 |
| **κ_pop > 1** | S1 | 759 / 41 | 0 / 800 | 1.000 | 0.949 | 0 |
| | S2 | 591 / 1609 | 15 / 9785 | 0.975 | **0.269** | 0.0015 |
| κ_pop > 1.5 | S2 | 455 / 945 | 151 / 10449 | 0.751 | 0.325 | 0.014 |
| κ_pop > 2 | S2 | 427 / 573 | 179 / 10821 | 0.705 | 0.427 | 0.016 |
| κ_adj_full > 1 (mine) | S2 | 590 / 1010 | 16 / 10384 | 0.974 | 0.369 | 0.0015 |
| κ_adj_full > 1.1 | S2 | 453 / 447 | 153 / 10947 | 0.748 | 0.503 | 0.014 |
| κ_adj_full > 1.25 | S2 | 380 / 220 | 226 / 11174 | 0.627 | 0.633 | 0.020 |
| Λ_min > 0 (brief) | S2 | 602 / 1698 | 4 / 9696 | 0.993 | 0.262 | 0.0004 |
| Λ_min > 1·log n | S2 | 525 / 975 | 81 / 10419 | 0.866 | 0.350 | 0.008 |
| passprob > 0.5 | S2 | 602 / 1098 | 4 / 10296 | 0.993 | 0.354 | 0.0004 |

The same rows for S2 ν ≥ 2.07 (where exact recovery is possible), for every ρ × beta_type cell, and for a scan c ∈ {−1, …, 8} of Λ_min > c·log n are in the table.

AUC for exact recovery (`e1_auc.tsv`), all fits / S1 / S2 / S2 with ν ≥ 2.07 / S2 bt1, ν ≥ 2.07:

| score | all | S1 | S2 | S2 ν ≥ 2.07 | S2 bt1, ν ≥ 2.07 |
|---|---|---|---|---|---|
| sample min t²/price (P1) | 0.989 | 0.980 | 0.984 | 0.939 | 0.899 |
| population min t²/price (= κ_del) | 0.984 | 0.978 | 0.980 | 0.923 | 0.877 |
| κ_pop (swap-aware, brief) | 0.976 | 0.978 | 0.958 | 0.845 | 0.762 |
| κ_adj_full (mine) | 0.986 | 0.978 | 0.972 | 0.895 | 0.849 |
| Λ_min/log n (brief) | 0.978 | 0.978 | 0.967 | 0.873 | 0.800 |

Reading:
- **No.** The swap-aware margin does not close the S2 gap. P(exact ∣ κ_pop > 1) = 0.27 on S2 (S1: 0.95, unchanged because κ_pop > 1 coincides with κ_del > 1 on S1). On S2 it is a worse ranker than κ_del (AUC 0.958 vs 0.980; 0.845 vs 0.923 among ν ≥ 2.07).
- **Why.** Neighbour-swap rivals do not predict failure. At ν = 6, bt1, exact recovery is 0.60–0.70 for ρ = 0, 0.35 and 0.7 alike (n = 100: 0.66, 0.60, 0.65), while κ_swap falls from 3.95 to 3.09 to 1.35. At ρ = 0.7, κ_pop < 1 for ν ≤ 3.52 predicts failure, but κ_del-type failure already happens there at ρ = 0.
- **What does move the transition on S2** is the saturation of the likelihood gain. With the σ²-estimated gain and the full set of deletions, a large deletion (most often the empty model) binds. Exact recovery then switches on across κ_adj_full ≈ 1.0 → 1.3, with P(exact) = 0.5 at 1.21–1.27 for bt1 and bt2 (ρ = 0, 0.35), 1.02 for bt1 ρ = 0.7, and 1.51 for bt2 ρ = 0.35 (8 successes; `e1_logistic_kappa.tsv`). The S1 value is 1.50. These agree within a factor 1.2 across suites. This reading is post hoc: it was defined after the first results, so it is a fit to these data, not a pre-declared test.
- **Residual gap.** Even κ_adj_full > 1.25 gives P(exact ∣ yes) = 0.63, not 0.95. At ν = 3.52, n = 100, ρ = 0, bt1: κ_del = 2.3, passprob = 0.81, κ_adj_full = 1.05, exact = 0.09. At ν = 6, n = 50: κ_adj_full = 1.28, exact = 0.62. The remainder is sample fluctuation in a regime with s0 log p/n = 0.69; it is not an identifiability failure.
- **Where S1 fails.** S1 failures at SNR ≥ 2 (41 fits) are not signal-margin failures: 40 of 41 are supersets of S0 (39 with exactly one extra null; `e7_failure_composition.tsv`). The superset margin is ω = price − log p = 1.49–1.84 nats per added null (S2: 0.69 at n = 100, 1.05 at n = 50; `omega_add_per_null`). This is O(1) nats, not scaled by SNR, and no deletion/swap margin sees it.

## E2. Hellinger-scale screening margin (SL Thm 3 route) (`e1_margin_by_setting.tsv`: `e2_*`; `summ_E1_E2.tsv`)

min over true j and S ∌ j, |S| ≤ s0+4 of Var(xᵀβ | x_S)/σ² (population; D ∋ j with |D| ≤ 3 exhaustive, N greedy with |N| ≤ 4+|D|), against ε_n² = s0 log p/n (P2's radius, not the TD radius M log n/n) and log n/n. *Lead note:* this is a restricted search, so where nested it gives an upper bound on the full-sieve minimum; it is a **scale diagnostic** and cannot certify A-MARGIN-H (C_H unknown).

| | S1 | S2 |
|---|---|---|
| margin | 0.0029–0.288 | 0.0004–0.60 (n = 100), 0.0011–1.20 (n = 50) |
| ratio to ε_n² (min / median / max) | 0.047 / 0.47 / 1.69 | 0.0006 / 0.056 / 1.74 |
| settings with ratio ≥ 1 | 4 of 16 (SNR 3 only) | 5 of 120 (n = 50, bt1/bt2 at ρ ≤ 0.35, ν ≥ 3.52 or 6) |
| ratio to log n/n | 0.42–23 | 0.009–15 |
| Gaussian d_H² version with τ = σ (fixed-variance squared distance, an **upper bound** on the variance-optimised 1 − (1 + margin/2)^(−1/4) of TS-a), 1 − (1+margin/4)^(−1/2), over ε_n² | 0.006–0.21 | 0.00007–0.18 |

Reading: the residual-variance/radius² ratio is ≥ 1 in 9/136 settings (max 1.74); the fixed-variance squared Hellinger ratio never reaches 1 (max 0.21). S1 SNR 2 has ratio 0.75 and still recovers exactly in 92–96% of fits. This is a scale diagnostic only: C_H is unknown, so it is not compared with ε_n² as a requirement. The margin is ≫ log n/n in most S1 and good S2 cells (up to 23×), which is the scale the margin condition needs.

## E3. Song–Liang Condition 3 (identifiability, p. 955), Gaussian AR(1) (`tables/e3_condition3.tsv`, `summ_E3.tsv`, `e3_numeric_check_S1_03.tsv`)

For Z = x_k + Σ b_i x_{j_i} ~ N(0, V), E exp(−Z²) = (1+2V)^(−1/2), so the condition holds with δ_SL = 1 − (1+2v)^(−1/2), v = min Var(x_k | others) = (1−ρ²)/(1+ρ²) for ≥ 2 others (1−ρ² at an end column). This is independent of r̄ ≥ 2 and of n. The form of the condition was taken from `SONG_LIANG_MAP.md` row 9; **Lead check:** it matches SL p. 955 as printed (E exp{−(x_k + Σ_{i≤r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n, δ_n ≻ ε_n², j_i ≠ k). r̄ε_n² is tabulated as the brief asks.

| ρ | v | δ_SL | ε_n²/δ_SL | r̄ε_n²/δ at r̄ = s0 | r̄ = 2s0 | r̄ = ⌈log n⌉s0 |
|---|---|---|---|---|---|---|
| 0.6 (S1) | 0.471 | 0.282 | 0.22–0.60 | 2.2–6.0 | 4.4–12.1 | 15–42 |
| 0 (S2) | 1 | 0.423 | 1.63 | 8.2–16.3 | 16.3–32.7 | 33–82 |
| 0.35 (S2) | 0.782 | 0.375 | 1.84 | 9.2–18.4 | 18.4–36.8 | 37–92 |
| 0.7 (S2) | 0.342 | 0.230 | 3.01 | 15–30 | 30–60 | 60–150 |

Numerical confirmation on S1_03 (n = 500, p = 500, ρ = 0.6): 1/[Σ⁻¹]_kk = 0.4706 (interior), 0.64 (end), equal to the formula. The minimum over 3,600 random sets of size 1–12 is 0.584 (0.4706 when the two neighbours are included). Monte Carlo E exp(−Z²) at the optimal b is 0.71771 vs the formula 0.71774. In a generated dataset (`gen_data`, rep 1) the residual variance of column 250 on columns 249 and 251 is 0.470 (SE 0.03).
Reading: δ_SL is a fixed positive constant (0.23–0.42), so Condition 3 holds in the population for every setting. The requirement ε_n² = o(δ_SL) is not satisfied numerically in S2 (ε_n²/δ = 1.6–3.0) and is only marginally satisfied in S1 (0.22–0.60). Any version with an extra factor r̄ ≥ s0 is not satisfied anywhere (2.2 and above).

## E4. Bounded signal (`tables/e4_bounded_signal.tsv`, `summ_E4.tsv`)

| | S1 | S2 |
|---|---|---|
| max_j ∣β_j∣ sd_j/σ | 0.12–1.17 (med 0.43) | 0.035–1.10 (med 0.22) |
| βᵀΣβ/σ² (= ν_pop) | 0.04–3.94 | 0.05–6.00 |
| β_min/(σ√(log p/n)) | 1–6 (= 2·SNR) | 0.13–2.95 |
| β_min/(σ√(log n/n)) | 0.95–7.0 | 0.16–3.9 |

Reading: bounded signal holds in every setting (max ≈ 1.17σ, i.e. 1.175σ; ν ≤ 6). S1's β shrinks as √(log p/n) by construction, so a fixed lower bound b_lo does not hold as a sequence. S2's β = 1 is fixed but β_min/(σ√(log p/n)) is below 1 in most S2 cells.

## E5. Eigenvalue floors (`tables/e5_eigen_floors.tsv`, `summ_E5.tsv`)

| | S1 (ρ = 0.6) | S2 ρ = 0 | S2 ρ = 0.35 | S2 ρ = 0.7 |
|---|---|---|---|---|
| population floor (1−ρ)/(1+ρ) for any T | 0.25 | 1 | 0.481 | 0.176 |
| exact λ_min(Σ_S0) | 0.256 | 1 | 0.490–1 | 0.181–1 |
| n × floor (margin over c_ψ/n) | 125–250 | 50–100 | 24–48 | 8.8–18 |
| sample λ_min(X_S0ᵀX_S0/n) median | 0.24 | 0.54–0.66 | 0.34–0.65 | 0.13–0.65 |
| sample greedy sparse floor at m1 = 2s0 | 0.14–0.20 | 0.032–0.040 | 0.028–0.035 | 0.014–0.020 |
| sample greedy at m2 = ⌈2(A+1)s0+2⌉ (capped at n−1) | 0.067–0.17 | 1.1e-5–2.4e-4 | 1.1e-5–2.4e-4 | 7e-6–2.0e-4 |
| m2 / floor | 0.27–0.69 | 1e-5–2e-4 | 2e-5–5e-4 | 4e-5–1e-3 |

Reading: the population floors hold analytically, and the vanishing floor λ_min(Corr(x_T)) ≥ c_ψ/n holds with margin n·(1−ρ)/(1+ρ) ≥ 8.8. The sample floors hold on S1 (0.07–0.20, i.e. 0.27–0.8 of the population floor), and are essentially zero on S2 at the theorem's m2 (1e-5–1e-4; the greedy value is an upper bound on the true sparse minimum). Sample EF is vacuous on S2.

## E6. Dimension regimes (`tables/e6_S1S2_regimes.tsv`, `e6_typical_regimes.tsv`)

| setting | A | p ≤ n^1.5 | n² | n³ | κ_eff = log p/(log n)² (SL Cor S1 needs < ¼) | log p/√n | log p/n |
|---|---|---|---|---|---|---|---|
| S1 (500, 500) | 1.00 | yes | yes | yes | 0.161 ok | 0.28 | 0.012 |
| S1 (500, 5000) | 1.37 | yes | yes | yes | 0.221 ok | 0.38 | 0.017 |
| S1 (1000, 500) | 0.90 | yes | yes | yes | 0.130 ok | 0.20 | 0.006 |
| S1 (1000, 5000) | 1.23 | yes | yes | yes | 0.178 ok | 0.27 | 0.009 |
| S2 (100, 1000) | 1.50 | yes | yes | yes | **0.326 fails** | 0.69 | 0.069 |
| S2 (50, 1000) | 1.77 | **no** | yes | yes | **0.451 fails** | 0.98 | 0.138 |

Typical user regimes (A = log p/log n; κ_eff in brackets):

| (n, p) | A | κ_eff < ¼? | log p/√n |
|---|---|---|---|
| (100, 10³) | 1.50 | 0.33 no | 0.69 |
| (500, 10⁴) | 1.48 | 0.24 yes | 0.41 |
| (1000, 10⁵) | 1.67 | 0.24 yes | 0.36 |
| (5000, 10⁶) | 1.62 | 0.19 yes | 0.20 |
| (300, 2·10⁴) gene expression | 1.74 | 0.30 no | 0.57 |
| (10⁴, 5·10⁵) GWAS | 1.42 | 0.16 yes | 0.13 |

Reading: p ≤ n² holds everywhere, including all typical regimes (A ≤ 1.77); n^1.5 fails only for S2 at n = 50 and for three of the six user regimes. log p ≤ √n holds in every setting (S2 n = 50 is close to the boundary at 0.98). Song–Liang Cor S1's p < n^{κ log n} with κ < ¼ holds on S1 and on four of the six user regimes, and fails (numerically) on S2 and on the two smaller-n user regimes. κ_eff is a numerical exponent, not an asymptotic statement, so this is "weak" rather than "contradicts".

## E7. Re-tabulated Engineering/Theory numbers and the proxy check

*Scope (v1.4).* E7 is a predictive-summary diagnostic: across-replicate quantiles of a predictive distance at posterior-mean coefficients, with a different radius from TD's. It does not measure within-data posterior mass. The selected-MPM variance ratio below illustrates variance inflation for a fitted subset; it does not verify a prespecified-candidate theorem.

**P2 E4 (Hellinger, Theory's d_H from P2's β̄; `tables/e7_E4_dH_by_group.tsv`, `e7_E4_dH_overall.tsv`; source `e4_dh_by_setting.tsv` columns `med_ratio`, `q90_d_mix`, `eps_n`).** d_H < ε_n in all 136 settings, for both the median and the q90. Median d_H/ε_n: S1 SNR ≥ 2: 0.136–0.166; S1 SNR ≤ 1: 0.28–0.46; S2 ν < 2.07: 0.105–0.42; ν = 2.07–3.52: 0.29–0.56; ν = 6: 0.18–0.46. Largest q90 ratio 0.63. Caveat (Theory's): list view only, and ε_n = 0.83 on S2 makes the check weak there.

**P2 E5 (cap; `e7_E5_size_cap.tsv`, from `p2_by_setting.tsv` columns `n_cap_binds_*`, `max_over_K`, `max_mass_size_ge_Km2`).** The cap never binds (0 of 13,600 fits, store and top 50) and the mass at |S| ≥ K−2 is 0. Largest stored size / K: S1 ≤ 0.068; S2 ≤ 0.52.

**P2 E6 (σ²; `e7_E6_sigma2_ratio.tsv`, columns `med_ratio_Esig2_list`, `med_ratio_sigma2_mpm`).** E[σ²∣y]/σ² (setting medians, range): S1 SNR ≥ 2: 0.96–1.00; S1 SNR ≤ 1: 1.03–1.22; S2 ν < 2.07: 1.00–2.17; ν = 2.07–3.52: 1.19–3.26; ν = 6: 0.90–1.70. **Recomputed σ²_C check** (KL projection onto the stored MPM, `e7_E6_sigma2C.tsv`): E[σ²∣y, MPM]/σ²_C has median 0.99 (S1 SNR ≥ 2: 0.987, SNR ≤ 1: 0.990), 0.98 (S2 ν < 2.07), 0.84 (S2 ν = 2.07–3.52 and ν = 6). Against σ²: 2.26 at ν = 2.07–3.52. The MPM misses a true predictor in 100% of S2 ν < 2.07 fits, 96% at ν = 2.07–3.52, 51% at ν = 6, and 0.1% in S1 SNR ≥ 2. Values below 1 are an in-sample bias of the residual variance of a selected model at n = 50–100.

**P1 E2/E3 (`e7_P1_E2E3_by_group.tsv`, from `p1_by_setting.tsv` columns `med_lmin_*`, `med_pi_ratio_given_exact`).** Sample floors: see E5. (1−π̂(S0))/√(log n/n) given exact recovery: S1 SNR ≥ 2: 4.14–5.05; S2 ν = 2.07–3.52: 2.05–4.10; ν = 6: 2.40–3.65. The particle-level π̂ is not available (P1 §4.4).

**Proxy behaviour among failed fits** (MPM from `records.rds`; `e7_proxy_summary.tsv`, `e7_proxy_shares_failed_fits.tsv`, `e7_failure_composition.tsv`; cross-checked against `bt2_diagnostic_per_rep.tsv` columns `FN_with_selected_neighbour`, `FP_adjacent` in `e7_bt2diag_crosscheck.tsv`: 0.0016 / 0.0005 / 0.0297 / 0.0020 for bt1/bt2 at ρ = 0.35/0.7, identical).

| failed fits | n | MPM misses a true variable and contains a null adjacent to a missed true | within distance 3 | misses a true variable | any null in MPM |
|---|---|---|---|---|---|
| S1 | 841 | 1 (0.1%) | 1 | 801 | 47 |
| S2 | 11,394 | 64 (0.6%) | 74 (0.6%) | 11,309 | 464 |
| S2, ν ≥ 2.07 | 2,994 | 49 (1.6%) | 53 (1.8%) | 2,909 | 285 |
| S2 bt1, ρ > 0 | 3,710 | 58 (1.6%) | 65 | 3,670 | 186 |
| S2 bt2, ρ > 0 | 3,992 | 5 (0.1%) | 7 | 3,992 | 145 |

Reading: in S1/S2 failures the MPM is almost never a "proxy" for a missed variable. It is empty or an under-selected subset: 87% of S2 ν ≤ 1.22 failures are empty MPMs; median |MPM| is 1–3 at ν = 2.07–6. The exception is S2 bt1 at ρ = 0.7 (3.0% of failed fits). This is a statement about well-specified data (no hidden columns) and about the same-data selected MPM (a selected-group summary): it shows the posterior does not substitute neighbours when the true variable is present in the candidate set. It says nothing about the hidden-column case (E8 of TH_PREP, needs refits).
Failure composition (`e7_failure_composition.tsv`): S1 SNR ≥ 2: 97.6% are supersets of S0 (95% with one extra null); S2 ν = 6: 89.5% miss a true variable, 10.5% supersets; S2 ν ≤ 3.52: ≥ 98.9% miss a true variable.

## E8. Engineering `perf/` items relevant to assumptions (all read-only)

- `perf/JOINT_PLAN.md` §1 and §2(iii) (via [A-06], [A-11], [A-14]): a best-subset reference told s0 finds S0 in 764 of 800 S2 fits at ν = 6 (bt1 or ρ = 0) against 515 for SMC-BVS; in 482 of 800 at ν = 3.52 (SMC-BVS 81). Under BB(1, p) and g = n, S0 beats even the empty model only above ν ≈ 5.2 (n = 50) or 4.6 (n = 100) (sample statement); my population ν at which (n/2)log(1+nν/(n−s0)) = s0·price is 3.52 / 3.22 (`nu_crit_empty`).
- `perf/experiments/E0_subset_enum/E0_REPORT.md`: exhaustive enumeration of the 2^s0 subsets of S0 (680 datasets, reps 101–105). S0 is the best subset of itself in 40/40 strong-S1; 0/40 at weak S1 (prior part −54 nats). For bt2 with ρ ≥ 0.35 a proper subset of the block beats S0 in 200/200 fresh datasets at every ν (median gap −7.1 at ρ = 0.35 and −23.1 at ρ = 0.7, ν = 6). This is the posterior preferring a subset, independent of search; it matches κ < 1 for bt2 and also shows that bt2 loss is a property of the target F.
- Prior/slab variants (`perf/JOINT_PLAN.md` §2(iii), §8; `designer_A/Q2_SLAB.md`): g = 4n or 9n turns all 15 S1 exact losses into modes but loses 92 or 170 of 2,400 feasible-S2 fits; FLS g = max(n, p²) +21 / −656; hyper-g, hyper-g/n, Zellner–Siow lose on both suites; BB(1, p^u) with u = 1.5 is +23 in S1 and −612 in S2; BB(1, p/4) flips 8 of 680 within-truth comparisons; Bernoulli(m/p) with m = 2 or 5 gains on both suites but was rejected as a tuned constant. None was run as an SMC fit. Consequence for theory: no monotone change in the price of a variable helps both suites, which is the superset margin ω (S1) versus the empty-model margin (S2) found above.
- `perf/experiments/S1_asi_gap/REPORT.md`: all 15 S1 exact losses are "S0 plus one null with PIP 0.50–0.62", 0 search misses (matches `e7_failure_composition.tsv`: 40 of 41 S1 failures at SNR ≥ 2 are supersets).
- N-ladders: none run (`JOINT_PLAN.md`, "No N-ladder (HQ ruling)").

## E9. Conditional Gaussian width of added nulls on S1 designs (Lead, council R1 follow-up; `scripts/e9_width_mc.py`, `tables/e9_width_s1.tsv`)

*v1.4 scope.* E9 and E9b check the **refined design-conditional form** (the v1.3 class-level condition, kept as a parallel sufficient condition in ASSUMPTIONS §3.3). They are not checks of the population form (U1)–(U2); the U2a check is in the Lead synthesis above.

Question (Opus R1 B1(c)): does A-MARGIN-U, with the design-specific width w_Dm(X) = E_g max_{|N|=m}(−⟨v_S, g⟩), cover S1's
boundary signals for mixed rivals, where the worst-case combinatorial width does not?

Method: for each S1 cell at SNR 2 and 3, 4 simulated designs (AR(1) ρ = 0.6, columns centred and scaled, β as in
`harness/generate.R`), every single deletion D = {j} (10 per cell), m = 1 (all cells) and m = 2 (p = 500 cells; all pairs);
300 Gaussian draws g per design. The class condition is checked in its limit form (δ = γ = t_n = 0, C = 1):
√(min_{|N|=m} R_n(S)/σ²) ≥ w_Dm + √(2B_Dm), B_Dm = Pr_n(1) − (m/2)log(n/log p) > 0. Population R_n(S) is exact; min over N
is exhaustive over the 40 nulls nearest S0, which contains an exact minimiser by the Gaussian AR(1) Markov property (if
max D < 10 the retained x_10 screens every null; if 10 ∈ D the nearest null x_11 screens the farther ones; Sol R2). No fits, no outcome data; ≈ 2 CPU-min,
single-threaded, under nice.

| n, p | SNR | m | w_comb = √(2 log C(p−s0,m)) | w_Dm(X) over j (MC) | √(2B) | √(min R/σ²) (binding j) | min surplus with w_Dm(X) | min surplus with w_comb |
|---|---|---|---|---|---|---|---|---|
| 500, 500 | 2 | 1 | 3.52 | 0.19–0.39 | 3.32 | 6.84 | 3.29 | 0.001 |
| 500, 500 | 2 | 2 | 4.84 | 0.38–0.59 | 2.58 | 6.84 | 3.85 | −0.57 |
| 500, 5000 | 2 | 1 | 4.13 | 0.28–0.41 | 3.99 | 8.01 | 3.68 | −0.11 |
| 1000, 500 | 2 | 1 | 3.52 | 0.10–0.32 | 3.32 | 6.84 | 3.36 | 0.001 |
| 1000, 500 | 2 | 2 | 4.84 | 0.26–0.52 | 2.44 | 6.84 | 4.07 | −0.43 |
| 1000, 5000 | 2 | 1 | 4.13 | 0.20–0.33 | 3.99 | 8.01 | 3.76 | −0.11 |
| all four | 3 | 1–2 | 3.52–4.84 | 0.12–0.59 | 2.44–3.99 | 10.26–12.01 | 6.70 (min 6.696) | 2.85 (min 2.849) |

Reading: the estimated conditional width on S1's AR(1) designs is an order of magnitude below the worst case. The mechanism
is generic: when no null is population-correlated with the residual direction, v_S moves by O(√(log p/n)) across N, and a
heuristic gives w_D1 ≈ (log p)/√n ≈ 0.28 at (500, 500) (Opus R2), matching the table. With it, the estimated zero-slack
surplus is large for d = 1, m = 1 (all cells) and m = 2 (p = 500); with the worst-case width the inequality is at equality
or fails at SNR 2. **Scope (Sol R2):** this is a diagnostic of the limit inequality with four-design mean widths at
δ = γ = t_n = 0, not a test of the positive-slack assumption or of its 1 − o(1) design-event quantifier. Not evaluated:
m = 2 at p = 5,000; m = 3 (B_D3 > 0 in all four cells at C = 1) and m = 4 at p = 5,000 (B_D4 > 0). Largest between-design
SD of w_Dm(X): 0.121.

**E9b. Extension to d ≤ 3 and to the credit constant** (council R2: Opus S-3, Sol 2; `scripts/e9b_width_mc_ext.py`,
`tables/e9b_width_ext_s1.tsv`, `logs/e9b_width_mc_ext.log`; ≈ 1 CPU-min, single thread, nice). **v1.4 rerun:** the mean μ is now the
raw-centred mean, as in `harness/generate.R`. The v1 table (coded mean) is kept as `tables/e9b_width_ext_s1_v1_codedmu.tsv` (superseded);
d = 1 is identical and d = 2, 3 change by ≤ 0.0015. The credit constant is C = 1 by convention (multiplier in the tight remainder).
"C ≍ (s0+1)² ≈ 121" is **withdrawn**: the C = 121 column is a **sensitivity setting** in which log(n/(C log p)) ≈ −0.7 to +0.3 at S1's sizes, so the
containing-model credit is about zero. E9b recomputes the surplus for d = 1, 2, 3, m = 1 (all cells) and m = 2 (p = 500), under C = 1, C = 121 and no
credit (B = Pr_n(d)); 4 designs × 300 draws. For each (d, m) the 3 D per cell are **selected examples**, chosen by smallest population min_N R; they
are not a sample of classes.

Exact minima over all evaluated classes at each (SNR, d) (δ = γ = t_n = 0; quoted to 4 decimals, never rounded upward):

| SNR | d | C = 1 | C = 121 | no credit |
|---|---|---|---|---|
| 2 | 1 | 3.2896 | 2.3862 | 2.4889 |
| 2 | 2 | 4.2658 | 3.6228 | 3.6867 |
| 2 | 3 | 4.2987 | 3.8030 | 3.7921 |
| 3 | 1 | 6.7098 | 5.8065 | 5.9091 |
| 3 | 2 | 9.1027 | 8.4597 | 8.5237 |
| 3 | 3 | 9.8397 | 9.3440 | 9.3332 |

The per-design mean widths w_Dm(X) range over 0.142–0.426 (individual draws 0.037–0.531). The minimum at SNR 2 is 2.3862 at
(d, m) = (1, 2) with C = 121 and 2.4889 with no credit. All evaluated classes are active at C = 121. Opus's R2 rerun (`.rc_tmp/opus_r2/`, 200 draws,
coded μ) gave 2.40–3.87 at SNR 2 with C = 121: it matched the v1 table within Monte Carlo error and is not re-quoted for v1.4. C = 121 can give a
*smaller* surplus than no credit, because log(n/(C log p)) < 0 turns the credit into a charge. Four designs at zero slack establish no 1 − o(1) event.

## Evidence against (what a theorem-writer should not assume)

1. **Sufficiency of any per-variable margin on S2.** κ_del > 1 gives P(exact) = 0.23 on S2; the swap-aware κ_pop > 1 gives 0.27 and ranks worse than κ_del (AUC 0.958 vs 0.980). At ν = 3.52, κ_del = 2.2–2.3 but exact recovery is 3–16%.
2. **Neighbour-swap rivals are not what limits recovery in S2 bt1.** At ν = 6, recovery is the same for ρ = 0, 0.35, 0.7 (0.60–0.70), while κ_swap falls by a factor 3. The brief's Λ (with m·log p multiplicity) is also not decisive: AUC 0.967 vs 0.980 for κ_del on S2.
3. **Quadratic gain overstates the margin.** ½R/σ² is not the right scale when R is a sizeable fraction of nσ²; with the σ²-estimated gain the empty-model rival binds (21 of the 36 S2 settings with ν ≥ 2.07; ν_crit = 3.2–3.5), and the transition (κ_adj_full ≈ 1.0–1.3) matches S2. This is post hoc.
4. **Superset failures (S1) are invisible to deletion margins.** 40 of 41 S1 failures at SNR ≥ 2 are supersets of S0 and 39 of 41 add exactly one null; the margin against that is ω = price − log p = 1.5–1.8 nats, independent of SNR. In S2 ω = 0.7–1.05 nats.
5. **S2 is not asymptotic**: s0 log p/n = 0.69, ε_n = 0.83, d_H ≤ 1, so the Hellinger check has almost no resolution and failures at ν ≤ 1.22 follow from the empty model beating S0.
6. **Sample eigenvalue floors are vacuous on S2** (1e-5–2e-4 at m2; n = 50: λ_min(R̂_T) = 0 in 30–35% of fits, P1). Only the population/random-design form is supportable there.
7. **SL Condition 3 and Cor S1 numerics on S2**: ε_n²/δ_SL = 1.6–3.0 (not o(1)); κ_eff = 0.33–0.45 > ¼.
8. **Screening scale diagnostic.** The residual-variance/radius² ratio is ≥ 1 in only 9/136 settings (max 1.74), yet recovery occurs at ratio 0.75 (S1 SNR 2). It is a scale diagnostic, not a test of A-MARGIN-H.
9. **Fixed beta-min in S1** is false as a sequence (β ∝ √(log p/n)); S2 β_min/(σ√(log p/n)) is 0.13–2.95.
10. **Rate evidence** for 1−π̂(S0) ∝ √(log n/n) rests on two sample sizes and the list view only (P1 §4.4).
11. **No evidence for proxy substitution** in well-specified data (0.1–1.6% of failed fits); this does not test T3 with hidden columns.

## Summary: assumption → statistic → S1 → S2 → verdict

| assumption (class) | statistic (table) | S1 | S2 | verdict |
|---|---|---|---|---|
| DIM: p ≤ n^A | A = log p/log n (`e0`) | 0.90–1.37 | 1.50–1.77 | supports (A ≤ 2); fails n^1.5 at n = 50 |
| SL Cor S1: p < n^{κ log n}, κ < ¼ | κ_eff (`e6`) | 0.13–0.22 | 0.33–0.45 | S1 supports; S2 numerically fails (weak) |
| log p ≤ √n; log p = o(n) | log p/√n; log p/n (`e0`, `e6`) | 0.20–0.38; 0.006–0.017 | 0.69–0.98; 0.069–0.138 | supports; S2 close to boundary |
| SP: s0 fixed, ε_n → 0 | s0 log p/n (`e0`) | 0.062–0.170 | 0.691 | S1 supports; S2 weak (not small) |
| EFS / NC / nec population floor | (1−ρ)/(1+ρ), n × floor (`e5`) | 0.25; 125–250 | 0.176–1; 8.8–100 | supports (analytic) |
| EF sample floor | greedy λ_min at m1, m2 (`e5`) | 0.14–0.20; 0.07–0.17 | 0.014–0.04; 1e-5–2e-4 | S1 supports; S2 contradicts |
| bs bounded signal | max ∣β∣/σ; ν (`e4`) | ≈ 1.17 (1.175); ≤ 3.9 | ≤ 1.10; ≤ 6 | supports |
| FSb fixed beta-min | β_min/(σ√(log p/n)) (`e4`) | 1–6 (∝ √(log p/n)) | 0.13–2.95 | S1 false as a sequence; S2 true but below the log p/n scale |
| asm:margin, necessary | sens. of κ_del > 1 (`e1_2x2`) | 1.000 | 1.000 (pop) / 0.985 (sample) | supports (MPM recovery and restricted κ: not a test of exact posterior mass or all active mixed classes) |
| asm:margin, sufficient | P(exact ∣ κ_pop > 1) | 0.949 | 0.269 (κ_adj_full > 1.25: 0.63) | S1 supports; S2 contradicts / weak |
| A-MARGIN-U population form, U2a | min R_n(B)/(2σ²Pr_n(d)) over D and ≤ 2 inside proxies (`u2a_check.py`) | = exact κ_n: 0.626–0.693 (SNR 1), 2.505–2.771 (SNR 2) | not run | S1 supports at these proxy sets; binding D retain x_10 |
| mixed rivals, refined design-conditional form (E9/E9b) | min surplus, δ = γ = t_n = 0 | SNR 2: 2.3862 (C = 121, sensitivity), 2.4889 (no credit) | not run | diagnostic of the refined form only: selected D, four designs, zero slack; no 1 − o(1) event |
| swap-aware margin (Λ, κ_swap) | AUC; P(exact ∣ yes) (`e1_auc`) | = κ_del | worse than κ_del | contradicts as an improvement |
| SL Cond 3 | δ_SL; ε_n²/δ_SL (`e3`) | 0.282; 0.22–0.60 | 0.23–0.42; 1.6–3.0 | holds in population; ε_n² = o(δ) weak on S1, fails on S2 |
| SL Thm 3 screening margin | residual-variance/radius² ratio (`e1`: e2) | 0.05–1.69 | 0.0006–1.74 | scale diagnostic only (ratio ≥ 1 in 9/136; recovery occurs below 1) |
| Hellinger rate (T2) | d_H/ε_n (`e7`) | 0.14–0.17 (SNR ≥ 2) | 0.10–0.56 | consistent (predictive-summary diagnostic at posterior-mean coefficients, different radius; not within-data posterior mass; S2 low resolution) |
| size cap K | max size/K (`e7`) | ≤ 0.068 | ≤ 0.52 | supports (never binds) |
| σ² convergence to σ²_C (T3) | E[σ²∣MPM]/σ²_C (`e7`) | 0.99 | 0.84–0.98 | illustrates variance inflation for a fitted (selected-MPM) subset; does not verify a prespecified-candidate theorem; downward in-sample bias |
| proxy behaviour (SL Cor 2 type) | share of failures, MPM misses and holds adjacent null (`e7`) | 0.1% | 0.6% (bt1 ρ = 0.7: 3%) | no evidence either way (well-specified data) |
| rate 1−π̂(S0) ∝ √(log n/n) | ratio given exact (`e7`) | 4.1–5.1 | 2.0–4.1 | weak (two n, list view) |

## Files produced
- `SIMULATION_DATA_ANALYSIS.md` (this report; the D1 draft was merged into it).
- `scripts/e9_width_mc.py` and `tables/e9_width_s1.tsv` (E9, Lead; `logs/e9_width_mc.log`).
- `scripts/e9b_width_mc_ext.py` and `tables/e9b_width_ext_s1.tsv` (E9b, Lead; `logs/e9b_width_mc_ext.log`; v1.4 rerun with the raw-centred mean).
- `tables/e9b_width_ext_s1_v1_codedmu.tsv` (E9b v1 table with the coded mean; **superseded**, kept for the record).
- `.rc_tmp/lead_v14/u2a_check.py` (U2a check, Lead; numbers in the Lead synthesis) and `.rc_tmp/lead_v14/worked_cases.py` (numerical check of the four worked cases in the DOSSIER).
- `scripts/`: `pop_lib.R`, `e1_margin.R`, `e1_fitlevel.R`, `e0_e3_e4_e5_e6.R`, `e7_retab_proxy.R`, `e7_bt2diag_crosscheck.R`, `e1_pool_check.R`, `make_summary_tables.R`, `run_all.sh`.
- `tables/` (about 40 TSV files; the main ones: `e1_margin_by_setting.tsv`, `e1_2x2_predictors.tsv`, `e1_auc.tsv`, `e1_logistic_kappa.tsv`, `e1_s1_cells.tsv`, `e1_setting_exact_vs_margin.tsv`, `e0_regime_by_setting.tsv`, `e3_condition3.tsv`, `e4_bounded_signal.tsv`, `e5_eigen_floors.tsv`, `e6_*.tsv`, `e7_*.tsv`, `validation_*.tsv`, `summ_*.tsv`); `logs/`.
- `.rc_tmp/song/s1s2_ro/` (staged read-only copies, `SOURCES.md`).
