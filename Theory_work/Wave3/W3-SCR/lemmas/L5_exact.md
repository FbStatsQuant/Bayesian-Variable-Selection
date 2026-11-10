# L5 — the excess set of a certified model (L5.1), exact recovery (SCR-C) and refit accuracy (SCR-R)

Uses L1 (L1.1-L1.3, L1.6, L1.7), L2 (E2ᶜʰⁱ, E3a, E3b), SCR-A / SCR-A° (L3). Version 3: L5.1 is stated with the two
geometric quantities α(S), ω(S) that its proof actually uses (R02 proposal 3; R04 finding 1); the eigenvalue-floor
form checked by R04 is the special case α ≥ φ, ω ≤ 1/φ.

## Two quantities of a strict superset S ⊋ S₀
Let E := S∖S₀, m := |E| ≥ 1, and work in the augmented space of L1.7. Let w_i := (I − P̃_{S₀})x̃_i (i ∈ E), a basis of
W := W(E) = span X̃_S ⊖ span X̃_{S₀}, with Gram matrix M := (w_iᵀw_j)_{i,j∈E} (positive definite: it is the Schur
complement of the S₀-block in G_S + λ₀I), and N := diag(M^{-1}). Define
 **α(S) := min_{j∈E} a(j|S∖j)/(n−1)**  (conditional length of each excess column given the rest of S; 0 < α(S) < n/(n−1)),
 **ω(S) := λ_max(N^{-1/2}M^{-1}N^{-1/2})**  (largest eigenvalue of the correlation matrix of M^{-1}; 1 ≤ ω(S) ≤ m).
Facts: (a) 1/(M^{-1})_{jj} = a(j|S∖j) (both are the squared norm of the part of x̃_j orthogonal to span X̃_{S∖j});
(b) if λ_min(G_S) ≥ φ(n−1) with φ ∈ (0, 1], then α(S) ≥ φ and ω(S) ≤ 1/φ;
(c) for m = 1, ω = 1; for m = 2, ω = 1 + |ρ| with ρ := M₁₂/√(M₁₁M₂₂) (the augmented partial correlation of the two
excess columns given S₀).
*Proof.* (a): L1.2(i) and the block-inverse formula. (b): a(j|S∖j) = 1/[(G_S+λ₀I)^{-1}]_{jj} ≥ λ_min(G_S+λ₀I) ≥ φ(n−1);
ω(S) ≤ λ_max(M^{-1})·max_j 1/(M^{-1})_{jj} = max_j a(j|S∖j)/λ_min(M) ≤ (n−1+λ₀)/(φ(n−1)+λ₀) ≤ 1/φ, using
a(j|S∖j) ≤ ‖x̃_j‖² = n−1+λ₀, λ_min(M) ≥ λ_min(G_S+λ₀I) (for unit z, zᵀMz = min_b [b; z]ᵀ(G_S+λ₀I)[b; z]) and φ ≤ 1.
(c): the correlation matrix of the inverse of a 2×2 matrix with correlation ρ has off-diagonal −ρ. The bounds
1 ≤ ω ≤ m hold for every m×m correlation matrix. ∎

## L5.1 (non-asymptotic: a locally optimal strict superset of S₀ forces an inequality)
Let S ⊋ S₀ be LO with |S| = k ≤ q ≤ K−1, E, m, α := α(S), ω := ω(S) as above. Let x, x′ > 0 and suppose
E2ᶜʰⁱ(x) ∩ E3a(q, x) ∩ E3b(q, x′) holds. Define
 Λ_k(α) := 2 log((2p−k)/k) + log(α(n² − 1)/n),
 1 − η_n(k, x) := [ (1 − 2√(x/(n−1)) − U(k, x)/(n−1))₊^{1/2} − ‖θ*‖₂/(σ√(n² − 1)) ]₊².
Then
 (EC′)  (1 − η_n(k, x))·(1 − 1.02/n)·(Λ_k(α))₊ ≤ ω·( 1 + √(2 log C(p−s₀, m)/m + 2x′) + ‖θ*‖₂/(σ√(m(n+1))) )².
In particular, if λ_min(G_S) ≥ φ(n−1) with φ ∈ (0, 1], then
 (EC)  φ·(1 − η_n(k, x))·(1 − 1.02/n)·(Λ_k(φ))₊ ≤ ( 1 + √(2 log C(p−s₀, m)/m + 2x′) + ‖θ*‖₂/(σ√(m(n+1))) )².

*Proof.* Since S ⊇ S₀, X̃θ* ∈ span X̃_S, so ỹ_c = X̃θ* − b̃ + ε̃ gives
 (I − P̃_S)ỹ_c = (I − P̃_S)(ε̃ − b̃),  and for j ∈ E (S∖j ⊇ S₀): ũ_jᵀỹ_c = ũ_jᵀ(ε̃ − b̃), ũ_j := ũ_{S∖j, j}.   (1)

*Step 1 (each excess variable must have a large gain).* For j ∈ E, the deletion S∖j is in 𝒩(S) and F(S∖j) ≤ F(S).
By L1.6, multiplied by τ̂² (g_{y_c} = τ̂²g_y, q_S(y_c) = τ̂²Q_S),
 g_{y_c}(j|S∖j) ≥ ((n+1)/(nν))·(0.02τ̂² + q_S(y_c))·B_j,  B_j := log((2p−k)/k) + ½ log D(j|S∖j).
By L1.3, D(j|S∖j) ≥ (n+1)a(j|S∖j)/n ≥ (n+1)α(n−1)/n. Hence 2B_j ≥ Λ_k(α) (and B_j ≥ 0, as 2p−k ≥ k and D ≥ 1).
By L1.1 and L1.7, q_S(y_c) ≥ (n/(n+1))·y_cᵀR_Sy_c = (n/(n+1))‖(I − P̃_S)ỹ_c‖², and by (1), ‖ε̃‖ = ‖Cε‖, E2ᶜʰⁱ, E3a:
 ‖(I − P̃_S)ỹ_c‖ ≥ (‖ε̃‖² − ‖P̃_Sε̃‖²)₊^{1/2} − ‖b̃‖ ≥ σ√(n−1)·[(1 − 2√(x/(n−1)) − U(k,x)/(n−1))₊^{1/2} − ‖θ*‖₂/(σ√(n²−1))],
so ‖(I − P̃_S)ỹ_c‖² ≥ σ²(n−1)(1 − η_n(k, x)) (a norm is ≥ 0, which justifies the outer positive part). Therefore
 g_{y_c}(j|S∖j) ≥ (1/ν)·σ²(n−1)(1 − η_n)·B_j ≥ σ²(1 − η_n)(1 − 1.02/n)·(Λ_k(α))₊,   (2)
where: 0.02τ̂² ≥ 0 is dropped; (n+1)/(nν)·n/(n+1) = 1/ν; B_j ≥ ½(Λ_k(α))₊ (B_j ≥ 0 and B_j ≥ Λ_k(α)/2); and
(n−1)/(2ν) = (n−1)/(n + 0.02) = 1 − 1.02/(n + 0.02) ≥ 1 − 1.02/n.

*Step 2 (the gains of the excess variables are jointly limited).* The dual basis d_j := Σ_i (M^{-1})_{ji}w_i satisfies
d_jᵀw_i = δ_{ij}, so d_j is proportional to (I − P̃_{S∖j})x̃_j (the part of w_j orthogonal to the other w_i; note
(I − P̃_{S∖j})x̃_j = (I − P̃_{S∖j})w_j because span X̃_{S₀} ⊆ span X̃_{S∖j}), i.e. ũ_j = ±d_j/‖d_j‖. The Gram matrix of (d_j)
is M^{-1}MM^{-1} = M^{-1}, so ‖d_j‖² = (M^{-1})_{jj} and the Gram matrix of (ũ_j)_{j∈E} is, up to signs,
N^{-1/2}M^{-1}N^{-1/2}. For any vector v, writing Ũ for the matrix with columns ũ_j ∈ W,
 Σ_{j∈E}(ũ_jᵀv)² = ‖ŨᵀP_Wv‖² ≤ λ_max(ŨᵀŨ)·‖P_Wv‖² = ω·‖P_Wv‖².
With v = ε̃ − b̃, (1), ‖b̃‖ = ‖θ*‖₂/√(n+1) and E3b:
 Σ_{j∈E} g_{y_c}(j|S∖j) = Σ_{j∈E}(ũ_jᵀ(ε̃ − b̃))² ≤ ω(‖P_Wε̃‖ + ‖b̃‖)² ≤ ω(σ√(U′(m, x′)) + ‖θ*‖₂/√(n+1))².   (3)

*Step 3.* Sum (2) over the m elements of E, compare with (3), divide by mσ², and use
U′(m, x′)/m = (1 + √(2 log C(p−s₀, m)/m + 2x′))². This is (EC′). For (EC): by fact (b), α ≥ φ and ω ≤ 1/φ, and
Λ_k is increasing in its argument; multiply (EC′) by φ. ∎

**Reading of L5.1 (the excess set of a certified model is controlled).** On the events of L5.1 and of SCR-A / SCR-A°,
every certified model C of size ≤ q is S₀ ∪ E where E is empty or belongs to the deterministic family
𝒜_n(q, x, x′) of excess sets satisfying (EC′). Write A := (1 − η_n(k, x))(1 − 1.02/n) ∈ [0, 1) and R_m for the squared
bracket on the right of (EC′). Then: (i) |C∖S₀| ≤ max{|E| : E ∈ 𝒜_n} (0 if 𝒜_n = ∅); (ii) for a single excess
variable (m = 1, ω = 1), (EC′) reads A·(2 log((2p−k)/k) + log(α(n²−1)/n))₊ ≤ R_1, which for A > 0 is the explicit upper
bound α ≤ (n/(n²−1))·exp(R_1/A − 2 log((2p−k)/k)) on its conditional length; (iii) in general (EC′) is the lower bound
ω(S) ≥ A·(Λ_k(α(S)))₊/R_m. If A = 0, (EC′) is vacuous; for A > 0, whether these bounds are restrictive depends on their
numerical values (x, x′, the coefficient bias and the other displayed parameters). Sufficient for A → 1:
U(k, x) = o(n), x = o(n) and ‖θ*‖₂/(σn) = o(1). No universal bound on |E|, and no general statement that α must be small
or ω large, is claimed.

**Corollary L5.2.** Let q ≤ K−1, x_A, x, x′ > 0, MC(q, x_A) (resp. MC°(q, x_A)). If (EC′) is **violated** for every
S ⊋ S₀ with |S| ≤ q — in particular if φ := φ_n(q) > 0 and (EC) with this φ is violated for every 1 ≤ m ≤ q − s₀
(k = s₀ + m) — then on 𝓔_C := E1(q,x_A) ∩ E2⁺(x_A) ∩ E2ᶜʰⁱ(x) ∩ E3a(q,x) ∩ E3b(q,x′) (resp. also ∩ E4(q, x_A)), with
P(𝓔_Cᶜ) ≤ 3e^{-x_A} + (1 + 2q)e^{-x} + e^{-x′}/(1 − e^{-x′}) (resp. with 4e^{-x_A}), **every LO model of size ≤ q
equals S₀**. (If q ≤ s₀ there is no strict superset of size ≤ q and nothing to check.)

*Proof.* On the screening event an LO model S with |S| ≤ q contains S₀ (SCR-A, resp. SCR-A°). If S ≠ S₀ then S ⊋ S₀
and L5.1 yields (EC′) for S — and (EC) with φ = φ_n(q), m = |S| − s₀, since λ_min(G_S) ≥ φ_n(q)(n−1) — a
contradiction. ∎

## SCR-C (asymptotic)
Assume: the hypothesis of (A∞) or of (A°∞) for q_n ∈ {0, …, K−1}; s₀ = O(1); ‖θ*‖₂ = O(σ√n); q_n log p = o(n);
n → ∞; and φ_n(q_n) ≥ ϑ_n + ε for all large n, where ϑ_n := 2 log p/(2 log p + log n) and ε > 0 is fixed. Then
P(∃ C ∈ 𝒞: |C| ≤ q_n, C ≠ S₀) → 0. (If q_n ≤ s₀ the claim is SCR-A / SCR-A°.)

*Proof.* Apply Corollary L5.2 with x_A := √(log n) (for which MC(q_n, x_A), resp. MC°(q_n, x_A), holds for large n:
proofs of (A∞), (A°∞)), x := x_n := 2 log n and x′ := ε₁ log n, ε₁ := ε/8. The failure probability is at most
4e^{-√(log n)} + (1 + 2q_n)n^{-2} + n^{-ε₁}/(1 − n^{-ε₁}) → 0 (q_n ≤ n).
It remains to show that (EC) is violated for all 1 ≤ m ≤ q_n − s₀ when n is large, with φ = φ_n(q_n) ∈ [ε, 1].
*Left side.* (i) U(k, x_n) ≤ 2k + 4k log(ep/k) + 8 log n ≤ 2q_n + 4q_n log(ep) + 8 log n = o(n) uniformly in k ≤ q_n
(k ↦ k log(ep/k) is increasing on [1, p], and q_n log p = o(n) forces q_n = o(n)); with ‖θ*‖₂/σ = O(√n) this gives
sup_{k≤q_n} η_n(k, x_n) → 0 (the term ‖θ*‖₂/(σ√(n²−1)) is O(n^{-1/2})). (ii) k = s₀ + m ≤ (s₀+1)m and 2p − k ≥ p, so
with ℓ := log(p/m) ∈ [0, log p]: Λ_k(φ) ≥ 2ℓ + log n − c₄, c₄ := 2 log(s₀+1) + log(1/ε) + 1 (bounded because
s₀ = O(1); for n ≥ 2, log((n²−1)/n²) ≥ −1). Hence
 LHS(EC) ≥ φ(1 − o(1))(2ℓ + log n − c₄)₊ with o(1) uniform in m.
*Right side.* log C(p−s₀, m)/m ≤ log(ep/m) = ℓ + 1 and ‖θ*‖₂/(σ√(m(n+1))) ≤ c₃ for a constant c₃, so
 RHS(EC) ≤ (1 + c₃ + √(2ℓ + 2 + 2ε₁ log n))² ≤ 2ℓ + 2ε₁ log n + 2(1 + c₃)√(2 log p + 2 + 2ε₁ log n) + (1 + c₃)² + 2.
*Comparison.* φ(2ℓ + log n) − 2ℓ = φ log n − 2(1 − φ)ℓ ≥ φ log n − 2(1 − φ) log p = φ(2 log p + log n) − 2 log p
≥ ε(2 log p + log n), by φ ≤ 1, ℓ ≤ log p and φ ≥ ϑ_n + ε. Therefore, with 𝐋 := 2 log p + log n → ∞ and
2ℓ + log n ≤ 𝐋,
 LHS − RHS ≥ ε𝐋 − o(1)·𝐋 − c₄ − 2ε₁𝐋 − 2(1 + c₃)√(2𝐋 + 2) − (1 + c₃)² − 2 ≥ (ε/2)𝐋 − O(√𝐋) > 0
for all large n, uniformly in m (in particular the positive part in LHS is active). So (EC) is violated for every m,
and Corollary L5.2 (with CC2-CC3) gives the claim. For p ≤ n^A, ϑ_n ≤ 2A/(2A+1). ∎

**Remark (what is and is not claimed beyond the floor).** The floor φ_n(q_n) enters twice: as a lower bound for the
conditional lengths α(S) (the determinant penalty, Step 1) and through ω(S) ≤ 1/φ (Step 2). A condition on ω alone is
**not** sufficient (R04 finding 1: two nearly collinear excess columns have ω ≤ 2 but conditional lengths ≈ 11/n, their
determinant penalty is O(1) instead of ½ log n, and S₀ plus that pair is LO with probability bounded away from 0).
The general tool is (EC′), which keeps both α(S) and ω(S); no asymptotic theorem in terms of (α, ω) is claimed here.

## SCR-R (refit accuracy)
Let 𝓔_R := E3a(q_n, 2 log n), failure probability ≤ 2q_n n^{-2} → 0. Work on 𝓔_R intersected with the screening event
supplied by SCR-A or SCR-A° (whichever hypothesis is assumed). Let C ∈ 𝒞 with 1 ≤ |C| = k ≤ q_n; then C ⊇ S₀, so
μ ∈ span X_C and, the columns being centred, the least-squares fitted mean satisfies
 P_Cy_c − μ = P_CCε = P_Cε,  ‖P_Cy_c − μ‖² = ‖P_Cε‖² ≤ σ²U(k, 2 log n) ≤ σ²(√k + √(2k log(ep/k) + 4 log n))²
(log C(p,k) ≤ k log(ep/k)); **this prediction bound needs no eigenvalue floor.** If moreover λ_min(G_C) ≥ φ(n−1) > 0,
G_C is invertible, θ̂_C − θ*_C = G_C^{-1}X_Cᵀε, X(θ̂_C − θ*) = P_Cε, and
 ‖θ̂_C − θ*‖₂² = εᵀX_CG_C^{-2}X_Cᵀε ≤ ‖P_Cε‖²/λ_min(G_C) ≤ the same bound /(φ(n−1)),
using X_CG_C^{-2}X_Cᵀ ⪯ λ_min(G_C)^{-1}P_C. ∎
