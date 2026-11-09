# E-S5CC summary (W2-SIM family S5)

source: `results/FAC-S5_CC/pilot01/cc_pilot.jsonl` (3 runs)

Units: r = kappa0 * max(|e_T|, max_j |e_{T minus j}|) / H with H = sqrt(2 log 2p); rT = centre only (kappa0 |e_T| / H);
m = number of retained nulls. cc_* = original s3_cc.py fields (units H_q). I(m) = #(tau>0) - #(tau<0) over retained nulls.

## Path and original fields

| design | p | n | runs | reached_S0 | steps (mode) | cc_max mean / max | cc_max_at_m (median) | cc_bulk_m30 mean / max | CCdelta margin/log n (min) |
|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 2000 | 1e+12 | 1 | 1/1 | 1996 | 0.159 / 0.159 | 2 | 0.0287 / 0.0287 | -0.048 |
| S5(5,.3,.7) | 10000 | 1e+12 | 1 | 1/1 | 9996 | 0.207 / 0.207 | 1 | 0.0296 / 0.0296 | -0.161 |
| S5(5,.3,.7) | 10000 | 1e+20 | 1 | 1/1 | 9996 | 0.204 / 0.204 | 1 | 0.0292 / 0.0292 | 0.281 |

## Global error in units of H (r) by phase

| design | p | n | r_bulk mean [95% CI] | r_bulk median / q90 / max | frac r_bulk >= 0.03 | argmax m <= 35 (frac) | rT_bulk mean / max | r_mid mean / max | r_end mean / max | rT_end mean / max |
|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 2000 | 1e+12 | 0.0378 [nan, nan] | 0.0378 / 0.0378 / 0.0378 | 1.00 | 1.00 | 0.0155 / 0.0155 | 0.114 / 0.114 | 0.210 / 0.210 | 0.103 / 0.103 |
| S5(5,.3,.7) | 10000 | 1e+12 | 0.0377 [nan, nan] | 0.0377 / 0.0377 / 0.0377 | 1.00 | 1.00 | 0.0239 / 0.0239 | 0.173 / 0.173 | 0.263 / 0.263 | 0.263 / 0.263 |
| S5(5,.3,.7) | 10000 | 1e+20 | 0.0377 [nan, nan] | 0.0377 / 0.0377 / 0.0377 | 1.00 | 1.00 | 0.0239 / 0.0239 | 0.173 / 0.173 | 0.263 / 0.263 | 0.263 / 0.263 |

## Bulk r by m-band (mean over runs of the per-run band maximum; '-' = band not visited)

| design | p | n | [30,100) | [100,300) | [300,1000) | [1000,3000) | [3000,10000) | [10000,30000) | [30000,100000) | [100000,inf) |
|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 2000 | 1e+12 | 0.0378 | 0.0165 | 0.0084 | 0.0053 | - | - | - | - |
| S5(5,.3,.7) | 10000 | 1e+12 | 0.0377 | 0.0174 | 0.0097 | 0.0083 | 0.0030 | - | - | - |
| S5(5,.3,.7) | 10000 | 1e+20 | 0.0377 | 0.0174 | 0.0097 | 0.0083 | 0.0030 | - | - | - |

## End-phase imbalance I(m) = #(tau>0) - #(tau<0) over retained nulls

| design | p | n | I30 dist | I10 dist | I5 dist | #|I|>=2 at m=30 / 10 / 5 / 4 / 3 / 2 | runs with max_{m<=5}|I| >= 2 [Wilson 95%] |
|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 2000 | 1e+12 | {'-2': 1} | {'-2': 1} | {'-1': 1} | 1/1 / 1/1 / 0/1 / 0/1 / 0/1 / 0/1 | 0/1 [0.00, 0.79] |
| S5(5,.3,.7) | 10000 | 1e+12 | {'-2': 1} | {'-2': 1} | {'-1': 1} | 1/1 / 1/1 / 0/1 / 1/1 / 0/1 / 1/1 | 1/1 [0.21, 1.00] |
| S5(5,.3,.7) | 10000 | 1e+20 | {'-2': 1} | {'-2': 1} | {'-1': 1} | 1/1 / 1/1 / 0/1 / 1/1 / 0/1 / 1/1 | 1/1 [0.21, 1.00] |

## Scaling with p: slope of log(mean statistic) on log p (OLS over p; 95% bootstrap CI, seeds resampled within p)

| design | n | statistic | p values | slope [95% CI] |
|---|---|---|---|---|
| S5(5,.3,.7) | 1e+12 | r_bulk | 2000,10000 | -0.002 [-0.002, -0.002] |
| S5(5,.3,.7) | 1e+12 | rT_bulk | 2000,10000 | 0.269 [0.269, 0.269] |
| S5(5,.3,.7) | 1e+12 | r_mid | 2000,10000 | 0.260 [0.260, 0.260] |
| S5(5,.3,.7) | 1e+12 | r_end | 2000,10000 | 0.141 [0.141, 0.141] |
| S5(5,.3,.7) | 1e+12 | band[30,..) | 2000,10000 | -0.002 [-0.002, -0.002] |
| S5(5,.3,.7) | 1e+12 | band[100,..) | 2000,10000 | 0.033 [0.033, 0.033] |
| S5(5,.3,.7) | 1e+12 | band[300,..) | 2000,10000 | 0.094 [0.094, 0.094] |
| S5(5,.3,.7) | 1e+12 | band[1000,..) | 2000,10000 | 0.276 [0.276, 0.276] |

## n-pairing check (same rng seed at n = 1e12 and 1e20)

* S5(5,.3,.7) p=10000: 1/1 seeds give identical e-statistics (r_bulk, r_end, end_trace) at n=1e+12 and n=1e+20.
