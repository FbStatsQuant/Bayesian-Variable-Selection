# Change report for the statement checker — T10 (old T11)

Lead's decision at step 1: **(a) correct as stated.** No hypothesis is added or removed; no conclusion is weakened. The theorem file contains four informal clauses; STATEMENT.md gives each a precise mathematical reading. I ask you to check that each reading is faithful to the original wording (neither stronger nor weaker in substance), and that the formal setting (definitions, quantifiers) matches the theorem file and 00_COMMON.md.

## Readings to check

1. **(ii), last sentence.** Original: "The unconditional one-addition bound carries the ordering factor 1/m; the v2 clause 'no ordering constant for a = 1' is false."
   Reading: the first half is the a = 1 case of (ii) (P(visit S+j) ≥ h_k/m). The second half (ii-neg) is an existence statement: there are admissible data, S (|S| = k < K), j ∉ S and φ ∈ [0,1] with P(visit S+j during the round | X₀ = S) < h_k. The lead reads the "v2 clause" as the inequality P(visit S+j | S) ≥ h_k without any ordering constant, since the theorem file defines no other form of it. Admissible data = any raw data satisfying 00_COMMON §1 (no statistical assumption); the lead intends to use a p = 2 instance (on which the production method would take the exact branch; the clause is about the round kernel, which is defined for every admissible data set).

2. **(iii).** Original: "At an actual execution of coordinate j with current state S, conditional on the whole past, the addition probability is o_j(S, φ) ≥ h_k; the expected number of such entries is Σ_e P(X_{e⁻} = S)o_j(S, φ_e) ≥ h_kΣ_e P(X_{e⁻} = S)."
   Reading: a filtration formulation over all elementary steps of a run; (iii-a) the conditional addition probability given 𝓕_{e⁻}; (iii-b) E N_j(S) = Σ_e E[1{λ_e = Gibbs j, X_{e⁻} = S} o_j(S, φ_e)] ≥ h_k Σ_e P(λ_e = Gibbs j, X_{e⁻} = S). Reason: in the pilot φ_e is adaptive (random), so "P(X_{e⁻} = S)o_j(S, φ_e)" is not a number; the expectation form is the correct general version and equals the original display when φ_e is non-random (e.g. the final run given 𝓒). The sum "over e" is read as over executions of coordinate j (the indicator of the label is included).

3. **(iv), first sentence and "not terminal-occupancy".** Reading (iv-a): an explicit instance where P(X_m = S+j | X₀ = S) < C(m,1)⁻¹h_k, with the ratio → 0 along a sequence of data sets. The lead reads "not terminal-occupancy statements" as "the visit bound does not transfer to end-of-round occupancy", which is a claim that requires a counterexample to be meaningful.

4. **(iv), second and third sentences.** Reading (iv-b): an explicit inverse-polynomial lower bound a!(16p²√(n+1))^{−a} for the (ii) bound when p ≤ n^A, a fixed. Reading (iv-c): "does not establish discovery within the declared budget" made precise as: with a = 1, k fixed, p = n, the (ii) lower bound summed over all final-run particle-rounds (budget of 00_COMMON §2) tends to 0; so (ii)–(iii) alone give no discovery guarantee. The theorem asserts nothing about discovery.

5. **(iv), last sentence.** Reading (iv-d): for |S| = K, j ∉ S: S+j ∉ Ω, γ_φ(S+j) = 0, o_j(S, φ) = 0; (i)–(iii) are asserted only for k < K (and k + a ≤ K in (ii)).

## Other formal choices

- "Visit during the round" = X_i = S′ for some i ∈ {0, …, m} (start included; irrelevant for a ≥ 1).
- (ii) also states that the bound is a lower bound for the specific event "the first a labels are the Gibbs labels of J and each adds" — this is the parenthesis of the original.
- Assumptions: EX-A, EX-S only. The theorem file says "SR only when a Gibbs evaluation is translated into a scoring event (via T11)"; T10 makes no scoring statement, so SR is not used.
- Cited result: T09(ii) (wave 1), for the Gibbs kernel formula and the zero addition probability at the cap.
