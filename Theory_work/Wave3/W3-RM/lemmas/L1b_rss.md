# L1b — Lemma B2τ: the fixed-design sandwich under RSS-normalised leakage (strengthening adopted from R02 P2)

Status: **PROVED (by this seat, unchecked)**. Origin: review R02 (`../reviews/R02_better_theorem_astra.md` P2,
"ADOPT NOW"). Setting F; notation `../STATEMENT.md` §1, GROW `lemmas/L0_toolkit.md`, `L3_sandwich.md`, GEN
`lemmas/L1_lemmaE.md` ([GEN-L1]). This file is a delta to GROW L3: only the steps listed change.

## Hypothesis
For U ⊆ [p] put Λ_U := ‖(I − P_U)μ‖² and **τ²_U := σ² + Λ_U/(n − 1)** — the residual energy scale of U: noise plus
the mean energy that U leaves unexplained (E[RSS_U]/(n − 1) = τ²_U − σ² rank(P_U)/(n − 1), so τ²_U is its value up to
O(1/n) for bounded |U|) [R06-1]. τ²_U ≥ σ², and U ⊆ U′ ⇒ τ²_{U′} ≤ τ²_U.

* **(L-gain^τ)** for every l ∉ Q and every U ⊆ [p] ∖ {l} with |U| ≤ 15: δ²_{U,l} ≤ η τ²_U log n (η < η_A).
* **(L_b^τ)** the same only for U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}.

Naming: (L-gain^τ), (L_b^τ) are the conditions that STATEMENT v1.2 calls (L-gain), (L_b); the v1.1 forms with σ² are
(L-gain^σ), (L_b^σ) (`L1_fixed.md`, Naming). (L-gain^σ) ⇒ (L-gain^τ) and (L_b^σ) ⇒ (L_b^τ), because τ²_U ≥ σ²: the
τ-form is weakly weaker and can be strictly weaker — unexplained mean energy enlarges the admissible positive
threshold (it is not strictly weaker in every design, e.g. when η = 0 or all outside gains vanish) [R06-2]. Lemmas B1
and B1′ (`L1_fixed.md`) hold with either normalisation (the quantifiers are the same).

## Lemma τ (RSS floor in τ-form)
On the event 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ of [GEN-L1] (`L1_lemmaE.md:26-28`) for a family 𝔉 with 𝒱𝒱 ⊇ {r_A : A ∈ 𝔉}, for every
A ∈ 𝔉:
  RSS_A ≥ (n − 1)τ²_A(1 − ω^τ_n),  ω^τ_n := h_n/√(n − 1) + (4n^{2/3} + t_n)/(n − 1),
and for nested A ⊆ A′ in 𝔉 (so RSS_A ≥ RSS_{A′}):
  ν log(RSS_A/RSS_{A′}) ≤ (1 + ϑ^τ_n)(RSS_A − RSS_{A′})/(2τ²_{A′}),  1 + ϑ^τ_n := (n + 0.02)/((n − 1)(1 − ω^τ_n)).
For the block family of GROW L3.0 (h_n², t_n = O(log n)): ω^τ_n log n → 0 and ϑ^τ_n log n → 0.

*Proof.* By [GEN-L1] (1.1) and the events (`L1_lemmaE.md:13, 46`),
RSS_A ≥ Λ_A − 2σh_n√Λ_A + σ²(n − 1) − σ²(2√((n − 1)n^{1/3}) + 2n^{1/3}) − σ²t_n. By AM–GM,
2σ√(n − 1)√Λ_A ≤ σ²(n − 1) + Λ_A = (n − 1)τ²_A, so 2σh_n√Λ_A ≤ (h_n/√(n − 1))(n − 1)τ²_A; and
σ²(2√((n − 1)n^{1/3}) + 2n^{1/3} + t_n) ≤ τ²_A(4n^{2/3} + t_n). This gives the first display. The second:
log u ≤ u − 1 with u = RSS_A/RSS_{A′}, ν = n/2 + 0.01, and the first display for A′. Rates: h_n = O(√log n),
t_n = O(log n). ∎

## Lemma B2τ
Lemma B2 (`L1_fixed.md`) holds with (L_b^σ) replaced by (L_b^τ): Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, a partition with blocks
≤ 16 that is a deterministic function of X, (G3a), (V_b) with M_n → ∞, (L_b^τ) with η < η_A, deterministic Q ⊇ S₀ with
(L-feas), log|Q| = o(log n) ⇒ P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1.

*Proof (delta to GROW L3; events 𝓔^blk, 𝓩, W_b, C(τ) exactly as `L3_sandwich.md:15-26`).* NEG enters the source at
two places only.

**(i) Step 1, display (3.3)** (`L3_sandwich.md:40-52`). Let b be good with N_b ≠ ∅, d := |N_b| ≤ 16,
U := Ũ_b ∖ N_b ⊇ S₀ ∩ C_b, Π := P_{Ũ_b} − P_U. The lower bound log r_b(Ũ_b) − log r_b(U) ≥ d log(p/k̃) is unchanged.
Upper bound: by L0.2(c) and Lemma τ (U ⊆ Ũ_b nested),
  log r_b(Ũ_b) − log r_b(U) ≤ −½d log(n + 1) + (1 + ϑ^τ_n)(RSS_U − RSS_{Ũ_b})/(2τ²_{Ũ_b}) + 2κ_E.
As in the source, RSS_U − RSS_{Ũ_b} = ‖Πμ + Πε‖² ≤ (1 + ε₁)‖Πε‖² + (1 + 1/ε₁)‖Πμ‖², and adding the elements of N_b
one at a time, ‖Πμ‖² = Σ_s δ²_{U_{s−1},l_s} ≤ Σ_s ητ²_{U_{s−1}} log n ≤ dητ²_U log n by (L_b^τ) (each U_{s−1} ⊇ U ⊇
S₀ ∩ C_b, l_s ∉ Q, and τ²_{U_{s−1}} ≤ τ²_U). Moreover Λ_U − Λ_{Ũ_b} = ‖Πμ‖², so
  τ²_{Ũ_b} = τ²_U − ‖Πμ‖²/(n − 1) ≥ τ²_U(1 − ζ_n),  ζ_n := 16η log n/(n − 1) → 0.
Finally ‖Πε‖² ≤ σ²dW_b ≤ τ²_U dW_b. Hence, with 1 + ϑ″_n := (1 + ϑ^τ_n)/(1 − ζ_n) (ϑ″_n log n → 0),
  d log(p/k̃) ≤ −½d log(n + 1) + (1 + ϑ″_n)(d/2)[(1 + ε₁)W_b + (1 + 1/ε₁)η log n] + 2κ_E,
and, dividing by d/2 (d ≥ 1),
  W_b ≥ [log(n + 1) + 2 log(p/k̃) − (1 + ϑ″_n)(1 + 1/ε₁)η log n − 4κ_E]/((1 + ϑ″_n)(1 + ε₁)).
This is the source's (3.3) with ϑ_n replaced by ϑ″_n. The choice of ε₁, (3.4) and the ladder
(`L3_sandwich.md:54-72`) use only ϑ_n → 0 and η < η_A, so they hold verbatim (W_b and its tail are unchanged).

**(ii) Step 2(b), junk out** (`L3_sandwich.md:86-93`). Let l ∈ Ũ_b ∖ Q, U := Ũ_b ∖ {l} ⊇ S₀ ∩ C_b (every block is
good after Step 2(a)). By L0.2(c) and Lemma τ,
  log γ₀(S̃ ∖ {l}) − log γ₀(S̃) ≥ log p − log k̃ + ½ log(n + 1) − 2κ_E − (1 + ϑ^τ_n)(δ_{U,l} + σZ_{U,l})²/(2τ²_{Ũ_b}),
and τ²_{Ũ_b} ≥ τ²_U(1 − ζ_n) as in (i). By (L_b^τ), 𝓩 and σ ≤ τ_U,
  (δ_{U,l} + σZ_{U,l})²/τ²_U ≤ (√(η log n) + (σ/τ_U)|Z_{U,l}|)² ≤ (√(η log n) + z_n)².
The right side is the source's bound; the final display [½ − η/2 − √(2Aη)] log n − o(log n) − log k̃ − 2κ_E > 0 follows
as in Lemma B2 (with ϑ″_n in place of ϑ_n, and log k̃ = o(log n)).

Step 2(a) (truth inclusion) does not use NEG and is unchanged. ∎

**Consequence.** Theorem RM-F (`L1_fixed.md`) holds with the leakage condition in its τ-form (L-gain^τ) (and (L_b^τ)
in the block-relative variant), as stated in STATEMENT v1.2: only the [SAND(Q)] bridge uses the leakage condition.

**What this does not give** (R02 P2, last paragraph): Form R does not become Form F conditional on X. Under Gaussian
rows the off-block signal heuristically (order of magnitude of the maximum of p Gaussian projections; not a proof)
makes δ_{U,l}/τ_U of order √(2A log n)·√(v/(σ² + v)) at its maximum over p columns, which is not below √(η_A log n) in
general; a distributional (counting) version of (L-gain^τ) would be needed, and proving it
over X for an X-measurable partition is the selection problem that (L-loc-R) solves.
