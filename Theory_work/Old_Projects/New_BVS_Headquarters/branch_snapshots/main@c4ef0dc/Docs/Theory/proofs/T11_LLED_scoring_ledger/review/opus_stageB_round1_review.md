# Review of PROOF_v3.tex (T11(iii): the final run's iid π₀ draws)

**Reviewer:** B (Opus). **Inputs read:** STATEMENT.md, REPORT_FORMAT.md, PROOF_v3.tex, and PROOF_v3.pdf (4 pages). I checked the PDF against the .tex and the content is the same. PDF numbering: Lemmas 1–3, Remark 4, Proposition 5, Theorem 6, Remarks 7–8, Corollary 9. Line numbers below refer to PROOF_v3.tex. I ran no code.

## Step-by-step check

1. **Lemma 1 (reading lemma), lines 36–60.** Checked. For fixed ι, I ran the coupling induction in both directions:
   - If ι ∉ {ι_1,…,ι_{k−1}}, then ι'_1 = ι_1. Whenever ι'_j = ι_j ≠ ι, we get V'_j = U^{(ι)}_{ι_j} = U_{ι_j} = V_j, so ι'_{j+1} = ι_{j+1}.
   - The reverse direction is the same with the roles swapped.
   - Because indices never repeat, {ι_k = ι} forces ι ∉ {ι_1,…,ι_{k−1}}, and {ι'_k = ι} does the same for the primed indices. So the set identity E∩{ι_k=ι} = E'∩{ι'_k=ι} holds as two inclusions.
   - The right side is σ(U_κ: κ≠ι)-measurable. I is countable, so summing over ι is valid.
   - The induction then closes. Correct.
2. **Lemma 2 (fresh block), lines 65–77.** This is the standard decomposition over {τ=t}. Correct.
3. **Lemma 3 (sampler), lines 87–120.** Checked the algebra:
   - Because the blocks partition [p], c^{(J)}_k = Σ_{|S|=k} ∏_b r_b(S∩C_b).
   - Z̄₀ = W_K^{−1} Σ_{k≤K} w(k) c^{(J)}_k, so M = W_K Z̄₀.
   - c^{(b)}_k > 0 exactly when 0 ≤ k ≤ Σ_{b'≤b}|C_{b'}|. By induction this is a convolution of sequences that are positive on intervals.
   - The step (b) probabilities sum to 1 by the recursion.
   - On a path, the e_b(j_b) factors cancel and the c-ratios telescope to c^{(0)}_0 / c^{(J)}_k with c^{(0)}_0 = 1. The result is w(|S|)∏r_b / (W_K Z̄₀) = π₀(S).
   - Any path with k_0 ≠ 0 contains the factor c^{(0)}_{k_0} = 0. An inverse CDF evaluated at u ∈ (0,1) never selects a value of mass 0.

   Correct. The lemma is redundant given EX-A, as the proof itself says.
4. **Q_f arithmetic.** 4N_e + 4N_e(T+L+4) = 4N_e(T+L+5). Correct.
5. **Proposition 5, lines 139–167.**
   - With υ fixed, the run's reads form a reading scheme: f_1 is constant, each later index is a measurable function of the values read so far (Setting item 2), and indices are distinct because only not-yet-read values are read.
   - Padding with the unread values of stream 10 makes the sequence infinite without changing the run.
   - {τ_m = t} ∈ 𝓕_t because the run's state after t reads is a function of V_1..V_t, and operations do not overlap.
   - D_i for i < m is 𝓕_{τ_m}-measurable. On {τ_m = t}, D_i is a function of V_1..V_t, since τ_i + (2J+1) ≤ t.
   - Lemma 2 then gives the product formula, and the induction over m is correct.
6. **Theorem 6, lines 171–192.**
   - Υ (streams 0–9) and Ξ (streams 10–13) are independent by EX-S.
   - h is jointly measurable by item 2.
   - Freezing / Fubini gives E[h(Υ,Ξ) | Υ] = g(Υ).
   - g(υ) = (1−π₀(s*(υ)))^{Q_f(υ)} on Λ, by Proposition 5.
   - g(Υ) is σ(𝓒)-measurable by items 4–6, and σ(𝓒) ⊆ σ(Υ), so the tower property gives P(A | 𝓒) = 1_Λ (1−π₀(S*))^{Q_f}.
   - Restricting to Λ ∈ σ(𝓒) is valid.
   - The inequality uses 0 ≤ 1−x ≤ e^{−x} and the monotonicity of y ↦ y^{Q} on [0,∞).

   Correct.
7. **Remark 7 counterexample, lines 196–205.** P(N=1) = 1−x and P(N=2) = x. So E(1−x)^N = (1−x)² + x(1−x)² = (1−x)²(1+x) = (1−x)(1−x²) < 1−x for x ∈ (0,1). Correct.

## Findings

**F1**
- **Location:** Lemma 1 proof, line 47 (U_ι replaced by the constant 0), together with its use in Proposition 5, lines 147–150.
- **Severity:** exposition.
- **Claim:** The coupling evaluates the reading scheme at a point where one coordinate equals 0, which is outside the support (0,1) of the streams. So the lemma's hypothesis ("f_k : [0,1]^{k−1} → I, indices pairwise distinct for every realisation") must hold for the final run at inputs it is never actually given.
- **Evidence:** Setting item 2 only specifies the algorithm on stream values. The argument goes through unchanged with any constant c ∈ (0,1). Also, distinctness in the final run is a structural property ("not-yet-read") and does not depend on the values read. Correctness is not affected.

**F2**
- **Location:** Lemma 2, line 67 (definition of 𝓕_τ) and line 66 (V_{τ+j}).
- **Severity:** exposition.
- **Claim:** 𝓕_τ is defined without requiring A ∈ 𝓕, and (V_{τ+j}) is not defined on {τ = ∞}.
- **Evidence:** τ < ∞ a.s., so both points concern null sets only. No effect.

**F3**
- **Location:** Proposition 5, lines 155–156 ("finite because the run reads a.s. finitely many values before its m-th call (each primitive operation reads finitely many)").
- **Severity:** exposition. This is the justification of a correct step.
- **Claim:** "Each primitive operation reads finitely many values" is not a setting item.
- **Evidence:** The needed fact, τ_m < ∞ a.s., follows from item 5 instead. On Λ every particle completes T+L+4 rounds, so the m-th designated call does occur. Operations run one at a time (item 2), so a call that occurs is preceded by finitely many reads: an operation that read infinitely many values would never finish. So the step holds under the setting, but the reason cited is not the right one.

**F4**
- **Location:** Proposition 5, line 153 ("The run makes exactly Q_f sampler calls"). Also lines 141–142.
- **Severity:** exposition.
- **Claim:** Item 5 names which Q_f draws are "the final iid draws", but it does not say the final run makes no other π₀-sampler calls.
- **Evidence:** If other calls existed, "the final run's π₀ draws" would no longer be exactly D_1..D_{Q_f}. The argument is unaffected: index only the designated calls. Whether the next call is a designated one is decided by the state at its start, so {m-th designated call starts after read t} ∈ 𝓕_t and Lemma 2 still applies.

**F5**
- **Location:** Proposition 5, lines 157–159 (D_m = G((V_{τ_m+j})_{j≥1}) with a single map G). Also Setting item 3.
- **Severity:** exposition (implicit assumption, not load-bearing).
- **Claim:** The proof uses a stronger form of EX-A than item 3 states: every sampler call is the same fixed measurable map G of the consecutive values it reads, regardless of the run's state, and G applied to an iid Unif sequence has law π₀. Item 3 says only that a call "when it reads fresh values, returns a draw with law exactly π₀", and "fresh" is not defined.
- **Evidence:**
  - Lemma 3's sampler is such a fixed map of 2J+1 values, and it matches item 3's one-line description of METHODOLOGY §6.3. I cannot check that it matches §6.3 in full, because METHODOLOGY is not in the packet.
  - The conclusion survives even if the map depended on an 𝓕_{τ_m}-measurable state Z_m. Lemma 2 makes the fresh block independent of (Z_m, D_1..D_{m−1}), and EX-A gives law π₀ for each state.
  - So this is a wording issue, not a gap.

**F6**
- **Location:** Lemma 3 proof, line 110 ("A set S ∈ Ω is produced by exactly one path").
- **Severity:** exposition.
- **Claim:** Strictly, S is produced by exactly one *positive-probability* path.
- **Evidence:** Paths with Σ_b j_b ≠ k would need a mass-0 selection at some step. The preceding sentences already rule these out, so the computation stands.

**F7**
- **Location:** Remark 4, lines 124–132. Cited at line 153.
- **Severity:** exposition (not load-bearing; the main proof uses item 5 as stated). The remark's own inference **cannot be fully verified from the packet**.
- **Claim:** The remark argues that no status interrupts a launched final run. Two parts of that argument rest on things the packet cannot confirm:
  - It reads EX-A ("scores … are exact") as "every score computation succeeds". Whether a Cholesky or QR step could fail even in exact arithmetic (a singular system) depends on the score formula and prior, which are not in the packet. Item 1's "m(·) > 0 is the marginal likelihood", stated for all arguments, supports the reading.
  - The three quoted statuses are an excerpt. A runtime abort during the final run (time or memory) is not shown to be impossible. The quoted resource_limit is only a preflight prediction.
- **Evidence:** STATEMENT.md quotes only §2, §6.5, §6.13 and §7 fragments. Since Theorem 6 uses item 5 directly, this bears on whether item 5 is faithful (see the Setting section below), not on whether the derivation is valid.

**F8**
- **Location:** Corollary 9, lines 211–218. This is outside claim (iii).
- **Severity:** gap (in the corollary only; it does not affect the verdict on (iii)).
- **Claim:** The step "by Proposition 5 they [the proposals alone] are iid π₀ given Υ" does not follow from Proposition 5 as stated.
- **Evidence:**
  - Proposition 5 proves that the chronologically numbered D_1..D_{Q_f} are iid. The proposals are a sub-family whose positions in that order may depend on Ξ: item 2 lets the order of operations depend on the values read so far, for example through how the islands are interleaved.
  - A sub-family chosen with data-dependent positions is not iid in general. For example, with D_1, D_2 iid, choosing D_1 if D_1 = s and D_2 otherwise does not give a π₀-distributed result.
  - The corollary can be repaired by rerunning Proposition 5's stopping-time argument over proposal calls only. Whether a call is a proposal is decided at its start, so that event is 𝓕_{τ_m}-measurable. As written, though, the citation does not supply this.

No fatal findings.

## Setting: faithfulness and sufficiency

- **Sufficiency.** Items 1–6 suffice for the proof. The only implicit points it uses are F1 (value 0), F3 (finite reads) and F5 (a single map G). Each is avoidable or follows from the setting, so none is a real extra hypothesis. Of item 1, the proof needs only that π₀ is a probability on Ω with an exact sampler. Positivity of π₀ is not needed for the inequality, which holds for x ∈ [0,1].
- **Item 6 (S* is a measurable function of data and 𝓒) carries the result.** If S* were allowed to depend on the final run (for example, the best model the final run scores), the identity would generally fail. The original wording does not define S* inside the packet, and the source theorem file is not provided. So I **cannot verify** that item 6 faithfully renders the intended S*. It covers, and extends, the natural case where S* is fixed by the data.
- **Item 5 also carries the result.** It fixes the exact count Q_f, exactly one independence step per round, and no early exit of a launched run. It is a specification of the method, not one of EX-A, EX-S or CAL. STATEMENT.md says no item adds a hypothesis beyond those three. That is plausible from the quoted method facts plus EX-A (see F7), but the quotes are excerpts, so I **cannot fully verify** it. The Q_f formula is arithmetically consistent with item 5's description.
- **Item 2 (one operation at a time; sampler calls do not overlap) is an idealisation.** A parallel or vectorised implementation would not literally satisfy it. Because the islands use separate streams and all values are fresh, the joint law of the draws would be the same. The single reading-scheme construction in the proof does rely on this item as stated.
- **Items 1, 3, 4** are internally consistent with how the proof uses them. In particular, Λ ∈ σ(𝓒) and T, L, N_e are finite on Λ. Item 1's definitions (K, w, r_b) cannot be checked against 00_COMMON or METHODOLOGY, which are not in the packet. They are not load-bearing beyond the existence of π₀ and EX-A.
- **Scope clause.** "The adaptive calibration draw count is never a fixed exponent" is correctly read as a disclaimer, not a claim. Remark 7's counterexample is correct (algebra checked above). Remark 7's point (2), that given 𝓒 the calibration draws "need not be iid π₀", is stated without an example. It is hedged and outside the claim.

## Conclusion

The proof establishes claim (iii) of STATEMENT.md under Setting items 1–6. Every load-bearing step checks out: Lemmas 1–2, Proposition 5 and the conditioning argument in Theorem 6. The findings are exposition-level for the claim itself. There is one gap, in Corollary 9, which lies outside (iii). Remaining caveats concern faithfulness to sources not in the packet (items 5 and 6, and the completeness of Remark 4), not the derivation.

**VERDICT: verified**
