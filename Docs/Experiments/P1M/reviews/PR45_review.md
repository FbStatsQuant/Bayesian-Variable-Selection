# PR #45 review — WP1 Store bulk loader + pair sort + one-per-model I1 check; INTERFACES v0.1.14

Reviewer: Opus 5.5 (high), independent of the author. 2026-11-16.
PR: https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/45 (head `bf7daa23`, base `exp/P1M-engine` at
`571f11bc` = merged PR #40). Checkout: detached `origin/exp/P1M-wp1-store-perf` in my own worktree. Read only.
Machine: Owls (Xeon Gold 6148, GCC 11.5.0), `nice -n 19`, ≤ 3 threads; benches single-threaded, one at a time; load
average 16–25 during the runs (other departments' jobs).

## Verdict: **ACCEPT-WITH-FIXES** (0 CRITICAL, 0 MAJOR, 4 MINOR, 4 INFO)

The code is correct. The bulk loader refuses every bad input I could make (1,547 hostile and randomised checks, 0
failures). Its content equals the offer + compact path bit for bit, and a loaded store behaves identically under later
offers. On a real merge the fit.bin is the same section for section (§(b)). The timings reproduce. The fixes are in
the contract text: v0.1.14 §7 describes WP4's **pending** calibration memory rule, which is not on the base branch and
contradicts the `calib_backend.h` comment there. Some §5.1 lines are slightly too strong, and there is one stale
§4.1 comment. None of this blocks the code. The text should be corrected, or the merge ordered after WP4's
`exp/P1M-wp4-calib2`.

## (a) The bulk loader refuses unsorted and duplicate input

Code read: `src/common/store.cpp:161-195`.
- **Order of checks:**
  - empty store, else `internal_error`;
  - `n ≤ cap`;
  - per entry: pool range (`len > pool_n || off > pool_n − len`, no overflow), NaN, `is_sorted_unique(S)`, and strict
    `better(prev, cur)` under the store's own order;
  - then copy, then one (hash, lex) pair sort. Equal neighbours = the same model twice, which resets the store with
    `init(cap, ord)` and throws `invalid_input`.
- **No partial state:** every refusal before the copy leaves the store untouched, and the duplicate refusal resets it.
- **Cut-off:** set exactly as `compact()` sets it.
- **The index:** the pair sort yields the unique (hash, lex) order. That is the order `compact()`'s index merge
  produces, so `hidx_` is the same and later `offer`/`compact` behave identically.

**Hostile tests I wrote** (`adv.cpp`, linked against the head `libv4_bit.a`). Each refusal is checked for status
`invalid_input`, an empty store afterwards (size 0, staging 0, cut-off −∞), and that the store can be reused:

| input | result |
|---|---|
| values ascending | refused |
| exact duplicate, adjacent | refused (strict order) |
| same model at 3.0 and 2.0, non-adjacent, otherwise sorted | refused (pair sort) |
| same model at F and nextafter(F), adjacent | refused |
| HPM tie: larger \|S\| first; HPM tie: lex reversed | refused |
| LEX order tie, lex reversed (and lex ascending accepted) | refused / accepted |
| model unsorted `{2,1}`; model with a repeat `{1,1}` | refused |
| NaN first / NaN second | refused |
| pool short by one; offset `UINT64_MAX − 1` (overflow probe); `len` 60000 beyond the pool | refused |
| n = 5 > cap = 4 | refused |
| duplicate as the last entry of a full store (n = cap) | refused, store reset, cut-off −∞ |
| target store not empty (one staged offer) | `internal_error` |
| ±∞ values, the empty model, cap 0 / n 0 | accepted, `check_invariants` true |
| **300 random stores** (HPM/LEX, cap 1–300, up to 900 offers, 1-ulp value variants): bulk vs offer path | equal `content_hash` and cut-off, `check_invariants` true |
| the same 300, then the raw stream re-offered at nextafter values into both | equal `content_hash` afterwards (index equivalence) |
| the same 300 with one entry's model overwritten by another's (same hash) | refused (every case) |
| a valid loaded store with that duplicate injected into its public arrays | `check_invariants` returns false (every case) |
| eval reader: hand-made `fit.bin` with a model twice / without | refused with `invalid_input` ("a model appears twice …") / accepted |

**Total: 1,547 checks, 0 failures.**

One gap: an input holding the same model under two **different** hashes is accepted (MINOR-4). This is not a
regression: the old offer path behaves the same.

## (b) Bits: content hashes, goldens and fit.bin on a real merge

- **Store benches** (cap 4·10⁷ + 1, k = 7), base `571f11bc` vs head:
  - `load` content hash `78d3ee905e7b5987`: base offer path, head offer path and head bulk all equal;
  - `merge` (3 islands, 50 % shared) `bc0c256cd1d1bbcd`: base = head;
  - my shape-1 merge `2fd0f5a52f41f7f8`: base = head.
- **Golden and v4_tests:** see "Test runs" below.
- **fit.bin on a real merge:**
  - I ran a copy of `wp4_golden.R` with one added line, after the T9-files merge, that keeps each case's `fit.bin`
    (that merge goes data/setup/calib/island files → `smcbvs4 merge` in process).
  - I ran it against the base tree (`git archive 571f11bc`) and against head.
  - I compared the two with `fitcmp.cpp`: the SHA-256 of every section, plus every `meta` key except `timings` and
    `binary`.
  - That path goes through all the new load sites: `load_island_full` (bulk), `read_store` for the setup table stores
    (bulk) and `Ledger::merge` (pair-sort `compact`).
  - **Result:** in all 5 quick cases (AR0.5_n150_p300, AR0.6_n100_p40, AR0.9_n100_p30_s34, AR0.9_n120_p120,
    IND_n80_p60_Te3), **all 39 data sections of fit.bin are identical** between base and head. These include the top
    store, log Z, PIPs, HPM and provenance, the local search, the occupancy rows and the counters.
  - **Two meta keys differ, both explained:**
    - `mem_estimate`: the intended 26 → 30 + 4k change (e.g. `merged` 225,475 → 241,485 B);
    - `inputs`: the input files' content hashes cover their own `meta`, and that holds the build's binary/git block.
      The base was built from `git archive`, with no git. `data.bin`'s hash differs too, and this PR does not touch its
      writer.
  - Golden on both trees: 443,598 checks, 0 failures.

## (c) Every edit outside WP1's `store.*`

| file | edit | check |
|---|---|---|
| `src/island/island_impl.h:89-90` (WP3 `to_record`) | offer + compact → `load_unique_sorted` | The island `TopStore` keeps one entry per model with its max value (`include/v4/island/store.h:3-10`), HPM order, cap 40p + 1 = the record ledger's cap (`ledger.cpp:53`). The input is therefore valid and the content is the same. **Behaviour change:** an island run with `store_cap` > 40p + 1 would now throw instead of truncating. No caller does this: `store_cap` is not exposed in the CLI, and the only non-default use (test_island.cpp:698, 2000) never calls `to_record`. The error status for internal data is `invalid_input` (INFO-2). OK. |
| `src/island/island_file.cpp:96-97` (WP3 reader) | new section-length check, then bulk load | OK. The pool range and order are verified by the loader. The hashes are not verified against the model (MINOR-4; same as before). |
| `src/merge/wp4_io.cpp:87-88` (`read_store`) | bulk load; `check_invariants` dropped | OK. Every entry is pre-checked (range, finite, `check_model`, Zobrist hash when `zob`). `load_unique_sorted` covers I1, including the cut-off. The `s.size() != n` line after it is dead code (INFO-2). |
| `src/merge/wp4_io.cpp:389-392` (`load_island_full`) | same | OK, same pre-checks with `ex.zob`. |
| `include/v4/merge.h:97-102` | entry 26 → 30 + 4k bytes; comment on the transient | Correct (26 data + 4 `hidx_`). Effect: +0.8 GB on the 10⁶ merge estimate (INFO-3). |
| `include/v4/calib_run.h:65, 73` | k_store citation v0.1.12 → v0.1.13 §5.1; entry 30 + 4k | Correct. It conflicts textually with the unpushed WP4 branch `exp/P1M-wp4-calib2` (4ad6a9fc), which edits the same line with 26 + 4k (MINOR-1). |
| `include/v4/wp4_io.h:43` | citation updated | OK. |
| `src/eval/io.cpp:26-40` (WP5) | refuse a fit.bin whose top store holds a model twice | Correct, and tested by me (the PR has no test of it: MINOR-3). It reads the pool through offsets checked by the pre-existing, overflow-prone `off + len > c` (INFO-1). Cost at 10⁶: 640 MB transient and one sort of 4·10⁷ pairs, against a 16G eval task. Acceptable. |
| `tools/bench_store.cpp`, `CMakeLists.txt` | three bench modes; `V4_HAVE_BULK` for the bench target | OK. The bench's model ids ≥ 10⁹ overflow `int32` (`make_model`), so a few models are wrapped or unsorted. Harmless for timing (INFO-4). |
| tests | `store_bulk_load_equals_offer_path_and_verifies`, `merge_two_islands_same_model_two_values` | Both read and pass. The WP4-shape test covers both merge orders, one entry with the larger value, HPM provenance at the smallest key with that value, and log Z_T counting the model once (PR40 #2 done). |

Other claims:
- **(2) Pair sort:** the comparator is the old `key_less` then `better`, on (hash, index) pairs. Exact-tie entries are
  bit-identical, so the unspecified order between them cannot change the output. Same bits (hashes above).
- **(3) `check_invariants`:**
  - the independent (hash, lex) sort detects a duplicate (my injection test);
  - `hidx_` is range-checked before any `key_less` read;
  - "independent" means independent of the index, not of the stored hashes (MINOR-4);
  - production code no longer calls `check_invariants` (only tests), so its new O(n log n) cost and 16 B per entry
    are test-only.
- **(4) Stale citations:** fixed where listed. INTERFACES.md:164 still says `compact()` "drop[s] exact duplicates"
  (MINOR-2). `island/memory.h` keeps 26 + 4k, which is correct: it describes WP3's own `TopStore`, whose index is
  counted separately.

## (d) Timings, and why PR40's reviewer measured the merge at 32 → 47 s

All MEASURED on Owls, 1 thread, nice 19, cap 4·10⁷ + 1, k = 7. The same `bench_store.cpp` (head source) was built
against base `571f11bc` and against head.

| shape | base 571f11bc | head bf7daa23 | PR claim | hash |
|---|---|---|---|---|
| load a valid store: offer + compact | 37.2 s | 30.3 s (pair sort) | 40.7 → 32.5 | equal |
| load: **bulk** | — | **7.4 s** (5.0× vs base) | 8.0 | equal |
| merge 3 islands, 50 % shared (`merge 40000001 3 7 0.5`) | 104.2 s | **87.8 s** (−16 %) | 109.5 → 95.6 | equal |
| peak RSS (load / merge) | 6.71 / 7.40 GB | 6.71 / 7.40 GB | unchanged | |

I did not re-run `fill` (1.6·10⁸ offers; not a production shape).

**Per island** (`rev_merge.cpp`, the PR's generator; "past cut" = offers that pass the cut-off and enter staging):

| shape | island | past cut | base | head |
|---|---|---|---|---|
| 0 (PR #45 bench) | 1 (into empty) | 4.0·10⁷ | 37.2 s | 31.8 s |
| | 2 | 4.0·10⁷ | 37.2 s | 32.7 s |
| | 3 | 3.0·10⁷ | 32.6 s | 28.1 s |
| 1 (non-shared half of islands 2–3 below the merged worst value) | 1 | 4.0·10⁷ | 38.2 s | 30.9 s |
| | 2 | 2.0·10⁷ | 26.9 s | 23.5 s |
| | 3 | 2.0·10⁷ | 22.6 s | 17.8 s |

**Why 32 → 47 s (PR40 review) and 109.5 → 95.6 s here:**
1. **Not the code.**
   - The PR40 reviewer's "after" is the code that is this PR's "before" (`571f11bc` holds the same `Store` as PR40's
     head `b8ae28e9`).
   - The same code gives 47.1 s in their bench and 104.2 s (mine) / 109.5 s (author) in this one.
   - The two benches therefore measure different workloads.
2. **The island size differs, not only the shape.**
   - The first island goes into an empty store: c sorted offers, all of which enter, and 4 compactions. That step
     does not depend on the shape.
   - It costs 37–38 s here, but 18.8 s in the PR40 review ("first island 14.7 → 18.8 s").
   - So the reviewer's islands most likely held about half as many entries (or shorter models) as `cap`. Their bench
     source (`bench_rev`) was removed with their temp folder, so I cannot confirm the generator.
3. **The shape then sets the cost of islands 2..R.**
   - The merge cost of an island is roughly proportional to the offers that pass the cut-off: about 0.8–0.9 s per
     10⁶ at this cap. Each 10⁷ staged offers triggers one full compaction of the 4·10⁷ kept run.
   - In PR #45's generator, every island's values interleave exactly with the merged store's (−i·10⁻³ for all
     islands), so 3–4·10⁷ offers per island enter: the most pessimistic case.
   - When the non-shared half falls below the cut-off (shape 1), islands 2–3 cost 27 / 23 s instead of 37 / 33 s.
   - The PR40 review's islands 2+3 cost 28.3 s in total, about 14 s each. That is consistent with smaller islands
     and/or most of their offers cut off.
4. **Both benches agree on the direction.**
   - PR #40 slowed `Store` merges.
   - PR #45 wins back 12–20 % per merged island through the pair sort, and 5× on the load. The load is the larger
     term: it happens twice per island (`to_record` or the file read, then the WP4 load).
   - The absolute 10⁶ numbers depend on the real island shape (how many of an island's 4·10⁷ entries beat the merged
     cut-off). Neither bench knows that shape. Use PR #45's numbers as an upper bound per island.

## (e) v0.1.14 text vs `calib_backend.h` and WP4's `calib.bin` writer

- **§5.1 `meta.k_store` only when ok.** It matches `write_calib` (`wp4_io.cpp:179`) and the reader's check
  (`wp4_io.cpp:260-263`).
- **§5.1 `meta.iterations`.**
  - It matches `wp4_io.cpp:165-173`.
  - But `overall_best` and E1–E3 are written only when `complete`, and each row also has `tier`, `iteration`,
    `grid_label` and `complete`. The text lists the four as unconditional (MINOR-2).
- **§5.1 `stage_stream`** = [islands × 3] (init_hash, position start, position end), `wp4_io.cpp:224`. It matches.
- **§5.1 `inh_d`.**
  - It is written only on the flat-export path (`inherited_flat`, `wp4_io.cpp:200-203`). The legacy `inherited` path
    (`wp4_io.cpp:204-207`) writes no `inh_d`.
  - The calibration stores, HPM and inherited sections are written only when the status is ok (`wp4_io.cpp:189-207`).
    The text says so only for `k_store` (MINOR-2).
- **§7 calibration memory rule: does not match the branch** (MINOR-1):
  - **`calib_backend.h:44-46` on this branch:** "the bytes this calibration process already holds (calibration
    ledger, tables, **data**) and **the budget left** for the island". v0.1.14 says `mem_budget` = the whole budget,
    and `resident` excludes data and setup.
  - **`calib_run.h:79` / `calib_run.cpp`:**
    - `resident = ledger + export + inputs`;
    - `island_budget = budget − resident` (`plan_json`);
    - the up-front refusal is `resident ≥ budget`, not `resident + inputs + island_ledger > budget`;
    - `kbar = max(8, |mode_S| + 1)`, not `max(8, q90(π₀ size) + 1)` from `size_logmass`.
  - The v0.1.14 text matches, line for line, WP4's **unpushed** branch `exp/P1M-wp4-calib2` (`4ad6a9fc`, "N-1, N-2,
    N-4": `calib_k_plan`, `total = resident + inputs + island_ledger`, `mem_budget` passed unchanged). The PR #39
    review (WP3 side) already flags the runner half of it.
  - Contract-first is the department's practice, so this is not a code defect of this PR. But after the merge the
    binding text and the integration branch disagree, and the PR does not say so.

## Findings

### MINOR-1 — §7's calibration memory rule is ahead of the code, and `calib_run.h` will conflict with WP4's pending fix
- **Where:** INTERFACES.md §7 "Calibration memory rule" (new) vs `include/v4/calib_backend.h:44-46`,
  `include/v4/calib_run.h:73-80` and `src/calib/calib_run.cpp` (`plan_json`, `kbar`, the `resident ≥ budget` refusal)
  on this branch.
- **Evidence:** §(e). The only code that implements the text is `exp/P1M-wp4-calib2` @ `4ad6a9fc` (local; no PR yet).
  That branch also edits `calib_run.h:73` with `entry = 26.0 + 4.0 * kbar` and keeps the stale v0.1.12 citation at
  `calib_run.h:65`.
- **Fix:**
  - In the v0.1.14 changelog, mark the §7 rule as "effective with WP4 PR37 re-check N-1/N-2 (exp/P1M-wp4-calib2)", or
    merge this PR after that branch.
  - Whoever merges second must keep `30 + 4k` and the v0.1.13 citation in `calib_run.h`.
  - Tell WP4.

### MINOR-2 — §4.1 / §5.1 wording
- **INTERFACES.md:164:** the struct comment says `compact()` "drop[s] exact duplicates". It now keeps one entry per
  model, with the best value.
- **The `load_unique_sorted` contract does not state its preconditions:**
  - the target store must be empty (`internal_error` otherwise);
  - `n > cap` is refused (the offer path would truncate);
  - "same bits as offer + compact" holds for valid input only.
- **§5.1** (see §(e)):
  - `iterations`: `overall_best` and E1–E3 only when `complete`;
  - `inh_d`: only on the flat-export path;
  - the stores, HPM and inherited sections: only when the status is ok.
- **Fix:** three short wording edits.

### MINOR-3 — the eval reader's new refusal has no test in the suite
- **Where:** `src/eval/io.cpp:26-40`; no test in `tests/` or `tests/wp5`.
- **Evidence:** I tested it by hand (a hand-made fit.bin with a model twice → `invalid_input`; without it → accepted).
- **Fix:** add the same two-file test to the WP5 tests.

### MINOR-4 — one entry per model is verified only modulo hash correctness
- **Where:** `store.cpp` `load_unique_sorted` and `check_invariants`; the callers `island_file.cpp:96-97` and
  `island_impl.h:89-90`.
- **Evidence:**
  - An input with the same model under two different hashes (one wrong) is **accepted** by the loader (my test).
  - `check_invariants`' "independent" sort uses the stored hashes too.
  - The WP4 load sites verify every hash against the Zobrist table (`ex.zob` / `zob`), so the merge is safe.
  - WP3's reader and `to_record` do not, but the hashes there come from the island itself.
  - Same as the old offer path: not a regression.
- **Fix:**
  - Say "one entry per model, assuming correct hashes" in `store.h` and §4.1, or give `load_unique_sorted` an optional
    `const Zobrist*`.
  - Optionally verify hashes in `read_island_file(verify = true)`.

### INFO-1 — `fit.bin` pool bound check can wrap (pre-existing; the new code reads through it)
`src/eval/io.cpp:24` tests `s.off[i] + s.len[i] > c`. An offset near 2⁶⁴ wraps and passes, and the new duplicate
check (and every later `model(i)`) then reads out of bounds. It needs a file whose content hash is valid but whose
data is hostile. Use `s.len[i] > c || s.off[i] > c − s.len[i]`, as the Store loader does.

### INFO-2 — small code nits
- `wp4_io.cpp:88` and `:392`: `if (size() != n) throw …` after `load_unique_sorted` can no longer fire.
- `to_record` (`island_impl.h:89`) surfaces a corrupt in-memory island store as `invalid_input`. It is internal data,
  so `internal_error` would be more accurate.

### INFO-3 — merge admission at 10⁶ under the driver's 16G (ESTIMATE; mostly pre-existing, outside this PR)
- **The change:** 30 + 4k adds 2 × 2.5 × 4·10⁷ × 4 B = **0.8 GB** to `estimate_merge_memory` at 10⁶ (≈ 7 %).
- **The estimate at kbar = 8:**
  - merged + one island: 12.4 GB;
  - pip / terminal: 0.26 GB;
  - data.bin: 1.6 GB;
  - total 14.3 GB, plus `extra = 2.5 × setup.bin`.
- **The budget:** the driver's `--mem-budget` for the 10⁶ merge is 0.9 × 16 GiB = **15.46 GB**.
- **The consequence:** the merge would refuse with `resource_limit` whenever setup.bin exceeds about 0.47 GB (0.79 GB
  with the old constant).
- **Check:** at 10⁶, setup.bin is several GB (LOG 05:06, 07:09). So the 10⁶ merge plan looks over budget
  **independently of this PR**, through the `2.5 × setup.bin` term (`wp4_io.cpp:864`).
- **Next step:** the manager should check this with the real 10⁶ setup.bin size (WP4/WP5). It is not a fix for this PR.

### INFO-4 — bench generator
`tools/bench_store.cpp` `make_model`: `(int32_t)(id * k + a)` with id ≥ 10⁹ wraps, so a few bench models are unsorted
or negative. That does not matter for timing or hash equality, but the bench is not valid island data.

## Scale (p = 10⁶) and discipline
- **Integer widths:** `uint32` indices (n ≤ cap = 4·10⁷ + 1 < 2³²) and `uint64` offsets; the pool-range check is
  overflow-safe.
- **Transient memory:**
  - bulk load: 16 B per entry for the pair sort (640 MB at 4·10⁷), plus exact-size arrays (no 2.5× staging room);
  - the compaction pair sort: 16 B × staged entries (≤ 160 MB at 10⁷ staged), freed before the steps that set the
    "≈ 9 B per entry" peak.
- **Peak RSS:** unchanged in my runs.
- **Discipline:** nothing written outside `engine_v4/`, no hard-coded paths, no large files.

## Test runs I did (Owls)
- **Head `bf7daa23`:** `TMPDIR=…/20261116-review-45 tests/run_tests.sh --quick --threads 3`.
  - **113/113 PASS**, including `store_bulk_load_equals_offer_path_and_verifies` and
    `merge_two_islands_same_model_two_values`.
  - WP5 Slurm-driver 17 tests OK; competitor harness OK; install script 23 checks OK.
  - **WP4 golden 443,598 checks, 0 failures.**
  - Build flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`.
  - (A first attempt was killed by a host restart mid-run. This is the complete re-run.)
- **Patched golden copy** (keeps each T9-files `fit.bin`), quick, 3 threads:
  - head: 443,598 / 0;
  - base (`git archive 571f11bc`): 443,598 / 0;
  - fit.bin comparison in §(b).
- **`adv.cpp`:** 1,547 hostile and randomised checks on `load_unique_sorted`, `check_invariants` and the eval reader,
  0 failures (§(a)).
- **`v4_bench_store load|merge`** at cap 4·10⁷ + 1, base and head; **`rev_merge.cpp`** per-island probes (§(d)).

All of my programs (`adv.cpp`, `rev_merge.cpp`, `fitcmp.cpp`, the patched golden copy, the base archive) lived in
`/home/fb31/SMC_Engineering_Department/tmp/20261116-review-45`. I removed that folder afterwards. I started no
sub-agents and used no NOTS. I stopped only my own processes, by PID.
