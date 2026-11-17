# PR #46 independent review

Reviewer: **Codex GPT-6.1 Sol, high**. Date: 2026-11-16 (Owls).

## Verdict: ACCEPT-WITH-FIXES

**Not ready to merge until findings 1–3 are dispositioned/fixed and the integrated suite is green.**
Counts: **CRITICAL 0 · MAJOR 3 · MINOR 1**. Finding 3 is inherited from the
current base's live-runner integration, rather than introduced by PR #46.

Reviewed [PR #46](https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/46),
`exp/P1M-wp4-calib2` → `exp/P1M-engine`, against the review brief, WP4 brief,
BUILD_COMMON, ENGINEERING_SPEC §0-v3/§0-v2, PROTOCOL, and the shared-clone binding
INTERFACES **v0.1.14**. This is a review of the N-1–N-4 follow-up to PR37_recheck,
including integration with the newly merged WP3 runner. No remote changes,
comments, branch updates, sub-agents, or NOTS work.

## Exact tree and integration

- PR head: `1293109463d96b0b88caa14aee070789394030d7`.
- Freshly fetched base: `8b7f89bea4f5c89fa2dcd26a5b87e1b63e359b2d`, including
  PRs **#40, #39, #42, #43**.
- Detached local integration tree: `ac57330b9b974c2f97b42c76c03bc394292e6de2`.
  This is a tree object, not a pushed or branch commit.
- The merge has **one conflict**, in `src/calib/calib_run.cpp`: the PR's old
  "runner not available" stub conflicts with the base's working WP3 runner.
  For testing I retained the base's live-runner block and all other automatically
  merged PR changes. Thus the test uses the PR's q90 plan and stop-export guard
  with the base's actual runner and unchanged whole-budget forwarding.
  The author must resolve this conflict the same way; retaining the stub would
  disable calibration. All source references below are under
  `Scripts/SMC_BVS/engine_v4/`; where line numbers differ, both are given.
- PR #45 was **not merged into the tested tree**. Its proposed contract and
  overlapping store-accounting fix were inspected separately.

## Numbered findings

### 1. MAJOR — the new required size law breaks the integrated calibration command test

**Where:** `src/calib/calib_run.cpp:97` on the PR head (`:112` integrated);
`tests/test_island.cpp:930–943` on the current base/integrated tree.

The command now requires `setup.bin.size_logmass`, correctly following §7.
However, the actual command fixture `calibrate_command_end_to_end`, added by the
merged WP3 work, never fills `SetupView::size_logmass`. Its file augmentation
adds `size_cum`, but not `size_logmass`. The stricter command therefore throws
before the first compat calibration, so none of that test's compat/law/V and
1/3-thread comparisons runs.

**Measured:** the unchanged integrated test, also run separately with the proper
scratch test-root setting, fails with:

```text
invalid_input: calibrate: setup.bin has no size_logmass (INTERFACES §5; the memory plan's k)
1 test cases, 1 failed, 1 check failures
```

**Fix:** populate `S.size_logmass = st.size_logmass` before `write_setup_min`, or
add that section along with `size_cum`. Keep the command's required-section
check. Re-run the existing command test in all four configurations and the
integrated suite. This is a fixture integration repair, not a reason to weaken
the production contract.

### 2. MAJOR — the strengthened admission check still occurs after full setup allocation

**Where:** `src/calib/calib_run.cpp:95–104` on the PR head (`:110–119`
integrated); `src/merge/wp4_io.cpp:517–558`.

N-2 changes the condition to `plan.total > budget`, but `read_setup` still runs
first. It copies `logr`, partition arrays, and every table store into owning
vectors, reconstructing the stores, before the command computes its plan or
returns `resource_limit`. These are substantive allocations scaling with the
tables and up to 80p stored models, not just bounded header parsing. Even
`--plan-only 1` follows this path.

**Measured reviewer probe:** on the PR's valid small V file fixture, tracking
global C++ `operator new` only during `calib::run` with `mem_budget = 1` and
`plan_only = 1` records **689 allocations, 129,640 requested bytes, largest
single request 7,984 bytes**, before the returned `resource_limit`. This excludes
direct malloc and mapped pages. Source inspection identifies the full setup
copies and store reconstruction before the check. At the 1M rung, an inadequate
budget can therefore encounter allocation failure before the promised
deterministic refusal.

**Fix:** separate a bounded plan reader from the full setup loader. Read the
dimensions, authenticated size-law section and section lengths/file sizes;
derive k and perform admission first. Load tables/stores and construct the
calibration state only after admission. Add a test that fails if those large
allocations occur before an obviously insufficient-budget refusal. The changed
inequality is correct, but it does not finish the §7 "before any allocation"
requirement. The early full loader is inherited code; this PR's N-2 guarantee
still needs to address it.

### 3. MAJOR — successful calibration is recorded as invalid_input by the CLI (inherited base issue)

**Where:** integrated `src/calib/calib_run.cpp:151–160`,
`src/cli/main.cpp:100`, `src/common/status.cpp:17–19`;
`tests/test_island.cpp:955`.

The live runner returns `rec["status"] = cal_status_name(co.status)`, which is
`"ok"` on success. `main` passes that field to `status_from_name`, which accepts
only task names (`completed`, etc.) and throws `invalid_input` for `ok`. The
calib.bin is written successfully, but its sidecar becomes a failure record and
the CLI exits 13. The driver consequently cannot continue a successful fit.
The direct C++ command test would not catch this even after its fixture is
fixed: it explicitly expects the internal calibration name `ok` and bypasses
`main`.

**Measured reproduction:** I retained the golden's n = 100, p = 30 fixture,
added the exact core-produced `size_logmass` and neighbour CSR sections with
fresh valid container hashes, and ran the real binary:

```bash
.rc_tmp/build/smcbvs4 calibrate --mode V \
  --data .rc_tmp/full_golden_retained/files_AR0.9_n100_p30_s34/data.bin \
  --setup .rc_tmp/cli_status_meta/setup_complete.bin --seed 77 --threads 1 \
  --I_max 0 --out .rc_tmp/cli_status_meta/calib_cli_success.bin
```

It exits **13**, with `status: invalid_input` and
`reason: invalid_input: unknown status ok`. The 230,144-byte calib.bin exists
and its binary metadata says `status: ok`, N = 2,500, with a positive k_store.
The probe outputs, complete fixture and metadata verification are retained.

**Fix:** command JSON must use
`status_name(task_status(co.status))`; keep the internal/core calibration name
in a separate field if needed. Preserve calib.bin's internal `ok` convention.
Update the direct test to expect `completed`, and add a real CLI success case
checking exit 0 and a completed sidecar, not only an in-process command call.
This block comes from the current base (PR #39), retained when resolving the
merge conflict. Assign it to the integration/WP3/WP4 owner; do not attribute its
introduction to this PR's N-1–N-4 changes. It is nevertheless a concrete blocker
in the exact combined tree requested for this review.

### 4. MINOR — calibration accounting still omits the per-entry model index from v0.1.14

**Where:** `include/v4/calib_run.h:80`.

`calib_memory_plan` still uses `entry = 26.0 + 4.0 * kbar`. INTERFACES v0.1.14
§4.1 specifies **30 + 4k** bytes, including the four-byte model index. The live
store already has that index. At p = 1,000,000, k = 8, the helper returns:

```text
ledger          11,600,000,145 B
resident        18,640,000,233 B
total (inputs=0)30,240,000,378 B
```

Using the contracted entry cost increases each ledger estimate by
**800,000,010 B**, resident by that amount, and this two-ledger total by
**1,600,000,020 B**. This is an ESTIMATE/model discrepancy, not a measured 1M RSS
claim.

**Fix:** retain PR #45's `30 + 4k` correction when integrating the two PRs, or
bring that small correction here. PR #45 already contains the exact fix, so this
is a known integration dependency rather than a new unassigned store bug. The
N-1 meaning of the fields is correct independently of this byte estimate.

## Requested extra checks and other results

**Stopped-calibration export: PASS.** `include/v4/calib_run.h:117–126` wraps
export construction and scoring in `status == CalStatus::ok`. An independent
probe supplied a nonempty top store and an evaluator that throws if invoked.
Both a pilot admission/resource stop and a numerical stop returned their
original status, with **factory calls 0 and inherited models 0**:

```text
stop=resource_limit returned=resource_limit factory_calls=0 inherited=0
stop=numerical_failure returned=numerical_failure factory_calls=0 inherited=0
```

**N-1 field rule: PASS.** The header matches shared INTERFACES v0.1.14 §7 and
PR #45: resident is the calibration ledger plus export, without data/setup;
`mem_budget` is the whole task's budget. In the integrated command,
`resident_own = plan.ledger + plan.export_` and `island_budget = budget`
(`src/calib/calib_run.cpp:145–149`). WP3's runner adds resident to its
caller-supplied input term exactly once and does not subtract it from the
budget (`include/v4/island/calib_runner.h:39–45`). Its input term is excluded
from percentage headroom, preserving the exact additive boundary. The new q90
helper copies `plan_island`'s exp/add/threshold order and floor 8. The existing
`calibration_admission_n1_rule` test also passes: its complete plan is
181,607,825 B; plan − 1 refuses, plan admits, and removing the 123,456,789 B
resident contribution admits at the correspondingly reduced budget. Findings 2 and 4
qualify allocation timing and byte accounting, not this field convention.

**N-4:** both new refusal and plan-from-setup cases pass. The numeric-type check
in `read_calib` correctly refuses NaN/Inf serialized as strings, and normal
non-ok files expose no inherited estimates. Missing size-law sections remain
permitted for other `read_setup` callers and are refused specifically by
`calibrate`.

**Arithmetic/scale/discipline:** no scorer or transition arithmetic changed in
this PR. Bit kernels retain `-O2 -fno-math-errno -ffp-contract=off
-march=x86-64-v2`; the new exp sum is admission-only. At n = 200, p = 1M the
changed plan's arithmetic uses wide/double intermediates; no new p² storage or
32-bit overflow was found. All nine PR files are inside `engine_v4/`, the largest
is 62,028 bytes, and no new production hard-coded path was introduced. This
review performs overlap-sized tests, not a 1M feasibility/RSS validation.

The passing existing edge tests include exact ties and the binding k = K cap
in `wp4_tail_threads_vs_serial`, empty-model scoring, constant/drop/data outcomes
in the prep tests, and **231 forced-route score comparisons with zero
mismatches** (Cholesky, refactor and QR). Ordinary fixture scoring happened to
use Cholesky only; forced-route coverage is what checks the other routes. The
full golden's `same` compares serialized IEEE double bits, not tolerances, and
its T9 checks include stores, HPM/provenance, evidence, PIPs and logical counters.

## Test record (MEASURED)

Owls `owls.stat.rice.edu`, Intel Xeon Gold 6148, g++ 11.5.0, CMake 3.31.8,
R 4.6.0, glibc 2.34. Tests/builds ran at nice 19 on affinity CPUs 0–2, OMP threads ≤ 3,
OpenBLAS/MKL threads 1. Runtime/build scratch directories were inside the
worktree-root `.rc_tmp/`; the runner's required process-local TMPDIR pointed
there. No shared department tmp directory was used. The manager's later binding
update requires retention: **no scratch or other files are deleted**, and this
review's delivery path is `.rc_tmp/PR46_review.md`. The earlier draft under
`reviews/` is left in place. No source rollback/merge-abort cleanup is performed.

Initial runner command (from the worktree root):

```bash
env TMPDIR="$PWD/.rc_tmp" OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 19 taskset -c 0-2 bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh \
  --full --threads 3 --build-dir "$PWD/.rc_tmp/build"
```

- Standard unit/golden binary: **118 cases, 1 failed, 1 check failure**, exit 1.
  The sole failure is finding 1. This includes the R/C++ scorer/table fixtures,
  pinned-reference check, thread/restart checks, all seven p = 20,000 measured
  memory-plan configurations, the byte-exact N-1 boundary, and WP3 calibration
  compat/law/failure-ledger goldens.
- Targeted CLI/driver-manifest rerun with `P1M_TEST_ROOT`: **1 case, 0 failed**.
- Targeted calibration-command rerun with the same setting: **1 case, 1 failed**,
  reproducing finding 1.
- WP5 Slurm driver: **17 tests OK**; competitor harness **OK**, with missing
  optional packages reported explicitly and mocks tested; install script
  **9 guard checks OK** (no package installs).
- Independent stop-status/allocation/plan probe: **exit 0**, outputs above.
- Additional real CLI success-path probe: **exit 13**, finding 3; the binary
  output itself is completed (`meta.status = ok`) but the task sidecar fails.
- **FULL-level WP4 golden coverage: all 7/7 fixtures completed across retained runs, with zero reported failures.** The final p = 2,000 shard completed **1,316,886 checks, 0 failures** and wrote its saved result plus `RETAINED_GOLDEN_FINISHED`. Its exit **137** is the intentional retention exit. The first six full-level fixtures completed in the preceding retained invocation. There is **no claimed overall aggregate check count**, because that invocation ended before its summary.

The initial full golden completed all six cases through p = 1,000 with no
reported mismatches (including 141,484 checks of that fixture's WP3 calibration)
and reached the p = 2,000 case. The manager then issued the binding no-deletion
update. I paused the R process and outer runner before further cleanup, then
stopped only those two recorded PIDs with SIGKILL, so their exit handlers could
not remove the retained files. That initial full run is **NOT COMPLETED**.

The full golden is rerun from `.rc_tmp/wp4_golden_retained.R`, using the exact
already-compiled `wp4_test_core.cpp.R` wrapper / `sourceCpp_2.so` and copied
unmodified core R files from the first run. The scratch script changes only
loading, progress output and retention: every explicit filesystem `unlink` and
cleanup finalizer is omitted; all seven full cases and comparisons are retained.
Its final result is written to `full_golden_retained/review_result.txt` and
`review_result.rds`, with the `RETAINED_GOLDEN_FINISHED` log marker. It then
self-terminates with SIGKILL to avoid R's automatic session-temp deletion;
**exit 137 is expected for this retention wrapper**, so the saved result and
completion marker determine the test outcome. Errors have a distinct
`RETAINED_GOLDEN_ERROR` marker. The scratch script, modules, logs, fixtures and
session temporary files are all left for the manager.

That retained full invocation later ended unexpectedly with **SIGTERM (143)**,
after the p = 2,000 production-runner calibration had also matched core
(278,709 checks, zero failures). It did **not** reach its completion marker or
aggregate summary; the cause of SIGTERM is unknown. All six preceding cases
had completed with no reported mismatches. To finish full-level coverage, the
original runner's supported single-case filtering is used in
`.rc_tmp/wp4_golden_final_case_retained.R` for `AR0.8_n200_p2000`, with `level =
full`, the same settings/comparisons, and a new `final_case_retained/` output
directory. This is test sharding after interruption, not a reduction to quick.
The final-case shard's saved result now confirms completion of all seven
full-level fixtures across these retained runs. No overall check count is inferred from an
interrupted process.

```bash
env TMPDIR="$PWD/.rc_tmp" P1M_TEST_ROOT="$PWD/.rc_tmp" \
  PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 19 taskset -c 0-2 Rscript .rc_tmp/wp4_golden_retained.R \
  "$PWD/Scripts/SMC_BVS/core" "$PWD/Scripts/SMC_BVS/engine_v4" \
  "$PWD/.rc_tmp/full_golden_retained"
```

The unrelated WP5 full-only `wp5_gate_T7_closed_forms_vs_monte_carlo` may double
sampling to 2²⁸ per case over 23 fixtures. I stopped only my own `v4_tests` PID
with SIGTERM while it was running that gate, after about six minutes of the
initial runner. The runner then continued through its WP5 extras and the
**full WP4 golden**. T7 is **NOT COMPLETED** in this review; the later full-only
p = 100,000 measured-RSS case was **NOT RUN**. The standard unit suite was run
separately against the same binaries with:

```bash
env TMPDIR="$PWD/.rc_tmp" P1M_TEST_ROOT="$PWD/.rc_tmp" \
  OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 19 taskset -c 0-2 .rc_tmp/build/v4_tests
```

The requested full golden was neither reduced to quick nor case-filtered. It
compiles unmodified `core/` together with the test harness; its reference code
and original arithmetic are unchanged. The harness adds data faults, wrappers
and v4 calls. The unit pin check also verifies revision D's 20 core files.

The first full invocation omitted `P1M_TEST_ROOT`, so its CLI/driver-manifest
case also refused the worktree scratch path with exit 64. The driver explicitly
supports the environment setting `P1M_TEST_ROOT="$PWD/.rc_tmp"`; that individual
case was re-run with it. This environment-only failure is not attributed to PR
#46. The calibration fixture failure above reproduces with that setting present.

Scratch probe sources, outputs and the complete test tree are retained under
the manager's binding update. Nothing requires an approval or an outside write.


The final-case replay used the same command as the retained full invocation,
with `.rc_tmp/wp4_golden_final_case_retained.R` and output directory
`.rc_tmp/final_case_retained`. It finished on 2026-11-16 at 19:30 CT. The saved
result is `level=full checks=1316886 failures=0`; the original full invocation
remains recorded as interrupted, not passed as a single unbroken run.

## Retained evidence

- [Completed final-case result](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/final_case_retained/review_result.txt)
- [Final-case log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/final_case_retained.log)
- [Preceding full-level log (first six complete; later interrupted)](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/full_golden_retained.log)
- [Unit test log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/units.log)
- [Stop-status and allocation probe](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/probe.log)
- [CLI success-path status failure](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/cli_status_success.log)
- [CLI binary/sidecar verification](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/cli_status_meta/verification.json)
- [Retention-only script diff](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/retention_only.diff)
- [Source/module hashes](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7c9d334a-bdd389eba13a7741/.rc_tmp/golden_provenance.json)
