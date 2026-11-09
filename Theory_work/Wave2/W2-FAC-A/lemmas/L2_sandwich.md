# L2 — Sandwich for Q = [p]: every start-mode maximiser contains S₀

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09; lemma check R03 (Sol high): VERIFIED-WITH-AMENDMENTS
(1 MINOR, applied). This re-proves the Q = [p] branch of C-GROW
lemmas/L3_sandwich.md L3.3(a) under reduced hypotheses (R01 item 5); C-GROW's L3 is "PROVED-CHECKED" inside
Theorem GROW but its hypothesis (G1) includes |Q| ≤ C_Q log n, which fails here, so it is not cited verbatim.

Hypotheses: model G; ‖μ‖² ≤ Mn; p ≤ n^A (any fixed A; (P) gives this); the method's actual blocks C_b with
|C_b| ≤ 16, a deterministic function of X; (G3a) λ_min(R̂_T) ≥ φ₀² for nonempty T ⊆ C_b (implied by (AG) with
φ₀² = 3ψ₀/4 once δ_n ≤ ψ₀/4); (TV) for a deterministic M_n → ∞: δ²_{U,j} ≥ M_n log n for all j ∈ S₀,
U ⊆ C_{b(j)} ∖ {j}; and K = p (true for n ≥ n₀ under (P), since p = o(n)).

**Lemma L2.** P(Sand_n) → 1, where Sand_n := {S₀ ⊆ S̃ for every maximiser S̃ of γ₀ on Ω}.

## Events (as GROW L3.0, block family only)

* 𝓔^blk: the events 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ of [GEN-L1] (`Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md`; GEN R02
  VERIFIED-WITH-AMENDMENTS) for the deterministic family 𝔉_blk := {U : U ⊆ C_b for some b}, which has |U| ≤ 16 and
  |𝔉_blk| ≤ 2^{16}p ≤ 2^{16}n^A, and the vector set {r_U, r_U − r_{U′} : U, U′ ∈ 𝔉_blk} (polynomially many). [GEN-L1]
  needs exactly: fixed maximal set size (16), polynomial family size, Gram floor (G3a) on its nonempty members, and
  ‖μ‖² ≤ Mn. Then P(𝓔^blk) → 1, and on 𝓔^blk, for n ≥ n₀, C-GROW L0.2(c) (score differences for block tables) and
  [GEN-L1] L1.4(b) (nested sets) hold on 𝔉_blk. (C-GROW L0 is only needed with its J fixed = 16 here, i.e. it is
  [GEN-L1] itself.)
* 𝓩 := {Z²_{U,j} ≤ z²_n for all b, U ⊆ C_b, j ∈ C_b ∖ U}, z²_n := 2 log(2^{21}p) + 2 log log n; P(𝓩ᶜ) ≤ 1/log n
  (at most 2^{20}p standard normals; GROW L3.0).

## Proof

Work on 𝓔^blk ∩ 𝓩, n ≥ n₀. Let S̃ be any maximiser of γ₀ on Ω, k̃ := |S̃|, Ũ_b := S̃ ∩ C_b. If k̃ = K = p then
S̃ = [p] ⊇ S₀. Otherwise k̃ < K, and for j ∈ S₀ ∖ S̃ with j ∈ C_b the set S̃ ∪ {j} lies in Ω. Since only block b's
factor and the prior change,
  log γ₀(S̃ ∪ {j}) − log γ₀(S̃) = log[(k̃ + 1)/(2p − 1 − k̃)] + log r_b(Ũ_b ∪ {j}) − log r_b(Ũ_b)
     ≥ −log(2p) − ½ log(n + 1) − 2κ_E + (RSS_{Ũ_b} − RSS_{Ũ_b∪{j}})/(2C_R)
(L0.2(c) and [GEN-L1] L1.4(b) for the nested block sets Ũ_b ⊆ Ũ_b ∪ {j}; constants C_R = 3(M + σ²), κ_E of
[GEN-L1]; k̃ + 1 ≥ 1 and 2p − 1 − k̃ ≤ 2p). Here, as in [GEN-L1] and GROW L0/L3, RSS_A := ‖(I − P_A)Y‖² for the
unscaled centred response Y = Cy^r = μ + Cε. [GEN-L1] L1.3 gives log m(A) = c′_n − ½|A| log(n + 1) − ν log RSS_A + R_A
with |R_A| ≤ κ_E uniformly on the block family; the change from scaled RSS^y_A to RSS_A contributes only to the common
c′_n, and both the ridge correction and the 0.02 term are included in R_A (R03 item 2; the shipped score itself is not
claimed scale invariant). By (TV) and 𝓩, with u := u_{Ũ_b,j} ⊥ 1,
RSS_{Ũ_b} − RSS_{Ũ_b∪{j}} = (uᵀY)² = (δ_{Ũ_b,j} + σZ_{Ũ_b,j})² ≥ δ²/2 − σ²Z² ≥ ½M_n log n − σ²z²_n. Since z²_n ≤ 2(A + 1) log n for
n ≥ n₀ and M_n → ∞, the right side of the display is positive for n ≥ n₀ (−log(2p) ≥ −(A + 1) log n), contradicting
maximality. Hence S₀ ⊆ S̃. The argument is per maximiser and the events do not depend on the maximiser, so it holds
for every maximiser simultaneously. P(𝓔^blk ∩ 𝓩) → 1. ∎

**Remarks.** (1) No size ladder (GROW L3.2) and no NEG are needed: with Q = [p] the upper inclusion S̃ ⊆ Q is trivial
and the only feasibility issue (adding a missing truth) is handled by "k̃ < K or S̃ = [p]". (2) The normalisation
(response scaled to yᵀy = n − 1 inside the score) is handled by [GEN-L1] L1.3 as stated in the proof: the scaling
enters only the common constant c′_n, and the ridge correction and the 0.02 term are part of R_A, |R_A| ≤ κ_E. (3) Under (P), K = p for n ≥ n₀; the lemma itself only needs
"k̃ = K ⇒ S̃ = [p]", i.e. K = p.
