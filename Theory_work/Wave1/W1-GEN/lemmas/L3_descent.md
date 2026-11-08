# L3 — Descent inside a bounded separated relevance set (probabilistic part of (C2))

Status: **PROVED (by this seat, unchecked)**; lemma check R04 (Codex Sol): VERIFIED-WITH-AMENDMENTS, amendments
applied (v2, reviews/R02_R04_disposition.md).

Hypotheses: G; R (‖μ‖² ≤ Mn); s₀ ≥ 1 fixed; p ≤ n^A; BM-∞; (H1) with constants v̄, φ₀ ∈ (0, 1], c_S ∈ [0, 1)
(STATEMENT.md §2). (H1a) implies φ₀ ≤ 1 (a nonempty normalized Gram matrix has trace equal to its dimension).
𝒱 = 𝒱_n denotes deterministic sets of uniformly bounded cardinality |𝒱_n| ≤ v̄ (they may change with n). Notation of STATEMENT.md §1
and L1. Write F(A) := log w(|A|) + log m(A) (common constants dropped; only differences are used), and

  L_n := (n − 1)φ₀⁴θ*²_min.   By BM-∞ and φ₀ fixed, L_n/log n → ∞.                                       (3.0)

## L3.0 The family and the event

𝔉 := {S ∪ L : S ⊆ 𝒱, L ⊆ [p] ∖ 𝒱, |L| ≤ 1}. Every A ∈ 𝔉 satisfies A ⊆ 𝒱 ∪ {l} for some l, so
|A| ≤ min(p, v̄ + 1) =: J and, by
(H1a) and Cauchy interlacing, λ_min(R̂_A) ≥ φ₀² for nonempty A. |𝔉| ≤ 2^{v̄}(p + 1) ≤ 2^{v̄+1}n^A, so L1 applies with
J = v̄ + 1, C_F = 2^{v̄+1}, D = A, and 𝒱𝒱 := {r_A − r_{A′} : A, A′ ∈ 𝔉} ∪ {r_A : A ∈ 𝔉} (D_V = 2A). Every neighbour
(flip or swap) of a set S ⊆ 𝒱, and every such set itself, belongs to 𝔉; all members of 𝔉 are feasible once
⌊n/2⌋ ≥ v̄ + 1 (then min(p, v̄ + 1) ≤ K). Only feasible neighbours are ever compared.

Additional Gaussian events:
* 𝒟₄ := {|Z_{T,e}| ≤ z_n for all S₀ ⊆ T ⊆ 𝒱 and e ∈ T ∖ S₀}, where u_{T,e} := unit vector of (P_T − P_{T∖{e}}) (rank
  one by (H1a)), Z_{T,e} := u_{T,e}ᵀε/σ, z_n := log log n. This is a family of at most v̄2^{v̄} standard normals
  (u ⊥ 1), so P(𝒟₄ᶜ) ≤ 2v̄2^{v̄}e^{−z_n²/2} → 0.
* 𝒟₅ := {Z²_{T,l} ≤ 2 log(2^{v̄}p) + 2 log log n for all S₀ ⊆ T ⊆ 𝒱 and l ∉ T}, Z_{T,l} := u_{T,l}ᵀε/σ with u_{T,l}
  the unit vector of (I − P_T)x_l (exists by (H1a)). At most 2^{v̄}p standard normals:
  P(𝒟₅ᶜ) ≤ 2^{v̄}p · 2exp(−log(2^{v̄}p) − log log n) = 2/log n → 0.

Ω_n := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ ∩ 𝒟₄ ∩ 𝒟₅ (𝒟₁–𝒟₃ from L1 with the data above). P(Ω_n) → 1.

n₀ denotes a threshold depending on σ², M, φ₀, A, v̄, c_S, the BM-∞ envelope, the onset n_SEP from which (H1b)
holds, and the feasibility onset ⌊n/2⌋ ≥ v̄ + 1. On Ω_n and for n ≥ n₀, L1.2–L1.4 hold on 𝔉, and we use the common
nonnegative bound

  Π := (A + 1) log n + 1 ≥ |log[w(|A|)/w(|A′|)]| + ½||A| − |A′|| log(n + 1) whenever ||A| − |A′|| ≤ 1,

because for every actual addition from size k ≤ p − 1: (k + 1)/(2p − 1 − k) ∈ [1/(2p), 1] (as 2p − 1 − k ≥ p), and
log(2p) ≤ A log n + log 2 (no lower bound on p is needed).
Let W_n := Π + 2κ_E = O(log n), and H_n := 4σ²h_n² + 2σ²t_n = O(log n).

## L3.1 Best truth addition (Lemma 3 of W1-T37R, re-proved on 𝒱)

**Lemma L3.1.** For S ⊆ 𝒱 with M := S₀ ∖ S ≠ ∅ there is j ∈ M with
δ²_{S,j} = Λ_S − Λ_{S∪{j}} ≥ (n − 1)φ₀⁴‖θ*_M‖²/|M| ≥ L_n. Also Λ_S ≥ (n − 1)φ₀²‖θ*_M‖² ≥ (n − 1)φ₀²θ*²_min.

*Proof.* (I − P_S)x_k = 0 for k ∈ S, so r_S = (I − P_S)μ = Σ_{k∈M} θ*_k ρ_k with ρ_k := (I − P_S)x_k. Hence
Λ_S = θ*_Mᵀ[X_Mᵀ(I − P_S)X_M]θ*_M; the bracket is the Schur complement of G_S in G_{S∪M}, whose smallest eigenvalue is
≥ λ_min(G_{S∪M}) ≥ (n − 1)φ₀² (S ∪ M ⊆ 𝒱). So Λ_S ≥ (n − 1)φ₀²‖θ*_M‖². Also Λ_S = ⟨r_S, r_S⟩ = Σ_k θ*_k⟨ρ_k, r_S⟩ ≤
‖θ*_M‖₁ max_k |⟨ρ_k, r_S⟩|, and for ρ_k ≠ 0, ⟨ρ_k, r_S⟩ = ⟨ρ_k, μ⟩ = δ_{S,k}‖ρ_k‖ with ‖ρ_k‖ ≤ ‖x_k‖ = √(n − 1)
(ρ_k ≠ 0 by the eigenvalue bound). So max_k δ²_{S,k} ≥ Λ_S²/(‖θ*_M‖₁²(n − 1)) ≥ (n − 1)φ₀⁴‖θ*_M‖⁴/‖θ*_M‖₁²
≥ (n − 1)φ₀⁴‖θ*_M‖²/|M| by Cauchy–Schwarz. Finally ‖θ*_M‖²/|M| ≥ θ*²_min, and Λ_S − Λ_{S∪{j}} = δ²_{S,j} by
Gram–Schmidt. ∎

## L3.2 States missing a truth

**Proposition L3.2.** On Ω_n, n ≥ n₀: for every S ⊆ 𝒱 with S ⊉ S₀, let j be as in L3.1 and P := S ∪ {j} ⊆ 𝒱,
E₂ := Λ_S − Λ_P ≥ L_n. Then (a) F(P) > F(S); (b) F(P) > F(A) for every neighbour A ⊄ 𝒱 of S (A = S ∪ {l} or
A = (S ∖ {i}) ∪ {l} with l ∉ 𝒱, i ∈ S). Explicitly, F(P) − F(S) ≥ L_n/(8C_R) − W_n and
F(P) − F(A) ≥ (1 − c_S)L_n/(8C_R) − W_n.

*Proof.* Put ε := (1 − c_S)/4 ∈ (0, ¼].
(a) P ⊇ S nested: r_S − r_P = (P_P − P_S)μ, ‖r_S − r_P‖² = E₂. By L1.4(a) (with Λ_S − Λ_P = E₂),
RSS_S − RSS_P ≥ E₂ − 2σh_n√E₂ − σ²t_n ≥ E₂/2 − 2σ²h_n² − σ²t_n (L1.4(c), ε = ½) ≥ E₂/4 once L_n ≥ 4H_n.
By L1.4(b) and (E6): F(P) − F(S) ≥ (E₂/4)/(2C_R) − W_n ≥ L_n/(8C_R) − W_n.
(b1) A = S ∪ {l}, l ∉ 𝒱. By (H1b), Λ_A ≥ Λ_S − ζ_n, so Λ_A − Λ_P ≥ E₂ − ζ_n; and
‖r_A − r_P‖ ≤ ‖r_A − r_S‖ + ‖r_S − r_P‖ = √(Λ_S − Λ_A) + √E₂ ≤ √ζ_n + √E₂ (r_S − r_A = (P_A − P_S)μ). By L1.4(a),(c):
RSS_A − RSS_P ≥ E₂ − ζ_n − 2σh_n(√ζ_n + √E₂) − σ²t_n ≥ (1 − ε)E₂ − (1 + ε)ζ_n − 2σ²h_n²/ε − σ²t_n.
With ζ_n ≤ c_S L_n ≤ c_S E₂ (eventually): (1 − ε)E₂ − (1 + ε)c_S E₂ = [(1 − c_S) − ε(1 + c_S)]E₂ ≥ [(1 − c_S) − 2ε]E₂
= (1 − c_S)E₂/2. Hence RSS_A − RSS_P ≥ (1 − c_S)E₂/2 − O(log n) ≥ (1 − c_S)E₂/4 for n ≥ n₀ (the O(log n) term is
(2/ε)σ²h_n² + σ²t_n with ε fixed, and E₂ ≥ L_n ≫ log n). By L1.4(b) and (E6): F(P) − F(A) ≥ (1 − c_S)L_n/(8C_R) − W_n.
(b2) A = (S ∖ {i}) ∪ {l}, i ∈ S, l ∉ 𝒱. Put S′ := S ∖ {i} ⊆ 𝒱 and E₁ := Λ_{S′} − Λ_S ≥ 0. By (H1b) at S′,
Λ_A ≥ Λ_{S′} − ζ_n, so Λ_A − Λ_P ≥ E₁ + E₂ − ζ_n. Also ‖r_A − r_P‖ ≤ ‖r_A − r_{S′}‖ + ‖r_{S′} − r_S‖ + ‖r_S − r_P‖
≤ √ζ_n + √E₁ + √E₂ (each difference is a nested projection difference: r_{S′} − r_A = (P_A − P_{S′})μ with norm²
Λ_{S′} − Λ_A ≤ ζ_n; r_{S′} − r_S = (P_S − P_{S′})μ with norm² E₁). By L1.4(a),(c) (three terms):
RSS_A − RSS_P ≥ (1 − ε)(E₁ + E₂) − (1 + ε)ζ_n − 3σ²h_n²/ε − σ²t_n ≥ (1 − c_S)E₂/2 − O(log n) ≥ (1 − c_S)E₂/4
(using E₁ ≥ 0 and the computation of (b1)). Conclude as in (b1); here |A| = |P| − 1, covered by Π. ∎

## L3.3 Supersets of S₀ inside 𝒱

**Proposition L3.3.** On Ω_n, n ≥ n₀: for every T with S₀ ⊆ T ⊆ 𝒱:
(a) for every l ∉ T with |T| < K: F(T ∪ {l}) − F(T) ≤ −½ log(n + 1) + log log n + c_v + o(1), with
c_v := v̄ log 2 + log(v̄ + 1) + 2κ_E + 1; in particular F(T ∪ {l}) < F(T);
(b) if T ≠ S₀, every e ∈ T ∖ S₀ satisfies F(T ∖ {e}) − F(T) ≥ ½ log(n + 1) − (log log n)²(1 + o(1)) − 2κ_E > 0;
(c) if T ≠ S₀, every neighbour A ⊄ 𝒱 of T satisfies F(A) < max_{e∈T∖S₀} F(T ∖ {e});
(d) (local maximum at S₀) every feasible flip or swap A of S₀ satisfies F(A) < F(S₀).

*Proof.* For T′ ∈ 𝔉 with T′ ⊇ S₀, μ ∈ span X_{S₀} ⊆ span X_{T′}, so r_{T′} = 0, Λ_{T′} = 0 and, by (1.1),
RSS_{T′} = ‖Cε‖² − ‖P_{T′}ε‖². On 𝒟₁ ∩ 𝒟₂: RSS_{T′} ≥ σ²n(1 − ω_n) with ω_n := 3n^{−1/3} + t_n/n → 0 (n ≥ n₀).
(a) RSS_T − RSS_{T∪{l}} = ‖(P_{T∪{l}} − P_T)ε‖² = σ²Z²_{T,l}. With x := σ²Z²_{T,l}/RSS_T ≤ (2 log(2^{v̄}p) + 2 log log n)/
(n(1 − ω_n)) → 0 on 𝒟₅ and −log(1 − x) ≤ x(1 + 2x) for x ≤ ¼:
ν log(RSS_T/RSS_{T∪{l}}) = −ν log(1 − x) ≤ (n/2 + 0.01)·σ²Z²_{T,l}(1 + 2x)/(σ²n(1 − ω_n)) = (Z²_{T,l}/2)(1 + o(1))
≤ log(2^{v̄}p) + log log n + o(1) (the excess is (Z²/2)·[(1 + 2x)(1 + 0.02/n)/(1 − ω_n) − 1]
= O(log n)·O(n^{−1/3} + log n/n) = o(1)). The prior term log[w(k + 1)/w(k)] = log((k + 1)/(2p − 1 − k)) ≤
log(v̄ + 1) − log p for k = |T| ≤ min(v̄, p − 1) (2p − 1 − k ≥ p). By (E6) with the determinant term −½ log(n + 1):
F(T ∪ {l}) − F(T) ≤ log(v̄ + 1) − log p − ½ log(n + 1) + log(2^{v̄}p) + log log n + 2κ_E + o(1), which is the claim.
(b) RSS_{T∖{e}} − RSS_T = ‖(P_T − P_{T∖{e}})ε‖² = σ²Z²_{T,e} ≤ σ²z_n² on 𝒟₄. So
ν log(RSS_{T∖{e}}/RSS_T) ≤ ν σ²z_n²/RSS_T ≤ z_n²(1 + o(1)). Prior: log[w(k − 1)/w(k)] = log((2p − k)/k) ≥ 0 for
1 ≤ k = |T| ≤ p. Determinant: +½ log(n + 1). By (E6), F(T ∖ {e}) − F(T) ≥ ½ log(n + 1) − z_n²(1 + o(1)) − 2κ_E.
(c) Outside neighbours of T: (c1) A = T ∪ {l}, l ∉ 𝒱: by (a), F(A) < F(T) < F(T ∖ {e}) (any e, by (b)).
(c2) A = (T ∖ {i}) ∪ {l}, l ∉ 𝒱, i ∈ T ∖ S₀: T ∖ {i} ⊇ S₀ is in the scope of (a), so F(A) < F(T ∖ {i}).
(c3) A = (T ∖ {i}) ∪ {l}, l ∉ 𝒱, i ∈ S₀: put T′ := T ∖ {i} ⊆ 𝒱; S₀ ∖ T′ = {i}, so by L3.1,
Λ_{T′} ≥ (n − 1)φ₀²θ*²_i ≥ L_n (φ₀ ≤ 1). By (H1b), Λ_A ≥ Λ_{T′} − ζ_n ≥ (1 − c_S)L_n. Compare with D := T ∖ {e},
e ∈ T ∖ S₀ (r_D = 0, Λ_D = 0, |D| = |T| − 1 = |A| − 1): by L1.4(a), RSS_A − RSS_D ≥ Λ_A − 2σh_n√Λ_A − σ²t_n
≥ Λ_A/2 − 2σ²h_n² − σ²t_n ≥ (1 − c_S)L_n/4 for n ≥ n₀; then, with k = |T|,
F(D) − F(A) ≥ log((2p − k)/k) + ½ log(n + 1) + (1 − c_S)L_n/(8C_R) − 2κ_E > 0 (the first two terms are ≥ 0).
(d) At S₀: additions (any l ∉ S₀) lose by (a) with T = S₀. Deletion of a truth i: by L3.1 applied to S₀ ∖ {i},
Λ_{S₀∖{i}} = δ² ≥ (n − 1)φ₀²θ*²_i ≥ L_n, and nested: RSS_{S₀∖{i}} − RSS_{S₀} ≥ (√Λ − σh_n)² ≥ Λ/4 ≥ L_n/4 (n ≥ n₀),
so F(S₀) − F(S₀ ∖ {i}) ≥ L_n/(8C_R) − W_n > 0. Swap i → l (any l ∉ S₀): A = (S₀ ∖ {i}) ∪ {l} ⊆ 𝒱 ∪ {l}, and
Λ_A = θ*²_i‖(I − P_A)x_i‖² ≥ (n − 1)φ₀²θ*²_i ≥ L_n (μ − θ*_ix_i ∈ span X_A; Schur complement of G_A in G_{A∪{i}},
A ∪ {i} = S₀ ∪ {l} ⊆ 𝒱 ∪ {l}). With r_{S₀} = 0: RSS_A − RSS_{S₀} ≥ Λ_A/2 − 2σ²h_n² − σ²t_n ≥ L_n/4, and
F(S₀) − F(A) ≥ L_n/(8C_R) − 2κ_E > 0. ∎

Remark (where each hypothesis enters). BM-∞ (through L_n ≫ log n) is used in L3.2 and L3.3(c3),(d); SEP only in
L3.2(b) and L3.3(c3); (H1a) for the Gram floor of 𝔉, for L3.1 and for the existence of the directions in 𝒟₄, 𝒟₅;
bounded v̄ for the polynomial size of 𝔉 and for the finiteness of the family in 𝒟₄ (the extras-deletion statistics
are O_P(1) **because** extras can only come from the deterministic sets 𝒱_n ∖ S₀ of uniformly bounded cardinality). No margin between progress and
non-progress moves inside 𝒱 is used.

**Corollary L3.4 (the event of (C2)).** On Ω_n, n ≥ n₀: for every S ⊆ 𝒱 with S ≠ S₀, every maximiser of F over
the feasible neighbours of S lies in 𝒱 and strictly exceeds F(S); and S₀ has no feasible neighbour with F ≥ F(S₀).
*Proof.* S ⊉ S₀: L3.2 (P ⊆ 𝒱 beats S and every outside neighbour). S ⊋ S₀: L3.3(b),(c). S₀: L3.3(d). ∎
