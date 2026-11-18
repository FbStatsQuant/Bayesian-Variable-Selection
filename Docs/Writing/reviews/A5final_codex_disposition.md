# Disposition of A5final_codex_fidelity.md (gpt-6.2-sol, 2026-11-17): 19 findings (2C 9S 6F 2E); 18 confirmed and fixed, 1 rejected

- 01 (E) **Rejected:** "(SG)" is the display label of the key SGR, used consistently everywhere; it differs only from the brief's wording.
- 02 (F) Stage 1 restores the stops: invalid inputs give no model; a constant response or no retained predictor gives the empty model and no estimates.
- 03 (F) The lower bound is stated as "exceeds log Z jointly with completion with probability at most 0.05".
- 04 (C) Theorem 2's conventions follow W3-D3 §0: raw labels; PIP_j := 0 for removed columns; π(S₀) := 0 if S₀ ∉ Ω; a point mass at ∅ if no column is retained.
- 05 (S) The mixtures sentence adds "with BBᵀ a correlation matrix" (ExSG).
- 06 (S) Remark Thm2X states its conditions: Gaussian rows with any positive variances; the floor on the correlation matrix; energy ≤ fixed × σ²; n min Σ_jj β_j²/(σ² log n) → ∞.
- 07 (F) "Display (14), with Assumption (d), carries over …" (the antecedent is made explicit).
- 08 (C) Visibility for AR is now qualified "with the true predictors spread apart (as in our designs)" in §5.3.3; Remark 11(ii) adds that visibility must still hold (spread placement, or Remark VIS). Counterexample accepted (adjacent coefficients 1, −2 in AR(1) 0.5).
- 09 (S) A nonempty list; the exact-branch qualification is moved into the corollary's main clause.
- 10 (F) Status: "recorded on the card as conditional on IMPL-LIST …, a check that concerns the identification of those fields with the quantities above".
- 11 (S) Result 4 In words adds the budget conditions; §1 says "whether or not the conditions of Result 3 hold".
- 12 (F) §6: Result 5 is a statement given the frozen calibration, on the event that it succeeds, about the potential uninterrupted estimate; no claim conditional on completion.
- 13 (S) Result 6 In words: p ≥ 2 and the size restriction for (a); (b) a lower bound in expectation.
- 14 (S) The exceptions now include Result 5 (no design or model assumption) and Result 4's budget in place of (DIM).
- 15 (E) The bibliography records the arXiv versions read (with suffixes); NH14 notes arXiv:1405.6545v1 for its page.
- 16 (F) "binary features whose success probability tends to zero".
- 17 (S) The riboflavin failure clause is replaced by "whether … is covered is being determined" (HOLD).
- 18 (S) The NL gloss gives the n^{-1/2} rate, the local conditioning and the locality conditions.
- 19 (S) §6 assigns conventions per result, and notes that under (C2⁺) every run produces output.
C findings 04 and 08 → diff-only Opus re-check (WD8).
