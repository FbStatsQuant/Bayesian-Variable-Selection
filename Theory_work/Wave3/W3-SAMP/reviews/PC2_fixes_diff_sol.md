# PC2 — review of the three PC1 fixes (Sol)

2026-11-11. Reviewed `git diff -- Theory_work/Wave3/W3-SAMP` against PC1's Verdict, STATEMENT §0, LT Step 2(b), and ST. Read-only except for this output file; no git state changes or subagents. References below are relative to `Theory_work/Wave3/W3-SAMP/` and use the inspected working-tree line numbers.

## 1. LT Step 3: display the λ₀ intermediate bound

**RESOLVED.** `lemmas/LT_theorem.md:48` now states

P(Λ̄ ≥ ε | 𝓒) ≤ λ₀/ε ≤ 19·o₁/ε.

This is correct for ε > 0: Λ̄ is nonnegative, and Step 2(b) (`:28–32`) already establishes E[Λ̄ | 𝓒] ≤ λ₀ in the localised fixed-data sense. Conditional Markov gives the first inequality. ST-c (`lemmas/ST_stay.md:39–44`) defines λ₀ as the sum of elementary leave probabilities and proves λ₀ ≤ (B+3)o₁ ≤ 19o₁ for coded B ≤ 16. Together with LT's existing pathwise bound and event inclusion (`:21`, `:48–49`), this yields LT-b with λ₀/ε before relaxation.

The edit introduces no new theorem or assumption: STATEMENT already displays this exact-λ₀ LT-b. It respects §0: the bound is conditional on data and 𝓒, on 𝒜, and does not condition on 𝒜 or completion or assert their probabilities tend to one. It fully fixes PC1's propagation finding and makes LT's numerical paragraph (`:105–106`) accurate about what Step 3 displays.

## 2. REPORT conventions: joint-law idealisation

**RESOLVED.** `REPORT.md:40–42` explicitly carries STATEMENT §0's idealisation and identifies its use in D/LT/C/TR joint-law integrations. The parenthetical specifies the ideal stream law **given the data and pilot information**; the final sentence correctly prevents an interpretation based merely on separate marginal independence, which would not suffice to establish the required joint conditional law.

This is mathematically correct as an assumed ideal law, not a new conclusion about actual seeded PRNG outputs. It faithfully explains `STATEMENT.md:34–36` and PC1's stated interpretation of those lines. The adjoining conventions retain localisation to 𝒜 or completion and explicitly reject any assumption P(𝒜) → 1. No new mathematical claim or stronger success-probability premise is introduced. Stating the qualification in the report's conventions fully satisfies PC1's request; duplicating it in the assumptions list is unnecessary.

## 3. REPORT and C1 disposition: provenance corrections

**RESOLVED.** `REPORT.md:104` now identifies C1's scores as votes on the pre-edit text and PC1 as the subsequent verification of the substantive edits. `reviews/C1_disposition.md:10–12` immediately corrects the preceding inaccurate assertion, explicitly acknowledges substantive changes to PC, D and LT-b, and likewise separates the historical votes from PC1 verification.

These are documentary corrections, not mathematical assertions or changes to §0's probability law. Their account is supported by PC1's inventory and Verdict, which verify the substantive mathematics while declining to treat the two C1 votes as reviews of the final text. The bracketed correction expressly labels the preceding assertion inaccurate, so the retained historical wording supplies no surviving justification for an exemption from re-review. Neither correction claims a fresh council vote or retroactive council approval. Together they provide the missing provenance for REPORT's checked-status statement and fully resolve PC1's corresponding request.

## Verdict: RESOLVED

All three requested fixes are correct and complete within this diff's scope. The mathematical display now matches its proof and statement, the standalone report explicitly states the joint-law idealisation, and both provenance notes distinguish pre-edit council votes from subsequent PC1 verification. No new mathematical claim is introduced.
