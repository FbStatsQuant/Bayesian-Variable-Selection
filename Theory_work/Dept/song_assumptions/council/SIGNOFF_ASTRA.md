# ASTRA senior sign-off · TH-SONG-ASSUMPTIONS · 3ee24ea9

**SIGN-OFF WITH FIXES.** Completeness **8.5/10**, generality and naturalness **9/10**, owner Q&A readiness **8/10**. The population margin can be stated before sampling for general designs. Its capped coefficient has a short proof once W3 includes the second Gaussian bound below. TS-b and TD′ remain targets.

## Stage 1 findings

- C-1 — RESOLVED. C = 1 is a normalization, 121 is a sensitivity setting, and the single-rival price and summed class bound are distinguished.
- C-2 — PARTLY. E9b uses the raw-centred mean, selected deletions and four-design zero-slack diagnostics are identified, but D4 and the final proof-path summary overstate the U2a check.
- C-3 — RESOLVED. TS-a gives predictorwise screening on the common localization event. TM-a0-inc gives inclusion under second moments alone.
- C-4 — PARTLY. Candidate dimension, conditioning and summability are explicit. Uniformity must apply to both versions of the unconditional bound.
- C-5 — RESOLVED. The SL map includes the singleton-tail, floor-free alternative and the detectable-signal rate analogue.
- C-6 — RESOLVED. The E1/E7 summaries identify MPM recovery, the predictive summary and the selected-subset variance diagnostic.
- C-7 — PARTLY. The package gives the pairwise boundary expansion and posterior liminf. The canonical spec claims equality, and the refined margin still quantifies over infeasible classes.

## Stage 1 assumption rows

- A-GL — RESOLVED. The Gaussian conditional law is independent of the design family.
- A-SPARSE — PARTLY. Bounded support is general. The optional empty-support forward extension remains outside the stated targets.
- A-DIM — RESOLVED. The polynomial envelope has a free fixed exponent.
- A-DIM′ — PARTLY. The catalogue separates the regime from its proof budget. The dossier still identifies them.
- A-SUBG — PARTLY. The varying-level window is preserved. Every fixed multiple of log n is stronger than the single window needed at one fixed level.
- A-NEC — RESOLVED on the floor and duplicate counterexample. The same window qualification applies.
- A-BS — RESOLVED. Coordinate effects are standardized in noise units.
- A-BS′ — RESOLVED. The recorded bounded-variance, vanishing-energy pair is distinguished from the open bounded-variance-only target.
- A-MARGIN-H — PARTLY. Both screening forms are present. The fixed-level infimum needs its omission restriction explicitly.
- A-MARGIN-U — PARTLY. U1/U2a/U2b, deterministic Q_n, slack loss in special case (ii), C-i and the sufficient beta-min implication in C-ii are sound on the common feasible range. W1 and W2 hold. W3 and the orthogonal gloss need the edits below.
- A-MIS(iii) — PARTLY. Conditional Gaussian deconvolution gives the stated primitive representation, including zero extra variance. The unconditional qualifier needs the C-4 edit.
- A-MOM — RESOLVED. A fixed law, full candidate rank and finitely many underfits yield the positive risk gap whenever underfits exist. Score moments enter for exclusion.

## Required edits

1. **W3 and proof path §3.3 step 3.** With G = binom(p−s,m), intersect W3 with the simultaneous direct bound −〈v_S,g〉 ≤ √(2[log G + l_n]) by the same union bound. Take the minimum before applying W2 to the capped sample coefficient. The printed uncapped chord can exceed 1 by a fixed amount at leakage above 3/4.
2. **C-ii, all copies.** Label the coordinatewise orthogonal display sufficient. Exact U1 requires n Σ_{j∈D} β_j² Var(x_j) ≥ 2(1+η)σ²Pr_n(d) for each nonempty D. The displayed logarithm upper-bounds the average coded refund.
3. **Converse, spec §2.** Give Φ(−c) as the limit for the specified rival beating T and a liminf lower bound for posterior mass at most ½, as Definitions §4.2 already does. For the local expansion explicitly require Pr_n(1)=O(log n) and fixed-support relative error O_P(n⁻¹ᐟ²), supplied for instance by DIM and relative SUBG on T.
4. **Sieve, Assumptions §2 refined form.** Replace m ≤ J with 0 ≤ m ≤ p−s and s−d+m ≤ min(K,J), retaining B_Dm > 0. Use the same feasibility convention in U2 and C-i.
5. **TM-a/TM-b, all copies.** Require common constants and a common validity threshold on admissible candidate sets in both unconditional cases. Then add P(C inadmissible), which vanishes identically for almost-sure admissibility.
6. **TS-a fixed-level remark, all copies.** Take the infimum over j ∉ S as well as |S| ≤ min(K,J). Including T makes the stated infimum zero.
7. **Windows and TD′, Definitions §§4–4.1 and dossier A-DIM′.** Describe every fixed c log n as sufficient across fixed levels. Delete the “i.e.” identifying the product budget with little-o. At fixed M, log p ∼ a√n for small a > 0 separates them.
8. **Evidence, D4 and Assumptions §6 item 7.** Restrict the U2a equality to all 1,023 deletions with at most two of the five tested proxies. Across copies, qualify the endpoint leakage formula by its conditioning set and require a uniform bound with max ϑ log p → 0 before invoking special case (ii). Even for geometric decay, L_n → ∞ alone need not give ρ^{2L_n} log p → 0.
9. **Dossier, A-MARGIN-U items 4 and 6.** Report the tabulated no-credit minimum 2.4889 in place of “exact” 2.489. At fallback the coefficient is 1 and the width allowance is √(2 log G).
10. **Generality.** Keep the historical 121 parenthesis in E9b evidence alone. Reframe D4's question around boundary signals and move its simulation result to Defence (b). The mathematical premises themselves require neither AR(1) nor any suite-specific constant.
11. **Worked cases and A-SPARSE-C defence.** Attribute bounded projection support to the Gaussian chain's separation by nearest retained neighbours. Local covariance dependence alone need not yield sparse regression. In the equicorrelation example Q_n=T is admissible even with positive leakage, and the formula describes the equal-loading one-factor case.
12. **Definitions §4.2, MARGIN* remark.** Describe U2a as charging every base the full deletion price. The earlier M1 lets inside proxies pay for entry, as the spec's weaker-variant remark explains.

The cutoff m̄_d leaves a negative log-odds budget for larger feasible k since d(A+½)−k/2 < 0. The truncated containing-model sum and coded mixed-odds argument are still proof obligations. This sign-off covers their formulation.
