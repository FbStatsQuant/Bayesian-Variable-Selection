## X1. Fits with a final-stage flag or an island spread sd(log Z_r) > 0.3
- 4-ADJOPP-n200-r04-V-s1: flags ['E2'], checks_passed_final False, sd(log Z_r) 1.088, sigma_hat 1.088 (robust 1.003), R_eff/R' 0.423, max-median 1.964, log Z_r range -230.21..-226.18 (median -228.08), HPM=S0 True, cost 1.54
- 4-AR-n100-r07-V-s1: flags [], checks_passed_final True, sd(log Z_r) 0.458, sigma_hat 0.458 (robust 0.383), R_eff/R' 0.773, max-median 1.090, log Z_r range -126.62..-125.11 (median -126.19), HPM=S0 True, cost 1.39
- 4-AR-n800-r02-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.032, sigma_hat 0.032 (robust 0.018), R_eff/R' 0.999, max-median 0.054, log Z_r range -601.20..-601.08 (median -601.14), HPM=S0 True, cost 1.76
- 4-ARweak-n100-r05-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.009, sigma_hat 0.009 (robust 0.003), R_eff/R' 1.000, max-median 0.028, log Z_r range -147.59..-147.55 (median -147.58), HPM=S0 False, cost 0.57
- 4-ARweak-n100-r06-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.043, sigma_hat 0.043 (robust 0.045), R_eff/R' 0.998, max-median 0.101, log Z_r range -143.76..-143.62 (median -143.72), HPM=S0 False, cost 1.28
- 4-ARweak-n100-r11-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.009, sigma_hat 0.009 (robust 0.010), R_eff/R' 1.000, max-median 0.015, log Z_r range -147.35..-147.32 (median -147.33), HPM=S0 False, cost 0.62
- 4-IND-n100-r02-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.027, sigma_hat 0.027 (robust 0.022), R_eff/R' 0.999, max-median 0.025, log Z_r range -125.88..-125.77 (median -125.80), HPM=S0 True, cost 1.54
- 4-IND-n100-r04-V-s1: flags ['low_empirical_ESS'], checks_passed_final False, sd(log Z_r) 0.237, sigma_hat 0.237 (robust 0.110), R_eff/R' 0.914, max-median 0.794, log Z_r range -141.49..-140.36 (median -141.15), HPM=S0 True, cost 1.31

## X2. Same quantities for the other designs' worst fits (largest sigma-hat per cell with sigma_hat > 0.1)
- 4-ADJOPP-n200-r04-V-s1: sigma_hat 1.088, R_eff/R' 0.423, max-median 1.964, flags ['E2']
- 4-AR-n100-r07-V-s1: sigma_hat 0.458, R_eff/R' 0.773, max-median 1.090, flags ['checks_passed_final']
- 4-IND-n100-r04-V-s1: sigma_hat 0.237, R_eff/R' 0.914, max-median 0.794, flags ['low_empirical_ESS']
- 4-BLK-n100-r03-V-s1: sigma_hat 0.111, R_eff/R' 0.989, max-median 0.169, flags ['checks_passed_final']
- 4-BLK-n100-r02-V-s1: sigma_hat 0.094, R_eff/R' 0.992, max-median 0.171, flags ['checks_passed_final']
- 4-BLK-n100-r05-V-s1: sigma_hat 0.080, R_eff/R' 0.994, max-median 0.134, flags ['checks_passed_final']

## X3. Reliability, AR-weak: bins 0.05-0.95 pooled (the mid-range)
variables with PIP in [0.05, 0.95): 101; active among them 49; expected active count (sum of PIP) 32.2
  n = 100: 40 variables, 24 active, expected 11.6
  n = 200: 48 variables, 23 active, expected 17.0
  n = 400: 10 variables, 2 active, expected 2.6
  n = 800: 3 variables, 0 active, expected 1.1

## X4. Store-BMA predictive d_H^2: s.e. and exactness
exact mixture (no tail sample): 0 of 155 fits; max h2_se_x 1.73e-03; max h2_se_tail 1.60e-04; max omitted store mass 0; max dropped_mass 0
largest relative s.e. (h2_se_x / h2): 0.023

## X5. Cost by class (committed model E; G-B criterion: class mean <= 1.5 E AND no fit > 2.5 E; every fit > 1.5 E listed)
| class | fits | mean | max | E | mean/E | max/E | class mean <= 1.5E | no fit > 2.5E | fits > 1.5E |
|---|---|---|---|---|---|---|---|---|---|
| A3 n200 | 16 | 1.87 | 3.21 | 2.76 | 0.68 | 1.16 | yes | yes | 0 |
| ADJOPP n200 | 5 | 1.46 | 1.61 | 2.69 | 0.54 | 0.60 | yes | yes | 0 |
| ADJOPP n400 | 5 | 1.13 | 1.42 | 4.62 | 0.24 | 0.31 | yes | yes | 0 |
| AR n100 | 10 | 1.67 | 2.07 | 1.55 | 1.08 | 1.33 | yes | yes | 0 |
| AR n200 | 21 | 1.52 | 2.64 | 2.18 | 0.70 | 1.21 | yes | yes | 0 |
| AR n400 | 10 | 1.12 | 1.53 | 3.64 | 0.31 | 0.42 | yes | yes | 0 |
| AR n800 | 10 | 1.49 | 2.06 | 6.94 | 0.21 | 0.30 | yes | yes | 0 |
| ARweak n100 | 22 | 0.76 | 1.28 | 1.36 | 0.56 | 0.94 | yes | yes | 0 |
| ARweak n200 | 20 | 1.47 | 1.96 | 1.87 | 0.78 | 1.05 | yes | yes | 0 |
| ARweak n400 | 10 | 1.23 | 1.67 | 3.05 | 0.40 | 0.55 | yes | yes | 0 |
| ARweak n800 | 10 | 1.25 | 1.54 | 5.67 | 0.22 | 0.27 | yes | yes | 0 |
| BLK n100 | 5 | 1.74 | 2.05 | 1.58 | 1.10 | 1.30 | yes | yes | 0 |
| BLK n200 | 5 | 1.77 | 2.41 | 2.22 | 0.80 | 1.09 | yes | yes | 0 |
| BLK n400 | 5 | 2.32 | 2.91 | 3.72 | 0.62 | 0.78 | yes | yes | 0 |
| IND n100 | 5 | 1.73 | 2.20 | 1.62 | 1.07 | 1.36 | yes | yes | 0 |
| IND n200 | 5 | 1.47 | 1.61 | 2.30 | 0.64 | 0.70 | yes | yes | 0 |
| IND n400 | 5 | 1.07 | 1.26 | 3.89 | 0.27 | 0.33 | yes | yes | 0 |
| NULL n200 | 5 | 0.44 | 0.50 | 0.51 | 0.87 | 0.97 | yes | yes | 0 |
| T law | 2 | 40.42 | 44.21 | (no class: T fits, report line 172.5) | - | - | - | - | - |
| prec N2500 m1 I0 | 6 | 5.00 | 5.55 | 5.76 | 0.87 | 0.96 | yes | yes | 0 |
| prec N2500 m1 I3 | 6 | 6.02 | 7.24 | 6.28 | 0.96 | 1.15 | yes | yes | 0 |
| prec N2500 m4 I3 | 6 | 12.37 | 14.01 | 12.36 | 1.00 | 1.13 | yes | yes | 0 |

G-B cost criterion on the 21 model classes: PASS in every class; fits above 1.5 x their committed model: 0 []

## X6. n-scaling (V arm, I_max = 0 frozen fits; mean billed core-h per fit; ratio to the same design's n = 200 mean; the planning model's nf(n) ratio 0.7 / 1.0 / 1.6 / 2.8)
| design | n=100 | n=200 | n=400 | n=800 | ratio 100/200 | ratio 400/200 | ratio 800/200 | mean island T (100/200/400/800) | mean islands core-h (100/200/400/800) |
|---|---|---|---|---|---|---|---|---|---|
| AR-strong | 1.67 | 1.46 | 1.12 | 1.49 | 1.14 | 0.77 | 1.02 | 22.10/15.40/9.30/19.80 | 1.47/1.27/0.91/1.21 |
| AR-weak | 0.77 | 1.47 | 1.23 | 1.25 | 0.52 | 0.84 | 0.85 | 4.90/16.15/10.50/11.10 | 0.61/1.27/0.99/1.02 |
| IND | 1.73 | 1.47 | 1.07 | - | 1.18 | 0.73 | - | 23.00/17.20/8.20/- | 1.52/1.22/0.82/- |
| BLK | 1.74 | 1.77 | 2.32 | - | 0.98 | 1.31 | - | 24.20/23.60/30.20/- | 1.52/1.56/2.05/- |
| ADJ-OPP | - | 1.46 | 1.13 | - | - | 0.77 | - | -/17.00/11.60/- | -/1.28/0.92/- |
| NULL | - | 0.44 | - | - | - | - | - | -/1.00/-/- | -/0.32/-/- |

All science V fits pooled by n (design mix differs by n): mean n100 1.23 (40 fits), n200 1.40 (60 fits), n400 1.32 (35 fits), n800 1.37 (20 fits); n = 200 excluding NULL: 1.49
Fits that cost more than the design's n = 200 mean: n = 400: AR-strong 1/10, AR-weak 1/10, IND 0/5, BLK 5/5, ADJ-OPP 0/5

## X7. Stage split, wall and memory (science V fits, by n: mean core-h per stage; max wall s; max RSS MB)
| n | fits | setup | calibrate | islands | merge | eval | max wall s cal / isl / merge | max RSS MB (setup / cal / isl / merge / eval) |
|---|---|---|---|---|---|---|---|---|
| 100 | 40 | 0.020 | 0.083 | 1.048 | 0.054 | 0.028 | 29 / 145 / 40 | 167 / 583 / 344 / 705 / 857 |
| 200 | 60 | 0.028 | 0.087 | 1.211 | 0.049 | 0.029 | 33 / 165 / 43 | 359 / 801 / 432 / 869 / 774 |
| 400 | 35 | 0.047 | 0.090 | 1.082 | 0.061 | 0.038 | 35 / 168 / 40 | 383 / 812 / 456 / 888 / 760 |
| 800 | 20 | 0.060 | 0.089 | 1.116 | 0.064 | 0.041 | 32 / 117 / 43 | 389 / 856 / 494 / 856 / 766 |

A3 fits (exact partition): mean cost 1.82 core-h; setup stage mean 0.036 core-h, max setup wall 19 s; max RSS setup 869 MB
