# Generator check (harness/check_generators.R)

Generated 2026-11-25 14:02 CST on owls.stat.rice.edu, R = 200 reps per setting (data seeds of INTERFACE.md, reps 1..200). PASS: |mean - target| <= 4 MC SE; deterministic rows exact to 1e-12.
Correlation targets are E r for population correlation r_k = rho^k, to O(1/n): r_k - r_k (1 - r_k^2) / (2n) (the sample correlation is biased toward 0; at n = 50, rho = 0.35 the bias is 0.003, several MC SE).

**Overall verdict: PASS** (58 checks, 0 FAIL)

| setting | label | check | estimate | MC SE | target | z | verdict |
|---|---|---|---|---|---|---|---|
| S1_03 | S1 n=500 p=500 SNR=2 | ||beta||_2 vs SNR sqrt(log p/n) sqrt(65) | 1.79766000 | 0.000000 | 1.7976600 | NA | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | sigma2 vs 1 | 1.00000000 | 0.000000 | 1.0000000 | NA | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | sample SNR Var(Xb)/s2 vs b'Sigma b | 1.27260000 | 0.005710 | 1.2772000 | -0.81 | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | support = 1,2,3,4,5,6,7,8,9,10 | NA | 0.000000 | NA | NA | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | Var(eps) vs sigma2 | 0.99978000 | 0.004540 | 1.0000000 | -0.05 | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | column variance vs 1 | 1.00010000 | 0.000479 | 1.0000000 | 0.19 | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | corr lag 1 vs E r(rho^1) | 0.59970000 | 0.000175 | 0.5996200 | 0.48 | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | corr lag 2 vs E r(rho^2) | 0.35994000 | 0.000246 | 0.3596900 | 1.03 | PASS |
| S1_03 | S1 n=500 p=500 SNR=2 | corr lag 5 vs E r(rho^5) | 0.07840900 | 0.000299 | 0.0776830 | 2.43 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | ||beta||_2 vs SNR sqrt(log p/n) sqrt(65) | 1.48811000 | 0.000000 | 1.4881100 | NA | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | sigma2 vs 1 | 1.00000000 | 0.000000 | 1.0000000 | NA | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | sample SNR Var(Xb)/s2 vs b'Sigma b | 0.87806000 | 0.002860 | 0.8752100 | 0.99 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | support = 1,2,3,4,5,6,7,8,9,10 | NA | 0.000000 | NA | NA | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | Var(eps) vs sigma2 | 1.00250000 | 0.003000 | 1.0000000 | 0.82 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | column variance vs 1 | 1.00010000 | 0.000357 | 1.0000000 | 0.18 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | corr lag 1 vs E r(rho^1) | 0.59991000 | 0.000136 | 0.5998100 | 0.76 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | corr lag 2 vs E r(rho^2) | 0.35996000 | 0.000184 | 0.3598400 | 0.63 | PASS |
| S1_15 | S1 n=1000 p=5000 SNR=2 | corr lag 5 vs E r(rho^5) | 0.07800800 | 0.000215 | 0.0777210 | 1.33 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | sample SNR Var(Xb)/s2 vs nu | 0.05069900 | 0.000714 | 0.0500000 | 0.98 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | sigma2 vs b'Sigma b/nu | 100.00000000 | 0.000000 | 100.0000000 | NA | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | support = 1,251,500,750,1000 | NA | 0.000000 | NA | NA | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | Var(eps) vs sigma2 | 97.95400000 | 1.340000 | 100.0000000 | -1.53 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | column variance vs 1 | 1.00060000 | 0.000933 | 1.0000000 | 0.65 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | corr lag 1 vs E r(rho^1) | 0.00094584 | 0.000685 | 0.0000000 | 1.38 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | corr lag 2 vs E r(rho^2) | -0.00063946 | 0.000746 | 0.0000000 | -0.86 | PASS |
| S2_001 | S2 high-5 bt=1 rho=0 nu=0.05 | corr lag 5 vs E r(rho^5) | -0.00160000 | 0.000772 | 0.0000000 | -2.07 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | sample SNR Var(Xb)/s2 vs nu | 0.70958000 | 0.010200 | 0.7100000 | -0.04 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | sigma2 vs b'Sigma b/nu | 7.04225000 | 0.000000 | 7.0422500 | NA | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | support = 1,251,500,750,1000 | NA | 0.000000 | NA | NA | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | Var(eps) vs sigma2 | 7.05840000 | 0.115000 | 7.0423000 | 0.14 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | column variance vs 1 | 1.00110000 | 0.001180 | 1.0000000 | 0.89 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | corr lag 1 vs E r(rho^1) | 0.34781000 | 0.000668 | 0.3469300 | 1.32 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | corr lag 2 vs E r(rho^2) | 0.12277000 | 0.000792 | 0.1212900 | 1.87 | PASS |
| S2_016 | S2 high-5 bt=1 rho=0.35 nu=0.71 | corr lag 5 vs E r(rho^5) | 0.00454620 | 0.000785 | 0.0051997 | -0.83 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | sample SNR Var(Xb)/s2 vs nu | 0.71225000 | 0.007290 | 0.7100000 | 0.31 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | sigma2 vs b'Sigma b/nu | 14.08450000 | 0.000000 | 14.0845000 | NA | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | support = 1,112,223,334,445,556,667,778,889,1000 | NA | 0.000000 | NA | NA | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | Var(eps) vs sigma2 | 14.10100000 | 0.138000 | 14.0850000 | 0.12 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | column variance vs 1 | 0.99918000 | 0.000786 | 1.0000000 | -1.05 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | corr lag 1 vs E r(rho^1) | 0.34863000 | 0.000457 | 0.3484600 | 0.37 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | corr lag 2 vs E r(rho^2) | 0.12193000 | 0.000562 | 0.1219000 | 0.06 | PASS |
| S2_076 | S2 high-10 bt=1 rho=0.35 nu=0.71 | corr lag 5 vs E r(rho^5) | 0.00554100 | 0.000560 | 0.0052259 | 0.56 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | sample SNR Var(Xb)/s2 vs nu | 5.97210000 | 0.061700 | 6.0000000 | -0.45 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | sigma2 vs b'Sigma b/nu | 6.92509000 | 0.000000 | 6.9250900 | NA | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | support = 1,2,3,4,5,6,7,8,9,10 | NA | 0.000000 | NA | NA | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | Var(eps) vs sigma2 | 6.87010000 | 0.064700 | 6.9251000 | -0.85 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | column variance vs 1 | 1.00230000 | 0.001200 | 1.0000000 | 1.93 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | corr lag 1 vs E r(rho^1) | 0.69880000 | 0.000363 | 0.6982100 | 1.61 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | corr lag 2 vs E r(rho^2) | 0.48876000 | 0.000539 | 0.4881400 | 1.15 | PASS |
| S2_120 | S2 high-10 bt=2 rho=0.7 nu=6 | corr lag 5 vs E r(rho^5) | 0.16743000 | 0.000825 | 0.1672500 | 0.21 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | sample SNR Var(Xb)/s2 vs nu | 0.72088000 | 0.010600 | 0.7100000 | 1.03 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | sigma2 vs b'Sigma b/nu | 12.30490000 | 0.000000 | 12.3049000 | NA | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | support = 1,2,3,4,5 | NA | 0.000000 | NA | NA | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | Var(eps) vs sigma2 | 12.24100000 | 0.165000 | 12.3050000 | -0.39 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | column variance vs 1 | 0.99978000 | 0.001030 | 1.0000000 | -0.22 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | corr lag 1 vs E r(rho^1) | 0.34622000 | 0.000672 | 0.3469300 | -1.05 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | corr lag 2 vs E r(rho^2) | 0.12120000 | 0.000782 | 0.1212900 | -0.12 | PASS |
| S2_046 | S2 high-5 bt=2 rho=0.35 nu=0.71 | corr lag 5 vs E r(rho^5) | 0.00514180 | 0.000852 | 0.0051997 | -0.07 | PASS |

## S1 generator against the authors' reference `lrrsg()` (HQ ruling 2026-11-25)

Reference: XitongLiang/The-PARNI-scheme @ `3b95d669e9bcf6df9e2ba46fb89fc536922e12e2` (Griffin is a co-author), clone at `ROOT/ext/The-PARNI-scheme@3b95d669…`.
- `R/simulation/dataset_generation.R:3-5,27`: n ∈ {500, 1000}, p ∈ {500, 5000, 50000}, SNR ∈ {0.5, 1, 2, 3}, `lrrsg(n, p, rho = 0.6, SNR, seed = NULL)`; lines 28-29: `X <- scale(dataset$X)`, `y <- scale(dataset$y, scale = FALSE)`.
- `R/simulation/linear regression random sample generator.R`: `beta_basis = c(2,-3,2,2,-3,3,-2,3,-2,3)` (l.5), `sigma2 = 1` default (l.7), positions `1:b_n` = 1..10 (l.15-17), `beta <- SNR * sqrt(sigma2 * log(p)/n) * beta` (l.19, natural log, σ² = 1), `X <- matrix(rnorm(n*p), n, p)` then the AR(1) recursion `X[,j] <- rho * X[,j-1] + sqrt(1-rho^2) * X[,j]` (l.21-27), `y <- a + X %*% beta + rnorm(n)` with a = 0 (l.31; the noise is N(0, 1), i.e. σ² = 1).
- Ours (`harness/generate.R`): the same Σ (AR(1), ρ = 0.6), the same β (σ² = 1, natural log p, positions 1..10), the same recursion and the same draw order (Z n×p column-major, then ε = rnorm(n)). So it is **not only the same law but the same draws**: called with `seed = data_seed`, `lrrsg()` returns our X, β and y bit for bit (table: max |Δy| = 0 at all 16 settings × reps 1–2). The seeds themselves are ours (INTERFACE). Our generator returns raw X and y (INTERFACE); the repo's `scale()` step is applied in the Bayesian adapters (HQ ruling (b)).

| setting | rep | X identical | β identical | max abs Δy | support = position |
|---|---|---|---|---|---|
| S1_01 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_01 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_02 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_02 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_03 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_03 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_04 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_04 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_05 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_05 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_06 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_06 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_07 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_07 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_08 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_08 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_09 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_09 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_10 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_10 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_11 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_11 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_12 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_12 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_13 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_13 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_14 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_14 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_15 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_15 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_16 | 1 | TRUE | TRUE | 0.0e+00 | TRUE |
| S1_16 | 2 | TRUE | TRUE | 0.0e+00 | TRUE |

## SMC-BVS: engine-internal preprocessing vs the repo preprocessing

`v3_fit` always calls `v3_preprocess` (core `v3_preprocess.R`, M §4.4, `v3_standardise`): every X column and y are divided by max|x|, centred and divided by the sample SD (n − 1). There is no intercept parameter; centring stands in for it. Feeding the engine the repo-preprocessed data (`scale(X)`, `scale(y, scale = FALSE)`) instead of raw data changes the engine's working input only by floating-point rounding:

| setting (rep 1) | max abs Δ standardised X | max abs Δ standardised y | max abs standardised X |
|---|---|---|---|
| S1_03 | 1.3e-15 | 8.9e-16 | 5.1e+00 |
| S1_15 | 1.8e-15 | 8.9e-16 | 5.0e+00 |

So the engine already does the equivalent of the repo preprocessing (it also scales y; because it standardises whatever y it receives, raw y and the repo's centred y reach the engine's model identically to rounding). The adapter passes raw X, y; no SMC smoke rerun is needed.
