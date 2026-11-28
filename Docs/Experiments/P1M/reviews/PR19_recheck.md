# PR #19 re-check — review fixes at 9d2cad3 (`exp/P1M-wp5-competitors`)

Reviewer: Opus 5.5 (independent re-check), high effort. Briefs: `briefs/REVIEW_PR_template.md` and `briefs/BUILD_COMMON.md`.
First review: `reviews/PR19_review.md` (2 MAJOR, 7 MINOR) at 5064989.

**Scope.**
- The head is 9d2cad3, which is 5396a9d (a merge of origin/exp/P1M-engine d9d64f3) plus the fix commit.
- Against the merge base d9d64f3 the diff has 7 files, all under `engine_v4/`: `tools/competitors/*`,
  `tools/slurm/p1m_cells.py`, `tools/slurm/test_p1m_driver.py`, and 3 added lines in `tests/run_tests.sh`.
- `exp/P1M-engine` has since moved to f982ced (PR #22). `git merge-tree` shows that **PR #19 still merges cleanly**.

Checkout: detached worktree, read only. Nothing was pushed and no GitHub comment was made.

## Verdict: **MERGE**

- Both MAJORs are fixed and asserted in code. Each assert has a negative test.
- All 7 MINORs are fixed or labelled OPEN, as asked.
- Every number in MANIFEST_CELLS.md v0.2 matches the generator's output exactly.
- The install-script guard held against every path trick I tried. My one bypass needs the caller to override `$HOME`
  (R-1).
- The quick suite passes.

The three remaining findings are MINOR and do not block the merge; each is a one-line fix that can go in a later PR.

Counts: CRITICAL 0 · MAJOR 0 · MINOR 3 (new) · NIT 2.

## What I ran (Owls, nice 19, ≤ 3 cores)
TMPDIR was `/home/fb31/SMC_Engineering_Department/tmp/20261115-recheck-19`; I removed it afterwards.

- **`tests/run_tests.sh --quick --threads 3`: rc 0.**
  - 61 test cases, 0 failed, 0 check failures;
  - WP5 Slurm-driver tests: 17 OK;
  - competitor harness: OK (the packages are absent on Owls, as expected);
  - **install-script test: 20/20 checks OK**.
- **`p1m_cells.py --summary`, `--tsv` and `--plans`.** Results:
  - **259 fits** (260 TSV lines including the header);
  - **47 plans** holding **239 distinct run ids**, i.e. every fit except the 20 T8 rows;
  - every plan passes `p1m_driver.resolve`, with at most 7 fits per plan (≤ 150 tasks);
  - Σ `worst_case_core_h` = **52,968**.
- **Mutation test of the install order.** I took a copy of the script and restored the v0.1 offline route
  (tarballs in sorted order, `repos = NULL`). `test_install_script.sh` then **fails** on that copy: "aaadep … below floor
  after install", "not installed", "lock file". So the new test discriminates.
- **Online dry `--resolve`** against the public 2026-11-02 snapshot index, with `--dept` set to my tmp folder:
  - the top-level versions match the TSV;
  - nothing was installed; the only file written was the `tmp/` folder (its `r-install-*` temp was removed).

## Claim-by-claim

### MAJOR-1 — precision arms: own final and calibration seeds — **FIXED**
`p1m_cells.py:65-67, 132-135, 160-186`. Arm a gets final seed = data + 100·(10 + a) and calib_seed = data + 100·(20 + a).

On AR rep 1, for example, the 8 final seeds are 402021001…402021701 and the 8 calibration seeds are
402022001…402022701.

My own check:
- the 48 precision values are pairwise distinct;
- none of them equals any data seed or any non-precision engine seed;
- no precision (data, seed) pair is shared with another fit.

`check_seeds()` asserts the same things inside `expand()`, and a negative test (two arms forced onto one seed) raises.

The 32 remaining shared (data, engine) pairs, at most 3 fits each, are all the intended pairings:
- T-s1 / V-s1 / A3 on the AR overlap reps;
- T vs V;
- the 1M N = 10⁴ self-check.

**Caveat (already stated in MANIFEST §2).** `calib_seed` and `grid_refine_m` are placeholders. The driver passes `params`
through, but nothing in `engine_v4` reads them yet. The independence only holds once WP4 wires `calib_seed` into the
calibration stream.

### MAJOR-2 — A3 paired — **FIXED**
`p1m_cells.py:93-94, 189-196`. A3 is now 10 AR + 5 BLK, 15 fits. Every A3 data seed has a default-partition V fit
(seed 1, N = 2,500, R′ = 16). `check_a3_pairing()` asserts this, and a negative test (an extra BLK rep-10 A3 fit) raises.

### Seed rule — **FIXED**
Data seed + 100·k, with the asserted widths: rep 1..99, n/100 1..99, D and R ≤ 9 (`:122-123`). The roles k = 0 / 1 /
10 + a / 20 + a fall in the otherwise-zero 10²–10³ digits, so the rule is one-to-one by construction. Seed 2 moves from
+50 to +100.

`check_seeds()` also asserts that every engine seed is k ∈ {0, 1}, or a precision final k ∈ [10, 20). The rep = 100
test raises. The docstring is corrected (R = 1 for T8).

### Fit and cost totals — **all reproduce exactly**
| | claimed | generator |
|---|---|---|
| fits / plans / planned fits | 264 → 259; 47 plans; 239 | 259; 47; 239 |
| science 10⁴ | 156 fits, 2,010 | 156, 2,010 |
| ablations | 482 | 482 |
| planned excl. D | 18,252 → 18,199 | 18,199 |
| × 1.25 | 22,749 | 22,749 |
| A + D with contingency | 26,940 → 26,874, +9.2% vs 24.6k | 26,874 (26,874 / 24,600 = 1.092) |
| Δ | −50 fits, −3 ablations = −53; −66 with contingency | ✓ (5 × 10; 5 × 10 × 0.06; 53 × 1.25) |
| two trims | ≈ 24.2k | 26,874 − 1,575 (20 × 63 × 1.25) − 1,058 (6 × 141.05 × 1.25) = 24,241 ✓ |
| worst case of the 47 plans | 52,968 | 52,968 |

**MANIFEST_CELLS.md v0.2** (untracked; shared doc). I checked every number in it against the code:
- §2 per-row costs: AR 70 / 120 / 160 / 280; AR-weak 140 / 180 / 160 / 280; IND 35 / 40 / 80; BLK 35 / 50 / 80; ADJ-OPP
  30 / 80; NULL 40; A3 150; 10⁵ 480 / 461 / 192 / 192; 10⁶ 2,889 / 963 / 963 / 3,600;
- precision ≈ 35 / ≈ 141 per fit, 2,117 in all;
- the fit counts, including the "(8 in overlap)" and "18 + (2)" notes;
- §3 totals and trims; §5 worst case.

**All match exactly.**

### ACCEPTANCE.md — **FIXED**
- 12 / 8 / 5 records, which match `ALL_METHODS` in `p1m_competitors.R:27-28`, including `ols_oracle`.
- The worst case is 48 + 128 + 160 = **336** ✓.
- The equal-CPU MCMC is recorded as OPEN (§4); MINOR-4's I_max / resampling arms are labelled OPEN and not costed
  (MANIFEST §2 and §6).
- `--only` now accepts 4|5|6, 1eK or p.

### Install script (MINOR-1/2/3) — **FIXED**
| claim | evidence |
|---|---|
| `P1M_TEST_ROOT` removed | It no longer appears in the script. `P1M_TEST_ROOT=$HOME --dept ~/not_dept` exits 64. |
| `--dept`, `--download-only` and `--from-dir` resolve inside the department, else exit 64 | See the guard probes below. |
| R TMPDIR under `$DEPT/tmp`, removed after | `:56-58`. The test checks that no `r-install-*` folder is left. |
| `--apply` needs CONFIRM=yes | `CONFIRM=no --apply` exits 65 and creates no library. |
| Offline tarballs in dependency order | `write_PACKAGES` on a symlink index in R's temp folder, then `contriburl` + `dependencies = NA` (`:110-116, 139`). Tested, and the test fails on the old route (mutation test above). DIR is left read-only. |
| No user library | `unset R_LIBS R_LIBS_USER`, and `.libPaths(lib)` (`:68, 84`). The dry run shows only `/usr/lib64/R/library : /usr/share/R/library`. |
| Below-floor packages are reinstalled; floors are re-checked after the install | `:90-97, 126, 146-148`. Tested: 0.1 → 0.2 upgrade; floor 0.3 unmet gives exit 1. |
| The lock file covers the closure | `:150-155`. Every package of the installed closure is recorded with its version, LibPath, Built and DESCRIPTION MD5. The test checks both dummy packages and their LibPath. |

**Guard probes.** The following were all **refused with exit 64**:
- `--dept /tmp/x`;
- `$ROOT/../x`, `$ROOT/./tmp/../../x`;
- the prefix tricks `${ROOT}_x` and `${ROOT}x`;
- a symlink inside the department pointing to `/tmp`, with `/x` or `/../x` appended;
- a **dangling** symlink to `/tmp/nonexistent`, with or without `/x`;
- `--download-only /tmp/x`, `--download-only $ROOT/../SMC_Engineering_Department_evil`, and a dangling symlink;
- `--from-dir /tmp`.

Correctly **accepted:** a symlink inside the department that points back into it.

**Bypass:** `HOME=…`. See R-1.

## Remaining findings (none blocking)

### R-1 (MINOR) — The department root comes from `$HOME`, so an environment override moves it (install_competitor_packages.sh:42)
`HOME=/tmp/fakehome --dept /tmp/fakehome/SMC_Engineering_Department` passes the guard and runs. I verified this in dry
mode: it created `/tmp/fakehome/SMC_Engineering_Department/tmp`. I have removed it.

This is a deliberate override, not an accident, so the risk is low. Still, it is the one environment variable that
moves the guard.

**Fix.** Take the root from the passwd database, e.g. `ROOT=$(realpath -m "$(getent passwd "$(id -u)" | cut -d: -f6)/SMC_Engineering_Department")`.

### R-2 (MINOR) — The dry run now writes, and a mistyped `--dept` inside the department leaves an empty folder behind (:56)
`mkdir -p "$DEPT/tmp"` runs in every mode, including the default dry run. A dry run with `--dept $ROOT/typo` therefore
leaves `$ROOT/typo/tmp`. My probes left `$ROOT/x/tmp` and a folder named `$ROOT/<newline>x/tmp`, which I have removed.

This stays within the department rule. But it contradicts "dry run: nothing written" in spirit, and it litters the
department folder.

**Fix.** Create RTMP under `$ROOT/tmp`, which always exists. Alternatively, create `$DEPT/tmp` only in the
apply/download modes.

### R-3 (MINOR, docs) — "+19 dependencies" in ACCEPTANCE.md §1 was measured with the user library visible
Now that the user library is excluded, the dry `--resolve` on Owls (bare R 4.6.0 site library) plans **52 packages:
the 10 listed + 42 dependencies** (MEASURED). These include the ggplot2 stack, which varbvs pulls in. The figure of 19
came from v0.1, where `~/R/…` was on `.libPaths()`.

On NOTS, the number depends on what the R/4.5.2 module's site library already has.

**Fix.** Write "up to 42 dependencies (bare R; MEASURED Owls 2026-11-15), fewer if the module library has them".

### NITs
- `--download-only ""` skips the guard, because the check is `[[ -n $DL ]]`. It then fails in R ("zero-length 'path'
  argument", exit 1) after fetching the index, and writes nothing. Reject an empty value at parse time.
- `p1m_cells.py:138`: `5000 if rung == 3` is dead code, since no cell has rung 3 (the 5k anchor is block-costed).

## Regression check
- The per-block costs for overlap, precision, 10⁵ and 10⁶ are unchanged from the first review. The only changes are
  the intended −5 fits and −53 core-h.
- The first review's `TestCells` still passes, now with updated counts.
- The plan grouping and cap are unchanged.
- No file outside `engine_v4/` is touched.
- The merge with d9d64f3 brings in only `exp/P1M-engine` content, and the PR still merges cleanly into the current
  f982ced.
