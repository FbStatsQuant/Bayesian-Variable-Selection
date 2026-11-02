# Reproduction - 24 controlled cases verified

Final snapshot verifier `verify_final.exit` = 0 and `verify_final.log` reports 24/24 pass. Every completed snapshot case has script exit 0 and a clean finished log. Across all 24, F1/F2 original-row columns, beta, diagnostics and convergence match deployed; F3 pilot beta is identical to both snapshot F1 and original-run F1; all six saved coefficient supports per method and both K37 rules per method match their checks against the frozen derivation. No substantive differences were found. Per-case rule sizes, statuses, runtimes and all 12 c100 post-fit truth diagnostics are tabulated below; full support strings and detailed flags are saved in F3_rules_capped.csv and case_summary_capped.csv.

HQ resource order and manager allocation: at most six campaign R jobs, W1 at most four and W2 at most two. The original launcher finished naturally. Existing controlled snapshot controller PID 20212 and watcher PIDs 20864, 40968 and 10604 remain suspended; their previously running case workers have finished. New capped controller PID 29376 accounted for inherited W1 workers and reserved extra capacity for suites that invoke nested R processes. It skipped clean saved cases with RDS and script exit 0, verified existing results, and captured exits for new jobs. The manager authorized counting script exits and clean logs for the suspended controller's workers; their OS exit files remain unavailable until that controller is resumed. Launcher and verification hashes are in CAPPED_LAUNCH_SHA256.txt.

Launcher PID 36468 started 2026-10-30 03:45:45 UTC. Command: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<bench_v2>/repro/launch.ps1"`. The launcher requested 24 cases, with at most 12 concurrent processes on 14 logical processors and BLAS/OpenMP thread limits of one. Each case runs deployed and v2 F1, deployed and v2 F2, then v2 F3; logs, stderr, exit markers and raw RDS outputs are named by dataset and scale in this directory. All 24 RDS files were saved; OS exit codes were not captured.

Local environment: Windows, R 4.4.1, glmnet 4.1-10. As in `bench_audit/mgr_checks/repro_f1f2.R`, the test harness overrides the package-version gate and invokes glmnet 4.1-10 with `thresh` and `maxit` directly, setting `fdev=0, devmax=1` via glmnet.control. Production remains pinned to 5.1.

Each finished RDS contains the two method outputs, exact comparisons of original rows, beta, diagnostics and convergence, differences returned by all.equal, F3 output, elapsed seconds and pilot identity. The first case has identical original row columns, beta, diagnostics and convergence for F1 and F2. The original script's `identical(data.frame)` row result was FALSE because it changed the row.names attribute from numeric to character during subsetting; `summarise.R` now compares the columns independently and retains the original attribute result. F3 pilot identity is TRUE, pilot k=78, all six statuses ok, rule sizes 64/51/15/15/15/15, F3 runtime 220.62 s.

All 24 original-case RDS outputs have been inspected: F1/F2 original columns, beta, diagnostics and convergence were identical in all 24; pilot identities were TRUE. All saved coefficient supports and K37 selections matched their rows/frozen derivation for F1/F2/F3 in all 24. The OS exit markers are empty and do not verify operating-system exit status. F3 results, in rule order cv_min/cv_1se/ebic1/ebic05/ebic1_K37/ebic05_K37:

| Case | Pilot k | Rule k | Statuses | F3 seconds |
|---|---:|---|---|---:|
| p0500 S1 c100 | 78 | 64/51/15/15/15/15 | all ok | 220.62 |
| p1000 S1 c100 | 61 | 52/45/14/14/14/14 | all ok | 247.83 |
| p0500 S2 c100 | 66 | 50/42/14/16/14/16 | all ok | 278.50 |
| p1000 S2 c100 | 103 | 83/75/14/14/14/14 | all ok | 264.61 |
| p0500 S3 c100 | 70 | 54/47/14/15/14/15 | all ok | 333.30 |
| p1000 S3 c100 | 58 | 55/32/14/14/14/14 | all ok | 426.63 |
| p0500 S4 c100 | 56 | 46/35/14/15/14/15 | all ok | 659.70 |
| p1000 S4 c100 | 73 | 56/38/14/19/14/19 | all ok | 527.18 |
| p0500 S5 c100 | 59 | 47/30/14/14/14/14 | all ok | 696.94 |
| p1000 S5 c100 | 59 | 57/32/14/18/14/18 | all ok | 430.52 |
| p0500 S6 c100 | 66 | 52/32/14/15/14/15 | all ok | 413.00 |
| p1000 S6 c100 | 81 | 72/53/14/16/14/16 | all ok | 669.78 |
| p0500 S1 c050 | 81 | 70/51/15/15/15/15 | all ok | 321.43 |
| p1000 S1 c050 | 57 | 54/45/13/15/13/15 | all ok | 516.14 |
| p0500 S2 c050 | 66 | 50/42/14/16/14/16 | all ok | 426.56 |
| p1000 S2 c050 | 102 | 89/77/14/14/14/14 | all ok | 563.24 |
| p0500 S3 c050 | 70 | 58/47/14/15/14/15 | all ok | 678.91 |
| p1000 S3 c050 | 58 | 56/32/14/14/14/14 | all ok | 492.32 |
| p0500 S4 c050 | 56 | 47/36/13/15/13/15 | all ok | 800.70 |
| p1000 S4 c050 | 70 | 49/40/14/20/14/20 | all ok | 1147.67 |
| p0500 S5 c050 | 56 | 47/35/14/14/14/14 | all ok | 1118.13 |
| p1000 S5 c050 | 61 | 59/34/18/18/18/18 | all ok | 660.16 |
| p0500 S6 c050 | 67 | 52/35/14/15/14/15 | all ok | 721.54 |
| p1000 S6 c050 | 80 | 72/51/17/17/17/17 | all ok | 855.56 |

The original `summarise.R` initially failed when the difference list was empty; that script was corrected. The final frozen-snapshot results are instead in `case_summary_capped.csv`, `F3_rules_capped.csv` and the tables below, produced after all case workers finished.

`case_summary.csv` records per-case elapsed seconds separately for deployed and v2 F1 and F2, along with F3. It also records all six F3 support strings and the support/K37 checks.

**Original-run provenance limitation:** `RUN_SOURCE_SHA256.txt` records hashes after launch. F3 fit code was edited after launch before its loading was observed. A subsequent `source_snapshot/` contains all 15 v2 source files and was checked byte-for-byte against the current tree, but those original jobs read the live tree, not the snapshot. Their F3 results are exploratory; the controlled frozen-snapshot rerun and verifier reported below provide the final-source evidence.

Before the manager's requested coefficient fix, all ten live F1/F2 file hashes matched `RUN_SOURCE_SHA256.txt`. The fix then changed both common.R files, so this first batch is not final-source evidence. Snapshot `snapshot_2a8362b2f348/` contains all 15 current source files and has tree hash `2a8362b2f348f45bbce4a547ed95ef6455cc704e148d1d799adb804f3acdaa67`. The original controlled launcher PID 20212 and watcher PID 40968 remain suspended under the manager's order; the capped replacement completed the remaining snapshot cases. The separate real F3 runner and validator already passed.

The final verifier read all 24 saved snapshot RDS files and passed all checks; inherited OS exits remain uncollected, while script exits and finished logs are available for every case.

The original launcher wrote empty exit files for its cases; their saved RDS and logs can be inspected but OS exit codes were not captured. The capped controller retains process handles and captures exits for its new jobs; all controlled case scripts also write their own script exit status. Original PID 36468 was not stopped.

The original launcher and earlier local tests did not explicitly set TEMP/TMP, so R may have created automatic temporary directories outside bench_v2. Subsequent launchers set TEMP/TMP to tests/local_tmp; the original batch could not inherit that change and was left untouched until it finished.

## Verified snapshot case table (24/24)

Rule order: cv_min / cv_1se / ebic1 / ebic05 / ebic1_K37 / ebic05_K37. All rows below have script exit 0, clean logs and pass all saved F1/F2, pilot, support and K37 comparisons. OS exits of inherited workers are not claimed.

| Case | Pilot k | Rule k | Rule statuses | F3 seconds |
|---|---:|---|---|---:|
| dev_p0500_S1_r001 c100 | 78 | 64/51/15/15/15/15 | ok/ok/ok/ok/ok/ok | 184.8 |
| dev_p1000_S1_r001 c100 | 61 | 52/45/14/14/14/14 | ok/ok/ok/ok/ok/ok | 298.08 |
| dev_p0500_S2_r001 c100 | 66 | 50/42/14/16/14/16 | ok/ok/ok/ok/ok/ok | 287.66 |
| dev_p1000_S2_r001 c100 | 103 | 83/75/14/14/14/14 | ok/ok/ok/ok/ok/ok | 258.35 |
| dev_p0500_S3_r001 c100 | 70 | 54/47/14/15/14/15 | ok/ok/ok/ok/ok/ok | 339.89 |
| dev_p1000_S3_r001 c100 | 58 | 55/32/14/14/14/14 | ok/ok/ok/ok/ok/ok | 284.08 |
| dev_p0500_S4_r001 c100 | 56 | 46/35/14/15/14/15 | ok/ok/ok/ok/ok/ok | 615.08 |
| dev_p1000_S4_r001 c100 | 73 | 56/38/14/19/14/19 | ok/ok/ok/ok/ok/ok | 385.17 |
| dev_p0500_S5_r001 c100 | 59 | 47/30/14/14/14/14 | ok/ok/ok/ok/ok/ok | 455.7 |
| dev_p1000_S5_r001 c100 | 59 | 57/32/14/18/14/18 | ok/ok/ok/ok/ok/ok | 319 |
| dev_p0500_S6_r001 c100 | 66 | 52/32/14/15/14/15 | ok/ok/ok/ok/ok/ok | 382.72 |
| dev_p1000_S6_r001 c100 | 81 | 72/53/14/16/14/16 | ok/ok/ok/ok/ok/ok | 338.36 |
| dev_p0500_S1_r001 c050 | 81 | 70/51/15/15/15/15 | ok/ok/ok/ok/ok/ok | 302.86 |
| dev_p1000_S1_r001 c050 | 57 | 54/45/13/15/13/15 | ok/ok/ok/ok/ok/ok | 388.06 |
| dev_p0500_S2_r001 c050 | 66 | 50/42/14/16/14/16 | ok/ok/ok/ok/ok/ok | 527.3 |
| dev_p1000_S2_r001 c050 | 102 | 89/77/14/14/14/14 | ok/ok/ok/ok/ok/ok | 350.52 |
| dev_p0500_S3_r001 c050 | 70 | 58/47/14/15/14/15 | ok/ok/ok/ok/ok/ok | 602.04 |
| dev_p1000_S3_r001 c050 | 58 | 56/32/14/14/14/14 | ok/ok/ok/ok/ok/ok | 379.17 |
| dev_p0500_S4_r001 c050 | 56 | 47/36/13/15/13/15 | ok/ok/ok/ok/ok/ok | 728.35 |
| dev_p1000_S4_r001 c050 | 70 | 49/40/14/20/14/20 | ok/ok/ok/ok/ok/ok | 756.9 |
| dev_p0500_S5_r001 c050 | 56 | 47/35/14/14/14/14 | ok/ok/ok/ok/ok/ok | 741.58 |
| dev_p1000_S5_r001 c050 | 61 | 59/34/18/18/18/18 | ok/ok/ok/ok/ok/ok | 380.44 |
| dev_p0500_S6_r001 c050 | 67 | 52/35/14/15/14/15 | ok/ok/ok/ok/ok/ok | 522.84 |
| dev_p1000_S6_r001 c050 | 80 | 72/51/17/17/17/17 | ok/ok/ok/ok/ok/ok | 470.59 |

## Post-fit c100 truth diagnostics

| Case | Method | Noise weights below weakest truth | Truth in screen | Truth on path | EBIC1 K37 exact |
|---|---|---:|---|---|---|
| dev_p0500_S1_r001 | ridge | 14 | TRUE | TRUE | FALSE |
| dev_p0500_S1_r001 | v2 | 0 | TRUE | TRUE | FALSE |
| dev_p1000_S1_r001 | ridge | 27 | TRUE | TRUE | TRUE |
| dev_p1000_S1_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p0500_S2_r001 | ridge | 10 | TRUE | TRUE | TRUE |
| dev_p0500_S2_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p1000_S2_r001 | ridge | 35 | TRUE | TRUE | TRUE |
| dev_p1000_S2_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p0500_S3_r001 | ridge | 7 | TRUE | TRUE | TRUE |
| dev_p0500_S3_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p1000_S3_r001 | ridge | 131 | TRUE | FALSE | FALSE |
| dev_p1000_S3_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p0500_S4_r001 | ridge | 11 | TRUE | FALSE | FALSE |
| dev_p0500_S4_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p1000_S4_r001 | ridge | 85 | TRUE | FALSE | FALSE |
| dev_p1000_S4_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p0500_S5_r001 | ridge | 14 | TRUE | TRUE | TRUE |
| dev_p0500_S5_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p1000_S5_r001 | ridge | 212 | TRUE | FALSE | FALSE |
| dev_p1000_S5_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p0500_S6_r001 | ridge | 38 | TRUE | TRUE | TRUE |
| dev_p0500_S6_r001 | v2 | 0 | TRUE | TRUE | TRUE |
| dev_p1000_S6_r001 | ridge | 204 | TRUE | FALSE | FALSE |
| dev_p1000_S6_r001 | v2 | 0 | TRUE | TRUE | TRUE |

## F1/F2 per-case wall times (seconds)

| Case | F1 deployed | F1 v2 | F2 deployed | F2 v2 |
|---|---:|---:|---:|---:|
| dev_p0500_S1_r001 c100 | 176.67 | 181.56 | 292.65 | 302.09 |
| dev_p1000_S1_r001 c100 | 266.73 | 273.75 | 393.06 | 372.75 |
| dev_p0500_S2_r001 c100 | 253.77 | 247.08 | 425.87 | 475.38 |
| dev_p1000_S2_r001 c100 | 298.04 | 294.34 | 387.49 | 341.99 |
| dev_p0500_S3_r001 c100 | 362.58 | 342.78 | 489.88 | 489.86 |
| dev_p1000_S3_r001 c100 | 398.91 | 361.33 | 486.62 | 418.65 |
| dev_p0500_S4_r001 c100 | 509.11 | 516.05 | 669.61 | 722.92 |
| dev_p1000_S4_r001 c100 | 374.18 | 381.18 | 443.46 | 489.47 |
| dev_p0500_S5_r001 c100 | 665.14 | 724.9 | 2641.67 | 1887.72 |
| dev_p1000_S5_r001 c100 | 344.08 | 341.67 | 2184.31 | 2072.04 |
| dev_p0500_S6_r001 c100 | 349.99 | 351.88 | 557.55 | 560.71 |
| dev_p1000_S6_r001 c100 | 382.47 | 364.83 | 433 | 426.25 |
| dev_p0500_S1_r001 c050 | 281.44 | 277.16 | 416.4 | 448.8 |
| dev_p1000_S1_r001 c050 | 431.62 | 445.11 | 508.59 | 449.25 |
| dev_p0500_S2_r001 c050 | 628.93 | 606.09 | 811.54 | 781.22 |
| dev_p1000_S2_r001 c050 | 485.61 | 451.6 | 455.15 | 402.41 |
| dev_p0500_S3_r001 c050 | 511.98 | 528.17 | 734.51 | 796.48 |
| dev_p1000_S3_r001 c050 | 348.44 | 349.3 | 423.33 | 431.5 |
| dev_p0500_S4_r001 c050 | 984.61 | 954.42 | 1043.48 | 1136.89 |
| dev_p1000_S4_r001 c050 | 687.58 | 694.23 | 607.28 | 640.77 |
| dev_p0500_S5_r001 c050 | 1037.59 | 882.02 | 2598.86 | 2617.83 |
| dev_p1000_S5_r001 c050 | 553.14 | 577.23 | 2684.18 | 2064.14 |
| dev_p0500_S6_r001 c050 | 621.97 | 665.78 | 847.91 | 731.21 |
| dev_p1000_S6_r001 c050 | 550.94 | 546.5 | 522.69 | 507.42 |
