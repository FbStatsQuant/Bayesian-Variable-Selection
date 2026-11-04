# RULINGS.md — the lead's rulings on the judge's changes (PROPOSAL_v2 → PROPOSAL_v3)

Lead: Fable 5.1 (high). Date: 2026-10-20. Inputs reviewed: council/PROPOSAL_v1.md, review/PROPOSAL_v2.md, review/CHANGES_v1_to_v2.md, review/OBJECTIONS.md + OBJECTIONS_ADDENDUM.md, council/OBJECTIONS_REPLY.md, judge/r1_JUDGE_PHASE1.md, judge/JUDGE_ORDERS.md, judge/sol1/RESULTS.md, judge/sol2/RESULTS.md, judge/PROPOSAL_v3.md, judge/CHANGES_v2_to_v3.md. Numbers below are the entries of judge/CHANGES_v2_to_v3.md. "Adopt" means the v3 text becomes the final text; "adopt with modification" states the modification; "reject" states the reason. Everything remains a conjecture about METHODOLOGY_v3.0 (SHA-256 93043758…8019c).

Lead's own checks of the judge's new mathematics (hand, not Sol): the Hölder interpolation of T16 clause 4 (odds against S₀ under q_φ ≤ R₀^{1−φ}R₁^{φ}) is correct; L-RC's reward bound |μ_j^W − PIP_j| ≤ π(W^c) is correct; T18's stability constant (B+3)u_π follows from reversibility; T14-H's corrected iid intensity N_e(T+L+5)/(p√n) agrees with the lead's own recomputation and with J7; the T15 proxy design (correlations 0.6 or 0.65) satisfies the eigenvalue floor and beats the true singletons in population fit.

## Rulings, one line per judge change

1. Adopt. Conditional headlines are the honest form for a conjecture list.
2. Adopt. The exclusivity claims that were not derivations are gone; the two derivable ones (DUP(a) vs SE/NIS; ORTH vs p > n) stay.
3. Adopt with modification: BM-C's constant M_* = 2L_*+1 is a *candidate* from the audited transfer (J1, provisional); the theorem file states BM-C and BM-∞ as alternative hypotheses and tells the proving run it may replace M_*.
4. Adopt.
5. Adopt. The mixed-endpoint form is the only one the proof can use.
6. Adopt.
7. Adopt (with the modification of 3).
8. Adopt. Screening gets its own comparison.
9. Adopt. A3 to core.
10. Adopt.
11. Adopt.
12. Adopt. "Known-size, known-noise benchmark"; no minimax wording.
13. Adopt.
14. Adopt.
15. Adopt.
16. Adopt.
17. Adopt.
18. Adopt. L-LED and T14-D merged; one ledger.
19. Adopt.
20. Adopt.
21. Adopt. NUM gives no coverage for implemented evidence.
22. Adopt.
23. Adopt.
24. Adopt.
25. Adopt.
26. Adopt. Constant 2/(1−ε*) with the endpoint term (J6).
27. Adopt.
28. Adopt. The linear L-OCC bound replaces the square-root bound.
29. Adopt.
30. Adopt. Vacuity claims that rested on upper bounds are withdrawn.
31. Adopt.
32. Adopt as an optional, explicitly unvalidated judge conjecture (T12).
33. Adopt.
34. Adopt.
35. Adopt. The factor-n error is corrected.
36. Adopt.
37. Adopt.
38. Adopt. T15(i′) withdrawn (J3 contradicts it).
39. Adopt.
40. Adopt.
41. Adopt. EXP is the named proof obligation.
42. Adopt (lead checked the Hölder step).
43. Adopt.
44. Adopt. Recording-prefix form.
45. Adopt.
46. Adopt. Conservative constant 1/(s₀+d+B+2)!; the lead notes that, since L → ∞, any fixed positive constant suffices for the asymptotic conclusion, so the loss of the slot constant costs nothing asymptotically.
47. Adopt.
48. Adopt. RET+OCC rate withdrawn (J10); PW2 recorded as research target.
49. Adopt.
50. Adopt.
51. Adopt.
52. Adopt.
53. Adopt.
54. Adopt.
55. Adopt.
56. Adopt. R-T20(iii) remains an open construction, no theorem file.
57. Adopt.
58. Adopt with modification: the φ*_n temperature-threshold necessary condition is removed from T21-E's statement, and recorded in DROPPED.md as returnable once an interference-controlled repair argument exists.
59. Adopt.
60. Adopt.
61. Adopt with modification (reject the reduction to questions only): T21-X is kept as an OPTIONAL conjecture file in the T18′-conditional form the judge itself states (G, R, SE, BM, EX-A, EX-S, CAL, SR, LK_d, EXIT_d, GAIN_d, a past-measurable eligible pilot particle and executed pilot terminal rounds ⇒ P(S₀ ∈ 𝒮_cal) → 1, hence no MISS-E/MISS-H instance with S₀ ∈ 𝓜). The BOCC-only form and the universal contrapositive go to DROPPED.md. Reason: a conjecture with a stated route and named hardest steps is what this architecture must carry for proof.md; the judge's demotion of the BOCC-only implication is right and is adopted.
62. Adopt.
63. Adopt. Simultaneous certificates (J7).
64. Adopt.
65. Adopt.
66. Adopt.
67. Adopt.
68. Adopt. Branch-dependent statuses (J9).
69. Adopt. Mass-qualified STIFF; range bound (D14); cutoff withdrawn.
70. Adopt.
71. Adopt.
72. Adopt.
73. Adopt (the judge's self-correction agrees with J8 and with the lead's reading).
74. Adopt.
75. Adopt (recorded as open).
76. Adopt (recorded as open; EXP).
77. Adopt (recorded as open).
78. Adopt (recorded as open).

## Lead's own final changes

L1. T21-X: kept as an optional conjecture in the T18′-conditional form (ruling 61).
L2. Theorem package layout: because the definitions are long and shared, `theorems/00_COMMON.md` holds the exact setting, notation, budgets, regimes and the full assumption inventory; every `theorems/T<k>_<name>.md` restates the definitions it needs in compact form and names the inventory codes it uses, and must be given to proof.md together with 00_COMMON.md and the method file (by path). This is the self-containment rule applied without copying the method 36 times.
L3. Files for statements with provable content only: R-T13 (finite-comparison pilot limit) and T23-R (mass-qualified bisection obstruction) get files at rank secondary and optional respectively; R-T20(i) and R-T20(iii) are remarks (recorded in THEOREM_MAP.md and DROPPED.md), not theorem files.
L4. Clause-level ranks are kept exactly as the judge set them (e.g., T15 semantics core / ORTH secondary / COH optional; T16 deterministic core / statistical secondary; T18 abstract core / instances secondary; T19 BW2 secondary / actual-run rate open). The file's headline rank is the highest clause rank; THEOREM_MAP.md lists the clause ranks.
L5. Confidence labels, sources and "provisional evidence (Sol check Jk)" labels are carried verbatim from v3 into the theorem files and THEORY.tex.
L6. Recommendations to Felipe (not adopted) are the judge's consolidated list of ten, unchanged; the lead adds none.
L7. Fable calls in the judge step: none (count stays at 15).

## Outcome

Adopted: 78 of 78 judge changes (75 as written, 3 with the modifications stated: 3/7, 58, 61). Rejected: none outright; one reduction (61, T21-X to questions only) partially reversed. Final counts: 36 theorem files (22 core, 10 secondary, 4 optional by headline rank; see THEOREM_MAP.md), 2 remarks without files, plus DROPPED.md.
