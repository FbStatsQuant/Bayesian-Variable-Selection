# API-AUDIT (R10 CODE-AUDIT): line-referenced code audit and the VAL-FP measurement

Run API-AUDIT, 2026-11-02, branch `theory/API-AUDIT`. The task file names `theory_campaign/CODE-AUDIT/AUDIT.md` as the
deliverable; under the run's write rule this file is `theory_campaign/API-AUDIT/AUDIT.md`.
**Nothing here has been reviewed.** Status words follow PROTOCOL.md. "PROVED by code reading" means: every cited line
was read in the source at the stated commit, and the claim follows from those lines. It says nothing about the
compiler or about R. Where a claim was also *executed*, the run is cited (§7, §8).

**Code version.** Branch base e58a949. The last commit touching `Scripts/SMC_BVS/core` is 39db138. The sha256
prefixes of all nine audited files equal those recorded by W5-LOCKBOOK (`theory/W5-LOCKBOOK:…/AUDIT.md`), so
W5-LOCKBOOK's audit applies to this code unchanged. All paths are relative to `Scripts/SMC_BVS/core/`. I re-read every
line reference below. **Relation to W5-LOCKBOOK.** This audit re-checks W5's lemmas IMPL-SR, IMPL-GUARD, IMPL-LS,
IMPL-EMIT and IMPL-STREAM line by line (all confirmed; corrections in §6). It adds what W5 could not do because it had
no R/C++ build:
(i) an executed GUARD check (bitwise identity with the guard-free run, and a forced stop);
(ii) the VAL-FP measurement (a long-double replay of 10 fits plus 100 extra final runs);
(iii) an audit of the only LS0 implementation in the repository (`theory/O-LS0`).

---

## 1. SR: scoring rule of `Engine::step_gibbs`

`cpp/v3_engine.h:113–132`. One Gibbs step at state S on coordinate j:

| Line | What happens |
|---|---|
| 115–116 | `in` = j ∈ S; `add_ok` = in ∨ \|S\| < K (R1: an addition beyond K is infeasible). |
| 118 | `held(P, ME_GIBBS_HELD)`: the current state is a logical score event, not re-evaluated (`:103–105`, `is_fresh = false`). |
| 119–123 | If the other configuration S Δ {j} is feasible, it is built in `tmpQ` and scored by `eval(tmpQ, ME_GIBBS_FLIP)`. The default `emit = true` applies (`:89`), so this is a ledger event. |
| 124–126 | o_j = plogis(log γ_φ(S∪j) − log γ_φ(S∖j)) is computed from the two scored configurations. |
| 128 | The RB accumulator is updated before the draw (R8). |
| 129–131 | Only now is the one uniform read, and the state updated (`P = tmpQ` if the indicator changes). |

**Finding SR-1 (PROVED by code reading).** Whenever the other configuration is feasible, it is scored, and offered
to the ledger, *before* the accept uniform is read, whatever the outcome. If it is infeasible (j ∉ S, |S| = K), it is
outside Ω; nothing is scored, o_j = 0, one uniform is still read, and the state cannot change (`u < 0` is false). So
SR holds with the reading **"both *feasible* configurations"** (the same as W5).

**Finding SR-2: "no call site disables emission" (PROVED by code reading, with one qualification).**
- `eval` has an `emit` flag (`:89, :98`). A search of `cpp/` for `eval(` finds exactly one call that can pass
  `false`: the local-search centre, `eval(C, ME_LOCAL, emit_centre)` (`:381`).
- Every production call of `local_search` passes `emit_centre = false` with centre `led->hpmS`, the current HPM:
  `cpp/v3_core.cpp:447` (final), `:610` (pilot), `:657` (diagnostics). The HPM has already been offered: via
  `offer_hpm`, from tables, inherited models or an earlier fresh event.
- All other `eval` calls use the default `emit = true`:
  - initial draws `:291`;
  - the Gibbs flip `:122`;
  - the uniform swap `:153`;
  - the neighbour swap `:174`;
  - the independence proposal `:186`;
  - local-search neighbours `:390`.
- Every engine that runs islands has a ledger attached: final run `cpp/v3_core.cpp:401–402`, calibration `:579–580`.
  So `if (led)` (`:99, :104`) is never false in a fit.

*Qualification: "offered to the ledger" is not "offered to the stores".* `Ledger::event` counts every event but passes
the model to the HPM and the stores only if `is_fresh` (`cpp/v3_ledger.h:110`). An event is fresh only on a cache miss
(`:90–94, :99`). This is correct because of two facts:
1. Every cache insertion happens inside an `eval` (`:93`) that also emits. The one exception is a centre with
   `emit_centre = false`, which in production is always the HPM, already offered.
2. Cache eviction is "clear when full" (`cpp/v3_score.h:284`). After a clear, a model is re-scored fresh and offered
   again. The stores are idempotent: `offer_hpm` uses the strict order `hpm_better`, and `TopStore::offer` rejects
   duplicates (`cpp/v3_ledger.h:51`).

Swap and independence proposals are likewise scored before their accept uniforms (`:153`<`:156`, `:174`<`:177`,
`:186`<`:189`). Two steps score nothing: a neighbour swap with N(j)∖S = ∅ (`:170`), and a uniform swap at
|S| ∈ {0, p} (`:148`).

**Finding SR-3 (new, harmless in production).** Inherited calibration models are scored and offered directly with
`led.offer_stores` (`cpp/v3_core.cpp:415–419`) and are **not** put in the cache. Table models are offered by
`ingest_tables` (`:369–384`), also without the cache. A later engine evaluation of such a model is therefore a cache
miss, so it is fresh and offered again (idempotent). This direction is safe: the cache can hide a model from the stores
only if the model was inserted *without* being offered. In production that happens only for the local-search centre,
which is the HPM.

## 2. GUARD: no guard path reads an RNG or changes a setting

**Finding GUARD-1 (PROVED by code reading; also executed, §7).**
- `RuntimeGuard` (`cpp/v3_runtime.h:13–28`) holds a clock origin, an allocation, a sticky flag and a record list.
  `check` (`:21–27`) reads `steady_clock` (`:19`), appends a record and returns the sticky flag. It has no access to a
  `VariateSource`, the `Data`, the `Start`, the `Ledger`, the `ScoreCache` or any setting.
- `records` and `exceeded` are read only by the report (`cpp/v3_core.cpp:745–758`).
- The only generator is `Xoshiro256ss` (`cpp/v3_util.h:43–61`), behind `RngSource` (`cpp/v3_engine.h:20–23`). No
  other generator appears in `cpp/`: a search for `rand`, `unif_rand`, `R::`, `mt19937` and `random_device` finds
  none.
- Guard call sites in C++:

| Site | When the check runs | What a firing check does |
|---|---|---|
| `cpp/v3_engine.h:335` | after `population_round` of each bridge stage (`:331`) | the island returns `partial` (`:336–337`) |
| `cpp/v3_core.cpp:450` | after the final local search (`:447–449`) | sets status `resource_limit` |
| `cpp/v3_core.cpp:613` | after the pilot local search (`:610–612`) | status `resource_limit` |
| `cpp/v3_core.cpp:660` | after the diagnostic local search (`:657–659`) | status `resource_limit` |
| `cpp/v3_core.cpp:738` | `cpp_runtime_check`, called from `v3_calib.R:75` after each grid construction | as `v3_calib.R:81, 113` |

- Every check is evaluated *after* the operation it times. A check that does not fire returns `false`, and execution
  continues on exactly the instruction path of the guard-free run (`guard == nullptr` / `runtime = NULL`).
- Every firing ends the fit with status `resource_limit`. The C++ sites: `cpp/v3_core.cpp:442` stops the later islands
  and skips the local search, and `:450` sets the status. In R: `v3_calib.R:57, 81, 100, 113, 144, 148`,
  `v3_fit.R:90, 126–131`, `v3_run.R:111–116`. I checked W5's complete list (C1–C7) again and found no new site.
- **So a run that no guard stops is the R̄ computation.** On {status ≠ `resource_limit`}, every statistical output
  equals that of the same code with `runtime = NULL`. Only operational fields can differ: `timings`, `seconds*`,
  `runtime_guard`.
- W5's caveats G1–G4 still apply. The main one (G1): a stopped fit returns an HPM labelled `hpm_incomplete`
  (`v3_fit.R:128`), which is not R̄'s, so Theorem 4 needs the convention "a stopped fit is no output". §7 confirms that
  the stop path behaves this way.

## 3. Local search: scan before limit (`Engine::local_search`, `cpp/v3_engine.h:378–418`)

The task cites lines 369–420. The function body is `:378–418`, and its specification comment is `:370–377`.

**Finding LS-1 (PROVED by code reading).**
- Each pass of `while (true)` (`:384`) first completes a full scan of the centre C:
  - all feasible flips j = 0..p−1 (`:393–398`); additions are skipped iff |C| ≥ K (`:396`);
  - then all swaps j ∈ C, l ∉ C (`:399–405`).
- Only after the scan is the archive written (`:406`, `scan_complete = 1` unconditionally), and only then is the move
  limit tested (`:407–409`).
- If the scan finds a strict F improvement (`best.F > C.F`) and `moves ≥ ell`: the search returns `best` without
  moving (`local_limit = TRUE`, `"move_limit"`), *after* scoring every neighbour of C. Otherwise it moves (`:411`).
- If there is no strict improvement: `"no_improvement"`, `local_certified = TRUE`, and C is returned (`:413`).
- So: at most ℓ moves and at most ℓ + 1 scans; every scan is complete; the last scan's neighbours are all scored.
- Every neighbour goes through `eval(q, ME_LOCAL)` with `emit = true` (`:390`). Ties in F are broken by plain
  lexicographic order (`:391`). An exact tie is not a move (`:407`). The search builds its own `Particle C` and
  `Q` and never touches particles or a `VariateSource`, so **the local search consumes no random numbers**.

## 4. LS0's `emit_centre`

**Finding LS0-1 (PROVED by code reading).**
- *Production v3 contains no LS0.* The three `local_search` calls (`cpp/v3_core.cpp:447, 610, 657`) all start at
  `led->hpmS` with `emit_centre = false`.
- The only LS0 implementation in the repository is the O-LS0 test export
  (`theory/O-LS0:theory_campaign/O-LS0/scripts/ls0_exports.cpp`). Its `cpp_final_run_ls0` is a verbatim copy of
  `cpp_final_run` plus one block after the final local search and its guard check:
  `ModeResult m = start_mode(st); LocalArchive A0 = E.local_search(m.S, o.ell, o.tier, true, -2);`, then a guard check
  labelled `"ls0"`. It runs on the **same** `Ledger` and `ScoreCache`, with **`emit_centre = true`**.
- Hence S̃₀ is scored as an event. If it is fresh, it is offered to the HPM and the stores. If it is a cache hit, it
  was offered when first scored (§1). All of LS0's scanned neighbours are emitted (`:390`).
- LS0 reads no `VariateSource`, so it does not perturb the final islands' streams. It runs after them.
- The block is guarded by `status == "completed"`, so it runs only on a completed final run, and a guard firing after
  LS0 sets `resource_limit`, consistent with GUARD-1.
- The standalone export `cpp_ls0_local_search` (own ledger, no cache) also passes `emit_centre` through. The O-LS0
  driver calls it with `TRUE` for LS0 (`10_ls0_fit.R:54`).

**Finding LS0-2 (PROVED by code reading; repeats W5 IMPL-EMIT, which is correct).** If LS0 were run with
`emit_centre = false` from a centre never scored before, the centre would be scored fresh and inserted in the cache
(`cpp/v3_engine.h:91–94`) but not offered. Every later evaluation in that run would be a cache hit and also not offered
(`cpp/v3_ledger.h:110`), until the cache is next cleared. So `emit_centre = true` is **required** for LS0, not
optional. The O-LS0 implementation sets it.

*Paper consequence.* The method with LS0 is defined by `cpp_final_run_ls0`, which is not in the production core. If
the paper's main theorem is about "v3 + LS0", the reference implementation of LS0 must be cited as that export, or
merged into the core, before the supplement says "the reference implementation".

## 5. IND-T: sequential stream reading (`run_island_s`, `cpp/v3_engine.h:274–368`)

**Finding STREAM-1 (PROVED by code reading).**
- *One stream per final island.* `RngSource rng; rng.g.seed_stream(seed, 9 + r)` is a fresh local object in each
  iteration of the island loop (`cpp/v3_core.cpp:434–437`), i.e. streams 10–13.
- *Calibration streams.* The pilot uses stream 0 (tier 0) or 5 (tier 1) (`:594–595`). The diagnostics use streams
  1–4 or 6–9 (`:635–636`). These calibration streams persist across rebuild iterations through the `CalState::stream`
  map (`:561–566`; R6).
- *Reading order within an island, all from the one `vs`:*
  1. N initial π₀ draws, particle 1 first (`:286–292`).
  2. Per bridge stage: the reweighting (no uniforms, `:317–322`), then `resample` reads N uniforms (`:250`), then
     `population_round` (`:331`).
  3. L burn-in rounds and then Hm measured rounds (`:343–360`).
- *Within a round.* `population_round` (`:215–218`) runs particle i's complete round before particle i+1's. Each round
  draws its m − 1 order uniforms first (`draw_order`, `:195–200`), then the step uniforms in the drawn order
  (`:202–214`).
- The number of uniforms a step reads depends on the state and on the uniforms already read:
  - Gibbs: always 1;
  - uniform swap: 0 at |S| ∈ {0, p}, else 3;
  - neighbour swap: 0 at S = ∅; 1 if N(j)∖S = ∅; else 3;
  - independence: the π₀ draw (variable length) plus 1.
- There are no per-particle streams and no reseeding. The guard (§2) and the local search (§3) read no uniforms.

So W5's Lemma STREAM applies as stated: under EX-S, the particles' within-round paths read consecutive blocks of one
iid stream, starting and ending at stopping times. Between resamplings, the particle trajectories are conditionally
independent Markov chains.
*Executed evidence.* In every replay of §8, the final stream positions (`position_end`) and the initial-draw hashes
agree exactly between the two precisions and between the guarded and guard-free runs.

## 6. Corrections and refinements to earlier records

- Task text "local_search lines 369–420": the function is `cpp/v3_engine.h:378–418` (comment `:370–377`).
- SR: as in W5, read SR as "both **feasible** configurations", and "offered to the ledger" as "a ledger event; passed
  to the HPM and stores on its first fresh evaluation" (§1, SR-2).
- SR-3 (new): table and inherited models enter the stores without entering the cache. This is harmless, and it is the
  safe direction.
- LS0 (new): production has no LS0. The only implementation is the O-LS0 export, which uses `emit_centre = true` on
  the run's ledger and cache (§4).
- VAL-FP wording (new, §8.4): the contract can be stated **given the frozen object 𝓒^fp** of the floating-point
  calibration, so the exact-arithmetic run need not reproduce the calibration. This replaces W5's repair ("the exact
  run has the same status and the same 𝓒"), which cannot hold literally for a continuous grid.
