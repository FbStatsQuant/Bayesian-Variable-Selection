# F1 fidelity review — disposition (writer, 2026-11-08 ~23:40 CST)

Reviewer: Codex gpt-6.1-sol, reasoningEffort high (fresh delegate; brief = files only). Reply verbatim: `F1_fidelity_sol.md`.
Verdict FAITHFUL-WITH-FIXES, FATAL 0 / MAJOR 5 / MINOR 5. Lemma CAP: VERIFIED-WITH-AMENDMENTS. All ten findings ACCEPTED and applied
with the reviewer's replacement text (lightly adapted to the chapter's macros); no objection recorded.

| # | sev | finding | disposition | where |
|---|---|---|---|---|
| 1 | MAJOR | Lemma Z dropped Gram floor and fixed-design scope | applied verbatim; added "general growing-p null case not claimed" | sections/s3_posterior.tex (Thm F paragraph) |
| 2 | MAJOR | GEN (H2a), (H2c) NL_avg not written out; SEP convention | (H2a), leakage family, NL_avg with E_{T,l}, h_n, conventions written out; GROW (G3a) made explicit; SEP max = 0 if V = [p] | sections/s5_hpm.tex §GEN, §GROW |
| 3 | MAJOR | GROW NA/TL stated as non-improvement | strict-inequality definitions of NA, TL inserted before (C1) | sections/s5_hpm.tex §GROW |
| 4 | MAJOR | GROW (C2)/(C3) lost antecedents; δ₀, η, C_Q fixedness | antecedents restored verbatim from C-GROW STATEMENT (C2)/(C3); fixed C_Q, deterministic M_n, fixed η ∈ [0, η_A), fixed δ₀ ∈ (0,1) | sections/s5_hpm.tex §GROW |
| 5 | MAJOR | AR(1) instances: ρ range, fixed θ*, σ², noise model of (c), piecewise relevance set | full (a) hypotheses and v2.1 piecewise construction; (c) noise model, scaling, partition, premises | sections/s5_hpm.tex instances |
| 6 | MINOR | CAP: integer caps, coupling, skipped branches | setting and lemma restricted to finite integer caps with explicit coupling; branch bookkeeping (exact, schedule_limit) added to proof of (b) | sections/s7_impl.tex |
| 7 | MINOR | GEN transfer reversed an implication | replaced by reviewer's wording | sections/s7_impl.tex |
| 8 | MINOR | global finite-n disclaimer too broad | replaced: "Selection consistency is asymptotic" with the finite-n scope of deterministic/sampler/delivery statements kept | sections/s8_scope.tex |
| 9 | MINOR | PXN constants and quantifier of (R) undefined | definitions of s, ψ̄, q_R, t*, I(t; r) inserted; (R) quantifier "for every fixed C > 0, n ≥ max{n₁, n₀(A, C, ρ, ψ̄)}" | sections/s5_hpm.tex §PXN |
| 10 | MINOR | N1 localisation event unnamed; Cor E lacked qualifier | E_r and the localised meaning defined before N1; Cor E prefixed accordingly | sections/s4_sampler.tex |

Lemma CAP status in the chapter: "PROVED (by this seat)" + this cross-family check (VERIFIED-WITH-AMENDMENTS, applied); not councilled.
Not re-reviewed after the fixes (one fidelity check was the brief); the fixes are the reviewer's own replacement texts.
