# N4 stress test summary (numbers only)

Designs: S1 (c=3, psi .2, beta 1,1,1, theta[b]=-psi*beta, visible group beta .7; S0 = 3 a-hubs + 3 b-hubs + vis hub), S2 (c=2, psi .5, betas 1,.6), S3 (c=1, beta .35, psi .2). g=9, rho=.4; seeds as listed; method seed 1000+seed; allocation 16 GB/24 h. peak_mem = process peak working set (one process per design x (n,p)).

| design | n | p | fits | status counts | non-smc | esc rate | hpm==S0 | mean N_p | max N_p | max pilot step (tier0) | max N_b | max intervals | T_0 / T_1 | frac cons S0 in V | frac Lambda_V<log(10/9) (n eval) | max sec | max peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 400 | 81 | 6 | completed:6 | 0 | 0.000 | 1/6 | 9.17 | 13 | 0.3824 | 7 | 20 | 1000 / 4000 | 1.000 (12/12) | 0.000 (0/12) | 139.5 | 173 |
| S1 | 1600 | 135 | 6 | completed:6 | 0 | 0.000 | 6/6 | 14.83 | 20 | 0.5912 | 15 | 28 | 1000 / 4000 | 1.000 (18/18) | 0.000 (0/18) | 180.4 | 193 |
| S1 | 3200 | 189 | 6 | completed:6 | 0 | 0.000 | 6/6 | 9.17 | 19 | 0.7690 | 16 | 25 | 1000 / 4000 | 1.000 (19/19) | 0.000 (0/19) | 255.6 | 215 |
| S2 | 400 | 81 | 6 | completed:6 | 0 | 0.000 | 5/6 | 12.17 | 14 | 0.2429 | 8 | 21 | 1000 / 4000 | 1.000 (17/17) | 0.000 (0/17) | 111.1 | 178 |
| S2 | 1600 | 135 | 6 | completed:6 | 0 | 0.000 | 6/6 | 8.50 | 23 | 1.0000 | 12 | 35 | 1000 / 4000 | 1.000 (17/17) | 0.000 (0/17) | 271.5 | 192 |
| S2 | 3200 | 189 | 6 | completed:6 | 0 | 0.000 | 6/6 | 9.67 | 31 | 1.0000 | 9 | 39 | 1000 / 4000 | 1.000 (16/16) | 0.000 (0/16) | 377.9 | 224 |
| S3 | 400 | 81 | 6 | completed:6 | 0 | 0.000 | 0/6 | 1.00 | 1 | 1.0000 | 0 | 1 | 1000 / 4000 | 1.000 (12/12) | 0.833 (10/12) | 30.3 | 165 |
| S3 | 1600 | 135 | 6 | completed:6 | 0 | 0.000 | 0/6 | 2.67 | 7 | 1.0000 | 5 | 12 | 1000 / 4000 | 1.000 (17/17) | 0.000 (0/17) | 67.8 | 179 |
| S3 | 3200 | 189 | 6 | completed:6 | 0 | 0.000 | 1/6 | 2.67 | 8 | 1.0000 | 5 | 13 | 1000 / 4000 | 1.000 (18/18) | 0.000 (0/18) | 148.3 | 213 |

Max intervals vs T_e per (design, n, tier):
```
 design    n tier  T_e intervals
     S1  400    0 1000        20
     S2  400    0 1000        21
     S3  400    0 1000         1
     S1 1600    0 1000        28
     S2 1600    0 1000        35
     S3 1600    0 1000        12
     S1 3200    0 1000        25
     S2 3200    0 1000        39
     S3 3200    0 1000        13
```

Non-completed statuses:
none

Constructions with ok == FALSE:
none

Escalated fits:
none

Trigger strings:
```
 design    n trig Freq
     S1  400  t0:    6
     S2  400  t0:    6
     S3  400  t0:    6
     S1 1600  t0:    6
     S2 1600  t0:    6
     S3 1600  t0:    6
     S1 3200  t0:    6
     S2 3200  t0:    6
     S3 3200  t0:    6
```

Fits: 54. estimates_available FALSE: 0. guard exceeded: 0. final tier not converged: 0. forced_pilot_steps>0 constructions: 0.

Fits with hpm != S0:
```
 design    n seed              hpm                  S0
     S1  400    1       1+19+37+55 1+10+19+28+37+46+55
     S1  400    3    1+19+37+46+55 1+10+19+28+37+46+55
     S1  400    4       1+19+37+55 1+10+19+28+37+46+55
     S1  400    5    1+10+19+37+55 1+10+19+28+37+46+55
     S1  400    6 1+10+19+37+46+55 1+10+19+28+37+46+55
     S2  400    5          1+10+19          1+10+19+28
     S3  400    1                1                1+10
     S3  400    2                1                1+10
     S3  400    3                1                1+10
     S3  400    4                1                1+10
     S3  400    5                1                1+10
     S3  400    6                1                1+10
     S3 1600    1                1                1+10
     S3 1600    2                1                1+10
     S3 1600    3             1+11                1+10
     S3 1600    4                1                1+10
     S3 1600    5                1                1+10
     S3 1600    6                1                1+10
     S3 3200    1                1                1+10
     S3 3200    2                1                1+10
     S3 3200    3                1                1+10
     S3 3200    4                1                1+10
     S3 3200    6                1                1+10
```
