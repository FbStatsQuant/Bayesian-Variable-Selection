# NUMERICS_LOC_VN — W2-APP numerics (local designs L1–L4, visible-null designs V1–V3)

> **SUPERSESSION NOTICE (lead, after council r2, C2 Sol issue 2).** The interpretation sections of this helper file are
> superseded by `numerics/LEAD_READING.md` (v2) and `numerics/vn_bound_recheck_out.txt`: (i) the 16 runs re-done with
> `n3b_fastls.py` used a SCREENED search — swaps pre-screened by Cholesky updates, only those within 1e-5 of the
> approximate maximum rescored exactly; three trajectories were validated identical to the port, the remaining decisions
> are unverified, and their `certified` flag means "no improvement among retained/rescored candidates", NOT a
> complete-scan certificate (24 of the 40 VN-example endpoints have complete-scan certificates; the 12 controls too);
> (ii) the "lemma_bound" column (|vis| − 16s₀ compared with visible nulls in the mode) is NOT Lemma VN's bound — the stated
> bound min(K − s₀, |𝒩| − 15s₀) compared with the total extras is in vn_bound_recheck_out.txt; (iii) V3b (Σ_kθ*_k = 0) is a
> no-claim control for VN, not an application. Historical CSV values are unchanged; read their old columns with this
> notice.

Falsification / observation numerics only — nothing here is a proof. Write location: `Theory_work/Wave2/W2-APP/numerics/` only; no git.
Python `C:/Users/felip/anaconda3/python.exe` (numpy/scipy). Method objects imported (not edited) from `Theory_work/Wave1C/C-GROW/numerics/bvs_core.py`
(`standardize_X, Problem, partition, block_tables/start_mode, local_search/neighbours, ell_cap, block_size, iid_design_raw, make_y_std`).

## Files
| file | role |
|---|---|
| `n0_common.py` | design builders (Σ for L1–L4, V1–V3), truth placement, data generator, `start_and_ls` (partition → start mode → LS0), `ls_timed` (copy of `bc.local_search` + wall-clock guard; path-identical, tested) |
| `n1_approx_innov.py` → `n1_results.csv`, `n1_out.txt` | part n1 (approximate innovations) |
| `n2_startmode_local.py` → `n2_results.csv`, `n2_out.txt` | part n2 (start-mode sandwich, LS0 on local designs) |
| `n3_visible_null.py` → `n3_results.csv`, `n3_out.txt` | part n3 (visible-null obstruction) |
| `n3b_fastls.py` → `n3b_results.csv`, `n3b_out.txt`, `n3b_validate_out.txt` | n3 re-run of the 16 data sets whose LS0 hit the 600 s guard, with a faster *exact-decision* LS0 (see deviations) |
| `n0_aggregate.py` → `agg_tables.md`, `n3_merged.csv` | aggregation (full tables incl. per-data-set n3 detail and the list of n2 data sets with far extras) |

Seeds: every rng is `default_rng(SeedSequence([20261109, tag, design_id, n, p, seed]))` (tags: 1 = n1 design+ε, 2 = n1 lattice sets (depend on design, p, seed only → same T-sets for all n), 3 = n2, 4 = n3); seeds 1–5 (n1), 1–6 (n2), 1–4 (n3).
Designs: raw rows iid N(0,Σ), unit-diagonal Σ; y = Xθ + ε on standardised X via `bc.make_y_std` (σ=1). Truths (L1–L4): indices round(p·(0.15, 0.5, 0.85)) = (30,100,170) at p=200, (60,200,340) at p=400, θ=(1,−0.8,1.2); (for L3 these fall in three different blocks of 20). V1: truth 0, θ=1, m=round(n^{1/3}) leaves (9, 15, 23 at n=800, 3200, 12800), corr 1/(2√m). V2: ρ=0.5 blocks of g=round(√n) (28, 57, 113), one truth at the middle of each of three full blocks (spread), θ=(1,−0.8,1.2). V3a: ρ=0.3, θ=(1,−0.8,1.2) (sum 1.4); V3b: θ=(1,−0.5,−0.5) (sum 0); truths at (30,100,170).
Σ checks: min eigenvalues L1 0.048 (MA(2) polynomial has a root inside the unit circle but the spectral density stays positive; Σ is PD), L2 0.218, L3 0.4, L4 0.333, V1 0.5, V2 0.5, V3 0.7.

## Runtime (8 cores, 7 workers)
n1 109 s · n2 47 s · n3 1848 s (incl. 16 data sets that stopped at the 600 s guard) · n3b re-run 525 s · validation of the faster LS0 249 s. Total ≈ 46 min.

## Deviations from the spec (all deliberate; none changes a reported number silently)
1. **n1 candidate set.** "within distance 10 of Q" is implemented as index distance ≤ 16 from S0 (Q has radius 6); 50 random far l are drawn from index distance > 16. Lattice T-sets: 300 per (design, seed), identical across n.
2. **n1 extra outputs.** Besides |Z−Z′| for one fixed ε per (design,n,seed) (this is a single Gaussian draw, so its max over ~38k pairs mostly measures the tail of N(0, sd²)), I report its design-conditional standard deviation sd = ‖u − g/‖g‖‖ = √(2 − 2‖r_{T,l}‖/‖g‖) (exact Gram identity; Z−Z′ | X ~ N(0, sd²)). All sample quantities are computed from the Gram matrix of the centred raw design M = CW (equivalent to the standardised-column construction since u and g are scale-free).
3. **n3, V2 at n=12800.** Block size 113 leaves only one full block at p=200, so "three truths in three different blocks" is impossible at p=200. Main rows: **p=400** (3 full blocks). Additional rows at p=200 with **s0=2** (θ=(1,−0.8)), truths in the two different blocks.
4. **n3 LS0 guard / faster scorer.** `ls_timed` stopped after 600 s for 16 data sets (V2 n=12800 all 8, V3a n=3200 ×4, V3a n=12800 ×4; start modes of 125–221 indices). These were **re-run in `n3b_fastls.py`** with `ls_fast`: swap scores pre-screened by bordered-Cholesky updates, then every add/delete and every swap within 1e-5 of the fast maximum is re-scored exactly with `Problem.F_many` and the production selection rule (max exact F, ties → lexicographically smallest) is applied. Validation (`n3b_validate_out.txt`): on 3 data sets the full path equals `bc.local_search` (identical path, moves, certified flag), max |fast − exact| swap score 7e−12, 12–30× faster. The merged table uses n3b rows for these 16 data sets, n3 rows for the other 36. This is a different implementation of the same search rule, validated on 3 cases, not on all 16.
5. n2 / n3 LS0 cap = `ell_cap(n,p)+|S̃0|`. `ell` (the cap) was never reached in any run.

# Part n1 — approximate innovations (`n1_approx_innov.py`, `n1_results.csv`)

n1 table (max over 5 seeds of the per-seed max; 'med' = mean over seeds of the per-seed median)

columns: max_dZ = max |Z-Z'| (one fixed eps per seed); med_dZ = median |Z-Z'|; max_sd / med_sd = sqrt(Var(Z-Z'|design)) = ||u-ghat||; max_popvar / med_popvar = Var(E[W_l|W_T]-E[W_l|W_T']); max_sd_far = max_sd over the 50 far l only; last = median of sd / sqrt(|T minus T'|/n).

### L1

| n | r | max_dZ | med_dZ | max_sd | med_sd | max_popvar | med_popvar | max_sd_far | sd_over_sqrt_nout_over_n_med |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 2.44 | 0.154 | 0.833 | 0.211 | 0.533 | 0 | 0.386 | 1.03 |
| 500 | 1 | 2.15 | 0.151 | 0.785 | 0.209 | 0.411 | 0 | 0.386 | 1.02 |
| 500 | 2 | 1.61 | 0.142 | 0.606 | 0.205 | 0.185 | 0 | 0.386 | 1.01 |
| 500 | 3 | 1.13 | 0.141 | 0.511 | 0.204 | 0.11 | 0 | 0.386 | 1.01 |
| 500 | 5 | 0.964 | 0.139 | 0.428 | 0.202 | 0.0257 | 0 | 0.386 | 1.01 |
| 500 | 8 | 0.964 | 0.139 | 0.386 | 0.202 | 0.00574 | 0 | 0.386 | 1.03 |
| 2000 | 0 | 2.48 | 0.082 | 0.824 | 0.105 | 0.533 | 0 | 0.176 | 1.03 |
| 2000 | 1 | 2.69 | 0.0793 | 0.777 | 0.104 | 0.411 | 0 | 0.176 | 1.02 |
| 2000 | 2 | 1.5 | 0.0737 | 0.605 | 0.103 | 0.185 | 0 | 0.176 | 1.01 |
| 2000 | 3 | 1.33 | 0.0723 | 0.503 | 0.102 | 0.11 | 0 | 0.176 | 1.01 |
| 2000 | 5 | 0.873 | 0.0706 | 0.275 | 0.101 | 0.0257 | 0 | 0.176 | 1.01 |
| 2000 | 8 | 0.673 | 0.0703 | 0.21 | 0.1 | 0.00574 | 0 | 0.176 | 1.03 |
| 8000 | 0 | 2.74 | 0.0409 | 0.806 | 0.0528 | 0.533 | 0 | 0.0905 | 1.03 |
| 8000 | 1 | 2.37 | 0.0394 | 0.746 | 0.0525 | 0.411 | 0 | 0.0905 | 1.03 |
| 8000 | 2 | 1.31 | 0.0367 | 0.566 | 0.052 | 0.185 | 0 | 0.0905 | 1.02 |
| 8000 | 3 | 0.855 | 0.0354 | 0.461 | 0.0514 | 0.11 | 0 | 0.0905 | 1.02 |
| 8000 | 5 | 0.571 | 0.0338 | 0.234 | 0.0507 | 0.0257 | 0 | 0.0905 | 1.01 |
| 8000 | 8 | 0.31 | 0.0335 | 0.121 | 0.0504 | 0.00574 | 0 | 0.0905 | 1.03 |

### L2

| n | r | max_dZ | med_dZ | max_sd | med_sd | max_popvar | med_popvar | max_sd_far | sd_over_sqrt_nout_over_n_med |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 2.46 | 0.24 | 1 | 0.302 | 0.667 | 0.0444 | 0.396 | 1.47 |
| 500 | 1 | 2.2 | 0.221 | 0.955 | 0.289 | 0.596 | 0.0327 | 0.396 | 1.41 |
| 500 | 2 | 1.61 | 0.197 | 0.818 | 0.253 | 0.448 | 0.0112 | 0.396 | 1.24 |
| 500 | 3 | 1.52 | 0.184 | 0.644 | 0.24 | 0.228 | 0.0065 | 0.396 | 1.19 |
| 500 | 5 | 1.25 | 0.168 | 0.532 | 0.226 | 0.119 | 0.00181 | 0.396 | 1.13 |
| 500 | 8 | 1.18 | 0.154 | 0.428 | 0.215 | 0.0457 | 0.000384 | 0.396 | 1.1 |
| 2000 | 0 | 3 | 0.169 | 0.953 | 0.232 | 0.667 | 0.0444 | 0.241 | 2.27 |
| 2000 | 1 | 2.3 | 0.153 | 0.888 | 0.215 | 0.596 | 0.0327 | 0.241 | 2.11 |
| 2000 | 2 | 1.79 | 0.127 | 0.757 | 0.166 | 0.448 | 0.0112 | 0.241 | 1.64 |
| 2000 | 3 | 1.61 | 0.114 | 0.553 | 0.141 | 0.228 | 0.0065 | 0.241 | 1.4 |
| 2000 | 5 | 1.31 | 0.0971 | 0.413 | 0.121 | 0.119 | 0.00181 | 0.241 | 1.22 |
| 2000 | 8 | 1.01 | 0.0834 | 0.295 | 0.111 | 0.0457 | 0.000384 | 0.241 | 1.14 |
| 8000 | 0 | 2.58 | 0.115 | 0.936 | 0.215 | 0.667 | 0.0444 | 0.192 | 4.17 |
| 8000 | 1 | 2.26 | 0.101 | 0.871 | 0.192 | 0.596 | 0.0327 | 0.192 | 3.79 |
| 8000 | 2 | 1.77 | 0.0785 | 0.737 | 0.139 | 0.448 | 0.0112 | 0.192 | 2.75 |
| 8000 | 3 | 1.47 | 0.0667 | 0.515 | 0.102 | 0.228 | 0.0065 | 0.192 | 2.04 |
| 8000 | 5 | 1.16 | 0.0523 | 0.381 | 0.0697 | 0.119 | 0.00181 | 0.192 | 1.39 |
| 8000 | 8 | 0.77 | 0.042 | 0.264 | 0.0583 | 0.0457 | 0.000384 | 0.192 | 1.21 |

### L3

| n | r | max_dZ | med_dZ | max_sd | med_sd | max_popvar | med_popvar | max_sd_far | sd_over_sqrt_nout_over_n_med |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 3.26 | 0.231 | 0.922 | 0.246 | 0.571 | 0 | 0.889 | 1.18 |
| 500 | 1 | 3.26 | 0.218 | 0.909 | 0.246 | 0.571 | 0 | 0.889 | 1.18 |
| 500 | 2 | 3.26 | 0.207 | 0.904 | 0.244 | 0.571 | 0 | 0.889 | 1.18 |
| 500 | 3 | 3.26 | 0.196 | 0.902 | 0.24 | 0.571 | 0 | 0.889 | 1.17 |
| 500 | 5 | 3.26 | 0.182 | 0.902 | 0.233 | 0.562 | 0 | 0.889 | 1.14 |
| 500 | 8 | 3.1 | 0.163 | 0.902 | 0.222 | 0.548 | 0 | 0.889 | 1.12 |
| 2000 | 0 | 2.89 | 0.115 | 0.874 | 0.118 | 0.571 | 0 | 0.839 | 1.14 |
| 2000 | 1 | 2.85 | 0.11 | 0.872 | 0.117 | 0.571 | 0 | 0.839 | 1.13 |
| 2000 | 2 | 2.8 | 0.106 | 0.872 | 0.117 | 0.571 | 0 | 0.839 | 1.13 |
| 2000 | 3 | 2.76 | 0.102 | 0.866 | 0.115 | 0.571 | 0 | 0.839 | 1.12 |
| 2000 | 5 | 2.76 | 0.0939 | 0.859 | 0.112 | 0.562 | 0 | 0.839 | 1.1 |
| 2000 | 8 | 2.01 | 0.0821 | 0.84 | 0.107 | 0.548 | 0 | 0.839 | 1.08 |
| 8000 | 0 | 3.11 | 0.0716 | 0.85 | 0.0603 | 0.571 | 0 | 0.82 | 1.16 |
| 8000 | 1 | 3.08 | 0.0696 | 0.85 | 0.0602 | 0.571 | 0 | 0.82 | 1.16 |
| 8000 | 2 | 2.99 | 0.0671 | 0.85 | 0.0598 | 0.571 | 0 | 0.82 | 1.15 |
| 8000 | 3 | 2.87 | 0.0644 | 0.842 | 0.059 | 0.571 | 0 | 0.82 | 1.14 |
| 8000 | 5 | 2.64 | 0.0579 | 0.834 | 0.0574 | 0.562 | 0 | 0.82 | 1.12 |
| 8000 | 8 | 2.07 | 0.0498 | 0.827 | 0.0549 | 0.548 | 0 | 0.82 | 1.11 |

### L4

| n | r | max_dZ | med_dZ | max_sd | med_sd | max_popvar | med_popvar | max_sd_far | sd_over_sqrt_nout_over_n_med |
|---|---|---|---|---|---|---|---|---|---|
| 500 | 0 | 2.33 | 0.155 | 0.803 | 0.216 | 0.4 | 3.81e-06 | 0.374 | 1.05 |
| 500 | 1 | 1.15 | 0.141 | 0.52 | 0.21 | 0.118 | 2.38e-07 | 0.374 | 1.03 |
| 500 | 2 | 0.968 | 0.136 | 0.384 | 0.206 | 0.0308 | 3.73e-09 | 0.374 | 1.02 |
| 500 | 3 | 0.968 | 0.134 | 0.384 | 0.204 | 0.00391 | 9.31e-11 | 0.374 | 1.01 |
| 500 | 5 | 0.968 | 0.133 | 0.384 | 0.204 | 0.000244 | 2.27e-13 | 0.374 | 1.02 |
| 500 | 8 | 0.968 | 0.133 | 0.384 | 0.204 | 3.81e-06 | 0 | 0.374 | 1.04 |
| 2000 | 0 | 2.14 | 0.0795 | 0.72 | 0.111 | 0.4 | 3.81e-06 | 0.183 | 1.08 |
| 2000 | 1 | 0.956 | 0.0703 | 0.421 | 0.108 | 0.118 | 2.38e-07 | 0.183 | 1.05 |
| 2000 | 2 | 0.518 | 0.0658 | 0.256 | 0.105 | 0.0308 | 3.73e-09 | 0.183 | 1.03 |
| 2000 | 3 | 0.504 | 0.0638 | 0.19 | 0.103 | 0.00391 | 9.31e-11 | 0.183 | 1.02 |
| 2000 | 5 | 0.504 | 0.0629 | 0.189 | 0.102 | 0.000244 | 2.27e-13 | 0.183 | 1.02 |
| 2000 | 8 | 0.504 | 0.0629 | 0.189 | 0.102 | 3.81e-06 | 0 | 0.183 | 1.04 |
| 8000 | 0 | 1.96 | 0.0453 | 0.695 | 0.0557 | 0.4 | 3.81e-06 | 0.0942 | 1.08 |
| 8000 | 1 | 0.903 | 0.0396 | 0.38 | 0.0538 | 0.118 | 2.38e-07 | 0.0942 | 1.05 |
| 8000 | 2 | 0.454 | 0.0363 | 0.207 | 0.0524 | 0.0308 | 3.73e-09 | 0.0942 | 1.03 |
| 8000 | 3 | 0.293 | 0.0349 | 0.122 | 0.0515 | 0.00391 | 9.31e-11 | 0.0942 | 1.02 |
| 8000 | 5 | 0.26 | 0.034 | 0.0959 | 0.0505 | 0.000244 | 2.27e-13 | 0.0942 | 1.01 |
| 8000 | 8 | 0.26 | 0.0339 | 0.0942 | 0.0504 | 3.81e-06 | 0 | 0.0942 | 1.03 |

### L4 (AR(1)) scaling of max_sd (sd of Z-Z'), r>=1: max_sd*sqrt(n) and max_sd*sqrt(n)/log n

| n | r | max_sd | max_sd*sqrt(n) | max_sd*sqrt(n)/log n | max_dZ | max_dZ*sqrt(n)/log n |
|---|---|---|---|---|---|---|
| 500 | 1 | 0.52 | 11.6 | 1.87 | 1.15 | 4.13 |
| 500 | 2 | 0.384 | 8.58 | 1.38 | 0.968 | 3.48 |
| 500 | 3 | 0.384 | 8.58 | 1.38 | 0.968 | 3.48 |
| 500 | 5 | 0.384 | 8.58 | 1.38 | 0.968 | 3.48 |
| 500 | 8 | 0.384 | 8.58 | 1.38 | 0.968 | 3.48 |
| 2000 | 1 | 0.421 | 18.8 | 2.48 | 0.956 | 5.63 |
| 2000 | 2 | 0.256 | 11.4 | 1.51 | 0.518 | 3.05 |
| 2000 | 3 | 0.19 | 8.52 | 1.12 | 0.504 | 2.96 |
| 2000 | 5 | 0.189 | 8.46 | 1.11 | 0.504 | 2.96 |
| 2000 | 8 | 0.189 | 8.46 | 1.11 | 0.504 | 2.96 |
| 8000 | 1 | 0.38 | 34 | 3.78 | 0.903 | 8.99 |
| 8000 | 2 | 0.207 | 18.5 | 2.06 | 0.454 | 4.52 |
| 8000 | 3 | 0.122 | 10.9 | 1.21 | 0.293 | 2.92 |
| 8000 | 5 | 0.0959 | 8.58 | 0.954 | 0.26 | 2.58 |
| 8000 | 8 | 0.0942 | 8.42 | 0.937 | 0.26 | 2.58 |

mean over pairs of |T minus T'| at r=8: L1 n=500: 19.2, L1 n=2000: 19.2, L1 n=8000: 19.2, L2 n=500: 19.4, L2 n=2000: 19.4, L2 n=8000: 19.4, L3 n=500: 19.2, L3 n=2000: 19.2, L3 n=8000: 19.2, L4 n=500: 19.3, L4 n=2000: 19.3, L4 n=8000: 19.3


# Part n2 — start-mode sandwich and LS0 on local designs (`n2_startmode_local.py`, `n2_results.csv`)

n2 table (6 seeds per cell; counts are out of 6)

| design | n | p | runs | S0_in_start | start_size_mean | extra_mean | extra_max | maxdist_extra | LS_S0_scored | LS_final_eq_S0 | LS_certified | LS_capped | moves_mean | moves_max | B | nblocks | blk_min | blk_max | blk_mean | truths_in_distinct_blocks | start_truncated | max_secs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 800 | 200 | 6 | 6 | 5.83 | 2.83 | 5 | 2 | 6 | 6 | 6 | 0 | 2.83 | 5 | 14 | 20.8 | 5 | 14 | 9.65 | 6 | 0 | 1.3 |
| L1 | 800 | 400 | 6 | 6 | 5 | 2 | 4 | 2 | 6 | 6 | 6 | 0 | 2 | 4 | 16 | 34.2 | 6 | 16 | 11.7 | 5 | 0 | 6.4 |
| L1 | 3200 | 200 | 6 | 6 | 10.2 | 7.17 | 10 | 4 | 6 | 6 | 6 | 0 | 7.17 | 10 | 14 | 20.8 | 5 | 14 | 9.6 | 5 | 0 | 1.1 |
| L1 | 3200 | 400 | 6 | 6 | 11.2 | 8.17 | 10 | 4 | 6 | 6 | 6 | 0 | 8.17 | 10 | 16 | 34.5 | 7 | 16 | 11.6 | 5 | 0 | 9.4 |
| L2 | 800 | 200 | 6 | 6 | 7.33 | 4.33 | 6 | 9 | 6 | 5 | 6 | 0 | 4.33 | 6 | 14 | 19.3 | 5 | 14 | 10.4 | 6 | 0 | 1.5 |
| L2 | 800 | 400 | 6 | 6 | 6.83 | 3.83 | 5 | 37 | 6 | 6 | 6 | 0 | 3.83 | 5 | 16 | 34.5 | 5 | 16 | 11.6 | 6 | 0 | 6.4 |
| L2 | 3200 | 200 | 6 | 6 | 12 | 9 | 10 | 14 | 6 | 6 | 6 | 0 | 9 | 10 | 14 | 20.5 | 5 | 14 | 9.78 | 6 | 0 | 1.2 |
| L2 | 3200 | 400 | 6 | 6 | 9.33 | 6.33 | 8 | 12 | 6 | 6 | 6 | 0 | 6.33 | 8 | 16 | 35.2 | 6 | 16 | 11.4 | 6 | 0 | 9.9 |
| L3 | 800 | 200 | 6 | 6 | 8.5 | 5.5 | 6 | 18 | 6 | 6 | 6 | 0 | 5.67 | 7 | 14 | 19.5 | 5 | 14 | 10.3 | 6 | 0 | 1.6 |
| L3 | 800 | 400 | 6 | 6 | 8.5 | 5.5 | 6 | 19 | 6 | 6 | 6 | 0 | 5.5 | 6 | 16 | 34.5 | 3 | 16 | 11.6 | 6 | 0 | 8.5 |
| L3 | 3200 | 200 | 6 | 6 | 14.2 | 11.2 | 12 | 19 | 6 | 6 | 6 | 0 | 11.2 | 12 | 14 | 18.8 | 5 | 14 | 10.6 | 6 | 0 | 1.4 |
| L3 | 3200 | 400 | 6 | 6 | 14.7 | 11.7 | 13 | 19 | 6 | 6 | 6 | 0 | 11.7 | 13 | 16 | 35.5 | 4 | 16 | 11.3 | 6 | 0 | 9 |
| L4 | 800 | 200 | 6 | 6 | 4.83 | 1.83 | 3 | 2 | 6 | 5 | 6 | 0 | 1.83 | 3 | 14 | 20.2 | 4 | 14 | 9.94 | 6 | 0 | 1.6 |
| L4 | 800 | 400 | 6 | 6 | 4.67 | 1.67 | 3 | 14 | 6 | 6 | 6 | 0 | 1.67 | 3 | 16 | 35.3 | 6 | 16 | 11.3 | 6 | 0 | 8.5 |
| L4 | 3200 | 200 | 6 | 6 | 4.67 | 1.67 | 3 | 3 | 6 | 6 | 6 | 0 | 1.67 | 3 | 14 | 20.3 | 5 | 14 | 9.86 | 6 | 0 | 0.9 |
| L4 | 3200 | 400 | 6 | 6 | 5 | 2 | 3 | 3 | 6 | 6 | 6 | 0 | 2 | 3 | 16 | 35.2 | 6 | 16 | 11.4 | 6 | 0 | 6.5 |

### n2: data sets where the LS0 endpoint != S0

| design | n | p | seed | S0 | mode | n_extra | ls_final_size | ls_final_symdiff | ls_certified | ls_S0_scored |
|---|---|---|---|---|---|---|---|---|---|---|
| L2 | 800 | 200 | 6 | [30, 100, 170] | [22, 30, 35, 100, 164, 170, 177] | 4 | 4 | 1 | True | True |
| L4 | 800 | 200 | 2 | [30, 100, 170] | [28, 30, 100, 170] | 1 | 4 | 1 | True | True |

### n2: data sets with a start-mode extra at distance > 8 from S0: L1 0/24, L2 14/24, L3 23/24, L4 1/24 (listing in `agg_tables.md`)

### n2: block-size histograms (first seed of each cell; size:count)

| design | n | p | B | blk_hist |
|---|---|---|---|---|
| L1 | 800 | 200 | 14 | 7:3 8:2 9:2 10:5 11:3 12:4 14:1 |
| L1 | 800 | 400 | 16 | 6:1 8:7 9:3 10:2 11:4 12:6 13:3 14:3 15:2 16:4 |
| L1 | 3200 | 200 | 14 | 6:1 7:2 8:4 9:4 10:3 11:4 12:1 13:2 |
| L1 | 3200 | 400 | 16 | 8:5 9:3 10:6 11:4 12:3 13:2 14:1 15:7 16:3 |
| L2 | 800 | 200 | 14 | 6:1 8:3 9:2 10:4 11:2 12:4 14:3 |
| L2 | 800 | 400 | 16 | 7:3 8:3 9:5 10:3 11:3 12:5 13:4 14:3 15:3 16:3 |
| L2 | 3200 | 200 | 14 | 7:6 8:3 9:3 10:4 11:5 12:1 |
| L2 | 3200 | 400 | 16 | 7:2 8:2 9:1 10:8 11:3 12:1 13:4 14:1 15:6 16:5 |
| L3 | 800 | 200 | 14 | 6:1 7:1 9:7 10:2 11:7 13:1 14:1 |
| L3 | 800 | 400 | 16 | 7:5 8:3 9:2 10:3 11:3 12:4 13:6 14:5 16:4 |
| L3 | 3200 | 200 | 14 | 5:2 7:2 9:1 10:4 11:2 12:2 13:3 14:3 |
| L3 | 3200 | 400 | 16 | 6:1 7:2 8:7 9:2 10:2 11:3 12:8 13:4 14:2 15:3 16:2 |
| L4 | 800 | 200 | 14 | 6:1 7:1 8:2 9:3 10:4 11:1 12:1 13:3 14:3 |
| L4 | 800 | 400 | 16 | 7:1 8:6 9:7 10:6 11:3 12:1 13:1 14:4 15:4 16:3 |
| L4 | 3200 | 200 | 14 | 5:1 6:1 7:4 8:3 9:3 10:5 11:2 12:2 14:1 |
| L4 | 3200 | 400 | 16 | 7:1 8:8 9:8 10:2 11:2 12:5 13:4 14:2 15:5 |


# Part n3 — visible-null obstruction (`n3_visible_null.py`, `n3b_fastls.py`; `n3_results.csv`, `n3b_results.csv`, `n3_merged.csv`)

n3 table (4 seeds per cell; counts out of 4). visible = V1 leaves / V2 nulls in truth blocks / V3 all nulls; lemma_bound = min(K-s0, |visible|-16 s0)

| design | n | p | runs | s0 | K | B | start_size_mean | start_size_min | start_size_max | extra_mean | S0_in_start | n_visible | vis_in_start_mean | vis_in_start_min | lemma_bound | bound_met | LS_S0_scored | LS_final_eq_S0 | LS_certified | LS_capped | LS_unfinished | moves_mean | moves_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V1 | 800 | 200 | 4 | 1 | 200 | 14 | 2.25 | 1 | 5 | 1.25 | 4 | 9 | 1.25 | 0 | -7 | 4 | 4 | 4 | 4 | 0 | 0 | 1.25 | 4 |
| V1 | 3200 | 200 | 4 | 1 | 200 | 14 | 12.2 | 10 | 15 | 11.2 | 4 | 15 | 11.2 | 9 | -1 | 4 | 4 | 4 | 4 | 0 | 0 | 11.5 | 14 |
| V1 | 12800 | 200 | 4 | 1 | 200 | 14 | 22 | 21 | 23 | 21 | 4 | 23 | 21 | 20 | 7 | 4 | 4 | 4 | 4 | 0 | 0 | 21 | 22 |
| V2 | 800 | 200 | 4 | 3 | 200 | 14 | 14.5 | 13 | 16 | 11.5 | 4 | 81 | 11.5 | 10 | 33 | 0 | 4 | 4 | 4 | 0 | 0 | 11.5 | 13 |
| V2 | 3200 | 200 | 4 | 3 | 200 | 14 | 61 | 56 | 67 | 58 | 4 | 168 | 58 | 53 | 120 | 0 | 4 | 4 | 4 | 0 | 0 | 58.5 | 64 |
| V2 | 12800 | 200 | 4 | 2 | 200 | 14 | 156 | 152 | 160 | 154 | 4 | 198 | 154 | 150 | 166 | 0 | 4 | 4 | 4 | 0 | 0 | 154 | 158 |
| V2 | 12800 | 400 | 4 | 3 | 400 | 16 | 216 | 210 | 221 | 214 | 4 | 336 | 214 | 207 | 288 | 0 | 4 | 4 | 4 | 0 | 0 | 214 | 218 |
| V3a | 800 | 200 | 4 | 3 | 200 | 14 | 63.2 | 59 | 66 | 60.2 | 4 | 197 | 60.2 | 56 | 149 | 0 | 4 | 4 | 4 | 0 | 0 | 61 | 64 |
| V3a | 3200 | 200 | 4 | 3 | 200 | 14 | 131 | 125 | 139 | 128 | 4 | 197 | 128 | 122 | 149 | 0 | 4 | 4 | 4 | 0 | 0 | 128 | 136 |
| V3a | 12800 | 200 | 4 | 3 | 200 | 14 | 186 | 181 | 192 | 182 | 4 | 197 | 182 | 178 | 149 | 4 | 4 | 4 | 4 | 0 | 0 | 182 | 189 |
| V3b | 800 | 200 | 4 | 3 | 200 | 14 | 6 | 5 | 7 | 3 | 4 | 197 | 3 | 2 | 149 | 0 | 4 | 4 | 4 | 0 | 0 | 3 | 4 |
| V3b | 3200 | 200 | 4 | 3 | 200 | 14 | 11 | 7 | 13 | 8 | 4 | 197 | 8 | 4 | 149 | 0 | 4 | 4 | 4 | 0 | 0 | 8 | 10 |
| V3b | 12800 | 200 | 4 | 3 | 200 | 14 | 21.2 | 20 | 23 | 18.2 | 4 | 197 | 18.2 | 17 | 149 | 0 | 4 | 4 | 4 | 0 | 0 | 18.2 | 20 |


(per-data-set n3 detail: `agg_tables.md`, `n3_merged.csv`)

## Reading (neutral; observations at these sizes only)
1. **n1.** The median design-conditional sd of Z−Z′ is ≈ √(|T∖T′|/n) (ratio 1.0–1.2) for L1, L3, L4, i.e. dominated by sample noise of the |T∖T′| ≈ 19 (max ≈ 39) extra regression coefficients, not by a log n factor; it shrinks like n^{-1/2} in n. The population term Var(E[W_l|W_T]−E[W_l|W_T′]) (max over the lattice) decays in r for L1 (0.53 → 0.006 at r=8), L2 (0.67 → 0.046) and L4 (0.40, 0.12, 0.031, 0.004, 2e−4, 4e−6 for r=0,1,2,3,5,8), but **not** for L3 (0.57 → 0.55 at r=8: window radius ≤ 8 < block size 20; max sd stays 0.83–0.92 for every r and n).
2. **n1, AR(1) control.** For r ≥ 5, max-over-lattice sd·√n is flat at 8.4–8.6 for n = 500, 2000, 8000 (so ≲ C/√n, no log n growth visible); for r = 1 it is *not* uniformly small (sd·√n = 11.6, 18.8, 34.0: the population term 0.118 comes from l whose nearest T-elements are > 1 away, since T has gaps). So the "r ≥ 1 ⇒ O(log n/√n)" expectation holds for these lattices only once r exceeds the largest gap between l and its nearest elements of T (r ≳ 3–5), and the realised max|Z−Z′| (one ε) is 0.26 at r=8, n=8000 (≈ 2.8 × max sd). L1/L2 decay in r is slow (max sd at r=8, n=8000: 0.12 and 0.26).
3. **n2.** S0 ⊆ S̃0 in 96/96 data sets. |S̃0∖S0| averages (n=800, 3200): L1 2.4, 7.7; L2 4.1, 7.7; L3 5.5, 11.4; L4 1.75, 1.83. Extras are near S0 for L1 (index distance ≤ 4) and L4 (≤ 3 except one data set at 14); for L2 14/24 data sets have an extra at distance > 8 (max 37, one data set at n=800, p=400); for L3 extras lie within the 20-blocks (distance ≤ 19, 23/24 data sets have one > 8). LS0 from S̃0 certified in 96/96, S0 scored in 96/96, endpoint = S0 in 94/96 (two exceptions: L2 n=800 p=200 seed 6 and L4 n=800 p=200 seed 2 end at S0 plus one null, a certified local maximum); moves = |S̃0∖S0| in 95/96; cap never reached. In three L1 cells (n=800/p=400, n=3200/p=200, n=3200/p=400) one data set packed two truths into the same data-driven block (truths_in_distinct_blocks = 5/6); all other cells 6/6.
4. **n3, visible nulls.** In all 52 data sets S0 ⊆ S̃0 and **every** extra index of S̃0 is a visible null (n_extra = #visible-in-S̃0 in 52/52). Counts grow with n: V1 1.3, 11.2, 21 (of 9, 15, 23 leaves); V2 11.5, 58, 154 (p=200; s0=2 at n=12800) and 214 (p=400, s0=3); V3a 60, 128, 182 (of 197); V3b (θ-sum 0) 3, 8, 18. Against the lemma bound min(K−s0, |vis|−16 s0): bound ≤ 0 (vacuous) in V1 n=800, 3200; observed ≥ bound in V1 n=12800 (21 ≥ 7) and V3a n=12800 (178–189 ≥ 149); observed **below** the bound in 36 of the 44 data sets with positive bound (all V2 rows, e.g. 154 vs 166 and 214 vs 288 at n=12800; V3a n ≤ 3200; all V3b rows, 18 vs 149 at n=12800).
5. **n3, method vs proof route.** LS0 from S̃0 (cap ℓ_n+|S̃0|, never reached) ended at S0, certified, in 52/52 data sets, including those with |S̃0| ≈ 125–221 and |S̃0∖S0| = 100–218 visible nulls; moves ≈ |S̃0∖S0| (≤ 2 more). So in these runs the presence of many visible nulls in the start mode (the obstruction to a route that needs S̃0 to be small) coincides with no failure of LS0; the reverse reading of the lemma bound (observed count below the stated lower bound in 36/44 positive-bound data sets, mostly at the n tested here) is reported as observed — the bound, if meant as an unconditional statement at these n and designs, is not supported by these runs, and may need an n-large / constant qualification (not tested here). The 16 slowest LS0 runs used the re-implemented search (deviation 4).
