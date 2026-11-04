# T13 (T10): Restricted ESS and the omitted-mass identity

**Status:** conjectured, not proven. Methodology SMC-BVS v3.0 (2026-10-19), SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c. Read with `00_COMMON.md`.

**Category / rank:** algorithmic validity; **core** (lemma).

## Definitions used
Bridge q_ψ for real ψ; candidate set V (frozen, nonempty); restricted ESS ρ_V(u, v) = Z̄_v(V)²/(Z̄_u(V)Z̄_{2v−u}(V)); a(ψ) := q_ψ(V); for W ⊆ V, a_W(ψ) := q_ψ(W), q^W_ψ = q_ψ(·|W); χ²(q_v‖q_u) = ∫(dq_v/dq_u)²dq_u − 1; 𝓔_grid (00_COMMON §2).

## Assumptions
EX-A; fixed V; COVER(V, ε_C) or COVER(W, ε_C) for the corollaries.

## Precise statement
For nonempty frozen V, u < v, w = 2v − u:
(i) [identity] 1 + χ²(q_v‖q_u) = ρ_V(u,v)⁻¹·a(v)²/(a(u)a(w)).
(ii) [COVER corollary] An accepted interval (ρ_V ≥ 0.9) with a(u), a(w) ≥ 1 − ε_C satisfies 1 + χ²(q_v‖q_u) ≤ 10/(9(1−ε_C)²). COVER supplies this at every grid evaluation point (φ_{t−1}, φ_t, w_t); coverage on [0,1] alone does not supply it when w_t > 1; the largest w_t is not automatically the worst coverage point.
(iii) [restricted working set] For nonempty W ⊆ V: 1 + χ²(q_v^W‖q_u^W) = ρ_V(u,v)⁻¹·(a_V(v)²/a_W(v)²)·(a_W(u)a_W(w))/(a_V(u)a_V(w)); COVER(W, ε_C) gives the same bound as (ii).
(iv) [restricted grid] If ∅ ∉ 𝓜 and calibration never scores 𝓜, then V ∩ 𝓜 = ∅; with the same pilot temperatures and the same V, restricting γ_φ to 𝓜^c leaves the grid construction unchanged.
No assertion derives particle mixing from ESS.

## Dependencies
Builds on: bridge definitions; project L4/L7. Used by: T18, T25, T28, T31, T36.

## Numerical evidence (provisional)
None specific (the identity is algebraic); provisional evidence (Sol check J6) uses it in the reflected-pair product check.

## Proof-route hint (optional)
Substitute Z̄_ψ(V) = a(ψ)Z̄_ψ into the two second-moment identities (project L4, L7; valid for every real ψ, so over-tempered points are covered); (iv): ρ_V depends only on γ_φ restricted to V. Hardest step: none for the identity; establishing coverage for the actual scored set is the substantive obstacle (T25). *When proof.md is run on this file, its lead considers the statement both with and without these hints; the hints never reach the reviewers.*
