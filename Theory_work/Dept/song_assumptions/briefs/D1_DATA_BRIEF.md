# D1 brief — S1/S2 simulation-data analysis for TH-SONG-ASSUMPTIONS (Sonnet 5.5, effort high)

You are a mechanical data-analysis worker for the Theory Department Task Lead (mission TH-SONG-ASSUMPTIONS, 2026-11-27).
Goal: produce the empirical evidence that tests every conjectured assumption of our three target theorems on the S1/S2
simulation data. You do NOT write theorems; you compute and tabulate, honestly, including evidence AGAINST an assumption.

## Hard rules
- Workspace (write here only): `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/` —
  scripts in `scripts/`, tables in `tables/`, your report in `SIMULATION_DATA_ANALYSIS_draft.md`.
  Scratch only under `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/` (POLICIES §14: no /tmp, no scratch elsewhere).
- READ-ONLY: `/home/fb31/Bayesian-Variable-Selection/_local/engineering/` (NEVER write there) and the harness
  `/home/fb31/BVS-wt/P1M/Experiments/S1S2/` (never write there either). No Slurm / NOTS jobs. No new SMC fits.
- Owls compute discipline: `nice -n 19`, at most 16 cores, and ALWAYS `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
  GOTO_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1` in the shell before any Rscript (setting it inside R is too late).
  Budget: ≤ 8 CPU-h total; most items below are population (analytic) computations that need seconds.
- Do not commit or push; the Lead commits. Do not delete files.
- Also stage, for Codex workers that cannot read outside the worktree, compact read-only copies under
  `.rc_tmp/song/s1s2_ro/`: `theory_checks/P1.md`, `P2.md`, `p1_by_setting.tsv`, `p2_by_setting.tsv`, `p1_2x2.tsv`,
  `p1_extra_*.tsv`, `final/README.md`, `final/results_S1_smcbvs.md`, `final/results_S2_smcbvs.md`,
  `S1_comparison_final.md`, `S2_smcbvs_deliverable.md`, `diagnostics/bt2_diagnostic.md`, the settings TSVs, and the
  harness `specs/settings.tsv` + `harness/generate.R` (all small text). Note their source paths in a `SOURCES.md`.

## Inputs (read them first)
- `_local/engineering/reports/S1S2/theory_checks/P1.md`, `P2.md` (+ per-fit / by-setting TSVs, scripts/).
- `_local/engineering/reports/S1S2/final/` (results, README), `S1_comparison_final.md`, `S2_smcbvs_deliverable.md`,
  `S2_smcbvs_findings.tsv`, `diagnostics/bt2_diagnostic*.{md,tsv}`, `perf/` (skim `PROJECT_BRIEF.md`, `LEAD_STATE.md`,
  `scoreboard/` only for anything theory-relevant, e.g. N-ladders or prior variants tried).
- Generator: `/home/fb31/BVS-wt/P1M/Experiments/S1S2/harness/generate.R` and `specs/settings.tsv` — derive β (values,
  positions, signs), Σ (AR(1) ρ), σ² per setting EXACTLY as the generator does (population quantities need no seeds
  unless β/positions are random per rep; if they are random, use the stored seeds via gen_data, as P1 did).
- Theory context: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/prep/TH_PREP.md` §1, §2, §4, §4a, §4b.

## Model facts you need
Prior as coded (v3.1.1): standardised X, y; slab β_S|S,σ² ~ N(0, nσ²(X_SᵀX_S+I)⁻¹) (g = n, unit ridge); σ² ~ IG(0.01,0.01);
model prior BB(1,p) truncated at K = min(p, ⌊n/2⌋). Per-variable price of adding one predictor to a size-k model:
price(k) = log[(2p−1−k)/(k+1)] + ½ log(n+1). Population t²_j = n β_j² / [(Σ_S0)⁻¹]_jj / σ² (unit-variance AR(1)).

## Computations (one row per setting, 136 settings; S1 and S2 separately; report medians/shares by cell)
E0. Regime table: n, p, s0, ρ, SNR/ν, A = log p/log n, s0 log p/n, log p/n, (log p)²/n, log log p / log n,
    ε_n = √(s0 log p/n), √(log n/n), success rate (MPM = S0) and Wilson CI, failure-type shares.
E1. **Residual-signal margin (the key new test).** For each setting define the population signal μ = xᵀβ (x ~ N(0,Σ)) and,
    for any set S, R(S) = n·Var(xᵀβ | x_S) = n·β_Dᵀ Σ_{DD·S} β_D (D = S0∖S; Σ_{DD·S} the conditional covariance).
    Define the per-variable margin ratio κ(S) = R(S) / (2 σ² |S0∖S| · price(s0)). Compute:
    (a) single deletions S = S0∖{j}: κ_del = min_j κ(S0∖{j}) (this equals min t²/(2·price), cross-check vs P1's
        `gt2price_pop` column);
    (b) multi-deletions S = S0∖D, |D| ≤ 3 (exhaustive over D);
    (c) swaps/replacements S = (S0∖D) ∪ N with |D| ≤ 2 and N ⊆ nulls, |N| ≤ 4, searched greedily for the N that
        minimises R(S) (on AR(1) the minimising N are near neighbours of D; restrict the candidate pool to indices within
        distance 3 of S0 and verify on a few settings that widening the pool does not lower the min). Report
        κ_swap = min over these S of R(S) / (2σ²·|D|·price(s0)), and ALSO the "multiplicity-adjusted" version
        κ_swap' = R(S) / (2σ²·[|D|·price(s0) + |N|·log p ... ]) — define precisely: for a rival S with d = |D| deletions and
        m = |N| additions, the heuristic log posterior odds against S is ½R(S)/σ² − (d−m)·price(s0) − m·log(p) [prior +
        Occam + multiplicity]; report the minimum of this "odds margin" Λ(S) over the searched rivals, Λ_min, in nats, and
        Λ_min/log n.
    (d) κ_pop := min(κ_del, κ_multi, κ_swap) and Λ_min.
    Then, at the fit level (13,600 fits, using P1/P2 per-fit tables for exact recovery), tabulate 2×2 tables and AUCs for
    the predictors: [min t² > 2·price] (P1), [κ_pop > 1], [κ_pop > 1+η] for η ∈ {0, .1, .25, .5, 1}, [Λ_min > c·log n]
    for a scan of c — reporting sensitivity, P(exact | predictor yes), P(exact | no), separately for S1, S2, S2 by ρ ×
    beta_type. The question: does the swap-aware margin close the sufficiency gap of min t² (P(exact|yes) = 0.95 S1, 0.45 S2)?
    Also give, per S1 cell, the value of κ_pop at the empirical recovery transition.
E2. **Hellinger-scale screening margin (Song–Liang Thm 3 route).** For each true j: min over S ∌ j, |S| ≤ s0 + 4 of
    Var(xᵀβ | x_S)/σ² (population; use the same greedy search) and compare with ε_n² = s0 log p/n and with log n/n:
    report the ratios. (This tests the weaker "sure screening" margin.)
E3. **Song–Liang Condition 3 (identifiability, p. 955)** for Gaussian AR(1): var(x_k | any r others) ≥ (1−ρ²)/(1+ρ²);
    tabulate vs r̄ ε_n² for r̄ ∈ {s0, 2 s0, ⌈log n⌉·s0}. Analytic; confirm numerically on one setting.
E4. **Bounded signal (bs):** max_j |β_j| sd_j / σ (population sd_j = 1) and βᵀΣβ/σ² per setting.
E5. **Eigenvalue floors:** population λ_min(Σ_T) bound (1−ρ)/(1+ρ) and λ_min(Σ_S0) exact per setting; sample λ_min on S0
    (from P1 logs), sample floors at 2s0 and ⌈2(A+1)s0+2⌉ (from P1 E2). Also compute, from the population, the vanishing
    floor check λ_min(Corr(x_T)) ≥ c_ψ/n — trivially true; just state the margin.
E6. **Dimension regimes:** where each setting sits relative to (i) p ≤ n^A for A ∈ {1.5, 2, 3}; (ii) Song–Liang Cor S1's
    p < n^{κ log n}, κ < 1/4; (iii) log p ≤ n^{1/2}; (iv) log p = o(n). Also add a short table of "typical user regimes"
    (n, p) = (100, 1e3), (500, 1e4), (1000, 1e5), (5000, 1e6), (300, 2e4) [gene expression], (10^4, 5·10^5) [GWAS] with
    A = log p / log n.
E7. Re-tabulate (do not recompute) P2's E4 (Hellinger d_H/ε_n), E5 (size cap), E6 (σ² vs KL-projection σ_C²) headline
    numbers with exact file/column provenance, and P1's E2/E3. For E6 add: the share of failed fits whose MPM misses a
    true predictor but includes a neighbour (proxy behaviour, Song–Liang Cor 2 type), from the stored MPMs if available.
E8. Anything in `perf/` relevant to assumptions (e.g. prior/slab variants Engineering tried and their recovery effect) —
    summarise in ≤ 15 lines with paths.

## Output
`SIMULATION_DATA_ANALYSIS_draft.md` with: a provenance header (exact source files, script names, commands, CPU used);
one section per item E0–E8 with the table(s) and 2–4 lines of plain reading; an "evidence against" list; and a final
summary table "assumption → statistic → value range on S1 → on S2 → supports / weak / contradicts". Every number must
trace to a script in `scripts/` and a table in `tables/`. Validate: κ_del vs P1 population min t² (must agree to <2%),
and one R(S) by brute force (sample of a large simulated X) on one setting. When finished, reply with a ≤ 25-line summary.
