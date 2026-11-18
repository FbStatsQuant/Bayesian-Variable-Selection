# CW reviewer (Claude Work, Opus 5.5 xhigh), round 2 on PROOF_v2 — reply from the task result (clientRequestId T03-review-CW-r2)

**Verdict: verified.** No fatal findings and no gaps. All eight round-1 findings are resolved (F2 only partly, which the change log does not claim to fix). Four new exposition findings. Renames done mechanically and correctly; the proof still proves STATEMENT.md from exactly its hypotheses.

Packet read: STATEMENT.md, PROOF_v2.tex, PROOF_v2.pdf (pp. 2, 5–7, 9 compared with the .tex), CHANGES_v1_to_v2.md, REPORT_FORMAT.md. Nothing else opened.

## A. Changes
1. Renames — every remaining `w` (lines 35, 39, 49, 69, 131, 133, 134, 139, 141, 259, 269, 293, 393) is the prior weight; y_c identities re-checked (score identity max error 4.4e-15; ‖y_c‖² − N s_y² = 0); υ_n only in Lemma 11 / Prop 12(a); every ν still ν; Υ_n consistent. Verified.
2. Plan typo — verified.
3. n₀ uniformity — δ_n, υ_n, ε_n, q_n depend on the design only through m_n and are nondecreasing; dominated by sequences in (s₀, A, φ₀, σ², M, n); ε̄_n → 0 since C_m log³n/N → 0; BM-∞ remark correct; small omission R2-3. Verified.
4. Lemma 7(a) — algebra redone; exponent −s²; lower tail e^{−t²/(4d)}; exact tail / e^{−x} ≤ 0.50 on a grid; 7(b) closed form and Γ bound correct. Verified.
5. §7 scope and tightness facts — verified.
6. (ii) every data set — verified.
7. (iii) direct bound — verified.

## B. Round-1 findings
F1 resolved; F2 partly (M family remains, R2-2); F3–F7 resolved; F8 resolved apart from R2-3.

## C. Full re-check
Lemmas 1–15, Definition 8, Proposition 12, Steps 0–1, (i)–(v) re-verified; constants: C* bounds G4 noise; L* ≥ 4C* for Lemma 14; L*/32 ≥ s₀(A+1)+2 gives κ_n ≤ e^{ρ_n}n^{−2}; (1−1/n)M* ≥ L* for n ≥ 2; j* controls the |J′| > j* tail. Numerical checks (one seed): M_S = h(YYᵀ) error 6e-14; Lemma 4 in 200 cases; Lemma 5(b) p < 40; scalar inequalities from n = 5 / n = 4; Lemma 11 chain at n = 400, p = 12, s₀ = 2: max(lhs − rhs) = −0.004; Lemma 13 first inequality: max(lhs − rhs) = −1.40.

## D. Findings (all exposition, all verified)
- **R2-1** (Lemma 11, Prop 12(a)): υ_n looks like ν = a₀ + n/2 in the same lines; distinguishable but close.
- **R2-2** (throughout; Remark 16): M family overlap remains (M_S, M, M*, M_n), and Remark 16 reuses M; U vs 𝒰 remains. Unambiguous in context.
- **R2-3** (§1 line 49): "s₀ ≤ K for n ≥ n₀" reads as sequence-dependent but is uniform (s₀ ≤ p always, so s₀ ≤ K iff n ≥ 2s₀). No conclusion depends on it.
- **R2-4** (§7 fact 2): "posterior masses bounded below" can be misread as "bounded from below"; meaning clear.

**Overall verdict: verified.**
