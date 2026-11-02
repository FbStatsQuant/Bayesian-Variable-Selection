# Stage B — Opus 5.5 (xhigh) review, round 1

Launched via T3 delegate_task on Claude Personal (provider claudeAgent, model claude-opus-5-5, effort xhigh), clientRequestId T15-stageB-opus-personal-r1, 2026-10-22. Packet review_B_opus: STATEMENT.md (v2), PROOF_v2.tex/.pdf, REPORT_FORMAT.md. (An earlier launch on Claude Work, T15-stageB-opus-r1, was cancelled unfinished; it produced no report.)

Reply, verbatim:

---

I checked every step of PROOF_v2.tex and re-derived all of the arithmetic in (iv). PROOF_v2.pdf has the same content as the .tex.

**Checks**
- **(i)** The pointwise bound f·1{W≥c} ≤ fW/c holds because W, f ≥ 0. Together with f·1{W<c} ≤ 1{W<c}, the identity E[Wf] = π(𝔄ᶜ), and E f ≤ 1, this gives exactly (i) for every c ∈ (0,1).
- **(ii)** On {f>u} ∩ {W≥c} we have fW ≥ fc > uc, so this event lies inside {fW ≥ cu}. Markov's inequality and the union bound then give exactly (ii).
- **(iii)** On {W<c} we have |W−1| ≥ 1−W > 1−c > 0. Markov's inequality gives B/(1−c), and substituting this into (i) and (ii) is valid.
- **(iv) constants:**
  - ε = ½·min{c, 4(1−c)/3, cu/3} ≤ cu/6 < 1/6, so h = 4 − 3ε ∈ (7/2, 4).
  - 3ε/4 ≤ cu/8 < cu/4 = a, so b > 0. Also b < a/h < a/3 < 1/12.
  - ε ≤ c/2 < c.
  - h/4 = 1 − 3ε/4 ≥ 1 − (1−c)/2 = (1+c)/2 > c.
- **(iv) law and moments:** the three probabilities are positive and sum to 1. E W = 3ε/4 + h/4 = 1, and E[Wf] = 3ε/4 + hb = a.
- **(iv) pooled tail:** with K ~ Bin(4, 1/4) counting islands at h, K ≥ 1 gives W̄ ≥ h/4 > c, and K = 0 gives W̄ = ε < c. So P(W̄<c) = 81/256.
- **(iv) final comparison:** E f₁ = P(f₁>u) = 3/4 + b > 192/256. On the right-hand side, a/c + 81/256 < 145/256 and a/(cu) + 81/256 = 145/256. Both strict inequalities hold. W_r > 0, f_r ∈ {0,1}, a = cu/4 ∈ (0,1), and the four pairs are i.i.d.
- **Remark 1:** the islandwise bounds hold in the example, using b < cu/12 < u/4.
- **Hypotheses:** parts (i)–(iii) use only (H-T12) with f = 1_{𝔄ᶜ}, W ≥ 0, 0 ≤ f ≤ 1, and Markov's inequality. Part (iii) also uses its own stated assumption. EXP and EXP′ are not used.

**Findings**

1. **Location:** STATEMENT.md §3(iv), the parenthetical "the properties that (H-T12) gives with a = π(𝔄ᶜ)"; PROOF §6.
   **Severity:** exposition.
   **Claim:** (H-T12) gives the identity E_𝓒[Ẑ_r q̂_{r,τ}(g)] = Zπ(g) for *every* bounded g fixed given 𝓒, not only for g = 1 and g = 1_{𝔄ᶜ}. The example is checked only against these two instances. The precise form of (iv) lists only those properties, so the stated claim is fully proved. The parenthetical, though, slightly overstates what "(H-T12) gives".
   **Evidence:** the example can be extended so that it satisfies the full identity, which would strengthen (iv). This extension is my own derivation and is not in the proof:
   - Take Ω with π(𝔄ᶜ) = a and any N.
   - Given (W, f), draw all N particle states i.i.d. from π restricted to 𝔄ᶜ and renormalised if f = 1, and from π restricted to 𝔄 and renormalised if f = 0.
   - Then E[W q̂(g)] = E[Wf]·π(g1_{𝔄ᶜ})/a + E[W(1−f)]·π(g1_𝔄)/(1−a) = π(g), because E[W(1−f)] = 1 − a.

   The author may wish either to say this or to reword the parenthetical as "the two instances of (H-T12) used".

2. **Location:** STATEMENT.md §3(iv), "together with conditional independence and identical distribution of the islands given 𝓒".
   **Severity:** exposition.
   **Claim:** The statement presents conditional i.i.d. of the four islands given 𝓒 as a property of the method. It is not among the hypotheses in §2 (EX-S mentions only "the method's stream separation"), and neither the statement nor the proof establishes it.
   **Evidence:** This does not affect the formal non-implication. Adding properties to a counterexample only strengthens it, and the proof verifies that the example pairs are i.i.d. But as written, the parenthetical asserts a fact about the method that rests on the method file, not on anything in this folder.

3. **Location:** STATEMENT.md §1, "Island evidence".
   **Severity:** exposition.
   **Claim:** The symbols Z̄₀, d(S), m(∅) and π₀ are not defined in STATEMENT.md. The finiteness and strict positivity of Ẑ_r are asserted ("Under EX-A …"), not derived.
   **Evidence:** Parts (i)–(iii) need only that W_r is a nonnegative random variable, and part (iv) is abstract. So nothing in the proof depends on these definitions, but the setting is not self-contained on this point.

4. **Location:** PROOF, Remark 2 (Scope), "No property of the final run beyond (H-T12) and 0 ≤ f_r ≤ 1, W_r ≥ 0 is used".
   **Severity:** exposition.
   **Claim:** The wording is slightly imprecise:
   - Part (iii) also uses its own hypothesis E_𝓒|W_r − 1| ≤ B, which also supplies the integrability of W_r.
   - Part (iii) itself does not use (H-T12) at all.
   - Part (iv) uses no property of the final run.

   **Evidence:** §5 of the proof uses only Markov's inequality applied to |W − 1|.

5. **Location:** STATEMENT.md §3(iv), first sentence ("The bounds (i)–(ii) with the pooled lower tail … do not follow"), against the precise form proved in PROOF §6.
   **Severity:** exposition.
   **Claim:** The pooled analogue of (i) contains min{1, ·}, but the precise form of (iv) and its proof refute only the form without the min. The step from one to the other is immediate and is not stated.
   **Evidence:** Since min{1, X} ≤ X, E f₁ > a/c + P(W̄<c) implies E f₁ > min{1, a/c + P(W̄<c)}. So the min form is also refuted.

No fatal findings and no gaps: every step of (i)–(iv) is correct and proves the conclusions exactly as stated in STATEMENT.md, using only the hypotheses in its §2 and elementary probability.

Verdict: verified
