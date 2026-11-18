Manifest verify printed `verify: OK MANIFEST 87dfd9f8258f978affc44879ac3ae01633ff9e481ed65406161091af781c5296` (exit 0). All scratch work is under `.rc_tmp/measd_r6_opus/`. I edited no tracked file, committed nothing and started no subagents.

- **Claimed edits.** All 21 rows of the brief's table are at the stated file:line, and the four ABSENT strings are absent. The three ticket files match the brief: sha256 prefixes `08c1ed7f…` / `a17058df…` / `8f0a2164…`, and 194 / 206 / 96 lines.
- **The diff file is faithful.** I took the MEASD5 ticket from `d5bf5194` (hashes match `MANIFEST_MEASD5.txt`) and diffed it character by character against MEASD6. The only changed lines are `STATEMENT.md:190, 194`, `MEAS_D.md:3, 24, 42, 50` and `REPORT.md:203-205`. Each change is exactly one of the claimed edits.

# R6 council review (Opus seat): W3-SAMP:MEAS-D

## 1. Per-item table

| # | ACCEPT/REJECT | note |
|---|---|---|
| 1 (F7) | ACCEPT, with F8 | **Same phrase in four places.** `STATEMENT.md:190`, `MEAS_D.md:24`, `MEAS_D.md:50` and `REPORT.md:203` all carry R5's phrase, "that is a Borel function of (data, S, c) with a bound B_h that does not depend on the data". The registry copy writes "section 2" (E26).<br>**Step 6 (`MEAS_D.md:50`).** H_r(h) = (4N_e)⁻¹Σ h(S_{rqi}; 𝓒°) and π(h) = Σ_S π(S)h(S; 𝓒°) are compositions of three Borel things: an h that is Borel in (data, S, c); 𝓒°, which is Borel by Step 3; and S_{rqi}, which are coordinates of the island record and so Borel by Step 4. N_e is a coordinate of 𝓒°, giving a countable cell split. π(h) also needs π Borel, which Step 2 proves, but the parenthetical does not cite it (E31). Given that, \|·\| ≤ B_h·1_{𝒜°}Ẑ_r and the κ_n·B_h bounds hold.<br>**Step 5 (`MEAS_D.md:42`).** For MR, g(x, c, u) is built from Ẑ_{r,t}/Z_t (Z_t is Borel by Step 2), the populations (Step 4), h, and the localisation indicators (coordinates of c). It is Borel exactly when h is Borel in (data, S, c), so the display is correct for every such h.<br>**No premise added.** The phrase narrows the class, which is correction-only and weaker. R5's counterexample h_x = 1{x ∈ N} is now excluded.<br>**Residual (F8).** The statement's "Consequently" clause still covers "every identity or bound of §2", which includes MR and N1 for any h of the fixed-data class. Step 5 now proves it only for h that is Borel in (data, S, c). This needs a QUALIFIER. |
| 2 (inventory) | ACCEPT as to correctness; REJECT as to completeness (WORDING, E32) | **Rows checked.** `LT_theorem.md:26, 37`; `C_theorem.md:28, 47`; pip_plain; f_t at `C_theorem.md:37-40`. I checked each against proved text and each has B_h = 1.<br>**f_t.** It is Borel through d = log BF − Σ_b log r_b(S ∩ C_b) (`STATEMENT.md:24`; T12 §0: r_b(U) = BF(U)), with Δ_t read from the grid coordinates of 𝓒°. Its reason rests on Step 2, and Step 2 says d is "continuous" on a cell. That is false where the block partition changes inside a cell, though the Borel conclusion still holds by BLK-c (C1).<br>**Missing h.** I grepped `W3-SAMP/STATEMENT.md` and `lemmas/` for MR uses. One row is missing: o_j, the RB summand of p̂_r(j) (`STATEMENT.md:56-57`). MR-c uses it in its "in particular" clause (`STATEMENT.md:113`, `MR_identities.md:33`), and so does (C-iv)'s bias clause (`C_theorem.md:65`). o_j depends on the data through γ₁ = γ₀e^{d} = ϖ·BF, and it lies in [0, 1].<br>**Not a gap.** o_j has a Borel reason in proved text: BF is continuous on each cell (`MEAS_D.md:32`), ϖ depends only on (p, size of S), and the size-K branch depends only on S. `W3-READER` and `W3-DIST` contain no MR use with an h. |
| 3 E25 | ACCEPT (E30 optional precision) | `MEAS_D.md:50` says "at most P(𝒜°) ≤ 1 … exactly P(𝒜° ∩ {T ≥ t}) for (MR-a)". This is correct against `MR_identities.md:27-33` with E₀ = 𝒜° (r ≤ R′ = 4, `STATEMENT.md:30-31`). The localised (MR-b) weight has expectation P(𝒜° ∩ {s ≤ L + 4}) (`MR_identities.md:30`). That is still "at most P(𝒜°)", so the text is true, but singling out MR-a invites reading MR-b as exact. |
| 3 E26 | ACCEPT | `REPORT.md:203` reads "section 2" in both places. `ingest.py convert` on the scratch copy exits 0. It gives one record with lines [190, 192], status_source `lemmas/MEAS_D.md:3`, 12 depends_on items, none with spaces, and no "§" in the conclusion. |
| 3 E27 | ACCEPT | Each part of the new wording at `STATEMENT.md:194` is true against `T5_CAL/STATEMENT.md:47-52` and `T1_GW/STATEMENT.md:80-102`:<br>- statistical-state event ∩ {completed}: P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°) (GW-iv);<br>- potential event ∩ 𝒜: P(𝒜 ∩ A°) ≤ P(𝒜° ∩ A°), since 𝒜 ⊆ 𝒜°;<br>- calibration-time event ∩ 𝒜: P(𝒜 ∩ A) = P(𝒜 ∩ A°) (CAL-d).<br>The 𝒜 ∖ 𝒪 final-run case is no longer covered. "Not part of any claim" is kept, and the remark adds nothing to any claim. |
| 3 E28 | ACCEPT | `REPORT.md:204` adds `W3-SAMP:MR@stmt:MR-a,MR-b,MR-c` and `W1-N1:Thm-N1@stmt`. Both ids are rows of `Theory_work/INFRA/registry/claims.tsv`. Step 6 uses MR-a, MR-b and MR-c at h ≡ 1 for the weights, and (N1) for the H_r(h) identity. |
| 3 E29 | ACCEPT | `MEAS_D.md:3` names R1 to R6 with MEASD to MEASD6 and binds Sol to "the MEASD6 digest". The gates pointer at `REPORT.md:205` is `reviews/R6_council_opus.md`. |
| 4 | ACCEPT | **Claim span.** The span is :190-192, and the only change R5→R6 inside it is the F7 phrase. :192 is unchanged.<br>**Against main.** Lines 1-186 differ from `origin/main` (13be759b) only at `36c36`.<br>**Scope.** Still potential-only (last sentence of :190).<br>**Converter.** Exits 0 on the scratch copy.<br>**Bars.** `STATEMENT.md:188-194` has no \| or ‖. The block `REPORT.md:199-206` has 5 \|, all of them field separators.<br>**Steps.** Steps 1-4 (`MEAS_D.md:30-40`) are unchanged. Steps 5-6 change only by the claimed phrases. F4 and E9-E24 are unchanged. |

## 2. Verdict lines

`(F7) the integrability clause and Step 6 are PROVED, NO NEW PREMISE | residual: the "Consequently" clause (STATEMENT.md:190, MEAS_D.md:24, REPORT.md:203) still applies Lemma MR to every h of §2, but Step 5 (MEAS_D.md:42) now proves it only for h Borel in (data, S, c); exact text in F8 (QUALIFIER)`

`(inventory) RIGHT, NOT COMPLETE | no h lacks a Borel reason in proved text; missing row: o_j of the RB PIP (STATEMENT.md:56-57, :113; MR_identities.md:33; used at C_theorem.md:65), Borel by MEAS_D.md:32; exact row in E32 (WORDING)`

## 3. Findings

**What I hold: QUALIFIER (F8, C1) and WORDING (E30, E31, E32) only. I hold no GENUINE GAP.** Each item below gives the exact text, to be applied as written.

**F8: the "Consequently" clause still quantifies over all h (QUALIFIER, apply as written).**
- **Problem.** At `STATEMENT.md:190` / `MEAS_D.md:24`, "every identity or bound of §2 about island r stated 'given 𝓒 on 𝒜' holds … conditionally on (data, 𝓒°)" includes Lemma MR (`STATEMENT.md:107-113`) for any family of fixed-data h. For a family that is not Borel in the data, the integrand is not a random variable. Step 5 (`MEAS_D.md:42`) proves the transfer only "when h is Borel in (data, S, c)". The statement therefore says more than the proof. Every consumer h is Borel (item 2), so nothing downstream changes.
- **Text for `STATEMENT.md:190` and `MEAS_D.md:24`** (the same replacement; it occurs once in each file):
  - Old: `stated "given 𝓒 on 𝒜" holds, for the potential pair`
  - New: `stated "given 𝓒 on 𝒜" (for Lemma MR, with h as in the preceding sentence) holds, for the potential pair`
- **Text for `REPORT.md:203`:**
  - Old: `every fixed-data given-C-on-A statement of section 2 about island r holds conditionally on (data, C0)`
  - New: `every fixed-data given-C-on-A statement of section 2 about island r (for Lemma MR, with h as in the preceding clause) holds conditionally on (data, C0)`
- **PURE check.** It is correction-only and weaker (it narrows the claim to the class Step 5 proves). No premise is added, the span stays :190-192, and no line numbers move. I applied it to a scratch copy: the converter exits 0, lines [190, 192], 12 depends_on items, and the file has no bars.

**C1: Step 2 says "continuous" where the block partition varies (QUALIFIER, apply as written).** `MEAS_D.md:32`.
- **Problem.** γ₀(S) = ϖ(S)Π_b r_b(S ∩ C_b) (T12 §0). The same holds for d, Z̄₀ and π₀: they read C(X), which can change inside a cell (`T2_BLK/STATEMENT.md:32-36`, BLK-c). So they are continuous only on each level set of the partition. The comparisons behind {S̃₀ = S} have the same issue. The conclusion of Step 2, "All of these are Borel", still holds, because C(X) is finite-valued with Borel level sets (BLK-c, already in depends_on as `W3-AUDIT-A:BLK@stmt`). f_t's row in the inventory rests on this sentence.
- **Text:**
  - Old: `and d(S) are continuous, and so are the finite sums Z, Z̄₀ and the ratios π, π₀.`
  - New: `and d(S) are continuous, and so are the finite sums Z, Z̄₀ and the ratios π, π₀; for γ₀, d, Z̄₀ and π₀, which read the block partition, and for the comparisons below that involve them, "continuous" means continuous on each of the finitely many Borel subsets of the cell on which the block partition is constant (`W3-AUDIT-A:BLK` (BLK-c): the partition map is finite-valued with Borel level sets).`
- **PURE check.** This is proof text only. The statement is untouched, the conclusion of Step 2 is unchanged, the lemma it cites is already a dependency, and no premise is added.

**E30: exact weight expectations (WORDING, apply as written).** `MEAS_D.md:50`.
- Old: ``(exactly P(𝒜° ∩ {T ≥ t}) for (MR-a), in its localised form, `MR_identities.md:27`;``
- New: ``(exactly P(𝒜° ∩ {T ≥ t}) for (MR-a), P(𝒜° ∩ {s ≤ L + 4}) for (MR-b) and P(𝒜°) for (MR-c), in their localised forms, `MR_identities.md:27-33`;``
- **PURE check.** Proof wording only. The "at most P(𝒜°)" bound is unchanged.

**E31: cite Step 2 for π (WORDING, apply as written).** `MEAS_D.md:50`.
- Old: `𝓒° is Borel by Step 3, and the S_{rqi}`
- New: `𝓒° is Borel by Step 3, π is Borel by Step 2, and the S_{rqi}`
- **PURE check.** Proof wording only. It cites an existing step.

**E32: complete the inventory (WORDING, apply as written; `H_CLAUSE_INVENTORY.md` is not hashed).**
- **Add this row** after the f_t row:

  `| (C-iv) bias and MR-c "in particular" (\`STATEMENT.md:113\`, \`lemmas/MR_identities.md:33\`, used at \`lemmas/C_theorem.md:65\`) | o_j(S) = γ₁(S∪j)/(γ₁(S∪j) + γ₁(S∖j)), and 0 if j ∉ S and S has K elements (\`STATEMENT.md:56-57\`), the RB summand of p̂_r(j) | **depends on the data through γ₁.** γ₁ = γ₀e^{d} = ϖ·BF (T12 §0), with ϖ a function of p and the size of S and BF continuous in the data on each cell (\`lemmas/MEAS_D.md:32\`); the size-K branch is a function of S; constant in c. So o_j is Borel in (data, S, c). | 1 |`
- **Replace** in the Result paragraph:
  - Old: `(the functions of S alone are trivial; f_t by MEAS-D Step 2 and CAL-c)`
  - New: `(the functions of S alone are trivial; f_t by MEAS-D Step 2 and CAL-c; o_j by MEAS-D Step 2)`
- **Replace:**
  - Old: `and R5's list is now complete.`
  - New: `and the list is complete with the o_j row added in R6.`
- **PURE check.** This changes a process record only. No ticket file and no claim changes.

**Summary.** F7's phrase is correct and proved. It leaves one adjacent over-claim, the "Consequently" clause (F8), which a qualifier fixes. Step 2's continuity wording (C1) is a pre-existing misstatement whose Borel conclusion holds by BLK-c. The inventory is missing o_j, which has a Borel reason in proved text. No step fails and no h lacks a Borel reason, so there is no GENUINE GAP.

## 4. Gates

- **G1 correctness: PASS, on the condition that F8 and C1 are applied as written.** With them, every step holds for every h the clauses cover. Without F8, the "Consequently" clause over-claims for families of h that are not Borel in the data. Without C1, Step 2's "continuous" is literally false, though its Borel conclusion holds.
- **G3 faithfulness and scope: PASS.** The scope is potential-only and no premise is added. E27 is now true and the remark is part of no claim. F8 only narrows.
- **G4 statuses and pins: PASS.** I checked these pins:
  - `MR_identities.md:25-33`
  - `L1_bridge.md:14-17`
  - `T1_GW/STATEMENT.md:80-102`
  - `T5_CAL/STATEMENT.md:47-52`
  - `T2_BLK/STATEMENT.md:32-36, 49-53`
  - `C_theorem.md:28, 37-40, 47, 65`
  - `LT_theorem.md:26, 37`
  - `W1-N1/STATEMENT.md:51-66`
  - T12 §0

  The E29 pointers are current.
- **G5 registration form: PASS.** The converter exits 0 (and also exits 0 with F8 applied). The span is 190-192, there are 12 depends_on items with no spaces, there is no "§", and there are no absolute-value bars.

gates=PASS. The only condition is that F8, C1 and E30-E32 are applied as written.

## 5. Score

**9.2.** F8 and C1 are each a one-phrase qualifier, and neither affects any consumer. I hold no S finding and no GENUINE GAP.

## 6. Claim table

| id | decision |
|---|---|
| W3-SAMP:MEAS-D | ACCEPT |

COUNCIL-VERDICT round=R6 manifest=87dfd9f8258f978affc44879ac3ae01633ff9e481ed65406161091af781c5296 seat=opus score=9.2 gates=PASS
