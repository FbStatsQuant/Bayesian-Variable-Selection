# W1 · Lemma ISL — PROOF v1.1 (line check of `W1-N1:B` (B-0), (B-b) control flow, (B-d) at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Reuse: T1 GW (`Theory_work/Wave3/W3-AUDIT/track_A/T1_GW/STATEMENT.md`: guard bodies draw no uniform, the potential run's
Booleans are FALSE), T5 CAL-C (`Theory_work/Wave3/W3-AUDIT/track_A/T5_CAL/STATEMENT.md`: final-run settings are functions
of 𝓒°; streams), T6 START-X (S) (`Theory_work/Wave3/W3-AUDIT/track_A/T6_START/STATEMENT.md:30-31`: a `draw_pi0` call
consumes a number of uniforms that is a function of the returned draw), T7 KER (`Theory_work/Wave3/W3-AUDIT/track_A/T7_KER/STATEMENT.md`:
(KER-c) order first; (KER-d) inputs fixed before the islands), FR (FR-a)
(`Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/PROOF.md`, Part 1: the island's control flow at the pin).

## Step 1 — the island's program at the pin
Island r is run serially with its own `RngSource` (`cpp/v3_core.cpp:443-446`): `rng.g.seed_stream(seed, 9 + r)` and
`E.vs = &rng`, so every `vs->u(·)` call of the island reads the next value of stream 9 + r; `RngSource::u` returns
`g.uniform()` and ignores its label (`cpp/v3_engine.h:20-22`). The island is `run_island` → `run_island_s` with a fixed
grid (`cpp/v3_engine.h:269-273`; `sch.adaptive` false, T = grid size − 1, `cpp/v3_engine.h:280`), executing:
1. N_e initial draws: `draw_start` = `draw_pi0` (`init_states` = nullptr; `cpp/v3_engine.h:286-292`, `cpp/v3_engine.h:108`), each followed by `eval`;
2. for t = 1..T (`cpp/v3_engine.h:303-308`): weights lw_i = Δ_t d(S_i), increment, log Ẑ update (`cpp/v3_engine.h:316-322`),
   `resample(lw)` (`cpp/v3_engine.h:324`), copy, one `population_round` at φ_t (`cpp/v3_engine.h:331`), then the guard
   check (`cpp/v3_engine.h:335`), whose Boolean is FALSE in the potential run (T1);
3. L rounds at φ = 1 (`cpp/v3_engine.h:343-347`); `rb_acc` reset (`cpp/v3_engine.h:350`); Hm = 4 measured rounds at
   φ = 1 (`cpp/v3_engine.h:351-360`; Hm = `measured_rounds` = `4L`, the R integer literal 4, `v3_run.R:90`).
A `population_round` runs `one_round` for i = 1..N_e in turn (`cpp/v3_engine.h:215-218`); `one_round` first draws the
order (`draw_order`, `cpp/v3_engine.h:195-200, 203`), then applies the m labels in that order (`cpp/v3_engine.h:205-211`).

## Step 2 — (ISL-0)
The uniform-reading sites of the island are exactly: `draw_pi0` (`cpp/v3_start.h:160, 164, 170`), `step_gibbs`
(`cpp/v3_engine.h:129`), `step_uswap` (`cpp/v3_engine.h:150, 151, 156`), `step_nswap` (`cpp/v3_engine.h:167, 171, 177`),
`step_indep` (its `draw_start`, `cpp/v3_engine.h:184`, and `cpp/v3_engine.h:189`), `draw_order` (`cpp/v3_engine.h:199`) and `resample`
(`cpp/v3_engine.h:250`); `eval`, `held`, the ledger and the cache read none (`cpp/v3_engine.h:89-105`), and the guard
bodies draw no uniform (T1 GW-i). Each transition, accept decision and weight is computed from the current state, c (φ,
N_e) and the data through `eval` (log m, lg0, d: `cpp/v3_engine.h:89-99`), whose score is exact whatever the cache history:
`ScoreCache::find` hits only when the hash and the full model agree (`cpp/v3_score.h:271-281`), `insert` stores the
scorer's value (`cpp/v3_score.h:282-293`), a capacity clear (`cpp/v3_score.h:284`) only causes later misses, and the scorer
is a deterministic function of S under EX-A; the neighbour lists, B and `st` are fixed before the islands (T7
KER-d). The clock reads (`cpp/v3_engine.h:284, 298, 304, 335, 336, 341, 348, 361`) set only `seconds_*` and the guard
argument. Engine
members shared across steps and islands (one `Engine`, `cpp/v3_core.cpp:410`) carry no information into a transition:
`tmpQ` is written before it is read in each step (`step_gibbs` reads it only when `include != in`, which needs the branch
`in || add_ok` that wrote it, `cpp/v3_engine.h:118-131`; the swaps and `step_indep` write it first, `cpp/v3_engine.h:152, 172, 185`);
`rb_acc` is written only and reset before the measured rounds; `ms`, `ev` are bookkeeping; `scratch` is workspace of
`st.comp`. The `resample` guard u = 0 ↦ the smallest positive double (`cpp/v3_engine.h:251`) changes the map only on
{u_i = 0}, a null set under H-U. Hence Φ̃(c, u) is a function of (c, u) (data fixed). This is `W1-N1:B` (B-0)
(`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:65-78`) at the pin; FR Part 1 lists the same facts.

## Step 3 — (ISL-st)
*Order and counts decided by the past.* By Step 1 the program is a fixed nesting of loops whose bounds are c's integers
(N_e, T, L, Hm = 4, m = p + B + 2) and whose bodies read uniforms only through `vs->u`. Inside an operation, the number
of uniforms read is decided by values already read: `draw_pi0` reads 1 (size) + one per iteration of the remaining-size
loop (stops when r = 0 or after J blocks) + one per positive-size block, ≤ 1 + 2J, a function of the draw (T6 (S));
`step_gibbs` exactly 1; `step_uswap` 0 (self-loop at |S| ∈ {0, p}, `cpp/v3_engine.h:148`) or 3; `step_nswap` 0 (|S| = 0),
1 (empty candidate set, `cpp/v3_engine.h:170`) or 3; `step_indep` (≤ 1 + 2J) + 1; `draw_order` m − 1; `resample` N_e.
The branch conditions (|S|, candidate set, the drawn values) are functions of the state, hence of (c, data, uniforms
already read) by Step 2. So for each operation O, {τ_O = k} is determined by (u₁, …, u_k): τ_O is an (𝓕_k)-stopping time.
*Bounds.* A particle-round reads ≤ (m − 1) + p·1 + 3 + B·3 + (1 + 2J + 1) = κ_max; summing over the program,
τ_O ≤ κ(c) = N_e(1 + 2J) + T·N_e + (T + L + 4)·N_e·κ_max < ∞.
*Fresh uniforms.* Under H-U, u is i.i.d. U[0, 1); for a bounded stopping time τ, (u_{τ+1}, u_{τ+2}, …) is i.i.d.
U[0, 1) and independent of 𝓕_τ (strong Markov property of an i.i.d. sequence: for each k, on {τ = k} the shifted
sequence is (u_{k+1}, …), independent of 𝓕_k; sum over the finitely many k). Every record variable produced before O is a
function of (c, u₁, …, u_τ) (Step 2), hence 𝓕_τ-measurable.
*Draw count.* Each round has exactly one `I` label (`cpp/v3_engine.h:211`), so the π₀ draws are the N_e initial draws and
one per particle per round over T + L + 4 rounds: D_r(c) = N_e(1 + T + L + 4) (as `W3-SAMP:CC` CC1).
This is the control-flow clause of `W1-N1:B` (B-b) (`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:78-86`) at the pin, with
the same κ_max. ∎(ISL-st)

## Step 4 — (ISL-d)
Fix a cell 𝒞 = {c ∈ A_s : T(c) = T, N_e(c) = N, L(c) = L, tier(c) = e} (countably many; A_s ∖ ∪𝒞 = ∅). On 𝒞, by Steps 2–3,
Φ̃(c, u) is computed by a finite program that reads at most κ := κ(c) (constant on 𝒞) uniforms and whose branches are
comparisons of finitely many Borel functions of (grid values, data constants, u₁, …, u_κ): `floor`, products,
`cat_draw_gt` thresholds, `u < o_j`, `u < α` with α = min(1, exp(·)), the resampling comparisons W_k < u, and the
grid-dependent weights Δ_t d(S). Under EX-A these are exact real functions, so Φ̃ on 𝒞 × Υ is a Borel function of
(grid, u₁, …, u_κ), and (c, u) ↦ (grid(c), u₁, …, u_κ) is 𝓔 ⊗ 𝓤-measurable. With Φ̃ ≡ o† off A_s, Φ̃ is
𝓔 ⊗ 𝓤-measurable on the countable measurable partition {𝒞} ∪ {A_s^c}. Its values (finitely many reals, finite
sequences of subsets of [p] and permutations of [m]) lie in a countable disjoint union of Euclidean spaces times finite
sets, a Polish space. The coordinates `W3-SAMP:MR` Step 2 uses are coordinates of Φ (stage-t populations, post-terminal
populations) or a finite case split over the order (Y^i_{q,ℓ} = path of particle i in post-terminal round L + q, the
(T + L + q)-th `population_round` of the island, at position σ_i⁻¹(ℓ) − 1); the D_r(c) draws are coordinates of Φ̃; the
partial evidence Ẑ_t = Z₀∏_{s≤t}(1/N_e)Σ_i e^{Δ_s d(S_i^{(s−1)})} (`cpp/v3_engine.h:299, 316-322`) is a Borel function of
grid(c) and the populations after the stage-(s − 1) rounds (coordinates of Φ), and W_r = Ẑ_r/Z with Z a data constant. This is `W1-N1:B` (B-d)
(`Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:115-122`) at the pin. ∎

## Line-check verdict on the `W1-N1:B` steps
(B-0), the control-flow clause of (B-b) and (B-d) hold at the pin with the line numbers above; the v2.2.1 → pin changes on
the island path (the removed write-only plain-PIP lines; `resample` is unchanged, its u = 0 guard was already in v2.2.1)
do not affect them.
