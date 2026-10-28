# SITREP v1 — VS strategy campaign (2026-10-13, lead)

Everything known, condensed. Thinkers and Fable work from this file and FAILED_ATTEMPTS.md only.

## 1. The model and the sampler
- Gaussian linear regression, n = 100, p = 30, X columns standardised, y not centred, no intercept.
  beta_S | sigma^2 ~ N(0, sigma^2 Lambda_S^{-1}), Lambda_S = (X_S'X_S + I)/n ("control" slab: g-prior g = n plus unit ridge);
  sigma^2 ~ IG(0.01, 0.01); model prior Bernoulli(h = 0.2), prior mean size 6.
  Closed-form score l(S) = log m(S) (Cholesky, O(|S|^3)). Posterior pi(S) ∝ p(S) m(S) on 2^30 models; PIP pi_j; evidence Z.
- SMC: composite start pi_0(S) ∝ p(S) prod_b m_b(S ∩ B_b) over blocks of 5 (random or X-aligned clustering), sampled exactly,
  Z_0 known. Geometric bridge q_phi = p(S) m~(S)^{1−phi} m(S)^phi, adaptive steps keeping incremental ESS >= 0.9 N, N = 10,000,
  systematic resampling every stage, one systematic-scan Gibbs sweep per stage. Outputs: N joint model draws, Z-hat (telescoping),
  plain PIPs, Rao–Blackwell PIPs (final sweep at phi = 1). FD1 engine v2 adds X-aligned blocks (stages halve in S3–S5),
  K = 4 polish sweeps at phi = 1, and an unbounded visited set V with exact log m(S) per scored model ("hybrid" estimator:
  exact mass over V + SMC estimate of the outside share f ~ 0.003).
- Exact reference: full 2^30 enumeration (C++), ~220 s per dataset on NOTS; used only for validation.

## 2. Accuracy (settled)
| | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Exp. 2 rerun, product Z-hat: MAE of relative Z error (%) | 0.80 | 0.94 | 1.37 | 2.01 | 1.25 |
| FD1 engine v2 hybrid, median abs log Z error (500 runs) | 3.4e-4 | 3.4e-4 | 4.7e-4 | 6.5e-4 | 4.2e-4 |
| RB PIP MAE, median (frozen engine) | 5e-5 | 1e-4 | 3e-4 | 8e-4 | 2.5e-4 |
| Hybrid sweep-averaged PIP MAE, median | 8.1e-5 | 7.5e-5 | 9.5e-5 | 1.5e-4 | 9.3e-5 |
SMC median/BFDR decisions = exact decisions in 97–100 % of datasets; PARNI (MCMC on the same target) = exact MPM in 96–100 %.
Conclusion: at p = 30 the sampler reproduces the exact posterior. Selection quality is a property of (target, decision rule),
not of the sampler. Any gain must come from the target (priors), the decision functional, or reporting resolution.

## 3. Scenarios (truth fixed across replicates)
S1–S5: S* = {2,3,8,14,19}, beta = (1, −1, 0.6, −0.8, 0.5), sigma = 1. Population blocks of 5: C1 = {1..5} holds the
cancelling pair (2,3); C2, C3, C4 hold one signal each (8, 14, 19); C5, C6 null.
S1 independent; S2 AR(1) 0.5; S3 within-block rho .7; S4 within-block rho .85; S5 within .7 + between .3.
S6: six independent blocks, rho = .4,.5,.6,.7,.8,.9; one signal per block, S* = {4,6,11,16,22,30},
beta = (2.3, −1.2, 0.9, −0.8, 0.7, −0.6) — weakest effects in the most correlated blocks.
Seeds: S1–S5 data 108000 + 1000(k−1) + r, S6 107000 + r (r = 1..100); blocks +100000, SMC +200000.

## 4. Selection results so far (exact recovery, count out of 100)
| Rule (control slab) | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| Median, Bernoulli(0.2) (CURRENT) | 88 | 79 | 72 | 29 | 65 | 49 |
| BFDR 5 %, Bernoulli(0.2) (current, best BFDR) | 93 | 87 | 57 | 12 | 56 | – |
| HPM, Bernoulli(0.2) | 87 | 81 | 73 | 33 | 63 | 63 |
| HPM, beta-binomial BB(1,p) [brainstorm, V-reweighted] | 93 | 90 | 76 | 33 | 73 | not run |
| Median, BB(1,p) | 92 | 89 | 72 | 30 | 70 | not run |
| PARNI plain PIP > .5 (same posterior) | 88 | 79 | 72 | 28 | 65 | 50 |
| SuSiE PIP > .5 (L = 10, refine = FALSE) | 90 | 82 | 24 | 0 | 12 | 54 |
| Best subset + BIC / + EBIC_1 | 37/86 | 34/80 | 42/72 | 18/29 | 34/61 | 27/58 |
| SSL (older bvs7 run) | 56 | 63 | 51 | 30 | 46 | – |
Truth included (median rule, Bernoulli 0.2): 99/97/82/38/80.
BB(1,p) robustness (HPM): BB(1,p/2) 92/87/76/33/70; BB(1,2p) 92/91/75/30/72; BB(1/8,p) 93/90/75/31/71.
BLiP q = .05 resolution-adjusted success (every true signal covered, no false region): Bern(0.2) 92/88/79/53/75; BB(1,p) 86/87/83/53/76.

## 5. Failure anatomy (exact posterior, Bernoulli(0.2); counts out of 100)
| | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| HPM superset (truth + extras) | 12 | 18 | 11 | 12 | 19 | 9 |
| HPM subset (omission) | 1 | 1 | 3 | 2 | 4 | 0 |
| HPM within-block swap (proxy replaces signal) | 0 | 0 | 11 | 41 | 13 | 26 |
| HPM mixed | 0 | 0 | 2 | 12 | 1 | 2 |
| MPM subset (omission) | 1 | 2 | 7 | 18 | 7 | 20 |
| MPM swap | 0 | 0 | 8 | 26 | 8 | 18 |
Under BB(1,p) (HPM, S1..S5): superset 2/6/4/4/8, subset 5/4/4/12/7, swap 0/0/14/34/11, mixed 0/0/2/17/1.
- Supersets in S1/S2/S5 are multiplicity extras (null variables with BF near 1); a multiplicity-correcting size prior removes most.
- Swaps are likelihood-driven: in cycle 1 (rho .85) the truth was the best-RSS size-5 subset in only 11/20 datasets; the lost
  variable is always a weak signal (8, 19; in S6 variable 30, beta −.6 in the rho .9 block: HPM lost 30 in 27/100, MPM in 42/100).
  Within a model size, a size-only prior cannot change the ranking: HPM = argmax_k [w(k) · max_{|S|=k} m(S)].
- MPM omissions in S4/S6 come from posterior mass split among within-block proxies (each PIP < .5 although the block is
  occupied with probability ~1); HPM avoids that (S6: MPM 49 vs HPM 63).
- Block certificates (top configuration of a cluster has mass >= .9) were never wrong when they fired but fired rarely under
  Bernoulli(0.2): null predictors keep PIP ~ .05 each, so P(null block empty) ~ .75.

## 6. Open facts (not yet measured)
- BB(1,p) or any sparser prior on S6 (risk: more omissions of variable 30).
- BB(1,p) inside the SMC (prior tempered along the bridge from a factorised surrogate) and its Z/PIP accuracy against an
  enumerator with the BB log-prior line. Only V-reweighting has been validated, for a Bernoulli prior.
- Fresh-seed confirmation of any rule (the 600 current datasets were used to choose among ~30 combinations).
- Per-scenario ceiling: fraction of datasets where the truth is the best m(S) model of its own size.
- Large-p behaviour (p in the hundreds): no enumerator; the visited set and HPM search must scale.

## 7. Constraints (Felipe's rules)
SMC-based; decision = functional of SMC output (particles, RB conditionals, V with exact scores, Z, block tables);
scalable to large p; target changes need inference-grounded justification (not tuned to S*) and a closed-form or cheap score;
goal is to beat the current rule and be competitive with the best benchmark, while Z and PIP accuracy (vs exact for the target
used) is no worse than now.

## 8. Update 2026-10-13 (lead desk check, S6 r1–50, V-reweighting; canaries: V median and HPM = exact 50/50)
| prior (S6, out of 50) | HPM correct | HPM swap | median correct | median subset |
|---|---|---|---|---|
| Bernoulli(0.2) | 34 | 11 | 28 | 9 |
| BB(1,p) | 36 | 11 | 30 | 9 |
| BB(1,p/2) | 36 | 11 | 29 | 9 |
| BB(1,2p) | 36 | 12 | 30 | 9 |
| Bernoulli(1/(p+1)) | 37 | 11 | 30 | 10 |
| BB(1,1) | 32 | 11 | 26 | 7 |
BB(1,p) does not hurt S6; swaps (11/50) are unchanged by any size prior, as expected. File: desk/LEAD/s6_priors_r001_050.csv.
Exact confirmation (stratified enumerator, S6 r1–50): exact HPM/median under the six size priors agree with the V-reweighting
screen in 300/300 (HPM) and 299/300 (median) prior-dataset pairs; the counts above are exact. File desk/LEAD/s6_exact_priors_r001_050.csv.

## 9. Ceilings and evidence (D1, 500 S1–S5 dev datasets; canaries passed 7000/7000 cells)
| | S1 | S2 | S3 | S4 | S5 | total |
|---|---|---|---|---|---|---|
| Truth = best m(S) of its size (ceiling of ANY size prior + HPM) | 100 | 98 | 83 | 43 | 85 | 409 |
| Truth within 1 nat of best of its size | 100 | 99 | 90 | 70 | 92 | |
| BB(1,p) HPM (best fixed size prior so far) | 93 | 90 | 76 | 33 | 73 | 365 |
| Bern(0.2) HPM / median (current) | 87/88 | 81/79 | 73/72 | 33/29 | 63/65 | 337/333 |
Headroom left for size-prior/decision functionals over BB-HPM: +7/+8/+7/+10/+12 (44 datasets); beyond that only structured
priors that change within-size ranking, or a different reported object.
- Evidence: Bern(0.2) has the highest Z_V in 500/500 datasets (V truncated under Bern(0.2) weights, so slightly favoured);
  "evidence-chosen size prior" = Bern(0.2) → EB over size priors gives nothing (confirms T2).
- Size posterior: P(|S| = 5) mean .26–.29 under Bern(0.2) (mode = 5 in 13–41/100); .40–.50 under BB(1,p) (mode = 5 in 62–83/100).

## 10. S6 exact, all 100 datasets (stratified enumerator; Bern(0.2) median 49 / HPM 63 reproduce Experiment 2 exactly)
| prior | HPM correct | HPM swap | median correct |
|---|---|---|---|
| Bern(0.2) | 63 | 26 | 49 |
| BB(1,p) | 66 | 27 | 52 |
| BB(1,2p) | 66 | 29 | 53 |
| Bern(1/(p+1)) | 67 | 29 | 52 |
r51–100 is the harder half (BB-HPM 30 vs 36 in r1–50); BB-HPM beats Bern-HPM in both halves (+2, +1). File desk/LEAD/s6_exact_priors_r001_100.csv.

## 11. Round-1 outcome (2026-10-13)
On D the frontier is BB(1,p)+HPM; every other functional/prior tested is at or below it (CANDIDATES.md). Costs: truth-included −4 (S1) vs
median, −3 to −8 vs Bern-HPM in S1–S4; S4 Hamming 1.72 → 1.93; S4 cancelling pair both-selected 86 → 72. Five ranked plans in PLANS_FOR_TODAY.md.

## 12. Phase 2 outcome (2026-10-13; RESULTS_PHASE2.md, red team RT2)
12 scenarios × 100 (S1–S6 sealed + W1–W6 weak-signal), both engines vs exact posteriors of their own prior. Pre-registered Plan-2 rule FIRED
(R1 −28/200, R2 +0.69 FN, R3 in W1, W2, W5): BB(1,p)+HPM withdrawn. Totals (SMC = exact for HPM in 2,400/2,400): S /600 — Bern median 382,
Bern HPM 400, BB HPM 431, BFDR5 340; W /600 — 104, 128, 63, 28. BB trades omissions for fewer false inclusions; its omission rate is higher in
every signal bin. Accuracy: both engines pass all gates on the hybrid Ẑ (RMSE ≤ 0.16 %); BB's particle-only estimates are 1.0–1.9× worse and its
product Ẑ has heavy outliers (S5_r005 fails systematically, −27 to −89 % over 4 seeds). Bern(0.2)+HPM (the existing HPM baseline, no change to
target or engine) is the best rule over all 12 scenarios; its edge over the median comes from S6 and W, not S1–S5.
