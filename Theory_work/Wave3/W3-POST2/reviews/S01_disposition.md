# S01 (exhaustive sweep, gpt-6.1-sol high, fresh) — disposition

17 findings: 0 FATAL / 2 MAJOR / 13 MINOR / 2 NIT. Reviewer's overall assessment: no fatal defect in A1, A2, B, C, D(a),
D(b), E after re-deriving their changed steps; corrections needed in numerics and sharpness wording. **All 17 fixed**
(numerics re-run: `numerics/post2_checks.py` v2 → `post2_checks_out.txt`, full re-run, seeded).

| # | finding | action |
|---|---|---|
| 1 MAJOR | bounded reference cost presented as necessary | ASSUMPTION_MAP v1.3: "sufficient for this proof's uniform bound; not necessary"; new numerics N6b growing-cost case (Θ″ 0.1 → 0.0125 with B = n − 1); B Remarks 7–8. |
| 2 MAJOR | numerical Occam weights omitted 2^{(j−d)/2} | Weights a_J = 2^{j/2}(eC_A j log n/max(d,1))^{d/2} implemented; outputs regenerated; N2 now 85 → 15 (amplified 2.7·10⁴ → 45); ASSUMPTION_MAP updated. |
| 3 MINOR | numerical Occam domain | m♯_n computed; range j ≤ min(m♯_n, p − s₀); assertion K = p (all comparison unions in Ω at p = 10) documented in the code. |
| 4 MINOR | N1 ID margin over a subfamily | `Post.margins`: full minima of Δ_S and L_S over all S ∈ Ω, S₀ ⊄ S, |S∖S₀| ≤ j₀; reported as IDmin/IDMmin; "ID holds" claims now quote these. |
| 5 MINOR | N4 not an (ID; c) instance | c relabelled "coefficient scale"; achieved full (ID)/(ID^M) minima reported. |
| 6 MINOR | gap between (OS) and A2 misdescribed | STATEMENT A2 paragraph and A_occam Remark (2): four-part decomposition (weights; feasible j > m♯_n; infeasible unions; amplified tail). |
| 7 MINOR | span membership ⇏ bounded determinant ratio | A_occam Remark (3) restricted to bounded minimal-norm representations, with the reviewer's counterexample noted. |
| 8 MINOR | N7 "attained" overclaim | D4 Remark 2 and ASSUMPTION_MAP: "consistent with"; only D(a)'s mean-part scale argued analytically (χ²_{s₀} spread). |
| 9 MINOR | map restored universal margin necessity | ASSUMPTION_MAP: "smaller margins work here; no universal improved constant proved". |
| 10 MINOR | LB domain dropped in sharpness record | Domain 1 ≤ s₀ < p, s₀ + 1 ≤ K stated; p = s₀ caveat. |
| 11 MINOR | effective-rank remark vague | B Remark 6: costs √f(λ) by eigenvalue scale (0, O(1/n), n^{−a}, fixed). |
| 12 MINOR | "posterior lives on" needs ω_n → ∞ | B Remark 4 restated with ω_n → ∞ and the integer cutoff min(K, ⌈·⌉ + 1). |
| 13 MINOR | boundary record incomplete | Added N8 ((F₀) boundary: rate holds as λ_min(R_{S₀}) → 0), N6b (mean ⊥ col X; growing cost); non-Gaussian and growing-p tests recorded as not undertaken, with reasons. |
| 14 MINOR | A2 slack only as median | min slack and violation count printed: 0 violations in all N1/N2/N8 runs; min slack ≥ 0.0035. |
| 15 MINOR | where Gaussianity enters B | ASSUMPTION_MAP POST2-GP corrected (lem:num needs only a positive f₀). |
| 16 NIT | "A → 0" | "fixed p, so log p/log n → 0; not probing growing p". |
| 17 NIT | nonexistent `A2` command | Usage line now lists N1 N2 N4 N5 N6 N6b N7 N8. |
