# Lemma P (post-terminal identity for the frozen run, fixed c)

Status: the statement is T12 clause (i.b) (with (i.a)), **PROVED-LOCKED** (card TH01 status row "T12, T31(i): PROVED-LOCKED";
`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md:59-60`, proof `PROOF_v6.tex:115-131`). The self-contained
proof below is a re-derivation for the reviewer's convenience; the dependency of N1 is on the locked T12 text.
v2, 2026-11-08 (v1 → v2: numerical paragraph reconciled with RESULTS.md, LC1 issues 5–6).

## Setting

T12's frozen island I(c) (T12 STATEMENT §2) for fixed admissible data and fixed parameters c: grid
0 = φ₀ < … < φ_T = 1 (T ≥ 1), N ≥ 1 particles, stage-0 flag unset, then any fixed finite number of rounds at φ = 1.
Ω finite; γ_φ = γ₀e^{φd} > 0; q_φ = γ_φ/Z̄_φ; G_t = e^{(φ_t − φ_{t−1})d}; Z_t := m(∅)Z̄_{φ_t}, so Z_0 = m(∅)Z̄₀ and Z_T = Z
(T12 Lemma "bridge", PROOF_v6.tex:42-52). Ẑ_0 := Z_0, Ẑ_t := Ẑ_{t−1}·(1/N)Σ_i G_t(X^{(t−1),i}); Ẑ := Ẑ_T.
q̂_t := (1/N)Σ_i δ_{X^{(t),i}} (population after the stage-t round); q̂^{(s)} the population after the s-th post-terminal
round, q̂^{(0)} := q̂_T. Randomness model (R1)–(R3) of T12 (for the coded island: Lemma B (B-b)).

Ingredients (all proved in T12 PROOF_v6 §1–§2, re-stated):
- (bridge) Z_{t−1} q_{t−1}(G_t f) = Z_t q_t(f) for every f : Ω → ℝ (`:42-52`).
- (invariance) each elementary step kernel K_e is q_φ-reversible, hence q_φ K_e = q_φ, hence the round kernel
  K_φ = (1/m!)Σ_σ K_{σ(1)}⋯K_{σ(m)} satisfies q_φ K_φ = q_φ (`:54-81`; N9 rows 1–6 for the coded steps).
- (resampling) under (R2), E[(1/N)Σ_l w^l · (1/N)Σ_i f(X^{A^i}) | 𝓕] = (1/N)Σ_k G(X^k) f(X^k) (`:100-106`).
- (round) under (R3), E[f(X^i_{[m]}) | 𝓗] = (K_φ f)(X̃^i) for a particle entering a round at X̃^i (`:108-113`, κ ≡ m).

## Statement

For every f : Ω → ℝ: (P-a) E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f) for t = 0, …, T; (P-b) E_c[Ẑ q̂^{(s)}(f)] = Z π(f) for every
s ≥ 0. In particular, with M = 4 measured rounds after L′ = L burn-in rounds, E_c[Ẑ q̂^{(L+q)}(f)] = Zπ(f), q = 1..4.

## Proof

(P-a), t = 0: Ẑ_0 = Z_0 is deterministic and X^{(0),i} = X_0^i are iid π₀ = q₀ by (R1) (flag unset), so
E[Ẑ_0 q̂_0(f)] = Z_0 q_0(f).

t − 1 → t: let 𝓕 be everything before the stage-t resampling; Ẑ_{t−1} and the population X^{(t−1)} are 𝓕-measurable. Let
Y^i = X^{(t−1),A^i} be the resampled particles and 𝓗 ⊇ 𝓕 everything before the stage-t round. By (round),
E[q̂_t(f) | 𝓗] = (1/N)Σ_i (K_{φ_t} f)(Y^i). Ẑ_t = Ẑ_{t−1}(1/N)Σ_l w^l is 𝓗-measurable, so
E[Ẑ_t q̂_t(f) | 𝓕] = Ẑ_{t−1} E[(1/N)Σ_l w^l (1/N)Σ_i (K_{φ_t}f)(Y^i) | 𝓕] = Ẑ_{t−1} (1/N)Σ_k G_t(X^{(t−1),k})(K_{φ_t}f)(X^{(t−1),k})
by (resampling) with G = G_t and the function K_{φ_t}f. This is Ẑ_{t−1} q̂_{t−1}(G_t·K_{φ_t}f). Taking expectations and using
the induction hypothesis with the function G_t·K_{φ_t}f: E[Ẑ_t q̂_t(f)] = Z_{t−1}q_{t−1}(G_t K_{φ_t}f) = Z_t q_t(K_{φ_t}f) (bridge)
= Z_t q_t(f) (invariance at φ_t).

(P-b): induction on s. s = 0 is (P-a) at t = T, since q_T = q_{φ_T} = q_{φ=1} = π (stage index T, temperature 1) and Z_T = Z. Step: the (s)-th post-terminal operation
is a round at φ = 1 with no reweighting, so Ẑ is unchanged and 𝓗_s-measurable (𝓗_s = everything before that round); by
(round), E[Ẑ q̂^{(s)}(f) | 𝓗_s] = Ẑ q̂^{(s−1)}(K_1 f); by the induction hypothesis with the function K_1 f,
E[Ẑ q̂^{(s)}(f)] = Zπ(K_1 f) = Zπ(f) (invariance at φ = 1). ∎

Remark. Only full rounds occur between the measured endpoints, so κ ≡ m suffices; the within-round prefix identity
(T12 (i.c)), which the Rao–Blackwellised record needs, is not used. No stationarity of the particles is claimed: the
identity is for the evidence-weighted population (Ẑ inside the expectation).

## Numerical falsification (numerics/RESULTS.md §2–§4)

Exact floating-point enumeration on production-extracted kernels, 10 designs (d0–d9), N = 1 on all designs and N = 2 on
the six designs with |Ω| ≤ 130 (d2, d3, d5, d6, d7, d9), three grids (production, {0,1}, {0,½,1}) plus L = 0 stress cases,
every basis indicator 1{S = s} and every measured round q separately: worst residual 9.3e-15 (RESULTS §3; tolerance 1e-10).
Round kernels: row sums, q_φ-invariance and (|Ω| ≤ 130) detailed balance to ≤ 5.6e-16 (RESULTS §2). Negative controls
NC1 (terminal rounds with the φ = ½ kernel) and NC2 (bridge stopped at φ_{T−1}, then the same rounds at φ = 1) give
discrepancies from 3.2e-3 to 7.7e-1 (RESULTS §4).
