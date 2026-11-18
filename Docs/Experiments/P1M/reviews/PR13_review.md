# PR #13 review — WP2 setup: correlation tiles, neighbour graph, exact/truncated partition (T11), tables, start law, start mode, setup.bin

Reviewer: Opus 5.5, high effort, independent of the author. Date: 2026-11-15.

PR: `exp/P1M-wp2-setup` @ `e9f90ce` → `exp/P1M-engine`. I reviewed only the four `WP2 setup:` commits
(`39c2f88`, `24843e9`, `c364178`, `e9f90ce`, i.e. `8ff9775..e9f90ce`).

Inputs:
- the review template (`briefs/REVIEW_PR_template.md`, N = 13);
- the WP brief (`briefs/WP2_setup.md`);
- the contract (`INTERFACES.md` v0.1.3);
- decisions D-4 and D-18 (`DECISIONS.md`).

Working conditions: read-only, in my own worktree (detached checkout). I pushed nothing and posted nothing on GitHub. I used
≤ 3 cores at `nice 19`, with `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261115-review-pr13`, which I removed
afterwards.

## Verdict: **ACCEPT-WITH-FIXES**

**Counts:** 0 CRITICAL, 2 MAJOR, 9 MINOR.

**Every bit-identity claim I checked holds**, both by reading the code against `core/` and by test:
- correlation tiles and neighbour graph;
- duplicate components and cut groups;
- exact dendrogram, cut and packing;
- tables, including the sorted-prefix Cholesky reuse;
- table top stores;
- start law;
- π₀ draws;
- start mode, including the tie-DP path.

**T11 holds.** The reasons:
- The argument (below) is a valid proof.
- The suite's T11 test checks it merge by merge, at the bit level, up to p = 20,000.
- My own exact-tie stress test passed. In it ≈ 95 % of merge heights are tied, unions of clusters with several members are
  compared under R13, and 10–13 merges fall exactly at height 1 − τ. The truncated forest agreed with `v3::complete_linkage`
  in every case.

**Both MAJOR findings are integration items, each with a small fix:**
1. The branch no longer merges into its base.
2. setup.bin's `meta` lacks the binary block that INTERFACES v0.1.2+ requires.

## Test runs (MEASURED, Owls `owls.stat.rice.edu`, Xeon Gold 6148, GCC 11.5.0, CMake 3.31.8, glibc 2.34, libm `840be1bb…3d7e` FMA variant)

| run | command | result |
|---|---|---|
| PR head `e9f90ce`, clean build | `tests/run_tests.sh --full --threads 3` (nice 19, make -j3) | **45 test cases, 0 failed, 0 check failures**, 9 min 10 s wall. T11 full: AR/BLK/IND/TIE at p = 20,000 (11,405 / 19,000 / 1,002 / 12,310 merges ≤ 1 − τ = 0.685302), AR strict at 20k, AR n = 400 at 10k: all pass. Tie-heavy start mode \|E\| = 128 |
| PR merged locally onto the current base `865f250` (INTERFACES v0.1.3; conflicts resolved by union, see M1) | `cmake` + `make -j2 smcbvs4 v4_tests v4_setup_bench`, then `v4_tests` (quick, 2 threads) | builds with **no warnings**; **49 test cases, 0 failed** (WP1 v0.1.3 tests + WP2) |
| reviewer's extra test (merged build) | 3 seeds × {Walsh h_a ± h_b (\|r\| ∈ {0, ½, 1}), Walsh h_a ± h_b ± h_c (\|r\| ∈ {0, ⅓, ⅔, 1})} with exact duplicates, shuffled; τ ∈ {0.3, 0.45, 0.5, 0.6, 1 − ⅔}, ≤ and <; truncated forest vs **`v3::complete_linkage` directly**; plus T11 at τ_n on the 12 duplicate-heavy designs below | **0 failures** in 66 T11 cases. 77–92 of 81–95 exact merges share their height with the previous merge. At τ = 1 − ⅔, 10–13 exact merges lie exactly at 1 − τ: ≤ includes them and < excludes them (69 vs 59, 71 vs 58, 68 vs 55 merges), and both match v3 |
| reviewer's extra test (start mode) | the Walsh designs + 12 random duplicate-heavy designs (p = 150–190, 4–7 duplicated signals, \|E\| up to **1,728**), exact and truncated partitions, caps {10⁶, 2, 3, 7, 50, 1000} × tie_dp {on, off} × {Auto, Enumerate, CountThenTieDP}, vs `v3::start_mode` | **0 failures**: same S, lg0 bits, ties, truncated, tie_dp_used |
| CLI end to end (merged build) | `gen` AR n = 200, p = 3,000 → `prep` → `setup --threads 1` and `--threads 3` → `info` | all `completed`. **41 of 42 section hashes are identical** across thread counts. Only `meta` differs (timings), so `content_sha256` differs (m3). `meta` has no `binary` key (M2) |

## Answers to the extra focus questions

**(a) T11: is it proved, including ties and the fl(1 − |r|) comparison?** Yes.

The argument in `partition.cpp:114-121` is a proof. Let d = fl(1 − fl(|G_jl| / (s_j s_l))), the bits that v3 uses
(`v3_blocks.h:15, 55`). The edge filter (`corr.cpp:189`) and the merge predicate (`partition.cpp:124, 130`) evaluate the same
expression `1.0 - absr` against the same double `hcut = 1.0 - tau`.

The induction has four steps:
1. **Heights do not decrease.** The Lance–Williams update for complete linkage, max(d(a,x), d(b,x)), never rounds and is
   ≥ the merge height. So the exact merges of height ≤ hcut form a prefix of the exact merge sequence.
2. **The queue holds exactly the admissible pairs.** By induction, the truncated queue Q holds exactly the pairs of live
   clusters whose complete-linkage distance passes the predicate: a merged cluster keeps a neighbour iff that neighbour was
   adjacent to both children.
3. **Both algorithms pick the same pair.** Both take the minimum under the same strict total order (distance, then R13 union
   order). Unions of disjoint live clusters are distinct, so the order has no ties and the set lookups by key are exact.
   v3's global minimum is therefore in Q whenever it passes the predicate.
4. **Q empties exactly when the prefix ends.** So the node ids, children (left = smaller minimum index), and the height bits
   coincide.

The suite's test (`test_setup.cpp:53-91`) checks:
- children and height bits for every truncated merge;
- that the next exact merge fails the predicate;
- that the clusters are identical.

It compares against v4's exact linkage. That exact linkage is a verbatim copy of v3's, and G2 checks it against
`v3::complete_linkage` up to p = 2,500.

The suite's tie coverage is thin (see m6):
- The TIE design ties only singleton duplicate pairs at d ≈ 0.
- Continuous heights never land on hcut.

My Walsh test closes both gaps (≈ 95 % tied heights, R13 comparisons of unions of clusters with several members, merges
exactly at hcut under ≤ and <) and passes.

One point needs a wording change, not a code change. The rule as implemented is fl(1 − |r|) ≤ fl(1 − τ), not |r| ≥ τ.
The two can differ within one rounding of the threshold. The PR states this (its known gap #2), but D-4 and the registry
still say "{|r| ≥ τ_n}" (m5).

**(b) Iterative start mode vs the recursive v3 code on tie-heavy cases.** Equal.

- **Enumeration** (`start.cpp:123-163`). It visits the same (level, size, code) sequence as `v3_start.h:281-300`: sizes
  increasing, codes increasing, leaf count and truncation at `count >= cap`, lex-min kept.
  - The `nz` push/pop bookkeeping is balanced.
  - `Fr&` is not used after `push_back`.
  - The stack is reserved to J + 1 frames.
- **`count_leaves`.** It reproduces v3's `ties = min(|E|, cap)` and `truncated = |E| ≥ cap`, with `__int128` saturation.
- **`CountThenTieDP` / `Auto`.** When |E| < cap, these return the tie-DP set instead of the enumeration's lex-min. That is
  valid because every element of E has size k_best, so for sets of equal size the greedy include-smallest-index choice is
  the lexicographic minimum (lemma TDP_E).
- **Incremental tie DP.** It makes the same decisions as v3's full recomputation:
  - fwd[b] depends on blocks < b and bwd[b] on blocks ≥ b;
  - `invalidate(bb)` moves F down to ≤ bb and Bk up to ≥ bb + 1, correctly;
  - "allowed unchanged → feasible" is sound, because the state is always feasible.
- **Tests.** The goldens (\|E\| = 128, all cap regimes, all three algorithms) and my 24 extra cases (\|E\| up to 1,728) all
  match.

**(c) 32-bit limits at p = 10⁶.** No overflow found.

- **Codes:** `uint32_t`, with m ≤ 16 checked (`tables.cpp:166`).
- **Code totals:** offsets are `int64_t` throughout (`code_ptr`, `logprof_ptr`, `cbs_ptr`/`sub_ptr`, `cond_ptr`, `arg_ptr`,
  `bptr`, the CSR `ptr`). At p = 10⁶ (B = 14), J·2^B ≈ 7·10⁸ codes, well inside int64. The global code index in
  `select_store` is `int64_t`.
- **Products are widened before multiplying:** `(size_t)j*B`, `(size_t)n*TW`, `(size_t)p*p`, `(size_t)(J+1)*(K+1)`,
  `64*(int64_t)p`, `40*p+1` in `uint64_t`.
- **Pairs and node ids:** the pair key is `uint64` packed (j<<32 | l). Node ids go to 2p − 1 < 2³¹.
- **Small counters:** `uint8_t` per-column counters with B ≤ 255 enforced (`corr.cpp:164`).
- **JSON:** `table_codes` (≈ 7·10⁸) is below 2⁵³. Table counters are hex.

Memory, not 32-bit limits, is the scale issue (m2, m3).

**(d) Thread invariance of setup.bin.** The content is invariant.

- **No race or order dependence found.**
  - Per-thread top-B lists are merged under a strict total order.
  - Edges are sorted by (j, l).
  - Tables are written per block.
  - Stores and the start law are serial.
  - Integer statistics are summed.
- **MEASURED:** all 41 non-meta section hashes are identical at 1 vs 3 threads (CLI). The suite also checks 1/2/3 threads
  and tiles 32/100/256/512.
- **The file content hash is not reproducible.** `meta` carries wall-clock timings and peak RSS
  (`setup_run.cpp:119-121`). The invariance test hides this by clearing `r.timings` before writing
  (`test_setup.cpp:129`). See m3.

**(e) Edits to WP1-owned files.** The edits are safe in substance, but they no longer merge (M1).

- **`CMakeLists.txt`** (lines 17-21, 42, 51-54): adds `src/setup/*.cpp` to `v4_bit` (correct flags), adds the two test
  sources and a `v4_setup_bench` tool. No flags or targets of WP1 change.
- **`stubs.cpp`**: removes the `setup` stub. `v4::setup::run(const Json&)` in `setup_run.cpp:160` has the declared
  signature, so the link stays whole.
- **`tests/run_tests.sh`** (lines 28-30): `--fixtures` also regenerates `setup_wp2`. Its `${TMPDIR:-/tmp}` fallback breaks
  the base's new rule ("set TMPDIR, never /tmp").
- **Conflicts:** `CMakeLists.txt` and `run_tests.sh` both conflict textually with `865f250`.
- **`tests/tk.h`** is untouched; `setup_tk.h` layers on it.

## Findings

### MAJOR

**M1. The branch does not merge into its base. GitHub reports `mergeable: CONFLICTING`.**
- **Where:** `CMakeLists.txt:42, 51-54`; `tests/run_tests.sh:28-31`.
- **Evidence:** `exp/P1M-engine` moved to `865f250` (PR #11 fixes + PR #14, INTERFACES v0.1.3). `git merge-tree` reports
  conflicts in both WP1-owned files:
  - the `v4_tests` source list (`test_cli.cpp` vs `test_setup.cpp golden_setup.cpp`);
  - the tool targets (`v4_bench_store` vs `v4_setup_bench`);
  - the runner's tail (`allow=()` vs the WP2 fixture block).
- **Effect:** none in substance. Resolved by union locally, the tree builds without warnings and passes 49/49 (quick).
- **Fix:**
  - Rebase on `865f250` and take the union in both files.
  - In `run_tests.sh`, use `"$TMPDIR/v4_fixwork_wp2"` (no `/tmp` fallback).
  - Keep `args=("${allow[@]}")`.
  - Re-run `--full` after the rebase.

**M2. setup.bin `meta` has no binary block (INTERFACES v0.1.2+ §5.1, §5.3).**
- **Where:** `setup_run.cpp:105-122`.
- **Rule:** §5.1 says "A `meta` json section in every file holds … the binary block (§5.3), so the content hash changes with
  the binary". The merge refuses islands whose binary blocks differ.
- **Evidence:** on the merged build, `meta` keys are B, J, K, cut_group, …, timings, with **no `binary`**. `data.bin`'s
  meta has `m["binary"] = binary_block()` (base `prep.cpp:117`). The PR acknowledges this as pending WP1 (known gap #4).
  WP1's code is now merged.
- **Effect:** two setup.bin files from different binaries can share a content hash.
- **Fix:**
  - Add `m["binary"] = binary_block();` (and, optionally, `m["schema"] = "smcbvs4.setup/1"`, as data.bin has).
  - Add a test that `meta.binary` exists.
  - At the same time, remove the now-redundant own guard (m4).

### MINOR

**m1. T11 tie coverage in the suite is thin. The claim holds, but the committed tests do not exercise the hard cases.**
- **Where:** `test_setup.cpp:83-91`; `setup_tk.h:65-70`.
- **Evidence:**
  - The TIE design ties only singleton duplicate pairs at d ≈ 0.
  - No union-lex comparison between clusters with several members.
  - No merge height equal to hcut (heights are continuous, so ≤ and < give identical forests: "907 merges" both ways).
- **Fix:** add the reviewer's exact-tie design as a unit case. The fixture:
  - n = 64;
  - columns h_a ± h_b over Walsh vectors h_k[i] = (−1)^popcount(i & k), a < b ≤ 10;
  - and h_a ± h_b ± h_c, a < b < c ≤ 8;
  - plus 6 exact duplicates, columns shuffled.

  Compare with τ ∈ {0.3, 0.5, 1 − ⅔} under ≤ and <, against `v3::complete_linkage` directly. With τ = 1 − ⅔ it puts 10–13
  merges exactly at hcut and separates the ≤ and < forests (69 vs 59 merges). It runs in milliseconds.

**m2. Peak memory at p = 10⁶ is set by the table stage, and D-18 does not reduce it.**
- **Where:** `tables.cpp:131-138, 169-170, 197`; `build_start` at `tables.cpp:252-253`.
- **Evidence:** with NG ≈ 7·10⁸ codes (mean block 13.2, PR measurement), these arrays coexist:
  - `logr` (8·NG);
  - the transient `logm` (8·NG);
  - `k` (NG);
  - `select_store`'s `tmp` (up to 8·NG).

  That is ≈ 17–18 GB. Afterwards `codes_by_size` (4·NG) and `sub_cum` (8·NG) are still built in memory for all blocks. The
  PR's ESTIMATE is a 25 GB setup peak.
- **Context:** D-18 (DECIDED) removes the two sections from the file only.
- **Fix, when implementing D-18:**
  - Do not materialise `codes_by_size`/`sub_cum` at all; recompute them per drawn block.
  - Pick the store threshold without `tmp`, e.g. a per-block top-c pre-filter or a bounded heap over (value, g).

  Until then, setup at 10⁶ needs a large-memory node; say so in the run plan.

**m3. The setup.bin content hash changes on every run, and the invariance test hides it.**
- **Where:** `setup_run.cpp:119-121`; `test_setup.cpp:129`.
- **Evidence:** `meta.timings` (seconds, peak RSS) is part of the hashed table. MEASURED: threads 1 vs 3 give identical
  non-meta sections but different `content_sha256`.
- **Why it matters:**
  - INTERFACES §5.1 permits run-specific content in meta, because T2 compares non-meta sections.
  - But a re-run of `setup` (e.g. a retry) yields a new file identity, so manifests written against the first file refuse
    the second.
  - Two runs with identical inputs never share a content hash.
- **Fix (either):**
  - move timings and RSS to the `<out>.json` record only (it already carries `seconds`), so setup.bin is reproducible; or
  - keep them and change the test to compare non-meta section hashes **without** clearing timings.

**m4. setup has its own libm guard with a bypass flag. Both are superseded by v0.1.3.**
- **Where:** `setup_run.cpp:161-163`.
- **Evidence:**
  - The command refuses unless `pm::fma_variant_expected()`, and accepts an undocumented `allow_non_fma_libm` override.
  - Under v0.1.3, `main` calls `require_bit_libm()` (function-result self-test) for every command before dispatch. So the
    guard in setup is redundant and keys on the superseded criterion.
  - The bypass flag also contradicts "Binding: glibc 2.34 libm (no bundling)".
- **Fix:** delete both lines after the rebase.

**m5. The truncation rule is a height predicate, but D-4 and the registry state it as an edge predicate.**
- **Where:** `partition.cpp:124, 130`; `corr.cpp:189`.
- **Evidence:** the code merges iff fl(1 − |r|) ≤ fl(1 − τ) (or <). D-4 says "on the sparse graph {|r| ≥ τ_n}". They differ
  only within one rounding of the threshold.
- **Assessment:** this is the correct choice for T11 to be an exact identity. But the law's definition should say so.
- **Fix:** have HQ/Theory word D-4 / THEORY-1 as "merge heights d = fl(1 − |r|) ≤ fl(1 − τ_n)", with ≥/> as the `strict`
  sub-choice. Record `strict` and `tau` in the registry entry. Both are already in `meta`.

**m6. "Packing by minimum index" (D-4) is not tested.**
- **Where:** `test_setup.cpp:102, 107`.
- **Evidence:**
  - `unit_truncated_partition_shape` declares `prev_min` and discards it (`(void)prev_min;`). The order of the retained
    clusters and the next-fit rule are therefore never checked.
  - The goldens on the truncated partition feed v4's own partition to v3, so they cannot catch a packing error.
- **Assessment:** the code (`partition.cpp:189-216`) is correct as read.
- **Fix:** in the shape test, recompute the retained clusters from the forest (cut at > B, left first), sort them by
  `minidx`, next-fit them, and compare the result with `P.members`/`P.bptr`.

**m7. Exact mode has no memory guard.**
- **Where:** `partition.cpp:54`.
- **Evidence:** `std::vector<double> dist((size_t)p * p)` needs 8p² bytes: 80 GB at p = 10⁵. The `bad_alloc` →
  `resource_limit` mapping (`setup_run.cpp:56`) depends on the allocator. With overcommit, the process can instead be
  OOM-killed with no record written.
- **Fix:** refuse `partition=exact` up front with `resource_limit` (or `invalid_input`) when 8p² exceeds a stated limit (a
  parameter, default e.g. 32 GB), and state the limit in the record.

**m8. Exceptions other than `Error` thrown inside the OpenMP regions terminate the process.**
- **Where:** `tables.cpp:181-187`; the sink lambda at `corr.cpp:180-193`.
- **Evidence:** `build_tables` catches only `Error` inside the parallel loop. `correlation_pass`'s sink pushes onto vectors
  inside `omp parallel`. A `std::bad_alloc` there escapes an OpenMP structured block, which calls `std::terminate`. The
  command then exits without a record or status, against §7 "commands catch everything at main".
- **Fix:**
  - In tables, `catch (...)` alongside the existing handler, setting a captured status (`resource_limit` for
    `bad_alloc`).
  - In the correlation pass, the same, with a flag checked after the region.

**m9. Small items.**
- **Per-thread top-B memory scales with the thread count.** `corr.cpp:174-179` costs ≈ 13·p·B bytes per thread: 0.55 GB
  at p = 10⁶, B = 14, so ≈ 26 GB at 48 threads on NOTS. Cap the number of top-B lists, or shard columns by owner.
- **The R script's default work directory lands inside the fixtures tree.** `tools/golden_setup_ref.R:9` defaults it to
  `tests/fixtures/core_copy_wp2` when the third argument is omitted, leaving a compiled core/ copy there. Require the
  argument, or default to `$TMPDIR`.
- **No CLI test for `setup`.** The base now has `tests/test_cli.cpp` with `V4_SMCBVS4`. Add a gen → prep → setup →
  `info` case that checks the exit code, the `status` and the sections.
- **The mode/partition pairing is implicit.** The default is `file_mode = law` with `partition = truncated`, and only
  compat refuses truncated (`setup_run.cpp:178-180`). Make the pairing explicit in the command help and the record. For
  example, should law/T at p ≤ 2·10⁴ default to the exact partition?

## Contract conformance (INTERFACES v0.1.3)

| item | status |
|---|---|
| §2 `Neighbours`, `Partition`, `Tables`, `Start` (types, layouts, `comp`, `draw_pi0(UniformSource&, Address, Model&)`) | conforms (`Neighbours` is `using = Csr`, same fields) |
| §3 π₀ uniforms at slots 0…u−1 in v3 draw order | conforms (slot = `a.slot + t`) |
| §5.1 setup.bin section names | conforms (all listed sections present). Adds `scalars_f64`, `scalars_i64` (allowed) |
| §5.1 `meta` holds the binary block | **deviation (M2)** |
| §5.1 u64 in JSON as hex | conforms (`table_stats`) |
| §6 guard = `require_bit_libm()` | **deviation (m4)**, own superseded check + bypass |
| §7 statuses, GUARD-W (no file unless completed) | conforms (`setup_run.cpp:83, 184`). See m7, m8 for crash paths |
| §7 thread rules | conforms. Results do not depend on threads (MEASURED) |
| §1 fixtures ≤ 20 MB | conforms (`setup_wp2` 2.2 MB) |
| D-18 (drop `codes_by_size`/`sub_cum` from setup.bin, on-demand recomputation) | not in this PR. It waits for INTERFACES v0.1.4 (WP1). Track it as a WP2 follow-up with D-18's bit test (draws identical with and without the stored sections), and see m2 |

## Discipline
- **Nothing is written outside `engine_v4/`.** Beyond the WP2 files themselves, the PR touches only the three WP1-owned
  files discussed in (e).
- **No hard-coded paths:**
  - fixtures are located via `V4_FIXTURE_DIR`;
  - the bench via CLI arguments;
  - the R script via its arguments (but see m9).
- **No file over 50 MB.** The largest is `AR_n200_p300/logr.f64`, 0.56 MB.

## Suggested order before merge
M1 (rebase), M2 + m4 (meta binary block, drop the own guard), then m3 and m6. Then re-run `--full`. The other items can
follow with the D-18 work.
