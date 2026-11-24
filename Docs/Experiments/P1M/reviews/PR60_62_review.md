# Review of PR #60 (O4a, 8d1c66bd) and PR #62 (O4b, b5afcc61, stacked on #60): WP7 O4 restart at scale

Reviewer: independent sub-agent (Sonnet 5.5), 2026-11-17, Owls, own worktree. Checked out `b5afcc61` detached. #62's head contains #60 unchanged; the #62 diff over #60 touches different hunks of `island_run.h`, and `ckpt_sum.h` is identical in both. Everything ran under `<worktree>/.rc_tmp/` (TMPDIR, `P1M_TEST_ROOT`), `nice -n 19`, at most 3 threads. I deleted nothing. Scratch kept in `.rc_tmp/` (`cks/`, `fx/`, `kr1/`, `t6run/`, `tmp/`). I ran `run_tests.sh --quick --keep`, so the script does not `rm -rf` its golden dir.

## Verdicts

| PR | Verdict | CRITICAL | MAJOR | MINOR |
|---|---|---|---|---|
| #60 O4a: parallel, thread- and chunking-independent checkpoint checksum, `SMCV4CK2` | **ACCEPT** | 0 | 0 | 3 |
| #62 O4b: `--stop-after-s` / exit 22, `restart` plan key, T6 plan + `p1m_t6.py` | **ACCEPT-WITH-FIXES** | 0 | 0 | 5 (findings 4–8; 4–6 should-fix) + 2 INFO |

No functional defect in either engine path. #62's fixes concern the driver output: byte-identity with the key off, a missing `ends.jsonl` record, and a kill-2 detection filter. All three are small.

## Tests run

- `tests/run_tests.sh --quick --keep` on the #62 head (cold build, ~35 min wall on a loaded host, load average ~15).
  - `v4_tests`: **184 test cases, 0 failed, 0 check failures**. These include `checkpoint_checksum_is_chunking_and_thread_independent` (0.48 s), `checkpoint_of_the_older_format_is_refused`, `time_stop_chain_equals_uninterrupted` and `island_command_time_stop_chain` (18 s).
  - WP5 Slurm-driver tests: **OK, Ran 33 tests** (includes the new `TestRestartAndT6`). Competitors and install script: OK.
  - WP4 golden: **540419 checks, 0 failures**.
- My own checks, independent of the builder's tests (details below):
  - A checksum fuzz against a separate Python implementation of the spec.
  - Real `smcbvs4` kill / resume / torn / old-format / soft-stop runs at p = 2000, n = 200, mode V, seed 502020001, T = 12.
  - Reproduction of the builder's `p1m_t6.py` locally.
  - A driver comparison against the base `exp/P1M-engine` and an end-to-end run of the generated `stage_islands.sbatch` with the real binary.
- #60 was not built on its own. Its diff is `ckpt_sum.h` (new), `island_run.h`, `INTERFACES.md` and `test_island.cpp`, all contained in the stacked head. The suite above covers it.

## (1) Checksum: PR #60

I compiled the PR's `ckpt_sum.h` into a standalone tool and compared it with a separate Python implementation of the documented algorithm: 1 MiB blocks, FNV-1a 64 per block, FNV-1a 64 over `(length, block hashes in order)`. The test file was 5.3 MiB of random bytes.

- **Thread and chunking independence:** the value is identical, and equal to the Python reference (`8cbd26537215580a`), at 1, 3 and 8 threads, for the whole region and for 9 write chunkings: random, 1 B, 4 KiB, B−1, B, B+1, 3B+7, 64 MiB and random multi-MiB. 0 mismatches.
- **Detection:** all of these changed the value, and the tool agreed with Python each time.
  - A flipped byte at 0, 1, B−1, B, B+1, 2B, the middle and the last byte, and each of the 8 bit positions of one byte.
  - Truncation by 1 byte, to a block boundary, to block boundary + 1, and to empty.
  - One appended zero byte.
  - A swap of two different 1 MiB blocks, a swap of two adjacent bytes, and a rotation by one block.
  - 0 of 24 mutations went undetected. Swapping two identical blocks leaves the file unchanged, so it is not a mutation.
- **The real checkpoint:** I recomputed the block checksum of the payload (file[32:]) of real checkpoints with the same tool, at 3 threads and random chunking. It equals the header field every time, including for files written at 1 thread. Each file's length equals `32 + len`.
- **Old format:** a checkpoint with magic `SMCV4CKP` makes `island` exit 13 with `invalid_input: checkpoint …island.ckpt.a is of the older format (serial checksum, before WP7 O4): remove it or finish the run with the binary that wrote it`. No island file is written and the checkpoint files are kept. It is refused, not read as "no checkpoint". Refusal also fires if only the older generation carries the old magic.
- **Scale at p = 10⁶:**
  - The big arrays (`putv` of the store's `v`, `hash`, `off`, `len`, `pool`) go through the parallel path. Only the ≤ 1 MiB tails use the memcpy path.
  - `total_` is `size_t` and `nb` is `size_t`. The 64 MiB read buffer is the only new memory. No 32-bit limits found.
  - Block hashes are 8 B per MiB, about 80 kB for 10 GB.
  - Inside a block FNV is still serial, about 1 ns/B. 10 GB over 48 threads is about 0.2 s, against the old serial 10–13 s.

Findings for #60:
1. MINOR: `WP3_DESIGN.md:462` and `:610` still describe the container as magic `SMCV4CKP` with an FNV checksum. Update them to `SMCV4CK2` and the block checksum.
2. MINOR: `ckpt_sum.h:8` mentions `of_stream`, which does not exist. `BlockSum::of_region` is used only by tests, so it is dead code in production. It is harmless. Either note it as a test and mapped-file helper or drop it.
3. MINOR: the `INTERFACES.md` header line still says v0.1.20, while the changelog goes to v0.1.23. This follows the file's own convention (line 684: "the header line moves with those PRs (WP1)"), so it is only for the WP1 owner to bump.

## (2) Resume correctness (real SIGKILLs): PR #60 and #62

At p = 2000, n = 200 the uninterrupted island is `0xaedbf7ddf79a9605`. It has 26 non-meta sections and 80 s at 1 thread.

My own harness (killing at 1 thread, resuming at 2) gave:

- SIGKILL **after the second checkpoint generation** (both `.a` and `.b` present):
  - Exit was −9 and there was no island file.
  - The state was `.a` = step 2 and `.b` = step 4, and both checksums verified independently.
- SIGKILL **mid-write** of the resumed process: `island.ckpt.a.tmp.<pid>` was present at the kill, and `.a` (step 2) and `.b` (step 4) were intact.
- Resume at 2 threads, G unchanged:
  - `resumed_from_step` = 4.
  - The stale `.tmp.<pid>` was removed.
  - The checkpoint files were removed on completion.
  - **The output hash and all 26 non-meta section hashes equal the reference.**

Torn checkpoint, starting from the state of the first kill (`.a` = 2, `.b` = 4, newest = `.b`), resuming at 2 threads:

| Damage to the newest generation | Result |
|---|---|
| truncated to half | resumed from the other generation (step 2), hash and sections equal the reference |
| truncated by 1 byte | same |
| one byte flipped in the middle | same |
| both generations flipped | no usable checkpoint, fresh start (`resumed_from_step` −1), hash and sections equal the reference |

Builder's `p1m_t6.py` reproduced at 2 threads, with `--ckpt-every-s 4` and 2 kills:

- All 11 checks are true.
- Kill 1 was after 11.7 s at the second checkpoint. Kill 2 was 7.4 s into the resumed process, during the write of `island.ckpt.a.tmp.3328450`.
- The final run resumed from step 5.
- The output hash `0xaedbf7ddf79a9605` and all 26 sections equal the reference, and the checkpoint files are removed.

Both matched the builder's description.

## (3) Soft stop (`--stop-after-s`): PR #62

I ran a chain with S = 12 s, alternating 1 and 2 threads.

- Attempts 1–4 each exited **22**. The record has `status` "completed", `island_status` "interrupted_resumable", `reason`, `stopped_after_step` and `resumed_from_step`, and **no `island_bin` and no island file**.
- `stopped_after_step` rose 6 → 10 → 17 → 21, and `resumed_from_step` on each attempt equalled the previous stop. The newest checkpoint file on disk had exactly that step and a valid independent checksum.
- Overshoot past S was 1.8–3.1 s, one step plus the write. The stop is at a step boundary, after `save_ckpt` returned. `save_ckpt` throws `io_error` on any failure and fsyncs the directory, so exit 22 cannot follow an incomplete checkpoint. `main.cpp` overwrites 22 if the record write fails.
- Attempt 5 finished (exit 0), resumed from 21. Its hash and sections equal the reference, and the checkpoint files were removed.
- `maybe_ckpt(step, stop, last_step)` never stops at the final step, `T+L+Hm`, which is the loop's last step (`island_run.h:741`, `:827`). `stop_after_s` counts from the start of `run()`, so the checkpoint load counts. Each attempt makes at least one step of progress.
- **An island that finishes before S**, with `--stop-after-s 100000` against the same command without the flag:
  - Both exit 0 and the sections and hash are identical.
  - The records differ only in the `island_bin` path (different `--out` dirs).
  - No checkpoint files are left.
- **Refusals:** S = 0, S = −3, S = `abc` and `--ckpt 0` with S all give exit 13 and write no file. The engine also refuses a calibration island or an adaptive schedule.

Findings:
- No CRITICAL or MAJOR issues here.
- INFO: the stopped record reports `T` = the grid length minus 1 (12), while the island ran 21+ steps. `stopped_after_step` is on the T+L+Hm scale. This is fine but may confuse a reader.
- INFO: the margin (`max(300 s, 15 % of the limit)`) must cover the step in flight plus checkpoint write and the double `check_stores`. At 10⁶ the step and write times are unmeasured. The calibration pilot's cost rows should be used to confirm it.

## (4) Driver `restart`: PR #62

- **Attempt count and worst case.** T5 plan with `restart {attempts: 3}`:
  - Worst case was **894.0 core-h** = 382.0 base + (3−1) × 16 islands × 48 CPUs × 20/60 h (512.0). This matches Σ attempts × CPUs × limit for the islands.
  - The task count was 21 + 2 × 16 = **53**. `submit.sh` has `for att in $(seq 2 3)`.
  - The ledger row, the `submit.sh` header and the CLI summary all print 894.0. A `core_h_cap` of 400 refuses the plan.
  - `attempts` is validated 1..6, and `margin_s` ≥ 0 and below the limit.
- **Dependency graph.** Attempt k+1 uses `--dependency=afterany:<attempt k>`. The `isa_check`, `merge` and `eval` jobs use `afterok:$ji` after the loop, so they wait for the **last** attempt (also checked by the builder's stub-sbatch test).
  - A failed island writes `.failed` and every later attempt repeats its exit code, so merge never starts on a real failure.
  - An island still unfinished after the last attempt exits 22, and merge does not start.
- **No infinite resubmission.** There are `attempts − 1` extra arrays, at most 5. No script resubmits itself.
- **End to end with the real binary.** I generated a 2-island plan (p = 2000, limit 3 min, margin 165 s, 4 attempts) and ran the generated `stage_islands.sbatch` locally for island 1, attempts 1–4, with the real binary and the `p1m_manifest.py` `--manifest` path.
  - Attempts 1 and 2: "soft stop … (checkpoint written)", exit 0.
  - Attempt 3: finished, `island_1.done` written.
  - Attempt 4: "already finished", the binary was not called.
  - `output_hash` = `0xaedbf7dd…`, equal to the uninterrupted reference. The CLI accepts `--stop-after-s` alongside `--manifest`.
- **Key off: not byte-identical** (finding 4).

### Findings for #62

4. **MINOR, should-fix.** With the `restart` key off, the output is not byte-identical to the base `exp/P1M-engine`. I generated the A2, P7 and T5 example plans from the base driver and from this PR with the same `--now`.
   - The `stage_*.sbatch`, `build.sh`, `env.sh` and manifests are byte-identical.
   - `submit.sh` gains one blank line (the empty `{retry}` placeholder line, `p1m_driver.py:650`). The A2 and T5 batches are affected.
   - `plan.resolved.json` gains `"t6_only": false` (`:142`).
   - Every batch gets a new file `p1m_t6.py`, so `SHA256SUMS` changes.
   - Suggested fix: put the retry block's trailing newline inside the `retry` string so an empty value leaves no line. Do not set `t6_only` unless the key is present. Copy `p1m_t6.py` only when `t6` is present. Or state in `T6_AND_RESTART.md` that the stage scripts and manifests, not the whole batch directory, are unchanged. The existing `test_stop_s_in_the_command` checks only that `stop-after-s` is absent. A byte-comparison test against a stored `submit.sh` would pin this.
5. **MINOR, should-fix.** The restart-mode islands body leaves the stage through `exit 0` / `exit 22` / `exit "$rc"` (`p1m_driver.py:403–420`) before the generated `ends.jsonl` line, so no "end" record is written for a finished, soft-stopped or failed attempt. In my end-to-end run `starts.jsonl` got a record per attempt and `ends.jsonl` got 0. Nothing in the repo reads `ends.jsonl` yet, but it is the provenance log. Suggested fix: write the end record in an `EXIT` trap, or before each `exit`, with the attempt number and exit code.
6. **MINOR, should-fix.** `p1m_t6.py:56`: the "during write" detector globs every `*.tmp.*`, not the `.tmp.<proc.pid>` of the process just started. A stale `.tmp` from a previous kill (only if that kill landed mid-write) would fire kill 2 before the process has loaded and removed it. Probability is negligible with `--ckpt-every-s 20`. Fix: match `base + ".ckpt.[ab].tmp.%d" % proc.pid`.
7. MINOR: the "Worst case of this file" line in `stage_islands.sbatch` (`:310`) and the `submit.sh` header's `ncalls` / "Job graph" comment (`:626`) describe one attempt. For the T5 restart plan the file header says 256.0 while the plan total is 894.0. This is cosmetic, because the ledger and summary are right.
8. MINOR: a mixed plan (a `t6` section without `t6_only`) is not refused. `submit_t6.sh` would print the full fit's `worst_case_core_h` as T6's cost (`:685–689`). Either refuse it (`t6` implies `t6_only`) or print `wc6`. The shipped plan has `t6_only: true` and prints 40.0, so there is no impact today.
9. INFO: `afterany` makes merge wait for all `attempts` arrays even if every island finished in attempt 1. The extra tasks cost seconds of billing, but each waits in the queue for 48 CPUs, so wall time grows. This is documented and acceptable.
10. INFO: a hard kill at the limit with the default `--ckpt-every-s 600` and no earlier checkpoint resumes from scratch. This is documented in `T6_AND_RESTART.md`. It stays within the worst case printed.

## (5) T6 plan: PR #62

- `plan_T6_1e5.json` resolves to **40.0 core-h** worst case (48 CPUs × 50 min), cap 50, 1 task. 40.0 ≤ 40.
- The generated directory has `stage_t6.sbatch`, `submit_t6.sh`, `build.sh` and helpers.
  - There is no `submit.sh`, `stage_setup`, `stage_calibrate`, `stage_islands`, `stage_merge` or `stage_eval`.
  - `submit_t6.sh` makes exactly one call, `sbatch --array=1-1 stage_t6.sbatch`, behind `CONFIRM=yes`, the department guard and the `SHA256SUMS` check.
  - `build.sh` builds and submits nothing. The commands in `T6_AND_RESTART.md` match the generated files.
- `stage_t6.sbatch` reuses the T5 `data.bin`, `setup.bin` and `calib.bin`, with `--kills 2 --ckpt-every-s 20 --max-seconds 2700` and `--time=00:50:00`. The Slurm limit bounds the final resumed run.
- It only kills processes it started, by PID. The only deletions are stale `island.bin*` / `island.ckpt*` in its own `--work` dir.

## Discipline

All changes are inside `engine_v4/`. No hard-coded user paths in code. No large files; the largest new file is `p1m_t6.py` at 176 lines. The contract lines v0.1.22 and v0.1.23 match the code: magic, exit 22, record fields, and the `restart` / `t6` / `t6_only` keys.

## Summary of what to fix before merge

- #60: nothing blocking. Do the doc touch-ups (findings 1–3) with the next WP1 pass.
- #62: findings 4, 5 and 6 (small); 7 and 8 optional.
