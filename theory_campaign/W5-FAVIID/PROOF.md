# W5-FAVIID — PROOF.md: a 2^B-free favourable-regime start rate on iid block-diagonal designs, on the actual partition

Notation of `Docs/Theory/theorems/00_COMMON.md`, of the locked T22(i) STATEMENT (`Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md`)
and of W3-PXN `PROOF.md`. Every result is a **candidate**: not reviewed, not adopted. Status words are the protocol's.
"Cited" marks a result of another run or of the locked register; its status is stated where it is used.

**Cited results.**
- **[T22i]** locked T22(i-a) (PROVED-LOCKED, deterministic, any partition, positive tables): with reference S° ∈ Ω,
  s = |S°|, if q < 1 then 1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e.
- **[W1-L1.1], [W1-L1.2]**: W1-EXP Lemmas 1.1 (Q_S = RSS^y_S + c_S) and 1.2 (determinant ratio), candidate PROVED in W1-EXP,
  VERIFIED by W3-VEXP (rows 1–2). Their proofs use only λ_min(G_S) ≥ φ²(n−1) for the sets involved, never block membership
  (W3-PXN checked this; I re-read both proofs for this run and agree).
- **[C1]** (standard; W3-PXN Lemma C1): for iid N(0, Σ) rows with bounded variances and log p = o(n), the sample covariances
  (and correlations) satisfy max_{j,k}|Ŝ_jk − Σ_jk| ≤ C₁√(log p/n) w.p. → 1 (Bickel & Levina 2008, Lemma A.3). Not re-proved.
- **[PXN-Tr]**: W3-PXN Lemma Tr (candidate PROVED). I re-derive the part I need with a sharper constant (Lemma Tr′).
- **[W2-L1]**: W2-T26 Lemma 1, Δ_n := 1 − inf_φ q_φ(S₀) = max{1 − π₀(S₀), δ₁} (candidate PROVED there; it is locked T22(iv-b)
  plus the endpoints).

---------------------------------------------------------------------------------------------------------

## 0. Setting: the family FAV and new symbols

**FAV(A, g, λ₀, σ², β).** Along n → ∞:
- (F1) **Design.** Rows of X^r ∈ ℝ^{n×p} are iid N(0, Σ_n). Σ_n has unit diagonal and is **block-diagonal over a deterministic
  partition 𝒦_n of [p] into groups** K of size |K| ≤ g ≤ 16 (columns in different groups are independent), and
  λ_min(Σ_n) ≥ λ₀ > 0 for all n.
- (F2) **Dimension.** s₀ < p = p_n ≤ n^A, A ≥ 1 fixed (p fixed or p → ∞; p ≫ n allowed).
- (F3) **Response.** S₀ ⊆ [p] with |S₀| = s₀ fixed. y^r = Σ_{k∈S₀} β_k x^r_k / ŝ_k + ε, with ε ~ N(0, σ²I_n) independent of X^r,
  fixed nonzero coefficients β = (β_k) (listed in a fixed order), and ŝ_k ∈ {1, the sample SD of x^r_k} (both conventions:
  ŝ_k = sample SD is the study generator's, `gen_dev_data.R`). Only §§7–8's deletion term uses the linear form; the start
  term (Lemma B′) holds for any y^r = f_n(X^r_{S₀}, ε).
- B = B_n = min(⌊√n⌋, ⌊√p⌋, 16); the v3 partition (complete linkage on 1 − |r̂|, top-down cut at B, next-fit packing) and
  the tables r_b(U) = BF(U) as in 00_COMMON §2.

**Study instances.** S1 (Σ = I; groups = singletons, g = 1), S3 (groups of 5, equicorrelation 0.7), S4 (0.85), S6 (groups of 5,
ρ ∈ {0.4, …, 0.9} by group): all FAV with λ₀ = 1, 0.3, 0.15, 0.1. s₀ = 14, one truth per group, β = the pattern
(1.4, −1.0, 1.8, −1.2, 0.8, −1.6) × scale. S2 (AR(1)) and S5 (common factor) are **not** block-diagonal and are not covered.

**Symbols introduced here.**
- For a set U and V ⊆ [p] ∖ U: X_{U,V} := 1 − RSS_{U∪V}/RSS_U (partial R² of y on X_V given X_U; RSS_T := ‖(C − P_T)Y‖²).
- 𝒯_K := S₀ ∩ K (truths of group K). A group is *truth-carrying* if 𝒯_K ≠ ∅; h₀ := number of truth-carrying groups (≤ s₀).
- **Q_n** := {every v3 block is a union of whole groups of 𝒦_n}; **Q_n(m)** := Q_n ∩ {every block meets at most m
  truth-carrying groups}.
- 𝒲_K(m) := {S₀ ∩ (K₁ ∪ … ∪ K_i) : 0 ≤ i ≤ m−1, K₁,…,K_i distinct truth-carrying groups ≠ K}; |𝒲(m)| := max_K |𝒲_K(m)|
  ≤ Σ_{i=0}^{m−1} C(h₀, i).
- t_n := 2(1+ε₀) log N_n for a fixed ε₀ > 0, where N_n is the size of the truncation family used (stated in each theorem;
  always N_n ≤ C n^A); τ_n := t_n/n; **ξ_n := √(t_n/(2(n+1)))** = √((1+ε₀)log N_n/(n+1)).
- **c_ML := min_{c>0} c·E_{1/2}(1/c) = 3.8311** (at c = 1.684), where E_{1/2}(x) := Σ_{j≥0} x^j/Γ(j/2+1) = e^{x²}erfc(−x)
  (Mittag-Leffler function; only the numerical value of the convergent series at x = 1/1.684 is used, checked in
  `scripts/sanity.py`, item 3).
- v_T := σ² + Var(β'x_{S₀} | x_T) (population, per row), v_∅ := σ² + β'Σ_{S₀}β; **x₁ := λ₀ min_k β_k² / v_∅**.

---------------------------------------------------------------------------------------------------------

## 1. Lemma X⁺ (one-sided chain-free table bound; the EXP′ remainder is ≤ O(1/n) from above) — PROVED

**Statement.** Fix any data (X, y) (standardised as in 00_COMMON), sets U ⊊ A ⊆ [p], j := |A ∖ U|, and φ ∈ (0, 1] with
λ_min(G_A) ≥ φ²(n−1) and (n+1)φ² ≥ 50. Then

  log BF(A) − log BF(U) ≤ −(j/2) log(n+1) − ν log(RSS_A/RSS_U) + κ⁺,
  κ⁺ := j(1 + φ^{−2})/(2φ²(n−1)) + ν/((n+1)φ² RSS^y_U).

Equivalently BF(A)/BF(U) ≤ e^{κ⁺}(n+1)^{−j/2}(1 − X_{U,A∖U})^{−ν}. Since r_b(U) = BF(U), this bounds every table ratio
r_b(A)/r_b(U), U ⊂ A ⊆ C_b, with no chain and no EXP′ constant.

**Proof.** BF(A)/BF(U) = (D_A/D_U)^{−1/2} [(0.02 + Q_A)/(0.02 + Q_U)]^{−ν}.
*Determinant.* Take any chain U = T₀ ⊂ T₁ ⊂ … ⊂ T_j = A adding one index at a time. By Cauchy interlacing every T_i satisfies
λ_min(G_{T_i}) ≥ φ²(n−1) (T_i ≠ ∅). [W1-L1.2] gives log D_{T_i} − log D_{T_{i−1}} ≥ log(n+1) − (1+φ^{−2})/(φ²(n−1)) at each step.
Summing, (D_A/D_U)^{−1/2} ≤ (n+1)^{−j/2} exp(j(1+φ^{−2})/(2φ²(n−1))).
*Q part.* [W1-L1.1]: for nonempty S with λ_min(G_S) ≥ φ²(n−1), 0.02 + Q_S = RSS^y_S + a_S with
a_S = 0.02 + t_S/(n+1) + nτ_S/(n+1), where t_S = y'P_S y and 0 ≤ τ_S ≤ 1/((n+1)φ²); for S = ∅, a_∅ = 0.02 (t = τ = 0).
Because U ⊆ A, P_U ≼ P_A and t_A ≥ t_U, so a_A − a_U ≥ −nτ_U/(n+1) ≥ −δ, δ := 1/((n+1)φ²) ≤ 0.02 ≤ a_U.
Write R_U := RSS^y_U ≥ R_A := RSS^y_A > 0. Then
  (R_U + a_U)/(R_A + a_A) ≤ (R_U + a_U)/(R_A + a_U − δ) ≤ (R_U + δ)/R_A,
where the last step is equivalent (cross-multiplying positive quantities) to 0 ≤ (a_U − δ)(R_U − R_A + δ), true because
a_U ≥ δ and R_U ≥ R_A. Hence [(0.02+Q_A)/(0.02+Q_U)]^{−ν} ≤ (R_U/R_A)^ν(1 + δ/R_U)^ν ≤ (RSS_A/RSS_U)^{−ν}e^{νδ/R_U}
(R_U/R_A = RSS_U/RSS_A: the response scaling cancels). Multiply. ∎

*Remarks.* (1) Numerically checked on 6,000 random (U, A) pairs, including high-SNR and strongly correlated designs:
max(R⁺ − κ⁺) = −0.005 ≤ 0 (`results/sanity.txt`, item 2). (2) This explains W1-EXP's observation that the EXP′ remainder is
O(1) (κ_EXP ≈ 100–1,700 nats at study SNR, W3-VEXP R1): the O(1) part is **nonpositive** — it only *lowers* table ratios — so
every upper bound on start mass off the reference can drop it. (3) The lower bound needed for deletions is Lemma X⁻.

**Lemma X⁻ (lower bound; PROVED).** Same hypotheses. Then
  log BF(A) − log BF(U) ≥ −(j/2)log(n+1) − ν log(RSS_A/RSS_U) − κ⁻,  κ⁻ := j(1+φ^{−2})/(2φ²(n−1)) + 1.03ν/RSS^y_A.
*Proof.* [W1-L1.2] two-sided gives (D_A/D_U)^{−1/2} ≥ (n+1)^{−j/2}e^{−j(1+φ^{−2})/(2φ²(n−1))}. And
(R_U + a_U)/(R_A + a_A) ≥ R_U/(R_A(1 + a_A/R_A)), so [(0.02+Q_A)/(0.02+Q_U)]^{−ν} ≥ (RSS_U/RSS_A)^ν e^{−νa_A/R_A}, with
a_A ≤ 0.02 + (n−1)/(n+1) + n/((n+1)²φ²) ≤ 1.03 when (n+1)φ² ≥ 50. ∎

---------------------------------------------------------------------------------------------------------

## 2. Lemma B′ (exact Beta law for any fixed group-union and any outside conditioning set) — PROVED

**Statement.** Assume (F1) and y^r = f(X^r_{S₀}, ε) for a measurable f, ε independent of X^r. Let Γ ⊆ [p] be a fixed union of
groups of 𝒦_n, W ⊆ [p] ∖ Γ a fixed set, U := (S₀ ∩ Γ) ∪ W, and V ⊆ Γ ∖ S₀ fixed and nonempty with m := n − 1 − |U| > |V|.
Then X_{U,V} ~ Beta(|V|/2, (m − |V|)/2), and X_{U,V} is independent of (X^r_U, y^r).

**Proof.** Put T := S₀ ∩ Γ and W^r := X^r_V − X^r_T Γ_V with Γ_V := Σ_{TT}^{−1}Σ_{TV} (population regression; Γ_V := 0 if T = ∅).
*Independence.* Group-wise independence (F1) makes the columns of Γ independent of (X^r_{[p]∖Γ}, ε). Within Γ, (W^r, X^r_T) is
jointly Gaussian (row-wise) with Cov(W^r, X^r_T) = 0, hence W^r ⊥ X^r_T. Combining the two (for independent pairs
(Z₁, Z₂) ⊥ Z₃ with Z₁ ⊥ Z₂: P(Z₁∈a, Z₂∈b, Z₃∈c) = P(Z₁∈a)P(Z₂∈b)P(Z₃∈c)), W^r ⊥ (X^r_T, X^r_{[p]∖Γ}, ε). Since U ⊆ T ∪ ([p]∖Γ),
S₀ ⊆ T ∪ ([p]∖Γ) and y^r = f(X^r_{S₀}, ε), W^r is independent of (X^r_U, y^r). Rows are iid, so the n × |V| matrix W^r equals
G Σ_{V|T}^{1/2} with G an iid N(0,1) matrix independent of (X^r_U, y^r), and Σ_{V|T} ≻ 0 (λ_min(Σ) ≥ λ₀).
*Geometry.* X_V = C X^r_V D_V^{−1} (centring and positive column scaling). Since T ⊆ U, (C − P_U)CX^r_T = 0, so
span((C − P_U)X_V) = span((C − P_U)W^r) = span((C − P_U)G). Let E := range(C − P_U), of dimension m a.s., and r := (C − P_U)Y;
both are functions of (X^r_U, y^r), and r ≠ 0 a.s. With Q_E an orthonormal basis of E, Q_E'G is an m × |V| iid N(0,1) matrix
given (X^r_U, y^r), so span((C−P_U)G) is a uniformly (Haar) distributed |V|-plane of E, of full dimension a.s. Since
C − P_{U∪V} = (C − P_U) − P_{span((C−P_U)X_V)}, X_{U,V} = ‖P_{span}r‖²/‖r‖², the squared length of the projection of a fixed unit
vector of E on a uniform |V|-plane: Beta(|V|/2, (m − |V|)/2), whatever the conditioning values. ∎

*Remarks.* (1) This is W3-PXN Lemma B(i) with two generalisations: W may be **any** fixed set outside Γ (in particular the truths
of other groups that happen to share a block), and y may be any function of (X_{S₀}, ε) (so the generator's sample-SD signal
convention is covered exactly). (2) KS checks for three (Γ, W, V) configurations in an S3-like design, generator convention:
p = 0.71, 0.77, 0.73 (`results/sanity.txt`, item 5).

---------------------------------------------------------------------------------------------------------

## 3. Lemma Tr′ (truncated moment and truncation event) — PROVED

Let X ~ Beta(j/2, (m−j)/2), m = n − 1 − u, 1 ≤ j, u ≥ 0, j + u ≤ 2B + s₀, ν = 0.01 + n/2, τ ∈ (0, ½].
(a) E[(1 − X)^{−ν} 1{X ≤ τ}] ≤ (1 − τ)^{−e₁}(mτ/2)^{j/2}/Γ(j/2 + 1), e₁ := (u + j + 3)/2 + 0.01.
(b) Let 𝔉_n be a family of N_n such variables (any dependence), with N_n → ∞ and N_n ≤ Cn^A. With τ_n = t_n/n,
    t_n = 2(1+ε₀)log N_n: P(max_{𝔉_n} X > τ_n) → 0.

*Proof.* (a) is W3-PXN Lemma Tr(a) before its last crude step: the integrand is x^{j/2−1}(1−x)^{−e₁}/B(j/2,(m−j)/2), and
(1−x)^{−e₁} ≤ (1−τ)^{−e₁} on [0, τ]; ∫₀^τ x^{j/2−1}dx = (2/j)τ^{j/2}; 1/B(j/2,(m−j)/2) ≤ (m/2)^{j/2}/Γ(j/2) (Wendel / integer case,
as in [PXN-Tr]). Keeping (1−τ)^{−e₁} instead of 2^{e₁} is the only change; for τ = τ_n it is 1 + O(B log n/n).
(b) X = A/(A + A′), A ~ χ²_j ⊥ A′ ~ χ²_{m−j}. X > τ ⟺ A(1−τ) > τA′. Let δ_n := n^{−1/3}. Laurent–Massart's lower tail with
x = (m−j)δ_n²/4 gives P(A′ < (m−j)(1−δ_n)) ≤ exp(−(m−j)n^{−2/3}/4) = exp(−Θ(n^{1/3})). On the complement X > τ_n forces
A > s_n := τ_n(m−j)(1−δ_n) = t_n(1 − O(n^{−1/3})). Laurent–Massart's upper tail P(A ≥ j + 2√(jx) + 2x) ≤ e^{−x} with
x := s_n/2 − √(j s_n) − j gives P(A > s_n) ≤ exp(−t_n/2 + O(√(log n))) = N_n^{−(1+ε₀)}e^{O(√log n)}. A union bound:
N_n[N_n^{−(1+ε₀)}e^{O(√log n)} + e^{−Θ(n^{1/3})}] → 0. ∎

---------------------------------------------------------------------------------------------------------

## 4. Lemma M (a B-free bound for the aggregation statistic D) — PROVED

**Statement.** Let a₁, …, a_N ≥ 0 be random, N ≥ 1, and suppose E[j! a_j] ≤ C₀(Nξ)^j/Γ(j/2 + 1) for j = 1, …, N, with C₀ ≥ 1,
ξ > 0. Then D := max_{1≤j≤N}(j! a_j)^{1/j} satisfies E D ≤ c_ML·C₀·Nξ, c_ML = 3.8311.

**Proof.** Put Y_j := (j!a_j)^{1/j}. For λ > 0, y ≥ 0 and j ≥ 1: y ≤ λ if y ≤ λ, and y ≤ λ(y/λ)^j if y > λ. Hence
max_j Y_j ≤ λ(1 + Σ_{j=1}^N (Y_j/λ)^j), and E D ≤ λ + λΣ_j E[j!a_j]/λ^j ≤ λ + λC₀Σ_{j≥1}(Nξ/λ)^j/Γ(j/2+1). With λ := cNξ,
E D ≤ C₀Nξ · c(1 + Σ_{j≥1}c^{−j}/Γ(j/2+1)) = C₀Nξ · c E_{1/2}(1/c). Take c = 1.684. ∎

*Remark.* W3-PXN bounded D ≤ Σ_j(j!a_j)^{1/j} and lost a factor of order g (plus 2^{g+3} from Lemma Tr's crude constant); the
locked T22(iii) loses 2^B through its sum over T ⊆ C_b. Lemma M loses only the absolute constant 3.83.

---------------------------------------------------------------------------------------------------------

## 5. Lemma S (projection onto a sum of nearly orthogonal subspaces) — PROVED

**Statement.** Let A₁, …, A_r be subspaces of ℝⁿ with ‖P_{A_i}P_{A_k}‖ ≤ c for i ≠ k and (r−1)c < 1. For every vector y,
  ‖P_{A₁+⋯+A_r} y‖² ≤ (1 − (r−1)c)^{−1} Σ_i ‖P_{A_i} y‖².

**Proof.** Any x ∈ A₁ + ⋯ + A_r is x = Σ a_i with a_i ∈ A_i, and |⟨a_i, a_k⟩| = |⟨P_{A_i}a_i, P_{A_k}a_k⟩| ≤ c‖a_i‖‖a_k‖, so
‖x‖² ≥ Σ‖a_i‖² − cΣ_{i≠k}‖a_i‖‖a_k‖ ≥ (1 − (r−1)c)Σ‖a_i‖² (since Σ_{i≠k}‖a_i‖‖a_k‖ ≤ (r−1)Σ‖a_i‖²). Then
‖P_{ΣA}y‖ = sup_{‖x‖=1}⟨x, y⟩ = sup Σ⟨a_i, P_{A_i}y⟩ ≤ sup (Σ‖a_i‖²)^{1/2}(Σ‖P_{A_i}y‖²)^{1/2} ≤ (1 − (r−1)c)^{−1/2}(Σ‖P_{A_i}y‖²)^{1/2}. ∎
(2,000 random checks, 0 violations: `results/sanity.txt`, item 4.)

---------------------------------------------------------------------------------------------------------

## 6. Lemma G (partition-free good events) — PROVED (given [C1])

Under FAV, put ε_n := C₁√(log p/n) and let k₀ := 2g + s₀. Each event below has probability → 1. **None refers to the v3
partition.**
(G1) **SE on small sets.** λ_min(R̂_T) ≥ φ₀² := λ₀/2 for every T with |T| ≤ max(B, k₀) (hence for every T inside any block).
(G2) **RSS floor.** RSS^y_T ≥ c_* n for every T with |T| ≤ B and for every T ⊆ S₀, with c_* := σ²/(5v_∅).
(G3) **Angles.** For all distinct groups K ≠ K′ and all U ⊆ S₀: with A := (C − P_U)span X_{K∖S₀}, A′ := (C − P_U)span X_{K′∖S₀},
     ‖P_A P_{A′}‖ ≤ c_n := C_G ε_n, C_G = C_G(λ₀, k₀).
(G4) **Visibility.** Let 𝔙 be the family of pairs (U, W) with W ⊆ S₀ nonempty, U ∩ W = ∅, |U ∪ W| ≤ B, such that U ∪ W ⊆ Γ for
     some union Γ of groups with S₀ ∩ Γ ⊆ U ∪ W. Then min_{(U,W)∈𝔙} X_{U,W}/|W| ≥ x₁/2.
(G5) **Truncation.** For a fixed (partition-free) family of triples (Γ, W, V) as in Lemma B′, of size N_n ≤ Cn^A, all
     X_{U,V} ≤ τ_n (Lemma Tr′(b)).

**Proof.** (G1) [C1] and ‖R̂_T − Σ_T‖_op ≤ |T|·max|r̂_jk − Σ_jk| (Frobenius) give λ_min(R̂_T) ≥ λ₀ − |T|ε_n ≥ λ₀/2 eventually
(λ_min(Σ_T) ≥ λ₀ by interlacing).
(G2) Under either convention μ := CX^r_{S₀}(β/ŝ) ∈ span X_{S₀}. For any T, W_T := span(X_T, X_{S₀}) ∋ μ has dimension
≤ |T| + s₀, and (W1-EXP Lemma 1.4's argument) RSS_T ≥ ‖(C − P_{W_T})Y‖² = ‖Cε‖² − ‖P_{W_T}ε‖². Given X,
‖P_{W_T}ε‖²/σ² ~ χ²_{≤B+s₀} and E e^{χ²_k/4} = 2^{k/2}; a union bound over the ≤ p^B + 2^{s₀} sets T gives
max_T ‖P_{W_T}ε‖² ≤ Lσ² log n w.p. → 1 for a fixed L > 4AB + 4. With ‖Cε‖² ≥ (3/4)σ²(n−1) w.p. → 1, RSS_T ≥ σ²n/2.
‖Y‖² = ‖μ‖² + 2μ'ε + ‖Cε‖² ≤ 2n v_∅ w.p. → 1 by the SLLN on the finitely many columns X^r_{S₀} (‖μ‖²/n → β'Σ_{S₀}β,
ŝ_k → 1 a.s.). Hence RSS^y_T = (n−1)RSS_T/‖Y‖² ≥ σ²(n−1)/(4v_∅) ≥ c_*n for n ≥ 5.
(G3) For T := (K∖S₀) ∪ (K′∖S₀) ∪ U (|T| ≤ k₀), the cosine matrix between A and A′ is Ŝ₁₁^{−1/2}Ŝ₁₂Ŝ₂₂^{−1/2}, where Ŝ is the Schur
complement of R̂_T with respect to U. Its population counterpart has S₁₂ = −Σ_{aU}Σ_{UU}^{−1}Σ_{Ub} = 0 (Σ_{aU} is supported on
U ∩ K, Σ_{Ub} on U ∩ K′, and Σ_{UU}^{−1} is block-diagonal over groups; Σ_{ab} = 0 across groups), and λ_min(S_ii) ≥ λ₀.
On (G1), the Schur complement is Lipschitz in R̂_T with a constant depending on (λ₀, k₀) only, so ‖Ŝ − S‖ ≤ C k₀ε_n and
‖P_AP_{A′}‖ ≤ ‖Ŝ₁₂‖/(λ₀ − Ck₀ε_n) ≤ C_Gε_n. [C1] controls all entries at once, so no union over (K, K′, U) is needed.
(G4) Population: for (U, W) ∈ 𝔙 the truths outside U ∪ W lie outside Γ, so they are independent of x_{U∪W}, and
v_U − v_{U∪W} = β'_W Σ_{W|U} β_W ≥ λ₀‖β_W‖² ≥ |W|λ₀ min β_k² (Schur complement eigenvalue ≥ λ_min(Σ)), while v_U ≤ v_∅. Hence
x^pop(U, W) := 1 − v_{U∪W}/v_U ≥ |W|x₁. Sample: apply [C1] to the (p+1)-dimensional Gaussian rows (x^r, y⁰), y⁰ := x^r_{S₀}'β + ε;
for every T with |T| ≤ B the sample residual variance v̂⁰_T := RSS⁰_T/(n−1) is a Lipschitz function of the sample covariance
entries on (G1), so max_{|T|≤B}|v̂⁰_T − v_T| = O(Bε_n) → 0 uniformly. The actual y differs from y⁰ by X^r_{S₀}(β/ŝ − β), and
|β/ŝ − β| = O_P(n^{−1/2}) (finitely many columns), so the actual RSS_T/(n−1) is within o_P(1) of v̂⁰_T uniformly in T. Since
v_T ≥ σ² > 0, X_{U,W} = 1 − RSS_{U∪W}/RSS_U ≥ |W|x₁ − o_P(1) uniformly on 𝔙, and |W| ≥ 1 gives (G4).
(G5) Lemma B′ gives each variable an exact Beta law with j + u ≤ 2B + s₀; Lemma Tr′(b). ∎

---------------------------------------------------------------------------------------------------------

## 7. Theorem A (fixed partition; the 2^B-free favourable rate) — PROVED (given [C1], [T22i], [W1-L1.1–1.2])

**Statement.** Assume FAV and let 𝒫_n be a **deterministic** partition of [p] into blocks of size ≤ B_n, each block a union of
groups of 𝒦_n. Let P_n := {the v3 partition equals 𝒫_n}. Let q̃, ẽ be the T22(i) quantities at the reference S₀ computed on
𝒫_n (they coincide with the actual q, e on P_n: an identity of random variables, so no conditioning on P_n is used).
Assume s₀ ≤ K eventually. Then, with N_n := Σ_b 2^{|C_b|} ≤ 2^B p and t_n, ξ_n as in §0:
(A1) on an event 𝒢_n with P(𝒢_n) → 1, E[q̃ 1_{𝒢_n}] ≤ c_ML C_{0,n} ξ_n, with C_{0,n} → 1 explicit (in the proof);
(A2) ẽ ≤ 2p√(n+1) e^{κ_e} exp(−νx₁/2) on 𝒢_n, with κ_e := (1+φ₀^{−2})/(2φ₀²(n−1)) + 1.03ν/(c_*n) → 0.52/c_* = 2.6v_∅/σ²
     (an SNR-dependent O(1) prefactor, harmless against the exponential factor; finite-n values are computed exactly in §4);
(A3) consequently, for every M > 0 and η > 0,
     limsup_n P(P_n ∩ {1 − π₀(S₀) > (1+η) M (s₀+1) c_ML ξ_n}) ≤ 1/M,
     i.e. 1_{P_n}(1 − π₀(S₀)) = O_P((s₀+1)·√(log n/n)), with leading constant (s₀+1)·3.83·√((1+ε₀)A).
**The constant does not depend on B or g** except through lower-order terms: t_n = 2(1+ε₀)log N_n ≤ 2(1+ε₀)(log p + B log 2)
and C_{0,n} = 1 + O((B + s₀)log n/n). For comparison, W3-PXN P3 had 2.3·2^{g+3}gξ_n and the locked T22(iii) 2^B√(log n)n^{−κ}.

**Proof.** Let 𝒢_n := (G1) ∩ (G2) ∩ (G4) ∩ (G5) for the family {(C_b, ∅, V) : b ∈ 𝒫_n, ∅ ≠ V ⊆ C_b ∖ S₀} (Lemma B′ with
Γ = C_b, W = ∅, U = U_b* := S₀ ∩ C_b), of size ≤ N_n. P(𝒢_n) → 1 by Lemma G.
*Single subset.* For a block b and V ⊆ C_b ∖ S₀, |V| = j ≥ 1, Lemma X⁺ with U = U_b*, A = U_b* ∪ V and φ = φ₀ (G1) gives
  r_b(U_b*∪V)/r_b(U_b*) ≤ e^{κ⁺}(n+1)^{−j/2}(1 − X_{U_b*,V})^{−ν},
and on (G2) κ⁺ ≤ κ̄_n := B(1+φ₀^{−2})/(2φ₀²(n−1)) + ν/((n+1)φ₀²c_*n) = O(1/n).
*Truncated moments.* On 𝒢_n every X_{U_b*,V} ≤ τ_n, so a_bj = ã_bj := Σ_{|V|=j}(ratio)·1{X ≤ τ_n}. By Lemma B′,
X_{U_b*,V} ~ Beta(j/2, (m−j)/2), m = n−1−|U_b*|, and Lemma Tr′(a) with mτ_n ≤ t_n gives
  E[ã_bj 1_{𝒢_n}] ≤ C(N_b, j)·e^{κ̄_n}(1−τ_n)^{−e₁}(n+1)^{−j/2}(t_n/2)^{j/2}/Γ(j/2+1),  N_b := |C_b ∖ S₀|,
so E[j!ã_bj1_{𝒢_n}] ≤ C_{0,n}(N_bξ_n)^j/Γ(j/2+1) with C_{0,n} := e^{κ̄_n}(1−τ_n)^{−(2B+s₀+3)/2−0.01} → 1
(j!C(N,j) ≤ N^j). (Here the "random variables" of Lemma M are a_j1_{𝒢_n}; the bound on a_bj holds on 𝒢_n.)
*Lemma M* gives E[D_b 1_{𝒢_n}] ≤ c_ML C_{0,n} N_b ξ_n, and since Σ_b N_b = p − s₀, E[q̃1_{𝒢_n}] ≤ c_ML C_{0,n}ξ_n: (A1).
*(A2).* ẽ = 2p max{[r_b(U)/r_b(U ∪ U_b*)]^{1/a}: b, U ⊆ C_b, a = |U_b*∖U| > 0}. For such (b, U) put W := U_b* ∖ U (so a = |W|).
Then W ⊆ S₀ is nonempty, U ∩ W = ∅, U ∪ W ⊆ C_b, |U ∪ W| ≤ B, and S₀ ∩ C_b = U_b* ⊆ U ∪ W with C_b a union of groups: (U, W) ∈ 𝔙.
Lemma X⁻ with A = U ∪ W and φ = φ₀ ((n+1)φ₀² ≥ 50 eventually):
[r_b(U)/r_b(U∪W)]^{1/a} ≤ (n+1)^{1/2}e^{κ⁻/a}(1 − X_{U,W})^{ν/a} ≤ (n+1)^{1/2}e^{κ⁻/a}exp(−νX_{U,W}/a), with
κ⁻/a ≤ (1+φ₀^{−2})/(2φ₀²(n−1)) + 1.03ν/RSS^y_{U∪W} ≤ κ_e by (G2) (|U ∪ W| ≤ B). (G4) gives X_{U,W}/a ≥ x₁/2. Hence
ẽ ≤ 2p√(n+1)e^{κ_e}e^{−νx₁/2}: (A2); it is o(n^{−k}) for every k since p ≤ n^A.
*(A3).* On P_n, q = q̃ and e = ẽ (identity). Markov: P(𝒢_n ∩ {q̃ > Mc_MLC_{0,n}ξ_n}) ≤ 1/M. On 𝒢_n ∩ {q̃ ≤ Mc_MLC_{0,n}ξ_n},
q̃ → 0, so [T22i] applies (q < 1) and 1 − π₀(S₀) ≤ (s₀+1)q̃/(1−q̃) + s₀ẽ ≤ (1+η)M(s₀+1)c_MLξ_n for n large (ẽ = o(ξ_n),
C_{0,n} → 1, q̃/(1−q̃) ≤ (1+η/2)q̃). Finally P(𝒢_n^c) → 0. ∎

*When does P(P_n) → 1?* (i) Groups of size g with g ≤ B < 2g and within-group correlations bounded away from all cross-group
correlations: blocks = groups w.p. → 1 (W3-PXN Lemma P1, same proof; asymptotically 9 ≤ g ≤ 16). This is the LH-like
favourable family (LH-iid with c = 0). (ii) **Not** for the study's groups of 5 (B ∈ {14, 15, 16}): there is no deterministic
limit partition (§8, Proposition N); Theorem B handles that case.

---------------------------------------------------------------------------------------------------------

## 8. The study's group structure: blocks are unions of whole groups, but the packing has no limit

### Lemma P1′ (union of groups w.p. → 1) — PROVED (given [C1])
**Statement.** Assume FAV with every group of size ≤ min_n B_n and **ρ₋ := min over pairs (j, k) in a common group of |Σ_jk| > 0**.
Then P(Q_n) → 1. Every block is a union of at most ⌊B/g_min⌋ groups, so Q_n ⊆ Q_n(m) with m := min(h₀, ⌊B/g_min⌋).
For S3, S4, S6 (g = 5): m = 2 when B = 14 (n ∈ [196, 224]) and m = 3 when B ∈ {15, 16}. For S1 (groups = singletons),
Q_n holds surely and m ≤ min(s₀, B).

**Proof.** Let D_in := max within-group distance 1 − |r̂_jk| and D_out := min cross-group distance. By [C1], w.p. → 1
D_in ≤ 1 − ρ₋ + ε_n < 1 − ε_n ≤ D_out. On {D_in < D_out}: (a) *laminarity* — by induction on merges (W3-PXN Lemma P1(a)):
while some group is not yet one cluster, two of its clusters are at complete-linkage distance ≤ D_in, whereas clusters inside
different groups are at distance ≥ D_out, so the next merge is inside a group; hence every group is a dendrogram node and every
node is either inside one group or a union of whole groups. (b) *Cut* — a retained node R ⊊ K (K a group) would have K as an
ancestor; K has size ≤ B and is visited first by the top-down traversal, which stops there. So every retained cluster is a
union of whole groups. (c) *Packing* concatenates whole retained clusters, so every block is a union of whole groups, and its
size ≤ B bounds the number of groups. ∎
*(S6 at n = 200: ρ₋ = 0.4 is close to the cross-group noise level √(4 log p/n) ≈ 0.35–0.37; empirically Q_n held in every design
I generated, §Evidence of REPORT.)*

### Proposition N (no deterministic limit partition for S3/S4) — PROOF SKETCH
**Statement.** In S3/S4 (all groups identically distributed), for any two fixed groups K ≠ K′,
P(K and K′ lie in the same retained cluster) ≤ (m−1)/(G−1), G = p/5; and the number of distinct block partitions over
independent replicates does not stabilise. In particular W3-VEXP R3's device "P_n = {partition = a fixed union of groups}"
with P(P_n) → 1 is not available for g = 5.
*Sketch.* On {D_in < D_out} the retained-cluster partition is determined by the group-level complete-linkage dendrogram on the
distances d(K, K′) = 1 − min_{a∈K,b∈K′}|r̂_ab|, which (no ties a.s.) is equivariant under relabelling groups; the group-level law
is exchangeable, so the partition of groups into retained clusters is an exchangeable random partition with blocks of ≤ m
groups, and each fixed pair is co-clustered with probability E[#co-clustered pairs]/C(G,2) ≤ G(m−1)/2/C(G,2). The packing
step (next-fit in leaf order, which depends on indices through the R13 left-child rule) is not equivariant; that is why this is
a sketch. Numerically (REPORT §4.2), two independent designs at the same n share almost no co-blocked group pairs at any n. ∎

---------------------------------------------------------------------------------------------------------

## 9. Theorem B (the actual, noise-dependent packing; uniform over packings) — PROVED (given [C1], [T22i], [W1-L1.1–1.2])

**Statement.** Assume FAV and s₀ ≤ K eventually. Fix m ≥ 1. Let N_n := Σ_K |𝒲_K(m)|·2^{|K|} ≤ |𝒲(m)|2^g p. Then there are a
partition-free event 𝒢′_n with P(𝒢′_n) → 1 and a partition-free random variable Q̄_n with
  E[Q̄_n] ≤ c_ML C′_{0,n} |𝒲(m)| ξ_n,  C′_{0,n} → 1,
such that **on Q_n(m) ∩ 𝒢′_n, whatever the realised packing**,
  q ≤ e^{κ̄_n + ζ_n} Q̄_n,  e ≤ 2p√(n+1)e^{κ_e}e^{−νx₁/2},  κ̄_n, ζ_n → 0,
and hence 1 − π₀(S₀) ≤ (s₀+1)q/(1−q) + s₀e. Consequently, for all M, η > 0,
  limsup_n P(Q_n(m) ∩ {1 − π₀(S₀) > (1+η)M(s₀+1)c_ML|𝒲(m)|ξ_n}) ≤ 1/M,
i.e. 1_{Q_n(m)}(1 − π₀(S₀)) = O_P(|𝒲(m)|(s₀+1)√(log n/n)). With Lemma P1′: **for S3, S4, S6,
1 − π₀(S₀) = O_P(√(log n/n)) unconditionally**, with leading constant 3.83·(s₀+1)·|𝒲(3)|·√((1+ε₀)A), |𝒲(3)| ≤ 1 + 14 + 91 = 106
(|𝒲(2)| = 15 while B = 14). For S1, Q_n(m) is an observable event (≤ m truths per block) and the constant carries
|𝒲(m)| ≤ Σ_{i<m}C(14, i).

**Proof.** *Fixed objects.* For every group K, every W ∈ 𝒲_K(m) and every ∅ ≠ V ⊆ K ∖ S₀ put U_{K,W} := 𝒯_K ∪ W and
X′_{K,W,V} := X_{U_{K,W},V}. By Lemma B′ (Γ = K) X′_{K,W,V} ~ Beta(|V|/2, (n−1−|U|−|V|)/2). Define, for j ≥ 1,
  a′_{K,W,j} := Σ_{V⊆K∖S₀, |V|=j}(n+1)^{−j/2}(1 − X′_{K,W,V})^{−ν}1{X′_{K,W,V} ≤ τ_n},  a′_{K,W,0} := 1,
D′_{K,W} := max_{j≥1}(j!a′_{K,W,j})^{1/j}, and Q̄_n := (p − s₀)^{−1}Σ_K Σ_{W∈𝒲_K(m)} D′_{K,W}. All are partition-free.
*Moment.* Lemma Tr′(a): E[j!a′_{K,W,j}] ≤ (1−τ_n)^{−e₁}(N_Kξ_n)^j/Γ(j/2+1), N_K := |K ∖ S₀|; Lemma M: E D′_{K,W} ≤
c_MLC′_{0,n}N_Kξ_n with C′_{0,n} := (1−τ_n)^{−(2B+s₀+3)/2−0.01}; summing (Σ_K N_K = p − s₀) gives E Q̄_n ≤ c_MLC′_{0,n}|𝒲(m)|ξ_n.
*Good event.* 𝒢′_n := (G1) ∩ (G2) ∩ (G3) ∩ (G4) ∩ (G5) with (G5) taken over the triples (K, W, V) above (N_n of them).
*Factorisation on Q_n(m) ∩ 𝒢′_n.* Take a realised block b. On Q_n, b = K₁ ∪ ⋯ ∪ K_R (whole groups, R ≤ B) and
U_b* = S₀ ∩ C_b = ∪_i𝒯_{K_i}; on Q_n(m), W_i := U_b* ∖ K_i ∈ 𝒲_{K_i}(m), so U_b* = U_{K_i,W_i} for every i. Let V ⊆ C_b ∖ S₀,
V_i := V ∩ K_i, and A_i := (C − P_{U_b*})span X_{V_i}. Then A₁ + ⋯ + A_R = (C − P_{U_b*})span X_V and
X_{U_b*,V} = ‖P_{ΣA_i}r‖²/‖r‖² with r := (C − P_{U_b*})Y, while ‖P_{A_i}r‖²/‖r‖² = X′_{K_i,W_i,V_i} (the same identity for one group).
By (G3) (A_i ⊆ the full-group subspace, which only increases the cosine) ‖P_{A_i}P_{A_k}‖ ≤ c_n, and Lemma S gives
  X_{U_b*,V} ≤ (1 − Bc_n)^{−1}Σ_i X′_{K_i,W_i,V_i} ≤ 2Bτ_n ≤ ½   (on (G5), n large).
Using −log(1−x) ≤ x/(1−x) ≤ x(1+2x) for x ≤ ½ and x′ ≤ −log(1−x′):
  −ν log(1 − X_{U_b*,V}) ≤ ν(1 + 4Bτ_n)(1 − Bc_n)^{−1}Σ_i X′_i ≤ Σ_i[−ν log(1 − X′_i)] + ζ_n,
  ζ_n := νBτ_n[(1+4Bτ_n)(1−Bc_n)^{−1} − 1] = O(B²t_n(τ_n + c_n)) = O(log^{3/2}n/√n) → 0.
With Lemma X⁺ (κ⁺ ≤ κ̄_n on (G1)–(G2)), for |V| = j:
  r_b(U_b*∪V)/r_b(U_b*) ≤ e^{κ̄_n+ζ_n}∏_i (n+1)^{−|V_i|/2}(1 − X′_{K_i,W_i,V_i})^{−ν}.
Summing over V with |V| = j (V ↔ (V₁, …, V_R)) and using the truncation indicators (all equal to 1 on (G5)):
  a_bj ≤ e^{κ̄_n+ζ_n} Σ_{j₁+⋯+j_R = j} ∏_i a′_{K_i,W_i,j_i}.
Since a′_{K,W,j} ≤ D′_{K,W}^j/j! (definition of D′; also for j = 0), the multinomial theorem gives
j!a_bj ≤ e^{κ̄_n+ζ_n}(Σ_i D′_{K_i,W_i})^j, hence D_b ≤ e^{κ̄_n+ζ_n}Σ_iD′_{K_i,W_i} ≤ e^{κ̄_n+ζ_n}Σ_{K⊆b}Σ_{W∈𝒲_K(m)}D′_{K,W}.
Summing over blocks (each group lies in exactly one block): q ≤ e^{κ̄_n+ζ_n}Q̄_n.
*Deletion term.* As in Theorem A's (A2): for b, U ⊆ C_b with a = |U_b*∖U| > 0, the pair (U, U_b*∖U) ∈ 𝔙 with Γ = C_b (a union
of groups on Q_n), so (G4) and Lemma X⁻ apply. (A3)'s Markov step concludes, since P(𝒢′_n) → 1. For S3/S4/S6 Lemma P1′ gives
P(Q_n(3)) → 1 (B ≤ 16, groups of 5). ∎

*Remarks.* (1) **This closes W3-VEXP's GAP (row 24, R3 last paragraph) without a leave-one-column-out lemma**: the dependence of
the packing on the null columns is irrelevant because the bound q ≤ e^{o(1)}Q̄_n holds simultaneously for every packing on
Q_n(m) ∩ 𝒢′_n, and Q̄_n is a fixed sum. The price is |𝒲(m)|, the number of possible *truth contexts* of a group (which truth
groups share its block) — a constant in n, but up to 106 for the study's groups at B = 16 and up to 2^{s₀} for S1.
(2) I believe |𝒲(m)| is an artefact (only one context per group is realised and the realised one is chosen by X alone).
CONJECTURE B′: the conclusion holds with constant 3.83(s₀+1)√((1+ε₀)A), as in Theorem A. Numerics (REPORT §4.1) support it:
the realised q is within the fixed-partition range.
(3) Lemma P1′'s condition ρ₋ > 0 excludes partial groups; if a group could be split across blocks, a null member co-blocked
with its own group's truth's *absence* leaks that truth's signal and the Beta law fails (this is the masked-regime mechanism
of W3-PXN §13). Union-of-groups is therefore the right event, not a technical convenience.

---------------------------------------------------------------------------------------------------------

## 10. Sharp first-order constant (why the bound is within a factor ≈ 7 of the truth) — PROOF SKETCH

For iid designs the null-addition mass is the leading term. Under Theorem A's setting, with Lemma X⁺ and its matching lower
bound for a single null addition (Lemma X⁻ with RSS^y ≍ n: both remainders are O(1/n) for nulls, since a_{U+l} − a_U =
x·RSS^y_U/(n+1) + O(1/n) is O(log n/n) on (G5)),
  Σ_{l∉S₀} π₀(S₀+l)/π₀(S₀) = ((s₀+1)/(2p−s₀−1)) Σ_{l∉S₀}(n+1)^{−1/2}(1 − X_{U*_{b(l)},l})^{−ν}(1 + O(log n/n)),
and (1 − X)^{−ν} = e^{χ²/2 + O(log²n/n)} with χ² := nX ≈ χ²₁. The X_{U*,l}, l ∉ S₀, are Beta(½, ·) (Lemma B′), weakly dependent
within a block. If they were independent, (1/p)Σ_l e^{χ²_l/2} would be p^{−1}× a sum of p variables with tail P(e^{χ²/2} > t) ~
1/(t√(π log t)) (index 1), whose typical size is M_p := 1 + (2/√π)√(log p) (truncated-mean scale). This predicts
  1 − π₀(S₀) ≈ (s₀+1)M_p/(2√(n+1))  (null additions only; no B, no g),
≈ (s₀+1)√(log p/(πn)) for large p. Theorem A's bound is (s₀+1)·3.83·√((1+ε₀)log N_n/(n+1)): a factor 3.83·√π ≈ 6.8
(times √(log N_n/log p)) above it. W3-PXN's LH-iid data (√(n/log n)(1 − π₀(S°)) ∈ [1.5, 2.6] with s = 2, p ≈ n^{1.25}) and this
run's S1/S3 data at large n (REPORT §4.3) agree with the prediction to within 30%. CONJECTURE (sharp constant).
In exactly orthogonal designs (W2-T26's ORTH) the null columns are orthogonal to the signal, X ≈ (σ²/v)χ²₁/n, the
moment E e^{(σ²/v)χ²/2} is finite, and the rate is n^{−1/2} without √log n — consistent with W2-T26 §4.2 and W1-EXP Thm 6.

---------------------------------------------------------------------------------------------------------

## 11. Finite n: a one-change ceiling, and the threshold n*(design)

### Proposition F (one-change ceiling; sharpens W3-VEXP Prop D) — PROVED (deterministic)
For any data, any partition with positive tables, and S₀ ∈ Ω with s₀ + 1 ≤ K:
  π₀(S₀) ≤ [1 + N_add + Σ_{j∈S₀} O^del_j + Σ_{j∈S₀, l∉S₀} O^swp_{j,l}]^{−1},
  N_add := Σ_{l∉S₀} γ₀(S₀+l)/γ₀(S₀) = [(s₀+1)/(2p−s₀−1)] Σ_{l∉S₀} r_{b(l)}(U*_{b(l)}+l)/r_{b(l)}(U*_{b(l)}),
  O^del_j := γ₀(S₀−j)/γ₀(S₀) = [(2p−s₀)/s₀]·r_{b(j)}(U*_{b(j)}−j)/r_{b(j)}(U*_{b(j)}),
  O^swp_{j,l} := γ₀(S₀−j+l)/γ₀(S₀) (a ratio of at most two table entries per block; no prior factor).
*Proof.* 1/π₀(S₀) = Σ_{S∈Ω}γ₀(S)/γ₀(S₀) ≥ 1 + (the sum over the one-change neighbours, all in Ω), and γ₀ factorises
over blocks with the prior ratios w(s₀±1)/w(s₀) = (s₀+1)/(2p−s₀−1), (2p−s₀)/s₀. ∎
Combined with T22(i) this brackets π₀(S₀) between two data-computable quantities. The **product refinement** used for
prediction (not a bound): summing the null additions over all subsets with the BB(1,p) prior gives the negative-binomial
factor (1 − N_add/(s₀+1))^{−(s₀+1)} ≈ e^{N_add} when the null odds are small and nearly independent, so
  log π₀(S₀) ≈ (s₀+1)log(1 − N_add/(s₀+1)) − Σ_j log(1 + O^del_j + Σ_l O^swp_{j,l}).          (11.1)
REPORT §4.1 ("decomposition" column) shows (11.1) evaluated at the *exact* odds reproduces the exact log₁₀π₀(S₀) to within
≈ 0.1 decades whenever π₀(S₀) ≥ 10⁻³, and to within a few decades in the deeply masked cells (n = 200).

### Population plug-in (the dilution threshold) — PROOF SKETCH for each limit; CONJECTURE for the median-level formula
For FAV with one truth per group, unit-variance groups, σ² = 1 and truths not co-blocked (the typical case), each term of
(11.1) has an explicit population counterpart (Lemma B′ for nulls, W3-PXN Prop W for truths):
- **Dilution:** v := σ² + Σ_k θ_k² (the block view of a truth sees all other truths' signal as noise);
  V_j := −(n/2)log(1 − θ_j²/v) (median of the block keep statistic −ν log(1 − X_j), nX_j ≈ (√(nθ_j²/v) + Z)²);
- **deletion odds** O^del_j ≈ [(2p−s₀)/s₀]√(n+1)e^{−V_j};
- **proxy-swap odds** (equicorrelated group, ρ_j, g − 1 mates) O^swp_j ≈ (g−1)exp(−(n/2)log((v − ρ_j²θ_j²)/(v − θ_j²)));
- **null-addition mass** N_add ≈ [(s₀+1)(p−s₀)/(2p−s₀−1)]·M(p,n)/√(n+1), M(p,n) := median of the average of p − s₀ iid
  (1 − B)^{−ν}, B ~ Beta(½, (n−3)/2) (≈ 1 + (2/√π)√(log p), the index-1 stable scale of §10).
The thresholds are then explicit functions of (θ, v, p, s₀, ρ):
- **n*_del(j)**: the smallest n with V_j ≥ log((2p−s₀)/s₀) + ½log(n+1) + log(2s₀) — scale-free in θ (θ_j²/v depends only
  on the *shares* θ_j²/Σθ², up to σ²), which is W3-VEXP/PXN's dilution observation;
- **n*_swp(j)**: (n/2)log((v − ρ_j²θ_j²)/(v − θ_j²)) ≥ log(2(g−1)s₀) — the only place the within-group correlation enters;
- **n*_null**: N_add ≤ log 2 (π₀(S₀) cannot exceed ½ before), ≈ ((s₀+1)M(p,n)/(2 log 2))² — **independent of θ and v**;
- **n*_half(design)** := first n at which (11.1)'s population version reaches log ½; **n*_hit** := first n at which
  Q_f^min·π₀(S₀) ≥ 3, Q_f^min = 4N₀(L + 6) the minimum number of iid π₀ draws scored by the final run (T ≥ 1), so that
  P(S₀ not drawn) ≤ e^{−3}.
REPORT §4.4 tabulates these thresholds and checks them against exact π₀ at n ∈ {200, …, 3200}.

---------------------------------------------------------------------------------------------------------

## 12. Consequences for Thm 5(a) (T38(a)) and Thm 6 (T26(i)–(ii)'s premise (P1))

**Corollary C1 (posterior concentration on FAV) — PROVED given locked T03 and [C1].** On FAV (S1, S3, S4, S6 included),
δ₁ = 1 − π(S₀) = O_P(√(log n/n)).
*Proof.* W3-PXN Lemma P2's argument applies verbatim to any Σ with λ_min(Σ) ≥ λ₀ and fixed nonzero coefficients: SE for
|T| ≤ m_n + s₀ = O(log n) (|T|ε_n → 0), R (‖μ‖²/n → β'Σ_{S₀}β a.s.; under the generator convention θ* = β exactly),
BM-∞ (fixed θ*), G given X. W3-PXN's design de-randomisation lemma (P8, PROVED there) transfers locked T03(i). ∎

**Corollary C2 (Thm 6's (P1) on the study-like family) — PROVED as a composition** (inputs: Theorem B here, Corollary C1,
W2-T26 Lemma 1 and Theorem A (candidates, PROVED there), locked T03; idealisations EX-A, EX-S, CAL, START, OUT).
On FAV with P(Q_n(m)) → 1 for a fixed m — in particular S3, S4, S6 (m = 3), and S1 on the event of at most m truths per
block —
  Δ_n = max{1 − π₀(S₀), δ₁} = O_P(√(log n/n)),  (T_n + 1)Δ_n ≤ (T^max_n + 1)Δ_n = O_P(log^{5/2}n/√n) → 0,
so (P1) holds in its deterministic-budget form, (P1-ex) holds by C1, and **T26(i)–(ii) (evidence and PIP consistency) hold on
S3/S4/S6-type designs with the actual partition and budgets**, with no EXP′, VIS, NL_η or NL_avg hypothesis.
*Proof.* T^max = 4max(1000, ℓ²) = O(log²n). W2-T26 Lemma 1 gives Δ_n; Theorem B and C1 bound both terms; W2-T26 Theorem A. ∎
This replaces W2-T26 Theorem B's CONDITIONAL route (through the locked T22(iii)) for these designs.

**Corollary C3 (Thm 5(a), favourable regime of T38) — PROVED as a composition** (inputs: Theorem B, C1, locked T21 route (a),
EX-S). On the same families, P(Uᶜ ∩ {S₀ never scored}) ≤ E[(1 − π₀(S₀))^{Q_f}] → 0, because Q_f ≥ 4N_e(L+6) → ∞ and
π₀(S₀) → 1 in probability; with C1 and T21, liminf P(Ŝ = S₀) ≥ 1 − limsup P(U).
*Remark (what is really needed).* Route (a) needs only Q_f·π₀(S₀) → ∞, far weaker than π₀(S₀) → 1: at the study budgets
Q_f ≥ 1.4·10⁵, so π₀(S₀) ≥ 2·10⁻⁵ already gives P(S₀ never drawn) ≤ e^{−3}. The thresholds n*_hit (≈ 330–440) and
n*_half (≈ 1,050–1,450) differ by a factor ≈ 3 (REPORT §4.4).

**Finite n.** With the deterministic budget T^max = 4,000, (T^max + 1)Δ_n < 1 needs Δ_n < 2.5·10⁻⁴, i.e. (by §10's sharp
constant) n of order ((s₀+1)·4001·M_p/2)² ≈ 10¹⁰ at s₀ = 14. With the **realised** pilot/grid stage count T_n (simulated in
REPORT §4.5) the first n with (T_n + 1)Δ_n < 1 is reported there.
