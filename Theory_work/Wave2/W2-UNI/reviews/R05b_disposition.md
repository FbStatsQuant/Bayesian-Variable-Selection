# R05b — disposition of the protocol exhaustive sweep (fresh Codex gpt-6-astra, high)

Reviewer reply verbatim: `reviews/R05b_sweep_astra.md`. Brief: STATEMENT v1.1.2, all lemmas, numerics, citecheck, REPORT draft;
no LOG/CHECKPOINT/PLAN/prior reviews. Verdict: VERIFIED-WITH-AMENDMENTS at the mathematical-proof level; no FATAL or MAJOR
defect; LOCL, U-LOC references/atoms, entropy union, empty-set extension, sample coupling and the uniform o(√log n)
remainder not broken; UNI-0's zero/subunit-distance replacements accepted. Counts: FATAL 0, MAJOR 0, MINOR 10, NIT 3.
All 13 fixed (2026-11-09, ~15:13–15:24 CST). Markers [R05b-#].

| # | Class | Disposition |
|---|---|---|
| 1 | MINOR | FIXED. REPORT headline: PLR "+ LSF ⇒ P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; unconditional consistency additionally uses F-UNI's delivery premises"; UNI-0 likewise with the explicit intersection, then its separate delivery conclusion. (STATEMENT/L5 were already correct, as the reviewer notes.) |
| 2 | MINOR | FIXED. REPORT §6: "controls every subset and is not equivalent to average pervasiveness — neither condition implies the other" (reviewer's two counterexamples accepted). |
| 3 | MINOR | FIXED. REPORT §6 example list: GMRFs only with fixed-range or uniformly exponentially decaying precision on a polynomial-growth geometry and uniform spectral bounds ("bounded spectrum alone is not enough"); AR/ARMA with roots uniformly outside the unit circle; fixed-bandwidth banded with uniform spectral bounds. |
| 4 | MINOR | FIXED. C_corollaries rows 6 and 7 reworded per the reviewer (LOC-BF not contained in UNI-0 as a whole; overlapping subclasses may be; polynomial decay alone does not imply LOC_M though the classes overlap). Same correction in STATEMENT §6 Not-claimed ("Ψ outside LOC_M, e.g. with only polynomial decay …") → STATEMENT v1.1.3 (wording of the not-claimed list only). |
| 5 | MINOR | FIXED. n4 rerun with the ported COMPLETE-scan local search (bc.local_search) for all 120 runs; the screened ls_fast is kept only as a labelled comparison (agreed with the complete search on final set and path in 120/120). Docstring and L2 §12 updated. |
| 6 | MINOR | FIXED. n4 now reports "sampled truth-deletion margin" and "sampled TL margin (deletions + all truth-removing swaps)"; both positive in 120/120 (swaps binding in 116/120). L2 §12 uses the swap-inclusive margin. |
| 7 | MINOR | FIXED. lattice_sup_h is computed over S₀ ⊆ T ⊆ Q_lat only (asserted); path statistics reported separately (out-of-lattice path states: 4, all in PC2 n = 2000 seed 3). |
| 8 | MINOR | FIXED. All aggregate counts generated programmatically into `numerics/n4_r2_pseudo_summary.txt`; R = 3 sandwich 117/120 (the "95/100" was wrong). |
| 9 | MINOR | FIXED. citecheck resolver made deterministic (prefix → same-line abbreviation → previous-line abbreviation → this ticket; bare lemma names → lemmas/); existence never used to choose; no basename fallback; the rule used is printed per citation. Eight citations that previously resolved only through fallback were made explicit in L2_k0 (LOC2 L1_toolkit, L2_NAR; Wave2/HQ_AUDIT). |
| 10 | MINOR | FIXED. The 12-substring status list is replaced by automatic extraction of every quoted status (61 occurrences, multi-line quotes included), attributed to its source ticket and required verbatim with a word boundary (so "VERIFIED" ≠ "VERIFIED-WITH-AMENDMENTS"); attachment to the specific result is part of the manual audit, which lists every occurrence. |
| 11 | NIT | FIXED. C_corollaries row 8 quotes "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)" in full. |
| 12 | NIT | FIXED at report freeze: REPORT names STATEMENT v1.1.3 and the final citecheck totals with the checker version. |
| 13 | NIT | FIXED. n2: −expm1 form; docstring states the one-sided direction only in exact arithmetic; rerun — n2_metric_out.txt unchanged at printed precision. |
