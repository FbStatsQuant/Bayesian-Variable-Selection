# WP2: setup sizes and memory at p = 10^6 (count-only, MEASURED sizes; byte columns are accounting)

Source: `tools/bench_setup.cpp count <design> 1000000 <n> 3 1` (PR #13, exp/P1M-wp2-setup), Owls (Xeon Gold 6148, shared, nice 19), 3 threads.
Data: WP1 `gen` seed 1, WP1 `prep::standardise`. Production partition: truncated linkage (D-4/D-4a), B_V = 14 (D-19), packing by minimum index.

- J, block histogram, C (codes), edges and the edge-pass time are MEASURED. Byte columns are in GB, from the exact accounting (estimate; bound) of the
  `--count-only` pass: nothing is materialised, so the measured RSS (≈ 2.4 / 4.8 / 11.8 GB at n = 200 / 400 / 1,000) is not the setup peak.
- **floor** = X + logr + table stores (estimate) + cond_cum: the irreducible setup working set.
- "island reads from setup.bin" excludes the table stores (D-18). "dep::Start" is the island-side layout before D-31; D-31 removes cond_cum from both.
- ADJ-OPP has the same X as AR (same seed). Every column here depends on X only, so ADJ-OPP = AR at each n (checked at n = 200: identical row).

| design | n | B / B_V | J | mean block | C (codes) | C/p | edges | X | logr | table stores (est; bound) | cond_cum | **floor** | setup peak est (bound) | setup.bin est | island reads from setup.bin | island in memory: dep::Start | edge pass (3 thr) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ADJ-OPP | 200 | 14 / 14 | 74,726 | 13.38 | 0.876e9 | 876 | 1,467,802 | 1.6 | 7.00 | 3.04; 6.56 | 0.87 | **12.5** | 14.1 (20.3) | 11.1 | 8.1 | 25.8 | 891 s |
| AR | 1000 | 16 / 14 | 78,261 | 12.78 | 0.695e9 | 695 | 3,131,833 | 8.0 | 5.56 | 3.04; 6.56 | 4.58 | **21.2** | 22.1 (28.4) | 13.6 | 10.6 | 25.5 | 4069 s |
| AR | 200 | 14 / 14 | 74,726 | 13.38 | 0.876e9 | 876 | 1,467,802 | 1.6 | 7.00 | 3.04; 6.56 | 0.87 | **12.5** | 14.1 (20.3) | 11.1 | 8.1 | 25.8 | 897 s |
| AR | 400 | 16 / 14 | 75,982 | 13.16 | 0.802e9 | 802 | 2,198,004 | 3.2 | 6.42 | 3.04; 6.56 | 1.80 | **14.5** | 15.1 (21.7) | 11.5 | 8.5 | 24.9 | 1666 s |
| BLK | 200 | 14 / 14 | 96,183 | 10.40 | 0.409e9 | 409 | 9,412,332 | 1.6 | 3.27 | 3.04; 6.56 | 0.92 | **8.8** | 10.4 (16.5) | 7.4 | 4.4 | 12.9 | 903 s |
| BLK | 400 | 16 / 14 | 96,673 | 10.34 | 0.399e9 | 399 | 9,547,960 | 3.2 | 3.19 | 3.04; 6.56 | 1.87 | **11.3** | 11.9 (18.1) | 8.4 | 5.4 | 13.9 | 1618 s |
| IND | 1000 | 16 / 14 | 71,712 | 13.94 | 1.142e9 | 1142 | 62,652 | 8.0 | 9.14 | 3.04; 6.56 | 4.52 | **24.7** | 25.6 (33.7) | 17.1 | 14.1 | 37.9 | 4179 s |
| IND | 200 | 14 / 14 | 71,574 | 13.97 | 1.156e9 | 1156 | 29,879 | 1.6 | 9.25 | 3.04; 6.56 | 0.86 | **14.8** | 16.4 (23.3) | 13.4 | 10.3 | 33.7 | 861 s |
| IND | 400 | 16 / 14 | 71,656 | 13.96 | 1.148e9 | 1148 | 48,220 | 3.2 | 9.18 | 3.04; 6.56 | 1.78 | **17.2** | 17.9 (25.8) | 14.3 | 11.2 | 34.6 | 1737 s |

Block-size histograms and wall/RSS of each run:

```
ADJ-OPP 200 histogram {'10': 1, '11': 176, '12': 6732, '13': 32168, '14': 35649} wall=906.54 cpu=296% maxrss_kb=2421216
AR 1000 histogram {'10': 996, '11': 9844, '12': 18913, '13': 24257, '14': 24240, '9': 11} wall=4141.36 cpu=296% maxrss_kb=11845680
AR 200 histogram {'10': 1, '11': 176, '12': 6732, '13': 32168, '14': 35649} wall=911.66 cpu=296% maxrss_kb=2424284
AR 400 histogram {'10': 28, '11': 2700, '12': 12471, '13': 30594, '14': 30189} wall=1702.45 cpu=296% maxrss_kb=4786940
BLK 200 histogram {'1': 20, '10': 11316, '11': 12060, '12': 12651, '13': 12752, '14': 12650, '2': 117, '3': 349, '4': 768, '5': 1320, '6': 5876, '7': 7311, '8': 8851, '9': 10142} wall=972.17 cpu=285% maxrss_kb=3010716
BLK 400 histogram {'1': 26, '10': 11621, '11': 11998, '12': 12535, '13': 12568, '14': 12140, '2': 108, '3': 333, '4': 704, '5': 1261, '6': 6043, '7': 7695, '8': 9206, '9': 10435} wall=1702.19 cpu=290% maxrss_kb=5016668
IND 1000 histogram {'13': 3962, '14': 67749, '8': 1} wall=4222.11 cpu=297% maxrss_kb=11756940
IND 200 histogram {'13': 2030, '14': 69543, '8': 1} wall=871.20 cpu=297% maxrss_kb=2382080
IND 400 histogram {'13': 3177, '14': 68478, '7': 1} wall=1759.02 cpu=296% maxrss_kb=4725344
```


## D-31 (PR #50): the same runs with cond_cum on demand and the corrected accounting (ESTIMATE; GB)

Recomputed from the records above with `v4_setup_bench acct` (the D-31 accounting, validated equal to a direct count run at p = 10^5). "cond" = cond_ptr + cond_cum -> cond0.
The table stage never held the conditional rows and becomes the limiting stage, so the overall setup peak falls by less than the retained size: unchanged at n <= 400, -2.9 to -3.0 GB at n = 1,000.

| design | n | cond rows: old -> cond0 (GB) | setup.bin est: old -> new (GB) | setup peak est: old -> new (GB), limiting stage | setup peak bound: old -> new (GB) | start_law stage est: old -> new (GB) |
|---|---|---|---|---|---|---|
| AR | 200 | 0.87 -> 0.06 | 11.1 -> 10.3 | 14.1 -> 14.1 (tables -> tables) | 20.3 -> 20.3 | 12.8 -> 12.0 |
| AR | 400 | 1.80 -> 0.12 | 11.5 -> 9.9 | 15.1 -> 15.1 (tables -> tables) | 21.7 -> 21.3 | 14.8 -> 13.1 |
| AR | 1000 | 4.58 -> 0.31 | 13.6 -> 9.4 | 22.1 -> 19.1 (start_mode -> tables) | 28.4 -> 25.2 | 21.7 -> 17.4 |
| IND | 200 | 0.86 -> 0.06 | 13.4 -> 12.5 | 16.4 -> 16.4 (tables -> tables) | 23.3 -> 22.5 | 15.0 -> 14.2 |
| IND | 400 | 1.78 -> 0.12 | 14.3 -> 12.6 | 17.9 -> 17.9 (tables -> tables) | 25.8 -> 24.2 | 17.5 -> 15.9 |
| IND | 1000 | 4.52 -> 0.29 | 17.1 -> 12.9 | 25.6 -> 22.7 (start_mode -> tables) | 33.7 -> 29.5 | 25.2 -> 21.0 |
| BLK | 200 | 0.92 -> 0.08 | 7.4 -> 6.6 | 10.4 -> 10.4 (tables -> tables) | 16.5 -> 16.5 | 9.1 -> 8.3 |
| BLK | 400 | 1.87 -> 0.16 | 8.4 -> 6.7 | 11.9 -> 11.9 (tables -> tables) | 18.1 -> 18.1 | 11.7 -> 9.9 |

Pending: BLK n=1000. Updated 2026-11-16T20:54.
