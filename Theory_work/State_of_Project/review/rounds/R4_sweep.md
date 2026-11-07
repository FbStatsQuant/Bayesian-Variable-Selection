# Pre-round-5 G4 sweep (Sol gpt-6.1-sol, high; self-described as partial) and the lead's dispositions

| # | Location | Finding (type) | Disposition |
|---|---|---|---|
| 1–4 | 01_problem.tex:9,11 | Proposal citations said to be off (e) | **Rejected (objection).** The proposal file contains 10 form-feed page breaks (`\x0c`); tools that split on them (e.g. Python `splitlines`) shift line numbers. Line numbers in this document follow newline counting (`cat -n`, `sed -n`), the convention used everywhere: line 184 is "with little mass on S = {j, ℓ}. Thus naive merging can destroy joint posterior uncertainty."; 410–413 is §8.4 Risk 4; 499–501 is §13.1. Verify with `sed -n '184p;410,413p;499,501p' Theory_work/Old_Projects/New_BVS_Headquarters/inputs/Local_to_Global_draft.txt`. |
| 5 | 04_theory.tex (TH04 plain) | reported PIPs vs store-restricted quantities (a) | Fixed: "every store-restricted PIP PIP^𝒯_j and every bounded store summary π_𝒯(h) … these are store quantities, not the particle-based reported PIPs". |
| 6 | 04_theory.tex:34, TH08 plain, registry TH08.d | polynomial work lacked "shipped budgets, any permitted polynomial R′" (a) | Fixed at all three (TLF:407). |
| 7 | 05_history.tex:164 | stale Prop D depth formula (b,f) | Fixed: final card's N_e(T+L+4)m (TLF:407); registry formula marked as an earlier form. |
| 8 | 04b_supplement.tex:556 | "Prop P(i)" numbering (c) | Fixed: "Seat A's clause (i) (R1_A:223) = METH-AUDIT Prop P(ii) (PROOFS:126-128)". |
| 9 | 04b_supplement.tex:556 | "biased at fixed N" stronger than "in general" (a) | Fixed: "differs from the posterior value 'in general' … retains any single-island bias for every R (Prop P(i))". |
| 10 | registry TH03 regime | (e) needs block orthogonality (a) | Fixed: "(a)-(d) any admissible X; (e) block orthogonality; (f) LH under G". |
| 11 | registry TH02.b2 | ratio of 1+χ², domain conditions (a) | Fixed. |
| 12 | registry TH02.b6 | missing (b6) premises (a) | Fixed (TLF:158 premises). |
| 13 | registry TH07.cp | missing 2⁻⁶⁰ ≤ h/2 and grid-success premises (a) | Fixed. |
| 14 | registry TH07.d | missing exact-frontier/initial/terminal log-odds qualifiers (a) | Fixed. |
| 15 | registry TH11 regime | preservation needs every group ≤ B (a) | Fixed. |
| 16 | 06_open_and_plan.tex:71 | IC7 card vs failed-clause distinction (a) | Fixed (LP-FOUND.md:112 wording). |
| 17 | 06 priority table | FR10/FR11 assigned to wave 3 (a,f) | Fixed: FR05 alone in wave 3; FR10/FR11 "deferred: future work for paper 1 (no HQ)" (FUTURE_WORK.md:3). |
| 18 | 06 ENG15; registry ENG15 | "code status not recorded" vs AMENDMENT_HQ_02.md:15 "not yet coded" (f) | Fixed: NOT CODED, citing AMENDMENT_HQ_02.md:15. |
| 19 | 05_history.tex:247; 06:90 | PXN Prop. Q is a sketch (a) | Fixed at both: "by PXN Prop. Q (a sketch)". |
| 20 | 03_empirics.tex:166 | 501/507 not on cited line (e) | Fixed: added EVIDENCE_L.md:243-258 (the p = 30, c = 0.5 table). |

Build after fixes: 236 pages; check.py 0 errors; 1,681 citations resolve; coverage 100%.
