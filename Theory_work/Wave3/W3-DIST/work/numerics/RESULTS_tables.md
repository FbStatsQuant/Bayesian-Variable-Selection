# W3-DIST numerics — auto-generated tables (aggregate.py; raw per-replication rows in raw_reps.csv)

Posterior draws per replication: 4000; fresh rows per replication: 20000 (40000 for spike). log Π floored at 0.5/4000 (log = -8.99) when no draw exceeds the threshold; 'frac reps floored' = share of replications at the floor. ĉ = −slope/log n from the regression of log(pooled exceedance fraction) on M over the M with ≥5 exceeding draws pooled over replications.

### N1 — sub-Gaussian AR(0.5), p=12, s0=3, β*=(1,−1,1)

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.89 | 3.51 | 5.46 | 0.482 | 0.898 | 1.395 | 2.06 | 1.60 | -3.09 | -7.78 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.05 |
| 100 | 40 | 1.30 | 2.50 | 3.83 | 0.282 | 0.543 | 0.831 | 1.44 | 1.21 | -6.58 | -8.94 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.08 | 2.14 | 3.34 | 0.204 | 0.403 | 0.631 | 1.21 | 1.07 | -8.05 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.12 | 2.16 | 3.36 | 0.186 | 0.360 | 0.560 | 1.24 | 1.11 | -8.60 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.12 | 2.11 | 3.24 | 0.167 | 0.316 | 0.485 | 1.24 | 1.12 | -8.91 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.17, q99 -0.17; of n·d²/log n (q99): -0.36

### N1 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.33 | 0.077, 0.047, 0.500, 0.258, 0.088, 0.030 | 0.94 | 0.87 | 0.94 | 0/40 | nan | 1.39 |
| 100 | 3.48 | 0.000, 0.000, 0.628, 0.285, 0.072, 0.015 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.02 |
| 200 | 3.29 | 0.000, 0.000, 0.749, 0.213, 0.034, 0.004 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 0.94 |
| 400 | 3.22 | 0.000, 0.000, 0.804, 0.172, 0.021, 0.003 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.02 |
| 800 | 3.14 | 0.000, 0.000, 0.869, 0.117, 0.012, 0.001 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.09 |

### N1 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 3.61e-01 | 1.57e-01 | 2.97e-02 | 1.96e-03 | 0.00e+00 | 3.71e-01 | 1.62e-01 | 2.64e-03 | 1.02 (11) |
| 100 | 2.32e-01 | 3.47e-02 | 3.16e-03 | 1.00e-04 | 0.00e+00 | 1.76e-01 | 1.78e-02 | 1.87e-05 | 1.20 (8) |
| 200 | 1.51e-01 | 1.18e-02 | 6.63e-04 | 1.87e-05 | 0.00e+00 | 6.75e-02 | 1.87e-03 | 0.00e+00 | 1.37 (7) |
| 400 | 1.57e-01 | 6.81e-03 | 1.94e-04 | 0.00e+00 | 0.00e+00 | 3.63e-02 | 1.94e-04 | 0.00e+00 | 1.59 (6) |
| 800 | 1.44e-01 | 5.07e-03 | 1.94e-04 | 6.25e-06 | 0.00e+00 | 1.56e-02 | 3.75e-05 | 0.00e+00 | 1.64 (7) |

### N2a — iid t_2.5 coordinates

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.72 | 3.31 | 4.88 | 0.440 | 0.845 | 1.247 | 1.94 | 1.31 | -3.62 | -8.26 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.26 |
| 100 | 40 | 1.41 | 2.68 | 4.17 | 0.306 | 0.583 | 0.905 | 1.55 | 1.26 | -5.91 | -8.87 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.93 |
| 200 | 40 | 1.30 | 2.48 | 3.81 | 0.246 | 0.467 | 0.719 | 1.44 | 1.17 | -7.33 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.18 | 2.24 | 3.47 | 0.198 | 0.374 | 0.578 | 1.31 | 1.08 | -8.41 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.26 | 2.32 | 3.53 | 0.188 | 0.347 | 0.528 | 1.38 | 1.19 | -8.58 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.12, q99 -0.12; of n·d²/log n (q99): -0.31

### N2a_t25 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 3.40e-01 | 1.19e-01 | 2.15e-02 | 6.25e-04 | 0.00e+00 | 3.47e-01 | 1.27e-01 | 9.13e-04 | 1.04 (9) |
| 100 | 2.50e-01 | 3.54e-02 | 1.41e-02 | 1.58e-03 | 6.25e-06 | 1.83e-01 | 2.36e-02 | 3.31e-04 | 0.90 (10) |
| 200 | 2.24e-01 | 2.57e-02 | 1.73e-03 | 1.00e-04 | 0.00e+00 | 1.12e-01 | 4.77e-03 | 0.00e+00 | 1.25 (8) |
| 400 | 1.82e-01 | 1.33e-02 | 5.56e-04 | 1.25e-05 | 0.00e+00 | 5.47e-02 | 5.56e-04 | 0.00e+00 | 1.44 (7) |
| 800 | 1.92e-01 | 2.07e-02 | 1.97e-03 | 1.31e-04 | 0.00e+00 | 4.19e-02 | 8.00e-04 | 0.00e+00 | 1.19 (8) |

### N2a — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.29 | 0.042, 0.100, 0.504, 0.256, 0.077, 0.021 | 0.89 | 0.95 | 0.91 | 0/40 | nan | 1.28 |
| 100 | 3.46 | 0.000, 0.008, 0.636, 0.263, 0.074, 0.018 | 1.00 | 1.00 | 0.99 | 0/40 | nan | 1.23 |
| 200 | 3.33 | 0.000, 0.000, 0.719, 0.236, 0.040, 0.005 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.12 |
| 400 | 3.19 | 0.000, 0.000, 0.833, 0.151, 0.016, 0.001 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.02 |
| 800 | 3.19 | 0.000, 0.000, 0.832, 0.151, 0.016, 0.001 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.06 |

### N2b — symmetric Pareto, tail index 2.1

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 2.55 | 3.78 | 4.94 | 0.651 | 0.965 | 1.264 | 2.57 | 1.95 | -2.55 | -8.74 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.94 |
| 100 | 40 | 1.49 | 2.95 | 4.48 | 0.323 | 0.640 | 0.972 | 1.64 | 1.27 | -5.21 | -8.91 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.38 |
| 200 | 40 | 1.40 | 2.63 | 3.95 | 0.264 | 0.497 | 0.746 | 1.54 | 1.24 | -7.04 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.07 | 2.10 | 3.28 | 0.179 | 0.350 | 0.547 | 1.20 | 0.96 | -8.52 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.19 | 2.25 | 3.43 | 0.178 | 0.337 | 0.513 | 1.32 | 1.09 | -8.86 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.27, q99 -0.15; of n·d²/log n (q99): -0.34

### N2b_pareto — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 6.47e-01 | 1.53e-01 | 2.93e-03 | 7.50e-05 | 0.00e+00 | 6.61e-01 | 1.88e-01 | 9.38e-05 | 1.42 (8) |
| 100 | 2.77e-01 | 5.59e-02 | 5.79e-03 | 3.38e-04 | 0.00e+00 | 2.27e-01 | 2.50e-02 | 4.37e-05 | 1.16 (9) |
| 200 | 2.54e-01 | 3.24e-02 | 7.36e-03 | 2.44e-04 | 6.25e-06 | 1.31e-01 | 1.07e-02 | 6.25e-06 | 1.12 (9) |
| 400 | 1.35e-01 | 6.15e-03 | 2.37e-04 | 0.00e+00 | 0.00e+00 | 2.92e-02 | 2.37e-04 | 0.00e+00 | 1.57 (7) |
| 800 | 1.81e-01 | 7.51e-03 | 2.50e-04 | 0.00e+00 | 0.00e+00 | 2.26e-02 | 6.25e-05 | 0.00e+00 | 1.61 (7) |

### N2b — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 2.40 | 0.252, 0.258, 0.295, 0.141, 0.042, 0.011 | 0.66 | 0.56 | 0.71 | 0/40 | nan | 2.50 |
| 100 | 3.27 | 0.003, 0.087, 0.618, 0.232, 0.051, 0.009 | 0.97 | 0.95 | 0.96 | 0/40 | nan | 1.26 |
| 200 | 3.31 | 0.000, 0.005, 0.738, 0.211, 0.040, 0.007 | 1.00 | 1.00 | 0.99 | 0/40 | nan | 1.26 |
| 400 | 3.21 | 0.000, 0.000, 0.816, 0.164, 0.019, 0.002 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.00 |
| 800 | 3.16 | 0.000, 0.000, 0.852, 0.134, 0.013, 0.001 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.11 |

### N2c — spike columns

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 0.27 | 0.75 | 1.45 | 0.069 | 0.191 | 0.371 | 0.37 | 0.96 | -8.83 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 100 | 40 | 0.28 | 0.72 | 1.37 | 0.062 | 0.157 | 0.298 | 0.37 | 0.97 | -8.87 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 0.33 | 0.76 | 1.41 | 0.061 | 0.144 | 0.267 | 0.41 | 0.98 | -8.99 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 0.38 | 0.88 | 1.58 | 0.063 | 0.146 | 0.263 | 0.47 | 0.97 | -8.99 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 0.39 | 0.91 | 1.63 | 0.059 | 0.136 | 0.243 | 0.49 | 0.91 | -8.99 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median 0.15, q99 0.05; of n·d²/log n (q99): -0.14

### N2c_spike — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 5.38e-03 | 5.00e-05 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 5.88e-03 | 6.88e-05 | 0.00e+00 | 2.39 (4) |
| 100 | 9.30e-03 | 2.12e-04 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 5.04e-03 | 6.25e-05 | 0.00e+00 | 1.93 (4) |
| 200 | 3.56e-03 | 2.50e-05 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 5.38e-04 | 0.00e+00 | 0.00e+00 | 2.97 (3) |
| 400 | 1.10e-02 | 5.62e-05 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 1.02e-03 | 0.00e+00 | 0.00e+00 | 2.48 (4) |
| 800 | 8.94e-03 | 5.62e-05 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 2.31e-04 | 0.00e+00 | 0.00e+00 | 2.52 (4) |

### N2c — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.01 | 0.060, 0.227, 0.441, 0.203, 0.057, 0.013 | 0.97 | 0.98 | 0.99 | 15/40 | 0.2 | 0.19 |
| 100 | 2.93 | 0.020, 0.298, 0.467, 0.170, 0.037, 0.007 | 0.97 | 0.96 | 1.00 | 17/40 | 0.3 | 0.16 |
| 200 | 2.99 | 0.000, 0.246, 0.565, 0.151, 0.033, 0.006 | 0.99 | 1.00 | 1.00 | 13/40 | 0.3 | 0.23 |
| 400 | 2.77 | 0.043, 0.284, 0.546, 0.113, 0.013, 0.001 | 1.00 | 1.00 | 1.00 | 15/40 | 0.3 | 0.32 |
| 800 | 2.87 | 0.024, 0.214, 0.644, 0.108, 0.010, 0.001 | 1.00 | 0.99 | 1.00 | 11/40 | 0.3 | 0.32 |

### N3 — no beta-min, β*=(1, c√(log n/n), c√(log n/n)), c=0.7

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.29 | 2.29 | 3.50 | 0.330 | 0.585 | 0.896 | 1.44 | 1.19 | -5.84 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 100 | 40 | 1.27 | 2.12 | 3.19 | 0.275 | 0.459 | 0.694 | 1.38 | 1.26 | -7.50 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.35 | 2.26 | 3.41 | 0.255 | 0.427 | 0.643 | 1.47 | 1.31 | -8.10 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.42 | 2.28 | 3.33 | 0.237 | 0.381 | 0.556 | 1.53 | 1.42 | -8.58 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.42 | 2.24 | 3.26 | 0.212 | 0.335 | 0.488 | 1.52 | 1.41 | -8.87 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median 0.04, q99 -0.01; of n·d²/log n (q99): -0.21

### N3 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 1.78e-01 | 3.56e-02 | 9.56e-04 | 6.25e-06 | 0.00e+00 | 1.87e-01 | 3.83e-02 | 6.25e-06 | 1.37 (7) |
| 100 | 1.50e-01 | 4.54e-03 | 5.00e-05 | 0.00e+00 | 0.00e+00 | 9.21e-02 | 1.46e-03 | 0.00e+00 | 1.87 (6) |
| 200 | 1.79e-01 | 1.41e-02 | 1.37e-03 | 6.25e-05 | 0.00e+00 | 7.16e-02 | 3.17e-03 | 0.00e+00 | 1.29 (8) |
| 400 | 1.90e-01 | 6.95e-03 | 2.19e-04 | 6.25e-06 | 0.00e+00 | 3.84e-02 | 2.19e-04 | 0.00e+00 | 1.67 (7) |
| 800 | 1.84e-01 | 5.57e-03 | 1.44e-04 | 6.25e-06 | 0.00e+00 | 1.74e-02 | 5.62e-05 | 0.00e+00 | 1.73 (7) |

### N3 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 1.69 | 0.515, 0.329, 0.115, 0.031, 0.008, 0.002 | 0.97 | 0.18 | 0.15 | 0/40 | nan | 1.09 |
| 100 | 1.57 | 0.551, 0.346, 0.085, 0.015, 0.002, 0.000 | 1.00 | 0.13 | 0.20 | 0/40 | nan | 1.26 |
| 200 | 1.60 | 0.522, 0.377, 0.084, 0.014, 0.002, 0.000 | 1.00 | 0.17 | 0.18 | 0/40 | nan | 1.28 |
| 400 | 1.51 | 0.566, 0.365, 0.062, 0.006, 0.000, 0.000 | 1.00 | 0.15 | 0.20 | 0/40 | nan | 1.33 |
| 800 | 1.50 | 0.555, 0.389, 0.051, 0.004, 0.000, 0.000 | 1.00 | 0.20 | 0.20 | 0/40 | nan | 1.38 |

### N4 — collinear nulls, τ² = n-2

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.36 | 2.76 | 4.35 | 0.349 | 0.705 | 1.111 | 1.56 | 1.20 | -4.50 | -8.67 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.95 |
| 100 | 40 | 1.12 | 2.13 | 3.23 | 0.243 | 0.461 | 0.702 | 1.24 | 1.07 | -7.68 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.07 | 2.04 | 3.14 | 0.201 | 0.386 | 0.592 | 1.18 | 1.07 | -8.50 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.17 | 2.17 | 3.28 | 0.195 | 0.363 | 0.547 | 1.28 | 1.16 | -8.77 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.22 | 2.24 | 3.37 | 0.183 | 0.335 | 0.505 | 1.34 | 1.22 | -8.79 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.03, q99 -0.07; of n·d²/log n (q99): -0.26

### N4 τ²=n-2 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 2.12e-01 | 7.52e-02 | 1.74e-02 | 1.44e-03 | 0.00e+00 | 2.21e-01 | 7.82e-02 | 1.91e-03 | 0.88 (9) |
| 100 | 1.49e-01 | 5.63e-03 | 1.31e-04 | 6.25e-06 | 0.00e+00 | 9.44e-02 | 1.93e-03 | 0.00e+00 | 1.67 (6) |
| 200 | 1.31e-01 | 9.91e-03 | 5.38e-04 | 0.00e+00 | 0.00e+00 | 5.40e-02 | 1.76e-03 | 0.00e+00 | 1.45 (7) |
| 400 | 1.69e-01 | 6.54e-03 | 2.50e-04 | 6.25e-06 | 0.00e+00 | 3.61e-02 | 2.50e-04 | 0.00e+00 | 1.55 (7) |
| 800 | 1.98e-01 | 1.33e-02 | 4.38e-04 | 6.25e-06 | 0.00e+00 | 3.32e-02 | 1.00e-04 | 0.00e+00 | 1.43 (6) |

### N4 τ²=n-2 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.86 | 0.014, 0.029, 0.412, 0.300, 0.152, 0.093 | 0.26 | 0.93 | 0.96 | 0/40 | nan | 1.10 |
| 100 | 3.87 | 0.000, 0.000, 0.461, 0.312, 0.149, 0.079 | 0.25 | 1.00 | 1.00 | 0/40 | nan | 1.09 |
| 200 | 3.89 | 0.000, 0.000, 0.456, 0.311, 0.150, 0.083 | 0.25 | 1.00 | 1.00 | 0/40 | nan | 0.99 |
| 400 | 3.86 | 0.000, 0.000, 0.465, 0.310, 0.149, 0.076 | 0.26 | 1.00 | 1.00 | 0/40 | nan | 1.11 |
| 800 | 3.79 | 0.000, 0.000, 0.495, 0.306, 0.135, 0.064 | 0.25 | 1.00 | 1.00 | 0/40 | nan | 1.08 |

### N4 — collinear nulls, τ² = n-1

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.53 | 3.00 | 4.65 | 0.391 | 0.768 | 1.189 | 1.73 | 1.36 | -3.93 | -8.50 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.41 |
| 100 | 40 | 1.25 | 2.38 | 3.65 | 0.271 | 0.516 | 0.792 | 1.39 | 1.22 | -6.64 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.38 | 2.49 | 3.73 | 0.260 | 0.471 | 0.704 | 1.51 | 1.35 | -7.53 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.29 | 2.37 | 3.61 | 0.215 | 0.396 | 0.602 | 1.42 | 1.28 | -8.45 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.16 | 2.14 | 3.29 | 0.174 | 0.321 | 0.492 | 1.29 | 1.15 | -8.87 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.08, q99 -0.10; of n·d²/log n (q99): -0.29

### N4 τ²=n-1 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 2.99e-01 | 6.74e-02 | 8.22e-03 | 1.94e-04 | 0.00e+00 | 3.11e-01 | 7.11e-02 | 2.81e-04 | 1.22 (9) |
| 100 | 2.03e-01 | 1.52e-02 | 7.25e-04 | 2.50e-05 | 0.00e+00 | 1.41e-01 | 6.39e-03 | 6.25e-06 | 1.37 (7) |
| 200 | 2.45e-01 | 2.56e-02 | 2.22e-03 | 9.38e-05 | 0.00e+00 | 1.18e-01 | 5.63e-03 | 0.00e+00 | 1.26 (9) |
| 400 | 2.07e-01 | 1.48e-02 | 6.50e-04 | 1.87e-05 | 0.00e+00 | 5.93e-02 | 6.56e-04 | 0.00e+00 | 1.42 (7) |
| 800 | 1.52e-01 | 5.95e-03 | 1.44e-04 | 1.25e-05 | 0.00e+00 | 1.80e-02 | 6.25e-05 | 0.00e+00 | 1.61 (7) |

### N4 τ²=n-1 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.45 | 0.020, 0.016, 0.587, 0.271, 0.081, 0.024 | 0.22 | 0.96 | 0.98 | 0/40 | nan | 1.37 |
| 100 | 3.41 | 0.000, 0.000, 0.677, 0.254, 0.056, 0.013 | 0.20 | 1.00 | 1.00 | 0/40 | nan | 1.16 |
| 200 | 3.29 | 0.000, 0.000, 0.754, 0.205, 0.035, 0.006 | 0.20 | 1.00 | 1.00 | 0/40 | nan | 1.21 |
| 400 | 3.22 | 0.000, 0.000, 0.808, 0.167, 0.022, 0.003 | 0.20 | 1.00 | 1.00 | 0/40 | nan | 1.21 |
| 800 | 3.14 | 0.000, 0.000, 0.872, 0.118, 0.010, 0.001 | 0.21 | 1.00 | 1.00 | 0/40 | nan | 1.06 |

### N4 — collinear nulls, τ² = logn_n

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.98 | 3.50 | 5.14 | 0.506 | 0.894 | 1.313 | 2.13 | 1.66 | -3.22 | -8.23 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.13 |
| 100 | 40 | 1.45 | 2.54 | 3.78 | 0.315 | 0.552 | 0.821 | 1.57 | 1.36 | -6.64 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.51 | 2.54 | 3.69 | 0.285 | 0.480 | 0.696 | 1.61 | 1.47 | -8.03 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.57 | 2.62 | 3.77 | 0.263 | 0.438 | 0.629 | 1.66 | 1.54 | -8.21 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.46 | 2.45 | 3.53 | 0.218 | 0.366 | 0.529 | 1.54 | 1.45 | -8.82 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.08, q99 -0.11; of n·d²/log n (q99): -0.30

### N4 τ²=logn_n — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 3.92e-01 | 1.36e-01 | 2.26e-02 | 1.24e-03 | 0.00e+00 | 4.04e-01 | 1.42e-01 | 1.71e-03 | 1.10 (10) |
| 100 | 2.45e-01 | 1.36e-02 | 9.63e-04 | 6.88e-05 | 0.00e+00 | 1.61e-01 | 5.83e-03 | 6.25e-06 | 1.35 (8) |
| 200 | 2.61e-01 | 1.08e-02 | 2.94e-04 | 6.25e-06 | 0.00e+00 | 1.03e-01 | 1.01e-03 | 0.00e+00 | 1.69 (7) |
| 400 | 3.00e-01 | 1.64e-02 | 5.75e-04 | 6.25e-06 | 0.00e+00 | 7.90e-02 | 6.06e-04 | 0.00e+00 | 1.51 (7) |
| 800 | 2.46e-01 | 9.09e-03 | 3.44e-04 | 6.25e-06 | 0.00e+00 | 2.69e-02 | 8.12e-05 | 0.00e+00 | 1.62 (7) |

### N4 τ²=logn_n — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.30 | 0.048, 0.052, 0.564, 0.248, 0.068, 0.019 | 0.31 | 0.90 | 0.92 | 0/40 | nan | 1.49 |
| 100 | 3.36 | 0.000, 0.000, 0.710, 0.229, 0.050, 0.011 | 0.39 | 1.00 | 1.00 | 0/40 | nan | 1.36 |
| 200 | 3.23 | 0.000, 0.000, 0.800, 0.176, 0.022, 0.002 | 0.34 | 1.00 | 1.00 | 0/40 | nan | 1.42 |
| 400 | 3.18 | 0.000, 0.000, 0.832, 0.152, 0.015, 0.001 | 0.36 | 1.00 | 1.00 | 0/40 | nan | 1.50 |
| 800 | 3.13 | 0.000, 0.000, 0.880, 0.110, 0.010, 0.001 | 0.44 | 1.00 | 1.00 | 0/40 | nan | 1.47 |

### N4 — collinear nulls, τ² = 1

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.97 | 3.71 | 5.38 | 0.504 | 0.947 | 1.376 | 2.13 | 1.70 | -2.91 | -8.12 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.28 |
| 100 | 40 | 1.42 | 2.68 | 4.11 | 0.308 | 0.582 | 0.892 | 1.56 | 1.36 | -5.75 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 1.26 | 2.38 | 3.63 | 0.239 | 0.449 | 0.684 | 1.39 | 1.24 | -7.72 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 1.20 | 2.31 | 3.54 | 0.200 | 0.385 | 0.591 | 1.33 | 1.18 | -8.40 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 1.14 | 2.19 | 3.34 | 0.170 | 0.327 | 0.499 | 1.27 | 1.14 | -8.86 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.18, q99 -0.16; of n·d²/log n (q99): -0.35

### N4 τ²=1 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 4.17e-01 | 1.47e-01 | 2.39e-02 | 5.81e-04 | 6.25e-06 | 4.26e-01 | 1.54e-01 | 1.05e-03 | 1.11 (9) |
| 100 | 2.74e-01 | 2.67e-02 | 1.70e-03 | 7.50e-05 | 0.00e+00 | 2.02e-01 | 1.17e-02 | 0.00e+00 | 1.31 (8) |
| 200 | 2.09e-01 | 1.39e-02 | 6.12e-04 | 3.13e-05 | 0.00e+00 | 9.25e-02 | 1.86e-03 | 0.00e+00 | 1.44 (8) |
| 400 | 1.84e-01 | 1.41e-02 | 8.69e-04 | 3.13e-05 | 0.00e+00 | 5.29e-02 | 8.88e-04 | 0.00e+00 | 1.39 (8) |
| 800 | 1.65e-01 | 7.35e-03 | 1.81e-04 | 6.25e-06 | 0.00e+00 | 2.28e-02 | 6.25e-05 | 0.00e+00 | 1.62 (7) |

### N4 τ²=1 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 3.46 | 0.050, 0.046, 0.472, 0.297, 0.101, 0.033 | 0.82 | 0.90 | 0.95 | 0/40 | nan | 1.65 |
| 100 | 3.55 | 0.000, 0.000, 0.571, 0.327, 0.085, 0.018 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.28 |
| 200 | 3.32 | 0.000, 0.000, 0.735, 0.215, 0.043, 0.008 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.09 |
| 400 | 3.24 | 0.000, 0.000, 0.789, 0.185, 0.025, 0.002 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.10 |
| 800 | 3.16 | 0.000, 0.000, 0.852, 0.137, 0.011, 0.001 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.14 |

### N5 — approximate sparsity β*_j = c j⁻², Var(xᵀβ*)=3

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 1.76 | 2.71 | 3.86 | 0.451 | 0.693 | 0.986 | 1.86 | 1.62 | -5.17 | -8.80 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 1.25 |
| 100 | 40 | 2.07 | 3.25 | 4.39 | 0.449 | 0.705 | 0.953 | 2.19 | 1.93 | -5.48 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 200 | 40 | 2.45 | 3.53 | 4.87 | 0.462 | 0.666 | 0.919 | 2.52 | 2.33 | -5.76 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 400 | 40 | 2.76 | 3.98 | 5.28 | 0.461 | 0.664 | 0.882 | 2.86 | 2.65 | -6.09 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |
| 800 | 40 | 3.26 | 4.52 | 5.84 | 0.488 | 0.676 | 0.874 | 3.34 | 3.23 | -6.40 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median 0.22, q99 0.15; of n·d²/log n (q99): -0.05

### N5 — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 3.38e-01 | 2.51e-02 | 1.91e-03 | 1.88e-04 | 0.00e+00 | 3.59e-01 | 2.79e-02 | 2.12e-04 | 1.24 (9) |
| 100 | 4.94e-01 | 5.25e-02 | 2.87e-03 | 1.31e-04 | 0.00e+00 | 3.81e-01 | 2.38e-02 | 6.25e-06 | 1.31 (8) |
| 200 | 6.53e-01 | 8.84e-02 | 4.96e-03 | 1.50e-04 | 0.00e+00 | 3.84e-01 | 1.46e-02 | 6.25e-06 | 1.35 (9) |
| 400 | 7.73e-01 | 1.38e-01 | 1.13e-02 | 2.81e-04 | 0.00e+00 | 3.91e-01 | 1.15e-02 | 0.00e+00 | 1.28 (9) |
| 800 | 8.84e-01 | 2.55e-01 | 2.57e-02 | 1.22e-03 | 0.00e+00 | 4.48e-01 | 1.13e-02 | 0.00e+00 | 1.16 (10) |

### N5 — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 2.08 | 0.341, 0.377, 0.185, 0.067, 0.022, 0.008 | 1.00 | 0.35 | 0.17 | 0/40 | nan | 1.73 |
| 100 | 2.49 | 0.096, 0.483, 0.290, 0.103, 0.023, 0.004 | 1.00 | 0.55 | 0.33 | 0/40 | nan | 1.97 |
| 200 | 2.83 | 0.003, 0.391, 0.420, 0.153, 0.029, 0.004 | 1.00 | 0.82 | 0.34 | 0/40 | nan | 2.29 |
| 400 | 3.41 | 0.000, 0.093, 0.507, 0.311, 0.077, 0.011 | 1.00 | 0.98 | 0.44 | 0/40 | nan | 2.77 |
| 800 | 4.01 | 0.000, 0.005, 0.240, 0.529, 0.198, 0.028 | 1.00 | 1.00 | 0.65 | 0/40 | nan | 3.20 |

### N7 — restricted family, AR(0.5), p=4n (RESTRICTED FAMILY)

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 3.90 | 6.15 | 8.23 | 0.998 | 1.573 | 2.104 | 4.20 | 3.31 | -1.17 | -4.28 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.53 |
| 100 | 40 | 1.11 | 2.41 | 3.87 | 0.242 | 0.523 | 0.840 | 1.30 | 1.06 | -6.38 | -8.64 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.24 |
| 200 | 40 | 1.09 | 2.12 | 3.36 | 0.205 | 0.399 | 0.634 | 1.21 | 1.06 | -7.76 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.92, q99 -0.65; of n·d²/log n (q99): -0.87

### N7 — restricted family, AR(0.5), p=4n — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 6.42e-01 | 5.68e-01 | 3.37e-01 | 6.17e-02 | 2.33e-03 | 6.46e-01 | 5.70e-01 | 7.11e-02 | 0.66 (14) |
| 100 | 1.76e-01 | 1.93e-02 | 5.53e-03 | 4.08e-03 | 9.38e-05 | 1.24e-01 | 1.10e-02 | 3.59e-03 | 0.69 (13) |
| 200 | 1.46e-01 | 1.34e-02 | 1.30e-03 | 8.75e-05 | 0.00e+00 | 6.51e-02 | 3.02e-03 | 0.00e+00 | 1.22 (8) |

### N7 — restricted family, AR(0.5), p=4n — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 1.92 | 0.418, 0.137, 0.370, 0.069, 0.005, 0.000 | 0.53 | 0.44 | 0.65 | 0/40 | nan | 4.84 |
| 100 | 3.07 | 0.003, 0.001, 0.921, 0.072, 0.003, 0.000 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 0.93 |
| 200 | 3.05 | 0.000, 0.000, 0.948, 0.049, 0.003, 0.000 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 0.91 |

### N7 — restricted family, AR(0.5), p=min(n^1.5,600) (RESTRICTED FAMILY)

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 4.94 | 6.61 | 8.43 | 1.264 | 1.690 | 2.156 | 4.93 | 4.15 | -0.75 | -3.78 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.63 |
| 100 | 40 | 1.26 | 2.56 | 4.09 | 0.274 | 0.557 | 0.887 | 1.46 | 1.20 | -6.02 | -8.31 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.12 |
| 200 | 40 | 1.02 | 2.02 | 3.24 | 0.193 | 0.381 | 0.612 | 1.15 | 0.99 | -7.97 | -8.97 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -1.14, q99 -0.69; of n·d²/log n (q99): -0.91

### N7 — restricted family, AR(0.5), p=min(n^1.5,600) — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 7.61e-01 | 7.19e-01 | 4.61e-01 | 4.96e-02 | 6.50e-04 | 7.62e-01 | 7.21e-01 | 6.14e-02 | 0.79 (14) |
| 100 | 2.00e-01 | 2.87e-02 | 1.34e-02 | 1.17e-02 | 3.06e-04 | 1.41e-01 | 1.99e-02 | 1.14e-02 | 0.60 (13) |
| 200 | 1.27e-01 | 8.53e-03 | 6.00e-04 | 2.50e-05 | 0.00e+00 | 5.11e-02 | 1.51e-03 | 6.25e-06 | 1.36 (7) |

### N7 — restricted family, AR(0.5), p=min(n^1.5,600) — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 1.43 | 0.578, 0.142, 0.248, 0.030, 0.002, 0.000 | 0.47 | 0.28 | 0.42 | 0/40 | nan | 5.23 |
| 100 | 3.07 | 0.008, 0.004, 0.900, 0.084, 0.004, 0.000 | 0.99 | 0.99 | 1.00 | 0/40 | nan | 1.11 |
| 200 | 3.04 | 0.000, 0.000, 0.957, 0.042, 0.001, 0.000 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 0.99 |

### N7 — restricted family, iid t_2.5, p=4n (RESTRICTED FAMILY)

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 3.86 | 5.41 | 7.01 | 0.988 | 1.384 | 1.792 | 3.81 | 2.78 | -1.59 | -5.42 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.65 |
| 100 | 40 | 1.44 | 3.10 | 4.68 | 0.313 | 0.673 | 1.016 | 1.67 | 1.27 | -5.56 | -8.22 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.26 |
| 200 | 40 | 1.14 | 2.17 | 3.40 | 0.215 | 0.409 | 0.641 | 1.27 | 1.00 | -7.79 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.88, q99 -0.52; of n·d²/log n (q99): -0.74

### N7 — restricted family, iid t_2.5, p=4n — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 6.93e-01 | 4.45e-01 | 2.06e-01 | 2.70e-02 | 2.50e-05 | 6.97e-01 | 4.58e-01 | 3.61e-02 | 0.79 (11) |
| 100 | 2.44e-01 | 5.90e-02 | 3.52e-02 | 1.66e-02 | 1.36e-03 | 1.84e-01 | 4.78e-02 | 1.47e-02 | 0.56 (14) |
| 200 | 1.72e-01 | 9.01e-03 | 3.44e-04 | 1.87e-05 | 0.00e+00 | 7.01e-02 | 1.21e-03 | 0.00e+00 | 1.49 (7) |

### N7 — restricted family, iid t_2.5, p=4n — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 2.18 | 0.253, 0.325, 0.374, 0.046, 0.002, 0.000 | 0.67 | 0.68 | 0.61 | 0/40 | nan | 3.79 |
| 100 | 3.05 | 0.011, 0.024, 0.876, 0.087, 0.004, 0.000 | 0.98 | 0.98 | 0.98 | 0/40 | nan | 1.10 |
| 200 | 3.02 | 0.000, 0.000, 0.976, 0.024, 0.000, 0.000 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 0.97 |

### N7 — restricted family, iid t_2.5, p=min(n^1.5,600) (RESTRICTED FAMILY)

(means over replications of the per-replication posterior quantiles; R = replications; d² = joint Hellinger, fresh-x Monte Carlo)

| n | R | n·d² med | n·d² q90 | n·d² q99 | n·d²/log n med | q90 | q99 | E[n·d²] | n·h̄² med (in-sample) | meanlogΠ M=1 | meanlogΠ M=2 | meanlogΠ M=4 | meanlogΠ M=8 | meanlogΠ M=16 | frac reps floored (M=8,16) | ĉ=−slope/log n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 40 | 3.90 | 5.70 | 7.35 | 0.997 | 1.458 | 1.879 | 3.96 | 3.12 | -1.74 | -4.79 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | 0.47 |
| 100 | 40 | 1.75 | 2.97 | 4.42 | 0.381 | 0.645 | 0.961 | 1.88 | 1.62 | -6.18 | -8.49 | -8.77 | -8.99 | -8.99 | 1.00,1.00 | 0.09 |
| 200 | 40 | 1.09 | 2.10 | 3.35 | 0.205 | 0.396 | 0.633 | 1.21 | 0.96 | -8.02 | -8.99 | -8.99 | -8.99 | -8.99 | 1.00,1.00 | nan |

log–log slope of n·d² vs n: median -0.92, q99 -0.57; of n·d²/log n (q99): -0.78

### N7 — restricted family, iid t_2.5, p=min(n^1.5,600) — finer tail resolution (pooled over all replications×draws, from arrays/*.npz)

P(·) are pooled exceedance fractions (R·4000 draws; smallest resolvable ≈ 1/(R·4000)). c_t = −slope of log P(n·d² > t) on t over integer t=1..14 with ≥ 5 exceedances (≥3 points); in the regime log P ≈ −c M log n with t = M log n this is the constant c of the tail claim.

| n | P(n d²>2) | P(n d²>4) | P(n d²>6) | P(n d²>8) | P(n d²>12) | P(n d²/log n>0.5) | P(n d²/log n>1) | P(n d²/log n>2) | c_t (#pts) |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 6.62e-01 | 4.65e-01 | 2.60e-01 | 5.39e-02 | 1.31e-04 | 6.65e-01 | 4.74e-01 | 7.46e-02 | 0.77 (12) |
| 100 | 2.08e-01 | 6.97e-02 | 5.71e-02 | 2.68e-02 | 2.50e-02 | 1.61e-01 | 6.45e-02 | 2.53e-02 | 0.20 (14) |
| 200 | 1.42e-01 | 1.04e-02 | 6.94e-04 | 4.37e-05 | 0.00e+00 | 5.95e-02 | 1.69e-03 | 0.00e+00 | 1.37 (8) |

### N7 — restricted family, iid t_2.5, p=min(n^1.5,600) — selection / size / dropped columns

| n | E|S| | P(|S|=0..) hist sizes 0-1,2,3,4,5,≥6 | incl x1 | incl x2 | incl x3 | reps with a true col dropped | median n·d² (dropped) | median n·d² (not dropped) |
|---|---|---|---|---|---|---|---|---|
| 50 | 2.10 | 0.292, 0.246, 0.410, 0.048, 0.003, 0.000 | 0.62 | 0.65 | 0.60 | 0/40 | nan | 3.63 |
| 100 | 2.97 | 0.021, 0.039, 0.888, 0.051, 0.001, 0.000 | 0.97 | 0.95 | 0.99 | 0/40 | nan | 1.03 |
| 200 | 3.03 | 0.000, 0.000, 0.969, 0.031, 0.001, 0.000 | 1.00 | 1.00 | 1.00 | 0/40 | nan | 1.04 |

### N6 — transfer ratio ρ = d²_mean / (2 t̄ + log n / n) over all posterior draws

| design | n | draws | max ρ | pooled 0.999 q | pooled median | max over reps of per-rep 0.999 q |
|---|---|---|---|---|---|---|
| N1 | 50 | 160000 | 0.835 | 0.727 | 0.296 | 0.769 |
| N1 | 100 | 160000 | 0.681 | 0.580 | 0.224 | 0.640 |
| N1 | 200 | 160000 | 0.567 | 0.485 | 0.185 | 0.542 |
| N1 | 400 | 160000 | 0.438 | 0.391 | 0.175 | 0.419 |
| N1 | 800 | 160000 | 0.450 | 0.376 | 0.169 | 0.421 |
| N2a_t25 | 50 | 160000 | 1.004 | 0.781 | 0.291 | 0.918 |
| N2a_t25 | 100 | 160000 | 0.717 | 0.612 | 0.247 | 0.680 |
| N2a_t25 | 200 | 160000 | 0.604 | 0.532 | 0.220 | 0.594 |
| N2a_t25 | 400 | 160000 | 0.572 | 0.484 | 0.187 | 0.557 |
| N2a_t25 | 800 | 160000 | 0.537 | 0.472 | 0.176 | 0.530 |
| N2b_pareto | 50 | 160000 | 0.922 | 0.743 | 0.396 | 0.864 |
| N2b_pareto | 100 | 160000 | 0.732 | 0.636 | 0.235 | 0.681 |
| N2b_pareto | 200 | 160000 | 0.589 | 0.517 | 0.220 | 0.568 |
| N2b_pareto | 400 | 160000 | 0.601 | 0.448 | 0.181 | 0.555 |
| N2b_pareto | 800 | 160000 | 0.554 | 0.434 | 0.182 | 0.493 |
| N2c_spike | 50 | 160000 | 0.251 | 0.219 | 0.014 | 0.242 |
| N2c_spike | 100 | 160000 | 0.160 | 0.149 | 0.015 | 0.156 |
| N2c_spike | 200 | 160000 | 0.201 | 0.183 | 0.024 | 0.200 |
| N2c_spike | 400 | 160000 | 0.157 | 0.149 | 0.024 | 0.157 |
| N2c_spike | 800 | 160000 | 0.138 | 0.132 | 0.023 | 0.135 |
| N3 | 50 | 160000 | 0.826 | 0.610 | 0.261 | 0.757 |
| N3 | 100 | 160000 | 0.626 | 0.465 | 0.234 | 0.541 |
| N3 | 200 | 160000 | 0.517 | 0.450 | 0.225 | 0.487 |
| N3 | 400 | 160000 | 0.478 | 0.396 | 0.217 | 0.457 |
| N3 | 800 | 160000 | 0.409 | 0.368 | 0.210 | 0.402 |
| N4_tau2=n-2 | 50 | 160000 | 0.842 | 0.757 | 0.241 | 0.808 |
| N4_tau2=n-2 | 100 | 160000 | 0.679 | 0.508 | 0.215 | 0.595 |
| N4_tau2=n-2 | 200 | 160000 | 0.551 | 0.407 | 0.184 | 0.448 |
| N4_tau2=n-2 | 400 | 160000 | 0.511 | 0.402 | 0.183 | 0.441 |
| N4_tau2=n-2 | 800 | 160000 | 0.436 | 0.387 | 0.173 | 0.419 |
| N4_tau2=n-1 | 50 | 160000 | 0.962 | 0.705 | 0.285 | 0.842 |
| N4_tau2=n-1 | 100 | 160000 | 0.694 | 0.512 | 0.229 | 0.593 |
| N4_tau2=n-1 | 200 | 160000 | 0.524 | 0.469 | 0.221 | 0.513 |
| N4_tau2=n-1 | 400 | 160000 | 0.496 | 0.418 | 0.193 | 0.462 |
| N4_tau2=n-1 | 800 | 160000 | 0.434 | 0.373 | 0.176 | 0.394 |
| N4_tau2=logn_n | 50 | 160000 | 0.872 | 0.759 | 0.313 | 0.838 |
| N4_tau2=logn_n | 100 | 160000 | 0.668 | 0.535 | 0.260 | 0.609 |
| N4_tau2=logn_n | 200 | 160000 | 0.576 | 0.457 | 0.242 | 0.511 |
| N4_tau2=logn_n | 400 | 160000 | 0.534 | 0.439 | 0.232 | 0.512 |
| N4_tau2=logn_n | 800 | 160000 | 0.452 | 0.393 | 0.213 | 0.441 |
| N4_tau2=1 | 50 | 160000 | 0.937 | 0.675 | 0.309 | 0.850 |
| N4_tau2=1 | 100 | 160000 | 0.678 | 0.552 | 0.247 | 0.657 |
| N4_tau2=1 | 200 | 160000 | 0.526 | 0.436 | 0.201 | 0.475 |
| N4_tau2=1 | 400 | 160000 | 0.474 | 0.408 | 0.177 | 0.439 |
| N4_tau2=1 | 800 | 160000 | 0.462 | 0.389 | 0.162 | 0.434 |
| N5 | 50 | 160000 | 0.993 | 0.653 | 0.329 | 0.932 |
| N5 | 100 | 160000 | 0.680 | 0.575 | 0.318 | 0.637 |
| N5 | 200 | 160000 | 0.623 | 0.521 | 0.318 | 0.580 |
| N5 | 400 | 160000 | 0.530 | 0.457 | 0.315 | 0.504 |
| N5 | 800 | 160000 | 0.478 | 0.430 | 0.321 | 0.466 |
| N7_ar_p4n | 50 | 160000 | 0.994 | 0.819 | 0.442 | 0.946 |
| N7_ar_p4n | 100 | 160000 | 0.762 | 0.548 | 0.203 | 0.612 |
| N7_ar_p4n | 200 | 160000 | 0.545 | 0.462 | 0.178 | 0.516 |
| N7_ar_p15 | 50 | 160000 | 1.002 | 0.895 | 0.485 | 0.939 |
| N7_ar_p15 | 100 | 160000 | 0.699 | 0.595 | 0.216 | 0.658 |
| N7_ar_p15 | 200 | 160000 | 0.542 | 0.437 | 0.172 | 0.491 |
| N7_t25_p4n | 50 | 160000 | 0.951 | 0.803 | 0.465 | 0.899 |
| N7_t25_p4n | 100 | 160000 | 0.848 | 0.654 | 0.237 | 0.774 |
| N7_t25_p4n | 200 | 160000 | 0.638 | 0.517 | 0.195 | 0.574 |
| N7_t25_p15 | 50 | 160000 | 0.970 | 0.894 | 0.416 | 0.913 |
| N7_t25_p15 | 100 | 160000 | 0.717 | 0.584 | 0.217 | 0.660 |
| N7_t25_p15 | 200 | 160000 | 0.670 | 0.580 | 0.193 | 0.645 |

Overall per design (all n pooled): N1: max 0.835, q.999 0.690; N2a_t25: max 1.004, q.999 0.738; N2b_pareto: max 0.922, q.999 0.653; N2c_spike: max 0.251, q.999 0.218; N3: max 0.826, q.999 0.549; N4_tau2=n-2: max 0.842, q.999 0.725; N4_tau2=n-1: max 0.962, q.999 0.644; N4_tau2=logn_n: max 0.872, q.999 0.738; N4_tau2=1: max 0.937, q.999 0.631; N5: max 0.993, q.999 0.604; N7_ar_p4n: max 0.994, q.999 0.762; N7_ar_p15: max 1.002, q.999 0.852; N7_t25_p4n: max 0.951, q.999 0.766; N7_t25_p15: max 0.970, q.999 0.871

## Final table

Rule: 'bounded' = log–log slope of the statistic against n is below 0.15 (growth slower than n^0.15; log n alone would give about 0.3–0.4 over n=50…800), 'unclear' 0.15–0.30, 'no' above 0.30. 'n·d² bounded' is read on the median and q99. Tail slope: ĉ at the largest n (and median over n).  

| design | n·d²/log n bounded? (q99 slope) | n·d² bounded? (med slope / q99 slope) | n·d² med at largest n | n·d² q99 at smallest→largest n | tail rate c_t (log P(n d²>t) ≈ −c_t t), per n |
|---|---|---|---|---|---|
| N1 | yes (-0.36) | yes (-0.17 / -0.17) | 1.12 | 5.46 → 3.24 | c_t by n: 50:1.02, 100:1.20, 200:1.37, 400:1.59, 800:1.64 |
| N2a_t25 | yes (-0.31) | yes (-0.12 / -0.12) | 1.26 | 4.88 → 3.53 | c_t by n: 50:1.04, 100:0.90, 200:1.25, 400:1.44, 800:1.19 |
| N2b_pareto | yes (-0.34) | yes (-0.27 / -0.15) | 1.19 | 4.94 → 3.43 | c_t by n: 50:1.42, 100:1.16, 200:1.12, 400:1.57, 800:1.61 |
| N2c_spike | yes (-0.14) | yes (0.15 / 0.05) | 0.39 | 1.45 → 1.63 | c_t by n: 50:2.39, 100:1.93, 200:2.97, 400:2.48, 800:2.52 |
| N3 | yes (-0.21) | yes (0.04 / -0.01) | 1.42 | 3.50 → 3.26 | c_t by n: 50:1.37, 100:1.87, 200:1.29, 400:1.67, 800:1.73 |
| N4_tau2=n-2 | yes (-0.26) | yes (-0.03 / -0.07) | 1.22 | 4.35 → 3.37 | c_t by n: 50:0.88, 100:1.67, 200:1.45, 400:1.55, 800:1.43 |
| N4_tau2=n-1 | yes (-0.29) | yes (-0.08 / -0.10) | 1.16 | 4.65 → 3.29 | c_t by n: 50:1.22, 100:1.37, 200:1.26, 400:1.42, 800:1.61 |
| N4_tau2=logn_n | yes (-0.30) | yes (-0.08 / -0.11) | 1.46 | 5.14 → 3.53 | c_t by n: 50:1.10, 100:1.35, 200:1.69, 400:1.51, 800:1.62 |
| N4_tau2=1 | yes (-0.35) | yes (-0.18 / -0.16) | 1.14 | 5.38 → 3.34 | c_t by n: 50:1.11, 100:1.31, 200:1.44, 400:1.39, 800:1.62 |
| N5 | yes (-0.05) | unclear (0.22 / 0.15) | 3.26 | 3.86 → 5.84 | c_t by n: 50:1.24, 100:1.31, 200:1.35, 400:1.28, 800:1.16 |
| N7_ar_p4n | yes (-0.87) | yes (-0.92 / -0.65) | 1.09 | 8.23 → 3.36 | c_t by n: 50:0.66, 100:0.69, 200:1.22 |
| N7_ar_p15 | yes (-0.91) | yes (-1.14 / -0.69) | 1.02 | 8.43 → 3.24 | c_t by n: 50:0.79, 100:0.60, 200:1.36 |
| N7_t25_p4n | yes (-0.74) | yes (-0.88 / -0.52) | 1.14 | 7.01 → 3.40 | c_t by n: 50:0.79, 100:0.56, 200:1.49 |
| N7_t25_p15 | yes (-0.78) | yes (-0.92 / -0.57) | 1.09 | 7.35 → 3.35 | c_t by n: 50:0.77, 100:0.20, 200:1.37 |