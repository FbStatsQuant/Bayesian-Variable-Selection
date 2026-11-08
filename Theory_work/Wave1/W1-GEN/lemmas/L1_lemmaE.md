# L1 — Uniform score expansion and Gaussian contrast toolkit (Lemma E)

Status: **PROVED (by this seat, unchecked)**; lemma check R02 (Codex Sol): VERIFIED-WITH-AMENDMENTS, amendments
applied (v2, see reviews/R02_disposition.md).
Source of the argument: BS/API-PXNGAP/PROOF.md §4 (Lemma E, candidate, unreviewed), re-proved here in the form used by
L2 and L3, with the Gaussian union bounds made explicit and the absolute error (E5) **not** used anywhere.

Setting: G and the notation of STATEMENT.md §1. Y := Cy^r = μ + Cε (μ ∈ 1^⊥ deterministic), y := Y/s_y with
s_y² := ‖Y‖²/(n − 1) (defined a.s.), so ‖y‖² = n − 1. For A ⊆ [p]: RSS_A := ‖(I − P_A)Y‖², RSS^y_A := ‖(I − P_A)y‖²
= (n − 1)RSS_A/‖Y‖², r_A := (I − P_A)μ, Λ_A = ‖r_A‖². Since every column of X is centred, P_A C = P_A and
P_A ≼ C, hence (I − P_A)Y = (C − P_A)Y and

  RSS_A = Λ_A + 2⟨r_A, ε⟩ + ‖Cε‖² − ‖P_Aε‖²                                                            (1.1)

(⟨r_A, Cε⟩ = ⟨r_A, ε⟩ because r_A ∈ 1^⊥: (I − P_A)μ = (C − P_A)μ).

## L1.1 Families and events

Let 𝔉 = 𝔉_n be a deterministic family of subsets of [p] with ∅ ∈ 𝔉, |A| ≤ J for A ∈ 𝔉, |𝔉| ≤ C_F n^D (J, C_F, D
fixed, C_F ≥ 1, D ≥ 0), and suppose λ_min(R̂_A) ≥ φ₀² > 0 for every nonempty A ∈ 𝔉 (Gram floor) and ‖μ‖² ≤ Mn. Let 𝒱𝒱 = 𝒱𝒱_n be a
deterministic set of vectors in ℝⁿ with |𝒱𝒱| ≤ C_V n^{D_V} (C_V > 0, D_V ≥ 0 fixed). Put

  t_n := 4(D + 2) log n,   h_n := √(2(D_V + 1) log n).

Define the events
* 𝒟₁ := {|‖Cε‖²/σ² − (n − 1)| ≤ 2√((n − 1)n^{1/3}) + 2n^{1/3}};
* 𝒟₂ := {max_{A∈𝔉} ‖P_Aε‖² ≤ σ² t_n};
* 𝒟₃ := {|⟨v, ε⟩| ≤ σ h_n ‖v‖ for every v ∈ 𝒱𝒱}.

**Lemma L1.1.** P(𝒟₁ᶜ) ≤ 2e^{−n^{1/3}}; P(𝒟₂ᶜ) ≤ C_F 2^{J/2} n^{−2}; P(𝒟₃ᶜ) ≤ 2C_V n^{−1}. Hence
P(𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃) → 1.

*Proof.* 𝒟₁: ‖Cε‖²/σ² ~ χ²_{n−1}; Laurent–Massart with x = n^{1/3}: P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x},
P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}. 𝒟₂: for a deterministic orthogonal projection P of rank d ≤ J,
‖Pε‖²/σ² ~ χ²_d and E exp{‖Pε‖²/(4σ²)} = (1 − ½)^{−d/2} = 2^{d/2}; Markov gives
P(‖Pε‖²/σ² > t) ≤ 2^{J/2}e^{−t/4} = 2^{J/2}n^{−(D+2)} at t = t_n; union over ≤ C_F n^D sets. 𝒟₃: for v ≠ 0,
⟨v, ε⟩/(σ‖v‖) ~ N(0,1) and P(|N(0,1)| > h) ≤ 2e^{−h²/2} = 2n^{−(D_V+1)}; union over ≤ C_V n^{D_V} vectors (v = 0 is
trivial). No independence between the events or members is used. ∎

## L1.2 RSS floor and ceiling

**Lemma L1.2.** On 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃, if 𝒱𝒱 ⊇ {r_A : A ∈ 𝔉}, then for n ≥ n₀(σ², M, D, D_V):
(a) RSS_A ≥ nσ²/2 for every A ∈ 𝔉 (in particular RSS_A > 0); (b) ‖Y‖² ≤ C_R n with C_R := 3(M + σ²); (c) RSS^y_A ≥ c_E n with
c_E := σ²/(12(M + σ²)); (d) RSS_A ≤ ‖Y‖² ≤ C_R n.

*Proof.* (a) By (1.1) and the events, RSS_A ≥ Λ_A − 2σh_n√Λ_A + σ²(n − 1 − 2√((n−1)n^{1/3}) − 2n^{1/3}) − σ²t_n. As a
quadratic in √Λ_A ≥ 0, Λ_A − 2σh_n√Λ_A ≥ −σ²h_n². So RSS_A ≥ σ²(n − 1 − 2n^{2/3} − 2n^{1/3} − h_n² − t_n) ≥ nσ²/2
for n ≥ n₀.
(b) ‖Y‖² ≤ 2‖μ‖² + 2‖Cε‖² ≤ 2Mn + 2σ²(n + 3n^{2/3}) ≤ 3(M + σ²)n for n ≥ n₀. (c) RSS^y_A = (n−1)RSS_A/‖Y‖²
≥ (n − 1)σ²/(6(M + σ²)) ≥ c_E n for n ≥ 2. (d) RSS_A = ‖(C − P_A)Y‖² ≤ ‖Y‖² since Y ∈ 1^⊥. ∎

## L1.3 Score expansion (EXP′ in uniform form)

For A ⊆ [p] (D0): G_A = X_AᵀX_A, z_A = X_Aᵀy, H_A = (n + 1)G_A + I, D_A = det H_A/det(G_A + I),
Q_A = yᵀy − n z_AᵀH_A⁻¹z_A, ν = 0.01 + n/2, log m(A) = log c_n − ½ log D_A − ν log(0.02 + Q_A).

**Lemma L1.3.** On 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ (with 𝒱𝒱 ⊇ {r_A : A ∈ 𝔉}) and n ≥ n₀(J, σ², M, φ₀, D, D_V), where n₀ in
particular ensures (n − 1)φ₀² ≥ max(J, 100) and n ≥ 3, for every A ∈ 𝔉:
(E1) log D_A = |A| log(n + 1) + η_A with −2|A|/((n − 1)φ₀²) ≤ η_A ≤ 0;
(E2) 0.02 + Q_A = RSS^y_A + a_A with 0.02 ≤ a_A ≤ 1.02 + 1/((n − 1)φ₀²);
(E4) log m(A) = c′_n − ½|A| log(n + 1) − ν log RSS_A + R_A, |R_A| ≤ κ_E := 0.52/c_E + 1, where c′_n does not depend on A.
Consequently, with F(A) := log w(|A|) − log W_K + log m(A) (the log posterior weight up to a common constant), for
A, A′ ∈ 𝔉:

  F(A) − F(A′) = log[w(|A|)/w(|A′|)] − ½(|A| − |A′|) log(n + 1) − ν log(RSS_A/RSS_{A′}) + (R_A − R_{A′}),
  |R_A − R_{A′}| ≤ 2κ_E,                                                                                 (E6)

and for within-block tables (A, A + l in 𝔉): log r_b(A + l) − log r_b(A) = −½ log(n + 1) − ν log(1 − x_{A,l})
+ (R_{A+l} − R_A) with x_{A,l} := 1 − RSS_{A+l}/RSS_A, for A ⊆ C_b, l ∈ C_b ∖ A (both in 𝔉), i.e. EXP′ whose remainder
R_{n,b,A,l} := log[r_b(A + l)/r_b(A)] + ½ log(n + 1) + ν log(1 − x_{A,l}) (defined a.s. for all n large, everywhere)
satisfies |R_{n,b,A,l}| ≤ 2κ_E simultaneously for all such pairs on the event; hence ρ_n := max|R_{n,b,A,l}| has
P(ρ_n > 2κ_E) ≤ P((𝒟₁∩𝒟₂∩𝒟₃)ᶜ) → 0, i.e. ρ_n = O_P(1) (strict version).

*Proof.* (E1) If g_i ≥ (n − 1)φ₀² are the eigenvalues of G_A, D_A = ∏_i ((n + 1)g_i + 1)/(g_i + 1)
= ∏_i (n + 1)(1 − x_i) with x_i := n/((n + 1)(g_i + 1)) ≤ 1/((n − 1)φ₀²) ≤ 0.01 for n ≥ n₀; and
log(1 − x) ∈ [−2x, 0] on [0, ½]. (E2) RSS^y_A = yᵀy − z_AᵀG_A⁻¹z_A (G_A invertible), so
Q_A − RSS^y_A = z_Aᵀ(G_A⁻¹ − nH_A⁻¹)z_A. All matrices are functions of G_A and commute;
G_A⁻¹ − nH_A⁻¹ = G_A⁻¹(H_A − nG_A)H_A⁻¹ = G_A⁻¹(G_A + I)H_A⁻¹ = G_A^{−1/2}[(G_A + I)H_A⁻¹]G_A^{−1/2}, and
(G_A + I)H_A⁻¹ has eigenvalues (g + 1)/((n + 1)g + 1) ∈ (0, (1 + 1/((n − 1)φ₀²))/(n + 1)]. Hence
0 ≤ Q_A − RSS^y_A ≤ (1 + 1/((n−1)φ₀²))(n + 1)⁻¹ z_AᵀG_A⁻¹z_A, and z_AᵀG_A⁻¹z_A = ‖P_Ay‖² ≤ ‖y‖² = n − 1. Put
a_A := 0.02 + Q_A − RSS^y_A. (For A = ∅: Q_∅ = RSS^y_∅ = yᵀy, a_∅ = 0.02.)
(E4) −ν log(0.02 + Q_A) = −ν log RSS^y_A − ν log(1 + a_A/RSS^y_A); by L1.2(c) and (E2),
0 ≤ ν log(1 + a_A/RSS^y_A) ≤ ν a_A/(c_E n) ≤ (n/2 + 0.01)(1.02 + 1/((n−1)φ₀²))/(c_E n) ≤ (½ + 0.01/n)(1.03)/c_E
< 0.52/c_E for n ≥ n₀.
Also −ν log RSS^y_A = −ν log RSS_A + ν log(‖Y‖²/(n − 1)), the last term common to all A. Put
R_A := −½η_A − ν log(1 + a_A/RSS^y_A) ∈ [−0.52/c_E, J/((n − 1)φ₀²)] ⊆ [−κ_E, κ_E] for n ≥ n₀ (J/((n−1)φ₀²) ≤ 1), and
c′_n := log c_n + ν log(‖Y‖²/(n − 1)). (E6) is the difference of (E4) for A and A′ plus the prior terms.
The table statement: r_b(U) = m(U)/m(∅), so the c′_n cancel and RSS_{A+l}/RSS_A = 1 − x_{A,l}. ∎

## L1.4 Contrast bounds (used by L3)

**Lemma L1.4.** On 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃, with 𝒱𝒱 ⊇ {r_A − r_{A′} : A, A′ ∈ 𝔉} ∪ {r_A : A ∈ 𝔉}, for all A, A′ ∈ 𝔉
((a), (c) at every n; (b) for n ≥ n₀ of L1.2, so that 0 < RSS_{A′} and RSS_A ≤ C_R n):
(a) RSS_A − RSS_{A′} ≥ (Λ_A − Λ_{A′}) − 2σh_n‖r_A − r_{A′}‖ − σ²t_n;
(b) if RSS_A ≥ RSS_{A′} then ν log(RSS_A/RSS_{A′}) ≥ (RSS_A − RSS_{A′})/(2C_R);
(c) for every ε ∈ (0, 1] and x ≥ 0: 2σh_n√x ≤ εx + σ²h_n²/ε.

*Proof.* (a) Subtract (1.1) for A′ from (1.1) for A: the ‖Cε‖² terms cancel; bound ⟨r_A − r_{A′}, ε⟩ by 𝒟₃ and
−‖P_Aε‖² + ‖P_{A′}ε‖² ≥ −σ²t_n by 𝒟₂. (b) log x ≥ 1 − 1/x gives ν log(RSS_A/RSS_{A′}) ≥ ν(RSS_A − RSS_{A′})/RSS_A
≥ (n/2)(RSS_A − RSS_{A′})/(C_R n) by L1.2(d). (c) AM–GM. ∎

*Counting used later.* If every A ∈ 𝔉 has |A| ≤ J and |𝔉| ≤ C_F n^D, then 𝒱𝒱 := {r_A − r_{A′}} ∪ {r_A} has
|𝒱𝒱| ≤ 2C_F² n^{2D} (C_V = 2C_F²), so D_V = 2D, h_n² = 2(2D + 1) log n and t_n = 4(D + 2) log n are both O(log n).
