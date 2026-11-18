# X-a-2
stop_reason: end_turn

# Card X, route X-a — Lemma X proved as stated, with explicit constants

**Result.** Lemma X holds as stated, with c = ½, C′ = 32, C depending only on A, and M₀, n₀ depending on (s₀^r, A, σ*², M, M′, c_D, κ₀); c_D enters only n₀. The route is X-a with two simplifications:

- Lemma V is replaced by a one-line bound, Q_{S₀} − Q_S ≤ σ*²χ²_J + ‖P_{S₀}e‖² + ρ′ (step B).
- Lemma S (a candidate, not proved elsewhere) is not consumed; the size tail above m_n(t) is proved directly (step A).

The three S1-06 factors are budgeted before Markov in step B. Below Q_S := Q^c_S, ρ′ := (‖μ‖² + ‖θ*‖²)/n ≤ M + M′, and ℓ(S) := w(|S|) D_S^{−1/2}(2b + Q_S)^{−ν} for every S ⊆ [p], so π(S)/π(S′) = ℓ(S)/ℓ(S′) on Ω.

## 0. Constants

- C′ := 32, j₁ := ⌈C′t/log n⌉, d_t = s₀ + j₁, c := ½.
- a₁ := 4A + 6; τ_k := a₁k log n + 4t for k ≥ 1, τ₀ := 0.
- a₂ := 33(A+1) + 1; a₃ := 33a₁ + 4; a₄ := 50.
- λ := max{32a₂, 4a₃ + 4, 47}; a₅ := a₃ + 2√(2a₂λ) + λ; a₆ := 2(a₅ + 11).
- C := max{4(a₄ + a₃ + λ), a₆}.
- From [P1] §1 and `lem:den`: b₋ = 0.005σ*², b₊ = 0.01(2(σ*² + M) + 1), κ = (b₊/b₋)^{0.51}, c_IG = min_{[σ*², 2σ*²]} IG(·; 0.51, b₊), c♯ := κ²/(c_IGσ*²), 𝓑_n = {b₋ ≤ b ≤ b₊}.
- K₁ := max_{s ≤ s₀^r} sup_{j≥1}(j+1)^s 2^{−j}.
- M₀ := max{16, s₀^r(A+3) + 2, a₁s₀^r, 8 + 2(M+M′)/σ*², 4 log(2c♯), log(4K₁)}.

Consequences of t ≥ M₀ log n ≥ M₀ (log n ≥ 1, log(n+1) ≤ 2 log n, p ≤ n^A):

- (k1) t ≥ 16; (s₀+1) log n ≤ t; 2s₀ + 1 ≤ t; a₁s₀ log n ≤ t; (M+M′)/σ*² ≤ t/2; 4K₁ ≤ e^t.
- (k2) 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} ≤ e^{s₀(A+3) log n} ≤ e^t, and 2(2p)^{s₀}(n+1)^{s₀/2} ≤ e^t.
- (k3) d_t ≤ d_t log n ≤ (s₀+1) log n + 32t ≤ 33t. Hence for k ≤ d_t: τ_k ≤ a₃t, and x_k := k(A log n + 1) + t ≤ a₂t.
- (k4) m_n(t) + s₀ ≤ 2s₀ + 1 + [(s₀(A+2) + 2) log n + 3t]/log 2 ≤ 7t.

Sequences depending only on (n, A, κ₀), valid for all t ≤ n^{1−κ₀} (so t/N ≤ 2n^{−κ₀}):

- δ̄_n := 2√2·n^{−κ₀/2} + 2(7a₁ log n + 6)n^{−κ₀};
- ε_n := (n + 0.02)/((n−1)(1 − δ̄_n)) − 1;
- q_n² := e(a₁+1) log n/(2c_D(n+1)).

n₀ is the least n ≥ 16 beyond which all of the following hold; each involves n and the constants only, so n₀ is one threshold for the whole t-range:

- (n1) δ̄_n ≤ ½, ε_n ≤ ¼, ε_na₁ log n ≤ log 2;
- (n2) 4n^{−κ₀/2} + 8n^{−κ₀} ≤ ½, and 2M/(n−1) + 2σ*²(4n^{−κ₀/2} + 4n^{−κ₀}) ≤ 1;
- (n3) 2b₊ + M + M′ + Nσ*²(4n^{−κ₀/2} + 4n^{−κ₀}) ≤ Nσ*²;
- (n4) n^{κ₀} ≥ 100, a₆n^{−κ₀/2} ≤ 1, 2b₊/σ*² ≤ √n;
- (n5) 4q_n² ≤ n^{−1/2}.

## 1. Tools

- **T1 (Gamma and χ² tails).** For Γ ~ Gamma(ν, 1) and x > 0: P(Γ > ν + √(2νx) + x) ≤ e^{−x} and P(Γ < ν − √(2νx)) ≤ e^{−x}. Reference: Boucheron–Lugosi–Massart, *Concentration Inequalities* (2013), §2.4. The proof is Chernoff with log E e^{λ(Γ−ν)} = ν(−log(1−λ) − λ) ≤ νλ²/(2(1−λ)) on [0, 1) and ≤ νλ²/2 for λ < 0. With χ²_d = 2Γ(d/2) this is Laurent–Massart (2000), Lemma 1: P(χ²_d − d > 2√(dx) + 2x) ≤ e^{−x}, P(χ²_d − d < −2√(dx)) ≤ e^{−x}.
- **T2.** [P1] `lem:chi`(a): r ≤ d ⇒ P(χ²_r ≥ 2d log 2 + 4x) ≤ e^{−x}. [P1] `lem:chi`(c): E[e^{χ²_d/2}1{χ²_d ≤ τ}] = (τ/2)^{d/2}/Γ(d/2+1) ≤ (eτ/d)^{d/2} for d ≥ 1.
- **T3.** [P1] `lem:prior`: (a) W_K ≤ 1; (b) w(k)/w(k+1) = (2p−k−1)/(k+1) ≤ 2p; proof of (c): Σ_{k>m}q_k ≤ 2^{−m} for m ≥ 0; (e) C(p−s₀, j)w(s₀+j)/w(s₀) ≤ 2(j+1)^{s₀}2^{−j} when s₀ + j ≤ p. Also 1/w(s₀) = 2C(2p−1, s₀) ≤ 2(2p)^{s₀}.
- **T4.** [P1] `lem:spec`: (d) S ⊆ S′ ⇒ Q_{S′} ≤ Q_S; (e) D_S = Πf(λ_i(G_S)), f(λ) = ((n+1)λ+1)/(λ+1) ∈ [1, n+1) increasing. Hence 1 ≤ D_S ≤ (n+1)^{|S|}. For S ⊆ S′, Cauchy interlacing gives λ_i(G_{S′}) ≤ λ_i(G_S) for i ≤ |S| (increasing order), so D_{S′}/D_S ≤ Π_{i>|S|}f(λ_i(G_{S′})) ≤ (n+1)^{|S′∖S|}.
- **T5.** [P1] `thm:T01i` + `thm:Ta` (deterministic, S₀ ∈ Ω): on 𝓑_n, π(E) ≤ κ² I_{b₋}(E)/(ϖ(S₀)m^c_{b₊}(S₀)) for every E ⊆ Ω. [P1] `lem:num`: E[I_{b₋}(E)/f₀(y_c)] = ϖ(E), f₀ the N(μ_c, σ*²I) density.
- **T6 (exact-reference denominator).** With E′ := ‖e‖²/σ*² and Λ := |E′ − N|/(2√n) + E′/(2n) + ρ′/(2σ*²):
  m^c_{b₊}(S₀)/f₀(y_c) ≥ D_{S₀}^{−1/2}c_IGσ*²n^{−1/2}e^{−Λ}.
  *Proof.* By the min-representation at φ = θ*_{S₀}, Q_{S₀} ≤ ‖y_c − X_{c,S₀}θ*‖² + θ*ᵀ(G_{S₀}+I)θ*/n = ‖e‖² + ρ′ (for s₀ = 0: Q_∅ = ‖e‖², ρ′ = 0). The paragraphs "Integral representation", "Lower bound on the exponent" and "Assembling" of [P1] `lem:den` use only Q_{S₀} ≤ σ*²E′ + R with R ≥ 0 and u ≥ 1; take R = ρ′ and do not apply D_{S₀} ≤ (n+1)^{s₀}. ∎ (This is `B_tail_approx.md` Steps 2–3 with r = 0.)
- **T7 (D1 identities).** With a_S := (I − M_S)μ_c: ‖a_S‖² ≤ L_S (as 0 ⪯ I − M_S ⪯ I); Q_S = L_S + 2eᵀa_S + eᵀ(I − M_S)e; ‖e‖² − ‖P_Se‖² ≤ eᵀ(I − M_S)e ≤ ‖e‖²; M_Sy_c − μ_c = M_Se − a_S with ‖M_Se‖ ≤ ‖P_Se‖ (M_S² ⪯ M_S ⪯ P_S). Also ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖ (U is an isometry).

## 2. The event 𝓔

Fix n ≥ n₀ and t ∈ [M₀ log n, n^{1−κ₀}]. For ∅ ≠ J ⊆ [p]∖S₀ put S_J := S₀ ∪ J and χ²_J := ‖(P_{S_J} − P_{S₀})e‖²/σ*². This is exactly χ²_{d_J}, d_J = rank X_{S_J} − rank X_{S₀} ≤ |J|, because the difference is an orthogonal projection of that rank. Let 𝓔 be the intersection of:

- **(N1)** |E′ − N| ≤ 2√(Nt) + 2t. Failure ≤ 2e^{−t} (T1).
- **(N2)** ‖P_Te‖² ≤ σ*²τ_{|T|} for every ∅ ≠ T ⊆ [p].
- **(N3)** χ²_J ≤ τ_{|J|} for every ∅ ≠ J ⊆ [p]∖S₀.
- **(N4)** |eᵀa_S| ≤ σ*‖a_S‖√(2x_{|S|}) for every S ⊆ [p] (S = ∅: a_∅ = μ_c, x₀ = t).
- **(M1)** N_m ≤ e^tϖ(|S| > m) at m := m_n(t), where N_m := I_{b₋}({|S| > m})/f₀(y_c). Failure ≤ e^{−t} (T5, Markov).
- **(M2)** V ≤ e^{−6t}, V defined in step B. Failure ≤ e^{−t} (step B).

For (N2), (N3): 2k log 2 + 4x_k ≤ (4A+6)k log n + 4t = τ_k, the rank is ≤ k, and there are ≤ p^k ≤ n^{Ak} sets of size k. By T2(a) the failure probability is ≤ Σ_{k≥1}n^{Ak}e^{−x_k} = e^{−t}Σ_{k≥1}e^{−k} ≤ 0.6e^{−t} each. For (N4): eᵀa_S ~ N(0, σ*²‖a_S‖²), so failure ≤ Σ_{k≥0}n^{Ak}·2e^{−x_k} ≤ 3.2e^{−t}.

Total: **P(𝓔ᶜ) ≤ 8.4e^{−t} ≤ 2e^{−t/2}** (t ≥ 16).

**On 𝓔 the scale event 𝓑_n holds.** ‖y_c‖² = ‖μ_c‖² + 2μ_cᵀe + ‖e‖².
- Lower: by (N4) at S = ∅, ‖y_c‖² ≥ ‖μ_c‖² − 2σ*‖μ_c‖√(2t) + ‖e‖² ≥ ‖e‖² − 2σ*²t ≥ Nσ*²(1 − 2√(t/N) − 4t/N) ≥ Nσ*²/2 by (n2).
- Upper: ‖y_c‖² ≤ 2nM + 2‖e‖² ≤ N[2M + 2σ*² + 2M/(n−1) + 2σ*²(2√(t/N) + 2t/N)] ≤ N(2(σ*² + M) + 1) by (n2).

So b₋ ≤ b ≤ b₊ on 𝓔.

## 3. Step A: π(|S| > m_n(t)) ≤ e^{−t} on 𝓔

Let m = m_n(t). If m = K the mass is 0. Otherwise (m − s₀) log 2 ≥ s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t. By T3, R_m := ϖ(|S| > m)/ϖ(S₀) ≤ 2(2p)^{s₀}2^{−m} ≤ 2^{1−s₀}(n+1)^{−(s₀+2)/2}e^{−3t}. With D_{S₀} ≤ (n+1)^{s₀} this gives R_m√(D_{S₀})√n ≤ 2e^{−3t}.

On 𝓔 ⊆ 𝓑_n, T5, T6 and (M1) give

π(|S| > m) ≤ κ²N_m/(ϖ(S₀)m^c_{b₊}(S₀)/f₀) ≤ c♯e^{t+Λ}R_m√(D_{S₀})√n ≤ 2c♯e^{−2t+Λ}.

By (N1): |E′ − N|/(2√n) ≤ √t + t/√n ≤ t/2 (t ≥ 16, n ≥ 16), and E′/(2n) ≤ 2. So Λ ≤ t/2 + 2 + (M+M′)/(2σ*²) ≤ 3t/4, since M₀ ≥ 8 + 2(M+M′)/σ*². Hence π(|S| > m) ≤ 2c♯e^{−5t/4} ≤ e^{−t}, since M₀ ≥ 4 log(2c♯).

## 4. Step B: π(d_t < |S| ≤ m_n(t)) ≤ e^{−t} on 𝓔

Let j̄ := min(m_n(t), p − s₀).

**B1 (one superset).** Fix J with 1 ≤ j := |J| ≤ j̄, S := S_J. Since μ_c ∈ col X_{c,S}, by (N1), (N2) and (k4):

Q_S ≥ ‖(I − P_S)e‖² = ‖e‖² − ‖P_Se‖² ≥ σ*²(N − 2√(Nt) − 2t − 7a₁t log n − 4t) ≥ Nσ*²(1 − δ̄_n) > 0.

By T6's first line and ‖P_Se‖² = ‖P_{S₀}e‖² + σ*²χ²_J:

0 ≤ Q_{S₀} − Q_S ≤ (‖e‖² + ρ′) − (‖e‖² − ‖P_Se‖²) = ρ′ + ‖P_{S₀}e‖² + σ*²χ²_J.

Since Q_{S₀} ≥ Q_S > 0 and b > 0, ((2b + Q_{S₀})/(2b + Q_S))^ν ≤ (Q_{S₀}/Q_S)^ν ≤ exp{ν(Q_{S₀} − Q_S)/Q_S}, and ν/Q_S ≤ (1 + ε_n)/(2σ*²). The three factors:

1. *S₀-noise and reference cost (j-independent).* By (N2) at T = S₀, (k1), (n1): (1+ε_n)[ρ′/σ*² + τ_{s₀}]/2 ≤ (5/8)[t/2 + t + 4t] ≤ 3.5t.
2. *Variance surcharge.* By (N3), (1+ε_n)χ²_J/2 ≤ χ²_J/2 + ε_nτ_j/2, and ε_nτ_j/2 = ε_na₁j log n/2 + 2ε_nt ≤ (j/2) log 2 + t/2 by (n1).
3. *Multiplicity* is handled in B2.

So on 𝓔:

ℓ(S_J)/ℓ(S₀) ≤ e^{4t}·[w(s₀+j)/w(s₀)](D_{S₀}/D_{S_J})^{1/2}·2^{j/2}e^{χ²_J/2}1{χ²_J ≤ τ_j}.

**B2 (all models of these sizes, through S ∪ S₀).** Let S ∈ Ω with d_t < |S| ≤ m_n(t), J′ := S∖S₀, S′ := S₀ ∪ J′. Then j₁ + 1 ≤ |S| − s₀ ≤ |J′| ≤ min(|S|, p − s₀) ≤ j̄, and each J′ arises from at most 2^{s₀} sets S. For every data set ([T03R] (C6)(a), re-derived):

ℓ(S)/ℓ(S′) = [w(|S|)/w(|S′|)](D_{S′}/D_S)^{1/2}((2b + Q_{S′})/(2b + Q_S))^ν ≤ (2p)^{s₀}(n+1)^{s₀/2},

by T3(b), T4 and Q_{S′} ≤ Q_S. Define

V := Σ_{j=j₁+1}^{j̄}[w(s₀+j)/w(s₀)]Σ_{|J|=j, J∩S₀=∅}(D_{S₀}/D_{S_J})^{1/2}2^{j/2}e^{χ²_J/2}1{χ²_J ≤ τ_j}.

Then on 𝓔, with π(S₀) ≤ 1, B1 and (k2):

π(d_t < |S| ≤ m_n(t)) ≤ Σ_S ℓ(S)/ℓ(S₀) ≤ 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}e^{4t}V ≤ e^{5t}V ≤ e^{−t} by (M2).

**B3 (probability of (M2)).** V ≥ 0 has a deterministic index set. For d := d_J ≥ 1, T2(c) gives E[e^{χ²_J/2}1{χ²_J ≤ τ_j}] ≤ (eτ_j/d)^{d/2} ≤ (eτ_j/j)^{j/2}, because d ↦ (eτ/d)^{d/2} is nondecreasing on d ≤ τ and d ≤ j ≤ τ_j. For d = 0 the expectation is 1 ≤ (eτ_j/j)^{j/2}. For j > j₁ ≥ 32t/log n, 4t/j ≤ log n, so eτ_j/j ≤ e(a₁+1) log n: **the truncation level per added variable is free of t beyond d_t**. By (ND; c_D, m_n(t)) on j ≤ j̄ and T3(e):

E V ≤ Σ_{j>j₁}2(j+1)^{s₀}2^{−j}[c_D(n+1)]^{−j/2}(2e(a₁+1) log n)^{j/2} = Σ_{j>j₁}2(j+1)^{s₀}q_n^j ≤ 2K₁Σ_{j>j₁}(2q_n)^j ≤ 4K₁n^{−(j₁+1)/4} ≤ 4K₁e^{−8t},

using 2q_n ≤ n^{−1/4} ≤ ½ (n5) and (j₁+1) log n ≥ 32t. By Markov and (k1), P(V > e^{−6t}) ≤ 4K₁e^{−2t} ≤ e^{−t}.

## 5. Step C: far small models

Let 𝒰 := {S ∈ Ω : |S| ≤ d_t, L_S > λσ*²t}. Claim: π(𝒰) ≤ e^{−t} on 𝓔.

For S ∈ 𝒰, by T7, (N4), (N2), (k3): Q_S ≥ L_S − 2σ*√(2a₂tL_S) + ‖e‖² − σ*²a₃t. With Q_{S₀} ≤ ‖e‖² + ρ′ and ρ′ ≤ σ*²t:

D := Q_S − Q_{S₀} ≥ L_S − 2σ*√(2a₂tL_S) − σ*²(a₃+1)t.

Since L_S ≥ 32a₂σ*²t, the square-root term is ≤ L_S/2; since L_S ≥ 4(a₃+1)σ*²t, D ≥ L_S/4 > λσ*²t/4 > 0.

On 𝓔, B₀ := 2b + Q_{S₀} ≤ 2b₊ + M + M′ + Nσ*²(1 + 2√(t/N) + 2t/N) ≤ 2Nσ*² by (n3). Using log(1+u) ≥ (log 2)min(u, 1):

- if D < B₀: ν log(1 + D/B₀) ≥ (n/2)(log 2)(λσ*²t/4)/(2Nσ*²) ≥ (log 2)λt/16 ≥ 2t (λ ≥ 47);
- if D ≥ B₀: ν log 2 ≥ 0.34n ≥ 2t by (n4).

Hence ℓ(S)/ℓ(S₀) ≤ [w(|S|)/w(s₀)](D_{S₀}/D_S)^{1/2}e^{−2t} ≤ [w(|S|)/w(s₀)](n+1)^{s₀/2}e^{−2t}. Since Σ_{S∈Ω}w(|S|) = W_K ≤ 1 and by (k2):

π(𝒰) ≤ Σ_{S∈𝒰}ℓ(S)/ℓ(S₀) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−2t} ≤ e^{−t}.

## 6. Step D: good models

Let 𝒜 := {S ∈ Ω : |S| ≤ d_t, L_S ≤ λσ*²t} and Bad′ := {‖μ̂ − μ‖² > Cσ*²t} ∪ {|v/σ*² − 1| > C√(t/n)}. Claim: on 𝓔, Π(Bad′ | S, y) ≤ 3e^{−t} for every S ∈ 𝒜.

*Deterministic bounds on 𝓔.* By T7, (N2), (N4), (k3):

- ‖M_Sy_c − μ_c‖² ≤ 2‖P_Se‖² + 2L_S ≤ 2σ*²(a₃ + λ)t;
- |Q_S − ‖e‖²| ≤ ‖P_Se‖² + 2|eᵀa_S| + L_S ≤ σ*²(a₃ + 2√(2a₂λ) + λ)t = σ*²a₅t.

With (N1) and t ≤ √(nt): |Q_S − Nσ*²| ≤ σ*²(a₅ + 4)√(nt).

*Variance.* Γ := (b + Q_S/2)/v ~ Gamma(ν, 1) given (S, y). By T1, outside conditional probability 2e^{−t}, |2Γ − (n + 0.02)| ≤ 2√((n + 0.02)t) + 2t ≤ 5√(nt). Then v/σ*² − 1 = [(2b + Q_S)/σ*² − 2Γ]/(2Γ). The numerator is ≤ 1.02 + (a₅+4)√(nt) + 2b₊/σ*² + 5√(nt) ≤ (a₅+11)√(nt) in absolute value, and the denominator is ≥ n − 5√(nt) ≥ n/2 by (n4). So |v/σ*² − 1| ≤ a₆√(t/n) ≤ 1, and v ≤ 2σ*².

*Mean.* Given (v, S, y), X_{c,S}(θ − θ̂_S) ~ N(0, vM_S), so its squared norm is vΣλ_iξ_i² with λ_i ∈ [0, 1) and at most rank ≤ |S| ≤ d_t nonzero terms; it is ≤ vχ²_r with r ≤ d_t. By T2(a) and (k3) (2d_t log 2 + 4t ≤ a₄t): Π(‖X_{c,S}(θ − θ̂_S)‖² > va₄t | v, S, y) ≤ e^{−t}. Off this event and the variance event:

‖μ̂ − μ‖² ≤ 2‖X_{c,S}(θ − θ̂_S)‖² + 2‖M_Sy_c − μ_c‖² ≤ 4σ*²(a₄ + a₃ + λ)t ≤ Cσ*²t.

So Π(Bad′ | S, y) ≤ 2e^{−t} + e^{−t}.

## 7. Assembly

On 𝓔, with Bad := Bad′ ∪ {|S| > d_t}:

Π(Bad | y) ≤ π(|S| > m_n(t)) + π(d_t < |S| ≤ m_n(t)) + π(𝒰) + max_{S∈𝒜}Π(Bad′ | S, y) ≤ e^{−t} + e^{−t} + e^{−t} + 3e^{−t} = 6e^{−t} ≤ e^{−t/2}.

(If d_t ≥ m_n(t) the second term is void.) With P(𝓔ᶜ) ≤ 2e^{−t/2} this is

**P_e[Π(‖μ̂ − μ‖² > Cσ*²t or |v/σ*² − 1| > C√(t/n) or |S| > d_t | y) > e^{−ct}] ≤ 2e^{−ct}, c = ½,**

for all n ≥ n₀ and all M₀ log n ≤ t ≤ n^{1−κ₀}. ∎

## 8. Remarks

1. **Where each hypothesis enters.**
   - (E): 𝓑_n, B₀, and ρ′.
   - (C): only through ρ′ ≤ M + M′ (T6, B1, C). An approximate reference with B_T(ϑ) ≤ B would pick up the εᵀr term of `B_tail_approx.md` Step 2; not done here.
   - (ND): only B3, and only on j₁ < j ≤ min(m_n(t), p − s₀).
   - p ≤ n^A: union bounds and (k2).
   - κ₀: only n₀ (δ̄_n log n → 0, t/n → 0).
   - No eigenvalue floor on S₀ or elsewhere.
2. **Budget versus ROUTES §2 (S1-06).** Factor (1) costs e^{3.5t}, factor (3) costs e^{t/2}·2^{j/2}, factor (2) costs e^t; the total e^{5t} is beaten by E V ≤ 4K₁e^{−C′t/4}. Because 4t/j ≤ log n for j > d_t − s₀, the t-part of the truncation is absorbed per variable, so log(n/t) ≥ κ₀ log n is not needed and C′ = 32 is numerical. Failure points (a)–(d) of ROUTES X4 are met: one n₀; the J-dependent weights are replaced by the envelope (eτ_j/j)^{j/2} before (ND) averages; unions S ∪ S₀ ∉ Ω are allowed since ℓ is defined on all subsets and (ND) runs to min(m_n(t), p − s₀); the size clause is on the same event.
3. **Externals consumed.** [P1] `thm:T01i`, `thm:Ta`, `lem:num`, the computation in `lem:den`, `lem:spec`(d),(e), `lem:prior`, `lem:chi`; the Gamma/χ² tail T1 (BLM §2.4; Laurent–Massart Lemma 1). Lemma V, Lemma S, [P2] Claims A, B, E and D(b) are not consumed.
4. The constants are not optimised (C is of order 10⁴(A+1)).

ATTEMPT X/X-a RESULT=PROVED GAPS=0
