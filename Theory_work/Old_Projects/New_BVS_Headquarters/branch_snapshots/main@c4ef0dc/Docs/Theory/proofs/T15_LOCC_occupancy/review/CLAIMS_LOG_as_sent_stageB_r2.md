# CLAIMS_OF_FATAL_FLAWS — T15 (L-OCC)

## Fatal or gap findings

None. Four reviews so far, and none raised a fatal or gap finding:
- Astra #1, round 1, on PROOF_v1: verified; 1 exposition finding.
- Astra #1, round 2, on PROOF_v2: verified; no new findings.
- Stage B Astra #2 on PROOF_v2: verified; no findings.
- Stage B Opus 5.5 xhigh on PROOF_v2: verified; 5 exposition findings.

## Exposition findings and the lead's answers (kept for the record)

| # | Reviewer | Finding (short) | Answer | Change |
|---|---|---|---|---|
| A1-1 | Astra #1 r1 | The (iv) example has W = 0 with probability 3/4, but actual island evidence is strictly positive. Heading scope needs care. | Accepted. | v2: example uses ε > 0; scope sentence added to (iv). |
| O-1 | Opus B r1 | (H-T12) gives the identity for every test function g, but the example checks only g ∈ {1, 1_{𝔄ᶜ}}. Opus suggested a populations-based extension. | Accepted; adopted as a strengthening. | v3: new (iv-b) realises the example with particle populations satisfying E[W q̂(g)] = π′(g) for all g, on any finite Ω′ (including the method's Ω, π) with π′(𝔄′ᶜ) = a. (iv) now holds for every a ∈ (0, cu/4]. |
| O-2 | Opus B r1 | Island i.i.d. given 𝓒 is presented as a method property, but it is not among the hypotheses. | Accepted. | v3: the claim about the method is removed; the example's i.i.d. property is described as only strengthening it. |
| O-3 | Opus B r1 | Z̄₀, d, m(∅), π₀ are undefined, and the positivity of Ẑ_r is asserted, not derived. | Accepted. | v3: the symbols are defined briefly with a pointer to 00_COMMON; positivity is derived from positive factors. The proof uses only W_r ≥ 0. |
| O-4 | Opus B r1 | The Scope remark misdescribes the hypothesis use of (iii) and (iv). | Accepted. | v3: the remark is rewritten part by part. |
| O-5 | Opus B r1 | (iv) refutes the pooled form of (i) without the min{1,·} and does not state that the min form is refuted too. | Accepted. | v3: the one-line step min{1,x} ≤ x is added to (iv-a) and its proof. |

Unified version after Stage B: STATEMENT.md (v3 bullet in §5) and proof/PROOF_v3.tex/.pdf. (i)–(iii) are unchanged in statement and proof.
