# WP3: 10^6 memory plans with the real setup tables (StartView; gate P5; regenerated for the PR57 fixes)

Tool: `v4_plan_tables` (engine_v4/tools/plan_tables.cpp), built from exp/P1M-wp3-startview at 0399568d
(includes engine head 7c2c6a75: #46, #55, #54). ESTIMATE: every number is the plan the code admits with: the island plan of
memory.h, WP4's calib_memory_plan and estimate_merge_memory, and `calib_island_plans` (calib_plan.h), the function calibrate
itself uses. The setup's dimensions come from WP2's --count-only accounting (SMC_Engineering_Department/tmp/20261115-wp2/counts,
WP2_COUNTS_1e6.md) through `dims_from_sizes`, the same section formula a real file gives (pinned equal in
tests/test_start_view.cpp); a real 10^6 setup.bin could not be made on Owls (the exact correlation pass at p = 10^6 ran past
the 2 h limit on 3 shared cores). k = max(8, q90(pi_0 size) + 1) = 8 at n = 200 (WP2's start-law q90 = 4-5). Threads: the
driver's 10^6 rung (islands 96, calibrate 96, merge 32). R' = 16, N = 2,500, V (class A, label-major).

Columns:
- final island: one final island (X, z, diag G, store, worker buffers, RB, rows, Gram rows, supports, particles, 12 % headroom)
  + its setup inputs: the mapped start-law sections + draw scratch + neighbour CSR + 1 MiB fixed heap.
- calibration island alone: the largest calibration island (pilot: leaders, round-start snapshot, N = 512) + those setup inputs;
  the pilot measurement without the calibration state.
- calibrate task = the calibration island under WP4's N-1 rule = what calibrate's admission requires of --mem-budget:
  island plan + its setup inputs + **WP4's live setup copy** (read_setup keeps logr and the partition arrays for the whole
  calibration; PR57 MAJOR-1; the three table stores are released once they are in the ledger) + the calibration's resident
  state (ledger at its staging peak + export, 17.4 GiB at k = 8). Anonymous memory the task must hold.
- + reclaimable file pages: the rest of setup.bin, paged in once by the section-hash check (RssFile; clean pages, reclaimable;
  counts toward a cgroup limit until reclaimed). Not in the plan; add it to the Slurm request if the node's reclaim is not trusted.
- merge task: WP4's estimate (merged store + one island store + pip / terminal supports + tail wave + data.bin + 2.5 x setup.bin).
- G = 1 is the admission floor: with --mem-budget the island takes the largest G <= 256 that fits.

| design | n | G | final island (96 thr) | calibration island alone (96 thr) | **calibrate task** = calibration island under N-1 (anonymous) | + reclaimable file pages | **merge task** (32 thr) | setup inputs of one island (mapped + scratch + nb) | WP4 live setup copy |
|---|---|---|---|---|---|---|---|---|---|
| AR | 200 | 1 | 19.5 GiB | 37.1 GiB | 61.7 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| AR | 200 | 64 | 22.4 GiB | 40.0 GiB | 64.6 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| AR | 200 | 256 | 31.7 GiB | 49.3 GiB | 73.9 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| IND | 200 | 1 | 21.6 GiB | 39.1 GiB | 65.9 GiB | 3.7 GiB | 44.5 GiB | 8.86 GiB | 8.63 GiB |
| IND | 200 | 64 | 24.5 GiB | 42.1 GiB | 68.8 GiB | 3.7 GiB | 44.5 GiB | 8.86 GiB | 8.63 GiB |
| IND | 200 | 256 | 33.8 GiB | 51.4 GiB | 78.1 GiB | 3.7 GiB | 44.5 GiB | 8.86 GiB | 8.63 GiB |
| BLK | 200 | 1 | 16.1 GiB | 33.6 GiB | 54.8 GiB | 3.7 GiB | 30.7 GiB | 3.33 GiB | 3.06 GiB |
| BLK | 200 | 64 | 19.0 GiB | 36.5 GiB | 57.7 GiB | 3.7 GiB | 30.7 GiB | 3.33 GiB | 3.06 GiB |
| BLK | 200 | 256 | 28.3 GiB | 45.8 GiB | 67.0 GiB | 3.7 GiB | 30.7 GiB | 3.33 GiB | 3.06 GiB |
| ADJ-OPP | 200 | 1 | 19.5 GiB | 37.1 GiB | 61.7 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| ADJ-OPP | 200 | 64 | 22.4 GiB | 40.0 GiB | 64.6 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| ADJ-OPP | 200 | 256 | 31.7 GiB | 49.3 GiB | 73.9 GiB | 3.7 GiB | 39.3 GiB | 6.78 GiB | 6.54 GiB |
| AR | 400 | 1 | 22.2 GiB | 39.8 GiB | 63.9 GiB | 4.5 GiB | 41.7 GiB | 6.36 GiB | 5.99 GiB |
| AR | 400 | 64 | 25.2 GiB | 42.7 GiB | 66.8 GiB | 4.5 GiB | 41.7 GiB | 6.36 GiB | 5.99 GiB |
| AR | 400 | 256 | 34.5 GiB | 52.0 GiB | 76.1 GiB | 4.5 GiB | 41.7 GiB | 6.36 GiB | 5.99 GiB |
| IND | 400 | 1 | 24.8 GiB | 42.4 GiB | 69.0 GiB | 4.5 GiB | 48.1 GiB | 8.93 GiB | 8.57 GiB |
| IND | 400 | 64 | 27.8 GiB | 45.3 GiB | 72.0 GiB | 4.5 GiB | 48.1 GiB | 8.93 GiB | 8.57 GiB |
| IND | 400 | 256 | 37.1 GiB | 54.6 GiB | 81.3 GiB | 4.5 GiB | 48.1 GiB | 8.93 GiB | 8.57 GiB |
| BLK | 400 | 1 | 19.3 GiB | 36.9 GiB | 57.9 GiB | 4.6 GiB | 34.5 GiB | 3.42 GiB | 2.98 GiB |
| BLK | 400 | 64 | 22.2 GiB | 39.8 GiB | 60.9 GiB | 4.6 GiB | 34.5 GiB | 3.42 GiB | 2.98 GiB |
| BLK | 400 | 256 | 31.6 GiB | 49.1 GiB | 70.2 GiB | 4.6 GiB | 34.5 GiB | 3.42 GiB | 2.98 GiB |
| AR | 1000 | 1 | 31.3 GiB | 48.8 GiB | 72.1 GiB | 6.9 GiB | 51.1 GiB | 5.92 GiB | 5.19 GiB |
| AR | 1000 | 64 | 34.2 GiB | 51.8 GiB | 75.1 GiB | 6.9 GiB | 51.1 GiB | 5.92 GiB | 5.19 GiB |
| AR | 1000 | 256 | 43.6 GiB | 61.1 GiB | 84.4 GiB | 6.9 GiB | 51.1 GiB | 5.92 GiB | 5.19 GiB |
| IND | 1000 | 1 | 34.6 GiB | 52.1 GiB | 78.7 GiB | 6.9 GiB | 59.3 GiB | 9.21 GiB | 8.52 GiB |
| IND | 1000 | 64 | 37.5 GiB | 55.1 GiB | 81.7 GiB | 6.9 GiB | 59.3 GiB | 9.21 GiB | 8.52 GiB |
| IND | 1000 | 256 | 46.8 GiB | 64.4 GiB | 91.0 GiB | 6.9 GiB | 59.3 GiB | 9.21 GiB | 8.52 GiB |

Change from the first version of this table (head 9344737d): the calibrate-task and N-1 columns include the setup copy
(+6.5 GiB at AR / 8.6 GiB at IND, n = 200) and no longer add the whole setup.bin on top; the merge column moves +0.8 GiB with
the merged head. The old "calibrate task" column (N-1 + setup.bin) was a different definition and is not comparable.

MEASURED, p = 10^5 (n 200, AR, WP2's real 1.0 GB setup.bin): the mapped sections are 668 MiB; the heap the island adds for the
start law (view + neighbours + draw scratch for 96 threads) is 12.8 MiB of RssAnon, against 2,512 MiB for the expanded dep::Start;
WP4's SetupView holds 687.3 MB (counted: 687.3 MB) once the table stores are released, 1,160 MB before (v4_plan_tables --load 3).

MEASURED, p = 2·10^4 (n 200, IND, real setup.bin, calibrate --mode V, 3 threads, --mem-budget 6 GiB): peak RSS 1,419 MiB (includes
file pages) against a plan of 1,639 MiB with the copy term; the plan without the copy was 1,464 MiB, only 3 % above the peak.
