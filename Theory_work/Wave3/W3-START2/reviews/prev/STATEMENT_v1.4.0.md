# W3-START2 — STATEMENT v1.4 (the four BT2 improvements of the start-mass rate)

Ticket W3-START2, Theory Wave 3. Lead: Claude Fable 5.2 (effort high).
Status of this file: **v1.4.0** (2026-11-12; record in `LOG.md`).
Protocol: `Theory_work/Wave3/PROTOCOL.md`. All results are asymptotic (n → ∞) unless marked *deterministic*.

**This is a delta statement.** BASE := `Theory_work/Wave3/W3-START/` is the frozen ticket W3-START; its statement
BASE `STATEMENT.md` is version 1.3.4. This file states **in full** every definition, assumption and claim of version
1.4 that differs from version 1.3.4, and takes everything else from BASE `STATEMENT.md` by line reference. Version 1.4
of the start-mass statement is: BASE `STATEMENT.md` with the definitions (D1), (D2) of §2 added and with the eight
claims of §3 in place of the claims of the same name. Proofs of the changed steps are supplied in `lemmas/`
(P1–P4), author-proved and awaiting independent acceptance; the status of each claim is recorded outside this file
(the ticket's final checkpoint file and the registry). **No method change is requested.**

## 0. What changes, in one table

| change | claim of v1.4 (this file) | replaces (BASE `STATEMENT.md`) | what is gained |
|---|---|---|---|
| P1 | (D1); Lemma LEAK-0 (new); (T1⁺) START-F; F2⁺; (T3⁺)(a) TRANSFER; IF-START⁺ | `:112-116`, `:245-264`, `:272-275`, `:290-305`, `:334-338` | for s₀ ≥ 1 the leading functional loses its term 15√(2/π)z_n/p; F2 holds with no growth condition on p (bounded p included) |
| P2 | Proposition OVL⁺ | `:339-344` | the overlap bound holds under margin visibility (V-m) as well as (V-c) |
| P3 | Proposition NEC⁺, clause (N2⁺) | `:316-331` | a partition-free leaking-null limit that is not vacuous for 1 ≤ s₀ ≤ 15 |
| P4 | (D2); bridge (B-R⁺); (T3⁺)(b) START-R | `:163-167`, `:237`, `:306-314` | no size restriction on the leakage set Q beyond \|Q\| ≤ K; the bound is informative up to \|Q\| = n^{1/2−ε} |

Each claim of §3 implies the claim it replaces (§5). Nothing else of version 1.3.4 changes: the main clause (Q = S₀,
p ≫ n allowed), its rate, Theorem FLOOR and every hypothesis other than (L-R) are as they were.

## 1. Base (taken from BASE `STATEMENT.md` v1.3.4, unchanged)

* Objects, code pins, Settings F and R, notation: `:39-82`. In particular π₀, γ₀, Ω, K, the block tables r_b, the
  partition (a function of X alone, blocks of size ≤ 16), o₀ := (1 − π₀(S₀))/π₀(S₀), P_U, Λ_U, Δ_U, τ²_U := σ² + Δ_U,
  δ_{U,l}, Z_{U,l}, b(l), U*_b := S₀ ∩ C_b, 𝓛(Q) := {T : S₀ ⊆ T ⊆ Q}, c_Q.
* Quantities: `:84-126` — the table functionals m_l, U_Q, U, T₁, Ξ_b(Q), Ξ, e_n; z_n; level vectors h and their tail
  budget b_n(h); J_h(d, t) and (J0)–(J3); 𝔏_n(Q; h); 𝔏⁰_n(h) (the leading functional **of version 1.3.4**, `:112-116`;
  it keeps this symbol and this meaning here); the block-relative versions; ϱ_n(Q; h); κ_L, κ_V.
* Assumptions: (E), (GF-16), (V-c), (V-m), (AL) (`:135-157`); (FL-R16), (V-R) (`:160-162`); implementation premises
  EX-A, [A:BLOCK-LE-16] (`:169-172`). **(L-R) (`:163-167`) is replaced by (L-R⁺) of §2.**
* Interface properties [TK], [VIS(κ; Q)], [LEAK(Q)], P-START, P-OVL: `:174-191`.
* Claims of version 1.3.4 that are **unchanged, not restated and not re-proved here**; they are used by id:
  (C0) Lemma AGG, (C1) Lemma ASM, (C2) Lemma NEC-b (`:197-226`); the bridges (B1), (B-TK), (B-L), (B-V1), (B-V2)
  (`:232-236`); (T0) Theorem FLOOR (`:241-243`); Corollaries F1, F3, F4 (`:268-271`, `:276-287`); (T6) Corollary MIS
  and (T7) the examples table (`:346-371`). Where one of these refers to (T1), (T3), (T4) or (T5), the claim of the
  same name in §3 may be read in its place, because each implies the one it replaces (§5).
* Constants of the BASE proofs used below: κ_E = κ_E(g_*, M, σ²) and the toolkit event 𝓔^blk of [TK] (`:181`,
  `:187-191`), with P((𝓔^blk)ᶜ) ≤ 2e^{−n^{1/3}} + 2/n (BASE `lemmas/L2_TK.md`, Lemma L2.1); n₂ = n₂(A), the threshold of
  the step bound (BASE `lemmas/L3_LEAK.md:48`).

## 2. Amended definitions and assumptions

**(D1) Sharp leading functional** (Q = S₀; a deterministic function of (X, θ*, σ) and of the level vector h for S₀).
* If s₀ ≥ 1: **𝔏^♯_n(h) := p⁻¹·Σ_{l∉S₀} max{J_{h_l}(δ_{U,l}, τ_U) : U ⊊ S₀, |U| ≤ 15}.**
* If s₀ = 0: 𝔏^♯_n(h) := 𝔏⁰_n(h) = √(2/π)·p⁻¹·Σ_l h_l (unchanged).
* 𝔏^♯_n := 𝔏^♯_n(z_n) (default levels).

(Only **proper** subsets of the truth are conditioned on. For s₀ ≥ 1 this is 𝔏⁰_n(h) of version 1.3.4 without its
last term: 𝔏^♯_n(h) = 𝔏⁰_n(h) − 15√(2/π)z_n/p. Elementary facts, proved in `lemmas/P1_LEADING.md`: for s₀ ≥ 1 and
p > s₀, **(p − s₀)/(4p) ≤ 𝔏^♯_n(h) ≤ 𝔏_n(S₀; h)**; hence 1/p ≤ 4𝔏^♯_n(h), so a functional "𝔏^♯_n(h) + 1/p" — the form
proposed in review BT2-P1 — is between 𝔏^♯_n(h) and 5𝔏^♯_n(h) and gives the same statements.)

**(D2) (L-R⁺) [A:START2-R-L]** (Gaussian rows; replaces (L-R)). Fixed constants C_L ≥ 0 and κ_Q ≥ 1. There are a
deterministic Q = Q_n ⊇ S₀ with **|Q| ≤ K** — no other restriction on the size of Q — and, for every l ∉ Q, a
deterministic H_l ⊇ {l} ∪ S₀ with |H_l| ≤ (log n)^{κ_Q}, such that for every U ⊆ [p] ∖ {l} with |U| ≤ 15, writing
U₀ := U ∩ H_l:
* (L-gain-R) |Cov(W_l, W_j | W_{U₀})| ≤ C_L·n^{−1/2} for j ∈ S₀ ∖ U₀;
* (L-loc-R) |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n for v ∈ U ∖ H_l, j ∈ S₀ ∖ U₀, with a
  deterministic r_n, r_n·(n log n)^{1/4} → 0.

"No leakage" is Q = S₀. (The two displayed conditions and the bound on |H_l| are those of (L-R), word for word; the
only change is that the requirement |Q| ≤ (log n)^{κ_Q} is dropped. The exponent κ_Q now bounds the reference sets
H_l only. (L-R) implies (L-R⁺).)

## 3. Claims of version 1.4

Setting, notation and assumptions as in §1–§2. "X_n = O_P(a_n) + o_P(n^{−κ})" means X_n ≤ A_n + B_n with A_n = O_P(a_n) and
n^κB_n → 0 in probability.

### 3.1 Supporting lemma (new)

**Lemma LEAK-0 (the leading term of the start odds).** Setting F, (E), (GF-16), **s₀ ≥ 1**, s₀ < K, h a level vector
for S₀, n ≥ n₂, and n^{−1/2}·𝔏^♯_n(h) ≤ 1. Then for every λ with 15e^{2κ_E+1} ≤ λ ≤ 15e^{2κ_E+1}·2²¹·p·log n:
  **P(T₁ > 5λ·(s₀ + 1)·n^{−1/2}·𝔏^♯_n(h)) ≤ P((𝓔^blk)ᶜ) + b_n(h) + 451·e^{2κ_E+1}/λ.**
Consequently, along a sequence with b_n(h) → 0 and n^{−1/2}𝔏^♯_n(h) ≤ 1 for all large n: T₁ = O_P(n^{−1/2}𝔏^♯_n(h)). The
bound is uniform in (X, θ*, h). (This sharpens the T₁ clause of [LEAK(S₀)], which has 𝔏^{b,0}_n(h) ≤ 𝔏⁰_n(h) on the
right. The at most 15 null columns that share a block with every truth have zero mean gain; for a bounded number of
such columns a fixed cut-off of the Gaussian tail replaces the level z_n, at the price of a constant that grows as
the allowed failure probability decreases.)

### 3.2 Theorems and corollaries

**(T1⁺) Theorem START-F (fixed design).** Setting F, the start as coded. Assume (E), (GF-16), visibility ((V-c) or
(V-m)), and (AL) for a deterministic Q ⊇ S₀ with |Q| ≤ K, with level vector h (default: h_l = z_n for l ∉ Q, giving
ϱ_n(Q; h) = ϱ_n(Q); when Q = S₀ this also gives 𝔏^♯_n(h) = 𝔏^♯_n and 𝔏_n(S₀; h) = 𝔏_n(S₀)). Then, for every κ ∈ (0, κ_V):
* (a) **lattice form.** 1 − π₀(𝓛(Q)) = O_P(ϱ_n(Q; h)) + o_P(n^{−κ}).
* (b) **no leakage, Q = S₀.** **o₀ = O_P(n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)²) + o_P(n^{−κ})**; in particular π₀(S₀) → 1 in
  probability.
* (c) **first-order form** (Q = S₀). If moreover κ_V > ½ and n^{−1/2}𝔏_n(S₀; h)² → 0, then o₀/T₁ → 1 in probability
  (T₁ > 0 because p > s₀).
* (d) **uniformity.** For every ε > 0 and κ ∈ (0, κ_V) there are C < ∞, c₀ > 0 and n₀ depending only on (ε, κ) and the
  fixed constants (A, M, σ², g_*, s₀ and c_V or (c_m, ε₀)) such that for n ≥ n₀ and every (X, θ*, Q, h) — a fixed
  design with p ≤ n^A retained columns, |supp θ*| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, h a level vector for Q — satisfying at n
  the inequalities ‖μ‖² ≤ Mn, (GF-16), the visibility condition and ϱ_n(Q; h) ≤ c₀:
  P(1 − π₀(𝓛(Q)) > C·ϱ_n(Q; h) + n^{−κ}) ≤ ε + b_n(h), and, for Q = S₀,
  **P(o₀ > C·[n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)²] + n^{−κ}) ≤ ε + b_n(h).**

Clauses (a), (c) and the first display of (d) are those of version 1.3.4, word for word; (b) and the second display
of (d) have 𝔏^♯_n(h) where version 1.3.4 has 𝔏⁰_n(h). For s₀ = 0 nothing changes. Proof structure: as in version 1.3.4
((B1), (B-TK), (B-L), (B-V1)/(B-V2), (C0)), with Lemma LEAK-0 in place of the T₁ clause of [LEAK(S₀)] when s₀ ≥ 1.

**F2⁺ (Corollary; strong signals; Q = S₀).** Setting F, (E), (GF-16), visibility with exponent κ_V, default levels.
Let s₀ ≥ 1, θ*_min ≥ θ_lo > 0 fixed, λ_min(R̂_{S₀}) ≥ φ₀² with a fixed φ₀ ∈ (0, 1], n^{−1/2}𝔏_n(S₀)² → 0, and suppose
δ²_{U,l} ≤ η′·Δ_U·log n for every l ∉ S₀ and every U ⊊ S₀ with |U| ≤ 15, with a fixed η′ ∈ [0, 1). Then
o₀ = O_P(n^{−(1−η′)/2}) + o_P(n^{−κ}) for every κ ∈ (0, κ_V). If η′ = 0 and κ_V > ½: **o₀ is of exact order n^{−1/2}**
(o₀ = O_P(n^{−1/2}), and o₀ ≥ ½(n + 1)^{−1/2} by (T0)). (The hypothesis p/√log n → ∞ of version 1.3.4 is not needed: p may
be bounded, as long as p > s₀.)

**(T3⁺) Theorem START-R (random design).**
* (a) **transfer (any design law; design-measurable targets).** Let X^r be a random raw design and let α, β, Q and a
  level vector h be measurable functions of X^r. Suppose that, conditionally on X^r, y^r = α(X^r)1 + X^rβ(X^r) + ε with
  ε | X^r ~ N_n(0, σ²I), σ² > 0 fixed. Put θ* := D_xβ(X^r), S₀ := supp β(X^r) (after dropping constant columns). Suppose
  there are fixed constants (A, M, g_*, s₀ and c_V or (c_m, ε₀)), deterministic ϱ̄_n → 0 and b̄_n → 0, and measurable
  sets 𝒳_n with P(X^r ∈ 𝒳_n) → 1 such that every design in 𝒳_n satisfies, at n, with its own (θ*, S₀, Q, h): p ≤ n^A
  retained columns, |S₀| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, ‖μ‖² ≤ Mn, (GF-16), the visibility condition, b_n(h) ≤ b̄_n and
  ϱ_n(Q; h) ≤ ϱ̄_n. Then under the joint law, for every κ < κ_V: 1 − π₀(𝓛(Q)) = O_P(ϱ̄_n) + o_P(n^{−κ}), where
  𝓛(Q) = {T : S₀(X^r) ⊆ T ⊆ Q(X^r)}; for Q = S₀, if moreover **n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)² ≤ r̄_n** on 𝒳_n for a
  deterministic r̄_n ≥ 0: o₀ = O_P(r̄_n) + o_P(n^{−κ}), with o₀ the start odds against S₀(X^r). Supports, coefficients,
  sets Q or level vectors selected using the response are not covered. *Convention off the design sets:* as in
  BASE `STATEMENT.md:301-305` (on realisations where the start, the lattice or the odds are not defined, the
  quantities 1 − π₀(𝓛(Q)) and o₀ are set to 0; nothing is claimed about a coded start on invalid inputs). The same
  convention applies in (b).
  (This is clause (a) of version 1.3.4 with 𝔏^♯_n(h) in place of 𝔏⁰_n(h) in the hypothesis of the Q = S₀ clause.)
* (b) **Gaussian rows.** Setting R with p > s₀ for all large n (nothing is claimed when p = s₀). Assume (FL-R16),
  (V-R) and **(L-R⁺)**. Then there is C_R < ∞, depending only on the fixed constants, with
  **P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)·n^{−1/2}·exp(C_R√log n)) → 1.**
  In particular with Q = S₀ (no leakage): P(π₀(S₀) ≥ 1 − n^{−c}) → 1 for every c < ½, for p ≤ n^A including p ≫ n; and
  if |Q| ≤ n^{1/2−ε_Q} for a fixed ε_Q ∈ (0, ½): P(π₀(𝓛(Q)) ≥ 1 − n^{−c}) → 1 for every c < ε_Q. If C_L = 0 (exactly zero
  population leakage): 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)·n^{−1/2}·(log n)^{15κ_Q+1/2}).
  (For a sequence Q_n along which (|Q| + 1)·n^{−1/2}·exp(C_R√log n) ≥ 1 the first display is trivially true, because
  the left side is at most 1; the same holds for the O_P bound. The displays are informative exactly when the
  right side is small — for example for |Q| ≤ n^{1/2−ε_Q}, where version 1.3.4 required |Q| ≤ (log n)^{κ_Q}.)
  Proof structure: bridge (B-R⁺), then the uniform bound (T1⁺)(d) conditionally on the design, as in (a).

**(B-R⁺) Bridge (Gaussian rows).** Setting R with p > s₀ for all large n, (FL-R16), (V-R), (L-R⁺) ⇒ with probability
→ 1 the design satisfies (E) (its energy bound holds with M = s₀²θ_hi²; p ≤ n^A, s₀ fixed and p > s₀ are assumed), the
normalised floor λ_min(R̂_T) ≥ φ₀² for 1 ≤ |T| ≤ 16 with a constant φ₀ > 0 (hence (GF-16)), (V-c) for every fixed c_V,
and 𝔏_n(Q) ≤ exp(C_B√log n), default levels, with a constant C_B depending only on the fixed constants. If C_L = 0:
𝔏_n(Q) = O_P((log n)^{15κ_Q+1/2}) (a tightness statement; a bound with a fixed constant and probability → 1 is not
claimed). (This is (B-R) of version 1.3.4 under (L-R⁺) instead of (L-R).)

**(T4⁺) Proposition NEC (limits; Setting F, (E), (GF-16)).** Ā := limsup log p/log n, A̲ := liminf log p/log n.
* (N1) = (T0): the exponent ½ in (T1⁺)–(T3⁺) is optimal; under F2⁺ with η′ = 0 and κ_V > ½ the order is exact.
* (N2⁺) **leaking nulls.** Let **s₀ ≥ 1** and r(s₀) := max(1, 17 − s₀). Suppose that for all large n there is a
  deterministic set I_n ⊆ [p] ∖ S₀ of r(s₀) distinct null columns such that δ²_{V,l} ≥ c·τ²_V·log n for every l ∈ I_n and
  every **proper** subset V ⊊ S₀ with |V| ≤ 15, with a fixed c > 1 + 2Ā. Then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every
  κ′ < (c − 1 − 2Ā)/2.
  **Scope of (N2⁺).** For s₀ ≥ 16 this is (N2) of version 1.3.4 (one null; every V ⊆ S₀ with |V| ≤ 15 is proper). For
  1 ≤ s₀ ≤ 15 the premise asks 17 − s₀ leaking nulls and can hold (`lemmas/P3_NEC.md` gives a design that satisfies it
  together with (E) and (GF-16)), whereas the premise of (N2) could not. One leaking null is **not** claimed to be
  enough when s₀ ≤ 15: a block can hold all the truths and up to 16 − s₀ nulls, and a null in that block gains nothing
  given the truths; among 17 − s₀ nulls at least one is outside it. The case s₀ = 0 is excluded (there is no proper
  subset of S₀, and no null can leak when μ = 0). On the actual partition, the one-column threshold is (C2)(i).
* (N3) **one weakly visible truth.** If for all large n some truth j = j_n has δ²_{V,j} ≤ c·τ²_V·log n for **every**
  V ⊆ S₀ ∖ {j} with |V| ≤ 15, with a fixed c < 1 + 2A̲, then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 + 2A̲ − c)/2.
* (N4) **outside the hypotheses.** As BASE `STATEMENT.md:329-331` (masked truths: PXN (S) is the law on PXN's
  family; strong-factor designs at p > K: nothing is claimed).

((N1), (N3), (N4) are those of version 1.3.4, word for word, with F2⁺ for F2 in (N1). (N2⁺) and (N3) follow from
(C2).)

**(T5⁺) Interface corollaries.**
* **IF-START⁺.** Under (T1⁺) with (AL) at Q = S₀ and level vector h: for every event 𝒜 and every κ with 0 < κ < κ_V,
  1_𝒜o₀ = O_P(r_n) with the deterministic rate **r_n := n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)² + n^{−κ}** → 0; under (T3⁺)(b)
  with Q = S₀ the same with r_n := n^{−1/2}exp(C_R√log n). Hence P-START holds, and SAMP Theorem C (C-v)'s rate clause
  applies with 1_𝒜δ̄ = O_P(max(r_n, r^{post}_n)) whenever P-CONC holds with a deterministic rate r^{post}_n. Only the
  start interface is supplied: P-CONC, P-MAP and SAMP's algorithm premises are not.
* **Proposition OVL⁺ (start mass under a bounded leakage set).** Setting F, (E), (GF-16), **visibility: (V-c), or
  (V-m) with this Q**; Q = Q_n ⊇ S₀ deterministic with |Q| ≤ K, |Q ∖ S₀| ≤ q̄ fixed, and (AL) for Q; and deterministic
  levels a_{n,l} with 0 ≤ a_{n,l} ≤ ā < ∞ for a fixed ā, uniformly in n and l ∈ Q_n ∖ S₀, such that
  δ²_{U,l} ≤ a_{n,l}·τ²_U·log n for every l ∈ Q ∖ S₀ and every U ⊆ [p] ∖ {l}, |U| ≤ 15. Then for every ε > 0:
  **P(π₀(S₀) ≥ n^{−E_n−ε}) → 1, E_n := Σ_{l∈Q∖S₀}[(a_{n,l} − 1)/2 − log p/log n]₊.**
  Hence P-OVL in SAMP Theorem D's production form (max(n, p)·log₂(n + 1)·π₀(S₀) → ∞) holds whenever
  limsup(E_n − max(1, log p/log n)) < 0 — also when the start mode is not S₀.
  (Version 1.3.4 has (V-c) only. The proof uses the exact identity 1/π₀(S₀) = [Σ_{T∈𝓛(Q)}γ₀(T)/γ₀(S₀)]/π₀(𝓛(Q)) and
  (T1⁺)(a); the truth-deletion functional e_n is not used.)

## 4. Not claimed (changes to BASE `STATEMENT.md:373-384`)

* Removed from that list: "Proposition OVL under (V-m)" (now claimed); "leakage sets beyond polylogarithmic size in
  (T3)(b)" (now: any |Q| ≤ K).
* Added: an informative bound in (T3⁺)(b) for leakage sets with (|Q| + 1)·n^{−1/2}·exp(C_R√log n) not tending to 0; a
  reference set H_l beyond polylogarithmic size; a partition-free limit with fewer than 17 − s₀ leaking nulls when
  s₀ ≤ 15; a sharper leading functional when s₀ = 0; a fixed constant in place of the ε-dependent constant C of
  (T1⁺)(d) (the leading term of the odds is tight but has no first moment).
* Everything else on that list stays not claimed (in particular: a Gaussian-row bridge to (V-m); necessity of
  (GF-16); sharpness of exp(C_R√log n); growing s₀; non-Gaussian noise; response-selected targets).

## 5. Dependencies and supersession

**Consumed (ticket W3-START, branch `theory/W3-START`; status as given in `BRIEF.md:3-4`: "council-passed, acceptance
pending only on INFRA R05"; council record R2, BASE `CHECKPOINT_3.md:241`).** W3-START:AGG, W3-START:FLOOR,
W3-START:TK, W3-START:LEAK, W3-START:VIS-c, W3-START:VIS-m, W3-START:NEC-b — by statement; and the proof files BASE
`lemmas/L1`–`L10`, whose unchanged steps are cited by line in `lemmas/P1`–`P4`. These claims are not yet rows of the
registry on `main`; the claims of this file can be accepted only after W3-START is (PROTOCOL rule 11; HQ's step).
No other registry claim is consumed (as in BASE `STATEMENT.md:386-396`).
**Consumers.** W3-SAMP:C@1.1.1 "PROVED-CHECKED", W3-SAMP:D@2.1.1 "PROVED-CHECKED" (premises P-START, P-OVL), as before.

**Supersession by implication** (LIFECYCLE §5: each new claim implies the one it replaces; ids W3-START2:⟨name⟩):

| new claim | implies | why |
|---|---|---|
| START-F (T1⁺) | W3-START:START-F | 𝔏^♯_n(h) ≤ 𝔏⁰_n(h); (a), (c) identical |
| F2 (F2⁺) | W3-START:F2 | same conclusion, one hypothesis fewer |
| TRANSFER (T3⁺)(a) | W3-START:TRANSFER | a bound r̄_n for the 1.3.4 rate is a bound for the 1.4 rate |
| IF-START (IF-START⁺) | W3-START:IF-START | the new rate r_n is at most the old one |
| OVL (OVL⁺) | W3-START:OVL | (V-c) is one of the two admitted visibility conditions |
| NEC (T4⁺) | W3-START:NEC | (N2⁺) = (N2) for s₀ ≥ 16; the premise of (N2) is empty for s₀ ≤ 15; (N1), (N3), (N4) identical |
| BR (B-R⁺) | W3-START:BR | (L-R) implies (L-R⁺) |
| START-R (T3⁺)(b) | W3-START:START-R | (L-R) implies (L-R⁺); same conclusions |

Lemma LEAK-0 is new and supersedes nothing (W3-START:LEAK stays as it is and is still used for U_Q).
