# WP3: 10^6 memory plans with the real setup tables (StartView; gate P5)

Tool: `v4_plan_tables` (engine_v4/tools/plan_tables.cpp, exp/P1M-wp3-startview). ESTIMATE: every number is the plan the
code admits with (memory.h island plan, WP4's calib_memory_plan and estimate_merge_memory), with the setup's real
dimensions. A 10^6 setup.bin could not be made on Owls (WP2's exact correlation pass at p = 10^6 ran past the 2 h
limit on 3 shared cores), so the dimensions come from WP2's --count-only accounting
(SMC_Engineering_Department/tmp/20261115-wp2/counts, WP2_COUNTS_1e6.md) through `dims_from_sizes`, the same section
formula a real file gives (pinned equal in tests/test_start_view.cpp). k = max(8, q90(pi_0 size) + 1, k_store) = 8
(WP2's start-law q90 = 4-5 at n = 200; k_store unknown before calibration, so the floor). Threads: the driver's 10^6
rung (islands 96, calibrate 96, merge 32). R' = 16, N = 2,500, V (class A, label-major).

Columns:
- final island: one final island (X, z, diag G, store, worker buffers, RB, rows, Gram rows, supports, particles,
  12 % headroom) + the setup inputs (mapped start-law sections + draw scratch + neighbour CSR).
- calibration island alone: the largest calibration island (pilot: leaders, round-start snapshot, N = 512) + setup inputs;
  the pilot measurement (v4_pilot_island) without the calibration ledger.
- calibration island, N-1: the same + the calibration's resident state (ledger at staging peak + export,
  17.4 GiB at k = 8); WP4's N-1 rule admits a calibration island iff this <= --mem-budget.
- calibrate task: N-1 + WP4's SetupView copy of setup.bin (read_setup: logr, table stores, ...; WP2's setup.bin
  estimate) until PR46's reader split; after it, about the N-1 column.
- merge task: WP4's estimate (merged store + one island store + pip / terminal supports + tail wave + data.bin
  + 2.5 x setup.bin).
- G = 1 is the admission floor: with --mem-budget the island takes the largest G <= 256 that fits.

| design | n | G | final island (96 thr) | calibration island alone (96 thr) | calibration island, N-1 | calibrate task | merge task (32 thr) | setup inputs (mapped + scratch + nb) |
|---|---|---|---|---|---|---|---|---|
| AR | 200 | 1 | 19.5 GiB | 37.1 GiB | 54.4 GiB | 64.8 GiB | 38.5 GiB | 6.78 GiB |
| AR | 200 | 64 | 22.4 GiB | 40.0 GiB | 57.4 GiB | 67.7 GiB | 38.5 GiB | 6.78 GiB |
| AR | 200 | 256 | 31.7 GiB | 49.3 GiB | 66.6 GiB | 77.0 GiB | 38.5 GiB | 6.78 GiB |
| IND | 200 | 1 | 21.6 GiB | 39.1 GiB | 56.5 GiB | 68.9 GiB | 43.7 GiB | 8.86 GiB |
| IND | 200 | 64 | 24.5 GiB | 42.1 GiB | 59.4 GiB | 71.9 GiB | 43.7 GiB | 8.86 GiB |
| IND | 200 | 256 | 33.8 GiB | 51.4 GiB | 68.7 GiB | 81.2 GiB | 43.7 GiB | 8.86 GiB |
| BLK | 200 | 1 | 16.1 GiB | 33.6 GiB | 51.0 GiB | 57.9 GiB | 30.0 GiB | 3.33 GiB |
| BLK | 200 | 64 | 19.0 GiB | 36.5 GiB | 53.9 GiB | 60.8 GiB | 30.0 GiB | 3.33 GiB |
| BLK | 200 | 256 | 28.3 GiB | 45.8 GiB | 63.2 GiB | 70.1 GiB | 30.0 GiB | 3.33 GiB |
| ADJ-OPP | 200 | 1 | 19.5 GiB | 37.1 GiB | 54.4 GiB | 64.8 GiB | 38.5 GiB | 6.78 GiB |
| ADJ-OPP | 200 | 64 | 22.4 GiB | 40.0 GiB | 57.4 GiB | 67.7 GiB | 38.5 GiB | 6.78 GiB |
| ADJ-OPP | 200 | 256 | 31.7 GiB | 49.3 GiB | 66.6 GiB | 77.0 GiB | 38.5 GiB | 6.78 GiB |
| AR | 400 | 1 | 22.2 GiB | 39.8 GiB | 57.2 GiB | 67.9 GiB | 41.0 GiB | 6.36 GiB |
| AR | 400 | 64 | 25.2 GiB | 42.7 GiB | 60.1 GiB | 70.8 GiB | 41.0 GiB | 6.36 GiB |
| AR | 400 | 256 | 34.5 GiB | 52.0 GiB | 69.4 GiB | 80.1 GiB | 41.0 GiB | 6.36 GiB |
| IND | 400 | 1 | 24.8 GiB | 42.4 GiB | 59.7 GiB | 73.0 GiB | 47.3 GiB | 8.93 GiB |
| IND | 400 | 64 | 27.8 GiB | 45.3 GiB | 62.7 GiB | 76.0 GiB | 47.3 GiB | 8.93 GiB |
| IND | 400 | 256 | 37.1 GiB | 54.6 GiB | 72.0 GiB | 85.3 GiB | 47.3 GiB | 8.93 GiB |
| BLK | 400 | 1 | 19.3 GiB | 36.9 GiB | 54.2 GiB | 62.1 GiB | 33.7 GiB | 3.42 GiB |
| BLK | 400 | 64 | 22.2 GiB | 39.8 GiB | 57.2 GiB | 65.0 GiB | 33.7 GiB | 3.42 GiB |
| BLK | 400 | 256 | 31.5 GiB | 49.1 GiB | 66.5 GiB | 74.3 GiB | 33.7 GiB | 3.42 GiB |
| AR | 1000 | 1 | 31.3 GiB | 48.8 GiB | 66.2 GiB | 78.9 GiB | 50.4 GiB | 5.92 GiB |
| AR | 1000 | 64 | 34.2 GiB | 51.8 GiB | 69.1 GiB | 81.8 GiB | 50.4 GiB | 5.92 GiB |
| AR | 1000 | 256 | 43.6 GiB | 61.1 GiB | 78.5 GiB | 91.2 GiB | 50.4 GiB | 5.92 GiB |
| IND | 1000 | 1 | 34.6 GiB | 52.1 GiB | 69.5 GiB | 85.4 GiB | 58.5 GiB | 9.21 GiB |
| IND | 1000 | 64 | 37.5 GiB | 55.1 GiB | 72.4 GiB | 88.4 GiB | 58.5 GiB | 9.21 GiB |
| IND | 1000 | 256 | 46.8 GiB | 64.4 GiB | 81.8 GiB | 97.7 GiB | 58.5 GiB | 9.21 GiB |

MEASURED at p = 10^5 (n = 200, AR, WP2's real setup.bin, 1.0 GB; Owls): the start law the island holds after the load
is the mapping, 668 MiB of sections; the heap it adds (StartView + neighbours + draw scratch for 96 threads) is
12.8 MiB of RssAnon, against 2,512 MiB for the expanded dep::Start of the same file (v4_plan_tables --load 2).
