# Audit auditD2-s1: W3-D2 API card
claims: Thm2X, Cor2X
stop_reason: end_turn

**Findings**

No ERROR or GAP found in either registered claim. I checked the q = 0 instance of (N)/(OV), the identity of π, δ_n, HPM, k_n and ρ_n with the master's objects, the floor coverage via B4.1, the dependence of C, the probability terms, P0.1–P0.3, the Markov steps, the corollary's reduction and the quoted recorded statement. Only the following local slips remain.

1. **MINOR — STATEMENT.md:62 (vs PROOF.md:9, 15-16).** §3 asserts the three deterministic facts "for every data set". The posterior and its outputs are defined only when y^r is non-constant and all p columns are non-constant ([W3P] :18; [MISR] :23-24). P0 proves the facts only for such data sets and then notes they hold almost surely. That is enough for every expectation and probability in §1, but the §3 wording should read "for every data set on which π is defined".

2. **MINOR — STATEMENT.md:63 and PROOF.md:15.** The cited source line ([MISR] :118-119) sits under "Consequences, for the same n and κ", i.e. for κ in the class and n ≥ n₀. Citing it as an unconditional source is loose. Nothing depends on it, because P0.1 proves the inequality directly.

3. **MINOR — PROOF.md:49-52.** CorGb-plus is stated for a sequence satisfying its hypotheses, yet its floor hypothesis is not even defined for n < 2s₀ (k_n needs s ≤ K). The proof therefore applies the master through its proof (G2_corr steps 1–5 are checked n by n), not through its statement. This is sound, since every threshold in G2_corr:44 is a "for n ≥ …" threshold and n_BM uses only the liminf. But it is an appeal to the master's proof and should be flagged as such, or the master should be restated with "for all large n".

4. **MINOR — STATEMENT.md:44 and PROOF.md:47-48.** "C depending only on (s₀, A, M₀, c)" does not follow from the master's statement alone, which says only that the beta-min constant is "c > c₀(s, A) fixed by the beta-min branch" ([MISR-R] :106-107). It needs the choice c′ = c₀(s, A) + 1 on the L = ∞ branch from G2_corr [R-3] (:24). The proof does cite this, and the claim is correct.

5. **MINOR — STATEMENT.md:52-55 and PROOF.md:62-64.** The corollary's list of recorded hypotheses does not say that α*, β* are non-random; P3 supplies this as a reading of NOTATION.md:15-20. Theorem 2X (§0, :19) requires both deterministic. A random α* would be harmless (the master allows it), but a random β* is not covered. The corollary should state the reading explicitly.

6. **MINOR — PROOF.md:16.** "(σ² > 0, n ≥ 2)" while the setting is n ≥ 3. Harmless.

7. **MINOR — PROOF.md:94 (P5, a remark outside the registered spans).** The constant 2.1239 should be 2.1234 (2.7096 − 1.0986·0.5336). The slip is in the conservative direction, so the conclusion of P5 is unaffected.

AUDIT W3-D2:Thm2X FINDINGS=0
AUDIT W3-D2:Cor2X FINDINGS=0