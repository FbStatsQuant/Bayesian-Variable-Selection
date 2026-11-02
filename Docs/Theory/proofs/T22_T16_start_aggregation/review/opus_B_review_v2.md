# Opus 5.5 (xhigh) Stage B review of PROOF_v2 — reply saved verbatim by the lead

# Review report: T22 (T16), parts (i), (ii), (iv), PROOF_v2

**Scope of review.** I read only the four packet files: STATEMENT.md, PROOF_v2.tex, PROOF_v2.pdf and REPORT_FORMAT.md. I ran no builds, simulations or jobs; the only command was a read-only directory listing. The PDF has the same mathematical content as the .tex, page by page.

## Claim-by-claim verification

**Lemma 1 (closed forms, positivity): checked.**
- The identity (I_n+cAAᵀ)A = A(I_k+cAᵀA) gives AH_S⁻¹Aᵀ = (1/c)(I − (I+cM_S)⁻¹), so the formula for t_S is correct.
- The eigenvalues of I − (I+cM_S)⁻¹ are cλ/(1+cλ), which lie in [0,1). So 0 ≤ t_S ≤ (n/(n+1))yᵀy and Q_S ≥ yᵀy/(n+1).
- Sylvester's identity with t = c and t = 1 gives the formula for D_S, and D_S ≥ 1 follows.
- w(k) > 0 for k ≤ p, because p ≤ 2p−1 when p ≥ 1. W_K ≥ w(0) = ½.
- For S = ∅ the formulas give t_∅ = 0 and D_∅ = 1, as the statement requires.

**Lemma 2: checked.**
- M_{S+l} = M_S + x_l x_lᵀ, and inversion reverses the Loewner order, so t_{S+l} ≥ t_S.
- The matrix determinant lemma with x replaced by √c·x gives the ratio (1+cα)/(1+β).
- α ≤ β, and 1 + cβ ≤ c(1+β) because c ≥ 1. Both factors of m(S+l)/m(S) are then bounded correctly.

**Lemma 3: checked.**
- C(N,k)/C(N,k+1) = (k+1)/(N−k).
- For i ≤ j−1 ≤ p−s−1, the denominator satisfies 2p−s−i−1 ≥ p ≥ p−s > 0.

**Equation (1) and the bijection Φ: checked.**
- γ₀ = γ₀^unc/W_K on Ω.
- (S∪S°)∖(S°∖S) = S; (T∖M)∪S° = T; S°∖(T∖M) = M.

**Lemma 4: checked.**
- The map T ↦ (V_b) is a bijection onto ∏_b 2^{C_b∖U_b*}. Grouping by j = Σ|V_b| gives exactly Σ_j [w(s+j)/w(s)]·c_j, with c_j = Σ ∏_b a_{b j_b}.
- The bound a_{bj} ≤ D_b^j/j! holds in all three ranges: j = 0 (including D_b = 0 with 0⁰ = 1), 1 ≤ j ≤ |C_b∖U_b*| (from the definition as a maximum), and larger j (where a_{bj} = 0).
- The multinomial theorem gives (ΣD_b)^j/j! = ((p−s)q)^j/j!.
- The binomial-coefficient step, the bound Σ_{j≤p−s} ≤ Σ_{j≥0} (uses q ≥ 0), and the negative binomial series for q < 1 are correct.
- The s = p case is handled separately.

**Lemma 5: checked.**
- If M ≠ ∅ then s ≥ 1, so e's index set is nonempty: it contains (b, ∅) for any b with U_b* ≠ ∅.
- For each b with a_b = |M∩C_b| > 0, the pair (b, U = S∩C_b) is in e's index set and T∩C_b = U∪U_b*.
- In the prior telescoping, every intermediate size k ≤ |T|−1 ≤ p−1, and w(k)/w(k+1) ≤ 2p−1 < 2p.

**(i-a): checked.**
- Σ_{M⊆S°} e^{|M|} = (1+e)^s, including s = 0, where e = 0 and the sum is 1.
- 1 − xz = (1−x) + x(1−z) ≤ (1−x) + (1−z) because x ≤ 1.
- Bernoulli's inequality holds for q ∈ [0,1).
- The mean value step for g(t) = 1 − (1+t)^{−s} is correct; at s = 0, g ≡ 0.

**(i-b): checked.**
- μ_l has a nonempty index set, because T = U_b* is admissible when l ∉ S°.
- The telescoping chain T_{i−1} ⊆ C_b∖{v_i} is admissible.
- j!·e_j(μ) ≤ (Σμ)^j for μ ≥ 0.
- The empty-block case gives 0 ≤ 0.
- The sets C_b∖U_b* partition [p]∖S°.
- The two bound functions have the required monotonicity on [0,1).

**(i-c): checked.**
- When s ≥ 1, δ^comp is a maximum over a nonempty finite set, since ∅ ∈ Ω and ∅ ⊉ S°.
- At most 2^s − 1 nonempty M occur per T. When s = 0 the factor is 1 + 0·0 = 1.
- Infeasible T only enlarge the upper bound.
- The step q ≤ u < 1 is taken from (i-b).

**(ii-a), Lemma 6, (ii-b): checked.**
- The normalisers cancel, and S₀, S° ∈ Ω.
- Only block b(l) changes.
- The ratio r_b(U+l)/r_b(U) = m(U+l)/m(U) is where the Bayes-factor tables are used, and Lemma 2 bounds it.
- The indices satisfy s+i ≤ s₀−1 ≤ K−1 ≤ p−1, so every r_{s+i} and w(k+1)/w(k) used is defined.
- The case s₀ = s gives S₀ = S°, which matches the empty product.

**Lemma 7, (iv-a), (iv-b), (iv-c): checked.**
- γ₁ = ϖ·BF, so q₁ = π. q₀ = π₀ holds by definition, since exp(0) = 1.
- R₀ = Σα_S and R₁ = Σβ_S.
- Hölder's inequality with exponents 1/(1−φ) and 1/φ gives the bound for φ ∈ (0,1). At φ ∈ {0,1} it is an equality because R₀, R₁ > 0.
- 1/(1 + max(R₀,R₁)) = min(π₀(S₀), π(S₀)).
- For (iv-c), the event inclusion {Σ_n > η} ⊆ E_nᶜ ∪ {1−π₀ > η/2} ∪ {1−π > η/2} is correct.
- φ ↦ q_φ(S₀) is continuous, so a supremum over rational φ suffices for measurability.

**Edge cases: all checked.**
- s = 0: e = δ^comp = 0, Lemma 5 is trivial, and 2⁰ − 1 = 0.
- s = p: q = u = 0, 𝒯 = {[p]}, and this case requires p ≤ K.
- Empty maxima: D_b, e and δ^comp.
- 0⁰ conventions: D_b⁰, e⁰ and R_i⁰.
- Size cap K: the completions may lie outside Ω and are used only in upper bounds; the (ii-b) chain stays inside Ω.

**Generality (C6).** Section 2 uses only positivity of the tables; it never uses r_b(∅) = 1 or the Bayes-factor structure. (ii-b) is the only place that uses r_b = BF, and the statement provides that.

**Hand checks.** I worked two small examples by hand and both satisfy the bounds.
- **p = 1, one block, S° = ∅:** π₀ = 1/(1+β). The (i-a) lower bound is 1−β, and (1+β)(1−β) ≤ 1.
- **S° = {1} in the same setting:** the (i-c) bound is attained with equality, β/(1+β).
- **p = 2, singleton blocks, S° = ∅, β₁ = β₂ = β:** (1−β)(1 + 2β/3 + β²/3) = 1 − β/3 − β²/3 − β³/3 ≤ 1.

## Findings

All five findings are exposition-level. None affects correctness.

**Finding 1**
- **Location:** PROOF_v2.pdf, page 3, the display in the proof of Proposition 1 ((i-a)).
- **Severity:** exposition.
- **Claim:** The display line is too wide. Its final factor γ₀^unc(S°) is cut off at the right margin of the compiled PDF.
- **Evidence:** The PDF line ends "…≤ (1+e)^s/(1−q)^{s+1} γ". The .tex source (line 122) contains the complete expression `\frac{(1+e)^s}{(1-q)^{s+1}}\,\gu(S^\circ)`.

**Finding 2**
- **Location:** Proof of Lemma 1, the step "I_n+cM_S ⪰ I_n+M_S ≻ 0, so D_S ≥ 1".
- **Severity:** exposition.
- **Claim:** The step uses, without saying so, that the determinant is monotone in the Loewner order.
- **Evidence:** The fact is standard and true here. M_S has eigenvalues λ_i ≥ 0, so D_S = ∏(1+cλ_i)/(1+λ_i) ≥ 1. A one-line justification would make the step self-contained.

**Finding 3**
- **Location:** Throughout the proof: preamble, Lemma 1, Lemma 2, Lemma 4, Proposition 6.
- **Severity:** exposition.
- **Claim:** Several symbols mean different things in different places:
  - c := n+1, but c_n is the normalising constant and c_j is a coefficient in Lemma 4.
  - t is both t_S and the real parameter in Sylvester's identity, and g(t) uses it again.
  - α and β mean one thing in Lemma 2 and α_S, β_S another in Proposition 6.
- **Evidence:** No step is ambiguous in context, so this does not affect correctness.

**Finding 4**
- **Location:** Proof of Proposition 6, the case "If Ω = {S₀}".
- **Severity:** exposition.
- **Claim:** This case can never occur, so the 0⁰ convention of (iv-a) is never actually needed.
- **Evidence:** n ≥ 3 and p ≥ 1 give K ≥ 1, so ∅ and {1} are both in Ω and |Ω| ≥ 2. Therefore R₀, R₁ > 0 always. Handling the case anyway is harmless, and the convention is still respected.

**Finding 5**
- **Location:** Preamble, and the coefficient bound and multinomial step in Lemma 4.
- **Severity:** exposition.
- **Claim:** The preamble states the convention e⁰ := 1 only for e. Lemma 4 also uses 0⁰ = 1 for D_b⁰ when D_b = 0, and inside the multinomial theorem.
- **Evidence:** The proof states this inline as "(D_b⁰ = 1)", so it is covered. A global statement of the convention would be cleaner.

## Conclusion

Every claim, (i-a), (i-b), (i-c), (ii-a), (ii-b), (iv-a), (iv-b) and (iv-c), is proved exactly as STATEMENT.md states it, with every hypothesis taken from STATEMENT.md or proved in the text. The edge cases s = 0 and s = p, the size cap K, the empty maxima and the 0⁰ conventions are all handled correctly. I could not construct a counterexample to any step. All findings are exposition-level.

VERDICT: verified
