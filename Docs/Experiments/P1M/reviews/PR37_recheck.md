# PR #37 re-check: WP4 calibration pipeline, review fixes (M-1..M-6, m-1..m-6)

- **Reviewer:** Opus 5.5 (high), independent of the author. Date: 2026-11-16. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** PR #37, branch `exp/P1M-wp4-calib-run`, head `7a950fde` (fix commit on top of `a69a2b5e`, which merges `exp/P1M-engine` @ `4c238a32`, INTERFACES v0.1.12). Re-checked diff: `a69a2b5e..7a950fde` (10 files, +457 / −96: `calib.h`, `calib_backend.h`, `calib_run.h`, `wp4_io.h`, `calib_run.cpp`, `wp4_io.cpp`, golden R + harness, `test_wp4.cpp`, `test_wp4_io.cpp`).
- **First review:** `PR37_review.md` (ACCEPT-WITH-FIXES: 6 MAJOR, 6 MINOR). Fix list: PR comment of 2026-11-16.
- **Contract:** INTERFACES v0.1.12 (§5, §7), DECISIONS D-1, D-26, D-29; WP3_DESIGN §1.11 (v0.6, on `exp/P1M-wp3-calib`).
- **How:** detached worktrees, read only, in `/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-37` (removed after). Nothing pushed, commented or branched; the local merge commit lived only in a detached temp worktree. Owls, `nice -n 19`, `taskset -c 0-2`, `--threads 3`, one suite at a time, no NOTS. Only my own PIDs were touched.

## Verdict: **MERGE** (all 6 MAJOR and 6 MINOR fixed; 4 new MINOR and 3 INFO to disposition, none blocking)

RESULTS_PLACEHOLDER
