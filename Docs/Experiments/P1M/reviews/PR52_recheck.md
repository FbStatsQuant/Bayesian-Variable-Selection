# PR #52 re-check of the fix round

Reviewer: Claude Sonnet 5.5, on Owls, 2026-11-16 (read only; scratch, builds and `TMPDIR` under this worktree's `.rc_tmp/`; nothing deleted, nothing written outside it).

## Verdict: MERGE

Counts: **0 CRITICAL, 0 MAJOR, 4 MINOR (+1 NIT)**. All four MAJOR findings of the first review (`PR52_review.md`) are fixed and re-measured. MINOR-5 and MINOR-6 are fixed. MINOR-7 is kept with a rationale that is only partly sound (see 5). The new MINORs are small and none blocks the T5 dependency.

## Scope and tree

- Head **a72a7777** (detached, clean). Fix commit **292904b0**; a72a7777 merges #49 (O2) and K3 (#51) via `82e985eb`. The merge is clean: `git show --cc a72a7777 -- engine_v4` is empty, so there is no hand-resolved hunk.
- Judged: `git diff 45fcd32d 292904b0` (the fix) plus the merged tree's behaviour. What #49 and K3 brought in is not reviewed.
- Executable SHA-256 `a8cbfde709812c903cfa4216057a34a548560e11c5dc87ca44fa139fed56eae7` (x86-64-v2, GCC 11.5.0, glibc 2.34).
- `git diff --check` clean. No change outside `Scripts/SMC_BVS/engine_v4/` in the fix diff (all 18 changed files are under it).

## Quick suite

`export TMPDIR="$PWD/.rc_tmp/tmp" P1M_TEST_ROOT="$TMPDIR" OMP_NUM_THREADS=3; nice -n 19 bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --quick --threads 3 --keep`

- C++: **133 test cases, 0 failed, 0 check failures** (129 at the first review; the merged heads add tests).
- WP5: 17 driver tests OK; competitor harness OK (optional packages missing); install script OK (9 checks).
- WP4 golden: **528,081 checks, 0 failures**.
- Runner exit **0**. Log: `.rc_tmp/quick.log`.
- Passing, among others: `island_command_end_to_end`, `island_command_driver_manifest`, `island_command_refusals_and_budget`, `island_command_resume`, `start_bytes_model_bounds_start_bytes`, `plan_from_sizes_equals_plan_island` (48 configurations), `golden_island_vs_core_engine`, `golden_compat_island_vs_core_serial_stream`, both calibration-island goldens.

## Checks on the fix commits

### 1. MAJOR-3 (B from `calib::budgets`) — FIXED
`island_cmd.cpp` takes B from `calib::budgets(n, p)` in the run (after reading n, p from data.bin metadata) and in the plan-only paths with and without files. A conflicting `--B` is `invalid_input`.

Re-run of the reviewer's n = 60, p = 30 fixture (same fixture bytes: rebuilt with the same generator; CLI `calibrate` per mode, seed 77, island 2, threads 1). The CLI output equals the in-process B = 5 run, section by section outside `meta`:

| mode | CLI output hash | in-process B = 5 | in-process B = 14 |
|---|---|---|---|
| V | **0x072cb398a4a33495** | 0x072cb398a4a33495, sections equal | 0xffce07af01f718de, sections differ |
| compat | **0x0ef08329972b0419** | 0x0ef08329972b0419, sections equal | 0x87206ab8beaaae97, sections differ |

Both values are the ones the first review gave for B = 5. Also:
- `--B 14` exits **13** with files plan-only, sizes-only plan-only and a full run. `--B 5` exits 0.
- The new test asserts `budgets(n,p).B == 5` and the CLI reference is built independently with `c.B = 5`.

Evidence: `independent.log`, `recheck_extra.log`.

### 2. MAJOR-1 (input hashes in the checkpoint identity) — FIXED
`IslandConfig::input_id = data|setup|calib` content hashes, added to `fingerprint()`. It is the first thing read in the checksum pass of `load_ckpt`, so a foreign checkpoint is refused before any state is read (island_run.h, `fp != fingerprint()` → `foreign` → `invalid_input`). An empty `input_id` adds no bytes, so the in-process callers and tests are unchanged.

- **Reviewer's changed-input resume, re-run.** The same construction: only the setup's neighbour graph changed to the empty CSR graph, setup hashes rewritten, a calibration copy's `meta.inputs.setup.bin` updated coherently, and the saved checkpoints copied to the new output stem after a real SIGKILL. It now exits **13** (`invalid_input: checkpoint … belongs to another configuration or binary`), writes no `foreign.bin`, and leaves the checkpoint in place. The changed inputs themselves run fine from scratch (`changed_fresh`, exit 0).
- **Same-input kill/resume, real `SIGKILL` of the CLI with both generations on disk, then the same command again.**

| mode | checkpoint steps a / b | resumed step | resumed hash = uninterrupted hash | non-meta sections |
|---|---|---|---|---|
| V | 4 / 10 | 10 | 0x072cb398a4a33495 | all equal |
| compat | 2 / 4 | 4 | 0x0ef08329972b0419 | all equal |

(Kill points differ from the first review because timing differs; the property holds at every kill point tried.) The same binary resumes the same inputs, so the refusal comes from the input identity and nothing else.

### 3. MAJOR-2 (admission before the loads) — FIXED for `island`; calibrate partly (see MINOR-2)
Reading `island_cmd.cpp`, the order is now: `calib.bin` head (meta + grid) → `data.bin` metadata (mapped, n/p/K) → `read_setup_dims` (mapped; block histogram, section lengths, `size_logmass`) → plan → admit or refuse → only then `load_data`, `load_start`, `load_neighbours`. `--plan-only` returns before any of them. `plan_island` and the command share `plan_sizes` / `plan_with_budget`, and `inputs_bytes` is `start_bytes_model(dims)` both before the load and in the run, so the pre-load refusal and the run's own admission are one number.

Measured with the reviewer's allocation probe (warmed, budget = 1 byte, operator-new requests, **not** RSS), on the n = 60, p = 30 fixture and a p = 300 fixture (10x larger setup; calibrated by the CLI):

| call | p = 30: calls / bytes | p = 300: calls / bytes | first review, p = 30 |
|---|---|---|---|
| island, run | 1,788 / 418,974 | 1,769 / 414,560 | 5,291 / 816,860 |
| island, plan-only | 1,680 / 393,548 | 1,661 / 389,187 | 3,880 / 470,377 |
| calibrate, run | 2,359 / 506,373 | 8,074 / 1,331,090 | 1,006 / 174,176 |
| calibrate, plan-only | 2,411 / 514,959 | 8,126 / 1,339,676 | 1,006 / 174,176 |

The island admission allocations are flat in p (largest request 5,248 B at both sizes): nothing grows with the setup before the refusal. Calibrate still grows with p because it reads data and `wp4io::read_setup` first (MINOR-2).

The "remaining expanded Start for admitted islands is StartView's" statement is in WP3_DESIGN §1.13 ("What remains for StartView": the process still holds the expanded Start after admission, the model bounds it, the setup is read twice). It is accurate and sufficient: admission is before the expansion, and the model is the plan's term. INTERFACES §7's rule (refuse before allocating) is met for the island command. Evidence: `allocation_warm.log`, `allocation_warm300.log`.

### 4. MAJOR-4 (explicit arguments on either side of `--manifest`) — FIXED for island, calibrate and the listed keys
`main` records the explicit values in `args["cli_explicit"]` (also for commands that ignore it); `cmd::explicit_args` / `refuse_manifest_conflicts` compare against the manifest's params regardless of order. Measured (manifest params seed 77, id 2, Rp 4):

| conflict | before `--manifest` | after `--manifest` | first review (before / after) |
|---|---|---|---|
| island `--seed 78` | 13 | 13 | 0 / 13 |
| island `--id 3` | 13 | 13 | 0 / 13 |
| island `--island 3` | 13 | 13 | n/a |
| island `--Rp 1` | 13 | 13 | 0 / 13 |
| island `--seed 77` (same value) | 0 | 0 | accepted |
| calibrate `--seed 78` | 13 | 13 | completed at 78 after the manifest |
| calibrate `--seed 77` (same value, plan-only) | 0 | 0 | accepted |

Remaining gap, same class, for an unlisted key: MINOR-1.

### 5. MINORs 5–7
- **MINOR-5 (calibrate plan-only, over-budget hides the island plan) — fixed.** `calibrate --plan-only 1 --mode V --n 200 --p 1000000 --threads 3 --mem-budget 1000` exits 11 and now carries `island_plan` (floor 49,364,844,050 B; the floor moved by +143 MB from the first review's 49,221,484,050 only because K3's `gram_rows` term merged into the memory plan).
- **MINOR-6 (refused compat island written as law) — fixed.** Refusal files now carry the request's identity: compat refusal has header mode 1, `meta.mode = compat`, N = 2500, T = 14, a 15-entry grid and no estimate sections; V refusal has header mode 3, `meta.mode = V`, T = 13. Exit 11 in both.
- **MINOR-7 (checkpoint container kept; rationale in §1.13).** The rationale is **partly sound**.
  - Sound: a streamed payload with two atomic generations works; the CLI resumes it bit-identically (re-measured above); the fingerprint (now with the input identity) and the FNV-64 checksum make a foreign or torn file a refusal, never a silent resume; and the document requests the INTERFACES §5.1 amendment instead of silently deviating. Nothing else in the pipeline reads these files, so it does not block T5.
  - Overstated: "`fmt::Writer` would hold a second copy of the store". `Writer::add()` / `add_raw()` keep a pointer, not a copy (`format.h:47-50`: "no copy: X is 1.6 GB at p = 10^6"); only `add_json()` and `add_copy()` own bytes. The big checkpoint payload is already contiguous vectors (`top.k->{v,hash,off,len,pool}` and the leader stores), which can be passed by reference; the remainder (per-particle `S`, `rb_round`, stage rows) is small and can be flattened. So a kind-8 container with SHA-256 sections is feasible without doubling memory; the cost is hashing GBs per checkpoint (seconds every 600 s). The honest reason to defer is effort, not memory.
  - Evidence it is still non-contract: `smcbvs4 info --in saved_V.b` exits 13 (`bad magic`; the file starts `SMCV4CKP`).
  - Recommendation: reword §1.13 to say that deferral is a choice and that the migration is feasible with `add_raw`; keep the requested amendment, or schedule the migration before the 10^5 T6 gate. MINOR, unchanged in grade.

### 6. The island_run.h edit
There is no hunk of the fix that conflicts with builder 7's O2 code: the merge is clean (`--cc` empty). The fix's changes to `island_run.h`, measured against #49's version (`82e985eb`), are three hunks, not two lines:
1. `fingerprint()`: +1 line, `f.bytes(cfg.input_id…)`. Correct: placed before the binary block, empty adds nothing (FNV over zero bytes leaves `h` unchanged), so every existing caller and golden hash is unchanged.
2. `plan_island`: its inline size/G computation is replaced by `plan_sizes` + `plan_with_budget` (−10 / +4). Correct and behaviour-identical: the removed lines are exactly the body of the new helpers, K3's `gram_slots_of(cfg, G, p)` is applied in both the first plan and the G-reduction loop, `G = z.G` is the final G, and `zout`/`kout`/`Gout` are filled after as before. `plan_from_sizes_equals_plan_island` pins the equality on 48 configurations (kernel × threads × G × role × budget).
3. `run_island` refusal: +2 lines setting `role/tier/iter/compat` and `grid/T` on the refusal result. Correct (the MINOR-6 fix; verified above).

If "the 2-line edit" meant hunk 3 (or hunk 1), it is minimal and correct; if it meant something else I did not find a separate 2-line change by the O2 builder in this diff.

## New findings

### 1. MINOR — an explicit `--N` before `--manifest` is dropped, not refused
**Location:** `island_cmd.cpp` (`parse_inputs` `param` lambda covers `id|island`, `seed`, `Rp` only; the N check at the `args.contains("N")` line compares against calib.bin, not the manifest's).
`main` copies manifest params over an earlier explicit value, and N is not in the `cli_explicit` comparison, so `island --N 100 --manifest M --plan-only 1` exits **0** while `island --manifest M --N 100 --plan-only 1` exits **13** (`N differs from calib.bin's frozen N = 2500`), with M's params N = 2500. Science is unaffected (N always comes from calib.bin and the manifest's N equals it in a driver-filled manifest), but "either order" is not uniformly true. Evidence: `man_N100_before.log`, `man_N100_after.log`.
**Fix:** add `N` (and any other scientific manifest param) to the `cli_explicit` comparison; also add before/after cases for every key the manifest may carry.

### 2. MINOR — calibrate still reads data.bin and the setup (`wp4io::read_setup`) before any admission
**Location:** `calib_run.cpp` (data `load_data`, then `read_setup`, then the plans).
Only the expansion of the Start is now after the admission. The allocation table above shows calibrate's pre-refusal requests growing with p. At p = 10^6, n = 200 this is X (1.6 GB) plus the setup tables before a refusal; the reader split is WP4's PR46 MAJOR-2 and is documented in §1.13. Not part of this PR's four MAJORs, and it does not block the island path.
**Fix:** use `read_setup_dims` plus mapped metadata for the calibrate plan, as the island command does, in the WP4 follow-up.

### 3. MINOR — `start_bytes_model` is pinned only on small fixtures
**Location:** `setup_load.h` (`start_bytes_model`); test `start_bytes_model_bounds_start_bytes` (blocks of 3, 5, 8; ratio 1.05–1.17).
It is an upper-bound model that now drives both the pre-load refusal and the run's admission. It is plausible by construction (payloads + headers, x2 for growth), but no p ≥ 10^5 measurement exists. The island record already carries `start_bytes_measured`.
**Fix:** compare `start_bytes_measured` with the model's `inputs_bytes` in the first 10^5 T6 run and record the ratio; widen the test to mixed block sizes up to 20.

### 4. MINOR — the checkpoint container rationale (see 5, MINOR-7 above)
Counted as the carried-over MINOR-7; no new defect.

### 5. NIT — persisted `size_logmass` is not cross-checked with the rebuild
**Location:** `setup_load.h` `load_start` (compares `size_cum` only); the pre-load admission uses the persisted `size_logmass` (`plan_k`), while `run_island`'s own plan uses the rebuilt Start's.
If a hash-valid setup.bin carried a `size_logmass` different from its rebuild, the two admissions could disagree (a late refusal, or a false early one). Unlikely with a producing tool in the loop.
**Fix:** add the same bitwise `same(R.vec("size_logmass"), st.size_logmass)` check as for `size_cum`.

## Residual notes (no change of verdict)
- The refusal text prints `budget 0 MiB` for a 1-byte budget (integer MiB); cosmetic.
- This is a small-p (n = 60, p = 30) check, not the required 10^5 T6 gate; no NOTS or large-p run was made.

## Evidence files (under `.rc_tmp/`)
`quick.log`, `independent.log` (kill/resume, B, manifest, foreign resume), `recheck_extra.log` (B variants, manifest both orders for island and calibrate, refusal files, calibrate plan-only floors, checkpoint info), `allocation_warm.log`, `allocation_warm300.log`, `man_N100_before.log`, `man_N100_after.log`; scripts `independent.py` (the reviewer's, run unchanged), `recheck_extra.py`, `probe.cpp`, `probe_p.cpp`, `allocation.cpp`; fixtures `fixture/` (n = 60, p = 30) and `fixture300/` (p = 300).
