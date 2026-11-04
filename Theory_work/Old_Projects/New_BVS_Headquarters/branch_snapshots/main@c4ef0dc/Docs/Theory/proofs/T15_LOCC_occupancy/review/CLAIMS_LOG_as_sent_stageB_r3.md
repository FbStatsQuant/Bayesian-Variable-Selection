# CLAIMS_OF_FATAL_FLAWS — T15 (L-OCC)

## Fatal or gap findings

None. Six reviews so far, and none raised a fatal or gap finding:
- Astra #1, round 1, on PROOF_v1: verified; 1 exposition finding.
- Astra #1, round 2, on PROOF_v2: verified; no new findings.
- Stage B Astra #2, round 1, on PROOF_v2: verified; no findings.
- Stage B Opus 5.5 xhigh, round 1, on PROOF_v2: verified; 5 exposition findings.
- Stage B Astra #2, round 2, on PROOF_v3 + this log: verified; 2 exposition findings. Agrees that no fatal or gap finding is outstanding. Rulings: A1-1, O-1, O-2, O-3, O-5 resolved; O-4 partially resolved.
- Stage B Opus, round 2, on PROOF_v3 + this log: verified; 4 exposition findings. Agrees that no fatal or gap finding is outstanding. Rulings: O-1 to O-5 resolved.

## Exposition findings and the lead's answers (kept for the record)

| # | Reviewer | Finding (short) | Answer | Change |
|---|---|---|---|---|
| A1-1 | Astra #1 r1 | The (iv) example has W = 0 with probability 3/4, but actual island evidence is strictly positive. Heading scope needs care. | Accepted. | v2: example uses ε > 0; scope sentence added to (iv). |
| O-1 | Opus B r1 | (H-T12) gives the identity for every test function g, but the example checks only g ∈ {1, 1_{𝔄ᶜ}}. Opus suggested a populations-based extension. | Accepted; adopted as a strengthening. | v3: new (iv-b) realises the example with particle populations satisfying E[W q̂(g)] = π′(g) for all g, on any finite Ω′ (including the method's Ω, π) with π′(𝔄′ᶜ) = a. (iv) now holds for every a ∈ (0, cu/4]. |
| O-2 | Opus B r1 | Island i.i.d. given 𝓒 is presented as a method property, but it is not among the hypotheses. | Accepted. | v3: the claim about the method is removed; the example's i.i.d. property is described as only strengthening it. |
| O-3 | Opus B r1 | Z̄₀, d, m(∅), π₀ are undefined, and the positivity of Ẑ_r is asserted, not derived. | Accepted. | v3: the symbols are defined briefly with a pointer to 00_COMMON; positivity is derived from positive factors. The proof uses only W_r ≥ 0. |
| O-4 | Opus B r1 | The Scope remark misdescribes the hypothesis use of (iii) and (iv). | Accepted. | v3: the remark is rewritten part by part. |
| O-5 | Opus B r1 | (iv) refutes the pooled form of (i) without the min{1,·} and does not state that the min form is refuted too. | Accepted. | v3: the one-line step min{1,x} ≤ x is added to (iv-a) and its proof. |
| B2-1 | Astra #2 r2 = Opus r2 #1 | The i.i.d. justification in (iv-b) cites (W_r, U, V) and leaves out f_r. | Accepted (both reviewers raised it independently). | v4: the argument now uses the quadruples (W_r, f_r, U_r, V_r). |
| B2-2 | Astra #2 r2 = Opus r2 #2 | "Part (iii) does not use (H-T12)" holds only for its first claim; the "consequently" clause rests on (i)–(ii). | Accepted. | v4: the note in STATEMENT §2 and the proof's final remark separate the two claims. |
| B2-3 | Opus r2 #3 | (iv-b) gives the identity at one position, while "full identity" suggests all of 𝒯. | Accepted. | v4: "full identity" is replaced by "identity for every test function", plus a remark that reusing the population at every τ gives every position. |
| B2-4 | Opus r2 #4 | "The method's Ω and π" example needs some set of posterior mass exactly a. | Accepted. | v4: the example states when such a set exists (smallest atom, if #Ω ≥ 4/(cu)). |

Unified version after Stage B round 1: v3. After Stage B round 2 (wording only): STATEMENT.md (v4 bullet in §5) and proof/PROOF_v4.tex/.pdf. (i)–(iii) are unchanged in statement and proof since v1.
