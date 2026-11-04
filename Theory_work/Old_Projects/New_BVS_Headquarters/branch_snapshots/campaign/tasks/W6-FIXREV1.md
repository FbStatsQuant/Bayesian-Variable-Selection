# W6-FIXREV1: Apply the cross-family (Astra) review A-REV1 to the repair and T38 package

Read `theory_campaign/A-REV1/REVIEW.md` on branch `theory/A-REV1` (GPT-6 Astra, a cross-family review). It found:
- **Theorem B:** VERIFIED after the F′ repair.
- **Corrected D2:** VERIFIED under its operational idealisation.
- **Proposition U:** ERROR in two bookkeeping shortcuts (§3.1 gives counterexamples):
  - independence moves can remove a truth without raising V or leaving the family;
  - an extra-for-extra swap need not stay in the phase-1 family.
- **Lemma S:** ERROR in the "attained by two-level weights" sentence on its full domain (it needs f > 1 − e).
- **E3(ii):** ERROR (it drops q < 1 from the locked T22(i-a); p = 2 counterexample).
- **Lemma U:** ERROR in the limiting constant (0.51/c_E, not 0.52/c_E).
- **CE1, broad wording:** GAP.
- **NL0 quantifier exchange (sup of a sum vs sum of sups):** GAP.
- **T38(b)-R:** GAP (rates for route b1′, an eligible-set interface for b2, execution qualifications). §7 gives a complete conditional repair.

Sources to repair:
- theory/W1-T24G and theory/W2-VT24G (Theorem B, Prop U, Lemmas F/F′/P, CE1);
- theory/W2-PREM (Lemma U, NL0);
- theory/W1-T38E and theory/W3-VT38E (Lemma S, D2, E3);
- theory/W4-T38FULL (assembled T38).

**Goal:** produce ONE corrected, consolidated package that incorporates every A-REV1 finding.
1. **Corrected Proposition U.** Repair both shortcuts: change the classification, or change the charging to η. Re-check that Theorem B's inequality, which A-REV1 says survives because it uses the full §0 definition, is unaffected, and say exactly why.
2. **Corrected Lemma S** (state the domain of attainment) and **E3(ii)** (restore q < 1, and check every downstream use of E3, including in W4-T38FULL and W3-PXN).
3. **Lemma U:** the corrected constant. **NL0:** the correct quantifier form and what it costs downstream (W2-PREM).
4. **T38 statement and proof:** rewrite them following A-REV1 §7 (pilot rates for b1′; the eligible-set interface plus the binomial bound for b2; execution and output qualifications matching W2-BOOK's Lemma RO / GUARD and W4-T38FULL's potential-uninterrupted-run form). Produce `T38_STATEMENT.md` and `T38_PROOF.md`, superseding W4-T38FULL's versions, with a change log.
5. **CE1:** the narrow, correct wording, with A-REV1 §5's explicit sequence.
6. For each item, state whether you agree with A-REV1. If you disagree, give a precise counter-argument; adjudication comes later.

**Deliverable:** `theory_campaign/W6-FIXREV1/REPORT.md` (a change log table: item | A-REV1 verdict | fix | downstream effects), plus the corrected T38 files and a confidence card.
