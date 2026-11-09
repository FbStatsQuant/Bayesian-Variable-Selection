# Lemma ST — staying at S₀ under π-invariant kernels

Status: PROVED (by this seat, unchecked). v1, 2026-11-09. Statement: STATEMENT.md v2 §2 "Lemma ST".

Setting: fixed data, φ = 1, the labelled elementary kernels of T12 §1 (`Docs/Theory/proofs/T12_T8_frozen_run_identities/
STATEMENT.md:28-34`): Gibbs G_j (j ∈ [p]), uniform swap U, B copies of the neighbour swap N, independence I. KERNEL: the
coded steps realise these kernels (W1-N1 Lemma B; N9) and each is π-invariant (in fact π-reversible) at φ = 1 (T12
"invariance", `PROOF_v6.tex:54-81`, as re-stated at `W1-N1/lemmas/L2_post_terminal.md:18-19`). S₀ ∈ Ω, π(S₀) > 0,
o₁ = π(Ω∖S₀)/π(S₀).

## (ST-a) Any π-invariant kernel leaves S₀ with probability at most o₁

Let K be a Markov kernel on the finite set Ω with πK = π. Evaluating at S₀:
π(S₀) = Σ_S π(S)K(S, S₀) = π(S₀)K(S₀, S₀) + Σ_{S≠S₀} π(S)K(S, S₀).
Hence π(S₀)·K(S₀, Ω∖S₀) = π(S₀)(1 − K(S₀, S₀)) = Σ_{S≠S₀} π(S)K(S, S₀) ≤ Σ_{S≠S₀} π(S) = π(Ω∖S₀), i.e.
K(S₀, Ω∖S₀) ≤ o₁. ∎

## (ST-b) The Gibbs family

T12 §1: at S, G_j moves to S⁺ = S ∪ {j} with probability o_j(S) and to S⁻ = S ∖ {j} otherwise, where o_j(S) =
γ₁(S⁺)/(γ₁(S⁺) + γ₁(S⁻)) if |S⁺| ≤ K and o_j(S) = 0 otherwise. At S = S₀:
- j ∈ S₀: S⁺ = S₀, so G_j leaves S₀ iff it moves to S₀ ∖ {j}, with probability 1 − o_j(S₀) = |o_j(S₀) − 1{j ∈ S₀}|; and
  1 − o_j(S₀) = π(S₀∖j)/(π(S₀) + π(S₀∖j)) ≤ π(S₀∖j)/π(S₀) (|S₀| ≤ K so S⁺ = S₀ ∈ Ω).
- j ∉ S₀: S⁻ = S₀, so G_j leaves iff it moves to S₀ ∪ {j}, with probability o_j(S₀) = |o_j(S₀) − 1{j ∈ S₀}|; if
  |S₀| = K this is 0; otherwise o_j(S₀) = π(S₀∪j)/(π(S₀) + π(S₀∪j)) ≤ π(S₀∪j)/π(S₀).
(γ₁ ∝ π on Ω.) So K_{G_j}(S₀, Ω∖S₀) = |o_j(S₀) − 1{j ∈ S₀}| ≤ π(S₀ ⊕ j)/π(S₀) (with π(S₀ ⊕ j) := 0 when S₀ ⊕ j ∉ Ω).
The models S₀ ⊕ j, j ∈ [p], are pairwise distinct and different from S₀, so
Σ_j K_{G_j}(S₀, Ω∖S₀) ≤ Σ_j π(S₀ ⊕ j)/π(S₀) ≤ π(Ω∖S₀)/π(S₀) = o₁. In particular κ₀ := max_j |o_j(S₀) − 1{j ∈ S₀}| ≤ o₁
(and even Σ_j |o_j(S₀) − 1{j ∈ S₀}| ≤ o₁). ∎

## (ST-c) One round

Let a particle enter a round at φ = 1 in state X_{[0]} = S₀; the order σ (a bijection from positions {1..m} to the m labels,
m = p + B + 2) has any law, independent of the entering state; given σ, the within-round path X_{[0]}, …, X_{[m]} is a
Markov chain with kernels K_{σ(1)}, …, K_{σ(m)} (T12 (R3), `STATEMENT.md:44`; W1-N1 Lemma B (B-b)). Let
E := {∃k ≤ m : X_{[k]} ≠ S₀}. On E let k* be the first such k; then X_{[k*−1]} = S₀. So
P(E | σ) = Σ_{k=1}^{m} P(X_{[0]} = … = X_{[k−1]} = S₀, X_{[k]} ≠ S₀ | σ) ≤ Σ_{k=1}^{m} K_{σ(k)}(S₀, Ω∖S₀) =
Σ_ℓ K_ℓ(S₀, Ω∖S₀) =: λ₀,
the last equality because σ is a bijection, so each label occurs exactly once. Taking expectation over σ, P(E) ≤ λ₀.
Bound λ₀: the p Gibbs labels contribute ≤ o₁ (ST-b); U, I and each of the B copies of N contribute ≤ o₁ each (ST-a, each
is π-invariant at φ = 1). So λ₀ ≤ (B + 3)o₁, and B = min(⌊√n⌋, ⌊√p⌋, 16) ≤ 16 (CC7) gives λ₀ ≤ 19·o₁. ∎

Remarks. (1) No reversibility is needed, only πK = π for each label. (2) The bound is pathwise in the order and holds for
every round at φ = 1, in particular the measured rounds, whatever happened before (the conditional law of the path given
everything before the round is as stated; Lemma B (B-b)). (3) Equality in ST-b is what makes κ₀ the *exact* RB error of a
particle sitting at S₀: its recorded value at G_j is o_j(S₀).

## Numerical falsification

`numerics/RESULTS_v1.txt` §1: exact kernel matrices built from T12 §1 for three targets (incl. cap K = 2 and B = 2):
Σ_j |o_j(S₀) − 1{j ∈ S₀}| equals the Gibbs leave-sum to machine precision and is ≤ o₁; every non-Gibbs label leaves with
probability ≤ o₁; λ₀ ≤ (B + 3)o₁; the simulated mean leave fraction E[Λ] is ≤ λ₀. Invariance errors ≤ 1.1e-16.
