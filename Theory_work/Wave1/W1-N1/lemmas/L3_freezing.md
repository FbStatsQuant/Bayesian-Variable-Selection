# Lemma F (conditioning on the frozen calibration, with calibration-dependent bounded h)

Status: PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08. Inherits the premise statuses START/KERNEL (N9: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT) and T12 (PROVED-LOCKED). v3. Uses the T12 freezing lemma (PROVED-LOCKED,
`Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:157-162`).

## Setting

Fixed data. 𝓒 is a random element of a measurable space (E, 𝓔) with 𝒜 ∈ σ(𝓒) the success event (CAL: 𝓒 is a function of
streams 0–9). For a fixed index r ≥ 1, U_r := final stream 9 + r, a random element of the sequence space
(Υ, 𝓤) = ([0,1)^ℕ, Borel), iid U[0,1) coordinates (H-U), independent of streams 0–9 and hence of 𝓒 (premise SI).
R′ is σ(𝓒)-measurable. Φ is the statistical record of Lemma B, extended by the dummy record o† off the success set, so it is
defined and jointly measurable on all of E × Υ (MEAS, Lemma B (B-d)). On 𝒜 ∩ {r ≤ R′}, island r's statistical record is
O_r = Φ(𝓒, U_r). **Localisation convention.** Island-r quantities (Ẑ_r, the endpoints S_{rqi}) are defined on
E₀ := 𝒜 ∩ {r ≤ R′} ∈ σ(𝓒); every identity about them is stated in the localised form E[1_{E₀}Y | 𝓒] = 1_{E₀}ψ(𝓒), with Y
any extension (its value off E₀ is irrelevant, since 1_{E₀}Y is then defined globally); "a.s. on E₀" means this form.
h : Ω × E → ℝ jointly measurable with |h| ≤ B_h (deterministic). For a record o, write Ẑ(o) for its evidence and
η_q(o)(f) for the empirical measure of its q-th measured population.

## Statement

For every q ∈ {1, …, 4}, almost surely,
  E[1_{E₀} Ẑ_r · η_{rq}(h(·; 𝓒)) | 𝓒] = 1_{E₀} ψ_q(𝓒), where ψ_q(c) := E[Ẑ(Φ(c, U)) · η_q(Φ(c, U))(h(·; c))] for c ∈ A₀
  (U an iid U[0,1) sequence), and ψ_q(c) := 0 otherwise.

## Proof

Write E₀ = {𝓒 ∈ A₀} with A₀ ∈ 𝓔 (possible since E₀ ∈ σ(𝓒)); take A₀ := A_s ∩ {c : R′(c) ≥ r} ∩ A_𝒜 with A_𝒜 ∈ 𝓔 a set such that 𝒜 = {𝓒 ∈ A_𝒜} (success set A_s as in Lemma B). Define
g : E × Υ → ℝ piecewise: g(c, u) := Ẑ(Φ(c, u)) · η_q(Φ(c, u))(h(·; c)) for c ∈ A₀, and g(c, u) := 0 for c ∉ A₀ (so the
dummy record o† is never evaluated).
*Measurability.* (c, u) ↦ Φ(c, u) is jointly measurable; Ẑ and the q-th population are measurable coordinates of the
record; η_q(o)(h(·; c)) = (1/N_e)Σ_i h(S_i(o); c) is a finite sum of compositions of the jointly measurable h with
measurable maps (N_e is a measurable integer coordinate of c, so the sum is measurable cell by cell on the countable
partition {N_e(c) = N}). Hence g is 𝓔 ⊗ 𝓤-measurable.
*Boundedness.* For c ∈ A₀ with grid (φ_t), every factor (1/N)Σ_i e^{Δ_t d(·)} lies in [e^{Δ_t min_Ω d}, e^{Δ_t max_Ω d}] and
Σ_t Δ_t = 1, so Ẑ ∈ [Z_0 e^{min_Ω d}, Z_0 e^{max_Ω d}] with Z_0 = m(∅)Z̄₀ — a bound depending only on the fixed data, not on c
(as in T12 PROOF_v6.tex:172). With |h| ≤ B_h, |g| ≤ B_h Z_0 e^{max_Ω d} < ∞ uniformly in (c, u).
By the T12 freezing lemma (bounded measurable g; 𝓒 independent of U_r), E[g(𝓒, U_r) | 𝓒] = ḡ(𝓒) a.s. with
ḡ(c) = E[g(c, U)] = ψ_q(c) (zero off A₀). Since g(𝓒, U_r) = 1_{E₀} Ẑ_r η_{rq}(h(·; 𝓒)) everywhere (both sides vanish off E₀;
on E₀, O_r = Φ(𝓒, U_r)), E[1_{E₀} Ẑ_r η_{rq}(h(·; 𝓒)) | 𝓒] = ψ_q(𝓒) = 1_{E₀}ψ_q(𝓒) a.s. ∎

Remark (why the bound is needed). Without a deterministic bound on h over c, g need not be integrable and the
conditional expectation needs a separate convention (SL1 item 1). Only island r's stream enters; no independence between
islands is used (premise SI, weaker than IND-T).

## Numerical falsification

Not separately falsifiable beyond Lemma B/P (measure-theoretic step). The numerics fix c (a production grid per design) and
draw fresh final streams, which is the right-hand side ψ_q(c).
