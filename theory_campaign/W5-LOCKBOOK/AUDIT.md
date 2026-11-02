# W5-LOCKBOOK — AUDIT.md: implementation lemmas (read-only code audit)

Run W5-LOCKBOOK, 2026-11-02. **Nothing here has been reviewed.** The engine was read, not executed: R is not
available in this container and the C++ was not compiled. Each lemma below is a statement about the **source text**
at the commit this branch was cut from (`theory/campaign` 9db8748; last commit touching `Scripts/SMC_BVS/core/cpp`
is 39db138). Status of every lemma: **PROVED by code reading** (each line cited was read; the compiled behaviour, the
R interpreter's behaviour and floating point were not tested). A same-seed replay is still the empirical test
(§8).

File fingerprints (sha256, first 16 hex): `v3_engine.h` 0a0b95ab126bc23b, `v3_core.cpp` 64c0a38c569f0abc,
`v3_runtime.h` f28e73c129bab734, `v3_ledger.h` 7641811d73e635bf, `v3_score.h` 41173ac1460e180e, `v3_start.h`
19e0a0bd0e479490, `v3_run.R` 330b9f8347c1e4f3, `v3_fit.R` 656f11d704e566c8, `v3_calib.R` 268aa414e811af96.
Paths below are relative to `Scripts/SMC_BVS/core/`.

Notation: R̄ is the potential uninterrupted run (W2-BOOK PROOF §0.1): the same code with `runtime = NULL`
(so every `guard && …` short-circuits) and no preflight. 𝒢 = {status = `resource_limit`}.

---

## 0. Inventory: every way a fit can end, and every clock read

**Clock reads that can change control flow** (all other clock reads only fill `seconds`/`timings` fields):
| # | Site | Effect when it fires |
|---|---|---|
| C1 | `v3_fit.R:90` preflight (`pf$exceeds`; SMC branch memory-only, `v3_fit.R:45`; exact branch also uses a timing measurement) | return `resource_limit` before any stream is read |
| C2 | `v3_calib.R:148` escalation preflight `preflight(1)` (memory-only, deterministic in (n, p, budgets, allocation)) | `resource_limit`, calibration stops |
| C3 | `cpp/v3_engine.h:335` `guard->check` after every bridge stage of **every** island (pilot, diagnostic, final) | island returns `partial = TRUE` |
| C4 | `cpp/v3_core.cpp:613`, `:660` check after the pilot / diagnostic local search | calibration status `resource_limit` |
| C5 | `v3_calib.R:75–76` check after each grid construction (`cpp_runtime_check`) | calibration status `resource_limit` |
| C6 | `cpp/v3_core.cpp:442` final island partial ⇒ `status = "resource_limit"`, later islands not run, no local search | final status `resource_limit` |
| C7 | `cpp/v3_core.cpp:450` check after the final local search | final status `resource_limit` (all final quantities were computed) |

`RuntimeGuard::check` (`cpp/v3_runtime.h:21–27`) reads `steady_clock` (`:19`), appends a record, sets the sticky
`exceeded` flag and returns it. It takes no `VariateSource`, holds no reference to `Data`, `Start`, `Ledger`,
`ScoreCache` or any setting, and nothing reads `records`/`exceeded` except the report (`cpp/v3_core.cpp:745–758`).
A search of `cpp/` for other generators (`rand`, `unif_rand`, `R::`, `mt19937`, `random_device`) finds none; the only
generator is `Xoshiro256ss` (`cpp/v3_util.h:43–61`) behind `RngSource` (`cpp/v3_engine.h:20–23`).

**Scorer call sites** (`Scorer::score`): `cpp/v3_engine.h:92` (`Engine::eval`: islands and local searches),
`cpp/v3_start.h:93` (tables), `cpp/v3_core.cpp:417` (inherited models, final run), `:682` (V rescoring),
`:506` (exact branch), `:131` (exact-branch timing), and the user interfaces `:112`, `:255` (not called by `v3_fit`).

---

## 1. GUARD (stop-only coupling)

**Lemma IMPL-GUARD.** For every input, seed and clock path: if the fit's status is not `resource_limit`, then the
status and every *statistical* output of the fit (HPM, its F and provenance, near-tie list, top/leader stores,
Ẑ_r, Ẑ, 0.05Ẑ, primary PIPs, MPM, flags E1–E3/low-ESS/local_limit/near_tie_truncated, `local_certified`, score
counters, the frozen object 𝓒 and the calibration archive) are those of R̄. Only the fields `timings`, `seconds_*`,
`runtime_guard` and `peak_memory_kb` (operational metadata) can differ. On 𝒢, the fit returns
`estimates_available = FALSE` and `hpm_incomplete = TRUE`.

*Evidence.*
1. No guard path touches an RNG: `check` has no generator argument (`cpp/v3_runtime.h:21`); the engine calls it
   *after* `population_round` for the stage (`cpp/v3_engine.h:331–335`), so a check that does not fire consumes no
   uniform and changes no particle. Stream positions are counted in `Xoshiro256ss::count` (`cpp/v3_util.h:45, 53`)
   and only `next()` advances them.
2. No guard path touches a setting: budgets come from `v3_budgets(n, p)` (`v3_preprocess.R:19–33`) and
   `v3_cal_settings`/`v3_run_settings` (`v3_calib.R:9–13`, `v3_run.R:85–90`), none of which reads the clock. The
   frozen object is built only when the calibration status is `ok` (`v3_calib.R:166–172`) from `last$grid`,
   `tier`, `N`, `L`, `ex$inherited`.
3. No guard path touches the inherited store or the cache: `ingest_tables`, `offer_stores` and `ScoreCache::insert`
   are reached only from scoring (`cpp/v3_ledger.h:102–111`, `cpp/v3_engine.h:89–101`, `cpp/v3_core.cpp:369–384,
   410–420`). The numerical-failure reconciliation (`cpp/v3_core.cpp:452–477`) is on a separate status and never
   runs on a guard stop.
4. Every firing of C1–C7 ends the fit with status `resource_limit`: C1 `v3_fit.R:90`; C2 `v3_calib.R:148` then
   `v3_fit.R:126–131`; C3 in calibration `cpp/v3_core.cpp:605` (pilot) and `:641–649` (diagnostic) then
   `v3_calib.R:57, 100` (`fail`) and `v3_calib.R:144`; C4 `v3_calib.R:57, 100`; C5 `v3_calib.R:81, 113`; C6, C7
   `cpp/v3_core.cpp:442, 450` then `v3_run.R:111–116`. **No path converts a fired check into a different setting,
   tier, grid or schedule** (in particular a calibration-time stop never leads to a final run on a modified 𝓒:
   `v3_fit.R:126–131` returns before `v3_final_run`).
5. Hence on 𝒢^c no check fired, every `guard && …` branch was not taken, and the executed instruction sequence is
   R̄'s (the clock is read but its value only enters timing fields). The sticky flag cannot fire "late" on 𝒢^c
   because 𝒢^c means it never fired.

*Stop-only coupling.* R̄ is a function of (data, streams 0–13). The actual status is a function of (R̄-prefix, clock):
the fit stops at the first firing checkpoint. No assumption on the law of the clock is needed or made.

**Caveats that the paper statement must carry (new, from this audit).**
- **(G1) HPM on a stopped fit.** On 𝒢 the fit *does* return an HPM (`v3_run.R:110–115`, `v3_fit.R:128`): the best
  model scored before the stop, labelled `hpm_incomplete`. That HPM is not R̄'s. Thm 4 is therefore valid with the
  study convention (D61) **𝒢 ⊆ U** ("a stopped fit is no output"); it is **false** if a stopped fit's HPM is counted as
  output, because the stopped run's scored set is a prefix of 𝒮̄ chosen by the clock. Exception: a C7 stop returns
  exactly R̄'s HPM, but the convention still counts it as no output; this only loses probability, never validity.
- **(G2) Archived partial values.** On a C6 stop the returned object carries `partial_final = raw`
  (`v3_run.R:113`), which contains the completed islands' `log_Z`, `pip` and the stopped island's *partial* `log_Z`
  (product over the stages run). These are archive fields, not estimates (`estimates_available = FALSE`), but they
  are partial evidences that differ from R̄'s. Any analysis that reads them is outside Prop 2 and Thm 6.
- **(G3) Errors outside the status set.** A C++ exception other than `NumericalFailure` (e.g. `std::bad_alloc`) or an
  R error aborts `v3_fit` with no return value. This is another no-output event; it belongs in U (and in 𝒪^c) and
  is also stop-only (it cannot change a returned value, because nothing is returned).
- **(G4) The guard is shared by calibration and final run** (`v3_fit.R:71`, passed at `v3_fit.R:123, 134`), so the
  final-run stop probability depends on calibration time. Irrelevant to validity (no law is assumed), relevant to
  any attempt to model P(𝒢).

Status: **PROVED by code reading.** This upgrades W2-BOOK's "GUARD (IMPL, code reading of three files)" to a reading
of every stop site, including the calibration paths and the R layer, with caveats G1–G4 added.

---

## 2. OUT (no partial estimate is ever *reported*)

**Lemma IMPL-OUT.** (i) The fields that carry the evidence and PIP estimates — `log_Z_r`, `log_Z`, `log_Z_lower95`,
`log_Z_rel_m0`, `pip_r`, `pip_primary`, `mpm` — are written only in `v3_assemble_final` after the test
`raw$status != "completed"` fails (`v3_run.R:111–130`), i.e. only when the final run's status is `completed`; on the
exact branch only when `e$status == "exact"` (`v3_fit.R:98–102`). (ii) Status `completed` is set only when all four
islands returned `partial = FALSE`, the final local search ran, the C7 check did not fire and no `NumericalFailure`
was thrown (`cpp/v3_core.cpp:404–452`). (iii) Hence on 𝒪_E = {status ∈ {exact, completed}} the reported estimates
are computed from four complete islands and equal R̄'s (Lemma IMPL-GUARD); `resource_limit` after allocation and
`numerical_failure` in the final run **never** return a reported Ẑ or PIP (`v3_run.R:111–116`: `estimates_available
= FALSE`, early return). (iv) The only partial evidence/PIP values ever returned are the archive fields of caveat G2
and the calibration estimates, which are labelled "never reported as the estimate" (`v3_calib.R:52–56, 96–99`).

*Answer to the task's question (b).* **No** failure mode returns a partial *reported* evidence or PIP. A partial
evidence is returned only in the archive (`partial_final`, calibration estimates). OUT as stated in W2-T26 (§0:
"on 𝒪_n ∩ 𝒢_n the reported outputs equal the potential run's") holds, provided "reported outputs" means the fields in
(i). Under EX-A, `numerical_failure` does not occur; in floating point it is a no-output event and must sit in 𝒪^c,
which is how W2-T26 and W2-BOOK already use it.

One more check needed by Thm 6: the reported MPM is `orig[pip_primary > 0.5]` with **no cap K**
(`v3_run.R:130`; METHODOLOGY §6.11 "it may exceed K and is reported as computed"). W2-BOOK Prop 1(1)'s "with the cap
K keep the min(K, N₊) largest PIPs" is the Bayes rule, not what the code reports; Thm 6 only uses MPM̂ = S₀ when all
PIP errors are < ½, where both coincide. Flagged for STATEMENTS wording (the paper's MPM is the uncapped one).

Status: **PROVED by code reading.**

---

## 3. SR (scoring rule of `step_gibbs`)

**Lemma IMPL-SR.** In every Gibbs step at state S on coordinate j (`cpp/v3_engine.h:113–132`):
(a) the current state S is recorded as a logical score event (`held`, `:118`; mechanism `gibbs_held`), without
re-evaluation; (b) if the other configuration S Δ {j} is feasible (j ∈ S, or |S| < K: `:116`), it is evaluated by
`eval` (`:119–123`) **before** the uniform is drawn (`:129`), whatever the outcome; (c) if it is infeasible (j ∉ S,
|S| = K) it is not in Ω and nothing is scored for it; o_j = 0 (`:117`, `:119` skipped), one uniform is still read
(`:129`) and the state is unchanged (`include = u < 0` is false); (d) every model that becomes a particle state was
offered to the HPM running best when first evaluated in this ledger.

*Evidence for (d) and for "offered to the HPM".* `Ledger::event` offers to the stores only on a fresh evaluation
(`cpp/v3_ledger.h:110`); `held` passes `is_fresh = false` (`cpp/v3_engine.h:104`). This is correct because
(1) every particle state is the output of an `eval` with `emit = true` (initial draw `:291`, flip `:122`, swap
proposals `:153, :174`, independence proposal `:186`) or a resampled copy of such a state (`:326`); (2) a cache hit
(`is_fresh = false`) returns a model that was inserted by an `eval` of the same engine (`:91–94`), and every insertion
in the final run comes from an `eval` with `emit = true`, except the final local-search centre (`emit_centre =
false`, `cpp/v3_core.cpp:447`), which is `led.hpmS`, already offered. The same holds for the calibration state
(`cpp/v3_core.cpp:610, 657`: centres are `led->hpmS`). (3) Cache eviction is "clear when full"
(`cpp/v3_score.h:283`), after which a model is re-evaluated fresh and re-offered (idempotent: `offer_hpm` uses the
strict order `hpm_better`, `cpp/v3_util.h:121–126`; stores reject duplicates, `cpp/v3_ledger.h:51`).
Swap and independence proposals are evaluated before their accept uniform (`:153` before `:156`; `:174` before
`:177`; `:186` before `:189`), so rejected proposals are scored. A neighbour swap with N(j)∖S = ∅ makes no proposal
and scores nothing (`:170`); a uniform swap at |S| ∈ {0, p} likewise (`:148`).

So the scored set 𝒮̄ of R̄ = table models (`cpp/v3_core.cpp:369–384`) ∪ inherited calibration models
(`:410–420`) ∪ every model evaluated by the four final islands (initial draws, both feasible Gibbs configurations,
every swap/independence proposal) ∪ the final local search's scanned neighbours; and the reported HPM is the
`hpm_better`-maximum over 𝒮̄ (`cpp/v3_ledger.h:82–86`). The centre of the final local search is already in 𝒮̄.

SR as used by T21/Thm 4 ("scored includes rejected proposals and both Gibbs configurations") holds with the reading
**"both feasible configurations"**. Status: **PROVED by code reading.**

---

## 4. IND-T premise (stream structure)

**Lemma IMPL-STREAM.** (a) Final island r uses exactly one generator, `seed_stream(seed, 9 + r)`
(`cpp/v3_core.cpp:435–436`), fresh per island; calibration uses streams 0–9 through `CalState::stream`
(`cpp/v3_core.cpp:562–566, 594–595, 635–636`). (b) Within an island the particles are processed **sequentially**:
`population_round` runs particle 1's complete round, then particle 2's, … (`cpp/v3_engine.h:215–218`), and each
round reads its m − 1 order uniforms first (`:195–200`) and then the step uniforms in the drawn order
(`:202–214`). (c) The number of uniforms a particle reads in a round depends on its state and on the uniforms read
(none for a uniform swap at |S| ∈ {0, p}, two fewer for a neighbour swap with N(j)∖S = ∅, a variable number for the
π₀ draw inside the independence step, `cpp/v3_start.h:158–176`). (d) There are no per-particle streams and no
reseeding (`v3_run.R:13`). (e) Resampling reads N uniforms before the stage's rounds (`cpp/v3_engine.h:248–257`).

**Lemma STREAM (probabilistic consequence). PROVED** (under EX-S: the stream is an iid U(0,1) sequence).
Let U₁, U₂, … be iid U(0,1), 𝓕_k = σ(U₁, …, U_k), and let a particle's round consume the uniforms U_{τ+1}, …, U_{τ′}
where τ and τ′ are stopping times of (𝓕_k) (τ′ is a stopping time because the decision to read one more uniform is a
function of the entering state, which is 𝓕_τ-measurable, and of the uniforms read so far). By the strong Markov
property of an iid sequence, (U_{τ+1}, U_{τ+2}, …) is iid U(0,1) and independent of 𝓕_τ. Hence, given 𝓕_τ (which
contains every earlier particle's and round's path), the particle's within-round path is the image of a fresh iid
sequence under its own round map started from its entering state, and the next particle's round starts at the
stopping time τ′. By induction over particles and over rounds, given the σ-field 𝓗 at a round boundary, the
particles' (order, path) pairs for that round are conditionally independent with the round-kernel laws (this is
T12's (R3)); and given the σ-field at a boundary after the last resampling, the **H-round trajectories** of distinct
particles (no resampling in between) are conditionally independent Markov chains with kernel K₁, each started at
its boundary state. (Induct on rounds: in round h + 1 each particle's segment is fresh given everything earlier,
including the other particles' round-h segments.) ∎

This is exactly the premise used by W1-T24G Cor. B-M and W2-BOOK (e-M): it holds **for the sequential single-stream
implementation** under EX-S, with no per-particle streams needed. What it does *not* give: anything about xoshiro's
actual output (EX-S is an idealisation), and independence across a resampling (ancestors couple the particles).

Status: IMPL-STREAM **PROVED by code reading**; Lemma STREAM **PROVED**.

---

## 5. The scan-before-limit rule and `emit_centre`

**Lemma IMPL-LS.** In `Engine::local_search` (`cpp/v3_engine.h:378–418`):
(a) **Scan before limit.** Every pass of the loop first completes a full scan of the current centre C — all
feasible flips j = 1..p (additions skipped iff |C| = K, `:393–398`) and all swaps j ∈ C, l ∉ C (`:399–405`) — and
only *then* tests the move limit (`:407–409`). So the last scan is always complete, and when `moves = ℓ` and an
improvement exists the search returns the best neighbour without moving to it (`local_limit = TRUE`, `:409`) but
after scoring every neighbour of C. (b) Each scanned model goes through `eval(q, ME_LOCAL)` with the default
`emit = true` (`:390`), so it is a score event and, if fresh, is offered to the HPM running best; if a cache hit, it
was offered at its first evaluation (§3). (c) Moves are strict-F improvements only (`:407`), ties broken by plain
lexicographic order (`:391`); at most ℓ moves, so at most ℓ + 1 scans (`:408, :411`). (d) A scan of a centre of size
k evaluates at most p flips (exactly p if k < K, exactly k if k = K) and exactly k(p − k) swaps. (e) The centre is
evaluated once with `emit = emit_centre` (`:381`); the method calls it with `emit_centre = false` in the final run
(`cpp/v3_core.cpp:447`), the pilot (`:610`) and the diagnostics (`:657`), always with centre `led->hpmS`, which is
already in the stores. (f) The search never alters particles (it builds its own `Particle C`).

**Finding (LS0 / `emit_centre`): stronger than the F-REFINE caveat.** If a local search is ever started from a
model that has **not** been offered (LS0 from the exact start mode S̃₀ is the case at hand) with `emit_centre =
false`, the centre is evaluated *fresh*, inserted into the run's cache (`cpp/v3_engine.h:91–94`) and not offered.
Every later evaluation of that model in the same run is then a cache hit (`is_fresh = false`) and is **also not
offered** (`cpp/v3_ledger.h:110`), until the cache is next cleared. So the reported HPM can fail to be the best scored
model even if a particle later sits on S̃₀. LS0 therefore needs `emit_centre = true` (one line), not just "as a
convenience": without it Lemma IMPL-SR(d) and Thm 4's definition of 𝒮̄ fail for that model.

Status: **PROVED by code reading.**

---

## 6. Two small facts used by T32(i) (proved in PROOF.md §T32)

- **IMPL-T.** Under EX-A, the pilot has at most T_e stages (`cpp/v3_calib.h:30–46`: each step either reaches 1, or
  advances by lo − φ ≥ 1/T_e, or is forced to min(1, φ + 1/T_e)); every successful grid has at most T_e intervals
  (`cpp/v3_calib.h:94`). Diagnostic islands run only on a successful grid (`v3_calib.R:84–86`, `g$ok`), and the final
  run only on the last successful grid of the final tier (`v3_calib.R:120, 153, 168`).
- **IMPL-LOOP.** Per tier: one pilot, at most ℓ diagnostic iterations of 4 islands (`v3_calib.R:85`), at most ℓ + 1 V
  rebuilds (`:79, :111`), one local search per pilot and per iteration. At most two tiers, each at most once
  (`v3_calib.R:141–150`). One final run of 4 islands and one final local search.

---

## 7. One-line implementation lemmas (paper/supplement form)

| Code | One-line lemma | Evidence |
|---|---|---|
| IMPL-GUARD | Every resource stop ends the fit; no stop alters a random number, a setting, the inherited store or the cache; so off `resource_limit` all statistical outputs equal those of the uninterrupted run. | `cpp/v3_runtime.h:13–28`; `cpp/v3_engine.h:331–338`; `cpp/v3_core.cpp:442, 450, 605, 613, 641–649, 660`; `v3_calib.R:57, 75–81, 100, 113, 144, 148`; `v3_fit.R:90, 126–131`; `v3_run.R:111–116` |
| IMPL-GUARD′ | A stopped fit reports an incomplete HPM; Thm 4 requires counting it as no output (𝒢 ⊆ U). | `v3_run.R:110–115`; `v3_fit.R:128–129` |
| IMPL-OUT | Evidence, its bound, PIPs and MPM are reported only on `exact`/`completed`; no failure mode reports a partial estimate (partial values exist only in labelled archive fields). | `v3_run.R:111–130`; `v3_fit.R:98–103`; `cpp/v3_core.cpp:404–452` |
| IMPL-SR | Each Gibbs step counts the current state and evaluates the other configuration whenever it is feasible, before the draw; every swap and independence proposal is evaluated before acceptance; every evaluated model reaches the HPM running best. | `cpp/v3_engine.h:113–132, 146–192, 89–105`; `cpp/v3_ledger.h:82–111` |
| IMPL-STREAM | One sequential stream per island, particles processed in order, uniforms read at state-dependent rates, no per-particle streams; under EX-S this gives (R3) and conditional independence of particle trajectories between resamplings (Lemma STREAM). | `cpp/v3_core.cpp:435–437`; `cpp/v3_engine.h:195–218, 248–257`; `cpp/v3_start.h:158–176` |
| IMPL-LS | Every local-search scan is completed before the move limit is tested; all scanned models are scored and reach the HPM; ≤ ℓ moves, ≤ ℓ + 1 scans, each ≤ p + k(p − k) evaluations, plus one centre evaluation. | `cpp/v3_engine.h:378–418` |
| IMPL-EMIT | The method's three local searches start at the current HPM with `emit_centre = false`, which is harmless; LS0 must set `emit_centre = true`, or its centre can be permanently hidden from the HPM by the cache. | `cpp/v3_engine.h:381, 89–101`; `cpp/v3_core.cpp:447, 610, 657`; `cpp/v3_ledger.h:110` |
| IMPL-T | Pilot stages ≤ T_e (EX-A); grid intervals ≤ T_e; at most two tiers, ≤ ℓ diagnostic iterations per tier. | `cpp/v3_calib.h:30–46, 94`; `v3_calib.R:85, 141–150` |

---

## 8. What this audit does not establish

- Compiled behaviour (no build here), R's behaviour, and floating point (VAL-FP is still unmeasured).
- That `xoshiro256**` behaves like EX-S.
- The D61 same-seed replay test of GUARD (completed fits re-run at a larger allocation should be bitwise identical,
  apart from timing fields) is the empirical check; it needs the R/C++ engine.
- An independent reader should re-check §1 item 4 (the list of stop sites) against any later engine commit; any
  new `guard` call or `cpp_runtime_check` must end the fit for IMPL-GUARD to survive.
