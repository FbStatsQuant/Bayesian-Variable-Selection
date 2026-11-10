# L4 — Lemma B (bridges: primitive design conditions ⇒ sparse visibility)

Deterministic. Notation: Δ(S) := ‖(I − P_S)μ‖²; c_θ := ‖θ*‖₂/√(n+1); for S ⊉ S₀, T := S₀∖S ≠ ∅.

**L4.0 (per-model inequality).** Let S ⊆ [p], S ⊉ S₀, and suppose √Δ(S) ≥ c_θ. Then
 max_{t∈T} γ(t|S) ≥ Δ(S)·(√Δ(S) − c_θ)² / (n·‖θ*_T‖₁²).

*Proof.* Use L1.7. Because μ̃ = X̃θ* − b̃ and (I − P̃_S)X̃_{S₀∩S} = 0,
 (I − P̃_S)μ̃ = (I − P̃_S)X̃_Tθ*_T − (I − P̃_S)b̃ =: w − (I − P̃_S)b̃.
Then
 Σ_{t∈T} θ*_t·x_tᵀR_Sμ = Σ_{t∈T} θ*_t·x̃_tᵀ(I − P̃_S)μ̃ = (X̃_Tθ*_T)ᵀ(I − P̃_S)μ̃ = ‖w‖² − wᵀb̃ ≥ ‖w‖(‖w‖ − ‖b̃‖),
using wᵀ(I−P̃_S)b̃ = wᵀb̃ and Cauchy–Schwarz. Now ‖w‖² = min_β{‖X_Tθ*_T − X_Sβ‖² + λ₀‖β‖²} + λ₀‖θ*_T‖₂²
≥ min_β‖X_Tθ*_T − X_Sβ‖² = ‖(I − P_S)X_Tθ*_T‖² = Δ(S) (as (I − P_S)μ = (I − P_S)X_Tθ*_T), and ‖b̃‖ = c_θ. The map
u ↦ u(u − c_θ) is increasing on [c_θ/2, ∞), so ‖w‖ ≥ √Δ(S) ≥ c_θ gives
 Σ_{t∈T} θ*_t·x_tᵀR_Sμ ≥ √Δ(S)(√Δ(S) − c_θ) ≥ 0.
The left side is ≤ ‖θ*_T‖₁·max_{t∈T}|x_tᵀR_Sμ|, and a(t|S) ≤ ‖x_t‖² + λ₀ = n − 1 + 1/(n+1) < n. Therefore
 max_{t∈T} γ(t|S) = max_t (x_tᵀR_Sμ)²/a(t|S) ≥ Δ(S)(√Δ(S) − c_θ)²/(n‖θ*_T‖₁²). ∎

**B1 (identifiability margin).** If Δ_n(q) ≥ c_θ² then Γ_n(q) ≥ Δ_n(q)(√Δ_n(q) − c_θ)²/(n‖θ*‖₁²).

*Proof.* For every S with |S| ≤ q, S ⊉ S₀: Δ(S) ≥ Δ_n(q) ≥ c_θ², the map Δ ↦ Δ(√Δ − c_θ)² is nondecreasing on
[c_θ², ∞), and ‖θ*_T‖₁ ≤ ‖θ*‖₁. Apply L4.0 and take the minimum over S. ∎

**B2 (anchored floor).** For every S with |S| ≤ q, S ⊉ S₀: Δ(S) ≥ φ^a_n(q)(n−1)‖θ*_T‖₂² ≥ φ^a_n(q)(n−1)θ_min².
If √(φ^a_n(q)(n−1))·θ_min ≥ c_θ, then
 Γ_n(q) ≥ (φ^a_n(q)(n−1)/n)·(√(φ^a_n(q)(n−1))·θ_min − c_θ)².

*Proof.* Δ(S) = θ*_TᵀX_Tᵀ(I − P_S)X_Tθ*_T ≥ λ_min(X_Tᵀ(I−P_S)X_T)‖θ*_T‖₂² ≥ φ^a(n−1)‖θ*_T‖₂² =: δ_T, and
‖θ*_T‖₂² ≥ |T|θ_min² ≥ θ_min². Since √δ_T ≥ √(φ^a(n−1))θ_min ≥ c_θ, L4.0 and monotonicity of Δ ↦ Δ(√Δ − c_θ)² give,
with ‖θ*_T‖₁² ≤ |T|‖θ*_T‖₂²,
 max_{t∈T}γ(t|S) ≥ δ_T(√δ_T − c_θ)²/(n|T|‖θ*_T‖₂²) = (φ^a(n−1)/n)·(√(φ^a(n−1))‖θ*_T‖₂ − c_θ)²/|T|
 ≥ (φ^a(n−1)/n)·(√(φ^a(n−1))θ_min − c_θ/√|T|)² ≥ (φ^a(n−1)/n)·(√(φ^a(n−1))θ_min − c_θ)²,
using ‖θ*_T‖₂ ≥ √|T|θ_min and that all the bracketed quantities are ≥ 0. ∎

**B2° (anchored floor ⇒ normalised visibility).** Let 0 < κ ≤ φ^a_n(q) and √(κ(n−1))·θ_min ≥ 2c_θ. Then
 Ψ_n(q) ≥ ((n−1)²/n)·κ²θ_min² / (4σ² + 9κ·s₀·θ_min²);
in particular with κ = φ^a_n(q).

*Proof.* Fix S with |S| ≤ q, S ⊉ S₀, T = S₀∖S, and keep the notation w, b̃ of L4.0; put u := ‖w‖. As in L4.0,
u² ≥ Δ(S) ≥ κ(n−1)‖θ*_T‖₂² =: u₀² and u₀ ≥ √(κ(n−1))θ_min ≥ 2c_θ. From the proof of L4.0,
max_{t∈T}γ(t|S) ≥ u²(u − c_θ)²/(n‖θ*_T‖₁²). Also m_S² = μᵀR_Sμ = ‖(I − P̃_S)μ̃‖² = ‖w − (I − P̃_S)b̃‖² ≤ (u + c_θ)², so
σ_S² ≤ σ² + (u + c_θ)²/(n−1). For u ≥ 2c_θ: u − c_θ ≥ u/2 and u + c_θ ≤ 3u/2, whence
 max_{t∈T}γ(t|S)/σ_S² ≥ (u⁴/4)(n−1) / (n‖θ*_T‖₁²(σ²(n−1) + 9u²/4)) = (n−1)u⁴ / (n‖θ*_T‖₁²(4σ²(n−1) + 9u²)).
The right side is increasing in u (u⁴/(A + Bu²) is increasing for A, B > 0), so we may replace u by u₀:
 ≥ ((n−1)²/n)·κ²‖θ*_T‖₂⁴ / (‖θ*_T‖₁²(4σ² + 9κ‖θ*_T‖₂²)) ≥ ((n−1)²/n)·κ²V / (|T|(4σ² + 9κV)),  V := ‖θ*_T‖₂²,
by ‖θ*_T‖₁² ≤ |T|V. V ↦ V/(4σ² + 9κV) is increasing and V ≥ |T|θ_min², so the last expression is
≥ ((n−1)²/n)·κ²θ_min²/(4σ² + 9κ|T|θ_min²) ≥ ((n−1)²/n)·κ²θ_min²/(4σ² + 9κs₀θ_min²). Take the minimum over S. ∎

**B2d (directional floor; R02 proposal 5).** Define the directional floor
 φ^d_n(q) := min{ ‖(I − P_S)X_Tθ*_T‖² / ((n−1)‖θ*_T‖₂²) : |S| ≤ q, S ⊉ S₀, T = S₀∖S }  (≥ φ^a_n(q)).
B2 and B2° hold verbatim with φ^d_n(q) in place of φ^a_n(q) (and, in B2°, for any 0 < κ ≤ φ^d_n(q)).

*Proof.* φ^d ≥ φ^a because ‖(I−P_S)X_Tθ*_T‖² = θ*_TᵀX_Tᵀ(I−P_S)X_Tθ*_T ≥ λ_min(X_Tᵀ(I−P_S)X_T)‖θ*_T‖₂². The proofs of B2
and B2° use the anchored floor only through the inequality Δ(S) ≥ κ(n−1)‖θ*_T‖₂² (first line of each proof), which is
the definition of φ^d_n(q) ≥ κ; everything after it is scalar algebra. ∎
(The directional floor only asks that the *realised* combination X_Tθ*_T of the missing true columns keeps a fixed
fraction of its energy outside span X_S; other combinations of the true columns may be singular.)

**B3 (sparse eigenvalue floor ⇒ anchored floor and superset floor).** If λ_min(G_U) ≥ κ(n−1) > 0 for every U ⊆ [p] with
|U| ≤ q + s₀, then φ^a_n(q) ≥ κ and φ_n(q + s₀) ≥ κ.

*Proof.* For |S| ≤ q, T = S₀∖S: G_S is invertible and X_Tᵀ(I − P_S)X_T is the Schur complement of the block G_S in
G_{S∪T}; the smallest eigenvalue of a Schur complement of a positive definite matrix is at least that of the matrix
(for unit v, vᵀ(M/A)v = min_u [u; v]ᵀM[u; v] ≥ λ_min(M)), and |S∪T| ≤ q + s₀. The second claim is immediate. ∎

**Remark (what the anchored floor does not ask).** φ^a_n(q) > 0 only requires that no combination of the *true*
columns missing from S lies in the span of q other columns. Non-true columns may be arbitrarily collinear among
themselves (exact duplicates included), which a sparse eigenvalue floor on all sets forbids.
