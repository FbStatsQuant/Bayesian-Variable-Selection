# PHASE 2 SPEC — deployment on Owls (lead, 2026-10-13; Felipe's greenlight 2026-10-13)

Single source of truth for every Phase-2 agent. Owls root: `E = /home/fb31/BVS/Experiment_10_13_2026` (Felipe's folder).
Local root: `Experiment/VS_Campaign_20261013/phase2/` (code and summaries only; no large data in OneDrive).

## Goal
Run the recommended strategy, BB(1,p) model prior + HPM inside the composite-start SMC, next to the current engine
(Bernoulli(0.2), median/HPM/BFDR) on 12 scenarios × 100 datasets, and report against the exact posterior of each prior:
(i) how often the true model is identified, (ii) RMSE of the percentage error of Ẑ (100(Ẑ/Z − 1)), (iii) PIP accuracy.

## Scenarios (12 × 100 = 1,200 datasets)
- **S1–S6 (existing sealed data, r = 1..100).** Copied from NOTS `~/projects/BVS/data` and `Benchmarks/data_S6`; on Owls at
  `E/data/S1-S6/<id>.rds`, `manifest.csv` (case_id, scenario, replicate, seed_data, sha256), all 600 hashes verified, read-only.
  Object fields: X (standardised, attrs), y, foldid, truth = list(beta, active, Sigma), scenario, replicate, seed_data, seed_folds, rng, R_version.
- **W1–W6 (new weak-signal stress, r = 1..100).** W_k uses the population covariance Σ_k of S_k (k = 1..6; Methodology Sec. "Common
  data-generating model", S6 = heterogeneous blocks ρ = .4..9). Data seed `s = 117000 + 1000(k−1) + r`; fold seed s + 300000.
  Per dataset, with `set.seed(s)` (Mersenne-Twister, Inversion, Rejection) and IN THIS ORDER:
  1. size m ~ uniform on {2, 3, 4} (`sample.int(3, 1) + 1`);
  2. m distinct population blocks C_b (blocks of 5: {1..5}, …, {26..30}) chosen uniformly (`sample.int(6, m)`), then one index
     uniformly within each chosen block (`sample.int(5, 1)` per block, in the order the blocks were drawn);
  3. signs ±1 equiprobable (`sample(c(-1, 1), m, replace = TRUE)`); magnitudes |β| ~ U(0.25, 0.45) (`runif(m, .25, .45)`);
  4. then, continuing the same RNG stream (no new set.seed), X and y with the same code path as the sealed-data generator
     (raw rows N_30(0, Σ_k), centre, scale with sd (n − 1), y = Xβ + N(0, 1), y not centred); foldid exactly as the generator
     does it with the fold seed. Sealed-data generator: `Experiment/Experiment_ 2/nots_mirror/Benchmarks/shared/design.R`
     (also `Others/BVS_Benchmarks/shared/prepare_data.R`); check it by regenerating S1_r001 and S6_r001 bit-identically.
  Truth varies across replicates (unlike S1–S6). Case ids `W<k>_r<rrr>`; same object fields as S data, scenario = "W<k>" stored
  as `scenario_label`, `scenario` = 10 + k (integer). Output `E/data/W1-W6/`, manifest.csv with sha256, read-only.
  Generator code is core code (CODE_LEDGER).

## Computations
1. **Exact (size-stratified enumerator, gated, CODE_LEDGER):** log Z_k, log N_jk, top-20 per size, for all 1,200 datasets.
   Gives the exact Z, PIPs, median model, HPM under Bernoulli(0.2) and BB(1,p) (apply_size_prior). Output `E/out/enum_strat/`.
   S6 r1–100 already done in `/home/fb31/BVS/vs_campaign_20261013/enum_stratified/out/` (to be copied after a data-hash check).
2. **Current engine (Bern):** FD1 engine v2, regime "both" (X-aligned blocks of 5, N = 10,000, ESS 0.90, 1 Gibbs sweep per stage,
   4 polish sweeps, unbounded visited set, Bernoulli(0.2), control slab, IG(.01,.01)); seeds blocks = data + 100000, SMC = data + 200000.
   Output "precheck" objects (fields exactly as `desk/S6V/run_s6_visited.R`) at `E/out/smc_bern/<id>__precheck.rds`.
   S1–S5 r1–100 already exist (brainstorm `Others/2_BVS_brainstorm_20261005/precheck/output/`, same engine and seeds) and S6 r1–50
   (`/home/fb31/BVS/vs_campaign_20261013/s6_visited/out/`); they are reused after a bit-reproduction check, the rest are run.
3. **BB engine (new):** FD1 engine v2 with model prior BB(a = 1, b = p) via the size-convolution start (below), same settings and
   seeds as 2. Output `E/out/smc_bb/<id>__precheck.rds`, same fields plus `prior = list(type = "betabinomial", a = 1, b = 30)`.

## BB engine maths (exact start; nothing else in the bridge changes)
Prior p(S) = B(a + |S|, b + p − |S|)/B(a, b). Block tables hold m̃_b(T) = composite marginal likelihood of T ⊆ C_b (no prior).
- Per-block size profiles c_k^(b) = Σ_{T ⊆ C_b, |T| = k} m̃_b(T); convolve over blocks: c_k = Σ_{|S| = k} Π_b m̃_b(S ∩ C_b).
- Z_0 = Σ_k c_k · B(a + k, b + p − k)/B(a, b) (exact, in logs).
- Start: draw k ∝ c_k B(a + k, b + p − k); draw block sizes (k_1..k_L) | k by backward DP on the partial convolutions;
  draw T_b ⊆ C_b with |T_b| = k_b ∝ m̃_b(T_b). This samples π_0(S) ∝ p(S) Π_b m̃_b(S ∩ C_b) exactly.
  Do NOT use "h ~ Beta, then S | h" (wrong: the h-marginal under π_0 is ∝ Beta(h) Z_0(h)).
- Bridge q_φ ∝ p(S) m̃(S)^{1−φ} m(S)^φ: incremental weights (Δφ)(log m − log m̃) unchanged.
- Gibbs log-odds for j given S_−j (k = |S_−j|): log((a + k)/(b + p − k − 1)) + φ Δ log m + (1 − φ) Δ log m̃. RB PIPs use the same conditional.
- Visited set / hybrid estimator: same, with the BB log prior in the weights.
- Bernoulli mode of the modified engine must reproduce engine v2 bit-for-bit (same seed → identical outputs).

## Decision rules scored (per prior, SMC and exact)
median (PIP > .5), HPM (max posterior over V for SMC; exact HPM from the stratified top-20), BFDR 5 % (definition as in
`Others/2_BVS_brainstorm_20261005/precheck/eval_rules3.R`). Primary SMC PIP for decisions: hybrid sweep-averaged (`pip_hybrid_mean`);
RB (`pip_rb`) reported as sensitivity. "Identified" = selected set equals the true support exactly.

## Metrics (per scenario, 100 datasets; for each engine against the exact posterior of its own prior)
- Identification counts / 100 for every rule × prior (SMC and exact) + SMC-decision = exact-decision agreement; FP, FN, truth included.
- Z: e = 100 (Ẑ/Z − 1) for Ẑ = product (telescoping) and Ẑ = hybrid. Report RMSE(e), mean(e) (bias), median |e|, max |e|.
- PIP: per dataset MAE over the 30 variables, max abs error, RMSE; report median and mean over datasets, for plain, RB (final
  sweep), RB-polish, hybrid, hybrid-mean.
- Cost: wall seconds per run, number of stages.

## Compute rules
Owls only; leave ≥ 12 of the 80 cores free for other users (cs222 currently uses 40). Lead launches all multi-dataset jobs;
code frozen to `E/runs/<UTC>_<piece>/code/` (read-only) with manifest.json; RUNS.md in the campaign root.

## AMENDMENT 1 (after Gate A, fable/04 + PLAN_REVIEW_PHASE2.md; binding, supersedes conflicting text above)
- **No reuse of old Bernoulli SMC outputs.** All 1,200 Bernoulli runs are re-run with the new build (engine_v2bb in
  `model_prior = "bernoulli"` mode, bit-identical to engine v2), so both engines share one code hash. The 550 old outputs
  (S1–S5 brainstorm, S6 r1–50) are kept as a reference and compared field by field (log Ẑ product/hybrid, |V|, PIPs, stages).
- **Pre-registered Plan-2 rule (exact posteriors).** BB(1,p)-HPM is demoted and Bern(0.2)-HPM becomes the confirmatory candidate if ANY:
  R1 pooled W1+W2: ident(BB-HPM) < ident(Bern-HPM) − 10/200; R2 pooled W1+W2: mean FN(BB-HPM) > mean FN(Bern-HPM) + 0.3;
  R3 any single W_k: BB-HPM below Bern-HPM or median@Bern by > 10/100. W3–W6 are descriptive otherwise.
  Written prediction (Fable): W1 Bern-HPM/median ≈ 30–40, BB-HPM ≈ 15–25; R1 likely fires.
- **Extra metrics.** |log(Ẑ/Z)| median and 95th percentile (product, hybrid); restricted-PIP MAE (variables with exact PIP in
  [.05,.95]); exact-HPM-in-V rate; failure anatomy (superset/subset/swap/mixed) per scenario × prior × rule; per-variable
  omission rate vs standardised signal β√(n−1)√(1−R²_j) (binned); Hamming (FP+FN); truth-included; exact P(|S| = m_true) and
  P(HPM | y) per prior.
- **Engine gates (BB vs exact BB):** median |log err| ≤ 1e-3, 95th ≤ 1e-2, HPM ∈ V ≥ 99 %, decision agreement ≥ 97 %,
  restricted MAE(BB) ≤ 2× Bern, seed SD(log Ẑ) BB ≤ 2× Bern on the seed subset.
- **Seed-SD subset:** 10 datasets (r1–10) × 2 extra SMC seeds (data + 200000 + 50000·s, s = 1, 2) × both engines × {S1, S4, S6, W1, W6} = 200 runs.
- **Launch checks:** m = m̃ run returns Z_0 to 1e-10; S = ∅ handled in start and Gibbs; 25-dataset BB pilot
  (5 × {S1, S4, S6, W1, W6}) passes the gates before the 1,200 job.
