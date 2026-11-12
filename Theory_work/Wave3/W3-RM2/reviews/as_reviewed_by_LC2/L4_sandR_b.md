# L4 — The Gaussian-row sandwich at polynomial size, with a product-form leak condition: Lemma SAND-R^b (bridge (P7))

Status: **PROVED (by this seat, unchecked)**. Ticket W3-RM2; statement: `../STATEMENT.md` v1.4 §3.2 ((L-R^b)), §4
(bridge (P7)). Attempt 1 of 2 on (P7) (HQ CP2 decision). This file also carries the two riders decided by HQ: **P3**
(leak and localisation scales; CP1 decision item 2) and **T6** (product-form localisation; CP2 decision item 4) —
both are part of the lemma as stated; §7 records what each changes.
Templates (their proofs are re-run; no conclusion of them is used as an input): RM Lemma SAND-R and SAND-R′
(`Theory_work/Wave3/W3-RM/lemmas/L3_SANDR.md`, `L3b_rate.md`; polylogarithmic Q and H_l, leak C_L n^{−1/2}, localisation
rate r_n(n log n)^{1/4} → 0) and C-GROW L6.2–L6.5 (`Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:85-389`).
Inputs: `L0_toolkit_b.md` (Lemma Toolkit-b), two deterministic facts of `L1_sandF_b.md` (per-block optimality (1.1)
and the count (2.1)), and the Laurent–Massart χ² bounds: for x ≥ 0,
P(χ²_d ≥ d + 2√(dx) + 2x) ≤ e^{−x} and P(χ²_d ≤ d − 2√(dx)) ≤ e^{−x}.

## 0. Setting, hypotheses, statement

**Setting R** (`../STATEMENT.md` §1). N := n − 1, C := I − 11ᵀ/n, h_n := √(log n/n). The raw design W ∈ ℝ^{n×p} has iid
rows N(m_n, Σ), Σ = Σ_n with unit diagonal; t_j := ‖CW_j‖/√N; x_j := CW_j/t_j; Y = Xθ* + Cε with ε ~ N_n(0, σ²I)
independent of W, σ > 0 fixed; S₀ = supp θ*, s₀ = |S₀| ≥ 1 fixed, θ_lo ≤ |θ*_j| ≤ θ_hi on S₀; p ≤ n^A, A ≥ 1 fixed;
K = min(p, ⌊n/2⌋), Ω = {S : |S| ≤ K}; D0 score, prior w, block tables r_b, γ₀ as in `L0_toolkit_b.md` §0 and
`L1_sandF_b.md` §0. The partition C₁, …, C_J of [p] has blocks of size ≤ 16 and is **any measurable function of X**.
For B ⊆ [p] and a ∉ B: RSS_B := ‖(I − P_B)Y‖² and, when RSS_B > 0,

  h_{B,a} := n(RSS_B − RSS_{B∪{a}})/RSS_B.

Conditional covariances Cov(· , · | W_B) are those of one row of the Gaussian law.

**Hypotheses** (fixed constants c ∈ (0, 1], a₀ > 0, b > 0, ρ > 0; deterministic sequences ℓ_n, r_n ≥ 0):
(R-FL) λ_min(Σ_S) ≥ c for every S ⊆ [p] with |S| ≤ 16 + s₀.
(R-V) PTV(a₀): |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀ for every j ∈ S₀ and U ⊆ [p] ∖ {j} with |U| ≤ 15.
(R-Q) Q = Q_n ⊇ S₀ deterministic, q := |Q| ≤ n^b, q ≤ K, and Q = [p] or K ≥ 2q + 32s₀ + 1 for n ≥ n₀ ((L-feas)).
(R-G) **(L-gain-R)**: |Cov(W_l, W_j | W_U)| ≤ ℓ_n for every l ∉ Q, U ⊆ [p] ∖ {l} with |U| ≤ 15, j ∈ S₀ ∖ U; and
      **ℓ_n√(n/log n) → 0**.
(R-L) **(L-loc-R)**: for every l ∉ Q a deterministic H_l ⊇ {l} ∪ S₀ with |H_l| ≤ n^ρ such that, for every
      U ⊆ [p] ∖ {l} with |U| ≤ 15 and U₀ := U ∩ H_l: |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n for
      every v ∈ U ∖ H_l and j ∈ S₀ ∖ U₀; and **r_n → 0**.
(R-B) **15ρ + b < ½**.

**Lemma SAND-R^b.** Under (R-FL), (R-V), (R-Q), (R-G), (R-L), (R-B), under the joint law of (W, ε):
P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1.

Neither (T1-R), the floor on Q ∪ {l}, nor any lattice condition is used. "n ≥ n₀" means: n larger than a
threshold depending only on the fixed constants (A, s₀, σ, θ_lo, θ_hi, c, a₀, b, ρ) and the sequences ℓ_n, r_n.
Constants C₁, C₂, … depend only on the fixed constants. If Q = [p] every statement about l ∉ Q is vacuous.

## 1. Regularity (the sizes of Q and H_l and the rates ℓ_n, r_n do not enter this section)

**1.1 The covariance event.** Let W̃ := (W, ε/σ) ∈ ℝ^{n×(p+1)}: its rows are iid Gaussian with covariance
Σ̃ := diag(Σ, 1) (unit diagonal, entries in [−1, 1]). Ŝ := W̃ᵀCW̃/N. Put C_A := 8√(2A + 3) and
  E_cov := {|Ŝ_{ab} − Σ̃_{ab}| ≤ C_A h_n for all a, b ∈ [p + 1]};  E_W := the same for a, b ∈ [p] only (W-measurable).
*Claim:* P(E_covᶜ) ≤ 16n^{−3} for n ≥ n₀. *Proof.* C = OOᵀ with O ∈ ℝ^{n×N} an orthonormal basis of 1^⊥; the rows
of OᵀW̃ are iid N(0, Σ̃) (Oᵀ1 = 0 removes the mean). For a pair (a, b) and a sign ±, the coordinate ξ_a ± ξ_b of a
row has variance v_± ≤ 4, and N·(N⁻¹Σ_i(ξ_{ia} ± ξ_{ib})²)/v_± ~ χ²_N (if v_± = 0 the sum is 0). With x := (2A + 3) log n,
Laurent–Massart gives |N⁻¹Σ_i(ξ_{ia} ± ξ_{ib})² − v_±| ≤ 4(2√(x/N) + 2x/N) outside an event of probability 2e^{−x}; by
polarisation Ŝ_{ab} − Σ̃_{ab} is one quarter of the difference of the two deviations, so
|Ŝ_{ab} − Σ̃_{ab}| ≤ 2(2√(x/N) + 2x/N) ≤ C_A h_n for n ≥ n₀. Union over (p + 1)² ≤ 4n^{2A} pairs and two signs:
P(E_covᶜ) ≤ 4n^{2A}·4n^{−(2A+3)}. ∎

**1.2 Deterministic consequences on E_cov (n ≥ n₀).** For B ⊆ [p] and coordinates a, a′ of W̃ outside B write
Ŝ(a, a′ | B) := Ŝ_{aa′} − Ŝ_{aB}Ŝ_{BB}⁻¹Ŝ_{Ba′} and S(a, a′ | B) for the same expression in Σ̃ (the population conditional
covariance). Both are bilinear in (a, a′), so they extend to linear combinations of coordinates. Let
Box := {β ∈ ℝ^{S₀} : |β_k| ≤ 2θ_hi} and, for β ∈ Box, V_β := Σ_{k∈S₀}β_kW_k + ε (coordinate vector (β, σ) of W̃).
(i) *Scales.* t_j² = Ŝ_{jj} ∈ [1 − C_Ah_n, 1 + C_Ah_n]; ‖CW_j‖ ≤ 2√n; β* := (θ*_k/t_k)_{k∈S₀} ∈ Box.
(ii) *Comparison in bounded dimension.* There is C₁ such that for every D ⊆ [p] with |D| ≤ 16 + s₀, every B ⊆ D
and all a, a′ ∈ (D ∖ B) ∪ {V_β : β ∈ Box}:  |Ŝ(a, a′ | B) − S(a, a′ | B)| ≤ C₁h_n, λ_min(Ŝ_{BB}) ≥ c/2.
*Proof.* ‖Ŝ_{BB} − Σ_{BB}‖_op ≤ |B|C_Ah_n ≤ c/2, so λ_min(Ŝ_{BB}) ≥ c/2 by (R-FL), and
‖Ŝ_{BB}⁻¹ − Σ_{BB}⁻¹‖_op ≤ (2/c²)|B|C_Ah_n. The vectors Ŝ_{aB}, Σ̃_{aB} have norm ≤ 2√|B| and differ by ≤ √|B|C_Ah_n. Expanding
the difference of the two triple products gives the bound for coordinates a, a′ ∈ (D ∖ B) ∪ {ε/σ}; by bilinearity it
holds for V_β with the factor (2s₀θ_hi + σ)² (the truths k ∈ S₀ lie in D or are added to it: |D ∪ S₀| is still
≤ 16 + s₀ in every use below, where D = U ∪ {l} ∪ S₀ or D = U ∪ {j} ∪ S₀ with |U| ≤ 15). ∎
For k ∈ B: Ŝ(k, · | B) = 0 = S(k, · | B) exactly.
(iii) *Sample floors.* For 1 ≤ |S| ≤ 16 + s₀: λ_min(R̂_S) ≥ c/2 (R̂_{jk} = Ŝ_{jk}/(t_jt_k) differs from Σ_{jk} by ≤ 3C_Ah_n).
In particular every X_S with |S| ≤ 16 + s₀ has full column rank and all u_{U,l}, |U| ≤ 15, are defined.
(iv) *The response and the add statistic.* Y = Σ_{k∈S₀}θ*_kCW_k/t_k + Cε = C·V_{β*} (rowwise evaluation). Hence for
B ⊆ [p], |B| ≤ 15, a ∉ B: RSS_B = N·Ŝ(V_{β*}, V_{β*} | B) > 0, [(I − P_B)CW_a]ᵀ(I − P_B)Y = N·Ŝ(a, V_{β*} | B), and
  h_{B,a} = n·ẑ²_{B,a},  ẑ_{B,a} := Ŝ(a, V_{β*} | B)/√(Ŝ(a, a | B)·Ŝ(V_{β*}, V_{β*} | B))                    (1.1)
(the sample partial correlation of W_a and Y given W_B; (I − P_B)x_a and (I − P_B)CW_a are proportional).
β* is random, but (ii) is uniform over Box: **every bound below is proved for all β ∈ Box and then used at β*.**
Population facts used with (ii): S(a, a | B) ∈ [c, 1] for a ∈ D ∖ B; S(V_β, V_β | B) ∈ [σ², C]; S(ε, · | B) = 0 for design
coordinates.
(v) *Visibility.* For j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15: δ²_{U,j} ≥ Na₀²/4.
*Proof.* With V° := Σ_kβ*_kW_k: x_jᵀ(I − P_U)μ = (N/t_j)Ŝ(j, V° | U) and ‖(I − P_U)x_j‖² = NŜ(j, j | U)/t_j², so
δ²_{U,j} = NŜ(j, V° | U)²/Ŝ(j, j | U). By (R-V), |S(j, Σ_kθ*_kW_k | U)| ≥ a₀; replacing θ* by β* changes it by at most
s₀θ_hi·max_k|1/t_k − 1| ≤ s₀θ_hiC_Ah_n, and (ii) (D = U ∪ {j} ∪ S₀) costs 2s₀θ_hiC₁h_n. So |Ŝ(j, V° | U)| ≥ a₀ − C h_n,
Ŝ(j, j | U) ≤ Ŝ_{jj} ≤ 1 + C_Ah_n, and δ² ≥ Na₀²/4 for n ≥ n₀. ∎
(vi) *Energy.* ‖μ‖² ≤ (Σ_k|θ*_k|‖x_k‖)² ≤ s₀²θ_hi²N surely.
(i), (iii), (v), (vi) involve W only and hold on E_W.

**1.3 The score event.** Conditionally on W ∈ E_W the model is Setting F with X fixed. Apply Lemma Toolkit-b
(`L0_toolkit_b.md`) to 𝔉₁₆ := {A ⊆ [p] : |A| ≤ 16} and 𝒱𝒱₁₆ := {r_A} ∪ {r_A − r_{A′}}: (H-F) with J_n = 16; (H-G) with
φ₀² := c/2 by (iii); (H-E) with M := s₀²θ_hi² by (vi); (H-S) since log|𝔉₁₆| ≤ 16 log(p + 1) + log 17 and
log|𝒱𝒱₁₆| ≤ 2 log|𝔉₁₆| + log 2 are O(log n). Let 𝓔¹⁶ be its toolkit event: P(𝓔¹⁶ᶜ | W) ≤ 2e^{−n^{1/3}} + n^{−2} + 2/n on E_W, with
n₀ and κ_E, C_R depending only on (σ², M, c, A). (T2)–(T5) and (E6-tab) hold on it for all sets of size ≤ 16 —
whatever the realised partition, which is a function of W.
Also let 𝓩^{S₀} := {|Z_{U,j}| ≤ z_n for all j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15}, z_n² := 2(15A + 16) log n. Given W ∈ E_W these are
at most s₀(p + 1)^{15} ≤ s₀2^{15}n^{15A} standard normals, so P(𝓩^{S₀ c} | W) ≤ s₀2^{16}n^{−16}.

## 2. Selection removal in product form [T6]

**Lemma 2.** On E_cov, for n ≥ n₀, for every l ∉ Q and every U ⊆ [p] ∖ {l} with |U| ≤ 15, with U₀ := U ∩ H_l:
  |ẑ_{U,l} − ẑ_{U₀,l}| ≤ C₂ζ_n,   ζ_n := ℓ_n + r_nh_n + h_n²;                                              (2.1)
  |ẑ_{U₀,l}| ≤ C₂h_n,  |ẑ_{U,l}| ≤ C₂h_n,  hence h_{U,l} ≤ C₂² log n;                                       (2.2)
  √h_{U,l} ≤ √h_{U₀,l} + C₂ϑ_n,   ϑ_n := √n·ζ_n = √n ℓ_n + r_n√(log n) + (log n)/√n = o(√log n).              (2.3)

*Proof.* Fix l, U; V := U ∖ H_l. If V = ∅ then U = U₀ and only (2.2) needs proof (below). Let β ∈ Box. All index
sets lie in D := U ∪ {l} ∪ S₀, |D| ≤ 16 + s₀.
*Population, given W_{U₀}.* s_ll := S(l, l | U₀) ∈ [c, 1]; s_yy := S(V_β, V_β | U₀) ∈ [σ², C];
s_ly := S(l, V_β | U₀) = Σ_{j∈S₀∖U₀}β_j Cov(W_l, W_j | W_{U₀}) (truths in U₀ and the noise contribute 0), so
|s_ly| ≤ 2s₀θ_hi ℓ_n by (R-G) applied to the set U₀; c_l := S(l, V | U₀) ∈ ℝ^V with entries ≤ r_n in absolute value and
c_y := S(V_β, V | U₀) with entries ≤ 2s₀θ_hi r_n, by (R-L); S_VV := S(V, V | U₀), the Schur complement of Σ_{U₀U₀} in Σ_{UU},
so λ_min(S_VV) ≥ c by (R-FL), and its entries are ≤ 1.
*The product form.* Iterated conditioning (Schur complement of S_VV) gives
  S(l, V_β | U) = s_ly − c_lᵀS_VV⁻¹c_y,
and S(l, V_β | U) = Σ_{j∈S₀∖U}β_j Cov(W_l, W_j | W_U), which is ≤ 2s₀θ_hi ℓ_n in absolute value by (R-G) applied to the
set U. Therefore
  |c_lᵀS_VV⁻¹c_y| ≤ 4s₀θ_hi ℓ_n.                                                                          (★)
(The cross term is small because the leak bound holds at U and at U₀ — not because c_l and c_y are separately
small; (R-L) is used only to make them tend to 0.)
*Sample.* Hats denote the same objects with Ŝ in place of S. By 1.2(ii) every scalar entry differs from its
population value by ≤ C₁h_n, λ_min(Ŝ_VV) ≥ c − 15C₁h_n ≥ c/2 and ‖Ŝ_VV⁻¹ − S_VV⁻¹‖_op ≤ (2/c²)·15C₁h_n. So
‖ĉ_l − c_l‖, ‖ĉ_y − c_y‖ ≤ √15·C₁h_n, ‖c_l‖ ≤ √15 r_n, ‖ĉ_l‖, ‖ĉ_y‖ ≤ C(r_n + h_n), and
  ĉ_lᵀŜ_VV⁻¹ĉ_y − c_lᵀS_VV⁻¹c_y = (ĉ_l − c_l)ᵀŜ_VV⁻¹ĉ_y + c_lᵀ(Ŝ_VV⁻¹ − S_VV⁻¹)ĉ_y + c_lᵀS_VV⁻¹(ĉ_y − c_y)
is at most C h_n(r_n + h_n) in absolute value. With (★): |ĉ_lᵀŜ_VV⁻¹ĉ_y| ≤ C(ℓ_n + r_nh_n + h_n²) = Cζ_n. Likewise
â_l := ĉ_lᵀŜ_VV⁻¹ĉ_l ≤ C(r_n + h_n)² and â_y := ĉ_yᵀŜ_VV⁻¹ĉ_y ≤ C(r_n + h_n)².
The sample Schur identities are exact: Ŝ(l, V_β | U) = ŝ_ly − ĉ_lᵀŜ_VV⁻¹ĉ_y, Ŝ(l, l | U) = ŝ_ll − â_l,
Ŝ(V_β, V_β | U) = ŝ_yy − â_y. With ŝ_ll ≥ c/2, ŝ_yy ≥ σ²/2 and |ŝ_ly| ≤ 2s₀θ_hi ℓ_n + C₁h_n ≤ C h_n (ℓ_n ≤ h_n for n ≥ n₀):
  |ẑ_{U,l} − ẑ_{U₀,l}| ≤ |ĉ_lᵀŜ_VV⁻¹ĉ_y|/√((ŝ_ll − â_l)(ŝ_yy − â_y)) + |ŝ_ly|·|((ŝ_ll − â_l)(ŝ_yy − â_y))^{−1/2} − (ŝ_llŝ_yy)^{−1/2}|
                  ≤ Cζ_n + C h_n(r_n + h_n)² ≤ C₂ζ_n
(r_n + h_n → 0 keeps the denominators ≥ cσ²/8, and h_n(r_n + h_n)² ≤ 2(r_nh_n + h_n²)). This holds for every β ∈ Box,
in particular at β*, which is (2.1) by (1.1). |ẑ_{U₀,l}| = |ŝ_ly|/√(ŝ_llŝ_yy) ≤ C h_n; then |ẑ_{U,l}| ≤ C h_n + C₂ζ_n ≤ C₂h_n
(enlarging C₂; ζ_n ≤ 3h_n for n ≥ n₀): (2.2). (2.3) is (2.1) multiplied by √n, with √n ℓ_n = o(√log n) by (R-G) and
r_n → 0. All constants depend only on (c, s₀, θ_hi, σ, A). ∎

Because Lemma 2 is a deterministic consequence of E_cov, it applies to conditioning sets U selected by the
partition (a function of W). For l ∉ Q the **reference family** I_l := {U₀ ⊆ H_l ∖ {l} : |U₀| ≤ 15} is deterministic,
contains U ∩ H_l for every U ∌ l, and |I_l| ≤ |H_l|^{15} ≤ n^{15ρ} (a set with m − 1 elements has at most m^{15} subsets
of size ≤ 15).

## 3. The spherical tail at a deterministic conditioning set [P3]

**Lemma 3.** There are C₃, c₃ > 0 such that for n ≥ n₀, every l ∉ Q, every deterministic U₀ ⊆ [p] ∖ {l} with
|U₀| ≤ 15 and every 0 ≤ t ≤ (2A + 3) log n:
  P(E_cov ∩ {h_{U₀,l} ≥ t}) ≤ C₃ exp(−t/2 + C₃√(n log n)·ℓ_n) + C₃ exp(−c₃√n).                              (3.1)
(By (R-G), √(n log n)·ℓ_n = o(log n): the loss is n^{o(1)}. With RM's ℓ_n = C_Ln^{−1/2} it is e^{C√log n}, the source's.)

*Proof.* D := U₀ ∪ S₀; l ∉ D (l ∉ Q ⊇ S₀) and |D ∪ {l}| ≤ 16 + s₀. Regress one row of W_l on W_D in the population:
  W_l − m_l = (W_{U₀} − m_{U₀})β⁰ + Σ_{j∈S₀∖U₀}α_j[(W_j − m_j) − (W_{U₀} − m_{U₀})β_j] + e,
β_j the regression coefficient of W_j on W_{U₀}, α := Var(W_{S₀∖U₀} | W_{U₀})⁻¹Cov(W_{S₀∖U₀}, W_l | W_{U₀}), and e independent of
W_D with variance τ² := Var(W_l | W_D) ∈ [c, 1] ((R-FL) on D ∪ {l}). The conditional covariance matrix of the truths
has λ_min ≥ c and, by (R-G) at the set U₀, the covariance vector has norm ≤ √s₀ ℓ_n: ‖α‖ ≤ √s₀ ℓ_n/c. As vectors in ℝⁿ
(rows iid): e has iid N(0, τ²) entries and is independent of (W_D, ε). Let Π := (I − P_{U₀})C, the orthogonal
projector onto 𝕍 := 1^⊥ ∩ span(CW_{U₀})^⊥ (P_{U₀} and C commute because range P_{U₀} ⊆ 1^⊥), of dimension d ≥ N − 15.
Applying Π kills the constants and CW_{U₀}:
  w := (I − P_{U₀})CW_l = g + m,   g := Πe,   m := Σ_{j∈S₀∖U₀}α_jΠW_j,
and ‖m‖ ≤ ‖α‖₁·max_{j∈S₀}‖CW_j‖ ≤ (2s₀/c)√n ℓ_n =: M_n on the W_D-measurable event CN_D := {‖CW_j‖ ≤ 2√n, j ∈ S₀};
E_cov ⊆ CN_D by 1.2(i), and M_n = o(√log n).
By (1.1), h_{U₀,l} = n(wᵀr_Y)²/(‖w‖²‖r_Y‖²) with r_Y := (I − P_{U₀})Y ∈ 𝕍 (on E_cov both norms are positive; put h := 0
otherwise, which cannot enlarge the upper tail). Condition on 𝒢 := σ(W_D, ε): r_Y, m, 𝕍 and CN_D are 𝒢-measurable —
Y = Σ_{k∈S₀}θ*_kCW_k/t_k + Cε uses only W_{S₀} and ε — while g = τG with G a standard Gaussian vector of 𝕍, independent of
𝒢. **No law is asserted after conditioning on E_cov or on the scales of other columns.**
Let v := r_Y/‖r_Y‖ and ℬ := {‖G‖ ≥ √d(1 − n^{−1/4})}. Since d(1 − n^{−1/4})² ≤ d − dn^{−1/4} (n ≥ 16), the lower χ² bound
with 2√(dx) = dn^{−1/4} gives P(ℬᶜ | 𝒢) ≤ exp(−dn^{−1/2}/4) ≤ exp(−√n/8). On ℬ ∩ CN_D, for n ≥ n₀:
‖g‖ ≥ √c·√d(1 − n^{−1/4}) ≥ √(cn)/2 ≥ 2M_n, hence, with κ := 4/√c,
  √h_{U₀,l} = √n|(g + m)ᵀv|/‖g + m‖ ≤ √n(|gᵀv| + M_n)/(‖g‖ − M_n)
          ≤ (√n|Gᵀv|/‖G‖)(1 + κM_n/√n) + κM_n ≤ |Gᵀv|(1 + 4n^{−1/4}) + κM_n,
using 1/(1 − x) ≤ 1 + 2x for x ≤ ½, √(n/d)/(1 − n^{−1/4}) ≤ 1 + 3n^{−1/4} and M_n/√n = o(n^{−1/4}). Given 𝒢, Gᵀv ~ N(0, 1).
So for t ≥ 0, on CN_D,
  P(h_{U₀,l} ≥ t | 𝒢) ≤ e^{−√n/8} + 2 exp(−(√t − κM_n)₊²/(2(1 + 4n^{−1/4})²)).
For 0 ≤ t ≤ (2A + 3) log n: (√t − κM_n)₊² ≥ t − 2κM_n√((2A + 3) log n), and (1 + 4n^{−1/4})^{−2} ≥ 1 − 8n^{−1/4}, with
8n^{−1/4}t ≤ 1 for n ≥ n₀. So the exponent is ≤ −t/2 + κM_n√((2A + 3) log n) + ½, and
κM_n√((2A + 3) log n) = (8s₀c^{−3/2}√(2A + 3))·√(n log n) ℓ_n. Finally
P(E_cov ∩ {h_{U₀,l} ≥ t}) ≤ E[1_{CN_D}P(h_{U₀,l} ≥ t | 𝒢)], which is (3.1). ∎

## 4. Counting the far nulls

J(t) := #{l ∉ Q : h_{U,l} ≥ t for some U ⊆ [p] ∖ {l} with |U| ≤ 15}.

**Lemma 4.** Fix ε₀ ∈ (0, ½]. There are C₄ and a deterministic ε_n → 0 such that for n ≥ n₀ (depending also on ε₀)
and every t ∈ [ε₀ log n, (2A + 2) log n]:
  E[1_{E_cov}J(t)] ≤ C₄·p·n^{15ρ}·[exp(−t/2 + ε_n log n) + exp(−c₃√n)].                                       (4.1)
*Proof.* On E_cov, if h_{U,l} ≥ t then by (2.3) √h_{U₀,l} ≥ √t − C₂ϑ_n with U₀ = U ∩ H_l ∈ I_l; for n ≥ n₀,
C₂ϑ_n ≤ √(ε₀ log n) ≤ √t, so h_{U₀,l} ≥ t′ := (√t − C₂ϑ_n)² ≥ t − 2C₂ϑ_n√((2A + 2) log n), and 0 ≤ t′ ≤ (2A + 3) log n. Thus
1_{E_cov}J(t) ≤ Σ_{l∉Q}Σ_{U₀∈I_l}1_{E_cov}1{h_{U₀,l} ≥ t′}; take expectations, use Lemma 3 at each deterministic (l, U₀) and
|I_l| ≤ n^{15ρ}. ε_n log n := C₂ϑ_n√((2A + 2) log n) + C₃√(n log n) ℓ_n = o(log n) by (2.3) and (R-G). ∎

Two uses. Let C₀ := 4κ_E + 1 and t_n(k) := log(n + 1) + 2 log(p/k) − C₀ for 1 ≤ k ≤ K; then
log n − C₀ ≤ t_n(k) ≤ (2A + 1) log n + 1, and p·e^{−t_n(k)/2} = k e^{C₀/2}/√(n + 1). By (4.1) with ε₀ = ½:
  E[1_{E_cov}J(t_n(k))] ≤ C₅·k·n^{−1/2+15ρ+ε_n} + C₅·n^{A+15ρ}e^{−c₃√n}  uniformly in 1 ≤ k ≤ K.                 (4.2)
Let ε* := (1 − 2b − 30ρ)/2 > 0 by (R-B), and T_n := 2 log p + (30ρ + ε*) log n ∈ [ε* log n, (2A + 1) log n]. By (4.1)
with ε₀ = min(½, ε*):
  P(E_cov ∩ {J(T_n) ≥ 1}) ≤ C₄n^{15ρ}·n^{−15ρ−ε*/2+ε_n} + C₄n^{A+15ρ}e^{−c₃√n} → 0.                               (4.3)

## 5. Every maximiser has size ≤ 2k₀, k₀ := q + 16s₀

**5.1 Score conversion.** On E_cov ∩ 𝓔¹⁶, n ≥ n₀: for every block C_b, every U ⊆ C_b and l ∈ C_b ∖ U with l ∉ Q,
  log r_b(U ∪ {l}) − log r_b(U) ≤ −½ log(n + 1) + ½h_{U,l} + 2κ_E + ½.                                      (5.1)
*Proof.* U, U ∪ {l} ∈ 𝔉₁₆ lie in one block, so (E6-tab) gives the left side as
−½ log(n + 1) − ν log(RSS_{U∪{l}}/RSS_U) + (R_{U∪{l}} − R_U), and RSS_{U∪{l}}/RSS_U = 1 − h_{U,l}/n. By (2.2), h := h_{U,l} ≤ C₂² log n,
so −ν log(1 − h/n) ≤ (n/2 + 0.01)(h/n)(1 + h/n) ≤ h/2 + ½ for n ≥ n₀ (−log(1 − x) ≤ x + x², x ≤ ½). ∎

**5.2 Count.** Fix any maximiser S̃ of γ₀ on Ω; k̃ := |S̃|, Ũ_b := S̃ ∩ C_b. As in `L1_sandF_b.md` §2 (a deterministic
argument): call b good if S₀ ∩ C_b ⊆ Ũ_b (at most s₀ blocks are not), N_b := Ũ_b ∖ Q for good b; then
k̃ ≤ k₀ + 16·#{b good : N_b ≠ ∅} ((2.1) there). For good b with N_b ≠ ∅, d := |N_b|, U := Ũ_b ∖ N_b: per-block optimality
((1.1) there; removing N_b gives a smaller, feasible set) and w(k − 1)/w(k) = (2p − k)/k ≥ p/k̃ for k ≤ k̃ ≤ p give
log r_b(Ũ_b) − log r_b(U) ≥ d log(p/k̃). Add the elements l₁, …, l_d of N_b to U one at a time,
U_s := U ∪ {l₁, …, l_s}; each l_s ∉ Q, U_{s−1} ⊆ C_b ∖ {l_s}, |U_{s−1}| ≤ 15. Summing (5.1),
d log(p/k̃) ≤ Σ_s[−½ log(n + 1) + ½h_{U_{s−1},l_s} + 2κ_E + ½], so for some s:
h_{U_{s−1},l_s} ≥ log(n + 1) + 2 log(p/k̃) − 4κ_E − 1 = t_n(k̃). Then l_s is counted in J(t_n(k̃)); distinct blocks give distinct
columns. Hence, on E_cov ∩ 𝓔¹⁶, simultaneously for all maximisers:
  k̃ ≤ k₀ + 16·J(t_n(k̃)).                                                                                   (5.2)

**5.3 Ladder.** m_i := 2^{i+1}k₀ (i ≥ 0; k₀ ≥ 1). If k̃ > 2k₀ take i with m_i < k̃ ≤ 2m_i; then m_i < K, and by (5.2)
16J(t_n(k̃)) ≥ k̃ − k₀ > k̃/2 > m_i/2. t_n(·) is decreasing and J(·) is non-increasing, so
J(t_n(min(2m_i, K))) ≥ J(t_n(k̃)) > m_i/32 — an event that does not depend on the maximiser. By Markov and (4.2),
P(E_cov ∩ 𝓔¹⁶ ∩ {some maximiser has k̃ > 2k₀}) ≤ Σ_{i≥0: m_i<K}(32/m_i)[C₅·2m_i·n^{−1/2+15ρ+ε_n} + C₅n^{A+15ρ}e^{−c₃√n}]
  ≤ log₂n·[64C₅n^{−1/2+15ρ+ε_n} + 32C₅n^{A+15ρ}e^{−c₃√n}] → 0,
because 15ρ < ½ and there are at most log₂n rungs (m_i < K ≤ n/2). **The size of Q enters only through k₀ ≥ 1;
the size of H_l through the factor n^{15ρ}.**

## 6. Truths in, junk out

𝒢_n := E_cov ∩ 𝓔¹⁶ ∩ 𝓩^{S₀} ∩ {k̃ ≤ 2k₀ for every maximiser} ∩ {J(T_n) = 0}. By 1.1, 1.3 (conditional bounds integrated over
W ∈ E_W ⊇ E_cov), 5.3 and (4.3), P(𝒢_n) → 1. Work on 𝒢_n, n ≥ n₀; fix a maximiser S̃.
**(a) S₀ ⊆ S̃.** If Q = [p] then q = p ≤ K ≤ p, so K = p: either S̃ = [p] ⊇ S₀ or k̃ < K. If Q ≠ [p],
k̃ ≤ 2k₀ = 2q + 32s₀ ≤ K − 1 by (R-Q). Suppose j ∈ S₀ ∖ S̃, j ∈ C_b. Then S̃ ∪ {j} ∈ Ω, Ũ_b and Ũ_b ∪ {j} are in 𝔉₁₆, and by
(E6-tab), the prior ratio (k̃ ≤ p − 1) and (T4)(b):
log γ₀(S̃ ∪ {j}) − log γ₀(S̃) ≥ −log(2p) − ½ log(n + 1) − 2κ_E + (RSS_{Ũ_b} − RSS_{Ũ_b∪{j}})/(2C_R),
and RSS_{Ũ_b} − RSS_{Ũ_b∪{j}} = (δ_{Ũ_b,j} + σZ_{Ũ_b,j})² ≥ δ²/2 − σ²Z² ≥ Na₀²/8 − σ²z_n² by 1.2(v) and 𝓩^{S₀} (|Ũ_b| ≤ 15, j ∉ Ũ_b). The
right side is positive for n ≥ n₀: this contradicts maximality.
**(b) S̃ ⊆ Q.** Nothing to prove if Q = [p]. Otherwise let l ∈ S̃ ∖ Q, l ∈ C_b, U := Ũ_b ∖ {l} (|U| ≤ 15); S̃ ∖ {l} ∈ Ω. By
the prior ratio w(k̃ − 1)/w(k̃) = (2p − k̃)/k̃ ≥ p/k̃, (5.1) and h_{U,l} < T_n (J(T_n) = 0):
log γ₀(S̃ ∖ {l}) − log γ₀(S̃) ≥ log p − log k̃ + ½ log(n + 1) − ½T_n − 2κ_E − ½
  ≥ ½(1 − 30ρ − ε*) log n − log k̃ − 2κ_E − ½ ≥ [½(1 − 30ρ − ε*) − b] log n − log(2 + 32s₀) − 2κ_E − ½
  = (ε*/2) log n − log(2 + 32s₀) − 2κ_E − ½ > 0
for n ≥ n₀, using k̃ ≤ 2k₀ ≤ (2 + 32s₀)n^b and ½(1 − 30ρ − ε*) − b = ε*/2. This contradicts maximality.
(a) and (b) hold for every maximiser on 𝒢_n, and all improvements are strict. ∎

## 7. Records

1. **The v1.3 form implies the hypotheses** (STATEMENT §3.2, "(L-R^b-loc)"; contains RM's (L-R)). Assume (R-FL), the
   leak bound only at localised sets — |Cov(W_l, W_j | W_{U₀})| ≤ ℓ′_n for l ∉ Q, U₀ = U ∩ H_l, j ∈ S₀ ∖ U₀, with
   ℓ′_n√(n/log n) → 0 — and (R-L) with the rate r_n(n/log n)^{1/4} → 0. Then (R-G) holds with ℓ_n := ℓ′_n + 15r_n²/c.
   *Proof.* For j ∈ S₀ ∖ U (⊆ S₀ ∖ U₀), with V = U ∖ H_l:
   Cov(W_l, W_j | W_U) = Cov(W_l, W_j | W_{U₀}) − c_lᵀS_VV⁻¹c_j, c_j := Cov(W_j, W_V | W_{U₀}); |c_lᵀS_VV⁻¹c_j| ≤ |V|r_n²/c ≤ 15r_n²/c;
   and r_n²√(n/log n) → 0. ∎ RM's (L-R) is the case ℓ′_n = C_Ln^{−1/2}, r_n(n log n)^{1/4} → 0, |H_l|, |Q| polylogarithmic.
2. **Rider P3 (leak and localisation scales): succeeded.** Leak: C_Ln^{−1/2} → any ℓ_n = o(√(log n/n)). It enters
   Lemma 2 only through |ẑ_{U₀,l}| ≤ C h_n and Lemma 3 through the mean shift, ‖m‖ ≤ C√n ℓ_n = o(√log n), whose cost
   exp(C√(n log n) ℓ_n) = n^{o(1)} is absorbed by the strict inequality (R-B). Localisation in the v1.3 form:
   r_n = o((n log n)^{−1/4}) → o((log n/n)^{1/4}) (item 1). What makes this possible is that the comparison is made on
   √h with an o(√log n) error, i.e. an o(log n) error on the thresholds, instead of the source's o(1) error on h.
3. **Rider T6 (product-form localisation): succeeded.** The source bounds the cross term c_lᵀS_VV⁻¹c_y by
   ‖c_l‖‖S_VV⁻¹‖‖c_y‖ ≤ Cr_n², which forces r_n² = o(h_n) and hence, for slowly decaying designs, neighbourhoods H_l of
   polynomial size. Here the cross term is identified exactly: it is the difference of the leak covariances at U₀
   and at U ((★)). So it is enough that the leak bound holds at every conditioning set, and (R-L) is needed only
   with r_n → 0: it controls the sample error r_nh_n of the cross term, nothing else. The budget 15ρ + b < ½ stays
   in the statement, but ρ now only has to accommodate the columns whose conditional correlation with l or with a
   truth does not vanish; for designs with decaying correlations |H_l| = n^{o(1)}, every ρ > 0 is admissible and the
   budget reads b < ½, as in Form F with η = 0.
4. **Not claimed.** A leak at the exact scale ℓ_n = κ√(log n/n) with a fixed κ > 0: Lemmas 2–4 then lose a factor
   n^{C(κ)} with an explicit but non-sharp C(κ), which would give a Form R frontier "15ρ + b + C(κ) < ½"; the sharp
   constant (the analogue of β(η, A)) is not derived. The count n^{15ρ} is that of the reference family; no attempt
   is made to replace 15 by a smaller exponent.
5. **Where each hypothesis is used.** (R-FL): 1.2(ii), (iii), the Schur floors in Lemma 2, τ² ≥ c and ‖α‖ in Lemma 3
   — only on sets of size ≤ 16 + s₀. (R-V): 1.2(v) → 6(a). (R-Q): k₀, feasibility in 6(a), log k̃ ≤ b log n + O(1) in
   6(b). (R-G): (★), |ŝ_ly|, ‖α‖. (R-L): ‖c_l‖, ‖c_y‖ → 0 and the count |I_l| ≤ n^{15ρ}. (R-B): 15ρ < ½ in 5.3, and
   30ρ + 2b < 1 in (4.3)/6(b). The partition enters only through "blocks of size ≤ 16, a function of W".
6. **Uniformity over maximisers and selected blocks.** Lemma 2 and (5.1) are deterministic on E_cov ∩ 𝓔¹⁶ for all
   (l, U); the probabilistic statements (Lemma 3) are made only for deterministic pairs (l, U₀); the events in 5.3
   and (4.3) do not depend on the maximiser or on the partition.
