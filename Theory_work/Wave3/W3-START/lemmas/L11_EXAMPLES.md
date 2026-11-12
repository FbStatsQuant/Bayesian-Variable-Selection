# L11 — Examples (T7): verification of the hypotheses for five families

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Object: the "Proposed examples" of `STATEMENT.md` §5.3 (T7). Each example is verified against the **partition-free**
hypotheses, for all small sets, not on a block. None of these families is a hypothesis of any theorem.
Uses: `lemmas/L3_LEAK.md` (Lemma J, L3.5), `lemmas/L6_COROLLARIES.md` (F1, F2, F4), `lemmas/L9_BR.md` ((T3)(b)).

## L11.0 A frame for the fixed-design examples

Let n ≥ 18, 17 ≤ p ≤ n − 1, N := n − 1. Since dim 1^⊥ = N ≥ p there are e₁, …, e_p ∈ ℝⁿ with 1ᵀe_i = 0 and e_iᵀe_j = N·1{i = j}.
Every design below has columns x_j ∈ span{e_i} with ‖x_j‖² = N; such a matrix is centred with sample standard deviations
1, so it is its own standardisation: X = X^r, D_x = I, θ* = β. σ² > 0 fixed; p = p_n with p ≤ n^A.
For a null l and a set U ∌ l: δ²_{U,l} = Λ_U − Λ_{U∪{l}}, Λ_U = ‖(I − P_U)μ‖².

## L11.1 Example F-1: orthogonal design (F1 with η = 0; F2)

x_j := e_j for all j; S₀ fixed with s₀ ≥ 1; θ*_j fixed and nonzero on S₀ (θ_lo ≤ |θ*_j| ≤ θ_hi). Assume p > s₀ for all
sufficiently large n.
* (E): ‖μ‖² = N‖θ*‖² ≤ s₀θ_hi²n. (GF-16): X_TᵀX_T = N·I, so g_* = 1 works (even the normalised floor holds).
* Null gains: for a null l and any U ∌ l, (I − P_U)x_l = e_l ⊥ μ, so δ_{U,l} = 0: F1's hypothesis with η = 0, Q = S₀.
* (V-c) for every c_V: for j ∈ S₀ and U ∌ j, δ²_{U,j} = Nθ*_j² and τ²_U ≤ σ² + ‖θ*‖²; so δ²_{U,j}/τ²_U ≥ Nθ_lo²/(σ² + s₀θ_hi²) ≥ c_V log n for
  n large.
* (AL), default levels: 𝔏_n(S₀) ≤ √(2/π)z_n (L6.1(iv)), so ϱ_n(S₀) = O(√(log n/n)) → 0.
**Conclusions.** (T1)(a)–(d) with Q = S₀: o₀ = O_P(√(log n/n)); κ_V is arbitrary, so (T1)(c): o₀/T₁ → 1. If moreover
p/√log n → ∞, F2 applies with η′ = 0 (λ_min(R̂_{S₀}) = 1; n^{−1/2}𝔏_n(S₀)² = O(log n/√n) → 0): **o₀ is of exact order n^{−1/2}**. ∎

## L11.2 Example F-3: near-duplicate null columns ((GF-16), not a normalised floor)

Fix d ∈ (0, 2] and m_n ≥ 1 with 1 + 2m_n ≤ p. x₁ := e₁ (the only truth, θ*₁ ≠ 0 fixed). For k = 1, …, m_n: x_{2k} := e_{2k},
x_{2k+1} := cos φ_n·e_{2k} + sin φ_n·e_{2k+1}, with φ_n ∈ (0, π/2] defined by 2N(1 − cos φ_n) = d² (so ‖x_{2k} − x_{2k+1}‖ = d). All remaining
columns x_j := e_j.
* (GF-16): for any T the Gram matrix X_TᵀX_T is block diagonal with blocks N (single columns) and
  N·[[1, cos φ_n], [cos φ_n, 1]] (a twin pair, both in T), whose eigenvalues are N(1 ± cos φ_n); the smallest is d²/2. So
  λ_min(X_TᵀX_T) ≥ min(N, d²/2) = d²/2 =: g_* for all T. The normalised floor fails: λ_min(R̂_{{2k,2k+1}}) = d²/(2N) → 0.
* Null gains: every null column and every set U ∌ 1 lie in span{e_i : i ≥ 2} ⊥ μ = θ*₁e₁, so (I − P_U)x_l ⊥ μ and δ_{U,l} = 0; if
  1 ∈ U then (I − P_U)μ = 0. Hence δ_{U,l} = 0 for every null l and every U: η = 0.
* (E), (V-c) (δ²_{U,1} = Nθ*₁² for U ∌ 1), (AL): as in F-1.
**Conclusions.** As in F-1: o₀ = O_P(√(log n/n)), o₀/T₁ → 1, and exact order n^{−1/2} if p/√log n → ∞ — with as many twin
pairs as desired (for instance every second null). ∎

## L11.3 Example F-2: one truth with fifteen correlated nulls ((V-m) not (V-c); F4 where default (AL) fails)

Fix A ∈ [0.1, 1], p := min(⌊n^A⌋, n − 1) (so log p/log n → A and A̲ = Ā = A), ρ² := 0.4, c := 2(1 + 2A).
x₁ := e₁; x_l := ρe₁ + √(1 − ρ²)e_l for l = 2, …, 16; x_j := e_j for j ≥ 17. S₀ = {1}, θ*₁ := σ√(c log n/N), so μ = θ*₁e₁ and
‖μ‖² = cσ² log n.
**Residual energies.** For N ⊆ [p] ∖ {1} let k := |N ∩ {2, …, 16}|. The columns e_j (j ≥ 17) are orthogonal to e₁ and to the
correlates, so they do not matter. For k ≥ 1 the Gram matrix of the k correlates is N[(1 − ρ²)I + ρ²11ᵀ], their inner
products with e₁ are Nρ1, and 1 is an eigenvector of the Gram matrix with eigenvalue N(1 − ρ² + kρ²). Hence
‖(I − P_N)e₁‖² = N[1 − kρ²/(1 − ρ² + kρ²)] = N·q_k,   q_k := (1 − ρ²)/(1 + (k − 1)ρ²) (k ≥ 1),  q₀ := 1.
So **Λ_N = cσ² log n·q_k**, with q₁ = 0.6, q₁₅ = 0.6/6.6 = 1/11, q_k decreasing; and σ² ≤ τ²_N ≤ σ²(1 + c log n/N).
* **(E):** ‖μ‖² = cσ² log n ≤ Mn. **(GF-16):** the 16 columns x₁, …, x₁₆ equal (e₁, …, e₁₆)B with B upper triangular with
  diagonal (1, √(1 − ρ²), …, √(1 − ρ²)), so their Gram matrix is N·BᵀB with λ_min(BᵀB) =: γ_B > 0 depending on ρ only; any X_TᵀX_T
  is block diagonal with a principal submatrix of N·BᵀB and N·I. So λ_min(X_TᵀX_T) ≥ Nγ_B ≥ γ_B =: g_*.
* **(V-m) holds, Q = S₀, with c_m := (1 + 2A)/6 and any ε₀ > 0.** The instances are V = D = {1}, R = ∅, N ⊆ [p] ∖ {1}, |N| ≤ 15;
  U = N, T = {1}, W = N ∪ {1}; Λ_T = Λ_W = 0, so the condition reads Λ_N/τ²_N ≥ [(1 + 2A)(1 − |N|)₊ + c_m] log n.
  N = ∅: Λ_∅/τ²_∅ = c log n/(1 + c log n/N) ≥ (1 + 2A + c_m) log n = (7/12)c log n for n large.
  N ≠ ∅: Λ_N/τ²_N ≥ cq₁₅ log n/(1 + c log n/N) ≥ (c/12) log n = c_m log n for n large (q_k ≥ 1/11; if k = 0, q₀ = 1).
  So κ_V = c_m/2 = (1 + 2A)/12.
* **(V-c) fails for every c_V > 1 + 2A:** at j = 1, U = {2, …, 16}: δ²_{U,1} = Λ_U − 0 = cσ² log n/11 ≤ (2(1 + 2A)/11)τ²_U log n, and
  2/11 < 1.
* **F4 applies with I_n := {2, …, 16}, ī = 15, level c′ := 0.8(1 + 2A) < 1 + 2A̲.** Let l ∈ I_n and U ∌ l, |U| ≤ 15. If 1 ∈ U, Λ_U = 0
  and δ_{U,l} = 0. Otherwise let k := |U ∩ I_n| ≤ 14; δ²_{U,l} = Λ_U − Λ_{U∪l} = cσ² log n(q_k − q_{k+1}), with q₀ − q₁ = ρ² = 0.4 and, for
  k ≥ 1, q_k − q_{k+1} = (1 − ρ²)ρ²/((1 + (k − 1)ρ²)(1 + kρ²)) ≤ 0.24/1.4 < 0.4. So δ²_{U,l} ≤ 0.4cσ² log n ≤ c′τ²_U log n.
  For a null l ≥ 17: x_l = e_l is orthogonal to every other column and to μ, so δ_{U,l} = 0 and J_n(0, τ_U) ≤ √(2/π)z_n. Hence
  ϱ^{−I}_n(S₀) ≤ 2n^{−1/2}√(2/π)z_n → 0, and |Q| + 1 = 2. By L3.5/L6.4, (AL) holds with the F4 levels, and
  ϱ_n(S₀; h) ≤ ϱ^{−I}_n(S₀) + 2n^{−(1+2A−c′)/2+o(1)} = O(n^{−0.1(1+2A)+o(1)}).
* **Default-level (AL) fails:** ϱ_n(S₀) → ∞. For l ∈ I_n and U = ∅: d := δ_{∅,l} = ρθ*₁√N = σ√(0.4c log n), t := τ_∅ with
  1 − a := 1 − σ²/t² ≤ c log n/N. Restricting the integral defining J to z ∈ [z_n − 1, z_n] (d > 0):
  J_n(d, t) ≥ (2π)^{−1/2}·exp(d²/(2t²) + dσ(z_n − 1)/t² − (1 − a)z_n²/2), and (1 − a)z_n² → 0, σ²/t² → 1, z_n² ≥ 2 log p. So
  log J_n(d, t) ≥ [0.2c + √(0.8cA) − o(1)] log n, and ϱ_n(S₀) ≥ 2n^{−1/2}p⁻¹J_n(d, t) ≥ n^{−1/2−A+0.2c+√(0.8cA)−o(1)}. With c = 2(1 + 2A) the
  exponent is −0.1 − 0.2A + √(1.6A + 3.2A²) − o(1), which is ≥ 0.3 for A ≥ 0.1 (at A = 0.1: −0.12 + √0.192 = 0.318; the
  expression increases in A).
**Conclusions.** (T1)(a), (b), (d) apply with (V-m) and the F4 levels: π₀(S₀) → 1 in probability and
o₀ = O_P(n^{−0.1(1+2A)+o(1)}) + o_P(n^{−κ}) for every κ < (1 + 2A)/12, i.e. o₀ = o_P(n^{−κ}) for every κ < (1 + 2A)/12 — although
(V-c) fails and the default-level condition fails. ((T1)(c) is not available: κ_V = (1 + 2A)/12 ≤ ¼.) ∎

## L11.4 Example G-1: Gaussian rows with independent columns (p ≫ n allowed)

Setting R with Σ_n = I_p, s₀ < p ≤ n^A otherwise arbitrary, s₀ ≥ 1, |θ*_j| ∈ [θ_lo, θ_hi] on S₀.
* (FL-R16): c_Σ = 1. (V-R): for j ∈ S₀, U ∌ j: Cov(W_j, Σ_kθ*_kW_k | W_U) = θ*_j (independence), so a_V = θ_lo.
* (L-R) with Q := S₀ (|Q| = s₀ ≤ min(K, (log n)^{κ_Q}) for n large, κ_Q := 1) and H_l := {l} ∪ S₀: for l ∉ Q, U ∌ l, U₀ = U ∩ H_l ⊆ S₀:
  Cov(W_l, W_j | W_{U₀}) = 0 for j ∈ S₀ ∖ U₀ (C_L = 0); for v ∈ U ∖ H_l (so v ∉ {l} ∪ S₀): Cov(W_l, W_v | W_{U₀}) = 0 and
  Cov(W_j, W_v | W_{U₀}) = 0 (r_n = 0).
**Conclusion.** (T3)(b) with C_L = 0, Q = S₀: 1 − π₀(S₀) = O_P(n^{−1/2}(log n)^{15κ_Q+1/2}), and P(π₀(S₀) ≥ 1 − n^{−c}) → 1 for every c < ½,
for every p ≤ n^A, p ≫ n included. (Here |I_l| ≤ 2^{s₀} is bounded, so the proof of L9.6(b) gives the sharper
𝔏_n(S₀) = O_P(√log n) and 1 − π₀(S₀) = O_P(√(log n/n)); only the stated rate is claimed.) ∎

## L11.5 Example G-2: block-diagonal covariance, one truth per group (lattice form)

Setting R with p > s₀; [p] is partitioned into groups of size ≤ ḡ (fixed); Σ_n is block diagonal over the groups, unit diagonal,
with λ_min(Σ^{(group)}) ≥ c > 0 for every group; each group contains at most one truth; G(j) := the group of j;
Q := ∪_{j∈S₀}G(j), |Q| ≤ s₀ḡ (≤ K and ≤ (log n)^{κ_Q} for n large); H_l := G(l) ∪ Q for l ∉ Q (|H_l| ≤ (s₀ + 1)ḡ).
Different groups are independent, and remain independent given any set of coordinates.
* (FL-R16): a principal submatrix of Σ_n is block diagonal with blocks that are principal submatrices of the group
  blocks, so λ_min(Σ_S) ≥ c for every S. (V-R): for j ∈ S₀, U ∌ j: Cov(W_j, W_k | W_U) = 0 for a truth k in another group, so
  Cov(W_j, Σ_kθ*_kW_k | W_U) = θ*_jVar(W_j | W_{U∩G(j)}), of absolute value ≥ θ_lo·c (Schur complement); a_V = cθ_lo.
* (L-gain-R): l ∉ Q, so G(l) contains no truth; for j ∈ S₀ ∖ U₀, l and j are in different groups: Cov(W_l, W_j | W_{U₀}) = 0; C_L = 0.
* (L-loc-R): v ∈ U ∖ H_l is neither in G(l) nor in a truth group, so Cov(W_l, W_v | W_{U₀}) = 0 = Cov(W_j, W_v | W_{U₀}); r_n = 0.
**Conclusion.** (T3)(b) with C_L = 0: 1 − π₀(𝓛(Q)) = O_P(n^{−1/2}(log n)^{15κ_Q+1/2}) with Q the union of the truths' groups (|Q| bounded);
p ≤ n^A is the only restriction on p. Nothing is claimed about π₀(S₀) itself: the nulls in a truth's group may leak. ∎

## L11.6 Not verified here
UNI-0 families and exact-separation AR(1) (listed in `STATEMENT.md` (T7) as expected examples): their verification of
(V-R) and (L-R) is in `Theory_work/Wave3/W3-RM/lemmas/L3_SANDR.md` §9 and its sources, of status "PROVED (by this seat,
unchecked)"; it is not re-proved here and nothing is claimed for them.
