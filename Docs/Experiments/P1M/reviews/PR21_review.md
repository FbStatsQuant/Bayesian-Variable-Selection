# PR #21 review — engine_v4 WP3 slice 1: the island (addressed uniforms, PM reference, island store, class-A label-major kernel, checkpoints, island_r.bin)

Reviewer: Opus 5.5 (high), independent of the author. 2026-11-15. Brief: `briefs/REVIEW_PR_template.md` + manager focus items 1–5.
PR head `exp/P1M-wp3-island2` @ `cd1a7e02`, base `exp/P1M-engine` @ `d04a2194` (merge-base `7fcbf560`). Contract: INTERFACES v0.1.7
(v0.1.5 sections for addresses, event keys, I4), ENGINEERING_SPEC §0-v3 → §0-v2, §3, §6; DECISIONS D-18..D-26.
Read-only review: detached checkout of the PR head in my worktree; nothing pushed or commented.

## Verdict: **ACCEPT-WITH-FIXES**

The core claims hold. I found no thread interleaving that changes the island store's kept set or order. The serial ledger is
reproduced for any thread count, G, tile size and kernel. The new >24-member support path gives the same bits as the scorer
(I checked this myself up to k = 99). The addresses follow INTERFACES v0.1.5, and I4 counts follow the contract. The full test
suite passes on Owls (56/56).

Three MAJOR findings must be fixed before production use:
- **M1.** A numerical failure aborts the process instead of returning `numerical_failure`. Reproduced.
- **M2.** Stale snapshots from the duplicate filter make the store's peak memory unbounded, and the 1M memory figure is understated.
- **M3.** The checkpoint fingerprint does not bind the island's input files, which INTERFACES §5.1 requires.

There are no CRITICAL findings. Counts: CRITICAL 0 · MAJOR 3 · MINOR 10.

---

## Test runs (Owls, `nice -n 19`, ≤ 3 threads, TMPDIR = `/home/fb31/SMC_Engineering_Department/tmp/20261115-review-PR21`, removed after)
1. `tests/run_tests.sh` (default build, x86-64-v2, gcc 11.5.0, OMP 3): **56 test cases, 0 failed, 0 check failures**, exit 0.
   git_commit in the binary `cd1a7e02…`. The island lines: T3 bit and class A, with PM and LM over threads 1–3 and
   G ∈ {1, 7, 16, 48}, tiles 64–256, all on one hash (bit `44a15bfc6fb8d233`, A `d2df149413596a19`); golden island vs
   `v3::Engine::run_island` passes for PM and LM; 13,000 flip scores vs `v3::Scorer`, 0 mismatches; t6 restart, kill-during-write,
   resubmission and refusal pass; store one-worker-all-winners passes.
2. `-DV4_ISLAND_ISA=x86-64-v4` build (AVX-512 island sources), `v4_tests` at OMP 3: see the result line at the end of this
   section.
3. **Reviewer check A: flips at k > 24 (the new path).** An out-of-tree program, `chk/bigk.cpp` in the tmp folder, linked
   against the PR's libs. Settings: p = 1,500, n = 200 (K = 100), supports of size k ∈ {25, 30, 40, 60, 80, 99}, two each,
   every label j. It compares `eval1<Bit>` with `BitScorer::score(S △ j)` and `eval1<ClassA>` with Bit.
   Result: **18,000 flips, 0 bit mismatches**, all supports fast. Class A: max relative |Δlog m| = **1.49e-15**,
   max |Δo| = 5.7e-14. (MEASURED, Owls, 1 thread.)
4. **Reviewer check B: a numerical failure inside the kernel** (`chk/nf.cpp`). Half the columns are scaled by 1e200 so that
   Cholesky, refactor and QR all fail. Calling `run_island<ClassA>` (LM, G = 16) **aborts with SIGABRT**: `terminate called after
   throwing an instance of 'v4::NumericalFailure'`, exit 134. This happens at threads = 1 and at threads = 2 (finding M1).

x86-64-v4 build result (item 2): **56 test cases, 0 failed**. The bit-form T3 hash is the same as in the default build
(`44a15bfc6fb8d233`, so the bit form does not depend on the ISA). The class-A hash differs from the default build
(`e9cc4ab39f8a72db`, FMA active), as expected for class A, and it is still identical across PM/LM, threads, G and tiles within
that build. Golden island vs core passes. Note that a class-A island therefore depends on the build ISA: the V-1M islands of
one fit must share a build (WP4 merge, `binary_compatible`).

---

## Answers to the manager's focus items

**1. Store determinism under threads.** Deterministic.
- `TopStore` (`include/v4/island/store.h:83-194`) keeps the top-c of {(S, max offered value of S)} under a strict total order.
  Every path that can drop or merge an offer preserves this set function:
  - **Cut-off drop** (`:111`): it drops only when v < τ, and ties are kept. τ is the c-th kept value. It only increases
    (`:176`), and a stale (smaller) τ only drops less. The WP3_DESIGN §1.3 proof is correct.
  - **Exact duplicate filter** (`:112-116`): it drops (S, v) only when an immutable snapshot of a published kept run holds S
    with a value ≥ v. That kept value was itself offered, so max(S) is unchanged. A snapshot of any age is a subset of the
    history, so staleness only drops less. The `refresh` race (gen read before the newer `k` is fetched) is harmless: the next
    offer just refreshes again.
  - **Compaction** (`:138-177`): the per-model de-duplication keeps the largest value, including the class-A case where a
    kept copy is smaller (marked dead). I traced the `r[w-1]` comparison: a model whose first staged copy was dropped against
    the kept run cannot slip through with a smaller second copy. The linear merge works on distinct models under the strict
    order, and truncation to c commutes with union.
  - **Flush timing, mutex order and per-thread buffer bounds** decide only *when* entries reach staging, never *which*
    entries end up kept.

  The serial ledger is reproduced for any thread count. Counters are summed exactly in u64. `island_best` is a max. The HPM
  uses a strict order (F, |S|, lex, EventKey). In phase B, the shortcut `F >= tau || F > island_best || F >= hpm.F`
  (`src/island/island_impl.h:472`) skips only events that cannot change any of the three. The phase-B key of a
  (support, label) is the smallest consuming particle's key, which is the minimum key because `particle` precedes `position`
  in the EventKey order. RB is an exact u128 fixed-point sum. Only `KernelStats` (merges, buffered, dup-dropped) depends on
  timing, and it is not hashed or written. One problem here is memory, not content: M2.

**2. The path for supports > 24.** It is exact. `flip8_bit` (`include/v4/island/kernel.h:138-190`) reproduces
`chol_inplace` / `forward_solve` / `finish_from_factors` (`core/cpp/v3_score.h:76-90, :93, :204-224`) operation by operation:
- the prefix rows < q are reused;
- the label row and the later rows are recomputed in the same t order, as `x - a*b` without contraction;
- `+ 0.0` is kept on off-diagonals;
- the prefix sums of log diag and of w² continue sequentially;
- `Q = yty - n·quad`;
- lanes that fail the pivot test, the Q < 1e-8 y'y test, `arg > 0` or finiteness fall back to the full scorer.

Removing `KM` only changed storage (heap `Mat`, thread-local lane scratch). Reviewer check A confirms this: 0 mismatches at
k = 25…99, and class A ≤ 1.5e-15 relative (contract ≤ 1e-9). The suite itself never exercises k > 12 (m6).

**3. RNG addressing and I4.** Conforms to INTERFACES v0.1.5 §3.
- Gibbs = `SLOT_ACCEPT` (kind 7).
- U / N_b = MOVE_J, MOVE_L, ACCEPT. The N_b no-score case reads MOVE_J only; self-loops read nothing.
- I = PI0_SIZE 0, PI0_BLOCKSIZE b for b = J−1…, PI0_SUBMODEL b, then ACCEPT.
- ORDER d = 0…m−2 at position 0; RESAMPLE at its own xph with destination particle i + 1.
- INIT slots at position 0. BURN and MEASURED use xph to separate stage = l / h.
- Event keys: (FINAL, tier, iter −1, r, xph, stage t / T, round t / l / h, i + 1, q, sub). Gibbs flip sub = 1; held events
  are never offered. Proposals and INIT use sub 0.

At p = 10⁶: m − 1 ≈ 10⁶ < 2²⁸ order slots, position < 2³², stage < 2²⁴, island < 2²⁰. `slot_of` and `address_key/ctr` throw on
overflow. G ≤ 256 is enforced (`island_impl.h:797`).

I4 by mechanism: held = G steps; flip = G − cap (LM detects the cap by the NaN row, `:468`; PM by `has_other`, `:230-231`, the
same rule as `core/cpp/v3_engine.h:113-130`, o = 0 at the cap); USWAP = executed U; NSWAP = executed − no-score; INDEP = I;
INIT = N. `i4_holds` is checked per phase in `logical_counts_and_invariants`, but the cap branch is never reached in any island
test (m6). The I5 runtime check (`CheckedSource`) is not wired (m5).

**4. Checkpoints and island_r.bin.**
- Streamed writes: FNV checksum while streaming, then header rewrite, `fflush` + `fsync`, rename from `.tmp.<pid>`
  (`island_impl.h:598-617`).
- Two-pass verified load: checksum pass, then parse (`:620-668`).
- A checksum-valid checkpoint with a foreign fingerprint is refused with `invalid_input` (`:642-646`).
- Tests cover: a torn newest generation plus a leftover temporary file (the older generation is used); repeated
  resubmission with changed threads, G and kernel; refusal on a seed change. All are bit-identical to the uninterrupted run.
  The "kill" is simulated by truncation, which is adequate for a rename-based protocol.
- Gaps: the fingerprint's identity (M3), the missing directory fsync, leftover temporary files and a partial-state return
  path (m4).
- `island_r.bin` (`src/island/island_file.cpp`): the sections match INTERFACES §5.1 except `st_moves` is T×12 (contract says
  T×11) and `rb_round` is Hm×p (contract says 4×p) (m1).
- **Terminal supports are correct**: the N particles' supports after the last measured round, in particle order
  (`island_impl.h:782`), written as `terminal_S_ptr` (N + 1) / `terminal_S` only when the run completed. After a resume from
  the last step's checkpoint they come from the loaded P. They are not cross-checked against an independent reference (m6).

**5. Scale at p = 10⁶, n = 200.** These are ESTIMATES from the code's allocation sizes, with c = 40p + 1 = 4·10⁷, mean k = 7,
an entry = 26 + 4k = 54 B, and an index of 2²⁷ u32 = 0.54 GB.
- One kept run is ≈ 2.16 GB + 0.54 GB index = 2.7 GB.
- **Compaction peak**: old kept 2.7 + new kept 2.16 + over-reserved pool 0.28 + new index 0.54 + staging (s = c/4 = 10⁷ entries;
  capacity after doubling ≈ 0.7–1.1 GB) + `r` refs 0.32 + dead flags 0.04 ≈ **6.7–7.1 GB**. The spec §2 / LOG "≈ 5.4 GB peak"
  counts only two kept runs. WP3_DESIGN §1.5's own figure is 7.2 GB.
- Every stale snapshot generation held by a worker adds 2.7 GB (M2).
- Other memory: X 1.6 GB plus the tiled copy `Xt` 1.6 GB. Group buffers at the default **G = 256**: `ord`/`inv` 2.05 GB +
  `lbuf`/`obuf` up to 4.1 GB (G = 64: 1.5 GB). Thread offer buffers: 96 × 65,536 × 54 B ≈ 0.34 GB. RB: 32 MB. End-of-run
  copies of the store: +4.4 GB (m8).
- Total ≈ 16–21 GB at G = 256 without stale snapshots: inside the 24–32 GB island request, but there is no admission check yet
  (known gap).
- No 32-bit overflow found: every n·p, G·m and nsup·p product is cast to `size_t` first; the hash index is u32 entry + 1 with
  c < 2³²; `len` is u16 with K ≤ n/2; positions, particles and slots are u32 within their limits.

---

## Findings

### MAJOR

**M1. A `NumericalFailure` inside any OpenMP region terminates the process. The island never returns `numerical_failure`.**
- Where: `src/island/island_impl.h:267-274` (orders), `:307-311` (`build_support` → `sc.score` for deletions), `:328-419`
  (phase A: `eval8_add` fallback lanes and the slow `eval1` → `sc.score`), `:423-434` (walk → `step_nongibbs` → `sc.score`),
  `:512-516` (PM rounds), `:701-708` (initial draws). The only handler is the `catch (const NumericalFailure&)` at `:768`,
  outside every parallel region.
- Evidence: an exception that leaves an OpenMP structured block calls `std::terminate`. Reviewer check B reproduces it: SIGABRT,
  core dump, exit 134, at 1 and 2 threads.
- Impact: spec §6 requires a deterministic `numerical_failure` status (HPM so far labelled incomplete, no estimates, no retry).
  Instead the Slurm task dies like a node failure and is resubmitted, where it deterministically crashes again until the retry
  budget runs out. No record is written, and GUARD-W and the status precedence never run.
- Fix: inside each parallel region, catch per thread into a shared "first error" slot. Pick it deterministically, for example
  the error of the smallest particle, support or tile index, so the reason string does not depend on the schedule. Skip the
  remaining work, then rethrow after the region. Add a test: the reviewer's `nf.cpp` setup, expecting `status == 2` for PM and
  LM at 1 and 3 threads.

**M2. Snapshots of the duplicate filter keep old kept runs alive without bound. The 1M store-memory figure is understated.**
- Where: `include/v4/island/store.h:61`, `:105-108`, `:174`; `src/island/island_impl.h:553-556`.
- Evidence: each `StoreBuffer` holds `shared_ptr<const Kept> snap`. It is refreshed only when that worker makes an offer that
  passes τ, and it is never released, not even at `sync_ledgers`. A worker whose offers all fall below τ, or that receives no
  work, keeps an arbitrarily old generation alive across any number of compactions. In the worst case T + 2 kept runs are live
  (2.7 GB each at 1M, k = 7; ≈ 4.3 GB each at k = 20).
- Separately, the compaction peak without stale snapshots is ≈ 6.7–7.1 GB (focus item 5), not the 5.4 GB in spec §2 / LOG,
  and the admission formula in WP3_DESIGN §1.6 does not include snapshots at all.
- Fix:
  - drop all snapshots at every step boundary (`for (auto& t : tl) t->buf.snap.reset();` in `sync_ledgers`);
  - in `flush()`, reset the flushing worker's snapshot;
  - optionally publish the generation and let `compact_locked` wait or skip while an old generation is held.
  - Then the bound is 2 kept runs + 1 snapshot generation (or 2 with reset-on-flush): put that number into the admission
    formula, and correct spec §2 (≈ 7 GB peak plus one snapshot generation at k = 7).
- A test can assert `k.use_count()` and that old generations are released at a step boundary.

**M3. The checkpoint fingerprint does not bind the island's inputs. INTERFACES §5.1: restart identity = content hash.**
- Where: `src/island/island_impl.h:562-567`, used at `:642-646`.
- Evidence: the fingerprint hashes seed, island, tier, N, grid, L, Hm, B, cap, n, p, y'y, log Z̄₀, J, the arithmetic and the
  raw binary block.
  - y'y is the same for every standardised response of the same n.
  - X, the neighbour graph and the partition enter only through log Z̄₀, J and p.
- A setup rebuilt with the same binary and partition but a different neighbour graph would therefore resume silently into a
  mixed-law island. Example: a changed τ_n or neighbour parameter that leaves the tables unchanged.
- Separately, hashing the whole block, including the libm path and SHA-256, is stricter than and different from the contract
  rule `binary_compatible(…, Restart)` (executable SHA-256 + git commit). The refusal message cannot name the reason.
- Fix: add `inputs` (the content SHA-256 of data.bin, setup.bin and calib.bin, which the CLI already verifies) to
  `IslandConfig` and hash them into the fingerprint. Store the writer's binary block in the checkpoint and check it with
  `require_binary_compatible(…, BinaryUse::Restart)` for a named refusal. The test should refuse on a changed input hash and
  on a changed binary block, not only on a changed seed. This can land with the CLI wiring, but must come before any
  production checkpoint is written.

### MINOR

**m1. island_r.bin vs INTERFACES §5.1.** `st_moves` is T×12 (`island_file.h:10`, `island_file.cpp:89`, with `gibbs_cap`
added) but the contract says "moves u64 T×11". `rb_round` is Hm×p but the contract says 4×p. The section name `st_moves` and
the extra sections (`grid`, `term_moves`, `term_distinct`, `hpm_val`, `hpm_ev`) are allowed additions. Fix: an INTERFACES
changelog line by the WP1 owner (12 fields, Hm×p, section names), and tell WP4 (its `merge.h` also assumes Hm×N terminal
supports, as the PR notes).

**m2. GUARD-W edge.** For a non-completed status the writer still emits `st_inc` and `st_cum` (`island_file.cpp:80-91`).
`st_cum` is the cumulative log Ẑ up to the last stage, an estimate. INTERFACES §7 says "No estimate field is written unless
status is completed". Fix: write `st_inc` / `st_cum` only when completed (keep φ, ESS, distinct counts and moves as
diagnostics), or record an explicit exemption in INTERFACES.

**m3. Status and error types.**
- `to_record` / `status_str` map status 1 ("interrupted", from `stop_after_step`) to `resource_limit`
  (`island_impl.h:75`, `island_file.cpp:66`).
- Configuration errors throw `std::invalid_argument` (`:792-797`); checkpoint I/O throws `std::runtime_error("io_error: …")`
  (`:603`, `:613`); I1 throws `std::runtime_error("internal_error: …")` (`:765`).
- INTERFACES §7 expects `v4::Error` with `invalid_input` / `io_error` / `internal_error`, so `main` can map them to exit codes.

Fix: throw `v4::Error(Status::…)`, and either make "interrupted" a non-file outcome or give it its own label.

**m4. Checkpoint durability details.**
- (a) No directory fsync after `rename` (`:613`). INTERFACES §5.1 requires it for `.bin` files, and the same reasoning applies
  here.
- (b) `.tmp.<pid>` files left by a killed writer are never removed. Each is ≈ 2–4.5 GB at 1M on /scratch, one per kill. Remove
  `<path>.{a,b}.tmp.*` at the start of `load_ckpt`.
- (c) If pass 2 fails (`r.bad`, or `np != N`) after `master`, `res`, `P` or `top.k` have been partly overwritten
  (`:653-665`), the function returns −1 and the run starts "from scratch" with a polluted tally and kept run. Today this is
  reachable only if the file changes between the passes. Fix: parse into locals and commit only on success, or reset
  `master` and `top` before starting from scratch.
- (d) `w.put(master.hpm.key)` writes the EventKey struct raw, including padding bytes, so the checkpoint bytes are not
  deterministic (harmless for the checksum; write the fields).

**m5. I5 is not wired (INTERFACES §3).** The island calls `uniform_at` / `philox8_positions` directly (`:161`, `:211`, `:239`,
`:405`, `:542`, `:704`). `CheckedSource` is never used, not even under `V4_CHECK_ADDRESSES`. I verified injectivity by
reading the code (focus item 3), but the contract asks for the runtime check in tests and under the option. Note for the fix:
phase A legitimately reads the same (particle, position) address again in a later pass (positions in (e, old best)), so a
UNIQUE check must count only *consumed* uniforms (phase B / walk / PM), not phase-A look-ahead.

**m6. Test coverage gaps.** All of these pass under my external checks or by inspection, but the suite does not pin them:
- (a) flips only at k ≤ 12 (`tests/test_island.cpp:66-69`, `:117`; golden `:57`). The k > 24 path that this commit
  generalises is untested. Add k ∈ {25, 40, 99} at K = 100: reviewer check A is a ready test.
- (b) `fallback lanes 0`: the pivot, Q and finiteness fallback inside `flip8_bit` / `flip8_A` is never hit. Add a near-duplicate
  column pair.
- (c) the Gibbs cap (|S| = K) and its I4 mechanism are never reached in an island (K = n/2 ≥ 40 with supports of about 5). Add
  an island with n small enough that K ≈ 3–4.
- (d) terminal supports are checked only against themselves. Compare them with core's final particle set in
  `golden_island_vs_core_engine`, or with the PM reference at 3 threads.
- (e) `golden` compares HPM keys without `xph` and `sub`.

**m7. TopStore does not refuse NaN** (`store.h:110-119`; INTERFACES v0.1.3 changelog: Store and ThreadLedger refuse NaN as
internal_error). A NaN passes `val < tau` and breaks the strict order in `std::sort`. No current call site produces one,
because phase B filters NaN rows, but a one-line guard keeps the contract.

**m8. Scale and performance hygiene at 1M.**
- (a) `top.check_invariant()` runs every step (`island_impl.h:765`). It allocates and sorts c (hash, index) pairs: about
  0.64 GB and seconds per step at c = 4·10⁷. Check sortedness linearly and duplicates through the existing hash index, or only
  under a debug flag.
- (b) End of run: `res.top_* = top.k->…` copies the store, and `return res;` (a member, so no NRVO) copies the whole
  `IslandRun` again. Together that is +4.4 GB while the group buffers and `Xt` are still alive. Move instead.
- (c) The default `G = 256` (`island.h:35`) at 1M means 6.1 GB of group buffers. The benches use G = 64, but nothing enforces
  that until the `--mem-budget` admission lands (known gap, D-24).
- (d) `scratch_P` is nA × Bk per thread. At large π₀ supports (nA up to G·k) that is up to about 26 MB per thread, which
  belongs in the admission formula.

**m9. ODR across ISAs.** `store.h`, `dep.h` and the non-template parts of `island_impl.h` (`TopStore`, `Kept::find`,
`draw_pi0`, …) are not in the `V4_ISLAND_ISA_NS` inline namespace. With `-DV4_WIDE_ISA=ON` they are compiled with
`-march=x86-64-v3` in `v4_a` and `-march=x86-64-v2` in `v4_bit`, and the linker keeps one copy. The behaviour is identical
(integer and ordering code), but an AVX2 copy can be picked for the "portable" library. Fix: put them in the ISA namespace too,
or compile them in one TU.

**m10. Nits.**
- `island.h:45`: the comments of `store_dup_filter` and `allow_test_kernels` landed on the `verbose` line.
- `stop_after_step` is silently ignored when `ckpt_path` is empty.
- `to_record` / `read_island_file` re-offer the whole store into a WP1 `v4::Store` (another full copy plus a compaction at 1M);
  acceptable for now.
- Class A: the HPM provenance of a model offered with two path values goes to the larger F, not the smaller key. That is
  allowed under D-23 (class A), but worth one sentence in WP3_DESIGN §3.7.

---

## Discipline
- Every changed file is under `Scripts/SMC_BVS/engine_v4/` (20 files). There are no hard-coded `/home`, `/scratch` or
  `/projects` paths and no file over 5 MB.
- `core/` is untouched. The pinned-reference test passes (core commit `72785fe8…`, 20 files).
- The NOTS bench scripts are self-contained and run inside an allocation; they submit nothing.
- PR description: the tests, machine and measured numbers are labelled. The known gaps are stated honestly: serial compaction,
  admission, compat island, CLI, provisional checkpoint container.
