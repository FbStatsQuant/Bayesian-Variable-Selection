# W5-FAVIID: A 2^B-free favourable-regime start rate on iid designs with the actual partition, and T26's (P1) on study-like designs

**Paper role:** Thm 2(iii), Thm 5(a), Thm 6 (P1). The locked and W1-EXP favourable rates carry 2^B (≥ 16,384 at
B = 14), which makes them numerically vacuous below n ≈ 10⁹; and the in-sample favourable regime for the study's iid
designs S1/S3/S4/S6 is a GAP (the packing depends on the noise column). W3-PXN's Beta-truncation method (exact Beta
laws + Lemma Tr) removes 2^B on LH-iid and should transfer to the favourable case.

Fetch and read: `origin/theory/W3-PXN` (PROOF §§2–6: Lemma B, Lemma Tr, P1, P3; REPORT §8 "Sharpened T22(iii)"),
`origin/theory/W3-VEXP` (REPORT rows 23–24; REPAIRS R3 and §D dilution; `scripts/study_check.py`), `origin/theory/W1-EXP`
(PROOF §§1–2: Thm 1, Prop 2.1/2.2, Thm 2, Thm 6; §4.3), `origin/theory/W2-T26` (REPORT §4.1–4.2; PROOF §1:
Theorem A/B; the (P1) premise), locked T22(iii) (`Docs/Theory/proofs/`, `LOCKED_PROOFS.md`), 00_COMMON,
`v3_blocks.h`, `Scripts/Data_generators/`.

Goals, in order:
1. **Theorem (favourable, iid rows, fixed partition).** Rows iid N(0, Σ) with Σ block-diagonal over groups, one
   truth per group, p ≤ n^A, fixed nonzero θ, and the event P_n = {the v3 partition equals a fixed union of groups}
   (W3-VEXP R3's device). On P_n, prove 1 − π₀(S₀) = O_P(√(log n/n)) **without** the 2^B factor, by PXN's method at
   the reference S₀ (U_h° = S₀ ∩ C_h; the visible-group computation). State the constant's dependence on B and g.
2. **P(P_n) → 1 for the study's group structure** (groups of 5, B = 14, two groups per block): is there a fixed
   partition the engine converges to? If the packing of whole groups into blocks is noise-dependent, prove the
   rate on the event "every block is a union of whole groups" (W3-VEXP found this holds in every design at
   n = 200) and show that the bound is uniform over the finitely many such packings. This closes the partition–noise
   decoupling GAP without a leave-one-column-out lemma.
3. **Dilution threshold.** From W3-VEXP's Prop D and W3-PXN's Prop W, derive the finite-n threshold n*(design) at
   which the start becomes favourable (median π₀(S₀) > ½) for S1/S3/S4/S6 at p ∈ {500, 1000}, scale ∈ {0.5, 1},
   as a function of (θ, v_T, p, s₀); check it against exact π₀ computations at n ∈ {200, 400, 800, 1600, 3200}.
4. **Consequences.** State the resulting versions of Thm 5(a) and Thm 6's (P1) for the study-like family with the
   realised grid T_n, and give the first n at which (T_n+1)Δ_n < 1 with T_n from the method's pilot rule (simulate
   the pilot's grid, not T^max).
5. Numerics at p ≤ 30 exact (convolution of block tables), and at p = 500 by the same convolution (the start law is
   block-wise, so exact π₀ is cheap).

Deliverable: `theory_campaign/W5-FAVIID/REPORT.md` + PROOF.md + scripts + results + confidence card.

---

_Source: theory_campaign/F-REFINE/NEXT_TASKS.md on branch theory/F-REFINE (Fable, 2026-11-02). Read F-REFINE's CARDS.md and ARCHITECTURE.md first: `git fetch origin theory/F-REFINE`._
