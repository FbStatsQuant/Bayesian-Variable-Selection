# L0 — Toolkit-b: the Gaussian score toolkit at general family sizes (bridge (P0))

Status: **PROVED (by this seat, unchecked)**. Ticket W3-RM2; statement: `../STATEMENT.md` §4, bridge (P0).
This file is **self-contained**: it re-proves, with every cardinality kept explicit, the statements of the toolkit
W1-GEN:L1 (`Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md`, fixed set size, polynomial family) and of C-GROW:L0.2
(`Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md:29-53`). Those sources are the templates; none of their conclusions
is used here as an input. Only two classical facts are quoted: the Laurent–Massart χ² bounds and the Gaussian tail
bound.

## 0. Setting and notation

Setting F (`../STATEMENT.md` §1): X ∈ ℝ^{n×p} fixed, columns centred with ‖x_j‖² = n − 1; C := I − 11ᵀ/n;
Y := Cy^r = μ + Cε with μ = Xθ* ∈ 1^⊥ deterministic and ε ~ N_n(0, σ²I), σ² > 0 fixed; y := Y/s_y,
s_y² := ‖Y‖²/(n − 1) (defined almost surely), so ‖y‖² = n − 1. For A ⊆ [p]: P_A the orthogonal projector on
span X_A (P_∅ = 0); R̂_A := X_AᵀX_A/(n − 1); RSS_A := ‖(I − P_A)Y‖²; RSS^y_A := ‖(I − P_A)y‖² = (n − 1)RSS_A/‖Y‖²;
r_A := (I − P_A)μ; Λ_A := ‖r_A‖². Every column is centred, so P_AC = P_A, (I − P_A)Y = (C − P_A)Y and

  RSS_A = Λ_A + 2⟨r_A, ε⟩ + ‖Cε‖² − ‖P_Aε‖²                                                              (0.1)

(⟨r_A, Cε⟩ = ⟨r_A, ε⟩ because r_A ∈ 1^⊥). D0 score: G_A := X_AᵀX_A, z_A := X_Aᵀy, H_A := (n + 1)G_A + I,
D_A := det H_A/det(G_A + I), Q_A := yᵀy − n z_AᵀH_A⁻¹z_A, ν := 0.01 + n/2,
log m(A) = log c_n − ½ log D_A − ν log(0.02 + Q_A) (c_n free of A); prior w(k) = 1/(2·binom(2p − 1, k));
F(A) := log w(|A|) + log m(A) up to a constant common to all A (the normaliser of the prior).

## 1. Hypotheses

(H-F) 𝔉 = 𝔉_n is a deterministic finite family of subsets of [p] with ∅ ∈ 𝔉 and |A| ≤ J_n for A ∈ 𝔉.
(H-G) λ_min(R̂_A) ≥ φ₀² for every nonempty A ∈ 𝔉, with a fixed φ₀ ∈ (0, 1].
(H-E) ‖μ‖² ≤ Mn, M fixed.
(H-V) 𝒱𝒱 = 𝒱𝒱_n is a deterministic nonempty finite set of vectors of ℝⁿ with
      𝒱𝒱 ⊇ {r_A : A ∈ 𝔉} ∪ {r_A − r_{A′} : A, A′ ∈ 𝔉}.
(H-S) with ℓ_𝔉 := log|𝔉| and ℓ_V := log|𝒱𝒱|: (ℓ_𝔉 + ℓ_V + J_n) log n/n → 0.
Put
  t_n := 4(ℓ_𝔉 + 2 log n + J_n),   h_n² := 2(ℓ_V + log n),   ω_n := 4n^{−1/3} + (h_n² + t_n + 1)/n,
  C_R := 3(M + σ²),   c_E := σ²/(12(M + σ²)),   κ_E := 0.52/c_E + 1,   1 + ϑ_n := (1 + 0.02/n)/(1 − ω_n).
By (H-S), (h_n² + t_n) log n/n → 0, hence ω_n log n → 0, ϑ_n log n → 0 and J_n/n → 0. Events:
* 𝒟₁ := {|‖Cε‖²/σ² − (n − 1)| ≤ 2√((n − 1)n^{1/3}) + 2n^{1/3}};
* 𝒟₂ := {max_{A∈𝔉} ‖P_Aε‖² ≤ σ²t_n};
* 𝒟₃ := {|⟨v, ε⟩| ≤ σh_n‖v‖ for every v ∈ 𝒱𝒱};
* 𝓔 := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ ("the toolkit event of (𝔉, 𝒱𝒱)").
"n ≥ n₀" below means: n larger than a threshold depending only on (σ², M, φ₀) and on the sequences
(ℓ_𝔉 + ℓ_V + J_n) log n/n; explicitly n₀ is such that for n ≥ n₀: n ≥ 512, ω_n ≤ ½, (n − 1)φ₀² ≥ max(J_n, 100).

## 2. Lemma Toolkit-b

Under (H-F), (H-G), (H-E), (H-V), (H-S):

**(T1) Probabilities.** P(𝒟₁ᶜ) ≤ 2e^{−n^{1/3}}, P(𝒟₂ᶜ) ≤ n^{−2}, P(𝒟₃ᶜ) ≤ 2/n; so P(𝓔ᶜ) ≤ 2e^{−n^{1/3}} + n^{−2} + 2/n.

**(T2) RSS bounds.** On 𝓔, for n ≥ n₀ and every A ∈ 𝔉:
(a) RSS_A ≥ σ²n(1 − ω_n) ≥ nσ²/2; (b) ‖Y‖² ≤ C_R n and RSS_A ≤ ‖Y‖²; (c) RSS^y_A ≥ c_E n;
(d) ‖Cε‖² ≤ σ²n(1 + 4n^{−1/3}); in particular RSS_A ≤ σ²n(1 + 4n^{−1/3}) whenever Λ_A = 0.

**(T3) Score expansion.** On 𝓔, for n ≥ n₀ and every A ∈ 𝔉:
log m(A) = c′_n − ½|A| log(n + 1) − ν log RSS_A + R_A with |R_A| ≤ κ_E, where c′_n does not depend on A. Hence for
A, A′ ∈ 𝔉:
  F(A) − F(A′) = log[w(|A|)/w(|A′|)] − ½(|A| − |A′|) log(n + 1) − ν log(RSS_A/RSS_{A′}) + (R_A − R_{A′}),
  |R_A − R_{A′}| ≤ 2κ_E,                                                                                   (E6)
and, for a block C_b of the partition and A, A′ ∈ 𝔉 both contained in C_b (r_b(U) := m(U)/m(∅)):
  log r_b(A′) − log r_b(A) = −½(|A′| − |A|) log(n + 1) − ν log(RSS_{A′}/RSS_A) + (R_{A′} − R_A).           (E6-tab)

**(T4) Contrasts.** On 𝓔, for A, A′ ∈ 𝔉:
(a) RSS_A − RSS_{A′} ≥ (Λ_A − Λ_{A′}) − 2σh_n‖r_A − r_{A′}‖ − σ²t_n (every n);
(b) for n ≥ n₀: if RSS_A ≥ RSS_{A′} then ν log(RSS_A/RSS_{A′}) ≥ (RSS_A − RSS_{A′})/(2C_R);
(c) [LC1A-1] for every e ∈ (0, 1] and x ≥ 0: 2σh_n√x ≤ ex + σ²h_n²/e (every n; no event needed).

**(T5) Likelihood-ratio bounds.** On 𝓔, for n ≥ n₀:
(a) if A ⊆ A′ are both in 𝔉 (so RSS_A ≥ RSS_{A′}): ν log(RSS_A/RSS_{A′}) ≤ (1 + ϑ_n)(RSS_A − RSS_{A′})/(2σ²);
(b) if moreover x := (RSS_A − RSS_{A′})/RSS_A ≤ ¼: ν log(RSS_A/RSS_{A′}) ≤ (1 + ϑ_n)(1 + 2x)(RSS_A − RSS_{A′})/(2σ²);
(c) if A ⊆ A′ are both in 𝔉 and Λ_A = 0: ν log(RSS_A/RSS_{A′}) ≥ (1 − 4n^{−1/3})(RSS_A − RSS_{A′})/(2σ²).

Prior ratios (exact; used with the lemma): w(k + 1)/w(k) = (k + 1)/(2p − 1 − k) for 0 ≤ k ≤ 2p − 2;
for 0 ≤ k ≤ p − 1: (k + 1)/(2p) ≤ w(k + 1)/w(k) ≤ (k + 1)/p; for 1 ≤ k ≤ p: w(k − 1)/w(k) = (2p − k)/k ∈ [p/k, 2p].

## 3. Proof

**(T1).** 𝒟₁: C is the projector on 1^⊥, so ‖Cε‖²/σ² ~ χ²_{n−1}. Laurent–Massart: for χ²_k and x > 0,
P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x} and P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}; take k = n − 1, x = n^{1/3}.
𝒟₂: for a deterministic orthogonal projector P of rank d, ‖Pε‖²/σ² ~ χ²_d and E exp{‖Pε‖²/(4σ²)} = (1 − ½)^{−d/2}
= 2^{d/2}; by Markov, P(‖Pε‖²/σ² > t) ≤ 2^{d/2}e^{−t/4}. For A ∈ 𝔉, d = rank P_A ≤ |A| ≤ J_n, and at t = t_n:
2^{J_n/2}e^{−t_n/4} = 2^{J_n/2}e^{−J_n}·|𝔉|⁻¹n^{−2} ≤ |𝔉|⁻¹n^{−2} (2^{1/2} < e). Union over the |𝔉| members.
𝒟₃: for v ≠ 0, ⟨v, ε⟩/(σ‖v‖) ~ N(0, 1) and P(|N(0, 1)| > h) ≤ 2e^{−h²/2}; at h = h_n this is 2/(|𝒱𝒱| n); union over
𝒱𝒱 (v = 0 is trivial). No independence between events or members is used. ∎

**(T2).** (d): on 𝒟₁, ‖Cε‖²/σ² ≤ n − 1 + 2√((n − 1)n^{1/3}) + 2n^{1/3} ≤ n + 4n^{2/3}; if Λ_A = 0 then r_A = 0 and by
(0.1) RSS_A = ‖Cε‖² − ‖P_Aε‖² ≤ ‖Cε‖². (a): by (0.1), 𝒟₃ applied to r_A ∈ 𝒱𝒱, 𝒟₁ and 𝒟₂,
RSS_A ≥ Λ_A − 2σh_n√Λ_A + σ²(n − 1 − 2√((n − 1)n^{1/3}) − 2n^{1/3}) − σ²t_n. As a quadratic in √Λ_A ≥ 0,
Λ_A − 2σh_n√Λ_A ≥ −σ²h_n²; and 2√((n − 1)n^{1/3}) + 2n^{1/3} ≤ 4n^{2/3}. So
RSS_A ≥ σ²(n − 1 − 4n^{2/3} − h_n² − t_n) = σ²n(1 − ω_n), and ω_n ≤ ½ for n ≥ n₀.
(b): ‖Y‖² ≤ 2‖μ‖² + 2‖Cε‖² ≤ 2Mn + 2σ²(n + 4n^{2/3}) ≤ 3(M + σ²)n because 8n^{2/3} ≤ n for n ≥ 512;
RSS_A = ‖(C − P_A)Y‖² ≤ ‖Y‖² since C − P_A is a projector and Y ∈ 1^⊥. (c): RSS^y_A = (n − 1)RSS_A/‖Y‖²
≥ (n − 1)(nσ²/2)/(C_R n) = (n − 1)σ²/(6(M + σ²)) ≥ c_E n for n ≥ 2. ∎

**(T3).** Fix A ∈ 𝔉, n ≥ n₀, on 𝓔.
(E1) log D_A = |A| log(n + 1) + η_A with −2|A|/((n − 1)φ₀²) ≤ η_A ≤ 0. Indeed, if g_i ≥ (n − 1)φ₀² are the
eigenvalues of G_A ((H-G); nothing to prove for A = ∅), D_A = ∏_i ((n + 1)g_i + 1)/(g_i + 1) = ∏_i (n + 1)(1 − x_i)
with x_i := n/((n + 1)(g_i + 1)) ∈ (0, 1/((n − 1)φ₀²)] ⊆ (0, 0.01], and log(1 − x) ∈ [−2x, 0] on [0, ½].
(E2) 0.02 + Q_A = RSS^y_A + a_A with 0.02 ≤ a_A ≤ 1.03. Indeed RSS^y_A = yᵀy − z_AᵀG_A⁻¹z_A, so
Q_A − RSS^y_A = z_Aᵀ(G_A⁻¹ − nH_A⁻¹)z_A; all matrices are functions of G_A, G_A⁻¹ − nH_A⁻¹ = G_A⁻¹(G_A + I)H_A⁻¹, and
(G_A + I)H_A⁻¹ has eigenvalues (g + 1)/((n + 1)g + 1) ∈ (0, (1 + 1/((n − 1)φ₀²))/(n + 1)]. Hence
0 ≤ Q_A − RSS^y_A ≤ (1.01/(n + 1))·z_AᵀG_A⁻¹z_A = (1.01/(n + 1))‖P_Ay‖² ≤ 1.01(n − 1)/(n + 1) ≤ 1.01; put
a_A := 0.02 + Q_A − RSS^y_A (a_∅ = 0.02).
(E4) −ν log(0.02 + Q_A) = −ν log RSS^y_A − ν log(1 + a_A/RSS^y_A), and by (T2)(c),
0 ≤ ν log(1 + a_A/RSS^y_A) ≤ νa_A/(c_E n) ≤ (½ + 0.01/n)(1.03)/c_E < 0.52/c_E (n ≥ 3). Also
−ν log RSS^y_A = −ν log RSS_A + ν log(‖Y‖²/(n − 1)), the last term common to all A. With
R_A := −½η_A − ν log(1 + a_A/RSS^y_A) ∈ [−0.52/c_E, |A|/((n − 1)φ₀²)] ⊆ [−κ_E, κ_E] (|A| ≤ J_n ≤ (n − 1)φ₀²) and
c′_n := log c_n + ν log(‖Y‖²/(n − 1)): log m(A) = c′_n − ½|A| log(n + 1) − ν log RSS_A + R_A.
(E6) is the difference of (E4) for A and A′ plus the prior terms (the prior normaliser cancels). (E6-tab):
log r_b(U) = log m(U) − log m(∅), so the terms c′_n and log m(∅) cancel in the difference. ∎

**(T4).** (a): subtract (0.1) for A′ from (0.1) for A; the ‖Cε‖² terms cancel; ⟨r_A − r_{A′}, ε⟩ ≥ −σh_n‖r_A − r_{A′}‖ by
𝒟₃ (r_A − r_{A′} ∈ 𝒱𝒱) and −‖P_Aε‖² + ‖P_{A′}ε‖² ≥ −σ²t_n by 𝒟₂. (b): log u ≥ 1 − 1/u gives
ν log(RSS_A/RSS_{A′}) ≥ ν(RSS_A − RSS_{A′})/RSS_A ≥ (n/2)(RSS_A − RSS_{A′})/(C_R n) by (T2)(b). (c): (√(ex) − σh_n/√e)² ≥ 0. ∎

**(T5).** For A ⊆ A′, span X_A ⊆ span X_{A′} gives RSS_A ≥ RSS_{A′}; RSS_{A′} > 0 by (T2)(a).
(a): log u ≤ u − 1 with u = RSS_A/RSS_{A′}: ν log u ≤ ν(RSS_A − RSS_{A′})/RSS_{A′} ≤ (n/2 + 0.01)(RSS_A − RSS_{A′})/
(σ²n(1 − ω_n)) = (1 + ϑ_n)(RSS_A − RSS_{A′})/(2σ²) by (T2)(a) for A′.
(b): ν log(RSS_A/RSS_{A′}) = −ν log(1 − x), and −log(1 − x) ≤ x + x² ≤ x(1 + 2x) on [0, ½]; νx = ν(RSS_A − RSS_{A′})/RSS_A
≤ (1 + ϑ_n)(RSS_A − RSS_{A′})/(2σ²) by (T2)(a) for A.
(c): −log(1 − x) ≥ x, so ν log(RSS_A/RSS_{A′}) ≥ ν(RSS_A − RSS_{A′})/RSS_A ≥ (n/2)(RSS_A − RSS_{A′})/(σ²n(1 + 4n^{−1/3}))
by (T2)(d), and 1/(1 + u) ≥ 1 − u. ∎

Prior ratios: w(k + 1)/w(k) = binom(2p − 1, k)/binom(2p − 1, k + 1) = (k + 1)/(2p − 1 − k); for k ≤ p − 1,
p ≤ 2p − 1 − k ≤ 2p. ∎

## 4. Two families used in this ticket

**(i) The block family.** For a partition C₁, …, C_J of [p] with |C_b| ≤ 16 and (G3a) (λ_min(R̂_T) ≥ φ₀² for nonempty
T inside a block): 𝔉_blk := {U : U ⊆ C_b for some b} (∅ included), J_n = 16, |𝔉_blk| ≤ 2^{16}p;
𝒱𝒱_blk := {r_U, r_U − r_{U′} : U, U′ ∈ 𝔉_blk}, |𝒱𝒱_blk| ≤ 2|𝔉_blk|². With p ≤ n^A: ℓ_𝔉, ℓ_V = O(log n), so (H-S)
holds and t_n, h_n² = O(log n).
**(ii) The lattice family.** For a deterministic Q ⊇ S₀ with q := |Q| ≤ K, 𝓛 := {T : S₀ ⊆ T ⊆ Q}, and (FL-Q)
(λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p]):
𝔉_lat := {∅} ∪ 𝓛 ∪ {T ∪ {l} : T ∈ 𝓛, l ∉ T} ∪ {T ∖ {i} : T ∈ 𝓛, i ∈ S₀} ∪ {(T ∖ {i}) ∪ {l} : T ∈ 𝓛, i ∈ S₀, l ∉ T}.
Every nonempty member is contained in Q ∪ {l} for some l ∈ [p] (for members of 𝓛 and pure deletions take any l), so
J_n = q + 1 and the Gram floor φ₀² holds on it by (FL-Q) and Cauchy interlacing (a principal submatrix of a positive
definite matrix has λ_min at least that of the matrix). |𝔉_lat| ≤ 1 + 2^{q−s₀}(1 + p + s₀ + s₀p);
𝒱𝒱_lat := {r_A, r_A − r_{A′} : A, A′ ∈ 𝔉_lat}, |𝒱𝒱_lat| ≤ 2|𝔉_lat|². With p ≤ n^A: ℓ_𝔉 + ℓ_V + J_n ≤ C(q + log n), so
**(H-S) holds as soon as q log n/n → 0**, in particular for q ≤ n^b with any fixed b < 1; then t_n + h_n² = O(q + log n).
(For T ∈ 𝓛: μ ∈ span X_{S₀} ⊆ span X_T, so r_T = 0 and Λ_T = 0.)

**Remark (what the lattice family costs).** The exponential cardinality of 𝔉_lat enters only through t_n, h_n² = O(q + log n)
in ω_n and in (T4)(a). In this ticket the lattice family is used for (T2), (T3), (T4)(b), (T5) only — score regularity;
the contrast bound (T4)(a) with its O(q) charge is not used on the lattice (`L2_width.md` §4 uses an exact identity
instead).
