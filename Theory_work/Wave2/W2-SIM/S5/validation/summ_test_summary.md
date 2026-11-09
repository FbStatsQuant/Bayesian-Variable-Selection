# E-S5CC summary (W2-SIM family S5)

source: `summ_test.jsonl` (6 rows); task tables: summ_test_tasks.tsv (7 tasks)

Integrity: 0 duplicate/unknown/rng problems; 1 missing tasks: summ_test_tasks.tsv task 7.

## Deletion path (Pi of s3_cc.py) and competing moves (recorded, never acted on)

deletion_path_complete = the deletion-only path reached S0 (= original field reached_S0); it is NOT a certification
of the LS0 path: additions are checked at every step, candidate swaps (bcs_core Path._swaps) only at checkpoints.

| design | p | n | runs | complete | incomplete (seed: reason, m_final) | max (add-del)/log n bulk / mid / end | steps add>=del | steps add>0 | max (swap-del)/log n bulk / mid / end | steps swap>=del (checked steps) | terminal improvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 2 | 2 | - | -1.000 / -1.091 / -1.074 | 0 | 0 | -0.500 / -0.546 / -0.547 | 0 (598) | 0/2 |
| S5(5,.3,.7) | 500 | 1e+20 | 2 | 2 | - | -1.000 / -1.055 / -1.044 | 0 | 0 | -0.500 / -0.527 / -0.528 | 0 (598) | 0/2 |
| S5(5,.3,.7) | 1000 | 1e+12 | 2 | 2 | - | -1.000 / -0.983 / -0.948 | 0 | 0 | -0.500 / -0.487 / -0.463 | 0 (800) | 0/2 |

## Centre condition CC_n(delta): admissible delta = min over visited T of 1 - (H_q + kappa0 max|e|)^2 / Lambda_k

Baseline = the same with e = 0 (deterministic). A negative baseline means CC_n(delta) fails at this finite (p, n) for
every delta >= 0 whatever e is (H_q^2 > Lambda_k): such cells cannot diagnose the global error; this is a finite-n
statement and does not bear on the asymptotic Lemma KL.

| design | p | n | baseline (e=0) | delta_adm mean / min | argmin m (median) | loss to e: mean (baseline - delta_adm) | pass rate delta >= 0 / 0.1 / 0.25 |
|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 0.0589 | 0.0408 / 0.0389 | 496 | 0.0182 | 1.00 / 0.00 / 0.00 |
| S5(5,.3,.7) | 500 | 1e+20 | 0.4132 | 0.3841 / 0.3711 | 4 | 0.0291 | 1.00 / 1.00 / 1.00 |
| S5(5,.3,.7) | 1000 | 1e+12 | 0.0088 | -0.0125 / -0.0264 | 996 | 0.0213 | 0.50 / 0.00 / 0.00 |

## Global error in units of H = sqrt(2 log 2p): r = kappa0 max(|e_T|, max_j |e_{T minus j}|)/H, rT = centre only
(per-run maxima over the phase; mean over runs that visited the phase [95% bootstrap CI], N = # such runs)

| design | p | n | N | r_bulk mean [CI] | r_bulk median / q90 / max | frac r_bulk >= 0.03 | argmax m <= 35 | rT_bulk mean / max | r_mid mean / max (N) | r_end mean / max (N) | rT_end mean / max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 2 | 0.0547 [0.0438, 0.0656] | 0.0547 / 0.0634 / 0.0656 | 1.00 | 0.50 | 0.0340 / 0.0424 | 0.153 / 0.162 (2) | 0.174 / 0.190 (2) | 0.105 / 0.142 |
| S5(5,.3,.7) | 500 | 1e+20 | 2 | 0.0547 [0.0438, 0.0656] | 0.0547 / 0.0634 / 0.0656 | 1.00 | 0.50 | 0.0340 / 0.0424 | 0.153 / 0.162 (2) | 0.174 / 0.190 (2) | 0.105 / 0.142 |
| S5(5,.3,.7) | 1000 | 1e+12 | 2 | 0.0598 [0.0594, 0.0603] | 0.0598 / 0.0602 / 0.0603 | 1.00 | 0.50 | 0.0414 / 0.0457 | 0.140 / 0.141 (2) | 0.161 / 0.166 (2) | 0.120 / 0.143 |

## Bulk proper: max r over m >= p/10 and over m >= sqrt(p)

| design | p | n | r(m>=p/10) mean [95% CI] / max (N) | r(m>=sqrt p) mean [95% CI] / max (N) |
|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 0.0442 [0.0378, 0.0505] / 0.0505 (2) | 0.0677 [0.0672, 0.0682] / 0.0682 (2) |
| S5(5,.3,.7) | 500 | 1e+20 | 0.0442 [0.0378, 0.0505] / 0.0505 (2) | 0.0677 [0.0672, 0.0682] / 0.0682 (2) |
| S5(5,.3,.7) | 1000 | 1e+12 | 0.0401 [0.0391, 0.0411] / 0.0411 (2) | 0.0588 [0.0582, 0.0594] / 0.0594 (2) |

## r at fixed m (single visited state; mean over runs that visited m: r | centre-only rT)

| design | p | n | m=30 | m=50 | m=100 | m=200 | m=500 |
|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 0.0500 / 0.0241 | 0.0357 / 0.0185 | 0.0245 / 0.0142 | 0.0191 / 0.0139 | - |
| S5(5,.3,.7) | 500 | 1e+20 | 0.0500 / 0.0241 | 0.0357 / 0.0185 | 0.0245 / 0.0142 | 0.0191 / 0.0139 | - |
| S5(5,.3,.7) | 1000 | 1e+12 | 0.0375 / 0.0107 | 0.0359 / 0.0189 | 0.0303 / 0.0207 | 0.0177 / 0.0131 | 0.0137 / 0.0112 |

## Bulk r by m-band (mean over runs of the per-run band maximum; '-' = band not visited)

| design | p | n | [30,100) | [100,300) | [300,1000) | [1000,3000) | [3000,10000) | [10000,30000) | [30000,100000) | [100000,inf) |
|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 0.0547 | 0.0330 | 0.0171 | - | - | - | - | - |
| S5(5,.3,.7) | 500 | 1e+20 | 0.0547 | 0.0330 | 0.0171 | - | - | - | - | - |
| S5(5,.3,.7) | 1000 | 1e+12 | 0.0598 | 0.0401 | 0.0175 | - | - | - | - | - |

## End-phase imbalance I(m) = #(tau>0) - #(tau<0) over retained nulls (tau = deletion statistic tau_{j|T\j})

N = runs that visited m <= 5. E1 (primary) = excursion |I| >= 2 at some m <= 5; E2 = re-entry (|I| >= 2 at m <= 5 after
|I| <= 1 at some m' in (m, 30]); E3 = |I| >= 2 at >= 2 of m in {5,..,1}. Wilson 95% intervals.

| design | p | n | N | I30 dist | I10 dist | I5 dist | #|I|>=2 at m = 30/10/5/4/3/2/1 | E1 [95%] | E2 [95%] | E3 [95%] |
|---|---|---|---|---|---|---|---|---|---|---|
| S5(5,.3,.7) | 500 | 1e+12 | 2 | {'0': 1, '2': 1} | {'0': 2} | {'1': 2} | 1 / 0 / 0 / 0 / 0 / 1 / 0 | 1/2 [0.09, 0.91] | 1/2 [0.09, 0.91] | 0/2 [0.00, 0.66] |
| S5(5,.3,.7) | 500 | 1e+20 | 2 | {'0': 1, '2': 1} | {'0': 2} | {'1': 2} | 1 / 0 / 0 / 0 / 0 / 1 / 0 | 1/2 [0.09, 0.91] | 1/2 [0.09, 0.91] | 0/2 [0.00, 0.66] |
| S5(5,.3,.7) | 1000 | 1e+12 | 2 | {'0': 2} | {'0': 2} | {'-1': 2} | 0 / 0 / 0 / 0 / 0 / 0 / 0 | 0/2 [0.00, 0.66] | 0/2 [0.00, 0.66] | 0/2 [0.00, 0.66] |

## Scaling with p: slope of log(mean statistic) on log p (complete paths only; OLS over p; 95% bootstrap CI, seeds
resampled within p; 'descriptive' when a contributing cell has < 2 runs)

| design | n | statistic | p values (runs) | slope [95% CI] |
|---|---|---|---|---|
| S5(5,.3,.7) | 1e+12 | r_bulk | 500(2),1000(2) | 0.130 [-0.144, 0.463] |
| S5(5,.3,.7) | 1e+12 | r_mid | 500(2),1000(2) | -0.125 [-0.218, -0.028] |
| S5(5,.3,.7) | 1e+12 | r_end | 500(2),1000(2) | -0.108 [-0.286, 0.082] |
| S5(5,.3,.7) | 1e+12 | rT_bulk | 500(2),1000(2) | 0.286 [-0.193, 0.843] |
| S5(5,.3,.7) | 1e+12 | rT_mid | 500(2),1000(2) | -0.348 [-0.792, 0.077] |
| S5(5,.3,.7) | 1e+12 | rT_end | 500(2),1000(2) | 0.194 [-0.553, 1.080] |
| S5(5,.3,.7) | 1e+12 | r_m_ge_p10 | 500(2),1000(2) | -0.139 [-0.370, 0.123] |
| S5(5,.3,.7) | 1e+12 | r_m_ge_sqrtp | 500(2),1000(2) | -0.204 [-0.229, -0.179] |
| S5(5,.3,.7) | 1e+12 | band[30,..) | 500(2),1000(2) | 0.130 [-0.144, 0.463] |
| S5(5,.3,.7) | 1e+12 | band[100,..) | 500(2),1000(2) | 0.283 [0.082, 0.504] |
| S5(5,.3,.7) | 1e+12 | band[300,..) | 500(2),1000(2) | 0.033 [-1.119, 0.802] |
| S5(5,.3,.7) | 1e+12 | r@m=30 | 500(2),1000(2) | -0.416 [-0.967, 0.185] |
| S5(5,.3,.7) | 1e+12 | r@m=100 | 500(2),1000(2) | 0.307 [0.028, 0.589] |

## n-pairing check (same rng stream at n = 1e12 and 1e20; e_T itself does not depend on n)

* S5(5,.3,.7) p=500: identical deletion sequence 2/2, identical all e-statistics 2/2; unpaired seeds none; differing fields none.
