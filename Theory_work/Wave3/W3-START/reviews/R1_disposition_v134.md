# Council round R1 — what version 1.3.4 does with the ten non-blocking issues (lead, 2026-11-11)

Supplement to `reviews/R1_disposition.md` (which records that nothing was applied to the content frozen for R1).
HQ ordered a round R2 on the merged tree with these edits applied (HQ_DECISIONS, 2026-11-12 UTC). Locations are in
the content frozen for R2.

| # | seat | issue | action in v1.3.4 | where |
|---|---|---|---|---|
| S1 / O3 | both | `ASSUMPTION_MAP.md` kept an early body with appended correction sections | applied: rewritten as one map of the final statement; the corrections are integrated in the body | `ASSUMPTION_MAP.md` (whole file) |
| S2 | sol | `numerics/RESULTS.md`: two phrases stronger than a finite simulation supports | applied: observational wording at both places (the second further corrected on SC5 finding 1) | `numerics/RESULTS.md:94-96`, `:130-133` |
| S3 | sol | (N1) abbreviates the exact-order consequence without κ_V > ½ | applied | `STATEMENT.md:317` |
| O1 | opus | Setting F also allows any A > 0 where C-GROW has A ≥ 1 | applied: "with s₀ ≥ 0 and any fixed A > 0 allowed" | `STATEMENT.md:65-68` |
| O2 | opus | F4 and example F-2 become informative only for very large n (tail budget of the F4 levels below 1 only for log n > 256); said in the numerics report, not in the statement or the report | **not applied.** Owner's standing rule: every result of the project is asymptotic, and the size of n at which a bound becomes informative is not presented as a limitation of a theorem. F4 and F-2 are asymptotic statements and are proved as such. The arithmetic fact stays recorded where it is an observation | `numerics/lemmas/RESULTS_LEMMAS.md:28` |
| O4 | opus | Lemma L3.3 displays e^{2κ_E+1} while the (B-L) row has e^{2κ_E+o(1)} | applied: L3.3 displays e^{2κ_E+ς_n} (≤ e^{2κ_E+1}); c_L of L3.4 unchanged | `lemmas/L3_LEAK.md:53-55` |
| O5 | opus | the code pin named `main` at a commit that has since advanced | applied: "the CORE tree as of commit 72785fe" | `STATEMENT.md:46-47` |
| O6 | opus | summaries write the Gaussian-row rate without the factor (s₀ + 1) | applied: "for some constant C" | `STATEMENT.md:29`, `REPORT.md:27` |
| O7 | opus | `citecheck.py` writes into the repository | applied: optional output-path argument | `citecheck.py:14-18`, `:66-69` |

The diff v1.3.3 → v1.3.4 was checked by an independent reviewer: `reviews/SC5_diff_check_sol.md` (EDITORIAL ONLY WITH
CHANGES, 2 MINOR, both applied: `reviews/SC5_disposition.md`). Also changed in the same step, by PROTOCOL rule 15 as
amended: `reviews/INPUTS.txt` no longer lists wave documents or the registry table.
