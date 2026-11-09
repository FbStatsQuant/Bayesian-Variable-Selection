# X_R01 disposition (family X lead), 2026-11-09 10:40

Verdict SOUND-WITH-CHANGES (5 MAJOR, 5 MINOR, no FATAL). All accepted; applied in x_paths.py v2 (sha256 b099783a…),
x_paths_k.py (49a9bb22…), summarize.py v2 (6525ba45…), gen_grid.py v2 (f7919561…) before batch 1 (x_A1, x_B1, x_BS1).

1. MAJOR (s_j outside T, NaNs) — fixed. s_j(T) now computed only for j ∈ T (ranks among kept nulls); non-finite values
   counted (`nonfinite_s`). Finite classes: holes measured per class in fixed ξ coordinates around ℓ_cX_T (`cls_*`,
   valid for deleted variables). The global deleted-variable s-excursion is removed; replaced by the unnormalised
   variable-centre frame d_j = ξ_j − ℓ_jX_T (defined for all j; labelled descriptive for continuous loadings). The CS
   ξ-frame statistics are computed only for CS (None otherwise).
2. MAJOR (start_size of full path) — fixed: `start_size` = len(actual path start) per path; DP size → `mode_size`.
3. MAJOR (attrition) — fixed: summarize.py reconstructs expected (cell, seed, path_from) units from the task tables,
   lists missing / unexpected units, marks cells incomplete, reports task return codes (ends.jsonl) and the number of
   distinct provenance sha sets; duplicates still an error.
4. MAJOR (trend analysis) — fixed: records store A_target, unrounded A_actual, p_capped_n2. summarize.py writes a trend
   table per (item, load, ρ, A_target, path_from): failures by n, pooled Wilson upper bound, and an exact-conditional
   (permutation) Cochran–Armitage test in log10 n (one-sided p for increasing and decreasing) when ≥ 1 failure.
   DESIGN.md now states the detectable effect (0/20 ⇒ Wilson upper 0.161 per cell) and that outcomes are finite-sample
   evidence; non-detection of a decline is not evidence of an asymptotic obstruction.
5. MAJOR (numerical validation) — fixed inside every run (read-only, ticket scorer unchanged): a Monitor hook compares
   the incremental gains with a fresh `PathState` recomputation at steps ≡ 199, 0 (mod 200) (the refresh boundary) and
   checks argmax agreement; a fresh recomputation at the endpoint gives the endpoint best gain; termination reason
   (stationary / move_limit), minimum top-two gap among improving scans, and `numerically_ok` = stationary ∧ fresh
   endpoint gain ≤ 0 ∧ no argmax disagreement are recorded. Runs with numerically_ok = False are reported as
   numerically inconclusive. Local check: max |incremental − fresh| 2e-11 (n 1e4, p 450) … 5e-7 (n 1e8, p 251).
6. MINOR (batch-2 policy) — fixed: `both_seeds` now means start=both on those seeds and [p] only on the others;
   gen_grid A2 generates it explicitly (10 seeds, both on 0–2).
7. MINOR (C2 eligibility / scope) — fixed: diagnostics only on states containing S₀ (`states_not_eligible` counted);
   C1 reported separately (`C1_start_eq_Sstar`); full-start paths labelled as (C2) with N = ∅; an oracle path from
   S*(N₀) is run whenever N₀ ≠ ∅ (`path_from = oracle_SstarN0`). The simultaneous-over-N claim is not tested (stated).
8. MINOR (w0 normalisation) — fixed: also distances / (w0 + n^{−1/3}) (`*_over_varpi1`) and `floor_over_w0`; C₀ stays
   explicit; growth of excursion/w0 is reported as a scaling diagnostic only.
9. MINOR (uncertainty output) — fixed: k/m and both Wilson ends for pure deletion, final = S₀, S₀ scored within cap,
   positive addition gain, numerically ok, C1 (mode paths), in CSV and Markdown.
10. MINOR (loading/sign confounding) — accepted: truth loadings and raw coefficients recorded per run; conclusions on
    item B stated conditionally on the arrays; prespecified sensitivity set x_BS1 (p 2000, n 1e5/1e6, 10 seeds):
    coef=rev (coefficient ↔ class pairing reversed) for the two-class designs, lseed 1, 2 (other continuous arrays).
