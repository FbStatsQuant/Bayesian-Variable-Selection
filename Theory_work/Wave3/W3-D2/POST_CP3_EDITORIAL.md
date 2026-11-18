# W3-D2 — post-CP3 editorial batch (2026-11-17; for the chapter transcription / one editorial version bump)

Sources: HQ API blind audit `Theory_work/Wave3/API_AUDIT/auditD2_results/auditD2-s1.md`, `auditD2-s2.md` (main; FINDINGS=0 on
both claims in both samples; MINOR only), council D1 seat note, the API card README. **Not applied** (hashed spans and the
frozen manifest stay as checked). The one in-span item about α*, β* was applied as a form fix (STATEMENT v1.5 §2, changelog;
check `reviews/F1_formcheck_opus.md`) and is not listed here.

| # | where | item | source | in a registered span? |
|---|---|---|---|---|
| 1 | STATEMENT.md:62, PROOF.md:9, 15-16 | "for every data set" → "for every data set on which π is defined (y^r and every column non-constant; almost surely under §0)" | s1-1, s2-1 | yes (§3, :60-64) — batch |
| 2 | STATEMENT.md:63, PROOF.md:15 | [MISR] :118-119 sits under "Consequences, for the same n and κ"; cite it as the same deterministic inequality, proved directly in P0.1 | s1-2 | yes (§3) — batch |
| 3 | PROOF.md:49-52 | say the master is applied where its own k_n is defined (s ≤ K), so 3 ≤ n < 2s₀ is outside its hypotheses by its statement; the appeal to G2's proof is then unnecessary | s1-3, s2-3 | no |
| 4 | STATEMENT.md:44, PROOF.md:47-48 | "C depending only on (s₀, A, M₀, c)" uses the choice c′ = c₀(s, A) + 1 on the → ∞ branch (G2_corr [R-3]); cite it in (E) | s1-4 | yes (§1 clause (E)) — batch |
| 5 | PROOF.md:39-40 | the master's floor formally includes T = ∅; say λ_min of an empty block is not used (vacuous) by the statement's convention, not only by G2's proof | s2-2 | no |
| 6 | PROOF.md:16 | "(σ² > 0, n ≥ 2)" → "n ≥ 3" | s1-6 | no |
| 7 | PROOF.md:94 (P5) | 2.1239 → 2.1234 (conservative slip) | s1-7, s2-5 | no |
| 8 | PROOF.md:22 | MISR-R `:51-54` → `:52-53` | s2-5 | no |
| 9 | STATEMENT.md:52 | RV `:263-270` → `:263-269` | s2-5 | yes (§2) — batch |
| 10 | PROOF.md:84 | "STATEMENT §7 caveat (b)" → "STATEMENT §4(b) and §7 caveat (b)" | s2-5 | no |
| 11 | PROOF.md:89 (P5) | `[R1] B2.1 (:38-40)` → `:36` | council D1 seat note | no |
| 12 | API_CARD.md:12-13 | dropped lines are PROOF :1, :3, :97 (see `reviews/API_CARD_README.md`) | manager | no |
| 13 | PROOF.md:62-64 | after the v1.5 form fix, P3's "read as non-random" can cite STATEMENT §2 directly | lead | no |
