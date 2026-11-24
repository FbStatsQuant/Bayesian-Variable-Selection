# SCORE_PATH_TRACE: is "same model ⇒ bit-identical score" true for every offer to the top store?

Read-only trace. Refs: core = `origin/main` `Scripts/SMC_BVS/core/` (paths below are under `cpp/` unless `.R`); v4 = `origin/exp/P1M-engine` `Scripts/SMC_BVS/engine_v4/`. Nothing was run; every claim is a code read plus the existing tests.

## VERDICT (per engine)

- **core v3.1: HOLDS BY CONSTRUCTION** for the invariant (with 3 stated residuals).
  - Every path calls `Scorer::score(S)` (`v3_score.h:227`) on a sorted S and forms F = `logprior[k] + lm` (`v3_engine.h:97`, `v3_core.cpp:382,427`).
  - The cache holds the bits of a fresh evaluation, and a clear-when-full re-score returns the same bits (`v3_score.h:255-294`).
  - Build is `-ffp-contract=off`, no fast-math (`Makevars.v3:5`).
  - Residuals: libm identity between setup and run, a scorer whose scratch state is read before write (checked: none), and `-O2` inlining (neutral without contraction).
  - Likelihood of a duplicate error at any p: ≈ 0 (not a function of p). A/B: 34 production + 5 status fits raised none.
- **engine v4: the invariant is FALSE BY DESIGN in class A (V mode, the 1M mode) and NOT PROVABLE in bit form; but the list error CANNOT FIRE (HOLDS BY CONSTRUCTION for "one entry per model").**
  - Every store that feeds the merged top store dedups by (hash, model) and keeps the LARGEST value (`store.cpp:127-153`, `island/store.h:235-249,302-309`).
  - A model with two different bit patterns is therefore one entry, not two.
  - `require_distinct` (`list_pip.cpp:20-35`) can only fire on a store that bypassed `offer/compact/merge/load_unique_sorted`. Likelihood at p = 10⁶: ≈ 0 (a code bug, not a numerical event).
  - Multi-valued models, on the other hand, are NORMAL at p = 10⁶ in V mode (~certain for any model reachable by two Gibbs additions). The list then uses the max class-A value of such a model (≤ 1e-9 relative to the bit form, tested), a deterministic and order-independent choice.
- **Fix:** core needs the list-level guard below (one R edit, legacy fields untouched). v4 needs no code change.

---

## 1. core v3.1: every path that reaches the stores

Stores: `Ledger::offer_stores` (`v3_ledger.h:89-94`) offers `top` (F, HPM order), `lead0` (lg0, lex), `lead1` (F, lex). `Ledger::event` offers only when `is_fresh` (`v3_ledger.h:112`). The list reads only `top`: `top_store <- led$top` (`v3_run.R:210`, `store_to_list` `v3_core.cpp:358-362`).

| Phase / Mech | Offer site | Scoring function and inputs | F |
|---|---|---|---|
| table / table | `ingest_tables` `v3_core.cpp:372-387`, event at `:384` | `Scorer::score(U)` in `build_tables` `v3_start.h:93`, U = block members in sorted order (blocks sorted, `v3_blocks.h:141`); `lm` read back from `st.logm_tab` | `D.logprior[|U|] + lm` (`:382`) |
| pilot, diag, final_init, bridge, burn-in, measured / init, gibbs_flip, uswap, nswap, indep | `Engine::eval` `v3_engine.h:89-101` (called `:122,153,174,186,291`) | cache probe, else `sc.score(q.S)` (`:92`); S kept sorted by `set_model/add_var/del_var` (`:80-85`) | `D.logprior[k] + lm` (`:97`) |
| gibbs_held | `Engine::held` `:103-105` → `event(..., is_fresh=false)` | no scoring; no store offer (`v3_ledger.h:112`) | n/a |
| local / local_scan, ls0 | `local_search` `v3_engine.h:379-419`: centre `:382`, scan `:391` via `eval` | same as `eval` (`E.local_search(..., PH_LS0)`, `v3_core.cpp:476`; same Engine, same `cache`, same ledger) | same |
| inherited / inherited | `v3_core.cpp:419-429` | RECOMPUTED, not copied: fresh `Scorer sc(&D)`, `sc.score(S).logm` (`:426`), S from `models_from_R`→`to_internal`, which sorts (`v3_core.cpp:34`) | `D.logprior[|S|] + lm` (`:427`) |
| test (PH_TEST) | testing samplers (`v3_step_sample`, `v3_round_sample`) | same `Engine::eval`; not part of a production run | same |

Single scoring function: **yes.** `Scorer::score` (`v3_score.h:227-238`) is the only scorer. It always evaluates in this order:
1. `try_chol(S, false)`: Gram from the stored G (`gram_sub` `:163-173`), H = (n+1)G+I, A = G+I (`:176-188`), `chol_inplace`, `finish_from_factors` (`:204-224`).
2. `try_chol(S, true)`: Gram recomputed from X.
3. `try_qr`.

The route is a pure function of S. There are no rank-1 updates, block tables or cached partial products in the scorer. The block-table values come out of the same `score`, and the Gram entries are the same sequential sums (`data_init` `v3_score.h:45-53`). Summation order is fixed (`:209,216`).

Scratch state: `bufH/bufA` are `assign`ed, `w/tmp/beta` are written before read (`:213-214,149-153`), `Gs` is `assign`ed (`:165`). No result depends on a previous call. The counters `D->routes` are write-only.

Floating point: `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2` (`Makevars.v3:5`): no FMA, and GCC does not reassociate FP without fast-math. libm (`log`, `sqrt`, `lgamma`) is the same binary for setup and run.

## 2. core cache

- `ScoreCache` (`v3_score.h:255-294`): keyed by sorted member list + Zobrist hash; stores `log m` only (`:260-262`). A hit returns the stored bits of the first fresh evaluation (`find` `:274-281`).
- NOT complete: bounded at `500·p` entries (`v3_run.R:92`, `v3_calib.R:147`) and CLEARED ENTIRELY when full (`insert` `:284`). A model can therefore be re-scored fresh. The re-score goes through the same `score` on the same S, so the bits are equal (invariant of §1), and `top.offer` finds it by `s.count(e)` (equal v, equal S) or re-inserts it once if it was evicted.
- Scope: one cache per final run (`v3_core.cpp:409`) and one per calibration (`cpp_cal_new` `:610`). A new `Ledger` per run (`:407`, `:608`). Calibration stores are NOT carried into the final top store. Only the inherited model list is, and it is RE-scored (§1). Cache is not shared across islands' stores (one ledger, one cache for the 4 islands, `:407-411`).
- Table models are never put in the cache (`ingest_tables` offers with `is_fresh=true` directly, `:384`). A table model reached later by a particle is a cache miss, scored fresh and offered a second time. This is the most frequent "same model offered twice" path in core. It relies on `build_tables`' `score(U)` (setup time) and `eval`'s `score(q.S)` (run time) being the same function on the same `D`: they are (`cpp_tables` `:176-181` and `Engine` `:410` both use the setup's `D`).

## 3. Inherited, LS0, local (core)

- Inherited: recomputed by `Scorer::score` on sorted S (§1). Same function ⇒ same bits as the calibration's `eval` value for the same model.
- LS0 and the final local search: same `Engine::eval`, same cache and ledger (`:456`, `:476`). The LS0 centre is emitted (`emit_centre=true`).
- `cpp_cal_V` (`:703-716`) re-scores V with a separate `Scorer`: same function, not offered to the stores.
- Exact branch (`cpp_enumerate` `:524-549`): each subset scored once by `sc.score(S)`; `top.offer` once per model, so no duplicate is possible there.

## 4. core residual risks (small)

1. libm identity: table values travel R-side as doubles (exact), but if a setup object were built on one glibc and the run done on another, `log`/`lgamma` results could differ in the last bit. All current flows build setup, calibration and run in one process or on one node type (`Makevars.v3:3-4`).
2. If anyone builds core without `Makevars.v3` (NOTS site flags carry `-march=native`, FMA contraction on): contraction decisions are per call site and could then differ between the table call site and the `eval` call site. Not the production build.
3. Nothing in core tests asserts "same model, same bits across paths" directly (see §7).

## 5. engine v4

### 5.1 Arithmetic forms and where each offered value comes from

Modes: T = `Arith::Bit` (bits of v3's scorer), V = `Arith::ClassA` (`INTERFACES.md:517-519`, `README.md:36`). The 1M pilot is V (`README.md:153-156,206-214`).

| Offer | Where | Scorer / value |
|---|---|---|
| tables | setup `tables.cpp:245-247` (stores), `wp4_io.cpp:772-778` (merge's pre-ledger) | `PrefixScorer` (`tables.cpp:25-80`): sorted-prefix reuse of Cholesky rows, forward solve, running log-det and quad; a SEPARATE implementation claimed bit-equal to `BitScorer`; fallbacks to `BitScorer` ref |
| init draws, U / N / I proposals | `island_run.h:688-692`, `island_pm.h:29,45,62,72` | `BitScorer::score` (`score.h:311`, `score.cpp`: v3's arithmetic, Gram-free, `pm::` libm) |
| Gibbs deletions (j ∈ S) | `kernel.h:184` (`del_logm`) | `BitScorer::score` (bits of the full score) |
| Gibbs additions (j ∉ S), fast path | `kernel.h:290-305` → `flip8_bit` `:194` (T) or `flip8_A` `:249` (V); offer at `island_lm.h:481`, `island_pm.h:139` | T: sorted-prefix reuse in `v8d` lanes, claimed bit-equal (`kernel.h:8-10`, golden-tested). **V: bordered update, label appended last, `fma8`, vector `alog8` (`:249-262`): path-dependent, ≤ 1e-9 relative to bit form (`kernel.h:11-13`)**. Bad lanes fall back to `BitScorer` (`:297-303`) |
| accepted particle states | `island_run.h:254-256` (`canonical`), `island_lm.h:534`, `island_pm.h:144` | V: re-scored by `BitScorer` ("Manager decision Q2b"); T: the flip bits. These states are offered via `offer_particle` (`island_run.h:263-265`) with the canonical value |
| final local search, LS0 | `tail.h:81-83,130,135,141`; evaluator `BitEval` `wp4_io.cpp:925-934` | `BitScorer::score` + `comp` |
| inherited (calib.bin) | `merge.h:237-243`, `wp4_io.cpp:380-392` | COPIED: `inh_F/lg0/logm` read from calib.bin (`:360-366`), written by the calibration's `CalibEval` = `BitScorer` (`calib_run.cpp:27-38`); hash recomputed by `zob.hash(S)` |

Answer to "ONE scoring function": **no.** There are four implementations of log m: `BitScorer` (reference), `PrefixScorer` (tables), `flip8_bit` (T Gibbs additions) and `flip8_A` (V Gibbs additions). The first three are claimed bit-equal by tests, not by construction. `flip8_A` is not bit-equal and not meant to be.

Consequence in V mode: the same model M can be offered with a `BitScorer` value (as a particle state, a proposal, a deletion flip, an inherited / table / tail model) and with ≥ 1 class-A bordered-update values (every parent S' with M = S' ∪ j, each path with its own rounding). Their bits differ in general.

### 5.2 Cache, offer floor, no-store-per-model dedup by value
- No score cache in production: `ledger.h:66` ("production passes fresh = true for every consumed score (no cache, OD-3)"); every consumed score is offered.
- Offer floor (V final islands only, `island/store.h:183-191`, `INTERFACES.md:221-238`): drops v < τ_cal from the island's top store. Dedup, compact, and duplicate filter never see the floor, so it cannot create a duplicate. It can only drop a lower-value copy of a model, and the merged store is proven equal to the unfloored merge (`INTERFACES.md:231-232`).

### 5.3 Dedup key and what a store does with two values
- Island store `TopStore` (`island/store.h:149-415`): `offer` (`:188-199`) drops an offer only if the worker's snapshot already holds that model with value ≥ v (`:192-196`), else buffers it. `compact_locked` (`:227-269`) sorts staged entries by (hash, |S|, S, v desc), keeps the FIRST per model (`:245`), matches against the kept run by hash index and replaces a smaller kept copy (`:246-247`: `dead[at]=1`). `compact_parallel` does the same (`:302-309`). The key is (hash, model), never the value.
- Merge-level `Store` (`store.cpp`): `offer` `:107-116`; `compact` `:123-202`: step 1 groups by (hash, model), best first, drops worse copies, and compares against the kept run through `hidx_` (`:127-153`); `merge` `:204-207` = offer all + compact. Header contract: `store.h:3-6` and `INTERFACES.md:203-208` ("one entry per model, with its best offered value").
- Merge path: `merge_stream` `merge.h:312` (`Ledger led = std::move(pre)`: tables + inherited), `:343` `led.merge(I.led)` per island (→ `Store::merge`), `:350` compact, tail `:358,371`, then `list_pip` from `led.top` at `:499`. Island files are loaded with hashes checked against Zobrist (`wp4_io.cpp:495-512`) and `load_unique_sorted` (`store.cpp:233-267`) refuses a model twice.
- Hash: `Zobrist::hash` = XOR of per-column keys from `splitmix64` seeded with a constant (`model.h:30-38`); incremental XOR in islands (`island_lm.h:481`, `island_pm.h:139`) equals `zob.hash(S)`. A model has one hash in every component.

Can the merged top store hold one model with two values? **No.** Dedup is by model; the larger value wins; the result is independent of offer order (T3 tests, below).

### 5.4 What v4's list helper does on a duplicate
`compute_list_pip` (`list_pip.cpp:38-65`) calls `require_distinct` (`:20-35`, groups by stored hash then compares models) at `:43`, BEFORE any flag → `Error(internal_error, "list PIP: the top store holds a duplicate model")`. In `merge_stream` the call (`merge.h:499`) is outside the tail's try/catch, so such an error would abort a completed merge, the same consequence as core. The same function runs in `smcbvs4 listpip` (`post/listpip.cpp:70`) on a store that `load_fit` has already checked for one entry per model (`eval/io.cpp:27-41`).

History worth knowing: before v0.1.13 a V-mode merge could hold a model twice (`eval/io.cpp:27-28`: "a fit.bin merged before that rule (V mode) may hold a model twice ... Refuse such files"). That is real evidence that class-A multi-valued models occur at scale; it is also why the store now keeps the max.

## 6. Verdict detail, and likelihood at p = 10⁶

| | core v3.1 | engine v4, T (bit) | engine v4, V (class A, the 1M mode) |
|---|---|---|---|
| same model ⇒ identical bits | HOLDS BY CONSTRUCTION (one scorer, §1) | by test, not by construction (4 implementations) | FALSE by design (`flip8_A`) |
| can the store hold the model twice | only if bits differ (§1 says no) | no (dedup by model) | no (dedup by model) |
| list `stop()` / `internal_error` possible | no in practice | no | no |
| value F(S) in the list | the single score | the single score (if the bit tests hold) | the MAX over offered values, ≤ 1e-9 relative above the bit form; deterministic |
| p = 10⁶ likelihood of the error | n/a (core not run at 1e6); ≈ 0 at any p | ≈ 0 | ≈ 0 (needs a dedup bug) |

Quantity to keep in mind for V (not measured here): a weight u_S = exp(F − Fmax) moves by a factor exp(δ), δ ≤ 1e-9·|F|; the injected test value is 1e-13 (`test_island.cpp:245,791`). This is a bias toward larger F for multi-path models, not an error.

## 7. Evidence: tests, A/B, goldens, rr2400

Would catch a violation of the INVARIANT (bit equality):
- v4: `tests/test_score.cpp:57` `score_bits_equal_v3_random_models`, `:70` fallback routes, `:118` `flip_scores_equal_scores`; `tests/test_island.cpp:140-199` (`eval8_add<Bit>` vs scorer bits, class A ≤ 1e-9), `:1020-1041` (kernel bits, class A ≤ 1e-9); `tests/test_setup.cpp:201-204` (table `logr` same-bits between two builds; I did not check that it is against core); WP4/WP5 goldens against core (`tests/wp5/test_golden_v3.cpp`, `tests/golden/*`: "568,269 checks, 0 failures", `IMPL_LIST_CODE_READ.md`).
- core: no direct test of "same model, same bits across table / eval / inherited / cleared cache". `tests/list_pip_units.R` (124 checks) exercises the helper, not this.

Would catch a duplicate in the STORE: v4 `tests/test_store.cpp:82-` (many values per model, content = reference), `:120-148` (invariant check detects a model twice), `tests/test_island.cpp:243-245,776-791,1061-1087,1379-1419` (class-A-like second values, stale snapshots, I1 violations), `tests/test_list_pip.cpp:80` (a raw duplicate throws).

Could the A/B, goldens or rr2400 have hit a violation?
- A/B (`summary.txt`): 39/39 identical, with `completed` fits at p = 500 and 1000 and 6 exact units: no `stop()` raised. Consistent with §1 for core. It cannot show an absence of bit differences at scale; it shows none on those fits (cache clears occurred only if `500·p` was exceeded, which is likely in the longer fits, `score_counts$cache` would say).
- Goldens: v3-vs-v4 bit comparisons in T mode only; V-mode multi-valued models are covered by the store tests, not by a v3 comparison.
- rr2400: I did not read its outputs. `RERUN_2400_PLAN.md` runs the v3.1 core (and v2.2.1) only, so the core verdict applies; no v4 fit is in it. It could have hit a violation only through core's cache-clear / table paths (§2), where §1 says the bits are equal.

## 8. RECOMMENDED minimal fix

**core (R only, `v3_run.R:253`).** The invariant holds by construction, so the guard is for safety. Do NOT dedup the store: that would change `top_store` (a duplicate takes a slot of the 40p+1, so removing it changes which models are kept, `list_full`, `near_tie`/leader inputs) and violate "legacy fields untouched".

In `v3_list_fields`, replace the `stop()`:
```r
key <- vapply(top$models, paste, "", collapse = ",")
dup <- duplicated(key)                       # first occurrence in store order = max F (store is sorted by value desc; ties are equal)
n_dup <- sum(dup)
if (n_dup) { top$models <- top$models[!dup]; F <- F[!dup]; m <- length(F) }   # then the existing code, unchanged
# ... and add to the returned list: list_dup_dropped = n_dup   (additive field; absent when 0 to keep today's output)
```
Properties: deterministic (first in store order = largest F, ties equal bits), reads nothing else, changes no legacy field. The count is a NEW additive field (suggested `list_dup_dropped`), not `pip_list_flag`, because every existing flag means "all NA". Spec §4 currently says a duplicate must stop, so this needs the HQ/Theory ruling that it replaces the stop. `list_size` would then be the post-dedup count (say so in the spec).

**v4: no change.** The store already dedups and keeps the max; `require_distinct` is a defensive assertion on an unreachable state.

**Targeted tests.**
1. core R (small p, `v3_score` `v3_setup.R:16` = `cpp_score`): for models taken from (a) a table subset (`setup$tables[[b]]$log_m`), (b) `v3_score(ctx, S)`, (c) the final `top_store` of a run with `cache_capacity` forced to 1 (a clear on every insert, so every model is re-scored fresh, incl. inherited and LS0 models): assert `identical(top$value[i], logprior[k] + log_m)` for all three and `anyDuplicated(...) == 0`; plus `identical()` of the whole `top_store` for default vs `cache_capacity = 1`. That test needs an option to pass `cache_capacity` (today fixed at `v3_run.R:92`), or a C++ unit.
2. core R helper: `v3_list_fields(list(models=list(c(1,2),c(1,2),c(3)), value=c(-1,-1-1e-15,-2), full=FALSE), orig=1:3)` → 2 models, `list_dup_dropped == 1`, `pip_list` equals the run with the duplicate absent (`identical`), legacy `top` unchanged.
3. v4: already present (`test_list_pip.cpp:80`, `test_store.cpp:82-148`). Add one V-mode end-to-end check: a tiny class-A island run whose merged store passes `check_invariants()` and in which a model offered with two different bit patterns appears once with the larger value (`test_island.cpp:776-791` does this on synthetic offers; a real kernel run would close the loop).
