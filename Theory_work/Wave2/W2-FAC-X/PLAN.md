# W2-FAC-X — PLAN

## Target 1 (Theorem FAC-CS-iid, STATEMENT v2 §4) — proof architecture

**X1 (exact representation, lemmas/X1_representation.md; checked in R01).** Rotation in 1^⊥: e₁ = e/‖e‖, e₂ ∝ factor part ⊥ e₁.
Raw centred columns x^r_j = √ρ f + √(1 − ρ)u_j have coordinates (√ρη + √(1−ρ)ξ_j, √ρφ + √(1−ρ)a_j, √(1−ρ)u_j^⊥),
W := (u_j^⊥ᵀu_l^⊥) ~ W_p(N, I), N = n − 3, independent of (‖e‖, η, φ, ξ, a). For T ⊇ S₀ (μ ∈ span X_T),
RSS_T = ‖e‖²/(1 + q_T), q_T = ṽ1_Tᵀ(W_T + ṽ2_Tṽ2_Tᵀ)⁻¹ṽ1_T, ṽ1 = ξ + ℓη1, ṽ2 = ℓφ1 + a (ℓ = √(ρ/(1 − ρ)));
q_T − q_{T∖j} = ω_j(T)² with ω_j the partial-regression statistic. Reference W = NI, a = 0 gives the RSS analogue of FACB L1 (R01 item 3):
√N·ω_j·√(1 − 1/(k + κ)) = ξ_j − x_T. Every exact neighbour gain (ridge H = (n+1)G + I, standardisation, Q vs RSS)
is written exactly as size term + determinant correction e¹ (absolute ≤ 3/(c₀n)) − ν log(1 + (1 + γ)M_T(1 + ε^d)τ̂² /ν +
r/ψ_T), with ridge remainder |r| ≤ Cn^{−3/2}(1 + P⁰) and ε^d ∈ [0, 2ω²] (absolute bounds, R01 item 3).

**X2 (perturbation bound + event, lemmas/X2_perturbation.md).** B := A_T/N = I + R + bbᵀ, R := W_T/N − I (R01 item 3:
the first-order term is −(B₀⁻¹Rc)_j with (Rc⁰)_j = N⁻¹Σ_l(W − NI)_{jl}(ξ_l − x_T), of size √(k/N)), b := ṽ2/√N;
B⁻¹ṽ1 = c − B₀⁻¹Rc + (B₀⁻¹R)²B⁻¹ṽ1, c := B₀⁻¹ṽ1. The diagonal term R_jj is separated first; the off-diagonal sums are
split over [p] ∖ j and the ξ-defined interval part I(a, b) (≤ (p + 1)² sets, fixed given ξ; conditionally on (ξ, u_j^⊥)
the W_jl, l ≠ j, are iid Gaussian; sums with weights ξ_l and 1 bounded separately and multiplied by the scalar x_T —
R01 item 4) and over the band ∪ exceptional set E (|E| ≤ 17, contains N₀ and one-move modifications: uniform crude bound
#·max_{l≠j}|R_jl|·max|c_l|). Second order ≤ ‖R‖²‖c‖/(1 − ‖R‖) ≍ p^{3/2}H̄/n; a-terms and normalisation O(√(p/n)H̄).
Result: |δ_j(T)| ≤ C_X(H̄ + |x_T|)[√(p log n/n) + (#Band + 17)√(log n/n)] on (a, b; w)-structured sets — a deterministic
consequence of the event 𝔈_n, so it can be applied to path sets (no circularity).

**X3 (deterministic soft-gap lemma, lemmas/X3_softgap.md).** For ϖ-approximate argmin deletions (|ξ_j − x| ≤ d + 2ϖ)
with the exact drift identity: (iii) a crossing (the centre passing a kept point) forces hole width < 4ϖ (|K| ≥ 3);
(iv) without crossing the hole [a, b] only grows; (v)–(vi) once the width is ≥ 4ϖ there are no further crossings and each
new deletion overshoots the kept edge by ≤ 2ϖ; (vii) **density hypothesis**: if every interval of length 9ϖ holds ≤ Q
points and 4Qϖ/(|K_0| − Q − 1 + κ′) ≤ ϖ/10, the initial (narrow-hole) phase has ≤ Q steps and the centre moves by ≤ ϖ/10
during it. R01's deterministic counterexample (all M deletions at distance ϖ above a slowly drifting centre, centre
travel ϖ·log M) violates this hypothesis (Q ≍ M ≍ |K_0|); on the Gaussian event D6, Q ≤ 18e²pϖ + 3 log n + 1 = o(m₀) in
regime (L) (R01 item 1). (ix) sparse case (all spacings > 9ϖ): exact interval holes.

**X4 (path lemma, lemmas/X4_path.md).** Induction on the step: 𝓗(i) (previous moves are R_ϖ-deletions) ⇒ X3 band
structure of T_i ⇒ X2 bound with #Band ≤ 2(2e²p·4.3ϖ + 3 log n + 1) ⇒ |δ| ≤ ¾ϖ **if p H̄√(log n/n) → 0 (A < ½)** ⇒ the
best deletion satisfies R_ϖ (gain-ordering slack C_g n^{−1/2} from X1.4). Proved simultaneously for all |N| ≤ 15 on events
over the deterministic null set (R01 item 4). Bulk (FACB Claim B): B1–B3 with band corrections (D7 tail-ratio event:
window counts ≤ ε′·kept tail + T₀); B4 additions **only at visited T and at T ∖ j**, using the centre bound
|x_T| ≤ ε_bH from B3 and the drift identity (R01 item 2: no family-wide no-addition claim); swaps = G_del(j; T) +
G_add(l; T ∖ j). End phase: D8 spacing of the top 2m₁ + 1 values ⇒ exact top sets; FACB L4.4 with τ̂ = τ + δ, swaps via
the exact identity of X1.4 (g5) relating V̂ to FACB's V (R01 item 2's suggested route). Truth moves: RSS jump ≥ c n
uniformly over T ⊇ S₀.

**X5 (start mode under iid rows, lemmas/X5_start.md).** FACB L2 conditional on X on a design event (sample partial
covariances within blocks = population + O(√(log n/n)) uniformly over |U| ≤ 15; zero pairs exactly zero since
μ ∈ span X_U); FACA L5.1 de-randomisation pattern.

**X6 (assembly + delivery, lemmas/X6_assembly.md).** (H0) on the design event (FACA L5.1 (ii)); [OP], M5-0, T03♯ via the
every-sequence argument; delivery via FACB L5.4 / A2 step 3 with 𝒦_n under the joint law.

## Review pipeline (protocol)
Statement lock (Sol high) → X1–X3 lemma checks (Sol high) → X4 key-lemma check (Sol xhigh) → falsification numerics
per lemma (N1X path, N2X perturbation size vs β_n, N3X soft-gap invariant) → CHECKPOINT → mid-point (fresh Sol xhigh) →
X5, X6 checks → sweep (Sol xhigh) → citation check → council (Sol xhigh + Opus high).

## Target 2 (Target 3, k ≥ 2, moved to W2-FAC-K2 by HQ)
After Target 1's key lemma: diagnose r-class one-factor and two-factor designs with iid_core (general Λ supported),
lock a v2 statement block, attempt the exact-Gram r-class case (per-class gaps; no crossing since the cross-class
drift ℓ_cℓ_{c′}R/(Σℓ²) < d), then iid rows via X2. Otherwise record exact obstructions.
