# W3-AUDIT — check of the [audit calc] lines (independent checker, Opus 5.5 high, 2026-11-16)

Scope: the six verdict-bearing rows of `TRACK_D.md:176-188` (the two track-D rows first), read against the working tree of
`/home/fb31/BVS-wt/W3-AUDIT` (W3-AUDIT files as of commit c63b0062 plus uncommitted edits; nothing pulled). No new proofs:
each check is the shortest argument that settles the line, with sources. Numeric checks: Python/NumPy, `nice -n 19`,
one core, scripts in the session scratchpad (not committed); their outputs are quoted.

Design facts used (1M plan, `/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md:80-97`,
untracked): σ* = 1, s₀ = 5, β*_{S₀} = a·(1.0, −0.8, 0.9, −0.7, 0.6), a ∈ {1, 0.6}; truths spread evenly (spacing ≈ p/5),
"shifted so that no two truths share a BLK block"; AR = Toeplitz 0.6^{|j−l|}; BLK = groups of 20 consecutive columns,
x_j = √.5 f_b + √.5 e_j (correlation 0.5 inside a group, 0 across); p = 10⁶, n ∈ {200, 400} at 1M, {100, …, 800} at 10⁴.

| # | Line | Verdict |
|---|---|---|
| 1 | TRACK_D §0: start mass on S₀ destroyed on AR and BLK (via NEC-b) | **CONFIRMED WITH CORRECTION** (asymptotic claim right; gain formula drops τ²_U; finite-n radius wrong) |
| 2 | TRACK_D core 4: P-OVL∞ fails on such designs; route TR cannot reach AR | **CONFIRMED WITH CORRECTION** (cite NEC-b's proof, not its statement, for "exponentially small"; TR's finite bound is vacuous too) |
| 3 | TRACK_B B5: λ_min(Σ) of the 13 designs | **CONFIRMED** (all 15 values exact, numerically and in closed form) |
| 4 | TRACK_B B7: Thm 9 (A3) ⇒ Song–Liang Condition 1 | **CONFIRMED WITH CORRECTION** (true; the qualifier "whenever r̄_n ≤ q_n" can be dropped; state "standardised predictors") |
| 5 | TRACK_B B8: visibility on S1–S4, S6, IND, AR, BLK, cs | **CONFIRMED** (exact for block designs and cs; AR via Markov structure; numeric worst-case search agrees) |
| 6 | TRACK_B B9: partial covariances under cs, fac2, s5 | **CONFIRMED WITH CORRECTION** (formula right; the "outside" verdict already follows at U = ∅, so no partial-covariance formula is needed) |
| — | TRACK_B B11: an AR neighbour or block-mate of a truth has fixed covariance | CONFIRMED (read off Σ: 0.5 / 0.6 / ≥ 0.4) |

Context: since this check started, HQ's order moved to #2 → #3 → #5′ with #1 deferred and #5 NO-GO, "only after the
checker confirms the [audit calc] lines" (`TRACK_D.md:164`, commit 3016d383). Items 1–2 support the NO-GO and the
deferral as **asymptotic** statements only; item 5 is what #5′'s design list (S2–S4, S6, AR, BLK, via Theorem 6) rests
on, and it holds; item 4 is the comparison #3 aims to remove. None of the six rows blocks those tickets.

---

## 1. Start mass on AR and BLK (TRACK_D.md:31-37; CHECKPOINT_2.md:3; TRACK_B.md:200-202)

**Verdict: CONFIRMED WITH CORRECTION.** As n → ∞ with ρ = 0.6 (AR) or the 20-column groups (BLK) fixed, P(π₀(S₀) ≤ n^{−κ})
→ 1 for **every** κ > 0, whatever partition the method builds. The scope verdict on candidate #1 ("not AR, not BLK") stands.
Three corrections: (a) the normalised gain carries τ²_U, which the audit line drops; (b) the "distance ≍ log n" argument
is more than is needed — a fixed radius of 8 does it, by pigeonhole; (c) the finite-n parenthetical (`TRACK_D.md:34-35`,
"radius only k_n = 1 to 3") is wrong: at the plan's sizes n = 200 and 400 **no** column at any distance meets NEC-b's
threshold, so NEC-b says nothing about π₀(S₀) at the sizes the 1M plan actually runs.

**The tool, as stated.** `W3-START:NEC-b@1.0.0`, registry "PROVED-CHECKED" (`INFRA/registry/claims.tsv:431`), statement
`W3-START/STATEMENT.md:221-226`, proof `W3-START/lemmas/L7_NEC.md:12-26`. Setting F with (E) and [TK] (quantitative form,
`STATEMENT.md:187-191`, delivered by (E) + (GF-16)). (C2)(i): if for all large n some null l has
δ²_{U,l} ≥ c·τ²_U·log n at **U = U*_{b(l)} = S₀ ∩ C_{b(l)}** (the truths of l's own block), c > 1 + 2Ā fixed, then
P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1 − 2Ā)/2. τ²_U := σ² + Λ_U/(n − 1) (`STATEMENT.md:76-78`). The proof uses
one Gaussian variable at an X-measurable witness and holds for every partition with blocks ≤ 16 that is a function of X
(`L7_NEC.md:46-48`, remarks (1), (3)).

**Hypotheses on the designs.**
- (E): ‖μ‖² ≤ Mn holds w.p. → 1 with M = 2θ*ᵀΣθ*; p ≤ n^A; s₀ = 5 fixed; p > s₀. ✓
- (GF-16): λ_min(Σ) = (1 − ρ)/(1 + ρ) = 0.25 for AR(0.6) and 0.5 for BLK (block-diagonal compound symmetry), so every
  principal 16 × 16 block has λ_min ≥ 0.25; the sample floor on all ≤ 16-sets w.p. → 1 is what `W3-START:BR`
  ("PROVED-CHECKED", `STATEMENT.md:237`) delivers from (FL-R16). ✓
- Random design. NEC-b is a Setting-F lemma; the audit applies it to Gaussian rows. The step is routine and I accept it:
  condition on X; on the X-event G_n where (E), (GF-16) hold with fixed constants and the gain premise holds, L7.1's
  failure probability is ≤ P((𝓔^blk)ᶜ | X) + 2/log n, uniformly over G_n (the quantitative [TK]; L7.1's "large n" depends
  only on n₁, s₀, c, Ā, κ_E, ω̄_n). So P(π₀(S₀) > n^{−κ′}) ≤ P(G_nᶜ) + o(1). **This conditioning step is not recorded
  anywhere**; a ticket that uses the conclusion should write it as one sentence.

**The gain premise (corrected calculation).** Take the truth j with |θ*_j| = a (the largest). Population, with
U ⊆ S₀ ∖ {j} (truths of other blocks):
  δ²_{U,l}/(n − 1) → γ²_{U,l} := Cov(W_l, Σ_k θ*_k W_k | W_U)² / Var(W_l | W_U),
  τ²_U → σ² + Var(Σ_k θ*_k W_k | W_U) ≤ σ² + Σ_k θ*_k² (+ O(ρ^{p/5})) = 1 + 3.3a² (4.30 strong, 2.19 weak).
- AR, null at distance k from j, far from the other truths: γ² = a²ρ^{2k}(1 + o(1)) (Markov structure; the other truths
  are ≈ p/5 away, so their terms and the effect of conditioning on them are O(ρ^{p/5})). Normalised sample gain
  δ²/τ² ≈ (n − 1)a²ρ^{2k}/τ²_U. **The audit's "nρ^{2k}θ_j² exceeds (1 + 2A) log n" omits the division by τ²_U** (it uses
  τ² = σ² = 1, i.e. as if U already explained all the signal). The order of k_n (≍ log n/(2 log(1/ρ))) is unchanged.
- BLK, null l in j's group: Cov(W_l, W_j | W_U) = 0.5 for every U of truths from other groups (independent), Var = 1, so
  γ² = 0.25a², δ²/τ² ≈ 0.25(n − 1)a²/τ²_U.
Both are ≍ n for every fixed k, hence exceed c·log n for **every** fixed c once n is large: the premise of (C2)(i) holds
with c arbitrarily large, so π₀(S₀) = o_P(n^{−κ}) for every κ. The sample/population passage is a law of large numbers on a
fixed-dimensional sub-design (the window of j, l, and the ≤ 4 other truths), so there is no uniformity issue.

**Existence of a witness on the actual partition (pigeonhole; partition-free).**
- AR: the 17 columns j − 8, …, j + 8 contain j and 16 nulls (the other truths are ≈ p/5 away). b(j) holds at most 15 of
  those nulls, so some null l at distance k ≤ 8 has b(l) ≠ b(j); then U*_{b(l)} ⊆ S₀ ∖ {j} and γ²_{U,l} ≥ a²ρ^{16}(1 − o(1))
  > 0. No log n radius is needed; the audit's argument (columns out to distance k_n → ∞ cannot all sit in a block of 16)
  is correct but uses only that k_n ≥ 8 eventually.
- BLK: j's group has 20 columns, b(j) ≤ 16, so ≥ 4 group-mates of j lie outside b(j). They are nulls (one truth per group,
  plan `:92`), and U*_{b(l)} contains no truth of j's group, so γ² = 0.25a². ✓
- Sign cancellation: not an issue on these designs (one truth per group in BLK; truths ≈ p/5 apart in AR). On the ADJ arm
  (two adjacent truths, plan `:101`) or a BLK variant with two truths per group of opposite signs the population covariance
  can cancel for particular l; the claim as worded ("AR", "BLK of the 1M plan") does not cover those.

**Finite n (the parenthetical is wrong).** NEC-b's threshold is (1 + 2A)·log n with A = log p/log n. Population
normalised gain G := (n − 1)a²ρ^{2k}/τ²_∅ (AR) or 0.25(n − 1)a²/τ²_∅ (BLK), U = ∅ (a block next to a truth's block
normally holds no truth), strong arm a = 1, τ²_∅ = 4.30:

| n (p = 10⁶) | threshold | AR, k = 1 | AR radius (corrected) | AR radius (audit, τ² dropped) | BLK |
|---|---|---|---|---|---|
| 200 | 32.9 | 16.7 | **0** | 1 | 11.6 |
| 400 | 33.6 | 33.4 | **0** (borderline) | 2 | 23.2 |
| 800 | 34.3 | 66.9 | 1 | 3 | 46.5 |
| 1600 | 35.0 | 134 | 2 | 3 | 93.0 |

Weak arm (a = 0.6, τ²_∅ = 2.19): AR k = 1 gives 11.8 / 23.6 / 47.3 at n = 200 / 400 / 800 (radius 0, 0, 1).
So at the plan's 1M sizes NEC-b is silent. A first-order heuristic (one term of T₁, `STATEMENT.md:89-90`:
(s₀ + 1)/(2p)·(n + 1)^{−1/2}·e^{G/2}; not a theorem) says one split neighbour at distance 1 costs ≈ 10⁻³ of start odds at
n = 200, ≈ 2.7 at n = 400 (π₀(S₀) ≈ 0.27 if j's neighbour is cut off) and ≈ 4·10⁷ at n = 800; for BLK ≈ 10⁻⁴, 0.02, 10³.
Whether this bites at n = 400–800 depends on whether the realised partition cuts a strong truth from its nearest
neighbours — an engineering quantity that the plan's C3 metric (exact π₀(S₀)) and rung A3 measure. The pigeonhole guarantee
at radius 8 needs G(k = 8) = (n − 1)ρ^{16}/4.3 ≈ 6.5·10⁻⁵ n above ≈ 40, i.e. n of order 10⁶: the asymptotic statement is
right, but it is a statement about very large n unless the partition separates near neighbours.

**What to change in the ticket text.** Keep "candidate #1 does not reach AR or BLK" as an **asymptotic** scope statement
(it is correct). Replace the parenthetical at `TRACK_D.md:34-35` by: "with τ²_U = σ² + unexplained signal (≈ 4.3 on the
strong AR arm), NEC-b's threshold is not met at any distance for n ≤ 400 at p = 10⁶; at those sizes the start mass on S₀
is an empirical question (C3)". Write the random-design step as one sentence (condition on X, quantitative [TK]).

Numeric check: `gains.py` (scratchpad), population gains vs (1 + 2A) log n at n ∈ {200, …, 10⁶}; output above.

## 2. Global overlap P-OVL∞ fails; route TR cannot reach AR (TRACK_D.md:133; CHECKPOINT_2.md:4)

**Verdict: CONFIRMED WITH CORRECTION.**

**The premise, exactly.** `W3-SAMP/STATEMENT.md:79-81`: P-OVL∞ is P(𝒜 ∩ {L/M ≤ c}) → 0 for every c > 0, with
M := max_{S∈Ω} π(S)/π₀(S) and L the executed terminal budget. TR (`:165-177`; registry `W3-SAMP:TR`, `claims.tsv:356`;
proof `W3-SAMP/lemmas/TR_theorem.md`) uses it in (TR-d) together with P-CONC; production corollary (`:171-173`):
L = max(4, ⌈log₂(n + 1)⌉), so P-OVL∞ reads M = o_P(log n) on 𝒜. `:183` records that P-OVL∞ is not derived from conditions
on (X, θ*) — the audit's citation at `TRACK_B.md:192-193` is accurate.

**The calculation.** M ≥ π(S₀)/π₀(S₀). TR-d assumes P-CONC, so π(S₀) → 1 in probability (and on AR/BLK P-CONC is
delivered anyway by `W2-APP:POST`, λ_min(Σ) ≥ 0.25). By item 1, π₀(S₀) ≤ n^{−κ} w.p. → 1 for every κ. Hence
M ≥ ½n^{κ} w.p. → 1 for every κ, and L/M ≤ 2 log₂(n + 1)·n^{−κ} → 0: P-OVL∞ fails at the production budget, and at any
polynomial budget L. ✓ Moreover the finite bound itself is empty: e_L = (1 − 1/M)^L ≥ 1 − L/M → 1, so (TR-b)/(TR-c) give
only E‖p̂_r − 1_{S₀}‖_∞ ≤ g + e_L ≈ 1. So route TR delivers nothing on these designs — not just its asymptotic clause.

**Corrections.**
- "π₀(S₀) is exponentially small" (`TRACK_D.md:133`) does **not** follow from the statement of NEC-b, which gives
  n^{−κ′} for every κ′ (super-polynomial). It does follow from L7.1's displayed inequality
  (`L7_NEC.md:21-24`: log[γ₀(S′)/γ₀(S₀)] ≥ (RSS_U − RSS_{U∪l})/(2τ²_U(1 + ω̄_n)) − ½ log(n + 1) − log 2p − 2κ_E on 𝒢,
  "No upper bound on the gain is used"), since the gain is ≍ n: π₀(S₀) ≤ e^{−c′n} on 𝒢. Either form suffices here; cite
  the proof line, or say "smaller than every power of n".
- Scope of the words "on leaky designs": the failure needs a leak **given the truths of the null's own method block**
  (NEC-b's U = U*_{b(l)}), not just any fixed-level leak. On designs where every leaking null shares a block with its
  truth (S3, S4, S6 if candidate #1's group-containment lemma holds) the calculation says nothing.
- Same asymptotic caveat as item 1: at n ≤ 400, p = 10⁶ no recorded result bounds π₀(S₀) away from 1 on AR/BLK.
- Not asked, one line: the same bound also kills P-OVL of Theorem D (D_r·π₀(S₀) → ∞) once e^{−c′n}·p·log n → 0, i.e.
  asymptotically at fixed A. This does not touch Thm 6 (reported model), whose route is the search (W3-RM), not D.

## 3. λ_min(Σ) of the 13 designs (TRACK_B.md:104-105)

**Verdict: CONFIRMED.** Closed forms (Σ as generated: `Scripts/Data_generators/gen_dev_data.R:18-30`;
`W3-P6/DESIGN.md:15-17`; 1M plan `:86-90`):
- S1, IND: I → 1. S2: AR(0.5), inf over p of λ_min = (1 − ρ)/(1 + ρ) = 1/3. AR(0.6): 0.25.
- S3 = 0.7H + 0.3I, S4 = 0.85H + 0.15I (H = blocks of ones of size 5): 0.3, 0.15.
- S5 = s5 = 0.3J + 0.4H + 0.3I: J, H ⪰ 0 and any vector summing to 0 inside each group is in both kernels → exactly 0.3.
- S6: block correlations 0.4 + 0.1((b − 1) mod 6) ∈ {0.4, …, 0.9} → 1 − 0.9 = 0.1.
- cs(ρ) = ρJ + (1 − ρ)I → 1 − ρ (0.7, 0.5, 0.3); FAC = cs(0.3) → 0.7; BLK = 0.5H₂₀ + 0.5I → 0.5.
- fac2 = 0.35J + 0.25vvᵀ + 0.40I, v_j = (−1)^j → 0.40 (p ≥ 3).
By Cauchy interlacing every principal submatrix has λ_min ≥ these values, so every small-set floor of Thm 1 (population
form), Thm 2 (A3), Thm 6/10 floors and Thm 9's (A4) (c_ψ/n ≤ 0.1 for n ≥ 10c_ψ) holds. Numeric: `designs.py`, λ_min at
p = 500 and 1000 equals the stated value to 4 decimals for all 15 entries (S2 and AR at finite p sit at 1/3 and 0.25 to
4 decimals). The "inside" entries of B5, B6 that rest on this line stand. (Not checked here: B5's separate sentence "No
upper eigenvalue bound is used", which is a reading of the theorems, not an [audit calc].)

## 4. Thm 9 (A3) ⇒ Song–Liang Condition 1 (TRACK_B.md:126-131)

**Verdict: CONFIRMED WITH CORRECTION** (the implication is stronger than the audit states).

*Sources.* Condition 1, Song & Liang (2015) p. 953 (read in place, `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf`,
pdf p. 7): there are constants M > 0 and δ > 0 such that for every subvector (x_{j_1}, …, x_{j_r}), r ≤ r̄_n, and |a_i| ≤ δ,
E exp{(Σ_i a_i x_{j_i}/r)²} ≤ exp(M). Their Gaussian example (same page): zero mean, unit variances, bound (1 − 2δ²)^{−1/2}.
Thm 9 (A3), `W3-READER/READER_VERSIONS.md:1080-1082` (W3-READER worktree at ff35f6b0, being edited; z_j := (x_j − Ex_j)/sd(x_j), `:1065`): for every
u with ≤ q_n nonzero entries, E exp(λuᵀz) ≤ exp(L²λ²Var(uᵀz)/2).

*The audit's calculation is right.* For r ≤ q_n: sd(Σa_iz_{j_i}) ≤ Σ|a_i| ≤ rδ (Minkowski; unit variances), so
Y := Σa_iz_{j_i}/r has Var(Y) ≤ δ² and, by (A3), E e^{λY} ≤ e^{L²δ²λ²/2}; with G ~ N(0, 1) independent,
E e^{Y²} = E e^{√2·GY} ≤ E e^{L²δ²G²} = (1 − 2L²δ²)^{−1/2} for δ < 1/(√2L). At L = 1 this is exactly SL's Gaussian bound.

*Correction: the qualifier "whenever r̄_n ≤ q_n" is unnecessary.* SL's r̄_n may grow faster than q_n ≍ log n, but (A3)
on q_n-sparse directions already controls every r. Split the r indices into consecutive groups B_1, …, B_m of size ≤ q_n
and write Y = Σ_b w_bY_b, Y_b := Σ_{i∈B_b}a_iz_{j_i}/|B_b|, w_b := |B_b|/r (Σw_b = 1). Each Y_b satisfies the bound above,
hence E exp(Y_b²/t²) ≤ 2 for t² = 8L²δ²/3, i.e. ‖Y_b‖_{ψ₂} ≤ √(8/3)·Lδ. The Orlicz norm ψ₂ is a norm, so
‖Y‖_{ψ₂} ≤ Σw_b‖Y_b‖_{ψ₂} ≤ √(8/3)·Lδ, and for δ ≤ √(3/8)/L: E e^{Y²} ≤ 2. **So (A3) implies Condition 1 for every r ≤ P_n,
with δ = √(3/8)/L and M = log 2**, whatever r̄_n is. Two words to keep: Condition 1 is not scale-free, so the implication is
for the standardised predictors z (SL's own setting: "all predictors have been standardized", p. 952, and their Gaussian
example); and (A3) is needed only for q_n ≥ 1.
*Converse fails* (the audit's "bounded, strongly dependent predictors"): accept, with a concrete witness — a direction
uᵀz = c·ξ, ξ ∈ {−1, 0, 1}, P(ξ ≠ 0) = ε: bounded, so Condition 1 holds, but (A3) at that u needs
L² ≳ 1/(ε log²(1/ε)), unbounded as ε → 0 (take λc = log(1/ε)). Verdict "stronger than Condition 1 (implies it)" stands.

## 5. Visibility on S1–S4, S6, IND, AR, BLK, cs (TRACK_B.md:148-151)

**Verdict: CONFIRMED.** Thm 6 (A3), `READER_VERSIONS.md:668-669` (at ff35f6b0): |Cov(W_j, Wᵀθ* | W_U)| ≥ a for every j ∈ S₀ and every
U ∌ j, |U| ≤ 15. Decomposition: Cov(W_j, Wᵀθ* | W_U) = θ*_jVar(W_j | W_U) + Σ_{k∈S₀∖(U∪{j})} θ*_kCov(W_j, W_k | W_U) (terms
with k ∈ U vanish), and Var(W_j | W_U) ≥ λ_min(Σ_{U∪{j}}) ≥ λ_min(Σ).
- Block-diagonal with one truth per block (S3, S4, S6 — `gen_dev_data.R:32-41`, one truth per group of 5; BLK — plan `:92`;
  S1, IND): blocks are independent and stay independent given any U, so the cross terms are 0 **exactly**: visibility
  holds with a = min|θ*_j|·λ_min (0.3, 0.15, 0.1, 0.5, 1). Sharper: Var(W_j | W_U) for cs(ρ) blocks is
  1 − ρ²u/(1 + (u − 1)ρ) ≥ 1 − ρ (u = group-mates in U).
- AR (S2: ρ = 0.5, truths 31–37 apart; 1M: ρ = 0.6, truths ≈ p/5 apart): Markov chain, so Var(W_j | W_U) ≥
  Var(W_j | both neighbours) = (1 − ρ²)/(1 + ρ²) (0.60, 0.47), and every cross term is O(ρ^{gap}) ≤ 0.5³¹ ≈ 5·10⁻¹⁰.
  The audit's "geometrically small terms, ≥ |θ_j|λ_min/2" is right (and loose).
- cs(ρ) of P6, aligned signs (`W3-P6/DESIGN.md:18-19`): all cross terms are θ*_k·ρ(1 − ρ)/(1 + (u − 1)ρ) > 0 with θ*_k > 0, so
  the sum is ≥ θ*_j(1 − ρ). ✓ (cs is outside B9 anyway, so this entry does not reach Thm 6.)
Numeric (`designs.py`; greedy minimisation over |U| ≤ 15 in a ±25 window plus the truths, nearest-15 sets, and 200 random
sets per truth): min_U |Cov(W_j, Wᵀθ* | W_U)|/|θ*_j| = S1 1.000, S2 0.600, S3 0.368, S4 0.186, S6 0.124, AR(0.6) 0.471,
BLK 0.531, cs(0.3) 0.740, cs(0.7) 0.319 — each above the audit's λ_min/2. Greedy search is evidence, not proof; the closed
forms above are the argument.
*The "unclear" entries (not verdict-bearing; these designs are outside B9):* the same search gives s5 0.364 and fac2 0.431
(P6 truths, aligned signs) — no cancellation found — but **S5 of the study 0.0056** (mixed signs ±): a near-cancellation
at some U with |U| ≤ 15, so S5 is likely outside (A3) at any fixed a of practical size; FAC with the 1M signs 0.16.
"Unclear" is the right word for S5 and should not be upgraded.

## 6. Partial covariances under factors (TRACK_B.md:163-168)

**Verdict: CONFIRMED WITH CORRECTION.** The cs(ρ) formula is right: with Σ_UU = (1 − ρ)I + ρJ_u,
Σ_UU⁻¹ = (1 − ρ)⁻¹[I − ρJ/(1 + (u − 1)ρ)], so ρ²1ᵀΣ_UU⁻¹1 = ρ²u/(1 + (u − 1)ρ) and
Cov(W_l, W_j | W_U) = ρ(1 − ρ)/(1 + (u − 1)ρ), minimised at u = 15: 0.0404 (ρ = 0.3), 0.0313 (0.5), 0.0194 (0.7). fac2 and
s5 also stay positive for every |U| ≤ 15: for fac2, loadings (a, ±b) with a² = 0.35, b² = 0.25, ψ² = 0.40, the
different-parity covariance is (a² − b²)/det(I + Λ_UᵀΛ_U/ψ²) > 0, smallest when U is balanced in parity:
0.10/146.5 = 6.8·10⁻⁴ at u = 15; same parity λᵀVλ > 0. Numeric greedy minima (`designs.py`): cs 0.04038 / 0.03125 /
0.01944 (= formula), fac2 6.8·10⁻⁴ (different parity), 0.0255 (same), s5 1.4·10⁻³ (different groups), FAC 0.0404.
**Correction (simplification):** Thm 6 (A4)(i), `READER_VERSIONS.md:670-674` (at ff35f6b0), asks |Cov(W_l, W_j | W_U)| ≤ ϖ_n → 0 for
**all** |U| ≤ 15, **U = ∅ included**. At U = ∅ every null–truth covariance is a fixed constant (cs ρ; fac2 0.60 or 0.10;
s5/S5 0.3 across groups; FAC 0.3), so every null must be in Q, Q = [p], and |Q| ≤ n^b forces p ≤ n^b. The partial-covariance
computation is correct but not needed: write the "outside" verdict for S5, P6 (cs, fac2, s5) and FAC from the marginal
covariance alone.

---

**Files.** Numeric scripts (session scratchpad, not committed): `gains.py` (item 1), `designs.py` (items 3, 5, 6),
`vis2.py` (item 5, factor designs). All runs `nice -n 19`, one core, < 2 min.
