# CLAIMS_OF_FATAL_FLAWS — T09 (T7)

Every fatal or gap finding, verbatim, with the lead's answer.

## Stage A, Astra #1 (session 01a16420-941b-7872-810a-426ec03c2ee9), review of PROOF_v1, finding 1 (fatal)

> **Location:** STATEMENT.md, claim (v), final sentence; PROOF_v1.tex, Section 6, closing paragraph (line 199).
>
> **Severity:** fatal (the literal concluding claim is false).
>
> **Claim:** The statement asserts that no upper bound on the absolute gap "(equivalently, no lower bound on its mixing time) that tends to 0" can follow from the listed conditions. The parenthetical does not give an equivalent assertion: a mixing-time lower bound tending to zero is compatible with uniformly fast mixing and is available here.
>
> **Evidence:** Define the usual worst-case mixing time t_mix(1/4) = min{h ≥ 0 : sup_x ‖K_φ^h(x,·) − q_φ‖_TV ≤ 1/4}. Every permitted state space contains at least ∅ and {1}. Therefore sup_x ‖δ_x − q_φ‖_TV = 1 − min_x q_φ(x) ≥ ½, so t_mix(1/4) ≥ 1. In particular, t_mix(1/4) ≥ 1/n, a valid lower bound tending to zero, including on the constructed family satisfying all three conditions.
>
> The quoted original wording concerns an **exponentially large** mixing-time lower bound. The explicit family faithfully demonstrates that such a conclusion need not follow: its geometric TV bound gives a mixing time bounded independently of n. The final parenthetical, read literally, does not faithfully express that conclusion. This finding concerns the concluding statement, not the validity of the constructed family.

**Lead's answer: accepted and fixed.** The parenthetical was a mis-stated gloss in my reading of the informal clause (a gap upper bound tending to 0 corresponds to a mixing-time lower bound tending to infinity, not to 0). Changes:
- STATEMENT.md, reading of (v): the consequence now reads "the family has t_mix(K₁) ≤ 55 for every n ≥ n₀; so no upper bound on gap*(K_φ) that tends to 0, and no lower bound on t_mix(K_φ) that tends to infinity (in particular none exponentially large in n), can be derived from …", with t_mix defined. Recorded in the STATEMENT.md change log. The original wording, the hypotheses and the existence claim are unchanged.
- PROOF_v2, Section 6: the proposition now also states t_mix(K₁) ≤ 55, proved from (39/40)^55 < 1/4; the closing paragraph is rewritten to match.

(Finding 2 of the same review is exposition: the 0/0 form of the reverse proposal probability for a non-symmetric neighbour family. Fixed in PROOF_v2 by writing both proposal probabilities by cases.)

## Stage B (independent reviews of PROOF_v2)

- Astra #2 (session 01a16428-59e8-7843-847b-ceb1857aa7cb): no findings; verdict verified.
- Opus 5.5 xhigh reviewer: verdict verified; seven findings, all graded exposition (F1 "exposition (borderline gap)"). No fatal or gap finding, so no entry is required here. For the record, F1 is quoted verbatim with its answer, because it was graded borderline:

> **F1.** Location: Section 6, closing paragraph ("any such implication would fail on this family"); STATEMENT (v), the "Consequently…" sentence. Severity: exposition (borderline gap). Claim: The proof shows the family has ε₁ ≤ e^{−κn} and discrepancy range ≥ κn with κ = κ_b/2, where κ_b = ½log(1/(1−c²ρ²)) for fixed correlation c and ρ. In fact ε₁ ≍ 1/BF(b) ≍ e^{−κ_b n}. Take a would-be implication whose hypothesis fixes a rate, such as "ε_φ ≤ e^{−5n} ⇒ gap → 0". At the example values c = ½, ρ = 3/5 we get κ_b ≈ 0.047, so the family does not satisfy that hypothesis and does not refute the implication. Evidence: κ_b = ½log(1/0.91) ≈ 0.047. The STATEMENT's own wording ("there exist constants c > 0") reads "exponentially small" and "large range" existentially, and under that reading the sentence is proved. The stronger fixed-rate version is easy to repair, but the proof never states the repair: κ_b → ∞ as cρ ↑ 1, and every argument in Lemmas 10–12 and Propositions 13–14 holds for any fixed c, ρ ∈ (0,1).

**Lead's answer: accepted; added in PROOF_v3 as Remark "Any prescribed exponential rate"** (for any K₀ > 0 choose τ, ρ with κ₂ ≥ 2K₀; all arguments hold for fixed τ, ρ; gap ≥ 1/40 and t_mix ≤ 55 unchanged). The statement is unchanged (its existential reading was already proved). The other exposition findings F2–F7 are all accepted and fixed in PROOF_v3 (see review/STAGE_B_CHANGES_v2_to_v3.md).
