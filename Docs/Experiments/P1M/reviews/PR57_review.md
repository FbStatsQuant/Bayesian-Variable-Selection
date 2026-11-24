# PR #57 gate review: WP3 StartView (mapped flat `setup::Start`; gate P5 of the 1M pilot)

Reviewer: Claude Opus 5.5 (high), second reviewer, after the first reviewer (Codex) was cut off. Owls, 2026-11-17.
Head `9344737d`, merge base `04d8d2b5` (`git diff $(git merge-base origin/exp/P1M-engine 9344737d) 9344737d`, 15 files, all under `engine_v4/`).
Worktree `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-3d20ff7b-00c2d8ced2e83172` (detached at 9344737d). All scratch, builds and `TMPDIR` are in its `.rc_tmp/`; `P1M_TEST_ROOT=$TMPDIR`; `nice -n 19`, `taskset -c 0-2`. Nothing was deleted, and nothing was written outside the worktree. Codex's `.rc_tmp` was only read; one of its probe binaries was copied into my `.rc_tmp` and run there.

## Verdict: ACCEPT-WITH-FIXES

**0 CRITICAL, 2 MAJOR, 5 MINOR.**

The core of the PR holds:
- The arithmetic matches the old engine bit for bit: final-island and calibration outputs equal the merge-base engine's on real WP2 setup files.
- No new heap allocation happens inside parallel regions.
- Mapping lifetime is correct, and the mapping is read-only.
- The island command's admission now counts what it loads, before it loads it, which closes PR52 MAJOR-2 for `island`.
- The heap reduction reproduces at p = 10⁴ and 3×10⁴.

Two fixes are needed before merge:
- **MAJOR-1:** calibrate's admission leaves out the SetupView copy that stays live beside the StartView.
- **MAJOR-2:** the mapped loader dropped the old loader's size-law validation, so a hash-valid but malformed `size_cum` produces a model with K + 1 members and an out-of-bounds read.

Both are local fixes; neither needs a redesign. **P5 should stay open until MAJOR-1 is fixed and WP3_PLANS_1e6.md is regenerated (MINOR-1).**

## Findings

### MAJOR-1: calibrate's N-1 admission omits the SetupView copy that stays resident beside the mapped StartView
**Location:** `src/calib/calib_run.cpp:179` (plan), `:208` (`wp4io::read_setup`, kept for the whole calibration), `:219` (`rc.inputs_bytes = ipl.setup_in`). The same applies to `include/v4/island/pilot_only.h:59,68`.

**What happens.** Calibrate's island admission counts `start_inputs_bytes(sd)` (mapped sections + scratch + neighbours) + `resident_own` (ledger + export). After admission it still calls `wp4io::read_setup`. That call copies `logr`, the partition arrays and the table stores into owned vectors (`SetupView`, `wp4_io.cpp:596`), and the copy lives until calibration ends. No term counts it. Before this PR the island term was the expanded-Start model, which was large enough to hide most of the gap. The PR replaces it with the much smaller mapped term while the copy stays, so the undercount grows. WP3_DESIGN §1.12 and the WP3_PLANS note ("until PR46's reader split; after it, about the N-1 column") assume the copy goes away. It does not: PR46 reordered the reads but did not remove the copy.

**MEASURED** (my probe `.rc_tmp/probes/setupview_heap.cpp`; log `.rc_tmp/probes/setupview_heap.log`; AR, n = 200, setups made by this head's `gen → prep → setup`):

| p | SetupView RssAnon retained | of which logr | counted setup inputs (3 thr) |
|---|---|---|---|
| 10⁴ | 111.7 MiB | 62.5 MiB | 64.5 MiB |
| 3×10⁴ | 343.4 MiB | 187.4 MiB | 192.5 MiB |

At p = 3×10⁴, `calibrate --mode V --threads 3 --plan-only 1 --mem-budget 1800MiB` returns `completed`, admitted at G = 64 with a planned total of 1,799.4 MiB (`.rc_tmp/s3e4/plan1800.json`). The live state including the uncounted copy is about 2,143 MiB. Codex measured the same gap at p = 10⁵ (1,046 MiB retained). By WP3_PLANS's own calibrate-task column the 1M gap is about 10 GiB. This is a missing live term in the admission check, not a measured OOM.

**Fix (pick one):**
- Have SetupView borrow the mapping: `logr` and the partition are the same sections StartView maps, which leaves only the table stores to count.
- Or add a `setup_view_bytes(sd)` term, computed from section lengths and the table-store sizes, to `calib_island_plans` and to `rc.inputs_bytes`.

Use the same function in the pilot tool and in `v4_plan_tables`. Add a test that sets a budget between the current total and the complete one and asserts the refusal.

### MAJOR-2: the mapped loader no longer validates the persisted size law; a hash-valid malformed `size_cum` gives k = K + 1 and an out-of-bounds read
**Location:** `include/v4/island/setup_load.h:191-226` (`map_start_view` checks shapes only); `include/v4/island/start_view.h:210,227` (`k = upper(size_cum, u)` with no k ≤ K check), `:73` (`c0` index), `:124-145`.

**What happens.**
- The old path (`load_start`) rebuilt the law from `logr` and refused a file whose `size_cum` differed from the rebuild. `map_start_view` checks every section length and the partition bijection, which I verified: all derived offsets are in bounds. It never checks values.
- If `size_cum[K] < u`, then `k = K + 1`. The first scan reads `cond0[(J-1)(K+1) + K + 1]`, one element past the section, and the draw returns K + 1 members, which then go to the scorer and `logprior[k]`.
- A non-normalised conditional row (`upper` returning `len`) can likewise give j > min(m, r). `codes_of_size(m, j)` then returns no codes, and `cs[upper(...)]` reads past the end.

**Reproduced** with Codex's probe, run by me on my own p = 10⁴ file. The probe rewrites only `size_cum` (K + 1 zeros) through `fmt::Writer`, so every hash is valid. The old loader refuses; the mapped loader accepts it, gives size category 101 with K = 100, and the draw returns a 101-member model (`.rc_tmp/probes/malformed_s1e4.log`).

Hash checks authenticate the bytes, not the invariants. D-31 deliberately moves trust from "the island rebuilds from logr" to "WP2's persisted tables", so the reader has to keep the invariants that bounds-safety depends on.

**Fix:** in `map_start_view`, at O(J·K) cost (≈ 7.5 M checks at 1M, sub-second):
- `size_cum` finite, non-decreasing, last entry exactly 1.0;
- `cond0` in [0, 1];
- optionally, recompute `cond0` and `size_cum` from `logprof`, `logF` and `size_logmass` and compare bits. This is the cheap part of the old rebuild and also catches a WP2 writer bug at p sizes the tests never reach.

Add negative tests for malformed `size_cum` and `cond0` to `test_start_view.cpp`; today there are no negative tests for the mapped loader.

### MINOR-1: WP3_PLANS_1e6.md N-1, calibrate-task and merge columns are stale at this head
I re-ran this head's `v4_plan_tables --counts` on WP2's `counts/{AR_n200,BLK_n200,IND_n1000}.json` (`.rc_tmp/plans_*.log`).

| row | final island | calib alone | N-1 | calibrate task | merge | setup inputs |
|---|---|---|---|---|---|---|
| AR 200 G=1, doc | 19.5 | 37.1 | 54.4 | 64.8 | 38.5 | 6.78 |
| AR 200 G=1, head | 19.5 | 37.1 | **55.2** | **65.5** | **39.3** | 6.78 |
| BLK 200 G=256, doc | 28.3 | 45.8 | 63.2 | 70.1 | 30.0 | 3.33 |
| BLK 200 G=256, head | 28.3 | 45.8 | **63.9** | **70.9** | **30.7** | 3.33 |

(GiB.) Final island, calibration alone and setup inputs reproduce exactly. I checked the AR setup-inputs value by hand from the counts histogram:

| term | value |
|---|---|
| view (`12p + 24(J+1) + 8C + 8Σ(min(m,K)+1) + 8(J+1)(K+1) + 16(K+1) + 8J(K+1)`, J = 74,726, C = 875,529,216, K = 100) | 6.6565 GiB |
| neighbour CSR | 0.1118 GiB |
| 96-thread draw scratch | ≈ 10 MiB |
| **total** | **6.778 GiB**, matching the tool |

The other three columns are about +0.7 GiB at this head: the doc predates the merge of #46/#55 (`0eb90a86`), which changed `calib_memory_plan`. Codex found the same for IND n=200.

**Fix:** regenerate the doc from the merged head after MAJOR-1, record the head and the counts files, and drop the claim that the SetupView copy disappears after PR46.

### MINOR-2: `v4_pilot_island` still loads data, SetupView and the start law before any admission, with a k rule that differs from calibrate
**Location:** `include/v4/island/pilot_only.h:54-75`. The ordering predates this PR, but the PR edits these lines and calls the pilot "as calibrate loads it".
- Admission happens only inside `runner.run`, after `load_data`, `read_setup`, the mapping, the neighbours and `offer_tables`. Codex measured 17.7 MB of allocation requests before a 1-byte budget refusal at p = 400.
- `kbar = max(8, |mode_S| + 1)` differs from calibrate's `calib_k_plan` (q90).

This is a measurement tool, not a pipeline stage, so MINOR.

**Fix:** reuse calibrate's dims-first plan, including the MAJOR-1 term.

### MINOR-3: the second open of setup.bin is not hash-verified or identity-checked (TOCTOU), and the mapping is `MAP_SHARED`
**Location:** `island_cmd.cpp:287`, `calib_run.cpp:214`, `pilot_only.h:66`.
- `load_neighbours(path, p, verify = false)` opens a second `fmt::Reader` on the same path and copies `nb_*` without hashing the sections. It relies on the first Reader having verified "the same file", but neither the StartView Reader nor this one compares its `content_hash()` with `sd.content_hash` from the plan.
- `fmt::Reader` maps with `PROT_READ, MAP_SHARED` (`format.cpp:109`). This is read-only, which is correct, but an in-place rewrite or truncation of setup.bin during a multi-hour island would change the bits or raise SIGBUS after verification.

Inputs are frozen by policy, so MINOR.

**Fix:** pass the expected content hash into `map_start_view` and `load_neighbours` and refuse on mismatch; this is cheap. Optionally note the immutability assumption in the design doc.

### MINOR-4: the plan omits small fixed heap, and verification pages the whole file into the mapping
- At p = 10⁴, 3×10⁴ and 10⁵, the measured StartView + neighbours + scratch heap exceeds the planned non-mapped part by about 0.5 MiB. The cause is WP2's static `codes_of_size` tables (≈ 2^16·4 B per m ≤ 16) and allocator overhead. The 12 % headroom covers it; add it as a constant for exactness.
- `map_start_view(verify = true)` SHA-256-hashes every section through the kept mapping. RssFile therefore grows to the whole setup.bin, including the table stores and other non-view sections (≈ 10.4 GiB file vs 6.66 GiB view at AR 1M), not just the `view_bytes` the plan counts. These are clean, reclaimable file pages, so not an OOM risk. Under a cgroup limit they do count toward usage until reclaimed. State this in the plan label.

### MINOR-5: test gaps
- No negative tests for `map_start_view`: malformed values, broken partition, wrong `code_ptr`.
- No calibrate admission test with the SetupView term (MAJOR-1).
- `setup_load.h` is not self-contained: it needs `island.h` (for `Neighbours`) included first. My probe failed to compile until I added that include.
- Equality tests on "mapped vs rebuilt" run both sides through the new engine, because the `dep::Start` overloads now flatten to StartView. The independent old-engine control below covers this; consider pinning one merge-base hash per fixture in the test.

## What I verified (items 1-5 of the brief)

**Spot-check of the first reviewer's evidence.**
- `AR_base.log` vs `AR_mapped.log`: identical across compat, law ×1/3 threads and V ×1/3 threads. The harness `island_compare.cpp` really uses `load_start` under `-DBASE`, built from a `git archive` of the merge base, and `map_start_view` at the head.
- `calibration_compare.log`: the script compares the section-table SHA-256 of all 40 non-meta calib.bin sections between the old and new `smcbvs4 calibrate` (compat 1, law 1/3, V 1/3); all equal.
- `fma_T3.log`: bit `44a15bfc6fb8d233`, A `e9cc4ab39f8a72db`, invariant over PM/LM, thread counts, G and tile.

The logs say what Codex's last message claimed.

**(1) Full suite and FMA CLI test.** Results are in the "Test runs" section below.

**(2) Allocation.**
- `IslandEngine`'s serial constructor calls `st.prepare(NT)` (`island_run.h:218`). `prepare` warms the static code tables and sizes each worker's scratch (`nz` K + 1; `lv`/`sc`/`e` C(max_m, ⌊max_m/2⌋), the largest within-size row; `codes` for m > 16; the fixed `lj`/`row`/`re[24]` cover rows of ≤ 21 entries).
- The draw sites are `init_particle` (inside `oom_guard`) and `step_nongibbs`, reached from `pm_round` and the LM walk, both inside `try { } catch (bad_alloc)`.
- The only heap left in a draw is the model's `push_back`, and `comp()`'s vector when k > 128. Both are identical to dep's and guarded.
- No StartView allocation is reachable in a parallel region outside a guard. Codex's global-new probe (3,000 draws × 3 workers, 0 parallel `new` calls) agrees.
- `scr()` throws `internal_error` (not caught by the guards) only if a thread id ≥ prepared count. This cannot happen under `num_threads(NT)`.
- Calibration islands run serially (`calib_backend.h:111,131`), so the "one engine per view at a time" rule holds.

**(3) Memory plan.**
- `read_setup_dims` sums the same 12 sections `StartView::bytes()` spans.
- `island_cmd.cpp:286` refuses (`internal_error`) if they differ after the load.
- `start_inputs_bytes` = view + `scratch_bytes(threads)` + neighbour CSR, used identically for `--plan-only`, the up-front refusal and the run.
- In `island`, admission (`:262`) comes before `load_data`, `load_start_view` and `load_neighbours` (`:283-287`), so PR52 MAJOR-2 is closed for the island command.
- `calibrate` also plans before loading, but its plan is incomplete (MAJOR-1).

Heap claim, MEASURED with this head's `v4_plan_tables --load 2`, AR n = 200, 96-thread scratch (`.rc_tmp/s1e4_load2.json`, `.rc_tmp/s3e4_load2.json`):

| p | J | mapped sections | StartView + nb + scratch (RssAnon) | expanded dep::Start (RssAnon) |
|---|---|---|---|---|
| 10⁴ | 757 | 63.9 MiB | **11.0 MiB** | **240.8 MiB** |
| 3×10⁴ | 2,269 | 191.6 MiB | **11.4 MiB** | **721.9 MiB** |
| 10⁵ (Codex, WP3's file) | 7,505 | 667.9 MiB | 12.8 MiB | 2,512.3 MiB |

dep::Start scales linearly (≈ 24 MiB per 1,000 p), which reproduces the 2,512 MiB figure. The StartView heap is almost constant: it is dominated by the 96-thread scratch at max_m = 14, about 10 MiB. The 2,512 → 12.8 MiB claim therefore holds, with the same accounting logic, at smaller p.

**(4) Mapping lifetime and safety.**
- **Lifetime:** `StartView::keep` holds `shared_ptr<fmt::Reader>`, which owns the mmap. Copies share it. In `island_cmd`, `calib_run` and `pilot_only` the view is a local that outlives `run_island` / `CalibIslandRunner`. The owning runner constructor declares `own_` before the `st_` reference. The `dep::Start` overloads keep their flattened temporary alive for the call.
- **Read-only:** `PROT_READ`, const spans, and no write path.
- **Hash before use:** `map_start_view` defaults to `verify = true`, a full section SHA-256 before any span is used, on all three paths. `read_setup_dims` before admission checks the header and table hashes only.
- **Bounds:** sections are 64-byte aligned with a dtype-multiple length (`format.cpp:131`). Shapes are checked: `code_ptr`/`logprof_ptr` start at 0, step 2^m and min(m, K) + 1, and end at the section length; `logF`, `cond0`, `size_*` lengths; `blk`/`pos`/`members` form a bijection. Every offset derived from the pointer arrays is therefore in range. Indices derived from values are not checked (MAJOR-2). The second open is not identity-checked (MINOR-3).
- **32-bit at 1M:** offsets are int64 or size_t, and section arithmetic is 64-bit.

**(5) WP3_PLANS rows.** AR 200 G = 1 and BLK 200 G = 256 were re-derived from the plan code (MINOR-1). The final-island and setup-input columns are right; the three calibration/merge columns are stale by about 0.7 GiB.

## Test runs (MEASURED, Owls, Xeon Gold 6148, g++ 11.5.0, `nice -n 19`, `taskset -c 0-2`, OMP 3)

**Portable full suite.** `tests/run_tests.sh --full --threads 3 --build-dir .rc_tmp/build_portable --keep`, log `.rc_tmp/full_portable.log`. Build flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`.
- **`v4_tests --full`: 177 test cases, 0 failed, 0 check failures.** This includes:
  - all core goldens (G1-G7, T11, island and calibration vs core engine);
  - `island_command_*` (5 tests);
  - `start_view_*` (3 tests);
  - the T7 gate.
- T3 portable: bit `44a15bfc6fb8d233`, A `d2df149413596a19`. Both match the pinned values.
- `start_view_mapped_wp2_setup` V/law/compat hashes: AR `bf63f80e…` / `5298f6a5…` / `c75513ef…`; BLK `0ad12c27…` / `eb1d5b4e…` / `ee17af9c…`. These are the same as the first reviewer's merge-base old-engine control.
- WP5: Slurm-driver tests OK (28); competitor harness OK; install script OK (9 checks).
- **WP4 R golden (`wp4_golden.R full`): not complete.** The run hit my 2 h background cap and was stopped during the last full case. Before that, all 7 cases (5 quick + 2 heavy: AR0.9_n100_p30_s34, AR0.6_n100_p40 + P2 tier-1 start, AR0.9_n120_p120, IND_n80_p60_Te3, AR0.5_n150_p300, AR0.7_n200_p1000, AR0.8_n200_p2000) reported `calibration == v3_calibrate, 0 failures` (504,676 checks in total). The T9 merge / T10 path steps after the last heavy case did not finish. The quick-mode WP4 golden cases are a subset of the cases that did finish.

**FMA build (`-DV4_ISLAND_ISA=x86-64-v4`).** `.rc_tmp/build_fma`, log `.rc_tmp/fma_cli.log`. The binary block reports `island_isa x86-64-v4`, `island_fma true`.
- `v4_tests --full island_command`: **5 / 5 pass**. Covered: end-to-end V/law/compat calibrate → island → merge through the CLI, the FMA-family refusal, the driver manifest, refusals/budget, and resume.
- `v4_tests --full start_view`: **3 / 3 pass**. Mapped = rebuilt in V/law/compat. The CLI island reads the mapped view, and the plan's setup inputs = sections + scratch + neighbours.
- `v4_tests --full t3_invariance`: **2 / 2 pass**. Bit `44a15bfc6fb8d233`, A `e9cc4ab39f8a72db`; the FMA pinned value matches.

**Reviewer probes** (all in `.rc_tmp/`):
- `s1e4/`, `s3e4/`: AR n = 200 at p = 10⁴ and 3×10⁴, made by this head's `gen → prep → setup`.
- `s{1,3}e4_load2.json`: the heap measurement.
- `probes/setupview_heap.{cpp,log}`: MAJOR-1.
- `s3e4/plan1800.json`: the MAJOR-1 admission.
- `probes/malformed_s1e4.log`: MAJOR-2, using Codex's probe binary copied in.
- `plans_{AR_n200,BLK_n200,IND_n1000}.log`: MINOR-1.
