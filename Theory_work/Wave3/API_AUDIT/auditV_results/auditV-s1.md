# Audit auditV-s1: Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD/REQ_V.md
claims: V:VIS-0, V:VIS-a, V:VIS-b, V:VIS-c, V:VIS-d, V:VIS-e, V:UNIF, V:SCOPE
stop_reason: end_turn

## V:SCOPE

**Problem.** The "Not claimed" bullet places track C's riboflavin-like D18 outside the lemma, as a design "whose local patterns are uncountable without a countable closure of 𝒩 … B may then have interior; no claim" (`STATEMENT.md:70-71`). By the design definition and the lemma's own (VIS-d)(i), D18 has finitely many local patterns, so it is covered and B has no interior.

**References and argument.**
- `C_PLAN.md:19` defines D18 as Σ_δ = 0.9R + 0.1I with R one fixed 4088 × 4088 sample correlation matrix. For p < 4088 it is a column subset of that matrix; for p > 4088 it is a "block-diagonal tiling of independent copies".
- Every labelled local matrix Σ_{n,V}, V = U ∪ S₀, |V| ≤ 15 + s₀, is therefore a direct sum of principal submatrices of one fixed matrix. Over all n, j, U (and any truth positions) there are finitely many such matrices.
- The floor holds: λ_min(Σ_δ) ≥ 0.1, so c_m ≥ 0.1 by interlacing (the table also reports pop λ_min = .1 at `RESULTS.md:48`).
- This is exactly the case "block-diagonal Σ_n with blocks from a fixed finite list of correlation matrices" of `STATEMENT.md:46-48`, proved at `PROOF.md:67-69`.
- Hence 𝒩 is finite and, by (VIS-c) (`STATEMENT.md:41-43`), B is a finite union of hyperplanes: closed, null, nowhere dense.
- So the lemma does make a claim for D18: any fixed ϑ ∉ B has the uniform margin a = c̲·dist(ϑ, B) > 0 (`STATEMENT.md:36-40`).

**Internal inconsistency.** The Remarks put D19 under (VIS-b) as "the FRED-QD-like tiles" (`PROOF.md:105`). D19 is built by the "same recipe" as D18 (`C_PLAN.md:20`). The two are treated oppositely.

**Consequence for the dossier comparison.** The dossier and track C record D18 as a population failure or "outside" (`TRACK_B.md:219-220, 233`; `RESULTS.md:48`, "pop ≈0"). Under the lemma this can only mean one of two things, and the texts establish neither:
- the specific ϑ lies exactly on one of finitely many hyperplanes (track C's searches "refute, never certify", `RESULTS.md:23-24`, and report ≈0, not 0); or
- D18 is inside with a small but n-uniform margin.

The stated reason for exclusion (uncountable patterns, B with interior) is false for D18 as defined.

The other design statements I checked hold. In particular, D14 spread lies on B: with ρ = 0.5, U = ∅ and j the second truth, Cov = −1.0 + 0.5·(1.4 + 1.8 − 1.2) = 0. The VSL1 example (`PROOF.md:92-95`) and the block-CS spread placement under (VIS-a) also check out.

AUDITV V:VIS-0 VERDICT=NO-FINDING
AUDITV V:VIS-a VERDICT=NO-FINDING
AUDITV V:VIS-b VERDICT=NO-FINDING
AUDITV V:VIS-c VERDICT=NO-FINDING
AUDITV V:VIS-d VERDICT=NO-FINDING
AUDITV V:VIS-e VERDICT=NO-FINDING
AUDITV V:UNIF VERDICT=NO-FINDING
AUDITV V:SCOPE VERDICT=REFUTED