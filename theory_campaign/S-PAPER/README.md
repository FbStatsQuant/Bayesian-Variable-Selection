# S-PAPER: theory section skeleton (JRSS-B)

Branch `theory/S-PAPER` (cut from `theory/campaign` @ `b8811e2`). Author: S-PAPER (Sonnet 5.5), 2026-11-02.
Deliverable: `theory_section.tex`, a self-contained `article` fragment (amsmath, amssymb, amsthm only).

**Nothing here is reviewed or adopted.** Every statement is a candidate. The status words are the campaign's and are never upgraded.
No proofs are included: each result says "Proof: see Supplement §S.x (source branch …)". The Supplement section numbers
S.1–S.9 are placeholders for the supplement the paper will have.

## Conventions in the `.tex`

- Every statement (definition, assumption, lemma, theorem, proposition, remark and each item of the disclosure list) is preceded by a comment line
  `% STATUS: <author status>; VERIFIED-BY: <branches>; SOURCE: <branch:file:label>`.
- `VERIFIED-BY: W…` is a same-family verifier (Claude checking Claude). `A-REV1`/`A-REV2` are the cross-family (GPT-6 Astra) reviews; their verdicts
  are quoted only for the items they cover. `none` = no verifier on the fetched branches.
- Numbering: Theorems 1–6 and Propositions 1–2 as in F-REFINE's paper map. Theorem 2 and Theorem 3 are stepped by hand and their parts are
  numbered 2(i)–2(v) and 3(i)–3(iv) (`thmpart` environment). The T02 size-tail results are Lemmas feeding Theorem 1.
- Where a source states a result with a hypothesis list, the hypotheses are copied (not paraphrased): Theorem 1 (W1-T03R §4, §6), Theorem 3(i) (W1-T37R Theorem A),
  3(ii) (W3-PGD Theorem W), Theorem 4 (W2-BOOK `STATEMENTS.tex`), Prop 2 (W2-BOOK `STATEMENTS.tex`), Theorem 6 (W2-T26 Theorem A).
  Where only F-REFINE's card is available (Theorem 2(i), 2(iii), 2(v); Theorem 5(b1-LH), (c)), the card's wording is used and the primary label is cited.

## Sources used, with head SHAs (fetched 2026-11-02)

| Branch | Head SHA | Files used | Used for |
|---|---|---|---|
| `theory/F-REFINE` | `db708ca9f98a616ea16c8ce8e950d8f65238835f` | `F-REFINE/CARDS.md`, `ARCHITECTURE.md` | skeleton, statements for Thm 2/3/5, story (ARCH §1), disclosure (ARCH §§6–7), data facts |
| `theory/W4-T38FULL` | `a0f9cb5e000dedf367e26fd0da019ccd2218fb42` | `T38_STATEMENT.md`, `T38_PROOF.md` (headers) | Theorem 5 (T38) with LS0; Lemma LS-score; Prop LH-LAT |
| `theory/W2-BOOK` | `57eb3d0f6699d76c0796e8b389415dacb182c231` | `STATEMENTS.tex`, `PROOF.md` | Prop 1 (T07), Prop 2 (T12+T31(i)), Theorem 4 (T21), Lemma RO, (d⁺) |
| `theory/W2-T26` | `0e4f1e7f5efd1e67330affa4168b69750eaff2f1` | `PROOF.md` | Theorem 6 (Theorem A, Lemma 1, Theorem B remark) |
| `theory/W1-T03R` | `7e14d6f090bef91861455f45c69017e2a5774198` | `PROOF.md` | Theorem 1 (T03♯), T02(i♯), T02(ii♯), hypotheses SE_λ, SE_w, BM |
| `theory/W2-VT03R` | `b9f6d9b8f6507dd1053d6b916d7a68e1f7b4aa5e` | `REPORT.md` | Lemma A1 (anchoring), R1 (proof thresholds 2.1e6), R2 (wording), Prop W, Prop D′ |
| `theory/W1-EXP` | `722bd18e51fcc3b485c07590097e137dac71a5aa` | `PROOF.md` | Theorem 2(ii)–(v): EXP′, Thms 2, 3, 4, 5, 6, LH family |
| `theory/W3-VEXP` | `7970fa0b00dd07c70d2670d17fcb44ba3748b52a` | via CARDS (REPORT/REPAIRS not re-read) | verification status of Thm 2; dilution Prop D |
| `theory/W1-T37R` | `3bcc42958f9d7373178ebab931f62ad38538c8f3` | `PROOF.md` | Theorem 3(i): Theorem A, Prop 1 (literal TD), Lemma 0, definitions |
| `theory/W3-VT37R` | `4988b966f2aafa9c61077e6002146297f0df0dd7` | `REPAIRS.md` | POS repair R1, R2 (Lemma 0(b) inference), R3 |
| `theory/W3-PGD` | `d8e98a8277340646634a2d6ddef1c3975019f9c0` | `PROOF.md` | Theorem 3(ii): Theorem W, LD♭, C-LD, P4 |
| `theory/W1-T24G` | `9e210a3fafbc074cfbbcae18dafc5c8547e81af1` | `PROOF.md` §4 | Theorem 3(iv): Theorem B |
| `theory/W2-VT24G` | `dba6ff4c12e0510c5a48bf733b1623834aa21c64` | via CARDS/A-REV1 | Lemma F′, B1′/B2′, (e′) edits |
| `theory/W2-PREM` | `988c5f55c0fb0fbd6050b6a4d0c75f14159716e3` | via CARDS/A-REV1 | IND-T, asymptotic premise table (Remark after Thm 3(iv)) |
| `theory/W1-T38E` | `436a7125ace4853eb9d2507513f53db9c47b3825` | via CARDS/A-REV1 | D2 route (b1′), E3 |
| `theory/W3-VT38E` | `3e4b732aff517140a124ac1f380410ee95a0d705` | via CARDS/A-REV1 | verification of D2, V1, C1 |
| `theory/W3-PXN` | `4aebea3bf003f5f3c0c7239a24c824ec2d2aa574` | via CARDS/T38_STATEMENT | LH-iid (p ≫ n) candidate, Prop Q/W, D2 instance |
| `theory/W4-SHARE` | `0d3f3fe581b72186c0c9bffe701950044cc7a464` | via CARDS | route (b2) envelope remark |
| `theory/A-REV1` | `26815e841f25cd472a20f8ea251c00b4ffab3e37` | `REVIEW.md` | cross-family verdicts quoted for Thm 3(iv), Thm 4, Thm 5 |
| `theory/A-REV2` | `09dc2307b3b4a133765877239d5cd2149c25cd89` | `REVIEW.md` | cross-family verdicts quoted for Thm 1, Thm 2(ii),(iv), Thm 3(i) |
| `theory/campaign` | `b8811e2ee4652b9405092190491529289ee8ec73` | `HQ/SR_AUDIT.md`, task specs W6-FIXREV1/2 | SR holds in engine (HQ read); LS0 decision (conditional on O-LS0) |
| main repository | (this branch) | `Docs/Theory/theorems/00_COMMON.md`, `Docs/Methodology/METHODOLOGY_v3.md` (via 00_COMMON) | §1 setting and notation; assumption codes |

Seen but **not** used for any status (in progress or only scripts, no final report when this was finalised):

| Branch | Head SHA | Note |
|---|---|---|
| `theory/W6-FIXREV1` | `7e58127` (full: see `git rev-parse origin/theory/W6-FIXREV1`) | scripts/checks only; no `T38_STATEMENT.md`, `T38_PROOF.md`, `REPORT.md` |
| `theory/W6-FIXREV2` | `d213e7b` | `NOTES.md` and scripts only; no `STATEMENTS.md`, `REPORT.md` |
| `theory/W5-LOCKBOOK` | `f3c037da66e2e294ab9bfe350a8817316a0aae69` | AUDIT.md (GUARD/OUT/SR code audit), STATEMENTS.tex in progress; cited as "in progress, unreviewed" |
| `theory/W5-VPGD` | `194e12c22616643f58eca93f74f237a32b46b3dc` | `REFEREE.md` "draft verdicts" on Theorem W: no ERROR, four minor GAPs; quoted as a draft, status not upgraded |
| `theory/W5-VMASK` | `c3e1b733f7eda2c7266a606df8ec274effe128e3` | independent core + sanity checks, no verdict |
| `theory/O-LS0` | `247170905d9dff734242ec9ea65a185fa1f1146a` | scripts only, no results; LS0's data check is therefore still pending |

(Final head SHAs are re-fetched at the end of the run; if a branch moved after this table was written, the table in the commit message is authoritative.)

## Pending edits when W6-FIXREV1 / W6-FIXREV2 land (the `.tex` has NOT incorporated them)

1. **Theorem 5 (T38)**: replace the statement with W6-FIXREV1's `T38_STATEMENT.md`. Expected changes from A-REV1: route (b1′) gets pilot rate margins; route (b2) gets an
   eligible-set interface plus the binomial bound; execution/output qualifications matching Lemma RO and GUARD; E3(ii) restored with q < 1; check every downstream use of E3.
2. **Theorem 3(iv) (Theorem B)**: Proposition U's classification (or charging to η) is changing (A-REV1 §3.1 counterexamples); the exact definitions of c_*, v, η must be re-read.
   CE1's broad wording must be replaced by the narrow, correct wording with A-REV1 §5's explicit sequence.
3. **Theorem 1 (T03♯), Theorem 2(ii), Lemma U, Theorem 3(i)**: apply W6-FIXREV2's `STATEMENTS.md` (tie-aware TD′ definition; limit constant 0.51/c_* in EXP′ (the `.tex` omits the
   limiting constant so there is nothing to correct); Lemma U with the budgeted quantifier and the μ ∈ span(X_T) condition for the matching lower bound).
4. Re-check Lemma 0 (the `.tex` states only the inclusion that A-REV2 says survives), and the "iff" in the definition of TD′_P (the `.tex` states strict separation as sufficient only).

## Judgement calls and discrepancies (for HQ)

- **Theorem 5 scope.** The theorem contains (0), (a), (b1), (b1-LH), (c). Routes (b1′) and (b2) are in a *Remark* ("not part of the theorem") because A-REV1 classifies the supplied
  T38(b)-R as a GAP for those routes. Route (b1) alone is the one A-REV1 verified as a direct implication; W4-T38FULL's Lemma M / LS-score / LH-LAT / Theorem b1 were not in A-REV1's
  scope and carry only the same-family referee status. The `.tex` says so in the status comments.
- **Ŝ⁺ notation.** Kept the source's Ŝ⁺ / 𝒮⁺ (LS0 included); Theorem 4 is stated for Ŝ (W2-BOOK) with a remark that the same inequality holds for Ŝ⁺ (W4-T38FULL (0)).
- **LS0 approval.** HQ's record is "APPROVED by Felipe (2026-11-02), conditional on O-LS0's data check". The `.tex` defines LS0 as part of the method and flags the condition.
- **Disagreement between F-REFINE files.** ARCHITECTURE §7(iv) says the start-rate factor is "≥ 10³ at B = 14 for n ≤ 10⁴"; CARDS Card 3 gives 2^B√(log n/n) = 2.7·10³ (n = 200), 497 (n = 10⁴), 61 (n = 10⁶).
  The `.tex` uses the CARDS numbers (stated product) and notes the conflict in a comment.
- **EXP′ constant.** W1-EXP prints κ → 0.52/c_*; A-REV2 §5.1 shows the actual limit is 0.51/c_*. The `.tex` states κ_EXP without the limit.
- **Prop 2 (f).** W2-BOOK `PROOF.md` states `α e^η P(𝒜) + ε`; `STATEMENTS.tex` states the weaker `α e^η + ε`; the weaker form is used.
- **Theorem 1 label.** T02(i♯) and T02(ii♯) are typeset as Lemmas feeding Theorem 1 (their sources call them theorems). No hypotheses were changed.
- **Compilation.** `pdflatex` exists; compile was attempted through `owls_run -j 1`, which refused repeatedly while 3 other jobs ran (policy rule 3: do not bypass). See `compile_status.txt`.
