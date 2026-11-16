# X-c-r2
stop_reason: end_turn

**Route X-c outcome (PARTIAL).** The fit-based route proves Lemma X's mean and variance clauses with (ND) replaced by a weaker "fit–Occam" interface (FO) on a shorter window of sizes, and shows (ND) ⇒ (FO) and the size clause. It rests on Lemma S (Card S), which is not proved here, and the claim that (FO) cannot be dropped altogether is only heuristic. Proofs are compressed and have not been checked by a second reader.

## 0. Notation and noise event

σ := σ*, m := m_n(t), ρ′ := θ*ᵀ(G_{S₀}+I)θ*/n = (‖μ‖²+‖θ*‖²)/n ≤ ρ̄ := M+M′, and L_{S₀} ≤ ρ′ ([P1] `lem:slab`). For S ⊆ [p]:

- F_S := eᵀM_Se (ridge noise fit), k_S := tr M_S ≤ rank X_S (effective dimension), c_S := eᵀ(I−M_S)μ_c, S′ := S∪S₀;
- ℓ(S) := w(|S|)D_S^{−1/2}(2b+Q^c_S)^{−ν} for all |S| ≤ p, so π(S) ≤ ℓ(S)/ℓ(S₀) on Ω;
- S ⊆ T ⇒ M_S ⪯ M_T ([P1] `lem:spec`(d)), hence F_S ≤ F_T, k_S ≤ k_T, L_S ≥ L_T.

C_A := 6+4A. "n ≥ n₀" always means a threshold depending on (s₀^r, A, σ², M, M′, κ₀) and the constants chosen, uniform over M₀ log n ≤ t ≤ n^{1−κ₀}. This is possible because t/n ≤ n^{−κ₀}. For M₀ large, m+s₀ ≤ 5t.

**Event 𝓔_t.**
- (N1) |‖e‖² − Nσ²| ≤ σ²(2√(Nt)+2t). Failure probability ≤ 2e^{−t} (Laurent–Massart 2000, Lemma 1: P(χ²_N−N ≥ 2√(Nx)+2x) ≤ e^{−x}, P(N−χ²_N ≥ 2√(Nx)) ≤ e^{−x}).
- (N2) ‖P_Te‖² ≤ σ²τ̄_{|T|}, τ̄_k := C_Ak log n + 4t, for all T ⊆ [p] with 1 ≤ |T| ≤ m+s₀. Failure probability ≤ e^{−t}: [P1] `lem:chi`(a) with x = k(log p+1)+t, at most p^k sets, and 2k log 2 + 4k(log p+1) ≤ C_Ak log n.

So P(𝓔_tᶜ) ≤ 3e^{−t}. On 𝓔_t, for n ≥ n₀: ‖e‖² ≤ 2Nσ², b ≤ b̄ := 0.02(1.5M+2σ²), and ‖P_{S₀}e‖² ≤ 5σ²t once M₀ ≥ C_As₀.

Fit-good class, for constants C_F, C_L, C_k: 𝔊 := {S : F_S ≤ C_Fσ²t, L_S ≤ C_Lσ²t, k_S ≤ C_kt}.

## 1. Lemma F1: fit-good models contract (no size cut, no design condition, no union over models)

**Claim.** On (N1), for n ≥ n₀ and every S ∈ Ω∩𝔊:
Π(‖μ̂−μ‖² > C₁σ²t or |v/σ²−1| > C₂√(t/n) | S, y) ≤ 3e^{−t}, with C₁ = 4(2C_k+3)+4(C_F+C_L).

*Proof.*
- Card identity (D1(d)): Q^c_S = ‖e‖² − F_S + 2c_S + L_S. Cauchy–Schwarz in the form I−M_S ⪰ 0 gives |c_S| ≤ (eᵀ(I−M_S)e)^{1/2}L_S^{1/2} ≤ ‖e‖√L_S ≤ σ²√(2C_LNt).
- With t ≤ √(Nt): |Q^c_S − Nσ²| ≤ C₃σ²√(Nt). Put β := b+Q^c_S/2; then |β/ν − σ²| ≤ C₄σ²√(t/n) (2ν = N+1.02, b ≤ b̄).
- G := β/v ~ Gamma(ν,1) given (S,y). Sub-gamma tails (Boucheron–Lugosi–Massart 2013, §2.4): P(G ≥ ν+√(2νx)+x) ≤ e^{−x}, P(G ≤ ν−√(2νx)) ≤ e^{−x}. With x = t, off probability 2e^{−t}: |G/ν−1| ≤ 3√(t/n) ≤ ½. Hence |v/σ²−1| ≤ 2(C₄+3)√(t/n) =: C₂√(t/n) and v ≤ 2σ².
- Given v, X_{c,S}(θ−θ̂_S) ~ N(0, vM_S), so its squared norm is vΣλ_iξ_i² with λ_i ∈ [0,1), Σλ_i = k_S. Laurent–Massart: off probability e^{−t} it is ≤ v(k_S+2√(k_St)+2t) ≤ 2σ²(2C_k+3)t.
- ‖M_Sy_c−μ_c‖² ≤ 2‖M_Se‖²+2‖(I−M_S)μ_c‖² ≤ 2F_S+2L_S (M_S² ⪯ M_S, (I−M_S)² ⪯ I−M_S). Add. ∎

Consequence: Π(Bad | y) ≤ 3e^{−t} + π(Ω∖𝔊), with Bad the mean/variance event.

## 2. Lemma F2: far models, at all sizes ≤ m, without a cross-term union bound

Let 𝔅^sup := {S₀∪J : J ⊆ [p]∖S₀, 1 ≤ |J| ≤ m, F_{S₀∪J} > C_Fσ²t or k_{S₀∪J} > C_kt}. Take S ∈ Ω∖𝔊 with |S| ≤ m.

- **(β)** If S′ ∈ 𝔅^sup: ℓ(S)/ℓ(S′) ≤ (2p)^{s₀}(n+1)^{s₀/2} ([T03R] (C6)(a), deterministic, valid for |S′| ≤ p).
- **(γ)** If S′ ∉ 𝔅^sup: F_S ≤ F_{S′} and k_S ≤ k_{S′} force L_S > C_Lσ²t, and I claim that on 𝓔_t, for n ≥ n₀, C_L ≥ 10C_F+10 and M₀ large:
  ℓ(S)/ℓ(S₀) ≤ [w(|S|)/w(s₀)](n+1)^{s₀/2}e^{−c_Lt}, c_L := C_L(log 2)/16.

*Proof of (γ).*
- Split c_S = eᵀ(M_{S′}−M_S)μ_c + eᵀ(I−M_{S′})μ_c. Since M_{S′}−M_S ⪰ 0: |first| ≤ F_{S′}^{1/2}(L_S−L_{S′})^{1/2} ≤ L_S/8 + 2C_Fσ²t.
- a′ := (I−M_{S′})μ_c ∈ col X_{c,S′} with ‖a′‖² ≤ L_{S′} ≤ ρ̄. By (N2): |eᵀa′| = |(P_{S′}e)ᵀa′| ≤ σ√(ρ̄τ̄_{m+s₀}) ≤ σ²t for M₀ large. The same bound holds for c_{S₀}.
- Hence Q^c_S ≥ ‖e‖² + 3L_S/4 − (5C_F+2)σ²t and Q^c_{S₀} ≤ ‖e‖² + 3σ²t, so Q^c_S − Q^c_{S₀} ≥ L_S/4 ≥ C_Lσ²t/4.
- 2b+Q^c_{S₀} ≤ 2Nσ², log(1+u) ≥ (log 2)min(u,1), ν ≥ N/2 give ((2b+Q_{S₀})/(2b+Q_S))^ν ≤ e^{−c_Lt}. Finally D_{S₀}/D_S ≤ (n+1)^{s₀}. ∎

Summing (γ) with Σ_kq_k ≤ 1 and 1/w(s₀) ≤ 2(2p)^{s₀}: π(γ-models) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−c_Lt}.

Each S′ comes from at most 2^{s₀} sets S, so with Amp := 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} ≤ n^{(A+2)s₀}:

  π(Ω∖𝔊) ≤ π(|S|>m) + 2(2p)^{s₀}(n+1)^{s₀/2}e^{−c_Lt} + Amp·Σ_{S_J∈𝔅^sup} ℓ(S_J)/ℓ(S₀).  (2.1)

(S₀ ∉ 𝔅^sup on 𝓔_t, since F_{S₀} ≤ 5σ²t.)

## 3. Lemma F3: supersets — fit capacity versus Occam

Fix η = 1, c = 2. Let M^{(c)}_T := X_{c,T}(G_T + c(G_T+I)/n)⁻¹X_{c,T}ᵀ, S = S_J = S₀∪J with |J| = j ≤ m, and D′ := M_S^{(1/c)} − M_{S₀}^{(c)}.

**(a) Lemma V(a), (b) re-derived.**
- Substituting ϑ = θ*+ϑ′ in the two variational forms and using (a+b)ᵀA(a+b) ≤ (1+η)aᵀAa + (1+1/η)bᵀAb and its reverse form: Q^c_{S₀} − Q^c_S ≤ eᵀD′e + (1+2/η)ρ′.
- 0 ⪯ D′ ⪯ M_S^{(1/c)} ⪯ P_S and ‖D′‖ < 1.
- Woodbury: I − M_T^{(c)} = (Σ_T^{(c)})⁻¹, Σ_T^{(c)} := I + (n/c)X_T(G_T+I)⁻¹X_Tᵀ ⪰ I, det Σ_T^{(c)} = Π(1 + (n/c)g_i/(g_i+1)).
- So D′ = (Σ₀^{(c)})⁻¹ − (Σ_S^{(1/c)})⁻¹ and det(I−D′) ≥ det(I − Σ₀^{1/2}D′Σ₀^{1/2}) = det Σ₀^{(c)}/det Σ_S^{(1/c)} ≥ c^{−(s₀+|S|)}D_{S₀}/D_S.
- Therefore (D_{S₀}/D_S)^{1/2}det(I−D′)^{−1/2} ≤ 2^{s₀+j/2}.

**(b) Variance surcharge.** On 𝓔_t: Q^c_S ≥ ‖(I−P_S)e‖² ≥ Nσ²(1−ε′_t) with ε′_t ≤ 3√(t/N) + τ̄_{5t}/N. So ν/Q^c_S ≤ (1+ε_t)/(2σ²) with ε̃_n := C_Aε_t log n → 0 uniformly in t. Since eᵀD′e ≤ ‖P_Se‖² ≤ σ²τ̄_{s₀+j}:

  ℓ(S_J)/ℓ(S₀) ≤ C_ρe^{6ε̃_nt}[w(s₀+j)/w(s₀)]Y_J,
  Y_J := (D_{S₀}/D_S)^{1/2}e^{eᵀD′e/2σ²}1{‖P_Se‖² ≤ σ²τ̄_{s₀+j}}, C_ρ := e^{3ρ̄/σ²}.

**(c) Two moment bounds.**
- *Tilt.* For a ≥ 0, with κ_i := δ_i/(1−δ_i) and δ_i the eigenvalues of D′_J:
  E[Y_J1{eᵀD′e > aσ²}] ≤ 2^{s₀+j/2}cap_J(a), cap_J(a) := P(Σ_iκ_iξ_i² > a).
  (The Gaussian change of measure e^{xᵀD′x/2σ²}N(0,σ²I) = det(I−D′)^{−1/2}N(0,σ²(I−D′)⁻¹), then (a).)
- *Occam.* E Y_J ≤ (D_{S₀}/D_S)^{1/2}E[e^{χ²_r/2}1{χ²_r ≤ τ̄_{s₀+j}}] ≤ (D_{S₀}/D_S)^{1/2}(e(C_A log n+4t))^{(s₀+j)/2}, r = rank X_S ([P1] `lem:chi`(c); d ↦ (eτ/d)^{d/2} is increasing on d ≤ τ).

**(d) Which supersets are bad.** On 𝓔_t:
- F_S ≤ eᵀD′e + ‖P_{S₀}e‖² ≤ eᵀD′e + 5σ²t, so F-bad ⇒ eᵀD′e > a_tσ² with a_t := (C_F−5)t.
- F_S ≤ ‖P_Se‖² ≤ σ²τ̄_{s₀+j}, so F-bad ⇒ j > j_lo := (C_F−4)t/(C_A log n) − s₀.
- k_S ≤ s₀+j, so k-bad ⇒ j > C_kt − s₀. This is a deterministic class and needs only the trivial bound cap ≤ 1.

**Interface (FO; C_F, C_k, c₁).**
  𝒪^fit_n(t) := Σ_{j_lo<j≤min(C_kt, m, p−s₀)} [w(s₀+j)/w(s₀)]Σ_{|J|=j} min{2^{j/2}cap_J(a_t), (D_{S₀}/D_{S_J})^{1/2}(e(C_A log n+4t))^{(s₀+j)/2}} ≤ e^{−c₁t}.

It is design-measurable. By [P1] `lem:prior`(e), the supersets with j > C_kt − s₀ contribute expectation ≤ Σ_{j>C_kt−s₀}2^{s₀+1}(j+1)^{s₀}2^{−j/2} ≤ C(s₀)e^{−0.28C_kt} with no design condition.

## 4. Theorem Xc (conditional on Lemma S)

Assume p ≤ n^A, s₀ ≤ K, (E; M), (C; M′).

**(i) Without (ND).** If (FO; C_F, C_k, c₁) holds, there are c, C, M₀, n₀ (one n₀ for the whole range) with
P_e[Π(‖μ̂−μ‖² > Cσ²t or |v/σ²−1| > C√(t/n) or tr M_S > C_kt | y) > e^{−ct}] ≤ 2e^{−ct}.
There is no clause on |S|; the effective-dimension clause tr M_S replaces it.

*Proof.* By §1 and (2.1), on 𝓔_t the posterior mass is at most
3e^{−t} + π(|S|>m) + 2(2p)^{s₀}(n+1)^{s₀/2}e^{−c_Lt} + Amp·C_ρe^{6ε̃_nt}V,
where V is the weighted sum of Y_J·1{bad} over a deterministic index set. By §3, E V ≤ C(s₀)e^{−0.28C_kt} + 2^{s₀}e^{−c₁t}. Amp·C_ρ·e^{6ε̃_nt} ≤ e^{ct} for M₀ ≥ C(A+2)s₀/c and n ≥ n₀. Markov's inequality on V gives V ≤ e^{−3ct} off probability e^{−ct}, for c ≤ min(c₁, 0.28C_k)/5. Lemma S gives π(|S|>m_n(t)) ≤ e^{−t} off probability Ce^{−t}+Ce^{−cn}. Take C_L = 10C_F+10, then M₀, then shrink c. ∎

**(ii) (ND; c_D, m_n(t)) ⇒ (FO) and the size clause.** Take the Occam branch. (ND) and `lem:prior`(e) give the j-th term ≤ 2(j+1)^{s₀}(Ct)^{s₀/2}x_n^j, with x_n := ½[e(C_A log n+4t)/(c_D(n+1))]^{1/2} ≤ n^{−κ₀/3} for n ≥ n₀, uniformly since t ≤ n^{1−κ₀}. Summing over j > j_lo gives ≤ n^{Cs₀}exp(−κ₀(C_F−4)t/(3C_A)) ≤ e^{−c₁t} for C_F large. Dropping the fit indicator and summing over j > d_t−s₀ = ⌈C′t/log n⌉ gives e^{−κ₀C′t/3}n^{Cs₀}; since |S| > d_t ⇒ |S′∖S₀| > d_t−s₀, the same Markov step gives Π(d_t < |S| ≤ m | y) ≤ e^{−ct}. So Lemma X as stated follows, given Lemma S. Compared with X-a, step X3 here needs no union bound over cross terms and no size restriction.

**(iii) How far (ND) is weakened.**
- *Range.* (FO) constrains only F-bad supersets with j_lo < j ≤ C_kt, where j_lo ≍ t/log n, instead of all 1 ≤ j ≤ m_n(t) ≈ 4.3t. Sizes above C_kt and all effective-dimension-bad models are handled by the design-free geometric bound.
- *Strength.* Any polynomial Occam decay suffices: average of (D_{S₀}/D_{S_J})^{1/2} ≤ n^{−aj} with a > (1−κ₀)/2, constants scaling as C_F ≍ 1/(a−(1−κ₀)/2).
- *Capacity branch.* If tr κ(J) ≤ a_t/4 and max_iκ_i(J) ≤ κ̄, then cap_J(a_t) ≤ exp(−a_t/(6κ̄)) (Laurent–Massart). So supersets whose new directions have bounded capacity need no Occam factor at all; exact duplicates of S₀-columns have κ = O(1/n). The window may be split into a capacity family and an Occam family.

## 5. Why (FO) cannot simply be dropped (heuristic)

Take S₀ = {1} and nulls x_j = ρx₁ + √(1−ρ²)u_j with u_j orthonormal and orthogonal to x₁, tuned so each new direction has κ ≍ log n. Then per direction cap ≍ 1 and the truncated Occam weight P(|N(0,κ+1)| ≤ √(2 log p)) =: q ≍ 1. The posterior size law is geometric with ratio ≈ q/2, and each selected direction fits ≍ σ² log n of noise. So Π(‖μ̂−μ‖² > Cσ²t | y) ≈ (q/2)^{cCt/log n} = e^{−c′Ct/log n} ≫ e^{−ct}.

If this holds, the exponential form at radius Cσ²t fails without a polynomial Occam or bounded-capacity condition (S-FIT in (15)-form at the sharp rate is false), and only the DIST-2 radius tℓ_n survives. This matches ROUTES §5. It is not a proved counterexample: the LLN for the heavy-tailed Bayes-factor sums and the coupling with the S₀ direction are not controlled.

## GAPs

- **GAP 1.** Lemma S (π(|S| > m_n(t)) ≤ e^{−t} off probability Ce^{−t}+Ce^{−cn}) is used as stated on Card S and not proved here.
- **GAP 2.** §5 (necessity of some condition of type (FO)) is heuristic; no rigorous lower bound is given.

ATTEMPT X/X-c RESULT=PARTIAL GAPS=2
