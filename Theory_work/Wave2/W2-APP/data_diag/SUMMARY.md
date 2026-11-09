# W2-APP data_diag: design-only diagnostics of public high-dimensional regression designs

Date: 2026-11-09. Numbers only: nothing here claims that any theorem applies. All results depend on the design X alone, except the clearly labelled plug-in (f) for riboflavin and diabetes_quad (the y passed to the production block context does not affect the blocks). Everything is in `Theory_work/Wave2/W2-APP/data_diag/`; no git commands were run.

## 1. What was run and where each design came from

| design | source (exact) | n x p raw | used |
|---|---|---|---|
| riboflavin | `hdi` 0.1-10 from the CRAN Archive (hdi was archived on CRAN 2026-07-10): https://cran.r-project.org/src/contrib/Archive/hdi/hdi_0.1-10.tar.gz, tarball md5 `e7cf1f703e575b5ac3acfdef79b2aa84`; only `hdi/data/riboflavin.RData` (md5 `2ea5489eabefbaa5ff1fe91d28b2b509`) and `data/datalist` were extracted into `downloads/hdi/` (loaded with `load()` only; nothing from the tarball was executed). X = `riboflavin$x`, y = `riboflavin$y` | 71 x 4088 | all |
| tecator (Fat spectra) | `fds` 1.8, R 4.4 library (`...win-library/4.4`), `data/Rdata.rdb` md5 `f0dd4959982d1ef5e6346cfa53f2892b`, object `Fatspectrum$y` (100 wavelengths x 215 samples) transposed | 215 x 100 | all |
| iclaims | `bsts` 0.9.10, R 4.4 library, `data/iclaims.RData` md5 `e96e68697531b9dbeffbded63b4ee8a2`, `initial.claims[,-1]` (the 10 Google-Trends columns; `iclaimsNSA` is the response and is excluded); weekly 2004-01-04..2012-09-23 | 456 x 10 | all |
| fred_qd | `BVAR` 1.0.5, R 4.4 library, `data/Rdata.rdb` md5 `e8a6695491a756245ea9cf99f02d03d8`, transformation table `fred_trans.csv` md5 `3c729ac3b865bcb93934ab5e2c3506ee`. 63 of 233 columns have NA and were dropped; the remaining 170 were transformed with BVAR's own code table (none / 1st-diff / log-diff x100 / log-2nd-diff x100 / pct-ch-diff); the BVAR namespace cannot be loaded under R 4.6, so `BVAR:::get_transformation` (lag 1, scale 100) was re-implemented in `prep_data.R`; first 2 rows (lost to differencing) dropped, no non-finite values. 1959-09..2023-09 | 259 x 233 -> 257 x 170 | all 170 |
| fred_md (extra) | same package/files; 19 of 118 columns have NA and were dropped, 99 kept, same transformation procedure | 777 x 118 -> 775 x 99 | all 99 |
| diabetes_quad | scikit-learn 1.4.2 `load_diabetes(scaled=True)` (`diabetes_data_raw.csv.gz` md5 `5a4dae33d045eae5db445e5260a3287c`); Efron et al. (2004) quadratic model built by `prep_sklearn.py` from unit-variance main effects: 10 main + 45 pairwise products + 9 squares (no `sex^2`) = 64 columns | 442 x 64 | all |
| spam | `kernlab` 0.9-33, R 4.4 library, `data/spam.rda` md5 `9d87dc369ed3c41bf2ad51a18a1ac544`, `spam[,1:57]`, raw word/character frequencies (no transformation) | 4601 x 57 | all |
| digits | scikit-learn 1.4.2 `load_digits` (`digits.csv.gz` md5 `9b335364a7bfd63947c7480a5bd51f2d`), 64 pixels | 1797 x 64 | 61 (3 constant pixels dropped) |

No constant or duplicate (|r| > 1-1e-10) columns existed except the 3 constant digits pixels. Columns were centred and scaled to unit sample variance; R = X'X/(n-1) (via the SVD of the scaled matrix when p > n).

Methods (all in `diag_lib.R`; thin per-design drivers `diag_<name>.R`; data export in `prep_data.R` / `prep_sklearn.py`):
- (b) eigenvalues from the SVD; "#factors" = argmax_{k=1..9} lambda_k/lambda_{k+1} (Ahn-Horenstein ER; k <= 9 only). Smallest eigenvalue reported only if p < n.
- (c) partner counts #{k: |r_jk| > tau} per variable (median / 90% / max; full tables in `out_<name>_partners.csv`); then the same after projecting out the top-k PC scores (columns rescaled to unit variance; all columns had residual variance share > 1e-8). "null ref max abs r" is the rough reference sqrt(2 log(p(p-1)/2)/n), the size of the largest |r| among p(p-1)/2 pairs of independent Gaussian columns; it is context only.
- (d) phi^2(k) = min over |S|=k of lambda_min(R_S). Labels: **EXACT** = true value (k=2: 1-max|r|; full enumeration whenever C(p,k) <= 2e5, which covers iclaims for every k <= 10; all triples whenever C(p,3) <= 5e7, i.e. p <= 668, via a closed-form 3x3 minimum eigenvalue (checked against `eigen` to 1.6e-15, and the pruned scan below was checked against the full scan on fred_qd, `out_test_checks.txt`); for larger p a Gershgorin-pruned exact triple scan, which did not finish within its work cap on riboflavin (1.5e9 triple visits in the first run, 2e8 in the final run), so riboflavin has **no** exact k=3 value). **UB** (upper bound on phi^2, i.e. a witness set's lambda_min): greedy search that adds the column minimising lambda_min (solved exactly for all candidates by the secular equation, rigorous bracket pruning), from the most correlated pair, from every exact minimiser, and from random pairs among the top-500 most correlated pairs, followed by a 1-swap refinement. **LB** (rigorous lower bound): max of simple Gershgorin 1-(k-1)max|r|, refined Gershgorin 1-max_j(sum of the k-1 largest |r_jl|) and, when p < n, lambda_min(R) (Cauchy interlacing). Negative LB values are uninformative.
- m#: m_sharp from the capped beta-binomial prior as specified (log space, `lchoose`; K = min(p, floor(n/2))). If no m < K satisfies the bound the value is K (as for iclaims, K = p = 10).
- (e) block partition: `core_copy/` is a byte-identical copy of `Scripts/SMC_BVS/core/` (R + C++, SHA-256 of every file in `core_copy/SOURCE_SHA256.txt`, all verified), used so that the Rcpp build cache is written inside `data_diag/` and not in the repo core directory. It compiled without error (Rtools GCC 14.3.0, R 4.6.1, cache key `fbe85b0a26ca...`), so the production C++ was used and no R re-implementation was needed. `ctx <- v3_context(Xs, ys)` with placeholder ys = first PC score of X + N(0,1) noise (seed 1) (riboflavin and diabetes use their real y; blocks do not depend on y), B = min(floor(sqrt n), floor(sqrt p), 16), `v3_blocks(ctx, B)`. Blocks were built on the cleaned design (the production code additionally keeps duplicate columns; none existed here). Leakage = for each variable the max |r| to any variable outside its own block.

## 2. Summary tables (one row per design; also `summary_table.csv`, `summary_tables.md`)

Run time per design (wall seconds, machine heavily loaded by other jobs during the riboflavin runs): riboflavin 466, tecator 111, iclaims 7, fred_qd 79, fred_md 88, diabetes_quad 76, spam 80, digits 105. Greedy restarts: 200 random restarts for every design except riboflavin (60 requested, time cap 360 s, 29 chains completed, swap refinement 15 s per k) and iclaims (only 45 distinct pairs exist: 51 chains in total). A first riboflavin run with 2 completed chains gave identical upper bounds (kept in `run1_riboflavin/`), i.e. the extra restarts did not improve on the chain started from the most correlated pair.

### Master table
| design | n | p | A_hat | top1 / top5 share | lam1/p | #fac | max abs r | med partners tau=.5 (raw -> minus factors) | phi2 exact k=2 / k=3 | phi2 UB k=7 / k=ceil(log n) | phi2 LB at k=ceil(log n) | m#(s0=1) / m#(s0=3) | B | #blocks | leak median / max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| riboflavin |   71 | 4088 | 1.95 | 0.364 / 0.614 | 0.364 | 1 | 0.991 | 982.5 -> 89 | 0.0094 / NA | 0.0026 / 0.00392 (k=5) | -2.92 | 23 / 35 |  8 | 683 | 0.82 / 0.975 |
| tecator |  215 |  100 | 0.857 | 0.986 /    1 | 0.986 | 1 |    1 | 99 -> 75 | 4.01e-06 / 4.06e-09 | 6.83e-11 / 8.78e-11 (k=6) | 1.7e-11 | 18 / 35 | 10 |  13 |    1 /    1 |
| iclaims |  456 |   10 | 0.376 | 0.826 / 0.951 | 0.826 | 1 | 0.899 | 9 -> 0 | 0.101 / 0.0964 | 0.0663 / 0.0663 (k=7) | 0.0644 | 10 / 10 |  3 |   4 | 0.858 / 0.872 |
| fred_qd |  257 |  170 | 0.926 | 0.265 / 0.497 | 0.265 | 1 | 0.996 | 7 -> 3 | 0.00396 / 1.87e-05 | 1.73e-05 / 1.75e-05 (k=6) | 2.29e-06 | 20 / 39 | 13 |  17 | 0.604 / 0.977 |
| fred_md |  775 |   99 | 0.691 | 0.213 / 0.455 | 0.213 | 1 | 0.985 | 4 -> 2 | 0.0148 / 9.07e-05 | 7.01e-05 / 7.01e-05 (k=7) | 4.18e-05 | 21 / 38 |  9 |  13 | 0.456 / 0.877 |
| diabetes_quad |  442 |   64 | 0.683 | 0.168 / 0.456 | 0.168 | 1 | 0.959 | 2 -> 1 | 0.0409 / 0.0118 | 8.08e-05 / 8.08e-05 (k=7) | 3.6e-07 | 18 / 33 |  8 |  11 | 0.558 / 0.835 |
| spam | 4601 |   57 | 0.479 | 0.116 / 0.264 | 0.116 | 1 | 0.996 | 0 -> 0 | 0.00393 / 0.0039 | 0.00387 / 0.00387 (k=9) | 0.00385 | 22 / 36 |  7 |  10 | 0.161 / 0.565 |
| digits | 1797 |   61 | 0.549 | 0.12 / 0.414 | 0.12 | 4 | 0.938 | 2 -> 0 | 0.0624 / 0.0594 | 0.0554 / 0.055 (k=8) | 0.0503 | 21 / 35 |  7 |  11 | 0.488 / 0.664 |

### Table 1 (spectrum)
| design | n | p | A_hat | top1 share | top5 share | lam1/p | #factors (AH ER) | max ER | max abs r |
|---|---|---|---|---|---|---|---|---|---|
| riboflavin |   71 | 4088 | 1.95 | 0.364 | 0.614 | 0.364 | 1 | 3.19 | 0.991 |
| tecator |  215 |  100 | 0.857 | 0.986 |    1 | 0.986 | 1 |  102 |    1 |
| iclaims |  456 |   10 | 0.376 | 0.826 | 0.951 | 0.826 | 1 | 16.8 | 0.899 |
| fred_qd |  257 |  170 | 0.926 | 0.265 | 0.497 | 0.265 | 1 | 3.04 | 0.996 |
| fred_md |  775 |   99 | 0.691 | 0.213 | 0.455 | 0.213 | 1 | 2.41 | 0.985 |
| diabetes_quad |  442 |   64 | 0.683 | 0.168 | 0.456 | 0.168 | 1 | 1.83 | 0.959 |
| spam | 4601 |   57 | 0.479 | 0.116 | 0.264 | 0.116 | 1 | 2.02 | 0.996 |
| digits | 1797 |   61 | 0.549 | 0.12 | 0.414 | 0.12 | 4 | 1.34 | 0.938 |

### Table 2 (pairwise structure)
| design | p_raw | const/dup dropped | med partners tau=.5 before | after | med partners tau=.3 before | after  | frac pairs >.3 | frac pairs >.3 after | max r after | null ref max abs r |
|---|---|---|---|---|---|---|---|---|---|---|
| riboflavin | 4088 | 0/0 | 982.5 | 89 | 2484.5 | 854.0 | 0.525 | 0.228 | 0.99 | 0.67 |
| tecator |  100 | 0/0 |  99.0 | 75 |   99.0 |  86.0 |    1 | 0.839 |    1 | 0.28 |
| iclaims |   10 | 0/0 |   9.0 |  0 |    9.0 |   2.5 |    1 | 0.311 | 0.577 | 0.13 |
| fred_qd |  170 | 0/0 |   7.0 |  3 |   35.0 |  15.0 | 0.23 | 0.107 | 0.99 | 0.27 |
| fred_md |   99 | 0/0 |   4.0 |  2 |   10.0 |   5.0 | 0.146 | 0.06 | 0.977 | 0.15 |
| diabetes_quad |   64 | 0/0 |   2.0 |  1 |    8.0 |   5.0 | 0.15 | 0.0947 | 0.942 | 0.19 |
| spam |   57 | 0/0 |   0.0 |  0 |    0.0 |   0.0 | 0.0414 | 0.01 | 0.981 | 0.057 |
| digits |   64 | 3/0 |   2.0 |  0 |    6.0 |   3.0 | 0.0951 | 0.0486 | 0.777 | 0.091 |

### Table 3 (sparse min eigenvalues)
| design | exact k=2 | exact k=3 | UB k=7 | k=ceil(log n) | UB at that k | LB k=7 | LB at ceil(log n) | lambda_min(R) (p<n) |
|---|---|---|---|---|---|---|---|---|
| riboflavin | 0.0094 | NA | 0.0026 | 5 | 0.00392 | -4.78 | -2.92 | NA |
| tecator | 4.01e-06 | 4.06e-09 | 6.83e-11 | 6 | 8.78e-11 | 1.7e-11 | 1.7e-11 | 1.7e-11 |
| iclaims | 0.101 | 0.0964 | 0.0663 | 7 | 0.0663 | 0.0644 | 0.0644 | 0.0644 |
| fred_qd | 0.00396 | 1.87e-05 | 1.73e-05 | 6 | 1.75e-05 | 2.29e-06 | 2.29e-06 | 2.29e-06 |
| fred_md | 0.0148 | 9.07e-05 | 7.01e-05 | 7 | 7.01e-05 | 4.18e-05 | 4.18e-05 | 4.18e-05 |
| diabetes_quad | 0.0409 | 0.0118 | 8.08e-05 | 7 | 8.08e-05 | 3.6e-07 | 3.6e-07 | 3.6e-07 |
| spam | 0.00393 | 0.0039 | 0.00387 | 9 | 0.00387 | 0.00385 | 0.00385 | 0.00385 |
| digits | 0.0624 | 0.0594 | 0.0554 | 8 | 0.055 | 0.0503 | 0.0503 | 0.0503 |

### Table 4 (m_sharp, blocks)
| design | m#(s0=1) | m#(s0=3) | B | #blocks | leak median | leak q90 | leak max | split frac(|r|>.5) |
|---|---|---|---|---|---|---|---|---|
| riboflavin | 23 | 35 |  8 | 683 | 0.82 | 0.911 | 0.975 | 0.995 |
| tecator | 18 | 35 | 10 |  13 |    1 |    1 |    1 | 0.929 |
| iclaims | 10 | 10 |  3 |   4 | 0.858 | 0.872 | 0.872 | 0.822 |
| fred_qd | 20 | 39 | 13 |  17 | 0.604 | 0.873 | 0.977 | 0.743 |
| fred_md | 21 | 38 |  9 |  13 | 0.456 | 0.796 | 0.877 | 0.584 |
| diabetes_quad | 18 | 33 |  8 |  11 | 0.558 | 0.678 | 0.835 | 0.529 |
| spam | 22 | 36 |  7 |  10 | 0.161 | 0.535 | 0.565 | 0.452 |
| digits | 21 | 35 |  7 |  11 | 0.488 | 0.589 | 0.664 | 0.328 |

Reading guide for the tables: "phi2 exact" values are exact; "phi2 UB" values are upper bounds (witness sets, so the true phi^2 is at most that); "phi2 LB" is a rigorous lower bound (max of the Gershgorin bounds and, for p < n, lambda_min(R)); a negative LB means no information. For p < n designs phi^2(k) >= lambda_min(R) for every k, so UB and LB bracket phi^2(k) (e.g. spam: phi^2(9) is in [0.00385, 0.00387]; digits: phi^2(8) in [0.0503, 0.0550]; diabetes_quad: phi^2(7) in [3.6e-7, 8.1e-5]). Per-k tables with witness sets: `out_<name>_sparse_eig.csv` and `out_<name>.txt`.

## 3. Correlation pattern per design (neutral description; the tag LOCAL / PERVASIVE is only a label for the pattern seen in these numbers)

**riboflavin (n=71, p=4088, A_hat=1.95) - pervasive / dense.** One dominant eigenvalue (lambda_1 = 1488, 36.4% of the trace; top-5 61%, top-10 75%); ER ratios 3.19, 2.15, then about 1.2, so 1 (possibly 2) factors. 52.5% of all pairs have |r| > 0.3; the median variable has 982 partners with |r| > 0.5 (of 4087) and 2484 above 0.3. After projecting out the top PC the median is still 89 (above 0.5) and 854 (above 0.3), 22.8% of pairs above 0.3. At n = 71 the null reference for the largest |r| among 8.4 million pairs is already about 0.67, so a good part of the |r| = 0.3-0.7 mass can be sampling noise plus the common factor; the high tail is sparse (|r| > 0.9: median 0 partners, 90% quantile 4, max 69; max |r| = 0.991). Blocks: B = 8 gives 683 blocks (sizes 2-8); the median variable has |r| = 0.82 with a variable outside its block (90%: 0.91, max 0.975) and 99.5% of the 2.07 million pairs with |r| > 0.5 are split across blocks. phi^2: exact only for k=2 (0.0094); witness sets give phi^2(5) <= 3.9e-3, phi^2(7) <= 2.6e-3, phi^2(16) <= 5.8e-4, phi^2(24) <= 1.5e-4, phi^2(36) <= 4.4e-6; the lower bounds are uninformative (p > n; Gershgorin negative for k >= 3). m#(s0=1) = 23, m#(s0=3) = 35 = K = floor(n/2), i.e. the cap K binds. Plug-in only (NOT verification): a 5-step orthogonal matching pursuit on the real y picks XHLA, YXLG, YOAB, ARGF, YHDZ (in-sample R^2 0.42, 0.63, 0.75, 0.84, 0.88); lambda_min of those supports (|S| = 2..5) is 0.78, 0.58, 0.47, 0.39; they lie in 5 different blocks (59, 53, 261, 106, 116) and each has |r| = 0.95, 0.91, 0.72, 0.85, 0.64 with some variable outside its own block.

**tecator / Fat spectra (n=215, p=100, A_hat=0.86) - pervasive, smooth-curve, near-collinear.** A single eigenvalue carries 98.6% of the trace (lambda_1 = 98.6; next 0.97, 0.28, 0.11, ER ratio 102); every one of the 4950 pairs has |r| > 0.3 and max |r| = 1 - 4e-6 (adjacent wavelengths 870/872 nm). After removing PC1 the residual is still dense (84% of pairs above 0.3, median 75 partners above 0.5, max |r| 0.9998), reflecting the smooth-curve structure carried by PC2-PC4. lambda_min(R) = 1.7e-11, and phi^2(3) = 4.1e-9 exactly (wavelengths 854/856/858), phi^2(7) <= 6.8e-11. Blocks: B = 10, 13 blocks of size 4-10, 12 of which are runs of consecutive wavelengths (one 9-member block spans columns 31-48 and is interleaved with another 9-member block covering 37-45); neighbouring blocks stay correlated at |r| = 0.9999 (leakage median/90%/max about 1.0; 93% of the |r| > 0.5 pairs split).

**iclaims (n=456, p=10, A_hat=0.38) - pervasive single factor, tiny p.** One factor carries 82.6% of the trace (top-5 95%); every pair has |r| > 0.7 (max 0.899). After removing PC1 the residual correlations are modest (max 0.577; median partners above 0.5: 0). The design is well conditioned: lambda_min(R) = 0.0644, exact phi^2 = 0.101 (k=2), 0.096 (k=3), 0.077 (k=4), 0.071 (k=5), 0.066 (k=7), 0.0644 (k=10) by full enumeration. B = 3, 4 blocks of size 2-3, leakage median 0.86. K = p = 10 and no m < K satisfies the bound, so m# = 10 for every s0 and k = 11, 13 are above p (skipped).

**fred_qd (n=257, p=170, A_hat=0.93) - mixed: common factor plus tight clusters of related series.** lambda_1/p = 0.265 (top-5 50%), ER ratios 3.04 then 1.41, 1.23, 1.53, so one factor. The partner counts are very uneven: median 7, 90% quantile 51, max 58 partners above 0.5 (tau = 0.3: 35 / 80 / 86); 23% of pairs above 0.3. After removing PC1: median 3, 90% 15, max 23 (above 0.5), 10.7% of pairs above 0.3; max |r| 0.99 in both cases. Near-exact linear relations exist among small groups: max |r| = 0.996 (PAYEMS/USPRIV), exact phi^2(2) = 0.0040, exact phi^2(3) = 1.87e-5 (CPF3MTB3Mx, TB3SMFFM, COMPAPFF: interest-rate spread series), phi^2(7) <= 1.7e-5, phi^2(40) <= 6.6e-6; lambda_min(R) = 2.3e-6 is the rigorous lower bound at every k. Blocks: B = 13, 17 blocks (sizes 6-13); leakage median 0.60, 90% 0.87, max 0.98; 74% of pairs with |r| > 0.5 are split across blocks. The 2020 values are left in and not treated specially.

**fred_md (extra; n=775, p=99, A_hat=0.69) - mixed, milder than fred_qd.** lambda_1/p = 0.213 (top-5 45.5%); partners above 0.5: median 4, 90% quantile 23, max 28 (tau = 0.3: 10 / 35 / 37), and median 2, 90% 9, max 11 after removing PC1; 14.6% of pairs above 0.3, 6.0% after removing PC1; max |r| = 0.985. exact phi^2(2) = 0.0148 (IPFPNSS/IPFINAL), phi^2(3) = 9.1e-5 (MANEMP, DMANEMP, NDMANEMP), phi^2(7) <= 7.0e-5; lambda_min(R) = 4.2e-5. B = 9, 13 blocks (5-9); leakage median 0.46, 90% 0.80, max 0.88; 58% of strong pairs split.

**diabetes_quad (n=442, p=64, A_hat=0.68) - local / block clusters, no dominant factor, near-collinear small subsets.** lambda_1/p = 0.168 (top-5 46%), ER ratios 1.83 then about 1.1-1.3 (spectrum nearly flat after the first). 15% of pairs above 0.3; median 2 partners above 0.5 (90%: 6, max 9), 1 after factor removal; max |r| = 0.959 (s1:s2 with s2^2). The strong correlations sit among the serum variables s1-s5 and their products/squares; the exact phi^2(2) = 0.041 and phi^2(3) = 0.0118, then phi^2(5) <= 6.1e-4, phi^2(7) <= 8.1e-5, phi^2(10) <= 1.8e-6 and phi^2(19), phi^2(34) <= 3.7e-7, 3.6e-7, against lambda_min(R) = 3.6e-7 (so phi^2(19) is in [3.6e-7, 3.7e-7]); witnesses are sets such as {s1, s2, s3, s5, s5^2, s2:s5, s1:s5, s3:s5, ...}. Blocks: B = 8, 11 blocks (4-8); leakage median 0.56, 90% 0.68, max 0.84; 53% of the 85 pairs above 0.5 are split. Plug-in only (NOT verification): 5-step OMP on the real target picks bmi, s5, bp, age:sex, bmi:bp (R^2 0.34, 0.46, 0.48, 0.50, 0.51); lambda_min of the supports (|S| = 2..5) is 0.554, 0.554, 0.552, 0.548; the five variables are in blocks 1, 1, 1, 2, 7, with max |r| to outside-block variables 0.41, 0.62, 0.26, 0.30, 0.41.

**spam (n=4601, p=57, A_hat=0.48) - local, sparse isolated pairs.** lambda_1/p = 0.116, top-5 26%; the median variable has no partner above 0.3 (90%: 10, max 11 above 0.3), 4.1% of pairs above 0.3 (1.0% after removing PC1). One near-duplicate word-count pair (num857/num415, |r| = 0.996) gives exact phi^2(2) = 0.00393, phi^2(3) = 0.00390 and the bounds phi^2(9) in [0.00385, 0.00387] (lambda_min(R) = 0.00385): the small value is produced by one pair and does not decrease further with k. Blocks: B = 7, 10 blocks (3-7); leakage median 0.16, 90% 0.54, max 0.57 (only 31 pairs have |r| > 0.5, 45% of them split). Raw heavy-tailed frequencies were used (no log transform).

**digits (n=1797, p=61, A_hat=0.55) - local, spatial pixel neighbourhoods, flat spectrum.** lambda_1/p = 0.12 (top-5 41%), ER ratios all below 1.34 (argmax k = 4); median 2 partners above 0.5 (90%: 4, max 6), 9.5% of pairs above 0.3. After removing the top-4 PCs: median 0 partners above 0.5, 4.9% of pairs above 0.3, max |r| 0.777 (0.938 before). Well conditioned: lambda_min(R) = 0.0503, exact phi^2(2) = 0.0624, phi^2(3) = 0.0594, phi^2(8) in [0.0503, 0.0550]. Blocks: B = 7, 11 blocks (3-7); leakage median 0.49, 90% 0.59, max 0.66; 33% of the 61 pairs above 0.5 are split.

## 4. Other numbers worth keeping

- m_sharp for s0 = 1, 2, 3, 5 (`out_<name>.txt`): riboflavin 23, 35, 35, 35 (K = 35); tecator 18, 27, 35, 48; fred_qd 20, 30, 39, 56; diabetes_quad 18, 26, 33, 43; the p ~ 60-100 designs lie in 18-22 (s0 = 1) and 33-39 (s0 = 3). j0 = ceil((2A+1)s0)+1 with A = max(1, A_hat) is 4 / 10 (s0 = 1 / 3) for every design with A_hat <= 1 and 6 / 16 for riboflavin (A = 1.95).
- Where the exact k = 3 value was available, greedy alone was not always exact: on fred_qd the first greedy chain gave 5.3e-5 against the exact 1.87e-5; hence the seeding with exact minimisers. At k >= 4 (no exact value) all UB entries are only upper bounds and could be improved by a stronger search.
- Riboflavin is the only design without an exact k = 3 value; every other design has exact k = 2 and k = 3.

## 5. Caveats

- Time budget: riboflavin took 466 s in the final run (an earlier run, 1328 s on a machine at 100% CPU load, is kept in `run1_riboflavin/`; same upper bounds). Greedy restarts were capped as described in section 2.
- The y used in the production-context call is a placeholder (first PC plus noise) except for riboflavin and diabetes_quad (real y); the blocks do not depend on it.
- The FRED transformation is the BVAR code table re-implemented (the BVAR namespace does not load under R 4.6); no outlier handling. iclaims has only p = 10 columns, so it is not high dimensional in the usual sense.
- Sampling noise: for small n relative to log p (riboflavin) many |r| values in 0.3-0.7 are at the null reference level (see "null ref max abs r" in Table 2); no shrinkage or thresholding was applied.
- Nothing here establishes that any consistency theorem applies to these designs.

## 6. Files (all under `Theory_work/Wave2/W2-APP/data_diag/`)

- `SUMMARY.md` (this file), `summary_table.csv` (one row per design, all numbers), `summary_tables.md` (generated tables), `make_summary.R`.
- Scripts: `diag_lib.R` (all diagnostics), `diag_riboflavin.R`, `diag_tecator.R`, `diag_iclaims.R`, `diag_fred_qd.R`, `diag_fred_md.R`, `diag_diabetes_quad.R`, `diag_spam.R`, `diag_digits.R`, `prep_data.R`, `prep_sklearn.py`, `diag_triples.cpp` (auto-written Rcpp), `test_checks.R` (unit checks, output `out_test_checks.txt`).
- Raw outputs per design: `out_<name>.txt` (full report), `out_<name>.rds` (all numbers), `out_<name>_eigs.csv`, `out_<name>_partners.csv`, `out_<name>_sparse_eig.csv`, `out_<name>_blocks.csv` (variable, block id, leakage), for name in riboflavin, tecator, iclaims, fred_qd, fred_md, diabetes_quad, spam, digits. `out_compile_test.txt` (first build of the core: compiled OK in 19.7 s).
- Data and provenance: `data/*.rds`, `data/*.csv` (design matrices as analysed), `data/PROVENANCE.txt`, `data/sklearn_version.txt`, `downloads/hdi/` (tarball, md5 file, extracted `riboflavin.RData` and `datalist`), `run1_riboflavin/`.
- `core_copy/` (byte-identical copy of `Scripts/SMC_BVS/core/` with `SOURCE_SHA256.txt` and its Rcpp build cache `.cpp_cache`); `.sourcecpp_cache/` (Rcpp cache of `diag_triples.cpp`). These caches are build products and can be deleted.

## Lead erratum (after sweep R07, 2026-11-09)
* riboflavin paragraph: the "null ref max abs r" (≈ 0.67) is an extreme-value context statistic only; it does not
  attribute the bulk of the 0.3–0.7 correlations to sampling noise (R07 #9: under independence the expected numbers of
  pairs with |r| > .3 / > .5 at n = 71 are ≈ 92,125 / 75, vs 2,066,732 observed above .5). That sentence is withdrawn.
* spam: φ²(k) is not constant in k; for k ≥ 2 it lies in [0.003855, 0.003934] (exact φ²(2) = 0.003934, φ²(3) = 0.003901).
