# Lemma CC — code facts used by W3-SAMP (code check)

Status: CODE-CHECKED (lead; re-checked against the code by SL1, LC1, SW1 and both council seats; council C1 PASSED round 1 (gpt-6-astra 9.1, Claude Opus 5.5 8.8; all six gates PASS on both seats)). History: v2, 2026-11-09 (SL1 item 5).

Code of record: the production core on main, `Scripts/SMC_BVS/core/` (= commit 4676af6: `git diff --stat 4676af6 HEAD --
Scripts/SMC_BVS/core` is empty). Paths below are relative to that folder. Line numbers are those of the working tree on
2026-11-09 (checked by `reviews/CITECHECK.txt` before the council).

**Relation to the N1 code of record.** W1-N1 used the frozen v2.2.1 core
(`Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`). `diff --strip-trailing-cr` of the two
`cpp/v3_engine.h` files shows only three differences: (1) main has **no plain-PIP accumulator** (`pip_plain`,
`plain_acc`, `plain_round` removed); (2) `local_search` takes a `phase` argument (LS0); (3) comments. The elementary steps,
the round, resampling and `draw_start` are byte-identical up to line shifts; `run_island_s` differs only by the removed
plain-PIP accumulator writes, with no change to its statistical transitions, weights or evidence increments. `cpp/v3_ledger.h` differs only
by the added phase `PH_LS0` and the removed registry hook. Other headers (SW1 #12; `diff --strip-trailing-cr` against the v2.2.1 tree, 2026-11-09): `cpp/v3_score.h`,
`cpp/v3_util.h`, `cpp/v3_blocks.h`, `cpp/v3_calib.h` identical; `cpp/v3_start.h` identical up to and including `draw_pi0`
(the text before `draw_pi0` and the function itself have equal SHA-256), its differences (from v2.2.1 line 181 on) being the
start-mode / tie-aware DP used only by LS0; `cpp/v3_runtime.h` differs in 4 lines of `local_event` (event labelling for
LS0). So every island-reachable sampler, table, scoring and start-draw function is unchanged, and N1's code bridge (W1-N1
`lemmas/L1_bridge.md`) applies to main's island verbatim, **except** for its sentence identifying `pip_plain`; on main the only coded PIP is the
Rao–Blackwell PIP.

## CC1 — every π₀ draw is scored and reaches the ledger before its accept decision

- Initial draws: `cpp/v3_engine.h:286-292` — for each of the N particles, `draw_start(S)` (`:289`), `set_model`, then
  `eval(P[i], ME_INIT)` (`:291`) with the default `emit = true`.
- Independence proposals: `step_indep` (`cpp/v3_engine.h:182-192`) draws S ~ π₀ (`:184`), scores it with
  `eval(tmpQ, ME_INDEP)` (`:186`, emit = true), and only then draws the accept uniform (`:189`) and accepts or not
  (`:190-191`). A rejected proposal is therefore scored and emitted.
- `draw_start` is `draw_pi0(st, *vs, S)` (`cpp/v3_engine.h:108`; `cpp/v3_start.h:158-176`): it consumes a
  state-independent sequence of fresh uniforms of the island's stream (sizes, block sizes, submodels), a number that
  depends only on the draw itself.
- Counts: one round = the m = p + B + 2 labels in a random order (`cpp/v3_engine.h:195-214`); exactly one label is `I`
  (`:211`), so every particle makes exactly one independence proposal per round. Per island: N_e initial draws; one round
  per bridge stage t = 1..T (`:303-339`, `population_round` at `:331`); L burn-in rounds (`:343-347`); Hm = 4 measured
  rounds (`:351-360`; `measured_rounds = 4L` at `v3_run.R:90`). Total exact π₀ draws per island:
  **D_r = N_e(1 + T + L + 4)**; with `islands = 4L` (`v3_run.R:91`), D = 4·D_r for the final run.
- The final islands run serially, island r on stream 9 + r (`cpp/v3_core.cpp:443-452`).

## CC2 — the reported HPM is the hpm_better-maximum of every model scored in the final run

- `eval` (`cpp/v3_engine.h:89-101`): cache miss ⇒ scorer call, `fresh = true`, cache insert; then, if `emit`,
  `led->event(..., fresh || !cache, ...)` (`:98-100`).
- `Ledger::event` (`cpp/v3_ledger.h:104-113`): if `is_fresh`, `offer_stores` (`:112`) ⇒ `offer_hpm` (`:89-90`), which
  replaces the running best iff `hpm_better(F, S, hpmF, hpmS)` (`:84-88`). `hpm_better` (`cpp/v3_util.h:121-126`) is the
  strict total order: larger F, then smaller size, then lexicographic. F = log ϖ(|S|-model prior) + log m(S)
  (`cpp/v3_engine.h:97`), so e^F ∝ π(S) on Ω and Σ_Ω e^F = Z.
- Non-fresh events are idempotent re-visits: (a) cache hits — the cache is created empty for the final run
  (`cpp/v3_core.cpp:409`) and is owned by it, so a hit means an earlier `eval` of the same model in this run; every
  `eval` with `emit = true` that inserted it also offered it. The only `emit = false` call in the final run is the centre
  of the final local search, `E.local_search(led.hpmS, ...)` with `emit_centre = false` (`cpp/v3_core.cpp:456`;
  `cpp/v3_engine.h:382`), whose centre is the current running best and was therefore already offered. A cache clear
  (`cpp/v3_score.h:284`) only causes a later fresh re-evaluation, hence a repeated (idempotent) offer. (b) `held`
  (`cpp/v3_engine.h:103-105`) re-emits the particle's current state, which entered the particle through an `eval`.
- Other offers: block tables (`cpp/v3_core.cpp:372-386`, `:408`; only |U| ≤ K, `cpp/v3_start.h:92`), inherited
  calibration models (`cpp/v3_core.cpp:418-429`, size checked at `:425`), the final local search and LS0
  (`:456`, `:476`), which use the same `eval`.
- Reporting: on `status == "completed"`, `out$hpm <- led$hpm$model` (`v3_run.R:142`); otherwise the HPM is labelled
  incomplete and no estimates are returned (`v3_run.R:143-149`).
- Hence, on a completed run: **Ŝ = the hpm_better-maximum of 𝓜**, where 𝓜 ⊇ {all models evaluated by the final
  islands} (in particular every π₀ draw of CC1). Since hpm_better ranks by F first, if F(S₀) > F(S) for every S ∈ Ω∖{S₀}
  and S₀ ∈ 𝓜, then Ŝ = S₀ (CC5 gives 𝓜 ⊆ Ω).

## CC3 — the coded PIPs, MPM and evidence

- RB recording: in a measured round, `step_gibbs` (`cpp/v3_engine.h:113-132`) computes o_j at the particle's current
  state — the state immediately before its Gibbs-j step — as o_j = γ₁(S∪j)/(γ₁(S∪j) + γ₁(S∖j)) (`:124-126`, φ = 1), with
  o_j = 0 when j ∉ S and |S| = K (`:116-119`, `oj` stays 0), and adds it to `rb_acc[j]` **before** the Gibbs uniform
  (`:128-129`). `rb_on` is true only in the measured rounds (`:354-356`).
- Island PIP: `res.pip[j] = rb_acc[j] / (N·Hm)` (`:364`), i.e. p̂_r(j) = (4N_e)⁻¹ Σ_{q=1}^{4} Σ_i o_j(Y^i_{q,j}).
- `pip_primary = rowMeans(P)`, P = cbind of the island PIPs (`v3_run.R:159-162`): equal-weight mean over the 4 islands.
- `mpm = orig[pip_primary > 0.5]` (`v3_run.R:163`), strict inequality.
- `log_Z = log((1/R) Σ_r Ẑ_r)` by log-sum-exp (`v3_run.R:154`); `log_Z_r` per island (`:150, 153`); island Ẑ_r as in
  N1 (`cpp/v3_engine.h:299` init, `:317-322` increments).
- **No plain (endpoint) PIP is computed on main** (`grep -n plain` over `cpp/` and `*.R` finds only a comment).

## CC4 — law of the draws (under H-U)

Under H-U (iid ideal U[0,1) uniforms U₁, U₂, … within stream 9 + r), let τ_k be the **number of uniforms already
consumed** when the k-th π₀ draw of island r begins. τ_k is a stopping time of 𝓕_n := σ(U₁, …, U_n) (whether the k-th
draw begins after n uniforms is determined by U₁..U_n). By the strong Markov property of an iid sequence,
(U_{τ_k+1}, U_{τ_k+2}, …) is iid U[0,1) and independent of 𝓕_{τ_k}. The draw is a measurable function of this
continuation (it consumes a number of uniforms determined by the draw itself, `cpp/v3_start.h:158-176`), so with START it
is π₀-distributed and independent of 𝓕_{τ_k}, which contains the previous k − 1 draws. Hence the D_r draws of the
potential island r are iid π₀ given 𝓒 (D_r is σ(𝓒)-measurable; SI). This is the indexing used by W1-N1
(`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:77-88`). Proof detail: `lemmas/D_theorem.md` §1.

## CC5 — every model the ledger sees lies in Ω

Particles start in Ω (π₀ on Ω); Gibbs adds only if |S| < K (`cpp/v3_engine.h:116`); swaps preserve size
(`:146-180`); proposals are π₀ draws; local search skips additions at size K (`:397`); tables |U| ≤ K
(`cpp/v3_start.h:92`); inherited models checked (`cpp/v3_core.cpp:425`). So 𝓜 ⊆ Ω.

## CC6 — the frozen grid length is at most T_e (production calibration only)

T_e = 4^e·max(1000, ℓ²), ℓ = ⌈log₂(n+p+1)⌉ (`v3_preprocess.R:23, 27, 30`). A constructed grid with more than T_e
intervals is a failure (`cpp/v3_calib.h:94`); in the pilot schedule every non-terminal step advances φ by at least 1/T_e and the
terminal step ends exactly at 1 (`cpp/v3_calib.h:32, 38-44`; the snap is toward 1), so in exact arithmetic it has at most
T_e stages; the tier-1 fallback grid is either a successful construction or the pilot schedule
(`v3_calib.R:122-124`). Hence on 𝒜, **1 ≤ T ≤ 4·max(1000, ⌈log₂(n+p+1)⌉²)**.

## CC7 — B is bounded

B = min(⌊√n⌋, ⌊√p⌋, 16) (`v3_preprocess.R:22`), so the number of neighbour-swap labels per round is ≤ 16.

Note (SL1 item 3, LC1 issue 1): CC6 and the D_r lower bound concern production calibration. `v3_frozen` accepts any
finite strictly increasing grid from 0 to 1 with no T_e ceiling (`v3_run.R:68-82`), and that grid reaches the engine
(`cpp/v3_core.cpp:446`); but `v3_run_settings` always takes N_e and L from `setup$budgets` (`v3_run.R:88-92`), so
`frozen$N`/`frozen$L` are not executed by the public wrapper. Arbitrary (N_e, L) are reachable only through the engine
component `Engine::run_island(r, N_e, grid, L, 4, tier, nullptr)` (`cpp/v3_engine.h:269-273`); `init_states = nullptr` is required for the N_e initial π₀ draws (SW1 #13).
