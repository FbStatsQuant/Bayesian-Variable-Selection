# Council C2 disposition (lead)

Seat A (gpt-6-astra high, `C2_council_astra.md`): 8.3; G1/G2/G3 FAIL, G4/G5/G6 PASS; 0 FATAL / 1 MAJOR / 1 MINOR / 3 NIT.
Seat B (Opus 5.5 high, `C2_council_opus.md`): 8.8; all gates PASS; 0 FATAL / 0 MAJOR / 1 MINOR / 7 NIT.
Round C2: NOT PASSED (seat A gates). Both seats: formal results (Theorem 1 items 1–7, Corollary 1R, Lemmas 1a/1a′,
Proposition LB) correct; all 22 C1 findings fixed (seat B), C1 reconciliation table in seat A §"Numerical, literature…".

| # | Finding | Action |
|---|---|---|
| A-F1 MAJOR | REPORT states LB without its domain (false at p = s₀; δ ≈ 6.5·10⁻¹⁰ at n = 20) | FIXED: domain "1 ≤ s₀ < p, s₀ + 1 ≤ K (a feasible one-variable extension exists)" attached at every REPORT/ASSUMPTION_MAP occurrence, incl. the expectation-rate remark; counterexample reproduced in `numerics/lb_domain.py` → `lb_domain_out.txt` (same value). STATEMENT item 7 and the lemma were already correct. |
| A-F2 MINOR | NH14 Condition 4.5 parameters omitted | FIXED: "for some ν < δ and κ < (K − 1)δ/2 (ν > 0 in m_n(ν))". |
| A-F3 NIT | E5 sketch remainder | FIXED: relative log weight written with O_P(√log n) + O(1); coefficients labelled deterministic leading coefficients. |
| A-F4 NIT | negative m in R_m | FIXED: q_k := 0 outside 0..K, sums from max(m+1, 0) (STATEMENT §0, L1a′). |
| A-F5 NIT | stale code comments | FIXED (comments only; outputs unchanged). |
| B-F1 MINOR | R02 called cross-family | FIXED: R01 cross-family, R02 same family as the lead. |
| B-N1 | item 7 before item 6 | FIXED: reordered. |
| B-N2 | |supp θ*| = s₀ on the events of item 6 | FIXED. |
| B-N3 | POST-E row vs Song–Liang Condition 2 | FIXED: "only analogous". |
| B-N4 | broken table row | FIXED: row joined; unescaped pipes escaped (checked by script). |
| B-N5 | E5 sketch re-derived by seat B | RECORDED in the row (status word unchanged). |
| B-N6 | LB check record | FIXED: check record naming C2 seats added; status word unchanged. |
| B-N7 | REPORT number only in reviewer scratch; minimax remark uncited | FIXED: `numerics/lb_domain.py`; Wainwright (2009) cited, marked "recalled, not re-read". |
