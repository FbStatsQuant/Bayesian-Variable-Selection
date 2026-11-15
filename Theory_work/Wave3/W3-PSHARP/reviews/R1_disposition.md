# Council R1 disposition (MANIFEST ce522b1f…bb6a; seat sol 7.6 gates FAIL; seat opus 9.0 gates PASS) — NOT PASSED

Both seats re-derived the four lemma files and found the mathematics and the locked STATEMENT sound (sol G1, G2 PASS;
opus all gates PASS). Seat sol failed G3–G6 on one reporting defect (M1). One fix round follows (brief: at most one).

| finding | disposition |
|---|---|
| sol M1 MAJOR — REPORT §1(b), §4 and the registry block of Claim B dropped the hypotheses s₀ ≤ min(K − 1, p/2) (consistency and rate necessities) and s₀/p → 0 (critical-scale cap); as written false (p = s₀ + 1: π(S₀) → 1 with s₀ ~ √n; p = 2s₀: limit e^{−λ/3}) | **Applied** with the reviewer's corrections: consequences introduced "for sequences with s₀ ≤ min(K − 1, p/2)"; "with s₀/p → 0" on the cap; §4 row qualified; registry conclusion/rate/scope split (inequality for 0 ≤ s₀ ≤ K − 1; consequences under s₀ ≤ p/2; rate c(p, s₀)/√n). A sentence added on why the restriction is needed (the reviewer's two examples). STATEMENT and proofs needed no change (they carried the hypotheses). |
| sol m1 MINOR — REPORT §3 called the orthogonal DP output "odds" without the size truncation | **Applied**: "odds summed over \|S\| ≤ min(K, s₀ + 60) (s₀ + 80 in E2): a lower bound … before quadrature error … not a certified enclosure". |
| sol m2 / opus MINOR-2 — "π(\|S\| > cutoff) = 1.000 for n ≥ 100" holds for the b = 3 rows only | **Applied**: b = 3 medians; b = 1 and b = 0.5 medians 0.95 and 0.47 stated; "far below the theorem's signal constant". |
| opus MINOR-1 — registry label A:COEF-REP = NECESSARY is inflated: Proposition C shows a failed removal; the bound ‖θ‖² ≤ nM′ itself is weakenable (Lemma 1a″; reviewer's near-collinear example) | **Applied**: FAILED-REMOVAL in the registry block and REPORT §4; "necessary in kind" replaced in REPORT §1(c) and STATEMENT (wording; v1.2.2). |
| opus NIT-1 — STATEMENT "the rate r_n can survive a slowly growing s₀" is an unproved existence remark | **Applied**: "The obstruction does not apply when log p = o(log n); no claim is made there." |
| opus NIT-2 — garbled phrase in ASSUMPTION_MAP row (E), (C) | **Applied** (reviewer's sentence). |
| opus NIT-3 — `b_check.py` F1 header printed "equality iff orthogonal" though the iff is not tested | **Applied**: header and docstring corrected; script re-run in full (`b_check_out.txt` matches the final script; numbers unchanged). |
| opus NIT-4 — notation clashes r_n(x) (A §3) and P (C §3 Step 4) | **Applied**: e_n(x); E_𝒳. |
| opus NIT-5 — rate (s₀+1)/(2√n) for B holds only as s₀/p → 0 | **Applied** (registry, ASSUMPTION_MAP): c(p, s₀)/√n. |
| opus NIT-6 — 𝔇_n is admissible only once n ≥ C_b(1 + σ*²/b̄²)(log n)²; n₀ = 200 never binds | **Applied**: sentence added to the design paragraph of STATEMENT §4. |

Nature of the changes: REPORT (summary, numerics description, registry block), ASSUMPTION_MAP, three wording points in
STATEMENT (no claim item changed), two symbol renames in proofs, one script header. Round R2: new manifest, both seats
blind first reads, plus a separate reconciliation reviewer on the R1 findings (rule 15).
