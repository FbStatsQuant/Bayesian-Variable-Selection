# CONFIRMATION FREEZE — sealed set C restricted to S1–S6 (written 2026-10-14 before any C data exists)

Felipe's instruction (2026-10-14): run a confirmation round; the candidate is beta-binomial + HPM unless evidence says otherwise.
This file is frozen (sha256 recorded in RUNS.md) before C is generated. Nothing below changes after unsealing.

## Data
- C = S1–S6 × 200 datasets, generator `Benchmarks/shared/design.R` (sealed generator, copy in phase2/A_data_bern/design.R) with the data seed
  replaced by s = 508000 + 1000(k − 1) + r (k = 1..6, r = 1..200), fold seed s + 300000; everything else (Σ_k, truth, n = 100, p = 30) unchanged.
  Case ids S<k>_r<rrr> in their own directories (Owls `E/confirm/`, NOTS `Experiments_oct_13/confirm/`), never mixed with development data.
- Development data (S1–S6 r1–100, seeds 107000/108000 bands) was used for selection; C seeds have never been used.

## Engines and settings (frozen)
- engine_v2bb, code tar sha256 9793239dcfeabf677c5eb88033e60e344fee97dbdedaa5c40ce58026b45c5bf3 (read-only snapshot), N = 10,000, ESS 0.90,
  X-aligned blocks of 5, 1 Gibbs sweep per stage, 4 polish sweeps, unbounded visited set; SMC seed = data seed + 200000.
- Candidate: BB(a = 1, b = p = 30) + HPM (argmax over the visited set under the BB weights; ties broken by smaller size, then smaller code).
- Comparators (same build, Bernoulli mode h = 0.2): median model (hybrid sweep-mean PIP > .5; current rule), HPM, BFDR 5 %.
- Exact references: size-stratified enumerator (sha256 cpp 5fd23788…, R 40bed713…), exact BB and Bernoulli posteriors.

## Primary endpoint and win rule (SMC decisions; "identified" = selected set equals the true support)
Pooled over S1–S6 (n = 1,200 paired datasets):
- W1: BB-HPM identifies more than median@Bern, exact McNemar test on discordant pairs, two-sided p < .05 after Holm over {W1, W2}.
- W2: BB-HPM identifies more than HPM@Bern, same test, Holm-adjusted.
Candidate CONFIRMED if W1 and W2 hold and no guardrail fails. If W1 holds but W2 fails → BB-HPM is reported as "beats the current rule, not
distinguishable from Bern-HPM"; candidate kept but the prior's added value is unconfirmed. If W1 fails → evidence against; fallback is
Bern(0.2)+HPM, and the campaign returns to Fable.

## Guardrails (each failure is reported; G1–G3 failures block "CONFIRMED")
- G1 per scenario: BB-HPM not below HPM@Bern or median@Bern by more than 10/200.
- G2 swap stratum (S3, S4, S6 pooled, n = 600): BB-HPM not below any comparator by more than 12/600.
- G3 engine gates (BB vs exact BB): median |log Ẑ_hybrid err| ≤ 1e-3, 95th pct ≤ 1e-2, exact HPM in V ≥ 99 %, SMC HPM = exact HPM ≥ 97 % per scenario.
- G4 (report only): truth-included and mean Hamming per scenario; product-Ẑ error distribution and the count of |e| > 5 %.

## Written predictions (from development data, before unsealing)
- BB-HPM − median@Bern: dev +49/600 (selected among ~40 rule–prior pairs) → predicted +40 to +60 per 1,200 (i.e., +20 to +30 per 600).
- BB-HPM − HPM@Bern: dev +31/600 → predicted +30 to +50 per 1,200.
- Per scenario identification /200 (predicted ranges from dev ±1 binomial SE): S1 180–192, S2 170–186, S3 142–162, S4 56–76, S5 136–156, S6 120–142.
- Truth-included: BB-HPM below Bern-HPM by 3–8 per 100 in S1–S4 (dev); S4 Hamming higher under BB (dev 1.93 vs 1.72).
- Engine: all G3 gates pass; product Ẑ under BB has a heavy tail in S4/S5 (dev: 25/1,200 beyond 5 %).
