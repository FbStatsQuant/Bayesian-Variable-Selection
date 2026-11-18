# T-c-1
stop_reason: end_turn

# Card T, route T-c (adversarial) — no counterexample; the statement is true as written, with a proof

**Verdict.** Every attack I tried fails, and the reason is structural: the lemma holds exactly as stated, with the card's constants. Section 2 gives a complete proof, which is the precise explanation of why the attacks fail. The proof needs only d ≤ P (to enlarge supports) and d ≤ n − 1 (so that 2n ≥ 2(d+1)).

Notation: g_θ(x) := min{1, (a + uᵀx)²/c} for θ = (a, u, c). P is the population law and P_n the empirical measure. S̄ := (eP/d)^d (2en/(d+1))^{2(d+1)} and η² := (4/n)[log S̄ + log(4/δ)]. This η² is exactly the card's remainder, and δ = 4S̄e^{−nη²/4}.

## 1. Attacks and why each fails

**A. d close to n (statement is vacuous there).**
- Since P ≥ d and δ < 1, the bracket is at least d + 2(d+1)log(2en/(d+1)) + log 4.
- With ρ := n/(d+1), η² < 1 forces ρ > 4 + 8 log(2eρ), i.e. ρ > 48.6. For d = 1 this means n ≥ 100.
- So the lemma has content only when n > 48(d+1); elsewhere the left side is ≤ 1 ≤ η².
- The natural attack is a hyperplane through d sample points in the d active coordinates, with c ↓ 0 so that g = 1{off the hyperplane}. It gives P_n g ≥ 1 − d/n and Pg ≤ 1, and 1 ≤ 2(1 − d/n) + η² whenever d ≤ n/2. It only bites for d ≥ n/2, which is deep in the vacuous region. (S1-01's counterexample needs d ≫ 2n and is excluded by d ≤ n − 1.)

**B. Atomic law with a hidden atom.**
- Take x = e₁ with probability q and x = 0 otherwise. With a = 0, u = e₁, c ≤ 1: g = 1{x ≠ 0}, Pg = q, P_n g = R/n with R ~ Bin(n, q).
- Failure means R < n(q − η²)/2. By the multiplicative Chernoff bound with γ = (q + η²)/(2q), the probability is ≤ exp(−n(q + η²)²/(8q)) ≤ e^{−nη²/2} = (δ/(4S̄))².
- The same holds for any single g and any law: for [0,1]-valued g, P(P_n g ≤ Pg − t) ≤ exp(−nt²/(2Pg)), and t = (Pg + η²)/2 gives ≤ e^{−nη²/2}.
- So one function fails with probability at most (δ/4S̄)². A counterexample would need about 16S̄²/δ nearly disjoint failure events, while the class shows at most S̄ distinct behaviours on any 2n points. Section 2 makes this exact.

**C. Best multiplicity attack found (falls short by a factor > 17 in q).**
- Mix: with probability q, x is continuous on ℝ^d; otherwise x = 0. If R ≤ d − 1 continuous points are sampled, an affine hyperplane contains the whole sample, so P_n g = 0 and Pg = q for g = 1{off the hyperplane}.
- For q ≈ (d − 1)/n this has constant probability, so a remainder of order below d/n would be false. The d/n order is necessary.
- But failure needs q > η² ≥ 17.5(d+1)/n. Then P(R ≤ d − 1) ≤ exp(−(1 − 1/17)²nq/2) < e^{−nη²/4} = δ/(4S̄).

**D. Heavy tails.**
- g takes values in [0,1] and the argument is purely combinatorial (traces on 2n points), so no moment enters.
- For P = d = 1 the level sets are complements of closed intervals, a class invariant under monotone maps. For a continuous law (Cauchy included) the problem is the uniform one.
- The worst set is the complement of the sample range, whose mass is Beta(2, n−1). Then P(mass > η²) ≤ (1 + nη²)e^{−(n−1)η²}, far below δ.

**E. Measurability of the supremum.**
- (a, u, c) ↦ g_θ(x) is continuous on {c > 0} for every x. By dominated convergence, Pg_θ and P_n g_θ are continuous in θ along sequences that keep supp u fixed.
- So the event of the lemma equals the same event over the countable set 𝒬 of rational parameters, and is measurable.
- Indicators of half-spaces are not pointwise separable under rational approximation. The proof avoids this by using only a countable class of sets (Step 3) and right-continuity in the level z.

## 2. Proof of the statement as written

**Step 0 (binomial lemma, elementary).** If B ~ Bin(n, p) and np ≥ 36, then P(B ≥ np) ≥ 1/16.

*Proof.* Let Z = B − np = Σξ_i and σ² = np(1−p).
- Eξ⁴ = p(1−p)[(1−p)³ + p³] ≤ p(1−p), so EZ⁴ = nEξ⁴ + 3n(n−1)(p(1−p))² ≤ σ² + 3σ⁴.
- Case σ² ≥ 1: EZ⁴ ≤ 4σ⁴. Hölder gives σ² = E|Z|^{2/3}|Z|^{4/3} ≤ (E|Z|)^{2/3}(EZ⁴)^{1/3}, so E|Z| ≥ σ/2 and EZ₊ = E|Z|/2 ≥ σ/4. Cauchy–Schwarz gives EZ₊ ≤ σ·P(Z > 0)^{1/2}, so P(Z > 0) ≥ 1/16.
- Case σ² < 1: 1 − p < 1/(np) ≤ 1/36, so λ := n(1−p) = σ²/p < 36/35. Also n ≥ 36, so λ/n < 1/35. Then P(B ≥ np) ≥ p^n = (1 − λ/n)^n ≥ exp(−λ/(1 − λ/n)) ≥ e^{−18/17} > 1/16. ∎

**Step 1 (trace count).** For T ⊆ [P] with |T| = d, let ℋ_T := {{f > 0} : f ∈ V_T}, V_T := span{1, x_j (j ∈ T)}, of dimension k := d + 1. Let 𝒜 := ∪_T {H ∪ H′ : H, H′ ∈ ℋ_T}.

(i) ℋ_T shatters no k+1 points. For z₁, …, z_{k+1} there is w ≠ 0 with Σw_i f(z_i) = 0 for all f ∈ V_T, and we may take {i : w_i > 0} ≠ ∅. If some f had {f > 0} ∩ {z_i} = {z_i : w_i > 0}, then Σw_i f(z_i) > 0, a contradiction.

(ii) Sauer–Shelah lemma (Sauer, J. Combin. Theory A 13 (1972) 145–147; Vapnik–Chervonenkis 1971): a class shattering no set of k+1 points has at most N_k(m′) := Σ_{i≤k} C(m′, i) traces on any m′ points.

(iii) For a 2n-tuple with m′ ≤ 2n =: m distinct points, the number of distinct indicator vectors of 𝒜 is at most C(P, d)·N_k(m)². Now:
- m ≥ 2k because d ≤ n − 1. So N_k(m) ≤ Σ_{i≤k} m^i/i! ≤ (m^k/k!)·Σ_{j≥0}(k/m)^j ≤ 2m^k/k!.
- k! ≥ e(k/e)^k (induction), so N_k(m) ≤ (2/e)(em/k)^k.
- C(P, d) ≤ P^d/d! ≤ e⁻¹(eP/d)^d.

Hence S(2n) := max over 2n-tuples of the number of indicator vectors satisfies **S(2n) ≤ (4/e³)·S̄**.

(iv) For every θ with |supp u| ≤ d and z ∈ [0, 1), with s = √(cz):
A_{θ,z} := {g_θ > z} = {(a − s) + uᵀx > 0} ∪ {(−a − s) − uᵀx > 0} ∈ 𝒜.
(Enlarge supp u to a set T of size d; this uses d ≤ P.)

**Step 2 (relative deviation, countable class; proved here).** Let 𝒜₀ ⊆ 𝒜 be countable and nη² > 36. Then

  P(∃A ∈ 𝒜₀ : P(A) − P_n(A) > η√P(A)) ≤ 16·S(2n)·e^{−nη²/4}.

*Proof.* Let x′ be an independent ghost sample with empirical measure P′_n. Define
- Q := {∃A ∈ 𝒜₀ : P(A) − P_n(A) > η√P(A)},
- R := {∃A ∈ 𝒜₀ : P′_n(A) − P_n(A) > η√((P_n(A) + P′_n(A))/2)}.

Both are countable unions of measurable events.

*Symmetrisation.* Enumerate 𝒜₀ = {A_ℓ} and let Q_ℓ be the event that A_ℓ is the first witness, so Q = ⊔Q_ℓ.
- On Q_ℓ, p := P(A_ℓ) > P_n(A_ℓ) + η√p ≥ η√p, so p > η² and np > 36.
- By independence and Step 0, P(Q_ℓ ∩ {P′_n(A_ℓ) ≥ p}) ≥ P(Q_ℓ)/16.
- On that event write α = P_n(A_ℓ) and β = P′_n(A_ℓ) ≥ p > α. The map β ↦ (β − α)/√(α + β) is increasing (its derivative has the sign of 3α + β). So (β − α)/√((α + β)/2) ≥ (p − α)/√((α + p)/2) ≥ (p − α)/√p > η, i.e. R holds.
- Therefore P(R) ≥ P(Q)/16.

*Swapping.* The law of (x, x′) is invariant under exchanging x_i ↔ x′_i for i in any subset. So P(R) = E P_ε(R after the swaps coded by i.i.d. signs ε).
- Fix (x, x′) and A. Put c_i = 1_A(x′_i) − 1_A(x_i) and k_A = Σ_i(1_A(x_i) + 1_A(x′_i)).
- After swapping, P′_n − P_n = n⁻¹Σε_i c_i and P_n + P′_n = k_A/n, with Σc_i² ≤ k_A.
- If k_A = 0 the event is empty. Otherwise Hoeffding (cosh λ ≤ e^{λ²/2}) gives P_ε(Σε_i c_i > η√(nk_A/2)) ≤ exp(−η²nk_A/(4Σc_i²)) ≤ e^{−nη²/4}.
- The event depends on A only through its indicator vector on the 2n-tuple. A union over at most S(2n) vectors gives P(R) ≤ S(2n)e^{−nη²/4}. ∎

**Step 3 (conclusion).**
- The condition of Step 2 holds: log S̄ ≥ d + 2(d+1)log(2e) ≥ 1 + 4 log(2e) > 7.77 and log(4/δ) > 1.386, so nη² > 36.6.
- Let 𝒬 be the set of θ with rational a, rational c > 0, rational u, |supp u| ≤ d. Let 𝒜₀ := {A_{θ,z} : θ ∈ 𝒬, z ∈ ℚ ∩ [0, 1)}, which is countable and contained in 𝒜 by Step 1(iv).
- By Steps 1–2, outside an event of probability ≤ 16·(4/e³)·S̄·e^{−nη²/4} = (16/e³)δ < δ, we have P(A) − P_n(A) ≤ η√P(A) for all A ∈ 𝒜₀.

On that event:

(a) *All levels.* Fix θ ∈ 𝒬. For each x, z ↦ 1{g_θ(x) > z} is right-continuous. By monotone convergence, z ↦ P(A_{θ,z}) and z ↦ P_n(A_{θ,z}) are right-continuous. So the inequality extends from rational z to all z ∈ [0, 1).

(b) *Layer cake.* g_θ = ∫₀¹ 1{g_θ > z}dz. By Fubini and Cauchy–Schwarz,
Pg_θ − P_n g_θ = ∫₀¹ [P(A_{θ,z}) − P_n(A_{θ,z})]dz ≤ η∫₀¹ √P(A_{θ,z}) dz ≤ η√(Pg_θ) ≤ (Pg_θ + η²)/2.
Hence Pg_θ ≤ 2P_n g_θ + η².

(c) *All parameters.* For arbitrary θ take θ_k ∈ 𝒬 with θ_k → θ and supp u_k ⊆ supp u. Then g_{θ_k} → g_θ pointwise with values in [0, 1], so Pg_{θ_k} → Pg_θ and P_n g_{θ_k} → P_n g_θ, and the inequality passes to the limit.

So with probability ≥ 1 − δ, simultaneously for all a, c > 0 and u with |supp u| ≤ d: E g ≤ 2P_n g + η². This is the card's statement, and the event is measurable. ∎

## 3. Remarks

- **Constants.** The classical inequality is P(sup_A (P(A) − P_n(A))/√P(A) > η) ≤ 4Π(2n)e^{−nη²/4} (Anthony & Shawe-Taylor, *Discrete Appl. Math.* 47 (1993) 207–217, Thm 2.1). Its factor 4 comes from P(Bin(n, p) ≥ np) > 1/4 for p > 1/n (Greenberg & Mohri, *Statist. Probab. Lett.* 86 (2014) 91–98, Thm 1). I quote both from memory and did not check them against the sources. The proof above uses neither: it uses 1/16 from Step 0 and recovers the card's exact constants from the slack S(2n) ≤ (4/e³)S̄.
- **Hypotheses used.** d ≤ P, d ≤ n − 1, i.i.d. Borel law. Nothing else: no moments, no n ≥ 3, and atoms and repeated points are allowed (traces are counted on tuples).
- **Sharpness.** Attack C shows a remainder of order below d/n is impossible. Attack B shows a single function fails with probability at most e^{−nη²/2}. The lemma's remainder is therefore conservative by constants and logarithms, but not by its order in d/n.

ATTEMPT T/T-c RESULT=PROVED GAPS=0
