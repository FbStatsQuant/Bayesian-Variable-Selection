# T38-RECORD: REPORT

Run T38-RECORD (Opus 5.5), 2026-11-02, branch `theory/T38-RECORD`, from `origin/theory/campaign` @ 581e4ba. Spec:
`theory/W8-SYNTH · SYNTHESIS.md §8 task 6`. This was text work only. No mathematics was recomputed, and no new
mathematics was written. The registry is built by a text-processing script.

## 1. Deliverables

| File | What it is |
|---|---|
| `T38_STATEMENT.md` | **Statement of record v3 for Theorem 5 (T38).** It has a change log against v2 (W6-FIXREV1), v1 (W4-T38FULL) and v0 (W1-T38E §7); Part I is the theorem; Part II the dependency map with SF and XF columns; Part III 16 marked conflicts; Part IV the decisions it depends on |
| `REGISTRY_v2.md` | Claims registry rebuilt from S-REGISTRY (3d88da6). It covers 431 named results (up from 337) and 49 flagged sub-claims, and adds sections on data facts, label renames, Lean, F-REFEREE objections and decisions |
| `LOCKABLE_v2.md` | Lockable candidates under S-REGISTRY's strict rule: **55** strict (up from 48). It adds Theorem 5 at a glance and the referees' own LOCKABLE lists |
| `registry_data.py` | verbatim copy of S-REGISTRY's rows |
| `registry_v2_data.py` | the overlay: annotations, new rows, and the A-REV5–A-REV9 verdicts |
| `build_registry_v2.py` | the builder: `PYTHONDONTWRITEBYTECODE=1 python3 -I theory_campaign/T38-RECORD/build_registry_v2.py` |

## 2. What changed in Theorem 5 (headline)

1. **LS0 is part of the method.** The approval is in effect: O-LS0 found 0/2,394 HPM changes. The statement names two
   variants, "the method" (with LS0) and "v3 as run" (without LS0), and every part says which variant it covers.
2. **The masked LS0 route is now cross-family verified.**
   - A-REV8 VERIFIED Theorem b1, Lemma LS-score (discovery), Lemma M and Prop. LH-LAT, and the joint exact-Gram (b1-LH)
     consistency with LS0.
   - (b1-LH) therefore has author PROVED, SF VERIFIED (W5-VMASK) and XF VERIFIED, and enters LOCKABLE_v2 as strict.
   - Two wording repairs come from the referees, applied verbatim and attributed:
     - the LS-score move count becomes max{Φ − 1, 0} (A-REV8 E1);
     - the side clause "iid draws miss S₀ when c ≥ 2, p → ∞" now requires n^{1−c/2}p^{−c}log²n → 0. A-REV5 rates the
       old clause ERROR and A-REV8 rates it GAP (⚑ III.13).
3. **A no-LS0 masked theorem now exists on an explicit LH subfamily.** A-REV7 VERIFIED two results.
   - W5-B2ENV Theorem B2-LH, conditional on STAB-LH, every c. A-REV7 supplied an analytic STAB certificate and a concrete
     growing-p subfamily (g = 9, c = 2, ρ = 0.4, ψ = 0.2). Both are **Astra-authored** and need a Claude verification.
   - Cor. D2-LH, c = 1, for qualitative consistency (its stated rate is a GAP).

   v3 adds them as parts **(b2-LH)** and **(b1′-LH)**, each with its author status word unchanged (PROVED-UNDER). This
   meets W8-SYNTH's condition for a no-LS0 headline. **The headline choice stays with HQ and Felipe** (Part IV, D2).
4. **What A-REV7 refuted.**
   - Unrestricted LH locking: C2 fails for allowed parameters.
   - F-SHARE's "DOM is void for c = 1" when visible groups are present.
   - F2 is a GAP.
   - BG3 is VERIFIED, and LH-lock is VERIFIED as a conditional fixed-p implication only; at fixed p production enumerates.
   - GU does not, on its own, give a no-LS0 route.
5. **Spine.** Remark 6 and the "Why it matters" paragraph say **moving off the start is needed, not tempering**. This
   follows `theory/E-SPINE` and W7-SEP. Three of v3's moves each suffice on LH: LS0's search, the pilot's first Gibbs
   stage, and the bridge plus terminal rounds under confinement.
6. **Cost.**
   - (c) is PROVED-UNDER T32(i). T32(i) is PROVED by W5-LOCKBOOK and re-counted by W7-SEC; v2's "CONJECTURE" was stale.
   - The displayed log² rate carries an A-REV6 GAP: there is a calibration log³ factor. Polynomiality survives.
   - A-REV5 asks that the T32(i) qualification be kept, and it is.
7. **GUARD.** The transfer holds for statistical outputs only, not for run diagnostics (A-REV8 E2, A-REV4, A-REV6). A-REV5
   and A-REV8 read the guard code and found it supports the stop-only coupling in that scope.
8. **p ≫ n.** (b1-LH-iid) is stated separately, with its XF GAP (A-REV3, A-REV6, A-REV8). It is not in the headline.

## 3. Registry rebuild

- **New rows.**
  - O-BGIBBS final: BG2, BG1′, LH-rate, BG3, LH-lock and the composite.
  - F-SHARE REPORT: F1, L1.2, F3, L3.1–3.4, PK, F2, §4, C4.3, F1′, F2-iid and the composite.
  - W7-SEP: SEP(A)–(E), BASIN, GU, GU-1, GU-2, Cor. GU-LH, GU-iid, GU with nulls, and the no-LS0 conjecture.
  - W7-PART: Theorems A–C, L1–L3, CE1–CE3, κ, and the open pairing question.
  - W7-SEC: T05, T33, error_bound, and the T32 fp addendum.
  - O-STAGES, O-DILUTE, F-SIGMA, and the statement of record (`T38-v3`).
- **Annotated rows.**
  - O-CERT rows carry O-VCERT's same-family verdicts.
  - T32(i) and Lemma 0(b) carry W7-SEC and S-ELS.
  - O-BGIBBS's earlier "final run OPEN" row is marked superseded on LH.
  - W3-PGD and W5-FAVIID point to their final REPORTs.
- **Cross-family verdicts from A-REV5 to A-REV9**, which landed during this run, are entered.
  - A re-review never raises an earlier adverse code on the original text. The repair rows (W6F1-*, W6F2-*) carry
    A-REV5's verdicts, so for example `PropU` stays ERROR while `W6F1-PropU′` is VERIFIED.
  - Astra-authored arguments are separate rows with author status REFEREE: the STAB certificate, the subfamily, the LH-lock
    completion, and A-REV6's candidate repairs.
- **Data facts** (§D2), from S-ELS and O-LS0.
- **Lean** (§G): L-LEAN is final, and Astra's round 2 is GREEN. This supersedes W8-SYNTH §7.
- **F-REFEREE objections** (§H), re-tagged: M2, M3 and M8 are now largely answerable.
- **Label renames** (§F): 26 proposals for W8-SYNTH §4.15. They are proposals only.
- **Conflicts** (§A2): 26 in all, of which 8 are new. The new ones cover T32(i), SEP(E), the no-LS0 question, the O-CERT
  §4 illustration, O-STAGES W′ versus O-WSTAB, common σ², the c = 2 clause, and GU's scope.
- **New strict lockables:** `LS-score`, `LemmaM`, `LH-LAT`, `T38-b1-LH` (W5-VMASK + A-REV8), and `OCERT-LemmaM`,
  `OCERT-C3`, `OCERT-C4` (O-VCERT + A-REV9). The *Qualification* column must travel with each.
- **Not upgraded, deliberately.**
  - T32(i)'s XF entry: A-REV6 wrote "supported", with no verdict word, so it is left at none.
  - LH-lock stays a PROOF SKETCH, although it is now XF VERIFIED as a conditional implication.
  - D2-LH and B2-LH stay PROVED-UNDER.

## 4. What I did not do (spec items outside this run's deliverable)

- **S-PAPER source comments and disclosure items 5–6.** `theory/E-SPINE` (dd0ec8a, cec1680) has already amended S-PAPER's
  `theory_section.tex`, according to its `AMENDMENTS_20261102.md §3`. I did not edit another branch.
- **The label renames are proposals** (REGISTRY_v2 §F). They are applied in T38_STATEMENT only as bracketed aliases.
- The A-REV5 REV1/REV2 checks, A-REV6's SHARE/WEIGHTS/PARTITION files, and A-REV9's two helper files were read through
  their parent REVIEW.md only.
- `theory/API-*` (AUDIT, FAVIID, POS, RESID) appeared after the cut-off and are listed in coverage, unread. API-FAVIID
  amends the W5-FAVIID report and should enter the next rebuild.
- The O-WSTAB rows were not mapped to A-REV9's W(a)–(f) verdicts. A-REV9 VERIFIED W(a)–(f) under H-ORTH, and W′ for the
  ideal grid.

## 5. For HQ: what needs a decision or a run

1. **D2, the headline.**
   - Option A: (b1-LH) with LS0. It is fully XF verified.
   - Option B: (b2-LH), no LS0. It is XF verified conditional on STAB-LH, and STAB-LH is discharged on an explicit
     subfamily by an Astra-authored certificate.
   - **Recommended before choosing B:** a short Claude verification of A-REV7 §4, covering the analytic STAB certificate,
     the subfamily and the η_n correction.
2. **D1, the output convention**: still open.
3. **Small repairs to write into the source branches** (all referee-supplied):
   - the LS-score move count;
   - the (b1-LH) growth condition;
   - the GUARD statistical scope;
   - the T32(c) log³ rate;
   - the W6-FIXREV2 Lemma U probability arrow and Theorem A cap;
   - F-REFINE Cards 3(i) and 4;
   - W3-PXN P7's r* and Beta shape.
4. **Still open after every review:**
   - the p ≫ n route (P6/P7);
   - DELIV outside LH;
   - T32(i) XF verdict word;
   - ORTH joint family;
   - masked Ẑ/PIP accuracy.

## 6. Heads used

These come from the final fetch:
- O-LS0 02348e2; W6-FIXREV1 a7833f3; W4-T38FULL a0f9cb5; W5-VMASK 4e41b97; W3-PXN 4aebea3;
- O-BGIBBS 55679ee; F-SHARE 13bc665; W5-B2ENV 053511d; W7-SEP 858004e; S-REGISTRY 3d88da6;
- A-REV5 189770c; A-REV6 02d6a4a; A-REV7 70eadf3; A-REV8 6417192; A-REV9 bbadda3;
- E-SPINE cec1680; L-LEAN cfa78ed.

Every other head is in `REGISTRY_v2.md §E`.
