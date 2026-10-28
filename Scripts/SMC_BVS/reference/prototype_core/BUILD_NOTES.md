# BUILD_NOTES — SMC-BVS v3 core layer (CORE_SPEC v2 §§0–9) and calibration layer (§10, core_dev)

Builder: agent A (Opus 5.5), 2026-10-20. Spec: `specs/CORE_SPEC.md` sha256 1ed91d47…4e2 (v2). Method: METHODOLOGY_v3.md
sha256 93043758…019c ("M"). Status: **built and smoke-tested by the builder only; not independently verified** (Part A
of VERIFY_PHASE1 is the independent check). Not built: §10 calibration layer, §11 pair moves (out of scope).

Usage:
```r
source("/projects/ml75/fb31/BVS/v3_profiling_20261020/code/core/v3.R")   # sources R files, compiles C++ (cached)
fit <- v3_fit(X, y, seed = 1, grid = c(0, 0.2, 0.6, 1), opts = list(force_smc = TRUE))
```
Compile/run only on compute nodes (`source $P/code/env.sh`). The compiled library is cached in
`.cpp_cache/<first 16 hex of sha256 over all cpp/*.h, cpp/*.cpp>/`; any header edit forces a rebuild. Do not start
several jobs at once on a fresh source hash (they would compile into the same cache directory concurrently): run one
job first (any script that sources v3.R), then the rest.

## 1. Files and what each implements

| File | Implements (spec section) |
|---|---|
| `v3.R` | entry: sources the R files, `v3_compile()` (Rcpp::sourceCpp with `-I cpp/`, hash-keyed cache) |
| `v3_preprocess.R` | §1: `v3_preprocess` (statuses, precedence, standardisation M §4.4, dup components), `v3_budgets` (M §3, exact-branch count) |
| `v3_setup.R` | §§2–3: `v3_context`, `v3_score`, `v3_blocks`, `v3_tables`, `v3_start`, `v3_start_logmass`, `v3_start_logdeficit`, `v3_start_draw`, `v3_start_mode`, `v3_discrepancy`, `v3_neighbours`, `v3_setup` |
| `v3_run.R` | §§4–7: `v3_frozen`, `v3_final_run` + output assembly (§6), `v3_replicate_final`, `v3_trace`, `v3_step_sample`, `v3_round_sample`, `v3_resample_sample` (extra, A17), `v3_local_search` |
| `v3_exact.R` | §7 `v3_enumerate` (M §6.2, R9); §8 exact reference `v3_reference` (p ≤ 22) |
| `v3_observer.R` | §8 observer preparation and report, start quantities (§8.1), `v3_operational` (R11 invariance helper) |
| `v3_fit.R` | §7 `v3_fit`, preflight (M §8.6, `resource_limit`), `summary.json` |
| `v3_calib.R` | §10: `v3_pilot_schedule`, `v3_build_grid`, `v3_calibrate` (pilot, V, rebuild loop, checks, escalation, freeze), §8.5 observer view |
| `cpp/v3_calib.h` | §10: pilot next-φ rule, population ESS, F_V and ρ_V, grid construction (fixed arithmetic `lse_cal`) |
| `cpp/Makevars.v3` | pinned compiler flags (no FMA contraction, portable ISA; §10.3 F1) |
| `cpp/v3_util.h` | RNG (SplitMix64 → xoshiro256**), log-sum-exp, log1mexp, logistic, Zobrist model hash, bitsets, lexicographic and HPM orders |
| `cpp/v3_score.h` | §2: `Data` (G, z, yᵀy, C_n, w(k), W_K), `Scorer` (Cholesky → refactor → augmented QR → `numerical_failure`; non-negative Q form), `ScoreCache` |
| `cpp/v3_blocks.h` | §3: complete linkage with R13, top-down cut, next-fit packing; neighbour graph (M §6.4) |
| `cpp/v3_start.h` | §3: tables (R2), size profiles, truncated convolution, log Z̄₀, exact backward sampler, start mode (max-plus), composite sum |
| `cpp/v3_ledger.h` | §7: HPM running best + provenance, top-(40p+1) store, two leader stores (R3), logical/fresh/held counters, island bests (R5), `dump_scored` |
| `cpp/v3_observer.h` | §8 items 2–4: watched-model ledger, opportunities/hazards, stage and round occupancy, watch-set first exits, recording prefix (T23) |
| `cpp/v3_engine.h` | §§4–7: particles, variate sources, tracer, the four steps, the random-order round, multinomial resampling, one final island (R7, R8), local search (R4) |
| `cpp/v3_core.cpp` | Rcpp entry points (conversions only), AGG/T22 start quantities, final run driver, replication, enumerate, reference |
| `smoke/` | builder's smoke scripts (`smoke*.R`, `run.sh`) and logs (`out/`) |

## 2. RNG and stream design (§5, §4.1)

- Generator per (seed, stream): x = seed·2³² + stream; xoshiro256** state = four successive SplitMix64(x) outputs.
  Uniform u = (next() >> 11)·2⁻⁵³ ∈ [0, 1).
- Final island r uses stream 9 + r (10..13); nothing in the core layer touches streams 0–9. Particles of an island are
  processed sequentially on the island's single stream (no per-particle streams). Test samplers: `v3_step_sample` /
  `v3_round_sample` stream 100; `v3_resample_sample` stream 101; `v3_start_draw` stream 200 unless given.
- The observer draws no random numbers (R11). Same seed ⇒ bit-identical outputs (smoke 3; replication = final run).
- Variate consumption order (documented for replay; also in `v3_trace(...)$variate_order_doc`):
  1. initial draws, particle 1..N: π₀ draw = `pi0_size` (1 uniform, categorical over k = 0..K); `pi0_block_size` for
     b = J..1 while the remaining size r > 0 (1 each); `pi0_submodel` for b = 1..J with k_b > 0 (1 each; subsets of
     the given size in increasing local bit-code order, bit i−1 ↔ i-th member of the block).
  2. per stage t: N `resample` uniforms (ancestor i = smallest k with W_k ≥ u_i; W_k = c_k/c_N, c_k = Σ_{i≤k} exp(lw_i − max lw), W_N := 1);
     then particles 1..N, each one round: m − 1 `order` uniforms (Fisher–Yates on G1..Gp, U, N1..NB, I: for i = m..2,
     j = ⌊u·i⌋ + 1, swap i and j), then per step in the realised order:
     Gibbs: 1 `gibbs` (include iff u < o_j; consumed even when o_j = 0);
     U: none at |S| ∈ {0, p}; else `uswap_j` (position ⌊u·k⌋+1 of S sorted), `uswap_l` (position ⌊u·(p−k)⌋+1 of the complement sorted), `uswap_accept`;
     N<b>: none at S = ∅; else `nswap_j`; if N(j)∖S = ∅ stop (rejected, no score); else `nswap_l`, `nswap_accept`;
     I: a π₀ draw (as in 1) then `indep_accept`.
  3. L burn-in rounds, then the measured rounds, each as in 2 without resampling.
- π₀ categoricals use "smallest k with cumulative > u" with the cumulative set to exactly 1 from the last positive-mass
  category on (never returns a zero-mass category); resampling uses the spec's "≥" rule.
- `v3_trace(..., variates = list(uniforms, orders, draws))`: prescribed uniforms are consumed in the order above
  (continuing across islands); prescribed `orders` (character label vectors, one per particle-round in execution order)
  replace the Fisher–Yates uniforms; prescribed `draws` (models) replace every π₀ draw (initial draws when
  `init_states` is NULL, then independence proposals, in execution order) and their uniforms.

## 3. CORE_SPEC interface → code

| CORE_SPEC | R | C++ |
|---|---|---|
| `v3_preprocess(X, y)` | v3_preprocess.R | — |
| `v3_budgets(n, p)` | v3_preprocess.R | `cpp_exact_count` (128-bit saturating) |
| `v3_context(Xs, ys)` (+ `orig`, `hooks`) | v3_setup.R | `data_init` |
| `v3_score(ctx, S)` | v3_setup.R | `Scorer::score` |
| `v3_blocks(ctx, B)` | v3_setup.R | `complete_linkage`, `make_blocks` |
| `v3_tables(ctx, blocks)` | v3_setup.R | `build_tables` |
| `v3_start(ctx, blocks, tables)` | v3_setup.R | `build_start` |
| `v3_start_logmass(start, S)`, `v3_start_draw(start, N, rng)`, `v3_start_mode(start)` | v3_setup.R | `Start::log_pi0`, `draw_pi0`, `start_mode` |
| `v3_discrepancy(ctx, start, S)` | v3_setup.R | `cpp_discrepancy` |
| `v3_neighbours(ctx)` (+ optional `B`) | v3_setup.R | `neighbour_graph` |
| setup bundle | `v3_setup(ctx, B_override = NULL)` | `cpp_setup` |
| `v3_step_sample(setup, S, label, phi, M, seed)` | v3_run.R | `Engine::step_gibbs/uswap/nswap/indep` |
| `v3_round_sample(setup, S, phi, M, seed, trace)` | v3_run.R | `Engine::one_round`, `Tracer` |
| `v3_replicate_final(setup, frozen, seeds, opts)` | v3_run.R | `cpp_replicate` → `Engine::run_island` |
| `v3_trace(setup, init_states, grid, opts, variates)` | v3_run.R | `cpp_final_run(trace = TRUE)` |
| `v3_final_run(setup, frozen, seed, observer, opts)` | v3_run.R | `cpp_final_run` |
| frozen object | `v3_frozen(grid, tier, N, L, inherited, budgets)` (sha256 attached) | — |
| `v3_local_search(setup, centre, state)` | v3_run.R | `Engine::local_search` |
| `v3_enumerate(ctx)` | v3_exact.R | `cpp_enumerate` |
| `v3_fit(X, y, seed, grid, observer, opts, allocation)` | v3_fit.R | — |
| exact reference files (§8) | `v3_reference(setup, path)` | `cpp_reference` |
| A17 resampler | `v3_resample_sample(logw, M, seed)` (extra) | `Engine::resample` |
| R11 invariance | `v3_operational(fit)` strips observer, timings, preflight, peak memory | — |

Conventions for the checker:
- Every model at R level is a sorted integer vector of 1-based original indices. Sampler outputs use keys
  `"j1,j2,..."` (`""` = ∅); `v3_key_to_model(key)` inverts.
- Labels: `"G<j>"` with j the **original** index, `"U"`, `"N<b>"` (b = 1..B, identical kernels), `"I"`.
- `v3_tables` entry `code + 1` holds subset U with bit i−1 ↔ `members[i]`; entries with |U| > K (only possible with
  `B_override` > K) are NA and never scored.
- Trace step table columns: island, phase, stage, round, particle, position, label, phi, pre, proposal, alpha, o_j,
  accepted, post, u_first, u_count, rb_recorded. For Gibbs: `proposal` = the other configuration (S∪j or S∖j; "NA" if
  the addition is infeasible), `alpha` NA, `accepted` = inclusion indicator. Self-loops: proposal "NA", accepted −1.
  Neighbour swap rejected without score: proposal "NA", alpha 0, accepted 0. `u_first`/`u_count` index the uniform log
  (`trace$uniforms`, with purpose and value). Stage list: incoming states, d, log weights, log increment, ESS,
  resampling uniforms, ancestors (1-based), cumulative log Ẑ. `trace$init`, `trace$orders`; RB accumulators in `rb`.
- Final-run output (selected): `log_Z_r`, `log_Z` (pooled), `log_Z_lower95` (= log 0.05Ẑ), `log_Z_rel_m0`,
  `log_increment` (per island, per stage), `pip_r`, `pip_primary`, `pip_secondary`, `mpm`, `stage_table`,
  `terminal_table`, `flags` (E1, E2, E3, low_empirical_ESS, local_limit, near_tie_truncated, checks_passed_final;
  calibration flags NA), `hpm`, `hpm_F`, `hpm_provenance` (phase, mechanism, tier, island, stage, round, particle,
  position, phi), `near_ties`, `local_search` (archive), `local_certified`, `island_best`, `leaders_gamma0`,
  `leaders_gamma1`, `top_store`, `score_counts` (logical / fresh, phase × mechanism; mechanisms table, init_draw, gibbs_held, gibbs_flip,
  uswap, nswap, indep, local_scan, inherited — R15), `cache`, `dump_scored`
  (models, F, log m, log γ₀, counts[model, phase, mechanism], first-score event), `resampler_trace` (offspring counts
  per stage), `rb`, `timings`, `settings` (resolved N, L, measured rounds, islands, tier, ell, cache capacity).
- `opts` accepted: N, islands, L, measured_rounds, ell (test override of the local-search move limit), force_smc,
  dump_scored, cache_capacity, B_override, resampler_trace, switch_no_candidate_grid (recorded only), hooks (scorer
  test hooks: `fail_min_size`, `fail_routes` ⊆ {chol, chol_refactor, qr}), out_dir (v3_fit writes fit.rds and
  summary.json), seed (v3_trace only).

## 4. Interpretations of the spec or M (reading chosen)

I1. **Local-search improvement (lead ruling R14, 2026-10-20; replaces the earlier total-order reading)**: the best
    scanned neighbour has the largest F, exact F ties broken by plain lexicographic order (proper prefix first); it is a
    move only if its F is strictly larger than the centre's F. An exact-F tie with the centre is not a move, does not
    count toward `local_limit` and does not prevent `local_certified`. Every scanned model still updates the HPM running
    best (HPM tie rule), so an exact-tie neighbour can become the reported HPM without being a move; the fit-level
    `local_certified` is the search's flag (it refers to the returned model). Scan order: flips j = 1..p (additions only
    if |S| < K), then swaps (j ∈ S ascending) × (l ∉ S ascending). After ℓ moves one further scan; if it finds a strict
    F improvement, `local_limit = TRUE`, `termination = "move_limit"`, the returned model is that neighbour (not
    scanned) and `local_certified = FALSE`. (Code review N-1: this reading stands by the lead's decision; the reviewer's
    A13 reference returned the last centre, and A13 did not compare the returned model. The HPM is unaffected.)
I2. **Lexicographic order** of sorted index vectors: first differing element; a proper prefix precedes. Leader stores (R3)
    break exact value ties lexicographically only; the HPM and the top-(40p+1) store use size then lexicographic.
I3. **Score events (SR; lead ruling R15)**: each Gibbs step logs two events under separate mechanism labels —
    `gibbs_held` (the current state, counted as scored, not re-evaluated) and `gibbs_flip` (the other feasible
    configuration S∪j or S∖j); at |S∖j| = K only `gibbs_held`. The split applies to `score_counts`, `dump_scored`
    counts and first-score events, the observer's per-model counts and first-score events. Observer Gibbs opportunities
    and watch-set exits caused by a Gibbs step are recorded under `gibbs_flip`. The per-stage move statistics column
    `gibbs_state_changes` (stage table: `acc_gibbs_change`) counts Gibbs steps that changed the state. Proposals of U/N/I are events whether accepted or not; a
    neighbour swap rejected because N(j)∖S = ∅ is not. Tables: every subset of every block is an event (∅ once per
    block). The local-search **centre** is not an event in production (it is the global best, already scored); in the
    `v3_local_search` testing interface (fresh ledger) it is evaluated as one `local_scan` event.
I4. **Stores are updated only on fresh evaluations.** The cache is owned by each run, so a cache hit or a held state was
    offered to the stores when first scored; re-offering is idempotent (also after eviction). Island bests (R5), the
    dump and the observer see every logical event. Verified: `cache_capacity = 16` gives identical outputs (smoke 3).
I5. **Cache**: open addressing keyed by the model bitset; clear-entirely-when-full eviction; default capacity
    max(500p, 2¹⁵) entries (≥ 500p). Tables and inherited models are not cached (R2).
I6. **B_override** changes B everywhere B appears: block size, neighbour-list cap and the number of N-labels.
I7. **R9 error bound** η(S) = 64ε[ν(yᵀy/Q)(1 + k·κ_H) + k(κ_H + κ_A) + |log C_n| + ν|log(2b₀+Q)|], κ = (max/min Cholesky
    diagonal)² (a cheap lower estimate of the condition number). `global_certified` iff F(HPM) − η(HPM) >
    max_{S≠HPM}[F(S) + η(S)] over the enumeration; margin and bound reported. This bound is a documented heuristic, not
    a proved bound (lead ruling R16: accepted for the prototype); outputs label it `hpm_error_bound_kind =
    "heuristic_condition_estimate"` (`v3_enumerate`, also inside `R9`) and `error_bound_kind` (`v3_score`).
I8. **Start-mode ties**: sets whose per-block choices attain the per-size block maxima and the DP maxima exactly
    (enumerated, cap 10⁶ sets, flag reported); floating-point absorption ties (a non-maximal prefix whose rounded sum
    equals the maximum) are not enumerated.
I9. **δ_comp** (T22): the supremum over S ⊉ S₀ reduces to T ⊆ ∪{blocks meeting S₀} with nothing outside (the prior ratio
    w(k)/w(k+a) decreases in k), computed by an exact DP over (|T|, |S₀∖T|); NA when > 3 blocks meet S₀ (spec). u_n and
    δ_comp are taken from `Theory_architecture_v3/theorems/T22_T16_start_aggregation.md` (the spec's "T22 definition";
    that file was read for the definitions only).
I10. **Correlations** for blocks and neighbours: r_jl = G_jl/√(G_jj G_ll) from the Gram of the standardised columns.
I11. **Preprocessing record**: `col_max` = max|x|, `col_mean`/`col_sd` on the max-scaled column, so raw
    x = col_max·(col_mean + col_sd·x_std); `s_y` on the raw scale; `y_max`, `y_mean`, `y_sd_scaled` likewise.
I12. **E1 (final)** compares each island's R5 best with the final HPM (after the final local search, including tables);
    **E2** uses sd with denominator R − 1 (FALSE for one island); **E3** = HPM changed by the final local search;
    `low_empirical_ESS` = any stage ESS < 0.5N; `checks_passed_final` = none of E1, E2, E3, low ESS.
I13. **near_tie_truncated** = the top store is full and its smallest F is within 10⁻⁹ of the best.
I14. **Preflight** planning assumptions (M §8.6 leaves them open): time = score count × measured seconds per fresh
    score at k̄ = min(K, 10) (SMC) or min(K, ⌈p/2⌉) (exact); SMC score count = ⌈p/B⌉2^B + R·N(T + L + 4)(p + B + 2)
    + (ℓ+1)(p + k̄(p−k̄)), T = length(grid) − 1 (or 50 if no grid). Memory: itemised in `v3_preflight`. Because the
    preflight times scores, a status of `resource_limit` near the boundary can depend on machine speed.
I15. **Opportunities before the first score** (§8.2) are reported as counts and hazard sums by phase × mechanism up to
    and including the successful opportunity (not as an event-by-event chronological list), per watched model.
    Watch-set first exits are recorded for every round with a `before_last_weight` flag (bridge rounds of stages < T).
I16. **Observer start quantities** use the observer scorer (a separate `Scorer`, no cache); the start mode, AGG q, e,
    u_n, δ_comp and chain ratios use only tables (no scoring).
I17. **Exact branch accumulation** uses long-double accumulators with rescaling when the running maximum increases.
I18. `v3_trace` applies `init_states` to every island; default islands = 1, `dump_scored` forced on.
I19. Numerical failure: inside tables (setup), the final run or the enumeration, the fit returns status
    `numerical_failure` with the best model scored so far, `hpm_incomplete = TRUE`, `message` and
    `estimates_available = FALSE` — the same fields on the exact and SMC branches (fix round, A3); `v3_score` itself
    raises an R error.
I20. Observer parts (fix round): every subset of {truth, watch, watch_sets, refs, chains}, including `list()` and empty
    or unnamed lists, is accepted; unnamed watch entries are named `watch<i>`, unnamed sets `set<i>`. Parts are read
    with exact names (`[[ ]]`; R's `$` partial matching made `observer$watch` return `watch_sets`).

## 5. Not implemented / limits

- §10 calibration (pilot, V, candidate grid, rebuilds, triggers, escalation, `schedule_limit`), §8.5 calibration
  snapshots: not built. `v3_fit` requires a numeric `grid` on the SMC branch; `grid = "calibrate"` raises an error.
  Calibration flags in outputs are NA. `switch_no_candidate_grid` is recorded only. Phases `pilot`, `diag` exist in the
  ledgers but are never used. The inherited state of `frozen` supports `inherited = list(models = list(...))` only
  (offered to the stores with provenance phase/mechanism `inherited`).
- §11 pair moves: not built.
- `dump_scored` has no hard p limit (memory grows with the number of distinct scored models).

## 6. Questions for the lead — rulings received (ASSUMPTIONS.md R14–R18)

R14 (Q1): applied (I1). R15 (Q2): applied (I3). R16 (Q3): applied (I7). R17 (Q4): as built. R18 (Q5, Q6): as built.

## 7. Smoke tests (builder's own; compute node, single seed)

Command pattern (`smoke/run.sh LOG PARTITION TIME MEM SCRIPT [ARGS]`):
`srun -n 1 -p commons -t <TIME> -c 1 --mem=<MEM> bash -lc "source $P/code/env.sh && cd $P/code/core/smoke && Rscript <SCRIPT> [ARGS]" > smoke/out/<LOG>.log`
Runs: `./run.sh smoke1_exact commons 00:20:00 4G smoke1_exact.R`, `./run.sh smoke2_fit commons 00:30:00 8G smoke2_fit.R`,
`./run.sh smoke3_status commons 00:30:00 8G smoke3_status.R`, `./run.sh smoke5_trace commons 00:30:00 8G smoke5_trace.R`,
`./run.sh smoke6_p20 commons 00:30:00 8G smoke6_timing.R p20`, `./run.sh smoke6_p500 commons 01:00:00 16G smoke6_timing.R p500`,
`./run.sh smoke6_p1000 commons 00:30:00 16G smoke6_timing.R p1000`. Full logs: `smoke/out/*.log`. The plain-R references
in `smoke/smoke_common.R` are the builder's own (written in the same session), not independent of the build's author.

(1) `v3_enumerate`, p = 10 (n = 40, K = 10, all 1,024 models) vs a plain-R brute force (solve/determinant):
```
log Z: build -55.543642494218  brute -55.543642494218  diff 7.105e-15
max |PIP diff| = 2.442e-15
HPM build: 4 7  brute: 4 7  F diff: 7.105427e-15
models scored: 1024 of 1024 ; global_certified: TRUE ; margin: 1.437 ; bound: 2.85e-12
scorer vs plain: max|dlog m| = 3.553e-14, max|dF| = 4.263e-14
log Zbar0: build 3.636113484594 brute 3.636113484594 diff 4.441e-16 ; max |log pi0 diff| = 7.105e-15
start mode build: 4 7  brute: 4 7 ; max |d diff| (50 models) = 7.105e-15
size law (2e5 draws): max |emp - exact| = 0.000627
```
Budgets spot values (M §3 table rows and threshold-adjacent pairs) printed in smoke1_exact.log, e.g.
`n=200 p=500 K=100 B=14 ell=10 L=8 N0=2500 H0=512 T0=1000 exact=FALSE`, `(200,17) exact=TRUE`, `(200,18) exact=FALSE`,
`(10,36) exact=TRUE`, `(10,37) exact=FALSE`, `(5,3000) exact=TRUE`.

(2) `v3_fit(X, y, 7, grid, opts = list(force_smc = TRUE, dump_scored = TRUE))`, easy p = 12 (n = 100, s0 = 2), supplied
oracle grid with T = 11 (exact full-space ESS rule at threshold 0.995, from `v3_reference`):
```
status: completed  branch decision: exact  branch run: smc
log Zhat_r: -119.23621 -119.23515 -119.23330 -119.23134
pooled log Zhat = -119.233997 ; exact log Z = -119.236535 ; diff = 2.5386e-03 ; log 0.05Zhat = -122.2297
max |PIP primary - exact| = 0.0000 ; secondary = 0.0000
HPM: 5 8  (exact HPM: 5 8 )  MPM: 5 8 ; flags all FALSE, checks_passed_final = TRUE ; local search no_improvement, certified
HPM == argmax over dump: TRUE ; missing outputs: (none)
```
(3) same seed twice: `same seed identical (operational): TRUE`; seed 8 gives a different log Ẑ (-119.2367).
(4) observer (truth, two watched models, one watch set, one completion chain, refs) on/off:
`observer on/off identical (operational): TRUE`; observer report present (first-score events, opportunities, AGG
q = 0.378, e = 0.0209, u_n = 0.473, δ_comp = 0.00609, max_j|o_j(S0,1) − 1{j∈S0}| = 0.0906, B̄_r ≈ 0.52, round/stage occupancy).
Also at (200, 20): `with observer: 0.62 s (overhead 6.6%); operational identical: TRUE`.

(5) `v3_trace(setup, init_states = list(integer(0), 1:4), grid = c(0, 0.3, 1), opts = list(L = 1, measured_rounds = 2))`,
p = 4, N = 2: uniforms 266, steps 80, orders 10, init 2, stages 2. Builder's internal checks:
```
(a) states chain through each realised order: TRUE
(b) max |o_j - exact conditional| over 40 Gibbs steps: 5.55e-17
(c) log increments reproduced (1e-12): TRUE   (d) ancestors reproduced: TRUE
(e) log Zhat_r = log m0 + log Zbar0 + sum inc: TRUE      (f) RB accumulators reproduced: TRUE
(g) replay from recorded uniforms (different seed) identical steps: TRUE  identical log Zhat: TRUE
(h) replay with prescribed orders and pi_0 draws: steps identical TRUE, log Zhat identical TRUE, HPM identical TRUE
(i) binding cap p = 5, n = 6 (K = 3): Gibbs additions at |S| = K have o_j = 0 and no proposal: TRUE; max size visited 3
(j) trace-derived scored set and per-model mechanism counts == dump_scored: TRUE (3 traces)
```
Step sampler (2e5 draws) vs exact o_j at S = {2}, φ = 0.37: G1 0.97288/0.97308, G2 0.99947/0.99948, G3 0.06190/0.06271,
G4 0.22577/0.22603 (exact/empirical); resampler offspring means 0.5015 1.0047 1.4938 vs 0.5 1 1.5.

Statuses and other checks (smoke3_status.log): invalid_input (NA, Inf, n < 3, p < 1), no_predictors, precedence
(no_predictors over y_constant; invalid_input over no_predictors), y_constant (HPM = ∅), a constant column dropped with
original indices carried (kept 1 2 4 5 6 7, HPM 5), exact with global_certified, resource_limit (tiny allocation),
numerical_failure via hooks in the exact branch, the SMC branch (best model so far, `hpm_incomplete`) and during
tables; routes chol / chol_refactor / qr reached by hooks; `cache_capacity = 16` (11,341 clears) leaves all outputs
except cache statistics and fresh counts identical; `v3_replicate_final` log Ẑ_r and PIP_r bit-identical to
`v3_final_run` for the same seeds; 10⁴ replications (N = 2, T = 2, L = 1, p = 12) in 0.20 s; local search with ℓ = 1
from ∅ ends `move_limit`, `local_limit = TRUE`, not certified; with ℓ = 7 it reaches the exact HPM {4, 6, 9}.

R14 re-check (`./run.sh smoke7_local commons 00:20:00 4G smoke7_local.R`, after the change; smoke 2 re-run unchanged in
every printed output):
```
R14 local search: build == plain-R reimplementation for 60 of 60 (centre, ell) cases
F({1}) == F({2}): TRUE        (column 2 an exact duplicate of column 1)
from centre {2}: termination no_improvement  moves 0  local_limit FALSE  certified TRUE  returned 2  ledger HPM 1
```

R15/R16 re-check (smoke2_fit.log, smoke5_trace.log after the change): all smoke-2/4/5 checks above unchanged
(log Ẑ − log Z = 2.54e-3; same-seed and observer on/off identical; trace checks (a)–(j) TRUE, dump soundness with the
new labels TRUE in 3 traces); `gibbs_held` / `gibbs_flip` totals in dump = ledger (2,640,000 each); observer counts
carry both labels; `R9 kind: heuristic_condition_estimate`.

Fix round after Part A (`./run.sh smoke8_fixround commons 00:30:00 8G smoke8_fixround.R`; smokes 2, 3, 5 re-run
unchanged):
```
branch exact status numerical_failure hpm integer(0) hpm_incomplete TRUE estimates_available FALSE message: numerical_failure: ...
branch smc   status numerical_failure hpm integer(0) hpm_incomplete TRUE estimates_available FALSE message: numerical_failure: ...
all 21 observer variants ok and R11-invariant: TRUE   (16 subsets of {truth, watch, watch_sets, refs} incl. {},
    unnamed / partly named watch, unnamed sets, empty watch lists, chains)
v3_fit with observer list(), truth, truth+unnamed watch, all parts: R11-invariant: TRUE TRUE TRUE TRUE
```

## 8. Timings (NOTS commons node, one core, final build)

| Case | Time |
|---|---|
| (200, 20): final run, 4 islands × N = 2,500, oracle grid T = 5, L = 8, 4 measured rounds, + local search | 0.58 s (target ≤ 2 min); |log Ẑ − log Z| = 0.0034, max|PIP − exact| = 0.0003 |
| (200, 20): same with observer | 0.62 s (+6.6%; target ≤ 10%) |
| (200, 20): setup / `v3_reference` (2²⁰ models) / `v3_enumerate` | 0.02 s / 0.79 s / 0.77 s |
| (200, 500): setup (blocks 0.01, tables 0.05 [126,336 entries, J = 53, B = 14], start 0.02, neighbours 0.02) | 0.12 s |
| (200, 500): ONE final island, N = 2,500, T = 20 (timing grid φ_t = (t/20)³), L = 8, 4 measured, + final local search | 11.9 s (init 0.003, bridge 6.5, burn-in 3.5, measured 1.7); 81.4M logical score events, 9.25M fresh; peak RSS 143 MB |
| (200, 1000): setup (blocks 0.03, tables 0.10 [230,944 entries, J = 105], start 0.04, neighbours 0.08) | 0.29 s; peak RSS 145 MB |

Scores at these sizes are cheap (small k); costs grow as O(k³) per fresh score with the model size k.

## 10. Calibration layer (merged into core; CORE_SPEC v2 §10, M §§6.1, 6.6–6.9)

Built in `$P/code/core_dev/` (development copy; `core/` untouched). New files: `v3_calib.R` (orchestration),
`cpp/v3_calib.h` (pilot rule, ρ_V, grid construction), `cpp/Makevars.v3` (pinned compiler flags); C++ entry points
`cpp_pilot_schedule`, `cpp_build_grid`, `cpp_cal_new`, `cpp_cal_pilot`, `cpp_cal_diag`, `cpp_cal_V`, `cpp_cal_export`,
`cpp_observer_new`, `cpp_observer_report` in `cpp/v3_core.cpp`. `run_island` generalised (fixed grid or adaptive
pilot schedule; calibration phase labels); with identical flags it reproduced core's final runs bit for bit
(smoke9, before the flag change below).

### 10.1 Interface additions (for the checker)

`v3_pilot_schedule(d_vector, H, T_e)` → `list(schedule, forced_pilot_steps, forced_stage, T)`. The pilot rule applied
repeatedly to a FIXED supplied vector d from φ = 0: if ESS(1 − φ) ≥ 0.9H then φ' = 1; else 60 halvings on (φ, 1]
(lo = φ, hi = 1; mid = (lo+hi)/2 passes → lo = mid, else hi = mid), φ' = lo; if φ' − φ < 1/T_e then
φ' = min(1, φ + 1/T_e) and the step is forced. ESS(δ) = exp(2·LSE(δd) − LSE(2δd)), LSE(x) = m + log(Σ exp(x_i − m))
(m = max, terms in double, summed in index order in long double, sum rounded to double, log in double; identical to
R's `m + log(sum(exp(x - m)))`). `schedule` starts at 0 and ends at exactly 1; `forced_stage` = 1-based stage
numbers of the forced steps. T_e is the argument (the test override of the stage ceiling).

`v3_build_grid(logg0_V, d_V, pilot_temps, T_e)` → `list(grid, ok, reason, rho_appended, intervals, F_V_evaluations,
seconds)`. F_V(t) = LSE(log γ₀ + t·d) over V in the supplied order (same LSE); ρ_V(u,v) = exp(2F_V(v) − F_V(u) −
F_V(2v−u)). From u = 0: b = smallest pilot temperature > u; if ρ_V(u,b) ≥ 0.90 append b, else 60 halvings on (u, b]
(lo = u, hi = b; passes → lo = mid) and append lo (no tested point passed → `non_progress`); validate v > u
(`non_progress`) and ρ_V(u,v) ≥ 0.90 (`validation_failed`); more than T_e intervals → `too_many_intervals`; no target
above u → `no_target_above_u`. On failure `grid` is the partial grid. Arithmetic: compiled without FMA contraction,
so an implementation doing the same operations in double reproduces every decision (builder's plain-R check: identical
grids and schedules in all cases, smoke10).

`v3_calibrate(setup, seed, tier = 0, opts = list())` → list:
- `status` ∈ {ok, schedule_limit, numerical_failure, resource_limit (v3_fit only), grid_failure_no_escalation (only with
  opts `escalate = FALSE`)}; `calibration_seed`; `tier_final`; `escalated`; `hpm` (model, F, provenance);
  `ledger` (calibration score counts by phase × mechanism, stores, dump if `dump_scored`); `cache`;
- `flags`: escalated, checks_passed_calibration, forced_pilot_steps (sum over tiers), grid_unconverged,
  triggers_fired, triggers_by_tier;
- `frozen` (status ok): `v3_frozen(grid, tier, N = N_e, L, inherited)` with `source = "calibration"` (or
  "calibration (switch_no_candidate_grid)"), sha256; `inherited = list(models = union of the top-(40p+1) store and both
  leader stores, hpm = list(model, F, provenance))`;
- `tiers[[k]]`: `tier`, `settings` (H, T_e, L, Hm, ell, `overrides`), `status`, `pilot` (schedule, forced_pilot_steps,
  `stream` (stream, position_start, position_end, init_draws_hash), local_search archive, best_before_local,
  best_after_local, `calibration_estimate` (label, log_Z, pip, ess, log_increment)), `grid`, `grid_source`,
  `converged`, `rebuilds`, `triggers` (E1, E2, E3, forced_pilot_steps, grid_failure, grid_unconverged, local_limit),
  `iterations[[it]]` (iteration, grid used, `streams` data frame (island, stream, position_start, position_end,
  init_draws_hash), log_Z_r, island_best, overall_best, E1, E2, E3, local_search archive, `calibration_estimate`
  (label, log_Z_r, pip_r, ess)), `snapshots[[k]]` (§8.5: label "preliminary" / "rebuild_<it>", size, truncated,
  models, log_gamma0, d), `grids[[k]]` (label, grid, ok, reason, intervals, F_V_evaluations), `grid_construction`
  (seconds, F_V_evaluations), `seconds` (pilot, rebuild_islands, rebuild_local, grid_construction, total).
- opts (test only, recorded in `settings$overrides`): `H` (pilot/diagnostic particles at tier 0, ×4 at tier 1),
  `T_e_override` (stage ceiling: scalar = both tiers; length 2 = tier 0, tier 1), `ell` (rebuild budget and
  local-search move limit), `L`, `N` (final N_e), `calibration_seed` (replaces `seed` for streams 0–9),
  `escalate = FALSE` (no tier 1), `switch_no_candidate_grid`, `dump_scored`, `cache_capacity`.
- Stream position = number of 64-bit xoshiro256** outputs consumed since the stream was seeded; init_draws_hash = hex of
  h ← SplitMix64(h ⊕ Zobrist(S_i) ⊕ i), i = 1..N, h₀ = 0x243F6A8885A308D3 (equal initial populations ⇒ equal hash).

`v3_fit(..., grid = "calibrate")` (also the default when `grid = NULL`): preflight before the calibration (tier 0) and
again before an escalation (tier 1) → `resource_limit`; calibration; `schedule_limit` if the tier-1 grid fails (best
scored model returned, estimates unavailable); else freeze and final run (streams 10–13). Output adds `calibration`
(the v3_calibrate list), `frozen`, and in `flags`: escalated, checks_passed_calibration, forced_pilot_steps,
grid_unconverged, calibration_triggers. Observer: one observer object spans calibration and final run;
`observer$calibration[[tier]]` = watched_in_V (snapshot × watched model logical matrix), V_truncated, grids, triggers.

Event context (all ledgers, dump first-score events, provenance, observer rows): new field `iter` = −1 (tables, final
run, testing interfaces), 0 (pilot and its local search), k (rebuild iteration k: diagnostic islands and their local
search). Phases `pilot` and `diag` label every event of those islands; their measured rounds are numbered L+1..L+4
(burn-in 1..L). Pilot island id 0, diagnostic islands 1..4. Observer stage/round/exit rows gained `phase`, `tier`,
`iter`. `v3_operational()` now strips `observer`, `timings`, `seconds`, `preflight`, `peak_memory_kb` recursively.

### 10.2 Readings chosen (calibration)

C1. Pilot (M §6.6): H_e particles on stream 0 (tier 0) / 5 (tier 1); rule as in v3_pilot_schedule applied to the
    current population's d at each stage; multinomial resampling and one round per stage; L burn-in and 4 measured
    rounds; then one local search from the global best (R4). Pilot log Ẑ and RB PIPs archived as calibration estimates.
C2. V (M §6.7, R3): {∅} ∪ top-20p by log γ₀ ∪ top-20p by log γ₁ (leader stores over everything scored in the fit,
    tables included), deduplicated, listed and summed in lexicographic order of the index vectors; log γ₀ and d
    recomputed by a separate scorer (not score events). V is frozen during each construction.
C3. Rebuild loop: preliminary grid from the pilot V; then for it = 1..ℓ: 4 diagnostic islands (H_e each, streams 1–4 /
    6–9 continuing across iterations, R6) on the current grid, L burn-in + 4 measured rounds each; one local search;
    rebuild V and grid; stop if the rebuilt grid equals the current one exactly (converged; that grid is used);
    a failed construction stops the tier (grid_failure). After ℓ iterations without equality: grid_unconverged and
    the last rebuilt grid is kept (used at tier 1).
C4. Checks (M §6.9, R5): E1 = some island best of the LAST iteration is > 1 nat below the global best after that
    iteration's local search; E2 = sd (denominator 3) of the last iteration's 4 log Ẑ > 1; E3 = any calibration local
    search (pilot or iteration) strictly increased the global best's F (RC-1; an exact-F tie change does not count); forced pilot steps > 0; grid_failure; grid_unconverged;
    local_limit in any calibration local search. Per-iteration E1/E2/E3 are archived.
C5. Escalation: any trigger at tier 0 → tier 1 (fresh pilot on stream 5, rebuilds on 6–9; ledger, stores and cache
    continue; one escalation at most); at tier 1 a grid failure → status schedule_limit; other triggers at tier 1 are
    reported only.
C6. switch_no_candidate_grid: pilot (and its local search) only; the pilot schedule is frozen as the final grid;
    available triggers (forced steps, E3, local_limit) may still escalate.
C7. Final run after calibration: fresh ledger (tables, then the inherited stores; the inherited HPM keeps its
    calibration provenance); everything else as in §6, so final trajectories, Ẑ_r and PIPs depend only on
    (grid, N_e, L, seed) — inherited models can change the HPM/near ties only.
C8. With ℓ = 0 (test override) no rebuild iteration runs and grid_unconverged is set.

### 10.3 Findings and questions for the lead

F1 (build flags; changes numbers). R's site Makeconf on NOTS compiles with `-march=native`: GCC then contracts a·b + c
    into FMA and the cached binary carries the ISA of whichever node compiled it (commons mixes node types, so a cached
    binary could fail with an illegal instruction elsewhere). core_dev pins `-O2 -fno-math-errno -ffp-contract=off
    -march=x86-64-v2` through a private Makevars (env var R_MAKEVARS_USER inside v3_compile only; nothing global).
    Effect vs core on supplied-grid runs: identical models, states, labels, counts, HPM; numeric outputs differ by
    ≤ 2e-12 (smoke9). This makes B1/B2-style bit-identity with an independent double implementation achievable.
    Decision needed at merge (Part A internal identity tests are unaffected; any cross-build bit comparison is).
F2 (ρ_V numerics). The formula exp{2F_V(v) − F_V(u) − F_V(2v−u)} loses all precision once |t·d| ≳ 10¹⁶ (absorption):
    e.g. V = {(0,0),(0,10²²)} gives ρ = 1 at (0, 0.5) although the exact value is 0.5, so the step is accepted. For
    non-progress, ρ_V must stay < 0.9 down to steps of (b−u)2⁻⁶⁰, which needs d spreads ≳ 10¹⁸ — exactly where the
    formula is unreliable. In double precision `non_progress` is therefore practically unreachable; a B2 non-progress
    case may need a different construction (or a ruling on a precision guard). Realistic |d| (≲ 10⁴) are unaffected.
Q1. C4: E1/E2 from the last rebuild iteration only (M's "checks" after the loop); E3 and local_limit from every
    calibration local search. Confirm.

### 10.4 Calibration smokes (core_dev, final build)
All on NOTS commons (`smoke/run.sh LOG commons TIME MEM SCRIPT`), build key 6ecb9167… (pinned flags):
- smoke10_rules: pilot rule on 3 supplied d vectors × T_e ∈ {1000, 10} (incl. a floor-forcing case: 10 forced steps)
  and grid construction on a two-mode V with a sharp crossing (V = {(log γ₀, d)} = {(0,0), (−20,25)}, targets
  {0, 0.5, 1} → 12 intervals clustered at the crossing t ≈ 0.8: 0 .356 .5 .609 .672 .714 .746 .773 .800 .827 .861 .917 1),
  T_e = 2 exceeded (`too_many_intervals`) and a random V: schedules, forced counts, grids and failure reasons identical
  to the builder's plain-R implementation in every case; min ρ_V at appended points 0.9000; d = 10²² case shows F2.
- smoke11_calfit (p = 12, n = 100, force_smc, production budgets H = 512, N = 2,500): status completed, no trigger,
  pilot T = 2, 1 rebuild, converged; log Ẑ − log Z = −6.8e-3, max|PIP − exact| = 1e-4, HPM = exact HPM (provenance
  pilot); same seed ⇒ identical; observer on/off ⇒ identical (observer: truth first scored in the pilot; watched_in_V
  matrix). Stream isolation: calibration seeds 101 vs 202 give different grids and inherited state; with grid/N/L
  fixed and only the inherited state swapped, final log Ẑ_r, PIP_r, stage table, terminal table and island bests are
  identical; `v3_fit` final == `v3_final_run(fit$frozen, same seed)`. switch_no_candidate_grid: final grid = pilot
  schedule. Triggers: T_e_override = 2 → forced_pilot_steps + grid_failure; H = 2, ℓ = 1 → E2 + grid_unconverged;
  ℓ = 0 → grid_unconverged; escalation runs tier 1 (H = 8 = 4×2, streams 5 / 6–9, V at tier-1 start ⊇ tier-0 V);
  T_e_override = c(2, 1000) → tier-0 grid failure → escalation → tier-1 grid → frozen tier 1; T_e_override = 2 (both
  tiers) → `schedule_limit` with the best scored model, estimates unavailable. R6: over 3 rebuild iterations every
  diagnostic island's stream position at the start of iteration k+1 equals its end position in iteration k, and the
  initial-draw hashes differ between iterations (TRUE / TRUE).
- smoke13_triggers (p = 60, n = 120, ρ = 0.8, tiny islands H ∈ {1,2}, ℓ ∈ {0,1,2}, 10 seeds each): E1 fired 2×, E2 14×,
  E3 9×, local_limit 6×, grid_unconverged 30× (with smoke11 every trigger of M §6.9 has been fired).
- smoke9_regress (core_dev vs core, supplied grid + trace): models, states, labels, counts, HPM, near ties identical;
  numeric outputs within 2e-12 (build flags differ, F1); before the flag change they were bit-identical.
- Core smokes re-run on core_dev: smoke2 (log Ẑ − log Z = 2.54e-3; same seed, observer on/off identical), smoke3
  (statuses, cache eviction, replicate == final run), smoke5 (trace checks (a)–(j) TRUE), smoke7 (R14: 60/60), smoke8
  (A3 fields; 21/21 observer variants R11-invariant): all as before.

### 10.5 Timings: end-to-end calibrated fit at (n, p) = (200, 500) (smoke12_e2e500, production budgets, one core)

| Phase | Seconds |
|---|---|
| setup (blocks, tables, start, neighbours) | 0.11 |
| pilot (H = 512, T = 12 stages, L = 8 + 4 rounds, local search) | 2.2 |
| rebuild iterations (5; 4 × 512 particles each, grid T = 18) | 49.8 |
| calibration local searches | 0.01 |
| grid construction (6 constructions, |V| ≈ 19,500, 7,128 F_V evaluations) | 1.1 |
| final run (4 × 2,500, T = 18, L = 8, 4 measured, local search) | 48.9 |
| total fit | 102.9 (target ≤ 2 h) |
Converged after 5 rebuilds, no trigger; HPM = truth; diagnostic log Ẑ_r sd 0.003–0.06; peak RSS 214 MB.

### 10.6 Concurrent loading (infrastructure fix after the Part C array)

Cause: 30 of 210 parallel tasks failed in `.sourceCppDynlibReadCache` (zero-byte index) because sourceCpp rewrites
its cache index on every call and concurrent tasks shared `.cpp_cache`. Fix (`v3.R`, `v3_compile`): the shared cache
`.cpp_cache/<key16>/` is built by exactly one process under an atomic lock (`mkdir <key16>.lock`) and marked
complete by `READY` (written via rename); other processes poll for READY (2 s; timeout 1 h; a lock older than 2 h
without READY is treated as stale and removed, and a partial cache is wiped before rebuilding). Every process, the
builder included, then copies the shared cache to `tempdir()/v3cpp_<key16>/` and calls sourceCpp on that private copy,
so the shared directory is only read after READY. A warm load does not recompile (0.2 s).
Smoke14 (`smoke/smoke14_concurrent.sh`, one node, `srun -c 20`): 20 concurrent `Rscript -e 'source(v3.R); v3_score(...)'`
processes with a cold cache (all racing to build) and then 20 with a warm cache:
```
cold: 20 of 20 OK; errors: 0   load seconds: min 15.2, median 16.3, max 16.3   (one build, 19 waited)
warm: 20 of 20 OK; errors: 0   load seconds: min 0.2, median 0.2, max 0.3
40 of 40 processes: same key 6ecb9167d2cf223f and same log m; 40 distinct private temp dirs; no lock left behind
```

### 10.7 Code-review fixes (verify/checker/CODE_REVIEW_core.md; lead rulings F1 accepted, F2 recorded, Q1 confirmed)

- D-1 preflight before any p×p allocation: `v3_fit` now runs `v3_preprocess(..., dup_components = FALSE)` (n×p only),
  budgets, then `v3_preflight(n, p, ...)` timed on a small context of the first min(p, 64) columns
  (`v3_time_scores`), and only then builds the full context (`return_gram = FALSE`: the Gram is no longer copied to R;
  `v3_context(..., return_gram = NULL)` copies it by default only for p ≤ 2000) and computes the duplicate components
  in C++ from the context's Gram (`cpp_dup_components`, pairwise screening, no temporaries). `v3_preprocess` used
  directly keeps `dup_components` but computes them column-chunked (512×512 cross-products). The memory estimate now
  counts 3 n×p copies, the Gram and the 2 further p×p matrices of block construction. In addition the score cache is
  now keyed by the sorted member list (int pool + 29-byte slots) instead of a p-bit bitset per entry, which removed an
  O(p²) allocation (≈ 6 GB at p = 6,000 with 500p entries); results are unchanged (smoke9 differences identical).
  smoke16 (n = 200, p = 6,000): allocation 0.5 GB → `resource_limit` after 0.3 s, peak RSS 133 MB (reviewer measured
  1,652 MB before the preflight in core); default allocation → setup + final run complete in 10.6 s, peak RSS 988 MB
  (estimate 1.33 GB), duplicate pair {1, 2} found.
- R-1 seeds: `v3_check_seed` (integer-valued, 1 ≤ seed ≤ 2³¹ − 1) in v3_fit, v3_final_run, v3_replicate_final (every
  seed), v3_trace (opts seed), v3_calibrate (seed and calibration_seed), v3_step_sample, v3_round_sample,
  v3_resample_sample, v3_start_draw (also the stream). smoke15: 1.5, 0, −1, 2³¹, NA, Inf rejected by all 10 entry
  points; 2³¹ − 1 accepted.
- R-2 exact-name access: every read of opts, frozen, allocation, state, observer, variates, inherited, hooks, rng uses
  `[[ ]]` (grep listing in the report; the only `$` match is an assignment to the package's own ctx object).
- R-3/R-4: watched models and truth with |S| > K are skipped and listed in `observer$infeasible_watched`;
  `observer$start$truth_feasible`, `watched[[w]]$feasible` and `chains[[c]]$feasible` report infeasibility (no AGG,
  o_j or chain values computed). smoke15: final run and calibrated fit complete, operational outputs identical to the
  runs without observer.
- R-5: `v3_start` errors unless there is one table per block with identical members and 2^|C_b| entries.
- R-6: block width 1..20 (`B_override` in v3_setup/v3_fit; `B` in v3_blocks, cpp_setup; block sizes in v3_tables and
  v3_start).
- R-7: resampling uses u' = max(u, smallest positive double): a particle whose normalised weight is 0 is never selected;
  identical to the §4.1 rule for every u > 0. `v3_resample_sample(logw, M, seed, uniforms)` accepts prescribed uniforms
  for this test (W = (0, 0.5, 1), u = (0, 0, 0.75) → offspring (0, 2, 1)).
- S-2: events of v3_step_sample / v3_round_sample carry phase `test` (new phase code after `inherited`).
- Rcpp cache race: §10.6 (smoke14 re-run on this build: 20/20 cold, 20/20 warm).
- Regression on this build: smoke2, 3, 5, 7, 8, 9, 10, 11 as before.

### 10.8 Fix round 3 (verify/checker/CODE_REVIEW_calib_and_fixes.md; work done directly in core after the merge)

- D-2 (v3_fit.R, before `v3_preflight`): the default grid (NULL → "calibrate") and the grid check are resolved before
  the preflight, so the estimate includes pilot, rebuild islands and calibration local searches. The preflight now
  reports `grid` and `score_components` (tables, final, final_local, and for "calibrate" pilot, rebuild_islands,
  calibration_local; `enumeration` on the exact branch). smoke17: default call at (200, 6000) with a 36 s allowance →
  `resource_limit` after 0.2 s, estimate 22,520 s (rebuild islands 2.4e10 of 3.3e10 scores), peak RSS 173 MB; at
  (200, 1000) the default-call estimate is 1,343 s with all six components vs 92 s for a supplied 3-point grid.
- RC-1 (v3_calib.R, `v3_E3_fires`): E3 fires iff the global best's F strictly increases during a calibration local
  search; an exact-F change of the model through the tie rule does not fire (reading C4 amended accordingly).
  smoke17: tie case FALSE, strict increase TRUE; p = 60 tiny-island runs consistent in 10/10.
- RC-2 (cpp/v3_calib.h, `pilot_next_phi` floor step and `build_grid`): a floor step or an appended grid point
  ≥ 1 − 1e-12 is set to exactly 1. smoke17: fully forced pilots at T_e ∈ {10, 1000, 2000, 4000, 16000} have exactly
  T_e stages (before: T_e = 10 gave 11 stages in smoke10); a target at 1 − 5e-13 is snapped (grid 0, 0.5, 1).
  The builder's plain-R reference in smoke10 now includes the snap (all 10 cases identical).
- RC-3 (v3_calib.R, `v3_calibrate`): the preflight before an escalation runs after the tier-0 triggers and before the
  tier change; if it fails: status `resource_limit`, `escalated = FALSE`, `tier_final = 0`,
  `escalation_blocked = "resource_limit"` (also in `flags`). smoke17: allocation 2 × the tier-0 estimate with a
  tier-0 grid failure → exactly these values, 1 tier run.
- Regression (core, this build): smoke2 (log Ẑ − log Z = 2.54e-3; same seed and observer on/off identical), smoke3
  (statuses, eviction, replicate == final), smoke10 (10/10 identical to the plain-R reference), smoke11 (calibrated
  p = 12 fit, isolation, triggers, escalation, schedule_limit, R6): as before.
- Final-run flag E3 (I12; lead ruling after round 3, M §6.9): now also fires only on a strict F increase of the global
  best during the final local search (v3_run.R:93, `v3_assemble_final`). Re-run: smoke2, smoke11, smoke17 as before.

## 11. sha256 of every file of core (BUILD_NOTES.md itself excluded; .cpp_cache/ and smoke/out/ not listed)

```
61984bf960fd53481d14bb35182910eef72b54ab243759fcc84fe1f075c12894  ./cpp/Makevars.v3
ca8aeb341b6031fe9f3e80f49697efb2d8a1a1ed79fdc6023c0bc5df1ed7abc0  ./cpp/v3_blocks.h
e9ad470bfe82548bdcdef11c57ec4bbff48401ba57d82468ca294c41c4ec2c7e  ./cpp/v3_calib.h
7ad69daae3a8f273740032dc19a6ff8767c0be827cf3cfeb7037439b49947ca0  ./cpp/v3_core.cpp
7852fad6529e5c5df1e9c792e1de2780abb6b5b7a36c903fb9668397c0c562f1  ./cpp/v3_engine.h
6353f3e19b22d7b4692b5f3bf25a7128f24e554101bbc9a8cd809120ca6a0c41  ./cpp/v3_ledger.h
09c18da76cd89b973ebdf3f8c3f49118a19862d800798d22c0d619805f5c30ad  ./cpp/v3_observer.h
b7707f56b54465dfe6fb7b6536c4bb2b8ebf3d6e474944b12f77dfeb8ff77758  ./cpp/v3_score.h
19e0a0bd0e47949025ead4c7d7df0a521980454f010ec0b0d7a2176e64b701a7  ./cpp/v3_start.h
1841122ef2ad6d963b1e0f1d622e1bc154f23fd9e5d347e2b7e02890334d2e15  ./cpp/v3_util.h
aa4212f886265ea5055065ed385117ce1101c1406fc0a1d5e33973591ce2ce3d  ./smoke/run.sh
8af6399a8af44dcda2c5cff1ec8567f66b50332cdbe29c3e450dc11ef20ff668  ./smoke/smoke10_rules.R
14499c4e61c2bbfb5776e5620b7dd396528b5de88b096bcb31999bb2b2e148d6  ./smoke/smoke11_calfit.R
ba21d27ec84ade363a9deb86ebbb983758b120cce28f5a2fc74e866cb7cf60f4  ./smoke/smoke12_e2e500.R
068c8bd5276737a26bb42474cd795517f7315a4346fbe1c50b0083e6a0865645  ./smoke/smoke13_triggers.R
5a790799b6ebfd86d0ce624b9a8a8e33d47bdfd98b1ea8fa5cd0ab31c6178fe9  ./smoke/smoke14_concurrent.sh
6bd5180cee4edac0acc7c21a268009820e982c144842cf91c11db434421a4f33  ./smoke/smoke15_review.R
175c1a4eae6c70b1f054229b7e61c94ccf2d98ae7e40bd41e08aeebb392679f3  ./smoke/smoke16_largep.R
82e33cb7eea5367bd7d88800a5b8a9bd39cd51b3709773d84b6d5ee6fd3242fd  ./smoke/smoke17_round3.R
007cb145b3c157fa2efff2e450699df68ec4f74c02172352e00651467ffe3bce  ./smoke/smoke1_exact.R
f254ee2b6087fa7a8457a66c079718cf9f561a33d5b063c7d11dbe974b840620  ./smoke/smoke2_fit.R
cbea4e1f42a360d86426d3e4f5b4a29db0aa1514671ad8edb5231035b3e27b4a  ./smoke/smoke3_status.R
896d9f245d3bd678e38b47649c1c15297f109af049ffad4d51da8441c3050363  ./smoke/smoke5_trace.R
ba5695be97790ca521901a9b553ab7cb38efe719cfe58fd9d2854b728376264d  ./smoke/smoke6_timing.R
f6f659c0d7ed3e5cbd5ffea40cdcfa3d9750ff25cb73f0e442e0d83ee5646565  ./smoke/smoke7_local.R
a4b881781c78ae31126411365d38aad5984027ccff0bcd40dc9935ce981e9bd6  ./smoke/smoke8_fixround.R
0dbe6ca6d6c8840a39a3a38da0b7c97c3d7a9b4759dc109a6facdd6f77e60de2  ./smoke/smoke9_regress.R
02a701feae3c5173625fc68445868218c124adbcb95157175cd79795b4e43b9d  ./smoke/smoke_common.R
48a1bb4ea6867481ee78fde3e9b33a8a7ec767df73b020dc8e1e22e7aa6a1054  ./v3_calib.R
f4716866619254b6153cbf4ade24f4d89cb69e9c784b0782d9db7c3658debb4e  ./v3_exact.R
aebc87bc0a6c52d5f9de97fdfb99f6e885302739053df3212136fb37ce9e91e8  ./v3_fit.R
c6ff61081b8ba5c8b88e719fd08cf2e5b6c790e1051cb76da34ae2ed80a08934  ./v3_observer.R
efd23b2bef3c5eada3d486e3d93d6d93037f62217e9ced6630b78a4f8aa6ee66  ./v3_preprocess.R
33916601a8cde838914c9352122fca6465a3884015d46496b82e041706dff1a5  ./v3.R
7518306dab4a2a55fa888ded8fff5105939bde2a9852c1f2f6ce119c00fad207  ./v3_run.R
1df48c2639c8768566cacaefbd44d56fdf9703769324d35ae7e2f2567c4c646a  ./v3_setup.R
```
