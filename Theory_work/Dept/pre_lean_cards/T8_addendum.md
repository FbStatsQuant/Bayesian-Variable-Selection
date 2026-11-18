# T8 addendum: Theorem 5 (`W3-START2-R:START-R`, `BR`, `W3-START:FLOOR`)

Input: walk `walks/T8_Thm5.md` on walkD b5a87cd2 (WALK COMPLETE to recorded inputs; 2 NOTEs, no FATAL, MAJOR or MINOR).

**Verdict:** no flaw in Theorem 5. No ruling in `T8.md` changes. This closes the gap I flagged there (Theorem 5 had no walk).

## 1. Rulings on the walk rows

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Fix |
|---|---|---|---|---|
| **F1 (NOTE):** START-R (i) is proved from Corollary L6.0′, which needs how the constants of START-F depend on ε; the registry row lists the dependency only at statement level | AGREE | Registry-edge precision and a Lean export; no mathematical gap (L6.0′ is proved) | No | Recorder: add the proof-level edge from `W3-START2-R:START-R` to `W3-START:START-F` (Proposition L5.2 with its explicit constants, Lemma L6.0, Corollary L6.0′). No text change. Lean: see item 3 below. |
| **F2 (NOTE):** the proof is three layers of "as before, with these lines replaced" (BASE L9, PARENT P4, R3_RATE) | AGREE | Lean note; the walker checked every substituted line | No | None. Lean: see item 2 below. |

## 2. Astra's Theorem 5 points

Both were already ruled in `T8.md`, and the walk re-confirms each independently:
- **T8-2** (`W3-START2-R/STATEMENT.md:237`, FLOOR needs s₀ < K): ruling unchanged, AGREE with the staged patch. Walk §1 re-derives FLOOR and uses exactly |S| < K and n ≥ 4.
- **T8-3** (`R3_RATE.md:87`, "=" should be "≤" on a probability-zero event): ruling unchanged. Walk §4 marks it as known and finds nothing else in that step.

There is no further Theorem 5 point in Astra's review.

## 3. What the walk leaves uncovered

By its own boundary note (§8), it did not open below their statements:
- BASE Proposition L5.2 (the fixed-design theorem START-F) and its chain (AGG, TK, LEAK, VIS, ASM);
- PARENT Lemma LEAK-0.

These are recorded inputs (PROVED-CHECKED). So in this pass the fixed-design start theorem itself has Astra's trail but no walk.

## 4. Lean readiness for Theorem 5 (ranked; replaces item 5 of `T8.md` §4; no item changes a statement)

1. **FLOOR first, at Level 1.** It is deterministic and shares its machinery with T1: the one-step determinant ratio, monotone Q, and the prior ratio (k+1)/(2p−1−k). It certifies "the exponent ½ cannot be improved" on its own.
   - Named axioms: none. Cost: small, once T1's lemmas exist.
2. **One parametrised statement each for L9.5 and L9.6** (walk F2): L9.5 with the shift bound d̄ as a parameter (it is used at two values), L9.6 with the number of reference sets as a parameter.
   - Gain: the three "replace these lines" layers collapse into one proof.
3. **Export Proposition L5.2, with its explicit constants, and Corollary L6.0′ as named lemmas** (walk F1).
   - Gain: START-R (i) follows directly at ε_n = 4/log n. The alternative, a diagonal choice of ε_n from the bare statement, is valid but awkward to formalise.
4. **START-R as "fixed-design bound on a design set, plus the probability of leaving it"**, the same pattern as T4 item 1 and T7 item 3.
   - Level-2 named axioms: Laurent–Massart χ² tails; covariance concentration for Gaussian rows (L9.1, L9.2); independence of the Gaussian regression innovation from the conditioning columns.
5. **The J-bounds (J0)–(J4) at Level 1** (one-dimensional Gaussian integrals), with Step 1's representation stated as "≤" (T8-3).
