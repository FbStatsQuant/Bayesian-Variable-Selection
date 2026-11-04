# REPORT_C — analyze_phase2.R (executor C)

Script: `phase2/C_aggregate/analyze_phase2.R`, sha256 `e5d3f65437c31b52872cc1205d1d2a8377ad86fa2117ceb408ce37a267050633` (base R only; sources `desk/ENUM/exact_stratified.R` for `apply_size_prior`, no Rcpp needed). Helper `check_canaries.R` (sha256 `22541ad4…fe1e`) prints T1–T3 from the CSVs. Example output: `EXAMPLE_TABLES_dev_S1-S6_Bernoulli.md` (full dev run, 313 lines); scratch outputs in `C:\Users\felip\BVS_campaign_data\vs_20261013\phase2_C\`.

## Commands (Windows, R 4.4.1)
Main (dev): `Rscript analyze_phase2.R "<Others/.../precheck/output>,<S6_precheck>" NONE "<S6_strat>" "<S6_data_r051_100>" <out> "--ref=<Experiment_ 2/results/exact_references>"` (600 cases, 3.5 min).
Compare: `Rscript analyze_phase2.R --compare <old_dir> <new_dir> <out>`. Checks: `Rscript check_canaries.R <out>`.

## Tests (all on the dev run, no tuning)
- **T1 PASS**: S6 r1–100 exact Bern median 49, HPM 63; BB median 52, HPM 66. S1–S5 exact median 88/79/72/29/65, HPM 87/81/73/33/63. S6 r1–50 SMC (hybrid-mean) median = exact in 50/50.
- **T2 PASS**: stratified vs Exp-2 references, n=100: max|ΔlogZ| 1.4e-12, max|ΔPIP| 1.5e-12, MPM and HPM identical 100/100.
- **T3**: hybrid median |log Ẑ err| S1–S5 = 3.36e-4 / 3.39e-4 / 4.71e-4 / 6.48e-4 / 4.24e-4; hybrid-mean PIP MAE median = 8.13e-5 / 7.52e-5 / 9.46e-5 / 1.50e-4 / 9.26e-5 (targets matched to 2 digits). Uses the `--ref` Bernoulli fallback (exact_source = ref).
- **T4 PASS**: two full independent runs give byte-identical sha256 for all 11 output files (no RNG, no timestamps).
- **C3: FAIL at the stated 1e-12**: `apply_size_prior(Bern .2)` vs enumerator's stored `bernoulli$log_Z/pip`, n=100: max|ΔlogZ| = 2.8e-14 (passes), max|ΔPIP| = 1.34e-12 (just above 1e-12; floating-point summation order, still ≪ the 1e-8 of T2). Not tuned; reported in TABLES.md and `exact_c3_check.csv`.

## Amendment 1 additions (implemented)
Median/95th |log(Ẑ/Z)| next to RMSE(e); restricted-PIP MAE ([.05,.95]); exact-HPM-in-V; failure anatomy (ident / superset = truth strictly ⊂ selected / subset = selected strictly ⊂ truth / swap = same size ≠ truth / mixed = rest; exact rules in TABLES.md, SMC rules in CSV); Hamming; omission vs standardised signal β√(n−1)√(1−R²_j) (bins on |signal|: <2, 2–3, 3–4, 4–5, ≥5; exact median and HPM, both priors; needs X from data or SMC objects); exact P(|S|=|S*|) and P(HPM|y); engine-gate table (PASS/FAIL/NA per gate, hybrid Ẑ used for gates 1–2, 6); seed-SD table (`<id>__s<k>__precheck.rds` plus seed-0 file; pooled SD and BB/Bern ratio); Plan-2 block (R1–R3, printed values and which fire); compare mode (identical counts and max|Δ| for log_Z, log_Z_hybrid, visited n_models, pip_rb, pip_hybrid_mean, n_stages).
Tested paths with synthetic BB, seed and W files (labelled synthetic, scratch only; values meaningless): gate table, seed SD, Plan-2 block and compare mode execute and give the arithmetic expected by construction. No real BB or W output exists yet, so those sections are untested on real data.

## Interpretation choices (flag if wrong)
- R3 read as: ident(BB-HPM) < ident(Bern-HPM) − 10/100 OR < ident(Bern-median) − 10/100, over all W1–W6; thresholds scale with n.
- Gate "decision agreement ≥ 97 %" applied to each of median (hybrid-mean PIP), HPM, BFDR5 (min shown); "seed SD" uses hybrid log Ẑ, pooled over seed-subset datasets.
- Truth needs a data dir (or an SMC object, or `--ref`); exact-only cases without truth are listed in notes.txt and skipped for decisions. Pass the W data dir on Owls.
- BB rows for S1–S5 exist only once strat outputs exist; until then only a labelled "bernV" sensitivity (Bernoulli V reweighted to BB) is shown against truth.

## Owls command (full set)
```
Rscript $E/code/C_aggregate/analyze_phase2.R $E/out/smc_bern $E/out/smc_bb $E/out/enum_strat $E/data/S1-S6,$E/data/W1-W6 $E/out/analysis "--ref=<Exp2 exact_references dir, optional>" "--strat-r=$E/code/C_aggregate/exact_stratified.R"
```
(copy `exact_stratified.R` next to the script or pass `--strat-r`; all directory args accept comma lists; extra-seed files may sit in the same dirs.) Memory: one object at a time; est. 15–25 min for 1,200 × 2 engines.
