# G-B read-back (gb_readback.py)

G-B: **PASS**; C6 rule: **PASS**; branch pass; winning fits ['5-ADJOPP-n200-r01-V-s1', '5-AR-n200-r01-V-s1']

| fit | N / I_max | billed (E, ratio) | C1 | C2 | C3 (max % of request) | C4 | M1 | M2 | M3 | pi_hat(S0) |
|---|---|---|---|---|---|---|---|---|---|---|
| 5-ADJOPP-n200-r01-V-s1 | 10000 / 0 | 65.65 (133, 0.4936) | OK | PASS | PASS (34.69) | True | 0.008355 | 0.0008055 | 0.04509 | 0.3397 |
| 5-ADJOPP-n200-r01-VI3-s1 | 10000 / 3 | 72.5 (142, 0.5106) | OK | PASS | PASS (41.48) | True | 0.008255 | 0.0009016 | 0.05061 | 0.3412 |
| 5-AR-n200-r01-V-s1 | 10000 / 0 | 76.39 (108, 0.7073) | OK | PASS | PASS (35.9) | True | 0.007625 | 0.0002723 | 0.01528 | 0.3865 |
| 5-AR-n200-r01-VI3-s1 | 10000 / 3 | 83.11 (118, 0.7043) | OK | PASS | PASS (40.28) | True | 0.007616 | 0.000283 | 0.01666 | 0.3849 |

Stages (billed core-h, wall s, MaxRSS GiB of request):
- 5-ADJOPP-n200-r01-V-s1: setup 0.5067 / 57 s / 2.5 of 16 G (15.63%); calibrate 1.813 / 102 s / 5.55 of 16 G (34.69%); islands 62.4 / 396 s / 3.7 of 12 G (30.83%); merge 0.8667 / 195 s / 6.864 of 24 G (28.6%); eval 0.0667 / 30 s / 1.723 of 16 G (10.77%)
- 5-ADJOPP-n200-r01-VI3-s1: setup 0.48 / 54 s / 2.497 of 16 G (15.6%); calibrate 8.462 / 476 s / 6.637 of 16 G (41.48%); islands 62.77 / 380 s / 3.611 of 12 G (30.09%); merge 0.7111 / 160 s / 6.872 of 24 G (28.63%); eval 0.0733 / 33 s / 1.879 of 16 G (11.74%)
- 5-AR-n200-r01-V-s1: setup 0.5333 / 60 s / 2.502 of 16 G (15.64%); calibrate 1.511 / 85 s / 5.744 of 16 G (35.9%); islands 73.51 / 447 s / 3.535 of 12 G (29.46%); merge 0.7644 / 172 s / 4.967 of 24 G (20.7%); eval 0.0711 / 32 s / 1.669 of 16 G (10.43%)
- 5-AR-n200-r01-VI3-s1: setup 0.4178 / 47 s / 2.511 of 16 G (15.69%); calibrate 10.99 / 618 s / 6.444 of 16 G (40.28%); islands 71.12 / 414 s / 3.532 of 12 G (29.43%); merge 0.4933 / 111 s / 4.829 of 24 G (20.12%); eval 0.0911 / 41 s / 1.824 of 16 G (11.4%)
