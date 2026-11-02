# n = 200 table: Theorem N200 terms, predicted vs observed, per cell (100 fits each)

Columns: obs U = fits with no output (resource_limit); obs miss = posterior misses among fits with output (S-ELS: every completed wrong HPM has F(S0) < F(S-hat); 0 search misses); obs wrong = U + miss = the event of Thm N200. P(L|X) = exact-score MC (R = 40 draws per design, 100 designs) of the one-move posterior-miss event, a rigorous LOWER bound on the posterior-miss term P(S-dagger != S0 | X); P(L or dd) adds the 91 double drops; excess = their difference (the measured multi-move contribution, not a bound); realised = the same events on the study's own y (count of 100); max_e p_e = rigorous lower bracket (PA closed forms); sum_e p_e = union bound on P(L|X) (PA), capped at 1 per design; T2 = O-SWAP's approximate predictor; Le Cam = pairwise two-point floor for ANY selector. pred wrong = obs U + n_out * mean P(L|X); z = (obs miss - n_out * mean P(L|X)) / SD (design binomial + MC error).


## c = 1.0

| p | S | obs U | obs miss (extra/missed/mixed) | **obs wrong** | P(L\|X) % | P(L or dd) % | excess pts | realised one/miss | max_e p_e % | sum_e p_e % | T2 % | Le Cam % | **pred wrong** | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | S1 | 0 | 5 (5/0/0) | **5** | 7.4 | 7.4 | 0.0 | 5/5 | 0.00 | 7.2 | 6.5 | 0.0 | **7.4** | -0.9 |
| 500 | S2 | 0 | 4 (4/0/0) | **4** | 6.9 | 6.9 | 0.0 | 4/4 | 0.00 | 7.4 | 6.6 | 0.0 | **6.9** | -1.1 |
| 500 | S3 | 0 | 6 (6/0/0) | **6** | 6.3 | 6.3 | 0.0 | 6/6 | 0.01 | 7.4 | 6.7 | 0.0 | **6.3** | -0.1 |
| 500 | S4 | 0 | 9 (5/0/4) | **9** | 5.9 | 5.9 | 0.0 | 9/9 | 0.30 | 8.8 | 8.0 | 0.4 | **5.9** | 1.3 |
| 500 | S5 | 1 | 10 (10/0/0) | **11** | 8.3 | 8.3 | 0.0 | 9/9 | 0.01 | 9.6 | 8.6 | 0.0 | **9.2** | 0.7 |
| 500 | S6 | 0 | 6 (6/0/0) | **6** | 5.8 | 5.8 | 0.0 | 6/6 | 0.08 | 7.5 | 6.8 | 0.1 | **5.8** | 0.1 |
| 500 | **sum** | 1 | 40 | **41** | 40.5 | 40.5 | | 39/39 | | | 43.1 | | **41.5** | |
| 1000 | S1 | 0 | 5 (5/0/0) | **5** | 6.2 | 6.2 | 0.0 | 5/5 | 0.00 | 6.8 | 6.1 | 0.0 | **6.2** | -0.5 |
| 1000 | S2 | 0 | 5 (5/0/0) | **5** | 5.5 | 5.5 | 0.0 | 5/5 | 0.00 | 6.8 | 6.1 | 0.0 | **5.5** | -0.2 |
| 1000 | S3 | 0 | 3 (3/0/0) | **3** | 5.5 | 5.5 | 0.0 | 2/2 | 0.01 | 6.7 | 6.0 | 0.0 | **5.5** | -1.1 |
| 1000 | S4 | 0 | 7 (4/0/3) | **7** | 5.7 | 5.7 | 0.0 | 7/7 | 0.32 | 8.4 | 7.6 | 0.4 | **5.7** | 0.6 |
| 1000 | S5 | 3 | 13 (13/0/0) | **16** | 8.4 | 8.4 | 0.0 | 14/14 | 0.01 | 9.2 | 8.1 | 0.0 | **11.2** | 1.8 |
| 1000 | S6 | 0 | 4 (4/0/0) | **4** | 6.3 | 6.3 | 0.0 | 4/4 | 0.09 | 7.0 | 6.3 | 0.1 | **6.3** | -0.9 |
| 1000 | **sum** | 3 | 37 | **40** | 37.3 | 37.3 | | 37/37 | | | 39.9 | | **40.3** | |

c = 1.0 totals over 1,200 fits: observed wrong = 81 (U = 4, posterior misses = 77); predicted wrong = U + sum P(L|X) = 81.8; with double drops = 81.8; realised one-move on study y = 76; T2 = 83.1.

## c = 0.5

| p | S | obs U | obs miss (extra/missed/mixed) | **obs wrong** | P(L\|X) % | P(L or dd) % | excess pts | realised one/miss | max_e p_e % | sum_e p_e % | T2 % | Le Cam % | **pred wrong** | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | S1 | 0 | 21 (13/6/2) | **21** | 21.6 | 21.9 | 0.2 | 20/20 | 4.65 | 37.4 | 21.5 | 0.4 | **21.6** | -0.1 |
| 500 | S2 | 0 | 16 (9/7/0) | **16** | 22.2 | 22.4 | 0.2 | 16/16 | 4.79 | 40.1 | 22.6 | 1.2 | **22.2** | -1.5 |
| 500 | S3 | 0 | 36 (11/7/18) | **36** | 31.4 | 31.5 | 0.1 | 35/36 | 4.64 | 58.7 | 34.7 | 3.4 | **31.4** | 1.0 |
| 500 | S4 | 0 | 75 (5/5/65) | **75** | 65.3 | 65.3 | 0.0 | 75/75 | 8.38 | 100.0 | 73.2 | 9.1 | **65.3** | 2.0 |
| 500 | S5 | 0 | 41 (6/18/17) | **41** | 48.0 | 49.1 | 1.1 | 40/40 | 18.45 | 100.0 | 52.4 | 3.8 | **48.0** | -1.4 |
| 500 | S6 | 0 | 41 (6/6/29) | **41** | 39.9 | 40.0 | 0.1 | 40/40 | 5.64 | 79.0 | 46.3 | 6.4 | **39.9** | 0.2 |
| 500 | **sum** | 0 | 230 | **230** | 228.3 | 230.0 | | 226/227 | | | 250.6 | | **228.3** | |
| 1000 | S1 | 0 | 29 (10/16/3) | **29** | 24.1 | 24.4 | 0.3 | 28/28 | 6.77 | 56.5 | 25.0 | 0.4 | **24.1** | 1.1 |
| 1000 | S2 | 0 | 25 (12/11/2) | **25** | 25.6 | 25.8 | 0.2 | 25/25 | 6.83 | 58.9 | 26.0 | 1.2 | **25.6** | -0.1 |
| 1000 | S3 | 0 | 33 (7/14/12) | **33** | 33.2 | 33.4 | 0.2 | 33/33 | 6.82 | 77.6 | 37.1 | 3.5 | **33.2** | -0.0 |
| 1000 | S4 | 0 | 65 (3/3/59) | **65** | 65.0 | 65.1 | 0.1 | 64/64 | 8.58 | 100.0 | 74.5 | 9.2 | **65.0** | 0.0 |
| 1000 | S5 | 2 | 67 (10/31/26) | **69** | 55.8 | 56.9 | 1.1 | 68/68 | 23.79 | 100.0 | 59.4 | 3.9 | **56.7** | 2.5 |
| 1000 | S6 | 0 | 39 (5/9/25) | **39** | 43.5 | 43.5 | 0.0 | 39/39 | 6.79 | 96.8 | 49.1 | 6.6 | **43.5** | -0.9 |
| 1000 | **sum** | 2 | 258 | **260** | 246.0 | 247.9 | | 257/257 | | | 270.0 | | **248.0** | |

c = 0.5 totals over 1,200 fits: observed wrong = 490 (U = 2, posterior misses = 488); predicted wrong = U + sum P(L|X) = 476.3; with double drops = 479.9; realised one-move on study y = 483; T2 = 520.6.

**Grand total (2,400 fits):** observed wrong = 571 (U = 6, posterior misses = 565, search misses = 0); predicted = 558.1 (U observed + sum of MC P(L|X)); RMS z over 24 cells = 1.08; max |z| = 2.52.

**Discovery / search-miss term:** observed 0 of 2394 completed fits (S-ELS); exact 95% Clopper-Pearson upper bound 0.125% per fit; pooled over the 24 cells.
