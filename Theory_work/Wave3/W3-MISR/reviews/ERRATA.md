# W3-MISR — ERRATA

## HQ 11-16, correctness event, Cor-H 2.1.0 (NARROW, correctness)

Entry copied verbatim from Theory_work/Wave3/W3-MISR-R/reviews/post_cp3/ERRATUM_W3-MISR_KL.md @93e50640 (W3-MISR-R lead). Applied: STATEMENT.md:191-195 narrowed (patch Theory_work/Dept/research/MISR_NARROW/STATEMENT_W3-MISR_v1.1.0.patch @d890acb5; Sol DIFF PASS, WEAKER, Theory_work/Dept/research/MISR_NARROW/DIFF_sol.md); registry W3-MISR:Cor-H NARROWED 2.0.0 -> cleared ACTIVE 2.1.0.

| field | value |
|---|---|
| id | ERR-W3-MISR-KL1 |
| ticket / claim | W3-MISR / W3-MISR:Cor-H@1.0.0 (interpretive sentence only; no displayed hypothesis or conclusion) |
| location | `Theory_work/Wave3/W3-MISR/STATEMENT.md:191-195`; its proof line `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:91-93` |
| kind | NARROW (an interpretive sentence is false on part of its stated scope; the registered conclusion field of Cor-H is unaffected) |
| defect | The row-wise reading "the conditional law of y_i given x_{𝒞,i} is N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞) … the Kullback–Leibler minimiser (SL's f₀)" is asserted "in the setting of Corollary G", whose response y^r = α1 + … does not make α deterministic and whose standing convention (`STATEMENT.md:38`) allows a random intercept. For a random α it is false. |
| counterexample | iid standard Gaussian candidate rows, independent N(0, 1) noise, α := (X^r_𝒞)²_{2,1}: Cor-G's hypotheses hold, but y_1 | x_{𝒞,1} is Gaussian plus an independent χ²₁ shift (W3-MISR-R `reviews/L1_statement_lock_sol.md` L1-1; `reviews/K1_linecheck_sol.md` K1-1). |
| correction (text) | `STATEMENT.md:191`: "**Kullback–Leibler reading, in the setting of Corollary G with a deterministic intercept α only:** there the conditional law of y_i …" (rest unchanged). `G_corollaries.md:91`: "In the setting of Corollary G with α deterministic, G.1 shows y_i \| x_{𝒞,i} ~ N(α + a + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞) independently over i; …". |
| effect downstream | None on registered conclusions. The reader row thm4 (`W3-READER/READER_VERSIONS.md:404-406`) uses the reading only with a fixed intercept (`:382-385`): unaffected (`W3-MISR-R/reviews/V11a_quote_check.md`). The corrected reading is the one carried by W3-MISR-R:CorH-plus (`W3-MISR-R/STATEMENT.md:128-130`). |
| evidence of check | counterexample reviewed by Sol at L1 (lock) and K1 (line check); the corrected deterministic-intercept reading passed council R3 in W3-MISR-R (sol=10.0, opus=9.6). |
| routing | parent folder is read-only (hashed); apply via HQ/W3-EDIT as an in-place erratum after acceptance, or carry in the chapter only. |

Proof-side copy: `lemmas/G_corollaries.md:91-93` has the same over-broad (random-intercept) reading; it is fixed in the post-freeze editorial batch (not edited now; the file is hashed by W3-MISR's manifests).

