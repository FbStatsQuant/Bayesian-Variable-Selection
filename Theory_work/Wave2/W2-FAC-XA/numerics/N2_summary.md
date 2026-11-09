# N2: Bartlett-Wishart full-start conditional diagnostics

Read XA PLAN.md and locked STATEMENT v1. No proof or asymptotic status is assigned.

120 runs: n=1e6,1e8; p=32,100,200; seeds 0-4; exact and random Grams for CS rho=.5 and unequal positive loadings linspace(.4,.85,p). Truth {0,1}, standardized theta=(1,1.3), noise variance 1. Every path starts from [p]; the actual start-mode event and visibility are not tested. The grid is not asserted to satisfy any locked growth or delivery hypothesis.

## Construction and validation

Lower Bartlett A has independent strict-lower N(0,1) entries and diagonal sqrt(chi2(n-1-i)), with i zero based. For Sigma=L L', W=L A A' L' has exactly the centered raw Gaussian scatter law. Normalize R_ij=W_ij/sqrt(W_ii W_jj). No n-row matrix is allocated for the main grid.

FAC-B ExactGram supplies the conditional response law: g=chol(R)z, z~N(0,I); ||C epsilon||^2=z'z+chi2(n-1-p). For Y=X theta+C epsilon, ||Y||^2=(n-1)theta'R theta+2 sqrt(n-1)theta'g+z'z+chi2(n-1-p); s^2=||Y||^2/(n-1), X'y=((n-1)R theta+sqrt(n-1)g)/s, y'y=n-1. Each run replays and verifies these identities and saves every normalization component. Exact/random pairs share z and the residual draw; cross-family cases share those coordinates too. This is a specified coupling of sufficient statistics.

Small-n validation uses n=32,p=4,6000 replicates per family and generator. Checks E[W]=(n-1)Sigma and Var(W_ij)=(n-1)(Sigma_ij^2+Sigma_ii Sigma_jj) for Bartlett and explicitly centered raw rows, then compares mean normalized-Gram entries and response sufficient statistics/scale with the N1 raw-row law. Maximum mean z statistic: 2.2699. These moment diagnostics do not prove equality in distribution; the Bartlett formula supplies the convention.

Exhaustive general-scorer validation at n=64,p=4,8 for both families and Gram kinds: 8 cases, 1088 model scores, 22976 neighbor comparisons. Maximum score error 1.42109e-13; no best-move mismatches. General FAC-B scan and production strict-improvement/exact-tie lexicographic rule are reused, with independent direct F_many Cholesky checks at full, middle and terminal centres. Main-grid maximum direct score error: 3.52859e-05.

## Observations

- Safe null-deletion-only paths: 120/120; truth loss: 0. Additions 0, swaps 0.
- S0 scored by path scans: 120/120; endpoints S0: 120/120. The separately audited S0 score does not count toward path discovery.
- Cap exhausted: 0; minimum slack 22. Cap=ceil(log2(n+p+1))+p; final complete scan included.
- Minimum best-null-deletion minus best-all-swap score: 6.21246238. No-swap/no-null scans excluded; additions and truth deletions also scanned.
- Exact top-neighbor tied scans: 1; improving tied scans: 1. Minimum top-two-neighbor score gap: 0. Raw gaps, score ULPs and direct-check errors are saved to expose floating-point sensitivity.
- Exact/random paths differ in 45/60 pairs; endpoints differ in 0.

Absolute norm is ||R-Sigma||op; relative norm is ||Sigma^(-1/2)(R-Sigma)Sigma^(-1/2)||op. Both, and competing scale normalizations, are in N2_runs.csv/N2_grouped.csv. Exact deviations are zero. No norm rate is inferred.

## Artifacts and limitations

N2_raw.jsonl contains each run and full path; N2_scans.jsonl/CSV contain every scan. N2_sufficient_stats.npz retains realized R, random scatter W, g and Xty for rescoring. N2_runs.csv, N2_grouped.csv and N2_paired_paths.csv provide summaries. N2_law_validation.csv and N2_score_validation.csv retain checks. N2_metadata.json records versions, times, grids and before/after source hashes.

Run: C:/Users/felip/anaconda3/python.exe -B Theory_work/Wave2/W2-FAC-XA/numerics/N2_simulations.py. Only N2-prefixed files are written; bytecode disabled. FAC-B sources and N1 are read-only. Local compute only; no start-mode, posterior/delivery, asymptotic proof or targeted lead-lemma norm experiment.
