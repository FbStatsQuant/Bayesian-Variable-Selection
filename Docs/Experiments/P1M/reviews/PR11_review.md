# PR #11 review — WP1: engine_v4 skeleton, container, Philox + compat streams, Store/Ledger, Bit scorer, gen, prep, fixtures

Reviewer: Opus 5.5 (independent of the author), 2026-11-15. PR `exp/P1M-wp1-skeleton` @ `8ff9775` → `exp/P1M-engine`.
Brief: `briefs/REVIEW_PR_template.md` (N = 11), `briefs/WP1_skeleton.md`, `briefs/BUILD_COMMON.md`; contract `INTERFACES.md`
v0.1.1. I worked read-only in my own worktree (detached at `origin/exp/P1M-wp1-skeleton`), pushed nothing and posted no
comments on GitHub.

## Verdict: **ACCEPT-WITH-FIXES**

- **Counts:** 0 CRITICAL, 1 MAJOR, 11 MINOR.
- **Bit-identity claims hold.**
  - The Bit scorer is a statement-by-statement copy of `core/cpp/v3_score.h:76-246`, including operation order and the
    v3 flags.
  - The Gram-free `gram()` gives the stored-Gram bits, because the product is commutative and the sum is sequential in i.
  - `prep` reproduces R's `real_mean` and `rsum`.
  - Philox matches the Random123 known-answer vectors, and the compat xoshiro streams equal v3's.
  - Store and Ledger equal `v3::TopStore` for any offer order.
  - The golden tests really compare against `core/`: against the v3 headers compiled unchanged in `v4_tests`, and against
    fixtures written by R-compiled `core/` (`tools/make_fixtures.R`).
- **What needs fixing:**
  - The MAJOR finding is a scale and contract issue that WP3 inherits: the memory of the top store and of the per-thread
    ledgers at p = 10⁶. It should be settled in INTERFACES before WP3 codes against rule §7(4).
  - The MINOR findings are small fixes or deferred obligations, which should be logged.

## Test run (MEASURED)

| | |
|---|---|
| Machine and toolchain | Owls (`owls.stat.rice.edu`, Xeon Gold 6148), GCC 11.5.0, CMake 3.31.8, glibc 2.34 (libm sha256 `840be1bb…3d7e`, FMA variant) |
| Command | `TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261115-review-pr11 tests/run_tests.sh --full --threads 3` (nice 19, make -j3), clean build |
| Result | **28 / 28 PASS**, 0 check failures; 24.2 s wall (39.4 s user) |
| Golden counts | 1,608 R `cpp_score` values; 773,998 `v3_setup` table entries; 5 R prep cases (1 anchored column); 4 designs × 3,000 random models plus n = 30 up to K against the core headers; 231 forced-route comparisons |
| Fixtures | 13 MB, 73 files; every SHA-256 matches `tests/fixtures/MANIFEST.json` (checked independently) |

Extra probes I ran (MEASURED, Owls, nice 19, 3 threads):
- **gen and prep at p = 10⁵, n = 200.** `gen` took 3.1 s and 160 MB RSS. `prep` took 7.3 s and 318 MB.
- **Container check.** `info` (full hash verification) of the 160 MB `data.bin` took 3.6 s, about 45 MB/s under nice. The
  PR quotes 140 MB/s.
- **Round trip.** `load_data(data.bin)` equals `make_data` from `raw.bin`: X, z, diagG and a k = 4 score are identical.
- **Manifest.**
  - A manifest with a wrong `inputs` hash is refused: status `invalid_input`, exit code 13.
  - A correct manifest runs.
- **Header tampering.** Changing the header `mode` byte to 3 is **not detected**: `info` reports `mode: V`, status
  `completed`, and the same content hash (finding 5).
- **Store probe.** `Store(40p+1, HPM)` at p = 10⁵ (c = 4·10⁶), with 1.6·10⁷ offers at k = 7 and improving values, took
  21.6 s and **724 MB peak RSS** (about 181 B per cap entry). See finding 1.

## Findings

### 1. MAJOR — top-store memory at p = 10⁶, and per-thread ledgers each holding a full top-(40p+1) store
- **Where:**
  - `src/common/store.cpp:39`: `offer` compacts only after `max(cap, 1024)` buffered offers, so the buffer reaches 2c.
  - `src/common/store.cpp:42-60`: `compact` holds the old 2c arrays, the new c arrays and a 2c index at the same time.
  - `INTERFACES.md:254`, §7 rule (4): "per-thread `Ledger`s merged by `Ledger::merge`".
  - `src/common/ledger.cpp` `init`: every Ledger gets `top` with cap 40p + 1.
- **Evidence:**
  - Measured peak at c = 4·10⁶ was 724 MB, so about **7 GB per store at p = 10⁶** (ESTIMATE, linear scaling, k = 7).
  - ENGINEERING_SPEC §2 budgets 2.2–4.5 GB for 2c.
  - Under §7(4), each of the 48 threads of an island owns a Ledger with its own c = 4·10⁷ store. Each thread's quick
    reject only knows its own worst entry, so each thread store fills to c and buffers up to 2c. That is O(threads × 7 GB)
    in the worst case, which does not fit on a node.
  - The reference implementation is correct; this concerns the contract that WP3 builds on. The PR does flag that
    "`Store::offer` ... needs WP3 tuning", but not the per-thread multiplication.
- **Fix:** add a line to INTERFACES now (WP1 owns it), for example:
  - per-thread ledgers hold **bounded offer buffers**, not full stores;
  - the buffers are flushed into one island store at fixed chunk boundaries, serially in chunk order. The result is
    order-free anyway;
  - workers read a shared, monotone "worst kept" threshold, so they can quick-reject early.
  - In `compact`, use `std::nth_element` / partial sort to cut to c before the full sort, and reserve the vectors;
    otherwise geometric growth adds up to 2× capacity slack.
  - Re-measure bytes per entry at p = 10⁵ and fix the ESTIMATE in spec §2.

### 2. MINOR — the libm guard is not enforced, and records carry no binary / libm block
- **Where:**
  - `src/common/pmath_info.cpp:12` (`fma_variant_expected`) is called only by `smcbvs4 version`, `v4_pmath_check` and a
    test.
  - `src/cli/main.cpp:68-71`.
  - `gen` and `prep` records and `meta` sections have no `binary` or `libm` fields.
- **Evidence:**
  - INTERFACES §6 says `fma_variant_expected()` "must be true for any bit-form run; the manifest records libm path +
    SHA-256 and `libm_fma_variant`".
  - `gen` itself depends on libm: the polar method calls `pm::log` (`gen.cpp:72`), so `raw.bin` bits depend on the ifunc
    variant. The hash makes a difference detectable, but not explainable.
  - No bit-form command exists yet, so this is a deferred obligation, not a defect today.
- **Fix:**
  - Add `pm::require_bit_form()`, which throws `invalid_input` when the guard is false.
  - Add one `binary_block()` helper (sha256 of `/proc/self/exe`, git commit, compiler, flags, libm path / sha / variant).
  - Call both in `main` for every command, and write the block into every record and `meta`.
  - Note it for WP3 and WP4.

### 3. MINOR — the brief's "test both" for prep: the `--from-r` path is untested and partly unhashed
- **Where:** `src/common/prep.cpp:154-170`.
- **Evidence:**
  - No test calls `prep::run` with `from_r` (searched for `from_r` / `from-r` in `tests/`).
  - Only `meta.json` and `Xs.f64` go into `inputs`. `ys.f64` and `col_*.f64` are read but not hashed.
  - `kept` and `dropped` are not checked against p and p_raw.
- **Fix:**
  - Add a test that writes the R-standardised fixture (`prep/scaled_*`) as a from-r directory and checks that `data.bin`
    equals the C++ path bit for bit.
  - Hash all six input files.
  - Validate `kept.size() == p` and `kept ∪ dropped = 1..p_raw`.

### 4. MINOR — golden tests pass when fixtures are missing; missing files cause out-of-range reads
- **Where:**
  - `tests/test_prep.cpp:49, 108, 132`: `SKIP` returns, and the case is reported as PASS.
  - `tests/test_prep.cpp:13-18, 90-95`: `read_f64` / `read_i32` return `{}` when a file is absent, and the result is
    then indexed.
- **Evidence:** a broken checkout or a moved fixture directory turns the bit tests green.
- **Fix:**
  - The fixtures are committed, so make a missing `index.json` a FAIL, unless `--allow-missing-fixtures` is given.
  - Check every vector's length against `index.json` before indexing.

### 5. MINOR — header fields are outside every hash; `mode` is not in `meta`
- **Where:**
  - `src/common/format.cpp:66` and `:109`: the content hash is the table SHA only.
  - `gen.cpp:168, 188` and `prep.cpp:98` write `M_NONE`, and their `meta` has no `mode`.
- **Evidence:**
  - Changing `mode` (and likewise `kind`, `format_version`) in the header leaves the content hash unchanged and is
    accepted (probe above).
  - INTERFACES:180: "A `meta` json section in every file holds ... its inputs' content hashes and the mode". `raw.bin`
    has neither `inputs` nor `mode`. Mode 0 ("none") is not one of the contract's modes 1, 2, 3.
- **Fix:**
  - Either compute the content hash as SHA-256(header with `table_sha256` zeroed ‖ table), or require `kind` and `mode`
    in `meta`.
  - Add `mode 0 = none (gen/prep outputs)` to §5.1 with a changelog line.

### 6. MINOR — `compat_stream` accepts tiers it cannot map
- **Where:** `include/v4/rng.h:84-92`.
- **Evidence:** `R_PILOT` with tier 2 returns 10, which is final island 1's stream. `R_DIAG` with tier 2 returns 11–14.
  v3 has only tiers 0 and 1 (`core/v3_run.R:8-11`).
- **Fix:** throw when `tier > 1` for PILOT / DIAG, and add a `CHECK_THROWS` test.

### 7. MINOR — contract items marked WP1 that are not implemented or not true of the tree
- **Where and evidence:**
  - INTERFACES:31 and :259 name `include/v4/types.h`, which does not exist. The types live in `data.h` and `model.h`.
  - INTERFACES:29 says the runner runs "R golden scripts if R is present". It does not. `prep.h:3` cites
    `tests/golden/prep_golden.R`, which does not exist. The golden comparisons are fixture-based, inside `v4_tests`.
  - INTERFACES:102: "Debug builds log every address and assert uniqueness (I5)". §3 compat: "debug builds check that the
    address sequence is strictly increasing". Neither is in `rng.h` or `CompatSource`.
  - The CLI has `gen-test` and `version` commands that the §1 command list does not include.
- **Fix:** either implement the debug address checker now (`rng.h` is WP1's: a thread-local set or sequence check under
  `#ifndef NDEBUG`), or move the item to WP3 in the changelog. Correct the file names and the runner description in
  INTERFACES.

### 8. MINOR — the address table's slot rule for the independence move is ambiguous
- **Where:** `INTERFACES.md:98`: "I: 0…k−1 the π₀ draw, then k accept".
- **Evidence:** a π₀ draw consumes a data-dependent number of uniforms: 1 size, then block sizes for b = J..1 while any
  remain, then one submodel per block with k_b > 0 (`core/v3_run.R` variate-order doc). Read as |S|, "k" gives clashing
  addresses. Read as "number consumed", it is correct but implicit.
- **Fix:** write "slots 0…u−1 for the u uniforms of the π₀ draw, then slot u for accept". Better, use a fixed accept
  slot (for example `0xFFFFFFFF`), so that the accept address does not depend on the draw.

### 9. MINOR — `prep` statuses `no_predictors` / `y_constant` exit 0 with no `data.bin`
- **Where:** `src/common/prep.cpp:182-185`.
- **Evidence:**
  - The record says `status: completed` and gives `prep_status` separately.
  - A Slurm chain that keys on the exit code goes on to `setup`, which then fails with `invalid_input` on a missing file.
  - Neither status exists in the INTERFACES §7 enum.
- **Fix:** document in §7 how prep-level statuses map onto task / fit statuses (v3 treats them as fit outcomes), and have
  the driver (WP5) check `prep_status`. Or write a `data.bin` stub that carries the status.

### 10. MINOR — hash verification cost at p = 10⁶, done twice per job
- **Where:**
  - `src/cli/main.cpp:52-56` verifies every manifest input with a full `Reader`.
  - The command then opens the file again, and `Reader(path, verify = true)` (`prep.cpp` `load_data`) hashes it a second
    time.
- **Evidence:**
  - Measured 45 MB/s under nice (the PR says 140 MB/s).
  - ESTIMATE: 1.6 GB `data.bin` at p = 10⁶ takes 12–36 s per pass; × 2 passes × every island / merge job.
- **Fix:**
  - Keep the verified `Reader`s from the manifest check and pass them to the command; or hash only the table at the
    manifest step and verify sections once on open.
  - Consider a multithreaded section hash (sections are independent).

### 11. MINOR — robustness of the `Reader` and `load_data`
- **Where:**
  - `src/common/format.cpp:113`: `e.offset + e.length > size_` can wrap around on crafted values, and nothing stops a
    section from overlapping the header or table.
  - `src/common/prep.cpp:128-130`: `z`, `diagG`, `col_*` and `kept` lengths are not checked against p.
  - `format.cpp` `write`: the parent directory is not fsync'd after `rename`.
- **Fix:**
  - Check `e.length <= size_ && e.offset <= size_ - e.length && e.offset >= 128 + 128·n_sections`.
  - Check every section count in `load_data`.
  - Fsync the directory (cheap).

### 12. MINOR — small items
- **R overflow branch** (`prep.cpp:17-18`). It divides `x[i] / (long double)n`, but R's `real_mean` overflow branch
  computes `dx[k]/n` in double. The branch cannot be reached after the division by max|x|. Copy R exactly anyway, or say
  in a comment that it is unreachable.
- **JSON precision** (`json.h:17-20`). Every number is a double, so u64 values above 2^53 (Zobrist keys, hashes, large
  counters) lose bits if they are ever put into `meta` or records. Store them as hex strings, and say so in §5.1.
- **Build location** (`tests/run_tests.sh:8`). The default build dir is `${TMPDIR:-$here}/v4_build`. Without TMPDIR it
  builds inside the source tree, and `v4_build` is not git-ignored.
- **`/tmp` fallback** (`run_tests.sh:26`). It falls back to `/tmp`, which breaks the "never /tmp" rule. Fail instead
  when TMPDIR is unset.
- **Untested comparison field** (`tests/test_score.cpp:27-28`). `compare_models` does not compare `cond_A`, which
  `error_bound` uses. Add it.
- **Missing CLI test.** There is no test of `prep::run`, `write_data` / `load_data` or the manifest refusal at CLI level.
  The README says "unit tests; input-hash refusal". My probes show they work; add them to `v4_tests`.

## Checklist summary

1. **Correctness.**
   - Scorer, linear algebra, q_nonneg, constants (`data_constants`, `log_sum_exp` with a long-double accumulator,
     `lchoose_d`), Zobrist, the orders, Store / Ledger semantics and island_best are faithful copies of `core/`.
   - No index-convention errors: internal 0-based int32, `orig` 1-based.
   - At p = 10⁶, every n·p product goes through `size_t` / `uint64_t`; `40p + 1` is uint64; the Store index is uint32
     (fine for 2c < 2³²); Philox field ranges are checked.
   - No races: `gen` writes disjoint entries, verified at 1, 2 and 3 threads, and `chunked_sum` is deterministic.
2. **Tests.**
   - The goldens are real comparisons against `core/`.
   - Edge cases covered: empty model, k = K (n = 30 and R's `seq_len(K)`), ties (Store / Ledger), forced routes,
     `q_nonneg`, a dropped constant column, an anchored near-constant column, NaN → `NumericalFailure`.
   - Gaps: findings 3, 4 and 12.
3. **Contract.** Deviations are listed in findings 2, 5, 7, 8 and 9. The INTERFACES copy in the branch is identical to
   the docs copy (v0.1.1).
4. **Scale.**
   - `gen` and `prep` are fine (ESTIMATE about 1.6 / 3.2 GB at 10⁶).
   - The scorer is Gram-free.
   - The Store and per-thread ledger memory is the open item (finding 1); hash time is finding 10.
5. **Discipline.**
   - The diff touches only `Scripts/SMC_BVS/engine_v4/`, and `core/` is unchanged.
   - No hard-coded paths, apart from the `/tmp` fallback in `run_tests.sh:26`.
   - The largest file is 4.7 MB and the fixtures total 13 MB (≤ 20 MB).
