# PR #19 review — WP5 competitor packages and install script (Sol F8); cell/seed manifest generator `p1m_cells.py` (Sol F7)

Reviewer: Opus 5.5 (independent of the author), high effort; brief `briefs/REVIEW_PR_template.md` (N = 19).
Scope: `exp/P1M-wp5-competitors` @ 5064989 into `exp/P1M-engine` (base d04a219). Two commits:
- 5ea9c1c: `tools/competitors/` ACCEPTANCE.md, competitor_packages.tsv, install_competitor_packages.sh;
- 5064989: `tools/slurm/p1m_cells.py` and a test in test_p1m_driver.py.

5 files, +390, all under `engine_v4/tools/`. Context: Sol F7, F8, F9; MANIFEST_CELLS.md; DECISIONS D-10, D-21, H-1;
REVIEW_disposition_sol F6. Checkout: detached worktree, read only.

## Verdict: **FIX FIRST** (ACCEPT-WITH-FIXES)

**The cost arithmetic reproduces exactly.** I recomputed it independently, including the ablation term. The
1M cells match D-10, and the 1M competitor set matches D-21.

**The install script never installs in the default dry mode.** Its department guard holds against `/tmp`,
`SMC_Engineering_Department_x`, `..` and a symlink pointing out.

Two **manifest design bugs** must be fixed before the manifest drives any submission (MAJOR-1, MAJOR-2). Each is a few
lines. Three small hardening items on the install script answer focus (a) directly (MINOR-1 to MINOR-3). Once these
are fixed: MERGE. A re-check of the diff is enough.

Counts: CRITICAL 0 · MAJOR 2 · MINOR 7.

## Tests and checks I ran (Owls, nice 19, ≤ 3 cores, TMPDIR `…/tmp/20261116-review-pr1819`, removed after)
- `test_p1m_driver.py`: **13 tests OK**, including the new `TestCells`.
- `p1m_cells.py --summary`, `--tsv`, `--plans`: **48 plans**. Every plan passes `p1m_driver.resolve`, and each has
  ≤ 150 tasks.
  - The plans hold 244 distinct run ids: every fit except the 20 T8 rows.
  - Σ `worst_case_core_h` = **53,378**, which matches "≈ 53k".
- **Fit count.** The TSV has **264 fits** (265 lines including the header); see MINOR-6.
- `install_competitor_packages.sh --no-modules` (dry, and dry `--resolve` against the public snapshot index):
  - It wrote nothing (the target library was not created).
  - The snapshot versions match the TSV and ACCEPTANCE.md exactly: glmnet 5.2, ncvreg 3.16.0, biglasso 1.7.2,
    bigmemory 4.6.6, L0Learn 2.1.0, susieR 0.14.2, varbvs 2.6-10, BAS 2.0.2.
  - The closure has **19 more packages**, as claimed.
- Guard probes. These were all refused with exit 64:
  - `--dept /tmp/x`;
  - `--dept ~/SMC_Engineering_Department_x`;
  - `--dept ~/SMC_Engineering_Department/../x`;
  - a symlink inside the department that points outside.

  **Accepted:** `P1M_TEST_ROOT=/home/fb31 --dept /home/fb31/not_dept` (MINOR-1).
- **Offline-route semantics.** Two dummy source packages, `aaadep` importing `zzzbase`, installed into a temp library
  with exactly the script's call: `install.packages(list.files(..), repos = NULL, type = "source", Ncpus = 3)`.
  **aaadep fails** ("non-zero exit status"), because the tarballs are installed in alphabetical order (MINOR-2).

## (a) Install script: never outside the department, never without the manager
- **Default is dry.** Nothing is written without `--apply` (`mkdir -p "$LIB"` happens only in apply mode, line 50) or
  `--download-only`.
- **Department guard.** `realpath -m` is applied to both `--dept` and the root, followed by an exact-or-`/`-prefix
  match (line 33). This is correct. The library, the lock file and every install go to `$DEPT/R/<ver>/…`, and
  `install.packages(lib = lib)` puts dependencies there too.
- **Gaps** (MINOR-1):
  - the test bypass is unrestricted;
  - `--download-only DIR` is unchecked;
  - TMPDIR is not set, so R builds in `/tmp`;
  - `--apply` has no confirmation gate. The Slurm driver's `submit.sh` has one (`CONFIRM=yes` plus SHA256SUMS), but
    here "manager only" is policy, not mechanism.

## (b) Counts and cost (all reproduced)
| block | fits (code) | MANIFEST | core-h (code) | MANIFEST |
|---|---|---|---|---|
| T8 exact | 20 | 20 | 50 | 50 |
| overlap 10⁴ | 40 (20 T + 20 V) | 20 + 20 | 2,500 (T 115 × 20 + V 10 × 20) | 2,500 |
| precision | 24 | 24 | 2,117 (35.3 × 12 + 141.1 × 12) | 2,117 |
| science 10⁴ | 161 | 161 | 2,060 | 2,060 |
| 10⁵ | 12 | 12 | 1,325 | 1,325 |
| 10⁶ | 6 (incl. the N = 10⁴ fit) | 6 | 8,415 | 8,415 |
| option D | 1 | 1 | 3,300 | 3,300 |
| fixed: gates 400, T5 200, 5k anchor 300, competitors 400 | — | — | 1,300 | 1,300 |
| ablations, 6% of V per distinct dataset | — | — | 485.4 (I summed: 10⁴ 1,950 + 10⁵ 1,325 + 10⁶ 4,815 = 8,090) | 485 |

**Totals:**
- planned **18,252**; × 1.25 = **22,815**;
- option D 3,300 × 1.25 = 4,125;
- A + D = **26,940**, which is **+9.5 %** against H-1's 24.6k.

All reproduce. The n-scaling c(n) = 120 + 0.9n gives factors 0.7 / 1.6 / 2.8 at n = 100 / 400 / 800, as used. The
dataset dedup is correct: shared overlap/science run ids are run once and costed to the overlap. The AR n = 200 count
of 12 + (8) and the AR-weak count of 18 + (2) match.

**D-10:** the 1M cells are AR-strong × 3, ADJ-OPP × 1 and AR-weak × 1, all at n = 200, plus the self-check.
**D-21:** the 1M competitors are lasso + 1 variational + SIS; this is in ACCEPTANCE.md.

## (c) Seeds
- **Data seeds** are unique per dataset (188 distinct values), all < 2³¹ − 1. Seed 2 (= data + 50) and the calibration
  seeds (= data + 71/72) hit no data seed of another dataset, and no engine seed. With the current rep counts there are
  **no collisions across cells.**
- Engine seeds are **not** unique per fit: 32 (data, seed) pairs are shared by 2–11 fits. Most of this is deliberate
  pairing (T vs V; A3 vs the default; the 1M N = 10⁴ self-check). But it breaks the precision study (MAJOR-1).
- The rule is collision-free only for rep ≤ 20 (MINOR-5).

## Findings

### MAJOR-1 — The precision study's final seeds are not independent (p1m_cells.py:51-52, 113-125)
**Evidence.** All 8 precision arms on a dataset get engine `seed` = data_seed. Only `calib_seed` differs (+71/+72).
On AR rep 1 this is the same seed as `4-AR-n200-r01-T-s1`, `…-V-s1` and `…-A3-exactlink-s1`, so 11 fits share
(402020001, 402020001).

REVIEW_disposition_sol F6 (ADOPT) requires **"independent calibration and final seeds"**, and MANIFEST_CELLS §2 says
"final seeds independent". The c1 and c2 arms differ only in calibration. Their final SMC runs share the Philox key, so
"uncertainty across independent fits" would be understated.

**Fix.**
- Give each precision arm its own final seed, e.g. data_seed + 60 + arm index (8 arms → +60…+67). With the current rep counts that
  stays clear of +50 and +71/72.
- Or draw the final seed from the calibration index.
- Assert in `expand()` that the precision arms' (seed, calib_seed) pairs are pairwise distinct.

### MAJOR-2 — A3 on BLK is unpaired for reps 6–10 (p1m_cells.py:72 vs 77)
**Evidence.** A3 is "exact complete linkage vs the 1M rule **on the same data**" (MANIFEST §2; the cell note). The BLK
A3 cell has 10 reps at n = 200, but the science BLK n = 200 cell has only 5. `4-BLK-n200-r06…r10-A3-exactlink-s1`
therefore have **no default-partition V fit** on their data. I checked this programmatically: these 5 are the only
A3 fits without a partner. Half of the BLK comparison would be missing, and this would only surface after the runs.

**Fix.** Either raise science BLK n = 200 to 10 reps (+5 V fits, +50 core-h, +3 core-h ablations), or cut the A3 BLK
cell to 5 reps. Add a test: every A3 data_seed has a default V fit.

### MINOR-1 — Focus (a): the install script's guards have four gaps (install_competitor_packages.sh:25, 33, 50-52)
- **`P1M_TEST_ROOT` is an unrestricted bypass, and no test uses it.** `P1M_TEST_ROOT=$HOME --apply --dept
  ~/anything` would install outside the department. I verified this in dry mode. Remove it, or as in PR #12 MINOR-8
  require it to lie inside `$TMPDIR` under the department. Also quote the pattern operand.
- **`--download-only DIR` is not checked.** Apply the same realpath/commonpath check, or document that DIR must be
  under the department on both hosts.
- **TMPDIR is not set.** R builds the 27 packages in `tempdir()`, which defaults to `/tmp`; department rule: never
  `/tmp`. Export `TMPDIR=$DEPT/tmp/r-install-<date>` (mkdir it; remove it after).
- **`--apply` has no mechanical gate.** Require `CONFIRM=yes` (as `submit.sh` does) so that a builder or agent
  cannot run it by mistake. Print the planned closure before installing.

### MINOR-2 — The offline route (`--apply --from-dir`) fails on its first pass (lines 91-94)
**Evidence.** `install.packages(<tarball paths>, repos = NULL)` installs in the order given, with no dependency
resolution. My dummy test reproduces the failure. For this closure, `biglasso_*.tar.gz` sorts before `bigmemory`,
`bigmemory.sri` and `BH`, so biglasso fails. The script then exits 1 with "FAILED to install". A second run works.

**Fix.** Run `tools::write_PACKAGES(from, type = "source")`, then
`install.packages(need, repos = paste0("file://", normalizePath(from)), type = "source", dependencies = NA)`. This
resolves the order exactly as the online route does. Also note that `need <- missing` (top-level only) is what is
compared; with a local repository the closure is computed the same way as online.

### MINOR-3 — "Every version from ONE snapshot" is not what gets pinned or recorded (lines 55-59, 80, 100-104)
**Evidence.**
- `have()` counts any package on `.libPaths()`, which includes the user library `~/R/…`. On Owls, jsonlite and digest
  come from there.
- A top-level package that is installed but **below its floor** is listed as "to install". The closure then drops it,
  because it is installed (`need <- cl[!have]`, line 80), so it is never upgraded.
- The final check (line 100) tests presence only, so the run reports success with a below-floor version.
- The lock file records only packages whose `LibPath == lib`. Dependencies satisfied by the module or the user library
  are not recorded.

**Fix.**
- Run R with `R_LIBS_USER=` (empty) and `.libPaths(c(lib, .Library))` during apply.
- Keep below-floor packages in `need`.
- Re-check versions ≥ floor after the install.
- Write the lock file for **every** package in the closure plus the competitor list, with version and LibPath.

### MINOR-4 — Precision-study arms in the prose are not in the manifest (MANIFEST §2; p1m_cells.py:51)
"I_max ∈ {0, 3} and systematic resampling (D-2, D-14) are compared on the N = 2,500 arms", but no arm carries these
parameters and none is costed. Either state that they are the same fits (and how), or add arms and their cost. This is
WP4's open item 1; it is fine to leave it open if it is labelled as such.

### MINOR-5 — The seed rule is collision-free only for rep ≤ 20, and nothing asserts it (p1m_cells.py:12, 125, 131)
- Seed 2 of rep r equals the calibration seed of rep r − 21 or r − 22 (+50 vs +70 + c), and equals the data
  seed of rep r + 50. The current counts (max 20 reps; seed 2 only at ≤ 10) are safe.
- The docstring says "collision-free" and "R = 3 = the 5k anchor / exact block", but the code uses R = 1 for T8, as
  MANIFEST says.

**Fix.** Assert that the union of {data seeds}, {seed-2 values} and {calibration seeds} has no unintended
coincidences, and that rep < 20. Fix the docstring.

### MINOR-6 — The fit count is 264, not 265 (commit 5064989 message; MANIFEST_CELLS.md "Executable form")
The TSV has 264 data rows plus a header (`wc -l` gives 265), and the per-block fits sum to 264. Of these, 244 go into
the 48 plans; the 20 T8 rows are block-costed and not planned. Correct the MANIFEST text, and give both numbers.

### MINOR-7 — Small items
- `--only` filters on p (`str(r["p"])`, line 157), but the usage line says `--only RUNG`. Accept a rung, or rename the
  option.
- MANIFEST §3, "the first two trims alone give ≈ 24.5k": this mixes a with-contingency trim (−1.6k) and a
  without-contingency one (−0.85k). With contingency on both: 26,940 − 1,575 − 1,058 ≈ **24.3k**.
- ACCEPTANCE.md:
  - The 10⁴ row's "11 methods" counts lasso_cv_min/1se as one method, but they are two records. Say so, or
    count 12.
  - Sol F8's 10⁴ equal-CPU model-space MCMC (same prior and scorer) is not in this package list. If the engine provides
    it, say so in §4; otherwise record it as open.

## Checklist items with no finding
- **Discipline.**
  - Every file is under `engine_v4/tools/`.
  - `p1m_cells.py` only writes the given `--tsv` and `--plans` paths. It has no `subprocess` and never submits.
  - Its plans carry `code_commit: UNSET-fill-at-freeze` and `kind: gated (needs HQ go)`.
- **Plans.** Groups are (block, p, n, mode, N, R′), with cap ⌊150 / (R′ + 4)⌋ = 7 at R′ = 16 and 2 at R′ = 64. The
  plan names are unique: 48 files, 244 distinct run ids, none overwritten.
- **Engine seed = data seed** is safe: role GEN is a separate Philox address domain (INTERFACES §3, v0.1.5).
