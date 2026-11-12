# W3-START2 — PLAN (lead: Claude Fable 5.2, effort high, Claude Work)

Ticket brief: `BRIEF.md`. Protocol: `Theory_work/Wave3/PROTOCOL.md` (rules 9–16). BASE := `Theory_work/Wave3/W3-START/`
(frozen; never edited). Target: `STATEMENT.md` v1.4 — the four improvements BT2-P1…P4 of the start-mass statement.
Each change re-proves only the steps it touches and cites BASE lemma lines for the rest.

## 1. Legs
| leg | output | reviewer |
|---|---|---|
| CP1 | `STATEMENT.md` v1.4, this plan, `LOG.md`; frozen manifest SL1 | Sol statement lock (Codex gpt-6.1-sol, high, blind) |
| CP2 / final | `lemmas/P1_LEADING.md`, `P2_OVL.md`, `P3_NEC.md`, `P4_BR.md`; `REPORT.md` with registry block; citecheck | two Sol line checks (P1+P3; P2+P4); council (Sol + Opus 5.5 on Claude Work, high) on one frozen manifest |

## 2. Two places where the target is stronger than the brief's wording (both imply it)
* **P1.** The brief replaces the term 15√(2/π)z_n/p of the leading functional by 1/p. By (J0) every summand of
  𝔏^♯_n(h) is ≥ ¼ and there is at least one null, so 1/p ≤ 4𝔏^♯_n(h): the term is dropped altogether and the factor 5
  goes into the constants.
* **P4.** The brief asks |Q| ≤ n^{1/2−ε_Q}. The Gaussian bridge never uses the size of Q, and the fixed-n inequality
  behind (T3)(b) either applies (when (|Q| + 1)n^{−1/2}e^{C_R√log n} < 1) or is trivial (when it is ≥ 1, since the left
  side is ≤ 1). So the only size condition kept is |Q| ≤ K; |Q| ≤ n^{1/2−ε_Q} is the stated special case.

## 3. Proof sketches (what each proof file will contain)

**P1 — Lemma LEAK-0, (T1⁺)(b),(d), F2⁺, (T3⁺)(a), IF-START⁺.**
1. Split the nulls: 𝒩_exc := {l ∉ S₀ : U*_{b(l)} = S₀} (the block of l contains every truth) and 𝒩_prop := the rest.
   For s₀ ≥ 1 one block at most contains S₀ and it has ≤ 16 columns, so |𝒩_exc| ≤ 16 − s₀ ≤ 15 (empty if s₀ ≥ 16);
   both sets are functions of X.
2. T₁ ≤ ((s₀ + 1)/p)·Σ_{l∉S₀} r_b(U*_b ∪ l)/r_b(U*_b) (BASE `lemmas/L3_LEAK.md:86`).
3. Proper columns: U*_{b(l)} ⊊ S₀, |U*_{b(l)}| ≤ 15, so J_{h_l}(δ_{U*,l}, τ_{U*}) ≤ p𝔏^♯_n(h) ≤ p√n and the gain is small
   (BASE `lemmas/L3_LEAK.md:61-62`); the step bound L3.3 (`:51-53`) on 𝓔^blk ∩ 𝓩_h, a truncated expectation and
   Markov's inequality give the proper part ≤ λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h) outside an event of probability e^{2κ_E+1}/λ.
4. Exceptional columns: δ_{S₀,l} = 0, τ_{S₀} = σ, Z_{S₀,l} ~ N(0, 1). With H := √(2 log(λ/(15e^{2κ_E+1}))) ≤ z_n, on
   {|Z_{S₀,l}| ≤ H for l ∈ 𝒩_exc} (failure ≤ 30e^{−H²/2} = 450e^{2κ_E+1}/λ) L3.3 gives each step ≤ e^{2κ_E+1}(n + 1)^{−1/2}e^{H²/2};
   the ≤ 15 steps with the prior factor (s₀ + 1)/p give ≤ λ(s₀ + 1)n^{−1/2}/p ≤ 4λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h).
5. (T1⁺)(d): the proof of BASE Proposition L5.2(ii) (`lemmas/L5_ASM_STARTF.md:49-67`) with the event
   {T₁ ≤ 5λ(s₀ + 1)n^{−1/2}𝔏^♯_n(h)} in place of 𝓜₀; its failure probability 451e^{2κ_E+1}/λ is ≤ ε/4 for the same
   λ = 4c_L/ε, and λ is in the admissible range once 1/log n ≤ ε/2. Same c₀ and n₀; C′ gets 5λ(s₀ + 1) in its first
   term. (T1⁺)(b) from (d) as in BASE L5.3(b). (a), (c) unchanged.
6. F2⁺: BASE L6.2(i)–(ii) bound every term of 𝔏^♯_n by C_F n^{η′/2} ((J1)); nothing else is needed, so the hypothesis
   p/√log n → ∞ goes. (T3⁺)(a): BASE L8.2(ii), L8.3 with the new (d). IF-START⁺: BASE L10.1 with the new rate.

**P2 — Proposition OVL⁺.** Exact identity 1/π₀(S₀) = [Z_𝓛/γ₀(S₀)]/π₀(𝓛(Q)), Z_𝓛 := Σ_{T∈𝓛(Q)}γ₀(T). For T = S₀ ∪ N,
N ⊆ Q ∖ S₀: γ₀(T)/γ₀(S₀) ≤ ∏_{l∈N}(|Q|m_l/p) by the path bound (P3) and the chain bound (CH) (BASE
`lemmas/L1_AGG_FLOOR.md:19-32`); summing, Z_𝓛/γ₀(S₀) ≤ ∏_{l∈Q∖S₀}(1 + |Q|m_l/p) (deterministic). π₀(𝓛(Q)) → 1 by (T1⁺)(a)
under either visibility condition. The bound m_l ≤ n^{(a_l−1)/2+ε/(3q̄)} is steps (iii)–(iv) of BASE L10.2
(`lemmas/L10_INTERFACES.md:44-52`), which use the toolkit only.

**P3 — (N2⁺).** For 1 ≤ s₀ ≤ 15: if every l ∈ I_n had U*_{b(l)} = S₀, the unique block containing S₀ would hold
s₀ + (17 − s₀) = 17 columns; so some l ∈ I_n has U*_{b(l)} ⊊ S₀, and the first such l (a function of X) is a witness for
(C2)(i). For s₀ ≥ 16 every null qualifies. Non-vacuity: s₀ = 1 and sixteen nulls with correlation ρ_n to the truth,
ρ_n² = c(σ² + θ²) log n/((n − 1)θ²), otherwise orthogonal.

**P4 — (B-R⁺), (T3⁺)(b).** In BASE `lemmas/L9_BR.md` the size of Q is used once, at `:161` (ϱ̄_n → 0): L9.1–L9.6 use
only |H_l| ≤ (log n)^{κ_Q} (N_ref, `:95`; P(Eᶜ), `:130`). So (B-R⁺) is L9.1–L9.6 verbatim. For (T3⁺)(b), at each n:
if a_n := (|Q| + 1)n^{−1/2}e^{C_R√log n} ≥ 1 the event is sure; if a_n < 1 then ϱ̄_n = a_ne^{−√log n} ≤ e^{−√log n} ≤ c_{0,n} for n
beyond a threshold that does not depend on Q, and BASE L8.2 in the form L6.0′ applies as in L9.7. The clause C_L = 0
by the same dichotomy with a constant C_ε.

## 4. Risks
* P1: the constant of (T1⁺)(d) must stay ε-dependent only through λ; the exceptional set must be a function of X.
* P2: (V-m) must be assumed with the same Q; lattice concentration alone does not control the mass of S₀ inside
  the lattice — the gain levels a_{n,l} do.
* P3: the count 17 − s₀ and the exclusion of s₀ = 0.
* P4: uniformity of (T1⁺)(d) in Q (it is uniform: the factor |Q| + 1 is inside ϱ_n).
