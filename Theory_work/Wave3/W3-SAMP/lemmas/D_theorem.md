# Theorem D — draw discovery

Status: PROVED (by this seat, unchecked). v2, 2026-11-09 (v1 → v2: MAP premise S† = S₀ replaces δ < ½, BT1 §3.1).
Statement: STATEMENT.md v3 §2 "Theorem D".

## §1 The draws are iid π₀ given 𝓒 (D-i)

Fix c ∈ A₀ (success set, index r ≤ R′) and run island r's potential record on an iid U[0,1) stream U₁, U₂, … (H-U).
By CC1 the island makes exactly D_r(c) = N_e(1 + T + L + 4) calls of `draw_start` = `draw_pi0` (N_e initial draws; one
independence proposal per particle per round; T + L + 4 rounds per particle). Order them by execution: k = 1, …, D_r.

Let τ_k be the number of uniforms already consumed when draw k begins, 𝓕_n := σ(U₁..U_n). Whether draw k begins after
exactly n uniforms is a function of U₁..U_n (W1-N1 Lemma B (B-b): the control flow and the number of uniforms each
operation reads are decided by values already read, the data and c), so τ_k is an (𝓕_n)-stopping time, finite since each
operation reads a bounded number of uniforms (`L1_bridge.md:77-88`). By the strong Markov property of iid sequences,
V^{(k)} := (U_{τ_k+1}, U_{τ_k+2}, …) is iid U[0,1) and independent of 𝓕_{τ_k}. Draw k equals Ψ(V^{(k)}) for the measurable
map Ψ realised by `draw_pi0` (it reads 1 + (number of nonzero block sizes considered) + (number of nonempty blocks)
uniforms, a number determined by the values it reads, `cpp/v3_start.h:158-176`). By START, Ψ(V) ~ π₀ for V iid uniform.
Draws 1..k−1 are 𝓕_{τ_k}-measurable (they end before draw k begins). Hence draw k ~ π₀ independently of draws 1..k−1, for
every k: the D_r draws are iid π₀. Therefore P_c(no draw equals S₀) = (1 − π₀(S₀))^{D_r(c)} exactly.

Every draw is evaluated with `emit = true` before its accept decision (CC1), so each draw lies in 𝓜_r:
{S₀ ∉ 𝓜_r} ⊆ {no draw equals S₀} and P_c(S₀ ∉ 𝓜_r) ≤ (1 − π₀(S₀))^{D_r(c)}.

*Freezing.* Augment the statistical record Φ(c, u) by the sequence of the D_r(c) π₀ draws: each draw is computed from
(c, u) by the same control flow as Φ (W1-N1 Lemma B (B-0), (B-d)), so the augmented record Φ̃ is jointly measurable. Put
g(c, u) := 1{no draw of Φ̃(c, u) equals S₀} for c ∈ A₀ and 0 otherwise; g is bounded and jointly measurable, and
𝓒 ⊥ U_r (SI), so by the T12 freezing lemma
P(no draw of island r equals S₀ | 𝓒) = 1_{E₀}(1 − π₀(S₀))^{D_r(𝓒)} in the localised form. ∎(D-i)

## §2 Several islands (D-ii)

Under IND-T, given 𝓒 the four streams are independent (and independent of streams 0–9), so the four indicator events
{no draw of island r equals S₀} are conditionally independent given 𝓒 (apply the freezing lemma to the product
g₁(c, u₁)⋯g₄(c, u₄) with (U₁..U₄) ⊥ 𝓒). Hence P(S₀ ∉ ∪_r𝓜_r | 𝓒) ≤ Π_r (1 − π₀(S₀))^{D_r} = (1 − π₀(S₀))^{4D_r}
(D_r does not depend on r). Without IND-T only D-i is used. ∎(D-ii)

## §3 The reported HPM (D-iii, D-iv)

*Deterministic step.* Let S† be the hpm_better-maximum of Ω (the exact HPM with the coded tie rule,
`cpp/v3_util.h:121-126`; a strict total order, so S† is unique). By Lemma PC, on {completed}, Ŝ is the hpm_better-maximum
of 𝓜 ⊆ Ω. If S† = S₀ and S₀ ∈ 𝓜, then S₀ is ⪰ every element of 𝓜, so Ŝ = S₀. Sufficient condition: δ < ½. Indeed then for
every S ∈ Ω∖S₀, π(S) ≤ π(Ω∖S₀) < ½ < π(S₀), so F(S₀) > F(S) (e^F ∝ π on Ω, CC2) and S† = S₀. So
{S† ≠ S₀} ⊆ {δ ≥ ½}.

*Probability.* {completed} ⊆ 𝒜 (no final run otherwise, `v3_fit.R` returns before `v3_final_run` when calibration
fails). Hence
{completed} ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜 ∩ {S₀ ∉ 𝓜_r}) for any fixed r ≤ 4,
and by D-i, integrating over 𝓒 and the data (the conditional bound is ≤ 1),
P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜 (1 − π₀(S₀))^{D_r}] ≤ P(δ ≥ ½) + E[1_𝒜 (1 − π₀(S₀))^{D_r}]; with IND-T the
exponent is 4D_r by D-ii.

*Production corollary.* Production budgets give N_e = 4^e·N₀ ≥ N₀ = max(2500, n, p) and L = max(4, ⌈log₂(n+1)⌉)
(`v3_preprocess.R:24-25`, tiers `:30`; `v3_run.R:90`), and T ≥ 1 on 𝒜; so D_r ≥ N₀(1 + 1 + L + 4) = N₀(L + 6). ∎(D-iii)

*Asymptotics (D-iv).* P(S† ≠ S₀) → 0 (the MAP premise; implied by P-CONC since {S† ≠ S₀} ⊆ {δ ≥ ½}). (1 − a)^D ≤ e^{−aD}, so E[1_𝒜(1 − π₀(S₀))^{D_r}] ≤ E[e^{−Q}] with Q := D_rπ₀(S₀) on 𝒜 and Q := ∞ off 𝒜 (LC1 issue 2), i.e. the integrand
1_𝒜e^{−D_rπ₀(S₀)} is defined as 0 off 𝒜; it is bounded and → 0 in probability by P-OVL, so its expectation → 0 (bounded convergence). In production, D_rπ₀(S₀) ≥
max(n, p)·(L + 6)·π₀(S₀) ≥ max(n, p)·log₂(n+1)·π₀(S₀), so the displayed deterministic condition suffices. ∎

## Remarks

- D is a discovery statement: it does not say the particles or the RB PIPs are right (LT♯/C do that). Gibbs flips, swaps,
  local search and LS0 only enlarge 𝓜, so the bound is conservative for the method; it is an equality for the draw
  mechanism alone (`numerics/RESULTS_v1.txt` §5: 0.3754 vs 0.3728, 0.7876 vs 0.7861, z ≤ 1.07).
- The equality concerns the potential run's D_r draws; a stopped run has fewer draws but reports no HPM as complete.
