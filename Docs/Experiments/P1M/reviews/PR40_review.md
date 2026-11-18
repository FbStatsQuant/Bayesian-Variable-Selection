# PR #40 review: WP1 INTERFACES v0.1.13 + `v4::Store` one entry per model

Reviewer: Opus 5.5 (high), independent of the author. 2026-11-16.
PR: https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/40 (head `b8ae28e9`, base `exp/P1M-engine` at `322e4a60`).
Read only: nothing pushed, no GitHub comments, no branch changed.
Machine: Owls (Xeon Gold 6148, GCC 11.5.0), `nice -n 19`, at most 3 threads. Store benches ran single-threaded, one at a time.
Temp: `/home/fb31/SMC_Engineering_Department/tmp/20261116-review-40` (removed after).

## Verdict: **ACCEPT** (the follow-ups below are not blocking)

The duplicate is real today in V mode, and the PR fixes it correctly. The 2.3–3.3× slowdown is confined to `v4::Store`. That class is used only in whole-store operations, a few per island: island record load, merge, calibration ledger, tail. The island's per-stage compaction (WP3 `TopStore`, the cost that dominates early 10⁶ bridge stages) uses a different class and is untouched. ESTIMATE of the total cost at p = 10⁶: +7 to +12 min of serial merge/calibration-task time.

Counts: CRITICAL 0 · MAJOR 0 · MINOR 6.

---

## (a) Correctness: is the duplicate possible today? Yes. Constructed and measured

**Construction** (`demo_dup.cpp`, linked against the base and head builds):
- Fixture: AR(0.6) data, n = 100, p = 300.
- Two real class-A islands: `run_island<Arith::ClassA>`, islands r = 1 and r = 2, seed 42, particle-major, 1 thread.
- Each island goes through `to_record`, then the two top stores are merged with `Store::merge`. This is exactly what `Ledger::merge` does for the stores (`src/common/ledger.cpp:76-79`).

| | base `322e4a60` | head `b8ae28e9` |
|---|---|---|
| models in both island stores | 6,319 | 6,319 |
| … with different class-A value bits | 757 (max rel. diff 8.6·10⁻¹⁶) | 757 |
| merged top store entries / distinct models | 12,001 / **11,418** | 12,001 / **12,001** |
| models stored twice | **583** | **0** |
| entries whose value ≠ max over islands | 583 | **0** |
| `check_invariants()` | **true** (the old I1 check cannot see it) | true |
| merged HPM F | −126.97987051427239 = larger island value | same |

**Consequences of the old behaviour in V mode** (all fixed by this PR):
- 583 of 12,001 slots (4.9 %) held second copies. The true top-c lost 583 models, and the cut-off was too high.
- `log_Z_T = LSE(top.v)` (`include/v4/merge.h:334-336`) double-counted those models, so it was no longer a lower bound.
- `PIP_T` and the top-M occupancy sets were over-weighted in the same way.

**Other routes to the duplicate.** It is not only two V islands. In V mode, any `v4::Store` that receives one model with two values hits the same bug:
- table and inherited models (bit-form F), or the tail's re-scores, against island class-A values;
- the calibration ledger of PR #37, which `Ledger::merge`s every class-A calibration island.

**Is the fix right?** I read `compact()` step by step (`src/common/store.cpp:50-126`).
- **Step 1.**
  - Staged entries are sorted by (hash, model), then by `better`. The first entry of each model is its best copy, and the later copies are dropped.
  - The survivors are matched against the kept run through `hidx_`, a sorted walk with `k` monotone. The worse of the staged and kept copies is dropped.
  - Equal value and equal model: `better` is false, so the staged copy is dropped. That is the old exact-duplicate rule.
- **Step 3.** Dropped kept entries are skipped. A replaced model moves to the position of its new value. Truncation at `cap` is safe: if the better copy is cut, the worse copy would also have been cut.
- **Step 4.** The new index is a linear merge of the old index and `sh`, both restricted to the selected entries. Keys are unique after step 1.
- **Cut-off.** It stays monotone. Every kept model's value can only rise, and at least c distinct models remain. The cut-off is now also *correct*: before the fix, c entries could cover fewer than c models.
- **`offer()`'s quick reject** stays valid. An offer below the worst kept value can only be dominated by c distinct models, or by its own kept copy.

**Provenance.** HPM provenance is not held in the Store. `Tally::offer_hpm` (`src/common/ledger.cpp:24-31`) already keeps the larger F, and on equal F and the same model the smaller event key. That is exactly the R7 wording ("first event with that larger value"). The island side (`include/v4/island/store.h` `hpm_cand_better`) is consistent with it. The PR does not touch provenance, and the demo's merged HPM is the larger value.

**Ordering, cut-off, determinism (T3).**
- The content after `compact()` is a function of the multiset of offers: the top-c of distinct models by best value.
- The new test `store_one_entry_per_model_best_value` checks this against a brute-force reference. It covers HPM and LEX orders, caps {1, 9, 120, 10⁵}, 3 offer orders, one store, and 3 stores merged in 2 orders. I re-ran it and it passed.
- T3 (`t3_invariance_bit`, `t3_invariance_classA`), `store_order_free_multithread`, `store_equals_wp1_reference_store` and `wp4_tail_threads_vs_serial` all pass at head.

## (b) Bits: compat and law outputs do not change

| run | base | head |
|---|---|---|
| `tests/run_tests.sh --quick --threads 3`: v4_tests | 108 cases, 0 failed | **109 cases, 0 failed** (+1 new) |
| island golden / T3 / T6 (inside v4_tests) | pass | pass |
| WP4 golden vs `core/` (calibration coded rule, T9 merge, T10 paths) | 254,268 checks, 0 failures | **254,268 checks, 0 failures** |
| WP5 driver / competitors / install script | OK | OK |
| demo: **bit-form** two-island merged store `content_hash` | `492779c4189cefd0` | **`492779c4189cefd0`** (identical) |
| demo: class-A merged store `content_hash` | `0db9631d733d8f4b` | `97537790cc87d8e8` (intended change) |

Why bit-form outputs cannot change: a bit-form value is a deterministic function of S, so all copies of a model are bit-equal. The new rule then drops exactly the copies the old adjacency rule dropped.

## (c) Performance scope (critical)

### Every `v4::Store` caller, and whether the slowdown applies

I found these with `grep` plus `nm` on the head libraries. Objects that reference `Store::{offer,compact,merge}`: `ledger.cpp.o`, `wp4_io.cpp.o`, `island_bit.cpp.o` (`to_record` only) and `island_file.cpp.o`. `island_a.cpp.o` references none of them.

| # | caller | how often (p = 10⁶, c = 4·10⁷ + 1) | slowdown applies? | MEASURED / ESTIMATE |
|---|---|---|---|---|
| 1 | **WP3 island top store and leader stores** (`v4::island::TopStore`, `include/v4/island/store.h:130`) | every flush and every step / pass boundary | **No.** It is a separate class with its own open-addressing index, and it already kept the max per model. The PR changes no island file, and island run loops never touch `v4::Store`. | no island measurement needed: nothing in the island run path changed (`git diff 322e4a60 b8ae28e9 -- include/v4/island src/island tools/bench_island.cpp` is empty) |
| 2 | island → record: `to_record` (`src/island/island_impl.h:89-90`), `read_island_file` (`island_file.cpp:96-97`), WP4 island load (`src/merge/wp4_io.cpp:321-322`) | once per island (at output, and again at the merge load) | yes: offer c unique entries + 4 compactions | MEASURED same shape: **57.6 → 77.8 s per island** (bench `merge` "gen", which includes the generator) |
| 3 | **WP4 merge** `Ledger::merge → Store::merge` (`include/v4/merge.h:278`) | once per island | yes | MEASURED, 3 islands, 50 % shared models: **32.0 → 47.1 s** (1.47×); first island 14.7 → 18.8 s |
| 4 | merge pre-ledger: `offer_tables` + `offer_inherited` (calibration's 3 stores) + `pre.compact()` (`wp4_io.cpp:766-769`) | once | yes | ESTIMATE: shape #2, about +20–40 s |
| 5 | **calibration ledger** (PR #37 `calib_backend.h`: `led_.merge(io.led)` per calibration island, top 4·10⁷ + 2 leaders of 2·10⁷) | once per calibration island (pilot + 4 per rebuild) | yes | ESTIMATE: about 2× #3 per island (3 stores), +10–20 s each |
| 6 | **tail** `local_search` (`include/v4/tail.h:136, 154`): merge local search + LS0, calibration searches | about 3 compactions per merge (+1 per calibration rebuild), each over the full kept run | yes, per compaction | MEASURED full 4·10⁷ store + 10³ / 10⁵ staged: **2.1 → 4.4 s** per compaction |
| 7 | `read_store` (setup table stores, `calib.bin` stores) (`wp4_io.cpp:71-89`) | at file read | yes | small (tables) or shape #2 (calibration stores) |
| — | `ThreadLedger::flush_into` (`ledger.cpp:85-107`) | tests only today | yes | — |

**Where the measured 2.3× comes from.** The author's probe `v4_bench_store 4000001 16000000 7` (every offer enters): MEASURED today **4.67 s / 516 MB → 12.89 s / 558 MB** (2.8× on a loaded Owls, load average about 21). The 10⁶-sized version (4·10⁷ cap, 1.6·10⁸ offers): **48.7 s / 4.82 GB → 160.6 s / 5.17 GB** (3.3×).

That shape exists nowhere in production. The island's high-volume offer stream goes to `TopStore`. The production `v4::Store` shapes are #2, #3 and #6 above, at 1.3–2.1×.

**What it costs the 10⁶ fit** (ESTIMATE from the MEASURED per-operation numbers, single thread):
- **merge task:** R′ = 16 islands × (about 20 s load + about 5 s merge), plus the pre-ledger and 3 tail compactions → **about +7–8 min**;
- **calibration task:** about 5–9 calibration-island merges × 10–20 s → **about +1–3 min**;
- **inside each island:** `to_record` adds about +20 s at the end of a multi-hour run.

None of this is in the island's per-stage loop.

**Why mode-gating saves nothing at 10⁶.** The 10⁶ run is V mode (`Arith::ClassA`), the one mode that needs the dedupe. "Only in V mode" would speed up compat and law, which run at small p, and would not change the 10⁶ run.

### Cheaper correct alternatives (evaluated)

1. **Profile of the new `compact()`** (MEASURED, timed copy of head `store.cpp`, fill 4·10⁶): 10.7 s in total.
   - The new steps take 6.6 s: key sort through an index 3.11 s, index rebuild 2.27 s, linear walk 1.19 s.
   - The old steps take about 3.4 s: order sort 1.16 s, merge 0.25 s, build 1.99 s.
   - All three new steps read `hash[]` and `pool` at random positions, through `uint32` indices.
2. **Sort contiguous `{hash, idx}` pairs instead of indices** (prototype `store_fastA.cpp`; same order: hash, then lex, then `better`).
   - Key sort MEASURED **3.11 → 1.75 s**.
   - The PR's 4 store tests pass, including the new one.
   - No memory change. Recommended as a free win.
3. **Keep the index's hashes contiguous** (`hkey_`, 8 B per entry, parallel to `hidx_`). The walk and the index merge then compare hashes sequentially and touch the models only on hash ties. Cost: +320 MB at c = 4·10⁷. Not measured; probably removes most of the 2.3 + 1.2 s.
4. **Bulk loader for input that is already I1** (`Store::load_unique_sorted`, used by callers #2, #4 and #7, whose input is a valid store): check the strict order in O(c), copy, and build `hidx_` with one pair sort. This replaces four full compactions per island load. **Largest win**: most of the merge-task cost is the load shape (57.6 → 77.8 s), not the merge itself. It would also be faster than base.
5. **Dedupe only in the merge path: not correct.** The tail (re-scores against stored class-A values), the calibration ledger (#5) and the pre-ledger also receive multi-valued offers in V mode.
6. **Value-aware check inside the existing sorted run: not recommended as the mechanism.**
   - Class-A copies of one model do differ by ulps (8.6·10⁻¹⁶ here), so they sit close together in value order. A window check would usually find them.
   - But exactness would rest on a numerical bound that is only a *target* (§6: ≤ 1e-9 relative against Bit, with a bit-form fallback), not a guarantee.
   - A by-model index is the only exact mechanism, which is what the PR does.

## (d) Memory: the index at p = 10⁶ (cap 4·10⁷ + 1)

| | persistent | transient during `compact()` |
|---|---|---|
| `hidx_` (4 B per kept entry) | **160 MB** per top store (+2 × 80 MB for the calibration leaders) | |
| `nh_idx` (new index) | | 160 MB |
| `newpos` (4 B × m, m ≤ c + c/4) | | ≤ 200 MB |
| `drop` (1 B × m) | | ≤ 50 MB (alive until the end of `compact()`) |
| `sh` (4 B × staged) | | ≤ 40 MB |

MEASURED peak deltas at c = 4·10⁷, k = 7:
- fill: **+350 MB** (4.82 → 5.17 GB);
- merge of 3 islands: **+516 MB** (6.88 → 7.40 GB);
- small compaction: **+340 MB** (4.31 → 4.65 GB).

That is about 7 % of a store's peak. The merge admission `estimate_merge_memory` (`merge.h:100-110`, 2.5·c·(26 + 4k) for each of the merged and loaded stores = 10.8 GB at k = 7) still bounds the measured 7.40 GB. Against H-9's 40 GB task, the index costs about 1.3 %. For comparison, WP3's `TopStore` open-addressing index costs 4 B × 2²⁷ = 537 MB for the same cap, so the PR's sorted index is the cheaper of the two.

---

## Findings

**1. MINOR (performance follow-up): `v4::Store::compact` is 2.3–3.3× slower; production shapes 1.3–2.1×.**
- **Where:** `src/common/store.cpp:56-104`.
- **Evidence:** §(c). Scope is the merge and calibration tasks only, ESTIMATE +7–12 min at 10⁶.
- **Fix (follow-up PR, not blocking):** in order of payoff:
  - a bulk loader for already-unique stores (alternative 4);
  - the pair sort (alternative 2, measured 3.11 → 1.75 s);
  - optionally contiguous index hashes (alternative 3).

**2. MINOR (tests): the V-mode duplicate is tested only at the `Store` level.**
- **Where:** `tests/test_store.cpp:82-117`.
- **Evidence:** nothing in `test_wp4*.cpp` merges two island ledgers that share a model at different values. My demo shows the base bug passes `check_invariants`.
- **Fix:** add a WP4 test. Two island `Ledger`s with one shared model at F and nextafter(F) go through `Ledger::merge`. Assert:
  - one entry, with the larger value;
  - HPM provenance = the smallest key among the events with the larger value;
  - `log_Z_T` counts the model once.

**3. MINOR (invariant check): `check_invariants` does not range-check `hidx_`.**
- **Where:** `src/common/store.cpp:135-137`.
- **Evidence:** the check verifies `hidx_.size() == v.size()` and strict key order, but an index ≥ `v.size()` is read by `key_less` (UB) before it can fail.
- **Fix:** check every `hidx_[t] < v.size()`. Together with the strict order and the equal size, that proves `hidx_` is a permutation.

**4. MINOR (docs): the memory model text is stale.**
- **Where:** `include/v4/merge.h:97` ("A store entry costs 26 + 4 k bytes"), `include/v4/store.h:8` and INTERFACES §4.1 ("peak ≈ 2.5·cap entries").
- **Evidence:** the index adds 4 B per kept entry persistent, plus about 9 B per entry transient (§d).
- **Fix:** write 30 + 4k bytes per kept entry, and note the transient (about +0.5 GB at 4·10⁷). The admission estimate is still an upper bound (measured 7.40 GB < estimated 10.8 GB).

**5. MINOR (contract precision): §5.1 `meta.k_store` is conditional, and §5.1 does not say so.**
- **Where:** INTERFACES §5.1 (line 314).
- **Evidence:** PR #37 writes it only when the calibration status is `ok` (`meta["k_store"]` under `co.status == ok`), and `read_calib` requires it finite and > 0. Several of PR #37's comments still cite "INTERFACES v0.1.12 §7".
- **Fix:** add "present iff the calibration completed (status ok)". PR #37 should cite v0.1.13 §5.1.

**6. MINOR (downstream checks and old artefacts): readers and pre-PR V-mode outputs.**
- **Where:** `src/eval/io.cpp:22`.
- **Evidence:** the eval reader of `fit.bin` checks only that the top store is sorted, not one entry per model. Any V-mode `fit.bin` merged before this PR can hold duplicate models: `log_Z_T` above the lower bound, `PIP_T` and occupancy over-weighted, models lost from the top-c.
- **Fix:** list and regenerate any V-mode `fit.bin` produced before the merge of this PR. I found none under `Docs/Experiments/P1M/results/`. Optionally, add a one-entry-per-model check to the eval reader.

**Contract text (INTERFACES v0.1.13).**
- The §4.1 "Values" paragraph matches WP3_ARCH_REVIEW R7 and the code.
- The §7 cross-reference to `meta.k_store` is right, and the changelog line is present.
- The branch copy and the shared copy (`Docs/Experiments/P1M/INTERFACES.md`, v0.1.13) are byte-identical (I checked with `cmp`).

**Scale and discipline.**
- `uint32` indices hold, since m ≤ 5·10⁷ < 2³².
- Nothing is written outside `engine_v4/`, there are no hard-coded paths, and there are no large files.

## Test runs I did (Owls)

- head: `TMPDIR=…/head tests/run_tests.sh --quick --threads 3 --keep` → 109/109, WP4 golden 254,268 / 0, WP5 OK, exit 0.
- base (`git archive 322e4a60`): same command → 108/108, WP4 golden 254,268 / 0.
- `demo_dup` (base, head): the class-A and bit-form two-island merges above.
- `bench_rev` (base, head; 1 thread, nice 19), each mode run base then head:
  - `fill 4000001 16000000 7`
  - `small 40000001 7 {1000, 100000}`
  - `merge 40000001 3 7 0.5`
  - `fill 40000001 160000000 7`
- Profiled `compact()` steps (`bench_prof`) and the pair-sort prototype (`bench_fastA`, plus the PR's `test_store.cpp` against it: 4/4 pass).
- All review programs lived in the temp folder; it was removed afterwards.
