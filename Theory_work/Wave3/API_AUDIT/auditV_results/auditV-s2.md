# Audit auditV-s2: Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD/REQ_V.md
claims: V:VIS-0, V:VIS-a, V:VIS-b, V:VIS-c, V:VIS-d, V:VIS-e, V:UNIF, V:SCOPE
stop_reason: end_turn

## V:SCOPE

**Problem.** The statement puts D18 outside the lemma because its closure 𝒩 would not be countable ("B may then have interior; no claim", `STATEMENT.md:70-71`). By the lemma's own (VIS-d)(i), D18 has finitely many local patterns, so 𝒩 is finite and B is a finite union of hyperplanes.

**Why D18 falls under (VIS-d)(i).**
- D18 is built from one fixed matrix: Σ_δ = 0.9R + 0.1I, with R the fixed 4088 × 4088 riboflavin correlation matrix. For p < 4088 it is a column subset; for p > 4088 it is a "block-diagonal tiling of independent copies" (`C_PLAN.md:19`).
- So for every n, every entry of Σ_n is either 0 (across copies) or an entry of the one fixed matrix Σ_δ.
- A labelled local matrix Σ_{n,V}, V = U ∪ S₀, |V| ≤ 15 + s₀ = 19, is fixed by three finite choices: the Σ_δ-column of each index (4088 options), which indices share a copy, and the labels. That is finitely many values over all n, j, U.
- This is exactly the hypothesis of (VIS-d)(i) and its first example, "block-diagonal Σ_n with blocks from a fixed finite list of correlation matrices" (`STATEMENT.md:46-48`, `PROOF.md:67-69`).
- The floor holds: Σ_δ ⪰ 0.1·I, so c_m ≥ 0.1 (the table gives pop λ_min = .1, `RESULTS.md:48`).

**Consequences.**
- By (VIS-c), B for D18 is closed, null and nowhere dense, with a computable minimum (`STATEMENT.md:41-43`). The reason given for excluding D18 is therefore false.
- The premise "local patterns are uncountable" (`STATEMENT.md:70`) cannot occur for any design sequence. Each 𝒩_n is finite because p is finite, so ∪_n 𝒩_n is always countable; only the closure can be uncountable.
- The treatment is inconsistent within the lemma's own texts. D19 is the "same recipe" (`C_PLAN.md:20`) and is listed as a (VIS-b) case (`PROOF.md:105`), while D18 is declared not covered.

**Conflict with the dossier.** With 𝒩 finite, only two cases are possible, and neither matches the texts.
- If ϑ ∉ B, then (VIS-b) certifies visibility for D18 with a uniform constant a = c̲·δ > 0. The dossier instead records D18 as a "concrete failure at the population level" and "outside" (`TRACK_B.md:218-220, 233`), and track C marks it OUT with "pop ≈0", not "pop 0" as for D14/D15 (`RESULTS.md:44-45, 48`).
- If ϑ lies exactly on one of the finitely many hyperplanes, D18 is a "ϑ on B" case like D14/D15 (`STATEMENT.md:68-69`). It is then not an "uncountable patterns / B with interior" case.

The texts do not say which case holds, but in both the D18 design statement (`STATEMENT.md:70-71`) contradicts (VIS-d)(i), and in the first case the lemma also contradicts the dossier.

The other design statements held up where I could check them. In particular D14 spread is on B: with ρ = 0.5, U = ∅ and the truth with θ = −1, Cov = −1 + 0.5·(1.4 + 1.8 − 1.2) = 0.

AUDITV V:VIS-0 VERDICT=NO-FINDING
AUDITV V:VIS-a VERDICT=NO-FINDING
AUDITV V:VIS-b VERDICT=NO-FINDING
AUDITV V:VIS-c VERDICT=NO-FINDING
AUDITV V:VIS-d VERDICT=NO-FINDING
AUDITV V:VIS-e VERDICT=NO-FINDING
AUDITV V:UNIF VERDICT=NO-FINDING
AUDITV V:SCOPE VERDICT=REFUTED