# W3-START2-R — STATEMENT v1.5 (rider on the start-mass statement: pointwise visibility, Gaussian-row rate)

Ticket W3-START2-R (Tier B rider), Theory Wave 3. Lead: Claude Opus 5.5 (effort high).
Status of this file: **v1.5** (2026-11-15; locked after review SL1 with the changes of `reviews/SL1_disposition.md`;
record in `LOG.md`). Protocol: `Theory_work/Wave3/PROTOCOL_v4.md`.
All results are asymptotic (n → ∞) unless marked *deterministic*.

**This is a delta statement.** PARENT := `Theory_work/Wave3/W3-START2/` (ticket W3-START2, STATEMENT v1.4.1, itself a
delta over BASE := `Theory_work/Wave3/W3-START/`, STATEMENT v1.3.4). "Version 1.4" means PARENT `STATEMENT.md` read
with BASE `STATEMENT.md` as it directs. **Version 1.5 of the start-mass statement** is version 1.4 with the definitions
(D3)–(D5) of §2 added, and the claims of §3 in place of the claims they supersede (§5). This file states in full every
definition, hypothesis and claim of version 1.5 that differs from version 1.4 and takes everything else by line
reference. Claims of version 1.4 not listed in §3 are unchanged, keep their version-1.4 hypotheses, and are used by id.
**This file fixes target statements only and asserts no proof status.** Proofs belong in `lemmas/R1`–`R5` (`PLAN.md`
§2); whether a proof is written or checked is recorded outside this file. **No method change is requested.**

## 0. What changes, in one table

| change | claims of v1.5 (this file) | supersedes | what is gained |
|---|---|---|---|
| T8 | (D3); VIS-c⁺⁺, VIS-m⁺⁺, (T1⁺⁺) START-F; F1⁺⁺–F3⁺⁺; OVL⁺⁺ | BASE `:140-151` (visibility), `:235-236`; PARENT `:93-117`, `:181-189`; BASE `:268-277` | visibility asked at the level **log n + 2 log p** of the actual p, not (1 + 2A) log n of the envelope p ≤ n^A; the margin form keeps the negative prior price of a net addition of nulls |
| T8 | (C2⁺⁺) NEC-b, (T4⁺⁺) NEC, F4⁺⁺ | BASE `:221-226`, `:278-287`; PARENT `:154-173` | necessity at the same level log n + 2 log p, so sufficiency and necessity meet at the constant 1 **for every sequence p_n**; drifting constants c_n with a window of width 1/√log n |
| T10 | (D4), (D5); (B-R⁺⁺); (T3⁺⁺)(b) START-R; IF-START⁺⁺ | PARENT `:63-73`, `:134-152`, `:176-180` | Gaussian rows, no leakage: **o₀ = O_P(√(log n/n))** when null and true columns are uncorrelated, in place of (log n)^{15κ_Q+1/2}/√n; reference sets H_l up to size exp(κ_H√log n) |
| T10 | (T3⁺⁺)(a) TRANSFER | PARENT `:119-133` | the transfer in conditional, self-normalised form (random rate), with the deterministic-envelope form as a corollary; \|S₀\| ≤ s̄ may vary with the design |
| restatements | MIS⁺⁺ (T6⁺⁺), EX⁺⁺ (T7⁺⁺) | BASE `:346-371` | under version 1.5; a Gaussian-row instance of (GR); examples at the new rate and with the new visibility |
| wording | §3.0 (Lemma LEAK-0, what it sharpens) | PARENT `:86-88` (remark only) | none: a remark of version 1.4 is stated correctly |

Each claim of §3 implies the claim it supersedes (§5). Nothing else of version 1.4 changes; in particular Theorem FLOOR
(T0), Lemma AGG (C0), Lemma ASM (C1), Lemma LEAK-0, the bridges (B1), (B-TK), (B-L), (D1), (D2) and the leading
functional 𝔏^♯_n are as they were. The hypotheses that change are exactly these: (V-c), (V-m) become (V-cp), (V-mp)
(both implied by the old ones, §2); (L-R⁺) becomes (L-R⁺⁺) (implied by it); the premises of (C2), (N2⁺), (N3), F4 are
restated at the level log n + 2 log p; (T3⁺⁺)(a) allows |S₀| ≤ s̄; (T3⁺⁺)(b)(iii) uses (L-gain-0).

## 1. Taken from version 1.4 unchanged

* Objects, code pins, Settings F and R, notation, quantities: BASE `STATEMENT.md:39-126`, with (D1) of PARENT
  `STATEMENT.md:52-61` (the sharp leading functional 𝔏^♯_n(h)) and LEAK-0 (PARENT `:82-89`).
* Assumptions (E), (GF-16), (AL) (BASE `:135-139`, `:152-157`); (FL-R16), (V-R) (BASE `:160-162`); (L-R⁺) (PARENT
  `:63-73`); EX-A, [A:BLOCK-LE-16] (BASE `:169-172`). Fixed constants as in BASE `:130-132`, with the additions of §2.
* Interface properties [TK], [VIS(κ; Q)], [LEAK(Q)], P-START, P-OVL (BASE `:174-191`); constants κ_E, 𝓔^blk, n₂ (PARENT
  `:46-48`).
* Claims used by id and not restated: (C0) AGG, (C1) ASM (BASE `:197-219`); (B1), (B-TK), (B-L) (BASE `:232-234`); (T0)
  FLOOR (BASE `:241-243`); Lemma LEAK-0 (PARENT `:82-89`). Where one of them refers to a claim restated in §3, the
  restated claim may be read in its place, because it implies the original (§5).
* Notation used below: **x_n = O_P(a_n)** for random a_n ≥ 0 means: for every ε > 0 there is C < ∞ with
  limsup_n P(x_n > C·a_n) ≤ ε. "x_n = O_P(a_n) + o_P(n^{−κ})" means x_n ≤ A_n + B_n with A_n = O_P(a_n) and n^κB_n → 0 in
  probability (PARENT `:77-78`, now also for random a_n).

## 2. Amended and new definitions and assumptions

**(D3) Visibility at the level of the actual p [A:START2R-V]** (replaces (V-c), (V-m) of BASE `:140-151`; one of):
* **(V-cp)** (constant level): for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15:
  **δ²_{U,j} ≥ τ²_U·(c_V·log n + 2 log p)**, with a fixed c_V > 1. Visibility exponent **κ_V := (c_V − 1)/2**.
* **(V-mp)** (margin form): there are fixed c_m > 0 and ε₀ > 0 such that for every V ⊆ S₀ with 1 ≤ |V| ≤ 16, every
  nonempty D ⊆ V, every R ⊆ Q ∖ S₀ and N ⊆ [p] ∖ Q with |V| + |R| + |N| ≤ 16, writing U := (V ∖ D) ∪ R ∪ N, T := V ∪ R,
  W := V ∪ R ∪ N, d := |D|, a := |N|:
  **(Λ_U − Λ_W)/τ²_U ≥ π_n(d, a; Q) + c_m·log n + (1 + ε₀)·(Λ_T − Λ_W)/τ²_W,**
  **π_n(d, a; Q) := (d − a)₊·(log n + 2 log p) − (a − d)₊·(log n + 2 log(p/c_Q)),** c_Q = |Q| + 15s₀ (BASE `:81`).
  Visibility exponent **κ_V := c_m/2**. For Q = S₀, R = ∅ and c_Q = 16s₀.
(π_n is, up to an additive constant, twice the log of the prior weight ω^Q(U) of BASE `:93` plus (d − a) log(n + 1):
the prior-plus-dimension price of the configuration U against T. For a > d it is negative: a net addition of nulls is
penalised by the prior, and (V-mp) asks correspondingly less. Version 1.4 replaced it by (1 + 2A)(d − a)₊ log n.)
*Relation to version 1.4.* (V-c) with c_V > 1 + 2A implies (V-cp) with c_V − 2A in place of c_V (2 log p ≤ 2A log n),
with the same κ_V. (V-m) with (c_m, ε₀) implies (V-mp) with the same (c_m, ε₀) for every n ≥ 256s₀² (then
π_n(d, a; Q) ≤ (1 + 2A)(d − a)₊ log n, because p/c_Q ≥ 1/(16s₀)). When log p/log n → A the constant-level thresholds of
(V-c) and (V-cp) agree at leading order; the margin form (V-mp) still asks less than (V-m) in that regime, because it
keeps the negative price −(a − d)(log n + 2 log(p/c_Q)) of a net addition of nulls (a > d), which (V-m) replaces by 0.
When p is smaller than the envelope, or log p/log n oscillates, both forms of (D3) ask less.

**(D4) (L-R⁺⁺) [A:START2R-R-L]** (Gaussian rows; replaces (L-R⁺) of PARENT `:63-73`). Fixed constants C_L ≥ 0 and
κ_H > 0. There are a deterministic Q = Q_n ⊇ S₀ with |Q| ≤ K, a deterministic sequence H̄_n with
**log H̄_n ≤ κ_H·√log n** for all large n, and, for every l ∉ Q, a deterministic H_l ⊇ {l} ∪ S₀ with **|H_l| ≤ H̄_n**,
such that for every U ⊆ [p] ∖ {l} with |U| ≤ 15, writing U₀ := U ∩ H_l:
* (L-gain-R) |Cov(W_l, W_j | W_{U₀})| ≤ C_L·n^{−1/2} for j ∈ S₀ ∖ U₀;
* (L-loc-R) |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n for v ∈ U ∖ H_l, j ∈ S₀ ∖ U₀, with a
  deterministic r_n, r_n·(n log n)^{1/4} → 0.
Put **N̄_n := (1 + H̄_n)^{15}** (a bound on the number of sets U₀ ⊆ H_l with |U₀| ≤ 15). "No leakage" is Q = S₀.
(The displayed conditions are those of (L-R⁺), word for word; the only change is |H_l| ≤ H̄_n in place of
|H_l| ≤ (log n)^{κ_Q}. (L-R⁺) implies (L-R⁺⁺) with H̄_n := (log n)^{κ_Q} and any κ_H > 0, since
κ_Q log log n ≤ κ_H√log n for all large n.)

**(D5) (L-gain-0) [A:START2R-R-L0]** (Gaussian rows; no leakage given proper subsets of the truth). A fixed C₀ ≥ 0 with
  **|Cov(W_l, W_j | W_U)| ≤ C₀·(n log n)^{−1/2} for every l ∉ S₀, every U ⊊ S₀ with |U| ≤ 15 and every j ∈ S₀ ∖ U.**
With C₀ = 0 this says exactly that **every null column is uncorrelated with every true column**, Cov(W_l, W_j) = 0 for
l ∉ S₀, j ∈ S₀ (take U = ∅ for one direction; for the other, Cov(W_l, W_j | W_U) = Σ_{lj} − Σ_{lU}Σ_{UU}⁻¹Σ_{Uj} = 0 when
U ⊆ S₀). (L-R⁺⁺) with Q = S₀ and C_L = 0 implies (L-gain-0) with C₀ = 0 (for U ⊊ S₀ ⊆ H_l, U₀ = U).

## 3. Claims of version 1.5

Setting, notation and assumptions as in §1–§2. Claim ids are W3-START2-R:⟨name⟩ (name in brackets).

### 3.0 A remark of version 1.4, stated correctly (no claim changes)
Lemma LEAK-0 (PARENT `:82-89`) bounds T₁ by n^{−1/2}𝔏^♯_n(h). It sharpens the **partition-free** leading functional of
version 1.3.4: 𝔏^♯_n(h) ≤ 𝔏⁰_n(h) (PARENT `:57-58`). It does not sharpen the block-relative bound of [LEAK(S₀)]
(BASE `:183`): 𝔏^♯_n(h) (a maximum over all proper subsets U ⊊ S₀) and 𝔏^{b,0}_n(h) (one set U*_{b(l)} ⊆ S₀ per
column, U*_{b(l)} = S₀ allowed) are not comparable in general. The sentence "This sharpens the T₁ clause of [LEAK(S₀)]"
of PARENT `:86-87` is to be read in this sense.

### 3.1 Fixed design (T8)

**[VIS-c] (B-V1⁺⁺).** Setting F, a deterministic Q ⊇ S₀ with |Q| ≤ K. (V-cp), [TK] (in the quantitative form of BASE
`:187-191`), [LEAK(Q)], (AL) ⇒ P(e_n > n^{−κ}) → 0 and [VIS(κ; Q)], for every κ < κ_V = (c_V − 1)/2 (as (B-V1), BASE
`:235`, with (V-cp) for (V-c)). *Refinement under (E), (GF-16)* (which deliver that form of [TK]): for every κ ∈ (0, κ_V)
there is n₄ depending only on κ and the fixed constants (A, M, σ², g_*, s₀, c_V) such that for n ≥ n₄, on the event
𝓔^blk ∩ 𝓧 of BASE `lemmas/L4_VIS.md:12` (probability ≥ 1 − P((𝓔^blk)ᶜ) − 1/log n): e_n ≤ 2^{−16}n^{−κ}, and on
𝓔^blk ∩ 𝓧 ∩ {c_QU_Q ≤ 1}: Ξ(Q) ≤ n^{−κ}.

**[VIS-m] (B-V2⁺⁺).** Setting F, a deterministic Q ⊇ S₀ with |Q| ≤ K. (V-mp) with this Q, [TK] (quantitative form) ⇒
[VIS(κ; Q)] for every κ < κ_V = c_m/2 (as (B-V2), BASE `:236`, with (V-mp) for (V-m)). *Refinement under (E), (GF-16):*
for every κ ∈ (0, κ_V) there is n₃ depending only on κ and the fixed constants (A, M, σ², g_*, s₀, c_m, ε₀) such that
for n ≥ n₃, on 𝓔^blk ∩ 𝓧: Ξ(Q) ≤ n^{−κ}.

**[START-F] (T1⁺⁺) Theorem START-F (fixed design).** Setting F, the start as coded. Assume (E), (GF-16), visibility
**(V-cp) or (V-mp)** (with this Q), and (AL) for a deterministic Q ⊇ S₀ with |Q| ≤ K, with level vector h (default:
h_l = z_n for l ∉ Q). Let κ_V be the exponent of (D3). Then, for every κ ∈ (0, κ_V):
* (a) **lattice form.** 1 − π₀(𝓛(Q)) = O_P(ϱ_n(Q; h)) + o_P(n^{−κ}).
* (b) **no leakage, Q = S₀.** o₀ = O_P(n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)²) + o_P(n^{−κ}); in particular π₀(S₀) → 1
  in probability.
* (c) **first-order form** (Q = S₀). If moreover κ_V > ½ and n^{−1/2}𝔏_n(S₀; h)² → 0, then o₀/T₁ → 1 in probability.
* (d) **uniformity.** For every ε > 0 and κ ∈ (0, κ_V) there are C < ∞, c₀ > 0 and n₀ depending only on (ε, κ) and the
  fixed constants (A, M, σ², g_*, s₀ and c_V or (c_m, ε₀)) such that for n ≥ n₀ and every (X, θ*, Q, h) — a fixed design
  with p ≤ n^A retained columns, |supp θ*| = s₀ < p, S₀ ⊆ Q, |Q| ≤ K, h a level vector for Q — satisfying at n the
  inequalities ‖μ‖² ≤ Mn, (GF-16), (V-cp) or (V-mp), and ϱ_n(Q; h) ≤ c₀:
  P(1 − π₀(𝓛(Q)) > C·ϱ_n(Q; h) + n^{−κ}) ≤ ε + b_n(h), and, for Q = S₀,
  P(o₀ > C·[n^{−1/2}·𝔏^♯_n(h) + n^{−1}·𝔏_n(S₀; h)²] + n^{−κ}) ≤ ε + b_n(h).
(This is (T1⁺) of PARENT `:93-110` with (D3) in place of (V-c), (V-m), word for word otherwise. Proof structure: as
for (T1⁺), with VIS-c⁺⁺ / VIS-m⁺⁺ in place of (B-V1) / (B-V2).)

**[F1], [F2], [F3] (Corollaries F1⁺⁺, F2⁺⁺, F3⁺⁺).** F1 (BASE `:268-271`), F2⁺ (PARENT `:112-117`) and F3 (BASE
`:276-277`), word for word, with "visibility with exponent κ_V" (BASE `:266`; PARENT `:112`) meaning (V-cp) or (V-mp)
with the exponent κ_V of (D3), and with (T1⁺⁺) in place of (T1), (T1⁺). (In F1 the constant A of κ_L(η, A) and η_A is
still the exponent of p ≤ n^A.)

**[F4] (Corollary F4⁺⁺; isolated leaking columns, non-default levels).** Setting F, (E), (GF-16), (V-cp) or (V-mp), a
deterministic Q ⊇ S₀ with |Q| ≤ K. Let I_n ⊆ [p] ∖ Q be deterministic with |I_n| ≤ ī (fixed), and let c_n ≤ 1 be numbers
with **δ²_{U,l} ≤ τ²_U·(c_n·log n + 2 log p)** for every l ∈ I_n and every U ⊆ [p] ∖ {l}, |U| ≤ 15. Put
h_l := min(z_n, √(4 log log n)) for l ∈ I_n and h_l := z_n otherwise. Then b_n(h) → 0, and for n ≥ n_F (depending only
on A):
  **ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)·ī·n^{−(1−c_n)/2}·exp(C_A·√(log n·log log n)),   C_A := 2√(1 + 2A) + 1,**
where ϱ^{−I}_n(Q) is ϱ_n(Q) with the columns of I_n left out of the sum. Hence (AL) holds, and (T1⁺⁺) applies with this
h, whenever ϱ^{−I}_n(Q) → 0 and the second term tends to zero — for a fixed c < 1 (c_n ≡ c): whenever ϱ^{−I}_n(Q) → 0
and (|Q| + 1)n^{−κ₁} → 0 for some κ₁ < (1 − c)/2. (By (C2⁺⁺)(i) a column whose gain given the truths of its block is
above τ²(c·log n + 2 log p) with c > 1 destroys the start mass: the two thresholds meet at c = 1 for every sequence p_n.)

**[NEC-b] (C2⁺⁺) Lemma NEC-b (component diagnostics; Setting F, (E), [TK] in the quantitative form of BASE `:187-191`,
which (E) and (GF-16) deliver).** On the actual partition:
* (i) Suppose that for all large n some null l = l_n has **δ²_{U,l} ≥ τ²_U·(c_n·log n + 2 log p)** at U = U*_{b(l)}.
  If c_n ≡ c > 1 is fixed: P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1)/2. If (c_n − 1)·√log n → ∞: π₀(S₀) → 0 in
  probability.
* (ii) Suppose that for all large n some truth j = j_n has **δ²_{U,j} ≤ τ²_U·(c_n·log n + 2 log p)** at
  U = U*_{b(j)} ∖ {j}. If c_n ≡ c < 1 is fixed: P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 − c)/2. If
  (1 − c_n)·√log n → ∞: π₀(S₀) → 0 in probability.

**[NEC] (T4⁺⁺) Proposition NEC (limits; Setting F, (E), (GF-16)).**
* (N1) = (T0): the exponent ½ in (T1⁺⁺)–(T3⁺⁺) is optimal; under F2⁺⁺ with η′ = 0 and κ_V > ½ the order is exact.
* (N2⁺⁺) **leaking nulls.** Let s₀ ≥ 1 and r(s₀) := max(1, 17 − s₀). Suppose that for all large n there is a deterministic
  set I_n ⊆ [p] ∖ S₀ of r(s₀) distinct null columns with **δ²_{V,l} ≥ τ²_V·(c_n·log n + 2 log p)** for every l ∈ I_n and
  every proper subset V ⊊ S₀ with |V| ≤ 15. If c_n ≡ c > 1: P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1)/2. If
  (c_n − 1)√log n → ∞: π₀(S₀) → 0 in probability. (Scope as PARENT `:160-166`, with this premise.)
* (N3⁺⁺) **one weakly visible truth.** Suppose that for all large n some truth j = j_n has
  **δ²_{V,j} ≤ τ²_V·(c_n·log n + 2 log p)** for every V ⊆ S₀ ∖ {j} with |V| ≤ 15. If c_n ≡ c < 1: P(π₀(S₀) ≤ n^{−κ′}) → 1
  for every κ′ < (1 − c)/2. If (1 − c_n)√log n → ∞: π₀(S₀) → 0 in probability. So the constant 1 in front of log n in
  (V-cp), and in (V-mp) for the instances D = {j}, N = ∅, cannot be lowered, for every sequence p_n ≤ n^A.
* (N4) As PARENT `:169-170`.
((N2⁺⁺) and (N3⁺⁺) follow from (C2⁺⁺) as (N2⁺), (N3) follow from (C2) (PARENT `:172-173`; P3 pigeonhole for (N2⁺⁺)).)

**[TRANSFER] (T3⁺⁺)(a) Theorem START-R, transfer (any design law; design-measurable targets).** Let X^r be a random raw
design and let α, β, Q and a level vector h be measurable functions of X^r; conditionally on X^r,
y^r = α(X^r)1 + X^rβ(X^r) + ε with ε | X^r ~ N_n(0, σ²I), σ² > 0 fixed; θ* := D_xβ(X^r), S₀ := supp β(X^r) (after dropping
constant columns). Fix constants (A, M, g_*, s̄ and c_V or (c_m, ε₀)). A realisation x of X^r is **admissible at n** if,
with its own (θ*, S₀, Q, h): p ≤ n^A retained columns, |S₀| ≤ s̄, |S₀| < p, S₀ ⊆ Q, |Q| ≤ K, h a level vector for Q,
‖μ‖² ≤ Mn, (GF-16), and (V-cp) or (V-mp) at n. Write ϱ_n := ϱ_n(Q; h), evaluated at the realised design, and
**R^♯_n := n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)²** on {Q = S₀}, R^♯_n := 0 on {Q ≠ S₀} (on {Q = S₀} the level vector h is
indexed by every l ∉ S₀, as these functionals require); both are random variables.
* (a1) **conditional form.** For every ε ∈ (0, 1) and κ ∈ (0, κ_V) there are C < ∞, c₀ > 0 and n₀, depending only on
  (ε, κ) and the fixed constants, such that for every n ≥ n₀, almost surely:
  on {X^r admissible, ϱ_n ≤ c₀}: **P(1 − π₀(𝓛(Q)) > C·ϱ_n + n^{−κ} | X^r) ≤ ε + b_n(h)**;
  on {X^r admissible, Q = S₀, ϱ_n ≤ c₀}: **P(o₀ > C·R^♯_n + n^{−κ} | X^r) ≤ ε + b_n(h)**.
* (a2) **random-rate form.** If P(X^r admissible at n) → 1, b_n(h) → 0 in probability and ϱ_n → 0 in probability, then
  for every κ ∈ (0, κ_V): 1 − π₀(𝓛(Q)) = O_P(ϱ_n) + o_P(n^{−κ}); if moreover P(Q = S₀) → 1, then
  **o₀ = O_P(R^♯_n) + o_P(n^{−κ})**.
* (a3) **deterministic envelopes.** If in (a2) moreover ϱ_n = O_P(ϱ̄_n) for a deterministic ϱ̄_n → 0, then
  1 − π₀(𝓛(Q)) = O_P(ϱ̄_n) + o_P(n^{−κ}); if R^♯_n = O_P(r̄_n) for a deterministic r̄_n and P(Q = S₀) → 1, then
  o₀ = O_P(r̄_n) + o_P(n^{−κ}). In particular (T3⁺)(a) of PARENT `:120-133` holds with (D3) in place of the visibility
  condition and |S₀| ≤ s̄ in place of |S₀| = s₀.
Supports, coefficients, sets Q or level vectors selected using the response are not covered. *Convention off the
admissible designs:* as BASE `:301-305` (also in (b)); in addition ϱ_n, R^♯_n and b_n(h) are set to 0 on realisations where their defining expressions are not available (no retained column, or h not a level vector for Q). With this they are measurable functions of X^r on the whole design space (`lemmas/R4_TRANSFER_COR.md`, Measurability), and no clause changes on admissible designs.

**[MIS] (T6⁺⁺) Corollary MIS.** BASE (T6) (`:346-357`) with the claims of version 1.5 in place of those of version
1.3.4: under (GR), each claim of version 1.5 holds for the start π₀^𝒞 of the method re-run on the candidate data
provided all of that claim's hypotheses hold after the substitution (p, β, σ², S₀) := (p_𝒞, β^𝒞, σ_𝒞², S₀^𝒞) of BASE
`:349-350`; random candidate designs through (T3⁺⁺)(a). **Gaussian-row instance.** If the raw rows of
(X^r_𝒞, X^r_𝓜) are iid N(m, Σ) with Σ_{𝒞𝒞} nonsingular, ε ~ N_n(0, σ²I) is independent of X^r, and
τ² := β_𝓜ᵀ(Σ_{𝓜𝓜} − Σ_{𝓜𝒞}Σ_{𝒞𝒞}⁻¹Σ_{𝒞𝓜})β_𝓜 does not depend on n, then (GR) holds in its conditional form with the
deterministic a := m_𝓜ᵀβ_𝓜 − m_𝒞ᵀγ and γ := Σ_{𝒞𝒞}⁻¹Σ_{𝒞𝓜}β_𝓜; so the random-candidate clause applies with no premise on
the omitted block beyond this, the candidate targets β^𝒞 = β_𝒞 + γ and S₀^𝒞 = supp β^𝒞 being deterministic. (The
substituted hypotheses still include |S₀^𝒞| ≤ s̄; γ is dense in general.)

**[EX] (T7⁺⁺) Examples table.** BASE (T7) (`:359-371`) and BASE `lemmas/L11_EXAMPLES.md`, with these changes:
* F-1 (orthogonal) and F-3 (near-duplicate nulls): exact order n^{−1/2} for s₀ ≥ 1 by F2⁺⁺, with no growth condition on
  p (p > s₀ suffices).
* F-2 (one truth, fifteen nulls correlated with it at ρ² = 0.4, θ*₁² = 2(1 + 2A)σ² log n/(n − 1), p = min(⌊n^A⌋, n − 1),
  A ∈ [0.1, 1]): (V-mp) holds with Q = S₀, every c_m < 1 + 2A and any ε₀ > 0 (version 1.3.4: c_m = (1 + 2A)/6); with the
  F4⁺⁺ levels (T1⁺⁺)(a), (b), (d) apply and **o₀ = O_P(n^{−(1+2A)/10+η})** for every η > 0; for A ∈ (3/4, 1],
  (T1⁺⁺)(c) applies: o₀/T₁ → 1 in probability.
* G-1 (Gaussian rows, Σ_n = I_p, p ≫ n allowed): (L-R⁺⁺) with Q = S₀, H_l = {l} ∪ S₀, C_L = 0, r_n = 0, and (L-gain-0)
  with C₀ = 0; by (T3⁺⁺)(b)(iii): **o₀ = O_P(√(log n/n))**.
* G-2 (block-diagonal Σ_n, groups of size ≤ ḡ, at most one truth per group, Q := the truths' groups): (L-R⁺⁺) with
  C_L = 0 and bounded H̄_n = (s₀ + 1)ḡ; by (T3⁺⁺)(b)(ii): **1 − π₀(𝓛(Q)) = O_P(√(log n/n))**.
Everything else as in BASE (T7).

**[OVL] (OVL⁺⁺) Proposition OVL.** OVL⁺ of PARENT `:181-189`, word for word, with "visibility: (V-cp), or (V-mp) with
this Q" in place of "visibility: (V-c), or (V-m) with this Q", and (T1⁺⁺)(a) in place of (T1⁺)(a).

### 3.2 Gaussian rows (T10)

**[BR] (B-R⁺⁺) Bridge (Gaussian rows).** Setting R with p > s₀ for all large n.
* (i) Under (FL-R16), (V-R), (L-R⁺⁺): with probability → 1 the design satisfies (E) (energy bound with M = s₀²θ_hi²;
  p ≤ n^A, s₀ fixed and p > s₀ are assumed), λ_min(R̂_T) ≥ φ₀² for 1 ≤ |T| ≤ 16 with a constant φ₀ > 0 (hence (GF-16)),
  (V-c) of BASE `:141` for every fixed c_V (hence (V-cp) for every fixed c_V), and **𝔏_n(Q) ≤ exp(C_B·√log n)**, default
  levels, with a constant C_B depending only on the fixed constants and κ_H.
* (ii) If moreover C_L = 0: **𝔏_n(Q) = O_P(N̄_n·√log n)** (tightness; N̄_n of (D4)).
* (iii) Under (FL-R16) and (L-gain-0) alone (no (V-R), no (L-R⁺⁺)): **𝔏^♯_n = O_P(√log n)** (tightness), default levels.
(With H̄_n = (log n)^{κ_Q}, (i)–(ii) are (B-R⁺) of PARENT `:147-152`: N̄_n ≤ 2^{15}(log n)^{15κ_Q}.)

**[START-R] (T3⁺⁺)(b) Theorem START-R, Gaussian rows.** Setting R with p > s₀ for all large n (nothing is claimed when
p = s₀). Assume (FL-R16), (V-R) and (L-R⁺⁺). Then:
* (i) there is C_R < ∞, depending only on the fixed constants and κ_H, with
  **P(1 − π₀(𝓛(Q)) ≤ (|Q| + 1)·n^{−1/2}·exp(C_R√log n)) → 1.**
  In particular with Q = S₀: P(π₀(S₀) ≥ 1 − n^{−c}) → 1 for every c < ½, for p ≤ n^A including p ≫ n; and if
  |Q| ≤ n^{1/2−ε_Q} for a fixed ε_Q ∈ (0, ½): P(π₀(𝓛(Q)) ≥ 1 − n^{−c}) → 1 for every c < ε_Q.
* (ii) If C_L = 0: **1 − π₀(𝓛(Q)) = O_P((|Q| + 1)·N̄_n·√(log n/n)).** (With H̄_n = (log n)^{κ_Q} this is the clause
  C_L = 0 of PARENT `:138-139`; with bounded H̄_n it is O_P((|Q| + 1)√(log n/n)).)
* (iii) **No leakage, uncorrelated nulls.** If Q = S₀ and (L-gain-0) holds (for instance C_L = 0 in (L-R⁺⁺) with
  Q = S₀): **o₀ = O_P(√(log n/n))**, hence 1 − π₀(S₀) = O_P(√(log n/n)).
(At each n where the right side of (i) is ≥ 1 its event is sure; the O_P statements need no rate tending to zero — as
PARENT `:140-144`. By (T0), o₀ ≥ ½(n + 1)^{−1/2} on every data set with s₀ < K and n ≥ 4, so (iii) is optimal up to the factor √log n.)
Proof structure: (B-R⁺⁺), then (T1⁺⁺)(d) conditionally on the design, as in (a); for (iii) the second display of
(T1⁺⁺)(d) with (B-R⁺⁺)(iii) for the leading term and (B-R⁺⁺)(i) for 𝔏_n(S₀).

**[IF-START] (T5⁺⁺) IF-START⁺⁺.** Under (T1⁺⁺) with (AL) at Q = S₀ and level vector h: for every event 𝒜 and every κ
with 0 < κ < κ_V, 1_𝒜o₀ = O_P(r_n) with r_n := n^{−1/2}𝔏^♯_n(h) + n^{−1}𝔏_n(S₀; h)² + n^{−κ} → 0; under (T3⁺⁺)(b) with
Q = S₀ the same with **r_n := n^{−1/2}exp(C_R√log n)**, and under (T3⁺⁺)(b)(iii) with **r_n := √(log n/n)**. Hence
P-START holds, and SAMP Theorem C (C-v)'s rate clause applies with 1_𝒜δ̄ = O_P(max(r_n, r^{post}_n)) whenever P-CONC
holds with a deterministic rate r^{post}_n. Only the start interface is supplied (as PARENT `:179-180`).

## 4. Not claimed (changes to PARENT `:191-201`)
* Removed from that list: "a reference set H_l beyond polylogarithmic size" (now up to exp(κ_H√log n) under (L-R⁺⁺)
  in (B-R⁺⁺) and (T3⁺⁺)(b); the stand-alone leading-functional bridge (B-R⁺⁺)(iii) needs no reference-set hypothesis).
* Added: a Gaussian-row lattice rate free of N̄_n for Q ⊋ S₀; a Gaussian-row bound o₀ = O_P(√(log n/n)) when
  (L-gain-0) fails; a lower bound of order √(log p/n) (BASE `:380` stays not claimed); drifting constants on the
  sufficiency side of (D3); (T3⁺⁺)(b) for a candidate run with deterministic **raw** coefficients (Setting R has θ*
  deterministic on the standardised scale); MIS for a general deterministic μ ∉ span X_𝒞 without (GR) (named open
  item W3-START2R-O1); the optional items T9 (F1 with the exact Laplace exponent, F3 with G_n = o(log n), F4 at n^ι
  columns) and T11 (factorised OVL⁺, many leakers) unless adopted at CP1.
* Everything else on that list stays not claimed.

## 5. Dependencies and supersession

**Consumed** (statement and proof lines; statuses as in the registry at CP1, to be quoted verbatim in REPORT):
W3-START2:START-F, :F2, :TRANSFER, :BR, :START-R, :IF-START, :OVL, :NEC, :LEAK-0 (PARENT v1.4.1, recorded on main);
W3-START:AGG, :FLOOR, :TK, :LEAK, :VIS-c, :VIS-m, :NEC-b, :F1, :F3, :F4, :MIS, :EX (BASE v1.3.4, recorded); their proof
files PARENT `lemmas/P1`–`P4`, BASE `lemmas/L1`–`L11`, cited by line in `lemmas/R1`–`R5`. **Consumers:** as PARENT
`:211` (W3-SAMP:C, W3-SAMP:D: premises P-START, P-OVL).

**Supersession by implication** (ids W3-START2-R:⟨name⟩; supersession of headline rows goes through HQ and the HQ
consultant, PROTOCOL_v4 H5):

| new claim | implies | why |
|---|---|---|
| START-F (T1⁺⁺) | W3-START2:START-F | (V-c) ⇒ (V-cp) with c_V − 2A, same κ_V; (V-m) ⇒ (V-mp), same (c_m, ε₀), n ≥ 256s₀²; conclusions identical |
| VIS-c (B-V1⁺⁺) | W3-START:VIS-c | same implication of hypotheses; same conclusion |
| VIS-m (B-V2⁺⁺) | W3-START:VIS-m | same |
| F1 (F1⁺⁺) | W3-START:F1 | visibility weaker; conclusions identical |
| F2 (F2⁺⁺) | W3-START2:F2 | same |
| F3 (F3⁺⁺) | W3-START:F3 | same |
| F4 (F4⁺⁺) | W3-START:F4 | c′ < 1 + 2A̲ in the old premise gives the new one with c = c′ − 2A̲ + 2η < 1 for large n; the new bound gives the old one as η ↓ 0 |
| NEC-b (C2⁺⁺) | W3-START:NEC-b | old premises give the new ones with c ∓ 2(Ā or A̲) ± 2η; conclusions recovered as η ↓ 0 |
| NEC (T4⁺⁺) | W3-START2:NEC | same, clause by clause; (N1), (N4) identical |
| TRANSFER (T3⁺⁺)(a) | W3-START2:TRANSFER | (a3) |
| BR (B-R⁺⁺) | W3-START2:BR | (L-R⁺) ⇒ (L-R⁺⁺) with H̄_n = (log n)^{κ_Q}; N̄_n ≤ 2^{15}(log n)^{15κ_Q} |
| START-R (T3⁺⁺)(b) | W3-START2:START-R | same, with (ii) at H̄_n = (log n)^{κ_Q} |
| IF-START (T5⁺⁺) | W3-START2:IF-START | each rate is at most the old one |
| OVL (OVL⁺⁺) | W3-START2:OVL | visibility weaker |
| MIS (T6⁺⁺) | W3-START:MIS | each substituted claim implies its version-1.3.4 counterpart |
| EX (T7⁺⁺) | W3-START:EX | each row's conclusion contains the version-1.3.4 one |

## Changelog (PROTOCOL_v4 §4.2; rows after the lock)

| version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| 1.5-draft0 | all | — | draft for the statement lock | — | — |
| 1.5 | VIS-c, VIS-m, NEC-b: hypothesis [TK] (quantitative form) in place of (E), (GF-16); the explicit thresholds kept as refinements under (E), (GF-16) | STRONGER (hypothesis back to the parent's interface form) | supersession must not strengthen a parent hypothesis | `reviews/SL1_statement_lock_sol.md` #1 | `reviews/LC1_line_check_sol.md` (tag confirmed) |
| 1.5 | (D3) relation remark | EQUAL (wording) | the margin forms differ also when log p/log n → A | SL1 #2 | `reviews/LC1_line_check_sol.md` |
| 1.5 | (T3⁺⁺)(a): R^♯_n defined on {Q = S₀}, 0 elsewhere; (a3) states the O_P-envelope consequence | EQUAL (definition completed; consequence of (a2)) | R^♯_n undefined when Q ⊋ S₀; SL1 OPTIONAL adopted | SL1 #3, OPTIONAL | `reviews/LC1_line_check_sol.md` |
| 1.5 | §4 scope sentence; PLAN section reference | EQUAL (wording) | — | SL1 #4, #5 | `reviews/LC1_line_check_sol.md` |
