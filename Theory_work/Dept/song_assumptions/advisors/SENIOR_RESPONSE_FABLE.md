# SENIOR_RESPONSE_FABLE — drafting advisor's reply to SENIOR_PROPOSAL_LEAD (Stage 2, single round)

Fable 5.2 (author of `advisors/FABLE_R1.md`), 2026-11-27. Read: SENIOR_FABLE, SENIOR_ASTRA, SENIOR_PROPOSAL_LEAD, ASSUMPTIONS §2 (A-MARGIN-H/U) and §3.3. No code run; every check below is by hand. Notation as in the proposal; c_m := √(2 log C(p−s, m)).

**Overall.** I agree with the merged population form as the headline. It is a sufficient condition for TS-b **after five corrections** (E1–E5). Two are errors as written (E1 sign, E2 cap), one is a false implication in Lemma W (E3), two are bookkeeping (E4, E5).

## 1. Answers to Q1–Q5

**Q1 — AMEND (correct in substance; five edits).**

- **E1. Price ratio is inverted.** "log[π(T)/π(T∖D)]" is negative under BB(1, p). Replace by
  `Pr_n(d) := max_{|D|=d} log[π(T∖D)/π(T)] + (d/2)·log(1+g)`.
  (Same slip in SENIOR_FABLE P-U. The package's Pr_n(d) = log[C(2p−1,s)/C(2p−1,s−d)] + (d/2)log(n+1) is this one.)
- **E2. The coefficient must be capped at 1.** a(ϑ) > 1 for ϑ > 3/4 and a(1) = √2, so "Q_n = T with a = √2 is the worst-case fallback" is wrong: the fallback (unit vectors, no centring) has coefficient 1. Replace by
  `ā(B, N) := min{1, √(2(1 − √(1 − ϑ(B, N))))}`,
  and the third special case by "Q_n = T with ā = 1 is the worst-case fallback".
- **E3. Common base B: correct, but Lemma W's conclusion must be per base, not per class (D, m).**
  - Within one base the per-rival form of (b) is right. R_n(B∪N) = (1−ϑ)R_n(B) falls and ā rises in ϑ, so "(b) for every N" is the same as "min_N √R_n(B∪N) ≥ … + max_N ā·c_m". Both extremes sit at the max-leakage N. Say this in one line.
  - Across bases it fails. Class (D, m) contains rivals from several bases (A, A∪{q}, …). (U2) gives min R base by base, while w_Dm is a maximum over all bases. Example at m = 1: base A∪{q} with a strong proxy q has R near the bare price and zero outside leakage; base A has larger R and moderate outside leakage ā_out. (a) and (b) hold, but the class-level inequality needs √R_n(A∪{q}) ≥ price term + ā_out·c_1, which (a) does not give.
  - So "the population form implies the current conditional-width A-MARGIN-U" is **false for Q_n ≠ T** (true for Q_n = T).
  - Replacement wording for the Lemma W conclusion: "the population form implies the base-indexed conditional-width condition: for every base B ⊆ Q_n and m, √((1−δ)·min_{N⊆Q_n^c,|N|=m} R_n(B∪N)/σ*²) ≥ w_{B,m} + t_n + √(2(1+δ)·B_{D,m_tot}), with w_{B,m}(X) := E_g max_N(−⟨v_{B∪N} − v_B, g⟩), m_tot = |B∖T| + m; TS-b step 3 is run per base."
  - No new proof obligation: for fixed B the sum over N ⊆ Q_n^c of containing-model odds π(T∪(B∖T)∪N | y)/π(T | y) is a sub-sum of the nonnegative class sum of step 2, so the same tight multiplier serves every base. Summing over at most |Q_n|^{m̄} = n^{o(1)} bases is absorbed by n^{−γ}.
- **E4. One slack, one scale.** (a) puts (1+η) on R, (b) puts (1+η) on √R. As written (b) does not follow from (a) even with zero leakage, since (1+η) > √(1+η). Replace (b) by
  `√(R_n(B∪N)/σ*²) ≥ √(2(1+η)·Pr_n(|T∖B|)) + ā(B, N)·c_m`,
  and the second special case by "if max ϑ·log p → 0 outside Q_n, (a) with η implies (b) with every η′ < η for large n" (loss √(1−ϑ) and ā·c_m ≤ √(2ϑ)·c_m → 0).
- **E5. Rival range.** Replace "|B∖T| ≤ m̄ … |N| = m ≤ m̄" by `|B∖T| + |N| ≤ m̄_d := ⌈(2A+1)·d⌉ + 1, d = |T∖B|`. Reasons:
  - As written the isometry window is s + 2m̄, not s + m̄ as (W2) says.
  - Classes with total m > m̄_d have Pr_n(d) − (m/2)·log(n/log p) ≤ −γ log n for large n (p ≤ n^A, any γ < 1), so step 3 dispatches them with no signal. Imposing the full price on them is pure over-demand, and it is large: at d = 1, s = 10, A = 1 the proposal asks for the width at m = 31 where m ≤ 4 suffices.
  - m̄_d stays explicit and population-level. (U1) is then the case B = T∖D, N = ∅ of (a); say so.
- **(a) with proxies at the full deletion price: AGREE as headline.** It is sufficient and needs no extra step. Record the cost honestly: it is not "slightly" stronger when several proxies in Q_n jointly reconstruct a true predictor (block designs; AR(1) with both neighbours of an isolated true predictor: factor (1+ρ²)/(1−ρ²) on the signal). Add a remark: "proxies inside Q_n pay their own full price: (a) may be weakened to the single-rival price [log π(B)/π(T) + ((s−|B|)/2)log(1+g)]₊ for |B| < s, R_n(B)/(σ*²(1+log|Q_n|)) → ∞ for |B| = s, and no condition for |B| > s (FABLE_R1 (M1)); this needs step 2 on the bases T ∪ (B∖T), not yet written." Keep it a remark, not the assumption.
- **Uniform-over-B centred term: AGREE.** For each B, max_N(−⟨v_S, g⟩) ≤ −⟨v_B, g⟩ + E max_N(−⟨v_S − v_B, g⟩) + (Lipschitz ≤ ā)·t. Union over #B ≤ |Q_n|^{m̄} gives √(2 log #B) = o(√log n) on both the centred term and the concentration term. It is absorbed by the slack because Pr_n(d) ≳ log n for d ≥ 1; fix δ ≤ η/(4√m̄) so that the factor √(1−δ) on the width part is absorbed as well.
- **Check on the S1 claim.** "(U2a) minimum ratio equals the exact κ_n" can hold only because the binding D is interior (retained endpoints screen all nulls; leakage 0). Confirm the minimum was taken over bases **with** proxies, e.g. D ∋ endpoint with its outside neighbour in B (ratio 0.735·κ(D) there), not over deletions only.

**Q2 — AMEND.** Display Astra's exact coefficient, capped (E2), and give the reading aid `√ϑ ≤ a(ϑ) ≤ √(2ϑ)` (both elementary; "Fable's 2√ϑ" is the upper bound a·c_m ≤ 2√(ϑ·log C)). The exact form is √2 sharper at small ϑ at no cost. Checked: ⟨v_S, v_B⟩ = ‖(I−P_S)μ‖/‖(I−P_B)μ‖ = √(1−ϑ̂) for S ⊇ B, so ‖v_S − v_B‖ = a(ϑ̂) exactly, and E⟨v_B, g⟩ = 0 for fixed B.

**Q3 — AGREE with the Lead (diverging ratio as headline), one amendment.** The quantifier must be "for every fixed k: inf{R_n(S) : j ∉ S, |S| ≤ k}/(σ*²·log n) → ∞", not |S| ≤ s + m̄: TS-a localises at J = ⌊s + C_s M⌋, which exceeds any fixed m̄ for large M. Keep Astra's fixed-constant version as the remark "at a fixed level M, a constant C_L above the inverse conversion constant on |S| ≤ min(K, J) suffices". Keep the sentence that S1 lies outside TS-a either way. This supersedes my R1 explicit-constant recommendation.

**Q4 — AGREE on status (recorded, not adopted), with one added fact that narrows the open target.** Under A-NEC on T, bounded population R² already bounds the coefficient energy: Σ_j β_j²Var(x_j) ≤ β*ᵀΣβ*/λ_min(Corr(x_T)) ≤ M_μσ*²·n/c_ψ. So "Fable's target form" plus A-NEC is the O(1)-energy pair (Astra R1's O(n) form), and Astra's "→ 0" pair is strictly stronger. Replacement wording: "A-BS′: Var(xᵀβ*) ≤ M_μσ*²; with A-NEC on T this gives Σβ_j²Var(x_j)/(nσ*²) ≤ M_μ/c_ψ. Open: whether the size lemma and the ridge remainder hold at O(1) rather than o(1) coefficient energy (at O(1) the ridge term shifts log odds by O(1) only)." My R1 clause s·b̄_n² = o(n) is the "→ 0" form at fixed s.

**Q5 — see §3 and §4.**

## 2. Lemma W: correctness check

| item | verdict | note |
|---|---|---|
| (W1) inner product and distance | correct | exact identity; use ā (E2) |
| (W1) width per base | correct | ≤ ā_max·c_m; the centred term matters only in the union over B |
| (W2) ϑ̂ ≤ ϑ + 2δ_n | correct | ϑ̂ ≤ 1 − (1−ϑ)(1−δ)/(1+δ) ≤ ϑ + 2δ; needs two-sided isometry on T ∪ B ∪ N (size ≤ s + m̄_d after E5) and R_n(B) > 0, which (a) gives |
| transfer to the coefficient | add one line | ā(ϑ̂) ≤ ā(ϑ) + 2√δ_n (slope of a² is ≤ 2 where a ≤ 1); the width error is 2√δ_n·c_m ≍ (log p)^{3/4}·n^{−1/4} → 0 under A-DIM. The cap is what makes this Lipschitz: without it the modulus near ϑ = 1 is δ^{1/4} |
| "implies the current A-MARGIN-U" | **false for Q_n ≠ T** | E3: state the base-indexed form |
| uniformity over B ⊆ Q_n | correct | needs m̄ fixed and log|Q_n| = o(log n); the tight multiplier is shared (sub-sum argument) |
| corollary (C-i) | correct | both terms are O(√log(p∨n)) |
| corollary (C-ii) | correct | R_n(S)/σ*² ≥ nφ²·d·θ_min² (Schur complement ≥ λ_min of the joint block), Pr_n(d) ≤ d·log(2p√(n+1)), log C(p−s, m) ≤ m̄·log(2p√(n+1)) |

One statement to add next to (U2): **Q_n is an accounting device, not an object to be found.** Any Q_n ⊇ T with log|Q_n| = o(log n) may be used; enlarging it moves rivals from (b) to (a). Non-vanishing leakage outside Q_n is allowed and is priced by ā. Otherwise a referee asks "how do I construct Q_n?".

Worked case for 0.11 (checked by hand): equicorrelation ρ, one omitted predictor, b retained, m added nulls: leakage = mρ²/[(1+(b+m−1)ρ)(1+bρ)], which is ρ²/(1+bρ)² at m = 1 (matches SENIOR_FABLE) and increases to ρ/(1+bρ) as m grows. Every null leaks equally, so Q_n = T and (b) with ā ≈ √leakage is the operative form — a clean example of the "interpolated" regime.

## 3. §0 items I would push back on

- **0.7 (windows "for every fixed c > 0").** Fine for fixed-M statements, but the delivered `thm:dist` holds for M₀ ≤ M ≤ √n/log n, where q_n(M) is far above c·log n. As worded, v1.4 would silently shrink the delivered theorem's range. Add: "for M = M_n → ∞ the window is q_n(M_n)" (Astra's common design order k_n ≥ q_n(M)).
- **0.2 (C = 1).** Agree. Consequence to state: with C = 1 the credit −(m/2)·log(n/log p) is a deterministic population quantity, so the merged form gives it up by choice, not by necessity. E5 recovers most of it through m̄_d.
- **0.8 (converse remainder).** Agree. The O_P(1) remainder is enough for the boundary limit P(π(T|y) ≤ ½) → Φ(−c): the leading fluctuation is √(2Pr_n)·(c + Z), which dominates O_P(1) except on an event of vanishing probability. Say so, or a referee will think o_P(1) is needed.
- **0.6.** Agree, including the Cramér-decomposition equivalence (τ² = 0 allowed). No objection to 0.1, 0.3–0.5, 0.9–0.12.

## 4. What a referee would still object to after v1.4 (three items)

1. **TS-b is still a target, not a theorem.** The truncated superset sum, the coded mixed-rival odds and the size lemma under A-BS are unwritten, and Lemma W with the base-indexed step 3 is now added to that list. Polynomial p and fixed s remain against SL Cor 1.
2. **No necessity counterpart for (U2b).** Constant 2 is proved sharp for deletions only. For mixed rivals there is one worst-case example (factor proxy, single swap) and no evidence that ā·c_m with m up to m̄_d is needed. The common-base bound is conservative when many null sets leak in nearly the same direction.
3. **The high-dimensional "misspecification" tier assumes a Gaussian-linear model for the candidates.** After 0.6 this is plainly stated, which is right, but the only result that tolerates a wrong response law is the fixed-dimension TM-a0.
