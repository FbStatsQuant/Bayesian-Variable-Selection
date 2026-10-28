# RESULTS — Phase 2 (12 scenarios × 100 datasets, two engines), 2026-10-13
Provisional: core code is AI-written and unreviewed (CODE_LEDGER.md). Full tables: Owls `/home/fb31/BVS/Experiment_10_13_2026/out/analysis_full/TABLES.md`
(local copy `C:\Users\felip\BVS_campaign_data\vs_20261013\phase2_full\analysis_full\`). Red team: redteam/RT2_phase2.md.

Engines: Bern = current composite-start SMC (FD1 engine v2 "both", Bernoulli(0.2)); BB = same engine with BB(1,30) prior via the exact
size-convolution start. Each engine is scored against the exact 2^30 posterior of its own prior. One SMC run per dataset (N = 10,000).
S1–S6: sealed datasets (fixed truth per scenario). W1–W6: weak-signal stress (Σ of S_k; 2–4 true variables, |β| ~ U(.25,.45), random truth).

## 1. Exact model identified (SMC decisions; count / 100)
| rule | S1 | S2 | S3 | S4 | S5 | S6 | **S total /600** | W1 | W2 | W3 | W4 | W5 | W6 | **W total /600** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bern median (current) | 88 | 79 | 72 | 29 | 65 | 49 | **382** | 40 | 23 | 11 | 5 | 11 | 14 | **104** |
| Bern BFDR 5 % (current) | 93 | 87 | 56 | 12 | 56 | 36 | **340** | 20 | 5 | 0 | 0 | 1 | 2 | **28** |
| Bern HPM | 87 | 81 | 73 | 33 | 63 | 63 | **400** | 42 | 23 | 15 | 9 | 19 | 20 | **128** |
| BB median | 92 | 89 | 72 | 30 | 70 | 52 | **405** | 24 | 11 | 4 | 5 | 2 | 6 | **52** |
| BB HPM | 93 | 90 | 76 | 33 | 73 | 66 | **431** | 25 | 12 | 5 | 5 | 4 | 12 | **63** |
SMC decision = exact decision: HPM 2,400/2,400 (both priors); median (hybrid PIP) Bern 1,196/1,200, BB 1,199/1,200; BFDR 5 % ≥ 99/100 per scenario.
Exact HPM is in the SMC visited set in 2,400/2,400. Lead's independent recount of exact HPM from raw enumerator output: 24/24 cells match.

## 2. Z: RMSE of the percentage error 100(Ẑ/Z − 1) over 100 datasets
| estimator | S1 | S2 | S3 | S4 | S5 | S6 | W1 | W2 | W3 | W4 | W5 | W6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bern hybrid | 0.055 | 0.053 | 0.077 | 0.098 | 0.069 | 0.062 | 0.116 | 0.107 | 0.134 | 0.154 | 0.112 | 0.127 |
| Bern product | 1.05 | 1.10 | 1.32 | 1.58 | 1.33 | 1.74 | 0.57 | 0.73 | 0.84 | 0.91 | 0.89 | 0.65 |
| BB hybrid | 0.039 | 0.038 | 0.041 | 0.066 | 0.042 | 0.050 | 0.035 | 0.038 | 0.043 | 0.057 | 0.028 | 0.054 |
| BB product | 1.17 | 1.22 | 1.76 | **4.58** | **5.16** | 2.17 | 0.56 | 0.56 | 0.52 | 0.66 | 1.00 | 0.64 |
Max |error| hybrid: Bern 0.45 %, BB 0.25 %. BB product: 25/1,200 datasets beyond 5 %, 3 beyond 10 % (S5_r005 −48 %, S4_r065 −25 %, S4_r014 −23 %); Bern product: none beyond 5 %.
Reruns with 3 more seeds: S5_r005 product error −27 % to −89 % on every seed (systematic: the BB bridge loses mass on this dataset), the four S4 cases
swing ±25 % (variance); hybrid within 0.15 % on all reruns. Seed-to-seed SD of log Ẑ (10 datasets × 3 seeds, S1, S4, S6, W1, W6): hybrid BB/Bern
ratio 0.29–0.90; product 1.03–1.29.

## 3. PIP accuracy (median over datasets of the per-dataset MAE over 30 variables)
| estimator | S1 | S2 | S3 | S4 | S5 | S6 | W1 | W2 | W3 | W4 | W5 | W6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bern plain | 1.4e-3 | 1.4e-3 | 1.6e-3 | 1.9e-3 | 1.5e-3 | 1.7e-3 | 1.6e-3 | 1.8e-3 | 1.9e-3 | 2.1e-3 | 1.8e-3 | 1.9e-3 |
| Bern RB | 5.5e-5 | 1.2e-4 | 2.9e-4 | 7.8e-4 | 2.5e-4 | 4.4e-4 | 1.1e-4 | 2.9e-4 | 5.3e-4 | 7.1e-4 | 4.9e-4 | 4.9e-4 |
| Bern hybrid (sweep-mean) | 8.1e-5 | 7.5e-5 | 9.5e-5 | 1.5e-4 | 9.3e-5 | 8.1e-5 | 1.5e-4 | 1.7e-4 | 2.0e-4 | 2.3e-4 | 1.6e-4 | 2.0e-4 |
| BB plain | 1.0e-3 | 1.0e-3 | 1.1e-3 | 1.6e-3 | 1.1e-3 | 1.4e-3 | 8.7e-4 | 9.3e-4 | 1.2e-3 | 1.3e-3 | 1.2e-3 | 1.2e-3 |
| BB RB | 4.7e-5 | 7.1e-5 | 2.7e-4 | 9.2e-4 | 2.0e-4 | 4.7e-4 | 6.2e-5 | 1.5e-4 | 3.0e-4 | 5.2e-4 | 2.8e-4 | 2.8e-4 |
| BB hybrid (sweep-mean) | 5.0e-5 | 4.9e-5 | 5.8e-5 | 9.1e-5 | 5.5e-5 | 6.5e-5 | 4.7e-5 | 5.3e-5 | 6.3e-5 | 7.3e-5 | 4.6e-5 | 6.2e-5 |
On variables with exact PIP in [.05,.95] (restricted MAE), BB/Bern ratio: hybrid 0.35–0.83 (BB better), RB 0.96–1.85 (BB worse; S4 1.85).
Red-team reading: BB's better visited-set numbers come from its more concentrated posterior (smaller outside share), not a better sampler;
its particle-only estimates (product Ẑ, RB/plain PIPs on uncertain variables) are 1.0–1.9× less accurate.

## 4. Pre-registered decision (Amendment 1, exact posteriors) — FIRED
R1 W1+W2: BB-HPM 37/200 vs Bern-HPM 65/200 (−28; bar −10). R2: mean FN 1.54 vs 0.85 (+0.69; bar +0.3). R3: W1 −17, W2 −11, W5 −15 (bar −10).
→ BB(1,p)+HPM is withdrawn as the proposed change. It trades omissions for fewer false inclusions: it wins only where extra null variables are the
main failure (S1, S2, S5: FP .03 vs .13 in S1) and loses heavily on small, weak truths (W: omission rate in signal bin 3–4: .60 vs .38).
Bern(0.2)+HPM — no prior change, no engine change — beats the current median on both sets (S 400 vs 382; W 128 vs 104), driven by S6 (63 vs 49) and
W (discordant pairs 27 vs 3); on S1–S5 alone HPM vs median is a wash (discordant 18 vs 14). BFDR 5 % remains best in S1–S2 (93/87).

## 5. Checks
Rebuilt engine in Bernoulli mode vs the 550 old runs: same |V| and stages in 550/550, log Ẑ ≤ 8e-13, S6 bit-identical. Enumeration: 1,200/1,200
files carry the sealed data hash and 2^30 models (430 Owls + 770 NOTS; NOTS smoke = Owls to 1e-13). Analysis deterministic (two runs byte-identical).
C3 "FAIL" in TABLES.md is a 3e-12 rounding difference (tolerance 1e-12). Red team: no bugs; wording corrections adopted above.
