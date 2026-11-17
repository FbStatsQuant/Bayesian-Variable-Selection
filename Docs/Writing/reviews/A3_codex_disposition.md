# Disposition of A3_codex_fidelity.md (Sol, 2026-11-16): 2 C, 5 S, 5 F, 0 E; all 12 confirmed against v1/the ledger and fixed

- C01: "for a fixed κ > 0" restored in Thm A.12 (v1 sec5_delivery.tex:303).
- C02: "b_n > 0" restored in Thm A.7 (v1 sec4_distribution.tex:150).
- S01: the leakage sentence after Thm A.9 now begins "keep the other assumptions of Theorem A.9" (v1 :103).
- S02: Table 1 row 5 and the Result 5 In words carry the size restriction min(K−1, p/2).
- S03: "expected posterior miss" in Table 1 row 5 and the Result 5 In words.
- S04: the abstract, Table 1 row 4 and the §6 In words/Why carry the indicator/event formulation and "no claim about how likely that event is".
- S05: the screening counts are attributed to the equicorrelation designs ρ ∈ {0.5, 0.7}, p ≥ 2.5n, s₀ ∈ {4, 8}.
- F01: §2.2 local search: move cap, final scan, certification flag as in v1; capped searches with an improving neighbour stop uncertified.
- F02: Table 1 footnote a (bridge pending) on Results 1, 3, 4 and 5.
- F03: Table 1 row 5 status: the exact order uses the fixed-design expectation bound and has its status.
- F04: §2.3: FAC is a contingent design run at p = 10⁴ only.
- F05: relative and log error named in the §6 In words and Why.
Diff of the fixes: .rc_tmp/a3_fix_diff.patch (as-read text in .rc_tmp/a3_as_read_*). C findings present, so a diff-only re-check by a fresh Opus reader (WD8).
