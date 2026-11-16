
### Item 1, n = 100: distribution over R = 200 data sets of Π(n·d² > t | D)   (1000000 posterior draws per data set; d² exact given the draw)
Resolution per data set: 1/1000000 = 1e-06.  log n = 4.61; 2 log n = 9.21; 3 log n = 13.82.  `frac>0` = share of data sets with at least one exceeding draw.

| t | q0.5 | q0.9 | q0.99 | max | mean (=pooled) | frac>0 | #sets with Π>0.01 | #sets with Π>0.05 |
|---|---|---|---|---|---|---|---|---|
| 1 | 5.60e-01 | 8.84e-01 | 1.00e+00 | 1.00e+00 | 5.75e-01 | 1.000 | 200 | 200 |
| 2 | 1.37e-01 | 4.70e-01 | 8.66e-01 | 9.68e-01 | 2.02e-01 | 1.000 | 199 | 167 |
| 3 | 2.34e-02 | 1.50e-01 | 5.38e-01 | 8.63e-01 | 6.47e-02 | 1.000 | 136 | 60 |
| 4 | 3.42e-03 | 3.84e-02 | 2.95e-01 | 6.63e-01 | 2.12e-02 | 1.000 | 56 | 16 |
| 4.5  (≈ log n) | 1.22e-03 | 1.74e-02 | 1.99e-01 | 5.39e-01 | 1.26e-02 | 1.000 | 31 | 10 |
| 5 | 4.31e-04 | 8.93e-03 | 1.27e-01 | 4.13e-01 | 7.59e-03 | 1.000 | 19 | 5 |
| 6 | 6.10e-05 | 2.21e-03 | 4.37e-02 | 2.02e-01 | 2.87e-03 | 0.910 | 7 | 2 |
| 8 | 1.00e-06 | 8.01e-05 | 9.71e-03 | 3.35e-02 | 3.89e-04 | 0.535 | 2 | 0 |
| 9  (≈ 2 log n) | 0.00e+00 | 1.31e-05 | 3.75e-03 | 1.41e-02 | 1.32e-04 | 0.290 | 1 | 0 |
| 10 | 0.00e+00 | 2.00e-06 | 6.72e-04 | 5.46e-03 | 4.02e-05 | 0.185 | 0 | 0 |
| 12 | 0.00e+00 | 0.00e+00 | 2.01e-05 | 5.14e-04 | 2.97e-06 | 0.065 | 0 | 0 |
| 13.75  (≈ 3 log n) | 0.00e+00 | 0.00e+00 | 1.02e-06 | 2.80e-05 | 1.65e-07 | 0.020 | 0 | 0 |
| 16 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.000 | 0 | 0 |

Per-data-set posterior quantiles of n·d² (rows: posterior level; columns: distribution over data sets):

| posterior level | q0.5 | q0.9 | q0.99 | max over data sets |
|---|---|---|---|---|
| 0.5 | 1.09 | 1.93 | 3.15 | 4.65 |
| 0.9 | 2.19 | 3.30 | 5.24 | 6.75 |
| 0.99 | 3.44 | 4.82 | 7.93 | 9.37 |
| 0.999 | 4.59 | 6.50 | 9.82 | 11.51 |

Sample interface quantities: ‖μ‖²/n median 1.498 (max 2.207); ‖θ*‖²/n median 0.0303 (max 0.0389); π(S₀) median 0.714, min 0.092.

**DIST-1 form, empirical failure frequency** F(C²,c,t) = share of the 200 data sets with Π(n·d² > C²t | D) > e^{-ct}  vs the bound 3e^{-ct}  (tail read at the largest grid point ≤ C²t, i.e. conservative; `<res` means e^{-ct} is below the 1/1000000 resolution, so a single exceeding draw counts):

| (C², c) | t = log n | t = 2 log n | t = 3 log n |
|---|---|---|---|
| (1, 0.5) | 0.025 vs 3e^-ct=0.300 | 0.005 vs 3e^-ct=0.030 | 0.000 vs 3e^-ct=0.003 |
| (1, 1) | 0.155 vs 3e^-ct=0.030 | 0.045 vs 3e^-ct=0.000 | 0.020 vs 3e^-ct=0.000 <res |
| (2, 0.5) | 0.000 vs 3e^-ct=0.300 | 0.000 vs 3e^-ct=0.030 | 0.000 vs 3e^-ct=0.003 |
| (2, 1) | 0.005 vs 3e^-ct=0.030 | 0.000 vs 3e^-ct=0.000 | 0.000 vs 3e^-ct=0.000 <res |
| (3, 1) | 0.000 vs 3e^-ct=0.030 | 0.000 vs 3e^-ct=0.000 | n/a (beyond grid) |
| (4, 1) | 0.000 vs 3e^-ct=0.030 | 0.000 vs 3e^-ct=0.000 | n/a (beyond grid) |

### Item 6b, n = 100: π(|S| > m) on the same 200 exact enumerations (p = 12, K = 12, S₀ = {1,2,3}) vs the cutoff inequality of Lemma S
Cutoff m_n(t) of STATEMENT §0 at t = log n: 12; at t = 2 log n: 12; K = 12.  **m_n(t) = K for every t ≥ log n here, so the statement at m = m_n(t) is vacuous (π(|S| > K) = 0)**; the table below tests the *inequality* for every m < K instead, with the exact R^T_m, exact log D_S₀ and t* = the largest t ∈ [1, n^{1−κ₀}] (κ₀ = ½) with  log R_m + ½ log D_S₀ + ½ log n + C·[1+√t+t/√n] ≤ −2t  (C is an unspecified constant of the lemma; C ∈ {0, 1, 3}).

R^T_m (exact, |T| = 3): m=0:1.77e+03, m=1:847, m=2:385, m=3:165, m=4:66, m=5:24.3, m=6:8.11, m=7:2.38, m=8:0.596, m=9:0.119, m=10:0.017, m=11:0.00131, m=12:0
Check R_m ≤ 2(2p)^{s₀}2^{−m}: max ratio R_m / bound over m ≤ 11 = 0.0641 (≤ 1 ⇒ holds).  Check D_S₀ ≤ (n+1)^{s₀}: max over data sets of log D_S₀ − 3 log(n+1) = -0.036 (≤ 0 ⇒ holds); log D_S₀ range [13.79, 13.81].


**C = 0**

| m | log R_m + ½log D_S₀ + ½log n (median over sets) | t*(m) median | π(|S|>m) median | π(|S|>m) max | e^{-t*} median | #sets with π(|S|>m) > e^{-t*} | smallest e^{-t*} over sets for which t* ≥ 1 |
|---|---|---|---|---|---|---|---|
| 0 | 16.68 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 1 | 15.95 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 2 | 15.16 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 3 | 14.31 | inequality fails at t = 1 for all sets | 0.286 | 0.903 | – | – | – |
| 4 | 13.39 | inequality fails at t = 1 for all sets | 0.0507 | 0.632 | – | – | – |
| 5 | 12.39 | inequality fails at t = 1 for all sets | 0.00674 | 0.237 | – | – | – |
| 6 | 11.30 | inequality fails at t = 1 for all sets | 0.000676 | 0.0606 | – | – | – |
| 7 | 10.07 | inequality fails at t = 1 for all sets | 5.2e-05 | 0.011 | – | – | – |
| 8 | 8.69 | inequality fails at t = 1 for all sets | 3.21e-06 | 0.00143 | – | – | – |
| 9 | 7.08 | inequality fails at t = 1 for all sets | 1.52e-07 | 0.000125 | – | – | – |
| 10 | 5.13 | inequality fails at t = 1 for all sets | 4.78e-09 | 6.71e-06 | – | – | – |
| 11 | 2.57 | inequality fails at t = 1 for all sets | 7.51e-11 | 1.7e-07 | – | – | – |

(C = 1 and C = 3 give the same verdict: the inequality fails at t = 1 for every m ≤ 11 because its left side is positive; only m = 12 = K, where R_12 = 0, satisfies it.)

**Unclamped cutoff m_n(t) of STATEMENT §0 versus the empirical size tail** (exact π(|S| > m)): m_emp(t) := min{m : π(|S| > m) ≤ e^{-t}} per data set; distribution over the 200 data sets.

| t | unclamped m_n(t) (before min with K) | m_emp(t) q0.5 | q0.9 | q0.99 | max |
|---|---|---|---|---|---|
| 1.00 | 38 | 3 | 4 | 5 | 5 |
| 4.61 | 54 | 5 | 6 | 7 | 8 |
| 9.21 | 74 | 7 | 8 | 9 | 10 |
| 13.82 | 94 | 9 | 10 | 11 | 11 |
| 23.03 | 134 | 11 | 12 | 12 | 12 |
(m_emp = 13 would mean π(|S| > 12) = 0 > e^{-t} is impossible, so it never occurs; the formula's m_n(t) exceeds K = 12 and therefore the statement at m = m_n(t) holds trivially in this p = 12 setting.)

### Item 1, n = 400: distribution over R = 200 data sets of Π(n·d² > t | D)   (1000000 posterior draws per data set; d² exact given the draw)
Resolution per data set: 1/1000000 = 1e-06.  log n = 5.99; 2 log n = 11.98; 3 log n = 17.97.  `frac>0` = share of data sets with at least one exceeding draw.

| t | q0.5 | q0.9 | q0.99 | max | mean (=pooled) | frac>0 | #sets with Π>0.01 | #sets with Π>0.05 |
|---|---|---|---|---|---|---|---|---|
| 1 | 4.92e-01 | 8.43e-01 | 9.91e-01 | 9.96e-01 | 5.26e-01 | 1.000 | 200 | 200 |
| 2 | 1.04e-01 | 4.33e-01 | 7.27e-01 | 8.27e-01 | 1.64e-01 | 1.000 | 199 | 145 |
| 3 | 1.50e-02 | 1.32e-01 | 4.05e-01 | 4.69e-01 | 4.61e-02 | 1.000 | 118 | 48 |
| 4 | 1.64e-03 | 3.00e-02 | 1.71e-01 | 1.77e-01 | 1.20e-02 | 1.000 | 43 | 12 |
| 5 | 1.76e-04 | 5.71e-03 | 4.82e-02 | 6.57e-02 | 2.85e-03 | 1.000 | 14 | 2 |
| 5.75  (≈ log n) | 2.60e-05 | 1.61e-03 | 1.77e-02 | 2.88e-02 | 9.03e-04 | 0.905 | 6 | 0 |
| 6 | 1.55e-05 | 9.63e-04 | 1.26e-02 | 2.16e-02 | 6.08e-04 | 0.850 | 4 | 0 |
| 8 | 0.00e+00 | 1.81e-05 | 4.49e-04 | 1.52e-03 | 2.19e-05 | 0.355 | 0 | 0 |
| 10 | 0.00e+00 | 1.00e-07 | 7.05e-06 | 5.20e-05 | 5.05e-07 | 0.100 | 0 | 0 |
| 11.75  (≈ 2 log n) | 0.00e+00 | 0.00e+00 | 0.00e+00 | 1.00e-06 | 5.00e-09 | 0.005 | 0 | 0 |
| 12 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 1.00e-06 | 5.00e-09 | 0.005 | 0 | 0 |
| 16 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.000 | 0 | 0 |
| 17.75  (≈ 3 log n) | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.00e+00 | 0.000 | 0 | 0 |

Per-data-set posterior quantiles of n·d² (rows: posterior level; columns: distribution over data sets):

| posterior level | q0.5 | q0.9 | q0.99 | max over data sets |
|---|---|---|---|---|
| 0.5 | 0.99 | 1.85 | 2.67 | 2.92 |
| 0.9 | 2.02 | 3.22 | 4.46 | 4.58 |
| 0.99 | 3.19 | 4.69 | 6.16 | 6.61 |
| 0.999 | 4.23 | 5.99 | 7.56 | 8.27 |

Sample interface quantities: ‖μ‖²/n median 1.492 (max 1.852); ‖θ*‖²/n median 0.0075 (max 0.0083); π(S₀) median 0.850, min 0.172.

**DIST-1 form, empirical failure frequency** F(C²,c,t) = share of the 200 data sets with Π(n·d² > C²t | D) > e^{-ct}  vs the bound 3e^{-ct}  (tail read at the largest grid point ≤ C²t, i.e. conservative; `<res` means e^{-ct} is below the 1/1000000 resolution, so a single exceeding draw counts):

| (C², c) | t = log n | t = 2 log n | t = 3 log n |
|---|---|---|---|
| (1, 0.5) | 0.000 vs 3e^-ct=0.150 | 0.000 vs 3e^-ct=0.008 | 0.000 vs 3e^-ct=0.000 |
| (1, 1) | 0.075 vs 3e^-ct=0.008 | 0.000 vs 3e^-ct=0.000 | 0.000 vs 3e^-ct=0.000 <res |
| (2, 0.5) | 0.000 vs 3e^-ct=0.150 | 0.000 vs 3e^-ct=0.008 | 0.000 vs 3e^-ct=0.000 |
| (2, 1) | 0.000 vs 3e^-ct=0.008 | 0.000 vs 3e^-ct=0.000 | 0.000 vs 3e^-ct=0.000 <res |
| (3, 1) | 0.000 vs 3e^-ct=0.008 | 0.000 vs 3e^-ct=0.000 | n/a (beyond grid) |
| (4, 1) | 0.000 vs 3e^-ct=0.008 | n/a (beyond grid) | n/a (beyond grid) |

### Item 6b, n = 400: π(|S| > m) on the same 200 exact enumerations (p = 12, K = 12, S₀ = {1,2,3}) vs the cutoff inequality of Lemma S
Cutoff m_n(t) of STATEMENT §0 at t = log n: 12; at t = 2 log n: 12; K = 12.  **m_n(t) = K for every t ≥ log n here, so the statement at m = m_n(t) is vacuous (π(|S| > K) = 0)**; the table below tests the *inequality* for every m < K instead, with the exact R^T_m, exact log D_S₀ and t* = the largest t ∈ [1, n^{1−κ₀}] (κ₀ = ½) with  log R_m + ½ log D_S₀ + ½ log n + C·[1+√t+t/√n] ≤ −2t  (C is an unspecified constant of the lemma; C ∈ {0, 1, 3}).

R^T_m (exact, |T| = 3): m=0:1.77e+03, m=1:847, m=2:385, m=3:165, m=4:66, m=5:24.3, m=6:8.11, m=7:2.38, m=8:0.596, m=9:0.119, m=10:0.017, m=11:0.00131, m=12:0
Check R_m ≤ 2(2p)^{s₀}2^{−m}: max ratio R_m / bound over m ≤ 11 = 0.0641 (≤ 1 ⇒ holds).  Check D_S₀ ≤ (n+1)^{s₀}: max over data sets of log D_S₀ − 3 log(n+1) = -0.009 (≤ 0 ⇒ holds); log D_S₀ range [17.97, 17.97].


**C = 0**

| m | log R_m + ½log D_S₀ + ½log n (median over sets) | t*(m) median | π(|S|>m) median | π(|S|>m) max | e^{-t*} median | #sets with π(|S|>m) > e^{-t*} | smallest e^{-t*} over sets for which t* ≥ 1 |
|---|---|---|---|---|---|---|---|
| 0 | 19.46 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 1 | 18.72 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 2 | 17.93 | inequality fails at t = 1 for all sets | 1 | 1 | – | – | – |
| 3 | 17.09 | inequality fails at t = 1 for all sets | 0.15 | 0.828 | – | – | – |
| 4 | 16.17 | inequality fails at t = 1 for all sets | 0.0132 | 0.365 | – | – | – |
| 5 | 15.17 | inequality fails at t = 1 for all sets | 0.000827 | 0.0642 | – | – | – |
| 6 | 14.07 | inequality fails at t = 1 for all sets | 3.91e-05 | 0.0104 | – | – | – |
| 7 | 12.85 | inequality fails at t = 1 for all sets | 1.46e-06 | 0.00123 | – | – | – |
| 8 | 11.46 | inequality fails at t = 1 for all sets | 4.42e-08 | 8.89e-05 | – | – | – |
| 9 | 9.85 | inequality fails at t = 1 for all sets | 1.03e-09 | 3.89e-06 | – | – | – |
| 10 | 7.91 | inequality fails at t = 1 for all sets | 1.6e-11 | 9.91e-08 | – | – | – |
| 11 | 5.34 | inequality fails at t = 1 for all sets | 1.23e-13 | 1.16e-09 | – | – | – |

(C = 1 and C = 3 give the same verdict: the inequality fails at t = 1 for every m ≤ 11 because its left side is positive; only m = 12 = K, where R_12 = 0, satisfies it.)

**Unclamped cutoff m_n(t) of STATEMENT §0 versus the empirical size tail** (exact π(|S| > m)): m_emp(t) := min{m : π(|S| > m) ≤ e^{-t}} per data set; distribution over the 200 data sets.

| t | unclamped m_n(t) (before min with K) | m_emp(t) q0.5 | q0.9 | q0.99 | max |
|---|---|---|---|---|---|
| 1.00 | 43 | 3 | 3 | 4 | 4 |
| 5.99 | 65 | 5 | 6 | 7 | 7 |
| 11.98 | 91 | 7 | 8 | 9 | 9 |
| 17.97 | 117 | 9 | 10 | 10 | 11 |
| 29.96 | 169 | 12 | 12 | 12 | 12 |
(m_emp = 13 would mean π(|S| > 12) = 0 > e^{-t} is impossible, so it never occurs; the formula's m_n(t) exceeds K = 12 and therefore the statement at m = m_n(t) holds trivially in this p = 12 setting.)