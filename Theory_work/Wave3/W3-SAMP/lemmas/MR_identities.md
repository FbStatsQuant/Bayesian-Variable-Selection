# Lemma MR — measured identities given 𝓒 (bridge stages, terminal endpoints, pre-step states)

Status: PROVED-CHECKED (lemma checks LC1/LC2 Codex Sol; mid-point MP1 CONTINUE; sweep SW1 fixed; council C1 PASSED round 1 (gpt-6-astra 9.1, Claude Opus 5.5 8.8; all six gates PASS on both seats); C1 non-blocking edits applied). Text history: v1, 2026-11-09. Statement: STATEMENT.md v3 §2 "Lemma MR".

## Sources used (with statuses, verbatim as in STATEMENT §1)

- T12 (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md`): (i.a) `:59`, (i.b) `:60`, (i.c) `:61`, (ii) `:64`,
  each "for every c" (fixed frozen parameters) and every f : Ω → ℝ; proof `PROOF_v6.tex`; T12 freezing lemma
  `PROOF_v6.tex:157-162`.
- W1-N1 Lemma B (code bridge, `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md`): the coded island with frozen c and an iid
  stream u is a realisation of T12's I(c) (B-a), satisfies (R1)–(R3) (B-b), with the **statistical record** Φ(c, u)
  containing the evidence, the population after the initial draws, after each stage-t resampling and each stage-t round,
  after each burn-in and measured round, and **for each particle and each round, its order and within-round path**
  (`L1_bridge.md:14-20`); jointly measurable (B-d). Lemma B was written for the frozen v2.2.1 core; on main the engine
  differs, **in the island computation**, only by the removed write-only plain-PIP lines; the other differences (the
  local-search `phase` argument, `PH_LS0`, the removed registry hook) are outside the island (`lemmas/CC_code_check.md`
  header; LC1 issue 4); `v3_start.h` is identical through `draw_pi0` and `v3_runtime.h` differs only in LS0 event labels
  (CC header, SW1 #12). Lemma B already lists the plain-PIP lines
  as statistically inert (`L1_bridge.md:29-31`). So Lemma B applies to main verbatim (its `pip_plain` sentence excepted).
- W1-N1 Lemma F (`L3_freezing.md`): the freezing step for terminal endpoints, with the localisation convention and the
  deterministic evidence bound Ẑ ∈ [Z₀e^{min_Ω d}, Z₀e^{max_Ω d}], Z₀ = m(∅)Z̄₀ (`L3_freezing.md:34-36`).

## Statement (repeated)

h : Ω × E → ℝ jointly measurable, sup_{S,c}|h(S; c)| ≤ B_h < ∞ deterministic, evaluated at c = 𝓒. E₀ := 𝒜 ∩ {r ≤ R′}.
Almost surely:
- (MR-a) for each fixed t ≥ 0: E[1_{E₀∩{T≥t}} (Ẑ_{r,t}/Z_t)·η_{r,t}(h(·; 𝓒)) | 𝓒] = 1_{E₀∩{T≥t}} q_t(h(·; 𝓒)), where
  η_{r,t} is the empirical measure of island r's population after the stage-t round (t = 0: initial draws), Ẑ_{r,t} the
  partial evidence and Z_t = m(∅)Z̄_{φ_t}, q_t = q_{φ_t} computed on 𝓒's grid;
- (MR-b) for each fixed s ≥ 0: E[1_{E₀∩{s≤L+4}} W_r·η^{(s)}_r(h(·; 𝓒)) | 𝓒] = 1_{E₀∩{s≤L+4}} π(h(·; 𝓒)), η^{(s)} the
  population after s rounds at φ = 1 following stage T;
- (MR-c) for each q ∈ {1..4} and label ℓ: E[1_{E₀} W_r·(1/N_e)Σ_i h(Y^i_{q,ℓ}; 𝓒) | 𝓒] = 1_{E₀} π(h(·; 𝓒)), Y^i_{q,ℓ}
  particle i's state immediately before its ℓ-step in measured round q; and E[1_{E₀} W_r p̂_r(j) | 𝓒] = 1_{E₀} π(j ∈ S).

## Proof

**Step 1 (fixed c).** Fix c ∈ A₀ (the set of calibration values of L3, `L3_freezing.md:27-29`, whose pullback E₀ = {𝓒 ∈ A₀} ∈ σ(𝓒) is the
localisation event; SW1 #21) and run the island on an
iid stream U. By Lemma B (B-a, B-b) the run is T12's I(c) with N = N_e(c), M = 4, L′ = L(c), flag unset, and satisfies
(R1)–(R3). Put f := h(·; c) : Ω → ℝ (bounded). Then:
- (MR-a) at fixed c is T12 (i.a) for t ≤ T(c): E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f); divide by the constant Z_t > 0.
- (MR-b) is T12 (i.b) with the operation sequence "s rounds at φ = 1" (s ≤ L + 4; the coded terminal operations are
  rounds, Lemma B (B-a)); s = 0 is (i.a) at t = T since q_T = π and Z_T = Z.
- (MR-c) is T12 (i.c) applied to the post-terminal round number L + q with κ_i = κ(σ_i) := σ_i⁻¹(ℓ) − 1, a fixed function
  of particle i's order alone (T12's own example, `STATEMENT.md:61`); X^i_{[κ_i]} is the state immediately before step ℓ,
  which in the code is the state at which `step_gibbs`/`step_*` for label ℓ is entered (`cpp/v3_engine.h:205-212`).
  The RB clause: for ℓ = G_j, f := o_j(·, 1) ∈ [0,1] (data-only), and π(o_j(·, 1)) = π(j ∈ S) because o_j(S, 1) is the
  π-conditional probability of j ∈ S given S ∖ {j} (with value 0 when S ∪ {j} ∉ Ω, where π gives that configuration mass 0);
  averaging over q gives T12 (ii) for p̂_r(j) = (4N_e)⁻¹Σ_{q,i} o_j(Y^i_{q,j}) (CC3).

**Step 2 (measurability).** Each left-side integrand is g(c, U) for a function g on E × Υ defined, for c ∈ A₀ with the
index in range, by g(c, u) := [Ẑ_t(Φ(c, u))/Z_t(c)]·(1/N_e(c))Σ_i h(X^{(t),i}(Φ(c, u)); c) (and the analogues with W and
with Y^i_{q,ℓ}), and g := 0 otherwise. The record Φ(c, u) contains the stage-t population, the post-terminal populations,
and every particle's order and within-round path (`L1_bridge.md:14-20`), so X^{(t),i}, X^{(s),i} and Y^i_{q,ℓ} =
(path of particle i in round L + q) evaluated at position σ_i⁻¹(ℓ) − 1 are measurable coordinates of Φ (a finite case split
over the finitely many orders). Z_t(c) = m(∅)Σ_Ω γ₀e^{φ_t(c)d} is measurable in c (φ_t(c) is a measurable coordinate on
{T(c) ≥ t}). N_e(c), T(c), L(c) are measurable integer coordinates; the sums are measurable cell by cell on the countable
partition they define. With (B-d), g is 𝓔 ⊗ 𝓤-measurable.

**Step 3 (bound).** Ẑ_t ∈ [Z₀e^{φ_t min d}, Z₀e^{φ_t max d}] (each stage factor lies in [e^{Δ_s min d}, e^{Δ_s max d}],
as in `L3_freezing.md:34-36`), and Z_t = m(∅)Σ_Ω γ₀e^{φ_t d} ∈ [Z₀e^{φ_t min d}, Z₀e^{φ_t max d}]. Hence
0 < Ẑ_t/Z_t ≤ e^{max_Ω d − min_Ω d} =: C_d, a constant of the fixed data. So |g| ≤ B_h·C_d uniformly in (c, u).

**Step 4 (freezing).** 𝓒 is independent of U_r (SI) and g is bounded and jointly measurable, so by the T12 freezing lemma
E[g(𝓒, U_r) | 𝓒] = ḡ(𝓒) a.s., ḡ(c) := E[g(c, U)], which by Step 1 equals q_t(h(·; c)) (resp. π(h(·; c))) on the range set
and 0 off it. On E₀ (and the range set) g(𝓒, U_r) equals the island-r integrand, since O_r = Φ(𝓒, U_r) there; off it both
sides vanish. This is the localised form. ∎

**Remark.** W1-N1 Lemma F is the case (MR-b) with s = L + q, q ≥ 1. The only new ingredients are the evaluation of the
augmented record at a stage or a prefix (Step 2) and the stage evidence ratio bound (Step 3). The h class cannot be widened
to "bounded and fixed before stream 10" (SL1 item 2: h ≡ V with V an unused calibration-stream bit independent of 𝓒 breaks
the identity).

## Numerical falsification

`numerics/RESULTS_v1.txt` §1: for three targets (generic, cap active with K = 2, flat) and two grids, MC with 60 000
islands checks E[W] = 1, E[W p̂(j)] = π(j ∈ S) for every j, E[W(1 − A_q)] = δ for q = 0..4, and the stage identities
E[W_t(1 − A^{br}_t)] = 1 − q_t(S₀): max |z| = 2.70 over 76 tests. Unweighted RB means are visibly biased in the "flat"
case (0.008), so the weighting matters.
