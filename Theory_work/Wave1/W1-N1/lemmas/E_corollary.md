# Corollary E (clause M1(e)): islandwise accuracy of every bounded summary

Status: PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08. Inherits the premise statuses START/KERNEL (N9: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT) and T12 (PROVED-LOCKED). Given Theorem N1. v3; history: v2, 2026-11-08 (v1 → v2: localised form; numerics citation; LC1 issues 4–5). Statement: STATEMENT.md v2 §4 (locked).

## Statement

Premises of Theorem N1. Let S₀ ⊆ [p] be fixed, δ₁ := 1 − π(S₀) (π(S₀) := 0 if |S₀| > K), and let h be as in STATEMENT §1
with values in [0, 1], defined on Ω ∪ {S₀} (jointly measurable in (S, c)). Then a.s. on 𝒜 ∩ {r ≤ R′}, with W_r = Ẑ_r/Z,

  E[W_r · |H_r(h) − h(S₀; 𝓒)| | 𝓒] ≤ E[W_r · H_r(1{S ≠ S₀}) | 𝓒] = δ₁ ≤ 2δ₁.

## Proof

Pointwise: for S ∈ Ω and c, h(S; c), h(S₀; c) ∈ [0, 1], so |h(S; c) − h(S₀; c)| ≤ 1 if S ≠ S₀ and = 0 if S = S₀; i.e.
|h(S; c) − h(S₀; c)| ≤ 1{S ≠ S₀}. Averaging over the 4N_e endpoints (triangle inequality),
|H_r(h) − h(S₀; 𝓒)| = |(4N_e)^{-1}Σ_{q,i}(h(S_{rqi}; 𝓒) − h(S₀; 𝓒))| ≤ (4N_e)^{-1}Σ_{q,i} 1{S_{rqi} ≠ S₀} = H_r(1{S ≠ S₀}).
Multiply by 1_{E₀}W_r ≥ 0 (E₀ = 𝒜 ∩ {r ≤ R′}) and take E[· | 𝓒] (monotonicity of conditional expectation; on E₀ every
integrand is bounded by Z₀e^{max d}/Z, as in Lemma F, and the localised integrands are zero off E₀). All statements are in
the localised form of Lemma F. The function
h₀(S) := 1{S ≠ S₀} on Ω (extended by h₀(S₀) := 0) is deterministic with values in [0, 1], so Theorem N1 gives E[W_r H_r(h₀) | 𝓒] = π(h₀) =
Σ_{S∈Ω, S≠S₀} π(S) = 1 − π(S₀) = δ₁ (if S₀ ∉ Ω, h₀ ≡ 1 on Ω and π(h₀) = 1 = δ₁). Finally δ₁ ≤ 2δ₁. ∎

Remarks.
- The card prints the constant 2δ₁ (`THEOREM_LIST_FINAL.md:111`); the plain measured-endpoint average satisfies the sharper
  δ₁ (the NEW-SYNTH form for the plain average, `NBH/ID_REGISTRY.md` TH412 (a)). The factor 2 is not needed.
- No posterior-concentration, design or regime assumption is used; δ₁ carries all the statistics. "Every regime and frozen
  grid" (card) holds.
- The bound is tight: equality for h = 1{S ≠ S₀}.

## Numerical check

Equality part E[W H(1{S ≠ S₀})] = δ₁: exact enumeration (an instance of N1; `numerics/RESULTS.md` §3, h = "1{S!=S0}").
Inequality for the other h ∈ [0,1] in the list: Monte Carlo on the production engine (`numerics/RESULTS.md` §5, column
"max z_E").
