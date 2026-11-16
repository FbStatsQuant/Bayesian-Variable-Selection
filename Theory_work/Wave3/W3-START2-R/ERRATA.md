# W3-START2-R — ERRATA (editorial findings; PROTOCOL_v4 §5.3: never blocking, applied later in one editorial batch)

Source reviews: council R1 seat sol (`reviews/R1_council_sol.md`, E #2–#4) and seat opus (`reviews/R1_council_opus.md`,
E #1–#10). None is applied in the frozen content; each is to be applied in the editorial batch (chapter transcription, or
one version bump with one "editorial only" diff check).

| # | source | location | erratum |
|---|---|---|---|
| 1 | sol E2; opus E9 | `READER_DELTA.md:12` | "(equivalently n^{−1/2}e^{C√log n})" → "(with the explicit parent envelope n^{−1/2}e^{C√log n}, which implies it)" |
| 2 | opus E9 | `READER_DELTA.md:41` | "in all cases 1 − π₀(S₀) ≥ ⅓(n + 1)^{−1/2} for every data set" → add "once n ≥ 2s₀ + 2" (s₀ < K, (T0)) |
| 3 | opus E10 | `READER_DELTA.md:82` | "Master: W3-START2-R:F3 and :F1" → "Master: W3-START2-R:F1 (its F3 and F1 clauses)" |
| 4 | sol E3; opus E6 | `REPORT.md:83` | "the predicted approach is like n^{−0.06}" → "the upper bound used in R5.2 decays like n^{−0.06+o(1)}, so it does not establish fast convergence on this grid" |
| 5 | sol E4; opus E3 | `STATEMENT.md:260-264`, `REPORT.md` §4 | add W3-START:ASM, W3-START:BR, W3-START:TRANSFER to the consumed list of §5 (consumed through BASE L5, L9, L8); quote the consumed claims' statuses verbatim in REPORT §4 (all "PROVED-CHECKED", ACTIVE per the opus seat's check of `claims.tsv`) |
| 6 | opus E4 | `REPORT.md` registry blocks VIS-c, EX, START-R; `DEPS.tsv` row S:EX | complete depends_on: VIS-c + W3-START:LEAK@stmt, W3-START:AGG@stmt; EX + W3-START2-R:BR@stmt; START-R + W3-START:BR@proof, W3-START:TRANSFER@proof, W3-START2:BR@proof; DEPS S:EX uses + S:F1-F3 |
| 7 | opus E5 | `REPORT.md:24-27`, `lemmas/R3_RATE.md:118` | derive the "honest reading" in one line from PARENT `STATEMENT.md:57-61` (𝔏⁰_n − 𝔏^♯_n = 15√(2/π)z_n/p and 𝔏^♯_n ≥ (p − s₀)/(4p)) instead of citing the triage file, which is outside the frozen content |
| 8 | opus E1 | `lemmas/R1_VIS.md:40-42` | "At every n with p < n^A … ask no more" → add "and n ≥ 256s₀²" |
| 9 | opus E2 | `STATEMENT.md:283` (row IF-START; same spirit row START-R) | "each rate is at most the old one" → "each rate is of the old form n^{−1/2}e^{C√log n} (for some C) or smaller" |
| 10 | opus E7 | `lemmas/R4_TRANSFER_COR.md:51-53` | add: the reading "Q = S₀ on 𝒳_n" also follows, since P(Q = S₀) ≥ P(X^r ∈ 𝒳_n) → 1 |
| 11 | opus E8 | `lemmas/R1_VIS.md:18-22`, `lemmas/R2_NEC.md:20-25`, `:125-129` | drop the stale "ISSUES FOR THE LEAD" notes; neutralise the workflow wording in R2.5 (N1) |
