## S0. Inventory and identity (read from the eval / calib_meta records)
fits read: 170 (V/VF 155, A3/A3F 15); not completed: 0; recorded arm (N, m, I_max, I_used, rule): {(2500, 1, 0, 0, 'bounded'): 170}; binary sha256: {'d0c30b65103e': 170}

| design | n | fits | datasets | tags | s0 | engine seeds |
|---|---|---|---|---|---|---|
| AR-strong | 100 | 10 | 10 | V 10 | [5] | [1] |
| AR-strong | 200 | 20 | 10 | V 12,VF 8 | [5] | [1, 2] |
| AR-strong | 400 | 10 | 10 | V 10 | [5] | [1] |
| AR-strong | 800 | 10 | 10 | V 10 | [5] | [1] |
| AR-weak | 100 | 20 | 20 | V 20 | [5] | [1] |
| AR-weak | 200 | 20 | 20 | V 18,VF 2 | [5] | [1] |
| AR-weak | 400 | 10 | 10 | V 10 | [5] | [1] |
| AR-weak | 800 | 10 | 10 | V 10 | [5] | [1] |
| IND | 100 | 5 | 5 | V 5 | [5] | [1] |
| IND | 200 | 5 | 5 | V 4,VF 1 | [5] | [1] |
| IND | 400 | 5 | 5 | V 5 | [5] | [1] |
| BLK | 100 | 5 | 5 | V 5 | [5] | [1] |
| BLK | 200 | 5 | 5 | V 5 | [5] | [1] |
| BLK | 400 | 5 | 5 | V 5 | [5] | [1] |
| ADJ-OPP | 200 | 5 | 5 | V 3,VF 2 | [5] | [1] |
| ADJ-OPP | 400 | 5 | 5 | V 5 | [5] | [1] |
| NULL | 200 | 5 | 5 | V 4,VF 1 | [0] | [1] |

## S1. C2 reported model = S0 (per cell; dataset-clustered; NULL: S0 = empty)
| design | n | P(HPM = S0) | outcome classes (fits) | mean Hamming HPM | HPM TP / FP / FN (mean per fit) | P(MPM = S0) | MPM TP / FP (mean) | HPM phase (fits) |
|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.50 [0.24, 0.76] (5/10 fits; 10 ds) | correct 5, posterior 5 | 0.70 [2.1e-02, 1.38] | 4.30 / 0.00 / 0.70 | 0.60 [0.31, 0.83] (6/10 fits; 10 ds) | 4.40 / 0.00 | final_bridge 3, pilot 7 |
| AR-strong | 200 | 1.00 [0.72, 1.00] (20/20 fits; 10 ds) | correct 20 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (20/20 fits; 10 ds) | 5.00 / 0.00 | final_bridge 14, pilot 6 |
| AR-strong | 400 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | pilot 10 |
| AR-strong | 800 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | pilot 10 |
| AR-weak | 100 | 0.00 [0.00, 0.16] (0/20 fits; 20 ds) | posterior 20 | 4.55 [4.23, 4.87] | 0.45 / 0.00 / 4.55 | 0.00 [0.00, 0.16] (0/20 fits; 20 ds) | 0.65 / 0.00 | final_bridge 2, pilot 2, table 16 |
| AR-weak | 200 | 0.50 [0.30, 0.70] (10/20 fits; 20 ds) | correct 10, posterior 10 | 0.80 [0.35, 1.25] | 4.25 / 0.05 / 0.75 | 0.50 [0.30, 0.70] (10/20 fits; 20 ds) | 4.35 / 0.05 | final_bridge 8, pilot 12 |
| AR-weak | 400 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | correct 10 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.72, 1.00] (10/10 fits; 10 ds) | 5.00 / 0.00 | final_bridge 5, pilot 5 |
| AR-weak | 800 | 0.90 [0.60, 0.98] (9/10 fits; 10 ds) | correct 9, posterior 1 | 0.10 [-0.13, 0.33] | 5.00 / 0.10 / 0.00 | 0.90 [0.60, 0.98] (9/10 fits; 10 ds) | 5.00 / 0.10 | final_bridge 1, pilot 9 |
| IND | 100 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | correct 4, posterior 1 | 0.60 [-1.07, 2.27] | 4.60 / 0.20 / 0.40 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 4.80 / 0.20 | final_bridge 1, pilot 4 |
| IND | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 5 |
| IND | 400 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | correct 4, posterior 1 | 0.20 [-0.36, 0.76] | 5.00 / 0.20 / 0.00 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 5.00 / 0.20 | final_bridge 1, pilot 4 |
| BLK | 100 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 0.80 [0.38, 0.96] (4/5 fits; 5 ds) | 5.00 / 0.20 | final_bridge 2, pilot 3 |
| BLK | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 3, pilot 2 |
| BLK | 400 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | pilot 5 |
| ADJ-OPP | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | final_bridge 4, pilot 1 |
| ADJ-OPP | 400 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 5.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 5.00 / 0.00 | pilot 5 |
| NULL | 200 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | correct 5 | 0.00 [0.00, 0.00] | 0.00 / 0.00 / 0.00 | 1.00 [0.57, 1.00] (5/5 fits; 5 ds) | 0.00 / 0.00 | table 5 |

Fits whose HPM is not S0 (design, n, rep, seed, tag: |HPM|, TP, FP, FN, F(HPM) - F(S0), S0 in store, MPM = S0):
- AR-strong n100 r01 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +0.355, S0 in store True, MPM=S0 True, outcome posterior
- AR-strong n100 r02 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +2.580, S0 in store True, MPM=S0 False, outcome posterior
- AR-strong n100 r04 s1 V: |HPM| 2, TP 2, FP 0, FN 3, dF +2.905, S0 in store True, MPM=S0 False, outcome posterior
- AR-strong n100 r05 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +1.598, S0 in store True, MPM=S0 False, outcome posterior
- AR-strong n100 r10 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +6.714, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r01 s1 V: |HPM| 1, TP 1, FP 0, FN 4, dF +11.501, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r02 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +22.768, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r03 s1 V: |HPM| 1, TP 1, FP 0, FN 4, dF +22.043, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r04 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +6.490, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r05 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +21.321, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r06 s1 V: |HPM| 2, TP 2, FP 0, FN 3, dF +12.992, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r07 s1 V: |HPM| 1, TP 1, FP 0, FN 4, dF +5.566, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r08 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +25.930, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r09 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +37.258, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r10 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +25.411, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r11 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +24.908, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r12 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +6.567, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r13 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +21.627, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r14 s1 V: |HPM| 1, TP 1, FP 0, FN 4, dF +15.871, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r15 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +15.281, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r16 s1 V: |HPM| 2, TP 2, FP 0, FN 3, dF +8.782, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n100 r17 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +26.409, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r18 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +23.541, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r19 s1 V: |HPM| 1, TP 1, FP 0, FN 4, dF +18.956, S0 in store False, MPM=S0 False, outcome posterior
- AR-weak n100 r20 s1 V: |HPM| 0, TP 0, FP 0, FN 5, dF +16.033, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r01 s1 VF: |HPM| 4, TP 4, FP 0, FN 1, dF +5.485, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r02 s1 VF: |HPM| 3, TP 3, FP 0, FN 2, dF +5.839, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r03 s1 V: |HPM| 3, TP 3, FP 0, FN 2, dF +0.928, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r04 s1 V: |HPM| 2, TP 2, FP 0, FN 3, dF +8.129, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r06 s1 V: |HPM| 6, TP 5, FP 1, FN 0, dF +1.072, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r07 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +2.082, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r09 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +1.387, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r12 s1 V: |HPM| 4, TP 4, FP 0, FN 1, dF +0.306, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r14 s1 V: |HPM| 3, TP 3, FP 0, FN 2, dF +2.245, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n200 r18 s1 V: |HPM| 3, TP 3, FP 0, FN 2, dF +0.585, S0 in store True, MPM=S0 False, outcome posterior
- AR-weak n800 r01 s1 V: |HPM| 6, TP 5, FP 1, FN 0, dF +2.213, S0 in store True, MPM=S0 False, outcome posterior
- IND n100 r03 s1 V: |HPM| 4, TP 3, FP 1, FN 2, dF +6.090, S0 in store True, MPM=S0 False, outcome posterior
- IND n400 r01 s1 V: |HPM| 6, TP 5, FP 1, FN 0, dF +1.838, S0 in store True, MPM=S0 False, outcome posterior

## S2. C4 PIP consistency (per cell; mean over datasets [95% t interval]; equal-weight PIP = primary, PIP_Z beside it)
| design | n | sup null PIP (eq) | min PIP over S0 (eq) | sup null (Z) | min over S0 (Z) | Brier (eq) | #null PIP > 0.1 (mean per fit; fits with >= 1) | #null PIP > 0.5 (fits with >= 1) | max abs(PIP_Z - PIP_eq) (max) |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.172 [0.076, 0.267] | 0.561 [0.250, 0.872] | 0.172 [0.076, 0.268] | 0.561 [0.250, 0.872] | 5.813e-05 [6.706e-06, 1.095e-04] | 1.20; 6/10 | 0/10 | 3.4e-04 |
| AR-strong | 200 | 0.124 [0.032, 0.217] | 1.000 [1.000, 1.000] | 0.124 [0.032, 0.217] | 1.000 [1.000, 1.000] | 4.110e-06 [-8.717e-07, 9.092e-06] | 0.60; 8/20 | 0/20 | 2.8e-05 |
| AR-strong | 400 | 0.055 [0.021, 0.090] | 1.000 [1.000, 1.000] | 0.055 [0.021, 0.090] | 1.000 [1.000, 1.000] | 7.344e-07 [1.316e-07, 1.337e-06] | 0.20; 2/10 | 0/10 | 9.7e-06 |
| AR-strong | 800 | 0.050 [0.021, 0.080] | 1.000 [1.000, 1.000] | 0.050 [0.021, 0.080] | 1.000 [1.000, 1.000] | 4.831e-07 [2.255e-09, 9.639e-07] | 0.10; 1/10 | 0/10 | 2.6e-06 |
| AR-weak | 100 | 0.117 [0.059, 0.174] | 2.2e-03 [-2.3e-04, 4.6e-03] | 0.117 [0.059, 0.174] | 2.2e-03 [-2.3e-04, 4.6e-03] | 4.029e-04 [3.557e-04, 4.500e-04] | 0.40; 7/20 | 0/20 | 3.2e-04 |
| AR-weak | 200 | 0.151 [0.065, 0.237] | 0.560 [0.374, 0.745] | 0.151 [0.065, 0.237] | 0.560 [0.374, 0.745] | 5.834e-05 [2.452e-05, 9.215e-05] | 0.45; 8/20 | 1/20 | 3.0e-05 |
| AR-weak | 400 | 0.090 [3.6e-03, 0.177] | 0.966 [0.894, 1.038] | 0.090 [3.6e-03, 0.177] | 0.966 [0.894, 1.038] | 3.844e-06 [-6.309e-07, 8.318e-06] | 0.40; 3/10 | 0/10 | 2.9e-05 |
| AR-weak | 800 | 0.123 [-0.073, 0.319] | 1.000 [1.000, 1.000] | 0.123 [-0.073, 0.319] | 1.000 [1.000, 1.000] | 8.326e-06 [-9.807e-06, 2.646e-05] | 0.20; 2/10 | 1/10 | 6.2e-06 |
| IND | 100 | 0.302 [-0.103, 0.708] | 0.748 [0.221, 1.276] | 0.302 [-0.103, 0.708] | 0.748 [0.221, 1.276] | 4.690e-05 [-5.400e-05, 1.478e-04] | 1.00; 3/5 | 1/5 | 1.3e-04 |
| IND | 200 | 0.095 [-8.7e-03, 0.199] | 1.000 [1.000, 1.000] | 0.095 [-8.7e-03, 0.199] | 1.000 [1.000, 1.000] | 1.992e-06 [-1.349e-06, 5.332e-06] | 0.20; 1/5 | 0/5 | 1.4e-05 |
| IND | 400 | 0.307 [-0.119, 0.733] | 1.000 [1.000, 1.000] | 0.307 [-0.119, 0.733] | 1.000 [1.000, 1.000] | 1.902e-05 [-2.089e-05, 5.894e-05] | 0.60; 3/5 | 1/5 | 3.2e-06 |
| BLK | 100 | 0.159 [-0.084, 0.402] | 0.960 [0.918, 1.002] | 0.159 [-0.084, 0.402] | 0.960 [0.918, 1.002] | 1.117e-05 [-1.553e-05, 3.786e-05] | 1.00; 2/5 | 1/5 | 2.8e-04 |
| BLK | 200 | 0.034 [0.021, 0.048] | 1.000 [1.000, 1.000] | 0.034 [0.021, 0.048] | 1.000 [1.000, 1.000] | 4.287e-07 [1.209e-07, 7.366e-07] | 0.00; 0/5 | 0/5 | 4.0e-06 |
| BLK | 400 | 0.089 [0.013, 0.165] | 1.000 [1.000, 1.000] | 0.089 [0.013, 0.165] | 1.000 [1.000, 1.000] | 1.307e-06 [-3.149e-08, 2.645e-06] | 0.60; 3/5 | 0/5 | 5.8e-06 |
| ADJ-OPP | 200 | 0.131 [-0.064, 0.327] | 1.000 [0.999, 1.000] | 0.131 [-0.064, 0.327] | 1.000 [0.999, 1.000] | 4.306e-06 [-5.173e-06, 1.379e-05] | 0.40; 2/5 | 0/5 | 1.5e-04 |
| ADJ-OPP | 400 | 0.049 [0.015, 0.084] | 1.000 [1.000, 1.000] | 0.049 [0.015, 0.084] | 1.000 [1.000, 1.000] | 5.068e-07 [-1.150e-07, 1.129e-06] | 0.00; 0/5 | 0/5 | 5.2e-06 |
| NULL | 200 | 0.011 [6.8e-03, 0.015] | n/a (S0 empty) | 0.011 [6.8e-03, 0.015] | n/a | 2.739e-08 [2.583e-09, 5.219e-08] | 0.00; 0/5 | 0/5 | 6.6e-08 |

Active-variable detection (fits with min PIP over S0 > 0.5 / > 0.9, equal-weight), per cell:
- AR-strong n100: > 0.5 in 6/10 fits, > 0.9 in 4/10; median min PIP 0.701; fits with min PIP < 0.1: 2
- AR-strong n200: > 0.5 in 20/20 fits, > 0.9 in 20/20; median min PIP 1.000; fits with min PIP < 0.1: 0
- AR-strong n400: > 0.5 in 10/10 fits, > 0.9 in 10/10; median min PIP 1.000; fits with min PIP < 0.1: 0
- AR-strong n800: > 0.5 in 10/10 fits, > 0.9 in 10/10; median min PIP 1.000; fits with min PIP < 0.1: 0
- AR-weak n100: > 0.5 in 0/20 fits, > 0.9 in 0/20; median min PIP 0.000; fits with min PIP < 0.1: 20
- AR-weak n200: > 0.5 in 11/20 fits, > 0.9 in 6/20; median min PIP 0.742; fits with min PIP < 0.1: 3
- AR-weak n400: > 0.5 in 10/10 fits, > 0.9 in 9/10; median min PIP 1.000; fits with min PIP < 0.1: 0
- AR-weak n800: > 0.5 in 10/10 fits, > 0.9 in 10/10; median min PIP 1.000; fits with min PIP < 0.1: 0
- IND n100: > 0.5 in 4/5 fits, > 0.9 in 3/5; median min PIP 0.961; fits with min PIP < 0.1: 1
- IND n200: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0
- IND n400: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0
- BLK n100: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 0.955; fits with min PIP < 0.1: 0
- BLK n200: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0
- BLK n400: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0
- ADJ-OPP n200: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0
- ADJ-OPP n400: > 0.5 in 5/5 fits, > 0.9 in 5/5; median min PIP 1.000; fits with min PIP < 0.1: 0

## S2b. PIP reliability curve, AR-weak arm (equal-weight PIP; a repeated-sampling diagnostic under a fixed truth, MANIFEST_CELLS section 4; NOT a calibration of any single posterior)
| bin | variables n (all AR-weak fits) | mean PIP (predicted frequency) | observed frequency of S0 | 95% dataset-cluster bootstrap | n_true (active) | datasets with >= 1 variable | observed by n (100 / 200 / 400 / 800) |
|---|---|---|---|---|---|---|---|
| 0.00-0.05 | 599722 | 0.0001 | 0.0001 | [7.84e-05, 1.70e-04] | 74 | 60 | 0.000 (70/199954) / 0.000 (4/199879) / 0.000 (0/99942) / 0.000 (0/99947) |
| 0.05-0.10 | 33 | 0.0708 | 0.1212 | [0.0294, 0.2353] | 4 | 23 | 0.333 (4/12) / 0.000 (0/16) / 0.000 (0/4) / 0.000 (0/1) |
| 0.10-0.15 | 14 | 0.1230 | 0.5000 | [0.2143, 0.8000] | 7 | 13 | 0.600 (3/5) / 0.667 (4/6) / 0.000 (0/2) / 0.000 (0/1) |
| 0.15-0.20 | 6 | 0.1727 | 0.1667 | [0.0000, 0.5000] | 1 | 6 | 0.500 (1/2) / 0.000 (0/3) / 0.000 (0/1) / - (0/0) |
| 0.20-0.25 | 5 | 0.2320 | 1.0000 | [1.0000, 1.0000] | 5 | 5 | 1.000 (2/2) / 1.000 (3/3) / - (0/0) / - (0/0) |
| 0.25-0.30 | 3 | 0.2595 | 0.3333 | [0.0000, 1.0000] | 1 | 3 | 0.333 (1/3) / - (0/0) / - (0/0) / - (0/0) |
| 0.30-0.35 | 4 | 0.3157 | 0.5000 | [0.0000, 1.0000] | 2 | 4 | 0.333 (1/3) / 1.000 (1/1) / - (0/0) / - (0/0) |
| 0.35-0.40 | 5 | 0.3866 | 0.2000 | [0.0000, 0.6667] | 1 | 5 | 0.500 (1/2) / 0.000 (0/3) / - (0/0) / - (0/0) |
| 0.40-0.45 | 4 | 0.4032 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (2/2) / 1.000 (1/1) / 0.000 (0/1) / - (0/0) |
| 0.45-0.50 | 2 | 0.4801 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | 1.000 (2/2) / - (0/0) / - (0/0) / - (0/0) |
| 0.50-0.55 | 1 | 0.5306 | 1.0000 | [1.0000, 1.0000] | 1 | 1 | 1.000 (1/1) / - (0/0) / - (0/0) / - (0/0) |
| 0.55-0.60 | 5 | 0.5682 | 1.0000 | [1.0000, 1.0000] | 5 | 4 | 1.000 (2/2) / 1.000 (3/3) / - (0/0) / - (0/0) |
| 0.65-0.70 | 1 | 0.6801 | 1.0000 | [1.0000, 1.0000] | 1 | 1 | - (0/0) / - (0/0) / 1.000 (1/1) / - (0/0) |
| 0.70-0.75 | 4 | 0.7297 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (1/1) / 0.667 (2/3) / - (0/0) / - (0/0) |
| 0.75-0.80 | 2 | 0.7762 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | 1.000 (1/1) / 1.000 (1/1) / - (0/0) / - (0/0) |
| 0.80-0.85 | 2 | 0.8289 | 1.0000 | [1.0000, 1.0000] | 2 | 2 | - (0/0) / 1.000 (1/1) / 1.000 (1/1) / - (0/0) |
| 0.85-0.90 | 4 | 0.8900 | 0.7500 | [0.0000, 1.0000] | 3 | 4 | 1.000 (2/2) / 1.000 (1/1) / - (0/0) / 0.000 (0/1) |
| 0.90-0.95 | 6 | 0.9429 | 1.0000 | [1.0000, 1.0000] | 6 | 5 | - (0/0) / 1.000 (6/6) / - (0/0) / - (0/0) |
| 0.95-1.00 | 177 | 0.9973 | 1.0000 | [1.0000, 1.0000] | 177 | 46 | 1.000 (6/6) / 1.000 (73/73) / 1.000 (48/48) / 1.000 (50/50) |

## S3. C5 distribution (per cell; mean over datasets [95% t interval]; d_H^2 = Hellinger^2 to the true predictive)
| design | n | d_H^2 HPM plug-in | d_H^2 MPM plug-in | d_H^2 store-BMA predictive | oracle d_H^2 (known-S0 fit) | ratio to oracle (BMA / oracle) | n d_H^2 (BMA) | n d_H^2 / (s0 log p) (BMA) | post. median d_H | test MSE - oracle | mlpd - oracle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.0364 [0.0093, 0.0635] | 0.0324 [0.0050, 0.0598] | 0.0314 [0.0103, 0.0525] | 0.0092 [0.0069, 0.0115] | 4.399 [0.175, 8.622] | 3.143 [1.032, 5.254] | 0.0682 [0.0224, 0.1141] | 0.2117 [0.1628, 0.2605] | 0.2180 [-0.0308, 0.4667] | -0.0789 [-0.1552, -0.0026] |
| AR-strong | 200 | 0.0043 [0.0029, 0.0056] | 0.0043 [0.0029, 0.0056] | 0.0048 [0.0037, 0.0059] | 0.0042 [0.0030, 0.0055] | 1.191 [0.936, 1.446] | 0.956 [0.733, 1.179] | 0.0208 [0.0159, 0.0256] | 0.1038 [0.0942, 0.1135] | 0.0038 [-0.0010, 0.0087] | -0.0020 [-0.0046, 6.28e-04] |
| AR-strong | 400 | 0.0015 [8.90e-04, 0.0020] | 0.0015 [8.90e-04, 0.0020] | 0.0015 [9.59e-04, 0.0021] | 0.0015 [9.11e-04, 0.0021] | 1.036 [0.991, 1.082] | 0.610 [0.384, 0.837] | 0.0133 [0.0083, 0.0182] | 0.0616 [0.0565, 0.0668] | 5.96e-04 [-1.97e-04, 0.0014] | -3.14e-04 [-7.28e-04, 9.94e-05] |
| AR-strong | 800 | 0.0011 [6.27e-04, 0.0016] | 0.0011 [6.27e-04, 0.0016] | 0.0011 [6.43e-04, 0.0015] | 0.0011 [6.27e-04, 0.0015] | 1.020 [0.996, 1.044] | 0.877 [0.514, 1.240] | 0.0190 [0.0112, 0.0269] | 0.0463 [0.0412, 0.0514] | -1.21e-05 [-4.29e-04, 4.05e-04] | 1.13e-05 [-1.95e-04, 2.18e-04] |
| AR-weak | 100 | 0.1055 [0.0971, 0.1139] | 0.1002 [0.0892, 0.1112] | 0.0933 [0.0822, 0.1044] | 0.0082 [0.0066, 0.0098] | 14.256 [9.958, 18.554] | 9.331 [8.221, 10.440] | 0.2026 [0.1785, 0.2267] | 0.3225 [0.3105, 0.3344] | 0.8639 [0.7410, 0.9869] | -0.2902 [-0.3256, -0.2547] |
| AR-weak | 200 | 0.0183 [0.0100, 0.0265] | 0.0164 [0.0089, 0.0238] | 0.0152 [0.0087, 0.0217] | 0.0046 [0.0034, 0.0059] | 3.496 [2.185, 4.807] | 3.039 [1.738, 4.340] | 0.0660 [0.0377, 0.0942] | 0.1463 [0.1248, 0.1678] | 0.0907 [0.0341, 0.1474] | -0.0393 [-0.0622, -0.0165] |
| AR-weak | 400 | 0.0024 [9.96e-04, 0.0037] | 0.0024 [9.96e-04, 0.0037] | 0.0031 [0.0011, 0.0051] | 0.0024 [0.0010, 0.0038] | 1.395 [0.794, 1.995] | 1.240 [0.433, 2.047] | 0.0269 [0.0094, 0.0445] | 0.0718 [0.0600, 0.0836] | 0.0058 [-0.0030, 0.0145] | -0.0026 [-0.0067, 0.0014] |
| AR-weak | 800 | 0.0013 [1.84e-04, 0.0023] | 0.0013 [1.84e-04, 0.0023] | 0.0011 [3.38e-04, 0.0020] | 7.82e-04 [5.14e-04, 0.0011] | 1.582 [0.295, 2.868] | 0.918 [0.270, 1.565] | 0.0199 [0.0059, 0.0340] | 0.0462 [0.0372, 0.0552] | 0.0022 [-0.0029, 0.0074] | -0.0014 [-0.0045, 0.0018] |
| IND | 100 | 0.0309 [-0.0341, 0.0959] | 0.0234 [-0.0209, 0.0678] | 0.0244 [-0.0168, 0.0656] | 0.0087 [0.0025, 0.0149] | 2.292 [-0.353, 4.937] | 2.440 [-1.684, 6.563] | 0.0530 [-0.0366, 0.1425] | 0.1977 [0.0865, 0.3089] | 0.1486 [-0.2192, 0.5164] | -0.0691 [-0.2377, 0.0996] |
| IND | 200 | 0.0052 [0.0019, 0.0086] | 0.0052 [0.0019, 0.0086] | 0.0052 [0.0023, 0.0080] | 0.0050 [0.0020, 0.0080] | 1.044 [0.950, 1.137] | 1.032 [0.467, 1.598] | 0.0224 [0.0101, 0.0347] | 0.1049 [0.0924, 0.1174] | 0.0013 [-4.56e-04, 0.0030] | -4.27e-04 [-0.0014, 5.72e-04] |
| IND | 400 | 0.0046 [-0.0019, 0.0112] | 0.0046 [-0.0019, 0.0112] | 0.0042 [-5.07e-04, 0.0089] | 0.0030 [8.13e-04, 0.0052] | 1.255 [0.850, 1.660] | 1.677 [-0.203, 3.557] | 0.0364 [-0.0044, 0.0772] | 0.0826 [0.0518, 0.1135] | 0.0088 [-0.0102, 0.0279] | -0.0054 [-0.0172, 0.0065] |
| BLK | 100 | 0.0067 [0.0039, 0.0096] | 0.0124 [-7.71e-04, 0.0256] | 0.0095 [0.0049, 0.0142] | 0.0064 [0.0041, 0.0087] | 1.752 [0.023, 3.480] | 0.953 [0.489, 1.416] | 0.0207 [0.0106, 0.0308] | 0.1569 [0.1142, 0.1996] | 0.0253 [-0.0183, 0.0688] | -0.0105 [-0.0309, 0.0099] |
| BLK | 200 | 0.0076 [0.0050, 0.0101] | 0.0076 [0.0050, 0.0101] | 0.0079 [0.0051, 0.0107] | 0.0078 [0.0051, 0.0105] | 1.007 [0.995, 1.019] | 1.578 [1.014, 2.141] | 0.0343 [0.0220, 0.0465] | 0.1129 [0.0996, 0.1263] | 5.89e-04 [-5.47e-04, 0.0017] | -3.16e-04 [-0.0010, 3.90e-04] |
| BLK | 400 | 0.0042 [0.0031, 0.0053] | 0.0042 [0.0031, 0.0053] | 0.0043 [0.0034, 0.0052] | 0.0042 [0.0032, 0.0052] | 1.020 [0.980, 1.061] | 1.708 [1.346, 2.070] | 0.0371 [0.0292, 0.0449] | 0.0823 [0.0752, 0.0895] | 0.0011 [-4.06e-04, 0.0026] | -5.13e-04 [-0.0011, 9.48e-05] |
| ADJ-OPP | 200 | 0.0053 [0.0030, 0.0076] | 0.0053 [0.0030, 0.0076] | 0.0060 [0.0039, 0.0082] | 0.0054 [0.0030, 0.0078] | 1.158 [0.756, 1.560] | 1.207 [0.778, 1.635] | 0.0262 [0.0169, 0.0355] | 0.1079 [0.0907, 0.1251] | 0.0046 [-0.0075, 0.0166] | -0.0023 [-0.0082, 0.0035] |
| ADJ-OPP | 400 | 0.0032 [0.0012, 0.0051] | 0.0032 [0.0012, 0.0051] | 0.0032 [0.0014, 0.0050] | 0.0032 [0.0014, 0.0050] | 1.026 [0.986, 1.067] | 1.289 [0.566, 2.013] | 0.0280 [0.0123, 0.0437] | 0.0742 [0.0614, 0.0871] | 9.50e-04 [2.13e-04, 0.0017] | -4.41e-04 [-7.64e-04, -1.18e-04] |
| NULL | 200 | 5.38e-04 [2.93e-04, 7.83e-04] | 5.38e-04 [2.93e-04, 7.83e-04] | 5.40e-04 [2.94e-04, 7.87e-04] | 5.40e-04 [2.97e-04, 7.83e-04] | 0.998 [0.980, 1.015] | 0.108 [0.059, 0.157] | n/a (s0 = 0) | 0.0289 [0.0250, 0.0328] | 6.18e-05 [-7.12e-05, 1.95e-04] | -3.19e-05 [-1.32e-04, 6.81e-05] |

Fitted slope of log d_H^2 on log n (OLS on the log of the dataset-mean per n; 95 percent percentile interval of a dataset bootstrap within each n; B = 4000, seed 20261119). The reference exponent of a rate d_H^2 proportional to 1/n is -1; no claim is made from it.
| design | n values (datasets) | slope, store-BMA predictive d_H^2 | slope, HPM plug-in d_H^2 | slope, oracle d_H^2 |
|---|---|---|---|---|
| AR-strong | 100 (10), 200 (10), 400 (10), 800 (10) | -1.62 [-1.89, -1.32] | -1.67 [-1.95, -1.32] | -1.08 [-1.28, -0.90] |
| AR-weak | 100 (20), 200 (20), 400 (10), 800 (10) | -2.13 [-2.42, -1.88] | -2.21 [-2.53, -1.94] | -1.11 [-1.29, -0.96] |
| IND | 100 (5), 200 (5), 400 (5) | -1.27 [-2.10, -0.15] | -1.37 [-2.38, 0.14] | -0.76 [-1.19, -0.22] |
| BLK | 100 (5), 200 (5), 400 (5) | -0.58 [-0.81, -0.31] | -0.34 [-0.55, -0.05] | -0.31 [-0.50, -0.09] |
| ADJ-OPP | 200 (5), 400 (5) | -0.90 [-1.63, -0.33] | -0.74 [-1.56, -0.10] | -0.78 [-1.52, -0.14] |

## S4. C7 evidence / merge (per cell)  [log Z-hat: dataset-mean over fits]
| design | n | log Z-hat (mean; range) | sigma-hat of Z_r (mean [CI]; max) | robust sigma-hat (mean) | max - median of log Z_r (mean; max) | R_eff / R' (min) | log Z-hat - log Z_T (mean; max) | omitted store mass (max) | island PIP sd, max (max) | sd of log Z-hat_occ(1000) over islands (max) |
|---|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 100 | -130.5 (-137.2 to -117.7) | 0.0894 [-0.0037, 0.1826]; 0.4579 | 0.0740 | 0.185; 1.090 | 0.773 | 0.2965; 0.4343 | 0 | 0.01058 | 0.0247 |
| AR-strong | 200 | -199.7 (-212.9 to -177.2) | 0.0216 [0.0186, 0.0247]; 0.0277 | 0.0208 | 0.039; 0.076 | 0.999 | 0.1395; 0.2339 | 0 | 0.00374 | 0.0205 |
| AR-strong | 400 | -347.4 (-368.5 to -334.7) | 0.0182 [0.0139, 0.0224]; 0.0310 | 0.0170 | 0.034; 0.050 | 0.999 | 0.0689; 0.0956 | 0 | 0.00089 | 0.0143 |
| AR-strong | 800 | -623.1 (-671.1 to -568.6) | 0.0213 [0.0167, 0.0258]; 0.0316 | 0.0192 | 0.041; 0.058 | 0.999 | 0.0324; 0.0489 | 0 | 0.00044 | 0.0109 |
| AR-weak | 100 | -145.8 (-147.6 to -140.3) | 0.0187 [0.0102, 0.0271]; 0.0780 | 0.0169 | 0.032; 0.101 | 0.995 | 0.0645; 0.1728 | 0 | 0.00905 | 0.0217 |
| AR-weak | 200 | -264.7 (-282.4 to -241.4) | 0.0267 [0.0228, 0.0305]; 0.0407 | 0.0265 | 0.050; 0.078 | 0.999 | 0.1362; 0.1904 | 0 | 0.00502 | 0.0221 |
| AR-weak | 400 | -485.9 (-511.2 to -467.8) | 0.0178 [0.0151, 0.0206]; 0.0233 | 0.0146 | 0.042; 0.067 | 0.999 | 0.0653; 0.0851 | 0 | 0.00228 | 0.0160 |
| AR-weak | 800 | -888.7 (-920.2 to -861.4) | 0.0161 [0.0114, 0.0208]; 0.0258 | 0.0152 | 0.027; 0.053 | 0.999 | 0.0343; 0.0474 | 0 | 0.00077 | 0.0112 |
| IND | 100 | -128.6 (-141.1 to -114.3) | 0.0806 [-0.0291, 0.1903]; 0.2373 | 0.0611 | 0.208; 0.794 | 0.914 | 0.3526; 0.4867 | 0 | 0.00591 | 0.0252 |
| IND | 200 | -191.7 (-210.4 to -175.8) | 0.0237 [0.0170, 0.0304]; 0.0310 | 0.0229 | 0.041; 0.058 | 0.999 | 0.1422; 0.1621 | 0 | 0.00212 | 0.0148 |
| IND | 400 | -340.1 (-352.3 to -326.5) | 0.0173 [0.0112, 0.0235]; 0.0236 | 0.0147 | 0.032; 0.042 | 0.999 | 0.0698; 0.0839 | 0 | 0.00116 | 0.0140 |
| BLK | 100 | -126.4 (-135.3 to -116.2) | 0.0739 [0.0352, 0.1125]; 0.1108 | 0.0733 | 0.124; 0.171 | 0.989 | 0.3232; 0.4923 | 0 | 0.00780 | 0.0203 |
| BLK | 200 | -208.1 (-222.2 to -169.7) | 0.0262 [0.0180, 0.0343]; 0.0376 | 0.0220 | 0.052; 0.076 | 0.999 | 0.1343; 0.1614 | 0 | 0.00072 | 0.0157 |
| BLK | 400 | -357.5 (-391.7 to -334.6) | 0.0296 [0.0193, 0.0400]; 0.0384 | 0.0286 | 0.043; 0.063 | 0.999 | 0.0664; 0.0917 | 0 | 0.00090 | 0.0142 |
| ADJ-OPP | 200 | -229.0 (-241.8 to -220.1) | 0.2381 [-0.3520, 0.8281]; 1.0880 | 0.2215 | 0.431; 1.964 | 0.423 | 0.1008; 0.2053 | 0 | 0.00341 | 0.0161 |
| ADJ-OPP | 400 | -401.3 (-427.8 to -376.4) | 0.0201 [0.0124, 0.0278]; 0.0283 | 0.0213 | 0.036; 0.070 | 0.999 | 0.0639; 0.0785 | 0 | 0.00052 | 0.0127 |
| NULL | 200 | -289.9 (-289.9 to -289.9) | 0.0014 [6.91e-04, 0.0021]; 0.0023 | 0.0012 | 0.003; 0.005 | 1.000 | 0.0075; 0.0086 | 0 | 0.00014 | 0.0052 |

Flag frequencies over the science fits (all run at I_max = 0). At I_max = 0 the calibration rebuild loop never runs: E1 / E2 of the CALIBRATION are NOT EVALUATED (not 0 %), `grid_unconverged` = True, `checks_passed_calibration` = False and `I_used` = 0 are CONSTANTS (PREREG section 7, last bullet; CAMPAIGN_FREEZE_ADDENDUM section 2). Reported here as constants, outside any quality aggregate:
- calibration constants / pilot-only flags, 155 fits: {'grid_unconverged True': 155, 'checks_passed_calibration False': 155, 'I_used = 0': 155, 'escalated': 0, 'forced_pilot_steps > 0': 0}
- calibration triggers fired (list of triggers: fits): {'grid_unconverged': 155}
- FINAL-stage flags in `fit.meta.flags` (frequency over 155 fits; computed on the final islands / merge; E1 and E2 here are the eval-record fields, which at I_max = 0 are not driven by a rebuild loop and must be read as 'not evaluated' when False): E1 0, E2 1, E3 0, checks_passed_final 148, final_local_limit 0, local_limit 0, low_empirical_ESS 6, ls0_hpm_changed 0, ls0_improved 0, ls0_local_limit 0, near_tie_truncated 0, occ_inhomogeneous 0
- cells with any of occ_inhomogeneous / low_empirical_ESS / local_limit / final_local_limit / near_tie_truncated / ls0_hpm_changed / ls0_improved: {'AR n800': {'low_empirical_ESS': 1}, 'ARweak n100': {'low_empirical_ESS': 3}, 'IND n100': {'low_empirical_ESS': 2}}
- island spread analogue of E2 (sd of log Z_r over the R' = 16 final islands = sigma-hat of log; > 1 would be the analogue): max over fits of the sd of log Z_r = 1.0880
- island stage count T of the frozen preliminary grid (mean over fits): 14.4; by n: n100 13.9, n200 15.4, n400 12.8, n800 15.4

## S5. A3 partition: exact (`partition exact`, tag A3 / A3F) vs the default truncated partition, paired by dataset (engine seed 1)
| pair (dataset) | default tag | HPM equal | HPM = S0 (A3 / default) | F(HPM) A3 - default | max abs(PIP_A3 - PIP_default) | log Z-hat A3 - default | island s.e. of the difference | d_H^2 BMA A3 / default | core-h A3 / default |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong n200 r01 | VF | True | True / True | +0.00e+00 | 1.32e-06 | +0.00291 | 0.00910 | 0.00737 / 0.00737 | 2.18 / 1.43 |
| AR-strong n200 r02 | VF | True | True / True | +0.00e+00 | 7.90e-06 | +0.00273 | 0.00642 | 0.00402 / 0.00402 | 1.51 / 1.62 |
| AR-strong n200 r03 | VF | True | True / True | +0.00e+00 | 3.35e-05 | -0.00801 | 0.00664 | 0.00371 / 0.00371 | 1.11 / 1.22 |
| AR-strong n200 r04 | VF | True | True / True | +0.00e+00 | 9.14e-07 | -0.00336 | 0.00692 | 0.00180 / 0.00180 | 1.64 / 1.57 |
| AR-strong n200 r05 | V | True | True / True | +0.00e+00 | 1.27e-05 | +0.00352 | 0.01056 | 0.00434 / 0.00434 | 1.68 / 1.51 |
| AR-strong n200 r06 | V | True | True / True | +2.84e-14 | 7.92e-05 | -0.00037 | 0.00584 | 0.00674 / 0.00674 | 1.24 / 1.14 |
| AR-strong n200 r07 | V | True | True / True | +0.00e+00 | 5.82e-05 | +0.00807 | 0.00715 | 0.00466 / 0.00466 | 1.85 / 1.22 |
| AR-strong n200 r08 | V | True | True / True | +0.00e+00 | 2.50e-04 | +0.00481 | 0.00931 | 0.00542 / 0.00540 | 2.27 / 2.30 |
| AR-strong n200 r09 | V | True | True / True | +0.00e+00 | 1.80e-04 | +0.00290 | 0.00764 | 0.00503 / 0.00504 | 1.38 / 1.33 |
| AR-strong n200 r10 | V | True | True / True | +0.00e+00 | 3.75e-06 | -0.00521 | 0.00577 | 0.00471 / 0.00471 | 1.48 / 1.24 |
| BLK n200 r01 | V | True | True / True | +0.00e+00 | 1.16e-05 | -0.00481 | 0.00851 | 0.01174 / 0.01173 | 3.21 / 1.72 |
| BLK n200 r02 | V | True | True / True | +0.00e+00 | 3.00e-07 | -0.01572 | 0.01300 | 0.00669 / 0.00669 | 2.52 / 2.41 |
| BLK n200 r03 | V | True | True / True | +0.00e+00 | 1.03e-05 | +0.00684 | 0.00861 | 0.00771 / 0.00770 | 1.49 / 1.26 |
| BLK n200 r04 | V | True | True / True | +0.00e+00 | 7.67e-07 | -0.00718 | 0.00963 | 0.00745 / 0.00745 | 2.19 / 1.82 |
| BLK n200 r05 | V | True | True / True | +0.00e+00 | 5.30e-06 | -0.01172 | 0.00876 | 0.00586 / 0.00586 | 1.54 / 1.63 |

Summary: 15 pairs, HPM identical in 15, HPM = S0 in 15 (A3) / 15 (default); max over pairs and variables of abs(dPIP) = 2.50e-04; dlogZ (A3 - default) mean -0.00164 [-0.00554, 0.00226], largest abs 0.01572, largest abs in island s.e. of the difference 1.34; cost A3 1.82 [1.51, 2.13] vs default 1.56 [1.35, 1.77] core-h; pi_0(S0) NOT AVAILABLE (B4, HQ Q6); d_H between the two partitions' predictives NOT COMPUTABLE (the default-partition fits have no law.bin: law.bin was kept for the precision and A3 fits only).

## S6. Second seed: AR-strong n = 200, engine seeds 1 and 2 on 10 datasets (the yardstick for any other V comparison)
| dataset | HPM equal | HPM = S0 (s1 / s2) | max abs(PIP_s1 - PIP_s2) | log Z-hat s1 - s2 | d_H^2 BMA s1 / s2 |
|---|---|---|---|---|---|
| AR n200 r01 | True | True / True | 2.89e-04 | -0.02161 | 0.00737 / 0.00737 |
| AR n200 r02 | True | True / True | 4.37e-05 | -0.00718 | 0.00402 / 0.00400 |
| AR n200 r03 | True | True / True | 1.14e-04 | +0.00704 | 0.00371 / 0.00371 |
| AR n200 r04 | True | True / True | 6.36e-05 | -0.00020 | 0.00180 / 0.00180 |
| AR n200 r05 | True | True / True | 6.51e-04 | -0.01629 | 0.00434 / 0.00434 |
| AR n200 r06 | True | True / True | 2.04e-04 | +0.00920 | 0.00674 / 0.00675 |
| AR n200 r07 | True | True / True | 4.79e-04 | -0.01447 | 0.00466 / 0.00466 |
| AR n200 r08 | True | True / True | 5.72e-04 | -0.02593 | 0.00540 / 0.00542 |
| AR n200 r09 | True | True / True | 8.67e-04 | -0.01021 | 0.00504 / 0.00504 |
| AR n200 r10 | True | True / True | 1.55e-04 | -0.00937 | 0.00471 / 0.00471 |

Summary: HPM equal in 10/10 datasets; max abs(dPIP) 8.67e-04 (median 2.47e-04); seed-to-seed sd of log Z-hat (pooled, sqrt(mean d^2 / 2)) = 0.00998; largest abs(dlogZ) 0.02593; seed-to-seed d_H^2 difference: mean abs 7.93e-06.

## S7. NULL control (n = 200, S0 empty; 5 datasets, one fit each)
| run | n_null PIP > 0.5 | n_null PIP > 0.1 | sup PIP (eq) | HPM size | outcome | log Z-hat | sigma-hat |
|---|---|---|---|---|---|---|---|
| 4-NULL-n200-r01-VF-s1 | 0 | 0 | 0.0080 | 0 | correct | -289.896 | 0.0010 |
| 4-NULL-n200-r02-V-s1 | 0 | 0 | 0.0126 | 0 | correct | -289.881 | 0.0014 |
| 4-NULL-n200-r03-V-s1 | 0 | 0 | 0.0081 | 0 | correct | -289.900 | 0.0009 |
| 4-NULL-n200-r04-V-s1 | 0 | 0 | 0.0098 | 0 | correct | -289.872 | 0.0014 |
| 4-NULL-n200-r05-V-s1 | 0 | 0 | 0.0157 | 0 | correct | -289.854 | 0.0023 |

n_null_gt_0.5 = 0 in 5 of 5 NULL fits; HPM empty in 5 of 5; largest sup PIP 0.0157.
Non-NULL fits with a null-variable PIP > 0.5 (n_null_gt_0.5 > 0): 5 (4-ARweak-n200-r06-V-s1: 1; 4-BLK-n100-r03-V-s1: 1; 4-IND-n100-r03-V-s1: 1; 4-IND-n400-r01-V-s1: 1; 4-ARweak-n800-r01-V-s1: 1)

## S8. n-trend summary (the same numbers as S1-S3, one line per design)
| design | n | P(HPM = S0) | min PIP over S0 (mean) | sup null PIP (mean) | d_H^2 BMA (mean) | n d_H^2 / (s0 log p) | sigma-hat (mean) |
|---|---|---|---|---|---|---|---|
| AR-strong | 100 | 0.50 | 0.561 | 0.172 | 0.0314 | 0.068 | 0.0894 |
| AR-strong | 200 | 1.00 | 1.000 | 0.124 | 0.0048 | 0.021 | 0.0216 |
| AR-strong | 400 | 1.00 | 1.000 | 0.055 | 0.0015 | 0.013 | 0.0182 |
| AR-strong | 800 | 1.00 | 1.000 | 0.050 | 0.0011 | 0.019 | 0.0213 |
| AR-weak | 100 | 0.00 | 2.2e-03 | 0.117 | 0.0933 | 0.203 | 0.0187 |
| AR-weak | 200 | 0.50 | 0.560 | 0.151 | 0.0152 | 0.066 | 0.0267 |
| AR-weak | 400 | 1.00 | 0.966 | 0.090 | 0.0031 | 0.027 | 0.0178 |
| AR-weak | 800 | 0.90 | 1.000 | 0.123 | 0.0011 | 0.020 | 0.0161 |
| IND | 100 | 0.80 | 0.748 | 0.302 | 0.0244 | 0.053 | 0.0806 |
| IND | 200 | 1.00 | 1.000 | 0.095 | 0.0052 | 0.022 | 0.0237 |
| IND | 400 | 0.80 | 1.000 | 0.307 | 0.0042 | 0.036 | 0.0173 |
| BLK | 100 | 1.00 | 0.960 | 0.159 | 0.0095 | 0.021 | 0.0739 |
| BLK | 200 | 1.00 | 1.000 | 0.034 | 0.0079 | 0.034 | 0.0262 |
| BLK | 400 | 1.00 | 1.000 | 0.089 | 0.0043 | 0.037 | 0.0296 |
| ADJ-OPP | 200 | 1.00 | 1.000 | 0.131 | 0.0060 | 0.026 | 0.2381 |
| ADJ-OPP | 400 | 1.00 | 1.000 | 0.049 | 0.0032 | 0.028 | 0.0201 |
| NULL | 200 | 1.00 | n/a | 0.011 | 5.40e-04 | n/a | 0.0014 |
