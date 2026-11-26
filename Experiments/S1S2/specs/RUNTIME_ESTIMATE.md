# Runtime estimate for the full S1/S2 grid (harness/runtime_estimate.R)

From `harness/smoke_table.tsv` (2026-11-25 23:16, 1 fit per (method, smoke combo)), 100 reps per setting, at most 16 single-threaded jobs on Owls.
Scaling (OURS): each setting takes the smoke runtime of the combo with the same (n, p[, s]); the smoke covers every (n, p) in the grid.
Not measured: the effect of SNR/ν/ρ/beta-type and of seed-to-seed variation. Band: ×0.5 (low) to ×3 (high) per fit.
Owls was shared during the smoke (load average 50–120 on 80 cores), so the timings include contention.

## Per fit (seconds, smoke)

| method | S1 500x500 | S1 500x5000 | S1 1000x500 | S1 1000x5000 | S2 50x1000 s5 | S2 100x1000 s10 |
|---|---|---|---|---|---|---|
| asi |  79.7 | 315.9 | 100.7 | 244.5 |  88.4 |  91.2 |
| bas_mc3 |  9.8 | 41.9 |  7.6 | 43.1 | 16.3 |  6.2 |
| lasso_cv | 1.4 | 3.3 | 2.2 | 8.3 | 0.3 | 0.5 |
| scad |  6.0 |  7.5 | 47.4 | 47.0 |  0.6 |  1.7 |
| smcbvs |    298.8 | 18,647.3 |    214.8 | 11,215.0 |    752.1 |     40.4 |
| susie |  1.2 | 17.9 |  2.2 | 27.7 |  1.5 |  1.6 |

## Full grid

| method | fits | core-h (central) | low | high | wall at 16 jobs (days, central) |
|---|---|---|---|---|---|
| asi | 13,600 | pending | pending | pending | pending |
| bas_mc3 | 13,600 | 48.9 | 24.4 | 146.6 | 0.13 |
| lasso_cv | 13,600 | 3 | 1.5 | 9.1 | 0.01 |
| scad | 13,600 | 15.8 | 7.9 | 47.5 | 0.04 |
| smcbvs | 13,600 | 4,695.9 | 2,348 | 14,087.8 | 12.23 |
| susie | 13,600 | 10.6 | 5.3 | 31.8 | 0.03 |
| **all (excl. asi)** | 68,000 | **4,774.3** | 2,387.1 | 14,322.8 | **12.4** |

## By (n, p) class, all methods except asi (core-h, central)

| class | settings | core-h |
|---|---|---|
| S1 1000x500 | 4 | 30.5 |
| S1 1000x5000 | 4 | 1,260.1 |
| S1 500x500 | 4 | 35.2 |
| S1 500x5000 | 4 | 2,079.8 |
| S2 100x1000 s10 | 60 | 84 |
| S2 50x1000 s5 | 60 | 1,284.7 |
