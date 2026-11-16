# PR #20 review: WP4 slice 2 (calib.bin / fit.bin writers, island_r.bin reader, `smcbvs4 merge`, streaming merge)

- **Reviewer:** Opus 5.5 (high), independent. Template: `briefs/REVIEW_PR_template.md`; rules: `briefs/BUILD_COMMON.md`.
- **Scope:** head `db58db70` (`exp/P1M-wp4-io`) into `exp/P1M-engine` (`7ce52251`, INTERFACES v0.1.10). The branch is based on
  `d4cedd88`. `git merge-tree` against `7ce52251` is clean (tree `824e976f`).
- **How:** own worktree, detached checkout, read only. Nothing was pushed, commented or branched. Temp files only in
  `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-20`, removed at the end. `nice -n 19`, ≤ 3 cores, no NOTS.
  Processes stopped only by PID.
- **Probe:** a reviewer program in TMPDIR, linked to the PR's own `libv4_bit.a`. It uses the PR's test fixture (`make_fx`, p = 24, R′ = 4).
  - It rewrites island, calib and setup files **hash-consistently**, with the WP1 `fmt::Writer`, so every header and section hash verifies.
  - It runs `merge::run` in a forked child, so a crash is observed and does not kill the probe.
  - It also runs random byte flips and truncations, φ cases, a thread × chunk sweep, and the real `smcbvs4` binary.

## Verdict: **REJECT** (for now; 1 CRITICAL, 2 MAJOR, 4 MINOR, 6 INFO)

| grade | count |
|---|---|
| CRITICAL | 1 |
| MAJOR | 2 |
| MINOR | 4 |
| INFO | 6 |

- **What works.** The library pieces reproduce the PR's claims and are good work:
  - The streaming merge holds one island at a time.
  - The φ reconstruction is exactly v3's.
  - fit.bin is identical across 22 thread × chunk × ℓ settings.
  - Random corruption is always refused.
  - The PR16 re-check minors m-1 to m-3 are fixed and tested.
  - Tests: **94/94**. Quick golden: **254,268 checks, 0 failures**.
- **What is broken.** The `merge` **command** is not safe or usable as shipped:
  - **C-1.** It takes R′ from the length of the `islands` argument and never checks it. Through the CLI, `--islands a,b,c,d` is a string, so R′ = 0. The result is a **"completed" fit, exit 0, `estimates_available = true`, log Ẑ = NaN** (MEASURED).
  - **M-1.** `--manifest`, the only form the WP5 driver uses, makes the merge fail ("json: not a string"). `--mem-budget` (INTERFACES §7, bytes) is silently ignored.
  - **M-2.** Section contents are not validated before use. Hash-consistent files with out-of-range indices crash the merge (SIGSEGV, heap-corruption abort) in 9 of 28 hostile cases.
- **Merge after:** C-1, M-1 and M-2 are fixed, with tests that run the `smcbvs4` binary the way the driver does and that read hostile files. A focused re-check is enough; the rest of the slice need not be re-reviewed.

## Claims, one by one

| claim | result |
|---|---|
| File-backed source: pass 1 validates headers, content hashes, meta.inputs, binary blocks; then one island at a time | **Verified** for those items (`wp4_io.cpp:222-245, 324-332`). **But section contents (indices, offsets, ranges) are never validated:** M-2 |
| `--mem-budget` works through the CLI | **Not verified: false.** `merge::run` reads `mem_budget_gb` only (`wp4_io.cpp:565`); `--mem-budget 1000` is ignored (M-1). The PR test sets `mem_budget_gb` in process (`test_wp4_io.cpp:268`) |
| hpm_ev has no φ; the merge rebuilds φ from the island grid, v3's values | **Verified** (I-1), apart from a silent 0 for an out-of-range stage (M-2) |
| m-1 terminal offsets validated before any read | **Verified** (`wp4_terminal.h:23-24`; probe H14 refused) |
| m-2 the merge refuses leader stores | **Verified** (`merge.h:234-238, 253-258`; test `wp4_merge_guardw_t10`) |
| m-3 failure several waves in = serial for every threads × chunk | **Verified** (`test_wp4.cpp` `wp4_tail_failure_path_equals_serial`: 4 problems × threads {1, 3} × chunk {3, 7, 64}) |
| Reader/writer cross-check against WP3's island_file, both ways; empty terminal sections omitted | **Verified** (`test_wp4_io.cpp:317-356`). See I-5 for the omitted-terminal direction |
| 94/94 v4_tests; quick golden 254,268 / 0; golden removes `$TMPDIR/wp4_golden` unless `--keep` | **Verified** (run 1; the work dir is gone after the run). Full golden (975,925) **not re-run**: the quick set contains the new T9-through-files comparison |

## Findings

### C-1 CRITICAL (GUARD-W): the merge command takes R′ from the islands list, unchecked; zero islands give a "completed" fit with NaN estimates
`src/merge/wp4_io.cpp:549-554, 561`; `include/v4/merge.h:195-196`

- **Evidence.**
  - `const int R = (int)il.size(); … ms.Rp = R;` are the only sources of R′.
  - `guard_heads` checks `src.count() != ms.Rp`, but both values are the same R here, so the check is vacuous in `merge::run`.
  - The manifest's `params.Rp` (the WP5 driver writes it, `p1m_driver.py:316`) is ignored. So:
    - **CLI (MEASURED, probe "cli").** `smcbvs4 merge --data … --setup … --calib … --islands i1,i2,i3,i4 --out …` puts a JSON **string** in `islands`, and `Json::size()` of a string is 0. The result: **exit 0, status `completed`, `estimates_available = true`, `Rp = 0`, `logZ = NaN`**, written to fit.bin and to the record. The same happens with `--mem-budget 1000` added.
    - **Subset (by reading).** An `islands` array holding 3 of a run's 4 island files passes every check (heads r = 1..3, N, p) and is pooled as R′ = 3. Spec §6 and the `merge.h` header say "no subset is ever pooled".
  - An empty `islands` array gives the same NaN "completed" fit: `lse({})` and `/R` divide by 0.
- **Why CRITICAL.** GUARD-W is the merge's main safety rule. Here a merge of nothing, or of a subset, reports `completed` with estimate fields, and the driver's afterok chain would pass it on to eval.
- **Fix.**
  - Require `islands` to be a non-empty JSON array of strings, else `invalid_input`. If the CLI should take a comma list, parse it explicitly.
  - Require R′ from the manifest (`params.Rp`) or an explicit `--Rp`, and refuse unless `il.size() == Rp`.
  - In `guard_heads`/`merge_stream`, refuse `Rp < 1`.
  - Before `estimates_available = true`, assert that log Ẑ and every pip are finite (an internal check).
  - Tests: the binary with `--islands` as the CLI passes it, an empty list, a 3-of-4 list against `Rp = 4`.

### M-1 MAJOR (contract §5.3/§7, CLI): `--manifest` breaks the merge; `--mem-budget` is ignored
`src/merge/wp4_io.cpp:532, 565`; `src/cli/main.cpp:50-55`; `tools/slurm/p1m_driver.py:248-250, 323`

- **Evidence (MEASURED, real `smcbvs4` from the PR build).**
  - **(a) `--manifest`.** `main.cpp` stores the parsed manifest **object** in `args["manifest"]`. `merge::run` then calls `read_json_file(args.at("manifest").str())`, which throws `invalid_input: json: not a string`, exit 13.
    - This is the only invocation the WP5 driver generates: `smcbvs4 merge --manifest merge.json --threads … --out fit.bin`.
    - Even with (a) fixed, the driver's merge manifest gives data/setup/calib/islands only as `inputs` paths and `params.Rp`. `merge::run` needs `data`, `setup`, `calib` and `islands` arguments, so the driver's command still could not run.
    - The CLI and the driver contract were not exercised end to end. The PR tests call `merge::run(Json)` in process.
  - **(b) `--mem-budget`.** INTERFACES §7 defines `--mem-budget` in **bytes** (0 = off). The CLI turns it into `args["mem_budget"]`, but `merge::run` reads only `mem_budget_gb` (GiB).
    - `--mem-budget 1000` → admitted, completed, `mem_estimate.budget = 0`.
    - `--mem-budget-gb 0.000001` → `resource_limit`, exit 11, as designed.
    - A budget given the documented way is silently ignored.
- **Fix.**
  - Accept `args["manifest"]` as the object the CLI provides (or as a path).
  - Take the input paths and R′ from the manifest in the way WP5's driver writes it, or agree a `params` layout with WP5 and add it to INTERFACES.
  - Read `mem_budget` in bytes. Keep `_gb` only as an alias, if at all.
  - Add a test that runs the built `smcbvs4 merge` binary with a driver-style manifest, including one refused budget.

### M-2 MAJOR (validation before use): hash-consistent hostile files crash the merge or are accepted with wrong content
`src/merge/wp4_io.cpp:38-54, 156-170, 247-296, 362-373`; `include/v4/merge.h` (PIP_T `acc[j]`, tail)

- **Random corruption is always caught** (MEASURED; detail in run 3):
  - island_1.bin: 300 byte flips → 292 refused, 8 accepted. All 8 were in the unhashed 64-byte alignment padding, so the content was identical.
  - 63 truncations → all refused.
  - calib.bin and setup.bin: 100 flips each → refused, or in padding.
  - Zero crashes.
- **Section contents are never checked against their meaning, though.** I rewrote one field at a time through the WP1 Writer, so every hash verifies. Results, with the merge run in a forked child (MEASURED):

| case | file field | result |
|---|---|---|
| H1 | `top_pool[0] = p + 10⁸` | **SIGSEGV** |
| H2 | `top_pool[0] = −1` | **SIGABRT `munmap_chunk(): invalid pointer`** (heap write through `acc[j]`, PIP_T) |
| H3 | an unsorted model in `top_pool` | accepted, `completed` |
| H4 | `top_off[i] = 2⁶⁴ − 1` (`off + len` wraps; `wp4_io.cpp:265`) | accepted, `completed`: reads before the pool |
| H5 | `hpm_S = {p + 10⁸}`, high F | **SIGSEGV** (tail local search from the HPM) |
| H6 | `hpm_S = {5, 2}` (unsorted), high F | **SIGSEGV** |
| H7 | `hpm_ev` phase 99, mech 77 | accepted; fit.bin gets phase "?", which `event_from_json` cannot read back |
| H8 | `hpm_val` F = NaN | accepted, `completed` |
| H10 / H11 | `st_ess` of length 1 (T = 3); empty `grid` with a BRIDGE stage-2 HPM | accepted; φ silently 0 |
| H18 | `pip_r[0] = NaN` | accepted: a **`completed` fit with NaN pip_eq / pip_Z** |
| H19 | `island_best` entries for the other islands = 1e300 | accepted and merged by max, so the E1 flag of every other island is masked (`wp4_io.cpp:281-282` copies all entries; only entry r belongs to this island) |
| C1 / C2 | calib `inh_idx[0] = p + 10⁸` | **SIGSEGV** |
| S3 / S4 / S5 | setup `code_ptr[0] = 10¹²`; `tstore_top_pool[0] = p + 10⁸`; `mode_S = {p + 10⁸}` | **SIGSEGV** |
| S2 | setup `pos[0] = 40` | accepted (`1u << 40` is UB in `SetupView::comp`) |

  - Refused correctly: H9 (NaN store value), H12/H13 (r, N), H14/H15 (terminal), H16 (`len` past the pool), H17 (empty logZ), H20 (logical size), C3, S1.
- **Root causes.**
  - `read_store` and `load_island_full` check `off + len ≤ |pool|` with a u64 sum that can wrap. They never check that each model is strictly increasing, inside [0, p) and of size ≤ K.
  - `hpm_S` is unchecked: range, order, size, membership or consistency with the store's best value.
  - `hpm_ev` is unchecked: `phase`/`mech` range; `seg = FINAL`, `unit = r`; `xph` ∈ {INIT, BRIDGE, BURN, MEASURED}; `stage ≤ T`.
  - `grid.size() == T + 1` and `st_ess.size() == T` are unchecked.
  - `pip_r` (finite, in [0, 1]) and the HPM F (finite) are unchecked. `island_best` entries other than r are not forced to −inf.
  - `read_calib`'s inherited models and HPM are unchecked.
  - `read_setup` does not check `blk`/`pos` length = p, `pos` < block size ≤ 31, `code_ptr[b] + 2^m ≤ |logr|`, `blk_ptr`, `mode_S`, or the table-store models.
  - Island-versus-calib consistency (T + 1 = |calib grid|, L, Hm, tier) is also unchecked. `meta.inputs` ties the files together, so only a writer bug would differ.
- **Reachability.** These need a hash-consistent bad file: a writer bug in another WP (WP3's island writer, WP2's setup) or a deliberately built file. That is the class of PR16 re-check m-1, which this PR fixed for one field. Here it covers every model-bearing field.
- **Grade.** MAJOR rather than MINOR because:
  - the merge is the one job that consumes every other WP's files;
  - a crash leaves no status record, where the driver expects exit 13;
  - H2 is a heap write;
  - the brief requires "never a crash or out-of-bounds read".
- **Fix.**
  - One `check_model(ModelView, p, K)` (strictly increasing, in range, size ≤ K) used for every model read: store pools, `hpm_S`, inherited, `mode_S`, table stores. The terminal reader already does this.
  - An overflow-safe `off ≤ np && len ≤ np − off`.
  - Range checks on the `hpm_ev` fields.
  - `stage ≤ T` with `grid.size() == T + 1`, else `invalid_input`, never a silent φ = 0.
  - Finite checks on F and `pip_r`.
  - The setup array-shape checks above.
  - A test with these rewritten files. The probe's `rewrite()` helper, about 20 lines, can be taken as is.

### m-1 MINOR (provenance): fit.bin `meta.inputs` records the manifest's expected island hashes, or "" without a manifest
`src/merge/wp4_io.cpp:573`
- MEASURED: without a manifest, `"island_1.bin": "" … "island_4.bin": ""`.
- The merge has opened each island and knows its actual content hash: `fmt::Reader::content_hash()` in `head_island`.
- Fix: carry the hash in `IslandHead` and record it.

### m-2 MINOR (scale accounting, v0.1.10): the merge's memory plan is not the whole task's
`include/v4/merge.h:95-104`; `src/merge/wp4_io.cpp:286-292`
- v0.1.10 says `--mem-budget` is the whole task's memory. The plan counts the merged store, one island, pip_r/terminal and the tail. It leaves out:
  - X of data.bin (mapped; n·p·8 = 1.6 GB at n = 200, p = 10⁶);
  - the setup inputs (table stores, blocks, logr);
  - `rb_round` and `rb_acc`. `load_island_full` loads them and copies `rb_round` twice (≈ 2·Hm·p·8 + 8p ≈ 72 MB at Hm = 4, p = 10⁶), though the merge never uses them;
  - kbar stays fixed at 8, where re-check m-2 asked for kbar from the islands' pool sizes.
- The NOTS plan has room: ≈ 11.9 + 1.6 + setup < 16 GB (ESTIMATE). But the admission is not the rule INTERFACES states.
- Fix:
  - add the X and setup terms;
  - take kbar from the section lengths `top_pool / top_len` (pass 1 already has the table);
  - skip `rb_round` and `rb_acc` in `load_island_full`.

### m-3 MINOR (diagnostics): every pass-2 load error is reported as "changed between the head check and its load"
`include/v4/merge.h:247-252`, `src/merge/wp4_io.cpp:329-332`
- A malformed section (H14–H16, H20) is not a change. The real error is appended in brackets, but the label misleads.
- Fix: a separate reason, "island r: malformed (…)".

### m-4 MINOR (hygiene): the output defaults to `fit.bin` in the working directory
`src/merge/wp4_io.cpp:538`
- Without `--out`, the merge writes `./fit.bin`, a "." fallback for an output.
- Fix: require `out` (`invalid_input` otherwise), as the other WP4 paths already require their inputs.

### I-1 INFO: the φ reconstruction is v3's, exactly
- **v3** (`core/cpp/v3_engine.h`):
  - INIT: φ = 0 (`:285`).
  - Bridge stage t: φ = `grid[t]`. `phi_new = grid[t+1]` before `++t`, so stage t uses `grid[t]`, and `ev.stage = t` (`:308, 323`).
  - Burn-in and measured: 1.0 (`:342`).
- **WP3** uses the same values (`src/island/island_impl.h:808-819`: `RoundCtx{X_BRIDGE, t, …, phi_new}`, and 1.0 for BURN / MEASURED). WP3's adaptive path appends each φ to `grid`, so `grid[t]` is the realised φ there as well.
- **Probe:** INIT → 0, BRIDGE 1/2/3 → 0.3/0.7/1, BURN → 1, MEASURED → 1, on grid {0, 0.3, 0.7, 1}: **6/6 equal**.
- The golden T9-through-files compares `hpm_provenance`, φ included, with v3's final run.
- Only an out-of-range stage falls back to 0 silently (in M-2).

### I-2 INFO: the streaming bound holds
- `merge_stream` declares one `IslandIn` per loop iteration; it is freed at the end of the iteration. The merged ledger is the only store that persists. Pass 1 reads heads only.
- Each `head_island` constructs a verifying `fmt::Reader`, which hashes every section, and pass 2 hashes again. So the merge reads every island twice: ≈ 2 × R′ × 2.2 GB at 10⁶ (ESTIMATE). That is I/O, not resident memory.
- The PR's 2.5c + 2.5c plan stays conservative for the stores (re-check I-1). Peak ESTIMATE as in the re-check, ≈ 11.9 GB plus m-2's terms.

### I-3 INFO: fit.bin determinism
- MEASURED. Threads {1, 2, 3} × chunk {1, 7, 64, 2048} × ℓ {3, 8}: **22/22 identical** in every section and in `meta`, apart from `timings` and `mem_estimate`.
- `mem_estimate.tail` depends on threads × chunk. So the fit.bin **content hash** differs between thread counts, as `timings` makes it do anyway. That is consistent with §5.1, where T2 compares non-meta sections. The driver should never compare fit.bin content hashes across runs.

### I-4 INFO: temp-file hygiene
- `fmt::Writer` writes `<name>.tmp.<pid>`, unlinks on any failure, renames, and fsyncs the directory (`format.cpp:77-98`, WP1).
- The tests' `TmpGuard` removes the tag's files even when a test throws. No `v4test_*` files were left after my runs.
- The golden removes `$TMPDIR/wp4_golden` (verified absent after run 2).
- At the PR head, `tests/tutil.h` still has the "." fallback. The base fixed it (PR #31), and the merged tree uses the base's refusing `tmp_path`, which `TmpGuard` handles (run 8).
- Not this PR: WP5's `test_post_e2e` left `$TMPDIR/wp5_e2e_<pid>` behind in run 1. The base touched that test in #31.

### I-5 INFO: the "both ways" cross-check covers only files with terminal supports
- WP3's `read_island_file` reads `terminal_S_ptr` unconditionally for a completed island (`island_file.cpp:110`). It would throw on a WP4-written completed island whose empty terminal sections were omitted.
- Only WP4's reference writer omits them (core islands in the golden), so this is harmless. One line in the WP3 reader, `if (rd.has(...))`, would make both readers agree.

### I-6 INFO: GUARD-W in the writers is right
- `write_fit` writes every estimate field only under `estimates_available`. HPM-so-far fields carry `hpm_incomplete`.
- `write_island` writes `logZ`, `st_inc`, `st_cum`, `rb_*`, `pip_r` and the terminal sections only for a completed island. The PR test checks this.
- The breach in C-1 is upstream, in how R′ is formed.

## Regressions and discipline
- The diff touches only `engine_v4/`: `wp4_io.{h,cpp}`, `merge.h`, `calib.h` (a cosmetic `fired()` rewrite), `wp4_terminal.h`, the stub list, CMake, `run_tests.sh`, tests and the golden.
- No hard-coded paths, no large files. Nothing outside `engine_v4/`.
- `calib::Settings::test_force_build_failure` (re-check I-3) is not exposed through calib.bin or the merge. Good.

## Test runs (MEASURED; Owls, Xeon Gold 6148, GCC 11.5.0, R 4.6.0, `nice -n 19`, ≤ 3 threads, 2026-11-16)

TMPDIR `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-20`, removed afterwards. No ASan: `libasan.so.6` is missing on Owls, so the configure step failed. Crashes were observed directly instead.

| # | what | result |
|---|---|---|
| 1 | `tests/run_tests.sh --quick --threads 3` at `db58db70` | `v4_tests` **94 cases, 0 failed**. WP5 driver, competitor harness and install script OK. **WP4 golden quick: 254,268 checks, 0 failures**. Wall 6 min 45 s (01:55:04 → 02:01:49) |
| 2 | after run 1 | `$TMPDIR/wp4_golden` absent (the golden clean-up works) |
| 3 | probe "fuzz", island_1.bin | 300 random byte flips → 292 refused, 8 completed (all 8 in unhashed alignment padding; content identical), **0 crashes**. 63 truncations → 63 refused. calib.bin and setup.bin: 100 flips each, refused or padding, 0 crashes |
| 4 | probe "hostile": 28 hash-consistent rewrites | **9 crashes** (H1, H2, H5, H6, C1, C2, S3, S4, S5: SIGSEGV or SIGABRT), **9 accepted with wrong content** (H3, H4, H7, H8, H10, H11, H18, H19, S2), 10 refused correctly. Table in M-2 |
| 5 | probe "phi" | 6/6 φ equal to v3's values; an out-of-range stage gives 0 silently |
| 6 | probe "det", threads 3 | 22/22 fit.bin identical (sections + meta without timings / mem_estimate) |
| 7 | probe "cli": real `smcbvs4 merge` | `--islands` comma list → **exit 0, completed, Rp = 0, logZ NaN**. `--mem-budget 1000` → ignored, completed. `--mem-budget-gb 1e-6` → exit 11 `resource_limit`. `--manifest` with `params.islands` → **exit 13 "json: not a string"** |
| 8 | PR merged onto `7ce52251` (`merge-tree` `824e976f`, extracted with `git archive`): build + `v4_tests` | **95 cases, 0 failed** (the base adds one test; its refusing `tmp_path` works with the PR's `TmpGuard`) |
