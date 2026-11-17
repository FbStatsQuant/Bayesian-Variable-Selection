# Audit auditD2-s2: W3-D2 API card
claims: Thm2X, Cor2X
stop_reason: end_turn

**Findings**

No ERROR or GAP was found in either registered claim. The instance of the master with q = 0, the identification of δ_n, HPM and k_n, the bound 2C r_n + … ≤ 2b_n, the Markov steps, the P0 inequalities and the corollary's reduction all check out against the consumed statements. Only local slips remain.

1. **MINOR — STATEMENT.md:62 vs PROOF.md:9, 15-16.** §3 asserts the three facts "for every data set", but P0 proves them only for data sets with y^r non-constant. The posterior is also only defined when every column of X^r is non-constant. Both conditions hold almost surely under §0 (Σ_jj > 0, σ² > 0), and P2 uses the facts only inside expectations and probabilities, so no claim is affected. §3 should read "for every data set on which π is defined".

2. **MINOR — PROOF.md:39-40.** The master's floor hypothesis (MISR-R STATEMENT.md:102) is stated for every T ⊆ 𝒞 with |T| ≤ k_n, which formally includes T = ∅, while (A2) starts at |T| ≥ 1. The proof closes this partly by appeal to the master's proof (G2_corr.md step 2) rather than its statement. The statement-level argument is the fallback already given: λ_min of a 0 × 0 block is vacuous.

3. **MINOR — PROOF.md:49-52.** The master is stated for a sequence, and the proof justifies ignoring 3 ≤ n < 2s₀ by inspecting the master's proof. That inspection is unnecessary. The master's own k_n is undefined when s > K (W3P STATEMENT.md:37), so its floor hypothesis can only be read where s ≤ K. There, P1 verifies it for every n ≥ max(3, 2s₀), and the energy and beta-min hypotheses hold at every n ≥ 3.

4. **MINOR — PROOF.md:62-65 (Cor2X).** The reduction to §0 needs α* and β* deterministic, since Theorem 2X's §0 states this. The recorded text (NOTATION.md:15-19, READER_VERSIONS.md:28) does not say it explicitly; the proof imports it as a reading ("read as non-random"). This is the standard reading of a "Truth" parameter, and for α the master would cover a random intercept anyway (MISR-R STATEMENT.md:52-53). The corollary statement (STATEMENT.md:52-55) should list it as part of the recorded setting rather than leave it to the proof.

5. **MINOR — citation and arithmetic slips, no effect on any claim.**
   - PROOF.md:22 cites MISR-R `:51-54` for the random α; the text is at `:52-53`, as PROOF.md:65 and :80 cite it.
   - STATEMENT.md:52 cites RV `:263-270` for the hypotheses; they end at `:269`.
   - PROOF.md:84 refers to "STATEMENT §7 caveat (b)"; the supplied statement span has no §7, and the matching text is §4(b).
   - PROOF.md:94 has the constant 2.1239 where 2.7096 − 0.5862 = 2.1234. The slip is on the conservative side, and P5 is outside the registered spans.

AUDIT W3-D2:Thm2X FINDINGS=0
AUDIT W3-D2:Cor2X FINDINGS=0