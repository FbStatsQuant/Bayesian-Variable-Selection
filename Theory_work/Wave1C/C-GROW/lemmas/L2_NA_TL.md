# L2 — The descent events have probability → 1 (claim (C2))

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high, reviews/R03_L0L1L2_check_sol.md):
VERIFIED-WITH-AMENDMENTS (2), applied (reviews/R03_disposition.md).
Hypotheses (minimal list, R08 item 9; (H0) and (G1) imply it): G; ‖μ‖² ≤ Mn; p ≤ n^A; |Q| ≤ C_Q log n and |Q| ≤ K;
(G2) λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p] (φ₀ ≤ 1, since normalized Gram matrices have unit diagonal); BM-∞
(used only for TL). For NA also (G4-χ) or (G4-dir). Notation: STATEMENT.md §1, L0, L1.

## L2.0 The family and the event 𝓔_n

(Amended after R03, item 1.)
𝔉 := {∅} ∪ 𝓛 ∪ {T ∪ {l} : T ∈ 𝓛, l ∉ T} ∪ {T ∖ {i} : T ∈ 𝓛, i ∈ S₀} ∪ {(T ∖ {i}) ∪ {l} : T ∈ 𝓛, i ∈ S₀, l ∉ T}.
Every nonempty A ∈ 𝔉 satisfies A ⊆ Q ∪ {l} for some l ∈ [p] (for pure deletions take l ∈ Q), so
|A| ≤ |Q| + 1 ≤ C_Q log n + 1 =: J_n ≤ C_J log n, and by (G2) and Cauchy interlacing λ_min(R̂_A) ≥ φ₀² for nonempty
A. |𝔉| ≤ 1 + 2^{|𝒫|}(1 + p + s₀ + s₀p) ≤ 5s₀ n^{C_P log 2 + A} (C_P := C_Q), so L0 applies with
D := C_P log 2 + A and 𝒱𝒱 := {r_A − r_{A′} : A, A′ ∈ 𝔉} ∪ {r_A : A ∈ 𝔉} (D_V = 2D); ∅ ∈ 𝔉 as [GEN-L1] requires.
Let 𝓔_n := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ (L0/[GEN-L1]) for this family; P(𝓔_n) → 1.

Facts used. (F1) For T ∈ 𝓛: μ ∈ span X_{S₀} ⊆ span X_T, so r_T = 0, Λ_T = 0. (F2) For T ∈ 𝓛, l ∉ T: u_{T,l} exists
((I − P_T)x_l ≠ 0 by (G2)), u_{T,l} ⊥ 1 and ⊥ span X_T, hence RSS_T − RSS_{T∪{l}} = (u_{T,l}ᵀY)² = σ²Z²_{T,l} with
Z_{T,l} := u_{T,l}ᵀε/σ ~ N(0, 1) (u ⊥ 1 gives u_{T,l}ᵀCε = u_{T,l}ᵀε; u ⊥ μ by (F1)).

## L2.1 TL

**Lemma L2.1.** On 𝓔_n, for n ≥ n₀(σ², M, φ₀, A, C_P, s₀, the BM-∞ envelope): TL(𝓛) holds. Hence P(TL(𝓛)) → 1.

*Proof.* Let T ∈ 𝓛, i ∈ S₀, and A = T ∖ {i} or A = (T ∖ {i}) ∪ {l}, l ∉ T, feasible. S₀ ∖ {i} ⊆ A, so
μ − θ*_ix_i ∈ span X_A and r_A = θ*_i(I − P_A)x_i; A ∪ {i} ⊆ Q ∪ {l}, so by the Schur complement and (G2)
Λ_A = θ*²_i‖(I − P_A)x_i‖² ≥ (n − 1)φ₀²θ*²_i ≥ (n − 1)φ₀²θ*²_min =: L′_n, and L′_n/log n → ∞ by BM-∞. With Λ_T = 0
and r_A − r_T = r_A, [GEN-L1] L1.4(a),(c) (valid by L0.1) give
RSS_A − RSS_T ≥ Λ_A − 2σh_n√Λ_A − σ²t_n ≥ Λ_A/2 − 2σ²h_n² − σ²t_n ≥ Λ_A/4 for n ≥ n₀.
By L0.2(c) and L1.4(b): F(A) − F(T) ≤ log[w(|A|)/w(|T|)] + ½ log(n + 1) + 2κ_E − (RSS_A − RSS_T)/(2C_R)
(|A| − |T| ∈ {−1, 0}; the term ½ log(n+1) bounds −½(|A| − |T|) log(n + 1)). log[w(|A|)/w(|T|)] ≤ log(2p) ≤ A log n + log 2
(L0 prior ratios; equal sizes give 0). Hence F(A) − F(T) ≤ (A + 1) log n + 1 + 2κ_E − L′_n/(8C_R) < 0 for n ≥ n₀. ∎

## L2.2 NA: the reduction to a maximal-Z condition

**Lemma L2.2.** Let c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2. On 𝓔_n ∩ {max_{T∈𝓛, l∉T} Z²_{T,l} ≤ c_n}
and n ≥ n₀, NA(𝓛) holds.

*Proof.* Let T ∈ 𝓛, |T| = k < K, l ∉ T. By L0.2(c), (F2):
F(T ∪ {l}) − F(T) = log[(k + 1)/(2p − 1 − k)] − ½ log(n + 1) + ν log(RSS_T/RSS_{T∪{l}}) + (R_{T∪{l}} − R_T).
k ≤ min(|Q|, K − 1) and K ≤ p, so 2p − 1 − k ≥ p and the prior term is ≤ log(|Q| + 1) − log p. With x := σ²Z²_{T,l}/RSS_T ≤
c_n/(n(1 − ω_n)) ≤ ¼ (n ≥ n₀; c_n = O(log n)), L0.2(b) gives ν log(RSS_T/RSS_{T∪{l}}) ≤ (Z²_{T,l}/2)(1 + ϑ_n)(1 + 2x)
≤ Z²_{T,l}/2 + ½ for n ≥ n₀ (the excess is O(log n)·(ϑ_n + log n/n) → 0). Hence
F(T ∪ {l}) − F(T) ≤ log(|Q| + 1) − log p − ½ log(n + 1) + c_n/2 + ½ + 2κ_E = −½ < 0. ∎

## L2.3 NA under (G4-χ) or (G4-dir)

**Lemma L2.3.** (a) Under (G4-χ) (|𝒫_n| ≤ (1 − δ₀) log n): P(max_{T,l} Z²_{T,l} ≤ c_n) → 1.
(b) Under (G4-dir) (|{u_{T,l} : T ∈ 𝓛, l ∉ T}| ≤ pN_n, log N_n = o(log n)): P(max_{T,l} Z²_{T,l} ≤ c_n) → 1.
Hence, with L2.2 and P(𝓔_n) → 1, P(NA(𝓛)) → 1 in both cases.

*Proof.* (a) Fix T ∈ 𝓛 and l ∉ T; put Q_l := Q ∖ {l} (so T ⊆ Q_l). Then
(I − P_T)x_l = a + b, a := (I − P_{Q_l})x_l, b := (P_{Q_l} − P_T)x_l, with a ⊥ b (P_{Q_l} − P_T is the orthogonal
projection onto span X_{Q_l} ⊖ span X_T) and a ≠ 0 (G2). By Cauchy–Schwarz, (aᵀε + bᵀε)² ≤ (‖a‖² + ‖b‖²)
[(aᵀε)²/‖a‖² + (b̂ᵀε)²] (b̂ := b/‖b‖, the second term read as 0 if b = 0), so
  Z²_{T,l} ≤ Z²_{Q_l,l} + ‖(P_{Q_l} − P_T)ε‖²/σ² ≤ Z²_{Q_l,l} + χ²_Q,  χ²_Q := ‖(P_Q − P_{S₀})ε‖²/σ²,
because range(P_{Q_l} − P_T) ⊆ range(P_Q − P_{S₀}) (S₀ ⊆ T ⊆ Q_l ⊆ Q). Here Z_{Q_l,l} = Z_{Q,l} for l ∉ Q (p − |Q|
standard normals) and Z_{Q∖{l},l} for l ∈ 𝒫 (|𝒫| standard normals): at most p standard normals in all, so with
z̄²_n := 2 log(2p) + 2 log log n, P(max Z²_{Q_l,l} > z̄²_n) ≤ p·2exp(−log(2p) − log log n) = 1/log n. χ²_Q ~ χ²_{|𝒫|} (P_Q − P_{S₀} has rank |𝒫| by (G2)); Laurent–Massart with
x = log log n: P(χ²_Q > |𝒫| + 2√(|𝒫| log log n) + 2 log log n) ≤ 1/log n. On both events, for all T, l:
Z²_{T,l} ≤ 2 log(2p) + 4 log log n + |𝒫| + 2√(|𝒫| log log n). This is ≤ c_n iff
  |𝒫| + 2√(|𝒫| log log n) + 4 log log n + 2 log 2 + 2 log(|Q| + 1) + 4κ_E + 2 ≤ log(n + 1),
which holds for n ≥ n₀ under (G4-χ) (the left side is at most (1 − δ₀) log n + O(√(log n · log log n)); R03 item 2).
(b) The family {Z_{T,l}} takes at most pN_n distinct values-as-functions (one per distinct direction), each a
standard normal. P(max Z² > 2 log(2pN_n) + 2 log log n) ≤ 1/log n. And 2 log(2pN_n) + 2 log log n ≤ c_n iff
2 log(2N_n) + 2 log log n + 2 log(|Q| + 1) + 4κ_E + 2 ≤ log(n + 1), true for n ≥ n₀ since log N_n = o(log n) and
|Q| = O(log n). ∎

**Remark (sharpness of (G4-χ)).** The bound Z²_{T,l} ≤ Z²_{Q_l,l} + χ²_Q charges every add statistic with the
noise fitted by all of 𝒫; it is attained only when x_l's residual aligns with the deleted extras' noise direction.
(G4-dir) replaces it by a count of distinct directions (L5: AR(1)). Neither is necessary; both are sufficient.
