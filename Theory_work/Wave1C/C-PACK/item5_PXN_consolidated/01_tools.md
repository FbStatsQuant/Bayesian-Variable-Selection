# Part 1 — Probability tools

Notation and the setting are those of Part 0. Throughout, "for n ≥ n₀" means for n large enough in the sense of §0.5.

## 1.1 [LM] Laurent–Massart

For k ≥ 1 and x > 0: P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x} and P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x} (eqs (4.3)–(4.4) of the cited paper).

## 1.2 Lemma CR (sample-correlation tails) and the corollary [CONC′]

**Lemma CR.** Let (u_i, v_i), i ≤ n (n ≥ 3), be iid bivariate normal with correlation r ∈ (−1,1), and r̂ the Pearson sample
correlation (centred, as computed from the standardised Gram matrix). Then for every δ ∈ (0, 2]:

  P(|r̂ − r| > δ) ≤ 6 exp(−(n−1)δ²/1024).

*Proof.* r̂ is invariant under positive affine maps of each coordinate, so take means 0, variances 1, and write
v = ru + sw, s := √(1−r²), with w iid N(0,1) independent of u. Let C be the centring matrix, N := n−1, and
α := ‖Cu‖²/N, β := ‖Cw‖²/N, γ := ⟨Cu, Cw⟩/N, 𝐌 := [[α, γ], [γ, β]], x := (r, s)ᵀ (‖x‖ = 1), e₁ := (1,0)ᵀ. Since
Cv = rCu + sCw,

  r̂ = e₁ᵀ𝐌x / (√(e₁ᵀ𝐌e₁) · √(xᵀ𝐌x)).

Let η ∈ (0, ¼] and E_η := {|α − 1| ≤ η, |β − 1| ≤ η, |γ| ≤ η}. On E_η, Δ := 𝐌 − I has entries bounded by η, so
‖Δ‖_op ≤ ‖Δ‖_F ≤ √(4η²) = 2η ≤ ½ (four entries, each of absolute value ≤ η). Then |e₁ᵀ𝐌x − r| = |e₁ᵀΔx| ≤ 2η, and
e₁ᵀ𝐌e₁, xᵀ𝐌x ∈ [1−2η, 1+2η], so the denominator d ∈ [1−2η, 1+2η]. Hence

  |r̂ − r| ≤ |e₁ᵀ𝐌x − r|/d + |r|·|1/d − 1| ≤ 2η/(1−2η) + 2η/(1−2η) ≤ 8η.

Probability of E_ηᶜ: Nα and Nβ are χ²_N. Upper tail with x = Nη²/16: 2√(Nx) + 2x = Nη/2 + Nη²/8 ≤ Nη (η ≤ 1), so
P(α − 1 > η) ≤ e^{−Nη²/16}. Lower tail with x = Nη²/4: P(α − 1 < −η) ≤ e^{−Nη²/4}. Same for β. Given u, Nγ = ⟨Cu, w⟩ ~ N(0, Nα)
(w ⊥ u, ⟨Cu, Cw⟩ = ⟨Cu, w⟩); on {α ≤ 1 + η} ⊆ {α ≤ 2}, P(|Nγ| > Nη | u) ≤ 2e^{−N²η²/(4N)} = 2e^{−Nη²/4}. So
P(E_ηᶜ) ≤ 2(e^{−Nη²/16} + e^{−Nη²/4}) + 2e^{−Nη²/4} ≤ 6e^{−Nη²/16}. With η := δ/8 ≤ ¼:
P(|r̂ − r| > δ) ≤ P(E_ηᶜ) ≤ 6e^{−Nδ²/1024}. ∎

**Corollary [CONC′].** For the LH-iid design (any p, rows iid N(0, Σ), Σ a correlation matrix) and any δ ∈ (0, 2]:

  P(max_{j<k} |r̂_jk − Σ_jk| > δ) ≤ 3p² e^{−(n−1)δ²/1024}.

With p ≤ n^A and δ_n := 32√(2(A+1) log n/(n−1)) (≤ 2 for n ≥ n₀(A)): the bound is ≤ 3n^{2A}n^{−2(A+1)} = 3n^{−2}, summable.
So max_{j<k}|r̂_jk − Σ_jk| ≤ δ_n = O(√(log n/n)) with probability ≥ 1 − 3n^{−2}. *Proof.* Union bound over ≤ p²/2 pairs. ∎

*Remark (non-strict form).* The bound is continuous in δ, so P(max_{j<k}|r̂_jk − Σ_jk| ≥ δ*) ≤ 3p² e^{−(n−1)δ*²/1024} for δ* ∈ (0, 2]
(apply [CONC′] at δ ↑ δ*). This is the form used in §2.4.

*Use.* In §2.2: ‖R̂_T − Σ_T‖_op ≤ |T|·δ_n ≤ L_nδ_n = O((log n)^{3/2}n^{−1/2}) → 0, so λ_min(R̂_T) ≥ λ₀/2 for all |T| ≤ L_n once
L_nδ_n ≤ λ₀/2, on an event of probability ≥ 1 − 3n^{−2}. The constant 1/1024 is not optimised; only the exponential-in-n form
and the explicit constants matter.

## 1.3 Lemma Tr-J (Beta truncated moments and tails; any fixed dimension; polynomial families)

**Lemma Tr-J.** Let X ~ Beta(j/2, (m−j)/2) with m := n − 1 − u, integers j ≥ 1, u ≥ 0, m − j ≥ 1. Let ν = 0.01 + n/2.

(a) *(truncated moment; any j, u)* For τ ∈ (0, ½] and e₁ := (u + j + 3)/2 + 0.01,
    E[(1 − X)^{−ν} 1{X ≤ τ}] ≤ 2^{e₁} (mτ/2)^{j/2} / Γ(j/2 + 1).

(b) *(tail; any j, u)* For τ ∈ (0,1): P(X > τ) ≤ exp(−(m−j)/16) + P(χ²_j > τ(m−j)/2).

(c) *(uniform tail over a polynomial family)* Fix J ∈ ℕ, D ≥ 0, C ≥ 1. Let (X_α)_{α∈𝔄_n} be any family (no independence
    assumed) of at most C n^D such variables with 1 ≤ j_α ≤ J and 0 ≤ u_α ≤ n/4. Put t_{n,D} := 8(D+1) log n and τ_{n,D} := t_{n,D}/n.
    Then for n ≥ n₀(J, D, C),
      P(max_α X_α > τ_{n,D}) ≤ C n^D [ e^{−n/32} + n^{−(D+1)} e^{√(2J(D+1) log n)} ] = O(n^{−1} e^{O(√log n)}) → 0.

*Proof.* (a) The density is x^{j/2−1}(1−x)^{(m−j)/2−1}/B(j/2, (m−j)/2). Multiplying by (1−x)^{−ν} gives the exponent
(m−j)/2 − 1 − ν = (n−1−u−j)/2 − 1 − 0.01 − n/2 = −e₁ < 0, so on [0, τ], (1−x)^{−e₁} ≤ (1−τ)^{−e₁} ≤ 2^{e₁}. Next
∫₀^τ x^{j/2−1}dx = (2/j)τ^{j/2}. Finally 1/B(j/2, (m−j)/2) = Γ(m/2)/(Γ(j/2)Γ((m−j)/2)) and, for y > 0 and a > 0,
Γ(y+a)/Γ(y) ≤ (y+a)^a: write a = k + f with k ∈ ℕ₀, f ∈ [0,1); Γ(y+k)/Γ(y) = ∏_{i<k}(y+i) ≤ (y+k)^k, and Wendel's
inequality Γ(z+f)/Γ(z) ≤ z^f (0 ≤ f < 1) at z = y + k gives the rest. With y = (m−j)/2, a = j/2, y + a = m/2:
E ≤ 2^{e₁}(2/j)τ^{j/2}(m/2)^{j/2}/Γ(j/2) = 2^{e₁}(mτ/2)^{j/2}/Γ(j/2+1). No restriction on j or u was used.

(b) X =_d χ²_j/(χ²_j + χ²_{m−j}) with independent chi-squares, so X ≤ χ²_j/χ²_{m−j}. On {χ²_{m−j} ≥ (m−j)/2}, X > τ forces
χ²_j > τ(m−j)/2. [LM] lower tail with x = (m−j)/16: P(χ²_{m−j} ≤ (m−j) − 2√((m−j)·(m−j)/16)) = P(χ²_{m−j} ≤ (m−j)/2) ≤ e^{−(m−j)/16}.

(c) For u ≤ n/4 and n ≥ 8(J+1): m − j ≥ 3n/4 − 1 − J ≥ n/2, so e^{−(m−j)/16} ≤ e^{−n/32} and τ_{n,D}(m−j)/2 ≥ t_{n,D}/4 =: t′.
By [LM] upper tail, P(χ²_j ≥ j + 2√(jx) + 2x) ≤ e^{−x}. Take x := t′/2 − √(j t′). If t′ ≥ 6j then x > 0 and
j + 2√(jx) + 2x ≤ j + 2√(j t′/2) + t′ − 2√(jt′) = t′ + j − (2−√2)√(jt′) ≤ t′ (since (2−√2)√(jt′) ≥ (2−√2)√6 j > j). Hence

  (χ) P(χ²_j > t′) ≤ exp(−t′/2 + √(jt′)) for every t′ ≥ 6j.

With t′ = t_{n,D}/4: P(χ²_j > t′) ≤ exp(−t_{n,D}/8 + √(J t_{n,D}/4)) = n^{−(D+1)} e^{√(2J(D+1)log n)}, since t_{n,D}/8 = (D+1) log n.
The union bound over at most C n^D variables gives C n^{−1} e^{O(√log n)} → 0. The requirement t′ ≥ 6J holds for n ≥ n₀. ∎

*Rate.* If a faster rate is wanted, take t_{n,D} := 8(D+D′+1) log n to get O(n^{−D′−1}e^{O(√log n)}); nothing below needs it.

*Where it is used, and with which (J, u, D):*

| use | J | u ≤ | family size | D |
|---|---|---|---|---|
| P3′ start mass (§3.2): X_{h,V}, V ⊆ C_h ∖ U_h° | g ≤ 16 | 1 | G_n 2^g ≤ 2^{16}n^A | A |
| Lemma Λ(a) (§4.1): null part of A, \|A\| ≤ s₀+2 | s₀+2 | s₀+2 | 2^{gs₀}(p+1)^{s₀+2} | A(s₀+2) |

In both rows u is uniformly bounded by a fixed constant, so u ≤ n/4 holds for all large n; J is fixed.

## 1.4 Lemma E (uniform score expansion on a polynomial family of small sets)

**Setting.** 𝔉 = 𝔉_n is a deterministic (or X-measurable) family of subsets of [p] with |A| ≤ J for all A ∈ 𝔉 and
|𝔉| ≤ C n^D (J, C, D fixed), containing ∅. Fix φ₀ > 0 and M. Let ℰ(𝔉, φ₀) := {λ_min(R̂_A) ≥ φ₀² for every nonempty A ∈ 𝔉}
(an X-event) and ℰ* := ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn} (or any X-measurable subevent of ℰ*). The conclusions hold for n ≥ n₀, where n₀
may depend on J, C, D, φ₀, M, σ².

**Lemma E.** Define c_E := σ²/(12(M + σ²)) and κ_E := 0.52/c_E + 1. There is an event 𝒟 = 𝒟(𝔉) (depending on (X, ε)) with
explicitly

  P(𝒟ᶜ ∩ ℰ*) ≤ 2e^{−n^{1/3}} + C n^D [n^{−4(D+1)} e^{√(8J(D+1) log n)} + 2n^{−2(D+1)}] → 0,

such that on 𝒟 ∩ ℰ*, for every A ∈ 𝔉, simultaneously:

(E1) log D_A = |A| log(n+1) + η_A,  −2|A|/((n−1)φ₀²) ≤ η_A ≤ 0;
(E2) 2b₀ + Q_A = RSS^y_A + a_A,  2b₀ ≤ a_A ≤ 2b₀ + 1 + 1/((n−1)φ₀²);
(E3) RSS_A ≥ nσ²/2 and ‖Y‖² ≤ 3(M+σ²)n; hence RSS^y_A ≥ c_E n;
(E4) F(A) = log w(|A|) − ½|A| log(n+1) − ν log RSS_A + c_n + R_A with |R_A| ≤ κ_E, where c_n does not depend on A;
(E5) |RSS_A − nσ² − Λ_A| ≤ C₂ n^{2/3} with the admissible explicit constant C₂ = 4σ√(M(D+1)) + σ²[5 + 8(D+1)], for n ≥ n₀.

In particular, for A, A′ ∈ 𝔉 (A′ ≠ A):

  F(A) − F(A′) = log[w(|A|)/w(|A′|)] − ½(|A| − |A′|) log(n+1) + ν log(RSS_{A′}/RSS_A) + (R_A − R_{A′}),  |R_A − R_{A′}| ≤ 2κ_E.   (E6)

*Proof.* Write G := G_A = (n−1)R̂_A with eigenvalues g_i ≥ (n−1)φ₀² on ℰ*, and H := (n+1)G + I.

(E1) D_A = det H/det(G+I) = ∏_i ((n+1)g_i + 1)/(g_i + 1) = ∏_i (n+1)[1 − n/((n+1)(g_i+1))]. With x_i := n/((n+1)(g_i+1)) ≤
1/((n−1)φ₀²) ≤ ½ for n ≥ n₀, log(1 − x_i) ∈ [−2x_i, 0]; sum over the |A| eigenvalues.

(E2) RSS^y_A = yᵀy − z_AᵀG⁻¹z_A and Q_A = yᵀy − n z_AᵀH⁻¹z_A, so Q_A − RSS^y_A = z_Aᵀ(G⁻¹ − nH⁻¹)z_A. The matrices commute, and
G⁻¹ − nH⁻¹ = G⁻¹(H − nG)H⁻¹ = G⁻¹(G+I)H⁻¹, with eigenvalues (g_i+1)/(g_i((n+1)g_i+1)) ∈ [0, (1 + 1/g_i)/((n+1)g_i)]. Hence
0 ≤ Q_A − RSS^y_A ≤ (1 + 1/((n−1)φ₀²))/(n+1) · z_AᵀG⁻¹z_A = (1 + 1/((n−1)φ₀²))/(n+1) · ‖P_Ay‖² ≤ 1 + 1/((n−1)φ₀²), using
‖P_Ay‖² ≤ ‖y‖² = n−1. Put a_A := 2b₀ + Q_A − RSS^y_A. For A = ∅, a_∅ = 2b₀.

(E3) Since Cμ = μ and P_AC = P_A (centred columns), RSS_A = ‖Π_A^⊥(μ + ε)‖² = Λ_A + 2⟨Π_A^⊥μ, ε⟩ + ‖Π_A^⊥ε‖², and
‖Π_A^⊥ε‖² = ‖Cε‖² − ‖P_Aε‖². Given X: ‖Cε‖²/σ² ~ χ²_{n−1}; ‖P_Aε‖²/σ² ~ χ²_{|A|}; ⟨Π_A^⊥μ, ε⟩ ~ N(0, σ²Λ_A). Let 𝒟 be the
intersection of:
 (d1) ‖Cε‖²/σ² ∈ [n − 1 − 2√((n−1)n^{1/3}), n − 1 + 2√((n−1)n^{1/3}) + 2n^{1/3}] — probability ≥ 1 − 2e^{−n^{1/3}} by [LM];
 (d2) max_{A∈𝔉} ‖P_Aε‖²/σ² ≤ 8(D+1) log n — by stochastic domination by χ²_J and the bound (χ) of Lemma Tr-J(c) with
      t′ = 8(D+1) log n (x = t′/2 − √(Jt′)), and a union bound; failure probability ≤ C n^D n^{−4(D+1)} e^{√(8J(D+1) log n)};
 (d3) max_{A∈𝔉, Λ_A>0} |⟨Π_A^⊥μ, ε⟩|/(σ√Λ_A) ≤ √(4(D+1) log n) — Gaussian tail 2n^{−2(D+1)} each, union bound.
No independence among (d1)–(d3) and none across sets is used. On 𝒟 ∩ ℰ*:
RSS_A ≥ Λ_A − 2σ√(Λ_A · 4(D+1) log n) + σ²(n − 1 − 2√((n−1)n^{1/3})) − 8(D+1)σ² log n. The first two terms, as a quadratic in
√Λ_A ≥ 0, are ≥ −4(D+1)σ² log n. So RSS_A ≥ σ²[n − 1 − 2n^{2/3} − 12(D+1) log n] ≥ nσ²/2 for n ≥ n₀. Also
‖Y‖² = ‖μ + Cε‖² ≤ 2‖μ‖² + 2‖Cε‖² ≤ 2Mn + 2σ²(n + 3n^{2/3}) ≤ 3(M+σ²)n for n ≥ n₀. Then RSS^y_A = (n−1)RSS_A/‖Y‖² ≥
(n−1)σ²/(6(M+σ²)) ≥ c_E n for n ≥ 2.

(E4) log m(A) = const − ½ log D_A − ν log(2b₀ + Q_A) = const − ½|A| log(n+1) − ½η_A − ν log RSS^y_A − ν log(1 + a_A/RSS^y_A).
On 𝒟 ∩ ℰ*, 0 ≤ ν log(1 + a_A/RSS^y_A) ≤ ν a_A/(c_E n) ≤ (n/2 + 0.01)(1.02 + 1/((n−1)φ₀²))/(c_E n) ≤ 0.52/c_E for n ≥ n₀.
And −ν log RSS^y_A = −ν log RSS_A + ν log(‖Y‖²/(n−1)), the second term common to all A. Put R_A := −½η_A − ν log(1 + a_A/RSS^y_A)
∈ [−0.52/c_E, J/((n−1)φ₀²)] ⊆ [−κ_E, κ_E], and c_n := const + ν log(‖Y‖²/(n−1)) − log W_K.

(E5) From the decomposition in (E3): |RSS_A − nσ² − Λ_A| ≤ 2σ√(Mn · 4(D+1) log n) + σ²(1 + 2n^{2/3} + 2n^{1/3}) + 8(D+1)σ² log n
≤ C₂ n^{2/3}, using √(log n) ≤ n^{1/6}, log n ≤ n^{2/3}, and 1, n^{1/3} ≤ n^{2/3} for n ≥ n₀; this gives C₂ = 4σ√(M(D+1)) + σ²[5 + 8(D+1)].
(E6) is (E4) for the two sets (c_n cancels). ∎

*Remarks.* (1) Lemma E needs no block structure. (2) The signal-norm bound is used to control ‖Y‖² and hence the standardised RSS
floor in (E3), and to obtain the uniform n^{2/3} approximation in (E5). The raw-scale RSS lower bound itself does not require it.
(3) *Within-group application.* For 𝔉 = {U ⊆ C_h : h ≤ G_n} the table expansion is

  log r̃_h(U + l) − log r̃_h(U) = −½ log(n+1) − ν log(1 − x_{U,l}) + R_{U+l} − R_U,  x_{U,l} := 1 − RSS_{U+l}/RSS_U,       (1.1)

with |R_{U+l} − R_U| ≤ 2κ_E =: κ (the size prior cancels in a table ratio). (4) *All small sets.* For 𝔉_n := {A : |A| ≤ s₀+2},
Lemma E is the uniform expansion (U1) of §4.2, with the explicit remainder bounds −0.52/c_E ≤ R_A ≤ J/((n−1)φ₀²).

**The two applications (their events are different because the families are different).**
- **𝒟_start** := the event of Lemma E for 𝔉_start := {U ⊆ C_h : h ≤ G_n} ∪ {∅}: J = g, D = A, C = 2^{16} (|𝔉_start| ≤ 2^{16}n^A under SIZE).
- **𝒟_search** := the event of Lemma E for 𝔉_n := {A ⊆ [p] : |A| ≤ s₀+2}: J = s₀+2, D = A(s₀+2), C = 2^{s₀+2} (|𝔉_n| ≤ (p+1)^{s₀+2} ≤ 2^{s₀+2}n^{A(s₀+2)}).

Each has P(𝒟ᶜ ∩ ℰ♯_n) ≤ 2e^{−n^{1/3}} + C n^D [n^{−4(D+1)} e^{√(8J(D+1) log n)} + 2n^{−2(D+1)}] with its own (J, D, C). 𝒟_start is used
in §3 and 𝒟_search in §4. The Tr-J thresholds are indexed by D: t_{n,D} = 8(D+1) log n, τ_{n,D} = t_{n,D}/n. (The event ℰ♯_n, on which both
applications take place, is defined in §2.2; it implies ℰ(𝔉, φ₀) and ‖μ‖² ≤ Mn for both families.)
