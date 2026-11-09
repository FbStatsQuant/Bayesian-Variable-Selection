# Part 5 — Posterior concentration (P) and the output composition (C); assembly of Theorem PXN

## 5.1 The cited input T03♯ (fixed-design posterior concentration)

**[T03♯]** (theorem of record TH128; statement and statuses in §0.7.) *Hypotheses.* R1 (fixed-design triangular array, s₀ fixed, p_n ≤ n^A, s₀ ≤ K eventually);
G (ε ~ N(0, σ²I_n), design fixed); R (‖μ‖² ≤ Mn, λ_min(R_{S₀}) ≥ φ₀²); SE_λ(j₀): λ_min(R_{S₀∪J}) ≥ φ₀² for all J ⊆ [p]∖S₀, |J| ≤ j₀ := ⌈(2A+1)s₀⌉ + 1;
SE_w(m♯_n; g₀): λ_min(G_{S₀∪J}) ≥ g₀ > 0 for all |J| ≤ m♯_n; BM-∞: θ*²_min · nφ₀²/(σ² log n) → ∞. *Conclusion (i):* 1 − π(S₀) = O_{P₀}(√(log n/n)).
Here q_k, R_m and m♯_n are as in §2.1 (the definition of TH128), and by Lemma K, m♯_n ≤ k_n = O(log n).

T03♯ is a fixed-design theorem; the passage to the random design (design event ℰ♯_n of §2.2 plus de-randomisation) is the argument of §5.2–§5.3.

## 5.2 Lemma (design de-randomisation)

**Lemma 5.2.** Let 𝒜′_n be X-measurable with P(𝒜′_n) → 1 and Z_n ≥ 0 such that for every deterministic sequence x_n ∈ 𝒜′_n (n ≥ n₀), Z_n = O_P(r_n) under
P(· | X = x_n). Then Z_n = O_P(r_n) unconditionally.

*Proof.* Let f_n(M) := sup_{x∈𝒜′_n} P(Z_n > Mr_n | X = x). If the conclusion fails there are ε > 0 and n_k ↑ ∞ with f_{n_k}(k) > ε, hence x_{n_k} ∈ 𝒜′_{n_k} with
P(Z_{n_k} > k r_{n_k} | x_{n_k}) > ε/2; complete to a sequence in 𝒜′_n (the sets 𝒜′_n are nonempty eventually since P(𝒜′_n) → 1; choose arbitrary admissible x_n at the
remaining indices). The hypothesis gives M, N with P(Z_n > Mr_n | x_n) < ε/2 for n ≥ N, contradicting the choice at n_k ≥ N, k ≥ M. So for every ε there are M, N with
f_n(M) ≤ ε for n ≥ N, and P(Z_n > Mr_n) ≤ ε + P(𝒜′_nᶜ). ∎

(Only the individual kernels h_n(x, M) = P_ε(Z_n(x, ε) > Mr_n) are integrated, so measurability of the supremum is not needed.)

## 5.3 Theorem P8♯ — conclusion (P)

**Theorem P8♯.** On LH-iid with 18 ≤ p_n ≤ n^A (A ≥ 1 fixed): δ₁ := 1 − π(S₀) = O_P(√(log n/n)) under the joint law of (X^r, ε). Hence E₀δ₁ → 0 and
P(δ₁ ≥ ½) → 0, i.e. P(π(S₀) > ½) → 1.

*Proof.* **Hypotheses of T03♯ on ℰ♯_n.** Fix a deterministic sequence x_n ∈ ℰ♯_n (n ≥ n₀) and work under P(· | X^r = x_n); since ε ⊥ X^r, this is the fixed-design model
y^r = x_nθ + ε with Gaussian noise: G holds. R1: s₀ fixed, p_n ≤ n^A, s₀ ≤ K by (d) of §2.2. R: by (b) and (a) of §2.2 with T = S₀. SE_λ(j₀): |S₀ ∪ J| ≤ s₀ + j₀ ≤ L_n, so
(a) of §2.2 applies (and to every nonempty subset, as the equivalent form of TH128 requires). SE_w(m♯_n; g₀) with g₀ := φ₀²: |S₀ ∪ J| ≤ s₀ + m♯_n ≤ L_n, so
λ_min(G_{S₀∪J}) = (n−1)λ_min(R̂_{S₀∪J}) ≥ (n−1)φ₀² ≥ φ₀². BM-∞: θ*²_min · nφ₀²/(σ² log n) ≥ b_min · nφ₀²/(σ² log n) → ∞, a deterministic lower bound common to all
sequences. All constants (A, s₀, M, φ₀, g₀, σ²) are fixed and do not depend on the sequence. T03♯(i) gives 1 − π(S₀) = O_P(√(log n/n)) under P(· | X^r = x_n).

**De-randomisation.** Apply Lemma 5.2 with 𝒜′_n := ℰ♯_n, Z_n := δ₁, r_n := √(log n/n): its hypothesis is exactly the previous paragraph for every deterministic sequence in ℰ♯_n;
conditional probabilities given X^r = x are evaluations of the ε-integral at x (ε ⊥ X^r). P(ℰ♯_n) → 1 by Lemma 2.2. Hence δ₁ = O_P(r_n) unconditionally.
δ₁ ∈ [0,1] and δ₁ → 0 in probability, so E₀δ₁ → 0 (bounded convergence) and P(δ₁ ≥ ½) → 0. ∎

(The rate and the de-randomisation argument do not depend on A; A enters j₀, k_n, hence L_n, and the unnamed onset of T03♯.)

## 6 Output: (C)

## 6.1 Deterministic step and Markov

**Lemma 6.1.** If S₀ ∈ 𝒮⁺ and π(S₀) > ½, then F(S₀) > F(S) for every S ≠ S₀ (π(S) < ½ < π(S₀)), so the running-best rule over 𝒮⁺ returns Ŝ⁺ = S₀ with no tie. Hence, for any
run, {Ŝ⁺ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ {S₀ ∉ 𝒮⁺}, and, with 𝒪 intersected on both sides, 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ (𝒪 ∩ {S₀ ∉ 𝒮⁺}). By Markov, P(δ₁ ≥ ½) ≤ 2E₀δ₁ (δ₁ ≥ 0). δ₁ is a function
of the data only, so the bound is unaffected by adjoining the run randomness and the operational variables Ξ; no conditioning on completion and no independence is used.

## 6.2 Closure under (OP) and the exact branch

**Closure.** 𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 of R̄⁺ does not score S₀}.
The first inclusion is (G2) of GUARD (W6 conventions; Lemma RO): on 𝒪 no guard stopped the run (a stopped post hoc LS0 is in U by OP-LS0), so the run performs exactly the R̄⁺
computation and 𝒮⁺ = 𝒮̄⁺. The second holds because R̄⁺ contains its deterministic LS0 with the emitted centre by definition (W6, 48–51 of T38_STATEMENT.md), also when st̄ = schedule_limit.
The theorem is about v3 + LS0 under (OP); the production bridge (merged LS0 with emit_centre = true, replay; registry items OB02(c), OB03, DF16, ENG02) remains an implementation
obligation, not a step of the proof.

**Exact branch (cases).** (a) For n with s₀ ≤ K, on the exact branch the run scores all of Ω (status exact ∈ 𝒪 under EX-A; `CODE/cpp/v3_core.cpp:523-558`), so S₀ ∈ 𝒮̄ and
𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ∩ {exact branch} = ∅; on the SMC branch 𝒮̄⁺ ⊇ 𝒮_LS0. (b) For n with s₀ > K, S₀ ∉ Ω and every feasible LS0 fails to score S₀, so the inclusion into
{LS0 of R̄⁺ does not score S₀} holds trivially; π(S₀) := 0 (zero extension) makes the posterior term trivial. The composition inequality of §6.3 therefore holds for every n with
D_n ≤ P(LS0 of R̄⁺ does not score S₀) (= 1 when s₀ > K); and, for n with s₀ ≤ K only, with the sharper D_n ≤ P(SMC branch, LS0 of R̄⁺ does not score S₀), with no execution of LS0
needed on the exact branch (the requirement of OP-LS0 is then vacuous for the conclusion). On the exact branch Ŝ⁺ is the global HPM, and the posterior term covers it.

## 6.3 Composition — conclusion (C)

**Theorem 6.3.** For every n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, with D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) ≤ P(LS0 of R̄⁺ does not score S₀). For n ≥ n₀ also
P(LS0 of R̄⁺ does not score S₀) ≤ P(𝒯_nᶜ) → 0, so D_n → 0. With (P), P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) = (1 − P(U)) − o(1), i.e.
P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0; hence liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U), and P(𝒪 ∩ {Ŝ⁺ = S₀}) → 1 − u whenever P(U) → u. Recovery with probability → 1
additionally needs P(U) → 0, which is not provided here.

*Proof.* The every-n statements: Lemma 6.1 gives 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ (𝒪 ∩ {S₀ ∉ 𝒮⁺}), and by the closure of §6.2 the second event has probability ≤ D_n ≤ P(LS0 of R̄⁺ does not
score S₀); Markov gives P(δ₁ ≥ ½) ≤ 2E₀δ₁. The n ≥ n₀ statement is Theorem P6′ (§4.6): {LS0 of R̄⁺ does not score S₀} ⊆ 𝒯_nᶜ for n ≥ n₀ (ℓ_n ≥ c − 1 and s₀ ≤ K are among the onset
conditions). The limits follow from P(𝒯_nᶜ) → 0 and E₀δ₁ → 0 (Theorem P8♯). ∎

## 6.4 Proof of Theorem PXN (assembly)

(R), including its explicit constant and exponent, is Theorem R (§2.3).
The independent route (R′) (§2.4) also proves summability and eventual p^{−C};
it supplies a weaker explicit bound and does not replace (R-b). (S) is P3′ and P4 (§3.2, §3.3). (E) is P5 (§3.4). (T) and (K) are Theorem P6′ (§4.6). (P) is Theorem P8♯ (§5.3). (C) is Theorem 6.3.
Every step holds for each fixed A ≥ 1; see Part 6. ∎

**Which premise is discharged where.**

| premise | discharged by | probability statement |
|---|---|---|
| partition recovery | Theorem R (§2.3; W7 Theorem B) or (R′) (§2.4) | explicit, ≤ p^{−C} eventually, summable |
| uniform control of the start mass on the random design | P3′ (Lemma T + Lemma B + Tr-J + Lemma E + T22(i-a)) | explicit moment bound, O_P(√(log n/n)) |
| eligibility of the start mode | P5 | P(S̃₀ = S°) ≥ P(π₀(S°) > ½) → 1 |
| discovery by LS0 | P6′ (Lemma U, Lemma Λ with Tr-J, §4.3, (L), Lemma LS) | → 1; failure ⊆ 𝒜ᶜ ∪ ℰ♯ᶜ ∪ 𝒟_searchᶜ ∪ {Λ-convergence fails} ∪ 𝒵ᶜ ∪ {S̃₀ ≠ S°} |
| π(S₀) → 1 | P8♯ (T03♯ + de-randomisation) | O_P(√(log n/n)) |
| masked regime (start not favourable) | P4 | π₀(S₀) → 0 at rate p^{−c}n^{−c/2} |
| composition | Theorem 6.3 | for every n |
