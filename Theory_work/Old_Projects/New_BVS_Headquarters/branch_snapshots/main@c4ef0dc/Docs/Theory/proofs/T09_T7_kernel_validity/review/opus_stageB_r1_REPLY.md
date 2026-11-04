(Stage B reviewer: Opus 5.5, effort xhigh, native Agent tool on Claude Personal, Plan (read-only) type, packet Temp/v3proofs/T09_T7_kernel_validity/review_B_opus/. Reply saved verbatim by the lead.)

# Stage B review of T09 (T7), PROOF_v2.tex against STATEMENT.md

**Verdict: verified.** I found no fatal error and no gap that blocks a claim. I re-derived every computation in the proof, including all of Section 6. The seven findings below are all exposition-level; F1 is the one to look at first.

## Scope and method

I read only REPORT_FORMAT.md, STATEMENT.md and PROOF_v2.tex, and ran nothing. Lemma numbers follow the shared LaTeX counter:
- Lemma 1: Positivity
- Lemma 2: Metropolis–Hastings form
- Lemma 3: Adjoints
- Lemma 4: Doeblin contraction
- Lemma 5: Convolution
- Proposition 6: Part (i)
- Lemma 7: the formula for ε_φ
- Proposition 8: Part (iv)
- Lemma 10: bounds B1–B3
- Lemma 11: asymptotics
- Lemma 12: start, target and discrepancy
- Proposition 13: the non-reversible order
- Proposition 14: Part (v)

## What I checked independently

**Lemma 1 (Positivity).**
- The vectors a_i = X_S b_i/√s_i are orthonormal, because a_iᵀa_j = b_iᵀG b_j/√(s_i s_j) = δ_ij.
- X_S H_S⁻¹ X_Sᵀ = Σ s_i/((n+1)s_i+1) a_i a_iᵀ, and every coefficient is below 1/(n+1).
- So Q_S ≥ ‖y‖²/(n+1) = (n−1)/(n+1) > 0.
- Each factor of D_S is ((n+1)s+1)/(s+1) ≥ 1.
- The prior weight w(k) = ½/C(2p−1,k) is positive for k ≤ K ≤ p ≤ 2p−1.

**Lemmas 2–4.**
- *Lemma 2:* with both proposals positive, q(x)Q(x,y)(1∧r) = min{q(x)Q(x,y), q(y)Q(y,x)}, which is symmetric. If only one proposal is positive, r = 0 and both sides are 0.
- *Lemma 3:* ⟨Pf,g⟩_q = Σ_y q(y)f(y)Σ_x P\*(y,x)g(x) with P\*(y,x) = q(x)P(x,y)/q(y). The product rule for adjoints holds, and reversibility plus stochasticity gives qP = q.
- *Lemma 4(a):* R = (P − c𝟏ν)/(1−c) is stochastic, and for μ(Ω) = 0, μP = (1−c)μR.
- *Lemma 4(b):* ½‖δ_x − q‖₁ = 1 − q(x).
- *Lemma 4(c):* P maps L²_0 into itself. For an eigenpair Pf = λf, μ = qf satisfies μP = λμ by reversibility, so |λ| ≤ 1 − c. Also (P − Π)(a𝟏 + g) = Pg. This gives gap\* ≥ c.

**Part (i).**
- Lemma 5 is a convolution induction. The positivity claim, c^{(b)}(t) > 0 exactly when 0 ≤ t ≤ P_b, holds because every r_b > 0.
- The step-1 denominator is at least w(0)c(0) = ½ · Π_b BF(∅) = ½.
- Step-2 well-definedness: the downward induction carries positivity of c^{(b)}(t_b) to t_0 = 0.
- The unique run producing S has probability [w(k)c(k)/ΣW]·[c^{(0)}(0)/c^{(J)}(k)]·Π r_b. Since Σ_{k′} w(k′)c(k′) = W_K Z̄₀ and w(k)Π r_b = W_K γ₀(S), this equals π₀(S). The e_b factors cancel and the c^{(b)} factors telescope.
- Truncating the convolution at degree K is exact, as the proof's remark says.

**Part (ii).**
- *Gibbs:* if K(S,T) > 0 then {T⁺,T⁻} = {S⁺,S⁻}, and q(S)K(S,T) = γ(S)γ(T)/(Z̄(γ(S⁺)+γ(S⁻))) is symmetric. S⁺ ∉ Ω exactly when j ∉ S and |S| = K.
- *Uniform swap:* Q(S,S′) = Q(S′,S) = 1/(|S|(p−|S|)). Moves preserve size, so the states of size 0 and p are never proposed from elsewhere.
- *Neighbour swap:*
  - Q(S,S′) = 1/(|S||N(j)∖S|) when l ∈ N(j); Q(S′,S) = 1/(|S′||N(l)∖S′|) when j ∈ N(l).
  - The denominators are nonzero because l ∈ N(j)∖S and j ∈ N(l)∖S′, and |S| = |S′| cancels.
  - If j ∉ N(l), the true Hastings ratio is 0, which matches the "read as 0" convention.
  - Symmetry of the method's graph rules that case out.
- *Independence:* q(S)/π₀(S) = (Z̄₀/Z̄_φ)e^{φd(S)}, so the ratio is e^{φ[d(S′)−d(S)]}.

**Part (iii).**
- K_σ\* = K_{σ(m)}⋯K_{σ(1)} = K_σ̄. Reversal is a bijection on orders, so K_φ\* = K_φ.
- K_σ is reversible exactly when K_σ = K_σ̄.

**Part (iv).**
- For u ≠ v: K_ind(u,v) = min{π₀(v), q(v)π₀(u)/q(u)} ≥ εq(v). Also K_ind(u,u) ≥ π₀(u) ≥ εq(u).
- With the round split around the independence step, Σ_u A(x,u)·ε·Σ_v q(v)C(v,y) = εq(y), using that A is stochastic and qC = q.
- ε ≤ 1 because π₀ > q everywhere would force 1 > 1.

**Section 6, the two-variable family.**
- Norms are ‖x₁‖² = ‖x₂‖² = ‖y‖² = s² = n−1. Inner products are x₁ᵀx₂ = (n−1)c, z₁ = (n−1)ρ, z₂ = (n−1)cρ.
- p = 2, K = 2 for n ≥ 4, and B = 1.
- Prior: w = (½, 1/6, 1/6).
- Singletons: H = (n+1)(n−1)+1 = n², D = n²/n = n, and Q = (n−1) − z²/n. This gives Q_a and Q_b as stated.
- The pair {1,2}:
  - Eigenvalues: α± = (n²−1)(1±c)+1 and β± = (n−1)(1±c)+1.
  - The identity α± = (n+1)β± − n holds, so D_ab = f(1+c)f(1−c) with f(x) = n+1 − n/((n−1)x+1). f is increasing (f′ = n(n−1)/((n−1)x+1)² > 0) and f ≤ n+1.
  - Projections: zᵀe± = (n−1)ρ(1±c)/√2. Since 1±c = (α±−1)/(n²−1), each term (1±c)²/α± equals ((1±c)/(n²−1))(1 − 1/α±).
  - So t_ab = n(n−1)ρ²/(n+1)·(1 − δ/2), with 0 < δ < 2/(n²−1).
  - Sanity check at c = 0: t_ab = (n−1)²ρ²/n, as expected.
- Lemma 10:
  - *B1:* n/(n+1) − (n−1)/n = 1/(n(n+1)). The first term is in [0, 1/n). The second is below nρ²/(n+1)², which is below 1/n.
  - *B2:* (n−1)/(n+1) ≥ ½ exactly when n ≥ 3.
  - *B3:* f(x) ≥ n/2+1 when (n−1)x ≥ 1.
- Lemma 11:
  - The limits (1/n)log R_a → κ_a, (1/n)log R_b → κ_b and (1/n)log R_{ab|b} → κ_a − κ_b all hold. The D-factors lie in [1/(3(n+1)), n^{1/2}], so they contribute only O(log n) to the logarithms.
  - γ₁(b)/γ₁(a) = (A_a/A_b)^ν, using D_a = D_b and w(1) = w(1).
  - A_a/A_ab ≤ 1 + 2/n, and (1+2/n)^ν ≤ e^{1+0.02/n} ≤ e^{1.01}. Combined with (D_a/D_ab)^{1/2} ≤ 2n^{−1/2}, this gives R_{ab|a} ≤ 2e^{1.01}n^{−1/2}.
- Lemma 12:
  - Start ratios: γ₀(a)/γ₀(ab) = 1/(3R_b), γ₀(b)/γ₀(ab) = 1/(3R_a), γ₀(∅)/γ₀(ab) = 3/(BF(a)BF(b)) = 1/(3R_aR_b).
  - Discrepancy: d(∅) = d(a) = d(b) = 0 and d(ab) = log R_{ab|a} − log(3R_b).
  - Bound: ε₁ ≤ π₀(a)/q₁(a) ≤ 1/(3R_b q₁(a)).
- Proposition 13:
  - Every path factor checks out.
  - K_ind(∅,∅) = 1 − π₀(a) − π₀(b) − π₀(ab)(1∧e^{d(ab)}).
  - The reversed order σ̄ = (ind, ns, us, G1, G2) is correct.
- Proposition 14:
  - 3!/5! = 1/20 of the orders end with Gibbs 1 then Gibbs 2.
  - For those orders, the probability Gibbs 1 adds variable 1 is R_a/(1+R_a) or R_{ab|b}/(1+R_{ab|b}). From a or ab, Gibbs 2 lands at a with probability 1/(1+R_{ab|a}).
  - So K₁(x,a) ≥ θ_n/20 ≥ 1/40, and Lemma 4 applies with ν = δ_a.
  - log(40/39) ≥ x − x²/2 with x = 1/39, giving 0.025312 > 0.0253; 55 × 0.0253 = 1.3915 > 1.39 > log 4 = 1.3863. 54 steps would not be enough with this bound (54 × 0.025318 ≈ 1.367 < log 4), so 55 is the tight count.
- The common rate κ = κ_b/2 works for both ε₁ ≤ e^{−κn} and the discrepancy range being at least κn.

## Faithfulness of the precise readings

- **(iii).** The original says "An individual realised order need not be reversible." The reading asks for existence of a non-reversible K_σ, and adds invariance of every K_σ and the criterion "reversible exactly when K_σ = K_σ̄". That is the original's content plus more, so it is faithful.
- **(v).** The original says a small minorisation constant "does not establish exponentially slow mixing" and that a switch or a large discrepancy range "alone" does not supply such a lower bound. The reading constructs one family that has all three features together, while the gap stays at least 1/40 and t_mix at most 55. That refutes each implication alone and all of them together. The v2 change-log correction (a lower bound tending to infinity, not to 0) is right. Faithful, subject to F1 and F7.

## Findings

**F1.**
- **Location:** Section 6, closing paragraph ("any such implication would fail on this family"); STATEMENT (v), the "Consequently…" sentence.
- **Severity:** exposition (borderline gap).
- **Claim:** The proof shows the family has ε₁ ≤ e^{−κn} and discrepancy range ≥ κn with κ = κ_b/2, where κ_b = ½log(1/(1−c²ρ²)) for fixed correlation c and ρ. In fact ε₁ ≍ 1/BF(b) ≍ e^{−κ_b n}. Take a would-be implication whose hypothesis fixes a rate, such as "ε_φ ≤ e^{−5n} ⇒ gap → 0". At the example values c = ½, ρ = 3/5 we get κ_b ≈ 0.047, so the family does not satisfy that hypothesis and does not refute the implication.
- **Evidence:** κ_b = ½log(1/0.91) ≈ 0.047. The STATEMENT's own wording ("there exist constants c > 0") reads "exponentially small" and "large range" existentially, and under that reading the sentence is proved. The stronger fixed-rate version is easy to repair, but the proof never states the repair: κ_b → ∞ as cρ ↑ 1, and every argument in Lemmas 10–12 and Propositions 13–14 holds for any fixed c, ρ ∈ (0,1).

**F2.**
- **Location:** Lemma 12(c), "so (1/n)d(ab) → −κ_b".
- **Severity:** exposition.
- **Claim:** This two-sided limit needs (1/n)log R_{ab|a} → 0, which requires a lower bound on R_{ab|a}. Lemma 11 states only the upper bound.
- **Evidence:** The limit follows from Lemma 11 through R_{ab|a} = R_{ab|b}·γ₁(b)/γ₁(a), where (κ_a−κ_b) − (κ_a−κ_b) = 0. A direct route: A_a/A_ab ≥ 1 − 2/n and D_a/D_ab ≥ n/(n+1)². Downstream, Proposition 14 uses only −d(ab) ≥ log(3R_b) − log(2e^{1.01}n^{−1/2}), which needs just the upper bound. So nothing breaks.

**F3.**
- **Location:** Section 6, "The family".
- **Severity:** exposition.
- **Claim:** Two justifications cite facts about the method that the packet does not contain, so I cannot verify them:
  - the preprocessing "being invariant to centring and positive rescaling";
  - "the top-down cut splits until every retained cluster has at most one member".
- **Evidence:** Neither is needed. STATEMENT §1 already says a standardised pair is returned unchanged, and |C_b| ≤ B = 1 forces the blocks {1}, {2} on [2]. The neighbour graph is left unspecified, which is harmless: N(j) ⊆ {1,2}∖{j}, and the neighbour-swap factors used (at ∅ and ab) are 1 for any graph.

**F4.**
- **Location:** Section 6 throughout.
- **Severity:** exposition.
- **Claim:** Several symbols are overloaded:
  - c is the correlation in the proof but the rate constant in STATEMENT (v); the proof uses κ for the rate.
  - b is the block index and also the state {2} (as in R_b, κ_b).
  - e_± are eigenvectors, while e_b(j) are the block size profiles.
  - π is used for q₁ in Lemma 12(b).
- **Evidence:** This is readable but invites misreading against STATEMENT.

**F5.**
- **Location:** Section 2, the conventions before Lemma 5; step (2) of the sampler.
- **Severity:** exposition.
- **Claim:** STATEMENT does not give the index ranges for the recursion c^{(b)}(t) = Σ_j e_b(j)c^{(b−1)}(t−j) or for the draw of j_b. The proof adopts e_b(j) = 0 outside 0..|C_b| and c^{(b)}(t) = 0 for t < 0.
- **Evidence:** These are the natural conventions and make the sum-to-one claim exact. The proof should say they are what STATEMENT intends.

**F6.**
- **Location:** Lemma 11 proof, "The factors D_S^{−1/2}, 1/3 and (D_b/D_ab)^{1/2} are between (n+1)^{−1}·⅓ and n^{1/2}".
- **Severity:** exposition.
- **Claim:** The sentence lumps several factors together.
- **Evidence:** Taken one by one, each factor and each relevant product lies in [1/(3(n+1)), n^{1/2}], so the O(log n) conclusion holds.

**F7.**
- **Location:** STATEMENT (v) reading.
- **Severity:** exposition (faithfulness note, not a defect).
- **Claim:** The original wording does not say which parameter "exponentially small" refers to. The reading fixes the sample size n as the parameter and the family keeps p = 2.
- **Evidence:** This is a legitimate reading, since BF ratios scale as e^{Θ(n)}. Results about exponential behaviour in p are neither claimed nor refuted. It would help to say this explicitly.

## Verdict

**Verified.** Under STATEMENT.md's stated quantifiers, the proof establishes every claim, (i) through (v), including the precise readings of (iii) and (v), and those readings are faithful to the quoted original wording. The fixed-rate strengthening in F1 is the only point worth tightening.
