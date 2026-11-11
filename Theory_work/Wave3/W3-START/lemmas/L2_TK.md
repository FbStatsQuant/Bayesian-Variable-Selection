# L2 — Lemma TK: the toolkit under the constant unnormalised Gram floor — bridge (B-TK), interface [TK]

Status: **PROVED (by this seat, unchecked)**.
Statement proved: `STATEMENT.md` §4 [TK] and §5.2 (B-TK). No registry claim is consumed. The argument follows
`Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md` and `Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md` (sources of the
argument only); the two places where those files use a normalised Gram floor ((E1), (E2)) are redone, the RSS bounds
are put in τ-form, and s₀ = 0 is allowed.

## L2.0 Setting

Setting F of `STATEMENT.md` §1 with s₀ ≥ 0: fixed design, Y = μ + Cε, μ = Xθ* ∈ 1^⊥, ε ~ N_n(0, σ²I), n ≥ 4. Hypotheses:
**(E)** ‖μ‖² ≤ Mn and p ≤ n^A; **(GF-blk)** λ_min(X_UᵀX_U) ≥ g_* > 0 for every nonempty U contained in a block — implied
by (GF-16) for every partition with blocks of size ≤ 16 (bridge (B1)). The partition is a function of X, hence
deterministic here. Family **𝔉 := {U : U ⊆ C_b for some b}** (∅ ∈ 𝔉; |U| ≤ 16; |𝔉| ≤ 2^{16}p: at most p blocks).
By (GF-blk), X_U has full column rank |U| for U ∈ 𝔉, so P_U has rank |U|.
Notation: r_U := (I − P_U)μ, Λ_U = ‖r_U‖², τ²_U = σ² + Λ_U/(n − 1), RSS_U := ‖(I − P_U)Y‖² (Y is centred, so
(I − P_U)Y = (C − P_U)Y), RSS^y_U := ‖(I − P_U)y‖² = (n − 1)RSS_U/‖Y‖² (y = Y/s_y, s_y² = ‖Y‖²/(n − 1)).
Since every column of X is centred: P_UC = P_U, P_U ≼ C, C − P_U is an orthogonal projection, and r_U = (C − P_U)μ.

**(2.1)** RSS_U = Λ_U + 2⟨r_U, ε⟩ + ‖Cε‖² − ‖P_Uε‖².
*Proof.* (C − P_U)Y = r_U + (C − P_U)ε; ⟨r_U, (C − P_U)ε⟩ = ⟨(C − P_U)r_U, ε⟩ = ⟨r_U, ε⟩; ‖(C − P_U)ε‖² = ‖Cε‖² − ‖P_Uε‖². ∎

## L2.1 The event 𝓔^blk

  t_n := 4 log(2^{24}pn),   q_n := √(2 log(2^{17}pn)),
  ω_n := q_n/√(n − 1) + [2√((n − 1)n^{1/3}) + 2n^{1/3} + t_n]/(n − 1).
* 𝒟₁ := {|‖Cε‖²/σ² − (n − 1)| ≤ 2√((n − 1)n^{1/3}) + 2n^{1/3}};
* 𝒟₂ := {‖P_Uε‖² ≤ σ²t_n for every U ∈ 𝔉};
* 𝒟₃ := {|⟨r_U, ε⟩| ≤ σq_n‖r_U‖ for every U ∈ 𝔉};
* **𝓔^blk := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃.**

**Lemma L2.1.** P((𝓔^blk)ᶜ) ≤ 2e^{−n^{1/3}} + 2/n. With p ≤ n^A: t_n ≤ 4(A + 1) log n + 67, q_n² ≤ 2(A + 1) log n + 24, and
ω_n ≤ ω̄_n, where ω̄_n depends only on (n, A) and ω̄_n = O(n^{−1/3}); in particular **ω̄_n log n → 0** (the rate that the
linearisation of a gain of order log n needs, `lemmas/L3_LEAK.md` L3.3).
*Proof.* Explicitly, ω̄_n := √((2(A + 1) log n + 24)/(n − 1)) + [2√((n − 1)n^{1/3}) + 2n^{1/3} + 4(A + 1) log n + 67]/(n − 1).
𝒟₁: ‖Cε‖²/σ² ~ χ²_{n−1}; Laurent–Massart (P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x}, P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}) with
x = n^{1/3}. 𝒟₂: ‖P_Uε‖²/σ² ~ χ²_d with d = |U| ≤ 16 and E exp(χ²_d/4) = 2^{d/2} ≤ 2^8, so P(‖P_Uε‖² > σ²t) ≤ 2^8e^{−t/4};
at t = t_n this is 2^{−16}/(pn); union over ≤ 2^{16}p sets: ≤ 1/n. 𝒟₃: for r_U ≠ 0, ⟨r_U, ε⟩/(σ‖r_U‖) ~ N(0, 1) and
P(|N(0, 1)| > q) ≤ 2e^{−q²/2} = 2^{−16}/(pn) at q = q_n; union: ≤ 1/n (r_U = 0 is trivial). No independence is used.
The bounds on t_n, q_n: log(2^{24}) < 16.64, log(2^{17}) < 11.8. ∎

## L2.2 Consequences on 𝓔^blk

Let n₁ = n₁(A) be such that ω̄_n ≤ ½ for n ≥ n₁. Everything below holds **on 𝓔^blk, for n ≥ n₁, simultaneously for all
sets in 𝔉**.

**(TK-a) τ-form of the RSS.** RSS_U = (n − 1)τ²_U(1 + ρ_U) with |ρ_U| ≤ ω_n. (No energy bound is used here.)
*Proof.* By (2.1), RSS_U − (n − 1)τ²_U = 2⟨r_U, ε⟩ + (‖Cε‖² − σ²(n − 1)) − ‖P_Uε‖². By 𝒟₃ and 2ab ≤ a²c + b²/c
(a = σ, b = √Λ_U, c = √(n − 1)): |2⟨r_U, ε⟩| ≤ 2σq_n√Λ_U ≤ q_n(σ²√(n − 1) + Λ_U/√(n − 1)) = q_n(n − 1)τ²_U/√(n − 1). By 𝒟₁, 𝒟₂
and σ² ≤ τ²_U the other two terms are ≤ τ²_U[2√((n − 1)n^{1/3}) + 2n^{1/3} + t_n] in absolute value. ∎

**(TK-b) Size of the scored residuals.** With C_R := (3/2)(σ² + M) and c_E := σ²/(6(σ² + M)):
0 < ‖Y‖² ≤ C_Rn; RSS_U ≥ (n − 1)σ²/2 > 0; RSS^y_U ≥ c_En.
*Proof.* ‖Y‖² = RSS_∅ ≤ (3/2)(n − 1)τ²_∅ = (3/2)(σ²(n − 1) + ‖μ‖²) ≤ C_Rn by (TK-a) and (E); RSS_U ≥ ½(n − 1)τ²_U
≥ ½(n − 1)σ². Hence RSS^y_U ≥ (n − 1)²σ²/(2C_Rn) ≥ σ²n/(4C_R) = c_En ((n − 1)² ≥ n²/2 for n ≥ 4). ∎

**(TK-c) Score expansion.** Scorer: log m(U) = log c_n − ½ log D_U − ν log(2b₀ + Q_U), D_U := det H_U/det(G_U + I),
H_U = (n + 1)G_U + I, Q_U = yᵀy − n z_UᵀH_U⁻¹z_U, ν = n/2 + 0.01, 2b₀ = 0.02. Then for every U ∈ 𝔉:
  **log m(U) = c′_n − ½|U| log(n + 1) − ν log RSS_U + R_U,   −κ₁ ≤ R_U ≤ κ₂,**
  κ₁ := 0.51(1.02 + 1/g_*)/c_E,  κ₂ := 8 log(1 + 1/g_*),  **κ_E := max(κ₁, κ₂)**,
where c′_n := log c_n + ν log(‖Y‖²/(n − 1)) does not depend on U. κ_E depends only on (g_*, M, σ²).
*Proof.* Let U ≠ ∅ and let g_i ≥ g_* be the eigenvalues of G_U.
(E1) D_U = ∏_i((n + 1)g_i + 1)/(g_i + 1) = (n + 1)^{|U|}∏_i(g_i + 1/(n + 1))/(g_i + 1), and each factor lies in
[g_*/(g_* + 1), 1] (g ↦ g/(g + 1) is increasing). So log D_U = |U| log(n + 1) + η_U with −|U| log(1 + 1/g_*) ≤ η_U ≤ 0.
(E2) G_U is invertible and RSS^y_U = yᵀy − z_UᵀG_U⁻¹z_U, so Q_U − RSS^y_U = z_Uᵀ(G_U⁻¹ − nH_U⁻¹)z_U. All matrices are
functions of G_U; G_U⁻¹ − nH_U⁻¹ = G_U⁻¹(H_U − nG_U)H_U⁻¹ = G_U^{−1/2}[(G_U + I)H_U⁻¹]G_U^{−1/2}, and (G_U + I)H_U⁻¹ has
eigenvalues (g_i + 1)/((n + 1)g_i + 1) ∈ (0, (1 + 1/g_*)/(n + 1)]. Hence
0 ≤ Q_U − RSS^y_U ≤ (1 + 1/g_*)(n + 1)⁻¹·z_UᵀG_U⁻¹z_U, and z_UᵀG_U⁻¹z_U = ‖P_Uy‖² ≤ ‖y‖² = n − 1. So
**0 ≤ Q_U − RSS^y_U ≤ 1 + 1/g_***. Put a_U := 0.02 + Q_U − RSS^y_U ∈ [0.02, 1.02 + 1/g_*].
(E4) −ν log(0.02 + Q_U) = −ν log RSS^y_U − ν log(1 + a_U/RSS^y_U), and by (TK-b)
0 ≤ ν log(1 + a_U/RSS^y_U) ≤ νa_U/(c_En) ≤ (½ + 0.01/n)(1.02 + 1/g_*)/c_E ≤ κ₁. Also
−ν log RSS^y_U = −ν log RSS_U + ν log(‖Y‖²/(n − 1)). So R_U := −½η_U − ν log(1 + a_U/RSS^y_U) ∈ [−κ₁, κ₂].
For U = ∅: D_∅ = 1, Q_∅ = yᵀy = RSS^y_∅, a_∅ = 0.02, R_∅ ∈ [−κ₁, 0]. ∎

**(TK-d) Table ratios.** For U, U′ contained in the same block C_b (r_b(U) = m(U)/m(∅)):
  log[r_b(U)/r_b(U′)] = −½(|U| − |U′|) log(n + 1) − ν log(RSS_U/RSS_{U′}) + (R_U − R_{U′}),   |R_U − R_{U′}| ≤ 2κ_E.

**(TK-e) RSS differences** (identities, valid everywhere). For U ⊆ W in 𝔉, Π := P_W − P_U is an orthogonal projection of
rank |W| − |U| with ΠC = Π, and RSS_U − RSS_W = ‖Π(μ + ε)‖², ‖Πμ‖² = Λ_U − Λ_W. For W = U ∪ {l}: Π = u_{U,l}u_{U,l}ᵀ and
  **RSS_U − RSS_{U∪{l}} = (δ_{U,l} + σZ_{U,l})²**,   Z_{U,l} = u_{U,l}ᵀε/σ ~ N(0, 1).
*Proof.* RSS_U − RSS_W = ‖(P_W − P_U)Y‖² and ΠY = Π(μ + Cε) = Π(μ + ε); ‖Πμ‖² = ‖(I − P_U)μ‖² − ‖(I − P_W)μ‖². ∎

**(TK-f) Log-ratio bounds.** Put 1 + ϑ_n := (n + 0.02)/((n − 1)(1 − ω_n)) (ϑ_n → 0). For U ⊆ W in 𝔉:
(f1) ν log(RSS_U/RSS_W) ≥ (RSS_U − RSS_W)/(2τ²_U(1 + ω_n));
(f2) ν log(RSS_U/RSS_W) ≤ (1 + ϑ_n)(RSS_U − RSS_W)/(2τ²_W);
(f3) if x := (RSS_U − RSS_W)/RSS_U ≤ ½: ν log(RSS_U/RSS_W) ≤ (1 + ϑ_n)(1 + x)(RSS_U − RSS_W)/(2τ²_U).
*Proof.* (f1) −log(1 − x) ≥ x: ν log(RSS_U/RSS_W) ≥ ν(RSS_U − RSS_W)/RSS_U, and ν/RSS_U ≥ (n/2)/((n − 1)τ²_U(1 + ω_n))
≥ 1/(2τ²_U(1 + ω_n)) by (TK-a). (f2) log u ≤ u − 1: ν log(RSS_U/RSS_W) ≤ ν(RSS_U − RSS_W)/RSS_W and
ν/RSS_W ≤ (n/2 + 0.01)/((n − 1)τ²_W(1 − ω_n)). (f3) −log(1 − x) ≤ x + x² on [0, ½] (Σ_{k≥2}x^k/k ≤ x²/(2(1 − x)) ≤ x²), and
ν/RSS_U ≤ (1 + ϑ_n)/(2τ²_U). ∎

## L2.3 Summary ([TK], bridge (B-TK))

Under Setting F (s₀ ≥ 0), (E) and (GF-16): P(𝓔^blk) ≥ 1 − 2e^{−n^{1/3}} − 2/n → 1, and on 𝓔^blk, for n ≥ n₁(A),
(TK-a)–(TK-f) hold on the whole block family, with ω_n ≤ ω̄_n(A) = O(n^{−1/3}) (so ω_n log n → 0) and
κ_E = κ_E(g_*, M, σ²). This is [TK] as stated
in `STATEMENT.md` §4. All bounds are uniform over the designs and coefficient vectors satisfying (E) and (GF-16) with
the same constants (A, M, σ², g_*): this is what (T1)(d) uses.

**Where each hypothesis is used.** (GF-16): full rank of block sets; (E1); (E2). ‖μ‖² ≤ Mn: only (TK-b) (RSS^y_U ≥ c_En,
needed for the remainder of (E4)). p ≤ n^A: only the sizes of t_n, q_n. Gaussian noise: the three tail bounds.
s₀ is not used.
