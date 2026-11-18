# PR #49 re-check (O2 = D-30 per-step cost records)

**Verdict: MERGE.** 0 CRITICAL, 0 MAJOR, 0 MINOR blocking; 5 non-blocking NITs/notes (below).
All 4 MAJOR and all 3 MINOR findings of the first review (`PR49_review.md`, REJECT at `fe8fda63`) are fixed in `0238b836`,
and the K1 merge (`81e89cea` of `544e38f9` + `769fe59b`) is integrated as the first review prescribed.

Reviewer: Opus 5.5-class review sub-agent, read only. Worktree detached at `769fe59b2c331007e6cb89d4edb232c6f2a2d9e1`.
Paths below are under `Scripts/SMC_BVS/engine_v4/`. I reviewed `git diff fe8fda63 0238b836` (fix round) and
`git diff 544e38f9 769fe59b` (O2 net of the K1 merge: 8 files, all under `engine_v4/`).
Note `origin/exp/P1M-engine` has since moved to `f188ae2a`; I did not re-merge it.

## Status of each first-review finding

| # | first review | status | evidence |
|---|---|---|---|
| 1 MAJOR | sidecar not exactly-once over checkpoint/restart | **FIXED** | `cost_log()` island_run.h ~L460: at the first write in a process the sidecar is rebuilt (header + `res.cost[0..n-2]`, i.e. the rows of the checkpoint the run continues from) into `<path>.tmp.<pid>`, then `rename`d over `<path>`; later lines are appended. Duplicate suffix, missing row, torn tail and a fallback to the older checkpoint all disappear. Test (c) variants 0-3 (orderly, lost last line, torn tail, repeat resume from the same checkpoint) at steps 0 and 3. My probe P2: newest checkpoint generation corrupted, resume falls back to step 4 (also with a different thread count), `sidecar_equals` holds. |
| 2 MAJOR | checkpointed rows lose finalized timing | **FIXED** | Rows are contiguous intervals closed by `cost_close()` right after the step's ledger sync, before `maybe_ckpt`; the checkpoint's own seconds go to the next row. No post-hoc `cost_complete()` remains. Test (c) does `memcmp(&r2.cost[i], &r1.cost[i], sizeof(StepCost))` on every raw field of rows 0..s (`static_assert(sizeof(StepCost)==8*35)`: no padding). My probe P2 repeats this after a fallback resume. |
| 3 MAJOR | rows != island totals; final check unassigned; failed step | **FIXED** | Exit row (kind 4) is closed after `check_stores()` (the O1 exit check) and the result assembly, so it holds the last checkpoint, any partial/failed step, the exit I1 check (test asserts `t_check > 0` on the exit row). The checkpoint carries the lifetime totals at the last close (`mark_io`: 13 u64 + 15 f64, field by field); `cost_restore` re-seeds `res.ks`, store counters, `dup_base`, `elapsed_base`; `res.ks` store fields and `t_total` are now taken from `cmark`. `cost_sums_match()` compares rounds, sweeps, pairs, passes, flips, act_cols, offers, merges, dup, wall = `t_total`, compaction, check, checkpoint seconds: passes uninterrupted, interrupted, resumed (steps 0 and 3, 4 variants), budget (resource_limit) exit, particle-major. My probe adds resume then failure exit (P3: status 3 on both segments, sums hold) and fallback resume with different threads (P2). |
| 4 MAJOR | short write leaves a partial line | **FIXED** | One `write()` per line on an `O_APPEND` fd; `w != ln.size()` -> `ftruncate(fd, cost_off)` to the last whole line, log disabled, `IslandRun::cost_log_error` set, island unaffected. Test (d): hook `test_cost_log_short=3`, whole lines only, trailing `\n`, status 0, hash unchanged. My probe P1 is the real path: `RLIMIT_FSIZE=2500` with SIGXFSZ ignored gives `short write`, a 2381-byte file of whole lines, `rows == T+L+Hm+2`, hash equal to the no-sidecar run. The sidecar is labelled non-authoritative in INTERFACES §5.1, `island.h` and v0.1.16; `meta.cost` is the authoritative record. |
| 5 MINOR | PM publishes unmeasured work as 0 | **FIXED** | `StepCost::kernel`; `cost_row_json` emits `"NaN"` for the label-major-only fields on PM rows (and `t_pm` on LM rows). Test (f) checks sweeps/passes/pairs/flips/act_cols/M/ratios/t_phaseA/t_phaseB are NaN, `particle_rounds` and `t_pm` numeric. My PM sidecar line (probe P4) shows it. |
| 6 MINOR | contract overstated | **FIXED** | §5.1: `rows` by status (completed = T+L+Hm+2; stopped = closed steps + exit row), matches the test; scope of "not hashed" now = `IslandRun::hash` / `meta.output_hash` / non-meta section hashes, container hash includes meta; counts are JSON numbers as a stated bounded-count exception to the hex rule (`Json(uint64_t)` throws above 2^53, so the writer refuses, not truncates); `"NaN"` rule; log non-authoritative. v0.1.16 line updated. Header-line version waits for PR #45 (WP1), stated. |
| 7 MINOR | calibration sidecar not wired | **FIXED (deferred, said so)** | §5.1: "Calibration islands get it from `calibrate --cost-dir` (WP7 O5); until then only `IslandConfig::cost_path` sets it". Claim narrowed; no false statement left. |

## K1 merge
- One `KernelStats::flip_evals` declaration (island.h L116, K1's comment); one increment `KS.flip_evals += nflip` (island_lm.h L303, K1's per-thread tally: packed-list length or dense valid-lane popcount). O2's `p - c.k` increment and duplicate declaration are gone (`grep flip_evals` lists only K1's sites plus O2's readers). `island_lm.h` differs from `544e38f9` by one line only: `KS.act_cols += nA` (serial).
- Slow-path decision made explicit: `flips` = fast-support additions only (K1 semantics), documented in INTERFACES §5.1 and `island.h`.
- O1's check-on-every-exit (`check_stores()` before the exit row), K1's bounded-scoring/NaN-test options and verbose diagnostics are intact. Under bounded scoring `flip_evals` is thread-schedule dependent; the resume test therefore compares only the law-determined totals (rounds, sweeps, pairs) across runs, and the sums-equal-totals check is per run: sound.

## Hashes
- Suite T3: bit `44a15bfc6fb8d233` (PM/LM, threads 1-3, all G/tile) and class A `d2df149413596a19`, identical to the values quoted in the PR comment; `golden_island_vs_core_engine`, `bounded_scoring_same_bits_bit/classA` pass.
- Island hash with the record on vs off: test (a) `r.hash()==h0` on, with the sidecar; (c)(d)(e) likewise after resume/short write; my probe P4 PM bit `d97b699a61b80299` with and without the sidecar (same value as the first review's PM probe). The in-memory record is unconditional, so "off" = no sidecar; the record writes nothing into any law output (counters are serial or per-thread-then-reduced).

## Tests run (Owls, `nice -n 19`, 3 threads, `OMP_THREAD_LIMIT=3`, `TMPDIR` and `P1M_TEST_ROOT` = `<worktree>/.rc_tmp/tmp`)
- Build `.rc_tmp/build` (Release), 0 warnings.
- `v4_tests cost_record_per_step`: **PASS**, 0 check failures (3.2 s).
- `v4_tests` (quick, i.e. without `--full`): **124 test cases, 0 failed, 0 check failures** (`.rc_tmp/suite.log`). I ran the binary directly, not `run_tests.sh`, because the script's `rm -rf` of the golden work dir and the competitor/install scripts conflict with the "delete nothing / write nowhere else" sandbox. The test binary's own `TmpGuard` removes its pid-named files, all inside `.rc_tmp/tmp`.
- WP4 R golden (`wp4_golden.R ... quick 3 --keep`): **528081 checks, 0 failures** (`.rc_tmp/golden.log`). WP5 Slurm-driver tests: **OK** (`.rc_tmp/driver.log`; bytecode off). Competitor-harness and install-script tests were not run (they write to default scratch paths); they are unrelated to this PR.
- Reviewer probe `.rc_tmp/probe/probe49.cpp` (+ `probe49.log`, includes the PR's `test_island.cpp` for its helpers): P1 real short write via `RLIMIT_FSIZE`; P2 newest checkpoint corrupted -> fallback + changed thread count + rows 0..4 bit-identical + sidecar equals rows; P3 resume then budget failure, sums = totals, sidecar = rows; P4 PM bit hash on/off and a PM row. **PASS**, 0 check failures.

## Non-blocking notes (none needs a fix before merge)
1. **NIT (doc)** island.h / INTERFACES: after a resume the lifetime record omits the previous process's work after its last row close (its last checkpoint write, exit check, assembly). island.h says so ("the dead job's work after its last row close is in neither"); INTERFACES §5.1 says only that rows sum exactly to `t_total`. Worth one clause so nobody reads `t_total` as the full job wall (relevant when sizing the 1M budget from resumed islands).
2. **NIT (doc)** INTERFACES §5.1: the exit row's `phi` is `"NaN"` (and kernel-unmeasured fields in it), which the "NaN" sentence does not list explicitly.
3. **NIT (wording)** the sidecar is rebuilt at the *first row close of the process*, not literally "at the start of every job segment". A segment killed before its first close leaves the old file until the next process rebuilds it; harmless for a non-authoritative log.
4. **NIT (cosmetic merge artefact)** `tools/bench_island.cpp`: the trailing comment "the pre-O1 behaviour (before/after comparisons)" now sits after the new `V4_COST_PATH` line instead of the `V4_CHECK_EACH_STEP` line.
5. **NOTE** `IslandConfig::test_cost_log_short` is a test hook in the production config struct (default -1 = off, one int compare per sidecar line). Acceptable, the same pattern as `test_corrupt_store_step`; the real failure path is covered by my RLIMIT_FSIZE probe, not by the PR's test.

No scale, discipline or hash concerns found: 8 files under `engine_v4/`, no hard-coded writable path, no large file, row = 280 B, all new work serial outside OpenMP regions. Production-scale overhead (p = 10^6) is still for the calibration/T5 gate to measure, as in the first review.
