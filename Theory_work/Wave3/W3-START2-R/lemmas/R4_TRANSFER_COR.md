# R4 — Transfer (T3⁺⁺)(a); Corollaries F1⁺⁺, F2⁺⁺, F3⁺⁺; Proposition OVL⁺⁺; Corollary MIS⁺⁺

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE = `Theory_work/Wave3/W3-START/` (v1.3.4), PARENT = `Theory_work/Wave3/W3-START2/` (v1.4.1); a short
citation `:a-b` continues the file cited last; `STATEMENT.md` without prefix is this ticket's v1.5.
Statement proved: `STATEMENT.md` §3.1 [TRANSFER] (`:167-188`), [F1], [F2], [F3] (`:129-133`), [OVL] (`:212-214`), [MIS]
(`:189-198`). Uses: (T1⁺⁺) of `lemmas/R1_VIS.md` (START-F⁺⁺, including its uniform form (d) and the high-probability form
of BASE Corollary L6.0′ under (D3)); BASE `lemmas/L8_TRANSFER.md` (L8.0, L8.1), BASE `lemmas/L6_COROLLARIES.md` (L6.1,
L6.3), BASE `lemmas/L10_INTERFACES.md` (L10.3); PARENT `lemmas/P1_LEADING.md` (P1.6), PARENT `lemmas/P2_OVL.md`.

## R4.1 (T3⁺⁺)(a): transfer

Setting and admissibility as in `STATEMENT.md:167-175` (fixed constants A, M, g_*, s̄ and c_V or (c_m, ε₀); visibility
(V-cp) or (V-mp) of (D3)). The convention off the admissible designs is BASE `lemmas/L8_TRANSFER.md:16-20`.

**Measurability.** ϱ_n = ϱ_n(Q(X^r); h(X^r)) and R^♯_n (defined on {Q = S₀}, 0 elsewhere) are measurable functions of X^r
(they are finite sums and maxima of measurable functions of (X, θ*(X^r), Q(X^r), h(X^r)); {Q = S₀} is measurable). The
set of admissible designs at n is measurable (finitely many measurable inequalities). **Extension off the admissible designs [T8-SA2].** The convention of `STATEMENT.md:186-187` sets ϱ_n, R^♯_n and b_n(h) to 0 where their defining expressions are not available; this is a definition, and what has to be proved is that the extended functions are measurable. (1) The set where the formulas are available, D_n := {p ≥ 1} ∩ {h is a level vector for Q}, is Borel: {p ≥ 1} is a finite union of the open sets {Cx_j ≠ 0}; Q and S₀ take finitely many values and are measurable (Q by hypothesis; S₀ = supp β on the retained columns), so the design space splits into finitely many measurable cells on which Q and S₀ are constant, and on a cell {1 ≤ h_l ≤ z_n for all l ∉ Q} is a finite intersection of measurable sets. (2) On each cell inside D_n the functions are finite sums and finite maxima of J_h(δ_{U,l}, τ_U) over fixed index sets (the paragraph above); the projection P_U is a Borel function of the design, being the pointwise limit of the continuous maps X_U(X_UᵀX_U + λI)⁻¹X_Uᵀ as λ ↓ 0, and J_h(d, t) is an integral of a jointly measurable nonnegative integrand, hence measurable in (d, t, h) by Tonelli. (3) A function that is measurable on each of finitely many measurable cells and equal to 0 on the measurable complement is measurable. No supremum over an uncountable set and no selection is involved.

**(a1).** Fix ε ∈ (0, 1) and κ ∈ (0, κ_V). For s ∈ {0, 1, …, s̄} let C_s, c_{0,s}, n_{0,s} be the constants of (T1⁺⁺)(d)
(`lemmas/R1_VIS.md`) for (ε, κ) and the fixed constants with s₀ := s (the visibility exponent κ_V does not depend on s₀).
Put **C := max_s C_s, c₀ := min_s c_{0,s}, n₀ := max_s n_{0,s}**. Define the measurable sets of (design, response) pairs
  B₁ := {1 − π₀(𝓛(Q(x))) > C·ϱ_n(Q(x); h(x)) + n^{−κ}},   B₂ := {Q(x) = S₀(x), o₀ > C·R^♯_n(x) + n^{−κ}}.
By BASE L8.1 (BASE `lemmas/L8_TRANSFER.md:27-31`), f_{B_i}(x) := ∫1{(x, α(x)1 + xβ(x) + e) ∈ B_i}N_n(0, σ²I)(de) is a version of
P(B_i | X^r = x), and for a fixed x it is the probability of B_i under Setting F with the fixed design x, coefficient β(x)
and the fixed targets (θ*(x), S₀(x), Q(x), h(x)). Let n ≥ n₀ and let x be admissible at n with ϱ_n(Q(x); h(x)) ≤ c₀, and put
s := |S₀(x)| ≤ s̄. The tuple (x, θ*(x), Q(x), h(x)) satisfies every requirement of (T1⁺⁺)(d) with s₀ = s, and c₀ ≤ c_{0,s},
n ≥ n_{0,s}, C ≥ C_s. So the first display of (T1⁺⁺)(d) gives f_{B₁}(x) ≤ ε + b_n(h(x)); if moreover Q(x) = S₀(x), the second
display gives f_{B₂}(x) ≤ ε + b_n(h(x)) (with C ≥ C_s and R^♯_n(x) the bracket of that display). Hence, almost surely,
P(B₁ | X^r) ≤ ε + b_n(h) on {X^r admissible, ϱ_n ≤ c₀}, and P(B₂ | X^r) ≤ ε + b_n(h) on {X^r admissible, Q = S₀, ϱ_n ≤ c₀}.
These are the two displays of (a1). ∎

**(a2).** Assume P(X^r admissible at n) → 1, b_n(h) → 0 and ϱ_n → 0 in probability. Fix κ ∈ (0, κ_V), put
κ″ := (κ + κ_V)/2, and fix ε ∈ (0, 1). Take (C, c₀, n₀) of (a1) for (ε, κ″). Let 𝒢_n := {X^r admissible at n, ϱ_n ≤ c₀}.
For n ≥ n₀, with B₁ for κ″:
  P(B₁) ≤ P(𝒢_nᶜ) + E[1_{𝒢_n}·min(1, ε + b_n(h))] ≤ P(𝒢_nᶜ) + ε + E[min(1, b_n(h))].
P(𝒢_nᶜ) → 0 by the assumptions, and E[min(1, b_n(h))] → 0 (bounded convergence; b_n(h) → 0 in probability). So
limsup P(B₁) ≤ ε. Put B_n := min(1 − π₀(𝓛(Q)), n^{−κ″}) and A_n := 1 − π₀(𝓛(Q)) − B_n = (1 − π₀(𝓛(Q)) − n^{−κ″})₊. Then
1 − π₀(𝓛(Q)) = A_n + B_n, n^κB_n ≤ n^{κ−κ″} → 0, and {A_n > Cϱ_n} ⊆ B₁, so limsup P(A_n > Cϱ_n) ≤ ε. As ε is arbitrary,
A_n = O_P(ϱ_n) (`STATEMENT.md:45-48`): 1 − π₀(𝓛(Q)) = O_P(ϱ_n) + o_P(n^{−κ}).
If moreover P(Q = S₀) → 1: P(o₀ > CR^♯_n + n^{−κ″}) ≤ P(B₂) + P(Q ≠ S₀) and
P(B₂) ≤ P(𝒢_nᶜ ∪ {Q ≠ S₀}) + ε + E[min(1, b_n(h))] (apply (a1) on 𝒢_n ∩ {Q = S₀}); the same split
A_n := (o₀ − n^{−κ″})₊, B_n := min(o₀, n^{−κ″}) gives o₀ = O_P(R^♯_n) + o_P(n^{−κ}). ∎

**(a3).** Under (a2), if ϱ_n = O_P(ϱ̄_n) with deterministic ϱ̄_n → 0: for ε > 0 take K with limsup P(ϱ_n > Kϱ̄_n) ≤ ε and C
with limsup P(A_n > Cϱ_n) ≤ ε ((a2)); then {A_n > CKϱ̄_n} ⊆ {A_n > Cϱ_n} ∪ {ϱ_n > Kϱ̄_n}, so limsup P(A_n > CKϱ̄_n) ≤ 2ε:
1 − π₀(𝓛(Q)) = O_P(ϱ̄_n) + o_P(n^{−κ}). The same argument with R^♯_n = O_P(r̄_n) (r̄_n deterministic, ≥ 0; no limit needed)
gives o₀ = O_P(r̄_n) + o_P(n^{−κ}) when P(Q = S₀) → 1.
*(T3⁺)(a) of PARENT `STATEMENT.md:120-133` under (D3) and |S₀| ≤ s̄.* Its hypotheses give measurable 𝒳_n with
P(X^r ∈ 𝒳_n) → 1 on which every design is admissible (now with (D3) and |S₀| ≤ s̄), b_n(h) ≤ b̄_n → 0 and ϱ_n ≤ ϱ̄_n → 0.
So P(X^r admissible) → 1, b_n(h) → 0 and ϱ_n → 0 in probability, and ϱ_n = O_P(ϱ̄_n). For "Q = S₀" (Q ≡ S₀ as functions
of X^r) with R^♯_n ≤ r̄_n on 𝒳_n: P(Q = S₀) = 1 and R^♯_n = O_P(r̄_n). Both conclusions of (T3⁺)(a) follow from the
previous paragraph. ∎
(For |S₀| ≡ s₀ and visibility (V-c)/(V-m), which imply (V-cp)/(V-mp) (`STATEMENT.md:63-69`; `lemmas/R1_VIS.md`), this is
(T3⁺)(a) itself: supersession row TRANSFER.)

## R4.2 Corollaries F1⁺⁺, F2⁺⁺, F3⁺⁺

The proofs of BASE F1 (BASE `lemmas/L6_COROLLARIES.md:28-45`), BASE F3 (BASE `lemmas/L6_COROLLARIES.md:62-72`) and PARENT F2⁺
(PARENT `lemmas/P1_LEADING.md:128-144`)
use the visibility hypothesis at exactly these places, and nowhere else:
| proof | where visibility enters | under (D3) |
|---|---|---|
| F1 (iii) (BASE `lemmas/L6_COROLLARIES.md:37-41`) | Corollary L6.0′ for an exponent κ₃ ∈ (κ, κ_V) | L6.0′ under (D3) (`lemmas/R1_VIS.md`) |
| F1 (iv) (BASE `lemmas/L6_COROLLARIES.md:42-45`) | (T1)(a) | (T1⁺⁺)(a) |
| F3 (BASE `lemmas/L6_COROLLARIES.md:62-72`) | Corollary L6.0′ for κ < κ_V | L6.0′ under (D3) |
| F2⁺ (ii)–(v) (PARENT `lemmas/P1_LEADING.md:133-142`) | (T1⁺)(b) for κ ∈ (0, κ_V); κ_V > ½ in (v) | (T1⁺⁺)(b); κ_V of (D3) |
Every other step of these proofs is a deterministic bound on 𝔏_n(Q), 𝔏^♯_n or ϱ_n from Lemma J (BASE
`lemmas/L3_LEAK.md:9-23`), the gain hypotheses of the corollary, p ≤ n^A (z̄_n; κ_L(η, A)), or (T0) — none involves
visibility. Corollary L6.0′ (BASE `lemmas/L6_COROLLARIES.md:19-26`) depends on visibility only through the threshold
n*(κ) of BASE L6.0 (`:11-17`: n ≥ n₃ or n₄ of the visibility bridge for κ′ = (κ + κ_V)/2), which `lemmas/R1_VIS.md`
supplies under (D3) with the constants of (D3). Hence F1, F2⁺, F3 hold verbatim with "visibility with exponent κ_V"
read as (V-cp) or (V-mp) with κ_V of (D3), and (T1⁺⁺) for (T1), (T1⁺): this is F1⁺⁺, F2⁺⁺, F3⁺⁺. (The constant A in
κ_L(η, A), η_A and z̄_n remains the exponent of p ≤ n^A.) ∎

## R4.3 Proposition OVL⁺⁺

PARENT `lemmas/P2_OVL.md` uses visibility at one place only: "*P(𝓐) → 1.* The hypotheses of (T1⁺)(a) hold … so
π₀(𝓛(Q)) ≥ ½ … This is the only place where visibility and (AL) are used" (PARENT `lemmas/P2_OVL.md:45-47`). Under
(V-cp), or (V-mp) with this Q, the hypotheses of (T1⁺⁺)(a) hold (with (E), (GF-16), (AL) for Q), and (T1⁺⁺)(a) gives
1 − π₀(𝓛(Q)) → 0 in probability, hence P(π₀(𝓛(Q)) ≥ ½) → 1. The rest of PARENT P2 (the deterministic identity P2.1 and
the bounds on m_l from the toolkit, PARENT `lemmas/P2_OVL.md:50-58`) uses no visibility condition. So OVL⁺ holds with (D3): OVL⁺⁺. ∎

## R4.4 Corollary MIS⁺⁺

**Substitution.** BASE L10.3 (BASE `lemmas/L10_INTERFACES.md:63-87`) with the claims of version 1.5. Under (GR), Lemma R′
(BASE `lemmas/L10_INTERFACES.md:71-73`) gives y^r = (α + a)1 + X^r_𝒞β^𝒞 + ε′, ε′ ~ N_n(0, σ_𝒞²I) (conditionally on X^r_𝒞 in the random form). For a fixed
candidate design the candidate data follow Setting F with (p, β, σ², S₀) := (p_𝒞, β^𝒞, σ_𝒞², S₀^𝒞); every claim of version 1.5
that is a statement about the coded start under Setting F (VIS-c⁺⁺, VIS-m⁺⁺, START-F⁺⁺, F1⁺⁺–F4⁺⁺, NEC-b⁺⁺, NEC⁺⁺, OVL⁺⁺,
IF-START⁺⁺(a), and the unchanged (C0), (C1), (T0), LEAK-0) therefore holds for π₀^𝒞 whenever its hypotheses hold after the
substitution, exactly as BASE `lemmas/L10_INTERFACES.md:77-83`. The Gaussian-row claims (B-R⁺⁺), (T3⁺⁺)(b), IF-START⁺⁺(b)–(c) have Setting R
among their hypotheses; after the substitution they apply whenever the candidate data satisfy Setting R (raw candidate
rows iid Gaussian, θ^𝒞 deterministic on the standardised scale, ε′ independent of the design) and the other substituted
hypotheses — a premise, not a consequence of (GR). **Random candidate designs:** BASE `lemmas/L10_INTERFACES.md:84-87` with (T3⁺⁺)(a) in place of
(T3)(a): conditionally on X^r_𝒞 this is the setting of R4.1 with X^r := X^r_𝒞, α := α + a(X^r_𝒞), β := β^𝒞(X^r_𝒞),
σ² := σ_𝒞², and S₀^𝒞, Q, h measurable functions of X^r_𝒞 with |S₀^𝒞| ≤ s̄ on the admissible designs.

**Gaussian-row instance.** Assume the raw rows (x_{𝒞,i}, x_{𝓜,i}), i ≤ n, are iid N(m, Σ) with Σ_{𝒞𝒞} nonsingular, ε ~ N_n(0, σ²I)
is independent of X^r = [X^r_𝒞, X^r_𝓜], and τ² := β_𝓜ᵀ(Σ_{𝓜𝓜} − Σ_{𝓜𝒞}Σ_{𝒞𝒞}⁻¹Σ_{𝒞𝓜})β_𝓜 does not depend on n. Put
γ := Σ_{𝒞𝒞}⁻¹Σ_{𝒞𝓜}β_𝓜 and a := m_𝓜ᵀβ_𝓜 − m_𝒞ᵀγ (deterministic). For each row, (x_{𝒞,i}, ω_i) with ω_i := x_{𝓜,i}ᵀβ_𝓜 is jointly
Gaussian, so the conditional law of ω_i given x_{𝒞,i} is N(m_𝓜ᵀβ_𝓜 + β_𝓜ᵀΣ_{𝓜𝒞}Σ_{𝒞𝒞}⁻¹(x_{𝒞,i} − m_𝒞), τ²) = N(a + x_{𝒞,i}ᵀγ, τ²).
The rows are independent, so given X^r_𝒞 the vector ξ := ω − a1 − X^r_𝒞γ has iid N(0, τ²) entries: ξ | X^r_𝒞 ~ N_n(0, τ²I).
ξ is a function of X^r and ε is independent of X^r, so given X^r_𝒞, ξ and ε are independent and ε ~ N_n(0, σ²I). With τ² ≥ 0
fixed, this is (GR) in its conditional form (C-MIS `Theory_work/Wave1C/C-MIS/STATEMENT.md:54-56`) with deterministic
(a, γ). Hence β^𝒞 = β_𝒞 + γ and S₀^𝒞 = supp β^𝒞 are deterministic, and the random-candidate clause applies with no further
premise on the omitted block; the substituted admissibility conditions (in particular |S₀^𝒞| ≤ s̄) remain premises. ∎
