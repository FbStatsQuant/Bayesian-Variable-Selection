# PR #52 independent review

Reviewer: **Codex GPT-6.1 Sol, high**, on Owls, 2026-11-16 (local time).

## Verdict: REJECT

Counts: **0 CRITICAL, 4 MAJOR, 3 MINOR**. The CLI works on the nominal path and ordinary restart is bit-identical, but it can silently resume a checkpoint made from different inputs. Admission still follows setup expansion, and the default N-swap budget changes the small-p science. Fix the major findings before merging this T5 dependency.

## Scope and exact tree

- PR: https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/52, `exp/P1M-wp3-islandcli` → `exp/P1M-engine`.
- Reviewed and built detached head **45fcd32de63fb2f213ff1836f5be081c5dcd01c3**.
- Fetched base at review start: **f188ae2a7d7c5d75577023f9e8be645f47bd75bb**; merge base **544e38f9e3eb9db66351ea8eeb40b43305810471**.
- Exact requested comparison: `git diff $(git merge-base origin/exp/P1M-engine 45fcd32d) 45fcd32d`; saved as [PR52.diff](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/PR52.diff). This is a head review, not a speculative integration build.
- Read the review brief and its binding Sandbox, WP3 brief, BUILD_COMMON, PROTOCOL, ENGINEERING_SPEC §0-v2/§0-v3 and relevant reference sections, shared binding INTERFACES **v0.1.15**, and PR39/PR46 reviews. No production-source edits, commits, pushes, GitHub comments, sub-agents, NOTS, or approval requests. Reviewer scratch/builds/logs and TMPDIR are under this worktree's `.rc_tmp/`; scratch remains for the manager.

## Findings

### 1. MAJOR — checkpoint resume does not bind the three input content hashes

**Location:** [src/island/island_cmd.cpp:226](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:226) (new CLI checkpoint wiring and call at 247); inherited fingerprint at [src/island/island_run.h:372](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:372).

The CLI computes data/setup/calib content hashes but only puts them in the output's `inputs`. None reaches the checkpoint fingerprint. That fingerprint checks seed, schedule, scalar dimensions, yty, start normaliser/J, arithmetic and binary, but omits the actual input identities and neighbour graph. INTERFACES §5.1 explicitly requires file identity by `content_sha256` for restart.

**MEASURED reproduction:** after a genuine SIGKILL left both checkpoint generations, I changed only setup's neighbour graph to the valid empty CSR graph, rewrote the setup hashes, and updated a calibration copy's `meta.inputs.setup.bin` coherently. All normal CLI input/hash checks pass. I copied the saved checkpoints to the new output stem and reran the CLI against these changed inputs. It exited **0**, resumed from **step 10**, and labelled the output with the new input hashes. Its science hash is **0xcf1aa1859340729f**; an uninterrupted run on those exact changed inputs gives **0xea06206c7a4bb828**. Non-meta sections differ. Expected: **invalid_input / exit 13**, with no estimates.

Evidence: [independent.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.log), [foreign_resume.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/foreign_resume.log), [changed_fresh.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/changed_fresh.log), [independent.py](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.py). The changed setup content hash is `8abe0dfc8eeb21df18a4d4fb3d9c8b9fed06a75e751dff9a3767955d12c1aaad`.

**Fix:** pass the verified data/setup/calib content hashes into the checkpoint identity and verify them before loading state. Keep this independent of execution parameters such as threads/G/tile. Add the changed-input negative test alongside the same-input kill/restart test. The lower-level omission predates this diff; the new production CLI now exposes it and has the identities available to fix it.

### 2. MAJOR — admission occurs after input/setup allocations, including in plan-only mode

**Location:** [src/island/island_cmd.cpp:206](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:206), especially load_start/load_neighbours at 215–216 before the first plan at 237; [src/calib/calib_run.cpp:131](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/calib/calib_run.cpp:131), 139, 153 and 176; [include/v4/island/setup_load.h:15](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/include/v4/island/setup_load.h:15).

`island` loads data, copies partition/table arrays, and fully rebuilds `dep::Start` (including sampler tables, duplicated logr storage, codes_by_size/sub_cum and conditional distributions) before checking its budget. The new calibration plan-only path also expands the Start before it can report the island plan. With large production tables these are substantial allocations and can cause OOM before the promised deterministic `resource_limit`. The design document acknowledges the gap, but INTERFACES §7's pre-allocation admission rule remains binding. StartView is an implementation solution, not an exception to that rule.

**MEASURED allocation probe:** after warming the binary/libm block outside the measurement, the small n=60,p=30 fixture with **budget=1 byte** still requests:

| call | operator-new calls | cumulative requested bytes | largest request |
|---|---:|---:|---:|
| island, run | 5,291 | 816,860 | 5,248 |
| island, plan-only | 3,880 | 470,377 | 5,248 |
| calibrate, run or plan-only | 1,006 | 174,176 | 10,176 |

These are allocation requests, **not peak RSS**. The source establishes their setup-size growth. Evidence: [allocation_warm.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/allocation_warm.log) and [allocation.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/allocation.cpp). The unprimed probe is also retained; its first-call libm self-test allocations are excluded from the figures above.

**Fix:** compute the input-dependent plan from metadata/mapped section lengths and the persisted setup size distribution before expanding/copying setup or constructing stores. Refuse first. A mapped Start can then avoid the expansion entirely. The calibration side inherits PR39 MINOR-6 / PR46 MAJOR-2; preserve its whole-task resident+inputs+island admission fix when integrating, and apply the same ordering to this new island command and its plan-only path.

### 3. MAJOR — default B=14 changes the small-p kernel relative to calibration/core

**Location:** [src/island/island_cmd.cpp:221](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:221); calibration uses the actual budget at [src/calib/calib_run.cpp:178](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/calib/calib_run.cpp:178) and [include/v4/calib_run.h:26](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/include/v4/calib_run.h:26). The new test reference duplicates the default at [tests/test_island_cmd.cpp:151](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/tests/test_island_cmd.cpp:151).

The command hard-codes `B=14` unless explicitly overridden. The coded budget is `min(isqrt(n), isqrt(p),16)`, so n=60,p=30 uses **B=5**, as the command's own preceding calibration does. B is the number of N-swap labels per round, changes the shuffled order/address positions and compat stream consumption, and changes actual output. It is not merely a block-size or execution parameter. Fourteen is correct for the n=200 large-p rung but not for supported small-p cases.

**MEASURED**, same n=60,p=30 fixture, seed 77, island 2, calibration schedule:

| mode | CLI / in-process B=14 | in-process core-budget B=5 |
|---|---|---|
| V | 0xffce07af01f718de | 0x072cb398a4a33495 |
| compat | 0x87206ab8beaaae97 | 0x0ef08329972b0419 |

In each mode the CLI matches every non-meta section of the B=14 in-process run; it differs from B=5. Thus the supplied same-bits test can pass while testing the wrong configuration. Evidence: [independent.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.log), [probe.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/probe.cpp); an explicit `--B 5` check is in [bit_fix_check.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/bit_fix_check.log).

**Fix:** derive B from the same authoritative setup/calibration budget (or the shared `calib::budgets(D.n,D.p)` helper), use it in both planning and execution, and refuse inconsistent science overrides where the manifest/frozen setup is authoritative. Include at least one n,p case whose B is not 14, with the reference configured independently from the CLI default.

### 4. MAJOR — manifest conflict detection loses explicit arguments before --manifest

**Location:** [src/island/island_cmd.cpp:101](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:101) (the new `param` comparison); common parsing at [src/cli/main.cpp:51](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/cli/main.cpp:51).

The common parser copies manifest params directly into `args`, overwriting any earlier explicit value. The new island parser then compares that overwritten object with the same manifest, so it cannot detect the conflict. The claimed refusal in either argument order is false for fields with the same key, including seed, id, Rp and the params.island form.

**MEASURED**, manifest params seed=77,id=2,Rp=4:

- `island --seed 78 --manifest M --plan-only 1` exits **0**; with `--seed 78` after M it exits **13**.
- The same before/after split is **0/13** for `--id 3` and `--Rp 1`.
- The PR's before-manifest test uses `--island` against manifest `id`, so it misses the overwritten-same-key case.

The new calibrate manifest path also accepts an explicit conflicting seed after the manifest: seed 78 produces a completed calibration for a manifest that freezes seed 77. The subsequent island can then refuse its calibration/manifest seed disagreement.

Evidence: [independent.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.log), [extra_checks.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/extra_checks.log), [cal_conflicting_seed.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/cal_conflicting_seed.log).

**Fix:** retain explicit arguments separately, parse the manifest independently, then compare scientific values before applying authority/defaults. Add before/after tests for identical keys, and validate the calibration seed against its manifest as well.

### 5. MINOR — an insufficient calibrate plan-only budget hides the minimum island budget

**Location:** [src/calib/calib_run.cpp:139](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/calib/calib_run.cpp:139) before the new island-plan block at 143.

`calibrate --plan-only 1 --mode V --n 200 --p 1000000 --threads 3 --mem-budget 1000` correctly exits **11**, but returns before adding either `plan_only` or `island_plan`. The requester therefore cannot inspect the island's minimum budget precisely when resizing is needed. With no budget, the new plan does expose the floor: **49,221,484,050 bytes** at G=1 for this sizes-only, three-thread estimate, excluding setup inputs and including calibration resident state.

Evidence: [cal_budget1000_plan.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/cal_budget1000_plan.log), [cal_1M_plan.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/cal_1M_plan.log).

**Fix:** construct and return the complete plan, including its island floor, on both admitted and refused plan-only outcomes; use the budget to select status/G without suppressing the plan.

### 6. MINOR — a refused compat island is written as a law-mode file

**Location:** [src/island/island_cmd.cpp:247](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:247); inherited admission result at [src/island/island_run.h:802](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:802) and writer at [src/island/island_file.cpp:23](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_file.cpp:23).

The admission-refusal `IslandRun` does not carry `cfg.compat`, tier or the configured grid. The new CLI always writes that result; the writer infers mode from `r.compat`. A compat request with `--mem-budget 1` exits **11** but writes a container with header mode **2** and `meta.mode="law"` (T=0, empty grid), while its task record says compat. Estimates are correctly absent. This loses the request identity and can make downstream validation report a mode mismatch instead of the original resource refusal.

Evidence: [extra_checks.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/extra_checks.log), [compat_refused.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/compat_refused.log).

**Fix:** initialise refusal results with the complete scientific configuration, or pass the authoritative mode/config explicitly to the writer. Test refusal-file metadata for all modes, not only V.

### 7. MINOR — CLI checkpoints still use the provisional non-contract container

**Location:** new checkpoint exposure at [src/island/island_cmd.cpp:228](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:228); inherited serializer at [src/island/island_run.h:117](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:117).

INTERFACES §5.1 specifies kind-8 containers and SHA-256 section verification for `island_r.ckpt.{a,b}`. Actual checkpoints start with **SMCV4CKP** and use a custom FNV-checksummed payload. `smcbvs4 info --in saved_V.b` exits **13**, bad magic. Normal same-binary resume works, but the standard inspection/verification tooling cannot read these files. This is inherited serializer debt newly exposed by the production command, rather than a new serializer regression.

Evidence: [extra_checks.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/extra_checks.log), [checkpoint_info.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/checkpoint_info.log), saved checkpoints [saved_V.a](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/saved_V.a) and [saved_V.b](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/saved_V.b).

**Fix:** migrate the checkpoint wrapper to `fmt::K_CKPT` while retaining streamed payload I/O and two-generation atomic replacement, or obtain an explicit contract amendment before treating this format as production-compliant.

## Verification

### Requested quick suite

C++ result: **129 test cases, 0 failed, 0 check failures**. WP5: **17 driver tests passed**; competitor harness passed with optional packages unavailable; install guards **9 checks passed**. WP4 R golden: **528,081 checks, 0 failures**, including whole-calibration comparisons through WP3's runner, T9 merge/tail equivalence, T10 paths, and bounded/blocked-rule checks. **The complete quick runner exited 0.**

The core-header goldens `golden_island_vs_core_engine`, `golden_compat_island_vs_core_serial_stream`, and both calibration-island goldens pass. The seven p=20,000 peak-memory rows also pass their plan ≥ 1.10 × observed increment check; that validates the existing island execution plan, not pre-admission setup allocation timing. Log: [quick.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/quick.log).

Command, from the worktree root:

```sh
export TMPDIR="$PWD/.rc_tmp/tmp"
export P1M_TEST_ROOT="$TMPDIR"
export OMP_NUM_THREADS=3
nice -n 19 bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3 --keep > .rc_tmp/quick.log 2>&1
```

`--keep` avoids the runner's final scratch deletion. All review test processes were constrained to at most three CPU cores; builds use the runner's `-j3` and `nice -n 19`. Compiler GCC 11.5.0, glibc 2.34, default x86-64-v2 bit/class-A build. Build provenance is clean head 45fcd32d, executable SHA-256 `afde97f770cd9fc281a706992dd83ff59a4d759fc2daac43d5c2918adabf5e40`. No fixtures were regenerated, and no source edits were made to accommodate test outcomes.

### Independent actual-kill and same-bits checks

The additional harness is [independent.py](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.py), backed by the small fixture/reference helper [probe.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/probe.cpp); full results are [independent.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-d3b0edd3-6d57d84494497161/.rc_tmp/independent.log). Every executable was run with `nice -n 19` and at most three cores. The fixture is n=60,p=30, seed 77, r=2,N=2500,L=6,Hm=4, with a CLI-produced calibration for each mode.

| mode | bridge stages | saved checkpoint steps a/b | SIGKILL result | resumed step | uninterrupted/resumed science hash |
|---|---:|---|---|---:|---|
| V | 13 | 4 / 10 | -9 | 10 | 0xffce07af01f718de |
| compat | 14 | 3 / 6 | -9 | 6 | 0x87206ab8beaaae97 |

I killed the actual CLI process after both atomic generations existed (`--ckpt-every-s 1`), waited for its death, saved the two generations, and reran the same command. **All non-meta section hashes match** an uninterrupted run in both modes, as does `IslandRun::hash()`. Meta is excluded as required by §5.1 because it contains timings. The same full outputs match independent in-process runs for the CLI's actual B=14 configuration in both compat and V; the B=5 comparison isolates finding 3. This is a small-p T6 check, not the required future 10^5 T6 gate.

### Calibration status correction

Successful CLI calibration now exits **0**, the record has `status="completed"`, `cal_status="ok"`, and the binary retains its internal `meta.status="ok"`. Checked independently in both V and compat, as well as through the requested suite. Inspection and a status probe confirm unchanged internal failure mappings: resource_limit→11, numerical_failure→12, schedule_limit→16, grid_failure_no_escalation→16. The budget refusal CLI paths still return resource_limit/11. This resolves PR46 MAJOR-3.

### Other observations and integration context

- Input path lookup by base name, the driver's `params.id` alias, frozen N/grid/L/Hm/tier, seed disagreement with calib, and output input hashes are wired coherently on the nominal driver path. Final RNG addresses keep FINAL role and tier/iter zero; provenance uses the frozen calibration tier. Compat forces one thread and the final stream 9+r; V selects class A / label-major.
- The new v4_cmd target removes the v4_bit↔v4_a cycle noted in PR39 MINOR-4; bit compiler flags are preserved. No arithmetic kernel implementation changes are part of this diff.
- Changed tracked files are all under engine_v4; no new tracked file approaches 50 MB, no p² structure or hard-coded external output path was introduced, and `git diff --check` passes.
- This exact head still contains the already-reviewed calibration-plan debt from PR46: resident-only early admission, `kbar=max(8,|mode_S|+1)` instead of setup q90, and `26+4k` entry accounting omitting the 4-byte per-model index in `calib_memory_plan`. They are inherited, not additional new PR52 findings/counts. Preserve the corresponding WP4/PR45 fixes when integrating; finding 2 explains the newly exposed allocation-order problem. This head's old setup-only fixture is not evidence that a PR46-integrated suite passes.
- The new calibration-island plan is useful and addresses PR39 MAJOR-2 on the non-early-return path. Sizes-only estimates explicitly omit setup inputs; they must not be used as a complete 1M task request. No 10^5/10^6 fit or NOTS measurement was run in this review.
