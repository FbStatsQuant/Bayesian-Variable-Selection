# Review: PR #66 (WP6 K6: PR53/61 review minors)

Reviewer: Claude Sonnet 5.5. This review was independent of the author and used no sub-agents. It followed `REVIEW_PR_template.md`, including its Sandbox section (read from `origin/exp/P1M`, since the PR branch does not carry `Docs/`). Checkout: detached at `e7afdd11d33f49cd8265c46887cff0d1245f84a1`, the head of `exp/P1M-wp6-k6` (base `exp/P1M-engine` = `423decb5`). Diff reviewed: `git diff 423decb5 e7afdd11`, 4 files, +88 / -4, all under `Scripts/SMC_BVS/engine_v4/`.

| PR | Head | Verdict | CRITICAL | MAJOR | MINOR |
|---|---|---|---:|---:|---:|
| #66 K6 | `e7afdd11` | **ACCEPT** | 0 | 0 | 3 |

None of the findings changes a successful run or blocks merge. They are about how precisely the new failure test and the PR text describe the failing-run behaviour. Findings 1 and 2 are best fixed in this PR's text and test; finding 3 is optional.

Answers to the four requested checks:

| Check | Result |
|---|---|
| (a) Stop-after-failure cannot alter a successful run | **Confirmed** (section A) |
| (b) On a failing run, status, reason and every output field equal group admission | **Confirmed for status, reason and every exported output; not for the in-memory `IslandRun::terminal` or the pass counters** (section B, findings 1 and 2) |
| (c) Both strengthened tests fail without their fix | **Confirmed**, by negative controls I applied myself (section C) |
| (d) Build, quick suite, hashes | **Confirmed**: 193 / 0 failed, WP4 golden 540,419 checks / 0 failures, both hashes unchanged (section D) |

---

## A. (a) The stop cannot reach a successful run

**Diff.** `src/island/island_lm.h:74-78` adds one predicate to the admission loop:

```cpp
const bool failed = fail_any();                                   // island_lm.h:77
for (int gi : admit) if (next < end && !failed) { pid[gi] = next++; admit[na++] = gi; }
```

`fail_any()` (`island_run.h:192`) returns `fail.has` under the mutex. For a successful run, `fail.has` is false at every admission:

- **Where `fail` is written.** The only writers are `fail.record(...)` and `oom_guard` (`island_lm.h:188,415,417,418,531`, `island_run.h:190,670,671`). Every one of them leaves `fail.has == true` until the round ends.
- **How a round ends after a record.** A numerical failure is thrown by `throw_if_failed()` (`island_run.h:200-208`), which is called after every `lm_group` (`island_run.h:287-288`). That call is also the only place that clears `has` on the normal path. A non-numerical failure returns at the next `fail_fatal()` check (`island_lm.h:97,137,388,511,538`) and is then thrown the same way.
- **Consequence.** A run in which `has` was ever true throws, which makes it a failed run. So for any run that completes, `failed == false` at all admissions, and the `for` is character-for-character the old loop. Its outputs are therefore unchanged.
- **First admission.** `fail.has` is false at the top of every `lm_group`. It is cleared by `throw_if_failed` and by `rebuild_prefix` (`island_run.h:698`), and no earlier state leaves it set. So the initial fill of the window is unaffected.
- **Groups kernel.** For the non-rolling path, `count == gN`, so all particles are admitted at the first iteration (`next < end`), and a stop later does nothing, because `next == end` already.

**Bits.** This agrees with the measured hashes in section D, with the 193-case suite, and with the pre-existing `rolling_admission_same_bits_*` (threads 1 and 3, G 1/5/7/16/48, dense and bounded), all of which pass.

**Soundness of the stop itself (failing runs).** Admission goes in increasing particle index, so every particle admitted after a failure at index *i* has index greater than *i*. `FailSlot::record` (`island_run.h:182-186`) keeps the smallest particle index. So the reported failure is unchanged, provided that every smaller-index particle is still run to the end. The change guarantees this: in-flight particles are not stopped, only new admissions are. Smaller-index particles were all admitted earlier. The author's comment (`island_lm.h:74-76`) says exactly this and is right.

**Other changes in the diff.**

- **`ConsumerLog` / `test_consumers` (`island.h:44-46,120`; `island_lm.h:457-462`).** Both are test-only. The production cost is a null check per consumed label.
- **`test_consumers_by_slot` (`island_lm.h:126`).** This is a per-support branch, not a per-label one.
- **CLI.** Neither field is set by any CLI path: `grep` finds them only in `island.h`, `island_lm.h` and the tests.
- **Checkpoint fingerprint.** Neither field enters it.

---

## B. (b) A failing run versus group admission

### What I measured

I wrote two extra tests (reviewer-only, in `.rc_tmp/chk/.../tests/test_island.cpp`, not part of the PR). Each compares rolling admission against groups on a failing run: status, reason, `IslandRun::hash()` (which covers every law output, including the exported store for calibration roles), and the `ks` counters.

- **`zz_rv_failing_*`**: the PR's own poisoning (labels scaled by 1e200 and `-inf` in the start table), for bad sets {37,151,222}, {222}, {5,299}; both forms; also the Pilot calibration role with leaders on. G ∈ {1,2,3,5,7,16,48}, threads 1 and 3. **84 legs: 0 differences** in status, reason or hash; particle-rounds, passes and sweeps were also equal. In every one of these legs the failing particle is particle 1 (index 0, bridge stage 1), which matters for finding 2.
- **`zz_rv2_late_*`**: a **late** failing particle, using the existing `test_fail_indep` hook: stage ∈ {1,2}, victim ∈ {0,5,20,37,47}, G ∈ {1,3,5,7,16}, threads 1 and 3, in A, bit and Pilot-A forms. That gives 100 legs for each of the three forms, 300 in all.

### What equals and what does not

| Output of the failing run | Rolling vs groups |
|---|---|
| `status`, `reason` (message, particle, position) | **Equal in all 384 legs** |
| `IslandRun::hash()` with `keep_terminal = false` (every other law output, incl. the calibration role's replayed ledger and store) | **Equal in all 300 late legs and all 84 poisoned legs** |
| `IslandRun::terminal` (the partial-round population, `island_run.h:875`; included in `hash()` at `island_run.h:82`; default `keep_terminal = true`) | **Differs in 34 of 100 late legs for A and for bit** (68 check failures with `keep_terminal` left on). The no-stop code (negative control C, below) differs in 76 of 100 for A. So the PR reduces the difference but does not remove it. The Pilot role is equal in all 100 legs, because its failure path replays from the round-start snapshot (`rebuild_prefix`, `island_run.h:696`). |
| `ks.particle_rounds` / `passes` / `sweeps` | Same in the 84 poisoned legs. In the late-victim legs `particle_rounds` differs in 34 of 100 (A, bit) and 54 of 100 (Pilot-A), up to **+16** above groups, and sometimes below (e.g. A, stage 1, victim 5, G 5: groups 10, rolling 7). No-stop code: 76 of 100 for A, up to +47. |

### Why `terminal` is not a production output

`island_file.cpp:26` sets `done = (r.status == 0)` and the terminal support lists are written only inside `if (done)` (`island_file.cpp:71-77`). The only other consumers, `wp4_io.cpp:382-385` and `merge.h:277,292`, read what that file carries and refuse any non-completed island. Calibration islands set `keep_terminal = false` (`calib_runner.h:56`). So no file or merge input differs; the difference is visible only in the in-memory `IslandRun` of a failed island. Status, reason and every exported output are the same as group admission.

The `ks` counters are execution diagnostics. They already differ with G and threads on successful runs (the existing rolling test asserts passes drop 298 → 199), and `hash()` does not include them.

### MINOR 1: "same bits / every output equal to groups" is too strong for the failing run in memory

**Where:** PR text ("5 particle-rounds (= groups) ... same status and reason"); `tests/test_island.cpp:447-448` ("no more particle-rounds than the first window"); `src/island/island_lm.h:74-76` ("the round's work is discarded anyway").

**Evidence:** table above. For a failing run, `IslandRun::terminal` (when `keep_terminal`) and the counters `particle_rounds` / `passes` / `sweeps` can differ from group admission. "Same bits" holds for successful runs and for every exported field of a failing run. The code comment "the round's work is discarded anyway" is correct for the stores and for exports, but not for the population `P` that `terminal` copies: particles that finished their round before the failure keep their new state, and which particles those are depends on the admission pattern. Reproduce: add the extra test to a tree and run with `RV_FIELDS=1`; the only differing field is `terminal` (log: `.rc_tmp/logs/chk3.log`, lines `RVF ...: differing fields: terminal`). With `keep_terminal = false` all 300 late legs are equal in every field (`.rc_tmp/logs/chk4_kt0.log`).

**Fix:** say "same status, reason and exported outputs; the in-memory partial population and the work counters of a failed island are execution-dependent". Optionally clear `res.terminal` when `res.status != 0`, which makes the failing-run `hash()` and the file agree and removes the difference. That is a one-line change at `island_run.h:875` (`if (cfg.keep_terminal && res.status == 0)`), but it changes an in-memory field, so I leave it to the author.

### MINOR 2: the new failure test covers only the best case (failing particle 0 in the first window)

**Where:** `tests/test_island.cpp:449-470`; assertion at `:464` (`particle_rounds <= G`).

**Evidence:** in the PR's fixture the failing particle is index 0 in every leg (my `zz_rv_failing_*` reasons all read "bridge stage 1, particle 1"). Failure is therefore recorded in the first pass, before any slot is refilled, and the `<= G` bound holds trivially. It is **not a property of the algorithm**: with a late victim, rolling admission can run more particle-rounds than the first window and than groups (up to +16 in my sweep, e.g. victim 37, G 5: groups 40, rolling 41; victim 20, G 5, stage 1: groups 25, rolling 22 but G 16: groups 32, rolling 21). The test therefore cannot exercise the clause "particles already running finish: one of them may fail lower" (`island_lm.h:75`), nor the soundness argument in section A for a later victim. The existing `indep_proposal_failure_deferred_to_its_position` does cover a late victim (37) with rolling on, but only for status and reason, not for the hash.

**Fix:** add legs with a late victim through `test_fail_indep` (as in my `zz_rv2_late_*`) and compare `status`, `reason` and `hash()` with `keep_terminal = false` against groups. Replace the `<= G` assertion by one that holds in general, for example "rolling ran fewer particle-rounds than the same run without the stop" (needs a test switch) or simply `< N`. The negative control below shows the current assertion does catch removal of the stop, so this is about strength for late failures, not a hole in what is claimed for particle 0.

### MINOR 3 (optional): thresholds weaker than the measured behaviour

**Where:** `tests/test_island.cpp:442` (`caught >= 2` of 6 legs); `:523-527` (counting-hook control); the unconditional "rolling = groups" text in the printf of `rolling_consumer_digest`.

**Evidence:**
- **`caught >= 2`.** The bug changes the log in 12 of 12 legs (6 per form; counted in `.rc_tmp/logs/quick.log`, "(differs)"), so a threshold of 6 would hold. With `>= 2` a future change that quietly weakens the test would not be seen.
- **Control at 3 threads only.** The counting hook's own control (line 523-526) uses `num_threads(3)`. The 1-thread claim rests on the negative control (section C), not on an in-tree control. A one-line `num_threads(1)` control in that block would pin the `omp_get_level()` semantics.
- **printf text.** The text "log ... rolling = groups" is printed even on failure (visible in the negative control B output), which is cosmetic and mildly misleading in a failure log.

**Fix:** require `caught == 6`; add the 1-thread control; print "=" or "!=" from the comparison.

---

## C. (c) Negative controls (applied by me)

Each control is a patched copy of the tree under `.rc_tmp/neg*/` with its own build `.rc_tmp/build_neg*/`. The tracked sources are unmodified. Logs: `.rc_tmp/logs/neg*.log`.

| Control | Patch | Result |
|---|---|---|
| **A** (K2 regression; counting test with the new predicate) | `island_lm.h:92`: `draw_indep(..., nullptr)` (no reserved scratch) | `order_phase_allocates_nothing_in_parallel_{bit,classA}` **FAIL**, **1,490 allocations in the order-phase region at every one of the 8 legs: threads 1 and 3, G 16 and 48, both forms**. Exit 1, 8 check failures. |
| **A2** (same regression, old predicate) | as A, plus test line 39 reverted to `omp_in_parallel()` | The threads-1 legs count **0**; the threads-3 legs count 1,490. Still FAIL overall, but only through the threads-3 legs. This confirms that the predicate change is exactly what makes the 1-thread legs count (MINOR A-1 of the earlier review). |
| **B** (consumer order) | `island_lm.h:126`: `if (true) std::sort(v.begin(), v.end());` (slot order always, the pre-K5 code) | `rolling_consumer_order_observable_{bit,classA}` **FAIL**: all 6 legs per form (G 5/7/16 x threads 1/3) show rolling != groups, 12 check failures. In the same build `rolling_admission_same_bits_{bit,classA}` **still PASS** with the same hashes, so the hash alone is blind to this tie and the new log is what sees it, exactly as the review of #53/#61 said. |
| **C** (stop-after-failure) | `island_lm.h:77`: `const bool failed = false;` | `rolling_stops_admitting_after_failure` **FAIL** in all 4 legs: rolling runs **48** particle-rounds against groups' 5 (G 5) or 16 (G 16), at both thread counts. The reason is unchanged (the test's first check passes), as the author reports. |

The test's own built-in control (`test_consumers_by_slot`) also works: with the correct code it changes the log in 12 of 12 legs and never changes the output hash (the `CHECKF` at `:436`).

The log's key (`(xph << 40) ^ (ustage << 8) ^ (c.h ^ zob.key[j]) * golden`, `island_lm.h:458`) and its value (`pid << 32 | fpos`) are deterministic functions of the model and the particle, and the reduction is a `min`, so the log is order-free as the author argues. It records 70,113 entries, which matches the PR text.

---

## D. (d) Build, quick suite, hashes

Owls, gcc 11.5.0, `nice -n 19`, `make -j3`, threads 3, one job at a time.

| Item | Result |
|---|---|
| Command | `TMPDIR = P1M_TEST_ROOT = <worktree>/.rc_tmp/tmp`; `tests/run_tests.sh --quick --threads 3 --keep --build-dir <worktree>/.rc_tmp/build`. Log `.rc_tmp/logs/quick.log`. **Exit 0.** |
| C++ tests (portable build) | **193 test cases, 0 failed, 0 check failures** |
| New tests | `order_phase_allocates_nothing_in_parallel_{bit,classA}` (0 allocations in all 8 legs), `rolling_consumer_order_observable_{bit,classA}` (70,113 entries, rolling = groups in 12 of 12 legs), `rolling_stops_admitting_after_failure` (rolling 5/5/16/16 = groups): all PASS |
| WP5 | Slurm driver 38 tests OK; competitor harness OK (eight optional packages absent here); install script 9 checks OK |
| **WP4 golden** | **540,419 checks, 0 failures** |

**Hash matrix.** Binary `v4_bench_island` built with `-DV4_ISLAND_ISA=x86-64-v4`, `-DV4_TESTS=OFF` (`.rc_tmp/build_v4`). p = 2·10⁴, n = 200, N = 300, `geo:4`, L = 1, Hm = 1, tile 128, execution overrides cleared. Script `.rc_tmp/run_matrix.sh`, log `.rc_tmp/logs/matrix.log`.

| Form | PM G 64 thr 1,3 | LM G 64 rolling thr 1,3 | LM G 256 rolling thr 1,3 | LM G 64 groups thr 3 | LM G 256 groups thr 3 |
|---|---|---|---|---|---|
| A | `263474601a55acb1` | `263474601a55acb1` | `263474601a55acb1` | `263474601a55acb1` | `263474601a55acb1` |
| bit | `f9c6272ed1ffbae5` | `f9c6272ed1ffbae5` | `f9c6272ed1ffbae5` | `f9c6272ed1ffbae5` | `f9c6272ed1ffbae5` |

All runs report "same across thread counts". Both pinned hashes are **unchanged**: A `263474601a55acb1`, bit `f9c6272ed1ffbae5`. 300 is not a multiple of 64 or 256, so the rolling runs really re-admit. I did not build the x86-64-v4 test binary (the previous review did, for this code path unchanged by K6 except in the test-only hook).

## Contract, scale, discipline

- **Contract / scale.** No INTERFACES, file-format, memory-plan or arithmetic change. `fail_any()` takes one uncontended mutex per admission iteration, once per pass: negligible. No new allocation in the parallel regions (`ConsumerLog` is test-only). Index arithmetic untouched.
- **Discipline.** All four changed files are under `engine_v4/`. `git diff --check 423decb5 e7afdd11` is clean. No hard-coded paths, no large files. `island.h` gains `<mutex>` and `<unordered_map>` includes for a test-only struct; this has precedent (`test_order_phase`), but note that the public header now carries a test-only type.
- **Integration.** `exp/P1M-engine` was at `423decb5` when I fetched it (`git rev-parse origin/exp/P1M-engine`); the PR's merge base is that commit. I did not merge or build anything else.

## Sandbox

- **Location.** All builds, scratch, `TMPDIR` and logs are under `<worktree>/.rc_tmp/`. The extra tests live only in `.rc_tmp/chk/` and `.rc_tmp/negC/`.
- **Resources.** `nice -n 19`, `make -j3`, at most 3 OpenMP threads, one test suite or bench at a time.
- **Deletions.** I deleted nothing. `run_tests.sh` used `--keep`, so the WP4 golden work directory stays. The test programs' own cleanup of their temporary files under `.rc_tmp/tmp` is test behaviour that I did not intercept.
- **Sources.** Tracked sources are unmodified; HEAD is detached at `e7afdd11`. The negative controls and extra tests are patched copies.
- **No outside actions.** No push, no GitHub comment, no merge, no NOTS, no permission requests, no sub-agents.
- **Machine load.** Owls was loaded by other jobs (load average about 22) during the review, so absolute timings in the logs are not meaningful.
