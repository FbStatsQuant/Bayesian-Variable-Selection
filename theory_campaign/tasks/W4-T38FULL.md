# W4-T38FULL: Assemble the main theorem T38, paper-ready, from the verified campaign results

Fetch and read these branches (`git fetch origin <branch>`; folders `theory_campaign/<ID>/`):
- **Wave 1:** W1-T38E (composition T38(b)-R, routes D2 and E3/LS0, Lemmas A/B/S), W1-T37R (refined T37 = Theorem A, TD′), W1-T24G (Theorem B = restated T24), W1-EXP (EXP′ Thm 1; unconditional favourable regime Thm 2/6; CL(L) Thm 3/4; LH family Thm 5), W1-T03R (T03♯).
- **Verifiers:** W2-VT24G (Lemma F′ repair, B1′/B2′), W2-VT03R (threshold correction R1, Prop. W), W3-VT37R (POS repair R1, R2–R6), W3-VT38E (D2 constant r*, C1 confirmed, the LS0 score-event caveat, reporting gaps), W3-VEXP (finite-n EXP′ certificate R1, iid-LH repair R3, the |ψ| < ρ boundary).
- **If already pushed:** W2-PREM, W3-PGD, W3-PXN, W2-T26, W2-BOOK.

**Goal:** one consolidated, internally consistent statement and proof of **T38**, the paper's main theorem, using only verified pieces with every repair applied:
- **(a) Favourable regime:** EXP′ (now a theorem) + T22(iii) + T11(iii).
- **(b) Masked regime:**
  - (b1) the LS0 route, with the refined T37 (Theorem A with POS) and TD′ named as an input;
  - (b1′) route D2, with no method change, for one-flip masking;
  - (b2) Gibbs-path repair via Theorem B, conditional on SHARE/LT, which stays named as open.
- **(c) Cost.**

Use the liminf form. Keep the regime split explicit. Name every hypothesis; for each, say whether it is PROVED, PROVED-UNDER, or an open input. Then:
1. Write `T38_STATEMENT.md`: the theorem as it would appear in the paper (main text), plus a one-page dependency map from inputs to sources (locked proof, or campaign branch and claim), each with its verification status.
2. Write `T38_PROOF.md`: the full proof, citing the sources' proofs by label rather than copying them, with every repair incorporated.
3. List the method-change dependencies, LS0 in particular, including the implementation caveat that LS0 must emit its centre as a score event. List what the paper can claim **without** LS0.
4. Produce the confidence card and a list of what remains open, ranked by importance for the paper.

**Deliverable:** `theory_campaign/W4-T38FULL/REPORT.md` + `T38_STATEMENT.md` + `T38_PROOF.md`.
