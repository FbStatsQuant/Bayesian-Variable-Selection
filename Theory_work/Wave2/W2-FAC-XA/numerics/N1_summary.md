# N1: numerics only; conditional full-model paths

XA STATEMENT.md was read as "v0 - proposed, NOT LOCKED". No proof work.

## Setup

320 runs: 10 seeds (0-9), n=512,2048; p=16,32,64,128; exact-CS, iid-CS, exact unequal loadings, iid unequal loadings. rho=0.5; unequal lambda_j=linspace(0.4,0.85,p), Sigma=diag(1-lambda^2)+lambda lambda'. Truth S0={0,1}, fixed standardized coefficients (1,1.3), noise variance 1. These grids are diagnostics, not a check of an asymptotic growth condition.

All paths start at [p]. This is a **conditional path experiment, not a start-mode test**. Neither the full-start event nor C2 visibility is tested. IID raw Gaussian rows are explicitly generated, centered and standardized. Response sufficient statistics are then sampled conditional on the realized Gram using FAC-B ExactGram, the exact Gaussian law for Y=X theta+C epsilon followed by response scaling. Exact designs use deterministic Gram Sigma. Each exact/iid pair shares Cholesky-coordinate Gaussian noise and the residual chi-square draw; ordering comparisons depend on this stated coupling. The four designs in each (n,p,seed) cell share noise coordinates, so their outcomes are correlated.

FAC-B fac_core.py, cs_core.py and bvs_core.py were imported read-only; SHA256 before/after is in N1_metadata.json. PYTHONDONTWRITEBYTECODE=1 and python -B disable import caches. The FAC-B score/prior, complete flip/swap scans, strict improvement and lexicographic exact-tie rule are reused. Move cap is ceil(log2(n+p+1))+p, with the final complete scan included.

## Observations

- Pure null-deletion paths: 320/320. Additions: 0; swaps: 0; paths losing a truth: 0.
- S0 scored: 316/320; endpoints equal S0: 316/320; cap exhausted: 0; minimum cap slack: 12.
- Minimum best-null-deletion minus best **all-swap** score: -0.297096945. Undefined scans (no null deletion or no swap) are excluded; terminal scans have no retained nulls in successful paths.
- Smallest gap between the best two deletions: 3.42220119e-07 (all scanned centres, including terminal centres). Null-only version: 3.42220119e-07.
- Exact/iid paths differed in 159/160 paired cases; endpoints differed in 0. See N1_paired_paths.csv for first differing state.
- The four non-S0 endpoints all occur at n=512, p=32, seed=3, one in each design type: each stops at {0,1,4,21} after 28 null deletions. These are correlated outcomes under the shared-noise construction.
- Over scans that accept a move, the minimum deletion-versus-all-swap margin is 0.749873693. The only two negative margins are terminal unequal-loading scans at the above cell: exact -0.297096945 and iid -0.130011822. Their best-neighbor gains are -1.91352630 and -1.60784682, respectively; neither accepts a swap. These observations do not refute an asymptotic statement.

## Sample Gram diagnostics

Rhat=X'X/(n-1). Absolute norm is ||Rhat-Sigma||op. Relative norm is ||Sigma^(-1/2)(Rhat-Sigma)Sigma^(-1/2)||op. Table entries are seed medians (iid only); normalizations inspect competing scales and do not establish a rate.

| n | p | family | abs | abs/sqrt(p/n) | abs/(p/sqrt(n)) | relative | relative/sqrt(p/n) |
|---|---|---|---|---|---|---|---|
| 512 | 16 | CS | 0.3144 | 1.779 | 0.4446 | 0.3329 | 1.883 |
| 512 | 16 | unequal | 0.3159 | 1.787 | 0.4468 | 0.3194 | 1.807 |
| 512 | 32 | CS | 0.7502 | 3.001 | 0.5304 | 0.5139 | 2.055 |
| 512 | 32 | unequal | 0.7519 | 3.008 | 0.5317 | 0.5254 | 2.101 |
| 512 | 64 | CS | 1.491 | 4.216 | 0.527 | 0.7668 | 2.169 |
| 512 | 64 | unequal | 1.488 | 4.209 | 0.5261 | 0.7805 | 2.208 |
| 512 | 128 | CS | 2.913 | 5.827 | 0.515 | 1.215 | 2.431 |
| 512 | 128 | unequal | 2.89 | 5.781 | 0.5109 | 1.208 | 2.416 |
| 2048 | 16 | CS | 0.1464 | 1.656 | 0.414 | 0.1689 | 1.911 |
| 2048 | 16 | unequal | 0.1787 | 2.021 | 0.5054 | 0.1642 | 1.858 |
| 2048 | 32 | CS | 0.347 | 2.776 | 0.4908 | 0.2488 | 1.991 |
| 2048 | 32 | unequal | 0.3874 | 3.099 | 0.5479 | 0.2475 | 1.98 |
| 2048 | 64 | CS | 0.6406 | 3.624 | 0.453 | 0.3688 | 2.086 |
| 2048 | 64 | unequal | 0.6804 | 3.849 | 0.4812 | 0.3699 | 2.092 |
| 2048 | 128 | CS | 1.146 | 4.585 | 0.4053 | 0.5397 | 2.159 |
| 2048 | 128 | unequal | 1.182 | 4.73 | 0.418 | 0.5422 | 2.169 |

Exact-Gram deviations are zero by construction in the sufficient-statistic experiment.

## Scan validation and artifacts

For p=4,8, n=64, seeds 0,1, all four design types: 16 validation cases; 2176 models and 45952 directed neighbor comparisons. Each scan is compared to direct Cholesky scoring of every feasible neighbor, at every possible centre. Maximum absolute score discrepancy 1.56319402e-13; best-move discrepancies 0. Exact-CS closed-form scores and endpoint/move counts were also checked; every exact-CS main-grid endpoint/move count agrees.

- Script: N1_simulations.py; rerun: `$env:PYTHONDONTWRITEBYTECODE="1"; & C:/Users/felip/anaconda3/python.exe -B Theory_work/Wave2/W2-FAC-XA/numerics/N1_simulations.py`.
- N1_raw.jsonl: per-run results and full visited paths; N1_runs.csv: per-run scalar diagnostics.
- N1_scans.csv: every scan, deletion gaps, deletion-versus-swap margins and accepted moves.
- N1_paired_paths.csv: ordering comparisons; N1_grouped.csv: per-cell aggregates.
- N1_validation.csv: exhaustive small-p scan checks; N1_metadata.json: versions, grid, UTC times and source hashes.

These are observed local simulations only; no proof, start-mode, delivery, or asymptotic consistency status is assigned.
