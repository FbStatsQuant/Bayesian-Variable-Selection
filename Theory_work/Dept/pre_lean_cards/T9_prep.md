# T9 preparation note (HELD: not the T9 card)

Input so far: walk `walks/T9_rest.md` on walkD b5a87cd2 (rows 3.5 and 4.1; 2 MINOR, 2 NOTE). Still to come: `walks/T9_Thm10.md` (walkB), T9's Astra review and the blind Sol read. Rulings are provisional until those are in.

## Provisional rulings on `T9_rest.md`

| Row | Provisional ruling | Kind of fix |
|---|---|---|
| **F1 (MINOR):** PoolZ's proof cites only `W1-N1:Thm-N1`, stated for the frozen v2.2.1 core | AGREE | **CITATION-ONLY (approved by HQ).** Insert after the first sentence of PoolZ's proof: "(N1 is stated for the frozen v2.2.1 core. For the core of record the same identity is `W3-SAMP:MR` (MR-b) with h ≡ 1, `W3-SAMP/STATEMENT.md:107-110`; N1's code bridge is carried to main's island by `W3-SAMP:CC`, `lemmas/CC_code_check.md:9-21`.)" Recorder: add `W3-SAMP:MR@stmt:MR-b` and `W3-SAMP:CC` to PoolZ's depends_on. |
| **F2 (MINOR):** PoolZ's joint-law clause uses measurability of the records in the data | AGREE | **Proved, not assumed (HQ steer): the lemma below. No premise is added anywhere.** |
| **F3 (NOTE):** "printed evidence" should name the field | AGREE | Card wording. `CLAIMS_CARD.md:76`: "equals the printed evidence" → "equals $\exp$ of the printed field `log_Z` (not `log_Z_list`, row 3.1L)". `:97`: "(equal to the printed evidence on completed runs" → "(equal to $\exp$(`log_Z`), the printed pooled evidence, on completed runs". |
| **F4 (NOTE, Lean):** N1's premises are hypotheses in Lean | AGREE | None. |

## F2: draft of the measurability lemma

**Result of the feasibility check: the proof is short and standard.** It is an assembly of two recorded code-reading lemmas plus continuity of the closed-form scores. There is no supremum over an uncountable set and no non-Borel tie rule: every tie rule in the code is a fixed finite chain of comparisons (score, then size, then lexicographic order).

### Statement (one sentence for W3-SAMP's "Two probability levels" paragraph, `STATEMENT.md:28-36`)

> **(MEAS-D) Joint measurability.** Fix n, p_raw and the options. On the Borel set of valid inputs, the potential calibration record 𝒞°, the four potential island records, the potential final-run ledger and Z are Borel functions of (X^r, y^r, seed, U^{(0)}, …, U^{(13)}). Hence every event and random variable in the joint-law statements of this file is measurable, and each identity or bound "given 𝒞 on 𝒜" holds given (data, 𝒞) under the joint law (proof: `lemmas/MEASD.md`).

### Proof (draft for `lemmas/MEASD.md`)

1. **Domain.** Valid inputs form a Borel set. Split it by the set of non-constant columns: finitely many Borel cells, since {Cx_j = 0} is closed. On a cell, p is fixed.
2. **Data-only objects.** On a cell the standardised (X, y) is a continuous function of (X^r, y^r) (all sample SDs are positive). For each S, the entries of G_S and H_S are polynomials, H_S is positive definite, and Q_S = yᵀy − n·z_SᵀH_S⁻¹z_S is a rational function with nonvanishing denominator. So log m(S), F(S), the start weights, Z, π and π₀ are continuous, hence Borel. The block partition and the start mode are finite-valued and determined by finitely many comparisons (`W3-AUDIT-A:BLK`, `W3-AUDIT-A:TDP`), hence Borel.
3. **Calibration.** 𝒞° = Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) with Ψ Borel. This is recorded: `W3-AUDIT-A:CAL-C@1.0.3` (CAL-b), PROOF Step 3 (a computation of length bounded in (n, p); each step is arithmetic, exp, log or floor, or a branch on a comparison of Borel functions).
4. **Final islands and searches.** For fixed (T, N_e, L), island r's potential record is computed by a program of bounded length whose steps are Borel operations of (grid values, scores, uniforms) or branches on comparisons of such: `W1-N1` Lemma B (B-0), (B-b), (B-d), valid for the core of record by `W3-SAMP:CC`. The scores are Borel in the data by step 2. The final local search and LS0 read no uniforms and are the routine already covered in CAL-C Step 3, with bounded move caps. A finite composition of Borel maps and Borel-predicate branches is Borel, and the cells (retained set, T, N_e, L) are countably many Borel sets. So the island records and the ledger are jointly Borel in (data, calibration value, stream); composing with step 3 gives the statement.
5. **Use.** Under the joint law, U^{(9+r)} is independent of (data, U^{(0)}, …, U^{(9)}) (H-U/SI as idealised, `STATEMENT.md:35-36`). For bounded Borel g, E[g(data, 𝒞°, U^{(9+r)}) | data, 𝒞°] = ḡ(data, 𝒞°) with ḡ(x, c) = E g(x, c, U). This is N1's freezing lemma (`W1-N1/lemmas/L3_freezing.md`) with (data, 𝒞°) in the frozen slot, and ḡ(x, ·) is the fixed-data conditional expectation of N1.

**Standard facts used** (Mathlib names I verified in the pinned checkout): composition (`Measurable.comp`); continuous implies Borel (`Continuous.measurable`); comparison sets (`measurableSet_lt`, `measurableSet_le`); branches (`Measurable.ite`, `Measurable.piecewise`); floor (`Int.measurable_floor`); countably many cells (`Measurable.find`, `measurable_from_prod_countable_left`); pairing (`Measurable.prodMk`); the independence step (`condExp_indep_eq` with Fubini). I did not verify the names for exp and log; `Continuous.measurable` covers exp.

### Scope: what the lemma serves, so that no premise is added

- `W3-READER:PoolZ`, the "Consequently" clause (row 3.5 joint form, row 4.1).
- `W3-SAMP`: (D-iii), (D-iv), (LT-e), (LT-e′), (C-v), (TR-d), i.e. every clause marked "asymptotic" or "unconditionally" (`STATEMENT.md:102, 104, 136, 158, 170`).
- Theorem 10 (row 3.6), through those clauses. **To confirm against `walks/T9_Thm10.md` when I write the card.**
- `W3-DIST:DIST-C`'s P⊗ clauses that integrate W3-SAMP's conditional bounds ((C-ii)(α-disc), (α′)).

### Two points to verify before this goes into the card

- **Potential versus actual objects.** The lemma is about potential (uninterrupted) records. {completed} and the actual 𝒜 depend on the run-time guard, which is not a function of (data, seeds); `W3-AUDIT-A:CAL-C` already says W3-SAMP's conditional claims hold for the potential pair and that upper bounds transfer pathwise. I need to check in `W3-AUDIT-A:GW` how the guard's Boolean is placed in the probability space, so that the lemma's statement does not overreach.
- **What I rely on without re-reading code.** Steps 3 and 4 rest on the recorded code-reading lemmas (CAL-C, Lemma B, CC, BLK, TDP). I have not re-read the code for them. If any of those lemmas turns out not to cover a step (for example the final local search), I will say so and stop, as instructed.
